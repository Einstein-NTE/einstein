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
#	Version No.: 0.08
#	Created by: 	    Hans Schweiger	    February 2008
#	Last revised by:    Hans Schweiger          24/03/2008
#                           Hans Schweiger          03/04/2008
#                           Tom Sobota              05/04/2008
#                           Hans Schweiger          16/04/2008
#                           Hans Schweiger          29/04/2008
#                           Stoyan Danov            18/06/2008
#                           Hans Schweiger          03/07/2008
#
#       Changes to previous version:
#       - structure of plots identical to that of HP
#       03/04/2008:         Adaptation to structure Modules
#       05/04/08    changed call to popup1 in OnButtonpageHPAddButton
#                   slight change to OK and Cancel buttons, to show the right icons
#       16/04/2008: HS  main as argument in __init__
#       29/04/2008: HS  method draw for panelBBFig
#       18/06/2008 SD: change to translatable text _(...)
#       03/07/2008: HS  change in display: call to updatePanel instead of
#                       initPanel
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
from einstein.modules.messageLogger import *
from GUITools import *
from numCtrl import *


[wxID_PANELBB, wxID_PANELBBBBCALCULATE, wxID_PANELBBBUTTONPAGEBBADD, 
 wxID_PANELBBBUTTONPAGEBBBACK, wxID_PANELBBBUTTONPAGEBBCANCEL, 
 wxID_PANELBBBUTTONPAGEBBFWD, wxID_PANELBBBUTTONPAGEBBOK, 
 wxID_PANELBBCBCONFIG1, wxID_PANELBBCBCONFIG3, wxID_PANELBBCHOICECONFIG4, 
 wxID_PANELBBGRID, wxID_PANELBBPANELFIG, wxID_PANELBBST12PAGEBB, 
 wxID_PANELBBST1PAGEBB, wxID_PANELBBST2PAGEBB, wxID_PANELBBST3PAGEBB, 
 wxID_PANELBBST4PAGEBB, wxID_PANELBBSTATICTEXT1, wxID_PANELBBSTINFO2_T3, 
 wxID_PANELBBSTCONFIG3, wxID_PANELBBSTCONFIG4, wxID_PANELBBSTCONFIG5, 
 wxID_PANELBBSTCONFIG6, wxID_PANELBBSTCONFIG7, wxID_PANELBBSTINFO1, 
 wxID_PANELBBSTINFO1VALUE, wxID_PANELBBSTINFO2, wxID_PANELBBSTINFO2VALUE, wxID_PANELBBSTINFO2_P1,   ####E.F. 01/08
 wxID_PANELBBSTINFO2_P2, wxID_PANELBBSTINFO2_P3, wxID_PANELBBSTINFO2_T1, 
 wxID_PANELBBSTINFO2_T2, wxID_PANELBBSTINFO2A, wxID_PANELBBTCCONFIG2, 
 wxID_PANELBBTCCONFIG5, wxID_PANELBBTCCONFIG6, wxID_PANELBBTCCONFIG7, 
] = [wx.NewId() for _init_ctrls in range(38)]

# constants
#

MAXROWS = 50
TABLECOLS = 6

TYPELIST = BBTYPES
FUELLIST = [_("Natural Gas"),\
            _("Biomass"),\
            _("Fuel oil")]

#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		
    if hasattr(self, 'subplot'):
        del self.subplot
    self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.plot(Interfaces.GData['BB Plot'][0],
                      Interfaces.GData['BB Plot'][1],
                      '--', color = MIDDLEGREY, label='QD [80ºC]')
    self.subplot.plot(Interfaces.GData['BB Plot'][0],
                      Interfaces.GData['BB Plot'][2],
                      ':', color = DARKGREY, label='QD [140ºC]')
    self.subplot.plot(Interfaces.GData['BB Plot'][0],
                      Interfaces.GData['BB Plot'][3],
                      '-', color = ORANGE, label='QD [Tmax]', linewidth=2)
#    self.subplot.axis([0, 100, 0, 3e+7])
    self.subplot.legend()

    self.subplot.axes.set_ylabel(_('Heat demand [kW]'))
    self.subplot.axes.set_xlabel(_('Cumulative hours [h]'))
    
    for label in self.subplot.axes.get_yticklabels():
#        label.set_color(self.params['ytickscolor'])
        label.set_fontsize(8)
#        label.set_rotation(self.params['yticksangle'])
    #
    # properties of labels on the x axis
    #
    for label in self.subplot.axes.get_xticklabels():
