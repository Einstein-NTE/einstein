# -*- coding: iso-8859-15 -*-
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	PanelQ9: Economic data
#
#==============================================================================
#
#	Version No.: 0.08
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota      06/05/2008
#                           Stoyan Danov    09/06/2008
#                           Stoyan Danov    17/06/2008
#                           Stoyan Danov    18/06/2008
#                           Hans Schweiger  18/06/2008
#                           Tom Sobota      03/07/2008
#                           Hans Schweiger  03/07/2008
#
#       Changes to previous version:
#       06/05/2008      Changed display logic
#       09/06/2008      Changed texts GUI
#       17/06/2008 SD   adapt to new unitdict
#       18/06/2008 SD   create display(), add imports
#                  HS: bug corrections and clean-up
#       03/07/2008 TS   general layout fix.
#                       some minor retouch in text and colour
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
import pSQL
from status import Status
from GUITools import *
from displayClasses import *
from units import *
from fonts import *

# constants that control the default sizes
# 1. font sizes
TYPE_SIZE_NORMAL        =   9
TYPE_SIZE_LEFT          =   TYPE_SIZE_NORMAL
TYPE_SIZE_MIDDLE        =   TYPE_SIZE_NORMAL
TYPE_SIZE_RIGHT         =   TYPE_SIZE_NORMAL
TYPE_SIZE_TITLES        =  10

# 2. field sizes
HEIGHT                  =  32
HEIGHT_RIGHT            =  32

LABEL_WIDTH_LEFT_TOP    = 300
LABEL_WIDTH_LEFT_MIDDLE =  20
LABEL_WIDTH_RIGHT       = 200

DATA_ENTRY_WIDTH_RIGHT  = 100
DATA_ENTRY_WIDTH_LEFT   = 100

UNITS_WIDTH             =  90

# 3. vertical separation between fields
VSEP_LEFT               =   2
VSEP_RIGHT              =   2

ORANGE = '#FF6000'
TITLE_COLOR = ORANGE

