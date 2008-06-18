#Boa:Frame:PanelEA3
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelEA3- GUI component for: Final energy by equipment - Yearly data
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
from einstein.modules.energyStats.moduleEA3 import *
import einstein.modules.matPanel as Mp

[wxID_PANELEA3, wxID_PANELEA3GRID1, wxID_PANELEA3GRID2, 
 wxID_PANELEA3PANELGRAPHFET, wxID_PANELEA3STATICTEXT1, 
 wxID_PANELEA3STATICTEXT2, wxID_PANELEA3STATICTEXT3,
 wxID_PANELEA3STATICTEXT4, wxID_PANELEA3PANELGRAPHUSH,
] = [wx.NewId() for _init_ctrls in range(9)]
#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem

MAXCOLS = 10

class PanelEA3(wx.Panel):
    def __init__(self, parent):
        self._init_ctrls(parent)
        keys = ['EA3_FET', 'EA3_USH'] 
        self.mod = ModuleEA3(keys)
        labels_column = 0
        # remaps drawing methods to the wx widgets.
        #
        # upper graph: FET by equipment
        #
        try:
            (rows,cols) = Interfaces.GData[keys[0]].shape
        except:
            print "PanelEA3: crash during initialisation avoided -> check this"
            rows = 1 #xxx dummy for avoiding crash
            cols = MAXCOLS #xxx dummy for avoiding crash

        ignoredrows = []
        ignoredrows.append(rows-1)

        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : _('FET by equipment'),     # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphFET,
                            wx.Panel,
                            drawPiePlot,
                            paramList)
        #
        # lower graph: USH by equipment
        #
        try:
            (rows,cols) = Interfaces.GData[keys[1]].shape
        except:
            print "PanelEA3: crash during initialisation avoided -> check this"
            rows = 1 #xxx dummy for avoiding crash
            cols = MAXCOLS #xxx dummy for avoiding crash
            
        ignoredrows = []
        ignoredrows.append(rows-1)

        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 2,                      # data column for this graph
                   'key'         : keys[1],                # key for Interface
                   'title'       : _('USH by equipment'),     # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphUSH,
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
        try:
            data = Interfaces.GData[keys[0]]
            (rows,cols) = data.shape
        except:
            data = [[0,0,0,0,0,0,0,0,0,0]]
            print "PanelEA3: crash during initialisation avoided -> check this"
            rows = 1 #xxx dummy for avoiding crash
            cols = MAXCOLS #xxx dummy for avoiding crash

        self.grid1.CreateGrid(max(rows,20), cols)

        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.SetColSize(0,120)
        self.grid1.SetColSize(1,115)
        self.grid1.EnableEditing(False)
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, _("Equipment"))
        self.grid1.SetColLabelValue(1, _("Fuel type"))
        self.grid1.SetColLabelValue(2, _("MWh"))
        self.grid1.SetColLabelValue(3, _("%"))
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
        try:
            data = Interfaces.GData[keys[1]]
            (rows,cols) = data.shape
        except:
            data = [[0,0,0,0,0,0,0,0,0,0]]
            print "PanelEA3: crash during initialisation avoided -> check this"
            rows = 1 #xxx dummy for avoiding crash
            cols = MAXCOLS #xxx dummy for avoiding crash

        self.grid2.CreateGrid(max(rows,20), cols)

        self.grid2.EnableGridLines(True)
        self.grid2.SetDefaultRowSize(20)
        self.grid2.SetRowLabelSize(30)
        self.grid2.SetColSize(0,120)
        self.grid2.EnableEditing(False)
        self.grid2.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid2.SetColLabelValue(0, _("Equipment"))
        self.grid2.SetColLabelValue(1, _("MWh"))
        self.grid2.SetColLabelValue(2, _("%"))
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
        self.staticText4.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA3, name=u'PanelEA3', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))

        self.staticText1 = wx.StaticText(id=wxID_PANELEA3STATICTEXT1,
              label=_(u'Final energy consumption for thermal use (FET) by equipment'),
              name='staticText1', parent=self, pos=wx.Point(40, 8),
              size=wx.Size(580, 20), style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELEA3STATICTEXT2,
              label=_(u'FET by equipment'),
              name='staticText2', parent=self, pos=wx.Point(320, 70),
              size=wx.Size(50, 17), style=0)

        self.grid1 = wx.grid.Grid(id=wxID_PANELEA3GRID1, name='grid1',
              parent=self, pos=wx.Point(40, 84), size=wx.Size(440, 210),
              style=0)

        self.panelGraphFET = wx.Panel(id=wxID_PANELEA3PANELGRAPHFET,
              name=u'panelGraphFET', parent=self, pos=wx.Point(512, 84),
              size=wx.Size(296,210), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphFET.SetBackgroundColour(wx.Colour(127, 127, 127))


        self.staticText3 = wx.StaticText(id=wxID_PANELEA3STATICTEXT3,
              label=_(u'Useful supply heat (USH) by equipment'),
              name='staticText3', parent=self, pos=wx.Point(40, 324),
              size=wx.Size(580, 20), style=0)

        self.staticText4 = wx.StaticText(id=wxID_PANELEA3STATICTEXT4,
              label=_(u'USH by equipment'),
              name='staticText4', parent=self, pos=wx.Point(200, 372),
              size=wx.Size(50, 17), style=0)

        self.grid2 = wx.grid.Grid(id=wxID_PANELEA3GRID2, name='grid2',
              parent=self, pos=wx.Point(40, 386), size=wx.Size(322, 210),
              style=0)

        self.panelGraphUSH = wx.Panel(id=wxID_PANELEA3PANELGRAPHUSH,
              name=u'panelGraphUSH', parent=self, pos=wx.Point(512, 386),
              size=wx.Size(296,210), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphUSH.SetBackgroundColour(wx.Colour(127, 127, 127))



    def display(self):
        self.panelGraphFET.draw()
        self.panelGraphUSH.draw()
        self.Show()
