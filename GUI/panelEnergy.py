# -*- coding: cp1252 -*-
#Boa:FramePanel:PanelEnergy
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelEnergy- GUI component for: Energetic performance simulation
#			
#==============================================================================
#
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger
#       Revised by:         Tom Sobota 31/03/2008
#                           Tom Sobota 31/03/2008
#                           Hans Schweiger  03/04/2008
#                           Hans Schweiger  16/04/2008
#                           Hans Schweiger  29/04/2008
#                           Stoyan Danov            18/06/2008
#                           Hans Schweiger  26/06/2008
#                           Hans Schweiger  09/07/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes to previous version:
#       31/03/08:           mod. to use numpy based graphics arg passing
#       03/04/08:           moduleEnergy passed from Interfaces
#       16/04/08:   HS      main as argument in __init__
#       29/04/08:   HS      method display added
#       18/06/2008 SD: change to translatable text _(...)
#       26/06/2008: HS  figure of instantaneous supply added
#       09/07/2008: HS  restructuring of the panel
#                       - elimination of pie-plot (already in E-stats)
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
from status import Status
from einstein.modules.interfaces import *
from einstein.GUI.graphics import drawPiePlot
import einstein.modules.matPanel as Mp
from GUITools import *
from numCtrl import *
import matplotlib.font_manager as font
from matplotlib.ticker import FuncFormatter

[wxID_PANELENERGY, wxID_PANELENERGYANNUAL, wxID_PANELENERGYBUTTONBACK, 
 wxID_PANELENERGYBUTTONCANCEL, wxID_PANELENERGYBUTTONFWD, 
 wxID_PANELENERGYBUTTONOK, wxID_PANELENERGYBUTTONRUNSIMULATION, 
 wxID_PANELENERGYCHOICESIMULATIONTOOL, wxID_PANELENERGYGRID, 
 wxID_PANELENERGYHOURLY, wxID_PANELENERGYMONTHLY, wxID_PANELENERGYST1, 
 wxID_PANELENERGYST2, wxID_PANELENERGYST3, wxID_PANELENERGYSTATICBOX1, 
 wxID_PANELENERGYSTATICBOX2,
 wxID_PANELENERGYPICTURE1, wxID_PANELENERGYPICTURE2,
] = [wx.NewId() for _init_ctrls in range(18)]

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

