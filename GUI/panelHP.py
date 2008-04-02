#Boa:FramePanel:PanelHP
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
#	Panel HEAT PUMP
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Panel for heat pump design assistant
#
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Hans Schweiger	    February 2008
#	Revised by:         Hans Schweiger          20/03/2008
#                           Hans Schweiger          02/04/2008
#
#       Changes to previous version:
#       - Event handler Design Assistant 1
#       02/04/08:   adaptation to format from PanelBB from Tom
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
from einstein.modules.heatPump.moduleHP import *
from einstein.GUI.status import Status
import einstein.modules.matPanel as Mp
from einstein.modules.interfaces import *
from numpy import *
from einstein.GUI.panelHP_PopUp1 import HPPopUp1



[wxID_PANELHP, wxID_PANELHPBUTTONPAGEHEATPUMPADD, 
 wxID_PANELHPBUTTONPAGEHEATPUMPBACK, wxID_PANELHPBUTTONPAGEHEATPUMPCANCEL, 
 wxID_PANELHPBUTTONPAGEHEATPUMPFWD, wxID_PANELHPBUTTONPAGEHEATPUMPOK, 
 wxID_PANELHPCB1PAGEHEATPUMP, wxID_PANELHPCHOICEPAGEHEATPUMP, 
 wxID_PANELHPGRIDPAGEHP, wxID_PANELHPHPCALCULATE, 
 wxID_PANELHPST10PAGEHEATPUMP, wxID_PANELHPST11PAGEHEATPUMP, 
 wxID_PANELHPST12PAGEHEATPUMP, wxID_PANELHPST1PAGEHEATPUMP, 
 wxID_PANELHPST2PAGEHEATPUMP, wxID_PANELHPST3PAGEHEATPUMP, 
 wxID_PANELHPST4PAGEHEATPUMP, wxID_PANELHPST5PAGEHEATPUMP, 
 wxID_PANELHPST6PAGEHEATPUMP, wxID_PANELHPST7PAGEHEATPUMP, 
 wxID_PANELHPST8PAGEHEATPUMP, wxID_PANELHPST9PAGEHEATPUMP, 
 wxID_PANELHPSTATICBOX1, wxID_PANELHPTC1PAGEHEATPUMP, 
 wxID_PANELHPTC2PAGEHEATPUMP, wxID_PANELHPTC3PAGEHEATPUMP, 
 wxID_PANELHPTC4PAGEHEATPUMP, wxID_PANELHPTC5PAGEHEATPUMP, 
 wxID_PANELHPTC6PAGEHEATPUMP, wxID_PANELHPTC7PAGEHEATPUMP,
 wxID_PANELHPFIG
] = [wx.NewId() for _init_ctrls in range(31)]

#XXX HS2008-04-02: block copied from panelBB
#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem


#------------------------------------------------------------------------------		
#HS2008-03-22: 
#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		
    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.plot(Interfaces.GData['HP Plot'][0],
                      Interfaces.GData['HP Plot'][1],
                      'go-', label='QD', linewidth=2)
    self.subplot.plot(Interfaces.GData['HP Plot'][0],
                      Interfaces.GData['HP Plot'][2],
                      'rs',  label='QA')
    self.subplot.plot(Interfaces.GData['HP Plot'][0],
                      Interfaces.GData['HP Plot'][3],
                      'go-', label='QD_mod', linewidth=2)
    self.subplot.plot(Interfaces.GData['HP Plot'][0],
                      Interfaces.GData['HP Plot'][4],
                      'rs',  label='QA_mod')
    self.subplot.axis([0, 100, 0, 3e+7])
    self.subplot.legend()


#------------------------------------------------------------------------------		
class PanelHP(wx.Panel):
#------------------------------------------------------------------------------		
#   Panel of the heat pump design assistant
#------------------------------------------------------------------------------		

    def __init__(self, parent, id, pos, size, style, name, sql, db):

        self.sql = sql
        self.db = db
        
        self._init_ctrls(parent)

	keys = ['HP Table']
        self.modHP = ModuleHP(keys)

#   graphic: Cumulative heat demand by hours
        labels_column = 0
        ignoredrows = []
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : 'Some title',           # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelHPFig, wx.Panel, self.getDrawFigure())
        del dummy

