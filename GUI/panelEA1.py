#Boa:Frame:PanelEA1
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelEA1- GUI component for: Final energy by fuels - Yearly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	22/03/2008
#       Revised by:         Tom Sobota 29/03/2008
#       Revised by:         Tom Sobota  28/04/2008
#                           Stoyan Danov            18/06/2008
#                           Stoyan Danov    30/06/2008
#                           Stoyan Danov    03/07/2008
#                           Stoyan Danov    06/07/2008
#                           Stoyan Danov    07/07/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes to previous version:
#       29/03/08:           mod. to use external graphics module
#       28/04/2008          created method display
#       18/06/2008 SD: change to translatable text _(...)
#       30/06/2008 SD: change esthetics - 1tab2fig
#       03/07/2008 SD: activate eventhandlers Fwd >>> and Back <<<
#       06/07/2008 SD: arrange column width, change background colour -> lightgrey
#       07/07/2008 SD:                       ->highlite Total
#       13/10/2008: SD  change _() to _U()
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
from einstein.modules.energyStats.moduleEA1 import *
import einstein.modules.matPanel as Mp
from GUITools import *


[wxID_PANELEA1, wxID_PANELEA1GRID, wxID_PANELEA1PANELGRAPHPEC, 
 wxID_PANELEA1PANELGRAPHPET, wxID_PANELEA1STATICTEXT1, 
 wxID_PANELEA1STATICTEXT2, wxID_PANELEA1STATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(7)]

#
# constants
#

ORANGE = '#FF6000'
LIGHTGREY = '#F8F8F8'
WHITE = '#FFFFFF'
DARKGREY = '#000060'
LIGHTGREEN = '#F0FFFF'

GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = DARKGREY     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = LIGHTGREY # idem
GRAPH_BACKGROUND_COLOR = WHITE # idem
TITLE_COLOR = ORANGE

def _U(text):
    return unicode(_(text),"utf-8")

class PanelEA1(wx.Panel):
    def __init__(self, parent):
        self._init_ctrls(parent)
        keys = ['EA1'] 
        self.mod = ModuleEA1(keys)
        labels_column = 0
        ignoredrows = [2] # totals row is always n.3

        #
        # left pie: PEC by fuel
        #
        paramList={'labels'      : 0,                     # labels column
                   'data'        : 2,                     # data column for this graph
                   'key'         : keys[0],               # key for Interface
                   'title'       :_U('PEC by fuel'),          # title of the graph
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
                   'title'       :_U('PET by fuel'),          # title of the graph
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

#####Security feature against non existing GData entry
        COLNO1 = 7 #grid has usually a fixed column size, not necessary to read from GData        
        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO1)

        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))


        attr2 = wx.grid.GridCellAttr()
        attr2.SetTextColour(GRID_LETTER_COLOR_HIGHLIGHT)
        attr2.SetBackgroundColour(GRID_BACKGROUND_COLOR_HIGHLIGHT)
        attr2.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        #
        # set upper grid
        #
        
        self.grid.CreateGrid(max(rows,10), COLNO1)

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        
        self.grid.SetColSize(0,195)
        self.grid.SetColSize(1,85)
        self.grid.SetColSize(2,85)
        self.grid.SetColSize(3,85)
        self.grid.SetColSize(4,85)
        self.grid.SetColSize(5,85)
        self.grid.SetColSize(6,85)
        
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Fuel type"))
        self.grid.SetColLabelValue(1, _U("MWh"))
        self.grid.SetColLabelValue(2, _U("%"))
        self.grid.SetColLabelValue(3, _U("MWh"))
        self.grid.SetColLabelValue(4, _U("%"))
        self.grid.SetColLabelValue(5, _U(" "))
        self.grid.SetColLabelValue(6, _U(" "))
        
        self.grid.SetCellValue(0,0,_U("Total Fuels"))
        self.grid.SetCellValue(1,0,_U("Total Electricity"))
        self.grid.SetCellValue(2,0,_U("Total (Fuels+Electricity)"))
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        #
        # copy values from dictionary to grid
        #


