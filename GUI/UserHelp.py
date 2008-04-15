import os
import wx
import wx.html

class FrameHelpUserManual(wx.Dialog):
    def __init__(self, parent, manualfile):
        wx.Dialog.__init__(self, id=-1, name=u'FrameHelpUserManual',
              parent=parent, pos=wx.Point(0,0), size=wx.Size(600,800),
              style=wx.DEFAULT_FRAME_STYLE, title='User manual')

	self.html = wx.html.HtmlWindow(self, id=-1, pos=wx.DefaultPosition,
				  style=wx.html.HW_SCROLLBAR_AUTO,
				  name="htmlManualWindow")
	if "gtk2" in wx.PlatformInfo:
	    self.html.SetStandardFonts()

	if os.access(manualfile,os.R_OK):
	    # if possible, load local manual
	    self.html.LoadFile(manualfile)
	else:
	    # else, go to einstein site
	    self.html.LoadPage("http://www.iee-einstein.org")


	manualButtonOK = wx.Button(id=wx.ID_OK, label=u'OK', name='manualButtonOK',
              parent=self, size=wx.Size(80, 24))

	manualButtonBack = wx.Button(id=wx.ID_BACKWARD, label=u'Back', name='manualButtonBack',
              parent=self, size=wx.Size(80, 24))
        self.Bind(wx.EVT_BUTTON, self.OnManualButtonBack, manualButtonBack)

	manualButtonForward = wx.Button(id=wx.ID_FORWARD, label=u'Forward', name='manualButtonForward',
              parent=self, size=wx.Size(80, 24))
        self.Bind(wx.EVT_BUTTON, self.OnManualButtonForward, manualButtonForward)

        sz0 = wx.BoxSizer(wx.HORIZONTAL)
        sz0.Add(manualButtonBack, 1, wx.ALL, 5)
        sz0.Add(manualButtonForward, 1, wx.ALL, 5)
        sz0.Add(manualButtonOK, 1, wx.ALL, 5)
        sz1 = wx.BoxSizer(wx.VERTICAL)
        sz1.Add(self.html, 1, wx.EXPAND, 5)
        sz1.Add(sz0, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sz1)

    def OnManualButtonBack(self, event):
	self.html.HistoryBack()

    def OnManualButtonForward(self, event):
	self.html.HistoryForward()


class FrameHelpAbout(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, id=-1, name=u'FrameHelpAbout',
              parent=parent, pos=wx.Point(0,0), size=wx.Size(620,500),
              style=wx.DEFAULT_FRAME_STYLE, title='About')

	self.html = wx.html.HtmlWindow(self, id=-1, pos=wx.DefaultPosition,
				  style=wx.html.HW_SCROLLBAR_AUTO,
				  name="htmlAboutWindow")
	if "gtk2" in wx.PlatformInfo:
	    self.html.SetStandardFonts()

	self.html.SetPage("<html><head><title>Einstein</title></head>"
		     "<body background=\"einstein_logo_bg.jpg\"><center>"
		     "<img src=\"einstein_logo.png\" width=\"580\", height=\"150\">"
		     "<br><br>"
		     "<b>Expert System for an Intelligent Supply of Thermal Energy in Industry</b><br>"
		     "<a href=\"http://www.iee-einstein.org\">www.iee-einstein.org</a>"
		     "<br><br>Version 0.1"
		     "<p>(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain&nbsp;2008</p>"
		     "<p>Web page: <a href=\"http://www.energyxperts.net\">www.energyxperts.net</a></p>"
		     "<p>Email: <a href=\"mailto://info@energyxperts.net\">info@energyxperts.net</a></p>"
		     "<br><hr><br>"
		     "This program is free software: you can redistribute it or modify it under"
		     "the terms of the GNU general public license as published by the Free"
		     "Software Foundation (<a href=\"http://www.gnu.org\">www.gnu.org</a>)."
		     "</center></body></html>")

        aboutButtonOK = wx.Button(id=wx.ID_OK, label=u'OK', name='aboutButtonOK',
              parent=self, size=wx.Size(80,24))
	
        sz0 = wx.BoxSizer(wx.HORIZONTAL)
        sz0.Add(aboutButtonOK, 1, wx.ALL, 5)
        sz1 = wx.BoxSizer(wx.VERTICAL)
        sz1.Add(self.html, 1, wx.EXPAND, 5)
        sz1.Add(sz0, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sz1)
