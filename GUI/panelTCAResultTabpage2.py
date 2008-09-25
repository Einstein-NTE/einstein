#Boa:FramePanel:panelResult2
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    panelResult1: TCA Resultpage - Diagram (Tabpage of panelTCA)
#                  (part of the TCA module)
#
#
#==============================================================================
#
#    Version No.: 0.01
#       Created by:          Florian Joebstl 15/09/2008  
#       Revised by:       
#
#       Changes to previous version:
#
#
#------------------------------------------------------------------------------
#    (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#    http://www.energyxperts.net/
#
#    This program is free software: you can redistribute it or modify it under
#    the terms of the GNU general public license as published by the Free
#    Software Foundation (www.gnu.org).
#
#==============================================================================

#from einstein.GUI.graphics import drawPiePlot
#import einstein.modules.matPanel as Mp

from einstein.modules.calculationTCA import *
from einstein.modules.plotPanel import PlotPanel
from pylab import *
import wx
#from matplotlib.ticker import MaxNLocator

class TCAPlotPanel (PlotPanel):
    """Plots several lines in distinct colors."""
    def __init__( self, parent, **kwargs ):
        self.parent = parent
        # initiate plotter
        PlotPanel.__init__( self, parent, **kwargs )
        self.SetColor( (255,255,255) )

    def draw( self ):
        """Draw data."""
        if not hasattr( self, 'subplot' ):
            self.subplot = self.figure.add_subplot( 111 )
            
        if (Status.mod.moduleTCA.result != None): 
            if (Status.mod.moduleTCA.displayPlot == 0):  
                self.plot("npv")
            else:            
                self.plot("mirr")   
                                                                       
    def plot(self,mode):                                  
        results = Status.mod.moduleTCA.result
                                                            
        results_to_display = 0
        for result in results: 
            if (result.display == 1)and(result.ResultPresent):
                results_to_display +=1  
                if (mode == "mirr"):
                    timeFrame = len(result.mirr)-1
                else:
                    timeFrame = len(result.npv)-1
        
        if (results_to_display == 0):
            return
            
        timeStep = 5.0
        size = int(timeFrame/timeStep)
        
        add_last_year = False
        if (timeFrame % timeStep)!=0: 
            add_last_year = True
            size = size+1
                         
        ind = arange(size)  
        width = 1.0/(results_to_display+1)
        count = 0
        colorcount = 0
        ticklabls = []
        color = ['b','g','r','y']
        
        for result in results:                       
            if (result.display == 1)and(result.ResultPresent):
                if (mode=="mirr"):
                    original_data = result.mirr
                    self.subplot.set_ylabel(_('MIRR / EUR')) 
                else:
                    original_data = result.npv
                    self.subplot.set_ylabel(_('NPV / EUR'))                                              
                data = [0.0] * (size)                      
                index = 0
                for i in xrange(0, timeFrame+1):                                                       
                    if (i % timeStep == 0)and(i!=0):                                
                        if original_data[i]>0:
                            data[index] = original_data[i]
                        ticklabls.append(_("Year ")+str(i))                                                                
                        index = index+1                        
                if (add_last_year):
                    ticklabls.append(_("Year ")+str(timeFrame))
                    data[len(data)-1] = (original_data[timeFrame-1])
                self.subplot.bar(ind+width*count,data, width, color = color[colorcount], label = "MIRR - "+str(result.name))                        
                count+=1  
            colorcount+=1
        
        self.subplot.xaxis.set_ticklabels(ticklabls)
        self.subplot.xaxis.set_ticks(ind+(width*count)/2)
        if (Status.mod.moduleTCA.showlegend):
            self.subplot.legend(loc = 4)       

     
import wx
from GUITools import *
[wxID_PANELRESULT2, wxID_PANELRESULT2BTNADD, wxID_PANELRESULT2BTNREMOVE, 
 wxID_PANELRESULT2CBSHOWLEGEND, wxID_PANELRESULT2CHOICE1, 
 wxID_PANELRESULT2PANEL1, wxID_PANELRESULT2RBMIRR, wxID_PANELRESULT2RBNPV, 
 wxID_PANELRESULT2STATICBOX1, wxID_PANELRESULT2STATICBOX2, 
 wxID_PANELRESULT2STATICBOX3, 
] = [wx.NewId() for _init_ctrls in range(11)]