class PanelQ9(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        self._init_ctrls(parent)
        self.__do_layout()


    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ9', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()

        # access to font properties object
        fp = FontProperties()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page0, _('Parameters and management'))

        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page1, _('Operation and maintenance'))
        #
        # frames
        #
        self.frame_management = wx.StaticBox(self.page0, -1, _("Management of energetic services"))
        self.frame_management.SetForegroundColour(TITLE_COLOR)
        self.frame_management.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_parameters = wx.StaticBox(self.page0, -1, _("Parameters used in the economic and comparative analysis of the possible alternatives"))
        self.frame_parameters.SetForegroundColour(TITLE_COLOR)
        self.frame_parameters.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_costs = wx.StaticBox(self.page1, -1, _("Yearly operation and maintenance costs"))
        self.frame_costs.SetForegroundColour(TITLE_COLOR)
        self.frame_costs.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        #
        # labels
        #
        self.label_funding = wx.StaticText(self.page0, -1, _("Public funding for energy\nsaving measures"))
        self.label_credit = wx.StaticText(self.page0, -1, _("Type (credit, subvention)"))

        self.labelSpc0= wx.StaticText(self.page1, -1,'')
        self.label_14 = wx.StaticText(self.page1, -1, _("Total costs\n[EUR]"))
        self.label_15 = wx.StaticText(self.page1, -1, _("Own personnel\n[EUR]"))
        self.label_16 = wx.StaticText(self.page1, -1, _("External personnel \n[EUR]"))
        self.label_17 = wx.StaticText(self.page1, -1, _("Spare parts and\n fungible assets\n[EUR]"))

        # set font for frames
        # 1. save actual font parameters on the stack
        fp.pushFont()
        # 2. change size and weight
        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
        self.frame_costs.SetFont(fp.getFont())
        self.frame_parameters.SetFont(fp.getFont())
        self.frame_management.SetFont(fp.getFont())
        # set font for labels
        fp.changeFont(size=TYPE_SIZE_NORMAL)
        self.label_funding.SetFont(fp.getFont())
        self.label_credit.SetFont(fp.getFont())
        self.label_14.SetFont(fp.getFont())
        self.label_15.SetFont(fp.getFont())
        self.label_16.SetFont(fp.getFont())
        self.label_17.SetFont(fp.getFont())
        # restore font
        fp.popFont()
        #
        # left tab controls
        # tab 0 - parameters and management
        #
        fs = FieldSizes(wHeight=HEIGHT,wLabel=LABEL_WIDTH_LEFT_TOP,
                       wData=DATA_ENTRY_WIDTH_LEFT,wUnits=UNITS_WIDTH)


        # tab 0 top side. parameters

        self.tc1 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='GROWTHRATE',
                              label=_("General inflation rate"),
                              tip=_("Specify the rate of prices variation estimated for the useful life of the installations (e.g. in the next 15-20 years)"))

        self.tc2 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='GROWTHRATE',
                              label=_("Rate of increment of energy prices"),
                              tip=_("Specify the rate of prices variation estimated for the useful life of the installations (e.g. in the next 15-20 years)"))

        self.tc3 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='GROWTHRATE',
                              label=_("Nominal rate of interest for external financing of installations"),
                              tip=_("Specify the rate of prices variation estimated for the useful life of the installations (e.g. in the next 15-20 years)"))

        self.tc4 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='FRACTION',
                              label=_("Percentage of external financing for installations"),
                              tip=_("Percentage of the external financing for the inversions"))

        self.tc5 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='LONGTIME',
                              label=_("Time for economic amortization of installations"),
                              tip=_("Amortization time"))

        fs = FieldSizes(wLabel=LABEL_WIDTH_LEFT_MIDDLE)


        self.tc6_1 = TextEntry(self.page0,maxchars=255,value='')
        self.tc6_2 = TextEntry(self.page0,maxchars=255,value='')

        self.tc7_1 = TextEntry(self.page0,maxchars=255,value='')
        self.tc7_2 = TextEntry(self.page0,maxchars=255,value='')

        self.tc8_1 = TextEntry(self.page0,maxchars=255,value='')
        self.tc8_2 = TextEntry(self.page0,maxchars=255,value='')

        self.tc9_1 = TextEntry(self.page0,maxchars=255,value='')
        self.tc9_2 = TextEntry(self.page0,maxchars=255,value='')


        # tab 0 bottom side. energy management
        self.checkBox6 = wx.CheckBox(self.page0, -1, _("An energy management system is already implemented"))
        self.checkBox6.SetValue(False)
        self.checkBox6.SetFont(fp.getFont())
        self.checkBox7 = wx.CheckBox(self.page0, -1, _("The energy management is externalized"))
        self.checkBox7.SetValue(False)
        self.checkBox7.SetFont(fp.getFont())


        #
        # right tab controls
        # tab 1 - operation and maintenance costs
        #
        fs = FieldSizes(wHeight=HEIGHT,wLabel=LABEL_WIDTH_RIGHT,
                       wData=DATA_ENTRY_WIDTH_RIGHT,wUnits=UNITS_WIDTH)
        

        self.label_9 = wx.StaticText(self.page1, -1, _("General maintenance"))
        self.tc10_1 = wx.TextCtrl(self.page1,-1, '')
        self.tc10_2 = wx.TextCtrl(self.page1,-1, '')
        self.tc10_3 = wx.TextCtrl(self.page1,-1, '')
        self.tc10_4 = wx.TextCtrl(self.page1,-1, '')
        
        self.label_10 = wx.StaticText(self.page1, -1, _("Buildings"))
        self.tc11_1 = wx.TextCtrl(self.page1,-1, '')
        self.tc11_2 = wx.TextCtrl(self.page1,-1, '')
        self.tc11_3 = wx.TextCtrl(self.page1,-1, '')
        self.tc11_4 = wx.TextCtrl(self.page1,-1, '')
        
        self.label_11 = wx.StaticText(self.page1, -1, _("Machines and equipment for processes"))
        self.tc12_1 = wx.TextCtrl(self.page1,-1, '')
        self.tc12_2 = wx.TextCtrl(self.page1,-1, '')
        self.tc12_3 = wx.TextCtrl(self.page1,-1, '')
        self.tc12_4 = wx.TextCtrl(self.page1,-1, '')
        
        self.label_12 = wx.StaticText(self.page1, -1, _("Generation and distribution of heat and cold"))
        self.tc13_1 = wx.TextCtrl(self.page1,-1, '')
        self.tc13_2 = wx.TextCtrl(self.page1,-1, '')
        self.tc13_3 = wx.TextCtrl(self.page1,-1, '')
        self.tc13_4 = wx.TextCtrl(self.page1,-1, '')
        
        self.label_13 = wx.StaticText(self.page1, -1, _("Total"))
        self.tc14_1 = wx.TextCtrl(self.page1,-1, '')
        self.tc14_2 = wx.TextCtrl(self.page1,-1, '')
        self.tc14_3 = wx.TextCtrl(self.page1,-1, '')
        self.tc14_4 = wx.TextCtrl(self.page1,-1, '')

        #
        # buttons
        #
        self.buttonOK = wx.Button(self,wx.ID_OK,"OK")
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,"Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        # recover previous font parameters from the stack
        fp.popFont()

    def __do_layout(self):
        flagText = wx.ALIGN_CENTER_VERTICAL|wx.TOP
        flagLabel = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT

        # global sizer for panel. Contains notebook w/two tabs + buttons Cancel and Ok
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)
        
        # sizer for left tab
        # tab 0, parameters and management
        sizerPage0= wx.StaticBoxSizer(self.frame_parameters, wx.VERTICAL)
        # top part: parameters
        sizerP0Parts = wx.BoxSizer(wx.VERTICAL)
        sizerP0PartTop = wx.BoxSizer(wx.VERTICAL)
        sizerP0PartTop.Add(self.tc1, 0, flagText, VSEP_LEFT)
        sizerP0PartTop.Add(self.tc2, 0, flagText, VSEP_LEFT)
        sizerP0PartTop.Add(self.tc3, 0, flagText, VSEP_LEFT)
        sizerP0PartTop.Add(self.tc4, 0, flagText, VSEP_LEFT)
        sizerP0PartTop.Add(self.tc5, 0, flagText, VSEP_LEFT)
        sizerP0Parts.Add(sizerP0PartTop,2,0,0)

        # middle part: funding
        sizerP0PartMiddle = wx.FlexGridSizer(5, 2, 1, 2) #r,c,vsep,hsep
        sizerP0PartMiddle.Add(self.label_funding,0,flagLabel,0)
        sizerP0PartMiddle.Add(self.label_credit,0,flagLabel,0)
        sizerP0PartMiddle.Add(self.tc6_1,0,flagText,0)
        sizerP0PartMiddle.Add(self.tc6_2,0,flagText,0)
        sizerP0PartMiddle.Add(self.tc7_1,0,flagText,0)
        sizerP0PartMiddle.Add(self.tc7_2,0,flagText,0)
        sizerP0PartMiddle.Add(self.tc8_1,0,flagText,0)
        sizerP0PartMiddle.Add(self.tc8_2,0,flagText,0)
        sizerP0PartMiddle.Add(self.tc9_1,0,flagText,0)
        sizerP0PartMiddle.Add(self.tc9_2,0,flagText,0)
        sizerP0Parts.Add(sizerP0PartMiddle,2,wx.LEFT,70)

        # bottom part: management
        sizerP0Bottom= wx.StaticBoxSizer(self.frame_management, wx.VERTICAL)
        sizerP0Bottom.Add(self.checkBox6,0,flagText,0)
        sizerP0Bottom.Add(self.checkBox7,0,flagText,0)
        sizerP0Parts.Add(sizerP0Bottom,1,wx.EXPAND|wx.ALL,10)

        sizerPage0.Add(sizerP0Parts,1,wx.EXPAND|wx.TOP,10)
        self.page0.SetSizer(sizerPage0)
        #
        # sizer for right tab
        # tab 1, operation and maintenance costs
        sizerPage1 = wx.StaticBoxSizer(self.frame_costs, wx.VERTICAL)
        sizerP1 = wx.FlexGridSizer(6, 5, 1, 2) #r,c,vsep,hsep
        sizerP1.Add(self.labelSpc0,0,0,0)
        sizerP1.Add(self.label_14,0,flagText,0)
        sizerP1.Add(self.label_15,0,flagText,0)
        sizerP1.Add(self.label_16,0,flagText,0)
        sizerP1.Add(self.label_17,0,flagText,0)
        sizerP1.Add(self.label_9,0,flagLabel,0)
        sizerP1.Add(self.tc10_1,0,0,0)
        sizerP1.Add(self.tc10_2,0,0,0)
        sizerP1.Add(self.tc10_3,0,0,0)
        sizerP1.Add(self.tc10_4,0,0,0)
        sizerP1.Add(self.label_10,0,flagLabel,0)
        sizerP1.Add(self.tc11_1,0,0,0)
        sizerP1.Add(self.tc11_2,0,0,0)
        sizerP1.Add(self.tc11_3,0,0,0)
        sizerP1.Add(self.tc11_4,0,0,0)
        sizerP1.Add(self.label_11,0,flagLabel,0)
        sizerP1.Add(self.tc12_1,0,0,0)
        sizerP1.Add(self.tc12_2,0,0,0)
        sizerP1.Add(self.tc12_3,0,0,0)
        sizerP1.Add(self.tc12_4,0,0,0)
        sizerP1.Add(self.label_12,0,flagLabel,0)
        sizerP1.Add(self.tc13_1,0,0,0)
        sizerP1.Add(self.tc13_2,0,0,0)
        sizerP1.Add(self.tc13_3,0,0,0)
        sizerP1.Add(self.tc13_4,0,0,0)
        sizerP1.Add(self.label_13,0,flagLabel,0)
        sizerP1.Add(self.tc14_1,0,0,0)
        sizerP1.Add(self.tc14_2,0,0,0)
        sizerP1.Add(self.tc14_3,0,0,0)
        sizerP1.Add(self.tc14_4,0,0,0)
        sizerPage1.Add(sizerP1,2,wx.EXPAND|wx.TOP,10)

        self.page1.SetSizer(sizerPage1)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)

        sizerGlobal.Add(self.notebook, 3, wx.EXPAND, 0)
        sizerGlobal.Add(sizerOKCancel, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizerGlobal)
        self.Layout()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------

    def OnButtonCancel(self, event):
        self.clear()
        event.Skip()
        
    def OnButtonOK(self, event):
        if Status.PId <> 0 and \
		len(Status.DB.questionnaire.Questionnaire_ID[Status.PId]) == 1:
            tmp = {
                "InflationRate":self.check(self.tc1.GetValue()),
                "FuelPriceRate":self.check(self.tc2.GetValue()),
                "InterestExtFinancing":self.check(self.tc3.GetValue()),
                "PercentExtFinancing":self.check(self.tc4.GetValue()),
                "AmortisationTime":self.check(self.tc5.GetValue()),
                "OMGenTot":self.check(self.tc10_1.GetValue()),
                "OMGenOP":self.check(self.tc10_2.GetValue()),
                "OMGenEP":self.check(self.tc10_3.GetValue()),
                "OMGenFung":self.check(self.tc10_4.GetValue()),
                "OMBuildTot":self.check(self.tc11_1.GetValue()),
                "OMBuildOP":self.check(self.tc11_2.GetValue()),
                "OMBuildEP":self.check(self.tc11_3.GetValue()),
                "OMBiuildFung":self.check(self.tc11_4.GetValue()),
                "OMMachEquipTot":self.check(self.tc12_1.GetValue()),
                "OMMachEquipOP":self.check(self.tc12_2.GetValue()),
                "OMMachEquipEP":self.check(self.tc12_3.GetValue()),
                "OMMachEquipFung":self.check(self.tc12_4.GetValue()),
                "OMHCGenDistTot":self.check(self.tc13_1.GetValue()),
                "OMHCGenDistOP":self.check(self.tc13_2.GetValue()),
                "OMHCGenDistEP":self.check(self.tc13_3.GetValue()),
                "OMHCGenDistFung":self.check(self.tc13_4.GetValue()),
                "OMTotalTot":self.check(self.tc14_1.GetValue()),
                "OMTotalOP":self.check(self.tc14_2.GetValue()),
                "OMTotalEP":self.check(self.tc14_3.GetValue()),
                "OMTotalFung":self.check(self.tc14_4.GetValue())
                  }

            q = Status.DB.questionnaire.Questionnaire_ID[Status.PId][0]
            q.update(tmp)
            Status.SQL.commit()


