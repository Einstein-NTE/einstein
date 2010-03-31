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
#    PanelDB0: Database Design Assistant
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

def _U(text):
    return unicode(_(text),"utf-8")

class PanelDB(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self._init_ctrls(parent)
        self.__do_layout()
        self.fillEquipmentList()

    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelDB0', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580))
        self.Hide()

        # access to font properties object
        fp = FontProperties()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = PanelBaseDBEditor(self.notebook, 'Descriptive Data', 'List of equipment',
                                       '', 'Delete Equipment')
        #self.page0 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page0, _U('Descriptive Data'))

        #
        # left tab controls
        # tab 0 - Descriptive Data
        #
        # right side: entries
        self.tc1 = StaticTextEntry(self.page0,maxchars=255,value='',
                             label=_U("Manufacturer"),
                             tip=_U("Manufacturer"))

        self.tc2 = StaticTextEntry(self.page0,maxchars=255,value='',
                             label=_U("Model"),
                             tip=_U("Model"))

        self.tc3 = StaticTextEntry(self.page0,maxchars=255,value='',
                             label=_U("Type"),
                             tip=_U("Type"))

        self.tc4 = StaticTextEntry(self.page0,maxchars=255,value='',
                             label=_U("Nominal Power"),
                             tip=_U("Nominal Power"))

        equipeTypeChoices = ["All", "Heatpump", "Solarthermal", "CHP"]
        self.tc5 = ChoiceEntry(self.page0,
                               values=equipeTypeChoices,
                               label=_U("Show"),
                               tip=_U("Show only equipment of this type"))
        self.tc5.SetValue(0)

        self.tc5.Bind(wx.EVT_CHOICE, self.OnChoiceEntryClick)
        #self.Bind(wx.EVT_BUTTON, self.OnButtonEditEquipment, self.page0.button1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteEquipment, self.page0.button2)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxEquipmentClick, self.page0.listBoxEquipment)

    def __do_layout(self):

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)

        self.page0.addControl(self.tc1)
        self.page0.addControl(self.tc2)
        self.page0.addControl(self.tc3)
        self.page0.addControl(self.tc4)
        self.page0.addStretchSpacer()
        self.page0.addControl(self.tc5)

        sizerGlobal.Add(self.notebook, 1, wx.EXPAND, 0)
        self.SetSizer(sizerGlobal)
        self.Layout()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------

    def OnListBoxEquipmentClick(self, event):
        self.equipeName = self.page0.listBoxEquipment.GetStringSelection()

        equipe = None
        name = None
        if self.equipeName.startswith('HP'):
            self.equipeName = self.equipeName.lstrip('HP ')
            name = 'HP'
            equipments = Status.DB.dbheatpump.DBHeatPump_ID[check(self.equipeName)]
            if len(equipments) > 0:
                equipe = equipments[0]
        elif self.equipeName.startswith('ST'):
            self.equipeName = self.equipeName.lstrip('ST ')
            name = 'ST'
            equipments = Status.DB.dbsolarthermal.DBSolarThermal_ID[check(self.equipeName)]
            if len(equipments) > 0:
                equipe = equipments[0]
        elif self.equipeName.startswith('CHP'):
            self.equipeName = self.equipeName.lstrip('CHP ')
            name = 'CHP'
            equipments = Status.DB.dbchp.DBCHP_ID[check(self.equipeName)]
            if len(equipments) > 0:
                equipe = equipments[0]

        if equipe == None:
            logDebug("PanelDB (ListBoxClick): equipe %s not found in database"%self.equipeName)
            return

        self.display(equipe, name)
        event.Skip()

    def OnChoiceEntryClick(self, event):
        self.fillEquipmentList(event.String)

    def OnButtonDeleteEquipment(self, event):
        self.equipeName = self.page0.listBoxEquipment.GetStringSelection()
        name = self.equipeName
        selectedEquipment = self.tc5.GetValue()

        if self.equipeName.startswith('HP'):
            self.equipeName = self.equipeName.lstrip('HP ')
            logTrack("PanelDBHP (DELETE Button): deleting heatpump ID %s"%self.equipeName)
            sqlQuery = "SELECT * FROM dbheatpump WHERE DBHeatPump_ID = '%s'"%self.equipeName
        elif self.equipeName.startswith('ST'):
            self.equipeName = self.equipeName.lstrip('ST ')
            logTrack("PanelDBHP (DELETE Button): deleting solarthermal ID %s"%self.equipeName)
            sqlQuery = "SELECT * FROM dbsolarthermal WHERE DBSolarThermal_ID = '%s'"%self.equipeName
        elif self.equipeName.startswith('CHP'):
            self.equipeName = self.equipeName.lstrip('CHP ')
            logTrack("PanelDBHP (DELETE Button): deleting chp ID %s"%self.equipeName)
            sqlQuery = "SELECT * FROM dbchp WHERE DBCHP_ID = '%s'"%self.equipeName

        result = Status.DB.sql_query(sqlQuery)

        if len(result) > 0:
            if name.startswith('HP'):
                sqlQuery = "DELETE FROM dbheatpump WHERE DBHeatPump_ID = '%s'"%self.equipeName
            elif name.startswith('ST'):
                sqlQuery = "DELETE FROM dbsolarthermal WHERE DBSolarThermal_ID = '%s'"%self.equipeName
            elif name.startswith('CHP'):
                sqlQuery = "DELETE FROM dbchp WHERE DBCHP_ID = '%s'"%self.equipeName

        Status.DB.sql_query(sqlQuery)

        self.clear()
        if selectedEquipment == 1:
            equip = "Heatpump"
        elif selectedEquipment == 2:
            equip = "Solarthermal"
        elif selectedEquipment == 3:
            equip = "CHP"
        else:
            equip = "All"

        self.fillEquipmentList(equip)

