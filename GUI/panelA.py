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
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	    03/04/2008
#	Revised by:    
#                           Tom Sobota              05/04/2008
#
#       Changes to previous version:
#       05/04/08    changed call to popup1 in OnButtonpageHPAddButton
#                   slight change to OK and Cancel buttons, to show the right icons
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
from einstein.GUI.graphics import drawPiePlot
from einstein.modules.modules import Modules
from einstein.GUI.status import Status
from einstein.GUI.addEquipment_popup import AddEquipment #TS 20080405 changed


import einstein.modules.matPanel as Mp
from einstein.modules.interfaces import *


[wxID_PANELA, wxID_PANELABUTTONPAGEABACK, wxID_PANELABUTTONPAGEACANCEL, 
 wxID_PANELABUTTONPAGEAFWD, wxID_PANELABUTTONPAGEAOK, wxID_PANELADESIGNHC, 
 wxID_PANELADESIGNHX, wxID_PANELADESIGNPA, wxID_PANELADESIGNPO, 
 wxID_PANELAGENERATENEW, wxID_PANELAGRIDPAGEA, wxID_PANELAPANELAFIG, 
 wxID_PANELAST1PAGEA, wxID_PANELAST3PAGEA, wxID_PANELASTTITLEPAGEA,
 wxID_PANELAFIG
] = [wx.NewId() for _init_ctrls in range(16)]

# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGA
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem


class PanelA(wx.Panel):

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
	keys = ['A Table']
#        self.modA = ModuleA(keys)  #creates and initialises module
        self.modA = Status.mod.moduleA
        
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
        self.gridPageA.CreateGrid(max(rows,20), cols)

        self.gridPageA.EnableGridLines(True)
        self.gridPageA.SetDefaultRowSize(20)
        self.gridPageA.SetRowLabelSize(30)
        self.gridPageA.SetColSize(0,115)
        self.gridPageA.EnableEditing(False)
        self.gridPageA.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.gridPageA.SetColLabelValue(0, "Alterntative No.")
        self.gridPageA.SetColLabelValue(1, "Name")
        self.gridPageA.SetColLabelValue(2, "Description")
        self.gridPageA.SetColLabelValue(3, "Primary energy consumption")
        self.gridPageA.SetColLabelValue(4, "Total annual energy cost")
        self.gridPageA.SetColLabelValue(5, "---")
        #
        # copy values from dictionary to grid
        #
        for r in range(rows):
            self.gridPageA.SetRowAttr(r, attr)
            for c in range(cols):
                self.gridPageA.SetCellValue(r, c, data[r][c])
                if c == labels_column:
                    self.gridPageA.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.gridPageA.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.gridPageA.SetGridCursor(0, 0)

        self.stTitlePageA.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELA, name='PanelA', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(808, 634), style=0)
        self.SetClientSize(wx.Size(800, 600))

        self.panelAFig = wx.Panel(id=wxID_PANELAFIG, name='panelAFigure',
              parent=self, pos=wx.Point(26, 346), size=wx.Size(382, 220),
              style=wx.TAB_TRAVERSAL)

        self.DesignPA = wx.Button(id=wxID_PANELADESIGNPA,
              label='pinch analysis', name='DesignPA', parent=self,
              pos=wx.Point(592, 360), size=wx.Size(184, 24), style=0)
        self.DesignPA.Bind(wx.EVT_BUTTON, self.OnDesignPAButton,
              id=wxID_PANELADESIGNPA)

        self.gridPageA = wx.grid.Grid(id=wxID_PANELAGRIDPAGEA, name='gridpageA',
              parent=self, pos=wx.Point(24, 56), size=wx.Size(752, 216),
              style=0)
        self.gridPageA.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageAGridCellLeftDclick, id=wxID_PANELAGRIDPAGEA)
        self.gridPageA.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageAGridCellRightClick, id=wxID_PANELAGRIDPAGEA)

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

        self.buttonpageACancel = wx.Button(id=wx.ID_CANCEL,
              label='Cancel', name='buttonpageACancel', parent=self,
              pos=wx.Point(616, 544), size=wx.Size(75, 23), style=0)
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
              pos=wx.Point(24, 280), size=wx.Size(184, 24), style=0)
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

    def OnACalculateButton(self, event):
        ret = self.modA.designAssistant1()
        if (ret == "ManualFinalSelection"):
            print "here I should edit the data base"
        ret = self.modA.designAssistant2()
        if ret == "changed":
            modA.calculateCascade()
            #updatePlots
        
    def OnGenerateNewButton(self, event):
        #show pop-up menu for adding equipment
        #TS20080405 FIXME put dbheatpump table here just for testing! Should be replaced by the
	#right table when it is created
        pu1 =  AddEquipment(self, self.modHP, 'Add Heat Pump equipment','dbheatpump', 0, False)
        if pu1.ShowModal() == wx.ID_OK:
            print 'PanelA AddEquipment accepted. Id='+str(pu1.theId)
#            ret = self.modA.add(AId)
            #update plots
        else:
            print 'Cancelled'

    def OnGridPageAGridCellLeftDclick(self, event):
        print "Grid - left button Dclick: here I should call the Q4H"
        ret = "ok"
        if (ret=="ok"):
            ret = self.modA.calculateCascade()
        #updatePlots

    def OnGridPageAGridCellRightClick(self, event):
        print "Grid - right button click: scroll-up should appear"
        #here a scroll-up should appear with some options: edit, delete,...
        RowNo = 1 #number of the selected boiler should be detected depending on the selected row
        ret = "delete"
        if (ret=="delete"):
            # a pop-up should confirm.
            ret = "ok"
            if (ret == "ok"):
                ret = self.modA.delete(RowNo)
                ret = self.modA.calculateCascade()
        elif (ret == "edit"):
            OnGridPageAGridCellLeftDclick(self,event)
        

    def OnCb1pageACheckbox(self, event):
        self.modA.storeModulePars()

    def OnChoicepageAChoice(self, event):
        self.modA.storeModulePars()

    def OnTc1pageATextEnter(self, event):
        self.modA.storeModulePars()

    def OnTc2pageATextEnter(self, event):
        self.modA.storeModulePars()

    def OnTc3pageATextEnter(self, event):
        self.modA.storeModulePars()

    def OnTc4pageATextEnter(self, event):
        self.modA.storeModulePars()

    def OnTc5pageATextEnter(self, event):
        self.modA.storeModulePars()

    def OnButtonpageAOkButton(self, event):
        saveOption = "save"
        self.modA.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleOK: now I should go back to HC"

    def OnButtonpageACancelButton(self, event):
        #warning: do you want to leave w/o saving ???
        saveOption = "save"
        self.modA.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleCancel: now I should go back to HC"

    def OnButtonpageABackButton(self, event):
        #pop-up: to save or not to save ...
        saveOption = "save"
        self.modA.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleBack: now I should show another window"

    def OnButtonpageAFwdButton(self, event):
        #pop-up: to save or not to save ...
        saveOption = "save"
        self.modA.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleFwd: now I should show another window"

    def OnDesignPAButton(self, event):
        event.Skip()

    def OnDesignHXButton(self, event):
        event.Skip()

    def OnDesignHCButton(self, event):
        event.Skip()

    def OnDesignPOButton(self, event):
        event.Skip()