class panelResult2(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELRESULT2, name='', parent=prnt,
              pos=wx.Point(373, 64), size=wx.Size(730, 350),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(722, 323))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELRESULT2STATICBOX1,
              label=_(u'Choose the proposal(s)'), name='staticBox1',
              parent=self, pos=wx.Point(560, 136), size=wx.Size(160, 184),
              style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_PANELRESULT2CHOICE1,
              name='choice1', parent=self, pos=wx.Point(568, 160),
              size=wx.Size(144, 21), style=0)
        self.choice1.Bind(wx.EVT_CHOICE, self.OnChoice1Choice,
              id=wxID_PANELRESULT2CHOICE1)

        self.btnAdd = wx.Button(id=wxID_PANELRESULT2BTNADD, label=_('Add'),
              name=u'btnAdd', parent=self, pos=wx.Point(568, 192),
              size=wx.Size(144, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_PANELRESULT2BTNADD)

        self.btnRemove = wx.Button(id=wxID_PANELRESULT2BTNREMOVE,
              label=_('Remove'), name=u'btnRemove', parent=self,
              pos=wx.Point(568, 224), size=wx.Size(144, 23), style=0)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.OnBtnRemoveButton,
              id=wxID_PANELRESULT2BTNREMOVE)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELRESULT2STATICBOX2,
              label=_(u'Choose Figure'), name='staticBox2', parent=self,
              pos=wx.Point(560, 0), size=wx.Size(160, 80), style=0)

        self.panel1 = wx.Panel(id=wxID_PANELRESULT2PANEL1, name='panel1',
              parent=self, pos=wx.Point(8, 8), size=wx.Size(544, 312),
              style=wx.TAB_TRAVERSAL)

        self.rbNPV = wx.RadioButton(id=wxID_PANELRESULT2RBNPV, label=u'NPV',
              name=u'rbNPV', parent=self, pos=wx.Point(584, 24),
              size=wx.Size(81, 13), style=0)
        self.rbNPV.SetValue(True)
        self.rbNPV.Bind(wx.EVT_RADIOBUTTON, self.OnRbNPVRadiobutton,
              id=wxID_PANELRESULT2RBNPV)

        self.rbMIRR = wx.RadioButton(id=wxID_PANELRESULT2RBMIRR, label=u'MIRR',
              name=u'rbMIRR', parent=self, pos=wx.Point(584, 48),
              size=wx.Size(81, 13), style=0)
        self.rbMIRR.SetValue(False)
        self.rbMIRR.Bind(wx.EVT_RADIOBUTTON, self.OnRbMIRRRadiobutton,
              id=wxID_PANELRESULT2RBMIRR)

        self.cbShowLegend = wx.CheckBox(id=wxID_PANELRESULT2CBSHOWLEGEND,
              label=_(u'Show/Hide'), name=u'cbShowLegend', parent=self,
              pos=wx.Point(584, 104), size=wx.Size(112, 13), style=0)
        self.cbShowLegend.SetValue(True)
        self.cbShowLegend.Bind(wx.EVT_CHECKBOX, self.OnCbShowLegendCheckbox,
              id=wxID_PANELRESULT2CBSHOWLEGEND)

        self.staticBox3 = wx.StaticBox(id=wxID_PANELRESULT2STATICBOX3,
              label=u'Legend', name='staticBox3', parent=self, pos=wx.Point(560,
              80), size=wx.Size(160, 56), style=0)

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)
        self.choice1.SetSelection(0)
        self.display()
        
    def __init_custom_ctrls(self, prnt):
          Status.mod.moduleTCA.displayPlot = 0 
          Status.mod.moduleTCA.showlegend = self.cbShowLegend.GetValue()     
          self.plotpanel = TCAPlotPanel(self.panel1)
                 
    
    def display(self):
        self.choice1.Clear()
        if (Status.mod.moduleTCA.result!=None):
            for result in Status.mod.moduleTCA.result:            
                self.choice1.Append(str(result.name))
            self.choice1.SetSelection(0)
        self.updateButtons()

    def OnRbNPVRadiobutton(self, event):        
        if (self.rbNPV.GetValue()==True):
            Status.mod.moduleTCA.displayPlot = 0            
            self.updatePanel()        
        event.Skip()

    def OnRbMIRRRadiobutton(self, event):
        if (self.rbMIRR.GetValue()==True):
            Status.mod.moduleTCA.displayPlot = 1            
            self.updatePanel()   
        event.Skip()

    def updatePanel(self):
        self.plotpanel.Hide() 
        self.plotpanel.Destroy()
        Status.mod.moduleTCA.showlegend = self.cbShowLegend.GetValue()     
        self.plotpanel = TCAPlotPanel(self.panel1)          
        self.plotpanel.Show()   
        
    def OnChoice1Choice(self, event):
        self.updateButtons()
        event.Skip()
    
    def updateButtons(self):
        try:
            index = self.choice1.GetSelection()
            if (Status.mod.moduleTCA.result[index].display == 0):
                self.btnAdd.Enabled = True
                self.btnRemove.Enabled  = False
            else:
                self.btnAdd.Enabled = False
                self.btnRemove.Enabled  = True
        except:
            pass

    def OnBtnAddButton(self, event):
        try:
            index = self.choice1.GetSelection()
            
            if (Status.mod.moduleTCA.result[index].ResultPresent):
                Status.mod.moduleTCA.result[index].display = 1
            else:
                name = Status.mod.moduleTCA.result[index].name
                wx.MessageBox(_("No result to display for proposal: ")+name)                
            self.updatePanel()
        except:
            pass
        self.display()
        event.Skip()

    def OnBtnRemoveButton(self, event):                
        try:
            index = self.choice1.GetSelection()
            Status.mod.moduleTCA.result[index].display = 0
            self.updatePanel()
        except:
            pass
        self.display()
        event.Skip()

    def OnCbShowLegendCheckbox(self, event):
        self.updatePanel()
        event.Skip()
        
