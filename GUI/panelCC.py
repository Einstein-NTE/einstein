#Boa:FramePanel:PanelCC
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
#	PanelCC
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Panel for handling of consistency checking
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	    23/04/2008
#	Revised by:    
#                           Hans Schweiger          24/04/2008
#
#       Changes to previous version:
#       23/04/08: HS    copy based on PanelA
#       24/04/08: HS    table for error messages adapted
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
from einstein.GUI.status import Status


from einstein.modules.interfaces import *
from einstein.GUI.dialogOK import *
from einstein.GUI.conflictFrame import *


[wxID_PANELCC, wxID_PANELCCBASICCHECK, wxID_PANELCCBUTTONPANELBACK, 
 wxID_PANELCCBUTTONPANELCANCEL, wxID_PANELCCBUTTONPANELFWD, 
 wxID_PANELCCBUTTONPANELOK, wxID_PANELCCCBSETACCURACY, wxID_PANELCCCHECKLIST, 
 wxID_PANELCCESTIMATEDATA, wxID_PANELCCGRID, wxID_PANELCCST1PANEL, 
 wxID_PANELCCST3PANEL, wxID_PANELCCSTSETACCURACY, wxID_PANELCCSTSTATISTICS1, 
 wxID_PANELCCSTSTATISTICS1VAL, wxID_PANELCCSTSTATISTICS2, 
 wxID_PANELCCSTSTATISTICS2VAL, wxID_PANELCCSTSTATISTICS3, 
 wxID_PANELCCSTSTATISTICS3VAL, wxID_PANELCCSTTITLEPANEL, 
] = [wx.NewId() for _init_ctrls in range(20)]

# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGA
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem

MAXROWS = 50
MAXCOLS = 5

