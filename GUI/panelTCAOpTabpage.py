#Boa:FramePanel:panelTCAOpTabpage
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    panelTCAOpTabpage: Detailed Operating Costs (Tabpage)
#                      (part of the TCA module)
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
import wx
import wx.grid
from GUITools import *

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

[wxID_PANELTCAOPTABPAGE, wxID_PANELTCAOPTABPAGEBTNADD, 
 wxID_PANELTCAOPTABPAGEBTNCHANGE, wxID_PANELTCAOPTABPAGEBTNREMOVE, 
 wxID_PANELTCAOPTABPAGECBNAME, wxID_PANELTCAOPTABPAGEGRID, 
 wxID_PANELTCAOPTABPAGESTATICBOX1, wxID_PANELTCAOPTABPAGESTATICTEXT1, 
 wxID_PANELTCAOPTABPAGETBVALUE, wxID_PANELTCAOPTABPAGETHELP, 
] = [wx.NewId() for _init_ctrls in range(10)]

class panelTCAOpTabpage(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELTCAOPTABPAGE, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(581, 457),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(573, 430))

        self.grid = wx.grid.Grid(id=wxID_PANELTCAOPTABPAGEGRID, name='grid',
              parent=self, pos=wx.Point(8, 8), size=wx.Size(488, 312), style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGridGridCellLeftClick)

        self.cbName = wx.Choice(choices=[], id=wxID_PANELTCAOPTABPAGECBNAME,
              name='cbName', parent=self, pos=wx.Point(48, 328),
              size=wx.Size(240, 21), style=0)

        self.tbValue = wx.TextCtrl(id=wxID_PANELTCAOPTABPAGETBVALUE,
              name='tbValue', parent=self, pos=wx.Point(296, 328),
              size=wx.Size(160, 21), style=0, value='0')

        self.staticText1 = wx.StaticText(id=wxID_PANELTCAOPTABPAGESTATICTEXT1,
              label='EUR/a', name='staticText1', parent=self, pos=wx.Point(464,
              328), size=wx.Size(30, 13), style=0)

        self.btnAdd = wx.Button(id=wxID_PANELTCAOPTABPAGEBTNADD, label=_U('Add'),
              name='btnAdd', parent=self, pos=wx.Point(504, 328),
              size=wx.Size(64, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_PANELTCAOPTABPAGEBTNADD)

        self.btnRemove = wx.Button(id=wxID_PANELTCAOPTABPAGEBTNREMOVE,
              label=_U('Remove'), name='btnRemove', parent=self,
              pos=wx.Point(504, 296), size=wx.Size(64, 23), style=0)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.OnBtnRemoveButton,
              id=wxID_PANELTCAOPTABPAGEBTNREMOVE)

        self.staticBox1 = wx.StaticBox(id=wxID_PANELTCAOPTABPAGESTATICBOX1,
              label=_U('Help'), name='staticBox1', parent=self, pos=wx.Point(8,
              360), size=wx.Size(560, 64), style=0)

        self.tHelp = wx.StaticText(id=wxID_PANELTCAOPTABPAGETHELP,
              label='HELPTEXT', name='tHelp', parent=self, pos=wx.Point(24,
              378), size=wx.Size(50, 13), style=0)
        self.tHelp.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL, False,
              'Tahoma'))

    def __init_custom_ctrls(self, prnt):
        #Grid-------------------------------------------------------------------------
        self.rows = 13
        self.cols = 2

        self.grid.CreateGrid(self.rows,self.cols)

        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(200)
        self.grid.SetColSize(0,250)
        self.grid.SetColSize(1,200)
        
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Description"))
        self.grid.SetColLabelValue(1, _U("Operating cost\n[EUR/a]"))
        
        self.updateGridAttributes()
        #choices--------------------------------------------------------------------------------
        self.cbName.Append(_U("H&C Storage"))
        self.cbName.Append(_U("CHP"))
        self.cbName.Append(_U("Solar thermal"))
        self.cbName.Append(_U("Heat pump"))
        self.cbName.Append(_U("Biomass"))
        self.cbName.Append(_U("Chillers"))
        self.cbName.Append(_U("Boilers and furnaces"))
        self.cbName.Append(_U("HX network"))
        self.cbName.Append(_U("H&C distribution"))
        self.cbName.SetSelection(0)
       
    def __init__(self, parent, id, pos, size, style, name):
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


    def display(self):          
        #Update grid------------------------------------------------
        div = len(self.items) - self.rows
        if (div>0):
            self.rows=len(self.items)
            self.grid.AppendRows(div) 
            self.updateGridAttributes()
        for r in range(0,self.rows):
            for c in range(self.cols):
                self.grid.SetCellValue(r, c, "")
        for r in range(len(self.items)):
            for c in range(self.cols):
                self.grid.SetCellValue(r, c, str(self.items[r][c]))

    def OnGridGridCellLeftClick(self, event):
        self.selectedRow = event.GetRow()  
        if (self.selectedRow < len(self.items)):
            entry = self.items[self.selectedRow]
            if self.cbName.FindString(str(entry[0]))<0: #create choice if not exists
                self.cbName.Append(str(entry[0]))
            self.cbName.SetStringSelection(str(entry[0]))                                 
            self.tbValue.SetValue(str(entry[1]))        
            self.btnAdd.SetLabel("Change")
        else:
            self.btnAdd.SetLabel("Add")
        event.Skip()  

    def OnBtnAddButton(self, event):
        try:
            name = self.cbName.GetStringSelection()
            value = float(self.tbValue.GetValue())                                    
                      
            if (value<0):
                raise            
            
            try:                    
                if (self.selectedRow < len(self.items)):
                    self.items[self.selectedRow] = [name,value]
                else:           
                    self.items.append([name,value])                  
            except:
                self.items.append([name,value])            
                          
        except:
            wx.MessageBox(_U("Reconsider values."))
        event.Skip()
        self.display()  

    def OnBtnRemoveButton(self, event):
        try:
            if (self.selectedRow < len(self.items)):
                self.items.pop(self.selectedRow)
        except:
            pass  
        event.Skip()
        self.display()    

    def OnBtnChangeButton(self, event):
        event.Skip()
