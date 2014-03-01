#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Customized App class
'''

import os

import wx
import wx.xrc as xrc

import i
import mainframe
import pref

__author__ = 'Joker Qyou'

L = wx.Locale()


class App(wx.App):
    '''
    Application class
    '''
    def __init__(self, redirect = True, filename = i.APP_DEBUG_LOG):
        wx.App.__init__(self, redirect, filename)
        self.MAINFRAME, self.INSTANCECHECKER = None, None

    def OnInit(self):
        instanceId = '%s - %s' % (self.GetAppName(), wx.GetUserId())
        self.INSTANCECHECKER = wx.SingleInstanceChecker(instanceId)
        if self.IsOnlyInstance():
            self.CONFIG = wx.FileConfig(
                appName = i.APP_NAME, 
                vendorName = i.APP_VENDOR, 
                localFilename = os.path.join(
                    os.path.abspath(os.path.curdir), 
                    i.APP_CONFIG_FILENAME
                    ), 
                style = wx.CONFIG_USE_LOCAL_FILE
                )
            self.initXRCLocale(
                self.CONFIG.Read(
                    i.APP_CONFIG_LOCALE_KEY, 
                    i.APP_DEFAULT_LOCALE
                    )
                )
            self.MAINFRAME = mainframe.MainFrame()
            self.MAINFRAME.Show(True)
        else:
            wx.Exit()
        return True

    def initXRCLocale(self, langCode):
        '''
        Init XRC i18n
        '''
        global L
        _localeConst = L.FindLanguageInfo(langCode).Language
        L.Init(_localeConst)
        L.AddCatalogLookupPathPrefix(i.APP_LOCALE_DIR)
        L.AddCatalog(i.APP_NAME)
        self.LOCALE = L

    def OnShowPref(self, event):
        '''
        Show preference frame.
        '''
        if hasattr(self, 'PREF'):
            try:
                self.PREF.Show(True)
            except Exception, e:
                self.PREF = pref.PrefFrame()
                self.PREF.Show(True)
        else:
            self.PREF = pref.PrefFrame()
            self.PREF.Show(True)

    def __del__(self):
        '''
        Destructor
        '''
        if hasattr(self, 'INSTANCECHECKER'):
            del self.INSTANCECHECKER
        if hasattr(self, 'CONFIG'):
            del self.CONFIG
        if hasattr(self, 'LOCALE'):
            del self.LOCALE
        if hasattr(self, 'MAINFRAME'):
            del self.MAINFRAME
        if hasattr(self, 'PREF'):
            del self.PREF

    def IsOnlyInstance(self):
        return not self.INSTANCECHECKER.IsAnotherRunning()
