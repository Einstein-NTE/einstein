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
#    PanelDBFuel: Database Design Assistant
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

class PanelDBFuel(PanelDBBase):
    def __init__(self, parent, title, closeOnOk = False):
        self.parent = parent
        self.title = title
        self.closeOnOk = closeOnOk
        self.name = "Fuel"
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

        PanelDBBase.__init__(self, self.parent, "Edit DBFuel", self.name)

        # DBFuel_ID needs to remain as first entry
        self.colLabels = "DBFuel_ID", "FuelName", "FuelType", "DBFuelUnit"

        self.db = Status.DB.dbfuel
        self.table = "dbfuel"
        self.identifier = self.colLabels[0]
        self.type = self.colLabels[2]

        # access to font properties object
        fp = FontProperties()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.notebook = wx.Notebook(self, -1, style = 0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page0, _U('Summary table'))
        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page1, _U('General information on fuel'))
        self.page2 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page2, _U('Main physical properties'))
        self.page3 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page3, _U('Properties for offgas calculations'))
        self.page4 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page4, _U('Environment parameters'))

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
        # tab 1 - General information on fuel
        #
        self.frame_general_information = wx.StaticBox(self.page1, -1, _U("General information on fuel"))
        self.frame_general_information.SetForegroundColour(TITLE_COLOR)
        self.frame_general_information.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_general_information.SetFont(fp.getFont())
        fp.popFont()

        self.tc1 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("FuelName"),
                             tip = _U("Name of the fuel"))

        self.tc2 = ChoiceEntry(self.page1,
                               values = [],
                               label = _U("FuelType"),
                               tip = _U("Fuel type"))

        self.tc3 = ChoiceEntry(self.page1,
                               values = [],
                               label = _U("DBFuelUnit"),
                               tip = _U("Default measurement unit"))

        self.tc4 = TextEntry(self.page1, maxchars = 200, value = '',
                             label = _U("FuelDataSource"),
                             tip = _U("Source of data"))

        self.tc5 = TextEntry(self.page1, maxchars = 200, value = '',
                             label = _U("FuelComment"),
                             tip = _U("Additional comments"))

        #
        # tab 2 - Main physical properties
        #
        self.frame_main_properties = wx.StaticBox(self.page2, -1, _U("Main physical properties"))
        self.frame_main_properties.SetForegroundColour(TITLE_COLOR)
        self.frame_main_properties.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_main_properties.SetFont(fp.getFont())
        fp.popFont()

        self.tc6 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              #unitdict = 'SPECIFICENTHALPY',
                              unitdict = 'FRACTION',
                              label = _U("FuelLCV"),
                              tip = _U("Lower calorific value"))

        self.tc7 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              #unitdict = 'SPECIFICENTHALPY',
                              unitdict = 'FRACTION',
                              label = _U("FuelHCV"),
                              tip = _U("Higher calorific value"))

        self.tc8 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              #unitdict = 'DENSITY',
                              unitdict = 'FRACTION',
                              label = _U("FuelDensity"),
                              tip = _U("Density"))

        #
        # tab 3 - Properties for offgas calculations
        #
        self.frame_offgas_properties = wx.StaticBox(self.page3, -1, _U("Properties for offgas calculations"))
        self.frame_offgas_properties.SetForegroundColour(TITLE_COLOR)
        self.frame_offgas_properties.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_offgas_properties.SetFont(fp.getFont())
        fp.popFont()

        self.tc9 = FloatEntry(self.page3,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              #unitdict = 'HEATCAPACITY',
                              unitdict = 'FRACTION',
                              label = _U("OffgasHeatCapacity"),
                              tip = _U("OffgasHeatCapacity"))

        self.tc10 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'DENSITY',
                               unitdict = 'FRACTION',
                               label = _U("OffgasDensity"),
                               tip = _U("OffgasDensity"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT + UNITS_WIDTH, wUnits = 0)

        self.tc11 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("Humidity"),
                               tip = _U("Humidity"))

        self.tc12 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("CombAir"),
                               tip = _U("CombAir"))

        self.tc13 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("Offgas"),
                               tip = _U("Offgas"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        #
        # tab 4 - Environment parameters
        #
        self.frame_environment_parameters = wx.StaticBox(self.page4, -1, _U("Environment parameters"))
        self.frame_environment_parameters.SetForegroundColour(TITLE_COLOR)
        self.frame_environment_parameters.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_environment_parameters.SetFont(fp.getFont())
        fp.popFont()

        self.tc14 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'DENSITY',
                               unitdict = 'FRACTION',
                               label = _U("PEConvFuel"),
                               tip = _U("Primary energy conversion ratio"))

        self.tc15 = FloatEntry(self.page4,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'CO2RATIO',
                               unitdict = 'FRACTION',
                               label = _U("CO2ConvFuel"),
                               tip = _U("Ratio of CO2 generation"))

    def __do_layout(self):
        flagText = wx.TOP | wx.ALIGN_CENTER_HORIZONTAL

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)

        sizerPage0 = wx.StaticBoxSizer(self.frame_summary_table, wx.VERTICAL)
        sizerPage0.Add(self.grid, 1, wx.EXPAND | wx.ALL, 56)
        sizerPage0.Add(self.tc_type, 0, flagText | wx.ALIGN_RIGHT, VSEP)

        self.page0.SetSizer(sizerPage0)


        sizerPage1 = wx.StaticBoxSizer(self.frame_general_information, wx.VERTICAL)
        sizerPage1.Add(self.tc1, 0, flagText, VSEP)
        sizerPage1.Add(self.tc2, 0, flagText, VSEP)
        sizerPage1.Add(self.tc3, 0, flagText, VSEP)
        sizerPage1.Add(self.tc4, 0, flagText, VSEP)
        sizerPage1.Add(self.tc5, 0, flagText, VSEP)

        self.page1.SetSizer(sizerPage1)


        sizerPage2 = wx.StaticBoxSizer(self.frame_main_properties, wx.VERTICAL)
        sizerPage2.Add(self.tc6, 0, flagText, VSEP)
        sizerPage2.Add(self.tc7, 0, flagText, VSEP)
        sizerPage2.Add(self.tc8, 0, flagText, VSEP)

        self.page2.SetSizer(sizerPage2)


        sizerPage3 = wx.StaticBoxSizer(self.frame_offgas_properties, wx.VERTICAL)
        sizerPage3.Add(self.tc9, 0, flagText, VSEP)
        sizerPage3.Add(self.tc10, 0, flagText, VSEP)
        sizerPage3.Add(self.tc11, 0, flagText, VSEP)
        sizerPage3.Add(self.tc12, 0, flagText, VSEP)
        sizerPage3.Add(self.tc13, 0, flagText, VSEP)

        self.page3.SetSizer(sizerPage3)


        sizerPage4 = wx.StaticBoxSizer(self.frame_environment_parameters, wx.VERTICAL)
        sizerPage4.Add(self.tc14, 0, flagText, VSEP)
        sizerPage4.Add(self.tc15, 0, flagText, VSEP)

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

        

