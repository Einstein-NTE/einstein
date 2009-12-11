#Boa:FramePanel:PanelTCAEnergy
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    PanelTCAEnergy: Energy and Operating cost
#                    (part of the TCA module)
#                    Subdialog: Detailed Operating Cost
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
from einstein.GUI.status import Status
from GUITools import *
from einstein.GUI.dialogTCADetailedOpCost import dlgOpcost

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

[wxID_PANELTCAENERGY, wxID_PANELTCAENERGYBTNADD, wxID_PANELTCAENERGYBTNDELETE, 
 wxID_PANELTCAENERGYBTNDETAILEDOPCOST, wxID_PANELTCAENERGYBTNGOMAIN, 
 wxID_PANELTCAENERGYBTNNEXT, wxID_PANELTCAENERGYCOMBOBOX1, 
 wxID_PANELTCAENERGYGRID, wxID_PANELTCAENERGYSTATICBOX1, 
 wxID_PANELTCAENERGYSTATICBOX2, wxID_PANELTCAENERGYSTATICBOX3, 
 wxID_PANELTCAENERGYSTATICBOX4, wxID_PANELTCAENERGYSTATICTEXT7, 
 wxID_PANELTCAENERGYSTATICTEXT8, wxID_PANELTCAENERGYTBDEMAND, 
 wxID_PANELTCAENERGYTBDEVELOPMENT, wxID_PANELTCAENERGYTBPRICE, 
 wxID_PANELTCAENERGYTBTOTALOPCOST, wxID_PANELTCAENERGYTENERGYHELP, 
 wxID_PANELTCAENERGYTOPCOSTHEP, 
] = [wx.NewId() for _init_ctrls in range(20)]

