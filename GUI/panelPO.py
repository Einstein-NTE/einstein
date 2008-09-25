#Boa:FramePanel:PanelPO
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    panelPO: Process opti.
#
#
#==============================================================================
#
#    Version No.: 0.01
#       Created by:          Florian Joebstl 25/09/2008  
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
from einstein.GUI.status import Status

from GUITools import *

[wxID_PANELPO, wxID_PANELPOBTNNEXT, wxID_PANELPOBTNPREV, wxID_PANELPOCBSECTOR, 
 wxID_PANELPOCBSUBSECTOR, wxID_PANELPOCBTYPICALPROCESS, wxID_PANELPOCBUNIT, 
 wxID_PANELPOLBTECH, wxID_PANELPOSTATICBOX1, wxID_PANELPOSTATICTEXT1, 
 wxID_PANELPOSTATICTEXT2, wxID_PANELPOSTATICTEXT3, wxID_PANELPOSTATICTEXT4, 
 wxID_PANELPOSTATICTEXT5, wxID_PANELPOSTATICTEXT6, wxID_PANELPOTCMEASURES, 
] = [wx.NewId() for _init_ctrls in range(16)]

class PanelPO(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELPO, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 616),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(792, 589))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELPOSTATICBOX1,
              label=u'Process Optimisation', name='staticBox1', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(760, 544), style=0)

        self.btnNext = wx.Button(id=wxID_PANELPOBTNNEXT, label=u'>>>',
              name=u'btnNext', parent=self, pos=wx.Point(696, 560),
              size=wx.Size(75, 23), style=0)

        self.btnPrev = wx.Button(id=wxID_PANELPOBTNPREV, label=u'<<<',
              name=u'btnPrev', parent=self, pos=wx.Point(8, 560),
              size=wx.Size(75, 23), style=0)

        self.lbTech = wx.ListBox(choices=[], id=wxID_PANELPOLBTECH,
              name=u'lbTech', parent=self, pos=wx.Point(16, 208),
              size=wx.Size(248, 328), style=0)

        self.tcMeasures = wx.TextCtrl(id=wxID_PANELPOTCMEASURES,
              name=u'tcMeasures', parent=self, pos=wx.Point(272, 208),
              size=wx.Size(488, 328), style=0, value=u'')
        self.tcMeasures.SetToolTipString(u'Measure')
        self.tcMeasures.SetEditable(False)

        self.staticText1 = wx.StaticText(id=wxID_PANELPOSTATICTEXT1,
              label=_(u'REFERENCE TECHNOLOGIES AND MEASURES:'),
              name='staticText1', parent=self, pos=wx.Point(16, 192),
              size=wx.Size(222, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELPOSTATICTEXT2,
              label=_(u'PROPOSED ENERGY EFFICIENCY MEASURES:'),
              name='staticText2', parent=self, pos=wx.Point(272, 192),
              size=wx.Size(218, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID_PANELPOSTATICTEXT3,
              label=u'Sector:', name='staticText3', parent=self,
              pos=wx.Point(24, 40), size=wx.Size(35, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_PANELPOSTATICTEXT4,
              label=u'Subsector:', name='staticText4', parent=self,
              pos=wx.Point(24, 72), size=wx.Size(52, 13), style=0)

        self.staticText5 = wx.StaticText(id=wxID_PANELPOSTATICTEXT5,
              label=u'Unit Operation:', name='staticText5', parent=self,
              pos=wx.Point(24, 104), size=wx.Size(74, 13), style=0)

        self.staticText6 = wx.StaticText(id=wxID_PANELPOSTATICTEXT6,
              label=u'Typical Process:', name='staticText6', parent=self,
              pos=wx.Point(24, 136), size=wx.Size(77, 13), style=0)

        self.cbSector = wx.Choice(choices=[], id=wxID_PANELPOCBSECTOR,
              name=u'cbSector', parent=self, pos=wx.Point(120, 40),
              size=wx.Size(312, 21), style=0)

        self.cbSubsector = wx.Choice(choices=[], id=wxID_PANELPOCBSUBSECTOR,
              name=u'cbSubsector', parent=self, pos=wx.Point(120, 72),
              size=wx.Size(312, 21), style=0)

        self.cbUnit = wx.Choice(choices=[], id=wxID_PANELPOCBUNIT,
              name=u'cbUnit', parent=self, pos=wx.Point(120, 104),
              size=wx.Size(312, 21), style=0)

        self.cbTypicalProcess = wx.Choice(choices=[],
              id=wxID_PANELPOCBTYPICALPROCESS, name=u'cbTypicalProcess',
              parent=self, pos=wx.Point(120, 136), size=wx.Size(312, 21),
              style=0)

    def __init_custom_ctrls(self,prnt):
        self.staticBox1.SetForegroundColour(TITLE_COLOR)
        self.staticBox1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))

    def __init__(self, parent, main, id, pos, size, style, name):
        self.main = main
        self.mod = Status.mod.modulePO
        self.shortName = _("PO")
        self.description = _("")               
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)

    def display(self):
        self.mod.updatePanel()
