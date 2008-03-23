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
from einstein.modules.energyStats.moduleEA2 import *
import einstein.modules.matPanel as Mp


[wxID_PANELEA2, wxID_PANELEA2GRID, wxID_PANELEA2PANELGRAPHPEC, 
 wxID_PANELEA2PANELGRAPHPET, wxID_PANELEA2STATICTEXT1, 
 wxID_PANELEA2STATICTEXT2, wxID_PANELEA2STATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(7)]

class PanelEA2(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.mod = ModuleEA2()

        # remaps drawing methods to the wx widgets.
        # gets the drawing methods from moduleEA2
        dummy = Mp.MatPanel(self.panelGraphPEC, wx.Panel, self.mod.getPlotMethod(0))
        dummy = Mp.MatPanel(self.panelGraphPET, wx.Panel, self.mod.getPlotMethod(1))
        del dummy
        #
        # additional widgets setup
        #
        self.grid.CreateGrid(3, 5)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetColSize(0,160)
        self.grid.EnableEditing(False)
        self.grid.SetDefaultCellFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, "Fuel type")
        self.grid.SetColLabelValue(1, "MWh")
        self.grid.SetColLabelValue(2, "%")
        self.grid.SetColLabelValue(3, "MWh")
        self.grid.SetColLabelValue(4, "%")
        self.grid.SetCellValue(0,0,"Total Fuels")
        self.grid.SetCellValue(1,0,"Total Electricity")
        self.grid.SetCellValue(2,0,"Total (Fuels+Electricity)")

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
              pos=wx.Point(152, 100), size=wx.Size(510, 92),
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


