#Boa:Frame:DBEditFrame
#HS 2008-04-13: preselection added as input
import wx
import einstein.GUI.pSQL as pSQL
from einstein.GUI.status import Status

def create(parent):
    return DBEditFrame(parent)

[wxID_DBEDITFRAME, wxID_DBEDITFRAMEBUTTON1, wxID_DBEDITFRAMEBUTTON2, 
 wxID_DBEDITFRAMEGRID1, 
] = [wx.NewId() for _init_ctrls in range(4)]

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
        wx.Dialog.__init__(self, id=wxID_DBEDITFRAME, name=u'DBEditFrame',
              parent=prnt, pos=wx.Point(354, 332), size=wx.Size(800, 400),
              style=wx.DEFAULT_FRAME_STYLE, title=self.title)
        self.SetClientSize(wx.Size(800, 400))

        self.grid1 = wx.grid.Grid(id=wxID_DBEDITFRAMEGRID1, name='grid1',
              parent=self, pos=wx.Point(8, 32), size=wx.Size(632, 352),
              style=wx.WANTS_CHARS | wx.VSCROLL | wx.HSCROLL)
        self.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.OnGridEdit, self.grid1)
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnGridEditStore, self.grid1)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnGridCellLeftClick, self.grid1)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnGridCellLeftDClick, self.grid1)

        self.button1 = wx.Button(id=wx.ID_CANCEL, label=u'Cancel',
              name='button1', parent=self, pos=wx.Point(656, 352),
              size=wx.Size(128, 32), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.button1)

        self.button2 = wx.Button(id=wx.ID_OK, label=u'OK', name='button2',
              parent=self, pos=wx.Point(656, 312), size=wx.Size(128, 32),
              style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.button2)

    def __init__(self, parent, title, tablename, col_returned, can_edit, preselection = None):
	self.title = title
	self.tablename = tablename
	self.can_edit = can_edit
	self.col_returned = col_returned
        self._init_ctrls(parent)
        self.preselection = preselection

        #self.maxrow = 25
        self.rowcount = 0
	self.theId = -1
        self.grid1.EnableEditing(can_edit)
	if can_edit:
	    self.backcolor = GRID_BACKGROUND_COLOR_EDITABLE
	else:
	    self.backcolor = GRID_BACKGROUND_COLOR_NOEDITABLE

        self.lastEditRow = 0
        self.lastEditCol = 0

        self.initDatabase()
        self.SetupGrid()
	self.displayData()

#HS2008-04-13: possibility of preselection-list added in DB Editor.
    def initDatabase(self):
        self.table = pSQL.Table(Status.DB, self.tablename)
#HS        sqlTable = pSQL.Table(Status.DB, self.tablename)
#HS        self.table = self.preSelected(sqlTable,self.preselection)
        self.rows = len(self.table.sql_select("%s > 0" % (self.table.keys()[0])))
#HS        self.rows = len(self.table)
#HS        self.keys = sqlTable.keys()
        
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

        #startrow = pagenr * self.maxrow - self.maxrow # if paginated
        startrow = 0
        if self.grid1.GetNumberRows() > 0:
            self.grid1.DeleteRows(pos=0,numRows=self.grid1.GetNumberRows())
        rownr = startrow + 1
        r = 0
        c = 0
        #for row in self.table.sql_select("%s > 0 ORDER BY %s LIMIT %s,%s" % (self.table.keys()[0],
        #                                                                     self.table.keys()[0],
        #                                                                     startrow, self.maxrow)):

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
	    self.theId = int(self.grid1.GetCellValue(event.GetRow(), self.col_returned))
	except:
	    print 'DBEditFrame. Returned cell is empty or not integer'
	    self.theId = -1

        event.Skip()


    def OnGridCellLeftDClick(self, event):
	try:
	    self.theId = int(self.grid1.GetCellValue(event.GetRow(), self.col_returned))
	except:
	    print 'DBEditFrame. Returned cell is empty or not integer'
	    self.theId = -1

	# accept editions and close this dialog
	if self.can_edit:
	    Status.DB.sql_query('commit')
	self.EndModal(wx.ID_OK)


    def OnButtonCancel(self,event):
	if self.can_edit:
	    Status.DB.sql_query('rollback')
        event.Skip()

    def OnButtonOK(self,event):
	if self.can_edit:
	    Status.DB.sql_query('commit')
        event.Skip()
