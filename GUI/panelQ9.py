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
#	Version No.: 0.06
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota      06/05/2008
#                           Stoyan Danov    09/06/2008
#                           Stoyan Danov    17/06/2008
#                           Stoyan Danov    18/06/2008
#                           Hans Schweiger  18/06/2008
#
#       Changes to previous version:
#       06/05/2008      Changed display logic
#       09/06/2008      Changed texts GUI
#       17/06/2008 SD   adapt to new unitdict
#       18/06/2008 SD   create display(), add imports
#                   HS: bug corrections and clean-up
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

# constants
LABELWIDTH=120
TEXTENTRYWIDTH=100


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

        self.buttonOK = wx.Button(self,wx.ID_OK,"OK")
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,"Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        self.sizer_6_staticbox = wx.StaticBox(self, -1, _("Operation and maintenance costs"))
        self.sizer_6_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_7_staticbox = wx.StaticBox(self, -1, _("Externalisation of energetic services"))
        self.sizer_7_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_5_staticbox = wx.StaticBox(self, -1, _("Parameters used in the economic and comparative analysis of the possible alternatives"))
        self.sizer_5_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.dummy1 = wx.StaticText(self, -1, "\n")
        self.dummy2 = wx.StaticText(self, -1, "\n")
        self.dummy3 = wx.StaticText(self, -1, "\n")

        #SD added
        self.tc1 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='GROWTHRATE',
                              label=_("General inflation rate [%]"),
                              tip=_("Specify the rate of prices variation estimated for the useful life of the installations (e.g. in the next 15-20 years)"))

        self.tc2 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='GROWTHRATE',
                              label=_("Rate of increment of energy prices [%]"),
                              tip=_("Specify the rate of prices variation estimated for the useful life of the installations (e.g. in the next 15-20 years)"))

        self.tc3 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='GROWTHRATE',
                              label=_("Nominal rate of interest for external financing of installations [%]"),
                              tip=_("Specify the rate of prices variation estimated for the useful life of the installations (e.g. in the next 15-20 years)"))

        self.tc4 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='FRACTION',
                              label=_("Percentage of external financing for installations"),
                              tip=_("Percentage of the external financing for the inversions"))

        self.tc5 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='LONGTIME',
                              label=_("Time for economic amortization of installations [years]"),
                              tip=_("Amortization time"))


        self.label_1 = wx.StaticText(self, -1, _("Public funding for energy\nsaving measures"))
        self.label_2 = wx.StaticText(self, -1, _("Type (credit,\n subvention)"))

        self.tc6_1 = wx.TextCtrl(self,-1, '')
        self.tc6_2 = wx.TextCtrl(self,-1, '')

        self.tc7_1 = wx.TextCtrl(self,-1, '')
        self.tc7_2 = wx.TextCtrl(self,-1, '')

        self.tc8_1 = wx.TextCtrl(self,-1, '')
        self.tc8_2 = wx.TextCtrl(self,-1, '')

        self.tc9_1 = wx.TextCtrl(self,-1, '')
        self.tc9_2 = wx.TextCtrl(self,-1, '')

        
        self.label_14 = wx.StaticText(self, -1, _("Total costs\n(EUR/year)"))
        self.label_15 = wx.StaticText(self, -1, _("Own personnel\n(EUR/year)"))
        self.label_16 = wx.StaticText(self, -1, _("External personnel \n(EUR/year)"))
        self.label_17 = wx.StaticText(self, -1, _("Spare parts and\n fungible assets\n(EUR/year)"))

        self.label_9 = wx.StaticText(self, -1, _("General maintenance"))
        self.tc10_1 = wx.TextCtrl(self,-1, '')
        self.tc10_2 = wx.TextCtrl(self,-1, '')
        self.tc10_3 = wx.TextCtrl(self,-1, '')
        self.tc10_4 = wx.TextCtrl(self,-1, '')
        
        self.label_10 = wx.StaticText(self, -1, _("Buildings"))
        self.tc11_1 = wx.TextCtrl(self,-1, '')
        self.tc11_2 = wx.TextCtrl(self,-1, '')
        self.tc11_3 = wx.TextCtrl(self,-1, '')
        self.tc11_4 = wx.TextCtrl(self,-1, '')
        
        self.label_11 = wx.StaticText(self, -1, _("Machines and equipment for processes"))
        self.tc12_1 = wx.TextCtrl(self,-1, '')
        self.tc12_2 = wx.TextCtrl(self,-1, '')
        self.tc12_3 = wx.TextCtrl(self,-1, '')
        self.tc12_4 = wx.TextCtrl(self,-1, '')
        
        self.label_12 = wx.StaticText(self, -1, _("Generation and distribution of heat and cold"))
        self.tc13_1 = wx.TextCtrl(self,-1, '')
        self.tc13_2 = wx.TextCtrl(self,-1, '')
        self.tc13_3 = wx.TextCtrl(self,-1, '')
        self.tc13_4 = wx.TextCtrl(self,-1, '')
        
        self.label_13 = wx.StaticText(self, -1, _("Total"))
        self.tc14_1 = wx.TextCtrl(self,-1, '')
        self.tc14_2 = wx.TextCtrl(self,-1, '')
        self.tc14_3 = wx.TextCtrl(self,-1, '')
        self.tc14_4 = wx.TextCtrl(self,-1, '')

        self.checkBox6 = wx.CheckBox(self, -1, _("An energy management system is already implemented"))
        self.checkBox6.SetValue(False)
        self.checkBox7 = wx.CheckBox(self, -1, _("The energy management is externalized"))
        self.checkBox7.SetValue(False)


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.StaticBoxSizer(self.sizer_6_staticbox, wx.VERTICAL)
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)

        labelFlags = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL

