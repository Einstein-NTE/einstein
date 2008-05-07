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
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	    February 2008
#	Last revised by:    Hans Schweiger          24/03/2008
#                           Hans Schweiger          03/04/2008
#                           Tom Sobota              05/04/2008
#                           Hans Schweiger          16/04/2008
#                           Hans Schweiger          29/04/2008
#
#       Changes to previous version:
#       - structure of plots identical to that of HP
#       03/04/2008:         Adaptation to structure Modules
#       05/04/08    changed call to popup1 in OnButtonpageHPAddButton
#                   slight change to OK and Cancel buttons, to show the right icons
#       16/04/2008: HS  main as argument in __init__
#       29/04/2008: HS  method draw for panelBBFig
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
from numpy import *
from einstein.GUI.addEquipment_popup import AddEquipment #TS 20080405 changed

import einstein.modules.matPanel as Mp
from einstein.GUI.dialogOK import *

from einstein.modules.interfaces import *
from einstein.modules.constants import *


[wxID_PANELBB, wxID_PANELBBBBCALCULATE, wxID_PANELBBBUTTONPAGEBBADD, 
 wxID_PANELBBBUTTONPAGEBBBACK, wxID_PANELBBBUTTONPAGEBBCANCEL, 
 wxID_PANELBBBUTTONPAGEBBFWD, wxID_PANELBBBUTTONPAGEBBOK, 
 wxID_PANELBBCB1PAGEBB, wxID_PANELBBCHOICEPAGEBB, wxID_PANELBBGRID, 
 wxID_PANELFIG, wxID_PANELBBSTCONFIG8, wxID_PANELBBST11PAGEBB, 
 wxID_PANELBBST12PAGEBB, wxID_PANELBBST1PAGEBB, wxID_PANELBBST2PAGEBB, 
 wxID_PANELBBST3PAGEBB, wxID_PANELBBST4PAGEBB, wxID_PANELBBSTCONFIG3, 
 wxID_PANELBBSTCONFIG4, wxID_PANELBBSTCONFIG5, wxID_PANELBBSTCONFIG6, 
 wxID_PANELBBSTCONFIG7, wxID_PANELBBSTATICTEXT1, wxID_PANELBBTCCONFIG3, 
 wxID_PANELBBTCCONFIG4, wxID_PANELBBTCCONFIG5, wxID_PANELBBTCCONFIG6, 
 wxID_PANELBBTCCONFIG7, wxID_PANELBBTC6PAGEBB, wxID_PANELBBTC7PAGEBB, 
] = [wx.NewId() for _init_ctrls in range(31)]
#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem

MAXROWS = 50
TABLECOLS = 6

TYPELIST = BBTYPES

#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		
    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.plot(Interfaces.GData['BB Plot'][0],
                      Interfaces.GData['BB Plot'][1],
                      'go-', label='QD', linewidth=2)
    self.subplot.plot(Interfaces.GData['BB Plot'][0],
                      Interfaces.GData['BB Plot'][2],
                      'rs',  label='QA')
    self.subplot.plot(Interfaces.GData['BB Plot'][0],
                      Interfaces.GData['BB Plot'][3],
                      'go-', label='QD_mod', linewidth=2)
    self.subplot.plot(Interfaces.GData['BB Plot'][0],
                      Interfaces.GData['BB Plot'][4],
                      'rs',  label='QA_mod')
    self.subplot.axis([0, 100, 0, 3e+7])
    self.subplot.legend()


#------------------------------------------------------------------------------		
class PanelBB(wx.Panel):
#------------------------------------------------------------------------------		
#   Panel of the boiler&burner design assistant
#------------------------------------------------------------------------------		

    def __init__(self, parent, main, id, pos, size, style, name):
        self.prnt = parent
        self.main = main
        self._init_ctrls(parent)
        
	self.keys = ['BB Table']
        self.mod = Status.mod.moduleBB
        