class PanelTCAEnergy(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELTCAENERGY, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(760, 617),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(752, 590))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELTCAENERGYSTATICBOX1,
              label=_U('Energy cost'), name='staticBox1', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(728, 392), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_PANELTCAENERGYSTATICBOX2,
              label=_U('Operating and maintenance cost'), name='staticBox2',
              parent=self, pos=wx.Point(8, 408), size=wx.Size(728, 144),
              style=0)

        self.grid = wx.grid.Grid(id=wxID_PANELTCAENERGYGRID, name='grid',
              parent=self, pos=wx.Point(24, 32), size=wx.Size(616, 248),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGrid1GridCellLeftClick)

        self.comboBox1 = wx.ComboBox(choices=[],
              id=wxID_PANELTCAENERGYCOMBOBOX1, name='comboBox1', parent=self,
              pos=wx.Point(40, 288), size=wx.Size(272, 21), style=0,
              value=_U('<Enter custom description or choose from list>'))

        self.tbDemand = wx.TextCtrl(id=wxID_PANELTCAENERGYTBDEMAND,
              name='tbDemand', parent=self, pos=wx.Point(320, 288),
              size=wx.Size(100, 21), style=0, value='0')

        self.tbPrice = wx.TextCtrl(id=wxID_PANELTCAENERGYTBPRICE,
              name='tbPrice', parent=self, pos=wx.Point(424, 288),
              size=wx.Size(100, 21), style=0, value='0')

        self.tbDevelopment = wx.TextCtrl(id=wxID_PANELTCAENERGYTBDEVELOPMENT,
              name='tbDevelopment', parent=self, pos=wx.Point(528, 288),
              size=wx.Size(100, 21), style=0, value='0')

        self.btnDelete = wx.Button(id=wxID_PANELTCAENERGYBTNDELETE,
              label=_U('Remove'), name='btnDelete', parent=self, pos=wx.Point(648,
              256), size=wx.Size(75, 23), style=0)
        self.btnDelete.Bind(wx.EVT_BUTTON, self.OnBtnDeleteButton,
              id=wxID_PANELTCAENERGYBTNDELETE)

        self.btnAdd = wx.Button(id=wxID_PANELTCAENERGYBTNADD, label=_U('Add'),
              name='btnAdd', parent=self, pos=wx.Point(648, 288),
              size=wx.Size(75, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_PANELTCAENERGYBTNADD)

        self.staticBox3 = wx.StaticBox(id=wxID_PANELTCAENERGYSTATICBOX3,
              label=_U('Help'), name='staticBox3', parent=self, pos=wx.Point(24,
              328), size=wx.Size(696, 64), style=0)

        self.tEnergyHelp = wx.StaticText(id=wxID_PANELTCAENERGYTENERGYHELP,
              label=_U('The values come from the audit questionnaire\nIf you would like to make any changes, please edit them'),
              name='tEnergyHelp', parent=self, pos=wx.Point(40, 352),
              size=wx.Size(270, 26), style=0)
        self.tEnergyHelp.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))

        self.staticBox4 = wx.StaticBox(id=wxID_PANELTCAENERGYSTATICBOX4,
              label=_U('Help'), name='staticBox4', parent=self, pos=wx.Point(24,
              480), size=wx.Size(696, 64), style=0)

        self.tbTotalOpCost = wx.TextCtrl(id=wxID_PANELTCAENERGYTBTOTALOPCOST,
              name='tbTotalOpCost', parent=self, pos=wx.Point(136, 440),
              size=wx.Size(152, 21), style=0, value='0')
        self.tbTotalOpCost.Bind(wx.EVT_TEXT, self.OnTbTotalOpCostText,
              id=wxID_PANELTCAENERGYTBTOTALOPCOST)
        self.tbTotalOpCost.Bind(wx.EVT_KILL_FOCUS,
              self.OnTbTotalOpCostKillFocus)

        self.staticText7 = wx.StaticText(id=wxID_PANELTCAENERGYSTATICTEXT7,
              label=_U('Total operating and\nmaintenance cost'),
              name='staticText7', parent=self, pos=wx.Point(32, 440),
              size=wx.Size(94, 26), style=0)

        self.staticText8 = wx.StaticText(id=wxID_PANELTCAENERGYSTATICTEXT8,
              label=_U('EUR/a'), name='staticText8', parent=self, pos=wx.Point(296,
              443), size=wx.Size(30, 13), style=0)

        self.btnDetailedOpCost = wx.Button(id=wxID_PANELTCAENERGYBTNDETAILEDOPCOST,
              label=_U('Detailed operating cost calculation...'),
              name='btnDetailedOpCost', parent=self, pos=wx.Point(528, 440),
              size=wx.Size(192, 23), style=0)
        self.btnDetailedOpCost.Bind(wx.EVT_BUTTON,
              self.OnBtnDetailedOpCostButton,
              id=wxID_PANELTCAENERGYBTNDETAILEDOPCOST)

        self.tOpcostHep = wx.StaticText(id=wxID_PANELTCAENERGYTOPCOSTHEP,
              label=_U('The value is the total of the operating and maintenance costs given in the questionaire. If you would like \nto change this value, please go back to the questionnaire module'),
              name='tOpcostHep', parent=self, pos=wx.Point(40, 504),
              size=wx.Size(504, 26), style=0)
        self.tOpcostHep.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))

        self.btnNext = wx.Button(id=wxID_PANELTCAENERGYBTNNEXT,
              label=_U('Save and go to next page >>>'), name='btnNext',
              parent=self, pos=wx.Point(544, 560), size=wx.Size(192, 23),
              style=0)
        self.btnNext.Bind(wx.EVT_BUTTON, self.OnBtnNextButton,
              id=wxID_PANELTCAENERGYBTNNEXT)

        self.btnGoMain = wx.Button(id=wxID_PANELTCAENERGYBTNGOMAIN,
              label=_U('Save and go back to main page'), name='btnGoMain',
              parent=self, pos=wx.Point(8, 560), size=wx.Size(192, 23),
              style=0)
        self.btnGoMain.Bind(wx.EVT_BUTTON, self.OnBtnGoMainButton,
              id=wxID_PANELTCAENERGYBTNGOMAIN)

    def __init_custom_ctrls(self, prnt):
        self.staticBox1.SetForegroundColour(TITLE_COLOR)
        self.staticBox1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        self.staticBox2.SetForegroundColour(TITLE_COLOR)
        self.staticBox2.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))
        
        #Grid-------------------------------------------------------------------------
        self.rows = 10
        self.cols = 4
      
        self.grid.CreateGrid(self.rows,self.cols)

        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(200)
        self.grid.SetColSize(0,260)
        self.grid.SetColSize(1,105)
        self.grid.SetColSize(2,105)
        self.grid.SetColSize(3,100)
        
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Description"))
        self.grid.SetColLabelValue(1, _U("Energy demand\n[kWh/a]"))
        self.grid.SetColLabelValue(2, _U("Energy price\n[EUR/kWh]"))
        self.grid.SetColLabelValue(3, _U("Development of \nenergy price [%/a]"))
        #choices--------------------------------------------------------------------------------
        self.comboBox1.Append(_U("Electicity"))
        self.comboBox1.Append(_U("Natural Gas"))
        self.comboBox1.Append(_U("Liquid Petroleum gas"))
        self.comboBox1.Append(_U("Heavy fuel oil"))
        self.comboBox1.Append(_U("Butane"))
        self.comboBox1.Append(_U("Propane"))
        self.comboBox1.Append(_U("Gas oil"))

        self.updateGridAttributes()
        
        self.tbDevelopment.Enabled = False
        self.tbTotalOpCost.Enabled = False
            
        #Helptext & DetailedButton
        self.btnDetailedOpCost.Enabled = False
        if (Status.ANo > 0):
            self.tEnergyHelp.SetLabel(_U("The values come from the audit questionnaire and Einstein database.\nIf you would like to make any change on them, please edit the values."))
            self.tOpcostHep.SetLabel(_U("If you would like to calculate the operating costs in details, please choose \"Detailed operating cost calculation\""))
            self.btnDetailedOpCost.Enabled = True

    def __init__(self, parent, main, id, pos, size, style, name):
        #print "Init Energy"      
        self.main = main
        self.mod = Status.mod.moduleTCA
        self.shortName = _U("TCAEnergy")
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
        div = len(self.mod.data.energycosts) - self.rows
        if (div>0):
            self.rows=len(self.mod.data.energycosts)
            self.grid.AppendRows(div) 
            self.updateGridAttributes()  
        for r in range(0,self.rows):
            for c in range(self.cols):
                self.grid.SetCellValue(r, c, "")
        for r in range(len(self.mod.data.energycosts)):
            for c in range(self.cols):
                try:
                    self.grid.SetCellValue(r, c, self.mod.data.energycosts[r][c])
                except:
                    self.grid.SetCellValue(r, c, str(self.mod.data.energycosts[r][c]))
                #FIXXXX this should be removed when tca can handle different
                #development of energy price!
                if c==3: 
                    self.grid.SetCellValue(r, c, str(self.mod.data.DEP))
                #ENDFIX


        #Update opcost
        self.mod.calculateTotalOpCostFromDetailedOpcost()
        opcost = "%.0f" % self.mod.data.totalopcost
        self.tbTotalOpCost.SetValue(opcost)
    
    def OnGrid1GridCellLeftClick(self, event):
        self.selectedRow = event.GetRow()  
        if (self.selectedRow < len(self.mod.data.energycosts)):
            entry = self.mod.data.energycosts[self.selectedRow]
            self.comboBox1.SetValue(entry[0])
            self.tbDemand.SetValue(str(entry[1]))
            self.tbPrice.SetValue(str(entry[2]))
            self.tbDevelopment.SetValue(str(entry[3]))
            self.btnAdd.SetLabel("Change")
        else:
            self.btnAdd.SetLabel("Add")
        event.Skip()  
                
    def OnBtnDeleteButton(self, event):
        try:
            if (self.selectedRow < len(self.mod.data.energycosts)):
                self.mod.data.energycosts.pop(self.selectedRow)
        except:
            pass  
        event.Skip()
        self.display()

    def OnBtnAddButton(self, event):
        try:
            name   = self.comboBox1.GetValue()
            demand = float(self.tbDemand.GetValue())
            price  = float(self.tbPrice.GetValue())
            dev    = float(self.tbDevelopment.GetValue())
           
            if (demand<0)or(price<0):
                raise           
            try:                    
                if (self.selectedRow < len(self.mod.data.energycosts)):
                    self.mod.data.energycosts[self.selectedRow] = [name,demand,price,dev]
                else:           
                    self.mod.data.energycosts.append([name,demand,price,dev])                
            except:
                self.mod.data.energycosts.append([name,demand,price,dev])
        except:
            wx.MessageBox(_U("Reconsider values."))
                
        event.Skip()
        self.display()  

    def OnBtnDetailedOpCostButton(self, event):
        try:
            dlg = dlgOpcost(None)
            dlg.ShowModal()
            if (dlg.save == True):
                dlg.store_data()
                self.mod.calculateTotalOpCostFromDetailedOpcost()
                self.display()              
        except:
            pass
        
        event.Skip()

    def OnTbTotalOpCostText(self, event):
        try:
            opcost = float(self.tbTotalOpCost.GetValue())
            self.mod.data.totalopcost = opcost
        except:
            self.mod.data.totalopcost = 0
        event.Skip()

    def OnTbTotalOpCostKillFocus(self, event):
        event.Skip()

    def OnBtnNextButton(self, event):
        self.Hide()
        self.mod.storeData()
        self.main.tree.SelectItem(self.main.qECO3, select=True)
        event.Skip()        

    def OnBtnGoMainButton(self, event):
        self.Hide()
        self.mod.storeData()
        self.main.tree.SelectItem(self.main.qECO, select=True)
        event.Skip()        
