#Boa:FramePanel:PanelHR
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
#	Panel Heat Recovery module
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Panel for HR design assistant
#
#==============================================================================
#
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	    10/06/2008
#	Last revised by:
#                       Stoyan Danov        18/06/2008
#                       Florian Joebstl     02/09/2008
#                       Hans Schweiger      06/07/2009
#                           
#
#   Changes to previous version:
#   
#   18/06/2008 SD: change to translatable text _(...)
#   02/09/2008 FJ: redone the entire GUI (grid,plot,controls...)
#   06/07/2009 HS: adaptations to UTF and number of decimals in grid
#   15/02/2010 MW: fixed visualization
#       
#------------------------------------------------------------------------------		
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008,2009
#	www.energyxperts.net / info@energyxperts.net
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#============================================================================== 

import wx
import wx.grid

from GUITools import *
from numCtrl import *
#from einstein.modules.plotPanel import PlotPanel
import einstein.modules.matPanel as Mp
from pylab import *
from matplotlib.ticker import MaxNLocator
from einstein.GUI.dialog_changeHX import *
from einstein.modules.modules import Modules
from einstein.GUI.status import Status
from einstein.modules.interfaces import *
from einstein.modules.messageLogger import *

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

[wxID_PANELHR, wxID_PANELHRBTNCALCULATE, wxID_PANELHRBTNCHANGEHX, 
 wxID_PANELHRBTNDELETEHX, wxID_PANELHRBTNSHOWSTDVALUES, 
 wxID_PANELHRBUTTONPAGEHRBACK, wxID_PANELHRBUTTONPAGEHRCANCEL, 
 wxID_PANELHRBUTTONPAGEHRFWD, wxID_PANELHRBUTTONPAGEHROK, 
 wxID_PANELHRCBCONSIDERCOND, wxID_PANELHRCBCURVEDISPLAY, wxID_PANELHRCBEXHX, 
 wxID_PANELHRGRID, wxID_PANELHRPANEL_DRAWCURVE, wxID_PANELHRRBCALC, 
 wxID_PANELHRRBREDESIGN, wxID_PANELHRSTATICBOX1, wxID_PANELHRSTATICBOX2, 
 wxID_PANELHRSTATICBOX3, wxID_PANELHRSTATICBOX4, wxID_PANELHRSTATICTEXT1, 
 wxID_PANELHRSTATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(22)]

# constants
#
#GRID_LETTER_SIZE = 8 #points
#GRID_LABEL_SIZE = 9  # points
#GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGHR
#GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
#GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem

MAXROWS = 50
COLNO = 12

spacing_left = 0.1
spacing_right = 0.95
spacing_bottom = 0.15
spacing_top = 0.9
spacing_w = 0.4

#from matplotlib.ticker import MaxNLocator