#HS2008-06-18: st's eliminated from grid sizer
        grid_sizer_2 = wx.FlexGridSizer(5, 2, 2, 0)
        grid_sizer_2.Add(self.dummy1, 0, 0, 0)
        grid_sizer_2.Add(self.dummy2, 0, 0, 0)
#        grid_sizer_2.Add(self.st1, 0, labelFlags, 0)
        grid_sizer_2.Add(self.tc1, 0, 0, 0)
#        grid_sizer_2.Add(self.st2, 0, labelFlags, 0)
        grid_sizer_2.Add(self.tc2, 0, 0, 0)
#        grid_sizer_2.Add(self.st3, 0, labelFlags, 0)
        grid_sizer_2.Add(self.tc3, 0, 0, 0)
#        grid_sizer_2.Add(self.st4, 0, labelFlags, 0)
        grid_sizer_2.Add(self.tc4, 0, 0, 0)
#        grid_sizer_2.Add(self.st5, 0, labelFlags, 0)
        grid_sizer_2.Add(self.tc5, 0, 0, 0)
        sizer_8.Add(grid_sizer_2, 2, wx.TOP|wx.EXPAND, 6)

        grid_sizer_1 = wx.FlexGridSizer(5, 2, 2, 2)
        grid_sizer_1.Add(self.label_1, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_1.Add(self.label_2, 0, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_1.Add(self.tc6_1, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.tc6_2, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.tc7_1, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.tc7_2, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.tc8_1, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.tc8_2, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.tc9_1, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.tc9_2, 0, wx.EXPAND, 0)
        sizer_8.Add(grid_sizer_1, 4, wx.LEFT|wx.TOP|wx.EXPAND, 6)
        sizer_5.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_5, 0, wx.EXPAND, 0)

        grid_sizer_3 = wx.FlexGridSizer(6, 5, 2, 2)
        grid_sizer_3.Add(self.dummy3, 0, 0, 0)
        grid_sizer_3.Add(self.label_14, 0, 0, 0)
        grid_sizer_3.Add(self.label_15, 0, 0, 0)
        grid_sizer_3.Add(self.label_16, 0, 0, 0)
        grid_sizer_3.Add(self.label_17, 0, 0, 0)
        grid_sizer_3.Add(self.label_9, 0, labelFlags, 0)
        grid_sizer_3.Add(self.tc10_1, 0, 0, 0)
        grid_sizer_3.Add(self.tc10_2, 0, 0, 0)
        grid_sizer_3.Add(self.tc10_3, 0, 0, 0)
        grid_sizer_3.Add(self.tc10_4, 0, 0, 0)
        grid_sizer_3.Add(self.label_10, 0, labelFlags, 0)
        grid_sizer_3.Add(self.tc11_1, 0, 0, 0)
        grid_sizer_3.Add(self.tc11_2, 0, 0, 0)
        grid_sizer_3.Add(self.tc11_3, 0, 0, 0)
        grid_sizer_3.Add(self.tc11_4, 0, 0, 0)
        grid_sizer_3.Add(self.label_11, 0, labelFlags, 0)
        grid_sizer_3.Add(self.tc12_1, 0, 0, 0)
        grid_sizer_3.Add(self.tc12_2, 0, 0, 0)
        grid_sizer_3.Add(self.tc12_3, 0, 0, 0)
        grid_sizer_3.Add(self.tc12_4, 0, 0, 0)
        grid_sizer_3.Add(self.label_12, 0, labelFlags, 0)
        grid_sizer_3.Add(self.tc13_1, 0, 0, 0)
        grid_sizer_3.Add(self.tc13_2, 0, 0, 0)
        grid_sizer_3.Add(self.tc13_3, 0, 0, 0)
        grid_sizer_3.Add(self.tc13_4, 0, 0, 0)
        grid_sizer_3.Add(self.label_13, 0, labelFlags, 0)
        grid_sizer_3.Add(self.tc14_1, 0, 0, 0)
        grid_sizer_3.Add(self.tc14_2, 0, 0, 0)
        grid_sizer_3.Add(self.tc14_3, 0, 0, 0)
        grid_sizer_3.Add(self.tc14_4, 0, 0, 0)
        sizer_6.Add(grid_sizer_3, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_10.Add(self.checkBox6, 0, 0, 0)
        sizer_10.Add(self.checkBox7, 0, 0, 0)
        sizer_9.Add(sizer_10, 1, wx.ALL|wx.EXPAND, 4)
        sizer_7.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_4.Add(sizer_7, 0, wx.EXPAND, 0)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.ALIGN_RIGHT, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.ALIGN_RIGHT, 2)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_1.Add(sizerOKCancel, 0, wx.ALIGN_RIGHT, 2)
        self.SetSizer(sizer_1)
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



