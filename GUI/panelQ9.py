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
#	Version No.: 0.09
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota      06/05/2008
#                           Stoyan Danov    09/06/2008
#                           Stoyan Danov    17/06/2008
#                           Stoyan Danov    18/06/2008
#                           Hans Schweiger  18/06/2008
#                           Tom Sobota      03/07/2008
#                           Hans Schweiger  03/07/2008
#                           Hans Schweiger  07/07/2008
#                           Hans Schweiger  17/09/2008
#                           Stoyan Danov    13/10/2008
#                           Florian Jöbstl  24/10/2008
#
#       Changes to previous version:
#       06/05/2008      Changed display logic
#       09/06/2008      Changed texts GUI
#       17/06/2008 SD   adapt to new unitdict
#       18/06/2008 SD   create display(), add imports
#                  HS: bug corrections and clean-up
#       03/07/2008: TS  general layout fix.
#                 : HS  some minor retouch in text and colour
#       07/07/2008: HS  bug-fix: self.check -> GUITools-check
#                       (compatibility with Tom's new FloatEntry)
#       17/09/2008: HS  adaptation to new nomenclature of TCA
#       13/10/2008: SD  change _() to _U()
#       24/10/2008: FJ  added updateOM() - function to sum fields and check
#                                          value consistency 
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
from einstein.modules.messageLogger import *
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