#        label.set_color(self.params['xtickscolor'])
        label.set_fontsize(8)
#        label.set_rotation(self.params['xticksangle'])

    try:
        lg = self.subplot.get_legend()
        ltext  = lg.get_texts()             # all the text.Text instance in the legend
        for txt in ltext:
            txt.set_fontsize(10)  # the legend text fontsize
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
        self.mod.initPanel()
        
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
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))

        key = self.keys[0]
        (rows,cols) = (MAXROWS,TABLECOLS)
        self.grid.CreateGrid(MAXROWS, cols)

        self.grid.EnableGridLines(True)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetColSize(0,115)
        self.grid.SetColSize(2,60)
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _("Short name"))
        self.grid.SetColLabelValue(1, _("Nom. power"))
        self.grid.SetColLabelValue(2, _("COP"))
        self.grid.SetColLabelValue(3, _("Type"))
        self.grid.SetColLabelValue(4, _("Operating\nhours"))
        self.grid.SetColLabelValue(5, _("Year manufact."))
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
        wx.Panel.__init__(self, id=wxID_PANELBB, name='PanelBB', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)


#..............................................................................
# box1: table
        self.box1 = wx.StaticBox(self, -1, _("Boilers and Burners in the HC Supply System"),
                                 pos = (10,10),size=(420,220))
        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid = wx.grid.Grid(id=wxID_PANELBBGRID, name='gridpageBB',
              parent=self, pos=wx.Point(40, 48), size=wx.Size(376, 168),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageBBGridCellLeftDclick, id=wxID_PANELBBGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageBBGridCellRightClick, id=wxID_PANELBBGRID)

#..............................................................................
# box2: figure

        self.box2 = wx.StaticBox(self, -1, _("Cumulative heat demand to be covered by boilers"),
                                 pos = (440,10),size=(350,270))
        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelFig = wx.Panel(id=wxID_PANELBBPANELFIG, name='panelFig', parent=self,
              pos=wx.Point(450, 40), size=wx.Size(320, 220),
              style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)


#..............................................................................
#   action buttons

        self.BBCalculate = wx.Button(id=wxID_PANELBBBBCALCULATE,
              label=_('run design assistant'), name='BB_Calculate', parent=self,
              pos=wx.Point(232, 240), size=wx.Size(184, 24), style=0)
        self.BBCalculate.Bind(wx.EVT_BUTTON, self.OnBBCalculateButton,
              id=wxID_PANELBBBBCALCULATE)

        self.buttonpageBBAdd = wx.Button(id=wxID_PANELBBBUTTONPAGEBBADD,
              label=_('add boiler / burner'), name='buttonpageBBAdd', parent=self,
              pos=wx.Point(32, 240), size=wx.Size(184, 24), style=0)
        self.buttonpageBBAdd.Bind(wx.EVT_BUTTON, self.OnButtonpageBBAddButton,
              id=wxID_PANELBBBUTTONPAGEBBADD)

#..............................................................................
# box 3     Configuration design assistant

        self.box3 = wx.StaticBox(self, -1, _("Design assistant options:"),
                                 pos = (10,270),size=(420,300))
        self.box3.SetForegroundColour(TITLE_COLOR)
        self.box3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

#..............................................................................
# 1. Maintain existing equipment ?

        self.st3pageBB = wx.StaticText(id=-1,
              label=_('Maintain existing equipment ?'), name='st3pageBB',
              parent=self, pos=wx.Point(40, 304), style=0)
        self.cbConfig1 = wx.CheckBox(id=wxID_PANELBBCBCONFIG1, label='',
              name='cbConfig1', parent=self, pos=wx.Point(288, 304),
              size=wx.Size(16, 16), style=0)
        self.cbConfig1.Bind(wx.EVT_CHECKBOX, self.OnCbConfig1Checkbox,
              id=wxID_PANELBBCBCONFIG1)

#..............................................................................
# 2. Safety factor

        self.st4pageBB = wx.StaticText(id=-1, label=_('Safety factor [%]'),
              name='st4pageBB', parent=self, pos=wx.Point(40, 344), style=0)

        self.tcConfig2 = wx.TextCtrl(id=wxID_PANELBBTCCONFIG2, name='tcConfig2',
              parent=self, pos=wx.Point(288, 336), size=wx.Size(128, 24),
              style=0, value='')
        self.tcConfig2.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig2TextEnter,
              id=wxID_PANELBBTCCONFIG2)


