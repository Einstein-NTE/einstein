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
#    PanelDBElectricityMix: Database Design Assistant
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
LABEL_WIDTH_LEFT = 250
DATA_ENTRY_WIDTH_LEFT = 140
UNITS_WIDTH = 55

VSEP = 4

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

class PanelDBElectricityMix(PanelDBBase):
    def __init__(self, parent, title, closeOnOk = False):
        self.parent = parent
        self.title = title
        self.closeOnOk = closeOnOk
        self.name = "ElectricityMix"
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

        PanelDBBase.__init__(self, self.parent, "Edit DBElectricityMix", self.name)

        # id needs to remain as first entry
        self.colLabels = "id", "Country", "Year", "Type"

        self.db = Status.DB.dbelectricitymix
        self.table = "dbelectricitymix"
        self.identifier = self.colLabels[0]
        self.type = self.colLabels[3]

        # access to font properties object
        fp = FontProperties()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.notebook = wx.Notebook(self, -1, style = 0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page0, _U('Summary table'))
        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page1, _U('General information'))
        self.page2 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page2, _U('Data'))

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
        # tab 1 - General information
        #
        self.frame_general_information = wx.StaticBox(self.page1, -1, _U("General information"))
        self.frame_general_information.SetForegroundColour(TITLE_COLOR)
        self.frame_general_information.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_general_information.SetFont(fp.getFont())
        fp.popFont()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT + UNITS_WIDTH, wUnits = 0)

        self.tc1 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Country"),
                             tip = _U("Country or region"))

        self.tc2 = FloatEntry(self.page1,
                              ipart = 4, decimals = 0, minval = 1900, maxval = 2100, value = 2010,
                              label = _U("Year"),
                              tip = _U("Year of data"))

        self.tc3 = TextEntry(self.page1, maxchars = 20, value = '',
                             label = _U("Type of electricity (user, source, supplier, etc.)"),
                             tip = _U("Specify e.g. average of national grid, high voltage grid, ..."))

        self.tc4 = TextEntry(self.page1, maxchars = 200, value = '',
                             label = _U("Bibliographic reference / data source"),
                             tip = _U("Please give a full reference of the data source that allows for tracking back the data"))

        self.tc5 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("AuditorID"),
                              tip = _U("Auditor responsible for data set"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        #
        # tab 2 - Data
        #
        self.frame_data = wx.StaticBox(self.page2, -1, _U("Data"))
        self.frame_percentage_of_generation = wx.StaticBox(self.page2, -1, _U("Percentage of generation by:"))
        self.frame_data.SetForegroundColour(TITLE_COLOR)
        self.frame_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_data.SetFont(fp.getFont())
        fp.popFont()

        self.tc6 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'FRACTION',
                              label = _U("Primary energy per unit of electricity"),
                              tip = _U("Only non-renewable part of primary energy"))

        self.tc7 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              #unitdict = 'CO2RATIO',
                              unitdict = 'FRACTION',
                              label = _U("CO2ConvEl"),
                              tip = _U("CO2 generation per unit of electricity"))

        self.tc8 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              #unitdict = 'CO2RATIO',
                              unitdict = 'FRACTION',
                              label = _U("NoNukesConvEl"),
                              tip = _U("Highly radiactive nuclear waste per unit of electricity"))

        self.tc9 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'FRACTION',
                              label = _U("PercNaturalGas"),
                              tip = _U("natural gas"))

        self.tc10 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("PercCarbon"),
                               tip = _U("carbon"))

        self.tc11 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("PercOil"),
                               tip = _U("oil"))

        self.tc12 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("PercRenewables"),
                               tip = _U("renewables"))

        self.tc13 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("PercNukes"),
                               tip = _U("nuclear"))

        self.tc14 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("PercCHP"),
                               tip = _U("CHP (except CHP using renewables)"))

        self.tc15 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("PercOther"),
                               tip = _U("other"))

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


        sizerPage2_perc = wx.StaticBoxSizer(self.frame_percentage_of_generation, wx.VERTICAL)
        sizerPage2_perc.Add(self.tc9, 0, flagText, VSEP)
        sizerPage2_perc.Add(self.tc10, 0, flagText, VSEP)
        sizerPage2_perc.Add(self.tc11, 0, flagText, VSEP)
        sizerPage2_perc.Add(self.tc12, 0, flagText, VSEP)
        sizerPage2_perc.Add(self.tc13, 0, flagText, VSEP)
        sizerPage2_perc.Add(self.tc14, 0, flagText, VSEP)
        sizerPage2_perc.Add(self.tc15, 0, flagText, VSEP)

        sizerPage2 = wx.StaticBoxSizer(self.frame_data, wx.VERTICAL)
        sizerPage2.Add(self.tc6, 0, flagText, VSEP)
        sizerPage2.Add(self.tc7, 0, flagText, VSEP)
        sizerPage2.Add(self.tc8, 0, flagText, VSEP)
        sizerPage2.Add(sizerPage2_perc, 0, flagText, VSEP)

        self.page2.SetSizer(sizerPage2)


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

        tmp = {
               "Country":check(self.tc1.GetValue()),
               "Year":check(self.tc2.GetValue()),
               "Type":check(self.tc3.GetValue()),
               "Reference":check(self.tc4.GetValue()),
               "AuditorID":check(self.tc5.GetValue()),
               "PE2ConvEl":check(self.tc6.GetValue()),
               "CO2ConvEl":check(self.tc7.GetValue()),
               "NoNukesConvEl":check(self.tc8.GetValue()),
               "PercNaturalGas":check(self.tc9.GetValue()),
               "PercCarbon":check(self.tc10.GetValue()),
               "PercOil":check(self.tc11.GetValue()),
               "PercRenewables":check(self.tc12.GetValue()),
               "PercNukes":check(self.tc13.GetValue()),
               "PercCHP":check(self.tc14.GetValue()),
               "PercOther":check(self.tc15.GetValue())
               }

        self.updateValues(tmp)

        if self.closeOnOk:
            self.EndModal(wx.ID_OK)

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------

    def display(self, q = None):
        self.clear()

        if q is not None:
            self.tc1.SetValue(str(q.Country)) if q.Country is not None else ''
            self.tc1.SetValue(str(q.Year)) if q.Year is not None else ''
            self.tc1.SetValue(str(q.Type)) if q.Type is not None else ''
            self.tc1.SetValue(str(q.Reference)) if q.Reference is not None else ''
            self.tc1.SetValue(str(q.AuditorID)) if q.AuditorID is not None else ''
            self.tc1.SetValue(str(q.PE2ConvEl)) if q.PE2ConvEl is not None else ''
            self.tc1.SetValue(str(q.CO2ConvEl)) if q.CO2ConvEl is not None else ''
            self.tc1.SetValue(str(q.NoNukesConvEl)) if q.NoNukesConvEl is not None else ''
            self.tc1.SetValue(str(q.PercNaturalGas)) if q.PercNaturalGas is not None else ''
            self.tc1.SetValue(str(q.PercCarbon)) if q.PercCarbon is not None else ''
            self.tc1.SetValue(str(q.PercOil)) if q.PercOil is not None else ''
            self.tc1.SetValue(str(q.PercRenewables)) if q.PercRenewables is not None else ''
            self.tc1.SetValue(str(q.PercNukes)) if q.PercNukes is not None else ''
            self.tc1.SetValue(str(q.PercCHP)) if q.PercCHP is not None else ''
            self.tc1.SetValue(str(q.PercOther)) if q.PercOther is not None else ''
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
        self.fillChoiceOfType()

    def getDBCol(self):
        return self.db.id

    def allFieldsEmpty(self):
        if len(self.tc1.GetValue()) == 0 and\
           self.tc2.GetValue() is None and\
           len(self.tc3.GetValue()) == 0 and\
           len(self.tc4.GetValue()) == 0 and\
           self.tc5.GetValue() is None and\
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
