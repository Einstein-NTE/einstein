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
#    PanelDBAuditor: Database Design Assistant
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

class PanelDBAuditor(PanelDBBase):
    def __init__(self, parent, title, closeOnOk = False):
        self.parent = parent
        self.title = title
        self.closeOnOk = closeOnOk
        self.name = "Auditor"
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

        PanelDBBase.__init__(self, self.parent, "Edit DBAuditor", self.name)

        # Auditor_ID needs to remain as first entry
        self.colLabels = "Auditor_ID", "Name", "City", "Country", "Company", "CompanyType"

        self.db = Status.DB.auditor
        self.table = "auditor"
        self.identifier = self.colLabels[0]
        self.type = self.colLabels[2]
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
        self.notebook.AddPage(self.page1, _U('General Data'))

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
        # tab 1 - General Data
        #
        self.frame_general_data = wx.StaticBox(self.page1, -1, _U("General data"))
        self.frame_general_data.SetForegroundColour(TITLE_COLOR)
        self.frame_general_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        fp.pushFont()
        self.frame_general_data.SetFont(fp.getFont())
        fp.popFont()

        self.tc1 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Name"),
                             tip = _U("Name"))

        self.tc2 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("City"),
                             tip = _U("City"))

        self.tc3 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Country"),
                             tip = _U("Country"))

        self.tc4 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Company"),
                             tip = _U("Company"))

        self.tc5 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("CompanyType"),
                             tip = _U("CompanyType"))

        self.tc6 = TextEntry(self.page1, maxchars = 100, value = '',
                             label = _U("Adress"),
                             tip = _U("Adress"))

        self.tc7 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Phone"),
                             tip = _U("Phone"))

        self.tc8 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Fax"),
                             tip = _U("Fax"))

        self.tc9 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("EMail"),
                             tip = _U("EMail"))

        self.tc10 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("Web"),
                             tip = _U("Web"))

    def __do_layout(self):
        flagText = wx.TOP | wx.ALIGN_CENTER_HORIZONTAL

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)


        sizerPage0 = wx.StaticBoxSizer(self.frame_summary_table, wx.VERTICAL)
        sizerPage0.Add(self.grid, 1, wx.EXPAND | wx.ALL, 56)
        sizerPage0.Add(self.tc_type, 0, flagText | wx.ALIGN_RIGHT, VSEP)
        sizerPage0.Add(self.tc_subtype, 0, flagText | wx.ALIGN_RIGHT, VSEP)

        self.page0.SetSizer(sizerPage0)


        sizerPage1 = wx.StaticBoxSizer(self.frame_general_data, wx.VERTICAL)
        sizerPage1.Add(self.tc1, 0, flagText, VSEP)
        sizerPage1.Add(self.tc2, 0, flagText, VSEP)
        sizerPage1.Add(self.tc3, 0, flagText, VSEP)
        sizerPage1.Add(self.tc4, 0, flagText, VSEP)
        sizerPage1.Add(self.tc5, 0, flagText, VSEP)
        sizerPage1.Add(self.tc6, 0, flagText, VSEP)
        sizerPage1.Add(self.tc7, 0, flagText, VSEP)
        sizerPage1.Add(self.tc8, 0, flagText, VSEP)
        sizerPage1.Add(self.tc9, 0, flagText, VSEP)
        sizerPage1.Add(self.tc10, 0, flagText, VSEP)

        self.page1.SetSizer(sizerPage1)


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
               "Name":check(self.tc1.GetValue()),
               "City":check(self.tc2.GetValue()),
               "Country":check(self.tc3.GetValue()),
               "Company":check(self.tc4.GetValue()),
               "CompanyType":check(self.tc5.GetValue()),
               "Adress":check(self.tc6.GetValue()),
               "Phone":check(self.tc7.GetValue()),
               "Fax":check(self.tc8.GetValue()),
               "EMail":check(self.tc9.GetValue()),
               "Web":check(self.tc10.GetValue())
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
            self.tc1.SetValue(str(q.Name)) if q.Name is not None else ''
            self.tc2.SetValue(str(q.City)) if q.City is not None else ''
            self.tc3.SetValue(str(q.Country)) if q.Country is not None else ''
            self.tc4.SetValue(str(q.Company)) if q.Company is not None else ''
            self.tc5.SetValue(str(q.CompanyType)) if q.CompanyType is not None else ''
            self.tc6.SetValue(str(q.Adress)) if q.Adress is not None else ''
            self.tc7.SetValue(str(q.Phone)) if q.Phone is not None else ''
            self.tc8.SetValue(str(q.Fax)) if q.Fax is not None else ''
            self.tc9.SetValue(str(q.EMail)) if q.EMail is not None else ''
            self.tc10.SetValue(str(q.Web)) if q.Web is not None else ''
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

    def fillChoices(self):
        self.fillChoiceOfType()
        self.fillChoiceOfSubType()

    def getDBCol(self):
        return self.db.Auditor_ID

    def allFieldsEmpty(self):
        if len(self.tc1.GetValue()) == 0 and\
           len(self.tc2.GetValue()) == 0 and\
           len(self.tc3.GetValue()) == 0 and\
           len(self.tc4.GetValue()) == 0 and\
           len(self.tc5.GetValue()) == 0 and\
           len(self.tc6.GetValue()) == 0 and\
           len(self.tc7.GetValue()) == 0 and\
           len(self.tc8.GetValue()) == 0 and\
           len(self.tc9.GetValue()) == 0 and\
           len(self.tc10.GetValue()) == 0:
            return True
        else:
            return False
