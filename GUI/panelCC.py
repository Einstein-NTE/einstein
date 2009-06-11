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
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	    23/04/2008
#	Revised by:    
#                           Hans Schweiger          24/04/2008
#                           Stoyan Danov            18/06/2008
#                           Hans Schweiger          17/07/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes to previous version:
#       23/04/08: HS    copy based on PanelA
#       24/04/08: HS    table for error messages adapted
#       18/06/2008 SD:  change to translatable text _(...)
#       17/07/2008: HS  bug-fix in translatable text (check list button)
#       13/10/2008: SD  change _() to _U()
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
from GUITools import *


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

MAXROWS = 50
COLNO = 5

def _U(text):
    return unicode(_(text),"utf-8")

class PanelCC(wx.Panel):

    def __init__(self, parent, main, id, pos, size, name):
        self._init_ctrls(parent)
	keys = ['CC Table','CC Info']
	self.keys = keys
	self.main = main

        self.mod = Status.mod.moduleCC
        self.checkOK = False

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
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))

        key = keys[0]


        self.grid.CreateGrid(MAXROWS, COLNO)

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(80)
        self.grid.SetColSize(0,100)
        self.grid.SetColSize(1,264)
        self.grid.SetColSize(4,180)
        
        self.grid.EnableEditing(False)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Name"))
        self.grid.SetColLabelValue(1, _U("Description"))
        self.grid.SetColLabelValue(2, _U("Value"))
        self.grid.SetColLabelValue(3, _U("max.Error"))
        self.grid.SetColLabelValue(4, _U("Action to be taken"))
        #
        # copy values from dictionary to grid
        #
        for r in range(MAXROWS):
            self.grid.SetRowAttr(r, attr)
            for c in range(COLNO):
                if c <= labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid.SetGridCursor(0, 0)
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELCC, name='PanelCC', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
        self.SetClientSize(wx.Size(800, 600))

#..............................................................................
# box 1: grid display

        self.box1 = wx.StaticBox(self, -1, _U('Cross checking of data'),
                                 pos = (10,10),size=(780,400))

        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.st1panel = wx.StaticText(id=-1, label=_U('list of data with unsufficient accuracy'),
              name='st1panel', parent=self, pos=wx.Point(20, 30), style=0)

        self.cbSetAccuracy = wx.ComboBox(choices=[_U("quick & dirty"),_U("standard"),_U("detailed")],
              id=wxID_PANELCCCBSETACCURACY, name='cbSetAccuracy', parent=self,
              pos=wx.Point(616, 26), size=wx.Size(162, 32), style=0,
              value=_U("quick and dirty"))
        self.cbSetAccuracy.SetLabel(_U("quick and dirty"))
        self.cbSetAccuracy.Bind(wx.EVT_COMBOBOX, self.OnCbSetAccuracyCombobox,
              id=wxID_PANELCCCBSETACCURACY)

        self.stSetAccuracy = wx.StaticText(id=wxID_PANELCCSTSETACCURACY,
              label=_U('required accuracy'), name='stSetAccuracy', parent=self,
              pos=wx.Point(512, 30), size=wx.Size(87, 13), style=0)

        self.grid = wx.grid.Grid(id=wxID_PANELCCGRID, name='gridpanel',
              parent=self, pos=wx.Point(20, 60), size=wx.Size(760, 340),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPanelGridCellLeftDclick, id=wxID_PANELCCGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPanelGridCellRightClick, id=wxID_PANELCCGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGridPanelGridCellLeftClick)


