# -*- coding: iso-8859-15 -*-
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    PanelDBCHP: Database Design Assistant
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by:     Manuel Wallner 08/03/2010
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
import pSQL
from status import Status
from displayClasses import *
from GUITools import *
from units import *
from fonts import *
from einstein.modules.messageLogger import *

from einstein.GUI.panelDBBase import PanelDBBase

HEIGHT = 20
LABEL_WIDTH_LEFT = 140
DATA_ENTRY_WIDTH_LEFT = 140
UNITS_WIDTH = 55

VSEP = 4

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

class PanelDBCHP(PanelDBBase):
    def __init__(self, parent, title, closeOnOk = False):
        self.parent = parent
        self.title = title
        self.closeOnOk = closeOnOk
        self.name = "CHP"
        self._init_ctrls(parent)
        self._init_grid(100)
        self.__do_layout()
        self.clear()
        self.fillEquipmentList()
        self.fillChoices()

    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        PanelDBBase.__init__(self, self.parent, "Edit DBCHP", self.name)

        # DBCHP_ID needs to remain as first entry
        self.colLabels = "DBCHP_ID", "Manufacturer", "CHPequip", "Type", "SubType", "CHPPt"

        self.db = Status.DB.dbchp
        self.table = "dbchp"
        self.identifier = self.colLabels[0]
        self.type = self.colLabels[3]
        self.subtype = self.colLabels[4]

        # access to font properties object
        fp = FontProperties()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.notebook = wx.Notebook(self, -1, style = 0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page0, _U('Summary table'))
        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page1, _U('Descriptive Data'))
        self.page2 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page2, _U('Technical Data'))
        self.page3 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page3, _U('Heat source / sink'))
        self.page4 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page4, _U('Economic Parameters'))

        #
        # tab 0 - Summary table
        #
        self.frame_summary_table = wx.StaticBox(self.page0, -1, _U("Summary table"))
        self.frame_summary_table.SetForegroundColour(TITLE_COLOR)
        self.frame_summary_table.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_summary_table.SetFont(fp.getFont())
        fp.popFont()

        self.grid = wx.grid.Grid(name = 'summarytable', parent = self.page0,
                                 pos = wx.Point(42, 32), style = 0)

        self.tc_type = ChoiceEntry(self.page0,
                                   values = [],
                                   label = _U("Type"),
                                   tip = _U("Show only equipment of type"))

        self.tc_subtype = ChoiceEntry(self.page0,
                                      values = [],
                                      label = _U("Subtype"),
                                      tip = _U("Show only equipment of subtype"))

        #
        # tab 1 - Descriptive Data
        #
        self.frame_descriptive_data = wx.StaticBox(self.page1, -1, _U("Descriptive data"))
        self.frame_descriptive_data.SetForegroundColour(TITLE_COLOR)
        self.frame_descriptive_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_descriptive_data.SetFont(fp.getFont())
        fp.popFont()

        self.tc1 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Manufacturer"),
                             tip = _U("Manufacturer"))

        self.tc2 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("CHPequip"),
                             tip = _U("CHPequip"))

        self.tc3 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Type"),
                             tip = _U("Type"))

        self.tc4 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("SubType"),
                             tip = _U("SubType"))

        self.tc5 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Reference"),
                             tip = _U("Source of data"))

        #
        # tab 2 - Technical data
        #
        self.frame_technical_data = wx.StaticBox(self.page2, -1, _U("Technical data"))
        self.frame_electricity = wx.StaticBox(self.page2, -1, _U("Electricity generation parameters"))
        self.frame_technical_data.SetForegroundColour(TITLE_COLOR)
        self.frame_technical_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_technical_data.SetFont(fp.getFont())
        fp.popFont()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT + UNITS_WIDTH, wUnits = 0)

        self.tc6 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("CHPPt"),
                              tip = _U("Nominal thermal power"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.tc7 = ChoiceEntry(self.page2,
                               values = [],
                               label = _U("FuelType"),
                               tip = _U("Fuel type"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT + UNITS_WIDTH, wUnits = 0)

        self.tc8 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("FuelConsum"),
                              tip = _U("Nominal fuel consumption"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.tc9 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'FRACTION',
                              label = _U("Eta_t"),
                              tip = _U("Nominal thermal conversion efficiency"))

        self.tc10 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'POWER',
                               label = _U("CHPPe"),
                               tip = _U("Nominal electrical power"))

        self.tc11 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("Eta_e"),
                               tip = _U("Electrical efficiency"))

        #
        # tab 3 - Heat source / sink
        #
        self.frame_heat_source_sink = wx.StaticBox(self.page3, -1, _U("Heat source / sink"))
        self.frame_heat_source_sink.SetForegroundColour(TITLE_COLOR)
        self.frame_heat_source_sink.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_heat_source_sink.SetFont(fp.getFont())
        fp.popFont()

        self.tc12 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'POWER',
                               label = _U("FluidSupply"),
                               tip = _U("Heat transport medium"))

        self.tc13 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'TEMPERATURE',
                               label = _U("Tsupply"),
                               tip = _U("Outlet temperature at nominal conditions"))

        self.tc14 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'MASSFLOWRATE',
                               unitdict = 'FRACTION',
                               label = _U("FlowRateSupply"),
                               tip = _U("Mass flow rate of heat transport medium"))

        self.tc15 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'POWER',
                               label = _U("FluidSupply2"),
                               tip = _U("Heat transport medium"))

        self.tc16 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'TEMPERATURE',
                               label = _U("Tsupply2"),
                               tip = _U("Outlet temperature at nominal conditions"))

        self.tc17 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'MASSFLOWRATE',
                               unitdict = 'FRACTION',
                               label = _U("FlowRateSupply2"),
                               tip = _U("Mass flow rate of heat transport medium"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        #
        # tab 4 - Economic Parameters
        #
        self.frame_economic_parameters = wx.StaticBox(self.page4, -1, _U("Economic parameters"))
        self.frame_economic_parameters.SetForegroundColour(TITLE_COLOR)
        self.frame_economic_parameters.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_economic_parameters.SetFont(fp.getFont())
        fp.popFont()

        self.tc18 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'PRICE',
                               label = _U("Price"),
                               tip = _U("Equipment price at factory applied installer's discount"))

        self.tc19 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'PRICE',
                               label = _U("InvRate"),
                               tip = _U("Turn-key price"))

        self.tc20 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'UNITPRICE',
                               unitdict = 'FRACTION',
                               label = _U("OMRateFix"),
                               tip = _U("Annual operational and maintenance fixed costs (approximate average per kW heating)"))

        self.tc21 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'UNITPRICEENERGY',
                               unitdict = 'FRACTION',
                               label = _U("OMRateVar"),
                               tip = _U("Annual operational and maintenance variable costs dependant on usage (approximate average per MWh heating)"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT + UNITS_WIDTH, wUnits = 0)

        self.tc22 = FloatEntry(self.page4,
                               ipart = 4, decimals = 0, minval = 1900, maxval = 2100, value = 2010,
                               label = _U("YearUpdate"),
                               tip = _U("Year of last update of the economic data"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

    def __do_layout(self):
        flagText = wx.TOP | wx.ALIGN_CENTER_HORIZONTAL

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)


        sizerPage0 = wx.StaticBoxSizer(self.frame_summary_table, wx.VERTICAL)
        sizerPage0.Add(self.grid, 1, wx.EXPAND | wx.ALL, 56)
        sizerPage0.Add(self.tc_type, 0, flagText | wx.ALIGN_RIGHT, VSEP)
        sizerPage0.Add(self.tc_subtype, 0, flagText | wx.ALIGN_RIGHT, VSEP)

        self.page0.SetSizer(sizerPage0)


        sizerPage1 = wx.StaticBoxSizer(self.frame_descriptive_data, wx.VERTICAL)
        sizerPage1.Add(self.tc1, 0, flagText, VSEP)
        sizerPage1.Add(self.tc2, 0, flagText, VSEP)
        sizerPage1.Add(self.tc3, 0, flagText, VSEP)
        sizerPage1.Add(self.tc4, 0, flagText, VSEP)
        sizerPage1.Add(self.tc5, 0, flagText, VSEP)

        self.page1.SetSizer(sizerPage1)


        sizerPage2 = wx.StaticBoxSizer(self.frame_technical_data, wx.VERTICAL)
        sizerPage2.Add(self.tc6, 0, flagText, VSEP)
        sizerPage2.Add(self.tc7, 0, flagText, VSEP)
        sizerPage2.Add(self.tc8, 0, flagText, VSEP)
        sizerPage2.Add(self.tc9, 0, flagText, VSEP)

        sizerPage2_electricity = wx.StaticBoxSizer(self.frame_electricity, wx.VERTICAL)
        sizerPage2_electricity.Add(self.tc10, 0, flagText, VSEP)
        sizerPage2_electricity.Add(self.tc11, 0, flagText, VSEP)
        sizerPage2.Add(sizerPage2_electricity, 0, flagText)

        self.page2.SetSizer(sizerPage2)


        sizerPage3 = wx.StaticBoxSizer(self.frame_heat_source_sink, wx.HORIZONTAL)
        sizerPage3_1 = wx.BoxSizer(wx.VERTICAL)
        sizerPage3_1.Add(self.tc12, 0, flagText, VSEP)
        sizerPage3_1.Add(self.tc13, 0, flagText, VSEP)
        sizerPage3_1.Add(self.tc14, 0, flagText, VSEP)

        sizerPage3_2 = wx.BoxSizer(wx.VERTICAL)
        sizerPage3_2.Add(self.tc15, 0, flagText, VSEP)
        sizerPage3_2.Add(self.tc16, 0, flagText, VSEP)
        sizerPage3_2.Add(self.tc17, 0, flagText, VSEP)

        sizerPage3.Add(sizerPage3_1, 0, flagText)
        sizerPage3.Add(sizerPage3_2, 0, flagText)

        self.page3.SetSizer(sizerPage3)


        sizerPage4 = wx.StaticBoxSizer(self.frame_economic_parameters, wx.VERTICAL)
        sizerPage4.Add(self.tc18, 0, flagText, VSEP)
        sizerPage4.Add(self.tc19, 0, flagText, VSEP)
        sizerPage4.Add(self.tc20, 0, flagText, VSEP)
        sizerPage4.Add(self.tc21, 0, flagText, VSEP)
        sizerPage4.Add(self.tc22, 0, flagText, VSEP)

        self.page4.SetSizer(sizerPage4)


        sizerAddDelete = wx.BoxSizer(wx.HORIZONTAL)
        sizerAddDelete.Add(self.buttonDeleteEquipment, 1, wx.EXPAND, 0)
        sizerAddDelete.Add(self.buttonAddEquipment, 1, wx.EXPAND | wx.LEFT, 4)

        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel.Add(self.buttonCancel, 1, wx.EXPAND, 0)
        sizerOKCancel.Add(self.buttonOK, 1, wx.EXPAND | wx.LEFT, 4)

        sizerGlobal.Add(self.notebook, 1, wx.EXPAND, 0)
        sizerGlobal.Add(sizerAddDelete, 0, wx.ALIGN_RIGHT, 0)
        sizerGlobal.Add(sizerOKCancel, 0, wx.ALIGN_RIGHT, 0)

        self.SetSizer(sizerGlobal)
        self.Layout()
        self.Show()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------

    def OnButtonOK(self, event):
        if self.allFieldsEmpty():
            self.theId = -1
            return

        fuelDict = Status.prj.getFuelDict()

        tmp = {
               "Manufacturer":check(self.tc1.GetValue()),
               "CHPequip":check(self.tc2.GetValue()),
               "Type":check(self.tc3.GetValue()),
               "SubType":check(self.tc4.GetValue()),
               "Reference":check(self.tc5.GetValue()),
               "CHPPt":check(self.tc6.GetValue()),
               "FuelType":check(findKey(fuelDict, self.tc7.GetValue(text = True))),
               "FuelConsum":check(self.tc8.GetValue()),
               "Eta_t":check(self.tc9.GetValue()),
               "CHPPe":check(self.tc10.GetValue()),
               "Eta_e":check(self.tc11.GetValue()),
               "FluidSupply":check(self.tc12.GetValue()),
               "Tsupply":check(self.tc13.GetValue()),
               "FlowRateSupply":check(self.tc14.GetValue()),
               "FluidSupply2":check(self.tc15.GetValue()),
               "Tsupply2":check(self.tc16.GetValue()),
               "FlowRateSupply2":check(self.tc17.GetValue()),
               "Price":check(self.tc18.GetValue()),
               "InvRate":check(self.tc19.GetValue()),
               "OMRateFix":check(self.tc20.GetValue()),
               "OMRateVar":check(self.tc21.GetValue()),
               "YearUpdate":check(self.tc22.GetValue())
               }

        self.updateValues(tmp)

        if self.closeOnOk:
            self.EndModal(wx.ID_OK)

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------

    def display(self, q = None):
        self.clear()

        fuelDict = Status.prj.getFuelDict()
        self.fillChoiceOfDBFuel(self.tc7.entry)

        if q is not None:
            self.tc1.SetValue(str(q.Manufacturer)) if q.Manufacturer is not None else ''
            self.tc2.SetValue(str(q.CHPequip)) if q.CHPequip is not None else ''
            self.tc3.SetValue(str(q.Type)) if q.Type is not None else ''
            self.tc4.SetValue(str(q.SubType)) if q.SubType is not None else ''
            self.tc5.SetValue(str(q.Reference)) if q.Reference is not None else ''
            self.tc6.SetValue(str(q.CHPPt)) if q.CHPPt is not None else ''
            if q.FuelType is not None:
                self.tc7.SetValue(fuelDict[int(q.FuelType)]) if int(q.FuelType) in fuelDict.keys() else ''
            self.tc8.SetValue(str(q.FuelConsum)) if q.FuelConsum is not None else ''
            self.tc9.SetValue(str(q.Eta_t)) if q.Eta_t is not None else ''
            self.tc10.SetValue(str(q.CHPPe)) if q.CHPPe is not None else ''
            self.tc11.SetValue(str(q.Eta_e)) if q.Eta_e is not None else ''
            self.tc12.SetValue(str(q.FluidSupply)) if q.FluidSupply is not None else ''
            self.tc13.SetValue(str(q.Tsupply)) if q.Tsupply is not None else ''
            self.tc14.SetValue(str(q.FlowRateSupply)) if q.FlowRateSupply is not None else ''
            self.tc15.SetValue(str(q.FluidSupply2)) if q.FluidSupply2 is not None else ''
            self.tc16.SetValue(str(q.Tsupply2)) if q.Tsupply2 is not None else ''
            self.tc17.SetValue(str(q.FlowRateSupply2)) if q.FlowRateSupply2 is not None else ''
            self.tc18.SetValue(str(q.Price)) if q.Price is not None else ''
            self.tc19.SetValue(str(q.InvRate)) if q.InvRate is not None else ''
            self.tc20.SetValue(str(q.OMRateFix)) if q.OMRateFix is not None else ''
            self.tc21.SetValue(str(q.OMRateVar)) if q.OMRateVar is not None else ''
            self.tc22.SetValue(str(q.YearUpdate)) if q.YearUpdate is not None else ''
        self.Show()

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
        self.tc12.SetValue('')
        self.tc13.SetValue('')
        self.tc14.SetValue('')
        self.tc15.SetValue('')
        self.tc16.SetValue('')
        self.tc17.SetValue('')
        self.tc18.SetValue('')
        self.tc19.SetValue('')
        self.tc20.SetValue('')
        self.tc21.SetValue('')
        self.tc22.SetValue('')

    def fillChoices(self):
        self.fillChoiceOfDBFuel(self.tc7.entry)
        self.fillChoiceOfType()
        self.fillChoiceOfSubType()

    def getDBCol(self):
        return self.db.DBCHP_ID

    def allFieldsEmpty(self):
        if len(self.tc1.GetValue()) == 0 and\
           len(self.tc2.GetValue()) == 0 and\
           len(self.tc3.GetValue()) == 0 and\
           len(self.tc4.GetValue()) == 0 and\
           len(self.tc5.GetValue()) == 0 and\
           self.tc6.GetValue() is None and\
           self.tc8.GetValue() is None and\
           self.tc9.GetValue() is None and\
           self.tc10.GetValue() is None and\
           self.tc11.GetValue() is None and\
           self.tc12.GetValue() is None and\
           self.tc13.GetValue() is None and\
           self.tc14.GetValue() is None and\
           self.tc15.GetValue() is None and\
           self.tc16.GetValue() is None and\
           self.tc17.GetValue() is None and\
           self.tc18.GetValue() is None and\
           self.tc19.GetValue() is None and\
           self.tc20.GetValue() is None and\
           self.tc21.GetValue() is None and\
           self.tc22.GetValue() is None:
            return True
        else:
            return False
