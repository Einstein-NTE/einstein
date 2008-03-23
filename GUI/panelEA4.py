#Boa:Frame:PanelEA4
#==============================================================================#
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
from einstein.modules.energyStats.moduleEA4 import *
import einstein.modules.matPanel as Mp

[wxID_PANELEA4, wxID_PANELEA4GRID1, wxID_PANELEA4GRID2, 
 wxID_PANELEA4PANELGRAPHUPH, wxID_PANELEA4PANELGRAPHHD,
 wxID_PANELEA4STATICTEXT1, wxID_PANELEA4STATICTEXT2,
 wxID_PANELEA4STATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(8)]

class PanelEA4(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.mod = ModuleEA4()

        # remaps drawing methods to the wx widgets.
        # gets the drawing methods from moduleEM1
        dummy = Mp.MatPanel(self.panelGraphUPH, wx.Panel, self.mod.getPlotMethod(0))
        dummy = Mp.MatPanel(self.panelGraphHD, wx.Panel, self.mod.getPlotMethod(1))
        del dummy
        #
        # additional widgets setup
        #
        self.grid1.CreateGrid(50, 3)
        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.SetColSize(0,115)
        self.grid1.EnableEditing(False)
        self.grid1.SetDefaultCellFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, "Process")
        self.grid1.SetColLabelValue(1, "MWh")
        self.grid1.SetColLabelValue(2, "%")

        self.grid2.CreateGrid(50, 4)
        self.grid2.EnableGridLines(True)
        self.grid2.SetDefaultRowSize(20)
        self.grid2.SetRowLabelSize(30)
        self.grid2.SetColSize(0,115)
        self.grid2.SetColSize(1,100)
        self.grid2.SetColSize(2,100)
        self.grid2.SetColSize(3,100)
        self.grid2.EnableEditing(False)
        self.grid2.SetDefaultCellFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.grid2.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid2.SetColLabelValue(0, "Process")
        self.grid2.SetColLabelValue(1, "Process\ntemperature")
        self.grid2.SetColLabelValue(2, "Distribution\ntemperature")
        self.grid2.SetColLabelValue(3, "Heat\ndemand MWh")

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