#XXXHS2008-04-02: copied block from PanelBB. Tom, please revise
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
        print "PanelHP (__init__): data = ",data
        (rows,cols) = data.shape
        self.gridPageHP.CreateGrid(max(rows,20), cols)

        self.gridPageHP.EnableGridLines(True)
        self.gridPageHP.SetDefaultRowSize(20)
        self.gridPageHP.SetRowLabelSize(30)
        self.gridPageHP.SetColSize(0,115)
        self.gridPageHP.EnableEditing(False)
        self.gridPageHP.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.gridPageHP.SetColLabelValue(0, "Short name")
        self.gridPageHP.SetColLabelValue(1, "Year")
        self.gridPageHP.SetColLabelValue(2, "Type")
        self.gridPageHP.SetColLabelValue(3, "Operating\nhours")
        self.gridPageHP.SetColLabelValue(4, "Power")
        self.gridPageHP.SetColLabelValue(5, "Temperature")
        #
        # copy values from dictionary to grid
        #
        for r in range(rows):
            self.gridPageHP.SetRowAttr(r, attr)
            for c in range(cols):
                self.gridPageHP.SetCellValue(r, c, data[r][c])
                if c == labels_column:
                    self.gridPageHP.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.gridPageHP.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.gridPageHP.SetGridCursor(0, 0)
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELHP, name='PanelHP', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
#        self.SetClientSize(wx.Size(792, 618))

#------------------------------------------------------------------------------		
#       Displays of status
#------------------------------------------------------------------------------		

#..............................................................................
# Figure to be plotted

        self.staticBox1 = wx.StaticBox(id=-1,
              label='Heat demand and availability with and without HP',
              name='staticBox1', parent=self, pos=wx.Point(440, 40),
              size=wx.Size(336, 256), style=0)

        self.panelHPFig = wx.Panel(id=wxID_PANELHPFIG, name='panelHPFigure', parent=self,
              pos=wx.Point(450, 66), size=wx.Size(316, 220),
              style=wx.TAB_TRAVERSAL)

#..............................................................................
# Grid for display of existing heat pumps

        self.gridPageHP = wx.grid.Grid(id=wxID_PANELHPGRIDPAGEHP,
              name='gridpageHP', parent=self, pos=wx.Point(40, 48),
              size=wx.Size(376, 168), style=0)
        self.gridPageHP.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageHPGridCellLeftDclick, id=wxID_PANELHPGRIDPAGEHP)
        self.gridPageHP.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageHPGridCellRightClick, id=wxID_PANELHPGRIDPAGEHP)


        self.st1pageHeatpump = wx.StaticText(id=-1,
              label='Existing Heat pumps in the HC system',
              name='st1pageHeatpump', parent=self, pos=wx.Point(40, 32),
              style=0)

#------------------------------------------------------------------------------		
#       Action buttons and text entry
#------------------------------------------------------------------------------		

# Button "run design assistant"
        self.hpCalculate = wx.Button(id=wxID_PANELHPHPCALCULATE,
              label='Run design assistant', name='HP_Calculate', parent=self,
              pos=wx.Point(232, 224), size=wx.Size(184, 23), style=0)

        self.hpCalculate.Bind(wx.EVT_BUTTON, self.OnHpCalculateButton,
              id=wxID_PANELHPHPCALCULATE)