#   graphic: Cumulative heat demand by hours
        labels_column = 0
        ignoredrows = []
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : self.keys[0],                # key for Interface
                   'title'       : 'Some title',           # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelFig, wx.Panel, drawFigure, paramList)
        del dummy

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

        key = self.keys[0]
        (rows,cols) = (MAXROWS,TABLECOLS)
        self.grid.CreateGrid(MAXROWS, cols)

        self.grid.EnableGridLines(True)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetColSize(0,115)
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, "Short name")
        self.grid.SetColLabelValue(1, "Nom. power")
        self.grid.SetColLabelValue(2, "COP")
        self.grid.SetColLabelValue(3, "Type")
        self.grid.SetColLabelValue(4, "Operating\nhours")
        self.grid.SetColLabelValue(5, "Year manufact.")
        #
        # copy values from dictionary to grid
        #
        for r in range(rows):
            self.grid.SetRowAttr(r, attr)
            for c in range(cols):
                self.grid.SetCellValue(r, c, "")
                if c == labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid.SetGridCursor(0, 0)

        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELBB, name='PanelBB', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

#------------------------------------------------------------------------------		
#       Displays of status
#------------------------------------------------------------------------------		

#..............................................................................
# Figure to be plotted

        self.staticText1 = wx.StaticText(id=wxID_PANELBBSTATICTEXT1,
              label=u'Heat demand and availability with and without BB',
              name='staticText1', parent=self, pos=wx.Point(424, 32),
              size=wx.Size(352, 17), style=0)

        self.panelFig = wx.Panel(id=wxID_PANELFIG, name='panelFig', parent=self,
              pos=wx.Point(450, 66), size=wx.Size(316, 220),
              style=wx.TAB_TRAVERSAL)

#..............................................................................
# Grid for display of existing boilers and burners

        self.grid = wx.grid.Grid(id=wxID_PANELBBGRID,
              name='gridpageBB', parent=self, pos=wx.Point(40, 48),
              size=wx.Size(376, 168), style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageBBGridCellLeftDclick, id=wxID_PANELBBGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageBBGridCellRightClick, id=wxID_PANELBBGRID)

        self.st1pageBB = wx.StaticText(id=-1,
              label='Existing Boilers and burners in the HC system',
              name='st1pageBB', parent=self, pos=wx.Point(40, 32), style=0)
#------------------------------------------------------------------------------		
#       Action buttons and text entry
#------------------------------------------------------------------------------		

# Button "run design assistant"
        self.BBCalculate = wx.Button(id=wxID_PANELBBBBCALCULATE,
              label='run design assistant', name='BB_Calculate', parent=self,
              pos=wx.Point(232, 224), size=wx.Size(184, 24), style=0)
        self.BBCalculate.Bind(wx.EVT_BUTTON, self.OnBBCalculateButton,
              id=wxID_PANELBBBBCALCULATE)
# Button "add BB"
        self.buttonpageBBAdd = wx.Button(id=wxID_PANELBBBUTTONPAGEBBADD,
              label='add boiler / burner', name='buttonpageBBAdd', parent=self,
              pos=wx.Point(32, 224), size=wx.Size(184, 24), style=0)
        self.buttonpageBBAdd.Bind(wx.EVT_BUTTON, self.OnButtonpageBBAddButton,
              id=wxID_PANELBBBUTTONPAGEBBADD)

#------------------------------------------------------------------------------		
#       Configuration design assistant
#------------------------------------------------------------------------------		

        self.st2pageBB = wx.StaticText(id=-1, label='Design assistant options:',
              name='st2pageBB', parent=self, pos=wx.Point(40, 272), style=0)
        self.st2pageBB.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

#..............................................................................
# 1. Maintain existing equipment ?

        self.st3pageBB = wx.StaticText(id=-1,
              label='Maintain existing equipment ?', name='st3pageBB',
              parent=self, pos=wx.Point(40, 304), style=0)

        self.cb1pageBB = wx.CheckBox(id=wxID_PANELBBCB1PAGEBB, label='',
              name='cb1pageBB', parent=self, pos=wx.Point(288, 308),
              size=wx.Size(24, 13), style=0)

        self.cb1pageBB.Bind(wx.EVT_CHECKBOX, self.OnCb1pageBBCheckbox,
              id=wxID_PANELBBCB1PAGEBB)