MAXROWS = 1
COLNO = 5

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		
#    if not hasattr(self, 'subplot'):
    self.subplot = self.figure.add_subplot(1,1,1)
    self.figure.subplots_adjust(left=spacing_left, right=spacing_right, bottom=spacing_bottom, top=spacing_top)

    gdata = Status.int.GData["ENERGY Plot1"]
    try:
        for j in range(1,len(gdata)):
            self.subplot.plot(gdata[0][1:],\
                              gdata[j][1:],\
                              LINETYPES[(j-1)%len(LINETYPES)],
                              color = ORANGECASCADE[(j-1)%len(ORANGECASCADE)],
                              label=gdata[j][0],
                              linewidth=2)
    except:
        pass
        
    self.subplot.axis(ymin = 0)
    self.subplot.legend(loc = 0)   #4: left lower; 0: best

    major_formatter = FuncFormatter(format_int_wrapper)
    self.subplot.axes.xaxis.set_major_formatter(major_formatter)
    self.subplot.axes.yaxis.set_major_formatter(major_formatter)
    fp = font.FontProperties(size = axeslabel_fontsize)
    try:
        if Status.Nt == 12*168:
            self.subplot.axes.set_ylabel(_U('Heat supply by equipment [MWh/month]'), fontproperties=fp)
            self.subplot.axes.set_xlabel(_U('Month'), fontproperties=fp)
            self.subplot.axis(xmax = 12)
            
        else:
            self.subplot.axes.set_ylabel(_U('Heat supply by equipment [MWh/week]'), fontproperties=fp)
            self.subplot.axes.set_xlabel(_U('Week'), fontproperties=fp)
            self.subplot.axis(xmax = 52)
    except:
        logDebug("PanelEnergy: problems setting axes")
        self.subplot.axis(xmax = 52)

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
##
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
class PanelEnergy(wx.Panel):
#------------------------------------------------------------------------------		

    def __init__(self, parent, main,id, pos, size, style, name):
        self.main = main
        self._init_ctrls(parent)
        self.mod = Status.mod.moduleEnergy
        keys = self.mod.keys
        self.mod.initPanel()
        labels_column = 0

        # remaps drawing methods to the wx widgets.
        #
        (rows,cols) = (MAXROWS,COLNO)

        # left graphic: Energy demand
        paramList={'labels'      : 0,                       # labels column
                   'data'        : 1,                      # data column for this graph
                   'key'         : 'ENERGY Plot1',                # key for Interface
                   'title'       : _U('Energy demand'),        # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : []}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelEnergy, wx.Panel, drawFigure, paramList)
        del dummy

        #
        # additional widgets setup
        #
        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR_HIGHLIGHT)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR_HIGHLIGHT)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        #
        # set grid
        #
        self.grid.CreateGrid(MAXROWS, COLNO)

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(30)
        self.grid.SetRowLabelSize(0)
        self.grid.SetColLabelSize(50)
        self.grid.SetDefaultColSize(105)
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Primary energy\n(PET)\n [MWh]"))
        self.grid.SetColLabelValue(1, _U("Primary energy\nFuels (LCV)\n[MWh]"))
        self.grid.SetColLabelValue(2, _U("Primary energy\nElectricity\n[MWh]"))
        self.grid.SetColLabelValue(3, _U("Useful supply\nheat\n[MWh]"))
        self.grid.SetColLabelValue(4, _U("Useful process\nheat\n[MWh]"))
        #
        # copy values from dictionary to grid
        #
        for r in range(MAXROWS):
            self.grid.SetRowAttr(r, attr)
            for c in range(COLNO):
                if c == labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);

        self.grid.EnableEditing(False)
        self.grid.SetGridCursor(0, 0)


    def _init_ctrls(self, prnt):
        # generated method, don't edit

        wx.Panel.__init__(self, id=wxID_PANELENERGY, name='PanelEnergy',
              parent=prnt, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
        self.SetClientSize(wx.Size(800, 600))

#..............................................................................
# upper box: simulation set-up and global results
        
        self.box1 = wx.StaticBox(self, -1, _U('energy performance'),
                                 pos = (10,10),size=(780,200))

        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.buttonRunSimulation = wx.Button(id=wxID_PANELENERGYBUTTONRUNSIMULATION,
              label=_U('run simulation'), name='buttonRunSimulation', parent=self,
              pos=wx.Point(20, 40), size=wx.Size(200, 24), style=0)
        self.buttonRunSimulation.Bind(wx.EVT_BUTTON,
              self.OnButtonRunSimulationButton,
              id=wxID_PANELENERGYBUTTONRUNSIMULATION)

        self.st3 = wx.StaticText(id=wxID_PANELENERGYST3,
              label=_U('simulation setup: '), name='st3', parent=self,
              pos=wx.Point(280, 40), style=0)
        self.st3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))

        self.choiceSimulationTool = wx.Choice(choices=[_U("einstein"),
              _U("external tool 1"),_U("external tool 2")], id=wxID_PANELENERGYCHOICESIMULATIONTOOL,
              name='choiceSimulationTool', parent=self, pos=wx.Point(400, 40),
              size=wx.Size(160, 21), style=0)
        self.choiceSimulationTool.Bind(wx.EVT_CHOICE,
              self.OnChoiceSimulationToolChoice,
              id=wxID_PANELENERGYCHOICESIMULATIONTOOL)

        self.st1 = wx.StaticText(id=wxID_PANELENERGYST1,
              label=_U('global energy performance data'), name='st1', parent=self,
              pos=wx.Point(20, 80), style=0)
        self.st1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))

        self.grid = wx.grid.Grid(id=wxID_PANELENERGYGRID, name='grid',
              parent=self, pos=wx.Point(20, 100), size=wx.Size(540, 80),
              style=0)
        
#right side of box: buttons annual/monthly/hourly
        
        self.st2 = wx.StaticText(id=wxID_PANELENERGYST2,
              label=_U('simulation results'), name='st2', parent=self,
              pos=wx.Point(640, 40), style=0)
        self.st2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))

        self.annual = wx.Button(id=wxID_PANELENERGYANNUAL, label=_U('annual data'),
              name='annual', parent=self, pos=wx.Point(600, 80),
              size=wx.Size(180, 24), style=0)
        self.annual.Bind(wx.EVT_BUTTON, self.OnAnnualButton,
              id=wxID_PANELENERGYANNUAL)

        self.monthly = wx.Button(id=wxID_PANELENERGYMONTHLY,
              label=_U('monthly data'), name='monthly', parent=self,
              pos=wx.Point(600, 120), size=wx.Size(180, 24), style=0)
        self.monthly.Bind(wx.EVT_BUTTON, self.OnMonthlyButton,
              id=wxID_PANELENERGYMONTHLY)

        self.hourly = wx.Button(id=wxID_PANELENERGYHOURLY,
              label=_U('hourly performance'), name='hourly', parent=self,
              pos=wx.Point(600, 160), size=wx.Size(180, 24), style=0)
        self.hourly.Bind(wx.EVT_BUTTON, self.OnHourlyButton,
              id=wxID_PANELENERGYHOURLY)

