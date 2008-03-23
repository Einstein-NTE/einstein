#Boa:Frame:PanelEA1
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelEA1- GUI component for: Primary energy - Yearly data
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
# import the data processing module for this panel.
from einstein.modules.energyStats.moduleEA1 import *
# import the remapping module
import einstein.modules.matPanel as Mp

[wxID_PANELEA1, wxID_PANELEA1GRID, wxID_PANELEA1PANELGRAPHFEC, 
 wxID_PANELEA1PANELGRAPHFET, wxID_PANELEA1STATICTEXT1, 
 wxID_PANELEA1STATICTEXT2, wxID_PANELEA1STATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(7)]

class PanelEA1(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        # loads and initializes the respective data-processing module
        self.mod = ModuleEA1()

        # remaps drawing methods to the wx widgets.
        # gets the two drawing methods from moduleEA1
        # 1. gets the graphing method for panelGraphFEC
        dummy = Mp.MatPanel(self.panelGraphFEC, wx.Panel, self.mod.getPlotMethod(0))

        # 2. gets the graphing method for panelGraphFET
        dummy = Mp.MatPanel(self.panelGraphFET, wx.Panel, self.mod.getPlotMethod(1))
        # the remapping object is no longer necessary so it can be deleted.
        # this is optative, just to make clear that it will not be used anymore.
        del dummy
        #
        # additional widgets setup
        # here, we modify some widgets attributes that cannot be changed
        # directly by Boa. This cannot be done in _init_ctrls, since that
        # method is rewritten by Boa each time.
        #
        self.grid.CreateGrid(50, 5)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetColSize(0,115)
        self.grid.EnableEditing(False)
        self.grid.SetDefaultCellFont(wx.Font(9, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, "Fuel type")
        self.grid.SetColLabelValue(1, "MWh")
        self.grid.SetColLabelValue(2, "%")
        self.grid.SetColLabelValue(3, "MWh")
        self.grid.SetColLabelValue(4, "%")

        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.staticText2.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.staticText3.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=-1, name='', parent=prnt, pos=wx.Point(6, 0),
              size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE)

        self.staticText1 = wx.StaticText(id=wxID_PANELEA1STATICTEXT1,
              label=u'Total final energy consumption (FEC) and final energy consumption for thermal use (FET)',
              name='staticText1', parent=self, pos=wx.Point(10, 8),
              size=wx.Size(580, 20), style=0)
        self.staticText1.Center(wx.HORIZONTAL)

        self.grid = wx.grid.Grid(id=wxID_PANELEA1GRID, name='grid', parent=self,
              pos=wx.Point(130, 100), size=wx.Size(480, 172),
              style=wx.VSCROLL | wx.THICK_FRAME)

        self.panelGraphFEC = wx.Panel(id=wxID_PANELEA1PANELGRAPHFEC,
              name=u'panelGraphFEC', parent=self, pos=wx.Point(72, 300),
              size=wx.Size(280, 224), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphFEC.SetBackgroundColour(wx.Colour(127, 127, 127))

        self.panelGraphFET = wx.Panel(id=wxID_PANELEA1PANELGRAPHFET,
              name=u'panelGraphFET', parent=self, pos=wx.Point(392, 300),
              size=wx.Size(280, 224), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphFET.SetBackgroundColour(wx.Colour(127, 127, 127))

        self.staticText2 = wx.StaticText(id=wxID_PANELEA1STATICTEXT2,
              label=u'Final energy\nconsumption (FEC)', name='staticText3',
              parent=self, pos=wx.Point(300, 70), size=wx.Size(219, 30),
              style=0)
        self.staticText2.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Sans'))

        self.staticText3 = wx.StaticText(id=wxID_PANELEA1STATICTEXT3,
              label=u'Final energy for\nthermal use', name='staticText4',
              parent=self, pos=wx.Point(460, 70), size=wx.Size(191, 30),
              style=0)
        self.staticText3.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Sans'))