#..............................................................................
# 2. BB type 
        self.st4pageBB = wx.StaticText(id=-1, label='Type of boiler/burner',
              name='st4pageBB', parent=self, pos=wx.Point(40, 344), style=0)

        self.choicepageBB = wx.Choice(choices=["steam boiler",
              "hot water (condensing)", "hot water (standard)"],
              id=wxID_PANELBBCHOICEPAGEBB, name='choicepageBB', parent=self,
              pos=wx.Point(288, 336), size=wx.Size(130, 21), style=0)
        self.choicepageBB.Bind(wx.EVT_CHOICE, self.OnChoicepageBBChoice,
              id=wxID_PANELBBCHOICEPAGEBB)

#..............................................................................
# 3. Minimum operating hours
        self.stConfig3 = wx.StaticText(id=-1,
              label='Minimum desired annual operation hours, h',
              name='stConfig3', parent=self, pos=wx.Point(40, 384), style=0)

        self.tcConfig3 = wx.TextCtrl(id=wxID_PANELBBTCCONFIG3, name='tcConfig3',
              parent=self, pos=wx.Point(288, 376), size=wx.Size(128, 21),
              style=0, value='')
        self.tcConfig3.Bind(wx.EVT_TEXT_ENTER, self.OnTcConfig3TextEnter,
              id=wxID_PANELBBTCCONFIG3)

#..............................................................................
# 4. Temperature lift
        self.stConfig4 = wx.StaticText(id=-1,
              label='Maximum desired temperature lift, \xbaC', name='stConfig4',
              parent=self, pos=wx.Point(40, 424), style=0)

        self.tcConfig4 = wx.TextCtrl(id=-1, name='tcConfig4', parent=self,
              pos=wx.Point(288, 416), size=wx.Size(128, 21), style=0, value='')
        self.tcConfig4.Bind(wx.EVT_TEXT_ENTER, self.OnTcConfig4TextEnter,
              id=wxID_PANELBBTCCONFIG4)

#..............................................................................
# 5. condensing temperature
        self.stConfig5 = wx.StaticText(id=-1,
              label='Maximum desired condensing temperature, \xbaC',
              name='stConfig5', parent=self, pos=wx.Point(40, 464), style=0)

        self.tcConfig5 = wx.TextCtrl(id=-1, name='tcConfig5', parent=self,
              pos=wx.Point(288, 456), size=wx.Size(128, 21), style=0, value='')
        self.tcConfig5.Bind(wx.EVT_TEXT_ENTER, self.OnTcConfig5TextEnter,
              id=wxID_PANELBBTCCONFIG5)

#..............................................................................
# 6. evaporating temperature
        self.stConfig6 = wx.StaticText(id=-1,
              label='Minimum desired evaporating temperature, \xbaC',
              name='stConfig6', parent=self, pos=wx.Point(40, 504), style=0)

        self.tcConfig6 = wx.TextCtrl(id=wxID_PANELBBTCCONFIG6, name='tcConfig6',
              parent=self, pos=wx.Point(288, 496), size=wx.Size(128, 21),
              style=0, value='')
        self.tcConfig6.Bind(wx.EVT_TEXT_ENTER, self.OnTcConfig6TextEnter,
              id=wxID_PANELBBTCCONFIG6)

#..............................................................................
# 7. condensing temperature: inlet temp.
        self.stConfig7 = wx.StaticText(id=-1, label='Only for absorption type:',
              name='stConfig7', parent=self, pos=wx.Point(40, 536), style=0)

        self.stConfig8 = wx.StaticText(id=-1,
              label='Inlet temperature of heating fluid in generator, \xbaC',
              name='stConfig8', parent=self, pos=wx.Point(40, 552), style=0)

        self.tcConfig7 = wx.TextCtrl(id=wxID_PANELBBTCCONFIG7, name='tcConfig7',
              parent=self, pos=wx.Point(288, 544), size=wx.Size(128, 21),
              style=0, value='')
        self.tcConfig7.Bind(wx.EVT_TEXT_ENTER, self.OnTcConfig7TextEnter,
              id=wxID_PANELBBTCCONFIG7)

