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
#       Revised by:          Florian Joebstl 16/09/2008  
#
#       Changes to previous version:
#            16/09/08 FJ Removed "Loan Interest Rate"
#                        Added "Nominal Interest Rate of external financing"
#                        Added "Inflation Rate"                         
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
from einstein.modules.messageLogger import *

from GUITools import *

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

[wxID_PANELTCA, wxID_PANELTCABTNNEXT, wxID_PANELTCABTNNEXTMODULE, 
 wxID_PANELTCABTNPREVMODULE, wxID_PANELTCABTNRESETALL, 
 wxID_PANELTCABTNRESETDATA, wxID_PANELTCANOTEBOOK1, wxID_PANELTCASTATICBOX1, 
 wxID_PANELTCASTATICBOX2, wxID_PANELTCASTATICTEXT1, wxID_PANELTCASTATICTEXT10, 
 wxID_PANELTCASTATICTEXT11, wxID_PANELTCASTATICTEXT2, 
 wxID_PANELTCASTATICTEXT3, wxID_PANELTCASTATICTEXT4, wxID_PANELTCASTATICTEXT5, 
 wxID_PANELTCASTATICTEXT6, wxID_PANELTCASTATICTEXT7, wxID_PANELTCASTATICTEXT8, 
 wxID_PANELTCASTATICTEXT9, wxID_PANELTCATBCSDRATE, 
 wxID_PANELTCATBENERGYPRICES, wxID_PANELTCATBINFLATION, wxID_PANELTCATBNIR, 
 wxID_PANELTCATBTIMEFAME, 
] = [wx.NewId() for _init_ctrls in range(25)]

