#Boa:FramePanel:PanelTCAInvestment
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    PanelTCAInvestment: Investment and Revenue
#                       (part of the TCA module)
#                        Subdialog: Estimate Revenue
#
#==============================================================================
#
#    Version No.: 0.01
#       Created by:          Florian Joebstl 15/09/2008  
#       Revised by:         Hans Schweiger  28/11/2008  
#
#       Changes to previous version:
#
#   28/11/2008: HS  str() functions eliminated, conversion to unicode !!!
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
from einstein.GUI.dialogTCARevenue import dlgRevenue
from GUITools import *

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

[wxID_PANELTCAINVESTMENT, wxID_PANELTCAINVESTMENTBTNADD, 
 wxID_PANELTCAINVESTMENTBTNDELETE, wxID_PANELTCAINVESTMENTBTNESTIMATE, 
 wxID_PANELTCAINVESTMENTBTNGOMAIN, wxID_PANELTCAINVESTMENTBTNNEXT, 
 wxID_PANELTCAINVESTMENTCBNAME, wxID_PANELTCAINVESTMENTGRID, 
 wxID_PANELTCAINVESTMENTSTATICBOX1, wxID_PANELTCAINVESTMENTSTATICBOX2, 
 wxID_PANELTCAINVESTMENTSTATICBOX3, wxID_PANELTCAINVESTMENTSTATICBOX4, 
 wxID_PANELTCAINVESTMENTSTATICTEXT3, wxID_PANELTCAINVESTMENTSTATICTEXT5, 
 wxID_PANELTCAINVESTMENTSTATICTEXT6, wxID_PANELTCAINVESTMENTSTATICTEXT7, 
 wxID_PANELTCAINVESTMENTSTATICTEXT9, wxID_PANELTCAINVESTMENTTBFUNDINGFIX, 
 wxID_PANELTCAINVESTMENTTBFUNDINGPERC, wxID_PANELTCAINVESTMENTTBINVESTMENT, 
 wxID_PANELTCAINVESTMENTTBREVENUEVALUE, wxID_PANELTCAINVESTMENTTUNIT, 
] = [wx.NewId() for _init_ctrls in range(22)]

