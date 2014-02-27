#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Shortcut functions
'''

import os
import random

import wx
import wx.xrc as xrc

__author__ = 'Joker Qyou'


def extof(fpath):
    '''
    Return the extension (with dot) of given file name / file path.
    '''
    return os.path.splitext(fpath)[-1].lower()


def dropext(fpath, baseonly = True):
    '''
    Return the basename of given file without extension.
    Args:
        baseonly <Bool> return only the basename instead of full path
    '''
    if baseonly:
        return os.path.splitext(os.path.basename(fpath))[0]
    else:
        return os.path.splitext(fpath)[0]


def randomstr(length):
    '''
    Generate random string of given length.
    '''
    return ''.join(
        random.sample(
            [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 
            'w', 'x', 'y', 'z', 
            'Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 
            'O', 'N', 'M', 'L', 'K', 'J', 'I', 'H', 'G', 'F', 'E', 
            'D', 'C', 'B', 'A', 
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
            ], length)
        ).replace(' ', '')


def disabletools(ids, parent = None):
    '''
    Disable tools with given ids.
    '''
    if not parent:
        return False
    else:
        try:
            return [parent.EnableTool(xrc.XRCID(id), False) for id in ids]
        except Exception, e:
            raise e


def enabletools(ids, parent = None):
    '''
    Enable tools with given ids.
    '''
    if not parent:
        return False
    else:
        try:
            return [parent.EnableTool(xrc.XRCID(id), True) for id in ids]
        except Exception, e:
            raise e


def rmwiredchars(fname, strict = True):
    '''
    Remove wired characters from given file name.
    This is used to avoid returning empty XML during the subprocess 
    call to Unix `mediainfo ` program.
    '''
    if strict:
        return fname\
            .replace('?', '')\
            .replace('!', '')\
            .replace(';', ' - ')\
            .replace(':', ' - ')\
            .replace(',', ' & ')\
            .replace('*', 'x')
    else:
        return fname.replace('?', '').replace('*', 'x')


def reformfilename(fname, strict = True, baseonly = True):
    '''
    Change file name, use `rmwiredchars ` to remove certain chars.
    '''
    ext = extof(fname)
    originFname = dropext(fname, baseonly = baseonly)
    newFname = rmwiredchars(originFname, strict = strict)
    return newFname + ext


def fileexists(fpath):
    '''
    Detect whether the given file path exists.
    '''
    return os.path.exists(os.path.abspath(fpath)) and \
        os.path.isfile(os.path.abspath(fpath))