#..............................................................................
# lower box: graph of simulation results

        self.box2 = wx.StaticBox(self, -1, _U('daily heat supply by equipment'),
                                 pos = (10,230),size=(780,320))

        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelEnergy = wx.Panel(id=wxID_PANELENERGYPICTURE1, name='panelEnergyDemand', parent=self,
              pos=wx.Point(20, 260), size=wx.Size(760, 280),
              style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)

#..............................................................................
# default action buttons

        self.buttonOK = wx.Button(id=wxID_PANELENERGYBUTTONOK, label=_U('ok'),
              name='buttonOK', parent=self, pos=wx.Point(500, 560),
              size=wx.Size(80, 20), style=0)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOKButton,
              id=wxID_PANELENERGYBUTTONOK)

        self.buttonCancel = wx.Button(id=wxID_PANELENERGYBUTTONCANCEL,
              label=_U('cancel'), name='buttonCancel', parent=self,
              pos=wx.Point(600, 560), size=wx.Size(80, 20), style=0)
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.OnButtonCancelButton,
              id=wxID_PANELENERGYBUTTONCANCEL)

        self.buttonFwd = wx.Button(id=wxID_PANELENERGYBUTTONFWD, label='>>>',
              name='buttonFwd', parent=self, pos=wx.Point(700, 560),
              size=wx.Size(80, 20), style=0)
        self.buttonFwd.Bind(wx.EVT_BUTTON, self.OnButtonFwdButton,
              id=wxID_PANELENERGYBUTTONFWD)

        self.buttonBack = wx.Button(id=wxID_PANELENERGYBUTTONBACK, label='<<<',
              name='buttonBack', parent=self, pos=wx.Point(400, 560),
              size=wx.Size(80, 20), style=0)
        self.buttonBack.Bind(wx.EVT_BUTTON, self.OnButtonBackButton,
              id=wxID_PANELENERGYBUTTONBACK)
        
#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   function activated on each entry into the panel from the tree
#------------------------------------------------------------------------------		

        self.mod.updatePanel()        # prepares data for plotting

        self.choiceSimulationTool.SetSelection(0)

#..............................................................................
# update of equipment table

        try:
            data = Interfaces.GData["ENERGY"]
            (rows,cols) = data.shape
            
        except:
            logDebug("PanelEnergy: problems reading GData entry")
            rows = 0
            cols = COLNO
            
        for r in range(rows):
            for c in range(cols):
                try:
                    self.grid.SetCellValue(r, c, convertDoubleToString(data[r][c]))
                except:
                    self.grid.SetCellValue(r, c, "---")

        for r in range(rows,MAXROWS):
            for c in range(cols):
                self.grid.SetCellValue(r, c, "")
        
        # left graphic: Energy demand
        paramList={'labels'      : 0,                       # labels column
                   'data'        : 1,                      # data column for this graph
                   'key'         : 'ENERGY Plot1',                # key for Interface
                   'title'       : _U('Energy demand'),        # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : []}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelEnergy, wx.Panel, drawFigure, paramList)
        self.panelEnergy.draw()
        self.Show()

#------------------------------------------------------------------------------		
#   Event handlers
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def OnButtonRunSimulationButton(self, event):
#------------------------------------------------------------------------------		
        self.mod.runSimulation()
        self.display()

    def OnButton1Button(self, event):
        event.Skip()

    def OnButtonpageHeatPumpBackButton(self, event):
        event.Skip()

    def OnButtonpageHeatPumpFwdButton(self, event):
        event.Skip()

    def OnMonthlyButton(self, event):
        event.Skip()

    def OnChoiceSimulationToolChoice(self, event):
        event.Skip()

    def OnButtonOKButton(self, event):
        event.Skip()

    def OnButtonCancelButton(self, event):
        event.Skip()

    def OnButtonFwdButton(self, event):
        event.Skip()

    def OnButtonBackButton(self, event):
        event.Skip()

    def OnHourlyButton(self, event):
        event.Skip()

    def OnAnnualButton(self, event):
        event.Skip()

#============================================================================== 



