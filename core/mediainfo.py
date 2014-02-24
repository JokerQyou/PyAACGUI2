#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
MediaInfo module for PyAACGUI2.
Requires: Unix `mediainfo ` program
2014.2.23
'''

import os
import xml.etree.ElementTree as eTree
from xml.etree.ElementTree import Element
import subprocess

__author__ = 'Joker Qyou'


# Info container
INFO = {
    'album': '', 
    'artist': '', 
    'title': '', 
    'writer': '', 
    'year': '', 
    'genre': '', 
    'track': '', 
    'totaltracks': '', 
    'comment': '', 
    'composer': ''
}


# Collation between tags returned by Unix `mediainfo ` and tags used by Nero
TAG_COLLATION = {
    'Album': 'album', 
    'Performer': 'artist', 
    'Track_name': 'title', 
    'Album_Performer': 'writer', 
    'Recorded_date': 'year', 
    'Genre': 'genre', 
    'Track_name_Position': 'track', 
    'Track_name_Total': 'totaltracks', 
    'Comment': 'comment', 
    'Composer': 'composer'
}


def _str2info(content):
    '''
    Turn given string content to XML Element, 
    and parse that element to media info container. 
    '''
    # Get info container
    info, _tags = INFO.copy(), None
    _xml = eTree.parse(content)
    _root = _xml.getroot()
    _info = _xml2dict(_root)['File']
    for _dict in _info['track']:
        if _dict.has_key('Complete_name'):
            _tags = _dict
    if _tags:
        for key in _tags:
            if TAG_COLLATION.has_key(key):
                info.update({TAG_COLLATION[key]: _tags[key]})
    return info


def _xml2dict(element):
    '''
    Turn given XML element to Python <dict>.
    Code from: [dingyaguang117]( https://github.com/dingyaguang117 )
    '''
    assert isinstance(element, Element) 
    ret = {}
    for child in list(element):
        # print child.tag, child.text
        if len(child) != 0:
            value = _xml2dict(child)
        else:
            value = child.text
        if child.tag in ret:
            if type(ret[child.tag]) != list:
                ret[child.tag] = [ret[child.tag]]
            ret[child.tag].append(value)
        else:
            ret[child.tag] = value
    return ret


def query(fpath):
    '''
    Get media info of given file in <dict>, using Unix `mediainfo ` program.
    '''
    if not os.path.exists(fpath):
        return INFO
    else:
        process = subprocess.Popen([
            'mediainfo', 
            '--output=xml', 
            fpath], stdout = subprocess.PIPE)
        process.wait()
        return _str2info(process.stdout)

