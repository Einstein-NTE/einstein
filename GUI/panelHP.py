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
#	Version No.: 0.12
#	Created by: 	    Hans Schweiger	    February 2008
#	Revised by:         Hans Schweiger          20/03/2008
#                           Hans Schweiger          02/04/2008
#                           Hans Schweiger          03/04/2008
#                           Tom Sobota              05/04/2008
#                           Hans Schweiger          07/04/2008
#                           Hans Schweiger          13/04/2008
#                           Stoyan Danov            14/04/2008
#                           Hans Schweiger          15/04/2008
#                           Hans Schweiger          17/04/2008
#                           Stoyan Danov            17/04/2008
#                           Hans Schweiger          18/04/2008
#
#       Changes to previous version:
#       - Event handler Design Assistant 1
#       02/04/08:   adaptation to format from PanelBB from Tom
#       03/04/08:   adaptation to structure Modules
#       05/04/08    changed call to popup1 in OnButtonpageHPAddButton
#                   slight change to OK and Cancel buttons, to show the right icons
#       07/04/08:   adapted for changes in heat pump module
#       13/04/08:   Small changes in AddButton
#                   introduction of function "display"
#       14/04/08:   in OnButtonpageHPAddButton substitute equipe.delete() with deleteEquipment(rowNo)
#       15/04/08:   Bugs in event-handlers corrected. EVT_TEXT_ENTER substituted
#                   by EVT_KILL_FOCUS.
#       17/04/08:   DialogOK added for delete equipment
#       17/04/08:   OnHpCalculateButton: mode = CANCEL option added
#       18/04/08:   Determination of panel-operation mode shifted to design.ass.1
#                   Robustness of panel against empty data sets in GData
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
#from einstein.modules.heatPump.moduleHP import *
from einstein.GUI.status import Status
import einstein.modules.matPanel as Mp
from einstein.GUI.panelQ4 import PanelQ4
from einstein.GUI.dialogOK import *

from einstein.modules.interfaces import *
from einstein.modules.modules import *
from einstein.modules.constants import *
from numpy import *
from einstein.GUI.addEquipment_popup import * #TS 20080405 changed



[wxID_PANELHP, wxID_PANELHPBUTTONPAGEHEATPUMPADD, 
 wxID_PANELHPBUTTONPAGEHEATPUMPBACK, wxID_PANELHPBUTTONPAGEHEATPUMPCANCEL, 
 wxID_PANELHPBUTTONPAGEHEATPUMPFWD, wxID_PANELHPBUTTONPAGEHEATPUMPOK, 
 wxID_PANELHPCBCONFIG1, wxID_PANELHPCHOICECONFIG2, 
 wxID_PANELHPGRIDPAGEHP, wxID_PANELHPHPCALCULATE, 
 wxID_PANELHPST10PAGEHEATPUMP, wxID_PANELHPST11PAGEHEATPUMP, 
 wxID_PANELHPST12PAGEHEATPUMP, wxID_PANELHPST1PAGEHEATPUMP, 
 wxID_PANELHPSTCONFIG, wxID_PANELHPSTCONFIG1, 
 wxID_PANELHPSTCONFIG2, wxID_PANELHPSTCONFIG3, 
 wxID_PANELHPSTCONFIG4, wxID_PANELHPSTCONFIG5, 
 wxID_PANELHPSTCONFIG6, wxID_PANELHPSTCONFIG7, 
 wxID_PANELHPSTATICBOX1, wxID_PANELHPTCCONFIG3, 
 wxID_PANELHPTCCONFIG4, wxID_PANELHPTCCONFIG5, 
 wxID_PANELHPTCCONFIG6, wxID_PANELHPTCCONFIG7, 
 wxID_PANELHPTCINFO1, wxID_PANELHPTCINFO2,
 wxID_PANELHPFIG
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

TYPELIST = HPTYPES


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

    def __init__(self, parent, main, id, pos, size, style, name, sql, db):

        print "PanelHP (__init__)"
        self.prnt = parent
        self.main = main
        
        self.sql = sql
        self.db = db

#        self.info = Interfaces.GData["HP Info"]
#        self.config = Interfaces.GData["HP Config"]
        
        self._init_ctrls(parent)

	self.keys = ['HP Table']
        self.mod = Status.mod.moduleHP
#        print "PanelHP (__init__): mod created",self.mod

#   graphic: Cumulative heat demand by hours
        labels_column = 0
        ignoredrows = []
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : self.keys[0],                # key for Interface
                   'title'       : 'Some title',           # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelHPFig, wx.Panel, drawFigure, paramList)
        del dummy

#XXXHS2008-04-02: copied block from PanelBB. Tom, please revise
#TS20080405 Looks fine ...
        #
        # additional widgets setup
        # here, we modify some widgets attributes that cannot be changed
        # directly by Boa. This cannot be done in _init_ctrls, since that
        # method is rewritten by Boa each time.
        #
        # data cell attributes
        print "PanelHP (__init__): creating grid"

        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

        key = self.keys[0]
#        data = Interfaces.GData[key]
#        print "data = ",data
        (rows,cols) = (MAXROWS,TABLECOLS)
#        self.gridPageHP.CreateGrid(max(rows,20), cols)
        self.grid.CreateGrid(MAXROWS, cols)

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetColSize(0,115)
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, "Short name")
        self.grid.SetColLabelValue(1, "Year")
        self.grid.SetColLabelValue(2, "Type")
        self.grid.SetColLabelValue(3, "Operating\nhours")
        self.grid.SetColLabelValue(4, "Power")
        self.grid.SetColLabelValue(5, "Temperature")
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

        self.grid = wx.grid.Grid(id=wxID_PANELHPGRIDPAGEHP,
              name='gridpageHP', parent=self, pos=wx.Point(40, 48),
              size=wx.Size(376, 168), style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageHPGridCellLeftDclick, id=wxID_PANELHPGRIDPAGEHP)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
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

