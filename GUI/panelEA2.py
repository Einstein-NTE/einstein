#Boa:Frame:PanelEA2
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelEA2- GUI component for: Final energy by fuels - Yearly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	22/03/2008
#       Revised by:         Tom Sobota 29/03/2008
#       29/03/08:           mod. to use external graphics module
#
#       Changes to previous version:
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
from einstein.modules.energyStats.moduleEA2 import *
import einstein.modules.matPanel as Mp


[wxID_PANELEA2, wxID_PANELEA2GRID, wxID_PANELEA2PANELGRAPHPEC, 
 wxID_PANELEA2PANELGRAPHPET, wxID_PANELEA2STATICTEXT1, 
 wxID_PANELEA2STATICTEXT2, wxID_PANELEA2STATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(7)]

#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem


class PanelEA2(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        keys = ['EA2'] 
        self.mod = ModuleEA2(keys)
        labels_column = 0
        ignoredrows = [2] # totals row is always n.3

        #
        # left pie: PEC by fuel
        #
        paramList={'labels'      : 0,                     # labels column
                   'data'        : 2,                     # data column for this graph
                   'key'         : keys[0],               # key for Interface
                   'title'       :'PEC by fuel',          # title of the graph
                   'backcolor'   :GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' :[2]}                    # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphPEC,   # widget that contains the graphic
                            wx.Panel,             # class of the widget
                            drawPiePlot,          # generic pie plotting routine
                            paramList)

        #
        # right pie: PET by fuel
        #

        paramList={'labels'      : 0,                     # labels column
                   'data'        : 4,                     # data column for this graph
                   'key'         : keys[0],               # key for Interface
                   'title'       :'PET by fuel',          # title of the graph
                   'backcolor'   :GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' :[2]}                    # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphPET,   # widget that contains the graphic
                            wx.Panel,             # class of the widget
                            drawPiePlot,          # generic pie plotting routine
                            paramList)

        #
        # additional widgets setup
        #
        data = Interfaces.GData[keys[0]]
        (rows,cols) = data.shape
        self.grid.CreateGrid(max(rows,20), cols)

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetColSize(0,160)
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, "Fuel type")
        self.grid.SetColLabelValue(1, "MWh")
        self.grid.SetColLabelValue(2, "%")
        self.grid.SetColLabelValue(3, "MWh")
        self.grid.SetColLabelValue(4, "%")
        self.grid.SetCellValue(0,0,"Total Fuels")
        self.grid.SetCellValue(1,0,"Total Electricity")
        self.grid.SetCellValue(2,0,"Total (Fuels+Electricity)")
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        #
        # copy values from dictionary to grid
        #
        for r in range(rows):
            self.grid.SetRowAttr(r, attr)
            for c in range(cols):
                self.grid.SetCellValue(r, c, data[r][c])
                if c == labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid.SetGridCursor(0, 0)

        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.staticText2.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.staticText3.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA2, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600),
              style=wx.DEFAULT_FRAME_STYLE)

        self.staticText1 = wx.StaticText(id=wxID_PANELEA2STATICTEXT1,
              label=u'Total primary energy consumption (PEC) and primary energy\nconsumption for thermal use (PET)',
              name='staticText1', parent=self, pos=wx.Point(200, 8),
              size=wx.Size(580, 40), style=0)
        self.staticText1.Center(wx.HORIZONTAL)

        self.grid = wx.grid.Grid(id=wxID_PANELEA2GRID, name='grid', parent=self,
              pos=wx.Point(152, 100), size=wx.Size(510, 120),
              style=wx.VSCROLL | wx.THICK_FRAME)

        self.panelGraphPEC = wx.Panel(id=wxID_PANELEA2PANELGRAPHPEC,
              name=u'panelGraphFEC', parent=self, pos=wx.Point(110, 300),
              size=wx.Size(280, 224), style=wx.TAB_TRAVERSAL)
        self.panelGraphPEC.SetBackgroundColour(wx.Colour(127, 127, 127))

        self.panelGraphPET = wx.Panel(id=wxID_PANELEA2PANELGRAPHPET,
              name=u'panelGraphFET', parent=self, pos=wx.Point(430, 300),
              size=wx.Size(280, 224), style=wx.TAB_TRAVERSAL)
        self.panelGraphPET.SetBackgroundColour(wx.Colour(127, 127, 127))

        self.staticText2 = wx.StaticText(id=wxID_PANELEA2STATICTEXT2,
              label=u'PEC', name='staticText2', parent=self, pos=wx.Point(405,
              82), size=wx.Size(56, 17), style=0)

        self.staticText3 = wx.StaticText(id=wxID_PANELEA2STATICTEXT3,
              label=u'PET', name='staticText3', parent=self, pos=wx.Point(565,
              82), size=wx.Size(40, 17), style=0)


