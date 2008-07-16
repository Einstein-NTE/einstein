#Boa:Frame:PanelCS5
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelCS5- GUI component for: Energy performance - Monthly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger  05/07/2008
#       Revised by:         Stoyan Danov    14/07/2008
#
#       Changes to previous version:
#       14/07/2008 SD: adaptation to module CS
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
from einstein.modules.moduleCS import *
import einstein.modules.matPanel as Mp
from einstein.GUI.graphics import drawStackedBarPlot
from GUITools import *
from numCtrl import *

[wxID_PANELCS5, wxID_PANELCS5BTNBACK, wxID_PANELCS5BTNFORWARD, 
 wxID_PANELCS5BTNOK, wxID_PANELCS5GRID1, wxID_PANELCS5PANELGRAPHMPHD, 
] = [wx.NewId() for _init_ctrls in range(6)]


COLNO = 4
MAXROWS = 20

#============================================================================== 
#============================================================================== 
class PanelCS5(wx.Panel):
#============================================================================== 
#============================================================================== 
#------------------------------------------------------------------------------		
    def __init__(self, parent):
#------------------------------------------------------------------------------		
        self._init_ctrls(parent)
        keys = ['CS5 Plot','CS5 Table'] 
        self.mod = ModuleCS(keys)
        self.mod.updatePanel()

        labels_column = 0


        # remaps drawing methods to the wx widgets.
        #
        # single grid: Monthly process heat demand
        #
        paramList={'labels'      : 0,                            # labels column
                   'data'        : 2,                            # data column for this graph
                   'key'         : "CS5 Plot",                      # key for Interface
                   'title'       :_('Annual cost'), # title of the graph
                   'ylabel'      :_('Total annual cost [EUR]'),                   # y axis label
                   'legend'      :[_('Amortization [EUR]'),_('Energy cost [EUR]'),_('O&M cost [EUR]')],  # legend
                   'backcolor'   :GRAPH_BACKGROUND_COLOR,        # graph background color
                   'tickfontsize': 8,                            # tick label fontsize
                   'ignoredrows' :[]}                        # rows that should not be plotted
        
        dummy = Mp.MatPanel(self.panelGraphMPHD,wx.Panel,drawStackedBarPlot,
                            paramList)

        #
        # additional widgets setup
        #
        #
        # set grid properties
        # warning: this grid has a variable nr. of cols
        # so the 1st.row has the column headings
        self.grid1.CreateGrid(MAXROWS, COLNO)

        self.grid1.EnableGridLines(True)
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)
        self.grid1.SetColLabelSize(40)
        self.grid1.EnableEditing(False)
        
#        headings = data[0] # extract the array of headings

        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
#        for col in range(len(headings)):
#            self.grid1.SetColSize(col,141)
#            self.grid1.SetColLabelValue(col, headings[col])
        self.grid1.SetDefaultColSize(150)
        self.grid1.SetColSize(0,255)
        self.grid1.SetColLabelValue(0, _("Alternative"))
        self.grid1.SetColLabelValue(1, _("Amortization\n[EUR]"))
        self.grid1.SetColLabelValue(2, _("Energy cost\n[EUR]"))
        self.grid1.SetColLabelValue(3, _("Operation and maintenance\n(O&M) cost [EUR]"))

        self.display()

#------------------------------------------------------------------------------		
    def _init_ctrls(self, prnt):
#------------------------------------------------------------------------------		
        wx.Panel.__init__(self, id=wxID_PANELCS5, name=u'PanelCS5', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

#...........box1....................................................................
        
        self.box1 = wx.StaticBox(self, -1, _(u'Annual cost'),
                                 pos = (10,10),size=(780,200))

        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid1 = wx.grid.Grid(id=wxID_PANELCS5GRID1, name='grid1',
              parent=self, pos=wx.Point(20, 40), size=wx.Size(760, 160),
              style=0)

#...........box2.....................................................................
        
        self.box2 = wx.StaticBox(self, -1, _(u'Annual cost comparative'),
                                 pos = (10,230),size=(780,320))

        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelGraphMPHD = wx.Panel(id=wxID_PANELCS5PANELGRAPHMPHD,
              name=u'panelGraphMPHD', parent=self, pos=wx.Point(20, 260),
              size=wx.Size(760, 280), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphMPHD.SetBackgroundColour(wx.Colour(127, 127, 127))


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
        Status.main.tree.SelectItem(Status.main.qCS4, select=True)

    def OnBtnForwardButton(self, event):
        self.Hide()
        Status.main.tree.SelectItem(Status.main.qCS6, select=True)

#------------------------------------------------------------------------------
    def display(self):
#------------------------------------------------------------------------------		
#   display function. carries out all the necessary calculations before
#   showing the panel
#------------------------------------------------------------------------------

        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))

        # data cell attributes for totals row
        attr2 = wx.grid.GridCellAttr()
        attr2.SetTextColour(GRID_LETTER_COLOR_HIGHLIGHT)
        attr2.SetBackgroundColour(GRID_BACKGROUND_COLOR_HIGHLIGHT)
        attr2.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

        data = Status.int.GData["CS5 Table"]
        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO)
        
        decimals = [-1,2,2,2]   #number of decimal digits for each colum
        labels_column = 0
        
        for r in range(rows):
            if r == 0:
                self.grid1.SetRowAttr(r, attr2)
            else:
                self.grid1.SetRowAttr(r,attr)
                
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


        try: self.panelGraphMPHD.draw()
        except: pass
        
        self.Show()
        
#============================================================================== 

