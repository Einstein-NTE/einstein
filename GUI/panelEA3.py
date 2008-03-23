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
from einstein.modules.energyStats.moduleEA3 import *
import einstein.modules.matPanel as Mp

[wxID_PANELEA3, wxID_PANELEA3GRID1, wxID_PANELEA3GRID2, 
 wxID_PANELEA3PANELGRAPHFET, wxID_PANELEA3STATICTEXT1, 
 wxID_PANELEA3STATICTEXT2, wxID_PANELEA3STATICTEXT3,
 wxID_PANELEA3STATICTEXT4, wxID_PANELEA3PANELGRAPHUSH,
] = [wx.NewId() for _init_ctrls in range(9)]

class PanelEA3(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.mod = ModuleEA3()

        # remaps drawing methods to the wx widgets.
        # gets the drawing methods from moduleEA3
        dummy = Mp.MatPanel(self.panelGraphFET, wx.Panel, self.mod.getPlotMethod(0))
        dummy = Mp.MatPanel(self.panelGraphUSH, wx.Panel, self.mod.getPlotMethod(1))
        del dummy
        #
        # additional widgets setup
        #
        self.grid1.CreateGrid(50, 4)
        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.SetColSize(0,120)
        self.grid1.SetColSize(1,115)
        self.grid1.EnableEditing(False)
        self.grid1.SetDefaultCellFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, "Equipment")
        self.grid1.SetColLabelValue(1, "Fuel type")
        self.grid1.SetColLabelValue(2, "MWh")
        self.grid1.SetColLabelValue(3, "%")

        self.grid2.CreateGrid(50, 3)
        self.grid2.EnableGridLines(True)
        self.grid2.SetDefaultRowSize(20)
        self.grid2.SetRowLabelSize(30)
        self.grid2.SetColSize(0,120)
        self.grid2.EnableEditing(False)
        self.grid2.SetDefaultCellFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.grid2.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid2.SetColLabelValue(0, "Equipment")
        self.grid2.SetColLabelValue(1, "MWh")
        self.grid2.SetColLabelValue(2, "%")

        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.staticText3.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.staticText2.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.staticText4.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA3, name=u'PanelEA3', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))

        self.staticText1 = wx.StaticText(id=wxID_PANELEA3STATICTEXT1,
              label=u'Final energy consumption for thermal use (FET) by equipment',
              name='staticText1', parent=self, pos=wx.Point(40, 8),
              size=wx.Size(580, 20), style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELEA3STATICTEXT2,
              label=u'FET by equipment',
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
              label=u'Useful supply heat (USH) by equipment',
              name='staticText3', parent=self, pos=wx.Point(40, 324),
              size=wx.Size(580, 20), style=0)

        self.staticText4 = wx.StaticText(id=wxID_PANELEA3STATICTEXT4,
              label=u'USH by equipment',
              name='staticText4', parent=self, pos=wx.Point(200, 372),
              size=wx.Size(50, 17), style=0)

        self.grid2 = wx.grid.Grid(id=wxID_PANELEA3GRID2, name='grid2',
              parent=self, pos=wx.Point(40, 386), size=wx.Size(322, 210),
              style=0)

        self.panelGraphUSH = wx.Panel(id=wxID_PANELEA3PANELGRAPHUSH,
              name=u'panelGraphUSH', parent=self, pos=wx.Point(512, 386),
              size=wx.Size(296,210), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphUSH.SetBackgroundColour(wx.Colour(127, 127, 127))



