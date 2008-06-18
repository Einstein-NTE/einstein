#Boa:FramePanel:PanelHC
# -*- coding: cp1252 -*-
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	Panel Boilers and Burners
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Panel for HC design assistant
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Hans Schweiger	    03/04/2008
#	Last revised by:    Hans Schweiger          16/04/2008
#                           Stoyan Danov            18/06/2008
#                           
#
#       Changes to previous version:
#       16/04/2008  HS  main as argument in __init__
#       18/06/2008 SD: change to translatable text _(...)
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
from einstein.GUI.graphics import drawPiePlot
from einstein.modules.modules import Modules
from einstein.GUI.status import Status
#from einstein.GUI.panelHC_PopUp1 import HCPopUp1

import einstein.modules.matPanel as Mp
from einstein.modules.interfaces import *


[wxID_PANELHC, wxID_PANELHCAUTODESIGN, wxID_PANELHCBUTTONPAGEHCBACK, 
 wxID_PANELHCBUTTONPAGEHCCANCEL, wxID_PANELHCBUTTONPAGEHCFWD, 
 wxID_PANELHCBUTTONPAGEHCOK, wxID_PANELHCGRID, wxID_PANELHCHCADD, 
 wxID_PANELHCMOVEDOWNWARDS, wxID_PANELHCMOVETOBOTTOM, wxID_PANELHCMOVETOTOP, 
 wxID_PANELHCMOVEUPWARDS, wxID_PANELHCST1PAGEHC, wxID_PANELHCSTATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(14)]

# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGHC
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem

MAXROWS = 50
COLNO = 6