# FIXXXME
        fuelDict = []
        fuelUnitDict = []

        tmp = {
               "FuelName":check(self.tc1.GetValue()),
               "FuelType":check(self.tc2.GetValue(text = True)),
#               "DBFuelUnit":check(findKey(fuelUnitDict, self.tc3.GetValue(text = True))),
               "FuelDataSource":check(self.tc4.GetValue()),
               "FuelComment":check(self.tc5.GetValue()),
               "FuelLCV":check(self.tc6.GetValue()),
               "FuelHCV":check(self.tc7.GetValue()),
               "FuelDensity":check(self.tc8.GetValue()),
               "OffgasHeatCapacity":check(self.tc9.GetValue()),
               "OffgasDensity":check(self.tc10.GetValue()),
               "Humidity":check(self.tc11.GetValue()),
               "CombAir":check(self.tc12.GetValue()),
               "Offgas":check(self.tc13.GetValue()),
               "PEConvFuel":check(self.tc14.GetValue()),
               "CO2ConvFuel":check(self.tc15.GetValue())
               }

        self.updateValues(tmp)

        if self.closeOnOk:
            self.EndModal(wx.ID_OK)

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------

    def display(self, q = None):
        self.clear()

        self.fillChoiceOfDBFuelType(self.tc2.entry)

# FIXXXME
        #self.fillChoiceOfDBFuelUnits(self.tc3.entry)

        if q is not None:
            self.tc1.SetValue(str(q.FuelName)) if q.FuelName is not None else ''
            if q.FuelType is not None:
                self.tc2.entry.SetStringSelection(q.FuelType)
#            if q.DBFuelUnit is not None:
#                self.tc3.SetValue(fuelUnitDict[int(q.DBFuelUnit)]) if int(q.DBFuelUnit) in fuelUnitDict.keys() else ''
            self.tc4.SetValue(str(q.FuelDataSource)) if q.FuelDataSource is not None else ''
            self.tc5.SetValue(str(q.FuelComment)) if q.FuelComment is not None else ''
            self.tc6.SetValue(str(q.FuelLCV)) if q.FuelLCV is not None else ''
            self.tc7.SetValue(str(q.FuelHCV)) if q.FuelHCV is not None else ''
            self.tc8.SetValue(str(q.FuelDensity)) if q.FuelDensity is not None else ''
            self.tc9.SetValue(str(q.OffgasHeatCapacity)) if q.OffgasHeatCapacity is not None else ''
            self.tc10.SetValue(str(q.OffgasDensity)) if q.OffgasDensity is not None else ''
            self.tc11.SetValue(str(q.Humidity)) if q.Humidity is not None else ''
            self.tc12.SetValue(str(q.CombAir)) if q.CombAir is not None else ''
            self.tc13.SetValue(str(q.Offgas)) if q.Offgas is not None else ''
            self.tc14.SetValue(str(q.PEConvFuel)) if q.PEConvFuel is not None else ''
            self.tc15.SetValue(str(q.CO2ConvFuel)) if q.CO2ConvFuel is not None else ''
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

    def fillChoices(self):
# FIXXXME
        self.fillChoiceOfDBFuelType(self.tc2.entry)
        #self.fillChoiceOfDBFuelUnits(self.tc3.entry)
        self.fillChoiceOfType()

    def getDBCol(self):
        return self.db.DBFuel_ID

    def allFieldsEmpty(self):
        if len(self.tc1.GetValue()) == 0 and\
           self.tc2.GetValue(text = True) == "None" and\
           len(self.tc4.GetValue()) == 0 and\
           len(self.tc5.GetValue()) == 0 and\
           self.tc6.GetValue() is None and\
           self.tc7.GetValue() is None and\
           self.tc8.GetValue() is None and\
           self.tc9.GetValue() is None and\
           self.tc10.GetValue() is None and\
           self.tc11.GetValue() is None and\
           self.tc12.GetValue() is None and\
           self.tc13.GetValue() is None and\
           self.tc14.GetValue() is None and\
           self.tc15.GetValue() is None:
            return True
        else:
            return False
