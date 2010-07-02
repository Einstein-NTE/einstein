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

        # unitOpDict required for appendResultToGridBenchmark
        self.unitOpDict = Status.prj.getUnitOpDict()

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
        self.labelButtonAdd = _U("Add equipment")
        self.labelButtonDelete = _U("Delete equipment")
        self.currentRow = -1
        self.currentCol = -1

    def _init_buttons(self):
        #
        # buttons
        #
        self.buttonAddEquipment = wx.Button(self, -1, label = self.labelButtonAdd)
        self.buttonDeleteEquipment = wx.Button(self, -1, label = self.labelButtonDelete)
        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, label = 'Close')
        self.buttonOK = wx.Button(self, wx.ID_OK, label = 'Save')
        self.buttonOK.SetDefault()

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

        self.grid.SetColMinimalAcceptableWidth(0)
        self.grid.SetColSize(0, 0)
        self.grid.SetGridCursor(0, 0)

    def _bind_events(self):
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddEquipment, self.buttonAddEquipment)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteEquipment, self.buttonDeleteEquipment)
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)

        self.Bind(wx.EVT_CHOICE, self.OnChoiceEntryClick, self.tc_type.entry)
        if self.tc_subtype is not None:
            self.Bind(wx.EVT_CHOICE, self.OnChoiceEntryClick, self.tc_subtype.entry)

        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnGridCellLeftClick, self.grid)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnGridCellDClick, self.grid)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnGridCellRightClick, self.grid)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_DCLICK, self.OnGridCellDClick, self.grid)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnGridLabelLeftClick, self.grid)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnGridLabelDClick, self.grid)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnGridLabelRightClick, self.grid)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnGridLabelDClick, self.grid)

        self.grid.GetGridWindow().Bind(wx.EVT_MOTION, self.OnMouseOver)

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------

    def OnButtonAddEquipment(self, event):
        self.addEquipment()
        event.Skip()

    def OnButtonDeleteEquipment(self, event):
        self.deleteEquipment()
        event.Skip()

    def OnButtonOK(self, event):
        if self.allFieldsEmpty():
            self.theId = -1
            print "Enter at least one value"
            return
        tmp = self.collectEntriesForDB()
        self.updateValues(tmp)
        if self.closeOnOk:
            self.EndModal(wx.ID_OK)

    def OnButtonCancel(self, event):
        event.Skip()

    def OnGridCellLeftClick(self, event):
        self.clear()
        self.grid.ClearSelection()
        try:
            row = event.GetRow() if event.GetRow() >= 0 else 0
            col = event.GetCol() if event.GetCol() >= 0 else 0
            self.grid.SetGridCursor(row, col)
            self.display(self.getCurrentEquipment(row))
        except:
            pass

        event.Skip()

    def OnGridCellRightClick(self, event):
        event.Skip()

    def OnGridCellDClick(self, event):
        event.Skip()

    def OnGridLabelLeftClick(self, event):
        self.clear()
        if event.GetRow() < 0 and event.GetCol() < 0:
            self.grid.ClearSelection()
            return

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

    def OnMouseOver(self, event):
        try:
            x, y = self.grid.CalcUnscrolledPosition(event.GetPosition())
            numRows, numCols = self.grid.GetNumberRows(), self.grid.GetNumberCols()

            col = -1
            row = -1

            totalColWidth = 0
            for i in range(numCols):
                totalColWidth += self.grid.GetColSize(i)
                if totalColWidth > x:
                    col = i
                    break

            totalRowHeight = 0
            for i in range(numRows):
                totalRowHeight += self.grid.GetRowSize(i)
                if totalRowHeight > y:
                    row = i
                    break

            if row is not self.currentRow or col is not self.currentCol:
                if row >= 0 and row < numRows and col >= 0 and col < numCols:
                    self.currentRow = row
                    self.currentCol = col
                    self.grid.GetGridWindow().SetToolTipString(self.grid.GetCellValue(row, col))
                else:
                    self.grid.GetGridWindow().SetToolTipString('')
        except:
            self.grid.GetGridWindow().SetToolTipString('')
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
                self.display(self.getCurrentEquipment(i))
                break
        self.fillChoiceOfType()
        self.fillChoiceOfSubType()

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
        if self.grid.IsSelection():
            row = self.grid.GetGridCursorRow()
            col = self.grid.GetGridCursorCol()

            try:
                self.getCurrentEquipment(row).update(tmp)
            except:
                return

            for i in range(self.grid.GetNumberRows()):
                self.grid.DeleteRows()
            self.fillChoiceOfType()
            self.fillChoiceOfSubType()
            self.fillEquipmentList()

            if row >= 0 and col >= 0:
                self.grid.SetGridCursor(row, col)
                self.grid.SelectRow(row)
                self.grid.MakeCellVisible(row, col)
        else:
            # no equipment selected, hence adding new one with already entered values
            tmp = self.collectEntriesForDB()
            self.addEquipment()
            self.updateValues(tmp)
            try:
                self.display(self.getCurrentEquipment(self.grid.GetGridCursorRow()))
            except:
                pass

    def getCurrentEquipment(self, row):
        equipe = None

        try:
            self.theId = self.grid.GetCellValue(row, 0)
            equipments = self.getDBCol()[check(self.theId)]
            if len(equipments) > 0:
                equipe = equipments[0]
        except:
            pass

        return equipe

    def getNACECodeandNACESubCodeList(self):
        naceTable = Status.DB.dbnacecode.DBNaceCode_ID['%']
        naceList = []
        for entry in naceTable:
            naceCode = entry.CodeNACE
            naceSubCode = entry.CodeNACEsub
            naceCode = naceCode + "." + naceSubCode
            naceList.append(str(naceCode))
        naceList.sort()
        return naceList

    def getProductCodeList(self):
        productCodeList = []
        for entry in PRODUCTCODES.values():
            productCodeList.append(str(entry))
        productCodeList.sort()
        return productCodeList

    def getFuelUnitList(self):
        fuelUnitsList = []
        for entry in UNITS["MASSORVOLUME"]:
            fuelUnitsList.append(str(entry))
        fuelUnitsList.sort()
        return fuelUnitsList

    def getUnitOpCodeList(self):
        unitOpTable = Status.DB.dbunitoperation.DBUnitOperation_ID['%']
        unitOpList = []
        for entry in unitOpTable:
            unitOpCode = entry.UnitOperationCode
            unitOpName = entry.UnitOperation
            unitOpList.append(unitOpCode + ": " + unitOpName)
        unitOpList.sort()
        return unitOpList

    def getEUnitList(self):
        eUnitTable = Status.DB.dbbenchmark.DBBenchmark_ID['%']
        eUnitList = []
        for entry in eUnitTable:
            eUnit = entry.E_Unit
            if str(eUnit) not in eUnitList and len(str(eUnit)) > 0:
                eUnitList.append(str(eUnit))
        return eUnitList

    def getHUnitList(self):
        hUnitTable = Status.DB.dbbenchmark.DBBenchmark_ID['%']
        hUnitList = []
        for entry in hUnitTable:
            hUnit = entry.H_Unit
            if str(hUnit) not in hUnitList and len(str(hUnit)) > 0:
                hUnitList.append(str(hUnit))
        return hUnitList

    def getTUnitList(self):
        tUnitTable = Status.DB.dbbenchmark.DBBenchmark_ID['%']
        tUnitList = []
        for entry in tUnitTable:
            tUnit = entry.T_Unit
            if str(tUnit) not in tUnitList and len(str(tUnit)) > 0:
                tUnitList.append(str(tUnit))
        return tUnitList

    def getSourceSinkList(self):
        sourceSinkList = HPSOURCESINK.values()
        sourceSinkList.sort()
        return sourceSinkList

    def getFluidNameList(self):
        fluidTable = Status.DB.dbfluid.DBFluid_ID['%']
        fluidNameList = []
        for entry in fluidTable:
            fluidName = entry.FluidName
            if str(fluidName) not in fluidNameList and len(str(fluidName)) > 0:
                fluidNameList.append(str(fluidName))
        fluidNameList.sort()
        return fluidNameList

    def getHPSubTypeList(self):
        hpSubTypeList = []
        for list in HPSUBTYPES.values():
            listEntry = ""
            for e in list:
                listEntry += e + "-"
            hpSubTypeList.append(listEntry.rstrip('-'))
        hpSubTypeList.sort()
        return hpSubTypeList

    def getCHPSubTypeList(self):
        chpSubTypeList = []
        for list in CHPSUBTYPES.values():
            listEntry = ""
            for e in list:
                listEntry += e + "-"
            chpSubTypeList.append(listEntry.rstrip('-'))
        chpSubTypeList.sort()
        return chpSubTypeList

    def getAuditorName(self):
        sqlQuery = "SELECT Name FROM auditor where Auditor_ID = (SELECT Auditor_ID FROM stool)"
        result = Status.DB.sql_query(sqlQuery)
        if str(result) == "()":
            result = None
        return result

    def getFluidIdOfName(self, name):
        result = None
        if name is not None and len(str(name)) > 0:
            sqlQuery = "SELECT DBFluid_ID FROM dbfluid where FluidName = '%s'"%str(name)
            result = Status.DB.sql_query(sqlQuery)
            if str(result) == "()":
                result = None
        if result is None: result = 0
        return int(result)

    def getFluidNameOfId(self, id):
        result = None
        if id is not None:
            sqlQuery = "SELECT FluidName FROM dbfluid where DBFluid_ID = %d"%int(id)
            result = Status.DB.sql_query(sqlQuery)
            if str(result) == "()":
                result = None
        if result is None: result = "None"
        return str(result)

    def fillChoiceOfNaceCode(self, entry):
        naceList = self.getNACECodeandNACESubCodeList()
        self.addNoneFront(naceList)
        fillChoice(entry, naceList)

    def fillChoiceOfProductCodes(self, entry):
        productCodeList = self.getProductCodeList()
        self.addNoneFront(productCodeList)
        fillChoice(entry, productCodeList)

    def fillChoiceOfDBFuel(self, entry):
        fuelDict = FUELTYPES
        fuelList = fuelDict.values()
        fuelList.sort()
        self.addNoneFront(fuelList)
        fillChoice(entry, fuelList)

    def fillChoiceOfDBFuelType(self, entry):
        fuelDict = FUELTYPES
        fuelList = fuelDict.keys()
        fuelList.sort()
        self.addNoneFront(fuelList)
        fillChoice(entry, fuelList)

    def fillChoiceOfDBFuelUnits(self, entry):
        fuelUnitList = self.getFuelUnitList()
        self.addNoneFront(fuelUnitList)
        fillChoice(entry, fuelUnitList)

    def fillChoiceOfDBUnitOpCodes(self, entry):
        unitOpList = self.getUnitOpCodeList()
        self.addNoneFront(unitOpList)
        fillChoice(entry, unitOpList)

    def fillChoiceYesNo(self, entry):
        values = ["No", "Yes"]
        fillChoice(entry, values, False)

    def fillChoiceOfEUnit(self, entry):
        productUnitList = self.getEUnitList()
        self.addNoneFront(productUnitList)
        fillChoice(entry, productUnitList)

    def fillChoiceOfHUnit(self, entry):
        productUnitList = self.getHUnitList()
        self.addNoneFront(productUnitList)
        fillChoice(entry, productUnitList)

    def fillChoiceOfTUnit(self, entry):
        productUnitList = self.getTUnitList()
        self.addNoneFront(productUnitList)
        fillChoice(entry, productUnitList)

    def fillChoiceOfHPSourceSink(self, entry):
        sourceSinkList = self.getSourceSinkList()
        self.addNoneFront(sourceSinkList)
        fillChoice(entry, sourceSinkList)

    def fillChoiceOfHPAbsHeatMed(self, entry):
        absHeatMedList = self.getFluidNameList()
        self.addNoneFront(absHeatMedList)
        fillChoice(entry, absHeatMedList)

    def fillChoiceOfBoilerType(self, entry):
        boilerTypeList = BBTYPES
        boilerTypeList.sort()
        self.addNoneFront(boilerTypeList)
        fillChoice(entry, boilerTypeList)

    def fillChoiceOfHPType(self, entry):
        hpTypeList = HPTYPES
        hpTypeList.sort()
        self.addNoneFront(hpTypeList)
        fillChoice(entry, hpTypeList)

    def fillChoiceOfHPSubType(self, entry):
        hpSubTypeList = self.getHPSubTypeList()
        self.addNoneFront(hpSubTypeList)
        fillChoice(entry, hpSubTypeList)

    def fillChoiceOfSTType(self, entry):
        stTypeList = STTYPES
        stTypeList.sort()
        self.addNoneFront(stTypeList)
        fillChoice(entry, stTypeList)

    def fillChoiceOfCHPType(self, entry):
        chpTypeList = CHPTYPES
        chpTypeList.sort()
        self.addNoneFront(chpTypeList)
        fillChoice(entry, chpTypeList)

    def fillChoiceOfCHPSubType(self, entry):
        chpSubTypeList = self.getCHPSubTypeList()
        self.addNoneFront(chpSubTypeList)
        fillChoice(entry, chpSubTypeList)

    def fillChoiceOfFluidSupply(self, entry):
        fluidNameList = self.getFluidNameList()
        self.addNoneFront(fluidNameList)
        fillChoice(entry, fluidNameList)

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
        self.fillChoiceOfType()
        self.fillChoiceOfSubType()
        self.fillEquipmentList()
        self.notebook.ChangeSelection(0)

    def addNoneFront(self, list):
        if "None" in list:
            list.remove("None")
        newList = ["None"]
        for e in list: newList.append(e)
        return newList

    def fillEquipmentList(self):
        if self.tc_subtype is not None:
            self.fillEquipmentListWithTypeAndSubType()
        else:
            self.fillEquipmentListWithType()

    def fillEquipmentListWithType(self):
        equipments = self.db.get_table()
        ids = equipments.column(self.identifier)
        fields = ', '.join([f for f in self.colLabels])
        if self.tc_type is not None:
            equipe_type = self.tc_type.GetValue(True)

        for id in ids:
            if equipe_type == "All" or len(equipe_type) <= 0:
                sqlQuery = "SELECT %s FROM %s WHERE %s = %s"%(fields,self.table,self.identifier,id)
            elif equipe_type == "None":
                sqlQuery = "SELECT %s FROM %s WHERE %s is NULL and %s = %s"%(fields,self.table,self.type,self.identifier,id)
            else:
                sqlQuery = "SELECT %s FROM %s WHERE %s = '%s' and %s = %s"%(fields,self.table,self.type,equipe_type,self.identifier,id)

            result = Status.DB.sql_query(sqlQuery)
            self.appendResultToGrid(result)

    def fillEquipmentListWithTypeAndSubType(self):
        equipments = self.db.get_table()
        ids = equipments.column(self.identifier)
        fields = ', '.join([f for f in self.colLabels])

        if self.tc_type is not None:
            equipe_type = self.tc_type.GetValue(True)
        if self.tc_subtype is not None:
            equipe_subtype = self.tc_subtype.GetValue(True)

        for id in ids:
            if (equipe_type == "All" or len(equipe_type) <= 0) and (equipe_subtype == "All" or len(equipe_subtype) <= 0):
                sqlQuery = "SELECT %s FROM %s WHERE %s = %s"%(fields,self.table,self.identifier,id)
            elif (equipe_type == "All" or len(equipe_type) <= 0) and equipe_subtype == "None":
                sqlQuery = "SELECT %s FROM %s WHERE %s is NULL and %s = %s"%(fields,self.table,self.subtype,self.identifier,id)
            elif equipe_type == "None" and (equipe_subtype == "All" or len(equipe_subtype) <= 0):
                sqlQuery = "SELECT %s FROM %s WHERE %s is NULL and %s = %s"%(fields,self.table,self.type,self.identifier,id)
            elif equipe_type == "None" and equipe_subtype == "None":
                sqlQuery = "SELECT %s FROM %s WHERE %s is NULL and %s is NULL and %s = %s"%(fields,self.table,self.type,self.subtype,self.identifier,id)
            elif (equipe_type == "All" or len(equipe_type) <= 0):
                sqlQuery = "SELECT %s FROM %s WHERE %s = '%s' and %s = %s"%(fields,self.table,self.subtype,equipe_subtype,self.identifier,id)
            elif (equipe_subtype == "All" or len(equipe_type) <= 0):
                sqlQuery = "SELECT %s FROM %s WHERE %s = '%s' and %s = %s"%(fields,self.table,self.type,equipe_type,self.identifier,id)
            elif equipe_type == "None":
                sqlQuery = "SELECT %s FROM %s WHERE %s is NULL and %s = '%s' and %s = %s"%(fields,self.table,self.type,self.subtype,equipe_subtype,self.identifier,id)
            elif equipe_subtype == "None":
                sqlQuery = "SELECT %s FROM %s WHERE %s = '%s' and %s is NULL and %s = %s"%(fields,self.table,self.type,equipe_type,self.subtype,self.identifier,id)
            else:
                sqlQuery = "SELECT %s FROM %s WHERE %s = '%s' and %s = '%s' and %s = %s"%(fields,self.table,self.type,equipe_type,self.subtype,equipe_subtype,self.identifier,id)

            result = Status.DB.sql_query(sqlQuery)
            self.appendResultToGrid(result)

    def appendResultToGrid(self, result):
        # We want to show the UnitOp as number and text, hence it is required to
        # ask if we are about to show dbbenchmark and call the respective method.
        # This results in slight lower performance. If this is not desired just
        # comment the following three lines and only the code will be shown.
        if self.table == "dbbenchmark":
            self.appendResultToGridBenchmark(result)
            return

        if len(result) > 0:
            self.grid.AppendRows(1, True)
            for i in range(len(self.colLabels)):
                self.grid.SetCellValue(self.grid.GetNumberRows() - 1, i, str(result[i]))

    def appendResultToGridBenchmark(self, result):
        if len(result) > 0:
            self.grid.AppendRows(1, True)
            for i in range(len(self.colLabels)):
                if self.colLabels[i] == "UnitOp":
                    try:
                        self.grid.SetCellValue(self.grid.GetNumberRows() - 1, i, str(result[i]) + ": " + self.unitOpDict[int(result[i])])
                    except:
                        self.grid.SetCellValue(self.grid.GetNumberRows() - 1, i, "None")
                else:
                    self.grid.SetCellValue(self.grid.GetNumberRows() - 1, i, str(result[i]))

# methods to be implemented by derived classes
    def display(self, q = None):
        pass

    def clear(self):
        pass

    def fillChoices(self):
        pass

    def getDBCol(self):
        pass
