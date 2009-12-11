#Boa:Frame:conflictFrame
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	conflictFrame
#			
#------------------------------------------------------------------------------
#			
#	windows for editing conflicts between parameters in cross checking
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	25/04/2008
#	Last revised by:
#                           Stoyan Danov        19/06/2008
#                           
#
#       Changes in last update:
#       19/06/2008 SD: change to translatable text _(...)
#
#------------------------------------------------------------------------------		
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	www.energyxperts.net / info@energyxperts.net
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================
import wx
import wx.grid
import einstein.GUI.pSQL as pSQL
from einstein.GUI.status import Status
from einstein.modules.ccheck.moduleCC import *
from GUITools import *

def create(parent):
    return conflictFrame(parent)

[wxID_CONFLICTFRAME, wxID_CONFLICTFRAMEBUTTON1, wxID_CONFLICTFRAMEBUTTON2, 
 wxID_CONFLICTFRAMEGRID, 
] = [wx.NewId() for _init_ctrls in range(4)]

#
# constants
#

MAXROWS = 150
COLNO = 3
tableKeys = ["1","2","3","4","5","6"]
labels_column = -1

class conflictFrame(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_CONFLICTFRAME, name=u'conflictFrame',
              parent=prnt, pos=wx.Point(80, 50), size=wx.Size(900, 660),
              style=wx.DEFAULT_FRAME_STYLE, title=self.title)
        self.SetClientSize(wx.Size(940, 660))

        self.grid = wx.grid.Grid(id=wxID_CONFLICTFRAMEGRID, name='grid',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(900, 600),
              style=wx.WANTS_CHARS | wx.VSCROLL | wx.HSCROLL)

        self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.OnGridEdit, id=wxID_CONFLICTFRAMEGRID)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridEditStore,
              id=wxID_CONFLICTFRAMEGRID)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnGridCellLeftClick,
              id=wxID_CONFLICTFRAMEGRID)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnGridCellLeftDClick,
              id=wxID_CONFLICTFRAMEGRID)

        self.button1 = wx.Button(id=wx.ID_CANCEL, label=_('Cancel'),
              name='button1', parent=self, pos=wx.Point(772, 610),
              size=wx.Size(128, 32), style=0)

        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, id=wx.ID_CANCEL)

        self.button2 = wx.Button(id=wx.ID_OK, label=_('OK'), name='button2',
              parent=self, pos=wx.Point(632, 610), size=wx.Size(128, 32),
              style=0)

        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, id=wx.ID_OK)

    def __init__(self, parent):
	self.title = _("conflicts in parameter specifications")
        self._init_ctrls(parent)

        #self.maxrow = 25
        self.rowcount = 0
	self.theId = -1
        self.grid.EnableEditing(False)
	self.backcolor = GRID_BACKGROUND_COLOR

        self.lastEditRow = 0
        self.lastEditCol = 0

        self.setupGrid()
        self.displayData()
        
    def setupGrid(self):
        self.grid.CreateGrid(MAXROWS, COLNO)

        for col in range(COLNO):
            self.grid.SetColLabelValue(col, tableKeys[col])

#        self.grid.AutoSizeColumns(setAsMin=True)
        self.grid.EnableEditing(False)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(100)
        self.grid.SetColSize(0,200)
        self.grid.SetColSize(2,600)
#        self.grid.SetColSize(4,200)

        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))

        self.grid.SetColLabelValue(0, _("parameter\n(values in conflict)"))
        self.grid.SetColLabelValue(1, _("data group\n(accuracy)"))
        self.grid.SetColLabelValue(2, _("description\n(calculated from)"))

        for r in range(MAXROWS):

            if r%3 == 0:    #main row of entry
                attr = wx.grid.GridCellAttr()
                attr.SetTextColour(GRID_LETTER_COLOR_HIGHLIGHT)
                attr.SetBackgroundColour(GRID_BACKGROUND_COLOR_HIGHLIGHT)
                attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

                self.grid.SetRowAttr(r, attr)

                self.grid.SetCellAlignment(r, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                self.grid.SetCellAlignment(r, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
                self.grid.SetCellAlignment(r, 2, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);                
            else:
                attr = wx.grid.GridCellAttr()
                attr.SetTextColour(GRID_LETTER_COLOR)
                attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
                attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))

                self.grid.SetRowAttr(r, attr)

                self.grid.SetCellAlignment(r, 0, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);
                self.grid.SetCellAlignment(r, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
                self.grid.SetCellAlignment(r, 2, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);                
                

        self.grid.SetGridCursor(0, 0)
    

    def displayData(self):

#..............................................................................
# display data

        try:
            data = Interfaces.GData["CC Conflict"]
            (rows,cols) = data.shape
            for r in range(rows):
                for c in range(cols):
                    self.grid.SetCellValue(r, c, data[r][c])

            for r in range(rows,MAXROWS):
                for c in range(cols):
                    self.grid.SetCellValue(r, c, "")            
        except:
            pass


    def OnGridEdit(self, event):
        self.lastEditRow = self.grid.GetGridCursorRow()
        self.lastEditCol = self.grid.GetGridCursorCol()
        event.Skip()
        
    def OnGridEditStore(self, event):
        value = self.grid.GetCellValue(self.lastEditRow, self.lastEditCol)
#        row = self.table.select({self.table.keys()[0]:self.grid.GetCellValue(self.lastEditRow,0)})[0]

        if value <> "" and value <> "None":
            row[self.lastEditCol] = value
        else:
            row[self.lastEditCol] = 'NULL'
        self.lastEditRow = 0
        self.lastEditCol = 0
        event.Skip()

    def OnGridCellLeftClick(self, event):
	try:
	    self.theId = int(self.grid.GetCellValue(event.GetRow(), self.col_returned))
	except:
	    print 'DBEditFrame. Returned cell is empty or not integer'
	    self.theId = -1

        event.Skip()


    def OnGridCellLeftDClick(self, event):
	try:
	    self.theId = int(self.grid.GetCellValue(event.GetRow(), self.col_returned))
	except:
	    self.theId = -1

	self.EndModal(wx.ID_OK)


    def OnButtonCancel(self,event):
        event.Skip()

    def OnButtonOK(self,event):
        event.Skip()
