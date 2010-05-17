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
#    PanelDBFluid: Database Design Assistant
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
LABEL_WIDTH_LEFT = 260
DATA_ENTRY_WIDTH_LEFT = 140
UNITS_WIDTH = 55

VSEP = 4

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

class PanelDBBenchmark(PanelDBBase):
    def __init__(self, parent, title, closeOnOk = False):
        self.parent = parent
        self.title = title
        self.closeOnOk = closeOnOk
        self.name = "Benchmark"
        self._init_ctrls(parent)
        self._init_grid(100)
        self.__do_layout()
        self.fillEquipmentList()
        self.fillChoices()

    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        PanelDBBase.__init__(self, self.parent, "Edit DBBenchmark", self.name)

        # DBBenchmark_ID needs to remain as first entry
        self.colLabels = "DBBenchmark_ID", "NACECode", "UnitOp", "ProductCode", "Product", "ProductUnit"

        self.db = Status.DB.dbbenchmark
        self.table = "dbbenchmark"
        self.identifier = self.colLabels[0]
        self.type = self.colLabels[4]

        # access to font properties object
        fp = FontProperties()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.notebook = wx.Notebook(self, -1, style = 0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page0, _U('Summary table'))
        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page1, _U('Validity of benchmark'))
        self.page2 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page2, _U('Electricity consumption'))
        self.page3 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page3, _U('Fuel consumption'))
        self.page4 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page4, _U('Total final energy consumption'))

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

        #
        # tab 1 - Validity of benchmark  association with industrial sector, unit operation and product type
        #
        self.frame_validity_of_benchmark = wx.StaticBox(self.page1, -1, _U("Validity of benchmark  association with industrial sector, unit operation and product type"))
        self.frame_validity_range = wx.StaticBox(self.page1, -1, _U("Validity range for benchmark (general)"))
        self.frame_limits_of_validity = wx.StaticBox(self.page1, -1, _U("Limits of validity range depending on company size / production volume"))
        self.frame_data_source = wx.StaticBox(self.page1, -1, _U("Data source"))
        self.frame_validity_of_benchmark.SetForegroundColour(TITLE_COLOR)
        self.frame_validity_of_benchmark.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_validity_of_benchmark.SetFont(fp.getFont())
        fp.popFont()

        self.tc1 = ChoiceEntry(self.page1,
                               values = [],
                               label = _U("NACE code of the industrial sector"),
                               tip = _U("The benchmark can be general or only valid for a specific industrial sector"))

        self.tc2 = ChoiceEntry(self.page1,
                               values = [],
                               label = _U("Unit operation code"),
                               tip = _U("The benchmark can be general for the industrial sector, or specific for some unit operation in the sector. \"General\" could be an unit-operation code = 0, or empty"))

        self.tc3 = ChoiceEntry(self.page1,
                               values = [],
                               label = _U("Product Code"),
                               tip = _U("Final product or intermediate product for unit operation specific benchmarks"))

        self.tc4 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Product short name"),
                             tip = _U("Final product or intermediate product for unit operation specific benchmarks"))

        self.tc5 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Measurement unit for product"),
                             tip = _U(""))

        self.tc6 = TextEntry(self.page1, value = '',
                             label = _U("Comments on range of application"),
                             tip = _U("Additional comments on validity range (e.g. restrictions to certain types of machinery, etc.)"))

        self.tc7 = TextEntry(self.page1, maxchars = 200, value = '',
                             label = _U("Data relevance/reliability"),
                             tip = _U(""))

        self.tc8 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              # FIXME
                              unitdict = 'FRACTION',
                              #unitdict = 'CURRENCY',
                              label = _U("Yearly turnover (minimum)"),
                              tip = _U(""))

        self.tc9 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              # FIXME
                              unitdict = 'FRACTION',
                              #unitdict = 'CURRENCY',
                              label = _U("Yearly turnover (maximum)"),
                              tip = _U(""))

        self.tc10 = FloatEntry(self.page1,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'PU',
                               label = _U("Yearly production volume (minimum)"),
                               tip = _U(""))

        self.tc11 = FloatEntry(self.page1,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'PU',
                               label = _U("Yearly production volume (maximum)"),
                               tip = _U(""))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT + UNITS_WIDTH, wUnits = 0)

        self.tc12 = FloatEntry(self.page1,
                               ipart = 4, decimals = 0, minval = 1900, maxval = 2100, value = 2010,
                               label = _U("Year (reference for economic data)"),
                               tip = _U("Reference year for the economic data"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.tc13 = TextEntry(self.page1, value = '',
                              label = _U("References"),
                              tip = _U("Bibliographic reference (data source) of the benchmark"))

        self.tc14 = TextEntry(self.page1, value = '',
                              label = _U("Complementary literature"),
                              tip = _U("Additional bibliography"))

        #
        # tab 2 - Electricity consumption
        #
        self.frame_electricity_consumption = wx.StaticBox(self.page2, -1, _U("Electricity consumption"))
        self.frame_electricity_consumption.SetForegroundColour(TITLE_COLOR)
        self.frame_electricity_consumption.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_electricity_consumption.SetFont(fp.getFont())
        fp.popFont()

        self.tc15 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (production cost) MIN"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc16 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (production cost) MAX"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc17 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (production cost) TARGET"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc18 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (turnover) MIN"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc19 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (turnover) MAX"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc20 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Electricity: Energy intensity TARGET (turnover)"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc21 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERPU',
                               label = _U("Specific Energy Consumption (MIN)"),
                               tip = _U("Specific energetic consumption per pruduct unit (generic ratios) or processed medium unit (specific ratios for determined unitary operation)"))

        self.tc22 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERPU',
                               label = _U("Specific Energy Consumption (MAX)"),
                               tip = _U("Specific energetic consumption per pruduct unit (generic ratios) or processed medium unit (specific ratios for determined unitary operation)"))

        self.tc23 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERPU',
                               label = _U("Specific Energy Consumption (SEC) TARGET"),
                               tip = _U("Specific energetic consumption per pruduct unit (generic ratios) or processed medium unit (specific ratios for determined unitary operation)"))

        self.tc24 = ChoiceEntry(self.page2,
                                values = [],
                                label = _U("Unit of measurement"),
                                tip = _U("Measuring unit for the quantity of product or the quantity of processed medium"))

        #
        # tab 3 - Fuel consumption
        #
        self.frame_fuel_consumption = wx.StaticBox(self.page3, -1, _U("Fuel consumption"))
        self.frame_fuel_consumption.SetForegroundColour(TITLE_COLOR)
        self.frame_fuel_consumption.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_fuel_consumption.SetFont(fp.getFont())
        fp.popFont()

        self.tc25 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (production cost) MIN [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc26 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Heat: Energy intensity (production cost) MAX [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc27 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (production cost) TARGET [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc28 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Heat: Energy intensity (turnover) MIN  [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc29 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (turnover) MAX [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc30 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Heat: Energy intensity (turnover) TARGET [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc31 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERPU',
                               label = _U("Specific Energy Consumption MIN"),
                               tip = _U("Specific energetic consumption per pruduct unit (generic ratios) or processed medium unit (specific ratios for determined unitary operation)"))

        self.tc32 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERPU',
                               label = _U("Specific Energy Consumption MAX"),
                               tip = _U("Specific energetic consumption per pruduct unit (generic ratios) or processed medium unit (specific ratios for determined unitary operation)"))

        self.tc33 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERPU',
                               label = _U("Specific Energy Consumption TARGET"),
                               tip = _U("Specific energetic consumption per pruduct unit (generic ratios) or processed medium unit (specific ratios for determined unitary operation)"))

        self.tc34 = ChoiceEntry(self.page3,
                                values = [],
                                label = _U("Unit of measurement"),
                                tip = _U("Measuring unit for the quantity of product or the quantity of processed medium"))

        #
        # tab 4 - Total final energy consumption
        #
        self.frame_energy_consumption = wx.StaticBox(self.page4, -1, _U("Total final energy consumption"))
        self.frame_energy_consumption.SetForegroundColour(TITLE_COLOR)
        self.frame_energy_consumption.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_energy_consumption.SetFont(fp.getFont())
        fp.popFont()

        self.tc35 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (production cost) MIN [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc36 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (production cost) MAX [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc37 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (production cost) TARGET [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc38 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (turnover) MIN [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc39 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (turnover) MAX [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc40 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERCU',
                               label = _U("Energy intensity (turnover) TARGET [kWh/]"),
                               tip = _U("Energetic intensity (energetic consumption  with respect to an economic value: (a) expressed as a production cost and (b) expressed as a turnover"))

        self.tc41 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERPU',
                               label = _U("Specific Energy Consumption (SEC)"),
                               tip = _U("Specific energetic consumption per pruduct unit (generic ratios) or processed medium unit (specific ratios for determined unitary operation)"))

        self.tc42 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERPU',
                               label = _U("Specific Energy Consumption (SEC) TARGET"),
                               tip = _U("Specific energetic consumption per pruduct unit (generic ratios) or processed medium unit (specific ratios for determined unitary operation)"))

        self.tc43 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               # FIXME
                               unitdict = 'FRACTION',
                               #unitdict = 'ENERGYPERPU',
                               label = _U("Specific Energy Consumption (SEC) AVERAGE"),
                               tip = _U("Specific energetic consumption per pruduct unit (generic ratios) or processed medium unit (specific ratios for determined unitary operation)"))

        self.tc44 = ChoiceEntry(self.page4,
                                values = [],
                                label = _U("Unit of measurement"),
                                tip = _U("Measuring unit for the quantity of product or the quantity of processed medium"))

    def __do_layout(self):
        flagText = wx.TOP | wx.ALIGN_CENTER_HORIZONTAL

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)

        sizerPage0 = wx.StaticBoxSizer(self.frame_summary_table, wx.VERTICAL)
        sizerPage0.Add(self.grid, 1, wx.EXPAND | wx.ALL, 56)
        sizerPage0.Add(self.tc_type, 0, flagText | wx.ALIGN_RIGHT, VSEP)

        self.page0.SetSizer(sizerPage0)


        sizerPage1_validy = wx.StaticBoxSizer(self.frame_validity_range, wx.VERTICAL)
        sizerPage1_validy.Add(self.tc1, 0, flagText, VSEP)
        sizerPage1_validy.Add(self.tc2, 0, flagText, VSEP)
        sizerPage1_validy.Add(self.tc3, 0, flagText, VSEP)
        sizerPage1_validy.Add(self.tc4, 0, flagText, VSEP)
        sizerPage1_validy.Add(self.tc5, 0, flagText, VSEP)
        sizerPage1_validy.Add(self.tc6, 0, flagText, VSEP)
        sizerPage1_validy.Add(self.tc7, 0, flagText, VSEP)

        sizerPage1_limits = wx.StaticBoxSizer(self.frame_limits_of_validity, wx.VERTICAL)
        sizerPage1_limits.Add(self.tc8, 0, flagText, VSEP)
        sizerPage1_limits.Add(self.tc9, 0, flagText, VSEP)
        sizerPage1_limits.Add(self.tc10, 0, flagText, VSEP)
        sizerPage1_limits.Add(self.tc11, 0, flagText, VSEP)

        sizerPage1_data = wx.StaticBoxSizer(self.frame_data_source, wx.VERTICAL)
        sizerPage1_data.Add(self.tc12, 0, flagText, VSEP)
        sizerPage1_data.Add(self.tc13, 0, flagText, VSEP)
        sizerPage1_data.Add(self.tc14, 0, flagText, VSEP)

        sizerPage1 = wx.StaticBoxSizer(self.frame_validity_of_benchmark, wx.VERTICAL)
        sizerPage1.Add(sizerPage1_validy, 0, flagText, VSEP)
        sizerPage1.Add(sizerPage1_limits, 0, flagText, VSEP)
        sizerPage1.Add(sizerPage1_data, 0, flagText, VSEP)

        self.page1.SetSizer(sizerPage1)


        sizerPage2 = wx.StaticBoxSizer(self.frame_electricity_consumption, wx.VERTICAL)
        sizerPage2.Add(self.tc15, 0, flagText, VSEP)
        sizerPage2.Add(self.tc16, 0, flagText, VSEP)
        sizerPage2.Add(self.tc17, 0, flagText, VSEP)
        sizerPage2.Add(self.tc18, 0, flagText, VSEP)
        sizerPage2.Add(self.tc19, 0, flagText, VSEP)
        sizerPage2.Add(self.tc20, 0, flagText, VSEP)
        sizerPage2.Add(self.tc21, 0, flagText, VSEP)
        sizerPage2.Add(self.tc22, 0, flagText, VSEP)
        sizerPage2.Add(self.tc23, 0, flagText, VSEP)
        sizerPage2.Add(self.tc24, 0, flagText, VSEP)

        self.page2.SetSizer(sizerPage2)


        sizerPage3 = wx.StaticBoxSizer(self.frame_fuel_consumption, wx.VERTICAL)
        sizerPage3.Add(self.tc25, 0, flagText, VSEP)
        sizerPage3.Add(self.tc26, 0, flagText, VSEP)
        sizerPage3.Add(self.tc27, 0, flagText, VSEP)
        sizerPage3.Add(self.tc28, 0, flagText, VSEP)
        sizerPage3.Add(self.tc29, 0, flagText, VSEP)
        sizerPage3.Add(self.tc30, 0, flagText, VSEP)
        sizerPage3.Add(self.tc31, 0, flagText, VSEP)
        sizerPage3.Add(self.tc32, 0, flagText, VSEP)
        sizerPage3.Add(self.tc33, 0, flagText, VSEP)
        sizerPage3.Add(self.tc34, 0, flagText, VSEP)

        self.page3.SetSizer(sizerPage3)


        sizerPage4 = wx.StaticBoxSizer(self.frame_energy_consumption, wx.VERTICAL)
        sizerPage4.Add(self.tc35, 0, flagText, VSEP)
        sizerPage4.Add(self.tc36, 0, flagText, VSEP)
        sizerPage4.Add(self.tc37, 0, flagText, VSEP)
        sizerPage4.Add(self.tc38, 0, flagText, VSEP)
        sizerPage4.Add(self.tc39, 0, flagText, VSEP)
        sizerPage4.Add(self.tc40, 0, flagText, VSEP)
        sizerPage4.Add(self.tc41, 0, flagText, VSEP)
        sizerPage4.Add(self.tc42, 0, flagText, VSEP)
        sizerPage4.Add(self.tc43, 0, flagText, VSEP)
        sizerPage4.Add(self.tc44, 0, flagText, VSEP)

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
#        if self.allFieldsEmpty():
#            self.theId = -1
#            return

        NACEDict = Status.prj.getNACEDict()
        unitOpDict = Status.prj.getUnitOpDict()





        tmp = {
               "NACECode":check(findKey(NACEDict, self.tc1.GetValue(text = True))),
               "UnitOp":check(findKey(unitOpDict, self.tc2.GetValue(text = True))),
               "ProductCode":check(self.tc28.GetValue()),
#  `Product` varchar(45) default NULL,
#  `E_EnergyInt_MIN_PC` double default NULL,
#  `E_EnergyInt_MAX_PC` double default NULL,
#  `E_EnergyInt_TARG_PC` double default NULL,
#  `E_EnergyInt_MIN_T` double default NULL,
#  `E_EnergyInt_MAX_T` double default NULL,
#  `E_EnergyInt_TARG_T` double default NULL,
#  `E_SEC_MIN` double default NULL,
#  `E_SEC_MAX` double default NULL,
#  `E_SEC_TARG` double default NULL,
#  `E_Unit` varchar(45) default NULL,
#  `H_EnergyInt_MIN_PC` double default NULL,
#  `H_EnergyInt_MAX_PC` double default NULL,
#  `H_EnergyInt_TARG_PC` double default NULL,
#  `H_EnergyInt_MIN_T` double default NULL,
#  `H_EnergyInt_MAX_T` double default NULL,
#  `H_EnergyInt_TARG_T` double default NULL,
#  `H_SEC_MIN` double default NULL,
#  `H_SEC_MAX` double default NULL,
#  `H_SEC_TARG` double default NULL,
#  `H_Unit` varchar(45) default NULL,
#  `T_EnergyInt_MIN_PC` double default NULL,
#  `T_EnergyInt_MAX_PC` double default NULL,
#  `T_EnergyInt_TARG_PC` double default NULL,
#  `T_EnergyInt_MIN_T` double default NULL,
#  `T_EnergyInt_MAX_T` double default NULL,
#  `T_EnergyInt_TARG_T` double default NULL,
#  `T_SEC_MIN` double default NULL,
#  `T_SEC_MAX` double default NULL,
#  `T_SEC_TARG` double default NULL,
#  `T_Unit` varchar(45) default NULL,
#  `Comments` text,
#  `YearReference` int(10) unsigned default NULL,
#  `Reference` text,
#  `Literature` text,
#  `DataRelevance` varchar(200) default NULL,
#  `TurnoverMin` double default NULL,
#  `TurnoverMax` double default NULL,
#  `ProductionMin` double default NULL,
#  `ProductionMax` double default NULL,
#  `ProductionUnit` double default NULL,







               }

        self.updateValues(tmp)

        if self.closeOnOk:
            self.EndModal(wx.ID_OK)

    def display(self, q = None):
        pass

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
        self.tc23.SetValue('')
        self.tc24.SetValue('')
        self.tc25.SetValue('')
        self.tc26.SetValue('')
        self.tc27.SetValue('')
        self.tc28.SetValue('')
        self.tc29.SetValue('')
        self.tc30.SetValue('')
        self.tc31.SetValue('')
        self.tc32.SetValue('')
        self.tc33.SetValue('')
        self.tc34.SetValue('')
        self.tc35.SetValue('')
        self.tc36.SetValue('')
        self.tc37.SetValue('')
        self.tc38.SetValue('')
        self.tc39.SetValue('')
        self.tc40.SetValue('')
        self.tc41.SetValue('')
        self.tc42.SetValue('')
        self.tc43.SetValue('')
        self.tc44.SetValue('')

    def fillChoices(self):
        pass

    def getDBCol(self):
        return self.db.DBHeatPump_ID

    def allFieldsEmpty(self):
        return False
