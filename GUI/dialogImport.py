# -*- coding: cp1252 -*-
#============================================================================== 				
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	DIALOG-IMPORT
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Dialog for import of databases
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	    25/09/2008
#                           Stoyan Danov    13/10/2008
#
#       Last modified by:
#       13/10/2008: SD  change _() to _U()
#
#       Changes to previous version:
#
#------------------------------------------------------------------------------		
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	www.energyxperts.net / info@energyxperts.net
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#============================================================================== 

import wx
from einstein.GUI.status import Status

def _U(text):
    return unicode(_(text),"utf-8")

def create(parent):
    return DialogImport(parent)

[wxID_DIALOGOK, wxID_DIALOGOKBUTTONCANCEL, wxID_DIALOGOKBUTTONOVERWRITE, 
 wxID_DIALOGOKBUTTONIGNORE,wxID_DIALOGOKSTDIALOG, 
] = [wx.NewId() for _init_ctrls in range(5)]

class DialogImport(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOGOK, name="dialogImport", parent=prnt,
              pos=wx.Point(400, 300), size=wx.Size(400, 160),
              style=wx.DEFAULT_DIALOG_STYLE, title=self.title)
        self.SetClientSize(wx.Size(392, 137))

        self.stDialog = wx.StaticText(id=wxID_DIALOGOKSTDIALOG,
              label=self.message, name='stDialog', parent=self,
              pos=wx.Point(24, 16), size=wx.Size(344, 64), style=0)
        self.stDialog.Center(wx.HORIZONTAL)

        self.buttonOverwrite = wx.Button(id=wxID_DIALOGOKBUTTONOVERWRITE, label=_U('overwrite'),
              name='buttonOverwrite', parent=self, pos=wx.Point(20, 100),
              size=wx.Size(100, 24), style=0)
        self.buttonOverwrite.Bind(wx.EVT_BUTTON, self.OnButtonOverwriteButton,
              id=wxID_DIALOGOKBUTTONOVERWRITE)

        self.buttonIgnore = wx.Button(id=wxID_DIALOGOKBUTTONIGNORE, label=_U('ignore'),
              name='buttonIgnore', parent=self, pos=wx.Point(140, 100),
              size=wx.Size(100, 24), style=0)
        self.buttonIgnore.Bind(wx.EVT_BUTTON, self.OnButtonIgnoreButton,
              id=wxID_DIALOGOKBUTTONIGNORE)

        self.buttonCancel = wx.Button(id=wxID_DIALOGOKBUTTONCANCEL,
              label=_U('cancel'), name='buttonCancel', parent=self,
              pos=wx.Point(260, 100), size=wx.Size(100, 24), style=0)
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.OnButtonCancelButton,
              id=wxID_DIALOGOKBUTTONCANCEL)

    def __init__(self, parent, title, message):
        self.message = message
        self.title = title
        self._init_ctrls(parent)

    def OnButtonOverwriteButton(self, event):
        self.EndModal(wx.ID_OK)

    def OnButtonIgnoreButton(self, event):
        self.EndModal(wx.ID_IGNORE)

    def OnButtonCancelButton(self, event):
        self.EndModal(wx.ID_CANCEL)
