#Boa:Dialog:dlgRevenue
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    dlgRevenue: Dialog for revenue estimation
#               (part of the TCA module)
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

def create(parent):
    return dlgRevenue(parent)

[wxID_DLGREVENUE, wxID_DLGREVENUEBTNADD, wxID_DLGREVENUEBTNAPPLY, 
 wxID_DLGREVENUEBTNCANCEL, wxID_DLGREVENUEBTNREMOVE, 
 wxID_DLGREVENUECBCATEGORY, wxID_DLGREVENUECBSUBCATEGORY, wxID_DLGREVENUEGRID, 
 wxID_DLGREVENUERBBOOKVALUE, wxID_DLGREVENUERBINITINVESTMENT, 
 wxID_DLGREVENUESTATICBOX1, wxID_DLGREVENUESTATICBOX2, 
 wxID_DLGREVENUESTATICBOX3, wxID_DLGREVENUESTATICTEXT1, 
 wxID_DLGREVENUESTATICTEXT2, wxID_DLGREVENUESTATICTEXT3, 
 wxID_DLGREVENUESTATICTEXT4, wxID_DLGREVENUETBDEPPERIOD, 
 wxID_DLGREVENUETBINITINVESTMENT, wxID_DLGREVENUETBPERC, 
 wxID_DLGREVENUETBREMPERIOD, wxID_DLGREVENUETRESULT, wxID_DLGREVENUETREVENUE, 
] = [wx.NewId() for _init_ctrls in range(23)]

