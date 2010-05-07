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
#    PanelDBBase: Database Design Assistant
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

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

class PanelDBBase(wx.Dialog):
    def __init__(self, parent, title, name):
        self.name = name
        wx.Dialog.__init__(self, parent, -1, title,
                           wx.Point(wx.CENTER_ON_SCREEN), wx.Size(800, 600),
                           wx.DEFAULT_FRAME_STYLE, name)

        self.Centre()
        self.Hide()

        # objects to be set by derived classes
        self.theId = -1
        self.colLabels = []
        self.db = None
        self.table = None
        self.identifier = None
        self.type = None
        self.subtype = None
        self.grid = None
        self.notebook = None
        self.tc_type = None
        self.tc_subtype = None

    def _init_grid(self, defaultColSize):
        self.grid.CreateGrid(0, len(self.colLabels))

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(defaultColSize)

        self.grid.EnableEditing(False)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        for i in range(len(self.colLabels)):
            self.grid.SetColLabelValue(i, _U(self.colLabels[i]))

        self.grid.SetGridCursor(0, 0)

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------

    def OnButtonAddEquipment(self, event):
        self.addEquipment()
        event.Skip()

    def OnButtonDeleteEquipment(self, event):
        self.deleteEquipment()
        event.Skip()

    def OnButtonCancel(self, event):
        event.Skip()

    def OnGridCellLeftClick(self, event):
        self.clear()
        self.grid.ClearSelection()
        self.grid.SetGridCursor(event.GetRow(), event.GetCol())
        id = self.grid.GetCellValue(event.GetRow(), 0)

        equipments = self.getDBCol()[check(id)]

        if len(equipments) > 0:
            equipe = equipments[0]

        self.display(equipe)

        event.Skip()

    def OnGridCellRightClick(self, event):
        event.Skip()

    def OnGridCellDClick(self, event):
        event.Skip()

    def OnGridLabelLeftClick(self, event):
        self.clear()
        if event.GetRow() >= 0:
            self.OnGridCellLeftClick(event)
            self.grid.SetGridCursor(event.GetRow(), 0)
        event.Skip()

    def OnGridLabelRightClick(self, event):
        event.Skip()

    def OnGridLabelDClick(self, event):
        event.Skip()

    def OnChoiceEntryClick(self, event):
        self.grid.ClearGrid()
        self.grid.ClearSelection()
        for i in range(self.grid.GetNumberRows()):
            self.grid.DeleteRows()
        self.fillEquipmentList()
        event.Skip()

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------

    def addEquipment(self):
        retval = self.db.insert({})
        self.clearPage0()
        for i in range(self.grid.GetNumberRows() - 1, -1, -1):
            if self.grid.GetCellValue(i, 0) == str(retval): 
                self.grid.SetGridCursor(i, 0)
                self.grid.MakeCellVisible(i, 0)
                self.grid.SelectRow(i)
                equipments = self.getDBCol()[check(retval)]
                if len(equipments) > 0:
                    equipe = equipments[0]
                    self.display(equipe)
                break
        self.fillChoices()

    def deleteEquipment(self):
        if not self.grid.IsSelection():
            print "Select a row first"
            return

        id = self.grid.GetCellValue(self.grid.GetGridCursorRow(), 0)
        logTrack("%s (DELETE Button): deleting equipment ID %s"%(self.name,id))

        sqlQuery = "SELECT * FROM %s WHERE %s = %s"%(self.table,self.identifier,id)
        result = Status.DB.sql_query(sqlQuery)

        if len(result) > 0:
            sqlQuery = "DELETE FROM %s WHERE %s = %s"%(self.table,self.identifier,id)
            Status.DB.sql_query(sqlQuery)

            self.clearPage0()

    def updateValues(self, tmp):
        row = self.grid.GetGridCursorRow()
        col = self.grid.GetGridCursorCol()

        try:
            self.theId = self.grid.GetCellValue(row, 0)
        except:
            return

        equipments = self.getDBCol()[check(self.theId)]

        if len(equipments) > 0:
            equipe = equipments[0]
            equipe.update(tmp)

        for i in range(self.grid.GetNumberRows()):
            self.grid.DeleteRows()
        self.fillChoiceOfType()
        self.fillChoiceOfSubType()
        self.fillEquipmentList()

        if row >= 0 and col >= 0:
            self.grid.SetGridCursor(row, col)
            self.grid.SelectRow(row)
            self.grid.MakeCellVisible(row, col)

    def display(self, q = None):
        pass

    def clear(self):
        pass

    def fillChoiceOfDBFuel(self, entry):
        fuelDict = Status.prj.getFuelDict()
        fuelList = fuelDict.values()
        fillChoice(entry, fuelList)

    def fillChoiceOfType(self):
        try:
            equipments = self.db.get_table()
            ids = equipments.column(self.identifier)
            typeList = []
            for id in ids:
                sqlQuery = "SELECT %s FROM %s WHERE %s = %s"%(self.type,self.table,self.identifier,id)
                result = Status.DB.sql_query(sqlQuery)
                if result not in typeList and result is not None:
                    typeList.append(str(result))
            fillChoice(self.tc_type.entry, typeList)
            self.tc_type.entry.Append("All")
            self.tc_type.entry.SetStringSelection("All")
        except:
            pass

    def fillChoiceOfSubType(self):
        try:
            equipments = self.db.get_table()
            ids = equipments.column(self.identifier)
            subtypeList = []
            for id in ids:
                sqlQuery = "SELECT %s FROM %s WHERE %s = %s"%(self.subtype,self.table,self.identifier,id)
                result = Status.DB.sql_query(sqlQuery)
                if result not in subtypeList and result is not None:
                    subtypeList.append(str(result))
            fillChoice(self.tc_subtype.entry, subtypeList)
            self.tc_subtype.entry.Append("All")
            self.tc_subtype.entry.SetStringSelection("All")
        except:
            pass

    def clearPage0(self):
        self.clear()
        self.grid.ClearGrid()
        self.grid.ClearSelection()
        for i in range(self.grid.GetNumberRows()):
            self.grid.DeleteRows()
        self.fillChoices()
        self.fillEquipmentList()
        self.notebook.ChangeSelection(0)

# methods to be implemented by derived classes
    def fillChoices(self):
        pass

    def fillEquipmentList(self):
        pass

    def getDBCol(self):
        pass
