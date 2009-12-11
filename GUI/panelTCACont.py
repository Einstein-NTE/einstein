#Boa:FramePanel:PanelTCAContingencies
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    PanelTCAContingencies: Contingencies
#                           (part of the TCA module)
#
#==============================================================================
#
#    Version No.: 0.01
#       Created by:          Florian Joebstl 15/09/2008  
#       Revised by:         Hans Schweiger  28/11/2008
#
#       Changes to previous version:
#
#   28/11/08: HS    changes to unicode in tables (str() eliminated)
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

import wx
import wx.grid
from einstein.GUI.status import Status
from GUITools import *

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

[wxID_PANELTCACONTINGENCIES, wxID_PANELTCACONTINGENCIESBTNADD, 
 wxID_PANELTCACONTINGENCIESBTNDELETE, wxID_PANELTCACONTINGENCIESBTNGOMAIN, 
 wxID_PANELTCACONTINGENCIESBUTTON1, wxID_PANELTCACONTINGENCIESCBNAME, 
 wxID_PANELTCACONTINGENCIESGRID, wxID_PANELTCACONTINGENCIESSTATICBOX1, 
 wxID_PANELTCACONTINGENCIESSTATICBOX2, wxID_PANELTCACONTINGENCIESSTATICTEXT1, 
 wxID_PANELTCACONTINGENCIESSTATICTEXT4, wxID_PANELTCACONTINGENCIESTEXTCTRL1, 
 wxID_PANELTCACONTINGENCIESTEXTCTRL2, 
] = [wx.NewId() for _init_ctrls in range(13)]