class PanelTCAInvestment(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELTCAINVESTMENT, name='',
              parent=prnt, pos=wx.Point(0, 0), size=wx.Size(808, 627),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(800, 600))
        self.Bind(wx.EVT_KILL_FOCUS, self.OnPanelTCAInvestmentKillFocus)

        self.staticBox1 = wx.StaticBox(id=wxID_PANELTCAINVESTMENTSTATICBOX1,
              label=_U('Total investment and fundings of the new equipments'),
              name='staticBox1', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(760, 424), style=0)

        self.grid = wx.grid.Grid(id=wxID_PANELTCAINVESTMENTGRID, name='grid',
              parent=self, pos=wx.Point(24, 32), size=wx.Size(648, 288),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGridGridCellLeftClick)

        self.tbInvestment = wx.TextCtrl(id=wxID_PANELTCAINVESTMENTTBINVESTMENT,
              name='tbInvestment', parent=self, pos=wx.Point(316, 328),
              size=wx.Size(100, 21), style=0, value='0')

        self.tbFundingPerc = wx.TextCtrl(id=wxID_PANELTCAINVESTMENTTBFUNDINGPERC,
              name='tbFundingPerc', parent=self, pos=wx.Point(456, 328),
              size=wx.Size(56, 21), style=0, value='30')

        self.btnAdd = wx.Button(id=wxID_PANELTCAINVESTMENTBTNADD, label=_U('Add'),
              name='btnAdd', parent=self, pos=wx.Point(680, 328),
              size=wx.Size(75, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_PANELTCAINVESTMENTBTNADD)

        self.btnDelete = wx.Button(id=wxID_PANELTCAINVESTMENTBTNDELETE,
              label=_U('Remove'), name='btnDelete', parent=self, pos=wx.Point(680,
              296), size=wx.Size(75, 23), style=0)
        self.btnDelete.Bind(wx.EVT_BUTTON, self.OnBtnDeleteButton,
              id=wxID_PANELTCAINVESTMENTBTNDELETE)

        self.cbName = wx.ComboBox(choices=[], id=wxID_PANELTCAINVESTMENTCBNAME,
              name='cbName', parent=self, pos=wx.Point(56, 328),
              size=wx.Size(256, 21), style=0,
              value=_U('<enter custom description or choose from list>'))

        self.staticText3 = wx.StaticText(id=wxID_PANELTCAINVESTMENTSTATICTEXT3,
              label=_U('The values of investment are suggested by the program.(The default funding for equipment is 30%) \nIf this do not apply to your process, please indicate your own values'),
              name='staticText3', parent=self, pos=wx.Point(40, 384),
              size=wx.Size(335, 26), style=0)
        self.staticText3.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))

        self.tbFundingFix = wx.TextCtrl(id=wxID_PANELTCAINVESTMENTTBFUNDINGFIX,
              name='tbFundingFix', parent=self, pos=wx.Point(536, 328),
              size=wx.Size(96, 21), style=0, value='0')

        self.staticText5 = wx.StaticText(id=wxID_PANELTCAINVESTMENTSTATICTEXT5,
              label=_U('EUR'), name='staticText5', parent=self, pos=wx.Point(424,
              328), size=wx.Size(20, 13), style=0)

        self.staticText6 = wx.StaticText(id=wxID_PANELTCAINVESTMENTSTATICTEXT6,
              label='%', name='staticText6', parent=self, pos=wx.Point(515,
              328), size=wx.Size(11, 13), style=0)

        self.staticText7 = wx.StaticText(id=wxID_PANELTCAINVESTMENTSTATICTEXT7,
              label=_U('EUR'), name='staticText7', parent=self, pos=wx.Point(640,
              328), size=wx.Size(20, 13), style=0)

        self.staticText9 = wx.StaticText(id=wxID_PANELTCAINVESTMENTSTATICTEXT9,
              label=_U('If you think there would be revenue from sale of replaced equipments, please indicate the possible value'),
              name='staticText9', parent=self, pos=wx.Point(40, 518),
              size=wx.Size(502, 13), style=0)
        self.staticText9.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))

        self.tbRevenueValue = wx.TextCtrl(id=wxID_PANELTCAINVESTMENTTBREVENUEVALUE,
              name='tbRevenueValue', parent=self, pos=wx.Point(32, 464),
              size=wx.Size(136, 21), style=0, value='0')
        self.tbRevenueValue.Bind(wx.EVT_KILL_FOCUS,
              self.OnTbRevenueValueKillFocus)
        self.tbRevenueValue.Bind(wx.EVT_TEXT, self.OnTbRevenueValueText,
              id=wxID_PANELTCAINVESTMENTTBREVENUEVALUE)

        self.btnEstimate = wx.Button(id=wxID_PANELTCAINVESTMENTBTNESTIMATE,
              label=_U('Estimate the renenue...'), name='btnEstimate',
              parent=self, pos=wx.Point(600, 464), size=wx.Size(152, 23),
              style=0)
        self.btnEstimate.Bind(wx.EVT_BUTTON, self.OnBtnEstimateButton,
              id=wxID_PANELTCAINVESTMENTBTNESTIMATE)

        self.tUnit = wx.StaticText(id=wxID_PANELTCAINVESTMENTTUNIT,
              label=_U('EUR'), name='tUnit', parent=self, pos=wx.Point(178, 468),
              size=wx.Size(20, 13), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELTCAINVESTMENTSTATICBOX2,
              label=_U('Help'), name='staticBox2', parent=self, pos=wx.Point(24,
              360), size=wx.Size(728, 64), style=0)

        self.btnGoMain = wx.Button(id=wxID_PANELTCAINVESTMENTBTNGOMAIN,
              label=_U('Save and go to the main page'), name='btnGoMain',
              parent=self, pos=wx.Point(8, 560), size=wx.Size(192, 23),
              style=0)
        self.btnGoMain.Bind(wx.EVT_BUTTON, self.OnBtnGoMainButton,
              id=wxID_PANELTCAINVESTMENTBTNGOMAIN)

        self.staticBox3 = wx.StaticBox(id=wxID_PANELTCAINVESTMENTSTATICBOX3,
              label=_U('Revenue from sale of replaced equipments'),
              name='staticBox3', parent=self, pos=wx.Point(8, 440),
              size=wx.Size(760, 112), style=0)

        self.staticBox4 = wx.StaticBox(id=wxID_PANELTCAINVESTMENTSTATICBOX4,
              label=_U('Help'), name='staticBox4', parent=self, pos=wx.Point(24,
              496), size=wx.Size(728, 48), style=0)

        self.btnNext = wx.Button(id=wxID_PANELTCAINVESTMENTBTNNEXT,
              label=_U('Save an go to the next page >>>'), name='btnNext',
              parent=self, pos=wx.Point(576, 560), size=wx.Size(192, 23),
              style=0)
        self.btnNext.Bind(wx.EVT_BUTTON, self.OnBtnNextButton,
              id=wxID_PANELTCAINVESTMENTBTNNEXT)

    def __init_custom_ctrls(self, prnt):
        #textcolor--------------------------------------------------------------------
        self.staticBox1.SetForegroundColour(TITLE_COLOR)
        self.staticBox1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        self.staticBox3.SetForegroundColour(TITLE_COLOR)
        self.staticBox3.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        #choice-----------------------------------------------------------------------
        self.cbName.Append(_U("H&C Storage"))
        self.cbName.Append(_U("CHP"))
        self.cbName.Append(_U("Solar thermal"))
        self.cbName.Append(_U("Heat pump"))
        self.cbName.Append(_U("Biomass"))
        self.cbName.Append(_U("Chillers"))
        self.cbName.Append(_U("Boilers"))
        self.cbName.Append(_U("HX network"))
        self.cbName.Append(_U("H&C distribution"))
        #Grid-------------------------------------------------------------------------
        self.rows = 12
        self.cols = 4
      
        self.grid.CreateGrid(self.rows,self.cols)

        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(200)
        self.grid.SetColSize(0,260)
        self.grid.SetColSize(1,135)
        self.grid.SetColSize(2,80)
        self.grid.SetColSize(3,120)
        
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Description"))
        self.grid.SetColLabelValue(1, _U("Investment\nEUR"))
        self.grid.SetColLabelValue(2, _U("Funding\n%"))
        self.grid.SetColLabelValue(3, _U("Additional\nfixed sum"))
        
        self.updateGridAttributes()
        #self.grid.SetBackgroundColor("black")
        #Revenue----------------------------------------------------------
        
        
    def updateGridAttributes(self):
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        for r in range(self.rows):
            self.grid.SetRowSize(r,20)
            self.grid.SetRowAttr(r, attr)
        
    def __init__(self, parent, main, id, pos, size, style, name):
        #print "Init Investment"      
        self.main = main
        self.mod = Status.mod.moduleTCA
        self.shortName = _U("TCAInvestment")
        self.description = _U("")
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)
        self.selectedRow = None
        #self.display()              
    
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
        if (Status.ANo == 0):            
            wx.MessageBox("There are no investments to enter for the current process. \n Please proceed with Energy and Operating costs")                                   
            self.main.tree.SelectItem(self.main.qECO2, select=True)            
        else:          
            if not(self.updatePanel()):
                return  
            #Revenue-----------------------------------------------------
            self.tbRevenueValue.SetValue(str(self.mod.data.revenue))                    
            #Update grid------------------------------------------------
            div = len(self.mod.data.investment) - self.rows
            if (div>0):
                self.rows=len(self.mod.data.investment)
                self.grid.AppendRows(div) 
                self.updateGridAttributes()  
            for r in range(0,self.rows):
                for c in range(self.cols):
                    self.grid.SetCellValue(r, c, "")
            for r in range(len(self.mod.data.investment)):
                for c in range(self.cols):
                    try:    #if it's already a unicode string, don't convert to string
                        self.grid.SetCellValue(r, c, self.mod.data.investment[r][c])
                    except:
                        self.grid.SetCellValue(r, c, str(self.mod.data.investment[r][c]))
                    
 
    def OnBtnAddButton(self, event):
        try:
            name = self.cbName.GetValue()
            investment  = float(self.tbInvestment.GetValue())
            fundingperc = float(self.tbFundingPerc.GetValue())
            fundingfix  = float(self.tbFundingFix.GetValue())
           
            if (investment<0)or(fundingperc<0)or(fundingperc>100)or(fundingfix<0):
                raise            
                          
            try:                    
                if (self.selectedRow < len(self.mod.data.investment)):
                    self.mod.data.investment[self.selectedRow] = [name,investment,fundingperc,fundingfix]
                else:           
                    self.mod.data.investment.append([name,investment,fundingperc,fundingfix])                 
            except:
                 self.mod.data.investment.append([name,investment,fundingperc,fundingfix])          
                                    
        except:
            wx.MessageBox(_U("Reconsider values."))
            
        event.Skip()
        self.display()  

    def OnBtnDeleteButton(self, event):
        if (self.selectedRow < len(self.mod.data.investment)):
            self.mod.data.investment.pop(self.selectedRow)  
        event.Skip()
        self.display()    

    def OnGridGridCellLeftClick(self, event):
        self.selectedRow = event.GetRow()  
        if (self.selectedRow < len(self.mod.data.investment)):
            entry = self.mod.data.investment[self.selectedRow]
            
            self.cbName.SetValue(entry[0])
            self.tbInvestment.SetValue(str(entry[1]))
            self.tbFundingPerc.SetValue(str(entry[2]))
            self.tbFundingFix.SetValue(str(entry[3]))            
            self.btnAdd.SetLabel("Change")
        else:
            self.btnAdd.SetLabel("Add")
        event.Skip()          

    def OnPanelTCAInvestmentKillFocus(self, event):
        #print "leave focus"
        event.Skip()
  
    def OnTbRevenueValueKillFocus(self, event):
        try:        
            value = float(self.tbRevenueValue.GetValue())
            if (value<0):
                raise
            self.mod.data.revenue = value                                      
        except:
            wx.MessageBox(_U("Numeric value greater or equal zero expected."))
                                     
        event.Skip()

    def OnBtnEstimateButton(self, event):
        try:
            dlg = dlgRevenue(None)
            dlg.ShowModal()
            if (dlg.apply):
                self.tbRevenueValue.SetValue("%.0f" % dlg.value)
                self.mod.data.revenue = dlg.value
        except:
            pass
        event.Skip()

    def OnTbRevenueValueText(self, event):
        try:        
            value = float(self.tbRevenueValue.GetValue())
            if (value<0):
                raise
            self.mod.data.revenue = value                                      
        except:
            self.mod.data.revenue = 0                                     
        event.Skip()

    def OnBtnGoMainButton(self, event):
        self.Hide()
        self.mod.storeData()
        self.main.tree.SelectItem(self.main.qECO, select=True)
        event.Skip()        

    def OnBtnNextButton(self, event):
        self.Hide()
        self.mod.storeData()
        self.main.tree.SelectItem(self.main.qECO2, select=True)
        event.Skip()
