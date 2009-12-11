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
#                           Stoyan Danov    18/06/2008
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
#       30/06/2008 SD: change esthetics - 2tab2fig
#       03/07/2008 SD: activate eventhandlers Fwd >>> and Back <<<
#       06/07/2008 SD: arrange column width, change background colour -> lightgrey,
#                       security feature modified (see #SD2008-07-06)
#       07/07/2008 SD:                       ->highlite Total
#       13/10/2008: SD  change _() to _U()
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
from einstein.modules.energyStats.moduleEA3 import *
import einstein.modules.matPanel as Mp
from GUITools import *

[wxID_PANELEA3, wxID_PANELEA3GRID1, wxID_PANELEA3GRID2, 
 wxID_PANELEA3PANELGRAPHFET, wxID_PANELEA3STATICTEXT1, 
 wxID_PANELEA3STATICTEXT2, wxID_PANELEA3STATICTEXT3,
 wxID_PANELEA3STATICTEXT4, wxID_PANELEA3PANELGRAPHUSH,
] = [wx.NewId() for _init_ctrls in range(9)]
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

MAXCOLS = 10

def _U(text):
    return unicode(_(text),"utf-8")

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
#SD2008-07-06
##        try:
##            (rows,cols) = Interfaces.GData[keys[0]].shape
##        except:
##            print "PanelEA3: crash during initialisation avoided -> check this"
##            rows = 1 #xxx dummy for avoiding crash
##            cols = MAXCOLS #xxx dummy for avoiding crash
        (rows,cols) = Interfaces.GData[keys[0]].shape
        ignoredrows = [rows-1]

        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : _U('FET by equipment'),     # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphFET,
                            wx.Panel,
                            drawPiePlot,
                            paramList)
        #
        # lower graph: USH by equipment
        #
#SD2008-07-06
##        try:
##            (rows,cols) = Interfaces.GData[keys[1]].shape
##        except:
##            print "PanelEA3: crash during initialisation avoided -> check this"
##            rows = 1 #xxx dummy for avoiding crash
##            cols = MAXCOLS #xxx dummy for avoiding crash
        (rows,cols) = Interfaces.GData[keys[1]].shape   
        ignoredrows = [rows-1]

        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 2,                      # data column for this graph
                   'key'         : keys[1],                # key for Interface
                   'title'       : _U('USH by equipment'),     # title of the graph
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
        data = Interfaces.GData[keys[0]]

#####Security feature against non existing GData entry
        COLNO1 = 4 #grid has usually a fixed column size, not necessary to read from GData        
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
        self.grid1.CreateGrid(max(rows,10), COLNO1)

        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)

        self.grid1.SetColSize(0,125)
        self.grid1.SetColSize(1,110)
        self.grid1.SetColSize(2,85)
        self.grid1.SetColSize(3,70)

        self.grid1.EnableEditing(False)
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, _U("Equipment"))
        self.grid1.SetColLabelValue(1, _U("Fuel type"))
        self.grid1.SetColLabelValue(2, _U("MWh"))
        self.grid1.SetColLabelValue(3, _U("%"))
        #
        # copy values from dictionary to grid
        #

#SD2008-06-30
        decimals = [-1,-1,0,1]   #number of decimal digits for each colum
        for r in range(rows):
            if r < rows-1:
                self.grid1.SetRowAttr(r, attr)
            else:
                self.grid1.SetRowAttr(r,attr2)  #highlight totals row
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
                elif c == 1:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);                
                else:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid1.SetGridCursor(0, 0)
        #
        # set lower grid
        #
        data = Interfaces.GData[keys[1]]

#####Security feature against non existing GData entry
        COLNO1 = 4 #grid has usually a fixed column size, not necessary to read from GData        
        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO1)

        self.grid2.CreateGrid(max(rows,10), COLNO1)

        self.grid2.EnableGridLines(True)
        self.grid2.SetDefaultRowSize(20)
        self.grid2.SetRowLabelSize(30)

        self.grid2.SetColSize(0,125)
        self.grid2.SetColSize(1,85)
        self.grid2.SetColSize(2,70)
        self.grid2.SetColSize(3,110)
        
        self.grid2.EnableEditing(False)
        self.grid2.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid2.SetColLabelValue(0, _U("Equipment"))
        self.grid2.SetColLabelValue(1, _U("MWh"))
        self.grid2.SetColLabelValue(2, _U("%"))
        self.grid2.SetColLabelValue(3, _U(" "))
        #
        # copy values from dictionary to grid
        #

#SD2008-06-30
        decimals = [-1,0,1,-1]   #number of decimal digits for each colum
        for r in range(rows):
            if r < rows-1:
                self.grid2.SetRowAttr(r, attr)
            else:
                self.grid2.SetRowAttr(r,attr2)  #highlight totals row
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

    def _init_ctrls(self, prnt):

        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA3, name=u'PanelEA3', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))
#..............................................................................
#   box 1

        self.box1 = wx.StaticBox(self, -1, _U('Final energy consumption for thermal use (FET) by equipment'),
                                 pos = (10,10),size=(780,260))
        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))


        self.grid1 = wx.grid.Grid(id=wxID_PANELEA3GRID1, name='grid1',#SD
              parent=self, pos=wx.Point(20, 40), size=wx.Size(440, 220),
              style=0)

        self.panelGraphFET = wx.Panel(id=wxID_PANELEA3PANELGRAPHFET,
              name=u'panelGraphFET', parent=self, pos=wx.Point(480, 40),
              size=wx.Size(300, 220), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphFET.SetBackgroundColour(wx.Colour(127, 127, 127))

#..............................................................................
#   box 2

        self.box2 = wx.StaticBox(self, -1, _U('Useful supply heat (USH) by equipment'),
                                 pos = (10,290),size=(780,260))
        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.grid2 = wx.grid.Grid(id=wxID_PANELEA3GRID2, name='grid2',
              parent=self, pos=wx.Point(20, 320), size=wx.Size(440, 220),
              style=0)


        self.panelGraphUSH = wx.Panel(id=wxID_PANELEA3PANELGRAPHUSH,
              name=u'panelGraphUSH', parent=self, pos=wx.Point(480, 320),
              size=wx.Size(300, 220), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphUSH.SetBackgroundColour(wx.Colour(127, 127, 127))

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
        Status.main.tree.SelectItem(Status.main.qEA2, select=True)
        print "Button exitModuleBack: now I should show another window"

    def OnBtnForwardButton(self, event):
        self.Hide()
        Status.main.tree.SelectItem(Status.main.qEA4a, select=True)
        print "Button exitModuleFwd: now I should show another window"


#------------------------------------------------------------------------------	
    def display(self):
#------------------------------------------------------------------------------		
#   display function. carries out all the necessary calculations before
#   showing the panel
#------------------------------------------------------------------------------	
#####Security feature against any strange thing in graphs
        try: self.panelGraphFET.draw()
        except: pass
        try: self.panelGraphUSH.draw()
        except: pass
        self.Show()
