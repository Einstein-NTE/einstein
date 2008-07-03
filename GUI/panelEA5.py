# -*- coding: cp1252 -*-
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
#       Revised by:         Tom Sobota  29/03/2008
#       Revised by:         Tom Sobota  28/04/2008
#                           Stoyan Danov            18/06/2008
#                           Stoyan Danov    30/06/2008
#                           Stoyan Danov    03/07/2008
#
#       Changes to previous version:
#       29/03/08:           mod. to use external graphics module
#       28/04/2008          created method display
#       18/06/2008 SD: change to translatable text _(...)
#       30/06/2008 SD: change esthetics - 2tab2fig
#       03/07/2008 SD: activate eventhandlers Fwd >>> and Back <<<
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
from numCtrl import *

from status import Status
from einstein.modules.energyStats.moduleEA5 import *
import einstein.modules.matPanel as Mp
from einstein.GUI.graphics import drawSimpleBarPlot, drawComparedBarPlot


[wxID_PANELEA5, wxID_PANELEA5GRID1, wxID_PANELEA5GRID2, 
 wxID_PANELEA5PANELGRAPHEI, wxID_PANELEA5PANELGRAPHSEC, 
 wxID_PANELEA5STATICTEXT1, wxID_PANELEA5STATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(7)]

#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem
ORANGE = '#FF6000'
TITLE_COLOR = ORANGE

##### HS 2006-07-01 aqui simetria de nomenclatura ... 
COLNO1 = 2#SD
COLNO2 = 4
MAXROWS = 10

class PanelEA5(wx.Panel):
    def __init__(self, parent):
        self._init_ctrls(parent)
        keys = ['EA5_EI', 'EA5_SEC']
        self.mod = ModuleEA5(keys)

#..............................................................................
# inicialización Grid 1

        labels_column = 0
        # remaps drawing methods to the wx widgets.
        #
        # upper graphic: Energy intensity
        #

#SD2008-06-30
        try:
            (rows,cols) = Interfaces.GData[keys[0]].shape
        except:
            print "PanelEA5: crash during initialisation avoided -> check this"
            rows = 1 #xxx dummy for avoiding crash
            cols = MAXCOLS #xxx dummy for avoiding crash
            
        ignoredrows = []
        ignoredrows.append(rows-1)

        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 1,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : _('Energy intensity'),     # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : [2]}                    # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphEI,wx.Panel,drawSimpleBarPlot,paramList)

#..............................................................................
# initialization Grid 2

        #
        # lower grid: SEC by product
        #

#SD2008-06-30
        try:
            (rows,cols) = Interfaces.GData[keys[1]].shape
        except:
            print "PanelEA5: crash during initialisation avoided -> check this"
            rows = 1 #xxx dummy for avoiding crash
            cols = MAXCOLS #xxx dummy for avoiding crash
        
        ignoredrows = []
        ignoredrows.append(rows-1)

        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 1,                      # data column for this graph
                   'key'         : keys[1],                # key for Interface
                   'title'       : _('SEC by product'),       # title of the graph
                   'ylabel'      : 'Energy',
                   'legend'      : [_('Energy by fuels'), _('Energy by electricity'), _('Primary energy')], # legend
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphSEC,wx.Panel,drawComparedBarPlot,paramList)
        
        #
        # additional widgets setup
        #
        #
        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        #
        # set upper grid
        #

        
#..............................................................................
# write data to grid 1

        data = Interfaces.GData[keys[0]]

#SD2008-06-30: like in EA1
# HS:2007-07-01 -> los dos controles son exactamente equivalentes
#       data = Interfaces.GData[keys[0]]
#       (rows,cols) = data.shape
#
#       y
#
#       (rows,cols) = Interfaces.GData[keys[0]].shape
#
#       -> es idéntico
#
#####Security feature against non existing GData entry
        COLNO1 = 2 #grid has usually a fixed column size, not necessary to read from GData        
        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO1)

        self.grid1.CreateGrid(max(rows,10), COLNO1)

        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.SetColSize(0,140)
        self.grid1.SetColSize(1,125)
        self.grid1.EnableEditing(False)
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, _("Energy type"))
        self.grid1.SetColLabelValue(1, _("Energy intensity\n[kWh/EUR]"))
        #
        # copy values from dictionary to grid
        #


#SD2008-06-30
        decimals = [-1,2]   #number of decimal digits for each colum
        for r in range(rows):
            self.grid1.SetRowAttr(r, attr)
            for c in range(cols):
                try:
                    if decimals[c] >= 0: # -1 indicates text
                        self.grid1.SetCellValue(r, c, \
                            convertDoubleToString(float(data[r][c]),nDecimals = decimals[c]))
                    else:
                        self.grid1.SetCellValue(r, c, data[r][c])
                except: pass
                if c == labels_column:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);


        self.grid1.SetGridCursor(0, 0)

#..............................................................................
# write data to grid 2

        data = Interfaces.GData[keys[1]]

#SD2008-06-30: like in EA1
#####Security feature against non existing GData entry


        COLNO1 = 4 #grid has usually a fixed column size, not necessary to read from GData        
        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO1)

        self.grid2.CreateGrid(max(rows,20), cols)

        self.grid2.EnableGridLines(True)
        self.grid2.SetDefaultRowSize(20)
        self.grid2.SetRowLabelSize(30)
        self.grid2.SetColLabelSize(50)
        self.grid2.SetColSize(0,100)
        self.grid2.SetColSize(1,100)
        self.grid2.SetColSize(2,100)
        self.grid2.SetColSize(3,100)
        self.grid2.EnableEditing(False)
        self.grid2.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid2.SetColLabelValue(0, _("Product"))
        self.grid2.SetColLabelValue(1, _("Energy by\nfuels\n[kWh/pu]"))
        self.grid2.SetColLabelValue(2, _("Energy by\nelectricity\n[kWh/pu]"))
        self.grid2.SetColLabelValue(3, _("Primary\nenergy\n[kWh/pu]"))
        #
        # copy values from dictionary to grid
        #