class dlgRevenue(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGREVENUE, name='dlgRevenue',
              parent=prnt, pos=wx.Point(374, 32), size=wx.Size(823, 685),
              style=wx.DEFAULT_DIALOG_STYLE,
              title='Estimate revenue from the sale of replaced equipments')
        self.SetClientSize(wx.Size(815, 658))

        self.rbInitInvestment = wx.RadioButton(id=wxID_DLGREVENUERBINITINVESTMENT,
              label='Calculate with percentage of initial investment',
              name='rbInitInvestment', parent=self, pos=wx.Point(24, 32),
              size=wx.Size(256, 13), style=0)
        self.rbInitInvestment.SetValue(True)
        self.rbInitInvestment.Bind(wx.EVT_RADIOBUTTON,
              self.OnRbInitInvestmentRadiobutton,
              id=wxID_DLGREVENUERBINITINVESTMENT)

        self.rbBookValue = wx.RadioButton(id=wxID_DLGREVENUERBBOOKVALUE,
              label='Calculate with percentage of current book value',
              name='rbBookValue', parent=self, pos=wx.Point(24, 48),
              size=wx.Size(264, 13), style=0)
        self.rbBookValue.SetValue(False)
        self.rbBookValue.Bind(wx.EVT_RADIOBUTTON, self.OnRbBookValueRadiobutton,
              id=wxID_DLGREVENUERBBOOKVALUE)

        self.staticBox1 = wx.StaticBox(id=wxID_DLGREVENUESTATICBOX1,
              label='Choose Method', name='staticBox1', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(800, 72), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_DLGREVENUESTATICBOX2,
              label='Calculation', name='staticBox2', parent=self,
              pos=wx.Point(8, 552), size=wx.Size(800, 96), style=0)

        self.tResult = wx.StaticText(id=wxID_DLGREVENUETRESULT,
              label='1000000 EUR', name='tResult', parent=self,
              pos=wx.Point(88, 576), size=wx.Size(65, 13), style=0)

        self.staticBox3 = wx.StaticBox(id=wxID_DLGREVENUESTATICBOX3,
              label='Data', name='staticBox3', parent=self, pos=wx.Point(8,
              88), size=wx.Size(800, 456), style=0)

        self.staticText1 = wx.StaticText(id=wxID_DLGREVENUESTATICTEXT1,
              label='Percentage:', name='staticText1', parent=self,
              pos=wx.Point(24, 600), size=wx.Size(59, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGREVENUESTATICTEXT2,
              label='Value:', name='staticText2', parent=self, pos=wx.Point(24,
              576), size=wx.Size(31, 13), style=0)

        self.tbPerc = wx.TextCtrl(id=wxID_DLGREVENUETBPERC, name='tbPerc',
              parent=self, pos=wx.Point(88, 600), size=wx.Size(24, 16), style=0,
              value='5')
        self.tbPerc.Bind(wx.EVT_TEXT, self.OnTbPercText,
              id=wxID_DLGREVENUETBPERC)

        self.staticText3 = wx.StaticText(id=wxID_DLGREVENUESTATICTEXT3,
              label='%', name='staticText3', parent=self, pos=wx.Point(112,
              603), size=wx.Size(11, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_DLGREVENUESTATICTEXT4,
              label='Revenue:', name='staticText4', parent=self,
              pos=wx.Point(24, 624), size=wx.Size(53, 13), style=0)
        self.staticText4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.tRevenue = wx.StaticText(id=wxID_DLGREVENUETREVENUE,
              label='50000 EUR', name='tRevenue', parent=self,
              pos=wx.Point(88, 624), size=wx.Size(60, 13), style=0)
        self.tRevenue.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.grid = wx.grid.Grid(id=wxID_DLGREVENUEGRID, name='grid',
              parent=self, pos=wx.Point(24, 112), size=wx.Size(688, 392),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGridGridCellLeftClick)

        self.btnApply = wx.Button(id=wxID_DLGREVENUEBTNAPPLY,
              label='Apply result as revenue', name='btnApply', parent=self,
              pos=wx.Point(528, 616), size=wx.Size(131, 23), style=0)
        self.btnApply.Bind(wx.EVT_BUTTON, self.OnBtnApplyButton,
              id=wxID_DLGREVENUEBTNAPPLY)

        self.btnCancel = wx.Button(id=wxID_DLGREVENUEBTNCANCEL, label='Cancel',
              name='btnCancel', parent=self, pos=wx.Point(664, 616),
              size=wx.Size(128, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGREVENUEBTNCANCEL)

        self.cbSubcategory = wx.ComboBox(choices=[],
              id=wxID_DLGREVENUECBSUBCATEGORY, name='cbSubcategory',
              parent=self, pos=wx.Point(184, 512), size=wx.Size(208, 21),
              style=0, value='<enter custom description or choose from list>')
        self.cbSubcategory.SetLabel('<enter custom description or choose from list>')

        self.tbInitInvestment = wx.TextCtrl(id=wxID_DLGREVENUETBINITINVESTMENT,
              name='tbInitInvestment', parent=self, pos=wx.Point(392, 512),
              size=wx.Size(100, 21), style=0, value='0')

        self.tbDepPeriod = wx.TextCtrl(id=wxID_DLGREVENUETBDEPPERIOD,
              name='tbDepPeriod', parent=self, pos=wx.Point(496, 512),
              size=wx.Size(100, 21), style=0, value='1')

        self.tbRemPeriod = wx.TextCtrl(id=wxID_DLGREVENUETBREMPERIOD,
              name='tbRemPeriod', parent=self, pos=wx.Point(600, 512),
              size=wx.Size(100, 21), style=0, value='1')

        self.btnAdd = wx.Button(id=wxID_DLGREVENUEBTNADD, label='Add',
              name='btnAdd', parent=self, pos=wx.Point(720, 512),
              size=wx.Size(75, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_DLGREVENUEBTNADD)

        self.btnRemove = wx.Button(id=wxID_DLGREVENUEBTNREMOVE, label='Remove',
              name='btnRemove', parent=self, pos=wx.Point(720, 480),
              size=wx.Size(75, 23), style=0)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.OnBtnRemoveButton,
              id=wxID_DLGREVENUEBTNREMOVE)

        self.cbCategory = wx.Choice(choices=[], id=wxID_DLGREVENUECBCATEGORY,
              name='cbCategory', parent=self, pos=wx.Point(56, 512),
              size=wx.Size(128, 21), style=0)
        self.cbCategory.Bind(wx.EVT_CHOICE, self.OnCbCategoryChoice,
              id=wxID_DLGREVENUECBCATEGORY)

    def __init_custom_ctrls(self, prnt):
        #textcolor--------------------------------------------------------------------
        self.staticBox1.SetForegroundColour(TITLE_COLOR)
        self.staticBox1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.staticBox2.SetForegroundColour(TITLE_COLOR)
        self.staticBox2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.staticBox3.SetForegroundColour(TITLE_COLOR)
        self.staticBox3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        #Grid-------------------------------------------------------------------------
        self.rows = 12
        self.cols = 4
        self.grid.CreateGrid(self.rows,self.cols)

        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(200)
        self.grid.SetColSize(0,335)
        self.grid.SetColSize(1,105)
        self.grid.SetColSize(2,105)
        self.grid.SetColSize(3,100)
      
        
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Description"))
        self.grid.SetColLabelValue(1, _U("Initial investment\n[EUR]"))
        self.grid.SetColLabelValue(2, _U("Depreciation period\n[years]"))
        self.grid.SetColLabelValue(3, _U("Remaining period\n[years]"))
        
        self.updateGridAttributes()
            
        #radio------------------------------------------------------------------------
        self.tbDepPeriod.Enabled = False
        self.tbRemPeriod.Enabled = False
        #choice-----------------------------------------------------------------------
        self.cbCategory.Append(_U("Purchased Equipment"))
        self.cbCategory.Append(_U("Utility Connections"))
        self.cbCategory.Append(_U("Buildings"))
        self.cbCategory.SetSelection(0)
        self.updateSubcategory()
        #text--------------------------------------------------------------------------        
        self.tResult.SetLabel("0 EUR")
        self.tRevenue.SetLabel("0 EUR")
        
    def __init__(self, parent):
        self.mod = Status.mod.moduleTCA
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)        
        self.display()
        self.Calculate()

    def updateGridAttributes(self):
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        for r in range(self.rows):
            self.grid.SetRowSize(r,30)
            self.grid.SetRowAttr(r, attr)


    def display(self):          
        #Update grid------------------------------------------------
        div = len(self.mod.data.revenues) - self.rows
        if (div>0):
            self.rows=len(self.mod.data.revenues)
            self.grid.AppendRows(div) 
            self.updateGridAttributes()
        
        for r in range(0,self.rows):
            for c in range(self.cols):
                self.grid.SetCellValue(r, c, "")
        for r in range(len(self.mod.data.revenues)):
            for c in range(self.cols):
                try:
                    self.grid.SetCellValue(r, c, self.mod.data.revenues[r][c])
                except:
                    self.grid.SetCellValue(r, c, str(self.mod.data.revenues[r][c]))


    def updateSubcategory(self):
        category = self.cbCategory.GetSelection()
        self.cbSubcategory.Clear()
        if (category == 0):
            self.cbSubcategory.Append(_U("process energy generation equipment"))
            self.cbSubcategory.Append(_U("equipment for energy generation and transformation"))
            self.cbSubcategory.Append(_U("equipment for energy recovery"))
            self.cbSubcategory.Append(_U("equipment for cooling/re-cooling/closure of cooling cycles"))
            self.cbSubcategory.Append(_U("air condition for processes"))
            self.cbSubcategory.Append(_U("conduction system for energy transportation"))
            self.cbSubcategory.Append(_U("storage and materials handling equipment"))
            self.cbSubcategory.Append(_U("safety/protective equipment"))
            self.cbSubcategory.Append(_U("monitoring/control equipment"))
            self.cbSubcategory.Append(_U("laboratory/analytical equipment"))
            self.cbSubcategory.SetSelection(0)
        if (category == 1):
            self.cbSubcategory.Append(_U("electricity"))
            self.cbSubcategory.Append(_U("steam"))
            self.cbSubcategory.Append(_U("water"))
            self.cbSubcategory.Append(_U("fuel"))
            self.cbSubcategory.Append(_U("plant air"))
            self.cbSubcategory.Append(_U("inert gas"))
            self.cbSubcategory.Append(_U("refrigeration"))
            self.cbSubcategory.Append(_U("sewerage"))
            self.cbSubcategory.Append(_U("pumping"))
            self.cbSubcategory.SetSelection(0)
                                
    def OnRbInitInvestmentRadiobutton(self, event):
        self.tbDepPeriod.Enabled = False
        self.tbRemPeriod.Enabled = False
        self.Calculate()
        event.Skip()

    def OnRbBookValueRadiobutton(self, event):
        self.tbDepPeriod.Enabled = True
        self.tbRemPeriod.Enabled = True
        self.Calculate()
        event.Skip()

    def Calculate(self):
        try:
            revenue = 0
            perc    = float(self.tbPerc.GetValue())/100.0
                    
            for p in self.mod.data.revenues:
                factor = 1
                if (self.rbBookValue.GetValue() == True):                    
                    factor = float(p[3])/float(p[2])             
                    print factor
                revenue += (p[1]*factor)
                
            self.tResult.SetLabel("%.0f EUR" % revenue)
            self.tRevenue.SetLabel("%.0f EUR" % (revenue*perc))
            self.value = (revenue*perc)
        except:
            self.tResult.SetLabel("ERROR")
            self.tRevenue.SetLabel("ERROR")

    def OnBtnApplyButton(self, event):
        self.apply = True
        self.Destroy()
        event.Skip()

    def OnBtnCancelButton(self, event):
        self.Destroy()
        event.Skip()

    def OnTbPercText(self, event):
        self.Calculate()
        event.Skip()

    def OnCbCategoryChoice(self, event):
        self.updateSubcategory()
        event.Skip()

    def OnBtnAddButton(self, event):
        try:
            category = self.cbCategory.GetStringSelection()
            subcategory = self.cbSubcategory.GetStringSelection()
            name = category + "\n(" + subcategory + ")"
            initinvestment = float(self.tbInitInvestment.GetValue())
            depperiod = int(self.tbDepPeriod.GetValue())
            remperiod = int(self.tbRemPeriod.GetValue())                                    
                      
            if (initinvestment<0)or(depperiod<1)or(remperiod<1):
                raise            
                        
            self.mod.data.revenues.append([name,initinvestment,depperiod,remperiod])                
        except:
            wx.MessageBox("Reconsider values.")
        event.Skip()
        self.Calculate()
        self.display()  
        

    def OnBtnRemoveButton(self, event):
        try:
            if (self.selectedRow < len(self.mod.data.revenues)):
                self.mod.data.revenues.pop(self.selectedRow)
        except:
            pass  
        event.Skip()
        self.Calculate()
        self.display()    

    def OnGridGridCellLeftClick(self, event):
        self.selectedRow = event.GetRow() 
        event.Skip()
