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
#	Version No.: 0.13
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
#                           Hans Schweiger          25/04/2008
#                           Hans Schweiger          29/04/2008
#                           Stoyan Danov            30/04/2008
#                           Stoyan Danov            22/05/2008
#                           Stoyan Danov            18/06/2008
#                           Hans Schweiger          28/06/2008
#                           Stoyan Danov    13/10/2008
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
#       25/04/08:   Some clean-up in adding HP manually
#       29/04/08:   call to method "draw" for panelHPFig added
#       30/04/08:   in OnButtonpageHPAddButton: delete equipeC in assignment of addEquipmentDummy
#       22/05/08:   in drawFigure: Interfaces -> Status.int
#       18/06/2008 SD: change to translatable text _(...)
#       28/06/2008: HS  eliminated sql and db as input parameters; minor clean-up.
#                   - bug-fix in read/write of HP type
#       13/10/2008: SD  change _() to _U()
#       15/02/2010 MW: fixed visualization
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
from GUITools import *

from einstein.modules.interfaces import *
from einstein.modules.modules import *
from einstein.modules.constants import *
from numpy import *
from numCtrl import *
from einstein.GUI.addEquipment_popup import * #TS 20080405 changed
import matplotlib.font_manager as font
from matplotlib.ticker import FuncFormatter

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
axeslabel_fontsize = 10
axesticks_fontsize = 8
legend_fontsize = 10
spacing_left = 0.2
spacing_right = 0.9
spacing_bottom = 0.2
spacing_top = 0.85

MAXROWS = 50
COLNO = 6

TYPELIST = TRANSHPTYPES.values()

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

#------------------------------------------------------------------------------		
#HS2008-03-22: 
#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		
    if hasattr(self, 'subplot'):
        del self.subplot
    self.subplot = self.figure.add_subplot(1,1,1)
    self.figure.subplots_adjust(left=spacing_left, right=spacing_right, bottom=spacing_bottom, top=spacing_top)

    self.subplot.plot(Status.int.GData['HP Plot'][0],
                      Status.int.GData['HP Plot'][1],
                      color = DARKGREY, label='QD', linewidth=2)
    self.subplot.plot(Status.int.GData['HP Plot'][0],
                      Status.int.GData['HP Plot'][2],
                      '--', color = DARKGREY, label='QA')
    self.subplot.plot(Status.int.GData['HP Plot'][0],
                      Status.int.GData['HP Plot'][3],
                      color = ORANGE,label='QDres', linewidth=2)
    self.subplot.plot(Status.int.GData['HP Plot'][0],
                      Status.int.GData['HP Plot'][4],
                      '--', color = ORANGE, label='QAres')
#    self.subplot.axis([0, 100, 0, 3e+7])
    self.subplot.legend()

    major_formatter = FuncFormatter(format_int_wrapper)
    self.subplot.axes.xaxis.set_major_formatter(major_formatter)
    self.subplot.axes.yaxis.set_major_formatter(major_formatter)
    fp = font.FontProperties(size = axeslabel_fontsize)
    self.subplot.axes.set_ylabel(_U('Yearly energy [MWh]'), fontproperties=fp)
    self.subplot.axes.set_xlabel(_U(u'Temperature [ºC]'), fontproperties=fp)
    
    for label in self.subplot.axes.get_yticklabels():
#        label.set_color(self.params['ytickscolor'])
        label.set_fontsize(axesticks_fontsize)
#        label.set_rotation(self.params['yticksangle'])
    #
    # properties of labels on the x axis
    #
    for label in self.subplot.axes.get_xticklabels():
#        label.set_color(self.params['xtickscolor'])
        label.set_fontsize(axesticks_fontsize)
#        label.set_rotation(self.params['xticksangle'])

    self.subplot.legend(loc = 'best')
    try:
        lg = self.subplot.get_legend()
        ltext  = lg.get_texts()             # all the text.Text instance in the legend
        for txt in ltext:
            txt.set_fontsize(legend_fontsize)  # the legend text fontsize
        # legend line thickness
        llines = lg.get_lines()             # all the lines.Line2D instance in the legend
        for lli in llines:
            lli.set_linewidth(1.5)          # the legend linewidth
        # color of the legend frame
        # this only works when the frame is painted (see below draw_frame)
        frame  = lg.get_frame()             # the patch.Rectangle instance surrounding the legend
        frame.set_facecolor('#F0F0F0')      # set the frame face color to light gray
        # should the legend frame be painted
        lg.draw_frame(False)
    except:
        # no legend
        pass


