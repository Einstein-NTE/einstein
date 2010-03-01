#Boa:FramePanel:PanelBM2
# -*- coding: cp1252 -*-
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	Panel BM2
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#       Benchmark module, part 1: global energy intensity
#
#==============================================================================
#
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	    08/04/2008
#       Revised by:         Tom Sobota              28/04/2008
#                           Stoyan Danov            18/06/2008
#                           Hans Schweiger          25/06/2008
#                           Stoyan Danov            30/09/2008
#                           Stoyan Danov    13/10/2008
#                           
#
#       Changes to previous version:
#       28/04/2008: TS  created method display
#       18/06/2008: SD  change to translatable text _(...)
#       25/06/2008: HS  adaptation to changes in module
#       30/09/2008: SD  graphics figure added
#       13/10/2008: SD  change _() to _U()
#       15/02/2010 MW: fixed visualization
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
import wx.grid
from einstein.GUI.graphics import drawPiePlot
from einstein.GUI.status import Status
from numCtrl import *
from einstein.modules.messageLogger import *
from GUITools import *
import matplotlib.font_manager as font
from matplotlib.ticker import FuncFormatter

import einstein.modules.matPanel as Mp
from einstein.modules.interfaces import *


[wxID_PANELBM2, wxID_PANELBM2BUTTONPAGEBM2BACK, 
 wxID_PANELBM2BUTTONPAGEBM2CANCEL, wxID_PANELBM2BUTTONPAGEBM2FWD, 
 wxID_PANELBM2BUTTONPAGEBM2OK, wxID_PANELBM2COMBOSEARCHCRIT1, 
 wxID_PANELBM2FINDBENCHMARKS, wxID_PANELBM2GRIDPAGE, wxID_PANELBM2FIG, 
 wxID_PANELBM2SEARCHCRIT2, wxID_PANELBM2ST1, wxID_PANELBM2ST1PAGEBM2, 
 wxID_PANELBM2ST2, wxID_PANELBM2ST3PAGEBM2, wxID_PANELBM2STATICTEXT1, 
 wxID_PANELBM2STSEARCHCRIT1, wxID_PANELBM2STSEARCHCRIT2UNIT, 
 wxID_PANELBM2STSEARCHCRIT3, wxID_PANELBM2STTITLEPAGE, 
 wxID_PANELBM2TCSEARCHCRIT2A, wxID_PANELBM2TCSEARCHCRIT2B, 
 wxID_PANELBM2TCSEARCHCRIT3A, wxID_PANELBM2TCSEARCHCRIT3B, 
] = [wx.NewId() for _init_ctrls in range(23)]

# constants
#

axeslabel_fontsize = 10
axesticks_fontsize = 8
legend_fontsize = 10
spacing_left = 0.2
spacing_right = 0.9
spacing_bottom = 0.2
spacing_top = 0.85

COLNO = 6
MAXROWS = 20

def _U(text):
    return unicode(_(text),"utf-8")

#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		
    if hasattr(self, 'subplot'):
       del self.subplot
    self.subplot = self.figure.add_subplot(1,1,1)
    self.figure.subplots_adjust(left=spacing_left, right=spacing_right, bottom=spacing_bottom, top=spacing_top)

    gdata = Status.int.GData["BM2 Figure"]
    axis = gdata[0]
    bmtar_el = gdata[1]
    bmtar_fuel = gdata[2]
    bm_el = gdata[3]
    bm_fuel = gdata[4]
    ps_el = gdata[5]
    ps_fuel = gdata[6]

    NBenchmarks = len(bmtar_fuel)
    print "PanelBM2 (drawFigure): NBenchmarks = ",NBenchmarks

    print "bmtar_el",bmtar_el
    print "bmtar_fuel",bmtar_fuel
    print "bm_el",bm_el
    print "bm_fuel",bm_fuel
    
    for i in range(len(ps_el)):
        self.subplot.plot(ps_el[i],
                      ps_fuel[i],
                      'rs-', label='FEC[%s]'%(i), linewidth=2)

    for i in range(NBenchmarks):
        self.subplot.plot(bmtar_el[i],
                          bmtar_fuel[i],
                          'go',  label='target')
        self.subplot.plot(bm_el[i],
                          bm_fuel[i],
                          'g-', label='min/max', linewidth=1)
    self.subplot.axis(axis)

