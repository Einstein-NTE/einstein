#Boa:Frame:PanelEA4
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelEA4- GUI component for: Process heat - Yearly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota 21/03/2008
#       Revised by:         Tom Sobota 29/03/2008
#
#       Changes to previous version:
#       29/03/08:           mod. to use external graphics module
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
from einstein.GUI.graphics import drawPiePlot

from status import Status
from einstein.modules.energyStats.moduleEA4 import *
import einstein.modules.matPanel as Mp

[wxID_PANELEA4, wxID_PANELEA4GRID1, wxID_PANELEA4GRID2, 
 wxID_PANELEA4PANELGRAPHUPH, wxID_PANELEA4PANELGRAPHHD,
 wxID_PANELEA4STATICTEXT1, wxID_PANELEA4STATICTEXT2,
 wxID_PANELEA4STATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(8)]
#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem

COLNO = 8
MAXROWS = 50


class PanelEA4(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        keys = ['EA4_UPH', 'EA4_HDP'] 
        self.mod = ModuleEA4(keys)
        labels_column = 0
        # remaps drawing methods to the wx widgets.
        #
        # upper graphic: UPH demand by process
        #
        try:
            (rows,cols) = Interfaces.GData[keys[0]].shape
        except:
            rows = MAXROWS
            cols = COLNO
            
        ignoredrows = [rows-1]
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 2,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : 'UPH by process',       # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphUPH,
                            wx.Panel,
                            drawPiePlot,
                            paramList)

        #
        # lower graphic: Heat demand by process temperature
        #
        # no rows to ignore here
        paramList={'labels'      : labels_column,              # labels column
                   'data'        : 3,                          # data column for this graph
                   'key'         : keys[1],                    # key for Interface
                   'title'       : 'HD by process temperature',# title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR}     # graph background color

        dummy = Mp.MatPanel(self.panelGraphHD,
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
        # set upper grid
        #
        key = keys[0]
        try:
            data = Interfaces.GData[key]
            (rows,cols) = data.shape
        except:
            rows = MAXROWS
            cols = COLNO
            
        self.grid1.CreateGrid(max(rows,20), cols)

        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.SetColSize(0,115)
        self.grid1.EnableEditing(False)
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, "Process")
        self.grid1.SetColLabelValue(1, "MWh")
        self.grid1.SetColLabelValue(2, "%")
        #
        # copy values from dictionary to grid
        #
        for r in range(rows):
            self.grid1.SetRowAttr(r, attr)
            for c in range(cols):
                try:
                    self.grid1.SetCellValue(r, c, data[r][c])
                except:
                    pass
                
                if c == labels_column:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid1.SetGridCursor(0, 0)
        #
        # set lower grid
        #
        key = keys[1]

        try:
            data = Interfaces.GData[key]
            (rows,cols) = data.shape
        except:
            rows = MAXROWS
            cols = COLNO
            
        self.grid2.CreateGrid(max(rows,20), cols)

        self.grid2.EnableGridLines(True)
        self.grid2.SetDefaultRowSize(20)
        self.grid2.SetRowLabelSize(30)
        self.grid2.SetColSize(0,115)
        self.grid2.SetColSize(1,100)
        self.grid2.SetColSize(2,100)
        self.grid2.SetColSize(3,100)
        self.grid2.EnableEditing(False)
        self.grid2.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid2.SetColLabelValue(0, "Process")
        self.grid2.SetColLabelValue(1, "Process\ntemperature")
        self.grid2.SetColLabelValue(2, "Distribution\ntemperature")
        self.grid2.SetColLabelValue(3, "Heat\ndemand MWh")
        #
        # copy values from dictionary to grid
        #
        for r in range(rows):
            self.grid2.SetRowAttr(r, attr)
            for c in range(cols):
                try:
                    self.grid2.SetCellValue(r, c, data[r][c])
                except:
                    pass
                if c == labels_column:
                    self.grid2.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid2.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid2.SetGridCursor(0, 0)

        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.staticText3.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.staticText2.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA4, name=u'PanelEA4', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))

        self.staticText1 = wx.StaticText(id=wxID_PANELEA4STATICTEXT1,
              label=u'Useful process heat (UPH) demand by process.',
              name='staticText1', parent=self, pos=wx.Point(40, 8),
              size=wx.Size(580, 20), style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELEA4STATICTEXT2,
              label=u'UPH by process', name='staticText2',
              parent=self, pos=wx.Point(220, 70), size=wx.Size(270, 17),
              style=0)

        self.grid1 = wx.grid.Grid(id=wxID_PANELEA4GRID1, name='grid1',
              parent=self, pos=wx.Point(40, 84), size=wx.Size(322, 210),
              style=0)

        self.panelGraphUPH = wx.Panel(id=wxID_PANELEA4PANELGRAPHUPH,
              name=u'panelGraphUPH', parent=self, pos=wx.Point(512, 84),
              size=wx.Size(296, 210), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphUPH.SetBackgroundColour(wx.Colour(127, 127, 127))

        self.staticText3 = wx.StaticText(id=wxID_PANELEA4STATICTEXT3,
              label=u'Heat demand by process temperature.', name='staticText3',
              parent=self, pos=wx.Point(40, 324), size=wx.Size(580, 20),
              style=0)

        self.grid2 = wx.grid.Grid(id=wxID_PANELEA4GRID2, name='grid2',
              parent=self, pos=wx.Point(40, 386), size=wx.Size(462, 210),
              style=0)

        self.panelGraphHD = wx.Panel(id=wxID_PANELEA4PANELGRAPHHD,
              name=u'panelGraphHD', parent=self, pos=wx.Point(512, 386),
              size=wx.Size(296, 210), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphHD.SetBackgroundColour(wx.Colour(127, 127, 127))