#SD2008-06-30
        decimals = [-1,0,1,0,1,-1,-1]   #number of decimal digits for each colum
        for r in range(rows):
            if r < rows-1:
                self.grid.SetRowAttr(r, attr)
            else:
                self.grid.SetRowAttr(r,attr2)  #highlight totals row
            for c in range(cols):
                try:
                    if decimals[c] >= 0: # -1 indicates text
                        self.grid.SetCellValue(r, c, \
                            convertDoubleToString(float(data[r][c]),nDecimals = decimals[c]))
                    else:
                        self.grid.SetCellValue(r, c, data[r][c])
                except: pass
                if c == labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

##################
        self.grid.SetGridCursor(0, 0)

##        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.staticText2.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.staticText3.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA1, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600),
              style=wx.DEFAULT_FRAME_STYLE)

#SD2008-06-30
        self.box1 = wx.StaticBox(self, -1, _U('Total primary energy consumption (PEC) and primary energy consumption for thermal use (PET)'),
                                 pos = (10,10),size=(780,240))        

        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid = wx.grid.Grid(id=wxID_PANELEA1GRID, name='grid', parent=self,
              pos=wx.Point(20, 40), size=wx.Size(760, 200),
              style=0)

#SD2008-06-30
        self.box2 = wx.StaticBox(self, -1, _U('PEC by fuel'),
                                 pos = (10,270),size=(380,280))
        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelGraphPEC = wx.Panel(id=wxID_PANELEA1PANELGRAPHPEC,
              name=u'panelGraphPEC', parent=self, pos=wx.Point(20, 300),
              size=wx.Size(360, 240), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphPEC.SetBackgroundColour(wx.Colour(127, 127, 127))

#SD2008-06-30
        self.box3 = wx.StaticBox(self, -1, _U('PET by fuel'),
                                 pos = (410,270),size=(380,280))

        self.box3.SetForegroundColour(TITLE_COLOR)
        self.box3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelGraphPET = wx.Panel(id=wxID_PANELEA1PANELGRAPHPET,
              name=u'panelGraphPET', parent=self, pos=wx.Point(420, 300),
              size=wx.Size(360, 240), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphPET.SetBackgroundColour(wx.Colour(127, 127, 127))

        self.staticText2 = wx.StaticText(id=wxID_PANELEA1STATICTEXT2,
              label=_U('PEC'), name='staticText2', parent=self, pos=wx.Point(320,
              24), size=wx.Size(56, 17), style=0)

        self.staticText3 = wx.StaticText(id=wxID_PANELEA1STATICTEXT3,
              label=_U('PET'), name='staticText3', parent=self, pos=wx.Point(490,
              24), size=wx.Size(40, 17), style=0)

#..............................................................................
#   default buttons
#..............................................................................
        self.btnBack = wx.Button(id=wx.ID_BACKWARD, label=u'<<<',
              name=u'btnBack', parent=self, pos=wx.Point(500, 560),
              size=wx.Size(80, 20), style=0)
        self.btnBack.Bind(wx.EVT_BUTTON, self.OnBtnBackButton,
              id=-1)

        self.btnOK = wx.Button(id=wx.ID_OK, label=_U('OK'), name=u'btnOK',
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

    def OnBtnForwardButton(self, event):
        self.Hide()
        Status.main.tree.SelectItem(Status.main.qEA2, select=True)


#------------------------------------------------------------------------------
    def display(self):
#------------------------------------------------------------------------------
#   display function. carries out all the necessary calculations before
#   showing the panel
#------------------------------------------------------------------------------	        

#####Security feature against any strange thing in graphs
        try: self.panelGraphPEC.draw()
        except: pass
        try: self.panelGraphPET.draw()
        except: pass
        self.Show()
