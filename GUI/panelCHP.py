#Boa:FramePanel:PanelCHP
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
#	Panel CHP (Combined Heat and Power)
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Panel for CHP design assistant
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	    05/09/2008
#                           based on PanelBB
#	Last revised by:
#                           Stoyan Danov    13/10/2008
#
#       Changes to previous version:
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
from numpy import *
from einstein.GUI.addEquipment_popup import AddEquipment #TS 20080405 changed

import einstein.modules.matPanel as Mp
from einstein.GUI.dialogOK import *

from einstein.modules.interfaces import *
from einstein.modules.constants import *
from einstein.modules.messageLogger import *
from GUITools import *
from numCtrl import *


[wxID_PANELCHP, wxID_PANELCHPCHPCALCULATE, wxID_PANELCHPBUTTONPAGECHPADD, 
 wxID_PANELCHPBUTTONPAGECHPBACK, wxID_PANELCHPBUTTONPAGECHPCANCEL, 
 wxID_PANELCHPBUTTONPAGECHPFWD, wxID_PANELCHPBUTTONPAGECHPOK, 
 wxID_PANELCHPCBCONFIG1, wxID_PANELCHPCHOICECONFIG2,wxID_PANELCHPCHOICECONFIG3, 
 wxID_PANELCHPGRID, wxID_PANELCHPPANELFIG, wxID_PANELCHPST12PAGECHP, 
 wxID_PANELCHPST1PAGECHP, wxID_PANELCHPST2PAGECHP, wxID_PANELCHPST3PAGECHP, 
 wxID_PANELCHPST4PAGECHP, wxID_PANELCHPSTATICTEXT1, wxID_PANELCHPSTINFO2_T3, wxID_PANELCHPSTINFO2_T4, 
 wxID_PANELCHPSTCONFIG3, wxID_PANELCHPSTCONFIG4, wxID_PANELCHPSTCONFIG5, 
 wxID_PANELCHPSTINFO1, 
 wxID_PANELCHPSTINFO1VALUE, wxID_PANELCHPSTINFO2, wxID_PANELCHPSTINFO2VALUE, wxID_PANELCHPSTINFO2_P1,   ####E.F. 01/08
 wxID_PANELCHPSTINFO2_P2, wxID_PANELCHPSTINFO2_P3, wxID_PANELCHPSTINFO2_P4, wxID_PANELCHPSTINFO2_T1, 
 wxID_PANELCHPSTINFO2_T2, wxID_PANELCHPSTINFO2A, wxID_PANELCHPTCCONFIG2, 
 wxID_PANELCHPTCCONFIG4, wxID_PANELCHPTCCONFIG5, 
] = [wx.NewId() for _init_ctrls in range(37)]

# constants
#

MAXROWS = 50
TABLECOLS = 6

def _U(text):
    return unicode(_(text),"utf-8")

TYPELIST = CHPTYPES
FUELLIST = [_U("Natural Gas"),\
            _U("Biomass"),\
            _U("Fuel oil")]

#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		
    if hasattr(self, 'subplot'):
        del self.subplot
    self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.plot(Interfaces.GData['CHP Plot'][0],
                      Interfaces.GData['CHP Plot'][2],
                      ':', color = MIDDLEGREY, label='QD [80 ºC]')
    self.subplot.plot(Interfaces.GData['CHP Plot'][0],
                      Interfaces.GData['CHP Plot'][3],
                      '-', color = MIDDLEGREY, label='QD [120 ºC]')
    self.subplot.plot(Interfaces.GData['CHP Plot'][0],
                      Interfaces.GData['CHP Plot'][4],
                      '--', color = DARKGREY, label='QD [250 ºC]')
    self.subplot.plot(Interfaces.GData['CHP Plot'][0],
                      Interfaces.GData['CHP Plot'][5],
                      '-', color = BLACK, label='QD [Total]', linewidth=2)
    self.subplot.plot(Interfaces.GData['CHP Plot'][0],
                      Interfaces.GData['CHP Plot'][1],
                      '-', color = ORANGE, label='CHP', linewidth=2)
