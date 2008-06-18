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
#
#       Changes to previous version:
#       31/03/08:           mod. to use numpy based graphics arg passing
#       03/04/08:           moduleEnergy passed from Interfaces
#       16/04/08:   HS      main as argument in __init__
#       29/04/08:   HS      method display added
#       18/06/2008 SD: change to translatable text _(...)
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
from einstein.modules.modules import *
from einstein.GUI.graphics import drawPiePlot
import einstein.modules.matPanel as Mp


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
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem

MAXROWS = 50
COLNO = 8

class PanelEnergy(wx.Panel):

    def __init__(self, parent, main,id, pos, size, style, name):
        self.main = main
        self._init_ctrls(parent)
        keys = ['ENERGY'] 
        self.mod = Status.mod.moduleEnergy
        labels_column = 0

        # remaps drawing methods to the wx widgets.
        #
        (rows,cols) = (MAXROWS,COLNO)
        ignoredrows = [rows-1,rows-2] # ignore totals and savings

        # left graphic: Energy demand
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : _('Energy demand'),        # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        #dummy = Mp.MatPanel(self.panelEnergyDemand, wx.Panel, drawPiePlot, paramList)


        # right graphic: Comparative performance
        paramList={'labels'      : labels_column,            # labels column
                   'data'        : 2,                        # data column for this graph
                   'key'         : keys[0],                  # key for Interface
                   'title'       : _('Comparative performance'),# title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR,   # graph background color
                   'ignoredrows' : ignoredrows}              # rows that should not be plotted


        dummy = Mp.MatPanel(self.panelComPerformance,
                            wx.Panel,
                            drawPiePlot,
                            paramList)


        #
        # additional widgets setup
        #
        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        #
        # set grid
        #
        self.grid.CreateGrid(MAXROWS, COLNO)

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(115)
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _("Equipment\ntype"))
        self.grid.SetColLabelValue(1, _("Useful supply\nheat/cold"))
        self.grid.SetColLabelValue(2, _("Primary energy\nconsumption"))
        self.grid.SetColLabelValue(3, _("CO2 generation"))
        #
        # copy values from dictionary to grid
        #
        for r in range(MAXROWS):
            self.grid.SetRowAttr(r, attr)
            for c in range(COLNO):
                if c == labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid.EnableEditing(False)
        self.grid.SetGridCursor(0, 0)


    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELENERGY, name='PanelEnergy',
              parent=prnt, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
        self.SetClientSize(wx.Size(792, 566))

        self.monthly = wx.Button(id=wxID_PANELENERGYMONTHLY,
              label=_('monthly data'), name='monthly', parent=self,
              pos=wx.Point(592, 144), size=wx.Size(184, 23), style=0)
        self.monthly.Bind(wx.EVT_BUTTON, self.OnMonthlyButton,
              id=wxID_PANELENERGYMONTHLY)

        self.grid = wx.grid.Grid(id=wxID_PANELENERGYGRID, name='grid',
              parent=self, pos=wx.Point(16, 104), size=wx.Size(504, 168),
              style=0)

        self.st2 = wx.StaticText(id=wxID_PANELENERGYST2,
              label=_('simulation results'), name='st2', parent=self,
              pos=wx.Point(632, 72), style=0)
        self.st2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.choiceSimulationTool = wx.Choice(choices=[_("einstein"),
              _("transEnergy")], id=wxID_PANELENERGYCHOICESIMULATIONTOOL,
              name='choiceSimulationTool', parent=self, pos=wx.Point(392, 16),
              size=wx.Size(130, 21), style=0)
        self.choiceSimulationTool.Bind(wx.EVT_CHOICE,
              self.OnChoiceSimulationToolChoice,
              id=wxID_PANELENERGYCHOICESIMULATIONTOOL)

        self.staticBox1 = wx.StaticBox(id=wxID_PANELENERGYSTATICBOX1,
              label=_('energy demand'), name='staticBox1', parent=self,
              pos=wx.Point(16, 288), size=wx.Size(360, 224), style=0)
        self.panelEnergyDemand = wx.Panel(id=wxID_PANELENERGYPICTURE1, name='panelEnergyDemand', parent=self,
              pos=wx.Point(24, 312), size=wx.Size(344, 192),
              style=wx.TAB_TRAVERSAL)

        self.buttonOK = wx.Button(id=wxID_PANELENERGYBUTTONOK, label=_('ok'),
              name='buttonOK', parent=self, pos=wx.Point(528, 528),
              size=wx.Size(75, 23), style=0)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOKButton,
              id=wxID_PANELENERGYBUTTONOK)

        self.buttonCancel = wx.Button(id=wxID_PANELENERGYBUTTONCANCEL,
              label=_('cancel'), name='buttonCancel', parent=self,
              pos=wx.Point(616, 528), size=wx.Size(75, 23), style=0)
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.OnButtonCancelButton,
              id=wxID_PANELENERGYBUTTONCANCEL)

        self.buttonRunSimulation = wx.Button(id=wxID_PANELENERGYBUTTONRUNSIMULATION,
              label=_('run simulation'), name='buttonRunSimulation', parent=self,
              pos=wx.Point(16, 16), size=wx.Size(184, 23), style=0)
        self.buttonRunSimulation.Bind(wx.EVT_BUTTON,
              self.OnButtonRunSimulationButton,
              id=wxID_PANELENERGYBUTTONRUNSIMULATION)

        self.buttonFwd = wx.Button(id=wxID_PANELENERGYBUTTONFWD, label='>>>',
              name='buttonFwd', parent=self, pos=wx.Point(704, 528),
              size=wx.Size(75, 23), style=0)
        self.buttonFwd.Bind(wx.EVT_BUTTON, self.OnButtonFwdButton,
              id=wxID_PANELENERGYBUTTONFWD)

        self.buttonBack = wx.Button(id=wxID_PANELENERGYBUTTONBACK, label='<<<',
              name='buttonBack', parent=self, pos=wx.Point(440, 528),
              size=wx.Size(75, 23), style=0)
        self.buttonBack.Bind(wx.EVT_BUTTON, self.OnButtonBackButton,
              id=wxID_PANELENERGYBUTTONBACK)

        self.hourly = wx.Button(id=wxID_PANELENERGYHOURLY,
              label=_('hourly performance'), name='hourly', parent=self,
              pos=wx.Point(592, 184), size=wx.Size(184, 23), style=0)
        self.hourly.Bind(wx.EVT_BUTTON, self.OnHourlyButton,
              id=wxID_PANELENERGYHOURLY)

        self.annual = wx.Button(id=wxID_PANELENERGYANNUAL, label=_('annual data'),
              name='annual', parent=self, pos=wx.Point(592, 104),
              size=wx.Size(184, 23), style=0)
        self.annual.Bind(wx.EVT_BUTTON, self.OnAnnualButton,
              id=wxID_PANELENERGYANNUAL)

        self.st3 = wx.StaticText(id=wxID_PANELENERGYST3,
              label=_('simulation setup: '), name='st3', parent=self,
              pos=wx.Point(280, 20), style=0)
        self.st3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.st1 = wx.StaticText(id=wxID_PANELENERGYST1,
              label=_('energetic performance'), name='st1', parent=self,
              pos=wx.Point(16, 82), style=0)
        self.st1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticBox2 = wx.StaticBox(id=wxID_PANELENERGYSTATICBOX2,
              label=_('comparative performance'), name='staticBox2', parent=self,
              pos=wx.Point(416, 288), size=wx.Size(360, 224), style=0)
        
        self.panelComPerformance = wx.Panel(id=wxID_PANELENERGYPICTURE2,
                                            name='panelComPerformance', parent=self,
              pos=wx.Point(424, 312), size=wx.Size(344, 192),
              style=wx.TAB_TRAVERSAL)
        
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

#        self.config = Interfaces.GData["BB Config"]
#        self.cbConfig1.SetValue(self.config[0])
#        try:        #try-except necessary if there comes a string that is not in list.
#            self.choiceConfig2.SetSelection(TYPELIST.index(self.config[1]))
#        except:
#            print "PanelHP (display): was asked to display an erroneous heat pump type",self.config[1]
#            pass
#        self.tcConfig3.SetValue(str(self.config[2]))
#        self.tcConfig4.SetValue(str(self.config[3]))
#        self.tcConfig5.SetValue(str(self.config[4]))
#        self.tcConfig6.SetValue(str(self.config[5]))
#        self.tcConfig7.SetValue(str(self.config[6]))
        
#..............................................................................
# update of info-values

#        self.info = Interfaces.GData["HP Info"]
        
#        self.tcInfo1.SetValue(str(self.info[0]))
#        self.tcInfo2.SetValue(str(self.info[1]))

        self.panelComPerformance.draw()
        self.Show()

    def OnButtonRunSimulationButton(self, event):
        self.mod.runSimulation()

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



