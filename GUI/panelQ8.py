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
#	PanelQ8: Building data
#
#==============================================================================
#
#	Version No.: 0.07
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger 02/05/2008
#                           Tom Sobota      05/05/2008
#                           Stoyan Danov    06/06/2008
#                           Stoyan Danov    17/06/2008
#                           Stoyan Danov    18/06/2008
#                           Hans Schweiger  18/06/2008
#
#       Changes to previous version:
#       02/05/08:       AlternativeProposalNo added in queries for table qproduct
#       05/05/2008      Changed display logic
#       06/06/2008      SD: new classes & texts, not functional still
#       17/06/2008 SD   adapt to new unitdict, change tc numbers to old one + add new
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
LABELWIDTH=200
TEXTENTRYWIDTH=160


class PanelQ8(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        self._init_ctrls(parent)
        self.__do_layout()

        self.buildingID = None

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ8', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()

        self.sizer_4_staticbox = wx.StaticBox(self, -1, _("Building list"))
        self.sizer_4_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_5_staticbox = wx.StaticBox(self, -1, _("Building (or part of building)"))
        self.sizer_5_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_6_staticbox = wx.StaticBox(self, -1, _("General data"))
        self.sizer_6_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_7_staticbox = wx.StaticBox(self, -1, _("Energy demand"))
        self.sizer_7_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_8_staticbox = wx.StaticBox(self, -1, _("Period of occupation"))
        self.sizer_8_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))


        # left side

        self.listBoxBuildingList = wx.ListBox(self,-1,choices=[])
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxBuildingListClick, self.listBoxBuildingList)

        self.buttonDeleteBuilding = wx.Button(self,-1,_("Delete building"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteBuilding, self.buttonDeleteBuilding)

        self.buttonAddBuilding = wx.Button(self,-1,_("Add building"))
	self.Bind(wx.EVT_BUTTON, self.OnButtonAddBuilding, self.buttonAddBuilding)


        # right side

#In staticbox: General data

        self.tc1 = TextEntry(self,maxchars=255,value='',
                             label=_("Building short name"),
                             tip=_("Give some brief name of the buildings to identify them in the reports"))


        self.tc2 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='AREA',
                              label=_("Constructed surface"),
                              tip=_("Surface limited by building's perimeter multiplied by number of floors"))

        self.tc3 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='AREA',
                              label=_("Useful surface"),
                              tip=_("Total useful surface of building (excluding walls)"))

        self.tc4 = TextEntry(self,maxchars=255,value='',
                             label=_("Use of the building"),
                             tip=_("Specify use, e.g. offices, production, storage,..."))


#In staticbox: Energy demand
        
        self.tc5 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='POWER',
                              label=_("Maximum heating power"),
                              tip=_("Maximum heating power (without including the security coefficient of the equipment)"))

        self.tc6 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='POWER',
                              label=_("Maximum cooling power"),
                              tip=_(" "))

        self.tc7 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='ENERGY',
                              label=_("Annual heating demand"),
                              tip=_("Thermal demand (useful heat and cold). Indicate MONTHLY data in a separate table (if available)"))

        self.tc8 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='ENERGY',
                              label=_("Annual demand of air conditioning"),
                              tip=_(" "))

        self.tc9 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='VOLUME',
                              label=_("Daily consumption of  DHW"),
                              tip=_("Only consumption of hot water that is not included yet in ''Processes''"))


#In staticbox: Period of occupation
        
        self.tc10 = FloatEntry(self,#SD:change type of entry?? -> time start - time stop?? or change tip: hours of occupation per day??
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict=None,
                              label=_("Hours of occupation"),
                              tip=_("Hours of occupation of the building, during which heating and air conditionning is active"))

        self.tc11 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict=None,
                              label=_("Days of use per year"),
                              tip=_(" "))

        self.tc12_10 = DateEntry(self,
                              value='',
                              label=_("Start period 1"),
                              tip=_("Period of year that the building is not used"))

        self.tc12_11 = DateEntry(self,
                              value='',
                              label=_("Stop period 1"),
                              tip=_("Period of year that the building is not used"))