#    self.subplot.axis([0, 100, 0, 3e+7])
    self.subplot.legend()

    self.subplot.axes.set_ylabel(_U('Heat demand [kW]'))
    self.subplot.axes.set_xlabel(_U('Cumulative hours [h]'))
    
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
class PanelCHP(wx.Panel):
#------------------------------------------------------------------------------		
#   Panel of the boiler&burner design assistant
#------------------------------------------------------------------------------		

    def __init__(self, parent, main, id, pos, size, style, name):
        self.prnt = parent
        self.main = main
        self._init_ctrls(parent)
        
	self.keys = ['CHP Table']
        self.mod = Status.mod.moduleCHP
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
        self.grid.SetDefaultRowSize(40)
        self.grid.SetRowLabelSize(40)
        self.grid.SetColSize(0,115)
        self.grid.SetColSize(2,60)
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Short name"))
        self.grid.SetColLabelValue(1, _U("Nom. power\nel./th.[kW]"))
        self.grid.SetColLabelValue(2, _U("COP\nel./th. [-]"))
        self.grid.SetColLabelValue(3, _U("Type"))
        self.grid.SetColLabelValue(4, _U("Operating\nhours"))
        self.grid.SetColLabelValue(5, _U("Year manufact."))
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
        wx.Panel.__init__(self, id=wxID_PANELCHP, name='PanelCHP', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)


#..............................................................................
# box1: table
        self.box1 = wx.StaticBox(self, -1, _U("CHP equipment in the HC Supply System"),
                                 pos = (10,10),size=(420,220))
        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid = wx.grid.Grid(id=wxID_PANELCHPGRID, name='gridpageCHP',
              parent=self, pos=wx.Point(40, 48), size=wx.Size(376, 168),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageCHPGridCellLeftDclick, id=wxID_PANELCHPGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageCHPGridCellRightClick, id=wxID_PANELCHPGRID)

#..............................................................................
# box2: figure

        self.box2 = wx.StaticBox(self, -1, _U("Cumulative heat demand to be covered by CHP"),
                                 pos = (440,10),size=(350,270))
        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelFig = wx.Panel(id=wxID_PANELCHPPANELFIG, name='panelFig', parent=self,
              pos=wx.Point(450, 40), size=wx.Size(320, 220),
              style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)


#..............................................................................
#   action buttons

        self.CHPCalculate = wx.Button(id=wxID_PANELCHPCHPCALCULATE,
              label=_U('run design assistant'), name='CHP_Calculate', parent=self,
              pos=wx.Point(232, 240), size=wx.Size(184, 24), style=0)
        self.CHPCalculate.Bind(wx.EVT_BUTTON, self.OnCHPCalculateButton,
              id=wxID_PANELCHPCHPCALCULATE)

        self.buttonpageCHPAdd = wx.Button(id=wxID_PANELCHPBUTTONPAGECHPADD,
              label=_U('add CHP system'), name='buttonpageCHPAdd', parent=self,
              pos=wx.Point(32, 240), size=wx.Size(184, 24), style=0)
        self.buttonpageCHPAdd.Bind(wx.EVT_BUTTON, self.OnButtonpageCHPAddButton,
              id=wxID_PANELCHPBUTTONPAGECHPADD)

#..............................................................................
# box 3     Configuration design assistant

        self.box3 = wx.StaticBox(self, -1, _U("Design assistant options:"),
                                 pos = (10,270),size=(420,300))
        self.box3.SetForegroundColour(TITLE_COLOR)
        self.box3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

#..............................................................................
# 1. Maintain existing equipment ?

        self.st3pageCHP = wx.StaticText(id=-1,
              label=_U('Maintain existing equipment ?'), name='st3pageCHP',
              parent=self, pos=wx.Point(40, 304), style=0)
        self.cbConfig1 = wx.CheckBox(id=wxID_PANELCHPCBCONFIG1, label='',
              name='cbConfig1', parent=self, pos=wx.Point(288, 304),
              size=wx.Size(16, 16), style=0)
        self.cbConfig1.Bind(wx.EVT_CHECKBOX, self.OnCbConfig1Checkbox,
              id=wxID_PANELCHPCBCONFIG1)

#..............................................................................
# 2. CHP Type

        self.stConfig2 = wx.StaticText(id=-1, label=_U('CHP System Type'),
              name='stConfig2', parent=self, pos=wx.Point(40, 344), style=0)
        self.choiceConfig2 = wx.Choice(choices=TRANSCHPTYPES.values(),
              id=wxID_PANELCHPCHOICECONFIG2, name='choiceConfig2', parent=self,
              pos=wx.Point(288, 336), size=wx.Size(128, 24), style=0)
        self.choiceConfig2.Bind(wx.EVT_CHOICE, self.OnChoiceConfig2Choice,
              id=wxID_PANELCHPCHOICECONFIG2)

