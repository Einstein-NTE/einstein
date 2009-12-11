#Boa:Frame:PanelEA2
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	PanelEA2- GUI component for: Primary energy - Yearly data
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Tom Sobota	21/03/2008
#       Revised by:         Hans Schweiger 28/03/2008
#                           Tom Sobota 29/03/2008
#       Revised by:         Tom Sobota  28/04/2008
#                           Stoyan Danov            18/06/2008
#                           Stoyan Danov    30/06/2008
#                           Stoyan Danov    03/07/2008
#                           Stoyan Danov    06/07/2008
#                           Stoyan Danov    07/07/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes to previous version:
#       28/03/08:           included functions draw ... (before in module)
#       29/03/08:           mod. to use external graphics module
#       28/04/2008          changed method display to display graphics the first time
#       18/06/2008 SD: change to translatable text _(...)
#       30/06/2008 SD: change esthetics - 1tab2fig
#       03/07/2008 SD: activate eventhandlers Fwd >>> and Back <<<
#       06/07/2008 SD: arrange column width, change background colour -> lightgrey
#       07/07/2008 SD:                       ->highlite Total
#       13/10/2008: SD  change _() to _U()
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	http://www.energyxperts.net/
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================

import wx

# import generic pie plot routine
from einstein.GUI.graphics import drawPiePlot
from numCtrl import *

from einstein.GUI.status import Status
# import the data processing module for this panel.
from einstein.modules.energyStats.moduleEA2 import *

# import the remapping module
import einstein.modules.matPanel as Mp
from GUITools import *

[wxID_PANELEA2, wxID_PANELEA2GRID, wxID_PANELEA2PANELGRAPHFEC,
 wxID_PANELEA2PANELGRAPHFET, wxID_PANELEA2STATICTEXT1,
 wxID_PANELEA2STATICTEXT2, wxID_PANELEA2STATICTEXT3,
] = [wx.NewId() for _init_ctrls in range(7)]
#
# constants
#


MAXROWS = 20
COLNO = 7

def _U(text):
    return unicode(_(text),"utf-8")

class PanelEA2(wx.Panel):

#------------------------------------------------------------------------------
    def __init__(self, parent=None):
#------------------------------------------------------------------------------
#   basic initialisation at build-up of the GUI
#------------------------------------------------------------------------------
        self._init_ctrls(parent)
        self.keys = ['EA2']
        self.mod = ModuleEA2(self.keys)
        self.mod.initPanel()
        
###xxxHS here could be simplified. in principle only no. of columns has to be known     
        data = Interfaces.GData[self.keys[0]]

        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO)

        labels_column = 0
        ignoredrows = [rows-1]

        #
        # left pie: FEC by fuel
        #

        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 2,                      # data column for this graph
                   'key'         : self.keys[0],                # key for Interface
                   'title'       : _U('FEC by fuel'),       # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphFEC,
                            wx.Panel,
                            drawPiePlot,
                            paramList)


        #
        # right pie: FET by fuel
        #
        paramList={'labels'      : labels_column,              # labels column
                   'data'        : 4,                          # data column for this graph
                   'key'         : self.keys[0],                    # key for Interface
                   'title'       : _U('FET by fuel'),# title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR,    # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphFET,
                            wx.Panel,
                            drawPiePlot,
                            paramList)
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
        self.grid.CreateGrid(MAXROWS, COLNO)

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
        self.grid.SetLabelFont(wx.Font(GRID_LABEL_SIZE, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Fuel type"))
        self.grid.SetColLabelValue(1, _U("MWh"))
        self.grid.SetColLabelValue(2, _U("%"))
        self.grid.SetColLabelValue(3, _U("MWh"))
        self.grid.SetColLabelValue(4, _U("%"))
        self.grid.SetColLabelValue(5, _U(" "))
        self.grid.SetColLabelValue(6, _U(" "))

        #
        # copy values from dictionary to grid
        #

        labels_column = 0
        decimals = [-1,0,1,0,1,-1,-1]   #number of decimal digits for each colum
        for r in range(MAXROWS):
            for c in range(COLNO):
                if c == labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid.SetGridCursor(0, 0)

        self.staticText2.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.staticText3.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))


    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=-1, name='', parent=prnt, pos=wx.Point(0,0),
              size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE)

#SD2008-06-30
        self.box1 = wx.StaticBox(self, -1, _U('Total final energy consumption (FEC) and final energy consumption for thermal use (FET)'),
                                 pos = (10,10),size=(780,240))

        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid = wx.grid.Grid(id=wxID_PANELEA2GRID, name='grid',parent=self,
              pos=wx.Point(20, 40), size=wx.Size(760, 200),
              style=0)

#SD2008-06-30
        self.box2 = wx.StaticBox(self, -1, _U('FEC by fuel'),
                                 pos = (10,270),size=(380,280))
        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelGraphFEC = wx.Panel(id=wxID_PANELEA2PANELGRAPHFEC,
              name=u'panelGraphFEC', parent=self, pos=wx.Point(20, 300),
              size=wx.Size(360, 240), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphFEC.SetBackgroundColour(wx.Colour(127, 127, 127))

#SD2008-06-30
        self.box3 = wx.StaticBox(self, -1, _U('FET by fuel'),
                                 pos = (410,270),size=(380,280))
        self.box3.SetForegroundColour(TITLE_COLOR)
        self.box3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.panelGraphFET = wx.Panel(id=wxID_PANELEA2PANELGRAPHFET,
              name=u'panelGraphFET', parent=self, pos=wx.Point(420, 300),
              size=wx.Size(370, 240), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphFET.SetBackgroundColour(wx.Colour(127, 127, 127))

        self.staticText2 = wx.StaticText(id=wxID_PANELEA2STATICTEXT2,
              label=_U('FEC'), name='staticText3',
              parent=self, pos=wx.Point(320, 24), size=wx.Size(219, 30),#SD pos (300, 70) before
              style=0)

        self.staticText3 = wx.StaticText(id=wxID_PANELEA2STATICTEXT3,
              label=_U('FET'), name='staticText4',
              parent=self, pos=wx.Point(490, 24), size=wx.Size(191, 30),#SD pos (460, 70) before
              style=0)

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
        Status.main.tree.SelectItem(Status.main.qEA1, select=True)
        event.Skip()

    def OnBtnForwardButton(self, event):
        self.Hide()
        Status.main.tree.SelectItem(Status.main.qEA3, select=True)
        print "Button exitModuleFwd: now I should show another window"
##        event.Skip()


#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   display function. carries out all the necessary calculations before
#   showing the panel
#------------------------------------------------------------------------------		

###xxxHS here could be simplified. in principle only no. of columns has to be known     
        data = Interfaces.GData[self.keys[0]]

        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO)

        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))


        attr2 = wx.grid.GridCellAttr()
        attr2.SetTextColour(GRID_LETTER_COLOR_HIGHLIGHT)
        attr2.SetBackgroundColour(GRID_BACKGROUND_COLOR_HIGHLIGHT)
        attr2.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

        labels_column = 0
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


#####Security feature against any strange thing in graphs
        try: self.panelGraphFEC.draw()
        except: pass
        try: self.panelGraphFET.draw()
        except: pass
        self.Show()
