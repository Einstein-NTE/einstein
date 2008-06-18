#Boa:Frame:PanelEA5
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelEA5- GUI component for: Energy intensity - Yearly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	21/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#       Revised by:         Tom Sobota  28/04/2008
#                           Stoyan Danov            18/06/2008
#
#       Changes to previous version:
#       29/03/08:           mod. to use external graphics module
#       28/04/2008          created method display
#       18/06/2008 SD: change to translatable text _(...)
#
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
from einstein.modules.energyStats.moduleEA5 import *
import einstein.modules.matPanel as Mp
from einstein.GUI.graphics import drawSimpleBarPlot, drawComparedBarPlot


[wxID_PANELEA5, wxID_PANELEA5GRID1, wxID_PANELEA5GRID2, 
 wxID_PANELEA5PANELGRAPHEI, wxID_PANELEA5PANELGRAPHSEC, 
 wxID_PANELEA5STATICTEXT1, wxID_PANELEA5STATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(7)]

#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem


class PanelEA5(wx.Panel):
    def __init__(self, parent):
        self._init_ctrls(parent)
        keys = ['EA5_EI', 'EA5_SEC']
        self.mod = ModuleEA5(keys)
        labels_column = 0
        # remaps drawing methods to the wx widgets.
        #
        # upper graphic: Energy intensity
        #

        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 1,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : _('Energy intensity'),     # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : [2]}                    # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphEI,wx.Panel,drawSimpleBarPlot,paramList)

        #
        # lower grid: SEC by product
        #
        (rows,cols) = Interfaces.GData[keys[1]].shape
        ignoredrows = []
        ignoredrows.append(rows-1)

        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 1,                      # data column for this graph
                   'key'         : keys[1],                # key for Interface
                   'title'       : _('SEC by product'),       # title of the graph
                   'ylabel'      : 'Energy',
                   'legend'      : [_('Energy by fuels'), _('Energy by electricity'), _('Primary energy')], # legend
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphSEC,wx.Panel,drawComparedBarPlot,paramList)
        
        #
        # additional widgets setup
        #
        #
        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        #
        # set upper grid
        #
        data = Interfaces.GData[keys[0]]
        (rows,cols) = data.shape
        self.grid1.CreateGrid(rows, cols)

        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.SetColSize(0,140)
        self.grid1.SetColSize(1,125)
        self.grid1.EnableEditing(False)
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, _("Energy type"))
        self.grid1.SetColLabelValue(1, _("Energy intensity\nkWh/euro"))
        #
        # copy values from dictionary to grid
        #
        for r in range(rows):
            self.grid1.SetRowAttr(r, attr)
            for c in range(cols):
                self.grid1.SetCellValue(r, c, data[r][c])
                if c == labels_column:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid1.SetGridCursor(0, 0)
        #
        # set lower grid
        #
        data = Interfaces.GData[keys[1]]
        (rows,cols) = data.shape
        self.grid2.CreateGrid(max(rows,20), cols)

        self.grid2.EnableGridLines(True)
        self.grid2.SetDefaultRowSize(20)
        self.grid2.SetRowLabelSize(30)
        self.grid2.SetColLabelSize(50)
        self.grid2.SetColSize(0,100)
        self.grid2.SetColSize(1,100)
        self.grid2.SetColSize(2,100)
        self.grid2.SetColSize(3,100)
        self.grid2.EnableEditing(False)
        self.grid2.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid2.SetColLabelValue(0, _("Product"))
        self.grid2.SetColLabelValue(1, _("Energy by\nfuels\nkWh/pu"))
        self.grid2.SetColLabelValue(2, _("Energy by\nelectricity\nkWh/pu"))
        self.grid2.SetColLabelValue(3, _("Primary\nenergy\nkWh/pu"))
        #
        # copy values from dictionary to grid
        #
        for r in range(rows):
            self.grid2.SetRowAttr(r, attr)
            for c in range(cols):
                self.grid2.SetCellValue(r, c, data[r][c])
                if c == labels_column:
                    self.grid2.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid2.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid2.SetGridCursor(0, 0)

        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.staticText2.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA5, name=u'PanelEA5', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))

        self.staticText1 = wx.StaticText(id=wxID_PANELEA5STATICTEXT1,
              label=_(u'Energy intensity by energy type (turnover)'),
              name='staticText1', parent=self, pos=wx.Point(40, 8),
              size=wx.Size(580, 20), style=0)

        self.grid1 = wx.grid.Grid(id=wxID_PANELEA5GRID1, name='grid1',
              parent=self, pos=wx.Point(40, 84), size=wx.Size(300, 92),
              style=0)

        self.panelGraphEI = wx.Panel(id=wxID_PANELEA5PANELGRAPHEI,
              name=u'panelGraphEI', parent=self, pos=wx.Point(512, 84),
              size=wx.Size(296, 210), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphEI.SetBackgroundColour(wx.Colour(77, 77, 77))


        self.staticText2 = wx.StaticText(id=wxID_PANELEA5STATICTEXT2,
              label=_(u'Specific energy consumption (SEC) by product.'),
              name='staticText2', parent=self, pos=wx.Point(40, 324),
              size=wx.Size(580, 20), style=0)

        self.grid2 = wx.grid.Grid(id=wxID_PANELEA5GRID2, name='grid2',
              parent=self, pos=wx.Point(40, 386), size=wx.Size(440, 210),
              style=0)

        self.panelGraphSEC = wx.Panel(id=wxID_PANELEA5PANELGRAPHSEC,
              name=u'panelGraphSEC', parent=self, pos=wx.Point(512, 386),
              size=wx.Size(296, 210), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphSEC.SetBackgroundColour(wx.Colour(127, 127, 127))


    def display(self):
        self.panelGraphEI.draw()
        self.panelGraphSEC.draw()
        self.Show()
        