###SD-20080930
#    self.subplot.legend()
    major_formatter = FuncFormatter(format_int_wrapper)
    self.subplot.axes.xaxis.set_major_formatter(major_formatter)
    self.subplot.axes.yaxis.set_major_formatter(major_formatter)
    fp = font.FontProperties(size = axeslabel_fontsize)
    self.subplot.axes.set_ylabel(_U('SEC - fuels [kWh/%s]')%"p.u.", fontproperties=fp)
    self.subplot.axes.set_xlabel(_U('SEC - electricity [kWh/%s]')%"p.u.", fontproperties=fp)
    
    for label in self.subplot.axes.get_yticklabels():
#        label.set_color(self.params['ytickscolor'])
        label.set_fontsize(axesticks_fontsize)
#        label.set_rotation(self.params['yticksangle'])
    #
    # properties of labels on the x axis
    #
    for label in self.subplot.axes.get_xticklabels():
#        label.set_color(self.params['xtickscolor'])
        label.set_fontsize(axesticks_fontsize)
#        label.set_rotation(self.params['xticksangle'])

    self.subplot.legend(loc = 'best')
    try:
        lg = self.subplot.get_legend()
        ltext  = lg.get_texts()             # all the text.Text instance in the legend
        for txt in ltext:
            txt.set_fontsize(legend_fontsize)  # the legend text fontsize
        # legend line thickness
        llines = lg.get_lines()             # all the lines.Line2D instance in the legend
        for lli in llines:
            lli.set_linewidth(1.5)          # the legend linewidth
        # color of the legend frame
        # this only works when the frame is painted (see below draw_frame)
        frame  = lg.get_frame()             # the patch.Rectangle instance surrounding the legend
        frame.set_facecolor('#F0F0F0')      # set the frame face color to light gray
        # should the legend frame be painted
        lg.draw_frame(False)
    except:
        # no legend
        pass

#XXXXXX To be checked how to bring x/y- labels to this plot ...
#    self.figure.xlabel('time (s)')
#    self.figure.ylabel('current (nA)')
#    self.figure.title('Gaussian colored noise')

#    self.subplot.legend()


#============================================================================== 
class PanelBM2(wx.Panel):
#============================================================================== 

#------------------------------------------------------------------------------		
    def __init__(self, parent):
#------------------------------------------------------------------------------		
        self.main = parent

	keys = ['BM2']
        self.mod = Status.mod.moduleBM

        print "PanelBM: calling initPanel"
        self.mod.initPanel(keys)
        
        print "PanelBM: calling init_ctrls"
        try: print "PanelBM - GData",Status.int.GData[keys[0]]
        except: pass

        self.naceSearch = Status.int.GData["BM Info"][0]
        self.naceSelector = Status.int.GData["BM Info"][1]
        print "PanelBM: ",self.naceSelector

        self.turnover0 = Status.int.GData["BM Info"][2]
        self.turnover1 = Status.int.GData["BM Info"][3]
        self.year0 = Status.int.GData["BM Info"][4]
        self.year1 = Status.int.GData["BM Info"][5]
        self.products = Status.int.GData["BM Info"][6]
        self.selector = Status.int.GData["BM Info"][9]
        
        self._init_ctrls(parent)
        
#==============================================================================
#   graphic: Cumulative heat demand by hours
#==============================================================================
        labels_column = 0
        ignoredrows = []
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : 'Some title',           # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelFig,
                            wx.Panel,
                            drawFigure,
                            paramList)

        #
        # additional widgets setup
        # here, we modify some widgets attributes that cannot be changed
        # directly by Boa. This cannot be done in _init_ctrls, since that
        # method is rewritten by Boa each time.
        #
        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.gridPage.CreateGrid(MAXROWS, COLNO)

        self.gridPage.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.gridPage.EnableGridLines(True)
        self.gridPage.SetDefaultRowSize(30)
        self.gridPage.SetDefaultColSize(88)
        self.gridPage.SetRowLabelSize(30)
        self.gridPage.SetColSize(0,180)
        self.gridPage.SetColSize(1,180)
        self.gridPage.SetColSize(2,80)
        self.gridPage.EnableEditing(False)
        self.gridPage.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.gridPage.SetColLabelValue(0, _U("Source"))
        self.gridPage.SetColLabelValue(1, _U("Reference"))
        self.gridPage.SetColLabelValue(2, _U("Validity"))
        self.gridPage.SetColLabelValue(3, _U("Primary energy"))
        self.gridPage.SetColLabelValue(4, _U("Fuels"))
        self.gridPage.SetColLabelValue(5, _U("Electricity"))
             #
        # copy values from dictionary to grid
        #
        for r in range(MAXROWS):
            self.gridPage.SetRowAttr(r, attr)
            for c in range(COLNO):
                if c <= labels_column:
                    self.gridPage.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.gridPage.SetCellAlignment(r, c, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);

        self.gridPage.SetGridCursor(0, 0)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELBM2, name='PanelBM2', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(808, 600), style=0)
        self.SetClientSize(wx.Size(800, 600))

