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
from GUITools import *
import einstein.modules.matPanel as Mp

[wxID_PANELEA4, wxID_PANELEA4GRID1, wxID_PANELEA4GRID2, 
 wxID_PANELEA4PANELGRAPHUPH, wxID_PANELEA4PANELGRAPHHD,
 wxID_PANELEA4STATICTEXT1, wxID_PANELEA4STATICTEXT2,
 wxID_PANELEA4STATICTEXT3
] = [wx.NewId() for _init_ctrls in range(8)]
#
# constants
#

COLNO = 7
MAXROWS = 20

#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)

    self.subplot.plot(Status.int.GData['EA4b Plot'][0],
                      Status.int.GData['EA4b Plot'][1],
                      'go-', label='UPH', linewidth=2)
    self.subplot.plot(Status.int.GData['EA4b Plot'][0],
                      Status.int.GData['EA4b Plot'][2],
                      'bo-', label='UPH proc', linewidth=2)
    self.subplot.plot(Status.int.GData['EA4b Plot'][0],
                      Status.int.GData['EA4b Plot'][3],
                      'rs-',  label='USH', linewidth=2)

#    self.subplot.axis([0, 100, 0, 3e+7])
    self.subplot.legend()

#------------------------------------------------------------------------------
class PanelEA4b(wx.Panel):
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def __init__(self, parent):
#------------------------------------------------------------------------------

        self._init_ctrls(parent)
        keys = ['EA4b Table','EA4b Plot']
        self.mod = ModuleEA4(keys)
        self.mod.updatePanel()

#..............................................................................
# build xy-plot

        labels_column = 0
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : 'EA4b Plot',                # key for Interface
                   'title'       : _('Some title'),           # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : []}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelEA4bFig, wx.Panel, drawFigure, paramList)
        del dummy

#..............................................................................
# build table

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

        self.grid1.CreateGrid(MAXROWS, COLNO)

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
        self.grid1.SetColLabelValue(0, _("Temperature levels\n[�C]"))
        self.grid1.SetColLabelValue(1, _("[MWh]"))
        self.grid1.SetColLabelValue(2, _("[%]"))
        self.grid1.SetColLabelValue(3, _("cumulative\n[%]"))
        self.grid1.SetColLabelValue(4, _("[MWh]"))
        self.grid1.SetColLabelValue(5, _("[%]"))
        self.grid1.SetColLabelValue(6, _("cumulative\n[%]"))

#..............................................................................
# bring data to table

        try:
            data = Status.int.GData['EA4b Table']
            (rows,cols) = data.shape
        except:
            logDebug("PanelEA4b: received corrupt data in key: EA4b Table")
            (rows,cols) = (0,COLNO)

        print "PanelEA4b: data arriving"
        print data
        print rows,cols

        decimals = [-1,2,2,2,2,2,2]   #number of decimal digits for each colum
        for r in range(rows):
            if r == rows-1:
                self.grid1.SetRowAttr(r, attr2) #highlight totals row
            else:   
                self.grid1.SetRowAttr(r, attr)
                
            for c in range(cols):
                print r,c,data[r][c]
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

        self.staticText2.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.staticText3.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))

#------------------------------------------------------------------------------
    def _init_ctrls(self, prnt):
#------------------------------------------------------------------------------
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELEA4, name=u'PanelEA4b', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600))


        self.box1 = wx.StaticBox(self, -1, _(u'Heat demand (UPH) and supply (USH) by temperature'),
                                 pos = (10,10),size=(780,200))

        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.staticText2 = wx.StaticText(id=-1,
              label=_(u'Heat demand (UPH) by process temperature (PT)'),
              name='staticText2', parent=self, pos=wx.Point(200, 24),
              size=wx.Size(50, 17), style=0)

        self.staticText3 = wx.StaticText(id=-1,
              label=_(u'Heat supply (USH) by central supply temperature (CST)'),
              name='staticText3', parent=self, pos=wx.Point(470, 24),
              size=wx.Size(50, 17), style=0)

        self.grid1 = wx.grid.Grid(id=wxID_PANELEA4GRID1, name='grid1',#SD
              parent=self, pos=wx.Point(20, 40), size=wx.Size(760, 160),
              style=0)


        self.box2 = wx.StaticBox(self, -1, _(u'Distribution of heat demand (UPH) by process temperatures'),
                                 pos = (10,230),size=(780,320))

        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

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
        Status.main.tree.SelectItem(Status.main.qEA4c, select=True)
        print "Button exitModuleFwd: now I should show another window"

        

#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		

        try:
            self.panelEA4bFig.draw()
        except: pass
        self.Show()
