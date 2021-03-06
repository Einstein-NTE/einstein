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
#    PanelDBBoiler: Database Design Assistant
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
HEIGHT_TE_MULTILINE = 180
LABEL_WIDTH_LEFT_SHORT = 140
LABEL_WIDTH_LEFT_LONG = 350
DATA_ENTRY_WIDTH_LEFT = 140
UNITS_WIDTH = 55
UNITS_WIDTH_LARGE = UNITS_WIDTH + 20

VSEP = 4

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

class PanelDBBoiler(PanelDBBase):
    def __init__(self, parent, title, closeOnOk = False):
        self.parent = parent
        self.title = title
        self.closeOnOk = closeOnOk
        self.name = "Boiler"
        self._init_ctrls(parent)
        self._init_buttons()
        self._init_grid(145)
        self.__do_layout()
        self._bind_events()
        self.clear()
        self.fillEquipmentList()
        self.fillChoices()

    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        PanelDBBase.__init__(self, self.parent, "Edit DBBoiler", self.name)

        # DBBoiler_ID needs to remain as first entry although it is not shown on the GUI
        self.colLabels = "DBBoiler_ID", "BoilerManufacturer", "BoilerModel", "BoilerType", "BBPnom"

        self.db = Status.DB.dbboiler
        self.table = "dbboiler"
        self.identifier = self.colLabels[0]
        self.type = self.colLabels[3]

        # access to font properties object
        fp = FontProperties()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT_SHORT,
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

        self.tc_help = wx.StaticBox(self.page0, -1, _U('Help'))
        self.tc_help_text = wx.StaticText(self.page0, -1, _U('Click on the column labels to sort the table.'))
        self.tc_help_text.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL, False, 'Tahoma'))

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
                             label = _U("Boiler Manufacturer"),
                             tip = _U("Boiler Manufacturer"))

        self.tc2 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Boiler Model"),
                             tip = _U("Boiler Model"))

        self.tc3 = ChoiceEntry(self.page1,
                               values = [],
                               label = _U("Boiler type"),
                               tip = _U("Boiler type"))

        fs = FieldSizes(wHeight = HEIGHT_TE_MULTILINE, wLabel = LABEL_WIDTH_LEFT_SHORT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.tc4 = TextEntry(self.page1, maxchars = 200, value = '',
                             isMultiline = True,
                             label = _U("Reference"),
                             tip = _U("Source of data"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT_SHORT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        #
        # tab 2 - Technical data
        #
        self.frame_technical_data = wx.StaticBox(self.page2, -1, _U("Technical data"))
        self.frame_boiler_spec = wx.StaticBox(self.page2, -1, _U("Boiler specific technical parameters"))
        self.frame_technical_data.SetForegroundColour(TITLE_COLOR)
        self.frame_technical_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_technical_data.SetFont(fp.getFont())
        fp.popFont()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT_LONG - 50,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH_LARGE)

        self.tc5 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                              unitdict = 'POWER',
                              label = _U("Nominal thermal power"),
                              tip = _U("Nominal thermal power"))

        self.tc6 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                              unitdict = 'FRACTION',
                              label = _U("Nominal efficiency"),
                              tip = _U("Nominal efficiency"))

        self.tc7 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                              unitdict = 'POWER',
                              label = _U("Nominal fuel consumption (LCV)"),
                              tip = _U("Nominal fuel consumption (LCV)"))

        self.tc8 = ChoiceEntry(self.page2,
                               values = [],
                               label = _U("Fuel type"),
                               tip = _U("Fuel type"))

        self.tc9 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                              unitdict = 'POWER',
                              label = _U("Nominal electrical power consumption"),
                              tip = _U("Nominal electrical power consumption"))

        self.tc10 = wx.RadioBox(self.page2, -1, "Economiser", choices = ["No", "Yes"], majorDimension = 2)
        self.tc10.SetToolTip(wx.ToolTip(_U("Does the equipment include an economiser (water preheater)?")))

        self.tc11 = wx.RadioBox(self.page2, -1, "Preheater", choices = ["No", "Yes"], majorDimension = 2)
        self.tc11.SetToolTip(wx.ToolTip(_U("Does the equipment include an air preheater?")))

        self.tc12 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("Typical excess air ratio"),
                               tip = _U("Typical excess air ratio"))

        self.tc13 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("Linear dependence of the efficiency on the load"),
                               tip = _U("Linear dependence of the efficiency on the load"))

        self.tc14 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("Quadratic dependence of the efficiency on the load"),
                               tip = _U("Quadratic dependence of the efficiency on the load"))

        self.tc15 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                               unitdict = 'INVTEMP',
                               label = _U("Linear dependence of the efficiency on the temperature"),
                               tip = _U("Linear dependence of the efficiency on the temperature"))

        self.tc16 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                               unitdict = 'INVTEMP2',
                               label = _U("Quadratic dependence of the efficiency on the temperature"),
                               tip = _U("Quadratic dependence of the efficiency on the temperature"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT_LONG,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        #
        # tab 3 - Heat source / sink
        #
        self.frame_heat_source_sink = wx.StaticBox(self.page3, -1, _U("Heat source / sink"))
        self.frame_heat_source_sink.SetForegroundColour(TITLE_COLOR)
        self.frame_heat_source_sink.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_heat_source_sink.SetFont(fp.getFont())
        fp.popFont()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT_SHORT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.tc17 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                               unitdict = 'TEMPERATURE',
                               label = _U("Maximum outlet temperature"),
                               tip = _U("Maximum outlet temperature"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT_LONG,
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

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT_LONG,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH_LARGE)

        self.tc18 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                               unitdict = 'PRICE',
                               label = _U("Equipment price at factory applied installer's discount"),
                               tip = _U("Equipment price at factory applied installer's discount"))

        self.tc19 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                               unitdict = 'PRICE',
                               label = _U("Price of installed equipment"),
                               tip = _U("Price of installed equipment (including work, additional accessories, pumps, regulation, etc)"))

        self.tc20 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                               unitdict = 'UNITPRICE',
                               label = _U("Annual operational and maintenance fixed costs"),
                               tip = _U("Annual operational and maintenance fixed costs (approximate average per kW heating)"))

        self.tc21 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = -INFINITE, maxval = INFINITE, value = 0.,
                               unitdict = 'ENERGYTARIFF',
                               label = _U("Annual operational and maintenance variable costs dependant on usage"),
                               tip = _U("Annual operational and maintenance variable costs dependant on usage (approximate average per MWh heating)"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT_LONG,
                        wData = DATA_ENTRY_WIDTH_LEFT + UNITS_WIDTH_LARGE, wUnits = 0)

        self.tc22 = FloatEntry(self.page4,
                               ipart = 4, decimals = 0, minval = 1900, maxval = 2100, value = 2010,
                               label = _U("Year of last update of the economic data"),
                               tip = _U("Year of last update of the economic data"))


        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT_LONG,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

    def __do_layout(self):
        flagText = wx.TOP | wx.ALIGN_CENTER_HORIZONTAL

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)


        sizerPage0 = wx.StaticBoxSizer(self.frame_summary_table, wx.VERTICAL)
        sizerPage0.Add(self.grid, 1, wx.EXPAND | wx.ALL, 56)
        sizerPage0.Add(self.tc_type, 0, flagText | wx.ALIGN_RIGHT, VSEP)

        sizerPage0Help = wx.StaticBoxSizer(self.tc_help, wx.VERTICAL)
        sizerPage0Help.Add(self.tc_help_text, 0, wx.EXPAND | wx.ALL, VSEP)
        sizerPage0.Add(sizerPage0Help, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, VSEP)

        self.page0.SetSizer(sizerPage0)


        sizerPage1 = wx.StaticBoxSizer(self.frame_descriptive_data, wx.VERTICAL)
        sizerPage1.Add(self.tc1, 0, flagText, VSEP)
        sizerPage1.Add(self.tc2, 0, flagText, VSEP)
        sizerPage1.Add(self.tc3, 0, flagText, VSEP)
        sizerPage1.Add(self.tc4, 0, flagText, VSEP)

        self.page1.SetSizer(sizerPage1)


        sizerPage2_eco_preh = wx.BoxSizer(wx.HORIZONTAL)
        sizerPage2_eco_preh.Add(self.tc10, 0, flagText | wx.ALL, VSEP)
        sizerPage2_eco_preh.Add(self.tc11, 0, flagText | wx.ALL, VSEP)

        sizerPage2_boiler_spec = wx.StaticBoxSizer(self.frame_boiler_spec, wx.VERTICAL)
        sizerPage2_boiler_spec.Add(sizerPage2_eco_preh, 0, wx.ALIGN_RIGHT)
        sizerPage2_boiler_spec.Add(self.tc6, 0, flagText, VSEP)
        sizerPage2_boiler_spec.Add(self.tc12, 0, flagText, VSEP)
        sizerPage2_boiler_spec.Add(self.tc13, 0, flagText, VSEP)
        sizerPage2_boiler_spec.Add(self.tc14, 0, flagText, VSEP)
        sizerPage2_boiler_spec.Add(self.tc15, 0, flagText, VSEP)
        sizerPage2_boiler_spec.Add(self.tc16, 0, flagText, VSEP)

        sizerPage2 = wx.StaticBoxSizer(self.frame_technical_data, wx.VERTICAL)
        sizerPage2.Add(self.tc5, 0, flagText, VSEP)
        sizerPage2.Add(self.tc7, 0, flagText, VSEP)
        sizerPage2.Add(self.tc8, 0, flagText, VSEP)
        sizerPage2.Add(self.tc9, 0, flagText, VSEP)
        sizerPage2.Add(sizerPage2_boiler_spec, 0, flagText, VSEP)

        self.page2.SetSizer(sizerPage2)


        sizerPage3 = wx.StaticBoxSizer(self.frame_heat_source_sink, wx.VERTICAL)
        sizerPage3.Add(self.tc17, 0, flagText, VSEP)

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
#--- Public methods
#------------------------------------------------------------------------------

    def collectEntriesForDB(self):
        tmp = {
               "BoilerManufacturer":check(self.tc1.GetValue()),
               "BoilerModel":check(self.tc2.GetValue()),
               "BoilerType":check(self.tc3.GetValue(text = True)),
               "Reference":check(self.tc4.GetValue()),
               "BBPnom":check(self.tc5.GetValue()),
               "BBEfficiency":check(self.tc6.GetValue()),
               "FuelConsum":check(self.tc7.GetValue()),
               "FuelType":check(self.tc8.GetValue(text = True)),
               "ElConsum":check(self.tc9.GetValue()),
               "Economiser":check(self.tc10.GetStringSelection()),
               "Preheater":check(self.tc11.GetStringSelection()),
               "ExcessAirRatio":check(self.tc12.GetValue()),
               "BBA1":check(self.tc13.GetValue()),
               "BBA2":check(self.tc14.GetValue()),
               "BBK1":check(self.tc15.GetValue()),
               "BBK2":check(self.tc16.GetValue()),
               "BoilerTemp":check(self.tc17.GetValue()),
               "BoilerPrice":check(self.tc18.GetValue()),
               "BoilerTurnKeyPrice":check(self.tc19.GetValue()),
               "BoilerOandMfix":check(self.tc20.GetValue()),
               "BoilerOandMvar":check(self.tc21.GetValue()),
               "YearUpdate":check(self.tc22.GetValue())
               }
        return tmp

    def display(self, q = None):
        self.clear()

        fuelDict = FUELTYPES

        if q is not None:
            self.tc1.SetValue(str(q.BoilerManufacturer)) if q.BoilerManufacturer is not None else ''
            self.tc2.SetValue(str(q.BoilerModel)) if q.BoilerModel is not None else ''
            self.tc3.SetValue(str(q.BoilerType)) if q.BoilerType is not None else ''
            self.tc4.SetValue(str(q.Reference)) if q.Reference is not None else ''
            self.tc5.SetValue(str(q.BBPnom)) if q.BBPnom is not None else ''
            self.tc6.SetValue(str(q.BBEfficiency)) if q.BBEfficiency is not None else ''
            self.tc7.SetValue(str(q.FuelConsum)) if q.FuelConsum is not None else ''
            if q.FuelType is not None:
                self.tc8.SetValue(str(q.FuelType)) if str(q.FuelType) in fuelDict.values() else ''
            self.tc9.SetValue(str(q.ElConsum)) if q.ElConsum is not None else ''
            if q.Economiser is not None and q.Economiser.lower() == "yes":
                self.tc10.SetStringSelection("Yes")
            else:
                self.tc10.SetStringSelection("No")
            if q.Preheater is not None and q.Preheater.lower() == "yes":
                self.tc11.SetStringSelection("Yes")
            else:
                self.tc11.SetStringSelection("No")
            self.tc12.SetValue(str(q.ExcessAirRatio)) if q.ExcessAirRatio is not None else ''
            self.tc13.SetValue(str(q.BBA1)) if q.BBA1 is not None else ''
            self.tc14.SetValue(str(q.BBA2)) if q.BBA2 is not None else ''
            self.tc15.SetValue(str(q.BBK1)) if q.BBK1 is not None else ''
            self.tc16.SetValue(str(q.BBK2)) if q.BBK2 is not None else ''
            self.tc17.SetValue(str(q.BoilerTemp)) if q.BoilerTemp is not None else ''
            self.tc18.SetValue(str(q.BoilerPrice)) if q.BoilerPrice is not None else ''
            self.tc19.SetValue(str(q.BoilerTurnKeyPrice)) if q.BoilerTurnKeyPrice is not None else ''
            self.tc20.SetValue(str(q.BoilerOandMfix)) if q.BoilerOandMfix is not None else ''
            self.tc21.SetValue(str(q.BoilerOandMvar)) if q.BoilerOandMvar is not None else ''
            self.tc22.SetValue(str(q.YearUpdate)) if q.YearUpdate is not None else ''
        self.Show()

    def clear(self):
        self.tc1.SetValue('')
        self.tc2.SetValue('')
        self.tc3.SetValue('None')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
        self.tc6.SetValue('')
        self.tc7.SetValue('')
        self.tc8.SetValue('None')
        self.tc9.SetValue('')
        self.tc10.SetStringSelection('No')
        self.tc11.SetStringSelection('No')
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
        self.fillChoiceOfBoilerType(self.tc3.entry)
        self.fillChoiceOfDBFuel(self.tc8.entry)
        self.fillChoiceOfType()

    def getDBCol(self):
        return self.db.DBBoiler_ID

    def allFieldsEmpty(self):
        if len(self.tc1.GetValue()) == 0 and\
           len(self.tc2.GetValue()) == 0 and\
           self.tc3.GetValue(text = True) == "None" and\
           len(self.tc4.GetValue()) == 0 and\
           self.tc5.GetValue() is None and\
           self.tc6.GetValue() is None and\
           self.tc7.GetValue() is None and\
           self.tc8.GetValue(text = True) == "None" and\
           self.tc9.GetValue() is None and\
           self.tc10.GetStringSelection() == "No" and\
           self.tc11.GetStringSelection() == "No" and\
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