#### CHECK CHECK CHECK Tom => please check the use of these labels ...
        self.st12 = Label(self, [self.tc12_10,self.tc12_11], _("Holidays period"),
                           [_("Holidays period (from)"),_("Holidays period (to)")])

        self.tc12_20 = DateEntry(self,
                              value='',
                              label=_("Start period 2"),
                              tip=_("Period of year that the building is not used"))

        self.tc12_21 = DateEntry(self,
                              value='',
                              label=_("Stop period 2"),
                              tip=_("Period of year that the building is not used"))

        self.tc12_30 = DateEntry(self,
                              value='',
                              label=_("Start period 3"),
                              tip=_("Period of year that the building is not used"))

        self.tc12_31 = DateEntry(self,
                              value='',
                              label=_("Stop period 3"),
                              tip=_("Period of year that the building is not used"))


        self.tc13_1 = DateEntry(self,
                              value='',
                              label=_("Start of heating period"),
                              tip=_(" "))

        self.tc13_2 = DateEntry(self,
                              value='',
                              label=_("Stop of heating period"),
                              tip=_(" "))
        self.st13 = Label(self,[self.tc13_1,self.tc13_2],_("Heating period"),
                          [_("Heating period (from)"), _("Heating period (to)")])

        self.tc14_1 = DateEntry(self,
                              value='',
                              label=_("Start of air conditioning period"),
                              tip=_(" "))

        self.tc14_2 = DateEntry(self,
                              value='',
                              label=_("Stop of air conditioning period"),
                              tip=_(" "))

        self.st14 = Label(self,[self.tc14_1,self.tc14_2],_("Air cond. period"),
                          [_("Air conditioning period (from)"), _("Air conditioning period (to)")])

        self.buttonOK = wx.Button(self,wx.ID_OK, label=_("OK"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL, label=_("Cancel"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_tc12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_tc13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_tc14 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.FlexGridSizer(14, 2, 1, 2) #r,c,vsep,hsep
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.VERTICAL)
        sizer_4.Add(self.listBoxBuildingList, 1, wx.EXPAND, 0)
        sizer_4.Add(self.buttonDeleteBuilding, 0, wx.EXPAND, 0)
        sizer_4.Add(self.buttonAddBuilding, 0, wx.EXPAND, 2)
        sizer_3.Add(sizer_4, 1, wx.EXPAND, 0)

        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)
        sizer_5.Add(grid_sizer_1, 1, wx.EXPAND, 2)


        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL
        flagText = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL

#HS: 2008-06-18: st's eliminated from grid sizer (except st12,13,14)
#        grid_sizer_1.Add(self.st1, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc1, 0, flagText, 0)
#        grid_sizer_1.Add(self.st2, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc2, 0, flagText, 0)
#        grid_sizer_1.Add(self.st3, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc3, 0, flagText, 0)
#        grid_sizer_1.Add(self.st4, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc4, 0, flagText, 0)
#        grid_sizer_1.Add(self.st5, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc5, 0, flagText, 0)
#        grid_sizer_1.Add(self.st6, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc6, 0, flagText, 0)
#        grid_sizer_1.Add(self.st7, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc7, 0, flagText, 0)
#        grid_sizer_1.Add(self.st8, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc8, 0, flagText, 0)
#        grid_sizer_1.Add(self.st9, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc9, 0, flagText, 0)
#        grid_sizer_1.Add(self.st10, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc10, 0, flagText, 0)
#        grid_sizer_1.Add(self.st11, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc11, 0, flagText, 0)

        grid_sizer_1.Add(self.st12, 0, flagLabel, 0)
        sizer_tc12.Add(self.tc12_10, 0, flagText, 0)
        sizer_tc12.Add(self.tc12_11, 0, flagText, 0)
        grid_sizer_1.Add(sizer_tc12, 0, flagText, 0)

        grid_sizer_1.Add(self.st13, 0, flagLabel, 0)
        sizer_tc13.Add(self.tc13_1, 0, flagText, 0)
        sizer_tc13.Add(self.tc13_2, 0, flagText, 0)
        grid_sizer_1.Add(sizer_tc13, 0, flagLabel, 0)
        
        grid_sizer_1.Add(self.st14, 0, flagLabel, 0)
        sizer_tc14.Add(self.tc14_1, 0, flagText, 0)
        sizer_tc14.Add(self.tc14_2, 0, flagText, 0)
        grid_sizer_1.Add(sizer_tc14, 0, flagText, 0)
            
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)
        sizer_3.Add(sizer_5, 4, wx.LEFT|wx.RIGHT|wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_1.Add(sizerOKCancel, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer_1)
        self.Layout()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------


    def OnListBoxBuildingListClick(self, event):
        self.buildingName = str(self.listBoxBuildingList.GetStringSelection())
        buildings = Status.DB.qbuildings.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        q = buildings.BuildName[self.buildingName][0]
        self.buildingID = q.QBuildings_ID

        self.tc1.SetValue(str(q.BuildName))
        self.tc2.SetValue(str(q.BuildConstructSurface))
        self.tc3.SetValue(str(q.BuildUsefulSurface))
        self.tc4.SetValue(str(q.BuildUsage))
        self.tc5.SetValue(str(q.BuildMaxHP))
        self.tc6.SetValue(str(q.BuildMaxCP))
        self.tc7.SetValue(str(q.BuildAnnualHeating))
        self.tc8.SetValue(str(q.BuildAnnualAirCond))
        self.tc9.SetValue(str(q.BuildDailyDHW))
        self.tc10.SetValue(str(q.BuildHoursOccup))
        self.tc11.SetValue(str(q.BuildDaysInUse))
        self.tc12_10.SetValue(str(q.BuildHolidaysPeriodStart1))
        self.tc12_11.SetValue(str(q.BuildHolidaysPeriodStop1))
        self.tc12_20.SetValue(str(q.BuildHolidaysPeriodStart2))
        self.tc12_21.SetValue(str(q.BuildHolidaysPeriodStop2))
        self.tc12_30.SetValue(str(q.BuildHolidaysPeriodStart3))
        self.tc12_31.SetValue(str(q.BuildHolidaysPeriodStop3))
        self.tc13_1.SetValue(str(q.BuildHeatingPeriodStart))
        self.tc13_2.SetValue(str(q.BuildHeatingPeriodStop))
        self.tc14_1.SetValue(str(q.BuildAirCondPeriodStart))
        self.tc14_2.SetValue(str(q.BuildAirCondPeriodStop))
        #event.Skip()

    def OnButtonOK(self, event):
        event.Skip()

    def OnButtonCancel(self, event):
        self.clear()
        event.Skip()

    def OnButtonDeleteBuilding(self, event):
        Status.prj.deleteBuilding(self.buildingID)
        self.clear()
        self.fillPage()
        event.Skip()

    def OnButtonAddBuilding(self, event):
        if Status.PId <> 0:

            buildingName = self.check(self.tc1.GetValue())
            buildings = Status.DB.qbuildings.BuildName[self.tc1.GetValue()].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
            if buildingName <> 'NULL' and len(buildings) == 0:

                newID = Status.prj.addBuildingDummy()

                tmp = {
                    "Questionnaire_id":Status.PId,
                    "AlternativeProposalNo":Status.ANo,
                    "BuildName":self.check(self.tc1.GetValue()),
                    "BuildConstructSurface":self.check(self.tc2.GetValue()),
                    "BuildUsefulSurface":self.check(self.tc3.GetValue()),
                    "BuildUsage":self.check(self.tc4.GetValue()),
                    "BuildMaxHP":self.check(self.tc5.GetValue()),
                    "BuildMaxCP":self.check(self.tc6.GetValue()),
                    "BuildAnnualHeating":self.check(self.tc7.GetValue()),
                    "BuildAnnualAirCond":self.check(self.tc8.GetValue()),
                    "BuildDailyDHW":self.check(self.tc9.GetValue()),
                    "BuildHoursOccup":self.check(self.tc10.GetValue()),
                    "BuildDaysInUse":self.check(self.tc11.GetValue()),
                    "BuildHolidaysPeriodStart1":self.check(self.tc12_10.GetValue()),
                    "BuildHolidaysPeriodStop1":self.check(self.tc12_11.GetValue()),
                    "BuildHolidaysPeriodStart2":self.check(self.tc12_20.GetValue()),
                    "BuildHolidaysPeriodStop2":self.check(self.tc12_21.GetValue()),
                    "BuildHolidaysPeriodStart3":self.check(self.tc12_30.GetValue()),
                    "BuildHolidaysPeriodStop3":self.check(self.tc12_31.GetValue()),
                    "BuildHeatingPeriodStart":self.check(self.tc13_1.GetValue()),
                    "BuildHeatingPeriodStop":self.check(self.tc13_2.GetValue()),
                    "BuildAirCondPeriodStart":self.check(self.tc14_1.GetValue()),
                    "BuildAirCondPeriodStop":self.check(self.tc14_2.GetValue())
                    }

                q = Status.DB.qbuildings.QBuildings_ID[newID][0]
                q.update(tmp)
                Status.SQL.commit()
                self.fillBuildingList()

            elif buildingName <> 'NULL' and len(buildings) == 1:

                tmp = {
                    "BuildName":self.check(self.tc1.GetValue()),
                    "BuildConstructSurface":self.check(self.tc2.GetValue()),
                    "BuildUsefulSurface":self.check(self.tc3.GetValue()),
                    "BuildUsage":self.check(self.tc4.GetValue()),
                    "BuildMaxHP":self.check(self.tc5.GetValue()),
                    "BuildMaxCP":self.check(self.tc6.GetValue()),
                    "BuildAnnualHeating":self.check(self.tc7.GetValue()),
                    "BuildAnnualAirCond":self.check(self.tc8.GetValue()),
                    "BuildDailyDHW":self.check(self.tc9.GetValue()),
                    "BuildHoursOccup":self.check(self.tc10.GetValue()),
                    "BuildDaysInUse":self.check(self.tc11.GetValue()),
                    "BuildHolidaysPeriodStart1":self.check(self.tc12_10.GetValue()),
                    "BuildHolidaysPeriodStop1":self.check(self.tc12_11.GetValue()),
                    "BuildHolidaysPeriodStart2":self.check(self.tc12_20.GetValue()),
                    "BuildHolidaysPeriodStop2":self.check(self.tc12_21.GetValue()),
                    "BuildHolidaysPeriodStart3":self.check(self.tc12_30.GetValue()),
                    "BuildHolidaysPeriodStop3":self.check(self.tc12_31.GetValue()),
                    "BuildHeatingPeriodStart":self.check(self.tc13_1.GetValue()),
                    "BuildHeatingPeriodStop":self.check(self.tc13_2.GetValue()),
                    "BuildAirCondPeriodStart":self.check(self.tc14_1.GetValue()),
                    "BuildAirCondPeriodStop":self.check(self.tc14_2.GetValue())
                    }
                q = buildings[0]
                q.update(tmp)
                Status.SQL.commit()
                self.fillBuildingList()

            else:
                self.showError("BuildingName have to be an uniqe value!")


#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------

    def display(self):
        self.clear()
        self.fillPage()
        self.Show()

    def fillBuildingList(self):
        self.listBoxBuildingList.Clear()
        buildings = Status.DB.qbuildings.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(buildings) > 0:
            for building in buildings:
                self.listBoxBuildingList.Append (str(building.BuildName))


    def fillPage(self):
	self.fillBuildingList()

    def check(self, value):
        if value <> "" and value <> "None":
            return value
        else:
            return 'NULL'

    def clear(self):
        self.tc1.SetValue('')
        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
        self.tc6.SetValue('')
        self.tc7.SetValue('')
        self.tc8.SetValue('')
        self.tc9.SetValue('')
        self.tc10.SetValue('')
        self.tc11.SetValue('')
        self.tc12_10.SetValue('')
        self.tc12_11.SetValue('')
        self.tc12_20.SetValue('')
        self.tc12_21.SetValue('')
        self.tc12_30.SetValue('')
        self.tc12_31.SetValue('')
        self.tc13_1.SetValue('')
        self.tc13_2.SetValue('')
        self.tc14_1.SetValue('')
        self.tc14_2.SetValue('')
