#Boa:Frame:PanelEA4b
# -*- coding: iso-8859-15 -*- 
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	PanelEA4b - GUI component for: Process heat by temperature - Yearly data
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
#                           Stoyan Danov    01/07/2008
#                           Stoyan Danov    02/07/2008
#                           Stoyan Danov    03/07/2008
#
#       Changes to previous version:
#       29/03/08:       mod. to use external graphics module
#       28/04/2008      created method display
#       18/06/2008: SD  change to translatable text _(...)
#       19/06/2008: HS  some security features added
#       20/06/2008: SD  change esthetics - continue: layout, security features
#                       grid1 decimals control, changes of position and size of objects
#       01/07/2008: SD  adappted as panelEAb - heat demand by temperature
#       02/07/2008: SD  changed to orange colour (staticBox)
#       03/07/2008 SD: activate eventhandlers Fwd >>> and Back <<<
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
 wxID_PANELEA4STATICTEXT3
] = [wx.NewId() for _init_ctrls in range(8)]
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


###SD
#------------------------------------------------------------------------------		
#HS2008-03-22: 
#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		

#SD2008-07-02: from dummydata3 (moduleEA4)
##    if not hasattr(self, 'subplot'):
##        self.subplot = self.figure.add_subplot(1,1,1)
##    print 'Status.int.GData[UPH Plot][0] =', Status.int.GData['UPH Plot'][0]
##    print 'Status.int.GData[UPH Plot][1] =', Status.int.GData['UPH Plot'][1]
##    print 'Status.int.GData[UPH Plot][2] =', Status.int.GData['UPH Plot'][2]
##    self.subplot.plot(Status.int.GData['UPH Plot'][0],
##                      Status.int.GData['UPH Plot'][1],
##                      'go-', label='UPH', linewidth=2)
##    self.subplot.plot(Status.int.GData['UPH Plot'][0],
##                      Status.int.GData['UPH Plot'][2],
##                      'bo-', label='UPH net', linewidth=2)
##    self.subplot.plot(Status.int.GData['UPH Plot'][0],
##                      Status.int.GData['UPH Plot'][3],
##                      'rs-',  label='USH', linewidth=2)
##    self.subplot.axis([0, 15, 0, 10])
##    self.subplot.legend()

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    print 'Status.int.GData[UPH Plot][0] =', Status.int.GData['UPH Plot'][0]
    print 'Status.int.GData[UPH Plot][1] =', Status.int.GData['UPH Plot'][1]
    print 'Status.int.GData[UPH Plot][2] =', Status.int.GData['UPH Plot'][2]
    self.subplot.plot(Status.int.GData['UPH Plot'][0],
                      Status.int.GData['UPH Plot'][1],
                      'go-', label='UPH', linewidth=2)
    self.subplot.plot(Status.int.GData['UPH Plot'][0],
                      Status.int.GData['UPH Plot'][2],
                      'bo-', label='UPH net', linewidth=2)
    self.subplot.plot(Status.int.GData['UPH Plot'][0],
                      Status.int.GData['UPH Plot'][3],
                      'rs-',  label='USH', linewidth=2)
    self.subplot.axis([0, 100, 0, 3e+7])
    self.subplot.legend()

class PanelEA4b(wx.Panel):
    def __init__(self, parent):
        self._init_ctrls(parent)
        keys = ['EA4_UPH','HP Table','UPH Plot']###SD: keys[1] changed from 'EA4_HDP' 
        self.mod = ModuleEA4(keys)
        labels_column = 0

###SD
#   graphic: Cumulative heat demand by hours
        (rows,cols) = Interfaces.GData[keys[1]].shape        
#        ignoredrows = []
        ignoredrows = rows-1        
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : keys[2],                # key for Interface
                   'title'       : _('Some title'),           # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelEA4bFig, wx.Panel, drawFigure, paramList)
        del dummy

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

        key = keys[1]
        data = Interfaces.GData[key]