#------------------------------------------------------------------------------		
class PanelHP(wx.Panel):
#------------------------------------------------------------------------------		
#   Panel of the heat pump design assistant
#------------------------------------------------------------------------------		

    def __init__(self, parent, main, id, pos, size, style, name):

        print "PanelHP (__init__)"
        self.prnt = parent
        self.main = main

        self._init_ctrls(parent)

	self.keys = ['HP Table']
        self.mod = Status.mod.moduleHP
        self.mod.initPanel()        # prepares data for plotting
        
#        print "PanelHP (__init__): mod created",self.mod

#   graphic: Cumulative heat demand by hours
        labels_column = 0
        ignoredrows = []
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : self.keys[0],                # key for Interface
                   'title'       : _U('Some title'),           # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelHPFig, wx.Panel, drawFigure, paramList)
        del dummy

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
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.grid.CreateGrid(MAXROWS, COLNO)

        self.grid.EnableGridLines(True)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetDefaultColSize(120)
        self.grid.SetRowLabelSize(30)
        self.grid.SetColSize(0,140)
        self.grid.SetColSize(2,100)
        self.grid.SetColSize(5,100)
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Short name"))
        self.grid.SetColLabelValue(1, _U("Nom. power"))
        self.grid.SetColLabelValue(2, _U("COP"))
        self.grid.SetColLabelValue(3, _U("Type"))
        self.grid.SetColLabelValue(4, _U("Operating\nhours"))
        self.grid.SetColLabelValue(5, _U("Year manufact."))
        #
        # copy values from dictionary to grid
        #
        (rows,cols) = (MAXROWS,COLNO)
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

        self.boxFig = wx.StaticBox(id=-1,
              label=_U('Heat demand and availability with and w/o HP'),
              name='boxFig', parent=self, pos=wx.Point(440, 170),
              size=wx.Size(350, 260), style=0)
        self.boxFig.SetForegroundColour(TITLE_COLOR)
        self.boxFig.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelHPFig = wx.Panel(id=wxID_PANELHPFIG, name='panelHPFigure', parent=self,
              pos=wx.Point(450, 200), size=wx.Size(330, 220),
              style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)

#..............................................................................
# Grid for display of existing heat pumps

        self.boxTable = wx.StaticBox(id=-1,
              label=_U('Existing heat pumps in the system'),
              name='boxTable', parent=self, pos=wx.Point(10, 10),
              size=wx.Size(780, 140), style=0)
        self.boxTable.SetForegroundColour(TITLE_COLOR)
        self.boxTable.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid = wx.grid.Grid(id=wxID_PANELHPGRIDPAGEHP,
              name='gridpageHP', parent=self, pos=wx.Point(20, 40),
              size=wx.Size(760, 100), style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageHPGridCellLeftDclick, id=wxID_PANELHPGRIDPAGEHP)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageHPGridCellRightClick, id=wxID_PANELHPGRIDPAGEHP)


#------------------------------------------------------------------------------		
#       Action buttons and text entry
#------------------------------------------------------------------------------		

# Button "run design assistant"
        self.hpCalculate = wx.Button(id=wxID_PANELHPHPCALCULATE,
              label=_U('Run design assistant'), name='HP_Calculate', parent=self,
              pos=wx.Point(220, 160), size=wx.Size(180, 24), style=0)

        self.hpCalculate.Bind(wx.EVT_BUTTON, self.OnHpCalculateButton,
              id=wxID_PANELHPHPCALCULATE)

# Button "add heat pump"
        self.buttonpageHeatPumpAdd = wx.Button(id=-1,
              label=_U('add heat pump manually'), name='buttonpageHeatPumpAdd',
              parent=self, pos=wx.Point(20, 160), size=wx.Size(180, 24),
              style=0)
        self.buttonpageHeatPumpAdd.Bind(wx.EVT_BUTTON, self.OnButtonpageHPAddButton,
              id=-1)

