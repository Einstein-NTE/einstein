#Boa:FramePanel:PanelTCANon
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    PanelTCAInvestment: Non reoccuring costs
#                       (part of the TCA module)
#
#
#==============================================================================
#
#    Version No.: 0.02
#       Created by:          Florian Joebstl 15/09/2008  
#       Revised by:         Hans Schweiger  28/11/2008    
#
#       Changes to previous version:
#
#   28/11/08: HS    changes to unicode (str() function in grid eliminated)
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

[wxID_PANELTCANON, wxID_PANELTCANONBTNADD, wxID_PANELTCANONBTNDELETE, 
 wxID_PANELTCANONBTNGOMAIN, wxID_PANELTCANONBTNNEXT, 
 wxID_PANELTCANONCBCOSTREV, wxID_PANELTCANONCBNAME, wxID_PANELTCANONGRID, 
 wxID_PANELTCANONSTATICBOX1, wxID_PANELTCANONSTATICBOX2, 
 wxID_PANELTCANONSTATICTEXT4, wxID_PANELTCANONTEXTCTRL1, 
 wxID_PANELTCANONTEXTCTRL2, 
] = [wx.NewId() for _init_ctrls in range(13)]

class PanelTCANon(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELTCANON, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(808, 627),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(800, 600))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELTCANONSTATICBOX1,
              label=_U('Non Re-Occuring Cost'), name='staticBox1', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(768, 544), style=0)

        self.grid = wx.grid.Grid(id=wxID_PANELTCANONGRID, name='grid',
              parent=self, pos=wx.Point(24, 32), size=wx.Size(640, 408),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGrid1GridCellLeftClick)

        self.textCtrl1 = wx.TextCtrl(id=wxID_PANELTCANONTEXTCTRL1,
              name='textCtrl1', parent=self, pos=wx.Point(388, 448),
              size=wx.Size(100, 21), style=0, value='0')

        self.textCtrl2 = wx.TextCtrl(id=wxID_PANELTCANONTEXTCTRL2,
              name='textCtrl2', parent=self, pos=wx.Point(498, 448),
              size=wx.Size(62, 21), style=0, value='0')

        self.staticText4 = wx.StaticText(id=wxID_PANELTCANONSTATICTEXT4,
              label=_U('year =  indicate when presumably occuring in years after investment'),
              name='staticText4', parent=self, pos=wx.Point(40, 504),
              size=wx.Size(331, 13), style=0)
        self.staticText4.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))

        self.btnAdd = wx.Button(id=wxID_PANELTCANONBTNADD, label=_U('Add'),
              name='btnAdd', parent=self, pos=wx.Point(680, 448),
              size=wx.Size(75, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_PANELTCANONBTNADD)

        self.btnDelete = wx.Button(id=wxID_PANELTCANONBTNDELETE, label=_U('Remove'),
              name='btnDelete', parent=self, pos=wx.Point(680, 416),
              size=wx.Size(75, 23), style=0)
        self.btnDelete.Bind(wx.EVT_BUTTON, self.OnBtnDeleteButton,
              id=wxID_PANELTCANONBTNDELETE)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELTCANONSTATICBOX2,
              label=_U('Help'), name='staticBox2', parent=self, pos=wx.Point(16,
              480), size=wx.Size(752, 64), style=0)

        self.cbName = wx.ComboBox(choices=[], id=wxID_PANELTCANONCBNAME,
              name='cbName', parent=self, pos=wx.Point(56, 448),
              size=wx.Size(328, 21), style=0,
              value=_U('<enter custom description or choose from list>'))

        self.cbCostRev = wx.Choice(choices=["Cost", "Revenue"],
              id=wxID_PANELTCANONCBCOSTREV, name='cbCostRev', parent=self,
              pos=wx.Point(568, 448), size=wx.Size(98, 21), style=0)
        self.cbCostRev.SetSelection(0)

        self.btnNext = wx.Button(id=wxID_PANELTCANONBTNNEXT,
              label=_U('Finish'), name='btnNext',
              parent=self, pos=wx.Point(584, 560), size=wx.Size(192, 23),
              style=0)
        self.btnNext.Bind(wx.EVT_BUTTON, self.OnBtnNextButton,
              id=wxID_PANELTCANONBTNNEXT)

    def __init_custom_ctrls(self, prnt):
        #textcolor--------------------------------------------------------------------
        self.staticBox1.SetForegroundColour(TITLE_COLOR)
        self.staticBox1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        
        #Grid-------------------------------------------------------------------------
        self.rows = 18
        self.cols = 4
      
        self.grid.CreateGrid(self.rows, self.cols)

        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(200)
        self.grid.SetColSize(0,330)
        self.grid.SetColSize(1,115)
        self.grid.SetColSize(2,65)
        self.grid.SetColSize(3,85)
        
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Description"))
        self.grid.SetColLabelValue(1, _U("EUR"))
        self.grid.SetColLabelValue(2, _U("Year"))
        self.grid.SetColLabelValue(3, _U("Type"))

        self.updateGridAttributes()
        #choices---------------------------------------------------------------------
        self.cbName.Append(_U("repair works for energy equipment"))
        self.cbName.Append(_U("exchange of collectors"))
        self.cbName.Append(_U("irregular maintainance costs"))
        self.cbName.Append(_U("permits"))
        self.cbName.Append(_U("fines/penalties"))
        self.cbName.Append(_U("legal costs"))
        self.cbName.Append(_U("property/natural resource damage"))
        self.cbName.Append(_U("remediation costs"))
        self.cbName.Append(_U("clean up costs"))
        self.cbName.Append(_U("revenue for marketable permits"))
        self.cbName.Append(_U("other revenues"))
     
        
        
    def __init__(self, parent, main, id, pos, size, style, name):
        #print "Init Non-reoccuring"       
        self.main = main
        self.mod = Status.mod.moduleTCA
        self.shortName = _U("TCAContingencies")
        self.description = _U("")   
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)
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
            #self.Hide()
            self.main.tree.SelectItem(self.main.qCC, select=True)
            return False
        else:
            self.mod.updatePanel()
            return True    
             
    def display(self):          
        if not(self.updatePanel()):
            return 
        #Update grid------------------------------------------------  
        div = len(self.mod.data.nonreoccuringcosts) - self.rows
        if (div>0):
            self.rows=len(self.mod.data.nonreoccuringcosts)
            self.grid.AppendRows(div) 
            self.updateGridAttributes()  
        for r in range(0,self.rows):
            for c in range(self.cols):
                self.grid.SetCellValue(r, c, "")
        for r in range(len(self.mod.data.nonreoccuringcosts)):
            for c in range(self.cols):
                try:
                    self.grid.SetCellValue(r, c, self.mod.data.nonreoccuringcosts[r][c])
                except:
                    self.grid.SetCellValue(r, c, str(self.mod.data.nonreoccuringcosts[r][c]))
 

    def OnGrid1GridCellLeftClick(self, event):
        self.selectedRow = event.GetRow() 
        
        if (self.selectedRow < len(self.mod.data.nonreoccuringcosts)):
            entry = self.mod.data.nonreoccuringcosts[self.selectedRow]
                        
            self.cbName.SetValue(entry[0])            
            self.textCtrl1.SetValue(str(entry[1]))
            self.textCtrl2.SetValue(str(entry[2]))
            self.cbCostRev.SetStringSelection(str(entry[3]))                        
            self.btnAdd.SetLabel("Change")
        else:
            self.btnAdd.SetLabel("Add")  
                 
        event.Skip()

    def OnChoice1Choice(self, event):
        event.Skip()

    def OnBtnAddButton(self, event):
        try:
            name = self.cbName.GetValue()
            euro = float(self.textCtrl1.GetValue())
            year = int(self.textCtrl2.GetValue())
            type = self.cbCostRev.GetStringSelection()
           
            if (euro<0)or(year<0):
                raise            
            try:                    
                if (self.selectedRow < len(self.mod.data.nonreoccuringcosts)):
                    self.mod.data.nonreoccuringcosts[self.selectedRow] = [name,euro,year,type]
                else:           
                    self.mod.data.nonreoccuringcosts.append([name,euro,year,type])               
            except:
                 self.mod.data.nonreoccuringcosts.append([name,euro,year,type])                   
                            
        except:
            wx.MessageBox(_U("Reconsider values."))
            
        event.Skip()
        self.display()  

    def OnBtnDeleteButton(self, event):
        try:
            if (self.selectedRow < len(self.mod.data.nonreoccuringcosts)):
                self.mod.data.nonreoccuringcosts.pop(self.selectedRow)
        except:
            pass  
        event.Skip()
        self.display()    

    def OnBtnNextButton(self, event):        
        self.Hide()
        self.mod.storeData()
        self.main.tree.SelectItem(self.main.qECO, select=True)
        event.Skip()  
              