#..............................................................................
# action buttons

        self.BasicCheck = wx.Button(id=wxID_PANELCCBASICCHECK,
              label='basic check', name='BasicCheck', parent=self,
              pos=wx.Point(24, 420), size=wx.Size(136, 24), style=0)
        self.BasicCheck.Bind(wx.EVT_BUTTON, self.OnBasicCheckButton,
              id=wxID_PANELCCBASICCHECK)

        self.estimateData = wx.Button(id=wxID_PANELCCESTIMATEDATA,
              label=_U('estimate data'), name='estimateData', parent=self,
              pos=wx.Point(176, 420), size=wx.Size(136, 24), style=0)
        self.estimateData.Bind(wx.EVT_BUTTON, self.OnEstimateDataButton,
              id=wxID_PANELCCESTIMATEDATA)

        self.checkList = wx.Button(id=wxID_PANELCCCHECKLIST, label=_U('check list'),
              name='checkList', parent=self, pos=wx.Point(328, 420),
              size=wx.Size(136, 24), style=0)
        self.checkList.Bind(wx.EVT_BUTTON, self.OnCheckListButton,
              id=wxID_PANELCCCHECKLIST)

#..............................................................................
# box 2: display of statistics
        self.box2 = wx.StaticBox(self, -1, _U('Cross check statistics'),
                                 pos = (10,460),size=(780,80))

        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.stStatistics1 = wx.StaticText(id=wxID_PANELCCSTSTATISTICS1,
              label=_U('No. of data checked'), name='stStatistics1', parent=self,
              pos=wx.Point(24, 480), size=wx.Size(98, 13), style=0)

        self.stStatistics2 = wx.StaticText(id=wxID_PANELCCSTSTATISTICS2,
              label=_U('No. of input data fixed'), name='stStatistics2',
              parent=self, pos=wx.Point(24, 500), size=wx.Size(110, 13),
              style=0)

        self.stStatistics3 = wx.StaticText(id=wxID_PANELCCSTSTATISTICS3,
              label=_U('No. of missing data'), name='stStatistics3', parent=self,
              pos=wx.Point(24, 520), size=wx.Size(93, 13), style=0)

        self.stStatistics1Val = wx.StaticText(id=wxID_PANELCCSTSTATISTICS1VAL,
              label='---', name='stStatistics1Val', parent=self,
              pos=wx.Point(176, 480), size=wx.Size(12, 13), style=0)

        self.stStatistics2Val = wx.StaticText(id=wxID_PANELCCSTSTATISTICS2VAL,
              label='---', name='stStatistics2Val', parent=self,
              pos=wx.Point(176, 500), size=wx.Size(12, 13), style=0)

        self.stStatistics3Val = wx.StaticText(id=wxID_PANELCCSTSTATISTICS3VAL,
              label='---', name='stStatistics3Val', parent=self,
              pos=wx.Point(176, 520), size=wx.Size(12, 13), style=0)
#..............................................................................
# default action buttons

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



#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   function activated on each entry into the panel from the tree
#------------------------------------------------------------------------------		
        self.mod.initPanel()        # prepares data for plotting

#..............................................................................
# update of alternatives table

        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))

        attr2 = wx.grid.GridCellAttr()
        attr2.SetTextColour(GRID_LETTER_COLOR_HIGHLIGHT)
        attr2.SetBackgroundColour(GRID_BACKGROUND_COLOR_HIGHLIGHT)
        attr2.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

        rows = 0
        try:
            data = Interfaces.GData[self.keys[0]]
            (rows,cols) = data.shape
            for r in range(rows):
                for c in range(COLNO):
                    self.grid.SetCellValue(r, c, data[r][c])
                    
#HS2008-07-05: WAS AN ATTEMPT TO HIGHLIGHT IMPORTANT DATA
#                if data[r][COLNO]==1:
#                    print "PanelCC: here I should highlight a row"
#                    self.grid.SetRowAttr(r,attr2)
#                else:
#                    self.grid.SetRowAttr(r,attr)

        except:
            pass

        for r in range(rows,MAXROWS):
                for c in range(COLNO):
                    self.grid.SetCellValue(r, c, "")

        try:
            info = Interfaces.GData[self.keys[1]]

            self.stStatistics1Val.SetLabel(str(info[0]))
            self.stStatistics3Val.SetLabel(str(info[2]))

            self.cbSetAccuracy.SetSelection(int(info[3]-1))     
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

        popup =  DialogOK(self,_U("confirm basic check"),\
                          _U("\nTake care: running the check will invalidate existing alternative proposals")+\
                          _U("\nDo You want to continue ?"))
        if popup.ShowModal() == wx.ID_OK:

            Status.prj.copyQuestionnaire()

            nc = self.mod.basicCheck()
            self.display()

            if nc > 0:
                self.checkOK = False
                self.cf = conflictFrame(self)
                self.cf.Show()
            else:
                self.checkOK = True
            
        event.Skip()
        
