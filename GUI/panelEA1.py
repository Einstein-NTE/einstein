#Boa:Frame:PanelEA1
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	PanelEA1- GUI component for: Primary energy - Yearly data
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
#
#       Changes to previous version:
#       28/03/08:           included functions draw ... (before in module)
#       29/03/08:           mod. to use external graphics module
#       28/04/2008          changed method display to display graphics the first time
#       18/06/2008 SD: change to translatable text _(...)
#       30/06/2008 SD: change esthetics - 2tab2fig
#
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

from einstein.GUI.status import Status
# import the data processing module for this panel.
from einstein.modules.energyStats.moduleEA1 import *

# import the remapping module
import einstein.modules.matPanel as Mp
from numCtrl import *

[wxID_PANELEA1, wxID_PANELEA1GRID, wxID_PANELEA1PANELGRAPHFEC,
 wxID_PANELEA1PANELGRAPHFET, wxID_PANELEA1STATICTEXT1,
 wxID_PANELEA1STATICTEXT2, wxID_PANELEA1STATICTEXT3,
] = [wx.NewId() for _init_ctrls in range(7)]
#
# constants
#
GRID_LETTER_SIZE = 8               # points
GRID_LABEL_SIZE = 9                # points
GRID_LETTER_COLOR = '#000060'      # specified as hex #RRGGBB
GRID_BACKGROUND_COLOR = '#F0FFFF'  # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem

MAXROWS = 20


class PanelEA1(wx.Panel):

#------------------------------------------------------------------------------
    def __init__(self, parent=None):
#------------------------------------------------------------------------------
#   basic initialisation at build-up of the GUI
#------------------------------------------------------------------------------
        self._init_ctrls(parent)

        ##### start of graphics setup ####################################
        #
        # 0. the keys for data in this panel
        #    these are the keys for the data of this panel in
        #    the dictionary Interfaces.GData
        #    The data has been previously stored by moduleEA1
        #    keys must be a list, in case there's more than one dataset
        #    in the panel. In the present case there is only one, so
        #    it's a list of 1 element.
        #
        self.keys = ['EA1']
##        self.keys = ['EA1_FEC', 'EA1_FET']   #SD: to be added, modify moduleEA1, interfaces,...
        
        # 0.1 loads and initializes the respective data-processing module
        self.mod = ModuleEA1(self.keys)

##        # 0.2 where the labels are in the data matrix
##        
##        labels_column = 0 # 0-based column where the labels for this plot are 
##        
##        # remaps drawing methods to the wx widgets.
##        #
##        # 1. the last row (totals) has to be ignored for both the graphics in this panel
##        #    we have to find its row number (in this case it's simple: the last row)
##
##        (rows,cols) = Interfaces.GData[self.keys[0]].shape
##
##        # make a list of ignored rows. In the general case, these rows could be
##        # several and in different places
##
##        ignoredrows = []
##        ignoredrows.append(rows-1)
##        
##        # 0-based column where the data for this plot are 
##        data_column = 2
##
##        # title of the graph
##        title = _('FEC by fuel')
##
##        # background color of the graph
##        backcolor = GRAPH_BACKGROUND_COLOR
##
##        # size of the tick marks font
##        ticklabelfontsize = 8
##
##        #
##        # 2. sets the graphing method for panelGraphFEC
##        #
##        # 2.1 sets the parameters for this plot
##        #     the parameters are in a dictionary:
##        #
##        paramList={'labels'      : labels_column,     # labels column                    Default: 0
##                   'data'        : data_column,       # data column for this graph       No default
##                   'key'         : self.keys[0],      # key for Interface                No default
##                   'title'       : title,             # title of the graph.              Default: none
##                   'backcolor'   : backcolor,         # graph background color.          Default: white
##                   'tickfontsize': ticklabelfontsize, # tick label fontsize.             Default: 9
##                   'ignoredrows' : ignoredrows}       # rows that should not be plotted. Default: none
##
##        #
##        # 2.2 calls matPanel to do the rest
##        #
##        dummy = Mp.MatPanel(self.panelGraphFEC,   # widget that contains the graphic
##                            wx.Panel,             # class of the widget
##                            drawPiePlot,          # generic pie plotting routine
##                            paramList)

###################################################################

        labels_column = 0
        # remaps drawing methods to the wx widgets.
        #
        # upper graphic: FEC by fuel
        #
        (rows,cols) = Interfaces.GData[self.keys[0]].shape
        ignoredrows = [rows-1]
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 2,                      # data column for this graph
                   'key'         : self.keys[0],                # key for Interface
                   'title'       : _('FEC by fuel'),       # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelGraphFEC,
                            wx.Panel,
                            drawPiePlot,
                            paramList)

###################################################################