#SD2008-06-30

        decimals = [-1,2,2,2]   #number of decimal digits for each colum
        for r in range(rows):
            self.grid2.SetRowAttr(r, attr)
            for c in range(cols):
                try:
                    if decimals[c] >= 0: # -1 indicates text
                        self.grid2.SetCellValue(r, c, \
                            convertDoubleToString(float(data[r][c]),nDecimals = decimals[c]))
                    else:
                        self.grid2.SetCellValue(r, c, data[r][c])
                except: pass
                if c == labels_column:
                    self.grid2.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid2.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);


        self.grid2.SetGridCursor(0, 0)

##        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))


#HS 2006-07-01: cancelado. staticText2 ya no existe.
# es extraño que esto no te haya dado error .... ???? -> tu vas comprobando el LOGfile ????
#        self.staticText2.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))

#------------------------------------------------------------------------------		
    def _init_ctrls(self, prnt):
#------------------------------------------------------------------------------		
#   build-up of controls
#------------------------------------------------------------------------------		
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA5, name=u'PanelEA5', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))

#..............................................................................
#   box 1

#SD2008-06-30
        self.box1 = wx.StaticBox(self, -1, _(u'Energy intensity by energy type (turnover)'),
                                 pos = (10,10),size=(780,260))

        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

##        self.staticText1 = wx.StaticText(id=wxID_PANELEA5STATICTEXT1,
##              label=_(u'Energy intensity by energy type (turnover)'),
##              name='staticText1', parent=self, pos=wx.Point(40, 8),
##              size=wx.Size(580, 20), style=0)

        self.grid1 = wx.grid.Grid(id=wxID_PANELEA5GRID1, name='grid1',#SD
              parent=self, pos=wx.Point(20, 40), size=wx.Size(440, 220),
              style=0)

        self.panelGraphEI = wx.Panel(id=wxID_PANELEA5PANELGRAPHEI,
              name=u'panelGraphEI', parent=self, pos=wx.Point(480, 40),
              size=wx.Size(300, 220), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphEI.SetBackgroundColour(wx.Colour(127, 127, 127))

#..............................................................................
#   box 2

#SD2008-06-30
        self.box2 = wx.StaticBox(self, -1, _(u'Specific energy consumption (SEC) by product.'),
                                 pos = (10,290),size=(780,260))
        
        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

##        self.staticText2 = wx.StaticText(id=wxID_PANELEA5STATICTEXT2,
##              label=_(u'Specific energy consumption (SEC) by product.'),
##              name='staticText2', parent=self, pos=wx.Point(40, 324),
##              size=wx.Size(580, 20), style=0)


        self.grid2 = wx.grid.Grid(id=wxID_PANELEA5GRID2, name='grid2',
              parent=self, pos=wx.Point(20, 320), size=wx.Size(440, 220),
              style=0)


        self.panelGraphSEC = wx.Panel(id=wxID_PANELEA5PANELGRAPHSEC,
              name=u'panelGraphSEC', parent=self, pos=wx.Point(480, 320),
              size=wx.Size(300, 220), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphSEC.SetBackgroundColour(wx.Colour(127, 127, 127))

#..............................................................................
#   default buttons
#..............................................................................
        self.btnBack = wx.Button(id=wx.ID_BACKWARD, label=u'<<<',
              name=u'btnBack', parent=self, pos=wx.Point(500, 560),
              size=wx.Size(80, 20), style=0)
        self.btnBack.Bind(wx.EVT_BUTTON, self.OnBtnBackButton,
              id=-1)

        self.btnOK = wx.Button(id=wx.ID_OK, label=_(u'OK'), name=u'btnOK',
              parent=self, pos=wx.Point(600, 560), size=wx.Size(80, 20),
              style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=-1)

        self.btnForward = wx.Button(id=wx.ID_FORWARD, label=u'>>>',
              name=u'btnForward', parent=self, pos=wx.Point(700, 560),
              size=wx.Size(80, 20), style=0)
        self.btnForward.Bind(wx.EVT_BUTTON, self.OnBtnForwardButton,
              id=-1)


#------------------------------------------------------------------------------		
#   Event handlers for default buttons
#------------------------------------------------------------------------------		
    def OnBtnOKButton(self, event):
        event.Skip()

    def OnBtnBackButton(self, event):
        self.Hide()
        Status.main.tree.SelectItem(Status.main.qEA4b, select=True)
        print "Button exitModuleBack: now I should show another window"

    def OnBtnForwardButton(self, event):
        self.Hide()
        Status.main.tree.SelectItem(Status.main.qEM1, select=True)
        print "Button exitModuleFwd: now I should show another window"


#------------------------------------------------------------------------------	
    def display(self):
#------------------------------------------------------------------------------		
#   display function. carries out all the necessary calculations before
#   showing the panel
#------------------------------------------------------------------------------	
#####Security feature against any strange thing in graphs
        try: self.panelGraphEI.draw()
        except: pass
        try: self.panelGraphSEC.draw()
        except: pass
        self.Show()