#..............................................................................
# 3. Redundancy necessary ?

        self.stConfig3 = wx.StaticText(id=-1, label=_('Is redundancy necessary ?'),
              name='stConfig3', parent=self, pos=wx.Point(40, 384), style=0)

        self.cbConfig3 = wx.CheckBox(id=wxID_PANELBBCBCONFIG3, label='',
              name='cbConfig3', parent=self, pos=wx.Point(288, 388),
              size=wx.Size(24, 13), style=0)
        self.cbConfig3.Bind(wx.EVT_CHECKBOX, self.OnCbConfig3Checkbox,
              id=wxID_PANELBBCBCONFIG3)


#..............................................................................
# 4. choose fuel

        self.stConfig4 = wx.StaticText(id=-1, label=_('Fuel Type'),
              name='stConfig4', parent=self, pos=wx.Point(40, 424), style=0)
        self.choiceConfig4 = wx.Choice(choices=FUELLIST,
              id=wxID_PANELBBCHOICECONFIG4, name='choiceConfig4', parent=self,
              pos=wx.Point(288, 416), size=wx.Size(128, 21), style=0)
        self.choiceConfig4.Bind(wx.EVT_CHOICE, self.OnChoiceConfig4Choice,
              id=wxID_PANELBBCHOICECONFIG4)

#..............................................................................
# 5. minimum operation hours

        self.stConfig5 = wx.StaticText(id=-1,
              label=_('Minimum operating hours (baseload boiler)'),
              name='stConfig5', parent=self, pos=wx.Point(40, 464), style=0)

        self.tcConfig5 = wx.TextCtrl(id=wxID_PANELBBTCCONFIG5, name='tcConfig5', parent=self,
              pos=wx.Point(288, 456), size=wx.Size(128, 24), style=0, value='')
        self.tcConfig5.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig5TextEnter,
              id=wxID_PANELBBTCCONFIG5)

#..............................................................................
# 5. minimum boiler power

        self.stConfig6 = wx.StaticText(id=-1, label=_('Minimum boiler power [kW]'),
              name='stConfig6', parent=self, pos=wx.Point(40, 504), style=0)

        self.tcConfig6 = wx.TextCtrl(id=wxID_PANELBBTCCONFIG6, name='tcConfig6',
              parent=self, pos=wx.Point(288, 496), size=wx.Size(128, 24),
              style=0, value='')
        self.tcConfig6.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig6TextEnter,
              id=wxID_PANELBBTCCONFIG6)

#..............................................................................
# 5. minimum efficiency

        self.stConfig7 = wx.StaticText(id=-1,
              label=_('Minimum effiency allowed [%]'), name='stConfig7',
              parent=self, pos=wx.Point(40, 544), style=0)

        self.tcConfig7 = wx.TextCtrl(id=wxID_PANELBBTCCONFIG7, name='tcConfig7',
              parent=self, pos=wx.Point(288, 544), size=wx.Size(128, 21),
              style=0, value='')
        self.tcConfig7.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig7TextEnter,
              id=wxID_PANELBBTCCONFIG7)

