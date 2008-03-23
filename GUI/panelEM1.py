#Boa:Frame:PanelEM1

import wx
import wx.grid
from status import Status
from einstein.modules.energyStats.moduleEM1 import *
import einstein.modules.matPanel as Mp

[wxID_PANELEM1, wxID_PANELEM1BTNBACK, wxID_PANELEM1BTNFORWARD, 
 wxID_PANELEM1BTNOK, wxID_PANELEM1GRID1, wxID_PANELEM1PANELGRAPHMPHD, 
] = [wx.NewId() for _init_ctrls in range(6)]

class PanelEM1(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.mod = ModuleEM1()

        # remaps drawing methods to the wx widgets.
        # gets the drawing methods from moduleEM1
        dummy = Mp.MatPanel(self.panelGraphMPHD, wx.Panel, self.mod.getPlotMethod(0))
        del dummy

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEM1, name=u'PanelEM1', parent=prnt,
              pos=wx.Point(6, 0), size=wx.Size(800, 600), style=0)

        self.grid1 = wx.grid.Grid(id=wxID_PANELEM1GRID1, name='grid1',
              parent=self, pos=wx.Point(40, 48), size=wx.Size(440, 168),
              style=0)

        self.panelGraphMPHD = wx.Panel(id=wxID_PANELEM1PANELGRAPHMPHD,
              name=u'panelGraphMPHD', parent=self, pos=wx.Point(40, 240),
              size=wx.Size(440, 272), style=wx.TAB_TRAVERSAL)
        self.panelGraphMPHD.SetBackgroundColour(wx.Colour(77, 77, 77))

        self.btnBack = wx.Button(id=wx.ID_BACKWARD, label=u'<<<',
              name=u'btnBack', parent=self, pos=wx.Point(160, 520),
              size=wx.Size(104, 32), style=0)
        self.btnBack.Bind(wx.EVT_BUTTON, self.OnBtnBackButton,
              id=wxID_PANELEM1BTNBACK)

        self.btnOK = wx.Button(id=wx.ID_OK, label=u'OK', name=u'btnOK',
              parent=self, pos=wx.Point(272, 520), size=wx.Size(104, 32),
              style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_PANELEM1BTNOK)

        self.btnForward = wx.Button(id=wx.ID_FORWARD, label=u'>>>',
              name=u'btnForward', parent=self, pos=wx.Point(384, 520),
              size=wx.Size(96, 32), style=0)
        self.btnForward.Bind(wx.EVT_BUTTON, self.OnBtnForwardButton,
              id=wxID_PANELEM1BTNFORWARD)


    def OnBtnOKButton(self, event):
        event.Skip()

    def OnBtnBackButton(self, event):
        event.Skip()

    def OnButton1Button(self, event):
        event.Skip()

    def OnBtnForwardButton(self, event):
        event.Skip()
