#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Converter class module for PyAACGUI2. 
Work as background thread in cooperation with GUI part. 
2014.2.23
'''

import multiprocessing
import tempfile as t
import threading

import wx

import core

__author__ = 'Joker Qyou'


class Converter(threading.Thread):
    '''
    Converter thread class for PyAACGUI2
    '''
    def __init__(self, 
        caller = None, 
        callback = None, 
        queue = [], 
        tempdir = t.gettempdir(), 
        bitrate = 512000, 
        delorigin = False, 
        encoder = None, 
        tagger = None):
        '''
        Init function
        Args:
            callback <func> Set the UI thread
            queue <set | list> Set queue to process
            tempdir <string> Set temporary file directory
            bitrate <int> Set bitrate
            delorigin <bool> Delete original files after conversion
            encoder <string> Set path to encoder executable
            tagger <string> Set path to tagger executable
        Notice:
            All args with `None ` as default value are not optional.
            Missing one of these args will raise RuntimeError.
        '''
        if not caller or \
            not callback or \
            not encoder or \
            not tagger:
            raise RuntimeError
        else:
            threading.Thread.__init__(self)
            self.CALLER = caller
            self.CALLBACK = callback
            self.QUEUE = list(queue)
            self.QUEUE.sort()
            self.DONE = []
            self.TEMPDIR = tempdir
            self.BITRATE = bitrate
            self.DELORIGIN = delorigin

            self.ENCODER = encoder
            self.TAGGER = tagger

    def progress(self):
        '''
        Return conversion progress in (done, total) format.
        '''
        return (len(self.DONE), len(self.QUEUE))

    def isDone(self):
        '''
        Return the status of conversion.
        '''
        return True
        # if (len(self.QUEUE) - len(self.DONE)) == 0:
        #     return True
        # else:
        #     return False

    def run(self):
        '''
        Start conversion sub-threads to do the actual work.
        '''
        # Get the maximum threads number according to CPU core count
        CORES = multiprocessing.cpu_count()

        # Start N threads each time and wait for their exiting
        for index in range(0, len(self.QUEUE), CORES):
            threads = []
            for sindex in range(0, CORES):
                findex = index + sindex
                try:
                    fname = self.QUEUE[findex]
                    thread = core.Converter(
                        fpath = fname, 
                        callback = self.CALLBACK, 
                        tempdir = self.TEMPDIR, 
                        index = findex, 
                        delorigin = self.DELORIGIN, 
                        encoder = self.ENCODER, 
                        tagger = self.TAGGER, 
                        bitrate = self.BITRATE
                        )
                    thread.start()
                    threads.append(thread)
                except IndexError, e:
                    pass
            for thread in threads:
                thread.join()
            for thread in threads:
                self.DONE.append(thread.CALL_INDEX)

        wx.CallAfter(self.CALLER.OnConversionDone)
        