#..............................................................................
# box 4     Info field

        self.box4 = wx.StaticBox(self, -1, _("System Performance Data"),
                                 pos = (440,320),size=(350,200))
        self.box4.SetForegroundColour(TITLE_COLOR)
        self.box4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))


        self.stInfo1 = wx.StaticText(id=wxID_PANELBBSTINFO1,
              label=_('Maximum demand temperature [°C]'), name='stInfo1', parent=self,
              pos=wx.Point(460, 352), style=0)
        self.stInfo1Value = wx.StaticText(id=wxID_PANELBBSTINFO1VALUE,
              label='-', name='stInfo1Value', parent=self, pos=wx.Point(660,
              352), style=0)

        self.stInfo2 = wx.StaticText(id=wxID_PANELBBSTINFO2,
              label=_('Residual power to be supplied [kW]'), name='stInfo2',
              parent=self, pos=wx.Point(460, 372), style=0)

        self.stInfo2Value = wx.StaticText(id=wxID_PANELBBSTINFO2VALUE,                    #### E.F. 01/08
              label='0', name='stInfo2Value', parent=self, pos=wx.Point(660,
              372), style=0)




        self.stInfo2a = wx.StaticText(id=wxID_PANELBBSTINFO2A,
              label=_('Temperature [\xbaC]'), name='stInfo3', parent=self,
              pos=wx.Point(504, 416), style=0)
        self.stInfo2b = wx.StaticText(id=-1, label=_('Peak demand [kW]'),
              name='stInfo2b', parent=self, pos=wx.Point(616, 416), style=0)

        self.stInfo2_T1 = wx.StaticText(id=wxID_PANELBBSTINFO2_T1, label=_('Up to 80'),
              name='stInfo2_T1', parent=self, pos=wx.Point(504, 440), style=0)

        self.stInfo2_T2 = wx.StaticText(id=wxID_PANELBBSTINFO2_T2, label=_('80<T<140'),
              name='stInfo2_T2', parent=self, pos=wx.Point(504, 464), style=0)

        self.stInfo2_T3 = wx.StaticText(id=wxID_PANELBBSTINFO2_T3, label=_('T<Tmax'),
#        self.stInfo2_T3 = wx.StaticText(id=wxID_PANELBBSTINFO2_T3, label=_('140<T<Tmax'),
              name='staticText3', parent=self, pos=wx.Point(504, 488), style=0)

        self.stInfo2_P1 = wx.StaticText(id=wxID_PANELBBSTINFO2_P1, label=_('0'),
              name='stInfo2_P1', parent=self, pos=wx.Point(616, 440), style=0)

        self.stInfo2_P2 = wx.StaticText(id=wxID_PANELBBSTINFO2_P2, label=_('0'),
              name='stInfo2_P2', parent=self, pos=wx.Point(616, 464), style=0)

        self.stInfo2_P3 = wx.StaticText(id=wxID_PANELBBSTINFO2_P3, label=_('0'),
              name='stInfo2_P3', parent=self, pos=wx.Point(616, 488), style=0)

#------------------------------------------------------------------------------		
#       Default action buttons: FWD / BACK / OK / Cancel

