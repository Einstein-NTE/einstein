#Boa:FramePanel:PanelBM3
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
#	Panel BM3
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#       Benchmark module, part 2: specific energy consumption by product
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	    08/04/2008
#       Revised by:         Tom Sobota  28/04/2008
#                           
#
#       Changes to previous version:
#       28/04/2008          created method display
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


[wxID_PANELBM3, wxID_PANELBM3BUTTONPAGEBM3BACK, 
 wxID_PANELBM3BUTTONPAGEBM3CANCEL, wxID_PANELBM3BUTTONPAGEBM3FWD, 
 wxID_PANELBM3BUTTONPAGEBM3OK, wxID_PANELBM3COMBOUNITOPERATION, 
 wxID_PANELBM3COMBOSEARCHCRIT1, wxID_PANELBM3FINDBENCHMARKS, 
 wxID_PANELBM3GRIDPAGE, wxID_PANELBM3FIG, wxID_PANELBM3SEARCHCRIT2, 
 wxID_PANELBM3ST1, wxID_PANELBM3ST1PAGEBM3, wxID_PANELBM3ST2, 
 wxID_PANELBM3ST3PAGEBM3, wxID_PANELBM3STATICTEXT1, wxID_PANELBM3STATICTEXT2, 
 wxID_PANELBM3STUNITOPERATION, wxID_PANELBM3STSEARCHCRIT1, 
 wxID_PANELBM3STSEARCHCRIT2UNIT, wxID_PANELBM3STSEARCHCRIT3, 
 wxID_PANELBM3STTITLE, wxID_PANELBM3TCSEARCHCRIT2A, 
 wxID_PANELBM3TCSEARCHCRIT2B, wxID_PANELBM3TCSEARCHCRIT3A, 
 wxID_PANELBM3TCSEARCHCRIT3B, 
] = [wx.NewId() for _init_ctrls in range(26)]

# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGA
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem


