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
LABEL_WIDTH_LEFT = 140
DATA_ENTRY_WIDTH_LEFT = 140
UNITS_WIDTH = 55

VSEP = 4

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

class PanelDBFluid(PanelDBBase):
    def __init__(self, parent, title, closeOnOk = False):
        self.parent = parent
        self.title = title
        self.closeOnOk = closeOnOk
        self.name = "Fluid"
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

        PanelDBBase.__init__(self, self.parent, "Edit DBFluid", self.name)

        # DBFluid_ID needs to remain as first entry
        self.colLabels = "DBFluid_ID", "FluidName", "RefrigerantCode"

        self.db = Status.DB.dbfluid
        self.table = "dbfluid"
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
        self.notebook.AddPage(self.page1, _U('General information on fluid'))
        self.page2 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page2, _U('Main physical properties'))
        self.page3 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page3, _U('Specific properties required only for refrigerants'))

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
        # tab 1 - General information on fluid
        #
        self.frame_general_information = wx.StaticBox(self.page1, -1, _U("General information on fluid"))
        self.frame_general_information.SetForegroundColour(TITLE_COLOR)
        self.frame_general_information.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_general_information.SetFont(fp.getFont())
        fp.popFont()

        self.tc1 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("FluidName"),
                             tip = _U("Name of the fluid"))

        self.tc2 = TextEntry(self.page1, maxchars = 6, value = '',
                             label = _U("RefrigerantCode"),
                             tip = _U("Refrigerant code"))

        self.tc3 = TextEntry(self.page1, maxchars = 200, value = '',
                             label = _U("FluidDataSource"),
                             tip = _U("Source of data"))

        self.tc4 = TextEntry(self.page1, maxchars = 200, value = '',
                             label = _U("FluidComment"),
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

        self.tc5 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              #unitdict = 'HEATCAPACITY',
                              unitdict = 'FRACTION',
                              label = _U("FluidCp"),
                              tip = _U("Specific heat in liquid state"))

        self.tc6 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              #unitdict = 'TEMPERATURE',
                              unitdict = 'FRACTION',
                              label = _U("TCond"),
                              tip = _U("Temperature of evaporation"))

        self.tc7 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              #unitdict = 'HEATCAPACITY',
                              unitdict = 'FRACTION',
                              label = _U("FluidCpG"),
                              tip = _U("Specific heat in gaseous state (vapour)"))

        self.tc8 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              #unitdict = 'SPECIFICENTHALPY',
                              unitdict = 'FRACTION',
                              label = _U("LatentHeat"),
                              tip = _U("Latent heat of evaporation"))

        self.tc9 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              #unitdict = 'DENSITY',
                              unitdict = 'FRACTION',
                              label = _U("FluidDensity"),
                              tip = _U("Density"))

        #
        # tab 3 - Specific properties required only for refrigerants
        #
        self.frame_refrigerant_properties = wx.StaticBox(self.page3, -1, _U("Specific properties required only for refrigerants"))
        self.frame_refrigerant_properties.SetForegroundColour(TITLE_COLOR)
        self.frame_refrigerant_properties.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_refrigerant_properties.SetFont(fp.getFont())
        fp.popFont()

        self.tc10 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'CO2RATIO',
                               unitdict = 'FRACTION',
                               label = _U("SpecificMassFlow"),
                               tip = _U("Typical specific mass flow of refrigerant"))

        self.tc11 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'TEMPERATURE',
                               unitdict = 'FRACTION',
                               label = _U("THighP"),
                               tip = _U("Typical outlet temperature of compressor"))

        self.tc12 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'DYNAMICVISCOSITY',
                               unitdict = 'FRACTION',
                               label = _U("Viscosity"),
                               tip = _U("Dynamic Viscosity at typical working conditions"))

        self.tc13 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'CONDUCTIVITY',
                               unitdict = 'FRACTION',
                               label = _U("Conductivity"),
                               tip = _U("Thermal conductivity at typical working conditions"))

        self.tc14 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'SPECIFICENTHALPY',
                               unitdict = 'FRACTION',
                               label = _U("SensibleHeat"),
                               tip = _U("Senisble heat at typical working conditions"))

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

        self.page1.SetSizer(sizerPage1)


        sizerPage2 = wx.StaticBoxSizer(self.frame_main_properties, wx.VERTICAL)
        sizerPage2.Add(self.tc5, 0, flagText, VSEP)
        sizerPage2.Add(self.tc6, 0, flagText, VSEP)
        sizerPage2.Add(self.tc7, 0, flagText, VSEP)
        sizerPage2.Add(self.tc8, 0, flagText, VSEP)
        sizerPage2.Add(self.tc9, 0, flagText, VSEP)

        self.page2.SetSizer(sizerPage2)


        sizerPage3 = wx.StaticBoxSizer(self.frame_refrigerant_properties, wx.VERTICAL)
        sizerPage3.Add(self.tc10, 0, flagText, VSEP)
        sizerPage3.Add(self.tc11, 0, flagText, VSEP)
        sizerPage3.Add(self.tc12, 0, flagText, VSEP)
        sizerPage3.Add(self.tc13, 0, flagText, VSEP)
        sizerPage3.Add(self.tc14, 0, flagText, VSEP)

        self.page3.SetSizer(sizerPage3)


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
               "FluidName":check(self.tc1.GetValue()),
               "RefrigerantCode":check(self.tc2.GetValue()),
               "FluidDataSource":check(self.tc3.GetValue()),
               "FluidComment":check(self.tc4.GetValue()),
               "FluidCp":check(self.tc5.GetValue()),
               "TCond":check(self.tc6.GetValue()),
               "FluidCpG":check(self.tc7.GetValue()),
               "LatentHeat":check(self.tc8.GetValue()),
               "FluidDensity":check(self.tc9.GetValue()),
               "SpecificMassFlow":check(self.tc10.GetValue()),
               "THighP":check(self.tc11.GetValue()),
               "Viscosity":check(self.tc12.GetValue()),
               "Conductivity":check(self.tc13.GetValue()),
               "SensibleHeat":check(self.tc14.GetValue())
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
            self.tc1.SetValue(str(q.FluidName)) if q.FluidName is not None else ''
            self.tc2.SetValue(str(q.RefrigerantCode)) if q.RefrigerantCode is not None else ''
            self.tc3.SetValue(str(q.FluidDataSource)) if q.FluidDataSource is not None else ''
            self.tc4.SetValue(str(q.FluidComment)) if q.FluidComment is not None else ''
            self.tc5.SetValue(str(q.FluidCp)) if q.FluidCp is not None else ''
            self.tc6.SetValue(str(q.TCond)) if q.TCond is not None else ''
            self.tc7.SetValue(str(q.FluidCpG)) if q.FluidCpG is not None else ''
            self.tc8.SetValue(str(q.LatentHeat)) if q.LatentHeat is not None else ''
            self.tc9.SetValue(str(q.FluidDensity)) if q.FluidDensity is not None else ''
            self.tc10.SetValue(str(q.SpecificMassFlow)) if q.SpecificMassFlow is not None else ''
            self.tc11.SetValue(str(q.THighP)) if q.THighP is not None else ''
            self.tc12.SetValue(str(q.Viscosity)) if q.Viscosity is not None else ''
            self.tc13.SetValue(str(q.Conductivity)) if q.Conductivity is not None else ''
            self.tc14.SetValue(str(q.SensibleHeat)) if q.SensibleHeat is not None else ''
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

    def fillChoices(self):
        self.fillChoiceOfType()

    def getDBCol(self):
        return self.db.DBFluid_ID

    def allFieldsEmpty(self):
        if len(self.tc1.GetValue()) == 0 and\
           len(self.tc2.GetValue()) == 0 and\
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
           self.tc14.GetValue() is None:
            return True
        else:
            return False
