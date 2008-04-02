#Boa:FramePanel:PanelBB
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
#	Panel for BB design assistant
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Hans Schweiger	    February 2008
#	Last revised by:    Hans Schweiger          24/03/2008
#
#       Changes to previous version:
#       - structure of plots identical to that of HP
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
from einstein.modules.boiler.ModuleBB import *
from einstein.GUI.status import Status
from einstein.GUI.panelBB_PopUp1 import BBPopUp1

import einstein.modules.matPanel as Mp
from einstein.modules.interfaces import *


[wxID_PANELBB, wxID_PANELBBBBCALCULATE, wxID_PANELBBBUTTONPAGEBBADD, 
 wxID_PANELBBBUTTONPAGEBBBACK, wxID_PANELBBBUTTONPAGEBBCANCEL, 
 wxID_PANELBBBUTTONPAGEBBFWD, wxID_PANELBBBUTTONPAGEBBOK, 
 wxID_PANELBBCB1PAGEBB, wxID_PANELBBCHOICEPAGEBB, wxID_PANELBBGRIDPAGEBB, 
 wxID_PANELBBFIG, wxID_PANELBBST10PAGEBB, wxID_PANELBBST11PAGEBB, 
 wxID_PANELBBST12PAGEBB, wxID_PANELBBST1PAGEBB, wxID_PANELBBST2PAGEBB, 
 wxID_PANELBBST3PAGEBB, wxID_PANELBBST4PAGEBB, wxID_PANELBBST5PAGEBB, 
 wxID_PANELBBST6PAGEBB, wxID_PANELBBST7PAGEBB, wxID_PANELBBST8PAGEBB, 
 wxID_PANELBBST9PAGEBB, wxID_PANELBBSTATICTEXT1, wxID_PANELBBTC1PAGEBB, 
 wxID_PANELBBTC2PAGEBB, wxID_PANELBBTC3PAGEBB, wxID_PANELBBTC4PAGEBB, 
 wxID_PANELBBTC5PAGEBB, wxID_PANELBBTC6PAGEBB, wxID_PANELBBTC7PAGEBB, 
] = [wx.NewId() for _init_ctrls in range(31)]
#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem


class PanelBB(wx.Panel):

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
	keys = ['BB Plot']
        self.modBB = ModuleBB(keys)  #creates and initialises module
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

        dummy = Mp.MatPanel(self.panelBBFig,
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
        self.gridPageBB.CreateGrid(max(rows,20), cols)

        self.gridPageBB.EnableGridLines(True)
        self.gridPageBB.SetDefaultRowSize(20)
        self.gridPageBB.SetRowLabelSize(30)
        self.gridPageBB.SetColSize(0,115)
        self.gridPageBB.EnableEditing(False)
        self.gridPageBB.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.gridPageBB.SetColLabelValue(0, "Short name")
        self.gridPageBB.SetColLabelValue(1, "Year")
        self.gridPageBB.SetColLabelValue(2, "Type")
        self.gridPageBB.SetColLabelValue(3, "Operating\nhours")
        self.gridPageBB.SetColLabelValue(4, "Power")
        self.gridPageBB.SetColLabelValue(5, "Temperature")
        #
        # copy values from dictionary to grid
        #
        for r in range(rows):
            self.gridPageBB.SetRowAttr(r, attr)
            for c in range(cols):
                self.gridPageBB.SetCellValue(r, c, data[r][c])
                if c == labels_column:
                    self.gridPageBB.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.gridPageBB.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.gridPageBB.SetGridCursor(0, 0)

        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELBB, name='PanelBB', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
        self.SetClientSize(wx.Size(800, 600))

#------------------------------------------------------------------------------		
#       Displays of status
#------------------------------------------------------------------------------		

#..............................................................................
# Figure to be plotted


        self.panelBBFig = wx.Panel(id=wxID_PANELBBFIG, name='panelBBFigure', parent=self,
              pos=wx.Point(450, 66), size=wx.Size(316, 220),
              style=wx.TAB_TRAVERSAL)

#..............................................................................

        self.BBCalculate = wx.Button(id=wxID_PANELBBBBCALCULATE,
              label='run design assistant', name='BB_Calculate', parent=self,
              pos=wx.Point(232, 224), size=wx.Size(184, 24), style=0)
        self.BBCalculate.Bind(wx.EVT_BUTTON, self.OnBBCalculateButton,
              id=wxID_PANELBBBBCALCULATE)

        self.gridPageBB = wx.grid.Grid(id=wxID_PANELBBGRIDPAGEBB,
              name='gridpageBB', parent=self, pos=wx.Point(40, 48),
              size=wx.Size(376, 168), style=0)
        self.gridPageBB.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageBBGridCellLeftDclick, id=wxID_PANELBBGRIDPAGEBB)
        self.gridPageBB.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageBBGridCellRightClick, id=wxID_PANELBBGRIDPAGEBB)

        self.st1pageBB = wx.StaticText(id=-1,
              label='Existing Boilers and burners in the HC system',
              name='st1pageBB', parent=self, pos=wx.Point(40, 32), style=0)

        self.st2pageBB = wx.StaticText(id=-1, label='Design assistant options:',
              name='st2pageBB', parent=self, pos=wx.Point(40, 272), style=0)
        self.st2pageBB.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.st3pageBB = wx.StaticText(id=-1,
              label='Maintain existing equipment ?', name='st3pageBB',
              parent=self, pos=wx.Point(40, 304), style=0)

        self.cb1pageBB = wx.CheckBox(id=wxID_PANELBBCB1PAGEBB, label='',
              name='cb1pageBB', parent=self, pos=wx.Point(288, 308),
              size=wx.Size(24, 13), style=0)
        self.cb1pageBB.SetValue(False)
        self.cb1pageBB.Bind(wx.EVT_CHECKBOX, self.OnCb1pageBBCheckbox,
              id=wxID_PANELBBCB1PAGEBB)

        self.st4pageBB = wx.StaticText(id=-1, label='Type of boiler/burner',
              name='st4pageBB', parent=self, pos=wx.Point(40, 344), style=0)

        self.choicepageBB = wx.Choice(choices=["steam boiler",
              "hot water (condensing)", "hot water (standard)"],
              id=wxID_PANELBBCHOICEPAGEBB, name='choicepageBB', parent=self,
              pos=wx.Point(288, 336), size=wx.Size(130, 21), style=0)
        self.choicepageBB.Bind(wx.EVT_CHOICE, self.OnChoicepageBBChoice,
              id=wxID_PANELBBCHOICEPAGEBB)

        self.st5pageBB = wx.StaticText(id=-1,
              label='Minimum desired annual operation hours, h',
              name='st5pageBB', parent=self, pos=wx.Point(40, 384), style=0)

        self.st6pageBB = wx.StaticText(id=-1,
              label='Maximum desired temperature lift, \xbaC', name='st6pageBB',
              parent=self, pos=wx.Point(40, 424), style=0)

        self.st7pageBB = wx.StaticText(id=-1,
              label='Maximum desired condensing temperature, \xbaC',
              name='st7pageBB', parent=self, pos=wx.Point(40, 464), style=0)

        self.st8pageBB = wx.StaticText(id=-1,
              label='Minimum desired evaporating temperature, \xbaC',
              name='st8pageBB', parent=self, pos=wx.Point(40, 504), style=0)

        self.st9pageBB = wx.StaticText(id=-1, label='Only for absorption type:',
              name='st9pageBB', parent=self, pos=wx.Point(40, 536), style=0)

        self.st10pageBB = wx.StaticText(id=-1,
              label='Inlet temperature of heating fluid in generator, \xbaC',
              name='st10pageBB', parent=self, pos=wx.Point(40, 552), style=0)

        self.tc1pageBB = wx.TextCtrl(id=wxID_PANELBBTC1PAGEBB, name='tc1pageBB',
              parent=self, pos=wx.Point(288, 376), size=wx.Size(128, 21),
              style=0, value='')
        self.tc1pageBB.Bind(wx.EVT_TEXT_ENTER, self.OnTc1pageBBTextEnter,
              id=wxID_PANELBBTC1PAGEBB)

        self.tc2pageBB = wx.TextCtrl(id=-1, name='tc2pageBB', parent=self,
              pos=wx.Point(288, 416), size=wx.Size(128, 21), style=0, value='')
        self.tc2pageBB.Bind(wx.EVT_TEXT_ENTER, self.OnTc2pageBBTextEnter,
              id=wxID_PANELBBTC2PAGEBB)

        self.tc3pageBB = wx.TextCtrl(id=-1, name='tc3pageBB', parent=self,
              pos=wx.Point(288, 456), size=wx.Size(128, 21), style=0, value='')
        self.tc3pageBB.Bind(wx.EVT_TEXT_ENTER, self.OnTc3pageBBTextEnter,
              id=wxID_PANELBBTC3PAGEBB)

        self.tc4pageBB = wx.TextCtrl(id=wxID_PANELBBTC4PAGEBB, name='tc4pageBB',
              parent=self, pos=wx.Point(288, 496), size=wx.Size(128, 21),
              style=0, value='')
        self.tc4pageBB.Bind(wx.EVT_TEXT_ENTER, self.OnTc4pageBBTextEnter,
              id=wxID_PANELBBTC4PAGEBB)

        self.tc5pageBB = wx.TextCtrl(id=wxID_PANELBBTC5PAGEBB, name='tc5pageBB',
              parent=self, pos=wx.Point(288, 544), size=wx.Size(128, 21),
              style=0, value='')
        self.tc5pageBB.Bind(wx.EVT_TEXT_ENTER, self.OnTc5pageBBTextEnter,
              id=wxID_PANELBBTC5PAGEBB)

        self.tc6pageBB = wx.TextCtrl(id=-1, name='tc6pageBB', parent=self,
              pos=wx.Point(640, 416), size=wx.Size(128, 21), style=0,
              value='??')

        self.tc7pageBB = wx.TextCtrl(id=-1, name='tc7pageBB', parent=self,
              pos=wx.Point(640, 456), size=wx.Size(128, 21), style=0,
              value='??')

        self.st11pageBB = wx.StaticText(id=-1, label='Pinch temperature \xb0C',
              name='st11pageBB', parent=self, pos=wx.Point(440, 424), style=0)

        self.st12pageBB = wx.StaticText(id=-1, label='Temperature gap \xb0K',
              name='st12pageBB', parent=self, pos=wx.Point(440, 464), style=0)

        self.buttonpageBBOk = wx.Button(id=wxID_PANELBBBUTTONPAGEBBOK,
              label='ok', name='buttonpageBBOk', parent=self, pos=wx.Point(528,
              544), size=wx.Size(75, 23), style=0)
        self.buttonpageBBOk.Bind(wx.EVT_BUTTON, self.OnButtonpageBBOkButton,
              id=wxID_PANELBBBUTTONPAGEBBOK)

        self.buttonpageBBCancel = wx.Button(id=wxID_PANELBBBUTTONPAGEBBCANCEL,
              label='cancel', name='buttonpageBBCancel', parent=self,
              pos=wx.Point(616, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageBBCancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpageBBCancelButton,
              id=wxID_PANELBBBUTTONPAGEBBCANCEL)

        self.buttonpageBBFwd = wx.Button(id=wxID_PANELBBBUTTONPAGEBBFWD,
              label='>>>', name='buttonpageBBFwd', parent=self,
              pos=wx.Point(704, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageBBFwd.Bind(wx.EVT_BUTTON, self.OnButtonpageBBFwdButton,
              id=wxID_PANELBBBUTTONPAGEBBFWD)

        self.buttonpageBBBack = wx.Button(id=wxID_PANELBBBUTTONPAGEBBBACK,
              label='<<<', name='buttonpageBBBack', parent=self,
              pos=wx.Point(440, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageBBBack.Bind(wx.EVT_BUTTON, self.OnButtonpageBBBackButton,
              id=wxID_PANELBBBUTTONPAGEBBBACK)

        self.buttonpageBBAdd = wx.Button(id=wxID_PANELBBBUTTONPAGEBBADD,
              label='add boiler / burner', name='buttonpageBBAdd', parent=self,
              pos=wx.Point(32, 224), size=wx.Size(184, 24), style=0)
        self.buttonpageBBAdd.Bind(wx.EVT_BUTTON, self.OnButtonpageBBAddButton,
              id=wxID_PANELBBBUTTONPAGEBBADD)

        self.staticText1 = wx.StaticText(id=wxID_PANELBBSTATICTEXT1,
              label=u'Heat demand and availability with and without BB',
              name='staticText1', parent=self, pos=wx.Point(424, 32),
              size=wx.Size(352, 17), style=0)


#==============================================================================
#   Event handlers
#==============================================================================

    def OnBBCalculateButton(self, event):
        ret = self.modBB.designAssistant1()
        if (ret == "ManualFinalSelection"):
            print "here I should edit the data base"
        ret = self.modBB.designAssistant2()
        if ret == "changed":
            modBB.calculateCascade()
            #updatePlots
        
    def OnButtonpageBBAddButton(self, event):
        #show pop-up menu 1: add from where ???
        pu1 = BBPopUp1(self)
        if pu1.ShowModal() == wx.ID_OK:
            print 'Accepted'
            ret = self.modBB.add(BBId)
            #update plots
        else:
            print 'Cancelled'

    def OnGridPageBBGridCellLeftDclick(self, event):
        print "Grid - left button Dclick: here I should call the Q4H"
        ret = "ok"
        if (ret=="ok"):
            ret = self.modBB.calculateCascade()
        #updatePlots

    def OnGridPageBBGridCellRightClick(self, event):
        print "Grid - right button click: scroll-up should appear"
        #here a scroll-up should appear with some options: edit, delete,...
        RowNo = 1 #number of the selected boiler should be detected depending on the selected row
        ret = "delete"
        if (ret=="delete"):
            # a pop-up should confirm.
            ret = "ok"
            if (ret == "ok"):
                ret = self.modBB.delete(RowNo)
                ret = self.modBB.calculateCascade()
        elif (ret == "edit"):
            OnGridPageBBGridCellLeftDclick(self,event)
        

    def OnCb1pageBBCheckbox(self, event):
        self.modBB.storeModulePars()

    def OnChoicepageBBChoice(self, event):
        self.modBB.storeModulePars()

    def OnTc1pageBBTextEnter(self, event):
        self.modBB.storeModulePars()

    def OnTc2pageBBTextEnter(self, event):
        self.modBB.storeModulePars()

    def OnTc3pageBBTextEnter(self, event):
        self.modBB.storeModulePars()

    def OnTc4pageBBTextEnter(self, event):
        self.modBB.storeModulePars()

    def OnTc5pageBBTextEnter(self, event):
        self.modBB.storeModulePars()

    def OnButtonpageBBOkButton(self, event):
        saveOption = "save"
        self.modBB.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleOK: now I should go back to HC"

    def OnButtonpageBBCancelButton(self, event):
        #warning: do you want to leave w/o saving ???
        saveOption = "save"
        self.modBB.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleCancel: now I should go back to HC"

    def OnButtonpageBBBackButton(self, event):
        #pop-up: to save or not to save ...
        saveOption = "save"
        self.modBB.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleBack: now I should show another window"

    def OnButtonpageBBFwdButton(self, event):
        #pop-up: to save or not to save ...
        saveOption = "save"
        self.modBB.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleFwd: now I should show another window"