class PanelHC(wx.Panel):

    def __init__(self, parent, main, id, pos, size, style, name):
        self.main = main
        self._init_ctrls(parent)
	self.keys = ['HC Table']
        self.mod = Status.mod.moduleHC
        self.selectedRow = 0
        labels_column = 0
        
        #
        # additional widgets setup
        # here, we modify some widgets attributes that cannot be changed
        # directly by Boa. This cannot be done in _init_ctrls, since that
        # method is rewritten by Boa each time.
        #
        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid.CreateGrid(MAXROWS, COLNO)

        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(60)
        self.grid.SetColSize(2,160)
        self.grid.SetColSize(3,160)

        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _("Cascade index"))
        self.grid.SetColLabelValue(1, _("Equipment No."))
        self.grid.SetColLabelValue(2, _("Equipment"))
        self.grid.SetColLabelValue(3, _("Type"))
        self.grid.SetColLabelValue(4, _("Nominal power [kW]"))
        self.grid.SetColLabelValue(5, _("Heat Supplied to pipe/duct no."))
        #
        # copy values from dictionary to grid
        #
        for r in range(MAXROWS):
            self.grid.SetRowAttr(r, attr)
            for c in range(COLNO):
                if c == labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);

        self.grid.SetGridCursor(0, 0)

        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELHC, name='PanelHC', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
        self.SetClientSize(wx.Size(800, 600))

        self.grid = wx.grid.Grid(id=wxID_PANELHCGRID,
              name='gridpageHC', parent=self, pos=wx.Point(40, 96),
              size=wx.Size(616, 328), style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridGridCellLeftDclick, id=wxID_PANELHCGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGridGridCellLeftClick, id=wxID_PANELHCGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridGridCellRightClick, id=wxID_PANELHCGRID)

        self.st1pageHC = wx.StaticText(id=-1, label=_('Order equipment cascade'),
              name='st1pageHC', parent=self, pos=wx.Point(664, 128), style=0)

        self.buttonpageHCOk = wx.Button(id=wxID_PANELHCBUTTONPAGEHCOK,
              label=_('ok'), name='buttonpageHCOk', parent=self, pos=wx.Point(528,
              544), size=wx.Size(75, 23), style=0)
        self.buttonpageHCOk.Bind(wx.EVT_BUTTON, self.OnButtonpageHCOkButton,
              id=wxID_PANELHCBUTTONPAGEHCOK)

        self.buttonpageHCCancel = wx.Button(id=wxID_PANELHCBUTTONPAGEHCCANCEL,
              label=_('cancel'), name='buttonpageHCCancel', parent=self,
              pos=wx.Point(616, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageHCCancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpageHCCancelButton,
              id=wxID_PANELHCBUTTONPAGEHCCANCEL)

        self.buttonpageHCFwd = wx.Button(id=wxID_PANELHCBUTTONPAGEHCFWD,
              label='>>>', name='buttonpageHCFwd', parent=self,
              pos=wx.Point(704, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageHCFwd.Bind(wx.EVT_BUTTON, self.OnButtonpageHCFwdButton,
              id=wxID_PANELHCBUTTONPAGEHCFWD)

        self.buttonpageHCBack = wx.Button(id=wxID_PANELHCBUTTONPAGEHCBACK,
              label='<<<', name='buttonpageHCBack', parent=self,
              pos=wx.Point(440, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageHCBack.Bind(wx.EVT_BUTTON, self.OnButtonpageHCBackButton,
              id=wxID_PANELHCBUTTONPAGEHCBACK)

        self.MoveToBottom = wx.Button(id=wxID_PANELHCMOVETOBOTTOM,
              label='to bottom', name='MoveToBottom', parent=self,
              pos=wx.Point(680, 344), size=wx.Size(96, 24), style=0)
        self.MoveToBottom.Bind(wx.EVT_BUTTON, self.OnMoveToBottomButton,
              id=wxID_PANELHCMOVETOBOTTOM)

        self.MoveDownwards = wx.Button(id=wxID_PANELHCMOVEDOWNWARDS,
              label=_('down'), name='MoveDownwards', parent=self, pos=wx.Point(680,
              304), size=wx.Size(96, 24), style=0)
        self.MoveDownwards.Bind(wx.EVT_BUTTON, self.OnMoveDownwardsButton,
              id=wxID_PANELHCMOVEDOWNWARDS)

        self.MoveUpwards = wx.Button(id=wxID_PANELHCMOVEUPWARDS, label=_('up'),
              name='MoveUpwards', parent=self, pos=wx.Point(680, 240),
              size=wx.Size(96, 24), style=0)
        self.MoveUpwards.Bind(wx.EVT_BUTTON, self.OnMoveUpwardsButton,
              id=wxID_PANELHCMOVEUPWARDS)

        self.MoveToTop = wx.Button(id=wxID_PANELHCMOVETOTOP, label=_('to top'),
              name='MoveToTop', parent=self, pos=wx.Point(680, 200),
              size=wx.Size(96, 24), style=0)
        self.MoveToTop.Bind(wx.EVT_BUTTON, self.OnMoveToTopButton,
              id=wxID_PANELHCMOVETOTOP)

        self.AutoDesign = wx.Button(id=wxID_PANELHCAUTODESIGN,
              label=_('get recommendations and automatic pre-design'),
              name='AutoDesign', parent=self, pos=wx.Point(40, 32),
              size=wx.Size(616, 24), style=0)
        self.AutoDesign.Bind(wx.EVT_BUTTON, self.OnAutoDesignButton,
              id=wxID_PANELHCAUTODESIGN)

        self.staticText1 = wx.StaticText(id=wxID_PANELHCSTATICTEXT1,
              label=_('Existing equipment in the system'),
              name='staticText1', parent=self, pos=wx.Point(40, 72), style=0)

#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   function activated on each entry into the panel from the tree
#------------------------------------------------------------------------------		
        self.mod.initPanel()        # prepares data for plotting

        data = Interfaces.GData[self.keys[0]]

#..............................................................................
# update of equipment table

        try:
            data = Interfaces.GData[self.keys[0]]
            (rows,cols) = data.shape
        except:
            rows = 0
            cols = COLNO
            
        for r in range(rows):
            for c in range(cols):
                self.grid.SetCellValue(r, c, data[r][c])

#XXX Here better would be updating the grid and showing less rows ... ????
        for r in range(rows,MAXROWS):
            for c in range(cols):
                self.grid.SetCellValue(r, c, "")

        self.Show()

#------------------------------------------------------------------------------		
    def OnGridGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
        self.selectedRow = event.GetRow()
        print _("PanelHC (GridLeftDclick): selected row = "),self.selectedRow
        event.Skip()

#------------------------------------------------------------------------------		
    def OnGridGridCellLeftClick(self, event):
#------------------------------------------------------------------------------		
	self.selectedRow = event.GetRow()
        print _("PanelHC (GridLeftClick): selected row = "),self.selectedRow
        event.Skip()

    def OnGridGridCellRightClick(self, event):
	self.selectedRow = event.GetRow()
        print _("PanelHC (GridRightClick): selected row = "),self.selectedRow
        event.Skip()
        
#==============================================================================
#   <<< OK Cancel >>>
#==============================================================================

    def OnButtonpageHCOkButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qA, select=True)
        print "Button exitModuleOK: now I should go back to HC"

    def OnButtonpageHCCancelButton(self, event):
        self.Hide()
        print "Button exitModuleCancel: now I should go back to HC"

    def OnButtonpageHCBackButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qA, select=True)
        print "Button exitModuleBack: now I should show another window"

    def OnButtonpageHCFwdButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHP, select=True)
        print "Button exitModuleFwd: now I should show another window"

#==============================================================================
#   Bottom Down Up Top
#==============================================================================
    def OnMoveToBottomButton(self, event):
        ci = self.selectedRow + 1
        print _("PanelHC (move to bottom)"),ci
        self.mod.cascadeMoveToBottom(ci)
        self.display()

    def OnMoveDownwardsButton(self, event):
        ci = self.selectedRow + 1
        print _("PanelHC (move down)"),ci
        self.mod.cascadeMoveDown(ci)
        self.display()

    def OnMoveUpwardsButton(self, event):
        ci = self.selectedRow + 1
        print _("PanelHC (move up)"),ci
        self.mod.cascadeMoveUp(ci)
        self.display()

    def OnMoveToTopButton(self, event):
        ci = self.selectedRow + 1
        print _("PanelHC (move to top)"),ci
        self.mod.cascadeMoveToTop(ci)   
        self.display()
#==============================================================================

    def OnAutoDesignButton(self, event):
        event.Skip()

