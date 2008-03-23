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
import wx.grid
from status import Status
from einstein.modules.energyStats.moduleEA5 import *
import einstein.modules.matPanel as Mp


[wxID_PANELEA5, wxID_PANELEA5GRID1, wxID_PANELEA5GRID2, 
 wxID_PANELEA5PANELGRAPHEI, wxID_PANELEA5PANELGRAPHSEC, 
 wxID_PANELEA5STATICTEXT1, wxID_PANELEA5STATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(7)]

class PanelEA5(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.mod = ModuleEA5()

        # remaps drawing methods to the wx widgets.
        # gets the drawing methods from moduleEM1
        dummy = Mp.MatPanel(self.panelGraphEI, wx.Panel, self.mod.getPlotMethod(0))
        dummy = Mp.MatPanel(self.panelGraphSEC, wx.Panel, self.mod.getPlotMethod(1))
        del dummy
        #
        # additional widgets setup
        #
        self.grid1.CreateGrid(50, 2)
        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.SetColSize(0,125)
        self.grid1.SetColSize(1,125)
        self.grid1.EnableEditing(False)
        self.grid1.SetDefaultCellFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, "Energy type")
        self.grid1.SetColLabelValue(1, "Energy intensity\nkWh/euro")

        self.grid2.CreateGrid(50, 4)
        self.grid2.EnableGridLines(True)
        self.grid2.SetDefaultRowSize(20)
        self.grid2.SetRowLabelSize(30)
        self.grid2.SetColLabelSize(50)
        self.grid2.SetColSize(0,100)
        self.grid2.SetColSize(1,100)
        self.grid2.SetColSize(2,100)
        self.grid2.SetColSize(3,100)
        self.grid2.EnableEditing(False)
        self.grid2.SetDefaultCellFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.grid2.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid2.SetColLabelValue(0, "Product")
        self.grid2.SetColLabelValue(1, "Energy by\nfuels\nkWh/pu")
        self.grid2.SetColLabelValue(2, "Energy by\nelectricity\nkWh/pu")
        self.grid2.SetColLabelValue(3, "Primary\nenergy\nkWh/pu")

        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.staticText2.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA5, name=u'PanelEA5', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))

        self.staticText1 = wx.StaticText(id=wxID_PANELEA5STATICTEXT1,
              label=u'Energy intensity by energy type (turnover)',
              name='staticText1', parent=self, pos=wx.Point(40, 8),
              size=wx.Size(580, 20), style=0)

        self.grid1 = wx.grid.Grid(id=wxID_PANELEA5GRID1, name='grid1',
              parent=self, pos=wx.Point(40, 84), size=wx.Size(294, 210),
              style=0)

        self.panelGraphEI = wx.Panel(id=wxID_PANELEA5PANELGRAPHEI,
              name=u'panelGraphEI', parent=self, pos=wx.Point(512, 84),
              size=wx.Size(296, 210), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphEI.SetBackgroundColour(wx.Colour(77, 77, 77))


        self.staticText2 = wx.StaticText(id=wxID_PANELEA5STATICTEXT2,
              label=u'Specific energy consumption (SEC) by product.',
              name='staticText2', parent=self, pos=wx.Point(40, 324),
              size=wx.Size(580, 20), style=0)

        self.grid2 = wx.grid.Grid(id=wxID_PANELEA5GRID2, name='grid2',
              parent=self, pos=wx.Point(40, 386), size=wx.Size(440, 210),
              style=0)

        self.panelGraphSEC = wx.Panel(id=wxID_PANELEA5PANELGRAPHSEC,
              name=u'panelGraphSEC', parent=self, pos=wx.Point(512, 386),
              size=wx.Size(296, 210), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphSEC.SetBackgroundColour(wx.Colour(127, 127, 127))