#..............................................................................
# box 1: grid display

        self.box1 = wx.StaticBox(self, -1, _U('Benchmark (2): specific energy consumption (SEC) by product'),
                                 pos = (10,10),size=(780,260))
        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))


        self.stProduct = wx.StaticText(id=-1,
              label=_U('Product:'), name='stProduct', parent=self, pos=wx.Point(10,
              280), size=wx.Size(80, 24), style=0)

        self.comboProduct = wx.ComboBox(choices=self.products,
              id=-1, name='comboProduct', parent=self,
              pos=wx.Point(100, 280), size=wx.Size(300, 24), style=0)
#        self.comboProduct.SetSelection(0)
        self.comboProduct.Bind(wx.EVT_COMBOBOX, self.OnComboProductChoice,id=-1)

        self.gridPage = wx.grid.Grid(id=wxID_PANELBM2GRIDPAGE,
              name='gridpageBM2', parent=self, pos=wx.Point(20, 40),
              size=wx.Size(760, 220), style=0)
        self.gridPage.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageGridCellLeftDclick, id=wxID_PANELBM2GRIDPAGE)
        self.gridPage.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageGridCellRightClick, id=wxID_PANELBM2GRIDPAGE)

        self.FindBenchmarks = wx.Button(id=wxID_PANELBM2FINDBENCHMARKS,
              label=_U('find benchmarks'), name='FindBenchmarks', parent=self,
              pos=wx.Point(592, 280), size=wx.Size(184, 24), style=0)
        self.FindBenchmarks.Bind(wx.EVT_BUTTON, self.OnFindBenchmarksButton,
              id=wxID_PANELBM2FINDBENCHMARKS)

#..............................................................................
# box 2: copmarison benchmarks

        self.box2 = wx.StaticBox(self, -1, _U('Comparison benchmark data'),
                                 pos = (10,310),size=(400,260))

        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelFig = wx.Panel(id=wxID_PANELBM2FIG, name='panelAFigure',
              parent=self, pos=wx.Point(22, 340), size=wx.Size(380, 220),
              style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)

