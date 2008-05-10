#Boa:FramePanel:PanelA
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
#	Panel Design of Alternative Proposals
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	
#
#==============================================================================
#
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	    03/04/2008
#	Revised by:    
#                           Tom Sobota              05/04/2008
#                           Hans Schweiger          15/04/2008
#       Revised by:         Tom Sobota  28/04/2008
#
#       Changes to previous version:
#       05/04/08    changed call to popup1 in OnButtonpageHPAddButton
#                   slight change to OK and Cancel buttons, to show the right icons
#       15/04/08 HS copy and delete buttons added. event handler "Generate New" linked
#       28/04/2008  added 'draw' to method display
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
from einstein.GUI.addEquipment_popup import AddEquipment #TS 20080405 changed


import einstein.modules.matPanel as Mp
from einstein.modules.interfaces import *
from einstein.GUI.dialogA import *
from einstein.GUI.dialogOK import *


[wxID_PANELA, wxID_PANELABUTTONPAGEABACK, wxID_PANELABUTTONPAGEACANCEL, 
 wxID_PANELABUTTONPAGEAFWD, wxID_PANELABUTTONPAGEAOK, wxID_PANELACOPYPROPOSAL, 
 wxID_PANELADELETEPROPOSAL, wxID_PANELADESIGNHC, wxID_PANELADESIGNHX, 
 wxID_PANELADESIGNPA, wxID_PANELADESIGNPO, wxID_PANELAGENERATENEW, 
 wxID_PANELAGRID, wxID_PANELAPANELAFIG, wxID_PANELAST1PAGEA, 
 wxID_PANELAST3PAGEA, wxID_PANELASTTITLEPAGEA, 
] = [wx.NewId() for _init_ctrls in range(17)]

# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGA
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem

MAXROWS = 10

class PanelA(wx.Panel):

    def __init__(self, parent, main):
        self._init_ctrls(parent)
	keys = ['A Table','A Plot']
	self.keys = keys
	self.main = main
        self.mod = Status.mod.moduleA
        self.shortName = "new alternative"
        self.description = "describe shortly the main differential features of the new alternative"
        self.ANo = Status.ANo
#==============================================================================
#   graphic: Cumulative heat demand by hours
#==============================================================================
        labels_column = 0
        ignoredrows = []
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : 'Some title',           # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelAFig,
                            wx.Panel,
                            drawPiePlot,
                            paramList)

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

        key = keys[0]
        data = Interfaces.GData[key]
        (rows,cols) = data.shape
        self.grid.CreateGrid(max(rows,MAXROWS), cols)

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(80)
        self.grid.SetColSize(0,40)
        self.grid.SetColSize(1,160)
        self.grid.SetColSize(2,320)
        self.grid.SetColSize(3,40)
        
        self.grid.EnableEditing(False)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, "Alternative No")
        self.grid.SetColLabelValue(1, "Name")
        self.grid.SetColLabelValue(2, "Description")
        self.grid.SetColLabelValue(3, "State of processing")
        self.grid.SetColLabelValue(4, "Primary energy consumption\n[MWh/a]")
        self.grid.SetColLabelValue(5, "Total annual energy cost\n[€/a]")
        #
        # copy values from dictionary to grid
        #
        for r in range(MAXROWS):
            self.grid.SetRowAttr(r, attr)
            for c in range(cols):