class PanelTCA(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELTCA, name='PanelTCA', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(808, 617), style=0)
        self.SetClientSize(wx.Size(800, 590))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELTCASTATICBOX1,
              label=_U('General Economic Data'), name='staticBox1', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(760, 152), style=0)

        self.staticText1 = wx.StaticText(id=wxID_PANELTCASTATICTEXT1,
              label=_U('Nominal interest rate of external financing'),
              name='staticText1', parent=self, pos=wx.Point(40, 60),
              size=wx.Size(202, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELTCASTATICTEXT2,
              label=_U('Company specific discount rate'), name='staticText2',
              parent=self, pos=wx.Point(40, 108), size=wx.Size(149, 13),
              style=0)

        self.tbNIR = wx.TextCtrl(id=wxID_PANELTCATBNIR, name='tbNIR',
              parent=self, pos=wx.Point(256, 56), size=wx.Size(100, 20),
              style=0, value='0')
        self.tbNIR.SetAutoLayout(False)
        self.tbNIR.Bind(wx.EVT_KILL_FOCUS, self.OnTbNIRKillFocus)
        self.tbNIR.Bind(wx.EVT_TEXT, self.OnTbNIRText, id=wxID_PANELTCATBNIR)

        self.tbCSDRate = wx.TextCtrl(id=wxID_PANELTCATBCSDRATE,
              name='tbCSDRate', parent=self, pos=wx.Point(256, 104),
              size=wx.Size(100, 21), style=0, value='0')
        self.tbCSDRate.Bind(wx.EVT_KILL_FOCUS, self.OnTbCSDRateKillFocus)
        self.tbCSDRate.Bind(wx.EVT_TEXT, self.OnTbCSDRateText,
              id=wxID_PANELTCATBCSDRATE)

        self.staticText3 = wx.StaticText(id=wxID_PANELTCASTATICTEXT3,
              label=_U('This timeframe will be applied to each equipment of all proposals\nIf you think there would be some maintainance or re-investment\ncaused by this time frame, please fill in the Contingencies'),
              name='staticText3', parent=self, pos=wx.Point(400, 120),
              size=wx.Size(267, 33), style=0)
        self.staticText3.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))

        self.staticText4 = wx.StaticText(id=wxID_PANELTCASTATICTEXT4,
              label=_U('Development of energy prices'), name='staticText4',
              parent=self, pos=wx.Point(40, 84), size=wx.Size(144, 13),
              style=0)

        self.staticText5 = wx.StaticText(id=wxID_PANELTCASTATICTEXT5,
              label=_U('Time frame for economic analysis'), name='staticText5',
              parent=self, pos=wx.Point(40, 132), size=wx.Size(158, 13),
              style=0)

        self.tbTimeFame = wx.TextCtrl(id=wxID_PANELTCATBTIMEFAME,
              name='tbTimeFame', parent=self, pos=wx.Point(256, 128),
              size=wx.Size(100, 21), style=0, value='1')
        self.tbTimeFame.Bind(wx.EVT_KILL_FOCUS, self.OnTbTimeFameKillFocus)
        self.tbTimeFame.Bind(wx.EVT_TEXT, self.OnTbTimeFameText,
              id=wxID_PANELTCATBTIMEFAME)

        self.tbEnergyPrices = wx.TextCtrl(id=wxID_PANELTCATBENERGYPRICES,
              name='tbEnergyPrices', parent=self, pos=wx.Point(256, 80),
              size=wx.Size(100, 21), style=0, value='0')
        self.tbEnergyPrices.Bind(wx.EVT_KILL_FOCUS,
              self.OnTbEnergyPricesKillFocus)
        self.tbEnergyPrices.Bind(wx.EVT_TEXT, self.OnTbEnergyPricesText,
              id=wxID_PANELTCATBENERGYPRICES)

        self.staticText6 = wx.StaticText(id=wxID_PANELTCASTATICTEXT6, label='%',
              name='staticText6', parent=self, pos=wx.Point(360, 64),
              size=wx.Size(32, 13), style=0)

        self.staticText7 = wx.StaticText(id=wxID_PANELTCASTATICTEXT7, label='%',
              name='staticText7', parent=self, pos=wx.Point(360, 40),
              size=wx.Size(11, 13), style=0)

        self.staticText8 = wx.StaticText(id=wxID_PANELTCASTATICTEXT8,
              label=_U('% of the current energy price (including Grid fee, excluding VAT)'),
              name='staticText8', parent=self, pos=wx.Point(360, 88),
              size=wx.Size(311, 13), style=0)

        self.staticText9 = wx.StaticText(id=wxID_PANELTCASTATICTEXT9,
              label=_U('years'), name='staticText9', parent=self,
              pos=wx.Point(360, 128), size=wx.Size(27, 13), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELTCASTATICBOX2,
              label=_U('Results'), name='staticBox2', parent=self,
              pos=wx.Point(8, 168), size=wx.Size(760, 384), style=0)

        self.btnResetData = wx.Button(id=wxID_PANELTCABTNRESETDATA,
              label=_U('Reset TCA data for current proposal'), name='btnResetData', parent=self,
              pos=wx.Point(8, 560), size=wx.Size(200, 23), style=0)
        self.btnResetData.Bind(wx.EVT_BUTTON, self.OnBtnResetDataButton,
              id=wxID_PANELTCABTNRESETDATA)

        self.btnNext = wx.Button(id=wxID_PANELTCABTNNEXT,
              label=_U('Go through TCA data'), name='btnNext', parent=self,
              pos=wx.Point(520, 560), size=wx.Size(192, 23), style=0)
        self.btnNext.Bind(wx.EVT_BUTTON, self.OnBtnNextButton,
              id=wxID_PANELTCABTNNEXT)

        self.notebook1 = wx.Notebook(id=wxID_PANELTCANOTEBOOK1,
              name='notebook1', parent=self, pos=wx.Point(16, 192),
              size=wx.Size(744, 352), style=0)
        self.notebook1.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,
              self.OnNotebook1NotebookPageChanged, id=wxID_PANELTCANOTEBOOK1)

        self.btnPrevModule = wx.Button(id=wxID_PANELTCABTNPREVMODULE,
              label='<<<', name='btnPrevModule', parent=self,
              pos=wx.Point(464, 560), size=wx.Size(48, 23), style=0)
        self.btnPrevModule.SetToolTipString('Back to H&C Supply')
        self.btnPrevModule.Bind(wx.EVT_BUTTON, self.OnBtnPrevModuleButton,
              id=wxID_PANELTCABTNPREVMODULE)

        self.btnNextModule = wx.Button(id=wxID_PANELTCABTNNEXTMODULE,
              label='>>>', name='btnNextModule', parent=self,
              pos=wx.Point(720, 560), size=wx.Size(48, 23), style=0)
        self.btnNextModule.SetToolTipString('forward to Comperativ Study')
        self.btnNextModule.Bind(wx.EVT_BUTTON, self.OnBtnNextModuleButton,
              id=wxID_PANELTCABTNNEXTMODULE)

        self.tbInflation = wx.TextCtrl(id=wxID_PANELTCATBINFLATION,
              name='tbInflation', parent=self, pos=wx.Point(256, 32),
              size=wx.Size(100, 21), style=0, value='0')
        self.tbInflation.Bind(wx.EVT_TEXT, self.OnTbInflationText,
              id=wxID_PANELTCATBINFLATION)
        self.tbInflation.Bind(wx.EVT_KILL_FOCUS, self.OnTbInflationKillFocus)

        self.staticText10 = wx.StaticText(id=wxID_PANELTCASTATICTEXT10,
              label='Inflation Rate', name='staticText10', parent=self,
              pos=wx.Point(40, 36), size=wx.Size(66, 13), style=0)

        self.staticText11 = wx.StaticText(id=wxID_PANELTCASTATICTEXT11,
              label='%', name='staticText11', parent=self, pos=wx.Point(360,
              108), size=wx.Size(11, 13), style=0)

        self.btnResetAll = wx.Button(id=wxID_PANELTCABTNRESETALL,
              label='Reset TCA for all proposals', name='btnResetAll', parent=self,
              pos=wx.Point(220, 560), size=wx.Size(200, 23), style=0)
        self.btnResetAll.Bind(wx.EVT_BUTTON, self.OnBtnResetAllButton,
              id=wxID_PANELTCABTNRESETALL)

    def __init_custom_ctrls(self, prnt):
        self.staticBox1.SetForegroundColour(TITLE_COLOR)
        self.staticBox1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        self.staticBox2.SetForegroundColour(TITLE_COLOR)
        self.staticBox2.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        
        self.resultpage1 = panelResult1(id=wx.NewId(), name=_U('Values'),
              parent=self.notebook1, pos=wx.Point(0, 0), size=wx.Size(504,
              438), style=wx.TAB_TRAVERSAL)  
        self.notebook1.AddPage(imageId=-1, page=self.resultpage1, select=True, text='Value')
        self.resultpage2 = panelResult2(id=wx.NewId(), name=_U('Diagram'),
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
    
    def updatePanel(self):
        #TCA should no run with present state(original)
        if (Status.ANo == -1):
            wx.MessageBox("Could not display TCA for unchecked state!")
            #self.Hide()
            self.main.tree.SelectItem(self.main.qCC, select=True)
            return False
        else:
            self.mod.updatePanel()
            return True                  
    
    def display(self):
        if not(self.updatePanel()):
            return
        
        self.mod.runTCAModule() 
        self.tbInflation.SetValue(str(self.mod.data.Inflation))
        self.tbNIR.SetValue(str(self.mod.data.NIR))
        self.tbCSDRate.SetValue(str(self.mod.data.CSDR))
        self.tbEnergyPrices.SetValue(str(self.mod.data.DEP))
        self.tbTimeFame.SetValue(str(self.mod.data.TimeFrame))
        
        self.resultpage1.display()        
        self.resultpage2.updatePanel()
        self.resultpage2.display()      

#Focus events------------------------------------------------------------------------------------------------
    def OnTbNIRKillFocus(self, event):
        try:
            self.mod.data.NIR = float(self.tbNIR.GetValue())
            if (self.mod.data.NIR<0)or(self.mod.data.NIR>100.0):
                raise
        except:
            wx.MessageBox(_("Nominal Interest rate: value between 0 and 100 expected."))
            self.tbNIR.SetFocus()
        event.Skip()

    def OnTbCSDRateKillFocus(self, event):
        try:
            self.mod.data.CSDR = float(self.tbCSDRate.GetValue())
            if (self.mod.data.CSDR<0)or(self.mod.data.CSDR>100.0):
                raise
        except:
            wx.MessageBox(_("Company specific discount rate: value between 0 and 100 expected."))
            self.tbCSDRate.SetFocus()
        event.Skip()

    def OnTbTimeFameKillFocus(self, event):
        try:
            self.mod.data.TimeFrame = int(self.tbTimeFame.GetValue())
            if (self.mod.data.TimeFrame<1)or(self.mod.data.TimeFrame>1000.0):
                raise
        except:
            wx.MessageBox(_("Time frame: value between 1 and 1000 expected."))
            self.tbTimeFame.SetFocus()
        event.Skip()

    def OnTbEnergyPricesKillFocus(self, event):
        try:
            self.mod.data.DEP = float(self.tbEnergyPrices.GetValue())
            if (self.mod.data.DEP<0)or(self.mod.data.DEP>100.0):
                raise
        except:
            wx.MessageBox(_("Development of energy prices: value between 0 and 100 expected."))
            self.tbEnergyPrices.SetFocus()
        event.Skip()

    
    def OnTbInflationKillFocus(self, event):
        try:
            self.mod.data.Inflation = float(self.tbInflation.GetValue())
            if (self.mod.data.Inflation<0)or(self.mod.data.Inflation>100.0):
                raise
        except:
            wx.MessageBox(_("Inflation rate: value between 0 and 100 expected."))
            self.tbInflation.SetFocus()
        
        event.Skip()

#TEXT EVENTS---------------------------------------------------------------------------------
    def OnTbNIRText(self, event):
        try:
            self.mod.data.NIR = float(self.tbNIR.GetValue())
            if (self.mod.data.NIR<0)or(self.mod.data.NIR>100.0):
                raise
        except:
            self.mod.NIR = 0
        event.Skip()

    def OnTbCSDRateText(self, event):
        try:
            self.mod.data.CSDR = float(self.tbCSDRate.GetValue())
            if (self.mod.data.CSDR<0)or(self.mod.data.CSDR>100.0):
                raise
        except:
            self.mod.data.CSDR = 0
        event.Skip()

    def OnTbTimeFameText(self, event):
        try:
            self.mod.data.TimeFrame = int(self.tbTimeFame.GetValue())
            if (self.mod.data.TimeFrame<1)or(self.mod.data.TimeFrame>1000.0):
                raise
        except:
            self.mod.data.TimeFrame = 1
        event.Skip()

    def OnTbEnergyPricesText(self, event):
        try:
            self.mod.data.DEP = float(self.tbEnergyPrices.GetValue())
            if (self.mod.data.DEP<0)or(self.mod.data.DEP>100.0):
                raise
        except:
            self.mod.data.DEP = 0
        event.Skip()
        
    def OnTbInflationText(self, event):
        try:
            self.mod.data.Inflation = float(self.tbInflation.GetValue())
            if (self.mod.data.Inflation<0)or(self.mod.data.Inflation>100.0):
                raise
        except:
            self.mod.data.Inflation = 0        
        event.Skip()
        
#-Nav----------------------------------------------------------------------------------------
    def OnBtnResetDataButton(self, event):
        dlg = wx.MessageDialog(None,_('Do you want to reset the data to proposed values from Einstein?\nAll your previous changes in the TCA will be lost.'),'Info',wx.YES_NO)
        if dlg.ShowModal()==wx.ID_YES:
            #print "reset tca data"
            self.mod.resetData()
            self.display()
        event.Skip()

    def OnBtnNextButton(self, event):
        self.Hide()
        self.mod.storeData()       
        self.main.tree.SelectItem(self.main.qECO1, select=False)
        #event.Skip()
         

    def OnBtnPrevModuleButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)
        event.Skip()

    def OnBtnNextModuleButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qCS, select=True)
        event.Skip()
   
    def OnNotebook1NotebookPageChanged(self, event):
        #To make sure add/remove proposal is corectly shon in both tab pages
        try:
            self.resultpage1.display()
            self.resultpage2.updatePanel()
            self.resultpage2.display()
        except:
            pass
        event.Skip()

    def OnBtnResetAllButton(self, event):     
        #print "------------------------------------"          
        if not(self.updatePanel()):
            return
        
        self.mod.resetTCA()
        self.display() 
        event.Skip()
