#!/usr/bin/env python
# -*- coding: cp1252 -*-

"""
##########################################################################################

EINSTEIN
Expert system for an intelligent supply of thermal energy in industry
www.energyxperts.net

energyXperts.BCN

Ingeniería Termo-energética y Energías Renovables
Thermo-energetical Engineering and Renewable Energies

Dr. Ullés, 2, 3o
08224 Terrassa (Barcelona), Spain


GUI-Modul Version 0.5
2008 by imsai eSoft Heiko Henning
heiko.henning@imsai.de


##########################################################################################
"""


#-----  Imports
import wx
import wx.grid
import einstein.GUI.pSQL as pSQL
from einstein.GUI.status import *


class DBEditFrame(wx.Frame):

    #def _init_ctrls(self, prnt):
    def __init__(self, prnt, fname, tablename):
        
        wx.Frame.__init__(self, id=-1, name='', parent=prnt, 
              pos=wx.Point(0, 0), size=wx.Size(800, 600),
              style=wx.DEFAULT_FRAME_STYLE, title=fname)


        self.table = pSQL.Table(Status.DB, tablename)
        self.maxrow = 25
        self.rowcount = 0
        self.lastEditCell = []
        
        
        self.window_1 = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.window_1_pane_2 = wx.Panel(self.window_1, -1, style=wx.STATIC_BORDER|wx.TAB_TRAVERSAL)
        self.window_1_pane_1 = wx.Panel(self.window_1, -1, style=wx.STATIC_BORDER|wx.TAB_TRAVERSAL)
        self.frame_1_statusbar = self.CreateStatusBar(1, 0)

        self.gridDBTable = wx.grid.Grid(self.window_1_pane_1, -1, size=(1, 1))

        self.DBPageSlider = wx.Slider(self.window_1_pane_2, -1, 1, 1, 1,
                                      style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_TOP|wx.SL_SELRANGE)

        self.buttonAddRow = wx.Button(self.window_1_pane_2, -1, "add row")
        self.buttonDeleteRow = wx.Button(self.window_1_pane_2, -1, "delete row")
        self.label_2 = wx.StaticText(self.window_1_pane_2, -1, " ")
        self.label_1 = wx.StaticText(self.window_1_pane_2, -1, "Page")
        
        
      
        self.window_1_pane_1.SetMinSize((-1, 500))
        self.DBPageSlider.SetMinSize((300, 90))
        self.window_1_pane_2.SetMinSize((-1, 100))
       
        self.sizer_3 = wx.GridSizer(1, 1, 0, 0)
        self.grid_sizer_1 = wx.GridSizer(2, 4, 0, 0)
        self.grid_sizer_2 = wx.GridSizer(1, 1, 0, 0)
        self.grid_sizer_2.Add(self.gridDBTable, 1, wx.EXPAND|wx.FIXED_MINSIZE, 0)
        self.window_1_pane_1.SetSizer(self.grid_sizer_2)
        self.grid_sizer_1.Add(self.DBPageSlider, 0, wx.EXPAND|wx.FIXED_MINSIZE, 0)
        self.grid_sizer_1.Add(self.buttonAddRow, 0, wx.ALIGN_RIGHT, 0)
        self.grid_sizer_1.Add(self.buttonDeleteRow, 0, wx.ALIGN_RIGHT, 0)
        self.grid_sizer_1.Add(self.label_2, 0, wx.ALIGN_RIGHT, 0)
        self.grid_sizer_1.Add(self.label_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.window_1_pane_2.SetSizer(self.grid_sizer_1)
        self.window_1.SplitHorizontally(self.window_1_pane_1, self.window_1_pane_2, 800)
        self.sizer_3.Add(self.window_1, 1, wx.EXPAND|wx.ALIGN_RIGHT|wx.FIXED_MINSIZE, 0)
        self.SetSizer(self.sizer_3)
        self.Layout()


        self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.OnGridEdit, self.gridDBTable)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridEditStore, self.gridDBTable)
        
        self.Bind(wx.EVT_COMMAND_SCROLL_ENDSCROLL, self.OnDBPageSliderScroll, self.DBPageSlider)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddRow, self.buttonAddRow)

        


        #----- add menu
        
        self.menuImport = wx.Menu()
        self.ImportData = self.menuImport.Append(-1, "Import from file")
        self.Bind(wx.EVT_MENU, self.OnImportData, self.ImportData)
        
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.menuImport, "File")        
        self.SetMenuBar(self.menuBar)

        
        
        self.setValues()
        self.SetupGrid()
        self.displayDBPage(1)
             

    def OnImportData(self, event):
        event.Skip()


    def OnDBPageSliderScroll(self, event):
        self.displayDBPage(self.DBPageSlider.GetValue())


    def OnButtonAddRow(self, event):
        tmp={}
        for col in self.table.keys():
            if col.find('_id') > -1:
                tmp[col] = 0 
            elif col.find('_ID') == -1:
                tmp[col] = 'NULL' 
                
        self.table.insert(tmp)    
        Status.DB.commit()
        self.setValues()
        self.displayDBPage(self.dbpages)
        self.DBPageSlider.SetValue(self.dbpages)



    def OnGridEdit(self, event):
        self.lastEditCell = [self.gridDBTable.GetGridCursorRow(), self.gridDBTable.GetGridCursorCol()]
        
    def OnGridEditStore(self, event):
        value = self.gridDBTable.GetCellValue(self.lastEditCell[0], self.lastEditCell[1])
        row = self.table.select({self.table.keys()[0]:self.gridDBTable.GetCellValue(self.lastEditCell[0],0)})[0]
        if value <> "" and value <> "None":
            row[self.lastEditCell[1]] = value
        else:
            row[self.lastEditCell[1]] = 'NULL'
        Status.DB.commit()
        self.lastEditCell = []

        
    def SetupGrid(self):
        self.gridDBTable.CreateGrid(0, len(self.table.keys()))
        for row in range(len(self.table.keys())):
            self.gridDBTable.SetColLabelValue(row, self.table.keys()[row])
        self.gridDBTable.AutoSizeColumns(setAsMin=True)
        self.gridDBTable.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.gridDBTable.SetMinSize((-1, 400))      


    def displayDBPage(self, pagenr):
        startrow = pagenr * self.maxrow - self.maxrow
        if self.gridDBTable.GetNumberRows() > 0:
            self.gridDBTable.DeleteRows(pos=0,numRows=self.gridDBTable.GetNumberRows())
        rownr = startrow + 1
        r = 0
        c = 0
        for row in self.table.sql_select("%s > 0 ORDER BY %s LIMIT %s,%s" % (self.table.keys()[0],
                                                                             self.table.keys()[0],
                                                                             startrow, self.maxrow)):
            self.gridDBTable.AppendRows(numRows=1)
            self.gridDBTable.SetRowLabelValue(r, "%s" % (rownr))
            for col in row:
                self.gridDBTable.SetCellValue(r, c, "%s" % (row[c]))
                if c == 0:self.gridDBTable.SetReadOnly(r, c, isReadOnly=True)
                c += 1
            c = 0
            r +=1
            rownr += 1
                

    def setValues(self):
        self.rowcount = len(self.table.sql_select("%s > 0" % (self.table.keys()[0])))
        
        if self.rowcount%self.maxrow > 0:
            tmp = 1
        else:
            tmp = 0

        self.dbpages = self.rowcount/self.maxrow + tmp
        self.DBPageSlider.SetRange(1, self.dbpages)