class PanelBM3(wx.Panel):

    def __init__(self, parent):
        self._init_ctrls(parent)
	keys = ['BM3 Table']
        self.mod = Status.mod.moduleBM
        
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

        dummy = Mp.MatPanel(self.panelFig,
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
        self.gridPage.CreateGrid(max(rows,20), cols)

        self.gridPage.EnableGridLines(True)
        self.gridPage.SetDefaultRowSize(20)
        self.gridPage.SetRowLabelSize(30)
        self.gridPage.SetColSize(0,115)
        self.gridPage.EnableEditing(False)
        self.gridPage.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.gridPage.SetColLabelValue(0, "Source")
        self.gridPage.SetColLabelValue(1, "Reference")
        self.gridPage.SetColLabelValue(2, "Validity")
        self.gridPage.SetColLabelValue(3, "Electricity (min)")
        self.gridPage.SetColLabelValue(4, "Electricity (target)")
        self.gridPage.SetColLabelValue(5, "Electricity (max)")
        self.gridPage.SetColLabelValue(6, "Fuels (min)")
        self.gridPage.SetColLabelValue(7, "Fuels (target)")
        self.gridPage.SetColLabelValue(8, "Fuels (max)")
        self.gridPage.SetColLabelValue(9, "Primary energy (min)")
        self.gridPage.SetColLabelValue(10, "Primary energy (target)")
        self.gridPage.SetColLabelValue(11, "Primary energy (max)")
     #
        # copy values from dictionary to grid
        #
        for r in range(rows):
            self.gridPage.SetRowAttr(r, attr)
            for c in range(cols):
                self.gridPage.SetCellValue(r, c, data[r][c])
                if c == labels_column:
                    self.gridPage.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.gridPage.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.gridPage.SetGridCursor(0, 0)

        self.stTitle.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELBM3, name='PanelBM3', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(808, 634), style=0)
        self.SetClientSize(wx.Size(800, 600))

        self.panelFig = wx.Panel(id=wxID_PANELBM3FIG, name='panelBM3Figure',
              parent=self, pos=wx.Point(26, 346), size=wx.Size(382, 220),
              style=wx.TAB_TRAVERSAL)

        self.gridPage = wx.grid.Grid(id=wxID_PANELBM3GRIDPAGE,
              name='gridpageBM3', parent=self, pos=wx.Point(24, 56),
              size=wx.Size(752, 216), style=0)
        self.gridPage.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageGridCellLeftDclick, id=wxID_PANELBM3GRIDPAGE)
        self.gridPage.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageGridCellRightClick, id=wxID_PANELBM3GRIDPAGE)

        self.st1pageBM3 = wx.StaticText(id=-1, label='Search criteria',
              name='st1pageBM3', parent=self, pos=wx.Point(448, 312), style=0)

        self.stTitle = wx.StaticText(id=wxID_PANELBM3STTITLE,
              label='Benchmarks 2: specific energy consumption by product',
              name='stTitle', parent=self, pos=wx.Point(24, 16), style=0)
        self.stTitle.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.buttonpageBM3Ok = wx.Button(id=wx.ID_OK, label='OK',
              name='buttonpageBM3Ok', parent=self, pos=wx.Point(528, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageBM3Ok.Bind(wx.EVT_BUTTON, self.OnButtonpageBM3OkButton,
              id=wx.ID_OK)

        self.buttonpageBM3Cancel = wx.Button(id=wx.ID_CANCEL, label='Cancel',
              name='buttonpageBM3Cancel', parent=self, pos=wx.Point(616, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageBM3Cancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpageBM3CancelButton, id=wx.ID_CANCEL)

        self.buttonpageBM3Fwd = wx.Button(id=wxID_PANELBM3BUTTONPAGEBM3FWD,
              label='>>>', name='buttonpageBM3Fwd', parent=self,
              pos=wx.Point(704, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageBM3Fwd.Bind(wx.EVT_BUTTON, self.OnButtonpageBM3FwdButton,
              id=wxID_PANELBM3BUTTONPAGEBM3FWD)

        self.buttonpageBM3Back = wx.Button(id=wxID_PANELBM3BUTTONPAGEBM3BACK,
              label='<<<', name='buttonpageBM3Back', parent=self,
              pos=wx.Point(440, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageBM3Back.Bind(wx.EVT_BUTTON,
              self.OnButtonpageBM3BackButton,
              id=wxID_PANELBM3BUTTONPAGEBM3BACK)

        self.FindBenchmarks = wx.Button(id=wxID_PANELBM3FINDBENCHMARKS,
              label='find benchmarks', name='FindBenchmarks', parent=self,
              pos=wx.Point(592, 280), size=wx.Size(184, 24), style=0)
        self.FindBenchmarks.Bind(wx.EVT_BUTTON, self.OnGenerateNewButton,
              id=wxID_PANELBM3FINDBENCHMARKS)

        self.st3pageBM3 = wx.StaticText(id=wxID_PANELBM3ST3PAGEBM3,
              label='Comparison benchmark data', name='st3pageBM3', parent=self,
              pos=wx.Point(24, 320), size=wx.Size(137, 13), style=0)

        self.staticText1 = wx.StaticText(id=wxID_PANELBM3STATICTEXT1,
              label='Benchmarks found:', name='staticText1', parent=self,
              pos=wx.Point(24, 40), style=0)

        self.stSearchCrit1 = wx.StaticText(id=wxID_PANELBM3STSEARCHCRIT1,
              label='NACE Code range (digits)', name='stSearchCrit1',
              parent=self, pos=wx.Point(448, 352), size=wx.Size(123, 13),
              style=0)

        self.SearchCrit2 = wx.StaticText(id=wxID_PANELBM3SEARCHCRIT2,
              label='process product volume', name='SearchCrit2', parent=self,
              pos=wx.Point(448, 416), size=wx.Size(89, 13), style=0)

        self.stSearchCrit3 = wx.StaticText(id=wxID_PANELBM3STSEARCHCRIT3,
              label='Year of data', name='stSearchCrit3', parent=self,
              pos=wx.Point(448, 440), size=wx.Size(61, 13), style=0)

        self.comboSearchCrit1 = wx.ComboBox(choices=["15500", "1550 _",
              "155 _ _", "15 _ _ _"], id=wxID_PANELBM3COMBOSEARCHCRIT1,
              name='comboSearchCrit1', parent=self, pos=wx.Point(640, 344),
              size=wx.Size(136, 21), style=0, value='1550 _')
        self.comboSearchCrit1.SetLabel('1550 _')

        self.tcSearchCrit2b = wx.TextCtrl(id=wxID_PANELBM3TCSEARCHCRIT2B,
              name='tcSearchCrit2b', parent=self, pos=wx.Point(712, 408),
              size=wx.Size(64, 24), style=1000, value='1000')

        self.tcSearchCrit2a = wx.TextCtrl(id=wxID_PANELBM3TCSEARCHCRIT2A,
              name='tcSearchCrit2a', parent=self, pos=wx.Point(640, 408),
              size=wx.Size(64, 24), style=0, value='0')

        self.st1 = wx.StaticText(id=wxID_PANELBM3ST1, label='max.', name='st1',
              parent=self, pos=wx.Point(728, 384), size=wx.Size(25, 13),
              style=0)

        self.st2 = wx.StaticText(id=wxID_PANELBM3ST2, label='min.', name='st2',
              parent=self, pos=wx.Point(664, 384), size=wx.Size(21, 13),
              style=0)

        self.tcSearchCrit3a = wx.TextCtrl(id=wxID_PANELBM3TCSEARCHCRIT3A,
              name='tcSearchCrit3a', parent=self, pos=wx.Point(640, 440),
              size=wx.Size(64, 24), style=0, value='2000')

        self.tcSearchCrit3b = wx.TextCtrl(id=wxID_PANELBM3TCSEARCHCRIT3B,
              name='tcSearchCrit3b', parent=self, pos=wx.Point(712, 440),
              size=wx.Size(64, 24), style=0, value='2008')

        self.stSearchCrit2Unit = wx.StaticText(id=wxID_PANELBM3STSEARCHCRIT2UNIT,
              label='t/year', name='stSearchCrit2Unit', parent=self,
              pos=wx.Point(592, 416), size=wx.Size(30, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELBM3STATICTEXT2,
              label='staticText2', name='staticText2', parent=self.panelFig,
              pos=wx.Point(400, -320), size=wx.Size(55, 13), style=0)

        self.stUnitOperation = wx.StaticText(id=wxID_PANELBM3STUNITOPERATION,
              label='UnitOperation:', name='stUnitOperation', parent=self, pos=wx.Point(512,
              16), size=wx.Size(42, 13), style=0)

        self.comboUnitOperation = wx.ComboBox(choices=["drying", "pasteurisation", "fermentation"],
              id=wxID_PANELBM3COMBOUNITOPERATION, name='comboUnitOperation', parent=self,
              pos=wx.Point(568, 8), size=wx.Size(210, 21), style=0,
              value='drying')
        self.comboUnitOperation.SetLabel('drying')


    def display(self):
        self.panelFig.draw()
        self.Show()

        
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
            print 'PanelBM3 AddEquipment accepted. Id='+str(pu1.theId)
#            ret = self.modA.add(AId)
            #update plots
        else:
            print 'Cancelled'

    def OnGridPageGridCellLeftDclick(self, event):
        print "PanelBM3: Grid - left button Dclick"

    def OnGridPageGridCellRightClick(self, event):
        print "PanelBM3: Grid - right button click: scroll-up should appear"
        
    def OnButtonpageBM3OkButton(self, event):
        saveOption = "save"
        self.mod.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleOK: now I should go back to HC"

    def OnButtonpageBM3CancelButton(self, event):
        #warning: do you want to leave w/o saving ???
        saveOption = "save"
        self.mod.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleCancel: now I should go back to HC"

    def OnButtonpageBM3BackButton(self, event):
        #pop-up: to save or not to save ...
        saveOption = "save"
        self.modA.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleBack: now I should show another window"

    def OnButtonpageBM3FwdButton(self, event):
        #pop-up: to save or not to save ...
        saveOption = "save"
        self.mod.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleFwd: now I should show another window"
