#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Converter class module for PyAACGUI2. 
Work as background thread in cooperation with GUI part. 
2014.2.23
'''

import os
import shutil
import subprocess
import tempfile as t
import threading
import time

import wx

import mediainfo
try:
    from .. import q
except ValueError, e:
    import q

__author__ = 'Joker Qyou'


class Converter(threading.Thread):
    '''
    Converter thread class for PyAACGUI2
    '''
    def __init__(self, 
        caller = None, 
        queue = [], 
        tempdir = t.gettempdir(), 
        bitrate = 512000, 
        delorigin = False):
        threading.Thread.__init__(self)
        self.CALLER = caller
        self.QUEUE = list(queue)
        self.DONE = []
        self.TEMPDIR = tempdir
        self.BITRATE = bitrate
        self.DELORIGIN = delorigin

    def isDone(self):
        '''
        Return the status of conversion.
        '''
        if (len(self.QUEUE) - len(self.DONE)) == 0:
            return True
        else:
            return False

    def convert2Wave(self, fname, dest = None):
        '''
        Convert given file to WAVE format using Unix `mplayer `.
        '''
        if not dest:
            return 1
        else:
            return subprocess.Popen([
                'mplayer', 
                '-vo', 'null', # No video output
                '-ao', 'pcm:file=%s' % dest, 
                fname
                ]).wait()

    def convert2Aac(self, fname, dest = None):
        '''
        Convert given file to AAC format using Nero AAC codec.
        '''
        if not dest:
            return 1
        else:
            # I don't know what's happened here, cause if I use 
            # `subprocess.Popen().wait() ` here, it will 100% raise 
            # core dump. So I use `Popen().poll() ` now. 
            aacProgress = subprocess.Popen([
                'neroAacEnc', 
                '-br', str(self.BITRATE), # Set bitrate
                '-2pass', # Use 2 pass
                '-ignorelength', # Ignore length info in header
                '-lc', # Use LC AAC profile
                '-if', fname, # Set input file
                '-of', dest # Set output file
                ], stdin = subprocess.PIPE)
            while not aacProgress.returncode == 0:
                # Instead of polling at max possible frequency, wait a short 
                # time would lower CPU usage efficiently, and cause nearly 
                # no difference in other ways.
                time.sleep(i.PROCESS_POLL_INTERVAL)
                aacProgress.poll()
            return aacProgress.returncode

    def prepare4TagCmd(self, fname, mediainfo = {}):
        '''
        Prepare for Nero AAC tagging cmdline.
        '''
        tagCmdline = ['neroAacTag', fname]
        for key in mediainfo:
            if mediainfo[key].strip():
                tagCmdline.append(
                    '-meta:%s=%s' % (key, mediainfo[key])
                    )
        return tagCmdline

    def tagAac(self, fname, mediainfo = {}):
        '''
        Tag given file using Nero AAC tag program.
        '''
        if not os.path.exists(fname):
            return 1
        else:
            cmdline = self.prepare4TagCmd(
                fname, 
                mediainfo = mediainfo
                )
            tagProcess =  subprocess.Popen(cmdline)
            while not tagProcess.returncode == 0:
                time.sleep(i.PROCESS_POLL_INTERVAL)
                tagProcess.poll()
            return tagProcess.returncode

    def run(self):
        waveext, aacext = '.wav', '.m4a'
        for item in self.QUEUE:
            current = self.QUEUE.index(item)
            # For non-WAVE files, use Unix `mplayer ` to encode them to WAVE, 
            # then encode using Nero AAC codec and tag the media info. 
            wx.CallAfter(self.CALLER.updateProgress, current)
            if not q.extof(item) == waveext:
                tempFname = os.path.join(
                    self.TEMPDIR, 
                    q.randomstr(20) + waveext
                    )
                if self.convert2Wave(item, dest = tempFname) == 0:
                    destFname = q.dropext(item, baseonly = False) + aacext
                    self.convert2Aac(tempFname, dest = destFname)
                    # This is really important! If tempdir is set to 
                    # `/dev/shm ` and temp file is not deleted, 
                    # sooner or later the user's memory would explode.
                    os.remove(tempFname)
                    # Unix `mediainfo ` program cannot handle file with 
                    # '?' in its name, so we'll have to get a copy of that 
                    # file and rename the copy, or this program will probably 
                    # hang up here.
                    if '?' in item:
                        tempFile4tag = os.path.join(
                            self.TEMPDIR, 
                            q.reformfilename(
                                item, 
                                strict = True, 
                                baseonly = True
                                )
                            )
                        shutil.copy(item, tempFile4tag)
                        minfo = mediainfo.query(tempFile4tag)
                        os.remove(tempFile4tag)
                    else:
                        minfo = mediainfo.query(item)
                    self.tagAac(
                        destFname, 
                        mediainfo = minfo
                        )

                    # Delete original file if DELORIGIN set to `True `
                    if self.DELORIGIN:
                        os.remove(item)
                else:
                    print 'Error occurred during convert2Wave.'
            # For WAVE files, encode directly using Nero AAC codec, and since 
            # WAVE files don't have media info with them, there's no need to 
            # tag them. 
            else:
                destFname = q.dropext(item, baseonly = False) + aacext
                self.convert2Aac(tempFname, dest = destFname)

                # Delete original file if DELORIGIN set to `True `
                if self.DELORIGIN:
                    os.remove(item)

            self.DONE.append(item)
        wx.CallAfter(self.CALLER.OnConversionDone)
        