#------------------------------------------------------------------------------		
#       Display field at the right
#------------------------------------------------------------------------------		

        self.st11pageBB = wx.StaticText(id=-1, label='Pinch temperature \xb0C',
              name='st11pageBB', parent=self, pos=wx.Point(440, 424), style=0)

        self.tc6pageBB = wx.TextCtrl(id=-1, name='tc6pageBB', parent=self,
              pos=wx.Point(640, 416), size=wx.Size(128, 21), style=0,
              value='??')

        self.tc7pageBB = wx.TextCtrl(id=-1, name='tc7pageBB', parent=self,
              pos=wx.Point(640, 456), size=wx.Size(128, 21), style=0,
              value='??')

        self.st12pageBB = wx.StaticText(id=-1, label='Temperature gap \xb0K',
              name='st12pageBB', parent=self, pos=wx.Point(440, 464), style=0)
#------------------------------------------------------------------------------		
#       Default action buttons: FWD / BACK / OK / Cancel
#------------------------------------------------------------------------------		

        self.buttonpageBBOk = wx.Button(id=wx.ID_OK,
              label='OK', name='buttonpageBBOk', parent=self, pos=wx.Point(528,
              544), size=wx.Size(75, 23), style=0)
        self.buttonpageBBOk.Bind(wx.EVT_BUTTON, self.OnButtonpageBBOkButton,
              id=wx.ID_OK)

        self.buttonpageBBCancel = wx.Button(id=wx.ID_CANCEL,
              label='Cancel', name='buttonpageBBCancel', parent=self,
              pos=wx.Point(616, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageBBCancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpageBBCancelButton,
              id=wx.ID_CANCEL)

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

#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   function activated on each entry into the panel from the tree
#------------------------------------------------------------------------------		
        self.mod.initPanel()        # prepares data for plotting

#..............................................................................
# update of equipment table

        try:
            data = Interfaces.GData[self.keys[0]]
            (rows,cols) = data.shape
        except:
            rows = 0
            cols = TABLECOLS
            
        for r in range(rows):
            for c in range(cols):
                self.grid.SetCellValue(r, c, data[r][c])

#XXX Here better would be updating the grid and showing less rows ... ????
        for r in range(rows,MAXROWS):
            for c in range(cols):
                self.grid.SetCellValue(r, c, "")

#..............................................................................
# update of design assistant parameters

        self.config = Interfaces.GData["BB Config"]
#        self.cbConfig1.SetValue(self.config[0])
#        try:        #try-except necessary if there comes a string that is not in list.
#            self.choiceConfig2.SetSelection(TYPELIST.index(self.config[1]))
#        except:
#            print "PanelHP (display): was asked to display an erroneous heat pump type",self.config[1]
#            pass
        self.tcConfig3.SetValue(str(self.config[2]))
        self.tcConfig4.SetValue(str(self.config[3]))
        self.tcConfig5.SetValue(str(self.config[4]))
        self.tcConfig6.SetValue(str(self.config[5]))
        self.tcConfig7.SetValue(str(self.config[6]))
        
#..............................................................................
# update of info-values

#        self.info = Interfaces.GData["HP Info"]
        
#        self.tcInfo1.SetValue(str(self.info[0]))
#        self.tcInfo2.SetValue(str(self.info[1]))

        self.panelFig.draw()
        self.Show()
#==============================================================================
#   Event handlers
#==============================================================================

#------------------------------------------------------------------------------		
    def OnBBCalculateButton(self, event):
#------------------------------------------------------------------------------		
#   Button "Run Design Assistant" pressed
#------------------------------------------------------------------------------		
#..............................................................................
# Step 1 design assistant: gets a preselected list of possible heat pumps

        print "PanelBB (run design assistant): calling function DA"
        (mode,BBList) = self.mod.designAssistant()
        
#..............................................................................
# In interactive mode open DB Edidor Heat pump and select manually

        if (mode == "MANUAL"):
            self.dbe = DBEditFrame(self,
                            'Select boiler or burner from preselected list', # title for the dialogs
			    'dbboiler',              # database table
			    0,                         # column to be returned
			    False,
                            preselection = BBList)      # database table can be edited in DBEditFrame?
            if self.dbe.ShowModal() == wx.ID_OK:
                BBId = self.dbe.theId
            else:
                BBId = -1
                print "PanelBB: no BB selected after DA1 -> check whether this works"

        elif (mode == "AUTOMATIC"):
            BBId = BBList[0]    #in automatic mode just take first in the list

        elif (mode == "CANCEL"):
            BBId = -1 #make designAssistant2 to understand that
        else:
            print "PanelBB (DesignAssistant-Button): erroneous panel mode: ",mode

#..............................................................................
# Step 2 design assistant: add selected equipment to the list and update display
        
        self.mod.designAssistant2(HPId)
        self.display()

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnButtonpageBBAddButton(self, event):
#------------------------------------------------------------------------------		
#   adds an equipment to the list
#------------------------------------------------------------------------------		
        try:                #creates space for new equipment in Q/C
	    self.equipe = self.mod.addEquipmentDummy() #SD change 30/04/2008, delete equipeC
            pu1 =  AddEquipment(self,                      # pointer to this panel
                                self.mod,                # pointer to the associated module
                                'Add boiler equipment', # title for the dialogs
                                'dbboiler',              # database table
                                0,                         # column to be returned
                                False)                     # database table can be edited in DBEditFrame?

            if pu1.ShowModal() == wx.ID_OK:
                print 'PanelBB AddEquipment accepted. Id='+str(pu1.theId)
            else:
                self.mod.deleteEquipment(None)
            self.display()
        except:
            print "PanelBB (HPAddButton): could not create equipment dummy"
	    pass

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnGridPageBBGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
#       edits the selected equipment
#------------------------------------------------------------------------------		
        rowNo = event.GetRow() #number of the selected boiler should be detected depending on the selected row
        EqId = self.mod.getEqId(rowNo)
	dialog = ManualAddDialog(self, EqId)

        if (dialog.ShowModal() ==wx.ID_OK):
            print "PanelHP (OnGridLeftDclick) - OK"
#            ret = self.mod.calculateCascade()

        self.display()

#------------------------------------------------------------------------------		
    def OnGridPageBBGridCellRightClick(self, event):
#   right double click
#   --> for the moment only DELETE foreseen !!!
#------------------------------------------------------------------------------		
        rowNo = event.GetRow() #number of the selected boiler should be detected depending on the selected row

        ret = "delete"
#..............................................................................
# "delete" selected:

        if (ret=="delete"):
            pu2 =  DialogOK(self,"delete equipment","do you really want to delete this equipment ?")
            if pu2.ShowModal() == wx.ID_OK:
                self.mod.deleteEquipment(rowNo)
                self.display()
                
        elif (ret == "edit"):
            OnGridPageBBGridCellLeftDclick(self,event)
        
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
#   Event handlers: parameter change in design assistant
#------------------------------------------------------------------------------		
    def OnCb1pageBBCheckbox(self, event):
        self.modBB.storeModulePars()

    def OnChoicepageBBChoice(self, event):
        self.modBB.storeModulePars()

    def OnTcConfig3TextEnter(self, event):
        print "new config[%s] value: "%2,self.config[2]
        self.config[2] = self.tcConfig3.GetValue()
        Interfaces.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

    def OnTcConfig4TextEnter(self, event):
        self.config[3] = self.tcConfig4.GetValue()
        print "new config[%s] value: "%3,self.config[3]
        Interfaces.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

    def OnTcConfig5TextEnter(self, event):
        self.config[4] = self.tcConfig5.GetValue()
        print "new config[%s] value: "%4,self.config[4]
        Interfaces.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

    def OnTcConfig6TextEnter(self, event):
        self.config[5] = self.tcConfig6.GetValue()
        print "new config[%s] value: "%5,self.config[5]
        Interfaces.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

    def OnTcConfig7TextEnter(self, event):
        self.config[6] = self.tcConfig7.GetValue()
        print "new config[%s] value: "%6,self.config[6]
        Interfaces.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()


#==============================================================================
#   <<< OK Cancel >>>
#==============================================================================

    def OnButtonpageBBOkButton(self, event):
        self.main.tree.SelectItem(self.main.qHC, select=True)
        self.Hide()

    def OnButtonpageBBCancelButton(self, event):
        print "Button exitModuleCancel: CANCEL Option not yet foreseen"

    def OnButtonpageBBBackButton(self, event):
        self.main.tree.SelectItem(self.main.qHP, select=True)
        self.Hide()

    def OnButtonpageBBFwdButton(self, event):
        self.main.tree.SelectItem(self.main.qEnergy, select=True)
        self.Hide()