class PanelCC(wx.Panel):

    def __init__(self, parent, main, id, pos, size, style, name):
        self._init_ctrls(parent)
	keys = ['CC Table','CC Info']
	self.keys = keys
	self.main = main

        self.mod = Status.mod.moduleCC

        self.shortName = "new alternative"
        self.description = "describe shortly the main differential features of the new alternative"

        self.ANo = Status.ANo
        labels_column = 1

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


        self.grid.CreateGrid(MAXROWS, MAXCOLS)

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(80)
        self.grid.SetColSize(0,120)
        self.grid.SetColSize(1,240)
        self.grid.SetColSize(4,180)
        
        self.grid.EnableEditing(False)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, "Name")
        self.grid.SetColLabelValue(1, "Description")
        self.grid.SetColLabelValue(2, "Value")
        self.grid.SetColLabelValue(3, "Accuracy")
        self.grid.SetColLabelValue(4, "Action to be taken")
        #
        # copy values from dictionary to grid
        #
        for r in range(MAXROWS):
            self.grid.SetRowAttr(r, attr)
            for c in range(MAXCOLS):
                if c == labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid.SetGridCursor(0, 0)

        self.stTitlePanel.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELCC, name='PanelCC', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(808, 634), style=0)
        self.SetClientSize(wx.Size(800, 600))

        self.grid = wx.grid.Grid(id=wxID_PANELCCGRID, name='gridpanel',
              parent=self, pos=wx.Point(24, 56), size=wx.Size(752, 296),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPanelGridCellLeftDclick, id=wxID_PANELCCGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPanelGridCellRightClick, id=wxID_PANELCCGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGridPanelGridCellLeftClick)

        self.st1panel = wx.StaticText(id=-1, label='list of data to be checked',
              name='st1panel', parent=self, pos=wx.Point(24, 40), style=0)

        self.stTitlePanel = wx.StaticText(id=wxID_PANELCCSTTITLEPANEL,
              label='Cross checking of data', name='stTitlePanel', parent=self,
              pos=wx.Point(24, 16), style=0)
        self.stTitlePanel.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.buttonpanelOk = wx.Button(id=wx.ID_OK, label='OK',
              name='buttonpanelOk', parent=self, pos=wx.Point(528, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpanelOk.Bind(wx.EVT_BUTTON, self.OnButtonpanelOkButton,
              id=wx.ID_OK)

        self.buttonpanelCancel = wx.Button(id=wx.ID_CANCEL, label='Cancel',
              name='buttonpanelCancel', parent=self, pos=wx.Point(616, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpanelCancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpanelCancelButton, id=wx.ID_CANCEL)

        self.buttonpanelFwd = wx.Button(id=wxID_PANELCCBUTTONPANELFWD,
              label='>>>', name='buttonpanelFwd', parent=self, pos=wx.Point(704,
              544), size=wx.Size(75, 23), style=0)
        self.buttonpanelFwd.Bind(wx.EVT_BUTTON, self.OnButtonpanelFwdButton,
              id=wxID_PANELCCBUTTONPANELFWD)

        self.buttonpanelBack = wx.Button(id=wxID_PANELCCBUTTONPANELBACK,
              label='<<<', name='buttonpanelBack', parent=self,
              pos=wx.Point(440, 544), size=wx.Size(75, 23), style=0)
        self.buttonpanelBack.Bind(wx.EVT_BUTTON, self.OnButtonpanelBackButton,
              id=wxID_PANELCCBUTTONPANELBACK)

        self.BasicCheck = wx.Button(id=wxID_PANELCCBASICCHECK,
              label='basic check', name='BasicCheck', parent=self,
              pos=wx.Point(24, 360), size=wx.Size(136, 24), style=0)
        self.BasicCheck.Bind(wx.EVT_BUTTON, self.OnBasicCheckButton,
              id=wxID_PANELCCBASICCHECK)

        self.st3panel = wx.StaticText(id=wxID_PANELCCST3PANEL,
              label='Cross check statistics', name='st3panel', parent=self,
              pos=wx.Point(24, 392), size=wx.Size(122, 13), style=0)
        self.st3panel.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.estimateData = wx.Button(id=wxID_PANELCCESTIMATEDATA,
              label='estimate data', name='estimateData', parent=self,
              pos=wx.Point(176, 360), size=wx.Size(136, 24), style=0)
        self.estimateData.Bind(wx.EVT_BUTTON, self.OnEstimateDataButton,
              id=wxID_PANELCCESTIMATEDATA)

        self.checkList = wx.Button(id=wxID_PANELCCCHECKLIST, label='check list',
              name='checkList', parent=self, pos=wx.Point(328, 360),
              size=wx.Size(136, 24), style=0)
        self.checkList.Bind(wx.EVT_BUTTON, self.OnCheckListButton,
              id=wxID_PANELCCCHECKLIST)

        self.stStatistics1 = wx.StaticText(id=wxID_PANELCCSTSTATISTICS1,
              label='No. of data checked', name='stStatistics1', parent=self,
              pos=wx.Point(24, 424), size=wx.Size(98, 13), style=0)

        self.stStatistics2 = wx.StaticText(id=wxID_PANELCCSTSTATISTICS2,
              label='No. of input data fixed', name='stStatistics2',
              parent=self, pos=wx.Point(24, 456), size=wx.Size(110, 13),
              style=0)

        self.stStatistics3 = wx.StaticText(id=wxID_PANELCCSTSTATISTICS3,
              label='No. of missing data', name='stStatistics3', parent=self,
              pos=wx.Point(24, 488), size=wx.Size(93, 13), style=0)

        self.stStatistics1Val = wx.StaticText(id=wxID_PANELCCSTSTATISTICS1VAL,
              label='---', name='stStatistics1Val', parent=self,
              pos=wx.Point(176, 424), size=wx.Size(12, 13), style=0)

        self.stStatistics2Val = wx.StaticText(id=wxID_PANELCCSTSTATISTICS2VAL,
              label='---', name='stStatistics2Val', parent=self,
              pos=wx.Point(176, 456), size=wx.Size(12, 13), style=0)

        self.stStatistics3Val = wx.StaticText(id=wxID_PANELCCSTSTATISTICS3VAL,
              label='---', name='stStatistics3Val', parent=self,
              pos=wx.Point(176, 488), size=wx.Size(12, 13), style=0)

        self.cbSetAccuracy = wx.ComboBox(choices=["quick and dirty", "final"],
              id=wxID_PANELCCCBSETACCURACY, name='cbSetAccuracy', parent=self,
              pos=wx.Point(616, 8), size=wx.Size(162, 21), style=0,
              value='"quick and dirty"')
        self.cbSetAccuracy.SetLabel('"quick and dirty"')
        self.cbSetAccuracy.Bind(wx.EVT_COMBOBOX, self.OnCbSetAccuracyCombobox,
              id=wxID_PANELCCCBSETACCURACY)

        self.stSetAccuracy = wx.StaticText(id=wxID_PANELCCSTSETACCURACY,
              label='required accuracy', name='stSetAccuracy', parent=self,
              pos=wx.Point(512, 16), size=wx.Size(87, 13), style=0)

    def display(self):
#------------------------------------------------------------------------------		
#   function activated on each entry into the panel from the tree
#------------------------------------------------------------------------------		
        self.mod.initPanel()        # prepares data for plotting

#..............................................................................
# update of alternatives table

        try:
            data = Interfaces.GData[self.keys[0]]
            print "data = ",data
            (rows,cols) = data.shape
            print rows,cols
            for r in range(rows):
                for c in range(cols):
                    self.grid.SetCellValue(r, c, data[r][c])

    #XXX Here better would be updating the grid and showing less rows ... ????
            for r in range(rows,MAXROWS):
                for c in range(cols):
                    self.grid.SetCellValue(r, c, "")

            info = Interfaces.GData[self.keys[1]]

            self.stStatistics1Val.SetLabel(str(info[0]))
            self.stStatistics3Val.SetLabel(str(info[2]))
            
        except:
            pass

        self.Show()
        self.main.panelinfo.update()
       
#------------------------------------------------------------------------------		

#==============================================================================
#   EVENT HANDLERS
#==============================================================================

#------------------------------------------------------------------------------		
    def OnBasicCheckButton(self, event):
#------------------------------------------------------------------------------		
#   Generate new alterantive proposal
#------------------------------------------------------------------------------		

        nc = self.mod.basicCheck(matrixCheck=False)
        self.display()

        if nc > 0:
            self.pu1 = conflictFrame(self)
            self.pu1.Show()
        
#------------------------------------------------------------------------------		
    def OnEstimateDataButton(self, event):
#------------------------------------------------------------------------------		
#   Generate new porposal copying from existing alternative
#------------------------------------------------------------------------------		
        self.shortName = self.grid.GetCellValue(self.selectedRow,1)+"(mod.)"
        self.description = self.grid.GetCellValue(self.selectedRow,2)+"(modified alternative based on "+self.grid.GetCellValue(self.selectedRow,1)+")"

        pu1 =  DialogA(self)
        if pu1.ShowModal() == wx.ID_OK:
            print "PanelCC - OK",self.shortName,self.description
            print "PanelCC (BasicCheck-Button): calling function createNewAlternative"

            self.display()

        elif pu1.ShowModal() == wx.ID_Cancel:
            print "PanelCC - Cancel"
        else:
            print "PanelCC - ???"

#------------------------------------------------------------------------------		
    def OnCheckListButton(self, event):
#------------------------------------------------------------------------------		
#   Delete alternative proposal
#------------------------------------------------------------------------------		

        pu2 =  DialogOK(self,"delete alternative","do you really want to delete this alternative ?")
        if pu2.ShowModal() == wx.ID_OK:
            if self.ANo > 0:
                self.display()
            elif self.ANo in [-1,0]:
                print "PanelCC (DeleteButton): cannot delete alternative ",self.ANo
            else:
                print "PanelCC (DeleteButton): erroneous alternative number ",self.ANo

#------------------------------------------------------------------------------		
    def OnGridPanelGridCellLeftClick(self, event):
#------------------------------------------------------------------------------		
#   Detects selected row
#------------------------------------------------------------------------------		
	self.selectedRow = event.GetRow()

        print "PanelCC - updating panelinfo"
        self.main.panelinfo.update()

        event.Skip()

#------------------------------------------------------------------------------		
    def OnGridPanelGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
        OnGridPanelGridCellLeftClick(event)
        event.Skip()

    def OnGridPanelGridCellRightClick(self, event):
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
    def OnButtonpanelOkButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)
        print "Button exitModuleOK: now I should go back to HC"

    def OnButtonpanelCancelButton(self, event):
        #warning: do you want to leave w/o saving ???
        print "Button exitModuleCancel: now I should go back to HC"

    def OnButtonpanelBackButton(self, event):
        self.Hide()
        print "Button exitModuleBack: now I should show another window"

    def OnButtonpanelFwdButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)
        print "Button exitModuleFwd: now I should show another window"

    def OnCbSetAccuracyCombobox(self, event):
        event.Skip()