class PanelTCAContingencies(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELTCACONTINGENCIES, name='',
              parent=prnt, pos=wx.Point(0, 0), size=wx.Size(808, 627),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(800, 600))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELTCACONTINGENCIESSTATICBOX1,
              label=_U('Contingencies'), name='staticBox1', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(696, 544), style=0)

        self.staticText1 = wx.StaticText(id=wxID_PANELTCACONTINGENCIESSTATICTEXT1,
              label=_U('Do you expect future costs for perpetuating use of the current energy source in the process?'),
              name='staticText1', parent=self, pos=wx.Point(24, 32),
              size=wx.Size(450, 13), style=0)

        self.grid = wx.grid.Grid(id=wxID_PANELTCACONTINGENCIESGRID, name='grid',
              parent=self, pos=wx.Point(24, 56), size=wx.Size(580, 380),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGrid1GridCellLeftClick)

        self.textCtrl1 = wx.TextCtrl(id=wxID_PANELTCACONTINGENCIESTEXTCTRL1,
              name='textCtrl1', parent=self, pos=wx.Point(356, 448),
              size=wx.Size(145, 21), style=0, value='0')

        self.textCtrl2 = wx.TextCtrl(id=wxID_PANELTCACONTINGENCIESTEXTCTRL2,
              name='textCtrl2', parent=self, pos=wx.Point(506, 448),
              size=wx.Size(85, 21), style=0, value='0')

        self.staticText4 = wx.StaticText(id=wxID_PANELTCACONTINGENCIESSTATICTEXT4,
              label=_U('time frame (in X years from now, X=0 for current year)'),
              name='staticText4', parent=self, pos=wx.Point(40, 504),
              size=wx.Size(265, 13), style=0)
        self.staticText4.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))

        self.btnAdd = wx.Button(id=wxID_PANELTCACONTINGENCIESBTNADD,
              label=_U('Add'), name='btnAdd', parent=self, pos=wx.Point(616, 448),
              size=wx.Size(75, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_PANELTCACONTINGENCIESBTNADD)

        self.btnDelete = wx.Button(id=wxID_PANELTCACONTINGENCIESBTNDELETE,
              label=_U('Remove'), name='btnDelete', parent=self, pos=wx.Point(616,
              416), size=wx.Size(75, 23), style=0)
        self.btnDelete.Bind(wx.EVT_BUTTON, self.OnBtnDeleteButton,
              id=wxID_PANELTCACONTINGENCIESBTNDELETE)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELTCACONTINGENCIESSTATICBOX2,
              label=_U('Help'), name='staticBox2', parent=self, pos=wx.Point(16,
              480), size=wx.Size(680, 64), style=0)

        self.cbName = wx.ComboBox(choices=[],
              id=wxID_PANELTCACONTINGENCIESCBNAME, name='cbName', parent=self,
              pos=wx.Point(56, 448), size=wx.Size(295, 21), style=0,
              value=_U('<enter custom description or choose from list>'))

        self.btnGoMain = wx.Button(id=wxID_PANELTCACONTINGENCIESBTNGOMAIN,
              label=_U('Save and go to main page'), name='btnGoMain', parent=self,
              pos=wx.Point(8, 560), size=wx.Size(192, 23), style=0)
        self.btnGoMain.Bind(wx.EVT_BUTTON, self.OnBtnGoMainButton,
              id=wxID_PANELTCACONTINGENCIESBTNGOMAIN)

        self.button1 = wx.Button(id=wxID_PANELTCACONTINGENCIESBUTTON1,
              label=_U('Save and go to the next page >>>'), name='button1',
              parent=self, pos=wx.Point(512, 560), size=wx.Size(192, 23),
              style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_PANELTCACONTINGENCIESBUTTON1)

    def __init_custom_ctrls(self, prnt):
        #textcolor--------------------------------------------------------------------
        self.staticBox1.SetForegroundColour(TITLE_COLOR)
        self.staticBox1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        
        #Grid-------------------------------------------------------------------------
        self.rows = 17
        self.cols = 3
        self.grid.CreateGrid(self.rows, self.cols)

        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(200)
        self.grid.SetColSize(0,300)
        self.grid.SetColSize(1,150)
        self.grid.SetColSize(2,90)
        #self.grid.SetColSize(3,160)
        
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Description"))
        self.grid.SetColLabelValue(1, _U("EUR/Year"))
        self.grid.SetColLabelValue(2, _U("time frame"))

        self.updateGridAttributes()
        #choices---------------------------------------------------------------------
        self.cbName.Append(_U("tax disadvantages (other than energy tax)"))
        self.cbName.Append(_U("obligatory provisions"))
        self.cbName.Append(_U("costs for remediation activities"))
        self.cbName.Append(_U("cost for compliance with legislation"))
        self.cbName.Append(_U("negative impacts on market share"))
        self.cbName.Append(_U("deterioration of company image"))
        self.cbName.Append(_U("affection by CO2-emission trading directive"))
     
        
        
    def __init__(self, parent, main, id, pos, size, style, name):
        #print "Init Contingencies"
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)
        self.main = main
        self.mod = Status.mod.moduleTCA
        self.shortName = _U("TCAContingencies")
        self.description = " "
        self.selectedRow = None

              
    def updateGridAttributes(self):
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        for r in range(self.rows):
            self.grid.SetRowSize(r,20)
            self.grid.SetRowAttr(r, attr)
    
    def updatePanel(self):
        #TCA should no run with present state(original)
        if (Status.ANo == -1):
            wx.MessageBox("Could not display TCA for unchecked state!")            
            self.main.tree.SelectItem(self.main.qCC, select=True)
            return False
        else:
            self.mod.updatePanel()
            return True    
             
    def display(self):          
        if not(self.updatePanel()):
            return
        #Update grid------------------------------------------------  
        div = len(self.mod.data.contingencies) - self.rows
        if (div>0):
            self.rows=len(self.mod.data.contingencies)
            self.grid.AppendRows(div) 
            self.updateGridAttributes()  
        for r in range(0,self.rows):
            for c in range(self.cols):
                self.grid.SetCellValue(r, c, "")
        for r in range(len(self.mod.data.contingencies)):
            for c in range(self.cols):
                try:
                    self.grid.SetCellValue(r, c, self.mod.data.contingencies[r][c])
                except:
                    self.grid.SetCellValue(r, c, str(self.mod.data.contingencies[r][c]))
 

    def OnGrid1GridCellLeftClick(self, event):
        self.selectedRow = event.GetRow()  
        
        if (self.selectedRow < len(self.mod.data.contingencies)):
            entry = self.mod.data.contingencies[self.selectedRow]
            
            self.cbName.SetValue(entry[0])
            self.textCtrl1.SetValue(str(entry[1]))
            self.textCtrl2.SetValue(str(entry[2]))                        
            self.btnAdd.SetLabel("Change")
        else:
            self.btnAdd.SetLabel("Add")
      
        event.Skip()

    def OnChoice1Choice(self, event):
        event.Skip()

    def OnBtnAddButton(self, event):
        try:
            name = self.cbName.GetValue()
            eur_year = float(self.textCtrl1.GetValue())
            timeframe = int(self.textCtrl2.GetValue())
           
            if (timeframe<0)or(eur_year<0):
                raise   
                     
            try:                    
                if (self.selectedRow < len(self.mod.data.contingencies)):
                    self.mod.data.contingencies[self.selectedRow] = [name,eur_year,timeframe]
                else:           
                    self.mod.data.contingencies.append([name,eur_year,timeframe])                
            except:
                 self.mod.data.contingencies.append([name,eur_year,timeframe])                
        except:
            wx.MessageBox(_U("Reconsider values."))
        event.Skip()
        self.display()  

    def OnBtnDeleteButton(self, event):
        if (self.selectedRow < len(self.mod.data.contingencies)):
            self.mod.data.contingencies.pop(self.selectedRow)  
        event.Skip()
        self.display()    

    def OnBtnGoMainButton(self, event):
        self.Hide()
        self.mod.storeData()
        self.main.tree.SelectItem(self.main.qECO, select=True)
        event.Skip()        

    def OnButton1Button(self, event):
        self.Hide()
        self.mod.storeData()
        self.main.tree.SelectItem(self.main.qECO4, select=True)
        event.Skip()        
