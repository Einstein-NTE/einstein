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

from einstein.GUI.graphics import drawPiePlot
import einstein.modules.matPanel as Mp
from matplotlib.ticker import MaxNLocator
from einstein.modules.calculationTCA import *

def drawFigure(self):
    if (Status.mod.moduleTCA.displayPlot == 0):
        if (Status.mod.moduleTCA.result != None):
            if hasattr(self, 'subplot'):
                del self.subplot                     
            self.subplot = self.figure.add_subplot(111)   
            for result in Status.mod.moduleTCA.result:    
                if (result.display == 1):  
                    npv = [0.0] * len(result.npv)
                    for i in xrange(0,len(result.npv)):
                        if (result.npv[i]>0):
                            npv[i] = result.npv[i]      
                    self.subplot.plot(npv, label = "NPV - "+str(result.name))  
                              
            self.subplot.legend(loc = 0)
            self.subplot.set_xlabel(_('time / Y'))
            self.subplot.set_ylabel(_('NPV / EUR'))  
    else:
        if (Status.mod.moduleTCA.result != None):
            if hasattr(self, 'subplot'):
                del self.subplot
                   
            self.subplot = self.figure.add_subplot(111)   
            for result in Status.mod.moduleTCA.result: 
                if (result.display == 1):   
                    mirr = [0.0] * len(result.mirr) 
                    for i in xrange(0, len(result.mirr)):
                        if result.mirr[i]>0:
                            mirr[i] = result.mirr[i]
                                
                    self.subplot.plot(mirr, label = "MIRR - "+str(result.name))  
                         
            self.subplot.legend(loc = 0)
            self.subplot.set_xlabel(_('time / Y'))
            self.subplot.set_ylabel(_('MIRR / EUR'))      
            
            #yaxis = self.subplot.axes.yaxis
            #self.subplot.axis()
            #print [0,len(result.mirr),0,max(result.mirr)]
            #self.subplot.axes.yaxis = yaxis
                                        
    
    #self.subplot.legend()   
    self.setSize(wx.Size(544, 312))
     
import wx
from GUITools import *
[wxID_PANELRESULT2, wxID_PANELRESULT2BTNADD, wxID_PANELRESULT2BTNREMOVE, 
 wxID_PANELRESULT2CHOICE1, wxID_PANELRESULT2PANEL1, wxID_PANELRESULT2RBMIRR, 
 wxID_PANELRESULT2RBNPV, wxID_PANELRESULT2STATICBOX1, 
 wxID_PANELRESULT2STATICBOX2, 
] = [wx.NewId() for _init_ctrls in range(9)]

class panelResult2(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELRESULT2, name='', parent=prnt,
              pos=wx.Point(373, 64), size=wx.Size(730, 350),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(722, 323))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELRESULT2STATICBOX1,
              label=_(u'Choose the proposal(s)'), name='staticBox1',
              parent=self, pos=wx.Point(560, 80), size=wx.Size(160, 240),
              style=0)

        self.choice1 = wx.Choice(choices=[], id=wxID_PANELRESULT2CHOICE1,
              name='choice1', parent=self, pos=wx.Point(568, 104),
              size=wx.Size(144, 21), style=0)
        self.choice1.Bind(wx.EVT_CHOICE, self.OnChoice1Choice,
              id=wxID_PANELRESULT2CHOICE1)

        self.btnAdd = wx.Button(id=wxID_PANELRESULT2BTNADD, label=_('Add'),
              name=u'btnAdd', parent=self, pos=wx.Point(568, 136),
              size=wx.Size(144, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_PANELRESULT2BTNADD)

        self.btnRemove = wx.Button(id=wxID_PANELRESULT2BTNREMOVE,
              label=_('Remove'), name=u'btnRemove', parent=self,
              pos=wx.Point(568, 168), size=wx.Size(144, 23), style=0)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.OnBtnRemoveButton,
              id=wxID_PANELRESULT2BTNREMOVE)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELRESULT2STATICBOX2,
              label=_(u'Please choose the parameters'), name='staticBox2',
              parent=self, pos=wx.Point(560, 0), size=wx.Size(160, 80),
              style=0)

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

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)
        self.choice1.SetSelection(0)
        self.display()
        
    def __init_custom_ctrls(self, prnt):
          Status.mod.moduleTCA.displayPlot = 0   
          self.chart = Mp.MatPanel(self.panel1, wx.Panel, drawFigure)
          del self.chart
    
    def display(self):
        self.panel1.draw()       
        self.choice1.Clear()
        if (Status.mod.moduleTCA.result!=None):
            for result in Status.mod.moduleTCA.result:            
                self.choice1.Append(str(result.name))
            self.choice1.SetSelection(0)
        self.updateButtons()

    def OnRbNPVRadiobutton(self, event):        
        if (self.rbNPV.GetValue()==True):
            Status.mod.moduleTCA.displayPlot = 0            
            self.chart = Mp.MatPanel(self.panel1, wx.Panel, drawFigure)
            del self.chart
            self.display()
            
        event.Skip()

    def OnRbMIRRRadiobutton(self, event):
        if (self.rbMIRR.GetValue()==True):
            Status.mod.moduleTCA.displayPlot = 1            
            self.chart = Mp.MatPanel(self.panel1, wx.Panel, drawFigure)
            del self.chart  
            self.display()          
        event.Skip()

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
            Status.mod.moduleTCA.result[index].display = 1
        except:
            pass
        self.display()
        event.Skip()

    def OnBtnRemoveButton(self, event):                
        try:
            index = self.choice1.GetSelection()
            Status.mod.moduleTCA.result[index].display = 0
        except:
            pass
        self.display()
        event.Skip()