#------------------------------------------------------------------------------		
#       Configuration design assistant
#------------------------------------------------------------------------------		

        self.stConfig = wx.StaticText(id=-1,
              label='Design assistant options:', name='stConfig',
              parent=self, pos=wx.Point(40, 272), style=0)
        self.stConfig.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

#..............................................................................
# 1. Maintain existing equipment ?

        self.stConfig1 = wx.StaticText(id=-1,
              label='Maintain existing equipment ?', name='stConfig1',
              parent=self, pos=wx.Point(40, 304), style=0)

        self.cbConfig1 = wx.CheckBox(id=-1, label='',
              name='cbConfig1', parent=self, pos=wx.Point(288, 308),
              size=wx.Size(24, 13), style=0)

        self.cbConfig1.Bind(wx.EVT_CHECKBOX, self.OnCbConfig1Checkbox,
              id=-1)

#..............................................................................
# 2. Heat pump type 

        self.stConfig2 = wx.StaticText(id=-1, label='Type of heat pump',
              name='stConfig2', parent=self, pos=wx.Point(40, 344),
              style=0)

        self.choiceConfig2 = wx.Choice(choices=TYPELIST, id=-1, name='choicepageHeatPump', parent=self,
              pos=wx.Point(288, 336), size=wx.Size(130, 21), style=0)

        self.choiceConfig2.Bind(wx.EVT_CHOICE, self.OnChoiceConfig2Choice,
              id=-1)

#..............................................................................
# 3. Minimum operating hours

        self.stConfig3 = wx.StaticText(id=-1,
              label='Minimum desired annual operation hours, h',
              name='stConfig3', parent=self, pos=wx.Point(40, 384),
              style=0)

        self.tcConfig3 = wx.TextCtrl(id=-1, name='tcConfig3',
              parent=self, pos=wx.Point(288, 376), size=wx.Size(128, 21),
              style=wx.TE_PROCESS_ENTER, value="")

        self.tcConfig3.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig3TextEnter,
              id=-1)


#..............................................................................
# 4. Temperature lift

        self.stConfig4 = wx.StaticText(id=-1,
              label='Maximum desired temperature lift, \xbaC',
              name='stConfig4', parent=self, pos=wx.Point(40, 424),
              style=0)

        self.tcConfig4 = wx.TextCtrl(id=-1, name='tcConfig4',
              parent=self, pos=wx.Point(288, 416), size=wx.Size(128, 21),
              style=wx.TE_PROCESS_ENTER, value="")

        self.tcConfig4.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig4TextEnter,
              id=-1)

#..............................................................................
# 5. condensing temperature

        self.stConfig5 = wx.StaticText(id=-1,
              label='Maximum desired condensing temperature, \xbaC',
              name='stConfig5', parent=self, pos=wx.Point(40, 464),
              style=0)

        self.tcConfig5 = wx.TextCtrl(id=-1, name='tcConfig5',
              parent=self, pos=wx.Point(288, 456), size=wx.Size(128, 21),
              style=wx.TE_PROCESS_ENTER, value="")

        self.tcConfig5.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig5TextEnter,
              id=-1)

