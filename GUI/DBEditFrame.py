# -*- coding: iso-8859-15 -*-
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	DBEditFrame
#			
#------------------------------------------------------------------------------
#			
#	Data base editing window
#
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Heiko Henning	February 2008
#	Last revised by:    Hans Schweiger      13/04/2008
#                           Tom Sobota          21/04/2008
#                           Tom Sobota          07/05/2008
#                           Stoyan Danov        19/06/2008
#
#       Changes in last update:
#       13/04/08:       preselection added as input
#       21/04/08: TS    Intercepted error when non existing table
#       07/05/08: TS    Changed layout, added Delete row, Add row buttons
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
import einstein.GUI.pSQL as pSQL
from einstein.GUI.status import Status

#debug
#def _(str):
#    return str

#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR_NOEDITABLE = '#F0FFFF' # idem
GRID_BACKGROUND_COLOR_EDITABLE = '#FFFFC0' # idem

class DBEditFrame(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=-1, name=u'DBEditFrame',
              parent=prnt, pos=wx.Point(354, 332), size=wx.Size(800, 400),
              style=wx.DEFAULT_FRAME_STYLE, title=self.title)
        self.SetClientSize(wx.Size(800, 400))

        self.grid1 = wx.grid.Grid(self,-1, name='grid1',
                                  style=wx.WANTS_CHARS | wx.VSCROLL | wx.HSCROLL)
        self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.OnGridEdit, self.grid1)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridEditStore, self.grid1)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnGridCellLeftClick, self.grid1)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnGridCellLeftDClick, self.grid1)

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,_('Cancel'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        self.buttonOK = wx.Button(self,wx.ID_OK,_('OK'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)

        if self.can_edit:
            # add and delete row buttons are shown only if
            # editing is allowed
            self.buttonAddRow = wx.Button(self, -1, _("Add row"))
            self.Bind(wx.EVT_BUTTON, self.OnButtonAddRow, self.buttonAddRow)
            self.buttonDeleteRow = wx.Button(self, -1, _("Delete row"))
            self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteRow, self.buttonDeleteRow)

        self.lblTableName = wx.StaticText(self, -1, "")

    def __init__(self, parent, title, tablename, col_returned, can_edit, preselection = None):
	self.title = title
	self.tablename = tablename
	self.can_edit = can_edit
	self.col_returned = col_returned
        self.preselection = preselection
        self._init_ctrls(parent)
        self.__do_layout()


        #self.maxrow = 25
        self.rowcount = 0
	self.theId = -1
        self.col0 = None
        self.grid1.EnableEditing(can_edit)
	if can_edit:
	    self.backcolor = GRID_BACKGROUND_COLOR_EDITABLE
            self.lblTableName.SetLabel(_(" Editing table ")+tablename)
	else:
	    self.backcolor = GRID_BACKGROUND_COLOR_NOEDITABLE
            self.lblTableName.SetLabel(_(" Viewing table ")+tablename)

        self.lastEditRow = 0
        self.lastEditCol = 0

        if self.initDatabase():
            self.SetupGrid()
            self.displayData()

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_3.Add(self.grid1, 1, wx.EXPAND, 0)
        sizer_3.Add(self.lblTableName, 0, wx.TOP|wx.EXPAND, 2)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

        if self.can_edit:
            sizer_2.Add(self.buttonAddRow, 0, 0, 0)
            sizer_2.Add(self.buttonDeleteRow, 0, 0, 0)
            
        sizer_2.Add(self.buttonCancel, 0, 0, 0)
        sizer_2.Add(self.buttonOK, 0, 0, 0)
        sizer_1.Add(sizer_2, 0, wx.ALIGN_BOTTOM, 0)
        self.SetSizer(sizer_1)
        self.Layout()

#HS2008-04-13: possibility of preselection-list added in DB Editor.
    def initDatabase(self):
        try:
            self.table = pSQL.Table(Status.DB, self.tablename)
            #HS         sqlTable = pSQL.Table(Status.DB, self.tablename)
            #HS         self.table = self.preSelected(sqlTable,self.preselection)
            self.rows = len(self.table.sql_select("%s > 0" % (self.table.keys()[0])))
            #HS         self.rows = len(self.table)
            #HS         self.keys = sqlTable.keys()
            return True
        except:
            dlg = wx.MessageDialog(None, _('Error accessing table ')+self.tablename,
                                   'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        
    def preSelected(self,sqlTable,preselection):
        pTable = []
        for row in sqlTable:
            print "preSelected: ", row.DBHeatPump_ID
            if (row.DBHeatPump_ID in preselection) or (preselection is None):
                print "OK"
                pTable.append(row)
        return pTable

    def SetupGrid(self):
#HS2008-04-13
        self.grid1.CreateGrid(self.rows, len(self.table.keys()))
#HS        self.grid1.CreateGrid(self.rows, len(self.keys))
        for row in range(len(self.table.keys())):
            self.grid1.SetColLabelValue(row, self.table.keys()[row])
#HS        for row in range(len(self.keys)):
#HS            self.grid1.SetColLabelValue(row, self.keys[row])
        self.grid1.AutoSizeColumns(setAsMin=True)
        self.grid1.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        #self.grid1.SetMinSize((-1, 400))      

        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))

    def displayData(self):
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(self.backcolor)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

        startrow = 0
        if self.grid1.GetNumberRows() > 0:
            self.grid1.DeleteRows(pos=0,numRows=self.grid1.GetNumberRows())
        rownr = startrow + 1
        r = 0
        c = 0

        for row in self.table.sql_select("%s > 0 ORDER BY %s" % (self.table.keys()[0],
								 self.table.keys()[0])):

            self.grid1.SetRowAttr(r, attr)
            self.grid1.AppendRows(numRows=1)
            self.grid1.SetRowLabelValue(r, "%s" % (rownr))
            for col in row:
                self.grid1.SetCellValue(r, c, "%s" % (row[c]))
                if c == 0:self.grid1.SetReadOnly(r, c, isReadOnly=True)
                c += 1
            c = 0
            r +=1
            rownr += 1

    def OnGridEdit(self, event):
        self.lastEditRow = self.grid1.GetGridCursorRow()
        self.lastEditCol = self.grid1.GetGridCursorCol()
        event.Skip()
        
    def OnGridEditStore(self, event):
        value = self.grid1.GetCellValue(self.lastEditRow, self.lastEditCol)
        row = self.table.select({self.table.keys()[0]:self.grid1.GetCellValue(self.lastEditRow,0)})[0]
