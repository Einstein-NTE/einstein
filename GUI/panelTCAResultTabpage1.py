#Boa:FramePanel:panelResult1

import wx
import wx.grid
from GUITools import *

[wxID_PANELRESULT1, wxID_PANELRESULT1BTNADDPROPOSAL, 
 wxID_PANELRESULT1BTNREMOVEPROPOSAL, wxID_PANELRESULT1CBPROPOSALS, 
 wxID_PANELRESULT1GRID, wxID_PANELRESULT1STATICBOX1, 
] = [wx.NewId() for _init_ctrls in range(6)]

class panelResult1(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELRESULT1, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(730, 350),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(722, 323))

        self.grid = wx.grid.Grid(id=wxID_PANELRESULT1GRID, name=u'grid',
              parent=self, pos=wx.Point(8, 8), size=wx.Size(704, 170), style=0)
        self.grid.EnableEditing(False)        
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGridGridCellLeftClick)

        self.cbProposals = wx.Choice(choices=[],
              id=wxID_PANELRESULT1CBPROPOSALS, name=u'cbProposals', parent=self,
              pos=wx.Point(24, 264), size=wx.Size(160, 21), style=0)

        self.staticBox1 = wx.StaticBox(id=wxID_PANELRESULT1STATICBOX1,
              label=u'Choose the proposal(s) to be additionaly displayed:',
              name='staticBox1', parent=self, pos=wx.Point(8, 240),
              size=wx.Size(704, 64), style=0)

        self.btnAddProposal = wx.Button(id=wxID_PANELRESULT1BTNADDPROPOSAL,
              label=u'Add', name=u'btnAddProposal', parent=self,
              pos=wx.Point(192, 264), size=wx.Size(75, 23), style=0)
        self.btnAddProposal.Bind(wx.EVT_BUTTON, self.OnBtnAddProposalButton,
              id=wxID_PANELRESULT1BTNADDPROPOSAL)

        self.btnRemoveProposal = wx.Button(id=wxID_PANELRESULT1BTNREMOVEPROPOSAL,
              label=u'Remove', name=u'btnRemoveProposal', parent=self,
              pos=wx.Point(272, 264), size=wx.Size(75, 23), style=0)
        self.btnRemoveProposal.Bind(wx.EVT_BUTTON,
              self.OnBtnRemoveProposalButton,
              id=wxID_PANELRESULT1BTNREMOVEPROPOSAL)

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)

    def __init_custom_ctrls(self, prnt):
#Grid-------------------------------------------------------------------------
        self.rows = 5
        self.cols = 1
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid.CreateGrid(self.rows,self.cols)

        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(25)
        self.grid.SetRowLabelSize(250)
        self.grid.SetDefaultColSize(230)
        self.grid.SetColSize(0,150)
        
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(10, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _("Proposal 1"))
        
        self.grid.SetRowLabelValue(0, _("Total investment capital (EUR)"))
        self.grid.SetRowLabelValue(1, _("Effective investment capital (EUR)"))
        self.grid.SetRowLabelValue(2, _("Benefit cost ratio"))
        self.grid.SetRowLabelValue(3, _("Payback period (years)"))
        self.grid.SetRowLabelValue(4, _("Internal rate of return at payback (%)"))
        
        self.grid.SetBackgroundColour(wx.Colour(255, 0, 0))
        #choices--------------------------------------------------------------------------------


    def OnGridGridCellLeftClick(self, event):
        event.Skip()

    def OnBtnAddProposalButton(self, event):
        event.Skip()

    def OnBtnRemoveProposalButton(self, event):
        event.Skip()
