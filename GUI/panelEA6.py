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
from einstein.modules.energyStats.moduleEA6 import *
import einstein.modules.matPanel as Mp


[wxID_PANELEA6, wxID_PANELEA6GRID1, wxID_PANELEA6PANELGRAPHCO2, 
 wxID_PANELEA6STATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(4)]

class PanelEA6(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.mod = ModuleEA6()

        # remaps drawing methods to the wx widgets.
        # gets the drawing methods from moduleEM1
        dummy = Mp.MatPanel(self.panelGraphCO2, wx.Panel, self.mod.getPlotMethod(0))
        del dummy
        #
        # additional widgets setup
        #
        self.grid1.CreateGrid(50, 3)
        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.SetColSize(0,125)
        self.grid1.SetColSize(1,125)
        self.grid1.SetColSize(2,125)
        self.grid1.EnableEditing(False)
        self.grid1.SetDefaultCellFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, "Fuel type")
        self.grid1.SetColLabelValue(1, "Production\nof CO2 t/a")
        self.grid1.SetColLabelValue(2, "Production\nof CO2 %")

        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA6, name=u'PanelEA6', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))

        self.staticText1 = wx.StaticText(id=wxID_PANELEA6STATICTEXT1,
              label=u'Production of CO2 by energy type', name='staticText1',
              parent=self, pos=wx.Point(40, 8), size=wx.Size(580, 20),
              style=0)

        self.grid1 = wx.grid.Grid(id=wxID_PANELEA6GRID1, name='grid1',
              parent=self, pos=wx.Point(40, 84), size=wx.Size(420, 210),
              style=0)

        self.panelGraphCO2 = wx.Panel(id=wxID_PANELEA6PANELGRAPHCO2,
              name=u'panelGraphCO2', parent=self, pos=wx.Point(512, 84),
              size=wx.Size(296, 210), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphCO2.SetBackgroundColour(wx.Colour(77, 77, 77))


