#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Some information
'''

__author__ = 'Joker Qyou'

APP_NAME = u'PyAACGUI2'
APP_VENDOR = u'Joker Qyou'
APP_DEBUG_LOG = u'debug.log'
APP_COPYRIGHT = APP_VENDOR
APP_DEVELOPERS = [APP_VENDOR]
APP_ARTISTS = [APP_VENDOR]
APP_TRANSLATORS = [APP_VENDOR]
APP_VERSION = u'2.0.1 dev'
APP_DEFAULT_LOCALE = u'en_US'
APP_CONFIG_FILENAME = u'config.ini'
APP_LICENSE = u'''
Copyright (c) 2014, Joker Qyou
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS "AS IS" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
APP_WEBSITE = u''
APP_DESCRIPTION = u'A GUI glue program for converting high quality music using Nero AAC Codec.'
APP_DEBUG = True

APP_MAIN_LAYOUT_FILE = u'layout/main.xrc'
APP_PREF_LAYOUT_FILE = u'layout/preference.xrc'
APP_BIG_ICON_FILE = u'resources/icon_big.png'

APP_CONFIG_LOCALE_KEY = u'locale'
APP_CONFIG_DEBUG_KEY = u'debug'
APP_CONFIG_TEMPDIR_KEY = u'tempdir'
APP_CONFIG_BITRATE_KEY = u'bitrate'
APP_CONFIG_DELORIGIN_KEY = u'delorigin'
APP_CONFIG_ENC_PATH_KEY = u'enc'
APP_CONFIG_TAG_PATH_KEY = u'tag'

APP_DEFAULT_DELORIGIN = False

AAC_DEFAULT_BITRATE = 512000

NERO_ENC_DEFAULT_PATH = u'neroAacEnc'
NERO_TAG_DEFAULT_PATH = u'neroAacTag'