#                self.grid.SetCellValue(r, c, "")
                if c == labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid.SetGridCursor(0, 0)

        self.stTitlePageA.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELA, name='PanelA', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(808, 634), style=0)
        self.SetClientSize(wx.Size(800, 600))

        self.panelAFig = wx.Panel(id=wxID_PANELAPANELAFIG, name='panelAFigure',
              parent=self, pos=wx.Point(26, 346), size=wx.Size(382, 220),
              style=wx.TAB_TRAVERSAL)

        self.DesignPA = wx.Button(id=wxID_PANELADESIGNPA,
              label='pinch analysis', name='DesignPA', parent=self,
              pos=wx.Point(592, 360), size=wx.Size(184, 24), style=0)
        self.DesignPA.Bind(wx.EVT_BUTTON, self.OnDesignPAButton,
              id=wxID_PANELADESIGNPA)

        self.grid = wx.grid.Grid(id=wxID_PANELAGRID, name='gridpageA',
              parent=self, pos=wx.Point(24, 56), size=wx.Size(752, 216),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageAGridCellLeftDclick, id=wxID_PANELAGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageAGridCellRightClick, id=wxID_PANELAGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGridPageAGridCellLeftClick)

        self.st1pageA = wx.StaticText(id=-1, label='Existing alternatives',
              name='st1pageA', parent=self, pos=wx.Point(24, 40), style=0)

        self.stTitlePageA = wx.StaticText(id=wxID_PANELASTTITLEPAGEA,
              label='Design of alternative proposals', name='stTitlePageA',
              parent=self, pos=wx.Point(24, 16), style=0)
        self.stTitlePageA.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.buttonpageAOk = wx.Button(id=wx.ID_OK, label='OK',
              name='buttonpageAOk', parent=self, pos=wx.Point(528, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageAOk.Bind(wx.EVT_BUTTON, self.OnButtonpageAOkButton,
              id=wx.ID_OK)

        self.buttonpageACancel = wx.Button(id=wx.ID_CANCEL, label='Cancel',
              name='buttonpageACancel', parent=self, pos=wx.Point(616, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageACancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpageACancelButton, id=wx.ID_CANCEL)

        self.buttonpageAFwd = wx.Button(id=wxID_PANELABUTTONPAGEAFWD,
              label='>>>', name='buttonpageAFwd', parent=self, pos=wx.Point(704,
              544), size=wx.Size(75, 23), style=0)
        self.buttonpageAFwd.Bind(wx.EVT_BUTTON, self.OnButtonpageAFwdButton,
              id=wxID_PANELABUTTONPAGEAFWD)

        self.buttonpageABack = wx.Button(id=wxID_PANELABUTTONPAGEABACK,
              label='<<<', name='buttonpageABack', parent=self,
              pos=wx.Point(440, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageABack.Bind(wx.EVT_BUTTON, self.OnButtonpageABackButton,
              id=wxID_PANELABUTTONPAGEABACK)

        self.GenerateNew = wx.Button(id=wxID_PANELAGENERATENEW,
              label='generate new proposal', name='GenerateNew', parent=self,
              pos=wx.Point(24, 280), size=wx.Size(136, 24), style=0)
        self.GenerateNew.Bind(wx.EVT_BUTTON, self.OnGenerateNewButton,
              id=wxID_PANELAGENERATENEW)

        self.st3pageA = wx.StaticText(id=wxID_PANELAST3PAGEA,
              label='Comparison of energy consumption', name='st3pageA',
              parent=self, pos=wx.Point(24, 320), size=wx.Size(170, 13),
              style=0)

        self.DesignHX = wx.Button(id=wxID_PANELADESIGNHX,
              label='HX network design', name='DesignHX', parent=self,
              pos=wx.Point(592, 400), size=wx.Size(184, 24), style=0)
        self.DesignHX.Bind(wx.EVT_BUTTON, self.OnDesignHXButton,
              id=wxID_PANELADESIGNHX)

        self.DesignHC = wx.Button(id=wxID_PANELADESIGNHC,
              label='Heat and cold supply', name='DesignHC', parent=self,
              pos=wx.Point(592, 440), size=wx.Size(184, 24), style=0)
        self.DesignHC.Bind(wx.EVT_BUTTON, self.OnDesignHCButton,
              id=wxID_PANELADESIGNHC)

        self.DesignPO = wx.Button(id=wxID_PANELADESIGNPO,
              label='process optimisation', name='DesignPO', parent=self,
              pos=wx.Point(592, 320), size=wx.Size(184, 24), style=0)
        self.DesignPO.Bind(wx.EVT_BUTTON, self.OnDesignPOButton,
              id=wxID_PANELADESIGNPO)

        self.copyProposal = wx.Button(id=wxID_PANELACOPYPROPOSAL,
              label='copy proposal', name='copyProposal', parent=self,
              pos=wx.Point(176, 280), size=wx.Size(136, 24), style=0)
        self.copyProposal.Bind(wx.EVT_BUTTON, self.OnCopyProposalButton,
              id=wxID_PANELACOPYPROPOSAL)

        self.deleteProposal = wx.Button(id=wxID_PANELADELETEPROPOSAL,
              label='delete proposal', name='deleteProposal', parent=self,
              pos=wx.Point(328, 280), size=wx.Size(136, 24), style=0)
        self.deleteProposal.Bind(wx.EVT_BUTTON, self.OnDeleteProposalButton,
              id=wxID_PANELADELETEPROPOSAL)

#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   function activated on each entry into the panel from the tree
#------------------------------------------------------------------------------		
        self.mod.initPanel()        # prepares data for plotting

#..............................................................................
# update of alternatives table

        data = Interfaces.GData[self.keys[0]]
        print "data = ",data
        (rows,cols) = data.shape
        print rows,cols
        for r in range(rows):
            for c in range(cols):
                try:
                    self.grid.SetCellValue(r, c, data[r][c])
                except:
                    pass

#XXX Here better would be updating the grid and showing less rows ... ????
        for r in range(rows,MAXROWS):
            for c in range(cols):
                self.grid.SetCellValue(r, c, "")

        self.panelAFig.draw()
        self.Show()
        self.main.panelinfo.update()
       
#------------------------------------------------------------------------------		

#==============================================================================
#   EVENT HANDLERS
#==============================================================================

#------------------------------------------------------------------------------		
    def OnGenerateNewButton(self, event):
#------------------------------------------------------------------------------		
#   Generate new alterantive proposal
#------------------------------------------------------------------------------		

        self.shortName = "New Proposal %s"%(Status.NoOfAlternatives+1)
        self.description = "based on present state"
        
        pu1 =  DialogA(self)
        if pu1.ShowModal() == wx.ID_OK:
            print "PanelA - OK",self.shortName,self.description
            print "PanelA (GenerateNew-Button): calling function createNewAlternative"

            Status.prj.createNewAlternative(0,self.shortName,self.description)
            self.display()

        elif pu1.ShowModal() == wx.ID_Cancel:
            print "PanelA - Cancel"
        else:
            print "PanelA ???"

        self.display()
        
#------------------------------------------------------------------------------		
    def OnCopyProposalButton(self, event):
#------------------------------------------------------------------------------		
#   Generate new porposal copying from existing alternative
#------------------------------------------------------------------------------		
        self.shortName = self.grid.GetCellValue(self.selectedRow,1)+"(mod.)"
        self.description = self.grid.GetCellValue(self.selectedRow,2)+"(modified alternative based on "+self.grid.GetCellValue(self.selectedRow,1)+")"

        pu1 =  DialogA(self)
        if pu1.ShowModal() == wx.ID_OK:
            print "PanelA - OK",self.shortName,self.description
            print "PanelA (GenerateNew-Button): calling function createNewAlternative"

            Status.prj.createNewAlternative(self.ANo,self.shortName,self.description)
            self.display()

        elif pu1.ShowModal() == wx.ID_Cancel:
            print "PanelA - Cancel"
        else:
            print "PanelA - ???"

#------------------------------------------------------------------------------		
    def OnDeleteProposalButton(self, event):
#------------------------------------------------------------------------------		
#   Delete alternative proposal
#------------------------------------------------------------------------------		

        pu2 =  DialogOK(self,"delete alternative","do you really want to delete this alternative ?")
        if pu2.ShowModal() == wx.ID_OK:
            if self.ANo > 0:
                Status.prj.deleteAlternative(self.ANo)
                self.display()
            elif self.ANo in [-1,0]:
                print "PanelA (DeleteButton): cannot delete alternative ",self.ANo
            else:
                print "PanelA (DeleteButton): erroneous alternative number ",self.ANo

#------------------------------------------------------------------------------		
    def OnGridPageAGridCellLeftClick(self, event):
#------------------------------------------------------------------------------		
#   Detects selected row
#------------------------------------------------------------------------------		
	self.selectedRow = event.GetRow()
	self.ANo = self.selectedRow - 1
        Status.prj.setActiveAlternative(self.ANo)

        print "PanelA - updating panelinfo"
        self.main.panelinfo.update()

        print "PanelA (GridCellLeftClick): row, ANo = ",self.selectedRow,self.ANo	    
        event.Skip()

#------------------------------------------------------------------------------		
    def OnGridPageAGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
        OnGridPageAGridCellLeftClick(event)
        event.Skip()

    def OnGridPageAGridCellRightClick(self, event):
        event.Skip()        

#==============================================================================
#   EVENT HANDLERS BUTTONS TO DESIGN ASSISTANTS
#==============================================================================
    def OnDesignPAButton(self, event):
        event.Skip()

    def OnDesignHXButton(self, event):
        event.Skip()

    def OnDesignHCButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)

    def OnDesignPOButton(self, event):
        event.Skip()

#------------------------------------------------------------------------------		
#   <<< OK Cancel >>>
#------------------------------------------------------------------------------		
    def OnButtonpageAOkButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)
        print "Button exitModuleOK: now I should go back to HC"

    def OnButtonpageACancelButton(self, event):
        #warning: do you want to leave w/o saving ???
        print "Button exitModuleCancel: now I should go back to HC"

    def OnButtonpageABackButton(self, event):
        self.Hide()
        print "Button exitModuleBack: now I should show another window"

    def OnButtonpageAFwdButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)
        print "Button exitModuleFwd: now I should show another window"


