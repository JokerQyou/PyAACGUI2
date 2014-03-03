#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Customized main frame class
'''

import multiprocessing
import os
import tempfile
import threading

import wx
import wx.xrc as xrc

import core
from core import converter
import i
import q

__author__ = 'Joker Qyou'

# Set debug switch
C = wx.FileConfig(
    appName = i.APP_NAME, 
    vendorName = i.APP_VENDOR, 
    localFilename = os.path.join(
        os.path.abspath(os.path.curdir), 
        i.APP_CONFIG_FILENAME
        ), 
    style = wx.CONFIG_USE_LOCAL_FILE
    )
i.APP_DEBUG = C.ReadBool(i.APP_CONFIG_DEBUG_KEY, i.APP_DEBUG)

if i.APP_DEBUG:
    import time

del C

# Use wxPython i18n instead of gettext module, 
# cause this would take care of XRC i18n also.
_ = wx.GetTranslation


class MainFrame(wx.Frame):
    '''
    Main frame class
    '''
    def __init__(self):
        '''
        Init function
        '''
        # Load XRC layout of main frame
        resource = xrc.XmlResource(i.APP_MAIN_LAYOUT_FILE)
        pre = wx.PreFrame()
        pre = resource.LoadFrame(None, 'mainframe')
        self.PostCreate(pre)

        # Set icon to window so it would not look so ugly. 
        # Notice that on Windows the resolution of the icon on the title bar 
        # cannot be too large, so this line would probably not work.
        self.SetIcon(wx.Icon(i.APP_BIG_ICON_FILE, wx.BITMAP_TYPE_PNG))

        # Setting min size to a quarter of screen size would be suitable, 
        # many desktop environment has docking feature, which allows a window 
        # to be resized to half or quarter the size of screen. If the min 
        # size set was too large, the docking feature will not take effect.
        self.SetMinSize((wx.DisplaySize()[0] / 2, wx.DisplaySize()[1] / 2))

        # Set default values of additional attributes
        self.FILELIST, self.QUEUE, self.CONVERTER = None, [], None
        self.PROGRESS = None

        # Insert rows into list ctrl
        self.initFileList()

        # Bind menu event handlers
        self.Bind(
            wx.EVT_MENU, 
            wx.GetApp().OnShowPref, 
            id = xrc.XRCID('menufilepref')
            )
        self.Bind(
            wx.EVT_MENU, 
            self.OnFileQuit, 
            id = xrc.XRCID('menufilequit')
            )
        self.Bind(
            wx.EVT_MENU, 
            self.OnHelpAbout, 
            id = xrc.XRCID('menuhelpabout')
            )

        # Bind tool event handlers
        self.Bind(
            wx.EVT_TOOL, 
            self.OnFileSelect, 
            id = xrc.XRCID('toolopen')
            )
        self.Bind(
            wx.EVT_TOOL, 
            self.OnConversionStart, 
            id = xrc.XRCID('toolconvert')
            )
        self.Bind(
            wx.EVT_TOOL, 
            self.OnHelpAbout, 
            id = xrc.XRCID('toolinfo')
            )
        self.Bind(
            wx.EVT_TOOL, 
            self.OnFileQuit, 
            id = xrc.XRCID('toolquit')
            )

        # Bind global event handlers
        # To avoid quiting during a conversion
        self.Bind(
            wx.EVT_CLOSE, 
            self.OnFileQuit
            )

        self.SetStatusText(_('Ready'))

    def initFileList(self):
        '''
        Init list ctrl for files.
        '''
        self.FILELIST = xrc.XRCCTRL(self, 'FILELIST')
        self.FILELIST.InsertColumn(
            0, 
            _('File path'), 
            format = wx.LIST_FORMAT_LEFT, 
            width = 750
            )
        self.FILELIST.InsertColumn(
            1, 
            _('Status'), 
            format = wx.LIST_FORMAT_LEFT, 
            width = 100
            )

    def fillFileList(self, fnames):
        '''
        Fill `FILELIST ` list ctrl with given fnames list.
        '''
        self.FILELIST.DeleteAllItems()
        lastIndex = 0
        for fname in fnames:
            index = self.FILELIST.InsertStringItem(
                lastIndex, 
                fname
                )
            self.FILELIST.SetStringItem(index, 1, _('Waiting'))
            lastIndex += 1

    def OnFileSelect(self, event):
        '''
        Handler for file selection.
        '''
        fFilters = ''.join([
            'Free Lossless Audio Codec (*.flac)|*.flac', 
            '|', 
            'WAVE audio (*.wav)|*.wav', 
            '|', 
            'Monkey\'s Audio (*.ape)|*.ape', 
            '|', 
            'Wave pack (*.wv)|*.wv', 
            '|', 
            'TTA audio (*.tta)|*.tta', 
            '|', 
            'TAK audio (*.tak)|*.tak', 
            '|', 
            'All files (*.*)|*.*'
            ])
        dlg = wx.FileDialog(
            None, 
            _('Select audio files'), # Title of dialog
            os.path.expanduser('~'), # Default directory
            '', # Default file
            fFilters, # File type filters
            wx.OPEN | wx.MULTIPLE
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.SetStatusText(_('Processing file paths...'))
            fnames = dlg.GetPaths()
            self.QUEUE = list(set(fnames))
            self.QUEUE.sort()
            self.fillFileList(self.QUEUE)
            self.SetStatusText(_('%d files queued.') % len(self.QUEUE))
        dlg.Destroy()

    def OnConversionStart(self, event):
        '''
        Start conversion.
        '''
        if len(self.QUEUE) == 0:
            dlg = wx.MessageDialog(
                None, 
                _('No file selected.'), 
                _('Nothing to do'), 
                wx.OK | wx.ICON_ERROR
                )
            dlg.ShowModal()
            dlg.Destroy()
        else:
            # Avoid adding files or starting another conversion, 
            # cause the background thread does not care whether the 
            # file queue has changed.
            q.disabletools(
                ['toolopen', 'toolconvert'], 
                parent = self.GetToolBar()
                )
            C = wx.GetApp().CONFIG

            # Find absolute path of encoder and tagger executables if they 
            # were set in config file, otherwise use default values.
            encpath = C.Read(i.APP_CONFIG_ENC_PATH_KEY, '')
            tagpath = C.Read(i.APP_CONFIG_TAG_PATH_KEY, '')
            if encpath and q.fileexists(os.path.abspath(encpath)):
                encpath = os.path.abspath(encpath)
            else:
                encpath = i.NERO_ENC_DEFAULT_PATH
            if tagpath and q.fileexists(os.path.abspath(tagpath)):
                tagpath = os.path.abspath(tagpath)
            else:
                tagpath = i.NERO_TAG_DEFAULT_PATH

            # Create background thread to do the actual work.
            self.CONVERTER = converter.ConversionMgr(
                caller = self, 
                callback = self.updateProgress, 
                queue = self.QUEUE, 
                tempdir = C.Read(
                    i.APP_CONFIG_TEMPDIR_KEY, 
                    tempfile.gettempdir()
                    ), 
                bitrate = C.ReadInt(
                    i.APP_CONFIG_BITRATE_KEY, 
                    i.AAC_DEFAULT_BITRATE
                    ), 
                delorigin = C.ReadBool(
                    i.APP_CONFIG_DELORIGIN_KEY, 
                    i.APP_DEFAULT_DELORIGIN
                    ), 
                encoder = encpath, 
                tagger = tagpath, 
                maxcorenum = C.ReadInt(
                    i.APP_CONFIG_CORE_NUM_KEY, 
                    multiprocessing.cpu_count()
                    )
                )

            self.SetStatusText(_('Processing files, please wait...'))
            self.CONVERTER.start()

    def updateProgress(self, *args):
        '''
        Update progress.
        '''
        index = self.QUEUE.index(args[0])
        self.FILELIST.SetStringItem(index, 1, _(args[1]))
        self.SetStatusText(
            _('Processing files: %d of %d') % self.CONVERTER.progress()
            )

    def OnConversionDone(self):
        '''
        Callback on background thread done.
        '''
        # Pop a message to user
        dlg = wx.MessageDialog(
            None, 
            _('All files converted.'), 
            _('Queue processed'), 
            wx.OK | wx.ICON_INFORMATION
            )
        dlg.ShowModal()
        dlg.Destroy()

        # Clear file queue to be ready for next conversion
        self.QUEUE = []
        self.SetStatusText(
            _('%d files queued.') % len(self.QUEUE)
            )

        # Re-enable tools disabled at the beginning of the conversion
        q.enabletools(
            ['toolopen', 'toolconvert'], 
            parent = self.GetToolBar()
            )

    def OnFileQuit(self, event):
        '''
        Handler for quiting procedure.
        '''
        # wx.Exit()
        if len(self.QUEUE) == 0 \
            or not self.CONVERTER \
            or (self.CONVERTER and self.CONVERTER.isDone()):
            wx.Exit()
        else:
            dlg = wx.MessageDialog(
                None, 
                _('Conversion subprocess is still running.'), 
                _('Subprocess running'), 
                wx.OK | wx.ICON_ERROR
                )
            dlg.ShowModal()
            dlg.Destroy()

    def OnHelpAbout(self, event):
        '''
        Show information about this program
        '''
        aboutInfo = wx.AboutDialogInfo()
        aboutInfo.SetIcon(wx.Icon(i.APP_BIG_ICON_FILE, wx.BITMAP_TYPE_PNG))
        aboutInfo.SetName(_(i.APP_NAME))
        aboutInfo.SetVersion(i.APP_VERSION)
        aboutInfo.SetDescription(_(i.APP_DESCRIPTION))
        aboutInfo.SetLicense(i.APP_LICENSE)
        aboutInfo.SetCopyright(i.APP_COPYRIGHT)
        aboutInfo.SetWebSite(i.APP_WEBSITE)
        [aboutInfo.AddDeveloper(developer) 
            for developer in i.APP_DEVELOPERS]
        [aboutInfo.AddArtist(artist) 
            for artist in i.APP_ARTISTS]
        [aboutInfo.AddTranslator(translator) 
            for translator in i.APP_TRANSLATORS]
        dlgAbout = wx.AboutBox(aboutInfo)