#..............................................................................
# 3. Choose fuel

        self.stConfig3 = wx.StaticText(id=-1, label=_U('Fuel Type'),
              name='stConfig3', parent=self, pos=wx.Point(40, 384), style=0)
        self.choiceConfig3 = wx.Choice(choices=FUELLIST,
              id=wxID_PANELCHPCHOICECONFIG3, name='choiceConfig3', parent=self,
              pos=wx.Point(288, 376), size=wx.Size(128, 24), style=0)
        self.choiceConfig3.Bind(wx.EVT_CHOICE, self.OnChoiceConfig3Choice,
              id=wxID_PANELCHPCHOICECONFIG3)


#..............................................................................
# 5. minimum operation hours

        self.stConfig4 = wx.StaticText(id=-1,
              label=_U('Minimum operating hours'),
              name='stConfig4', parent=self, pos=wx.Point(40, 424), style=0)

        self.tcConfig4 = wx.TextCtrl(id=wxID_PANELCHPTCCONFIG5, name='tcConfig4', parent=self,
              pos=wx.Point(288, 416), size=wx.Size(128, 24), style=0, value='')
        self.tcConfig4.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig4TextEnter,
              id=wxID_PANELCHPTCCONFIG4)

#..............................................................................
# 5. minimum effective electrical efficiency

        self.stConfig5 = wx.StaticText(id=-1, label=_U('Min. electrical efficiency (ef.) [%]'),
              name='stConfig5', parent=self, pos=wx.Point(40, 464), style=0)

        self.tcConfig5 = wx.TextCtrl(id=wxID_PANELCHPTCCONFIG5, name='tcConfig5',
              parent=self, pos=wx.Point(288, 456), size=wx.Size(128, 24),
              style=0, value='')
        self.tcConfig5.Bind(wx.EVT_KILL_FOCUS, self.OnTcConfig5TextEnter,
              id=wxID_PANELCHPTCCONFIG5)

#..............................................................................
# box 4     Info field

        self.box4 = wx.StaticBox(self, -1, _U("System Performance Data"),
                                 pos = (440,320),size=(350,200))
        self.box4.SetForegroundColour(TITLE_COLOR)
        self.box4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))


        self.stInfo1 = wx.StaticText(id=wxID_PANELCHPSTINFO1,
              label=_U('CHP Operating hours'), name='stInfo1', parent=self,
              pos=wx.Point(460, 352), style=0)
        self.stInfo1Value = wx.StaticText(id=wxID_PANELCHPSTINFO1VALUE,
              label='-', name='stInfo1Value', parent=self, pos=wx.Point(660,
              352), style=0)

        self.stInfo2 = wx.StaticText(id=wxID_PANELCHPSTINFO2,
              label=_U('Effective electrical efficiency'), name='stInfo2',
              parent=self, pos=wx.Point(460, 372), style=0)

        self.stInfo2Value = wx.StaticText(id=wxID_PANELCHPSTINFO2VALUE,                    #### E.F. 01/08
              label='0', name='stInfo2Value', parent=self, pos=wx.Point(660,
              372), style=0)




        self.stInfo2a = wx.StaticText(id=wxID_PANELCHPSTINFO2A,
              label=_U('Temperature [\xbaC]'), name='stInfo3', parent=self,
              pos=wx.Point(504, 392), style=0)
        self.stInfo2b = wx.StaticText(id=-1, label=_U('Demand at min. op. hours [kW]'),
              name='stInfo2b', parent=self, pos=wx.Point(616, 392), style=0)

        self.stInfo2_T1 = wx.StaticText(id=wxID_PANELCHPSTINFO2_T1, label=_U('T< 80'),
              name='stInfo2_T1', parent=self, pos=wx.Point(504, 416), style=0)

        self.stInfo2_T2 = wx.StaticText(id=wxID_PANELCHPSTINFO2_T2, label=_U('T<140'),
              name='stInfo2_T2', parent=self, pos=wx.Point(504, 440), style=0)

        self.stInfo2_T3 = wx.StaticText(id=wxID_PANELCHPSTINFO2_T3, label=_U('T<250'),
              name='staticText3', parent=self, pos=wx.Point(504, 464), style=0)

        self.stInfo2_T4 = wx.StaticText(id=wxID_PANELCHPSTINFO2_T4, label=_U('Total'),
              name='staticText4', parent=self, pos=wx.Point(504, 488), style=0)

        self.stInfo2_P1 = wx.StaticText(id=wxID_PANELCHPSTINFO2_P1, label=_U('0'),
              name='stInfo2_P1', parent=self, pos=wx.Point(616, 416), style=0)

        self.stInfo2_P2 = wx.StaticText(id=wxID_PANELCHPSTINFO2_P2, label=_U('0'),
              name='stInfo2_P2', parent=self, pos=wx.Point(616, 440), style=0)

        self.stInfo2_P3 = wx.StaticText(id=wxID_PANELCHPSTINFO2_P3, label=_U('0'),
              name='stInfo2_P3', parent=self, pos=wx.Point(616, 464), style=0)

        self.stInfo2_P4 = wx.StaticText(id=wxID_PANELCHPSTINFO2_P4, label=_U('0'),
              name='stInfo2_P4', parent=self, pos=wx.Point(616, 488), style=0)