def drawFigure(self):
    try:
        if not hasattr( self, 'subplot' ):
            self.subplot = self.figure.add_subplot( 121 )
        if not hasattr(self, 'subplot2'):
            self.subplot2 = self.figure.add_subplot(122)
        self.figure.subplots_adjust(left=spacing_left, right=spacing_right, bottom=spacing_bottom, top=spacing_top, wspace=spacing_w)

        if not hasattr(Status.int, 'hrdata'):
            return
        data = Status.int.hrdata.curves            
        if (len(data)==0):
            return

        self.subplot = self.figure.add_subplot(121)
        curve = data[0]
        self.subplot.plot(curve.X,curve.Y,'b',label =curve.Name)            
        self.subplot.legend(loc = 0)
        self.subplot.set_title(curve.Name)
        self.subplot.set_xlabel(_U('Power [kW]'))
        self.subplot.set_ylabel(_U('Temperature [C]'))

        mmx = [ max(curve.X), min(curve.X) ]
        mmy = [ max(curve.Y), min(curve.Y) ]
                                      
        curve = data[1]
        self.subplot.plot(curve.X,curve.Y,'r',label =curve.Name)          
        self.subplot.legend(loc = 0)
        self.subplot.set_title(curve.Name)          
        
        mmx.append(max(curve.X))
        mmx.append(min(curve.X))
        mmy.append(max(curve.Y))
        mmy.append(min(curve.Y))            
        
        m = (max(mmy) - min(mmy))*0.2
        m2 = (max(mmx) - min(mmx))*0.2
        
        self.subplot.axis([min(mmx),max(mmx)+m2,min(mmy),max(mmy)+m])
                            
        curve = data[2]
        self.subplot2.plot(curve.X,curve.Y,'g',label =curve.Name)
        
        m = (max(curve.Y) - min(curve.Y))*0.2
        m2 = (max(curve.X) - min(curve.X))*0.2
        
        self.subplot2.axis([min(curve.X),max(curve.X)+m2,min(curve.Y),max(curve.Y)+m])
        self.subplot2.legend(loc = 0)
        self.subplot2.set_title(curve.Name)
        self.subplot2.set_xlabel(_U('Power [kW]'))
        self.subplot2.set_ylabel(_U('Temperature [C]'))

        #change axis
        self.subplot.xaxis.set_major_locator(MaxNLocator(4))
        self.subplot2.xaxis.set_major_locator(MaxNLocator(4))
    except:
        pass


def drawFigure2( self ):
    """Draw data."""
    if not hasattr( self, 'subplot' ):
        self.subplot = self.figure.add_subplot( 121 )
    if not hasattr(self, 'subplot2'):
        self.subplot2 = self.figure.add_subplot(122)
    self.figure.subplots_adjust(left=spacing_left, right=spacing_right, bottom=spacing_bottom, top=spacing_top, wspace=spacing_w)
   
    if not hasattr(Status.int, 'hrdata'):
        return
    
    if not hasattr(Status.int.hrdata, 'QD_T'):
        return        
    data = Status.int.hrdata.QD_T             
    if (len(data)==0):
        return    
                 
    min_ = 100000
    max_ = 0
    
    X = xrange(0, 406, 5)      
    Y = data[:]   
    for i in range(0,len(Y)): #scale to MWh
        Y[i]=Y[i]/1000.0
         
    self.subplot = self.figure.add_subplot(121)
    self.subplot.plot(X,Y,'b',label ="QD_T")    
    self.subplot.legend(loc = 0)                             
    self.subplot.axis([min(X),max(X),min(Y),max(Y)*1.1])   
    self.subplot.set_ylabel(_U('Energy [MWh]'))
    self.subplot.set_xlabel(_U('Temperature [C]'))
    
    if not hasattr(Status.int.hrdata, 'QA_T'):
        return    
    data = Status.int.hrdata.QA_T              
    min_ = 100000
    max_ = 0
                    
    X = xrange(0, 406, 5)      
    Y = data[:] 
    for i in range(0,len(Y)): #scale to MWh
        Y[i]=Y[i]/1000.0                    

    self.subplot2.plot(X,Y,'r',label ="QA_T")    
    self.subplot2.legend(loc = 0)                             
    self.subplot2.axis([min(X),max(X),min(Y),max(Y)*1.1])   
    self.subplot2.set_ylabel(_U('Energy [MWh]'))
    self.subplot2.set_xlabel(_U('Temperature [C]'))  


class HRPlotPanelHCG (wx.Panel):
    """Plots several lines in distinct colors."""
    def __init__( self, parent, **kwargs ):
        self.parent = parent
        # initiate plotter
        wx.Panel.__init__(self, id=wx.ID_ANY, name='Panel', parent=parent,
                          pos=wx.Point(0, 0), size=parent.GetSize(), style=0)


class HRPlotPanelYED (wx.Panel):
    """Plots several lines in distinct colors."""
    def __init__( self, parent, **kwargs ):
        self.parent = parent
        # initiate plotter
        wx.Panel.__init__(self, id=wx.ID_ANY, name='Panel', parent=parent,
                          pos=wx.Point(0, 0), size=parent.GetSize(), style=0)
        #Status.HRTool = "estimate"


