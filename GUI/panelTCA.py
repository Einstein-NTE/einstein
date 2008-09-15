#Boa:FramePanel:PanelTCA
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    panelTCA: General economic data and results
#              (part of the TCA module)
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
from einstein.GUI.status import Status
from einstein.GUI.panelTCAResultTabpage1 import panelResult1
from einstein.GUI.panelTCAResultTabpage2 import panelResult2

from GUITools import *

[wxID_PANELTCA, wxID_PANELTCABTNNEXT, wxID_PANELTCABTNRESETDATA, 
 wxID_PANELTCANOTEBOOK1, wxID_PANELTCASTATICBOX1, wxID_PANELTCASTATICBOX2, 
 wxID_PANELTCASTATICTEXT1, wxID_PANELTCASTATICTEXT2, wxID_PANELTCASTATICTEXT3, 
 wxID_PANELTCASTATICTEXT4, wxID_PANELTCASTATICTEXT5, wxID_PANELTCASTATICTEXT6, 
 wxID_PANELTCASTATICTEXT7, wxID_PANELTCASTATICTEXT8, wxID_PANELTCASTATICTEXT9, 
 wxID_PANELTCATBCSDRATE, wxID_PANELTCATBENERGYPRICES, 
 wxID_PANELTCATBLOANINTERRESTRATE, wxID_PANELTCATBTIMEFAME, 
] = [wx.NewId() for _init_ctrls in range(19)]