#..............................................................................
# box 3: search criteria

        self.box3 = wx.StaticBox(self, -1, _U('Search criteria'),
                                 pos = (430,310),size=(360,220))
        self.box3.SetForegroundColour(TITLE_COLOR)
        self.box3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.stSearchCrit1 = wx.StaticText(id=wxID_PANELBM2STSEARCHCRIT1,
              label=_U('NACE Code range (digits)'), name='stSearchCrit1',
              parent=self, pos=wx.Point(448, 352), size=wx.Size(123, 13),
              style=0)

        self.comboSearchCrit1 = wx.ComboBox(choices=self.naceSelector, id=wxID_PANELBM2COMBOSEARCHCRIT1,
              name='comboSearchCrit1', parent=self, pos=wx.Point(640, 344),
              size=wx.Size(136, 21), style=0)
        self.comboSearchCrit1.SetSelection(self.naceSearch)

        self.st1 = wx.StaticText(id=wxID_PANELBM2ST1, label=_U('max.'), name='st1',
              parent=self, pos=wx.Point(728, 384), size=wx.Size(25, 13),
              style=0)

        self.st2 = wx.StaticText(id=wxID_PANELBM2ST2, label=_U('min.'), name='st2',
              parent=self, pos=wx.Point(664, 384), size=wx.Size(21, 13),
              style=0)

        self.SearchCrit2 = wx.StaticText(id=wxID_PANELBM2SEARCHCRIT2,
              label=_U('Production volume'), name='SearchCrit2', parent=self,
              pos=wx.Point(448, 416), size=wx.Size(120, 13), style=0)

        self.stSearchCrit2Unit = wx.StaticText(id=wxID_PANELBM2STSEARCHCRIT2UNIT,
              label=_U('[t/a]'), name='stSearchCrit2Unit', parent=self,
              pos=wx.Point(592, 416), size=wx.Size(22, 13), style=0)

        self.stSearchCrit3 = wx.StaticText(id=wxID_PANELBM2STSEARCHCRIT3,
              label=_U('Year of data'), name='stSearchCrit3', parent=self,
              pos=wx.Point(448, 440), size=wx.Size(61, 13), style=0)

        self.tcSearchCrit2b = wx.TextCtrl(id=wxID_PANELBM2TCSEARCHCRIT2B,
              name='tcSearchCrit2b', parent=self, pos=wx.Point(712, 408),
              size=wx.Size(64, 24), style=0, value=str(self.turnover1))

        self.tcSearchCrit2a = wx.TextCtrl(id=wxID_PANELBM2TCSEARCHCRIT2A,
              name='tcSearchCrit2a', parent=self, pos=wx.Point(640, 408),
              size=wx.Size(64, 24), style=0, value=str(self.turnover0))

        self.stSearchCrit3 = wx.StaticText(id=wxID_PANELBM2STSEARCHCRIT3,
              label=_U('Year of data'), name='stSearchCrit3', parent=self,
              pos=wx.Point(448, 440), size=wx.Size(61, 13), style=0)

        self.tcSearchCrit3a = wx.TextCtrl(id=wxID_PANELBM2TCSEARCHCRIT3A,
              name='tcSearchCrit3a', parent=self, pos=wx.Point(640, 440),
              size=wx.Size(64, 24), style=0, value=str(self.year0))

        self.tcSearchCrit3b = wx.TextCtrl(id=wxID_PANELBM2TCSEARCHCRIT3B,
              name='tcSearchCrit3b', parent=self, pos=wx.Point(712, 440),
              size=wx.Size(64, 24), style=0, value=str(self.year1))