#------------------------------------------------------------------------------		
        self.buttonpageBBOk = wx.Button(id=wx.ID_OK, label=_('OK'),
              name='buttonpageBBOk', parent=self, pos=wx.Point(528, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageBBOk.Bind(wx.EVT_BUTTON, self.OnButtonpageBBOkButton,
              id=wx.ID_OK)

        self.buttonpageBBCancel = wx.Button(id=wx.ID_CANCEL, label=_('Cancel'),
              name='buttonpageBBCancel', parent=self, pos=wx.Point(616, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageBBCancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpageBBCancelButton, id=wx.ID_CANCEL)

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

#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   function activated on each entry into the panel from the tree
#------------------------------------------------------------------------------		

        self.mod.updatePanel()        # prepares data for plotting

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

# emptying cells
        for r in range(rows,MAXROWS):
            for c in range(cols):
                self.grid.SetCellValue(r, c, "")

#..............................................................................
# update of design assistant parameters

        self.config = Interfaces.GData["BB Config"]
        
        try:
            if self.config[0] == 1:
                self.cbConfig1.SetValue(True)
            elif self.config[0] == 0:
                self.cbConfig1.SetValue(False)
        except:
            logTrack("PanelBB: problem loading config[0] value %s "%self.config[0])

        try: self.tcConfig2.SetValue(str(self.config[1]))
        except:
            logTrack("PanelBB: problem loading config[1] value %s "%self.config[1])

        try:
            if self.config[2] == 1:
                self.cbConfig3.SetValue(True)
            elif self.config[2] == 0:
                self.cbConfig3.SetValue(False)
        except:
            logTrack("PanelBB: problem loading config[2] value %s "%self.config[2])

        try:        #try-except necessary if there comes a string that is not in list.
            self.choiceConfig4.SetSelection(0)
#            self.choiceConfig4.SetSelection(TYPELIST.index(self.config[1]))
        except:
            print _("PanelBB (display): was asked to display an erroneous heat pump type"),self.config[1]
            pass

        self.tcConfig5.SetValue(str(self.config[4]))
        self.tcConfig6.SetValue(str(self.config[5]))
        self.tcConfig7.SetValue(str(self.config[6]))
        
#..............................................................................
# update of info-values

        self.info = Interfaces.GData["BB Info"]
        
        self.stInfo1Value.SetLabel(convertDoubleToString(self.info[0]))
        self.stInfo2Value.SetLabel(convertDoubleToString(self.info[1]))
        self.stInfo2_P1.SetLabel(convertDoubleToString(self.info[2]))
        self.stInfo2_P2.SetLabel(convertDoubleToString(self.info[3]))
        self.stInfo2_P3.SetLabel(convertDoubleToString(self.info[4]))

        self.Hide()
        try: self.panelFig.draw()
        except: pass
        
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
        self.mod.designAssistant()
        
        self.display()

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnButtonpageBBAddButton(self, event):
#------------------------------------------------------------------------------		
#   adds an equipment to the list
#------------------------------------------------------------------------------		

	self.equipe = self.mod.addEquipmentDummy() #SD change 30/04/2008, delete equipeC
        pu1 =  AddEquipment(self,                      # pointer to this panel
                            self.mod,                # pointer to the associated module
                            'Add boiler equipment', # title for the dialogs
                            'dbboiler',              # database table
                            0,                         # column to be returned
                            False)                     # database table can be edited in DBEditFrame?

        if pu1.ShowModal() == wx.ID_OK:
            print _('PanelBB AddEquipment accepted. Id=')+str(pu1.theId)
        else:
            self.mod.deleteEquipment(None)
        self.display()

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
            pu2 =  DialogOK(self,_("delete equipment"),_("do you really want to delete this equipment ?"))
            if pu2.ShowModal() == wx.ID_OK:
                self.mod.deleteEquipment(rowNo)
                self.display()
                
        elif (ret == _("edit")):
            OnGridPageBBGridCellLeftDclick(self,event)
        
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
#   Event handlers: parameter change in design assistant
#------------------------------------------------------------------------------		
    def OnCbConfig1Checkbox(self, event):
        val = self.cbConfig1.GetValue()
        if val == True:
            self.config[0] = 1
        elif val == False:
            self.config[0] = 0
        else:
            self.config[0] = None
            
        print _("PanelBB: new config[%s] value: ")%0,self.config[0]
        Interfaces.GData["BB Config"] = self.config
        self.mod.setUserDefinedPars()

    def OnTcConfig2TextEnter(self, event):
        self.config[1] = self.tcConfig2.GetValue()
        print _("PanelBB: new config[%s] value: ")%1,self.config[1]
        Interfaces.GData["HP Config"] = self.config
        self.mod.setUserDefinedPars()

    def OnCbConfig3Checkbox(self, event):
        val = self.cbConfig3.GetValue()
        if val == True:
            self.config[2] = 1
        elif val == False:
            self.config[2] = 0
        else:
            self.config[2] = None
        print _("PanelBB: new config[%s] value: ")%2,self.config[2]
        Interfaces.GData["BB Config"] = self.config
        self.mod.setUserDefinedPars()

    def OnChoiceConfig4Choice(self, event):
        self.config[3] = FUELLIST[self.choiceConfig4.GetSelection()]
        print _("PanelBB: new config[%s] value: ")%3,self.config[3]
        Interfaces.GData["HP Config"] = self.config[3]
        self.mod.setUserDefinedPars()

    def OnTcConfig5TextEnter(self, event):
        self.config[4] = self.tcConfig5.GetValue()
        print _("PanelBB: new config[%s] value: ")%4,self.config[4]
        Interfaces.GData["HP Config"] = self.config
        self.mod.setUserDefinedPars()

    def OnTcConfig6TextEnter(self, event):
        self.config[5] = self.tcConfig6.GetValue()
        print _("PanelBB: new config[%s] value: ")%5,self.config[5]
        Interfaces.GData["HP Config"] = self.config
        self.mod.setUserDefinedPars()

    def OnTcConfig7TextEnter(self, event):
        self.config[6] = self.tcConfig7.GetValue()
        print _("PanelBB: new config[%s] value: ")%6,self.config[6]
        Interfaces.GData["HP Config"] = self.config
        self.mod.setUserDefinedPars()


#==============================================================================
#   <<< OK Cancel >>>
#==============================================================================

    def OnButtonpageBBOkButton(self, event):
        self.main.tree.SelectItem(self.main.qHC, select=True)
        self.Hide()

    def OnButtonpageBBCancelButton(self, event):
        print _("Button exitModuleCancel: CANCEL Option not yet foreseen")

    def OnButtonpageBBBackButton(self, event):
        self.main.tree.SelectItem(self.main.qHP, select=True)
        self.Hide()

    def OnButtonpageBBFwdButton(self, event):
        self.main.tree.SelectItem(self.main.qEnergy, select=True)
        self.Hide()