#------------------------------------------------------------------------------		
#       Configuration design assistant
#------------------------------------------------------------------------------		

        self.boxDA = wx.StaticBox(id=-1,
              label=_U('Configuration of design assistant'),
              name='boxDA', parent=self, pos=wx.Point(10, 250),
              size=wx.Size(420, 320), style=0)
        self.boxDA.SetForegroundColour(TITLE_COLOR)
        self.boxDA.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

#..............................................................................
# 1. Maintain existing equipment ?

        self.stConfig1 = wx.StaticText(id=-1,
              label=_U('Maintain existing equipment ?'), name='stConfig1',
              parent=self, pos=wx.Point(40, 304), style=0)

        self.cbConfig1 = wx.CheckBox(id=-1, label='',
              name='cbConfig1', parent=self, pos=wx.Point(288, 308),
              size=wx.Size(24, 13), style=0)

        self.cbConfig1.Bind(wx.EVT_CHECKBOX, self.OnCbConfig1Checkbox,
              id=-1)

#..............................................................................
# 2. Heat pump type 

        self.stConfig2 = wx.StaticText(id=-1, label=_U('Type of heat pump'),
              name='stConfig2', parent=self, pos=wx.Point(40, 344),
              style=0)

        self.choiceConfig2 = wx.Choice(choices=TYPELIST, id=-1, name='choicepageHeatPump', parent=self,
              pos=wx.Point(288, 336), size=wx.Size(130, 21), style=0)

        self.choiceConfig2.Bind(wx.EVT_CHOICE, self.OnChoiceConfig2Choice,
              id=-1)

#..............................................................................
# 3. Minimum operating hours

        self.stConfig3 = wx.StaticText(id=-1,
              label=_U('Minimum desired annual operation hours, h'),
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
              label=_U(u'Maximum desired temperature lift, ºC'),
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
              label=_U(u'Maximum desired condensing temperature, ºC'),
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
              label=_U(u'Minimum desired evaporating temperature, ºC'),
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
              label=_U('Only for absorption type:'), name='stConfig7a',
              parent=self, pos=wx.Point(40, 536), style=0)

        self.stConfig7b = wx.StaticText(id=-1,
              label=_U(u'Inlet temperature of heating fluid in generator, ºC'),
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
              label=_U(u'Pinch temperature [ºC]'), name='stInfo1',
              parent=self, pos=wx.Point(440, 460), style=0)

        self.tcInfo1 = wx.TextCtrl(id=-1, name='tcInfo1',
              parent=self, pos=wx.Point(640, 460), size=wx.Size(128, 21),
              style=0, value="")

        self.stInfo2 = wx.StaticText(id=-1,
              label=_U('Temperature gap [K]'), name='stInfo2',
              parent=self, pos=wx.Point(440, 500), style=0)

        self.tcInfo2 = wx.TextCtrl(id=-1, name='tcInfo2',
              parent=self, pos=wx.Point(640, 500), size=wx.Size(128, 21),
              style=0, value="")



