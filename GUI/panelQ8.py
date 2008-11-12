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
#                           Tom Sobota      03/07/2008
#                           Hans Schweiger  07/07/2008
#                           Tom Sobota      07/07/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes to previous version:
#       02/05/08:       AlternativeProposalNo added in queries for table qproduct
#       05/05/2008      Changed display logic
#       06/06/2008      SD: new classes & texts, not functional still
#       17/06/2008 SD   adapt to new unitdict, change tc numbers to old one + add new
#       18/06/2008 SD   create display(), add imports
#                   HS: bug corrections and clean-up
#       03/07/2008 TS   general layout fix.
#       07/07/2008: HS  bug-fix: self.check - GUITools-check
#                       (compatibility with Tom's new FloatEntry)
#        7/07/2008 TS   Fixed buttons AddEquipment, DeleteEquipment
#       13/10/2008: SD  change _() to _U()
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
TYPE_SIZE_LEFT    =   9
TYPE_SIZE_MIDDLE  =   9
TYPE_SIZE_RIGHT   =   9
TYPE_SIZE_TITLES  =  10

# 2. field sizes
HEIGHT                 =  32
HEIGHT_RIGHT           =  32

LABEL_WIDTH_LEFT       = 300
LABEL_WIDTH_RIGHT      = 200

DATA_ENTRY_WIDTH_RIGHT = 100
DATA_ENTRY_WIDTH_LEFT  = 100

UNITS_WIDTH            =  90

# 3. vertical separation between fields
VSEP_LEFT              =   2
VSEP_RIGHT             =   2

ORANGE = '#FF6000'
TITLE_COLOR = ORANGE