class PanelTCA(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELTCA, name='PanelTCA', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(808, 619), style=0)
        self.SetClientSize(wx.Size(800, 592))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELTCASTATICBOX1,
              label=_('General Economic Data'), name='staticBox1', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(760, 152), style=0)

        self.staticText1 = wx.StaticText(id=wxID_PANELTCASTATICTEXT1,
              label=_('Loan interest rate'), name='staticText1', parent=self,
              pos=wx.Point(40, 40), size=wx.Size(86, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELTCASTATICTEXT2,
              label=_('Company specific descount rate'), name='staticText2',
              parent=self, pos=wx.Point(40, 67), size=wx.Size(153, 13),
              style=0)

        self.tbLoanInterrestRate = wx.TextCtrl(id=wxID_PANELTCATBLOANINTERRESTRATE,
              name='tbLoanInterrestRate', parent=self, pos=wx.Point(232, 40),
              size=wx.Size(100, 20), style=0, value='0')
        self.tbLoanInterrestRate.SetAutoLayout(False)
        self.tbLoanInterrestRate.Bind(wx.EVT_KILL_FOCUS,
              self.OnTbLoanInterrestRateKillFocus)
        self.tbLoanInterrestRate.Bind(wx.EVT_TEXT,
              self.OnTbLoanInterrestRateText,
              id=wxID_PANELTCATBLOANINTERRESTRATE)

        self.tbCSDRate = wx.TextCtrl(id=wxID_PANELTCATBCSDRATE,
              name='tbCSDRate', parent=self, pos=wx.Point(232, 64),
              size=wx.Size(100, 21), style=0, value='0')
        self.tbCSDRate.Bind(wx.EVT_KILL_FOCUS, self.OnTbCSDRateKillFocus)
        self.tbCSDRate.Bind(wx.EVT_TEXT, self.OnTbCSDRateText,
              id=wxID_PANELTCATBCSDRATE)

        self.staticText3 = wx.StaticText(id=wxID_PANELTCASTATICTEXT3,
              label=_('This timeframe will be applied to each equipment of all proposals\nIf you think there would be some maintainance or re-investment\ncaused by this time frame, please fill in the Contingencies'),
              name='staticText3', parent=self, pos=wx.Point(368, 112),
              size=wx.Size(307, 39), style=0)

        self.staticText4 = wx.StaticText(id=wxID_PANELTCASTATICTEXT4,
              label=_('Development of energy prices'), name='staticText4',
              parent=self, pos=wx.Point(40, 94), size=wx.Size(144, 13),
              style=0)

        self.staticText5 = wx.StaticText(id=wxID_PANELTCASTATICTEXT5,
              label=_('Choose time frame for economic'), name='staticText5',
              parent=self, pos=wx.Point(40, 120), size=wx.Size(154, 13),
              style=0)

        self.tbTimeFame = wx.TextCtrl(id=wxID_PANELTCATBTIMEFAME,
              name='tbTimeFame', parent=self, pos=wx.Point(232, 112),
              size=wx.Size(100, 21), style=0, value=u'1')
        self.tbTimeFame.Bind(wx.EVT_KILL_FOCUS, self.OnTbTimeFameKillFocus)
        self.tbTimeFame.Bind(wx.EVT_TEXT, self.OnTbTimeFameText,
              id=wxID_PANELTCATBTIMEFAME)

        self.tbEnergyPrices = wx.TextCtrl(id=wxID_PANELTCATBENERGYPRICES,
              name='tbEnergyPrices', parent=self, pos=wx.Point(232, 88),
              size=wx.Size(100, 21), style=0, value='0')
        self.tbEnergyPrices.Bind(wx.EVT_KILL_FOCUS,
              self.OnTbEnergyPricesKillFocus)
        self.tbEnergyPrices.Bind(wx.EVT_TEXT, self.OnTbEnergyPricesText,
              id=wxID_PANELTCATBENERGYPRICES)

        self.staticText6 = wx.StaticText(id=wxID_PANELTCASTATICTEXT6, label='%',
              name='staticText6', parent=self, pos=wx.Point(336, 64),
              size=wx.Size(32, 13), style=0)

        self.staticText7 = wx.StaticText(id=wxID_PANELTCASTATICTEXT7, label='%',
              name='staticText7', parent=self, pos=wx.Point(336, 40),
              size=wx.Size(11, 13), style=0)

        self.staticText8 = wx.StaticText(id=wxID_PANELTCASTATICTEXT8,
              label=_('% of the current energy price (including Grid fee, excluding VAT)'),
              name='staticText8', parent=self, pos=wx.Point(336, 88),
              size=wx.Size(311, 13), style=0)

        self.staticText9 = wx.StaticText(id=wxID_PANELTCASTATICTEXT9,
              label=_('year'), name='staticText9', parent=self,
              pos=wx.Point(336, 112), size=wx.Size(22, 13), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELTCASTATICBOX2,
              label=_('Results'), name='staticBox2', parent=self, pos=wx.Point(8,
              168), size=wx.Size(760, 384), style=0)

        self.btnResetData = wx.Button(id=wxID_PANELTCABTNRESETDATA,
              label=_('Reset TCA data'), name=u'btnResetData', parent=self,
              pos=wx.Point(8, 560), size=wx.Size(192, 23), style=0)
        self.btnResetData.Bind(wx.EVT_BUTTON, self.OnBtnResetDataButton,
              id=wxID_PANELTCABTNRESETDATA)

        self.btnNext = wx.Button(id=wxID_PANELTCABTNNEXT,
              label=_('Go through TCA data >>>'), name='btnNext', parent=self,
              pos=wx.Point(576, 560), size=wx.Size(192, 23), style=0)
        self.btnNext.Bind(wx.EVT_BUTTON, self.OnBtnNextButton,
              id=wxID_PANELTCABTNNEXT)

        self.notebook1 = wx.Notebook(id=wxID_PANELTCANOTEBOOK1,
              name='notebook1', parent=self, pos=wx.Point(16, 192),
              size=wx.Size(744, 352), style=0)

    def __init_custom_ctrls(self, prnt):
        self.staticBox1.SetForegroundColour(TITLE_COLOR)
        self.staticBox1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        self.staticBox2.SetForegroundColour(TITLE_COLOR)
        self.staticBox2.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        
        self.resultpage1 = panelResult1(id=wx.NewId(), name=_('Values'),
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(504,
              438), style=wx.TAB_TRAVERSAL)  
        self.notebook1.AddPage(imageId=-1, page=self.resultpage1, select=True, text='Value')
        self.resultpage2 = panelResult2(id=wx.NewId(), name=_('Diagram'),
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(504,
              438), style=wx.TAB_TRAVERSAL)  
        self.notebook1.AddPage(imageId=-1, page=self.resultpage2, select=False, text='Diagram')
        
    def __init__(self, parent, main, id, pos, size, style, name):      
        self.main = main
        self.mod = Status.mod.moduleTCA
        self.shortName = _("TCA")
        self.description = _("")
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)
    
    def display(self):
        self.mod.updatePanel()  
        self.tbLoanInterrestRate.SetValue(str(self.mod.LIR))
        self.tbCSDRate.SetValue(str(self.mod.CSDR))
        self.tbEnergyPrices.SetValue(str(self.mod.DEP))
        self.tbTimeFame.SetValue(str(self.mod.TimeFrame))      