# Button "add heat pump"
        self.buttonpageHeatPumpAdd = wx.Button(id=-1,
              label='add heat pump manually', name='buttonpageHeatPumpAdd',
              parent=self, pos=wx.Point(40, 224), size=wx.Size(184, 23),
              style=0)
        self.buttonpageHeatPumpAdd.Bind(wx.EVT_BUTTON, self.OnButtonpageHPAddButton,
              id=-1)

        self.st2pageHeatPump = wx.StaticText(id=-1,
              label='Design assistant options:', name='st2pageHeatPump',
              parent=self, pos=wx.Point(40, 272), style=0)
        self.st2pageHeatPump.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.st3pageHeatPump = wx.StaticText(id=-1,
              label='Maintain existing equipment ?', name='st3pageHeatPump',
              parent=self, pos=wx.Point(40, 304), style=0)

        self.cb1pageHeatPump = wx.CheckBox(id=-1, label='',
              name='cb1pageHeatPump', parent=self, pos=wx.Point(288, 308),
              size=wx.Size(24, 13), style=0)
        self.cb1pageHeatPump.SetValue(False)

        self.st4pageHeatPump = wx.StaticText(id=-1, label='Type of heat pump',
              name='st4pageHeatPump', parent=self, pos=wx.Point(40, 344),
              style=0)

        self.choicepageHeatPump = wx.Choice(choices=["compression",
              "absorption"], id=-1, name='choicepageHeatPump', parent=self,
              pos=wx.Point(288, 336), size=wx.Size(130, 21), style=0)

        self.st5pageHeatPump = wx.StaticText(id=-1,
              label='Minimum desired annual operation hours, h',
              name='st5pageHeatPump', parent=self, pos=wx.Point(40, 384),
              style=0)

        self.st6pageHeatPump = wx.StaticText(id=-1,
              label='Maximum desired temperature lift, \xbaC',
              name='st6pageHeatPump', parent=self, pos=wx.Point(40, 424),
              style=0)

        self.st7pageHeatPump = wx.StaticText(id=-1,
              label='Maximum desired condensing temperature, \xbaC',
              name='st7pageHeatPump', parent=self, pos=wx.Point(40, 464),
              style=0)

        self.st8pageHeatPump = wx.StaticText(id=-1,
              label='Minimum desired evaporating temperature, \xbaC',
              name='st8pageHeatPump', parent=self, pos=wx.Point(40, 504),
              style=0)

        self.st9pageHeatPump = wx.StaticText(id=-1,
              label='Only for absorption type:', name='st9pageHeatPump',
              parent=self, pos=wx.Point(40, 536), style=0)

        self.st10pageHeatPump = wx.StaticText(id=-1,
              label='Inlet temperature of heating fluid in generator, \xbaC',
              name='st10pageHeatPump', parent=self, pos=wx.Point(40, 552),
              style=0)

        self.tc2pageHeatPump = wx.TextCtrl(id=-1, name='tc2pageHeatPump',
              parent=self, pos=wx.Point(288, 416), size=wx.Size(128, 21),
              style=0, value='')

        self.tc3pageHeatPump = wx.TextCtrl(id=-1, name='tc3pageHeatPump',
              parent=self, pos=wx.Point(288, 456), size=wx.Size(128, 21),
              style=0, value='')

        self.tc4pageHeatPump = wx.TextCtrl(id=-1, name='tc4pageHeatPump',
              parent=self, pos=wx.Point(288, 496), size=wx.Size(128, 21),
              style=0, value='')

        self.tc6pageHeatPump = wx.TextCtrl(id=-1, name='tc6pageHeatPump',
              parent=self, pos=wx.Point(640, 416), size=wx.Size(128, 21),
              style=0, value='')

        self.tc1pageHeatPump = wx.TextCtrl(id=-1, name='tc1pageHeatPump',
              parent=self, pos=wx.Point(288, 376), size=wx.Size(128, 21),
              style=0, value='')

        self.tc7pageHeatPump = wx.TextCtrl(id=-1, name='tc7pageHeatPump',
              parent=self, pos=wx.Point(640, 456), size=wx.Size(128, 21),
              style=0, value='')

        self.tc5pageHeatPump = wx.TextCtrl(id=-1, name='tc5pageHeatPump',
              parent=self, pos=wx.Point(288, 544), size=wx.Size(128, 21),
              style=0, value='')

        self.st11pageHeatPump = wx.StaticText(id=-1,
              label='Pinch temperature \xb0C', name='st11pageHeatPump',
              parent=self, pos=wx.Point(440, 424), style=0)

        self.st12pageHeatPump = wx.StaticText(id=-1,
              label='Temperature gap \xb0K', name='st12pageHeatPump',
              parent=self, pos=wx.Point(440, 464), style=0)