#------------------------------------------------------------------------------		
#       Default action buttons: FWD / BACK / OK / Cancel

#------------------------------------------------------------------------------		
        self.buttonpageCHPOk = wx.Button(id=wx.ID_OK, label=_U('OK'),
              name='buttonpageCHPOk', parent=self, pos=wx.Point(528, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageCHPOk.Bind(wx.EVT_BUTTON, self.OnButtonpageCHPOkButton,
              id=wx.ID_OK)

        self.buttonpageCHPCancel = wx.Button(id=wx.ID_CANCEL, label=_U('Cancel'),
              name='buttonpageCHPCancel', parent=self, pos=wx.Point(616, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageCHPCancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpageCHPCancelButton, id=wx.ID_CANCEL)

        self.buttonpageCHPFwd = wx.Button(id=wxID_PANELCHPBUTTONPAGECHPFWD,
              label='>>>', name='buttonpageCHPFwd', parent=self,
              pos=wx.Point(704, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageCHPFwd.Bind(wx.EVT_BUTTON, self.OnButtonpageCHPFwdButton,
              id=wxID_PANELCHPBUTTONPAGECHPFWD)

        self.buttonpageCHPBack = wx.Button(id=wxID_PANELCHPBUTTONPAGECHPBACK,
              label='<<<', name='buttonpageCHPBack', parent=self,
              pos=wx.Point(440, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageCHPBack.Bind(wx.EVT_BUTTON, self.OnButtonpageCHPBackButton,
              id=wxID_PANELCHPBUTTONPAGECHPBACK)

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

        self.config = Interfaces.GData["CHP Config"]
        
        try:
            if self.config[0] == 1:
                self.cbConfig1.SetValue(True)
            elif self.config[0] == 0:
                self.cbConfig1.SetValue(False)
        except:
            logTrack("PanelCHP: problem loading config[0] value %s "%self.config[0])

        try:        #try-except necessary if there comes a string that is not in list.
            self.choiceConfig2.SetSelection(0)
#            self.choiceConfig4.SetSelection(TYPELIST.index(self.config[1]))
        except:
            print "PanelCHP (display): was asked to display an erroneous fuel type",self.config[1]
            pass

        try:        #try-except necessary if there comes a string that is not in list.
            self.choiceConfig3.SetSelection(0)
#            self.choiceConfig4.SetSelection(TYPELIST.index(self.config[1]))
        except:
            print "PanelCHP (display): was asked to display an erroneous fuel type",self.config[2]
            pass

        self.tcConfig4.SetValue(str(self.config[3]))
        self.tcConfig5.SetValue(str(self.config[4]))
        
#..............................................................................
# update of info-values

        self.info = Interfaces.GData["CHP Info"]
        
        self.stInfo1Value.SetLabel(convertDoubleToString(self.info[0]))
        self.stInfo2Value.SetLabel(convertDoubleToString(self.info[1]))
        self.stInfo2_P1.SetLabel(convertDoubleToString(self.info[2]))
        self.stInfo2_P2.SetLabel(convertDoubleToString(self.info[3]))
        self.stInfo2_P3.SetLabel(convertDoubleToString(self.info[4]))
        self.stInfo2_P4.SetLabel(convertDoubleToString(self.info[5]))

        self.Hide()
        try: self.panelFig.draw()
        except: pass
        
        self.Show()
#==============================================================================
#   Event handlers
#==============================================================================

#------------------------------------------------------------------------------		
    def OnCHPCalculateButton(self, event):
#------------------------------------------------------------------------------		
#   Button "Run Design Assistant" pressed
#------------------------------------------------------------------------------		
#..............................................................................
# Step 1 design assistant: gets a preselected list of possible heat pumps

        (mode,CHPList) = self.mod.designAssistant1()
        logTrack("PanelHP: preselected heat pumps %s"%CHPList)
        
#..............................................................................
# In interactive mode open DB Edidor Heat pump and select manually

        if (mode == "MANUAL"):
            self.dbe = DBEditFrame(self,
                            _U('Select CHP equipment from preselected list'), # title for the dialogs
			    'dbchp',              # database table
			    0,                         # column to be returned
			    False,
                            preselection = CHPList)      # database table can be edited in DBEditFrame?
            if self.dbe.ShowModal() == wx.ID_OK:
                CHPId = self.dbe.theId
            else:
                CHPId = -1

        elif (mode == "AUTOMATIC"):
            CHPId = CHPList[0]    #in automatic mode just take first in the list

        elif (mode == "CANCEL"):
            CHPId = -1 #make designAssistant2 to understand that
        else:
            logDebug("PanelCHP (DesignAssistant-Button): erroneous panel mode: %s"%mode)

#..............................................................................
# Step 2 design assistant: add selected equipment to the list and update display
        
        self.mod.designAssistant2(CHPId)
        self.display()


#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnButtonpageCHPAddButton(self, event):
#------------------------------------------------------------------------------		
#   adds an equipment to the list
#------------------------------------------------------------------------------		

	self.equipe = self.mod.addEquipmentDummy() #SD change 30/04/2008, delete equipeC
        pu1 =  AddEquipment(self,                      # pointer to this panel
                            self.mod,                # pointer to the associated module
                            'Add boiler equipment', # title for the dialogs
                            'dbchp',              # database table
                            0,                         # column to be returned
                            False)                     # database table can be edited in DBEditFrame?

        if pu1.ShowModal() == wx.ID_OK:
            print 'PanelCHP AddEquipment accepted. Id='+str(pu1.theId)
        else:
            self.mod.deleteEquipment(None)
        self.display()

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnGridPageCHPGridCellLeftDclick(self, event):
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
    def OnGridPageCHPGridCellRightClick(self, event):
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
                
        elif (ret == _U("edit")):
            OnGridPageCHPGridCellLeftDclick(self,event)
        
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
            
        print "PanelCHP: new config[%s] value: "%0,self.config[0]
        Interfaces.GData["CHP Config"] = self.config
        self.mod.setUserDefinedPars()


    def OnChoiceConfig2Choice(self, event):
        self.config[1] = FUELLIST[self.choiceConfig2.GetSelection()]
        print "PanelCHP: new config[%s] value: "%3,self.config[1]
        Interfaces.GData["CHP Config"] = self.config[1]
        self.mod.setUserDefinedPars()

    def OnChoiceConfig3Choice(self, event):
        self.config[2] = FUELLIST[self.choiceConfig3.GetSelection()]
        print "PanelCHP: new config[%s] value: "%3,self.config[2]
        Interfaces.GData["CHP Config"] = self.config[2]
        self.mod.setUserDefinedPars()

    def OnTcConfig4TextEnter(self, event):
        self.config[3] = self.tcConfig4.GetValue()
        print "PanelCHP: new config[%s] value: "%3,self.config[3]
        Interfaces.GData["CHP Config"] = self.config
        self.mod.setUserDefinedPars()
        
    def OnTcConfig5TextEnter(self, event):
        self.config[4] = self.tcConfig5.GetValue()
        print "PanelCHP: new config[%s] value: "%4,self.config[4]
        Interfaces.GData["CHP Config"] = self.config
        self.mod.setUserDefinedPars()

#==============================================================================
#   <<< OK Cancel >>>
#==============================================================================

    def OnButtonpageCHPOkButton(self, event):
        self.main.tree.SelectItem(self.main.qHC, select=True)
        self.Hide()

    def OnButtonpageCHPCancelButton(self, event):
        print "Button exitModuleCancel: CANCEL Option not yet foreseen"

    def OnButtonpageCHPBackButton(self, event):
        self.main.tree.SelectItem(self.main.qHC, select=True)
        self.Hide()

    def OnButtonpageCHPFwdButton(self, event):
        self.main.tree.SelectItem(self.main.qST, select=True)
        self.Hide()