#..............................................................................
# default action buttons

        self.buttonpageBM2Ok = wx.Button(id=wx.ID_OK, label=_U('OK'),
              name='buttonpageBM2Ok', parent=self, pos=wx.Point(528, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageBM2Ok.Bind(wx.EVT_BUTTON, self.OnButtonpageBM2OkButton,
              id=wx.ID_OK)

        self.buttonpageBM2Cancel = wx.Button(id=wx.ID_CANCEL, label=_U('Cancel'),
              name='buttonpageBM2Cancel', parent=self, pos=wx.Point(616, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageBM2Cancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpageBM2CancelButton, id=wx.ID_CANCEL)

        self.buttonpageBM2Fwd = wx.Button(id=wxID_PANELBM2BUTTONPAGEBM2FWD,
              label='>>>', name='buttonpageBM2Fwd', parent=self,
              pos=wx.Point(704, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageBM2Fwd.Bind(wx.EVT_BUTTON, self.OnButtonpageBM2FwdButton,
              id=wxID_PANELBM2BUTTONPAGEBM2FWD)

        self.buttonpageBM2Back = wx.Button(id=wxID_PANELBM2BUTTONPAGEBM2BACK,
              label='<<<', name='buttonpageBM2Back', parent=self,
              pos=wx.Point(440, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageBM2Back.Bind(wx.EVT_BUTTON,
              self.OnButtonpageBM2BackButton,
              id=wxID_PANELBM2BUTTONPAGEBM2BACK)

#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		

        self.mod.updatePanel()
#..............................................................................		
#   create data table

        data = Status.int.GData["BM2"]
        try: (rows,cols) = data.shape
        except:
            rows = 0

        for r in range(rows):
            for c in range(3):
                try: self.gridPage.SetCellValue(r, c, data[r][c])
                except:
                    print "PanelBM (display): problems with data[%s][%s]: %s"%(r,c,data[r][c])

            try:
                self.gridPage.SetCellValue(r,3,self.displayBM(data[r][3:6]))
            except:
                print "PanelBM (display): problems with BMel: %s)"%self.displayBM(data[r][3:6])
            try:
                self.gridPage.SetCellValue(r,4,self.displayBM(data[r][6:9]))
            except:
                print "PanelBM (display): problems with BMel: %s)"%self.displayBM(data[r][6:9])
            try:
                self.gridPage.SetCellValue(r,5,self.displayBM(data[r][9:12]))
            except:
                print "PanelBM (display): problems with BMel: %s)"%self.displayBM(data[r][9:12])

        for r in range(rows,MAXROWS):
            for c in range(COLNO):
                self.gridPage.SetCellValue(r, c, "")
            
#..............................................................................		
#   create graphic representation

        self.Hide()
        print "PanelBM2 (display): updating panel figure"
        self.panelFig.draw()

        self.Show()
        
#------------------------------------------------------------------------------		
    def OnFindBenchmarksButton(self, event):
#------------------------------------------------------------------------------		
        naceSearch = self.comboSearchCrit1.GetSelection()

        turnover0 = float(self.tcSearchCrit2a.GetValue())
        turnover1 = float(self.tcSearchCrit2b.GetValue())

        if turnover0 < 0 or turnover1 > 1.0e+6 or turnover0 > turnover1:
            showWarning(_U("revise your search criteria: turnover in between %s and %s M€")%(turnover0,turnover1))
            print (turnover0<=0.0),(turnover1 > 1.0e+6),(turnover0 > turnover1)
            return

        year0 = int(self.tcSearchCrit3a.GetValue())
        year1 = int(self.tcSearchCrit3b.GetValue())

        if (year0 < 1980 or year1 > 2050 or year0 > year1) and year0 > 0:
            showWarning(_U("revise your search criteria: year of data in between %s and %s")%(year0,year1))
            return

        product = self.comboProduct.GetValue()
        selector = self.comboProduct.GetSelection()
        
        searchCriteria = [naceSearch,None,turnover0,turnover1,year0,year1,product,None,None,selector]
        Status.int.setGraphicsData("BM Info",searchCriteria)
        
        self.mod.updateSearch()
        
        self.display()
    
#------------------------------------------------------------------------------		
    def OnComboProductChoice(self, event):
#------------------------------------------------------------------------------		
        print "PanelBM2: ComboBox event handler active !!!"
        self.OnFindBenchmarksButton(event)

#------------------------------------------------------------------------------		
    def OnGridPageGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
        pass

#------------------------------------------------------------------------------		
    def OnGridPageGridCellRightClick(self, event):
#------------------------------------------------------------------------------		
        pass
        
#------------------------------------------------------------------------------		
#   Event handlers default panel buttons: <<< OK Cancel >>>
#------------------------------------------------------------------------------		

    def OnButtonpageBM2OkButton(self, event):
        saveOption = "save"
#        self.mod.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleOK: now I should go back to HC"

    def OnButtonpageBM2CancelButton(self, event):
        #warning: do you want to leave w/o saving ???
        saveOption = "save"
#        self.mod.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleCancel: now I should go back to HC"

    def OnButtonpageBM2BackButton(self, event):
        #pop-up: to save or not to save ...
        saveOption = "save"
#        self.modA.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleBack: now I should show another window"

    def OnButtonpageBM2FwdButton(self, event):
        #pop-up: to save or not to save ...
        saveOption = "save"
#        self.mod.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleFwd: now I should show another window"

#------------------------------------------------------------------------------		
#   Auxiliary functions
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
    def displayBM(self, bm):
#------------------------------------------------------------------------------		
#       displays a benchmark given as a list bm:
#       0: target 1: minimum 2: maximum
#
#       in the format
#
#       99.99 (55.55 - 101.00)
#------------------------------------------------------------------------------		

        try: bm_tar = convertDoubleToString(float(bm[0]))
        except: bm_tar = "---"
        try: bm_min = convertDoubleToString(float(bm[1]))
        except: bm_min = "---"
        try: bm_max = convertDoubleToString(float(bm[2]))
        except: bm_max = "---"
        
        try: displayString = str(bm_tar + "\n(" + bm_min + " - " + bm_max + ")")
        except:
            print "PanelBM (displayBM): problems with data tar/min/max",bm_tar,bm_min,bm_max
            displayString = ""
        return displayString