def _U(text):
    return unicode(_(text),"utf-8")

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

        # access to font properties object
        fp = FontProperties()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page0, _U('General data'))

        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page1, _U('Occupation'))
        
        self.frame_building_list = wx.StaticBox(self.page0, -1, _U("Building list"))
        self.frame_building_list.SetForegroundColour(TITLE_COLOR)
        self.frame_building_list.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        #self.frame_building = wx.StaticBox(self.page0, -1, _U("Building (or part of building)"))
        self.frame_general_data = wx.StaticBox(self.page0, -1, _U("General data"))
        self.frame_general_data.SetForegroundColour(TITLE_COLOR)
        self.frame_general_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_energy_demand = wx.StaticBox(self.page0, -1, _U("Energy demand"))
        self.frame_energy_demand.SetForegroundColour(TITLE_COLOR)
        self.frame_energy_demand.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_occupation = wx.StaticBox(self.page1, -1, _U("Period of occupation"))
        self.frame_occupation.SetForegroundColour(TITLE_COLOR)
        self.frame_occupation.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        # set font for titles
        # 1. save actual font parameters on the stack
        fp.pushFont()
        # 2. change size and weight
        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
        self.frame_building_list.SetFont(fp.getFont())
        #self.frame_building.SetFont(fp.getFont())
        self.frame_general_data.SetFont(fp.getFont())
        self.frame_energy_demand.SetFont(fp.getFont())
        self.frame_occupation.SetFont(fp.getFont())
        # 3. recover previous font state
        fp.popFont()


        fs = FieldSizes(wHeight=HEIGHT,wLabel=LABEL_WIDTH_LEFT,
                       wData=DATA_ENTRY_WIDTH_LEFT,wUnits=UNITS_WIDTH)

        #
        # left tab controls
        # tab 0 - general data
        #
        # tab 0 left side. building list

        self.listBoxBuildingList = wx.ListBox(self.page0,-1,choices=[])
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxBuildingListClick, self.listBoxBuildingList)


        # tab 0 right side. data entries
        # tab 0 top staticbox: General data

        self.tc1 = TextEntry(self.page0,maxchars=255,value='',
                             label=_U("Building short name"),
                             tip=_U("Give some brief name of the buildings to identify them in the reports"))


        self.tc2 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='AREA',
                              label=_U("Constructed surface"),
                              tip=_U("Surface limited by building's perimeter multiplied by number of floors"))

        self.tc3 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='AREA',
                              label=_U("Useful surface"),
                              tip=_U("Total useful surface of building (excluding walls)"))

        self.tc4 = TextEntry(self.page0,maxchars=255,value='',
                             label=_U("Use of the building"),
                             tip=_U("Specify use, e.g. offices, production, storage,..."))


        # tab 0 bottom staticbox: Energy demand
        
        self.tc5 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='POWER',
                              label=_U("Maximum heating power"),
                              tip=_U("Maximum heating power (without including the security coefficient of the equipment)"))

        self.tc6 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='POWER',
                              label=_U("Maximum cooling power"),
                              tip=_U(" "))

        self.tc7 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='ENERGY',
                              label=_U("Annual heating demand"),
                              tip=_U("Thermal demand (useful heat and cold). Indicate MONTHLY data in a separate table (if available)"))

        self.tc8 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='ENERGY',
                              label=_U("Annual demand of air conditioning"),
                              tip=_U(" "))

        self.tc9 = FloatEntry(self.page0, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='VOLUME',
                              label=_U("Daily consumption of  DHW"),
                              tip=_U("Only consumption of hot water that is not included yet in 'Processes'"))

        #
        # right tab controls
        # tab 0 - Period of occupation
        #
        fs = FieldSizes(wHeight=HEIGHT,wLabel=LABEL_WIDTH_RIGHT,
                        wData=DATA_ENTRY_WIDTH_RIGHT,wUnits=UNITS_WIDTH)

        #SD:change type of entry?? -> time start - time stop?? or change tip: hours of occupation per day??
        self.tc10 = FloatEntry(self.page1, decimals=1, minval=0., maxval=999., value=0.,
                               unitdict=None,
                               label=_U("Hours of occupation"),
                               tip=_U("Hours of occupation of the building, during which heating and air conditionning is active"))

        self.tc11 = FloatEntry(self.page1, decimals=1, minval=0., maxval=999., value=0.,
                               unitdict=None,
                               label=_U("Days of use per year"),
                               tip=_U(" "))

        self.tc12_10 = DateEntry(self.page1, value='',
                              label=_U("Start holiday period 1"),
                              tip=_U("Period of year that the building is not used"))

        self.tc12_11 = DateEntry(self.page1, value='',
                              label=_U("Stop holiday period 1"),
                              tip=_U("Period of year that the building is not used"))

        self.tc12_20 = DateEntry(self.page1, value='',
                              label=_U("Start holiday period 2"),
                              tip=_U("Period of year that the building is not used"))

        self.tc12_21 = DateEntry(self.page1, value='',
                              label=_U("Stop holiday period 2"),
                              tip=_U("Period of year that the building is not used"))

        self.tc12_30 = DateEntry(self.page1, value='',
                              label=_U("Start holiday period 3"),
                              tip=_U("Period of year that the building is not used"))

        self.tc12_31 = DateEntry(self.page1, value='',
                              label=_U("Stop holiday period 3"),
                              tip=_U("Period of year that the building is not used"))


        self.tc13_1 = DateEntry(self.page1, value='',
                              label=_U("Start of heating period"),
                              tip=_U(" "))

        self.tc13_2 = DateEntry(self.page1, value='',
                              label=_U("Stop of heating period"),
                              tip=_U(" "))


        self.tc14_1 = DateEntry(self.page1, value='',
                              label=_U("Start of air\nconditioning period"),
                              tip=_U(" "))

        self.tc14_2 = DateEntry(self.page1, value='',
                              label=_U("Stop of air\nconditioning period"),
                              tip=_U(" "))

        #
        # buttons
        #
        self.buttonDeleteBuilding = wx.Button(self.page0,-1,_U("Delete building"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteBuilding, self.buttonDeleteBuilding)
        self.buttonDeleteBuilding.SetMinSize((136, 32))
        self.buttonDeleteBuilding.SetFont(fp.getFont())
        
        self.buttonAddBuilding = wx.Button(self.page0,-1,_U("Add building"))
	self.Bind(wx.EVT_BUTTON, self.OnButtonAddBuilding, self.buttonAddBuilding)
        self.buttonAddBuilding.SetMinSize((136, 32))
        self.buttonAddBuilding.SetFont(fp.getFont())
        
        self.buttonOK = wx.Button(self,wx.ID_OK, label=_U("OK"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL, label=_U("Cancel"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)

         # recover previous font parameters from the stack
        fp.popFont()
        
    def __do_layout(self):
        flagText = wx.ALIGN_CENTER_VERTICAL|wx.TOP

        # global sizer for panel. Contains notebook w/two tabs + buttons Cancel and Ok
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)
        
        # sizer for left tab
        # tab 0, general data
        sizerPage0 = wx.BoxSizer(wx.HORIZONTAL)
        # left part: listbox
        sizerP0Left= wx.StaticBoxSizer(self.frame_building_list, wx.VERTICAL)
        sizerP0Left.Add(self.listBoxBuildingList, 1, wx.EXPAND, 0)
        sizerP0Left.Add(self.buttonAddBuilding, 0, wx.ALIGN_RIGHT, 0)
        sizerP0Left.Add(self.buttonDeleteBuilding, 0, wx.ALIGN_RIGHT, 0)
        sizerPage0.Add(sizerP0Left,2,wx.EXPAND|wx.TOP,10)

        # right part: data entries
        sizerP0Right= wx.BoxSizer(wx.VERTICAL)
        sizerP0RightTop= wx.StaticBoxSizer(self.frame_general_data, wx.VERTICAL)
        sizerP0RightTop.Add(self.tc1, 0, flagText, VSEP_LEFT)
        sizerP0RightTop.Add(self.tc2, 0, flagText, VSEP_LEFT)
        sizerP0RightTop.Add(self.tc3, 0, flagText, VSEP_LEFT)
        sizerP0RightTop.Add(self.tc4, 0, flagText, VSEP_LEFT)
        sizerP0Right.Add(sizerP0RightTop,4,wx.EXPAND,0)
        
        sizerP0RightBottom= wx.StaticBoxSizer(self.frame_energy_demand, wx.VERTICAL)
        sizerP0RightBottom.Add(self.tc5, 0, flagText, VSEP_LEFT)
        sizerP0RightBottom.Add(self.tc6, 0, flagText, VSEP_LEFT)
        sizerP0RightBottom.Add(self.tc7, 0, flagText, VSEP_LEFT)
        sizerP0RightBottom.Add(self.tc8, 0, flagText, VSEP_LEFT)
        sizerP0RightBottom.Add(self.tc9, 0, flagText, VSEP_LEFT)
        sizerP0Right.Add(sizerP0RightBottom,4,wx.EXPAND,0)
        sizerPage0.Add(sizerP0Right,5,wx.EXPAND|wx.TOP,10)
        self.page0.SetSizer(sizerPage0)

        # sizer for right tab
        # tab 1, occupation

        sizerPage1 = wx.StaticBoxSizer(self.frame_occupation, wx.VERTICAL)
        grid_sizer_P1 = wx.FlexGridSizer(6, 2, 1, 2) #r,c,vsep,hsep
        grid_sizer_P1.Add(self.tc10, 0, flagText, 0)
        grid_sizer_P1.Add(self.tc11, 0, flagText, 0)
        grid_sizer_P1.Add(self.tc12_10, 0, flagText, 0)
        grid_sizer_P1.Add(self.tc12_11, 0, flagText, 0)
        grid_sizer_P1.Add(self.tc12_20, 0, flagText, 0)
        grid_sizer_P1.Add(self.tc12_21, 0, flagText, 0)
        grid_sizer_P1.Add(self.tc12_30, 0, flagText, 0)
        grid_sizer_P1.Add(self.tc12_31, 0, flagText, 0)
        grid_sizer_P1.Add(self.tc13_1, 0, flagText, 0)
        grid_sizer_P1.Add(self.tc13_2, 0, flagText, 0)
        grid_sizer_P1.Add(self.tc14_1, 0, flagText, 0)
        grid_sizer_P1.Add(self.tc14_2, 0, flagText, 0)
        sizerPage1.Add(grid_sizer_P1,0,wx.EXPAND|wx.TOP,10)

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


    def OnListBoxBuildingListClick(self, event):
        self.buildingName = self.listBoxBuildingList.GetStringSelection()
        buildings = Status.DB.qbuildings.Questionnaire_id[Status.PId].\
                    AlternativeProposalNo[Status.ANo]
        
        q = buildings.BuildName[check(self.buildingName)][0]
        self.buildingID = q.QBuildings_ID

        self.tc1.SetValue(q.BuildName)
        self.tc2.SetValue(str(q.BuildConstructSurface))
        self.tc3.SetValue(str(q.BuildUsefulSurface))
        self.tc4.SetValue(q.BuildUsage)
        self.tc5.SetValue(str(q.BuildMaxHP))
        self.tc6.SetValue(str(q.BuildMaxCP))
        self.tc7.SetValue(str(q.BuildAnnualHeating))
        self.tc8.SetValue(str(q.BuildAnnualAirCond))
        self.tc9.SetValue(str(q.BuildDailyDHW))
        self.tc10.SetValue(str(q.BuildHoursOccup))
        self.tc11.SetValue(str(q.BuildDaysInUse))
        self.tc12_10.SetValue(str(q.BuildHolidaysPeriodStart_1))
        self.tc12_11.SetValue(str(q.BuildHolidaysPeriodStop_1))
        self.tc12_20.SetValue(str(q.BuildHolidaysPeriodStart_2))
        self.tc12_21.SetValue(str(q.BuildHolidaysPeriodStop_2))
        self.tc12_30.SetValue(str(q.BuildHolidaysPeriodStart_3))
        self.tc12_31.SetValue(str(q.BuildHolidaysPeriodStop_3))
        self.tc13_1.SetValue(str(q.BuildHeatingPeriodStart))
        self.tc13_2.SetValue(str(q.BuildHeatingPeriodStop))
        self.tc14_1.SetValue(str(q.BuildAirCondPeriodStart))
        self.tc14_2.SetValue(str(q.BuildAirCondPeriodStop))
        #event.Skip()

    def OnButtonAddBuilding(self, event):
        self.clear()
        event.Skip()

    def OnButtonCancel(self, event):
        self.clear()
        event.Skip()

    def OnButtonDeleteBuilding(self, event):
        Status.prj.deleteBuilding(self.buildingID)
        self.clear()
        self.fillPage()
        event.Skip()

    def OnButtonOK(self, event):
        if Status.PId <> 0:

            buildingName = self.tc1.GetValue()
            buildings = Status.DB.qbuildings.BuildName[check(buildingName)].\
                        Questionnaire_id[Status.PId].\
                        AlternativeProposalNo[Status.ANo]
            
            if buildingName <> 'NULL' and len(buildings) == 0:

                newID = Status.prj.addBuildingDummy()

                tmp = {
                    "Questionnaire_id":Status.PId,
                    "AlternativeProposalNo":Status.ANo,
                    "BuildName":check(self.tc1.GetValue()),
                    "BuildConstructSurface":check(self.tc2.GetValue()),
                    "BuildUsefulSurface":check(self.tc3.GetValue()),
                    "BuildUsage":check(self.tc4.GetValue()),
                    "BuildMaxHP":check(self.tc5.GetValue()),
                    "BuildMaxCP":check(self.tc6.GetValue()),
                    "BuildAnnualHeating":check(self.tc7.GetValue()),
                    "BuildAnnualAirCond":check(self.tc8.GetValue()),
                    "BuildDailyDHW":check(self.tc9.GetValue()),
                    "BuildHoursOccup":check(self.tc10.GetValue()),
                    "BuildDaysInUse":check(self.tc11.GetValue()),
                    "BuildHolidaysPeriodStart_1":check(self.tc12_10.GetValue()),
                    "BuildHolidaysPeriodStop_1":check(self.tc12_11.GetValue()),
                    "BuildHolidaysPeriodStart_2":check(self.tc12_20.GetValue()),
                    "BuildHolidaysPeriodStop_2":check(self.tc12_21.GetValue()),
                    "BuildHolidaysPeriodStart_3":check(self.tc12_30.GetValue()),
                    "BuildHolidaysPeriodStop_3":check(self.tc12_31.GetValue()),
                    "BuildHeatingPeriodStart":check(self.tc13_1.GetValue()),
                    "BuildHeatingPeriodStop":check(self.tc13_2.GetValue()),
                    "BuildAirCondPeriodStart":check(self.tc14_1.GetValue()),
                    "BuildAirCondPeriodStop":check(self.tc14_2.GetValue())
                    }

                q = Status.DB.qbuildings.QBuildings_ID[newID][0]
                q.update(tmp)
                Status.SQL.commit()
                self.fillBuildingList()

            elif buildingName <> 'NULL' and len(buildings) == 1:

                tmp = {
                    "BuildName":check(self.tc1.GetValue()),
                    "BuildConstructSurface":check(self.tc2.GetValue()),
                    "BuildUsefulSurface":check(self.tc3.GetValue()),
                    "BuildUsage":check(self.tc4.GetValue()),
                    "BuildMaxHP":check(self.tc5.GetValue()),
                    "BuildMaxCP":check(self.tc6.GetValue()),
                    "BuildAnnualHeating":check(self.tc7.GetValue()),
                    "BuildAnnualAirCond":check(self.tc8.GetValue()),
                    "BuildDailyDHW":check(self.tc9.GetValue()),
                    "BuildHoursOccup":check(self.tc10.GetValue()),
                    "BuildDaysInUse":check(self.tc11.GetValue()),
                    "BuildHolidaysPeriodStart_1":check(self.tc12_10.GetValue()),
                    "BuildHolidaysPeriodStop_1":check(self.tc12_11.GetValue()),
                    "BuildHolidaysPeriodStart_2":check(self.tc12_20.GetValue()),
                    "BuildHolidaysPeriodStop_2":check(self.tc12_21.GetValue()),
                    "BuildHolidaysPeriodStart_3":check(self.tc12_30.GetValue()),
                    "BuildHolidaysPeriodStop_3":check(self.tc12_31.GetValue()),
                    "BuildHeatingPeriodStart":check(self.tc13_1.GetValue()),
                    "BuildHeatingPeriodStop":check(self.tc13_2.GetValue()),
                    "BuildAirCondPeriodStart":check(self.tc14_1.GetValue()),
                    "BuildAirCondPeriodStop":check(self.tc14_2.GetValue())
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
        self.main.showWarning(_U("You can fill in data if you are happy with this, but building H&C demand is not yet considered in this version of EINSTEIN"))

    def fillBuildingList(self):
        self.listBoxBuildingList.Clear()
        buildings = Status.DB.qbuildings.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(buildings) > 0:
            for building in buildings:
                self.listBoxBuildingList.Append(unicode(building.BuildName,"utf-8"))


    def fillPage(self):
	self.fillBuildingList()

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