#Focus events------------------------------------------------------------------------------------------------
    def OnTbLoanInterrestRateKillFocus(self, event):
        try:
            self.mod.LIR = float(self.tbLoanInterrestRate.GetValue())
            if (self.mod.LIR<0)or(self.mod.LIR>100.0):
                raise
        except:
            wx.MessageBox(_("Load interest rate: value between 0 and 100 expected."))
            self.tbLoanInterrestRate.SetFocus()
        event.Skip()

    def OnTbCSDRateKillFocus(self, event):
        try:
            self.mod.CSDR = float(self.tbCSDRate.GetValue())
            if (self.mod.CSDR<0)or(self.mod.CSDR>100.0):
                raise
        except:
            wx.MessageBox(_("Company specific discount rate: value between 0 and 100 expected."))
            self.tbCSDRate.SetFocus()
        event.Skip()

    def OnTbTimeFameKillFocus(self, event):
        try:
            self.mod.TimeFrame = int(self.tbTimeFame.GetValue())
            if (self.mod.TimeFrame<1)or(self.mod.TimeFrame>1000.0):
                raise
        except:
            wx.MessageBox(_("Time frame: value between 1 and 1000 expected."))
            self.tbTimeFame.SetFocus()
        event.Skip()

    def OnTbEnergyPricesKillFocus(self, event):
        try:
            self.mod.DEP = float(self.tbEnergyPrices.GetValue())
            if (self.mod.DEP<0)or(self.mod.DEP>100.0):
                raise
        except:
            wx.MessageBox(_("Development of energy prices: value between 0 and 100 expected."))
            self.tbEnergyPrices.SetFocus()
        event.Skip()

#TEXT EVENTS---------------------------------------------------------------------------------
    def OnTbLoanInterrestRateText(self, event):
        try:
            self.mod.LIR = float(self.tbLoanInterrestRate.GetValue())
            if (self.mod.LIR<0)or(self.mod.LIR>100.0):
                raise
        except:
            self.mod.LIR = 0
        event.Skip()

    def OnTbCSDRateText(self, event):
        try:
            self.mod.CSDR = float(self.tbCSDRate.GetValue())
            if (self.mod.CSDR<0)or(self.mod.CSDR>100.0):
                raise
        except:
            self.mod.CSDR = 0
        event.Skip()

    def OnTbTimeFameText(self, event):
        try:
            self.mod.TimeFrame = int(self.tbTimeFame.GetValue())
            if (self.mod.TimeFrame<1)or(self.mod.TimeFrame>1000.0):
                raise
        except:
            self.mod.TimeFrame = 1
        event.Skip()

    def OnTbEnergyPricesText(self, event):
        try:
            self.mod.DEP = float(self.tbEnergyPrices.GetValue())
            if (self.mod.DEP<0)or(self.mod.DEP>100.0):
                raise
        except:
            self.mod.DEP = 0
        event.Skip()

    def OnBtnResetDataButton(self, event):
        event.Skip()

    def OnBtnNextButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qOptiProEconomic1, select=True)
        event.Skip()

