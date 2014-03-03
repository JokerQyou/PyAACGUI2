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
        tagger = None, 
        maxcorenum = multiprocessing.cpu_count()):
        '''
        Init function
        Args:
            caller <wx.Frame> Set the UI thread
            callback <func> Which function to call inside child thread
            queue <set | list> Set queue to process
            tempdir <string> Set temporary file directory
            bitrate <int> Set bitrate
            delorigin <bool> Delete original files after conversion
            encoder <string> Set path to encoder executable
            tagger <string> Set path to tagger executable
            maxcorenum <int> Set max job number
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

            self.MAX_CORE_NUM = maxcorenum

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
        # Start N threads each time and wait for their exiting
        for index in range(0, len(self.QUEUE), self.MAX_CORE_NUM):
            threads = []
            for sindex in range(0, self.MAX_CORE_NUM):
                findex = index + sindex
                try:
                    fname = self.QUEUE[findex]
                    thread = core.Converter(
                        fpath = fname, 
                        callback = self.CALLBACK, 
                        tempdir = self.TEMPDIR, 
                        index = findex, 
                        parent = self, 
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

        wx.CallAfter(self.CALLER.OnConversionDone)
        
