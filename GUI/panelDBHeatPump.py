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
#    PanelDBHeatPump: Database Design Assistant
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
DATA_ENTRY_WIDTH_LEFT = 195
UNITS_WIDTH = 0

VSEP = 4

def _U(text):
    try:
        return unicode(_(text), "utf-8")
    except:
        return _(text)

class PanelDBHeatPump(PanelDBBase):
    def __init__(self, parent, title, closeOnOk = False):
        self.parent = parent
        self.title = title
        self.closeOnOk = closeOnOk
        self.name = "HeatPump"
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

        PanelDBBase.__init__(self, self.parent, "Edit DBHeatPump", self.name)

        # DBHeatPump_ID needs to remain as first entry
        self.colLabels = "DBHeatPump_ID", "HPManufacturer", "HPModel", "HPType", "HPSubType", "HPHeatCAP"

        self.db = Status.DB.dbheatpump
        self.table = "dbheatpump"
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
                             label = _U("HPManufacturer"),
                             tip = _U("Heatpump Manufacturer"))

        self.tc2 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("HPModel"),
                             tip = _U("Heatpump Model"))

        self.tc3 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("HPType"),
                             tip = _U("Heatpump Type"))

        self.tc4 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("HPSubType"),
                             tip = _U("Heatpump Sub Type"))

        self.tc5 = TextEntry(self.page1, maxchars = 200, value = '',
                             label = _U("Reference"),
                             tip = _U("Source of data"))

        #
        # tab 2 - Technical data
        #
        self.frame_technical_data = wx.StaticBox(self.page2, -1, _U("Technical data"))
        self.frame_heating = wx.StaticBox(self.page2, -1, _U("Heating"))
        self.frame_cooling = wx.StaticBox(self.page2, -1, _U("Cooling"))
        self.frame_general = wx.StaticBox(self.page2, -1, _U("General"))
        self.frame_nominal_working_conditions = wx.StaticBox(self.page2, -1, _U("Nominal working conditions"))
        self.frame_theoretical_efficiency = wx.StaticBox(self.page2, -1, _U("Theoretical efficiency and exergetic efficiency"))
        self.frame_technical_data.SetForegroundColour(TITLE_COLOR)
        self.frame_technical_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_technical_data.SetFont(fp.getFont())
        fp.popFont()

        self.tc6 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("HPHeatCap"),
                              tip = _U("Nominal heating capacity"))

        self.tc7 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("HPHeatCOP"),
                              tip = _U("Nominal COP for heating mode"))

        self.tc8 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("HPCoolCap"),
                              tip = _U("Nominal cooling capacity"))

        self.tc9 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("HPCoolCOP"),
                              tip = _U("Nominal COP for cooling mode"))

        self.tc10 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPFuelConsum"),
                               tip = _U("Nominal fuel consumption"))

        self.tc11 = ChoiceEntry(self.page2,
                                values = [],
                                label = _U("FuelType"),
                                tip = _U("Fuel type"))

        self.tc12 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPElectConsum"),
                               tip = _U("Nominal electrical power consumption"))

        self.tc13 = TextEntry(self.page2, maxchars = 45, value = '',
                              label = _U("HPWorkFluid"),
                              tip = _U("Refrigerant / absorbent refrigerant pair"))

        self.tc14 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPCondTinC"),
                               tip = _U("inlet temperature to the condenser (and absorber)"))

        self.tc15 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPGenTinC"),
                               tip = _U("inlet temperature to the generator"))

        self.tc16 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPEvapTinC"),
                               tip = _U("inlet temperature to the evaporator"))

        self.tc17 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPConstExCoolCOP"),
                               tip = _U("Temperature range around the nominal temperatures for which the constant exergetic COP approximation is valid (e.g. +-20 K)"))

        self.tc18 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPCondTinH"),
                               tip = _U("inlet temperature to the condenser (and absorber)"))

        self.tc19 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPGenTinH"),
                               tip = _U("inlet temperature to the generator"))

        self.tc20 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPEvapTinH"),
                               tip = _U("inlet temperature to the evaporator"))

        self.tc21 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPConstExHeatCOP"),
                               tip = _U("Temperature range around the nominal temperatures for which the constant exergetic COP approximation is valid (e.g. +-20 K)"))

        self.tc22 = StaticTextEntry(self.page2, maxchars = 255, value = '',
                                    label = _U("HPExCoolCOP"),
                                    tip = _U("Calculated from the nominal and theoretical COP at the manufact. catalogue nominal conditions and applied as a constant in extrapolation for other working conditions (see next point)."))

        self.tc23 = StaticTextEntry(self.page2, maxchars = 255, value = '',
                                    label = _U("HPThCoolCOP"),
                                    tip = _U("Carnot COP for cooling mode at nominal conditions (see next point)."))

        self.tc24 = StaticTextEntry(self.page2, maxchars = 255, value = '',
                                    label = _U("HPExHeatCOP"),
                                    tip = _U("Calculated from the nominal and theoretical COP at the manufact. catalogue nominal conditions and applied as a constant in extrapolation for other working conditions (see next point)."))

        self.tc25 = StaticTextEntry(self.page2, maxchars = 255, value = '',
                                    label = _U("HPThHeatCOP"),
                                    tip = _U("Carnot COP for heating mode at nominal conditions (see next point)."))

        #
        # tab 3 - Heat source / sink
        #
        self.frame_heat_source_sink = wx.StaticBox(self.page3, -1, _U("Heat source / sink"))
        self.frame_low_temp_heat_source_sink = wx.StaticBox(self.page3, -1, _U("Low temperature heat source / sink"))
        self.frame_high_temp_heat_source_sink = wx.StaticBox(self.page3, -1, _U("High temperature heat source / sink"))
        self.frame_heat_source_sink.SetForegroundColour(TITLE_COLOR)
        self.frame_heat_source_sink.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_heat_source_sink.SetFont(fp.getFont())
        fp.popFont()

        self.tc26 = ChoiceEntry(self.page3,
                                values = [],
                                label = _U("HPAbsEffects"),
                                tip = _U("Heat source and sink"))

        self.tc27 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPLimDT"),
                               tip = _U("Maximum acceptable temperature difference between evaporator and condenser temperatures (primary fluid: Tco - Tev) - working limit"))

        self.tc28 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPCondTmax"),
                               tip = _U("Maximum condensing (and absorption) temperature (primary fluid) - working limit"))

        self.tc29 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPEvapTmin"),
                               tip = _U("Minimum evaporating temperature (primary fluid) - working limit"))

        self.tc30 = ChoiceEntry(self.page3,
                                values = [],
                                label = _U("HPAbsHeatMed"),
                                tip = _U("Heat transport medium used for heat supply to the generator"))

        self.tc31 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPGenTmin"),
                               tip = _U("Minimum required inlet temperature to the generator"))

        #
        # tab 4 - Economic Parameters
        #
        self.frame_economic_parameters = wx.StaticBox(self.page4, -1, _U("Economic parameters"))
        self.frame_economic_parameters.SetForegroundColour(TITLE_COLOR)
        self.frame_economic_parameters.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_economic_parameters.SetFont(fp.getFont())
        fp.popFont()

        self.tc32 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPPrice"),
                               tip = _U("Equipment price at factory applied installer's discount"))

        self.tc33 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPTurnKeyPrice"),
                               tip = _U("Price of installed equipment (including work, additional accessories, pumps, regulation, etc)"))

        self.tc34 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPOandMfix"),
                               tip = _U("Annual operational and maintenance fixed costs (approximate average per kW heating)"))

        self.tc35 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("HPOandMvar"),
                               tip = _U("Annual operational and maintenance variable costs dependant on usage (approximate average per MWh heating)"))

        self.tc36 = FloatEntry(self.page4,
                               ipart = 4, decimals = 0, minval = 1900, maxval = 2100, value = 2010,
                               label = _U("HPYearUpdate"),
                               tip = _U("Year of last update of the economic data"))

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


        sizerPage2_H1 = wx.StaticBoxSizer(self.frame_heating, wx.VERTICAL)
        sizerPage2_H1.Add(self.tc6, 0, flagText, VSEP)
        sizerPage2_H1.Add(self.tc7, 0, flagText, VSEP)

        sizerPage2_C1 = wx.StaticBoxSizer(self.frame_cooling, wx.VERTICAL)
        sizerPage2_C1.Add(self.tc8, 0, flagText, VSEP)
        sizerPage2_C1.Add(self.tc9, 0, flagText, VSEP)

        sizerPage2_G = wx.StaticBoxSizer(self.frame_general, wx.VERTICAL)
        sizerPage2_G.Add(self.tc10, 0, flagText, VSEP)
        sizerPage2_G.Add(self.tc11, 0, flagText, VSEP)
        sizerPage2_G.Add(self.tc12, 0, flagText, VSEP)
        sizerPage2_G.Add(self.tc13, 0, flagText, VSEP)

        sizerPage2_nwc_C = wx.BoxSizer(wx.VERTICAL)
        sizerPage2_nwc_C.Add(self.tc14, 0, flagText, VSEP)
        sizerPage2_nwc_C.Add(self.tc15, 0, flagText, VSEP)
        sizerPage2_nwc_C.Add(self.tc16, 0, flagText, VSEP)
        sizerPage2_nwc_C.Add(self.tc17, 0, flagText, VSEP)

        sizerPage2_nwc_H = wx.BoxSizer(wx.VERTICAL)
        sizerPage2_nwc_H.Add(self.tc18, 0, flagText, VSEP)
        sizerPage2_nwc_H.Add(self.tc19, 0, flagText, VSEP)
        sizerPage2_nwc_H.Add(self.tc20, 0, flagText, VSEP)
        sizerPage2_nwc_H.Add(self.tc21, 0, flagText, VSEP)

        sizerPage2_nwc = wx.StaticBoxSizer(self.frame_nominal_working_conditions, wx.HORIZONTAL)
        sizerPage2_nwc.Add(sizerPage2_nwc_C)
        sizerPage2_nwc.Add(sizerPage2_nwc_H)

        sizerPage2_teee_C = wx.BoxSizer(wx.VERTICAL)
        sizerPage2_teee_C.Add(self.tc22, 0, flagText, VSEP)
        sizerPage2_teee_C.Add(self.tc23, 0, flagText, VSEP)

        sizerPage2_teee_H = wx.BoxSizer(wx.VERTICAL)
        sizerPage2_teee_H.Add(self.tc24, 0, flagText, VSEP)
        sizerPage2_teee_H.Add(self.tc25, 0, flagText, VSEP)

        sizerPage2_teee = wx.StaticBoxSizer(self.frame_theoretical_efficiency, wx.HORIZONTAL)
        sizerPage2_teee.Add(sizerPage2_teee_C)
        sizerPage2_teee.Add(sizerPage2_teee_H)

        sizerPage2 = wx.StaticBoxSizer(self.frame_technical_data, wx.VERTICAL)
        sizerPage2.Add(sizerPage2_H1, 0, flagText, 4)
        sizerPage2.Add(sizerPage2_C1, 0, flagText, 4)
        sizerPage2.Add(sizerPage2_G, 0, flagText, 4)
        sizerPage2.Add(sizerPage2_nwc, 0, flagText, 4)
        sizerPage2.Add(sizerPage2_teee, 0, flagText, 4)

        self.page2.SetSizer(sizerPage2)


        sizerPage3_low = wx.StaticBoxSizer(self.frame_low_temp_heat_source_sink, wx.VERTICAL)
        sizerPage3_low.Add(self.tc26, 0, flagText, VSEP)
        sizerPage3_low.Add(self.tc27, 0, flagText, VSEP)
        sizerPage3_low.Add(self.tc28, 0, flagText, VSEP)
        sizerPage3_low.Add(self.tc29, 0, flagText, VSEP)

        sizerPage3_high = wx.StaticBoxSizer(self.frame_high_temp_heat_source_sink, wx.VERTICAL)
        sizerPage3_high.Add(self.tc30, 0, flagText, VSEP)
        sizerPage3_high.Add(self.tc31, 0, flagText, VSEP)

        sizerPage3 = wx.StaticBoxSizer(self.frame_heat_source_sink, wx.VERTICAL)
        sizerPage3.Add(sizerPage3_low, 0, flagText, 4)
        sizerPage3.Add(sizerPage3_high, 0, flagText, 4)

        self.page3.SetSizer(sizerPage3)

        sizerPage4 = wx.StaticBoxSizer(self.frame_economic_parameters, wx.VERTICAL)
        sizerPage4.Add(self.tc32, 0, flagText, VSEP)
        sizerPage4.Add(self.tc33, 0, flagText, VSEP)
        sizerPage4.Add(self.tc34, 0, flagText, VSEP)
        sizerPage4.Add(self.tc35, 0, flagText, VSEP)
        sizerPage4.Add(self.tc36, 0, flagText, VSEP)

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
               "HPManufacturer":check(self.tc1.GetValue()),
               "HPModel":check(self.tc2.GetValue()),
               "HPType":check(self.tc3.GetValue()),
               "HPSubType":check(self.tc4.GetValue()),
               "Reference":check(self.tc5.GetValue()),
               "HPHeatCap":check(self.tc6.GetValue()),
               "HPHeatCOP":check(self.tc7.GetValue()),
               "HPCoolCap":check(self.tc8.GetValue()),
               "HPCoolCOP":check(self.tc9.GetValue()),
               "HPFuelConsum":check(self.tc10.GetValue()),
               "FuelType":check(findKey(fuelDict, self.tc11.GetValue(text = True))),
               "HPElectConsum":check(self.tc12.GetValue()),
               "HPWorkFluid":check(self.tc13.GetValue()),
               "HPCondTinC":check(self.tc14.GetValue()),
               "HPAbsTinC":check(self.tc14.GetValue()), # equal to HPCondTinC
               "HPGenTinC":check(self.tc15.GetValue()),
               "HPEvapTinC":check(self.tc16.GetValue()),
               "HPConstExCoolCOP":check(self.tc17.GetValue()),
               "HPCondTinH":check(self.tc18.GetValue()),
               "HPAbsTinH":check(self.tc18.GetValue()), # equal to HPCondTinH
               "HPGenTinH":check(self.tc19.GetValue()),
               "HPEvapTinH":check(self.tc20.GetValue()),
               "HPConstExHeatCOP":check(self.tc21.GetValue()),
               "HPExCoolCOP":check(self.tc22.GetValue()),
               "HPThCoolCOP":check(self.tc23.GetValue()),
               "HPExHeatCOP":check(self.tc24.GetValue()),
               "HPThHeatCOP":check(self.tc25.GetValue()),
