#Boa:Frame:PanelEA4
#==============================================================================
#
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
#	Version No.: 0.05
#	Created by: 	    Tom Sobota      21/03/2008
#       Revised by:         Tom Sobota      29/03/2008
#       Revised by:         Tom Sobota      28/04/2008
#                           Stoyan Danov    18/06/2008
#                           Hans Schweiger  19/06/2008
#                           Stoyan Danov    20/06/2008
#
#       Changes to previous version:
#       29/03/08:       mod. to use external graphics module
#       28/04/2008      created method display
#       18/06/2008: SD  change to translatable text _(...)
#       19/06/2008: HS  some security features added
#       20/06/2008: SD  change esthetics - continue: layout, security features
#                       grid1 decimals control, changes of position and size of objects
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
from einstein.modules.energyStats.moduleEA4 import *
import einstein.modules.matPanel as Mp

[wxID_PANELEA4, wxID_PANELEA4GRID1, wxID_PANELEA4GRID2, 
 wxID_PANELEA4PANELGRAPHUPH, wxID_PANELEA4PANELGRAPHHD,
 wxID_PANELEA4STATICTEXT1, wxID_PANELEA4STATICTEXT2,
 wxID_PANELEA4STATICTEXT3, 
] = [wx.NewId() for _init_ctrls in range(8)]
#
# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem


class PanelEA4(wx.Panel):
    def __init__(self, parent):
        self._init_ctrls(parent)
        keys = ['EA4_UPH', 'EA4_HDP'] 
        self.mod = ModuleEA4(keys)
        labels_column = 0
        # remaps drawing methods to the wx widgets.
        #
        # upper graphic: UPH demand by process
        #
        (rows,cols) = Interfaces.GData[keys[0]].shape
        ignoredrows = [rows-1]
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 2,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : _('UPH by process'),       # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphUPH,
                            wx.Panel,
                            drawPiePlot,
                            paramList)

        #
        # lower graphic: Heat demand by process temperature
        #
        # no rows to ignore here
        paramList={'labels'      : labels_column,              # labels column
                   'data'        : 3,                          # data column for this graph
                   'key'         : keys[1],                    # key for Interface
                   'title'       : _('HD by process temperature'),# title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR}     # graph background color

        dummy = Mp.MatPanel(self.panelGraphHD,
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
        key = keys[0]
        data = Interfaces.GData[key]

        
#####Security feature against non existing GData entry
        COLNO1 = 3 #grid has usually a fixed column size, not necessary to read from GData
        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO1)
        
        self.grid1.CreateGrid(max(rows,10), COLNO1)

        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)

        self.grid1.SetColSize(0,115)
        self.grid1.SetColSize(1,91)#SD added
        self.grid1.SetColSize(2,91)#SD added
        self.grid1.EnableEditing(False)
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, _("Process"))
        self.grid1.SetColLabelValue(1, _("MWh"))
        self.grid1.SetColLabelValue(2, _("%"))
        #
        # copy values from dictionary to grid
        #
##        for r in range(rows): #SD: initial state
##            self.grid1.SetRowAttr(r, attr)
##            for c in range(cols):
##                self.grid1.SetCellValue(r, c, data[r][c])
##                if c == labels_column:
##                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
##                else:
##                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);
##
##        self.grid1.SetGridCursor(0, 0)

#######LAYOUT: use of function numCtrl, SD new one with decimals control

        decimals = [-1,0,1]   #number of decimal digits for each colum
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

        


    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA4, name=u'PanelEA4', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))


        self.box1 = wx.StaticBox(self, -1, _(u'Useful process heat (UPH) demand by process'),
                                 pos = (10,10),size=(780,240))

        
#######LAYOUT: here the position (pos) and size (size) of the grid is fixed.
#######        default PANEL size = 800 x 600 pixels. (0,0) is the left upper corner.
        self.grid1 = wx.grid.Grid(id=wxID_PANELEA4GRID1, name='grid1',#SD
              parent=self, pos=wx.Point(20, 40), size=wx.Size(760, 200),
              style=0)

#######LAYOUT: static text can be moved in a similar way
        self.box2 = wx.StaticBox(self, -1, _(u'Heat demand by process temperature'),
                                 pos = (10,270),size=(380,280))

#######LAYOUT: here the position (pos) and size (size) of the figure-panels is fixed.
#######        default PANEL size = 800 x 600 pixels. (0,0) is the left upper corner.
        self.panelGraphUPH = wx.Panel(id=wxID_PANELEA4PANELGRAPHUPH,
              name=u'panelGraphUPH', parent=self, pos=wx.Point(20, 300),
              size=wx.Size(360, 240), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphUPH.SetBackgroundColour(wx.Colour(127, 127, 127))

#######LAYOUT: static text can be moved in a similar way
        self.box3 = wx.StaticBox(self, -1, _(u'Heat demand by ?????'),
                                 pos = (410,270),size=(380,280))
        
#######LAYOUT: here the position (pos) and size (size) of the figure-panels is fixed.
#######        default PANEL size = 800 x 600 pixels. (0,0) is the left upper corner.
        self.panelGraphHD = wx.Panel(id=wxID_PANELEA4PANELGRAPHHD,
              name=u'panelGraphHD', parent=self, pos=wx.Point(420, 300),
              size=wx.Size(360, 240), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphHD.SetBackgroundColour(wx.Colour(127, 127, 127))

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
        event.Skip()

    def OnBtnForwardButton(self, event):
        event.Skip()

#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   display function. carries out all the necessary calculations before
#   showing the panel
#------------------------------------------------------------------------------		

#####Security feature against any strange thing in graphs
        try: self.panelGraphUPH.draw()
        except: pass
        try: self.panelGraphHD.draw()
        except: pass
        self.Show()
