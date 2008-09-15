#Boa:FramePanel:panelResult2
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    panelResult1: TCA Resultpage - Diagram (Tabpage of panelTCA)
#                  (part of the TCA module)
#
#
#==============================================================================
#
#    Version No.: 0.01
#       Created by:          Florian Joebstl 15/09/2008  
#       Revised by:       
#
#       Changes to previous version:
#
#
#------------------------------------------------------------------------------
#    (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#    http://www.energyxperts.net/
#
#    This program is free software: you can redistribute it or modify it under
#    the terms of the GNU general public license as published by the Free
#    Software Foundation (www.gnu.org).
#
#==============================================================================

import wx
from GUITools import *
[wxID_PANELRESULT2, wxID_PANELRESULT2BTNADD, wxID_PANELRESULT2BTNREMOVE, 
 wxID_PANELRESULT2CBMIRR, wxID_PANELRESULT2CBNVP, wxID_PANELRESULT2CHOICE1, 
 wxID_PANELRESULT2PANEL1, wxID_PANELRESULT2STATICBOX1, 
 wxID_PANELRESULT2STATICBOX2, 
] = [wx.NewId() for _init_ctrls in range(9)]

class panelResult2(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELRESULT2, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(730, 350),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(722, 323))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELRESULT2STATICBOX1,
              label=_(u'Choose the proposal(s) to be additionaly displayed in the diagram'),
              name='staticBox1', parent=self, pos=wx.Point(8, 240),
              size=wx.Size(360, 64), style=0)

        self.choice1 = wx.Choice(choices=[],
              id=wxID_PANELRESULT2CHOICE1, name='choice1',
              parent=self, pos=wx.Point(24, 264), size=wx.Size(160, 21),
              style=0)

        self.btnAdd = wx.Button(id=wxID_PANELRESULT2BTNADD,
              label=_('Add'), name=u'btnAdd', parent=self, pos=wx.Point(192, 264),
              size=wx.Size(75, 23), style=0)

        self.btnRemove = wx.Button(id=wxID_PANELRESULT2BTNREMOVE,
              label=_('Remove'), name=u'btnRemove', parent=self, pos=wx.Point(272,
              264), size=wx.Size(75, 23), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELRESULT2STATICBOX2,
              label=_('Please choose the parameters to be displayed in the diagram'),
              name='staticBox2', parent=self, pos=wx.Point(376, 240),
              size=wx.Size(336, 64), style=0)

        self.panel1 = wx.Panel(id=wxID_PANELRESULT2PANEL1,
              name='panel1', parent=self, pos=wx.Point(8, 8), size=wx.Size(200,
              100), style=wx.TAB_TRAVERSAL)

        self.cbNVP = wx.CheckBox(id=wxID_PANELRESULT2CBNVP,
              label=_('NVP'), name=u'cbNVP', parent=self, pos=wx.Point(400, 272),
              size=wx.Size(70, 13), style=0)
        self.cbNVP.SetValue(True)
        self.cbNVP.Bind(wx.EVT_CHECKBOX, self.OnCbNVPCheckbox,
              id=wxID_PANELRESULT2CBNVP)

        self.cbMIRR = wx.CheckBox(id=wxID_PANELRESULT2CBMIRR,
              label=_('MIRR'), name=u'cbMIRR', parent=self, pos=wx.Point(464,
              272), size=wx.Size(70, 13), style=0)
        self.cbMIRR.SetValue(False)
        self.cbMIRR.Bind(wx.EVT_CHECKBOX, self.OnCbMIRRCheckbox,
              id=wxID_PANELRESULT2CBMIRR)

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)

    def OnCbNVPCheckbox(self, event):
        event.Skip()

    def OnCbMIRRCheckbox(self, event):
        event.Skip()