def _U(text):
    return unicode(_(text),"utf-8")

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
        self.notebook.AddPage(self.page0, _U('Parameters and management'))

        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page1, _U('Operation and maintenance'))
        #
        # frames
        #
        self.frame_management = wx.StaticBox(self.page0, -1, _U("Management of energetic services"))
        self.frame_management.SetForegroundColour(TITLE_COLOR)
        self.frame_management.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_parameters = wx.StaticBox(self.page0, -1, _U("Parameters used in the economic and comparative analysis of the possible alternatives"))
        self.frame_parameters.SetForegroundColour(TITLE_COLOR)
        self.frame_parameters.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_costs = wx.StaticBox(self.page1, -1, _U("Yearly operation and maintenance costs"))
        self.frame_costs.SetForegroundColour(TITLE_COLOR)
        self.frame_costs.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        #
        # labels
        #

        self.labelSpc0= wx.StaticText(self.page1, -1,'')
        self.label_14 = wx.StaticText(self.page1, -1, _U("Total costs\n[EUR]"))
        self.label_15 = wx.StaticText(self.page1, -1, _U("Utilities and\noperating materials\n[EUR]"))
        self.label_16 = wx.StaticText(self.page1, -1, _U("Labour costs\n[EUR]"))
        self.label_17 = wx.StaticText(self.page1, -1, _U("External costs\n[EUR]"))
        self.label_18 = wx.StaticText(self.page1, -1, _U("Regulatory compliance,\ninsurance and\nfuture liability costs\n[EUR]"))

        # set font for frames
        # 1. save actual font parameters on the stack
        fp.pushFont()
        # 2. change size and weight
        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
        self.frame_costs.SetFont(fp.getFont())
        self.frame_parameters.SetFont(fp.getFont())
        self.frame_management.SetFont(fp.getFont())
        # set font for labels
        fp.changeFont(size=8, weight = wx.NORMAL)
        self.label_14.SetFont(fp.getFont())
        self.label_15.SetFont(fp.getFont())
        self.label_16.SetFont(fp.getFont())
        self.label_17.SetFont(fp.getFont())
        self.label_18.SetFont(fp.getFont())
        # restore font
        fp.popFont()
        #
        # left tab controls
        # tab 0 - parameters and management
        #
        fs = FieldSizes(wHeight=HEIGHT,wLabel=LABEL_WIDTH_LEFT_TOP,
                       wData=DATA_ENTRY_WIDTH_LEFT,wUnits=UNITS_WIDTH)


        # tab 0 top side. parameters

        self.tc1 = FloatEntry(self.page0, decimals=1, minval=0., maxval=1.e+4, value=0.,
                              unitdict='GROWTHRATE',
                              label=_U("General inflation rate"),
                              tip=_U("Specify the rate of prices variation estimated for the useful life of the installations (e.g. in the next 15-20 years)"))

        self.tc2 = FloatEntry(self.page0, decimals=1, minval=0., maxval=1.e+4, value=0.,
                              unitdict='GROWTHRATE',
                              label=_U("Rate of increment of energy prices"),
                              tip=_U("Specify the rate of prices variation estimated for the useful life of the installations (e.g. in the next 15-20 years)"))

        self.tc3 = FloatEntry(self.page0, decimals=1, minval=0., maxval=1.e+4, value=0.,
                              unitdict='GROWTHRATE',
                              label=_U("Nominal rate of interest for external financing of installations"),
                              tip=_U("Specify the rate of prices variation estimated for the useful life of the installations (e.g. in the next 15-20 years)"))

        self.tc4 = FloatEntry(self.page0, decimals=1, minval=0., maxval=1.e+4, value=0.,
                              unitdict='FRACTION',
                              label=_U("Percentage of external financing for installations"),
                              tip=_U("Percentage of the external financing for the inversions"))

        self.tc4b = FloatEntry(self.page0, decimals=1, minval=0., maxval=1.e+4, value=0.,
                              unitdict='GROWTHRATE',
                              label=_U("Company specific discount rate"),
                              tip=_U(" "))
        self.tc5 = FloatEntry(self.page0, decimals=1, minval=0., maxval=1.e+4, value=0.,
                              unitdict='LONGTIME',
                              label=_U("Time for economic amortization of installations"),
                              tip=_U("Amortization time"))

        fs = FieldSizes(wLabel=LABEL_WIDTH_LEFT_MIDDLE)


        # tab 0 bottom side. energy management
        self.checkBox6 = wx.CheckBox(self.page0, -1, _U("An energy management system is already implemented"))
        self.checkBox6.SetValue(False)
        self.checkBox6.SetFont(fp.getFont())
        self.checkBox7 = wx.CheckBox(self.page0, -1, _U("The energy management is externalized"))
        self.checkBox7.SetValue(False)
        self.checkBox7.SetFont(fp.getFont())


        #
        # right tab controls
        # tab 1 - operation and maintenance costs
        #
        fs = FieldSizes(wHeight=HEIGHT,wLabel=LABEL_WIDTH_RIGHT,
                       wData=DATA_ENTRY_WIDTH_RIGHT,wUnits=UNITS_WIDTH)
        

        self.label_9 = wx.StaticText(self.page1, -1, _U("General maintenance"))
        self.tc10_1 = wx.TextCtrl(self.page1,-1, '')
        self.tc10_2 = wx.TextCtrl(self.page1,-1, '')
        self.tc10_3 = wx.TextCtrl(self.page1,-1, '')
        self.tc10_4 = wx.TextCtrl(self.page1,-1, '')
        self.tc10_5 = wx.TextCtrl(self.page1,-1, '')
        
        self.label_10 = wx.StaticText(self.page1, -1, _U("Buildings"))
        self.tc11_1 = wx.TextCtrl(self.page1,-1, '')
        self.tc11_2 = wx.TextCtrl(self.page1,-1, '')
        self.tc11_3 = wx.TextCtrl(self.page1,-1, '')
        self.tc11_4 = wx.TextCtrl(self.page1,-1, '')
        self.tc11_5 = wx.TextCtrl(self.page1,-1, '')
        
        self.label_11 = wx.StaticText(self.page1, -1, _U("Machines and equipment for processes"))
        self.tc12_1 = wx.TextCtrl(self.page1,-1, '')
        self.tc12_2 = wx.TextCtrl(self.page1,-1, '')
        self.tc12_3 = wx.TextCtrl(self.page1,-1, '')
        self.tc12_4 = wx.TextCtrl(self.page1,-1, '')
        self.tc12_5 = wx.TextCtrl(self.page1,-1, '')
        
        self.label_12 = wx.StaticText(self.page1, -1, _U("Generation and distribution of heat and cold"))
        self.tc13_1 = wx.TextCtrl(self.page1,-1, '')
        self.tc13_2 = wx.TextCtrl(self.page1,-1, '')
        self.tc13_3 = wx.TextCtrl(self.page1,-1, '')
        self.tc13_4 = wx.TextCtrl(self.page1,-1, '')
        self.tc13_5 = wx.TextCtrl(self.page1,-1, '')
        
        self.label_13 = wx.StaticText(self.page1, -1, _U("Total"))
        self.tc14_1 = wx.TextCtrl(self.page1,-1, '')
        self.tc14_2 = wx.TextCtrl(self.page1,-1, '')
        self.tc14_3 = wx.TextCtrl(self.page1,-1, '')
        self.tc14_4 = wx.TextCtrl(self.page1,-1, '')
        self.tc14_5 = wx.TextCtrl(self.page1,-1, '')

        # restore font
        fp.pushFont()
        #
        fp.changeFont(size=8,weight=wx.NORMAL)
        self.label_9.SetFont(fp.getFont())
        self.label_10.SetFont(fp.getFont())
        self.label_11.SetFont(fp.getFont())
        self.label_12.SetFont(fp.getFont())
        self.label_13.SetFont(fp.getFont())

        # restore font
        fp.popFont()
        #
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
        sizerP0PartTop.Add(self.tc4b, 0, flagText, VSEP_LEFT)
        sizerP0PartTop.Add(self.tc5, 0, flagText, VSEP_LEFT)
        sizerP0Parts.Add(sizerP0PartTop,2,0,0)

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
        sizerP1 = wx.FlexGridSizer(6, 6, 1, 2) #r,c,vsep,hsep
        sizerP1.Add(self.labelSpc0,0,0,0)
        sizerP1.Add(self.label_14,0,flagText,0)
        sizerP1.Add(self.label_15,0,flagText,0)
        sizerP1.Add(self.label_16,0,flagText,0)
        sizerP1.Add(self.label_17,0,flagText,0)
        sizerP1.Add(self.label_18,0,flagText,0)
        sizerP1.Add(self.label_9,0,flagLabel,0)
        sizerP1.Add(self.tc10_1,0,0,0)
        sizerP1.Add(self.tc10_2,0,0,0)
        sizerP1.Add(self.tc10_3,0,0,0)
        sizerP1.Add(self.tc10_4,0,0,0)
        sizerP1.Add(self.tc10_5,0,0,0)
        sizerP1.Add(self.label_10,0,flagLabel,0)
        sizerP1.Add(self.tc11_1,0,0,0)
        sizerP1.Add(self.tc11_2,0,0,0)
        sizerP1.Add(self.tc11_3,0,0,0)
        sizerP1.Add(self.tc11_4,0,0,0)
        sizerP1.Add(self.tc11_5,0,0,0)
        sizerP1.Add(self.label_11,0,flagLabel,0)
        sizerP1.Add(self.tc12_1,0,0,0)
        sizerP1.Add(self.tc12_2,0,0,0)
        sizerP1.Add(self.tc12_3,0,0,0)
        sizerP1.Add(self.tc12_4,0,0,0)
        sizerP1.Add(self.tc12_5,0,0,0)
        sizerP1.Add(self.label_12,0,flagLabel,0)
        sizerP1.Add(self.tc13_1,0,0,0)
        sizerP1.Add(self.tc13_2,0,0,0)
        sizerP1.Add(self.tc13_3,0,0,0)
        sizerP1.Add(self.tc13_4,0,0,0)
        sizerP1.Add(self.tc13_5,0,0,0)
        sizerP1.Add(self.label_13,0,flagLabel,0)
        sizerP1.Add(self.tc14_1,0,0,0)
        sizerP1.Add(self.tc14_2,0,0,0)
        sizerP1.Add(self.tc14_3,0,0,0)
        sizerP1.Add(self.tc14_4,0,0,0)
        sizerP1.Add(self.tc14_5,0,0,0)
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
        self.updateOM()
        
        if Status.PId <> 0 and \
		len(Status.DB.questionnaire.Questionnaire_ID[Status.PId]) == 1:
            tmp = {
                "InflationRate":check(self.tc1.GetValue()),
                "FuelPriceRate":check(self.tc2.GetValue()),
                "InterestExtFinancing":check(self.tc3.GetValue()),
                "PercentExtFinancing":check(self.tc4.GetValue()),
                "CompSpecificDiscountRate":check(self.tc4b.GetValue()),
                "AmortisationTime":check(self.tc5.GetValue()),
                "OMGenTot":check(self.tc10_1.GetValue()),
                "OMGenUtilities":check(self.tc10_2.GetValue()),
                "OMGenLabour":check(self.tc10_3.GetValue()),
                "OMGenExternal":check(self.tc10_4.GetValue()),
                "OMGenRegulatory":check(self.tc10_5.GetValue()),
                "OMBuildTot":check(self.tc11_1.GetValue()),
                "OMBuildUtilities":check(self.tc11_2.GetValue()),
                "OMBuildLabour":check(self.tc11_3.GetValue()),
                "OMBuildExternal":check(self.tc11_4.GetValue()),
                "OMBuildRegulatory":check(self.tc11_5.GetValue()),
                "OMMachEquipTot":check(self.tc12_1.GetValue()),
                "OMMachEquipUtilities":check(self.tc12_2.GetValue()),
                "OMMachEquipLabour":check(self.tc12_3.GetValue()),
                "OMMachEquipExternal":check(self.tc12_4.GetValue()),
                "OMMachEquipRegulatory":check(self.tc12_5.GetValue()),
                "OMHCGenDistTot":check(self.tc13_1.GetValue()),
                "OMHCGenDistUtilities":check(self.tc13_2.GetValue()),
                "OMHCGenDistLabour":check(self.tc13_3.GetValue()),
                "OMHCGenDistExternal":check(self.tc13_4.GetValue()),
                "OMHCGenDistRegulatory":check(self.tc13_5.GetValue()),
                "OMTotalTot":check(self.tc14_1.GetValue()),
                "OMTotalUtilities":check(self.tc14_2.GetValue()),
                "OMTotalLabour":check(self.tc14_3.GetValue()),
                "OMTotalExternal":check(self.tc14_4.GetValue()),
                "OMTotalRegulatory":check(self.tc14_5.GetValue())
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
        self.updateOM(doWarnings = True)
        self.Show()

    def clear(self):
        self.checkBox6.SetValue(False)
        self.checkBox7.SetValue(False)
        self.tc1.entry.Clear()
        self.tc2.entry.Clear()
        self.tc3.entry.Clear()
        self.tc4.entry.Clear()
        self.tc4b.entry.Clear()
        self.tc5.entry.Clear()
        self.tc10_1.Clear()
        self.tc10_2.Clear()
        self.tc10_3.Clear()
        self.tc10_4.Clear()
        self.tc10_5.Clear()
        self.tc11_1.Clear()
        self.tc11_2.Clear()
        self.tc11_3.Clear()
        self.tc11_4.Clear()
        self.tc11_5.Clear()
        self.tc12_1.Clear()
        self.tc12_2.Clear()
        self.tc12_3.Clear()
        self.tc12_4.Clear()
        self.tc12_5.Clear()
        self.tc13_1.Clear()
        self.tc13_2.Clear()
        self.tc13_3.Clear()
        self.tc13_4.Clear()
        self.tc13_5.Clear()
        self.tc14_1.Clear()
        self.tc14_2.Clear()
        self.tc14_3.Clear()
        self.tc14_4.Clear()
        self.tc14_5.Clear()


    def fillPage(self):
	if Status.PId == 0:
	    return

	q = Status.DB.questionnaire.Questionnaire_ID[Status.PId][0]
	self.tc1.SetValue(str(q.InflationRate))
	self.tc2.SetValue(str(q.FuelPriceRate))
	self.tc3.SetValue(str(q.InterestExtFinancing))
	self.tc4.SetValue(str(q.PercentExtFinancing))
	self.tc4b.SetValue(str(q.CompSpecificDiscountRate))
	self.tc5.SetValue(str(q.AmortisationTime))
	self.tc10_1.SetValue(str(q.OMGenTot))
	self.tc10_2.SetValue(str(q.OMGenUtilities))
	self.tc10_3.SetValue(str(q.OMGenLabour))
	self.tc10_4.SetValue(str(q.OMGenExternal))
	self.tc10_5.SetValue(str(q.OMGenRegulatory))
	self.tc11_1.SetValue(str(q.OMBuildTot))
	self.tc11_2.SetValue(str(q.OMBuildUtilities))
	self.tc11_3.SetValue(str(q.OMBuildLabour))
	self.tc11_4.SetValue(str(q.OMBuildExternal))
	self.tc11_5.SetValue(str(q.OMBuildRegulatory))
	self.tc12_1.SetValue(str(q.OMMachEquipTot))
	self.tc12_2.SetValue(str(q.OMMachEquipUtilities))
	self.tc12_3.SetValue(str(q.OMMachEquipLabour))
	self.tc12_4.SetValue(str(q.OMMachEquipExternal))
	self.tc12_5.SetValue(str(q.OMMachEquipRegulatory))
	self.tc13_1.SetValue(str(q.OMHCGenDistTot))
	self.tc13_2.SetValue(str(q.OMHCGenDistUtilities))
	self.tc13_3.SetValue(str(q.OMHCGenDistLabour))
	self.tc13_4.SetValue(str(q.OMHCGenDistExternal))
	self.tc13_5.SetValue(str(q.OMHCGenDistRegulatory))
	self.tc14_1.SetValue(str(q.OMTotalTot))
	self.tc14_2.SetValue(str(q.OMTotalUtilities))
	self.tc14_3.SetValue(str(q.OMTotalLabour))
	self.tc14_4.SetValue(str(q.OMTotalExternal))
	self.tc14_5.SetValue(str(q.OMTotalRegulatory))

	if q.EnergyManagExisting is None:
	    self.checkBox6.SetValue(False)
	else:
	    self.checkBox6.SetValue(bool(q.EnergyManagExisting))

	if q.EnergyManagExternal is None:
	    self.checkBox7.SetValue(False)
	else:
	    self.checkBox7.SetValue(bool(q.EnergyManagExternal))


    def __lockFields(self,fields):
        for field in fields:
            field.Enabled = False
    
    def __getValueSecure(self,obj):
    # reads value from a textfield and returns it as float 
    # if value is not a float 0.0 is returned
        str = obj.GetValue()        
        try: return float(str)
        except: return 0.0    
        

    def __checkFields(self,fields,override_if_not_match_total = False,doWarnings = False):
    # fields = [<name>,<totalfield>,[<listofsubfields>]]
    # override_if_not_match_total : if TRUE the value from the totalfield will be
    #                               overridden by the calculated sum     
        for category in fields:
            name        = category[0]  
            totalField  = category[1]
            valueFields = category[2]            
            sum = 0.0
            for valueField in valueFields:
                sum += self.__getValueSecure(valueField)
            totalValue = self.__getValueSecure(totalField)
            if (totalValue != sum)and(doWarnings):
                logWarning(_("Yearly OM: total from database does not match sum from values for: "+name))
            if (override_if_not_match_total):
                totalField.SetValue(str(sum))

    def updateOM(self,doWarnings = False):
        
        fields = [self.tc10_1,self.tc11_1,self.tc12_1,self.tc13_1,self.tc14_1,self.tc14_2,self.tc14_3,self.tc14_4,self.tc14_5]
        self.__lockFields(fields)
        
        fields = []
        #               NAME                                          TOTAL FIELD  SUBFIELDS
        fields.append(["General maintenance"                         ,self.tc10_1,[self.tc10_2,self.tc10_3,self.tc10_4,self.tc10_5]])
        fields.append(["Buildings"                                   ,self.tc11_1,[self.tc11_2,self.tc11_3,self.tc11_4,self.tc11_5]])
        fields.append(["Machines and equipment for processes"        ,self.tc12_1,[self.tc12_2,self.tc12_3,self.tc12_4,self.tc12_5]])
        fields.append(["Generation and distribution of heat and cold",self.tc13_1,[self.tc13_2,self.tc13_3,self.tc13_4,self.tc13_5]])      
        #check subtotals ; Total costs
        self.__checkFields(fields,override_if_not_match_total = True,doWarnings = doWarnings)
  
        fields = []
        #               NAME                              TOTAL FIELD  SUBFIELDS
        fields.append(["Total Costs"                      ,self.tc14_1,[self.tc10_1,self.tc11_1,self.tc12_1,self.tc13_1]])
        fields.append(["Utilities and operating materials",self.tc14_2,[self.tc10_2,self.tc11_2,self.tc12_2,self.tc13_2]])
        fields.append(["Labour costs"                     ,self.tc14_3,[self.tc10_3,self.tc11_3,self.tc12_3,self.tc13_3]])
        fields.append(["External costs"                   ,self.tc14_4,[self.tc10_4,self.tc11_4,self.tc12_4,self.tc13_4]])
        fields.append(["Regulatory"                       ,self.tc14_5,[self.tc10_5,self.tc11_5,self.tc12_5,self.tc13_5]])
        #check totals ; Total of Total costs
        self.__checkFields(fields,override_if_not_match_total = True,doWarnings = doWarnings)    
      

