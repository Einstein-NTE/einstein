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
#	Version No.: 0.03
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger 02/05/2008
#                           Tom Sobota      05/05/2008
#
#       Changes to previous version:
#       02/05/08:       AlternativeProposalNo added in queries for table qproduct
#       05/05/2008      Changed display logic
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
from wx.lib.stattext import *
import pSQL
from status import Status

# constants
LABELWIDTH=200
TEXTENTRYWIDTH=160


class Label2(wx.lib.stattext.GenStaticText):
    # same as Label but there are two or more associated text controls
    # to the label
    w0 = None
    w1 = None
    def __init__(self,parent,txtlist,text,tiplist,width0=None,width1=None):
        wx.lib.stattext.GenStaticText.__init__(self,ID=-1,parent=parent,label='',
                                              style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
        print repr(text)
        self.SetLabel(text)
        h = self.GetMinHeight()
        if width0 is None:
            if Label.w0 is not None:
                self.SetMinSize((Label.w0, h))
        else:
            Label.w0 = width0
            self.SetMinSize((Label.w0, h))
        if width1 is None:
            if Label.w1 is not None:
                for tc  in txtlist:
                    tc.SetMinSize((Label.w1, h))
        else:
            Label.w1 = width1
            for tc  in txtlist:
                tc.SetMinSize((width1, h))

        self.SetToolTipString(text)
        for i in range(len(txtlist)):
            txtlist[i].SetToolTipString(tiplist[i])

class Label(wx.lib.stattext.GenStaticText):
    # auxiliary class for labels (static text)
    # will show a short descriptive string and
    # generate a longer tooltip.
    # the tooltip is also associated to the text control
    #
    w0 = None
    w1 = None
    def __init__(self,parent,txtctrl,text,tip,width0=None,width1=None):
        wx.lib.stattext.GenStaticText.__init__(self,ID=-1,parent=parent,label='',
                                              style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
        self.SetLabel(text)
        h = self.GetMinHeight()
        if width0 is None:
            if Label.w0 is not None:
                self.SetMinSize((Label.w0, h))
        else:
            Label.w0 = width0
            self.SetMinSize((Label.w0, h))
        if width1 is None:
            if Label.w1 is not None:
                txtctrl.SetMinSize((Label.w1, h))
        else:
            txtctrl.SetMinSize((width1, h))
            Label.w1 = width1

        self.SetToolTipString(tip)
        self.SetHelpText(u'esto es un help')
        txtctrl.SetToolTipString(tip)


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


        # left side

        self.listBoxBuildingList = wx.ListBox(self,-1,choices=[])
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxBuildingListClick, self.listBoxBuildingList)

        self.buttonDeleteBuilding = wx.Button(self,-1,_("Delete building"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteBuilding, self.buttonDeleteBuilding)

        self.buttonAddBuilding = wx.Button(self,-1,_("Add building"))
	self.Bind(wx.EVT_BUTTON, self.OnButtonAddBuilding, self.buttonAddBuilding)

        # right side
        
        self.tc1 = wx.TextCtrl(self,-1,'')
        self.st1 = Label(self, self.tc1, _("Building name"), _("Building short name"),
                         LABELWIDTH, TEXTENTRYWIDTH)

        self.tc2 = wx.TextCtrl(self,-1,'')
        self.st2 = Label(self, self.tc2, _("Constructed surface"), _("Constructed surface (m2)"))

        self.tc3 = wx.TextCtrl(self,-1,'')
        self.st3 = Label(self, self.tc3, _("Useful surface"), _("Useful surface (m2)"))

        self.tc4 = wx.TextCtrl(self,-1,'')
        self.st4 = Label(self, self.tc4, _("Use"), _("Use of the building"))

        self.tc5 = wx.TextCtrl(self,-1,'')
        self.st5 = Label(self, self.tc5, _("Max. heating power"), _("Maximum heating power (kW)"))

        self.tc6 = wx.TextCtrl(self,-1,'')
        self.st6 = Label(self, self.tc6, _("Max. cooling power"), _("Maximum cooling power (kW)"))

        self.tc7 = wx.TextCtrl(self,-1,'')
        self.st7 = Label(self, self.tc7, _("Heating demand"), _("Annual heating demand (MWh / year)"))

        self.tc8 = wx.TextCtrl(self,-1,'')
        self.st8 = Label(self, self.tc8, _("Air conditioning demand"),
                         _("Annual demand of air conditioning (MWh / year)"))

        self.tc9 = wx.TextCtrl(self,-1,'')
        self.st9 = Label(self, self.tc9, _("Consumption of DHW"), _("Daily consumption of DHW (l/day)"))

        self.tc10 = wx.TextCtrl(self,-1,'')
        self.st10 = Label(self, self.tc10, _("Hours of occupation"), _("Hours of occupation (h/day)"))

        self.tc11 = wx.TextCtrl(self,-1,'')
        self.st11 = Label(self, self.tc11, _("Days of use"), _("Days of use per year (days/year)"))

        self.tc12_1 = wx.TextCtrl(self,-1,'')
        self.tc12_2 = wx.TextCtrl(self,-1,'')
        self.st12 = Label2(self, [self.tc12_1,self.tc12_2], _("Holidays period"),
                           [_("Holidays period (from)"),_("Holidays period (to)")])

        self.tc13_1 = wx.TextCtrl(self,-1,'')
        self.tc13_2 = wx.TextCtrl(self,-1,'')
        self.st13 = Label2(self,[self.tc13_1,self.tc13_2],_("Heating period"),
                          [_("Heating period (from)"), _("Heating period (to)")])

        self.tc14_1 = wx.TextCtrl(self,-1,'')
        self.tc14_2 = wx.TextCtrl(self,-1,'')
        self.st14 = Label2(self,[self.tc14_1,self.tc14_2],_("Air cond. period"),
                          [_("Air conditioning period (from)"), _("Air conditioning period (to)")])


        self.buttonOK = wx.Button(self,wx.ID_OK, label=_("OK"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)

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
        grid_sizer_1.Add(self.st1, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc1, 0, flagText, 0)
        grid_sizer_1.Add(self.st2, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc2, 0, flagText, 0)
        grid_sizer_1.Add(self.st3, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc3, 0, flagText, 0)
        grid_sizer_1.Add(self.st4, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc4, 0, flagText, 0)
        grid_sizer_1.Add(self.st5, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc5, 0, flagText, 0)
        grid_sizer_1.Add(self.st6, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc6, 0, flagText, 0)
        grid_sizer_1.Add(self.st7, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc7, 0, flagText, 0)
        grid_sizer_1.Add(self.st8, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc8, 0, flagText, 0)
        grid_sizer_1.Add(self.st9, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc9, 0, flagText, 0)
        grid_sizer_1.Add(self.st10, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc10, 0, flagText, 0)
        grid_sizer_1.Add(self.st11, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc11, 0, flagText, 0)

        grid_sizer_1.Add(self.st12, 0, flagLabel, 0)
        sizer_tc12.Add(self.tc12_1, 0, flagText, 0)
        sizer_tc12.Add(self.tc12_2, 0, flagText, 0)
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
        self.tc12_1.SetValue(str(q.BuildHolidaysPeriodStart))
        self.tc12_2.SetValue(str(q.BuildHolidaysPeriodStop))
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
                    "BuildHolidaysPeriodStart":self.check(self.tc12_1.GetValue()),
                    "BuildHolidaysPeriodStop":self.check(self.tc12_2.GetValue()),
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
                    "BuildHolidaysPeriodStart":self.check(self.tc12_1.GetValue()),
                    "BuildHolidaysPeriodStop":self.check(self.tc12_2.GetValue()),
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
        self.tc12_1.SetValue('')
        self.tc12_2.SetValue('')
        self.tc13_1.SetValue('')
        self.tc13_2.SetValue('')
        self.tc14_1.SetValue('')
        self.tc14_2.SetValue('')