#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------

    def display(self):
        self.clear()
        self.fillPage()
        self.Show()

    def clear(self):
        self.checkBox6.SetValue(False)
        self.checkBox7.SetValue(False)
        self.tc1.entry.Clear()
        self.tc2.entry.Clear()
        self.tc3.entry.Clear()
        self.tc4.entry.Clear()
        self.tc5.entry.Clear()
        self.tc10_1.Clear()
        self.tc10_2.Clear()
        self.tc10_3.Clear()
        self.tc10_4.Clear()
        self.tc11_1.Clear()
        self.tc11_2.Clear()
        self.tc11_3.Clear()
        self.tc11_4.Clear()
        self.tc12_1.Clear()
        self.tc12_2.Clear()
        self.tc12_3.Clear()
        self.tc12_4.Clear()
        self.tc13_1.Clear()
        self.tc13_2.Clear()
        self.tc13_3.Clear()
        self.tc13_4.Clear()
        self.tc14_1.Clear()
        self.tc14_2.Clear()
        self.tc14_3.Clear()
        self.tc14_4.Clear()


    def fillPage(self):
	if Status.PId == 0:
	    return

	q = Status.DB.questionnaire.Questionnaire_ID[Status.PId][0]
	self.tc1.SetValue(str(q.InflationRate))
	self.tc2.SetValue(str(q.FuelPriceRate))
	self.tc3.SetValue(str(q.InterestExtFinancing))
	self.tc4.SetValue(str(q.PercentExtFinancing))
	self.tc5.SetValue(str(q.AmortisationTime))
	self.tc10_1.SetValue(str(q.OMGenTot))
	self.tc10_2.SetValue(str(q.OMGenOP))
	self.tc10_3.SetValue(str(q.OMGenEP))
	self.tc10_4.SetValue(str(q.OMGenFung))
	self.tc11_1.SetValue(str(q.OMBuildTot))
	self.tc11_2.SetValue(str(q.OMBuildOP))
	self.tc11_3.SetValue(str(q.OMBuildEP))
	self.tc11_4.SetValue(str(q.OMBiuildFung))
	self.tc12_1.SetValue(str(q.OMMachEquipTot))
	self.tc12_2.SetValue(str(q.OMMachEquipOP))
	self.tc12_3.SetValue(str(q.OMMachEquipEP))
	self.tc12_4.SetValue(str(q.OMMachEquipFung))
	self.tc13_1.SetValue(str(q.OMHCGenDistTot))
	self.tc13_2.SetValue(str(q.OMHCGenDistOP))
	self.tc13_3.SetValue(str(q.OMHCGenDistEP))
	self.tc13_4.SetValue(str(q.OMHCGenDistFung))
	self.tc14_1.SetValue(str(q.OMTotalTot))
	self.tc14_2.SetValue(str(q.OMTotalOP))
	self.tc14_3.SetValue(str(q.OMTotalEP))
	self.tc14_4.SetValue(str(q.OMTotalFung))

	if q.EnergyManagExisting is None:
	    self.checkBox6.SetValue(False)
	else:
	    self.checkBox6.SetValue(bool(q.EnergyManagExisting))

	if q.EnergyManagExternal is None:
	    self.checkBox7.SetValue(False)
	else:
	    self.checkBox7.SetValue(bool(q.EnergyManagExternal))