class PanelHR(wx.Panel):

    def __init__(self, parent, main, id, pos, size, style, name):
        self.main = main
        self.keys = ['HR Table','HR Curves']
        self.mod = Status.mod.moduleHR
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELHR, name='PanelHR', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(808, 627), style=0)
        self.SetClientSize(wx.Size(800, 600))

        self.grid = wx.grid.Grid(id=wxID_PANELHRGRID, name='gridpageHR',
              parent=self, pos=wx.Point(32, 360), size=wx.Size(720, 160),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridGridCellLeftDclick, id=wxID_PANELHRGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGridGridCellLeftClick, id=wxID_PANELHRGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridGridCellRightClick, id=wxID_PANELHRGRID)

        self.panel_drawcurve = wx.Panel(id=wxID_PANELHRPANEL_DRAWCURVE,
              name='panel_drawcurve', parent=self, pos=wx.Point(32, 32),
              size=wx.Size(576, 280), style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)

        self.buttonpageHROk = wx.Button(id=wxID_PANELHRBUTTONPAGEHROK,
              label=_U('ok'), name='buttonpageHROk', parent=self,
              pos=wx.Point(520, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageHROk.Bind(wx.EVT_BUTTON, self.OnButtonpageHROkButton,
              id=wxID_PANELHRBUTTONPAGEHROK)

        self.buttonpageHRCancel = wx.Button(id=wxID_PANELHRBUTTONPAGEHRCANCEL,
              label=_U('cancel'), name='buttonpageHRCancel', parent=self,
              pos=wx.Point(608, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageHRCancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpageHRCancelButton,
              id=wxID_PANELHRBUTTONPAGEHRCANCEL)

        self.buttonpageHRFwd = wx.Button(id=wxID_PANELHRBUTTONPAGEHRFWD,
              label='>>>', name='buttonpageHRFwd', parent=self,
              pos=wx.Point(696, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageHRFwd.Bind(wx.EVT_BUTTON, self.OnButtonpageHRFwdButton,
              id=wxID_PANELHRBUTTONPAGEHRFWD)

        self.buttonpageHRBack = wx.Button(id=wxID_PANELHRBUTTONPAGEHRBACK,
              label='<<<', name='buttonpageHRBack', parent=self,
              pos=wx.Point(432, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageHRBack.Bind(wx.EVT_BUTTON, self.OnButtonpageHRBackButton,
              id=wxID_PANELHRBUTTONPAGEHRBACK)

        self.btnCalculate = wx.Button(id=wxID_PANELHRBTNCALCULATE,
              label=_U('calculate'), name='btnCalculate', parent=self,
              pos=wx.Point(648, 32), size=wx.Size(104, 24), style=0)
        self.btnCalculate.Bind(wx.EVT_BUTTON, self.OnBtnCalculateButton,
              id=wxID_PANELHRBTNCALCULATE)

        self.cbCurveDisplay = wx.Choice(choices=['HCC/CCC/GCC', 'YED'],
              id=wxID_PANELHRCBCURVEDISPLAY, name='cbCurveDisplay', parent=self,
              pos=wx.Point(640, 248), size=wx.Size(120, 21),
              style=wx.FULL_REPAINT_ON_RESIZE)
        self.cbCurveDisplay.SetSelection(0)
        self.cbCurveDisplay.Bind(wx.EVT_CHOICE, self.OnCbCurveDisplayChoice,
              id=wxID_PANELHRCBCURVEDISPLAY)

        self.cbExHX = wx.CheckBox(id=wxID_PANELHRCBEXHX,
              label=_U('Consider existing'), name='cbExHX', parent=self,
              pos=wx.Point(648, 112), size=wx.Size(112, 16), style=0)
        self.cbExHX.SetValue(False)
        self.cbExHX.Bind(wx.EVT_CHECKBOX, self.OnCbExHXCheckbox,
              id=wxID_PANELHRCBEXHX)

        self.btnDeleteHX = wx.Button(id=wxID_PANELHRBTNDELETEHX,
              label=_U('Hide HX'), name='btnDeleteHX', parent=self,
              pos=wx.Point(16, 544), size=wx.Size(75, 23), style=0)
        self.btnDeleteHX.Bind(wx.EVT_BUTTON, self.OnBtnDeleteHXButton,
              id=wxID_PANELHRBTNDELETEHX)

        self.btnChangeHX = wx.Button(id=wxID_PANELHRBTNCHANGEHX,
              label=_U('Change HX'), name='btnChangeHX', parent=self,
              pos=wx.Point(104, 544), size=wx.Size(75, 23), style=0)
        self.btnChangeHX.Bind(wx.EVT_BUTTON, self.OnBtnChangeHXButton,
              id=wxID_PANELHRBTNCHANGEHX)

        self.staticBox1 = wx.StaticBox(id=wxID_PANELHRSTATICBOX1,
              label=_U('HX Network'), name='staticBox1', parent=self,
              pos=wx.Point(632, 8), size=wx.Size(136, 208), style=0)

        self.btnShowStdValues = wx.Button(id=wxID_PANELHRBTNSHOWSTDVALUES,
              label=_U('Standard values for HX'), name='btnShowStdValues',
              parent=self, pos=wx.Point(192, 544), size=wx.Size(128, 23),
              style=0)
        self.btnShowStdValues.Bind(wx.EVT_BUTTON, self.OnBtnShowStdValuesButton,
              id=wxID_PANELHRBTNSHOWSTDVALUES)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELHRSTATICBOX2,
              label=_U('Display Options'), name='staticBox2', parent=self,
              pos=wx.Point(632, 224), size=wx.Size(136, 56), style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELHRSTATICTEXT2,
              label=_U('HXs in network \ncalculation'), name='staticText2',
              parent=self, pos=wx.Point(667, 128), size=wx.Size(74, 26),
              style=0)

        self.staticBox3 = wx.StaticBox(id=wxID_PANELHRSTATICBOX3,
              label=_U('Performance Curves'), name='staticBox3', parent=self,
              pos=wx.Point(16, 8), size=wx.Size(608, 320), style=0)

        self.staticBox4 = wx.StaticBox(id=wxID_PANELHRSTATICBOX4,
              label=_U('Existing heat exchangers in the system'),
              name='staticBox4', parent=self, pos=wx.Point(16, 336),
              size=wx.Size(752, 192), style=0)

        self.rbCalc = wx.RadioButton(id=wxID_PANELHRRBCALC,
              label=_U('Calculate only'), name='rbCalc', parent=self,
              pos=wx.Point(648, 64), size=wx.Size(96, 13), style=0)
        self.rbCalc.SetValue(True)
        self.rbCalc.Bind(wx.EVT_RADIOBUTTON, self.OnRbCalcRadiobutton,
              id=wxID_PANELHRRBCALC)

        self.rbRedesign = wx.RadioButton(id=wxID_PANELHRRBREDESIGN,
              label=_U('Redesign network'), name='rbRedesign', parent=self,
              pos=wx.Point(648, 88), size=wx.Size(104, 13), style=0)
        self.rbRedesign.Bind(wx.EVT_RADIOBUTTON, self.OnRbRedesignRadiobutton,
              id=wxID_PANELHRRBREDESIGN)

        self.cbConsiderCond = wx.CheckBox(id=wxID_PANELHRCBCONSIDERCOND,
              label=_U('Consider conden-'), name='cbConsiderCond', parent=self,
              pos=wx.Point(648, 160), size=wx.Size(112, 24), style=0)
        self.cbConsiderCond.SetValue(False)
        self.cbConsiderCond.Bind(wx.EVT_CHECKBOX, self.OnCbConsiderCondCheckbox,
              id=wxID_PANELHRCBCONSIDERCOND)

        self.staticText1 = wx.StaticText(id=wxID_PANELHRSTATICTEXT1,
              label='sation heat in off \ngas of boilers?', name='staticText1',
              parent=self, pos=wx.Point(667, 179), size=wx.Size(88, 26),
              style=0)

    def __init_custom_ctrls(self, prnt):
        self.staticBox1.SetForegroundColour(TITLE_COLOR)
        self.staticBox1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.staticBox2.SetForegroundColour(TITLE_COLOR)
        self.staticBox2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.staticBox3.SetForegroundColour(TITLE_COLOR)
        self.staticBox3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.staticBox4.SetForegroundColour(TITLE_COLOR)
        self.staticBox4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))                
        #----Grid-------------------------------------------------------------------------
        self.selectedRow = 0
        labels_column = 0
        
        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid.CreateGrid(MAXROWS, COLNO)

        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(90)
        self.grid.SetColSize(1,60)
        #self.grid.SetColSize(3,160)
        
        self.enableButtons(False)

        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Name"))
        self.grid.SetColLabelValue(1, _U("Power\n[kW]"))
        self.grid.SetColLabelValue(2, _U("Size storage tank\n[m³]"))
        self.grid.SetColLabelValue(3, _U("Hot Medium"))
        self.grid.SetColLabelValue(4, _U("T1 hot med.\n[°C]"))
        self.grid.SetColLabelValue(5, _U("T2 hot med.\n[°C]"))
        self.grid.SetColLabelValue(6, _U("Cold medium"))
        self.grid.SetColLabelValue(7, _U("T3 cold med.\n[°C]"))
        self.grid.SetColLabelValue(8, _U("T4 cold med.\n[°C]"))
        self.grid.SetColLabelValue(9, _U("surface area\n[m²]"))
        self.grid.SetColLabelValue(10, _U("inv. cost\n[EUR]"))
        self.grid.SetColLabelValue(11, _U("oper. cost\n[EUR]"))
        #
        # copy values from dictionary to grid
        #
        for r in range(MAXROWS):
            self.grid.SetRowAttr(r, attr)

        self.grid.SetGridCursor(0, 0)         
        self.plotpanel = HRPlotPanelHCG(self.panel_drawcurve)
        #----------------------------------------------------------------
        self.rbRedesign.SetValue(True)
        self.mod.redesign = True
        
        self.Show()  
        
       

    def display(self):
#------------------------------------------------------------------------------		
#   function activated on each entry into the panel from the tree
#------------------------------------------------------------------------------		
        self.mod.initPanel()        # prepares data for plotting
        self.UpdateGrid()           
        self.UpdatePlot()          
        self.Show()
    
    def UpdateGrid(self):
        try:
            data = Interfaces.GData[self.keys[0]]
            (rows,cols) = data.shape
        except:
            rows = 0
            cols = COLNO
            
        decimals = [-1,2,2,-1,2,2,-1,2,2,2,0,0]   #number of decimal digits for each colum

        for r in range(rows):
            for c in range(cols):
                if decimals[c] < 0:
                    try:
                        self.grid.SetCellValue(r,c,unicode(data[r][c],"utf-8"))
                    except:
                        self.grid.SetCellValue(r,c,data[r][c])
                else:
                    try:
                        self.grid.SetCellValue(r, c, convertDoubleToString(float(data[r][c]),nDecimals = decimals[c]))
                    except:
                        self.grid.SetCellValue(r, c, "")
                        logDebug("PanelHR (UpdateGrid): received corrupt data value [%s] at [r][c] = [%s][%s]"% \
                                 (r,c,data[r][c]))

        for r in range(rows,MAXROWS):
            for c in range(cols):
                self.grid.SetCellValue(r, c, "")

    def UpdatePlot(self):      
        if (self.cbCurveDisplay.GetCurrentSelection() == 0):
            try:
                self.plotpanel.Hide() 
                self.plotpanel.Destroy()
            except:
                pass
            self.plotpanel = HRPlotPanelHCG(self.panel_drawcurve)   
            self.plotpanel.Show()
            dummy = Mp.MatPanel(self.plotpanel, wx.Panel, drawFigure, None)
            del dummy
            self.plotpanel.draw()
        else:
            self.plotpanel.Hide() 
            self.plotpanel.Destroy()
            self.plotpanel = HRPlotPanelYED(self.panel_drawcurve)   
            self.plotpanel.Show()
            dummy = Mp.MatPanel(self.plotpanel, wx.Panel, drawFigure2, None)
            del dummy
            self.plotpanel.draw()
            
    def updateButtons(self,index):
        if (self.mod.indexExists(index)):
            self.enableButtons(True)
        else:
            self.enableButtons(False)
        
        if self.selectedRow in self.mod.HiddenHX:
            self.btnDeleteHX.Label = _U("Show HX")
        else:
            self.btnDeleteHX.Label = _U("Hide HX")
            
        
            
    def enableButtons(self,bool):        
        self.btnDeleteHX.Enabled = bool
        self.btnChangeHX.Enabled = bool
        
#------------------------------------------------------------------------------		
    def OnGridGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
        self.selectedRow = event.GetRow()
        print "PanelHR (GridLeftDclick): selected row = ",self.selectedRow
        event.Skip()

#------------------------------------------------------------------------------		
    def OnGridGridCellLeftClick(self, event):
#------------------------------------------------------------------------------		
        self.selectedRow = event.GetRow()
        self.updateButtons(self.selectedRow)
        print "PanelHR (GridLeftClick): selected row = ",self.selectedRow
        event.Skip()

    def OnGridGridCellRightClick(self, event):
        self.updateButtons(self.selectedRow)
        self.selectedRow = event.GetRow()
        print "PanelHR (GridRightClick): selected row = ",self.selectedRow
        event.Skip()
        
#==============================================================================
#   <<< OK Cancel >>>
#==============================================================================

    def OnButtonpageHROkButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qA, select=True)
        print "Button exitModuleOK: now I should go back to HR"

    def OnButtonpageHRCancelButton(self, event):
        self.Hide()
        print "Button exitModuleCancel: now I should go back to HR"

    def OnButtonpageHRBackButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qA, select=True)
        print "Button exitModuleBack: now I should show another window"

    def OnButtonpageHRFwdButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHP, select=True)
        print "Button exitModuleFwd: now I should show another window"


#==============================================================================
      
    def OnCbCurveDisplayChoice(self, event):            
        self.UpdatePlot()
        event.Skip()

    def OnBtnCalculateButton(self, event):
        print ("PanelHR (OnBtnCalculateButton)")      
        if (self.mod.redesign):
            self.mod.runHRDesign(exhx = self.cbExHX.GetValue())  
        else:
            self.mod.runHRModule(exhx = self.cbExHX.GetValue())            
        self.enableButtons(False)
        self.display()        
        event.Skip()

    def OnBtnDeleteHXButton(self, event):        
        self.mod.ShowHideHX(self.selectedRow)
        self.enableButtons(False)
        self.OnCbCurveDisplayChoice(event)
        self.display()
        event.Skip()

    def OnBtnChangeHXButton(self, event):
        self.mod.changeHX(self.selectedRow)
        self.UpdateGrid()
        event.Skip()

    def OnBtnShowStdValuesButton(self, event):
        dlg = DlgChangeHX(None)
        dlg.LockInput()
        dlg.ShowModal()        
        event.Skip()

    def OnCbExHXCheckbox(self, event):
        #self.mod.ExHX = self.cbExHX.GetValue()
        #print self.mod.ExHX
        event.Skip()

    def OnRbRedesignRadiobutton(self, event):
        self.mod.redesign = True
        event.Skip()

    def OnRbCalcRadiobutton(self, event):
        self.mod.redesign = False
        event.Skip()

    def OnCbConsiderCondCheckbox(self, event):
        self.mod.ConCondensation = self.cbConsiderCond.GetValue()
        event.Skip()