#------------------------------------------------------------------------------		
    def OnEstimateDataButton(self, event):
#------------------------------------------------------------------------------		
#   Generate new porposal copying from existing alternative
#------------------------------------------------------------------------------		
        if self.checkOK == False:
            showMessage(_U("First You have to run the basic check and eliminate possible conflicts in redundant data"))
            return
            
        popup =  DialogOK(self,_U("confirm data estimation"),\
                          _U("\nTake care: running data estimate will automatically estimate missing data.")+\
                          _U("\nAlternatively you can also manually add estimated data to the questionnaire and rerun basic check")+\
                          _U("\nDo You want to continue ?"))
        if popup.ShowModal() == wx.ID_OK:
            nc = self.mod.basicCheck(estimate=True)
            self.display()

            if nc > 0:
                self.cf = conflictFrame(self)
                self.cf.Show()

        event.Skip()
#------------------------------------------------------------------------------		
    def OnCheckListButton(self, event):
#------------------------------------------------------------------------------		
#   Delete alternative proposal
#------------------------------------------------------------------------------		

        pu2 =  DialogOK(self,_U("confirm check list"),_U("CHECK LIST NOT YET IMPLEMENTED. DO IT YOURSELF AND BE HAPPY"))
        if pu2.ShowModal() == wx.ID_OK:
            pass
#------------------------------------------------------------------------------		
    def OnGridPanelGridCellLeftClick(self, event):
#------------------------------------------------------------------------------		
#   Detects selected row
#------------------------------------------------------------------------------		
	self.selectedRow = event.GetRow()

        self.main.panelinfo.update()

        event.Skip()

#------------------------------------------------------------------------------		
    def OnGridPanelGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
        self.OnGridPanelGridCellLeftClick(event)
        event.Skip()

    def OnGridPanelGridCellRightClick(self, event):
        event.Skip()        

#------------------------------------------------------------------------------		
    def OnCbSetAccuracyCombobox(self, event):
#------------------------------------------------------------------------------		

        accuracy = self.cbSetAccuracy.GetSelection()
        self.mod.setPriorityLevel(accuracy+1)
        self.display()
        event.Skip()


#------------------------------------------------------------------------------		
#   <<< OK Cancel >>>
#------------------------------------------------------------------------------		
    def OnButtonpanelOkButton(self, event):

        if self.checkOK == True:
            popup =  DialogOK(self,_U("accept data"),\
                              _U("Press OK to confirm that the data are correct\n")+\
                              _U("(This will block the questionnaire for further modifications)"))
            if popup.ShowModal() == wx.ID_OK:
                Status.prj.setActiveAlternative(0,checked = True)
                Status.mod.moduleEA.update()
                self.Hide()
                self.main.tree.SelectItem(self.main.qEA4a, select=True)
        else:
            popup =  DialogOK(self,_U("revise data"),\
                              _U("EINSTEIN cannot accept these data. You first have to eliminate inconsistencies"))

    def OnButtonpanelCancelButton(self, event):
        #warning: do you want to leave w/o saving ???
        print "Button exitModuleCancel: now I should go back to HC"

    def OnButtonpanelBackButton(self, event):
        self.Hide()
        print "Button exitModuleBack: now I should show another window"

    def OnButtonpanelFwdButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qEA1, select=True)