##        #
##        # 3. sets the graphing method for panelGraphFET
##        #
##        # 3.1 sets the parameters for this plot
##        #
##
##        paramList={'labels'      : 0,                 # labels column
##                   'data'        : 4,                 # data column for this graph
##                   'key'         : self.keys[0],      # key for Interface
##                   'title'       : _('FET by fuel'),     # title of the graph
##                   'backcolor'   : backcolor,         # graph background color
##                   'tickfontsize': ticklabelfontsize, # tick label fontsize
##                   'ignoredrows' : ignoredrows}       # rows that should not be plotted
##
##        #
##        # 3.2 calls matPanel to do the rest
##        #
##
##        dummy = Mp.MatPanel(self.panelGraphFET,
##                            wx.Panel,
##                            drawPiePlot,
##                            paramList)

########################################################################
        #
        # lower graphic: FET by fuel
        #
        # no rows to ignore here
        paramList={'labels'      : labels_column,              # labels column
                   'data'        : 4,                          # data column for this graph
                   'key'         : self.keys[0],                    # key for Interface
                   'title'       : _('FET by fuel'),# title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR}     # graph background color

        dummy = Mp.MatPanel(self.panelGraphFET,
                            wx.Panel,
                            drawPiePlot,
                            paramList)


########################################################################
        
##        ##### end of graphics setup ####################################
##        #
##        # additional widgets setup
##        #
##        # here, we modify some widgets attributes that cannot be changed
##        # directly by Boa. This cannot be done in _init_ctrls, since that
##        # method is rewritten by Boa each time.
##        #
##
##        # extract the data for presenting
##
###xxxHS here could be simplified. in principle only no. of columns has to be known     
##        data = Interfaces.GData[self.keys[0]]
##        (rows,cols) = data.shape
###        self.grid.CreateGrid(max(rows,20), cols)
##        self.grid.CreateGrid(MAXROWS, cols)
##
##        self.grid.EnableGridLines(True)
##        self.grid.SetDefaultRowSize(20)
##        self.grid.SetRowLabelSize(30)
##        self.grid.SetColSize(0,115)
##        self.grid.EnableEditing(False)
##        self.grid.SetLabelFont(wx.Font(GRID_LABEL_SIZE, wx.ROMAN, wx.ITALIC, wx.BOLD))
##        self.grid.SetColLabelValue(0, _("Fuel type"))
##        self.grid.SetColLabelValue(1, _("MWh"))
##        self.grid.SetColLabelValue(2, _("%"))
##        self.grid.SetColLabelValue(3, _("MWh"))
##        self.grid.SetColLabelValue(4, _("%"))
##
##        attr = wx.grid.GridCellAttr()
##        attr.SetTextColour(GRID_LETTER_COLOR)
##        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
##        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
##        #
##        # copy values from dictionary to grid
##        #
##        for r in range(rows):
##            self.grid.SetRowAttr(r, attr)
##            for c in range(cols):
###                self.grid.SetCellValue(r, c, data[r][c])
##                if c == labels_column:
##                    self.grid.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
##                else:
##                    self.grid.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);
##
##        self.grid.SetGridCursor(0, 0)
##
##        self.staticText1.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
##        self.staticText2.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
##        self.staticText3.SetFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))

####################################################################################
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
        key = self.keys[0]
        data = Interfaces.GData[key]

        
#####Security feature against non existing GData entry
##        COLNO1 = 3 #grid has usually a fixed column size, not necessary to read from GData
        COLNO1 = 5 #grid has usually a fixed column size, not necessary to read from GData        
        try: (rows,cols) = data.shape
        except: (rows,cols) = (0,COLNO1)
        
        self.grid.CreateGrid(max(rows,10), COLNO1)

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)

        self.grid.SetColSize(0,115)
        self.grid.SetColSize(1,91)#SD added
        self.grid.SetColSize(2,91)#SD added
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _("Fuel type"))
        self.grid.SetColLabelValue(1, _("MWh"))
        self.grid.SetColLabelValue(2, _("%"))
        self.grid.SetColLabelValue(3, _("MWh"))
        self.grid.SetColLabelValue(4, _("%"))
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

        decimals = [-1,0,1,0,1]   #number of decimal digits for each colum
        for r in range(rows):
            self.grid.SetRowAttr(r, attr)
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

        self.grid.SetGridCursor(0, 0)

####################################################################################

    def _init_ctrls(self, prnt):
