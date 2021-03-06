#Boa:Frame:PanelCS2
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelCS2- Comparative analysis: Useful process and supply heat
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger  05/07/2008
#       Revised by:         Stoyan Danov    09/07/2008
#                           Stoyan Danov    10/07/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes to previous version:#
#       09/07/2008 SD: created from CS1, columns and graphics adapted
#       10/07/2008 SD: graphic ComparedBarPlot set, labels and legend arranged
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

from status import Status
from einstein.modules.moduleCS import *
import einstein.modules.matPanel as Mp
from einstein.GUI.graphics import drawComparedBarPlot
from GUITools import *
from numCtrl import *

[wxID_PANELCS2, wxID_PANELCS2BTNBACK, wxID_PANELCS2BTNFORWARD, 
 wxID_PANELCS2BTNOK, wxID_PANELCS2GRID1, wxID_PANELCS2PANELGRAPHMPHD, 
] = [wx.NewId() for _init_ctrls in range(6)]


COLNO = 5
MAXROWS = 20

def _U(text):
    return unicode(_(text),"utf-8")

#============================================================================== 
#============================================================================== 
class PanelCS2(wx.Panel):
#============================================================================== 
#============================================================================== 
#------------------------------------------------------------------------------		
    def __init__(self, parent):
#------------------------------------------------------------------------------		
        self._init_ctrls(parent)
        keys = ['CS2_Plot','CS2_Table'] 
        self.mod = ModuleCS(keys)
        self.mod.updatePanel()

        labels_column = 0


        # remaps drawing methods to the wx widgets.
        #
        # single grid: Monthly process heat demand
        #
        paramList={'labels'      : 0,                            # labels column
                   'data'        : 2,                            # data column for this graph
                   'key'         : "CS2_Plot",                      # key for Interface
                   'title'       :_U('Relative comparison of prosess & supply heat'), # title of the graph
                   'ylabel'      :_U('[%]'),                   # y axis label
                   'legend'      :[_U('USH [% of present state]'),_U('UPH [% of present state]')],                   # y axis label
                   'backcolor'   :GRAPH_BACKGROUND_COLOR,        # graph background color
                   'tickfontsize': 8,                            # tick label fontsize
                   'ignoredrows' :[]}                        # rows that should not be plotted
        
        dummy = Mp.MatPanel(self.panelGraphMPHD,wx.Panel,drawComparedBarPlot,
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
        self.grid1.SetDefaultColSize(130)
        self.grid1.SetColSize(0,185)
        self.grid1.SetColLabelValue(0, _U("Alternative"))
        self.grid1.SetColLabelValue(1, _U("Useful process\nheat (UPH) [MWh]"))
        self.grid1.SetColLabelValue(2, _U("Savings (UPH)\n[MWh]"))
        self.grid1.SetColLabelValue(3, _U("Useful supply\nheat (USH) [MWh]"))
        self.grid1.SetColLabelValue(4, _U("Savings (USH)\n[MWh]"))

        self.display()

#------------------------------------------------------------------------------		
    def _init_ctrls(self, prnt):
#------------------------------------------------------------------------------		
        wx.Panel.__init__(self, id=wxID_PANELCS2, name=u'PanelCS2', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

#...........box1....................................................................
        
        self.box1 = wx.StaticBox(self, -1, _U('Useful process and supply heat (UPH and USH)'),
                                 pos = (10,10),size=(780,200))

        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid1 = wx.grid.Grid(id=wxID_PANELCS2GRID1, name='grid1',
              parent=self, pos=wx.Point(20, 40), size=wx.Size(760, 160),
              style=0)

#...........box2.....................................................................
        
        self.box2 = wx.StaticBox(self, -1, _U('Relative comparison of process and supply heat'),
                                 pos = (10,230),size=(780,320))

        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelGraphMPHD = wx.Panel(id=wxID_PANELCS2PANELGRAPHMPHD,
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
        Status.main.tree.SelectItem(Status.main.qCS1, select=True)

    def OnBtnForwardButton(self, event):
        self.Hide()
        Status.main.tree.SelectItem(Status.main.qCS3, select=True)

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

        data = Status.int.GData["CS2_Table"]
        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO)
        
        decimals = [-1,2,2,2,2]   #number of decimal digits for each colum
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