#..............................................................................
# 6. evaporating temperature

        self.stConfig6 = wx.StaticText(id=-1,
              label='Minimum desired evaporating temperature, \xbaC',
              name='stConfig6', parent=self, pos=wx.Point(40, 504),
              style=0)

        self.tcConfig6 = wx.TextCtrl(id=-1, name='tcConfig6',
              parent=self, pos=wx.Point(288, 496), size=wx.Size(128, 21),
              style=wx.TE_PROCESS_ENTER, value="")

        self.tcConfig6.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig6TextEnter,
              id=-1)

#..............................................................................
# 7. condensing temperature: inlet temp.

        self.stConfig7a = wx.StaticText(id=-1,
              label='Only for absorption type:', name='stConfig7a',
              parent=self, pos=wx.Point(40, 536), style=0)

        self.stConfig7b = wx.StaticText(id=-1,
              label='Inlet temperature of heating fluid in generator, \xbaC',
              name='stConfig7b', parent=self, pos=wx.Point(40, 552),
              style=0)

        self.tcConfig7 = wx.TextCtrl(id=-1, name='tcConfig7',
              parent=self, pos=wx.Point(288, 544), size=wx.Size(128, 21),
              style=wx.TE_PROCESS_ENTER, value="")

        self.tcConfig7.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig7TextEnter,
              id=-1)

#------------------------------------------------------------------------------		
#       Display field at the right
#------------------------------------------------------------------------------		


        self.stInfo1 = wx.StaticText(id=-1,
              label='Pinch temperature \xb0C', name='stInfo1',
              parent=self, pos=wx.Point(440, 424), style=0)

        self.tcInfo1 = wx.TextCtrl(id=-1, name='tcInfo1',
              parent=self, pos=wx.Point(640, 416), size=wx.Size(128, 21),
              style=0, value="")

        self.stInfo2 = wx.StaticText(id=-1,
              label='Temperature gap \xb0K', name='stInfo2',
              parent=self, pos=wx.Point(440, 464), style=0)

        self.tcInfo2 = wx.TextCtrl(id=-1, name='tcInfo2',
              parent=self, pos=wx.Point(640, 456), size=wx.Size(128, 21),
              style=0, value="")