#####Security feature against non existing GData entry
        COLNO2 = 7 #grid has usually a fixed column size, not necessary to read from GData
        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO2)

        self.grid1.CreateGrid(max(rows,10), COLNO2)

        self.grid1.EnableGridLines(True)
#######LAYOUT: here the default row size is fixed
        self.grid1.SetDefaultRowSize(20)
        self.grid1.SetRowLabelSize(30)

#######LAYOUT: here the column size of the table is fixed (in pixels)
        self.grid1.SetColSize(0,115)
        self.grid1.SetColSize(1,90)
        self.grid1.SetColSize(2,90)
        self.grid1.SetColSize(3,95)
        self.grid1.SetColSize(4,105)
        self.grid1.SetColSize(5,105)
        self.grid1.SetColSize(6,105)
        self.grid1.EnableEditing(False)
        self.grid1.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid1.SetColLabelValue(0, _("Temperature levels\n[ºC]"))
        self.grid1.SetColLabelValue(1, _("no cumulative\n[MWh]"))
        self.grid1.SetColLabelValue(2, _("total\n[%]"))
        self.grid1.SetColLabelValue(3, _("cumulative\n[%]"))
        self.grid1.SetColLabelValue(4, _("no cumulative\n[MWh]"))
        self.grid1.SetColLabelValue(5, _("total\n[%]"))
        self.grid1.SetColLabelValue(6, _("cumulative\n[%]"))

        #
        # copy values from dictionary to grid
        #

#######LAYOUT: use of function numCtrl

        decimals = [-1,2,2,2,2,2,2]   #number of decimal digits for each colum
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
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
                else:
                    self.grid1.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid1.SetGridCursor(0, 0)        

###SD
##        self.staticText1.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.staticText2.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.staticText3.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA4, name=u'PanelEA4b', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))


        self.box1 = wx.StaticBox(self, -1, _(u'Heat demand (UPH) by process temperatures'),
                                 pos = (10,10),size=(780,200))

        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

###SD
##        self.staticText1 = wx.StaticText(id=-1,
##              label=_(u'Temperature levels'),
##              name='staticText1', parent=self, pos=wx.Point(60, 24),
##              size=wx.Size(50, 17), style=0)

        self.staticText2 = wx.StaticText(id=-1,
              label=_(u'Heat consumption by process temperature'),
              name='staticText2', parent=self, pos=wx.Point(200, 24),
              size=wx.Size(50, 17), style=0)

        self.staticText3 = wx.StaticText(id=-1,
              label=_(u'Total heat supply by central supply temperature'),
              name='staticText3', parent=self, pos=wx.Point(470, 24),
              size=wx.Size(50, 17), style=0)

        self.grid1 = wx.grid.Grid(id=wxID_PANELEA4GRID1, name='grid1',#SD
              parent=self, pos=wx.Point(20, 40), size=wx.Size(760, 160),
              style=0)


        self.box2 = wx.StaticBox(self, -1, _(u'Distribution of heat demand (UPH) by process temperatures'),
                                 pos = (10,230),size=(780,320))

        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))


###SD
        self.panelEA4bFig = wx.Panel(id=-1, name='panelEA4bFig', parent=self,
              pos=wx.Point(200, 260), size=wx.Size(400, 280), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelEA4bFig.SetBackgroundColour(wx.Colour(127, 127, 127))


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
        Status.main.tree.SelectItem(Status.main.qEA4a, select=True)
        print "Button exitModuleBack: now I should show another window"

    def OnBtnForwardButton(self, event):
        self.Hide()
        Status.main.tree.SelectItem(Status.main.qEA5, select=True)
        print "Button exitModuleFwd: now I should show another window"

        

    def display(self):

#####Security feature against any strange thing in graphs
        try:
##            self.panelGraphHD.draw()
###SD
            self.panelEA4bFig.draw()
        except: pass
        self.Show()