#HS        row = self.table.select({self.keys[0]:self.grid1.GetCellValue(self.lastEditRow,0)})[0]
        if value <> "" and value <> "None":
            row[self.lastEditCol] = value
        else:
            row[self.lastEditCol] = 'NULL'
        self.lastEditRow = 0
        self.lastEditCol = 0
        event.Skip()

    def OnGridCellLeftClick(self, event):
	try:
	    i = self.grid1.GetCellValue(event.GetRow(), self.col_returned)
	    self.theId = int(i)
	except:
	    print 'DBEditFrame. Returned cell is empty or not integer:'+repr(i)
	    self.theId = -1
        self.col0 = self.grid1.GetCellValue(event.GetRow(), 0)

        event.Skip()


    def OnGridCellLeftDClick(self, event):
	# accept editions and close this dialog
	if self.can_edit:
	    Status.DB.sql_query('commit')
	self.EndModal(wx.ID_OK)


    def OnButtonCancel(self,event):
	if self.can_edit:
	    Status.DB.sql_query('rollback')
	self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def OnButtonOK(self,event):
	if self.can_edit:
	    Status.DB.sql_query('commit')
	self.EndModal(wx.ID_OK)
        event.Skip()

    def OnButtonAddRow(self,event):
        tmp={}
        for col in self.table.keys():
            # create empty row
            ty = col.find('_id')
            if ty >= 0:
                tmp[col] = 0 
            else:
                tmp[col] = 'NULL' 
                
        self.table.insert(tmp)    
        self.displayData()
        event.Skip()

    def OnButtonDeleteRow(self,event):
        if self.col0 is None:
            dlg = wx.MessageDialog(None,_('A row must be selected!\n'\
                                   'Please click on any data cell\n'\
                                   'to select a row'),
                                   _('Warning'), wx.OK | wx.ICON_EXCLAMATION)
            ret = dlg.ShowModal()
            dlg.Destroy()
        else:
            field = self.table.columns()[0]
            dlg = wx.MessageDialog(None, _('Delete row with %s=%s?') % (field,self.col0),
                                   _('Confirm delete'), wx.YES_NO | wx.ICON_QUESTION)
            ret = dlg.ShowModal()
            dlg.Destroy()
            if ret == wx.ID_NO:
                return
            try:
                dummy = int(self.col0)
                rows = self.table.select({field:self.col0})
                if len(rows) == 1:
                    row = rows[0]
                    row.delete()
                    self.displayData()
            except:
                dlg = wx.MessageDialog(None,_('Cannot delete row with %s=%s') % (field,self.col0),
                                       _('Warning'), wx.OK | wx.ICON_EXCLAMATION)
                ret = dlg.ShowModal()
                dlg.Destroy()
        event.Skip()
