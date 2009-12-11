#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	dialogLanguage: Tool main menu -> language selection
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	April 2008
#	Last revised by:
#                           Stoyan Danov        19/06/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes to previous version:
#       19/06/2008 SD: change to translatable text _(...)
#       13/10/2008: SD  change _() to _U()
#
#
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	http://www.energyxperts.net/
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================

import wx
from einstein.modules.constants import updateConstants
from einstein.GUI.status import Status

def _U(text):
    return unicode(_(text),"utf-8")

class DialogLanguage(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=-1, name='DialogLanguage', parent=prnt,
              pos=wx.Point(433, 283), size=wx.Size(350, 300),
              style=wx.DEFAULT_DIALOG_STYLE, title=_U('Select language'))

        self.st1 = wx.StaticText(id=-1,
                                 label=_U('Available languages'),
                                 name='st1',
                                 parent=self,
                                 pos=wx.Point(10, 16),
                                 size=wx.Size(200, 32),
                                 style=0)

        self.listBoxLang = wx.ListBox(id=-1,
                                      choices=[],
                                      name='listBoxLang',
                                      parent=self,
                                      pos=wx.Point(10, 50),
                                      size=wx.Size(200, 200),
                                      style=wx.LB_SINGLE|wx.LB_SORT)
        self.listBoxLang.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.BOLD, False, 'Ne Times Roman'))
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListBoxLangDclick, self.listBoxLang)

        self.buttonOK = wx.Button(id=wx.ID_OK,
                                  label=_U('OK'),
                                  name='buttonOK',
                                  parent=self,
                                  pos=wx.Point(220, 50),
                                  size=wx.Size(91, 23),
                                  style=0)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOKButton, id=wx.ID_OK)

        self.buttonCancel = wx.Button(id=wx.ID_CANCEL,
                                      label=_U('Cancel'),
                                      name='buttonCancel',
                                      parent=self,
                                      pos=wx.Point(220, 80),
                                      size=wx.Size(91, 23),
                                      style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.language = ''
        self.fillPage()
        
#------------------------------------------------------------------------------
#--- Eventhandlers
#------------------------------------------------------------------------------		
    def OnButtonOKButton(self, event):
        self.language = self.listBoxLang.GetStringSelection().split("-")[0]

        Status.LanguageTool = self.language

        stool = Status.DB.stool.STool_ID[1][0]
        stool.LanguageTool = self.language

        self.EndModal(wx.ID_OK)

    def OnListBoxLangDclick(self, event):
        self.language = self.listBoxLang.GetStringSelection().split("-")[0]

        Status.LanguageTool = self.language

        stool = Status.DB.stool.STool_ID[1][0]
        stool.LanguageTool = self.language

        self.EndModal(wx.ID_OK)

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		
    def SetLangList(self,list):
        self.listBoxLang.Clear()
        for lang in list:
            self.listBoxLang.Append(lang)
        self.listBoxLang.SetSelection(0)

    def clear(self):
        self.listBoxLang.Clear()

    def fillPage(self):
	self.SetLangList([_U('en-English'),
                          _U('cat-Catalan'),
                          _U('cz-Czech'),
                          _U('de-Deutsch'),
                          _U('it-Italiano'),
                          _U('pl-Polish'),
                          _U('si-Slovenian'),
                          _U('es-Spanish')])

    def GetLanguage(self):
        return self.language