#------------------------------------------------------------------------------		
#       Default action buttons: FWD / BACK / OK / Cancel
#       TS20080405 Notice: the OK button should always have an ID = wx.ID_OK
#                  and a label='OK' (uppercase)
#                  The Cancel button should always have an ID = wx.ID_CANCEL
#                  and a label 'Cancel' (as written)
#                  In this way, wxWidgets will show the right icons on the buttons
#------------------------------------------------------------------------------		

        self.buttonpageHeatPumpOk = wx.Button(id=wx.ID_OK, label='OK',
              name='buttonpageHeatPumpOk', parent=self, pos=wx.Point(528, 544),
              size=wx.Size(75, 23), style=0)

        self.buttonpageHeatPumpCancel = wx.Button(id=wx.ID_CANCEL, label='Cancel',
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

        self.config = Interfaces.GData["HP Config"]
        self.cbConfig1.SetValue(self.config[0])
        try:        #try-except necessary if there comes a string that is not in list.
            self.choiceConfig2.SetSelection(TYPELIST.index(self.config[1]))
        except:
            print "PanelHP (display): was asked to display an erroneous heat pump type",self.config[1]
            pass
        self.tcConfig3.SetValue(str(self.config[2]))
        self.tcConfig4.SetValue(str(self.config[3]))
        self.tcConfig5.SetValue(str(self.config[4]))
        self.tcConfig6.SetValue(str(self.config[5]))
        self.tcConfig7.SetValue(str(self.config[6]))
        
#..............................................................................
# update of info-values

        self.info = Interfaces.GData["HP Info"]
        
        self.tcInfo1.SetValue(str(self.info[0]))
        self.tcInfo2.SetValue(str(self.info[1]))

        self.Show()
        
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

        (mode,HPList) = self.mod.designAssistant1()
        
#..............................................................................
# In interactive mode open DB Edidor Heat pump and select manually

        if (mode == "MANUAL"):
            self.dbe = DBEditFrame(self,
                            'Select heat pump from preselected list', # title for the dialogs
			    'dbheatpump',              # database table
			    0,                         # column to be returned
			    False,
                            preselection = HPList)      # database table can be edited in DBEditFrame?
            if self.dbe.ShowModal() == wx.ID_OK:
                HPId = self.dbe.theId
            else:
                HPId = -1
                print "PanelHP: no HP selected after DA1 -> check whether this works"

        elif (mode == "AUTOMATIC"):
            HPId = HPList[0]    #in automatic mode just take first in the list

        elif (mode == "CANCEL"):
            HPId = -1 #make designAssistant2 to understand that
        else:
            print "PanelHP (DesignAssistant-Button): erroneous panel mode: ",mode

#..............................................................................
# Step 2 design assistant: add selected equipment to the list and update display
        
        self.mod.designAssistant2(HPId)
        self.display()

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnButtonpageHPAddButton(self, event):
#------------------------------------------------------------------------------		
#   adds an equipment to the list
#------------------------------------------------------------------------------		
        try:                #creates space for new equipment in Q/C
	    (self.equipe,self.equipeC) = self.mod.addEquipmentDummy()
	except:
            print "PanelHP (HPAddButton): could not create equipment dummy"
	    pass
        
        #show pop-up menu for adding equipment
        #TS20080405 FIXME put dbheatpump table here just for testing! Should be replaced by the
	#right table when it is created
	# the args are:
	# 1. the module address
	# 2. Title for the dialogs (for both AddEquipment and DBEditFrame)
	# 3. The name of the db table (for DBEditFrame)
	# 4. The column from a table whose value will be eventually returned by DBEditFrame. Must
	#    be an integer.
	# 5. If the database can be edited in DBEditFrame
	#
	# On return, the value in the specified column (arg 4) in the selected row is available
	# in pu1.theId, if a selection from the grid was made. If not, pu1.theId is -1. 
	# The selection is made clicking once in any field of the grid and then clicking on the
	# 'ok' button, or just double-clicking on any field.
	#
	# If the database is editable in DBEditFrame (arg 5), the background color of the
	# grid will be a tone of Yellow. If not, a tone of Cyan.
	#

        pu1 =  AddEquipment(self,                      # pointer to this panel
			    self.mod,                # pointer to the associated module
			    'Add Heat Pump equipment', # title for the dialogs
			    'dbheatpump',              # database table
			    0,                         # column to be returned
			    False)                     # database table can be edited in DBEditFrame?

        if pu1.ShowModal() == wx.ID_OK:
            print 'PanelHP AddEquipment accepted. Id='+str(pu1.theId)
        else:
            self.mod.deleteEquipment(None)

#        self.mod.calculateCascade()    
        self.display()


#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnGridPageHPGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
#       edits the selected equipment
#------------------------------------------------------------------------------		
        print "Grid - left button Dclick: here I should call the Q4H"
        rowNo = event.GetRow() #number of the selected boiler should be detected depending on the selected row
        EqId = self.mod.getEqId(rowNo)
        print "now editing equipment in row %s with id = "%rowNo,EqId
#        self.Hide()
	dialog = ManualAddDialog(self, EqId)

#Tom: here should be a link between the outcome of the dialog and what continues
        if (dialog.ShowModal() ==wx.ID_OK):
            print "PanelHP (OnGridLeftDclick) - OK"
#            ret = self.mod.calculateCascade()

        self.display()

#------------------------------------------------------------------------------		
    def OnGridPageHPGridCellRightClick(self, event):
#------------------------------------------------------------------------------		
#   right double click
#   --> for the moment only DELETE foreseen !!!
#------------------------------------------------------------------------------		

        rowNo = event.GetRow() #number of the selected boiler should be detected depending on the selected row

        print "Grid - right button click: scroll-up should appear"
        #here a scroll-up should appear with some options: edit, delete,...
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
#   Event handlers: parameter change in design assistant
#------------------------------------------------------------------------------		

    def OnCbConfig1Checkbox(self, event):
        self.config[0] = self.cbConfig1.GetValue()
        print "new config[%s] value: "%0,self.config[0]
        Interfaces.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

    def OnChoiceConfig2Choice(self, event):
        self.config[1] = TYPELIST[self.choiceConfig2.GetSelection()]
        print "new config[%s] value: "%1,self.config[1]
        Interfaces.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

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

#------------------------------------------------------------------------------		
#   Default event handlers: FWD / BACK / OK / Cancel - Buttons
#------------------------------------------------------------------------------		

    def OnButtonpageHeatPumpBackButton(self, event):
        self.Hide
        self.main.tree.SelectItem(self.main.qHC, select=True)
        event.Skip()

    def OnButtonpageHeatPumpFwdButton(self, event):
        self.Hide
        self.main.tree.SelectItem(self.main.qBB, select=True)
        event.Skip()

    def OnButtonpageBBOkButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)
        event.Skip()

    def OnButtonpageBBCancelButton(self, event):
        print "Button exitModuleCancel: CANCEL Option not yet foreseen"

#============================================================================== 				

        