#               "HPSourceSink":check(self.tc26.GetValue()),
               "HPLimDT":check(self.tc27.GetValue()),
               "HPCondTmax":check(self.tc28.GetValue()),
               "HPEvapTmin":check(self.tc29.GetValue()),
#               "HPAbsHeatMed":check(self.tc30.GetValue()),
               "HPGenTmin":check(self.tc31.GetValue()),
               "HPPrice":check(self.tc32.GetValue()),
               "HPTurnKeyPrice":check(self.tc33.GetValue()),
               "HPOandMfix":check(self.tc34.GetValue()),
               "HPOandMvar":check(self.tc35.GetValue()),
               "HPYearUpdate":check(self.tc36.GetValue())
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
        self.fillChoiceOfDBFuel(self.tc11.entry)

        if q is not None:
            self.tc1.SetValue(str(q.HPManufacturer)) if q.HPManufacturer is not None else ''
            self.tc2.SetValue(str(q.HPModel)) if q.HPModel is not None else ''
            self.tc3.SetValue(str(q.HPType)) if q.HPType is not None else ''
            self.tc4.SetValue(str(q.HPSubType)) if q.HPSubType is not None else ''
            self.tc5.SetValue(str(q.Reference)) if q.Reference is not None else ''
            self.tc6.SetValue(str(q.HPHeatCap)) if q.HPHeatCap is not None else ''
            self.tc7.SetValue(str(q.HPHeatCOP)) if q.HPHeatCOP is not None else ''
            self.tc8.SetValue(str(q.HPCoolCap)) if q.HPCoolCap is not None else ''
            self.tc9.SetValue(str(q.HPCoolCOP)) if q.HPCoolCOP is not None else ''
            self.tc10.SetValue(str(q.HPFuelConsum)) if q.HPFuelConsum is not None else ''
            if q.FuelType is not None:
                self.tc11.SetValue(fuelDict[int(q.FuelType)]) if int(q.FuelType) in fuelDict.keys() else ''
            self.tc12.SetValue(str(q.HPElectConsum)) if q.HPElectConsum is not None else ''
            self.tc13.SetValue(str(q.HPWorkFluid)) if q.HPWorkFluid is not None else ''
            self.tc14.SetValue(str(q.HPCondTinC)) if q.HPCondTinC is not None else ''
            self.tc15.SetValue(str(q.HPGenTinC)) if q.HPGenTinC is not None else ''
            self.tc16.SetValue(str(q.HPEvapTinC)) if q.HPEvapTinC is not None else ''
            self.tc17.SetValue(str(q.HPConstExCoolCOP)) if q.HPConstExCoolCOP is not None else ''
            self.tc18.SetValue(str(q.HPCondTinH)) if q.HPCondTinH is not None else ''
            self.tc19.SetValue(str(q.HPGenTinH)) if q.HPGenTinH is not None else ''
            self.tc20.SetValue(str(q.HPEvapTinH)) if q.HPEvapTinH is not None else ''
            self.tc21.SetValue(str(q.HPConstExHeatCOP)) if q.HPConstExHeatCOP is not None else ''
            self.tc22.SetValue(str(q.HPExCoolCOP)) if q.HPExCoolCOP is not None else ''
            self.tc23.SetValue(str(q.HPThCoolCOP)) if q.HPThCoolCOP is not None else ''
            self.tc24.SetValue(str(q.HPExHeatCOP)) if q.HPExHeatCOP is not None else ''
            self.tc25.SetValue(str(q.HPThHeatCOP)) if q.HPThHeatCOP is not None else ''
            self.tc26.SetValue(str(q.HPSourceSink)) if q.HPSourceSink is not None else ''
            self.tc27.SetValue(str(q.HPLimDT)) if q.HPLimDT is not None else ''
            self.tc28.SetValue(str(q.HPCondTmax)) if q.HPCondTmax is not None else ''
            self.tc29.SetValue(str(q.HPEvapTmin)) if q.HPEvapTmin is not None else ''
            self.tc30.SetValue(str(q.HPAbsHeatMed)) if q.HPAbsHeatMed is not None else ''
            self.tc31.SetValue(str(q.HPGenTmin)) if q.HPGenTmin is not None else ''
            self.tc32.SetValue(str(q.HPPrice)) if q.HPPrice is not None else ''
            self.tc33.SetValue(str(q.HPTurnKeyPrice)) if q.HPTurnKeyPrice is not None else ''
            self.tc34.SetValue(str(q.HPOandMfix)) if q.HPOandMfix is not None else ''
            self.tc35.SetValue(str(q.HPOandMvar)) if q.HPOandMvar is not None else ''
            self.tc36.SetValue(str(q.HPYearUpdate)) if q.HPYearUpdate is not None else ''
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

    def fillChoices(self):
        self.fillChoiceOfDBFuel(self.tc11.entry)
        self.fillChoiceOfType()
        self.fillChoiceOfSubType()

    def getDBCol(self):
        return self.db.DBHeatPump_ID

    def allFieldsEmpty(self):
        if len(self.tc1.GetValue()) == 0 and\
           len(self.tc2.GetValue()) == 0 and\
           len(self.tc3.GetValue()) == 0 and\
           len(self.tc4.GetValue()) == 0 and\
           len(self.tc5.GetValue()) == 0 and\
           self.tc6.GetValue() is None and\
           self.tc7.GetValue() is None and\
           self.tc8.GetValue() is None and\
           self.tc9.GetValue() is None and\
           self.tc10.GetValue() is None and\
           self.tc12.GetValue() is None and\
           len(self.tc13.GetValue()) == 0 and\
           self.tc14.GetValue() is None and\
           self.tc15.GetValue() is None and\
           self.tc16.GetValue() is None and\
           self.tc17.GetValue() is None and\
           self.tc18.GetValue() is None and\
           self.tc19.GetValue() is None and\
           self.tc20.GetValue() is None and\
           self.tc21.GetValue() is None and\
           self.tc26.GetValue() < 0 and\
           self.tc27.GetValue() is None and\
           self.tc28.GetValue() is None and\
           self.tc29.GetValue() is None and\
           self.tc30.GetValue() < 0 and\
           self.tc31.GetValue() is None and\
           self.tc32.GetValue() is None and\
           self.tc33.GetValue() is None and\
           self.tc34.GetValue() is None and\
           self.tc35.GetValue() is None and\
           self.tc36.GetValue() is None:
            return True
        else:
            return False