#------------------------------------------------------------------------------		
#       Default action buttons: FWD / BACK / OK / Cancel
#------------------------------------------------------------------------------		

        self.buttonpageHeatPumpOk = wx.Button(id=wx.ID_OK, label=_U('OK'),
              name='buttonpageHeatPumpOk', parent=self, pos=wx.Point(528, 544),
              size=wx.Size(75, 23), style=0)

        self.buttonpageHeatPumpCancel = wx.Button(id=wx.ID_CANCEL, label=_U('Cancel'),
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
        self.mod.updatePanel()        # prepares data for plotting

#..............................................................................
# update of equipment table

        try:
            data = Status.int.GData[self.keys[0]]
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

#..............................................................................
# update of design assistant parameters

        self.config = Status.int.GData["HP Config"]
        self.cbConfig1.SetValue(self.config[0])
        
        if self.config[1] in TRANSHPTYPES.keys():
            self.choiceConfig2.SetStringSelection(TRANSHPTYPES[self.config[1]])
        else:
            self.main.logWarning(_U("PanelHP (display): was asked to display an erroneous heat pump type -> %s")%self.config[1])

        self.tcConfig3.SetValue(str(self.config[2]))
        self.tcConfig4.SetValue(str(self.config[3]))
        self.tcConfig5.SetValue(str(self.config[4]))
        self.tcConfig6.SetValue(str(self.config[5]))
        self.tcConfig7.SetValue(str(self.config[6]))
        
#..............................................................................
# update of info-values

        self.info = Status.int.GData["HP Info"]
        
        self.tcInfo1.SetValue(str(self.info[0]))
        self.tcInfo2.SetValue(str(self.info[1]))

        self.Hide()
        self.panelHPFig.draw()
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
        print "PanelHP: preselected heat pumps ",HPList
        
#..............................................................................
# In interactive mode open DB Edidor Heat pump and select manually

        if (mode == "MANUAL"):
            self.dbe = DBEditFrame(self,
                            _U('Select heat pump from preselected list'), # title for the dialogs
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
            logDebug("PanelHP (DesignAssistant-Button): erroneous panel mode: %s"%mode)

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

	self.equipe = self.mod.addEquipmentDummy() #SD change 30/04/2008, delete equipeC

        pu1 =  AddEquipment(self,                      # pointer to this panel
                            self.mod,                # pointer to the associated module
                            _U('Add Heat Pump equipment'), # title for the dialogs
                            _U('dbheatpump'),              # database table
                            0,                         # column to be returned
                            False)                     # database table can be edited in DBEditFrame?

        if pu1.ShowModal() == wx.ID_OK:
            print 'PanelHP AddEquipment accepted. Id='+str(pu1.theId)
        else:
            self.mod.deleteEquipment(None)

        self.display()

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnGridPageHPGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
#       edits the selected equipment
#------------------------------------------------------------------------------		

        rowNo = event.GetRow() #number of the selected boiler should be detected depending on the selected row
        EqId = self.mod.getEqId(rowNo)
	dialog = ManualAddDialog(self, EqId)

        if (dialog.ShowModal() ==wx.ID_OK):
            print "PanelHP (OnGridLeftDclick) - OK"

        self.display()

#------------------------------------------------------------------------------		
    def OnGridPageHPGridCellRightClick(self, event):
#------------------------------------------------------------------------------		
#   right double click
#   --> for the moment only DELETE foreseen !!!
#------------------------------------------------------------------------------		

        rowNo = event.GetRow() #number of the selected boiler should be detected depending on the selected row

        ret = "delete"

#..............................................................................
# "delete" selected:

        if (ret=="delete"):
            pu2 =  DialogOK(self,_U("delete equipment"),_U("do you really want to delete this equipment ?"))
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
        Status.int.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

    def OnChoiceConfig2Choice(self, event):
        newType = self.choiceConfig2.GetStringSelection()
        print "newType =",newType
        if newType in TRANSHPTYPES.values(): self.config[1] = findKey(TRANSHPTYPES,newType)
        print "new config[%s] value: "%1,self.config[1]
        Status.int.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

    def OnTcConfig3TextEnter(self, event):
        print "new config[%s] value: "%2,self.config[2]
        self.config[2] = self.tcConfig3.GetValue()
        Status.int.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

    def OnTcConfig4TextEnter(self, event):
        self.config[3] = self.tcConfig4.GetValue()
        print "new config[%s] value: "%3,self.config[3]
        Status.int.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

    def OnTcConfig5TextEnter(self, event):
        self.config[4] = self.tcConfig5.GetValue()
        print "new config[%s] value: "%4,self.config[4]
        Status.int.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

    def OnTcConfig6TextEnter(self, event):
        self.config[5] = self.tcConfig6.GetValue()
        print "new config[%s] value: "%5,self.config[5]
        Status.int.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

    def OnTcConfig7TextEnter(self, event):
        self.config[6] = self.tcConfig7.GetValue()
        print "new config[%s] value: "%6,self.config[6]
        Status.int.GData["HP Config"] = self.config
        self.mod.setUserDefinedParamHP()

#------------------------------------------------------------------------------		
#   Default event handlers: FWD / BACK / OK / Cancel - Buttons
#------------------------------------------------------------------------------		

    def OnButtonpageHeatPumpBackButton(self, event):
        self.Hide
        self.main.tree.SelectItem(self.main.qST, select=True)
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

        

