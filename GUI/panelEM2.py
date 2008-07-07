#Boa:Frame:PanelEM1
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelEM2- GUI component for: Heat supply - Monthly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	28/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#       Revised by:         Tom Sobota  28/04/2008
#                           Stoyan Danov    18/06/2008
#                           Stoyan Danov    03/07/2008
#                           Stoyan Danov    04/07/2008
#
#       Changes to previous version:
#       28/04/2008          created method display
#       18/06/2008 SD: change to translatable text _(...)
#       03/07/2008 SD: activate eventhandlers Fwd >>> and Back <<<, esthetics & security features
#       04/07/2008 SD: changed min No columns, col width, 
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

from status import Status
from einstein.modules.energyStats.moduleEM2 import *
import einstein.modules.matPanel as Mp
from einstein.GUI.graphics import drawStackedBarPlot

[wxID_PANELEM2, wxID_PANELEM2BTNBACK, wxID_PANELEM2BTNFORWARD, 
 wxID_PANELEM2BTNOK, wxID_PANELEM2GRID1, wxID_PANELEM2PANELGRAPHMPHS, 
] = [wx.NewId() for _init_ctrls in range(6)]

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


class PanelEM2(wx.Panel):
    def __init__(self, parent):
        self._init_ctrls(parent)
        keys = ['EM2'] 
        self.mod = ModuleEM2(keys)

        labels_column = 0

        # remaps drawing methods to the wx widgets.
        #
        # single grid: Monthly process heat demand
        #
        paramList={'labels'      : labels_column,                 # labels column
                   'data'        : 4,                             # data column for this graph
                   'key'         : keys[0],                       # key for Interface
                   'title'       : _('Monthly process heat supply'), # title of the graph
                   'ylabel'      : _('UPH (MWh)'),                   # y axis label
                   'backcolor'   : GRAPH_BACKGROUND_COLOR,        # graph background color
                   'tickfontsize': 8,                             # tick label fontsize
                   'ignoredrows' : [0,1]}                        # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphMPHS,wx.Panel,drawStackedBarPlot,paramList)

        #
        # additional widgets setup
        #
        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        #
        # set grid properties
        # warning: this grid has a variable nr. of cols
        # so the 1st.row has the column headings
        data = Interfaces.GData[keys[0]]

#####Security feature against non existing GData entry
        COLNO1 = 5 # minimum number of columns-for the case if only ONE equipment exists
        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO1)
        
        self.grid1.CreateGrid(max(rows,20), max(COLNO1, cols))
        
        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.EnableEditing(False)
        headings = data[0] # extract the array of headings
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        for col in range(len(headings)):
            self.grid1.SetColSize(col,141)
            self.grid1.SetColLabelValue(col, headings[col])
        self.grid1.SetColSize(0,141)
        #
        # copy values from dictionary to grid
        # ignore the 1st. row, the column headings, which has been already
        # processed
#######LAYOUT: use of function numCtrl

        decimals = [-1]   #number of decimal digits for each colum
        for i in range(cols-1): #fill decimals list according numbers of columns (variable)
            decimals.append(1)
            
        for r in range(rows-1):
            self.grid1.SetRowAttr(r, attr)
            for c in range(cols):
                try:
                    if decimals[c] >= 0: # -1 indicates text
                        self.grid1.SetCellValue(r, c, \
                            convertDoubleToString(float(data[r+1][c]),nDecimals = decimals[c]))
                    else:
                        self.grid1.SetCellValue(r, c, data[r+1][c])
                except: pass
                if c == labels_column:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid1.SetGridCursor(0, 0)


    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEM2, name=u'PanelEM2', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

#...........box1....................................................................
        
        self.box1 = wx.StaticBox(self, -1, _(u'Monthly useful supply heat'),
                                 pos = (10,10),size=(780,200))

        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid1 = wx.grid.Grid(id=wxID_PANELEM2GRID1, name='grid1',
              parent=self, pos=wx.Point(20, 40), size=wx.Size(760, 160),
              style=0)

#...........box2....................................................................
        
        self.box2 = wx.StaticBox(self, -1, _(u'Distribution of useful supply heat per months'),
                                 pos = (10,230),size=(780,320))

        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelGraphMPHS = wx.Panel(id=wxID_PANELEM2PANELGRAPHMPHS,
              name=u'panelGraphMPHS', parent=self, pos=wx.Point(20, 260),
              size=wx.Size(760, 280), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphMPHS.SetBackgroundColour(wx.Colour(127, 127, 127))


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
        Status.main.tree.SelectItem(Status.main.qEM1, select=True)
        print "Button exitModuleBack: now I should show another window"

    def OnBtnForwardButton(self, event):
        event.Skip()
##        self.Hide()
##        Status.main.tree.SelectItem(Status.main.qEH1, select=True)
##        print "Button exitModuleFwd: now I should show another window"

#------------------------------------------------------------------------------
    def display(self):
#------------------------------------------------------------------------------		
#   display function. carries out all the necessary calculations before
#   showing the panel
#------------------------------------------------------------------------------
        try: self.panelGraphMPHS.draw()
        except: pass
        self.Show()
