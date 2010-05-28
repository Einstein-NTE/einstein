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
#    PanelDBSolarThermal: Database Design Assistant
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

class PanelDBSolarThermal(PanelDBBase):
    def __init__(self, parent, title, closeOnOk = False):
        self.parent = parent
        self.title = title
        self.closeOnOk = closeOnOk
        self.name = "SolarThermal"
        self._init_ctrls(parent)
        self._init_grid(125)
        self.__do_layout()
        self.clear()
        self.fillEquipmentList()
        self.fillChoices()

    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        PanelDBBase.__init__(self, self.parent, "Edit DBSolarThermal", self.name)

        # DBSolarThermal_ID needs to remain as first entry
        self.colLabels = "DBSolarThermal_ID", "STManufacturer", "STModel", "STType", "STPnomColl"

        self.db = Status.DB.dbsolarthermal
        self.table = "dbsolarthermal"
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
        self.notebook.AddPage(self.page1, _U('Descriptive Data'))
        self.page2 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page2, _U('Technical Data'))
        self.page3 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page3, _U('Economic Parameters'))

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
        # tab 1 - Descriptive Data
        #
        self.frame_descriptive_data = wx.StaticBox(self.page1, -1, _U("Descriptive data"))
        self.frame_descriptive_data.SetForegroundColour(TITLE_COLOR)
        self.frame_descriptive_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_descriptive_data.SetFont(fp.getFont())
        fp.popFont()

        self.tc1 = TextEntry(self.page1, maxchars = 20, value = '',
                             label = _U("STManufacturer"),
                             tip = _U("Solarthermal Manufacturer"))

        self.tc2 = TextEntry(self.page1, maxchars = 20, value = '',
                             label = _U("STModel"),
                             tip = _U("Solarthermal Model"))

        self.tc3 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("STType"),
                             tip = _U("Solarthermal Type"))

        self.tc4 = TextEntry(self.page1, maxchars = 200, value = '',
                             label = _U("STReference"),
                             tip = _U("Source of data"))

        #
        # tab 2 - Technical data
        #
        self.frame_technical_data = wx.StaticBox(self.page2, -1, _U("Technical data"))
        self.frame_col_eff_par = wx.StaticBox(self.page2, -1, _U("Collector efficiency parameters"))
        self.frame_col_dim_wei = wx.StaticBox(self.page2, -1, _U("Collector dimension and weight"))
        self.frame_technical_data.SetForegroundColour(TITLE_COLOR)
        self.frame_technical_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_technical_data.SetFont(fp.getFont())
        fp.popFont()

        self.tc5 = StaticTextEntry(self.page2, maxchars = 255, value = '',
                                   label = _U("STPnomColl"),
                                   tip = _U("STPnomColl"))

        self.tc6 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'FRACTION',
                              label = _U("STc0"),
                              tip = _U("Optical efficiency"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT + UNITS_WIDTH, wUnits = 0)

        self.tc7 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("STc1"),
                              tip = _U("Linear thermal loss coefficient"))

        self.tc8 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("STc2"),
                              tip = _U("Quadratic thermal loss coefficient"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.tc9 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'FRACTION',
                              label = _U("K50L"),
                              tip = unicode("Incidence angle correction factor at 50º (longitudinal)", 'latin-1'))

        self.tc10 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("K50T"),
                               tip = unicode("Incidence angle correction factor at 50º (transversal)", 'latin-1'))

        self.tc11 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'MASSORVOLUMEFLOW',
                               label = _U("STMassFlowRate"),
                               tip = _U("Recommended collector mass flow rate"))

        self.tc12 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'LENGTH',
                               label = _U("STLengthGross"),
                               tip = _U("STLengthGross"))

        self.tc13 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'LENGTH',
                               label = _U("STHeightGross"),
                               tip = _U("STHeightGross"))

        self.tc14 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'AREA',
                               label = _U("STAreaGross"),
                               tip = _U("STAreaGross"))

        self.tc15 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'LENGTH',
                               label = _U("STLengthAper"),
                               tip = _U("STLengthAper"))

        self.tc16 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'LENGTH',
                               label = _U("STHeightAper"),
                               tip = _U("STHeightAper"))

        self.tc17 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'AREA',
                               label = _U("STAreaAper"),
                               tip = _U("STAreaAper"))

        self.tc18 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("STAreaFactor"),
                               tip = _U("STAreaFactor"))

        self.tc19 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'MASSPERAREA',
                               unitdict = 'FRACTION',
                               label = _U("STWeightFactor"),
                               tip = _U("STWeightFactor"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        #
        # tab 3 - Economic Parameters
        #
        self.frame_economic_parameters = wx.StaticBox(self.page3, -1, _U("Economic parameters"))
        self.frame_economic_parameters.SetForegroundColour(TITLE_COLOR)
        self.frame_economic_parameters.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_economic_parameters.SetFont(fp.getFont())
        fp.popFont()

        self.tc20 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'UNITPRICE',
                               unitdict = 'FRACTION',
                               label = _U("STUnitPrice300kW"),
                               tip = _U("STUnitPrice300kW"))

        self.tc21 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'UNITPRICE',
                               unitdict = 'FRACTION',
                               label = _U("STUnitTurnKeyPrice30kW"),
                               tip = _U("STUnitTurnKeyPrice30kW"))

        self.tc22 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'UNITPRICE',
                               unitdict = 'FRACTION',
                               label = _U("STUnitTurnKeyPrice300kW"),
                               tip = _U("STUnitTurnKeyPrice300kW"))

        self.tc23 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'UNITPRICE',
                               unitdict = 'FRACTION',
                               label = _U("STUnitTurnKeyPrice3000kW"),
                               tip = _U("STUnitTurnKeyPrice3000kW"))

        self.tc24 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               #unitdict = 'UNITPRICE',
                               unitdict = 'FRACTION',
                               label = _U("STOMUnitFix"),
                               tip = _U("STOMUnitFix"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT + UNITS_WIDTH, wUnits = 0)

        self.tc25 = FloatEntry(self.page3,
                               ipart = 4, decimals = 0, minval = 1900, maxval = 2100, value = 2010,
                               label = _U("STYearUpdate"),
                               tip = _U("Year of last update of the economic data"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

    def __do_layout(self):
        #flagText_left = wx.TOP | wx.ALIGN_LEFT
        flagText = wx.TOP | wx.ALIGN_CENTER_HORIZONTAL

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)


        sizerPage0 = wx.StaticBoxSizer(self.frame_summary_table, wx.VERTICAL)
        sizerPage0.Add(self.grid, 1, wx.EXPAND | wx.ALL, 56)
        sizerPage0.Add(self.tc_type, 0, wx.TOP | wx.ALIGN_RIGHT, VSEP)

        self.page0.SetSizer(sizerPage0)


        sizerPage1 = wx.StaticBoxSizer(self.frame_descriptive_data, wx.VERTICAL)
        sizerPage1.Add(self.tc1, 0, flagText, VSEP)
        sizerPage1.Add(self.tc2, 0, flagText, VSEP)
        sizerPage1.Add(self.tc3, 0, flagText, VSEP)
        sizerPage1.Add(self.tc4, 0, flagText, VSEP)

        self.page1.SetSizer(sizerPage1)


        sizerPage2 = wx.StaticBoxSizer(self.frame_technical_data, wx.VERTICAL)
        sizerPage2.Add(self.tc5, 0, flagText, VSEP)

        sizerPage2_eff = wx.StaticBoxSizer(self.frame_col_eff_par, wx.VERTICAL)
        sizerPage2_eff.Add(self.tc6, 0, flagText, VSEP)
        sizerPage2_eff.Add(self.tc7, 0, flagText, VSEP)
        sizerPage2_eff.Add(self.tc8, 0, flagText, VSEP)
        sizerPage2_eff.Add(self.tc9, 0, flagText, VSEP)
        sizerPage2_eff.Add(self.tc10, 0, flagText, VSEP)
        sizerPage2_eff.Add(self.tc11, 0, flagText, VSEP)

        sizerPage2.Add(sizerPage2_eff, 0, flagText, VSEP)

        sizerPage2_dim_gross = wx.BoxSizer(wx.VERTICAL)
        sizerPage2_dim_gross.Add(self.tc12, 0, flagText, VSEP)
        sizerPage2_dim_gross.Add(self.tc13, 0, flagText, VSEP)
        sizerPage2_dim_gross.Add(self.tc14, 0, flagText, VSEP)

        sizerPage2_dim_aper = wx.BoxSizer(wx.VERTICAL)
        sizerPage2_dim_aper.Add(self.tc15, 0, flagText, VSEP)
        sizerPage2_dim_aper.Add(self.tc16, 0, flagText, VSEP)
        sizerPage2_dim_aper.Add(self.tc17, 0, flagText, VSEP)

        sizerPage2_dim = wx.StaticBoxSizer(self.frame_col_dim_wei, wx.HORIZONTAL)
        sizerPage2_dim.Add(sizerPage2_dim_gross)
        sizerPage2_dim.Add(sizerPage2_dim_aper)

        sizerPage2.Add(sizerPage2_dim, 0, flagText, VSEP)
        sizerPage2.Add(self.tc18, 0, flagText, VSEP)
        sizerPage2.Add(self.tc19, 0, flagText, VSEP)

        self.page2.SetSizer(sizerPage2)


        sizerPage3 = wx.StaticBoxSizer(self.frame_economic_parameters, wx.VERTICAL)
        sizerPage3.Add(self.tc20, 0, flagText, VSEP)
        sizerPage3.Add(self.tc21, 0, flagText, VSEP)
        sizerPage3.Add(self.tc22, 0, flagText, VSEP)
        sizerPage3.Add(self.tc23, 0, flagText, VSEP)
        sizerPage3.Add(self.tc24, 0, flagText, VSEP)
        sizerPage3.Add(self.tc25, 0, flagText, VSEP)

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
               "STManufacturer":check(self.tc1.GetValue()),
               "STModel":check(self.tc2.GetValue()),
               "STType":check(self.tc3.GetValue()),
               "STReference":check(self.tc4.GetValue()),
               "STc0":check(self.tc6.GetValue()),
               "STc1":check(self.tc7.GetValue()),
               "STc2":check(self.tc8.GetValue()),
               "K50L":check(self.tc9.GetValue()),
               "K50T":check(self.tc10.GetValue()),
               "STMassFlowRate":check(self.tc11.GetValue()),
               "STLengthGross":check(self.tc12.GetValue()),
               "STHeightGross":check(self.tc13.GetValue()),
               "STAreaGross":check(self.tc14.GetValue()),
               "STLengthAper":check(self.tc15.GetValue()),
               "STHeightAper":check(self.tc16.GetValue()),
               "STAreaAper":check(self.tc17.GetValue()),
               "STAreaFactor":check(self.tc18.GetValue()),
               "STWeightFactor":check(self.tc19.GetValue()),
               "STUnitPrice300kW":check(self.tc20.GetValue()),
               "STUnitTurnKeyPrice30kW":check(self.tc21.GetValue()),
               "STUnitTurnKeyPrice300kW":check(self.tc22.GetValue()),
               "STUnitTurnKeyPrice3000kW":check(self.tc23.GetValue()),
               "STOMUnitFix":check(self.tc24.GetValue()),
               "STYearUpdate":check(self.tc25.GetValue())
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
            self.tc1.SetValue(str(q.STManufacturer)) if q.STManufacturer is not None else ''
            self.tc2.SetValue(str(q.STModel)) if q.STModel is not None else ''
            self.tc3.SetValue(str(q.STType)) if q.STType is not None else ''
            self.tc4.SetValue(str(q.STReference)) if q.STReference is not None else ''
            self.tc5.SetValue(str(q.STPnomColl)) if q.STPnomColl is not None else ''
            self.tc6.SetValue(str(q.STc0)) if q.STc0 is not None else ''
            self.tc7.SetValue(str(q.STc1)) if q.STc1 is not None else ''
            self.tc8.SetValue(str(q.STc2)) if q.STc2 is not None else ''
            self.tc9.SetValue(str(q.K50L)) if q.K50L is not None else ''
            self.tc10.SetValue(str(q.K50T)) if q.K50T is not None else ''
            self.tc11.SetValue(str(q.STMassFlowRate)) if q.STMassFlowRate is not None else ''
            self.tc12.SetValue(str(q.STLengthGross)) if q.STLengthGross is not None else ''
            self.tc13.SetValue(str(q.STHeightGross)) if q.STHeightGross is not None else ''
            self.tc14.SetValue(str(q.STAreaGross)) if q.STAreaGross is not None else ''
            self.tc15.SetValue(str(q.STLengthAper)) if q.STLengthAper is not None else ''
            self.tc16.SetValue(str(q.STHeightAper)) if q.STHeightAper is not None else ''
            self.tc17.SetValue(str(q.STAreaAper)) if q.STAreaAper is not None else ''
            self.tc18.SetValue(str(q.STAreaFactor)) if q.STAreaFactor is not None else ''
            self.tc19.SetValue(str(q.STWeightFactor)) if q.STWeightFactor is not None else ''
            self.tc20.SetValue(str(q.STUnitPrice300kW)) if q.STUnitPrice300kW is not None else ''
            self.tc21.SetValue(str(q.STUnitTurnKeyPrice30kW)) if q.STUnitTurnKeyPrice30kW is not None else ''
            self.tc22.SetValue(str(q.STUnitTurnKeyPrice300kW)) if q.STUnitTurnKeyPrice300kW is not None else ''
            self.tc23.SetValue(str(q.STUnitTurnKeyPrice3000kW)) if q.STUnitTurnKeyPrice3000kW is not None else ''
            self.tc24.SetValue(str(q.STOMUnitFix)) if q.STOMUnitFix is not None else ''
            self.tc25.SetValue(str(q.STYearUpdate)) if q.STYearUpdate is not None else ''
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

    def fillChoices(self):
        self.fillChoiceOfType()

    def getDBCol(self):
        return self.db.DBSolarThermal_ID

    def allFieldsEmpty(self):
        if len(self.tc1.GetValue()) == 0 and\
           len(self.tc2.GetValue()) == 0 and\
           len(self.tc3.GetValue()) == 0 and\
           len(self.tc4.GetValue()) == 0 and\
           self.tc6.GetValue() is None and\
           self.tc7.GetValue() is None and\
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
           self.tc22.GetValue() is None and\
           self.tc23.GetValue() is None and\
           self.tc24.GetValue() is None and\
           self.tc25.GetValue() is None:
            return True
        else:
            return False