#------------------------------------------------------------------------------		
#       Default action buttons: FWD / BACK / OK / Cancel
#------------------------------------------------------------------------------		

        self.buttonpageHeatPumpOk = wx.Button(id=-1, label='ok',
              name='buttonpageHeatPumpOk', parent=self, pos=wx.Point(528, 544),
              size=wx.Size(75, 23), style=0)

        self.buttonpageHeatPumpCancel = wx.Button(id=-1, label='cancel',
              name='buttonpageHeatPumpCancel', parent=self, pos=wx.Point(616,
              544), size=wx.Size(75, 23), style=0)

        self.buttonpageHeatPumpFwd = wx.Button(id=wxID_PANELHPBUTTONPAGEHEATPUMPFWD,
              label='>>>', name='buttonpageHeatPumpFwd', parent=self,
              pos=wx.Point(704, 544), size=wx.Size(75, 23), style=0)

        self.buttonpageHeatPumpFwd.Bind(wx.EVT_BUTTON,
              self.OnButtonpageHeatPumpFwdButton,
              id=wxID_PANELHPBUTTONPAGEHEATPUMPFWD)

        self.buttonpageHeatPumpBack = wx.Button(id=wxID_PANELHPBUTTONPAGEHEATPUMPBACK,
              label='<<<', name='buttonpageHeatPumpBack', parent=self,
              pos=wx.Point(440, 544), size=wx.Size(75, 23), style=0)

        self.buttonpageHeatPumpBack.Bind(wx.EVT_BUTTON,
              self.OnButtonpageHeatPumpBackButton,
              id=wxID_PANELHPBUTTONPAGEHEATPUMPBACK)

#------------------------------------------------------------------------------		
    def getDrawFigure(self):
#------------------------------------------------------------------------------		
#   function for drawing 
#------------------------------------------------------------------------------		

        global drawFigure
        return drawFigure

#==============================================================================
#   Event handlers
#==============================================================================

#------------------------------------------------------------------------------		
    def OnHpCalculateButton(self, event):
#------------------------------------------------------------------------------		
#   Button "Run Design Assistant" pressed
#------------------------------------------------------------------------------		

#..............................................................................
# Step 1 design assistant: gets a preselected list of possible heat pumps

        (mode,HPList) = self.modHP.designAssistant1()
        
#..............................................................................
# In interactive mode open DB Edidor Heat pump and select manually

        if (mode == "MANUAL"):
            print "PanelHP (OnHpCalculateButton): here I should edit the data base"
            HPId = 11
        elif (mode == "AUTOMATIC"):
            HPId = HPList[0]

#..............................................................................
# Step 2 design assistant: add selected equipment to the list
        
        self.modHP.designAssistant2(HPId)
        self.modHP.updatePanel()

        #updatePlots ???

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnButtonpageHPAddButton(self, event):
#------------------------------------------------------------------------------		
#   adds an equipment to the list
#------------------------------------------------------------------------------		
        (self.equipe,self.equipeC) = self.modHP.addEquipmentDummy()      #creates space for new equipment in Q/C
        
        #show pop-up menu 1: add from where ???
        pu1 = HPPopUp1(self)
        if pu1.ShowModal() == wx.ID_OK:
            print 'Accepted'
        else:
            self.equipe.delete()         #delete the space created before, if not accepted
            self.equipeC.delete()
            print 'Cancelled'
            
        Status.SQL.commit()
        self.modHP.updatePanel()


#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnGridPageHPGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
#   adds an equipment to he 
#------------------------------------------------------------------------------		
        print "Grid - left button Dclick: here I should call the Q4H"
        ret = "ok"
        if (ret=="ok"):
#            ret = self.modBB.calculateCascade()
            pass
        #updatePlots

    def OnGridPageHPGridCellRightClick(self, event):
        print "Grid - right button click: scroll-up should appear"
        #here a scroll-up should appear with some options: edit, delete,...
        RowNo = 1 #number of the selected boiler should be detected depending on the selected row
        ret = "delete"
        if (ret=="delete"):
            # a pop-up should confirm.
            ret = "ok"
            if (ret == "ok"):
                ret = self.modHP.delete(RowNo)
                ret = self.modHP.calculateCascade()
        elif (ret == "edit"):
            OnGridPageBBGridCellLeftDclick(self,event)
        

        
    def OnButton1Button(self, event):
        event.Skip()

#------------------------------------------------------------------------------		
#   Default event handlers: FWD / BACK / OK / Cancel - Buttons
#------------------------------------------------------------------------------		

    def OnButtonpageHeatPumpBackButton(self, event):
        event.Skip()

    def OnButtonpageHeatPumpFwdButton(self, event):
        event.Skip()

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


