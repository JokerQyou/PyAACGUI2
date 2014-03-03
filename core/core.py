#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Core class for core module.
This class do the actual conversion work, where as the 
`converter.Converter ` class just exists as a background processor.
2014.3.2
'''

import os
import shutil
import subprocess
import tempfile as t
import threading

import wx

import mediainfo
try:
    from .. import q
except ValueError, e:
    import q


class Converter(threading.Thread):
    '''
    Converter class
    '''
    def __init__(self, 
        fpath = '', 
        callback = None, 
        tempdir = t.gettempdir(), 
        index = 0, 
        parent = None, 
        delorigin = False, 
        encoder = None, 
        tagger = None, 
        bitrate = 512000):
        threading.Thread.__init__(self)
        if not fpath or \
            not type(index) == int or \
            not callback or \
            not parent or \
            not encoder or \
            not tagger:
            raise RuntimeError

        self.CALLBACK = callback
        self.TEMPDIR = tempdir
        self.FILE = fpath
        self.CALL_INDEX = index
        self.PARENT = parent
        self.DELORIGIN = delorigin

        self.ENCODER = encoder
        self.TAGGER = tagger
        self.BITRATE = bitrate


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
            return subprocess.Popen([
                self.ENCODER, 
                '-br', str(self.BITRATE), # Set bitrate
                '-2pass', # Use 2 pass
                '-ignorelength', # Ignore length info in header
                '-lc', # Use LC AAC profile
                '-if', fname, # Set input file
                '-of', dest # Set output file
                ], stdin = subprocess.PIPE).wait()

    def prepare4TagCmd(self, fname, mediainfo = {}):
        '''
        Prepare for Nero AAC tagging cmdline.
        '''
        tagCmdline = [self.TAGGER, fname]
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
            return subprocess.Popen(cmdline).wait()

    def run(self):
        waveext, aacext = '.wav', '.m4a'
        wx.CallAfter(self.CALLBACK, self.FILE, 'Converting')
        if not q.extof(self.FILE) == waveext:
            tempFname = os.path.join(
                self.TEMPDIR, 
                q.randomstr(20) + waveext
                )
            if self.convert2Wave(self.FILE, dest = tempFname) == 0:
                destFname = q.dropext(self.FILE, baseonly = False) + aacext
                self.convert2Aac(tempFname, dest = destFname)
                # This is really important! If tempdir is set to 
                # `/dev/shm ` and temp file is not deleted, 
                # sooner or later the user's memory would explode.
                os.remove(tempFname)
                # Unix `mediainfo ` program cannot handle file with 
                # '?' in its name, so we'll have to get a copy of that 
                # file and rename the copy, or this program will probably 
                # hang up here.
                if q.containwiredchar(self.FILE):
                    tempFile4tag = os.path.join(
                        self.TEMPDIR, 
                        q.reformfilename(
                            self.FILE, 
                            strict = True, 
                            baseonly = True
                            )
                        )
                    shutil.copy(self.FILE, tempFile4tag)
                    minfo = mediainfo.query(tempFile4tag)
                    os.remove(tempFile4tag)
                else:
                    minfo = mediainfo.query(self.FILE)
                self.tagAac(
                    destFname, 
                    mediainfo = minfo
                    )

                # Delete original file if DELORIGIN set to `True `
                if self.DELORIGIN and q.fileexists(destFname):
                    os.remove(self.FILE)
                wx.CallAfter(self.CALLBACK, self.FILE, 'Done')
                self.PARENT.DONE.append(self.CALL_INDEX)
            else:
                wx.CallAfter(self.CALLBACK, self.FILE, 'Error')
        # For WAVE files, encode directly using Nero AAC codec, and since 
        # WAVE files don't have media info with them, there's no need to 
        # tag them. 
        else:
            destFname = q.dropext(self.FILE, baseonly = False) + aacext
            self.convert2Aac(tempFname, dest = destFname)

            # Delete original file if DELORIGIN set to `True `
            if self.DELORIGIN and q.fileexists(destFname):
                os.remove(self.FILE)
            wx.CallAfter(self.CALLBACK, self.FILE, 'Done')
            self.PARENT.DONE.append(self.CALL_INDEX)
