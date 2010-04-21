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
from einstein.GUI.panelBaseDBEditor import *

HEIGHT = 20
LABEL_WIDTH_LEFT = 140
DATA_ENTRY_WIDTH_LEFT = 140
UNITS_WIDTH = 55

def _U(text):
    return unicode(_(text), "utf-8")

class PanelDBCHP(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self._init_ctrls(parent)
        self.__do_layout()
        self.fillEquipmentList()

    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id = -1, name = 'PanelDBCHP', parent = parent,
              pos = wx.Point(0, 0), size = wx.Size(780, 580))
        self.Hide()

        # access to font properties object
        fp = FontProperties()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.notebook = wx.Notebook(self, -1, style = 0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = PanelBaseDBEditor(self.notebook, 'Descriptive Data', 'List of chp equipment',
                                       'Add Equipment', 'Delete Equipment')

        self.page1 = PanelBaseDBEditor(self.notebook, 'Technical Data', 'List of chp equipment',
                                       'Add Equipment', 'Delete Equipment')

        self.page2 = PanelBaseDBEditor(self.notebook, 'Heat source / sink', 'List of chp equipment',
                                       'Add Equipment', 'Delete Equipment')

        self.page3 = PanelBaseDBEditor(self.notebook, 'Economic Parameters', 'List of chp equipment',
                                       'Add Equipment', 'Delete Equipment')

        self.notebook.AddPage(self.page0, _U('Descriptive Data'))
        self.notebook.AddPage(self.page1, _U('Technical Data'))
        self.notebook.AddPage(self.page2, _U('Heat source / sink'))
        self.notebook.AddPage(self.page3, _U('Economic Parameters'))

        #
        # left tab controls
        # tab 0 - Descriptive Data
        #
        # right side: entries
        self.tc1 = TextEntry(self.page0, maxchars = 45, value = '',
                             label = _U("Manufacturer"),
                             tip = _U("Manufacturer"))

        self.tc2 = TextEntry(self.page0, maxchars = 45, value = '',
                             label = _U("CHPequip"),
                             tip = _U(""))

        self.tc3 = TextEntry(self.page0, maxchars = 45, value = '',
                             label = _U("Type"),
                             tip = _U(""))

        self.tc4 = TextEntry(self.page0, maxchars = 45, value = '',
                             label = _U("SubType"),
                             tip = _U(""))

        self.tc5 = TextEntry(self.page0, maxchars = 45, value = '',
                             label = _U("Reference"),
                             tip = _U("Source of data"))

        #
        # middle left tab controls
        # tab 1 - Technical data
        #
        self.tc6 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("CHPPt"),
                              tip = _U("Nominal thermal power"))

        self.tc7 = ChoiceEntry(self.page1,
                               values = [],
                               label = _U("FuelType"),
                               tip = _U("Fuel type"))

        self.tc8 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              label = _U("FuelConsum"),
                              tip = _U("Nominal fuel consumption"))

        self.tc9 = FloatEntry(self.page1,
                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                              unitdict = 'FRACTION',
                              label = _U("Eta_t"),
                              tip = _U("Nominal thermal conversion efficiency"))

        self.tc10 = FloatEntry(self.page1,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'POWER',
                               label = _U("CHPPe"),
                               tip = _U("Nominal electrical power"))

        self.tc11 = FloatEntry(self.page1,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'FRACTION',
                               label = _U("Eta_e"),
                               tip = _U("Electrical efficiency"))

        #
        # middle right tab controls
        # tab 2. Heat source / sink
        #
        fs = FieldSizes(wHeight = HEIGHT, wLabel = 100,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.tc12 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'POWER',
                               label = _U("FluidSupply"),
                               tip = _U("Heat transport medium"))

        self.tc13 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'TEMPERATURE',
                               label = _U("Tsupply"),
                               tip = _U("Outlet temperature at nominal conditions"))

        self.tc14 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                               unitdict = 'MASSFLOWRATE',
                               label = _U("FlowRateSupply"),
                               tip = _U("Mass flow rate of heat transport medium"))

        self.tc15 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'POWER',
                               label = _U("FluidSupply2"),
                               tip = _U("Heat transport medium"))

        self.tc16 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'TEMPERATURE',
                               label = _U("Tsupply2"),
                               tip = _U("Outlet temperature at nominal conditions"))

        self.tc17 = FloatEntry(self.page2,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                               unitdict = 'MASSFLOWRATE',
                               label = _U("FlowRateSupply2"),
                               tip = _U("Mass flow rate of heat transport medium"))

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        #
        # right tab controls
        # panel 3. Economic Parameters
        #
        self.tc18 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'PRICE',
                               label = _U("Price"),
                               tip = _U("Equipment price at factory applied installer's discount"))

        self.tc19 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               unitdict = 'PRICE',
                               label = _U("InvRate"),
                               tip = _U("Turn-key price"))

        self.tc20 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                               unitdict = 'UNITPRICE',
                               label = _U("OMRateFix"),
                               tip = _U("Annual operational and maintenance fixed costs (approximate average per kW heating)"))

        self.tc21 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                               unitdict = 'UNITPRICEENERGY',
                               label = _U("OMRateVar"),
                               tip = _U("Annual operational and maintenance variable costs dependant on usage (approximate average per MWh heating)"))

        self.tc22 = FloatEntry(self.page3,
                               ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
                               label = _U("YearUpdate"),
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
        self.page0.addControl(self.tc5)

        self.page1.addControl(self.tc6)
        self.page1.addControl(self.tc7)
        self.page1.addControl(self.tc8)
        self.page1.addControl(self.tc9)
        self.page1.addControl(self.tc10)
        self.page1.addControl(self.tc11)

        self.page2.addControlBottomLeft(self.tc12)
        self.page2.addControlBottomLeft(self.tc13)
        self.page2.addControlBottomLeft(self.tc14)

        self.page2.addControlBottomRight(self.tc15)
        self.page2.addControlBottomRight(self.tc16)
        self.page2.addControlBottomRight(self.tc17)

        self.page3.addControl(self.tc18)
        self.page3.addControl(self.tc19)
        self.page3.addControl(self.tc20)
        self.page3.addControl(self.tc21)
        self.page3.addControl(self.tc22)

        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.EXPAND, 0)
        sizerOKCancel.Add(self.buttonOK, 0, wx.EXPAND | wx.LEFT, 4)

        sizerGlobal.Add(self.notebook, 1, wx.EXPAND, 0)
        sizerGlobal.Add(sizerOKCancel, 0, wx.ALIGN_RIGHT, 0)
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
        logTrack("PanelDBCHP (DELETE Button): deleting chp ID %s" % self.equipeName)

        sqlQuery = "SELECT * FROM dbchp WHERE DBCHP_ID = '%s'" % self.equipeName
        result = Status.DB.sql_query(sqlQuery)

        if len(result) > 0:
            sqlQuery = "DELETE FROM dbchp WHERE DBCHP_ID = '%s'" % self.equipeName
            Status.DB.sql_query(sqlQuery)
            self.clearPage0()

    def OnButtonCancel(self, event):
        self.clearPage0()

    def OnButtonOK(self, event):
        if self.allFieldsEmpty():
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

        if len(self.page0.listBoxEquipment.GetSelections()) + \
           len(self.page1.listBoxEquipment.GetSelections()) + \
           len(self.page2.listBoxEquipment.GetSelections()) + \
           len(self.page3.listBoxEquipment.GetSelections()) == 0:
            retval = Status.DB.dbchp.insert(tmp)
            self.fillEquipmentList()
            self.page0.listBoxEquipment.SetStringSelection(str(retval))
            self.page1.listBoxEquipment.SetStringSelection(str(retval))
            self.page2.listBoxEquipment.SetStringSelection(str(retval))
            self.page3.listBoxEquipment.SetStringSelection(str(retval))
        else:
            self.equipeName = self.page0.listBoxEquipment.GetStringSelection()
            equipments = Status.DB.dbchp.DBCHP_ID[check(self.equipeName)]

            if len(equipments) > 0:
                equipe = equipments[0]

            equipe.update(tmp)
            self.page0.listBoxEquipment.SetStringSelection(str(self.equipeName))

    def OnListBoxEquipmentClick(self, event):
        self.equipeName = event.String
        self.page0.listBoxEquipment.SetStringSelection(self.equipeName)
        self.page1.listBoxEquipment.SetStringSelection(self.equipeName)
        self.page2.listBoxEquipment.SetStringSelection(self.equipeName)
        self.page3.listBoxEquipment.SetStringSelection(self.equipeName)

        equipments = Status.DB.dbchp.DBCHP_ID[check(self.equipeName)]

        if len(equipments) > 0:
            equipe = equipments[0]
        else:
            logDebug("PanelDBCHP (ListBoxClick): equipe %s not found in database" % self.equipeName)
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
        elif old == 3:
            selection = self.page3.listBoxEquipment.GetStringSelection()

        self.page0.listBoxEquipment.SetStringSelection(selection)
        self.page1.listBoxEquipment.SetStringSelection(selection)
        self.page2.listBoxEquipment.SetStringSelection(selection)
        self.page3.listBoxEquipment.SetStringSelection(selection)

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------

    def display(self, q = None):
        self.clear()

        fuelDict = Status.prj.getFuelDict()
        self.fillChoiceOfDBFuel()

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

    def fillChoiceOfDBFuel(self):
        fuelDict = Status.prj.getFuelDict()
        fuelList = fuelDict.values()
        fillChoice(self.tc7.entry, fuelList)

    def fillEquipmentList(self):
        self.page0.clearListBox()
        self.page1.clearListBox()
        self.page2.clearListBox()
        self.page3.clearListBox()

        equipments = Status.DB.dbchp.get_table()

        for equipe in equipments:
            self.page0.addListBoxElement(equipe.DBCHP_ID)
            self.page1.addListBoxElement(equipe.DBCHP_ID)
            self.page2.addListBoxElement(equipe.DBCHP_ID)
            self.page3.addListBoxElement(equipe.DBCHP_ID)

    def clearPage0(self):
        self.clear()
        self.page0.listBoxEquipment.DeselectAll()
        self.page1.listBoxEquipment.DeselectAll()
        self.page2.listBoxEquipment.DeselectAll()
        self.page3.listBoxEquipment.DeselectAll()
        self.fillEquipmentList()
        self.fillChoiceOfDBFuel()
        self.notebook.ChangeSelection(0)

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