##        # generated method, don't edit
##        wx.Panel.__init__(self, id=-1, name='', parent=prnt, pos=wx.Point(0,0),
##              size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE)
##
##        self.staticText1 = wx.StaticText(id=wxID_PANELEA1STATICTEXT1,
##              label=_(u'Total final energy consumption (FEC) and\n') + \
##                                         _(u'final energy consumption for thermal use (FET)'),
##              name='staticText1', parent=self, pos=wx.Point(130, 8),
##              size=wx.Size(500, 50), style=0)
##        self.staticText1.Center(wx.HORIZONTAL)
##
##        self.grid = wx.grid.Grid(id=wxID_PANELEA1GRID, name='grid', parent=self,
##              pos=wx.Point(130, 100), size=wx.Size(480, 172),
##              style=wx.VSCROLL | wx.THICK_FRAME)
##
##        self.panelGraphFEC = wx.Panel(id=wxID_PANELEA1PANELGRAPHFEC,
##              name=u'panelGraphFEC', parent=self, pos=wx.Point(72, 300),
##              size=wx.Size(280, 224), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
##        self.panelGraphFEC.SetBackgroundColour(wx.Colour(127, 127, 127))
##
##        self.panelGraphFET = wx.Panel(id=wxID_PANELEA1PANELGRAPHFET,
##              name=u'panelGraphFET', parent=self, pos=wx.Point(392, 300),
##              size=wx.Size(280, 224), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
##        self.panelGraphFET.SetBackgroundColour(wx.Colour(127, 127, 127))
##
##        self.staticText2 = wx.StaticText(id=wxID_PANELEA1STATICTEXT2,
##              label=_(u'Final energy\nconsumption (FEC)'), name='staticText3',
##              parent=self, pos=wx.Point(300, 70), size=wx.Size(219, 30),
##              style=0)
##        self.staticText2.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
##              False, u'Sans'))
##
##        self.staticText3 = wx.StaticText(id=wxID_PANELEA1STATICTEXT3,
##              label=_(u'Final energy for\nthermal use'), name='staticText4',
##              parent=self, pos=wx.Point(460, 70), size=wx.Size(191, 30),
##              style=0)
##        self.staticText3.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
##              False, u'Sans'))


        # generated method, don't edit
        wx.Panel.__init__(self, id=-1, name='', parent=prnt, pos=wx.Point(0,0),
              size=wx.Size(800, 600), style=wx.DEFAULT_FRAME_STYLE)

##        self.box1 = wx.StaticBox(self, -1, _(u'Useful process heat (UPH) demand by process'),
##                                 pos = (10,10),size=(780,240))
        self.box1 = wx.StaticBox(self, -1, _(u'Total final energy consumption (FEC) and\n final energy consumption for thermal use (FET)'),
                                 pos = (10,10),size=(780,240))
        
        
#######LAYOUT: here the position (pos) and size (size) of the grid is fixed.
#######        default PANEL size = 800 x 600 pixels. (0,0) is the left upper corner.

        self.grid = wx.grid.Grid(id=wxID_PANELEA1GRID, name='grid',parent=self,#SD grid1->grid
              pos=wx.Point(20, 40), size=wx.Size(760, 200),
              style=0)

#######LAYOUT: static text can be moved in a similar way
        self.box2 = wx.StaticBox(self, -1, _(u'FEC by fuel'),
                                 pos = (10,270),size=(380,280))

#######LAYOUT: here the position (pos) and size (size) of the figure-panels is fixed.
#######        default PANEL size = 800 x 600 pixels. (0,0) is the left upper corner.

        self.panelGraphFEC = wx.Panel(id=wxID_PANELEA1PANELGRAPHFEC,
              name=u'panelGraphFEC', parent=self, pos=wx.Point(20, 300),
              size=wx.Size(360, 240), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphFEC.SetBackgroundColour(wx.Colour(127, 127, 127))

#######LAYOUT: static text can be moved in a similar way
        self.box3 = wx.StaticBox(self, -1, _(u'FET by fuel'),
                                 pos = (410,270),size=(380,280))
        
#######LAYOUT: here the position (pos) and size (size) of the figure-panels is fixed.
#######        default PANEL size = 800 x 600 pixels. (0,0) is the left upper corner.

        self.panelGraphFET = wx.Panel(id=wxID_PANELEA1PANELGRAPHFET,
              name=u'panelGraphFET', parent=self, pos=wx.Point(420, 300),
              size=wx.Size(360, 240), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
        self.panelGraphFET.SetBackgroundColour(wx.Colour(127, 127, 127))

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

###------------------------------------------------------------------------------
##    def display(self):
###------------------------------------------------------------------------------
###   function executed on entering from tree (or from panelEnergy)
###------------------------------------------------------------------------------
##        self.mod.initPanel()
##        
##        data = Interfaces.GData[self.keys[0]]
##        (rows,cols) = data.shape
##        for r in range(rows):
##            for c in range(cols):
##                self.grid.SetCellValue(r, c, data[r][c])
##
###XXX Here better would be updating the grid and showing less rows ... ????
##        for r in range(rows,MAXROWS):
##            for c in range(cols):
##                self.grid.SetCellValue(r, c, "")
##
##        #TS20080428 to draw the graphics the first time
##        self.panelGraphFEC.draw()
##        self.panelGraphFET.draw()
##        self.Show()
       
#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   display function. carries out all the necessary calculations before
#   showing the panel
#------------------------------------------------------------------------------		

#####Security feature against any strange thing in graphs
        try: self.panelGraphFEC.draw()
        except: pass
        try: self.panelGraphFET.draw()
        except: pass
        self.Show()
