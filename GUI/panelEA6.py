#Boa:Frame:PanelEA6
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelEA6- GUI component for: Production of CO2 - Yearly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	22/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#       Revised by:         Tom Sobota  28/04/2008
#                           Stoyan Danov            18/06/2008
#
#       Changes to previous version:
#       29/03/08:           mod. to use external graphics module
#       28/04/2008          created method display
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
from einstein.modules.energyStats.moduleEA6 import *
import einstein.modules.matPanel as Mp
from einstein.GUI.graphics import drawPiePlot

[wxID_PANELEA6, wxID_PANELEA6GRID1, wxID_PANELEA6PANELGRAPHCO2, 
 wxID_PANELEA6STATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(4)]
#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem


class PanelEA6(wx.Panel):
    def __init__(self, parent):
        self._init_ctrls(parent)
        keys = ['EA6'] 
        self.mod = ModuleEA6(keys)
        labels_column = 0
        # remaps drawing methods to the wx widgets.
        #
        # single grid: CO2 by energy type
        #
        (rows,cols) = Interfaces.GData[keys[0]].shape
        ignoredrows = []
        ignoredrows.append(rows-1)

        paramList={'labels'      : labels_column,               # labels column
                   'data'        : 2,                           # data column for this graph
                   'key'         : keys[0],                     # key for Interface
                   'title'       : _('Production of CO2 by fuel'), # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR,      # graph background color
                   'ignoredrows' : ignoredrows}                 # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphCO2, wx.Panel, drawPiePlot, paramList)
        #
        # additional widgets setup
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
        self.grid1.CreateGrid(max(rows,20), cols)

        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.SetColSize(0,125)
        self.grid1.SetColSize(1,125)
        self.grid1.SetColSize(2,125)
        self.grid1.EnableEditing(False)
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, _("Fuel type"))
        self.grid1.SetColLabelValue(1, _("Production\nof CO2 t/a"))
        self.grid1.SetColLabelValue(2, _("Production\nof CO2 %"))
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

        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA6, name=u'PanelEA6', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))

        self.staticText1 = wx.StaticText(id=wxID_PANELEA6STATICTEXT1,
              label=_(u'Production of CO2 by energy type'), name='staticText1',
              parent=self, pos=wx.Point(40, 8), size=wx.Size(580, 20),
              style=0)

        self.grid1 = wx.grid.Grid(id=wxID_PANELEA6GRID1, name='grid1',
              parent=self, pos=wx.Point(40, 84), size=wx.Size(420, 210),
              style=0)

        self.panelGraphCO2 = wx.Panel(id=wxID_PANELEA6PANELGRAPHCO2,
              name=u'panelGraphCO2', parent=self, pos=wx.Point(512, 84),
              size=wx.Size(296, 210), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphCO2.SetBackgroundColour(wx.Colour(77, 77, 77))


    def display(self):
        self.panelGraphCO2.draw()
        self.Show()
        
