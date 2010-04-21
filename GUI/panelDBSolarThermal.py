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
from einstein.GUI.panelBaseDBEditor import *

HEIGHT = 20
LABEL_WIDTH_LEFT = 140
DATA_ENTRY_WIDTH_LEFT = 140
UNITS_WIDTH = 55

def _U(text):
    return unicode(_(text), "utf-8")

class PanelDBSolarThermal(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self._init_ctrls(parent)
        self.__do_layout()
        self.fillEquipmentList()

    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id = -1, name = 'PanelDBSolarthermal', parent = parent,
              pos = wx.Point(0, 0), size = wx.Size(780, 580))
        self.Hide()

        # access to font properties object
        fp = FontProperties()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.notebook = wx.Notebook(self, -1, style = 0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = PanelBaseDBEditor(self.notebook, 'Descriptive Data', 'List of solarthermals',
                                       'Add Equipment', 'Delete Equipment')

#        self.page0 = wx.Panel(self.notebook)
#        self.notebook.AddPage(self.page0, _U('Descriptive Data'))

        self.page1 = PanelBaseDBEditor(self.notebook, 'Technical Data', 'List of solarthermals',
                                       'Add Equipment', 'Delete Equipment')
#        self.page1 = wx.Panel(self.notebook)
#        self.notebook.AddPage(self.page1, _U('Technical Data'))

        self.page2 = PanelBaseDBEditor(self.notebook, 'Economic Parameters', 'List of solarthermals',
                                       'Add Equipment', 'Delete Equipment')

#        self.page2 = wx.Panel(self.notebook)
#        self.notebook.AddPage(self.page2, _U('Economic Parameters'))

        self.notebook.AddPage(self.page0, _U('Descriptive Data'))
        self.notebook.AddPage(self.page1, _U('Technical Data'))
        self.notebook.AddPage(self.page2, _U('Economic Parameters'))

#        self.frame_descriptive_data = wx.StaticBox(self.page0, -1,_U("Descriptive Data"))
#        self.frame_descriptive_data.SetForegroundColour(TITLE_COLOR)
#        self.frame_descriptive_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
#
#        self.frame_technical_data = wx.StaticBox(self.page1, -1, _U("Technical Data"))
#        self.frame_technical_data.SetForegroundColour(TITLE_COLOR)
#        self.frame_technical_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
#
#        self.frame_economix = wx.StaticBox(self.page2, -1, _U("Economic Parameters"))
#        self.frame_economix.SetForegroundColour(TITLE_COLOR)
#        self.frame_economix.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        # set font for titles
        # 1. save actual font parameters on the stack
#        fp.pushFont()
#        # 2. change size and weight
#        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
#        self.frame_descriptive_data.SetFont(fp.getFont())
#        self.frame_technical_data.SetFont(fp.getFont())
#        self.frame_economix.SetFont(fp.getFont())
#        # 3. recover previous font state
#        fp.popFont()

#        fs = FieldSizes(wHeight=HEIGHT,wLabel=LABEL_WIDTH_LEFT,
#                       wData=DATA_ENTRY_WIDTH_LEFT,wUnits=UNITS_WIDTH)

        #
        # left tab controls
        # tab 0 - Descriptive Data
        #
        #right side: entries
        self.tc1 = TextEntry(self.page0, maxchars = 20, value = '',
                             label = _U("STManufacturer"),
                             tip = _U("Solarthermal Manufacturer"))

        self.tc2 = TextEntry(self.page0, maxchars = 20, value = '',
                             label = _U("STModel"),
                             tip = _U("Solarthermal Model"))

        self.tc3 = TextEntry(self.page0, maxchars = 45, value = '',
                             label = _U("STType"),
                             tip = _U("Solarthermal Type"))

        self.tc4 = TextEntry(self.page0, maxchars = 200, value = '',
                             label = _U("STReference"),
                             tip = _U("Source of data"))

        #
        # middle tab controls
        # tab 1 - Technical data
        #
        fs = FieldSizes(wHeight = HEIGHT, wLabel = 100,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.tc5 = StaticTextEntry(self.page1, maxchars = 255, value = '',
                              label = _U("STPnomColl"),
                              tip = _U(""))

        self.tc6 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'FRACTION',
                              label = _U("STc0"),
                              tip = _U("Optical efficiency"))

        self.tc7 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("STc1"),
                              tip = _U("Linear thermal loss coefficient"))

        self.tc8 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("STc2"),
                              tip = _U("Quadratic thermal loss coefficient"))

        self.tc9 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'FRACTION',
                              label = _U("K50L"),
                              tip = unicode("Incidence angle correction factor at 50º (longitudinal)", 'latin-1'))

        self.tc10 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'FRACTION',
                              label = _U("K50T"),
                              tip = unicode("Incidence angle correction factor at 50º (transversal)", 'latin-1'))

        self.tc11 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'MASSORVOLUMEFLOW',
                              label = _U("STMassFlowRate"),
                              tip = _U("Recommended collector mass flow rate"))

        self.tc12 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'LENGTH',
                              label = _U("STLengthGross"),
                              tip = _U(""))

        self.tc13 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'LENGTH',
                              label = _U("STHeightGross"),
                              tip = _U(""))

        self.tc14 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'AREA',
                              label = _U("STAreaGross"),
                              tip = _U(""))

        self.tc15 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'LENGTH',
                              label = _U("STLengthAper"),
                              tip = _U(""))

        self.tc16 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'LENGTH',
                              label = _U("STHeightAper"),
                              tip = _U(""))

        self.tc17 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'AREA',
                              label = _U("STAreaAper"),
                              tip = _U(""))

        self.tc18 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'FRACTION',
                              label = _U("STAreaFactor"),
                              tip = _U(""))

        self.tc19 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              unitdict = 'MASSPERAREA',
                              label = _U("STWeightFactor"),
                              tip = _U(""))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        #
        # right tab controls
        # panel 2. Economic Parameters
        #
        self.tc20 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              unitdict = 'UNITPRICE',
                              label = _U("STUnitPrice300kW"),
                              tip = _U(""))

        self.tc21 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              unitdict = 'UNITPRICE',
                              label = _U("STUnitTurnKeyPrice30kW"),
                              tip = _U(""))

        self.tc22 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              unitdict = 'UNITPRICE',
                              label = _U("STUnitTurnKeyPrice300kW"),
                              tip = _U(""))

        self.tc23 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              unitdict = 'UNITPRICE',
                              label = _U("STUnitTurnKeyPrice3000kW"),
                              tip = _U(""))

        self.tc24 = FloatEntry(self.page2,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              unitdict = 'UNITPRICE',
                              label = _U("STOMUnitFix"),
                              tip = _U(""))

        self.tc25 = FloatEntry(self.page2,
                               ipart = 4, decimals = 0, minval = 1900, maxval = 2100, value = 2010,
                               label = _U("STYearUpdate"),
                               tip = _U("Year of last update of the economic data"))

        #
        # buttons
        #
        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, label = 'Cancel')
        self.buttonOK = wx.Button(self, wx.ID_OK, label = 'OK')
        self.buttonOK.SetDefault()

        self.Bind(wx.EVT_BUTTON, self.OnButtonAddEquipment, self.page0.button1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteEquipment, self.page0.button2)
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxEquipmentClick, self.page0.listBoxEquipment)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged, self.notebook)

    def __do_layout(self):

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)

        self.page0.addControl(self.tc1)
        self.page0.addControl(self.tc2)
        self.page0.addControl(self.tc3)
        self.page0.addControl(self.tc4)

        self.page1.addControl(self.tc5)
        self.page1.addControl(self.tc6)
        self.page1.addControl(self.tc7)
        self.page1.addControl(self.tc8)
        self.page1.addControl(self.tc9)
        self.page1.addControl(self.tc10)
        self.page1.addControl(self.tc11)

        self.page1.addControlBottomLeft(self.tc12)
        self.page1.addControlBottomLeft(self.tc13)
        self.page1.addControlBottomLeft(self.tc14)

        self.page1.addControlBottomRight(self.tc15)
        self.page1.addControlBottomRight(self.tc16)
        self.page1.addControlBottomRight(self.tc17)

        self.page1.addControl(self.tc18)
        self.page1.addControl(self.tc19)

        self.page2.addControl(self.tc20)
        self.page2.addControl(self.tc21)
        self.page2.addControl(self.tc22)
        self.page2.addControl(self.tc23)
        self.page2.addControl(self.tc24)
        self.page2.addControl(self.tc25)

        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL | wx.EXPAND, 0)
        sizerOKCancel.Add(self.buttonOK, 0, wx.EXPAND | wx.LEFT, 4)

        sizerGlobal.Add(self.notebook, 1, wx.EXPAND, 0)
        sizerGlobal.Add(sizerOKCancel, 0, wx.TOP | wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizerGlobal)
        self.Layout()
        self.Show()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------

    def OnButtonAddEquipment(self, event):
        self.clearPage0()

    def OnButtonDeleteEquipment(self, event):
        self.equipeName = self.page0.listBoxEquipment.GetStringSelection()
        logTrack("PanelDBSolarThermal (DELETE Button): deleting solarthermal ID %s" % self.equipeName)

        sqlQuery = "SELECT * FROM dbsolarthermal WHERE DBSolarThermal_ID = '%s'" % self.equipeName
        result = Status.DB.sql_query(sqlQuery)

        if len(result) > 0:
            sqlQuery = "DELETE FROM dbsolarthermal WHERE DBSolarThermal_ID = '%s'" % self.equipeName
            Status.DB.sql_query(sqlQuery)
            self.clearPage0()

    def OnButtonCancel(self, event):
        self.clearPage0()

    def OnButtonOK(self, event):
        if self.allFieldsEmpty():
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

        if len(self.page0.listBoxEquipment.GetSelections()) + \
           len(self.page1.listBoxEquipment.GetSelections()) + \
           len(self.page2.listBoxEquipment.GetSelections()) == 0:
            retval = Status.DB.dbsolarthermal.insert(tmp)
            self.fillEquipmentList()
            self.page0.listBoxEquipment.SetStringSelection(str(retval))
            self.page1.listBoxEquipment.SetStringSelection(str(retval))
            self.page2.listBoxEquipment.SetStringSelection(str(retval))
        else:
            self.equipeName = self.page0.listBoxEquipment.GetStringSelection()
            equipments = Status.DB.dbsolarthermal.DBSolarThermal_ID[check(self.equipeName)]

            if len(equipments) > 0:
                equipe = equipments[0]

            equipe.update(tmp)
            self.page0.listBoxEquipment.SetStringSelection(str(self.equipeName))

    def OnListBoxEquipmentClick(self, event):
        self.equipeName = event.String
        self.page0.listBoxEquipment.SetStringSelection(self.equipeName)
        self.page1.listBoxEquipment.SetStringSelection(self.equipeName)
        self.page2.listBoxEquipment.SetStringSelection(self.equipeName)

        equipments = Status.DB.dbsolarthermal.DBSolarThermal_ID[check(self.equipeName)]

        if len(equipments) > 0:
            equipe = equipments[0]
        else:
            logDebug("PanelDBSolarThermal (ListBoxClick): equipe %s not found in database" % self.equipeName)
            return

        self.display(equipe)

    def OnNotebookPageChanged(self, event):
        old = event.OldSelection
        selection = ''

        if old == 0:
            selection = self.page0.listBoxEquipment.GetStringSelection()
        elif old == 1:
            selection = self.page1.listBoxEquipment.GetStringSelection()
        if old == 2:
            selection = self.page2.listBoxEquipment.GetStringSelection()

        self.page0.listBoxEquipment.SetStringSelection(selection)
        self.page1.listBoxEquipment.SetStringSelection(selection)
        self.page2.listBoxEquipment.SetStringSelection(selection)

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

    def fillEquipmentList(self):
        self.page0.clearListBox()
        self.page1.clearListBox()
        self.page2.clearListBox()

        equipments = Status.DB.dbsolarthermal.get_table()

        for equipe in equipments:
            self.page0.addListBoxElement(equipe.DBSolarThermal_ID)
            self.page1.addListBoxElement(equipe.DBSolarThermal_ID)
            self.page2.addListBoxElement(equipe.DBSolarThermal_ID)

    def clearPage0(self):
        self.clear()
        self.page0.listBoxEquipment.DeselectAll()
        self.page1.listBoxEquipment.DeselectAll()
        self.page2.listBoxEquipment.DeselectAll()
        self.fillEquipmentList()
        self.notebook.ChangeSelection(0)

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