#    def OnButtonEditEquipment(self, event):
#        pass

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------

    def display(self, q = None, name = None):
        self.clear()

        if q is not None and name is not None:
            if name == 'HP':
                manufacturer = q.HPManufacturer if q.HPManufacturer is not None else ''
                model = q.HPModel if q.HPModel is not None else ''
                type = q.HPType if q.HPType is not None else ''
                nompower = ''
            elif name == 'ST':
                manufacturer = q.STManufacturer if q.STManufacturer is not None else ''
                model = q.STModel if q.STModel is not None else ''
                type = q.STType if q.STType is not None else ''
                nompower = ''
            elif name == 'CHP':
                manufacturer = q.CHPequip if q.CHPequip is not None else ''
                model = ''
                #type = q.Type if q.Type is not None else ''
                type = ''
                nompower = q.CHPPt if q.CHPPt is not None else ''

            self.tc1.SetValue(manufacturer)
            self.tc2.SetValue(model)
            self.tc3.SetValue(type)
            self.tc4.SetValue(str(nompower))

        self.Show()

    def clear(self):
        self.tc1.SetValue('')
        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')

    def fillEquipmentList(self, equip = None):
        self.page0.clearListBox()

        if equip == "Heatpump":
            equipments = Status.DB.dbheatpump.get_table()
            for equipe in equipments:
                self.page0.addListBoxElement(' '.join(['HP', str(equipe.DBHeatPump_ID)]))
        elif equip == "Solarthermal":
            equipments = Status.DB.dbsolarthermal.get_table()
            for equipe in equipments:
                self.page0.addListBoxElement(' '.join(['ST', str(equipe.DBSolarThermal_ID)]))
        elif equip == "CHP":
            equipments = Status.DB.dbchp.get_table()
            for equipe in equipments:
                self.page0.addListBoxElement(' '.join(['CHP', str(equipe.DBCHP_ID)]))
        else:
            equipments = Status.DB.dbheatpump.get_table()
            for equipe in equipments:
                self.page0.addListBoxElement(' '.join(['HP', str(equipe.DBHeatPump_ID)]))
            equipments = Status.DB.dbsolarthermal.get_table()
            for equipe in equipments:
                self.page0.addListBoxElement(' '.join(['ST', str(equipe.DBSolarThermal_ID)]))
            equipments = Status.DB.dbchp.get_table()
            for equipe in equipments:
                self.page0.addListBoxElement(' '.join(['CHP', str(equipe.DBCHP_ID)]))
