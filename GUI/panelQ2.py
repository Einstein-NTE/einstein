import wx
import wx.grid
import pSQL
import HelperClass
from status import Status


class PanelQ2(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ2', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)


        #self.tc1 = wx.TextCtrl(id=-1, name='tc1', parent=self.,
        #      pos=wx.Point(248, 64), size=wx.Size(200, 21), style=0, value='')

        self.st1 = wx.StaticText(id=-1, label=self.PList["0401"][1], name='st1', parent=self, pos=wx.Point(248, 48), style=0)
        self.choiceOfDBFuelType = wx.Choice(choices=[],
              id=-1, name='choiceOfDBFuelType', parent=self, pos=wx.Point(248, 64),
              size=wx.Size(200, 21), style=0)

        self.st2 = wx.StaticText(id=-1, label=self.PList["0402"][1], name='st2', parent=self, pos=wx.Point(248, 88), style=0)

        self.tc2 = wx.TextCtrl(id=-1, name='tc2', parent=self,
              pos=wx.Point(248, 104), size=wx.Size(200, 21), style=0, value='')

        self.st3 = wx.StaticText(id=-1, label=self.PList["0403"][2], name='st3', parent=self, pos=wx.Point(248, 128), style=0)

        self.tc3 = wx.TextCtrl(id=-1, name='tc3', parent=self,
              pos=wx.Point(248, 144), size=wx.Size(200, 21), style=0, value='')

        self.st4 = wx.StaticText(id=-1, label=self.PList["0404"][2], name='st4', parent=self, pos=wx.Point(472, 48), style=0)

        self.tc4 = wx.TextCtrl(id=-1, name='tc4', parent=self,
              pos=wx.Point(472, 64), size=wx.Size(200, 21), style=0, value='')

        self.st5 = wx.StaticText(id=-1, label=self.PList["0405"][1] + " " + self.PList["0405"][2], name='st5', parent=self, pos=wx.Point(472, 88), style=0)

        self.tc5 = wx.TextCtrl(id=-1, name='tc5', parent=self,
              pos=wx.Point(472, 104), size=wx.Size(200, 21), style=0, value='')

        self.st6 = wx.StaticText(id=-1, label=self.PList["0406"][1] + " " + self.PList["0406"][2], name='st6', parent=self, pos=wx.Point(472, 128), style=0)

        self.tc6 = wx.TextCtrl(id=-1, name='tc6', parent=self,
              pos=wx.Point(472, 144), size=wx.Size(200, 21), style=0, value='')

        self.stInfo1 = wx.StaticText(id=-1, label=self.PList["X029"][1], name='stInfo1', parent=self, pos=wx.Point(32, 24), style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.fuelListBox = wx.ListBox(choices=[], id=-1, name='fuelListBox',
              parent=self, pos=wx.Point(32, 64), size=wx.Size(160, 112),
              style=0)
        self.Bind(wx.EVT_LISTBOX, self.OnFuelListBoxClick, self.fuelListBox)

        self.stInfo2 = wx.StaticText(id=-1, label=self.PList["X030"][1], name='stInfo2', parent=self, pos=wx.Point(32, 48), style=0)
        self.stInfo2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.buttonAddFuel = wx.Button(id=-1, label=self.PList["X031"][1],
              name='buttonAddFuel', parent=self, pos=wx.Point(592,
              176), size=wx.Size(192, 32), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddFuel, self.buttonAddFuel)


        self.buttonRemoveFuelFromList = wx.Button(id=-1,
              label=self.PList["X032"][1], name='buttonRemoveFuelFromList',
              parent=self, pos=wx.Point(88, 184), size=wx.Size(192, 32),
              style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonRemoveFuelFromList, self.buttonRemoveFuelFromList)

        #self.scrolledWindow = wx.ScrolledWindow(id=-1,
        #      name='scrolledWindow', parent=self, pos=wx.Point(0,
        #      268), size=wx.Size(790, 260), style=wx.HSCROLL)
        #self.scrolledWindow.SetScrollbars(1,1, 950,240)

        self.buttonStore = wx.Button(id=-1, label=self.PList["X019"][1],
              name='buttonStore', parent=self, pos=wx.Point(696,
              560), size=wx.Size(192, 32), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonStore, self.buttonStore)


        self.stInfo3 = wx.StaticText(id=-1, label=self.PList["X033"][1], name='stInfo3', parent=self, pos=wx.Point(32, 240), style=0)
        self.stInfo3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.buttonClear = wx.Button(id=-1, label=self.PList["X028"][1],
              name='buttonClear', parent=self, pos=wx.Point(248,
              176), size=wx.Size(192, 32), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClear, self.buttonClear)



        ###-- grid setup
        self.grid = wx.grid.Grid(id=-1,
				 name='grid',
				 parent=self,
				 pos=wx.Point(0, 268),
				 size=wx.Size(940, 240),
				 style=0)
        
        self.grid.EnableGridLines(True)
        self.grid.CreateGrid(9, 6)

        self.grid.SetDefaultColSize(120, resizeExistingCols=False)
        self.grid.SetDefaultRowSize(23, resizeExistingRows=False)

        self.grid.SetRowLabelSize(220)
        
        
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour("light gray")
        attr.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid.SetAttr(7, 0, attr)
        self.grid.SetAttr(7, 1, attr)
        self.grid.SetAttr(7, 2, attr)
        self.grid.SetAttr(7, 3, attr)
        self.grid.SetAttr(7, 4, attr)
        self.grid.SetAttr(7, 5, attr)
        

        attr2 = wx.grid.GridCellAttr()
        attr2.SetBackgroundColour("light gray")
        attr2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid.SetAttr(6, 0, attr2)
        self.grid.SetAttr(6, 3, attr2)

        

        attr3 = wx.grid.GridCellAttr()
        attr3.SetBackgroundColour("light gray")
        attr3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid.SetAttr(2, 4, attr3)


        attr4 = wx.grid.GridCellAttr()
        attr4.SetBackgroundColour("light gray")
        attr4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid.SetAttr(1, 4, attr4)
        
        
        
        self.grid.SetColLabelValue(0,self.PList["X043"][1])
        self.grid.SetColLabelValue(1,self.PList["X044"][1])
        self.grid.SetColLabelValue(2,self.PList["X045"][1])
        self.grid.SetColLabelValue(3,self.PList["X046"][1])
        self.grid.SetColLabelValue(4,self.PList["X047"][1])
        self.grid.SetColLabelValue(5,self.PList["X048"][1])

        self.grid.SetRowLabelValue(0,self.PList["X034"][1])
        self.grid.SetRowLabelValue(1,self.PList["X035"][1])
        self.grid.SetRowLabelValue(2,self.PList["X036"][1])
        self.grid.SetRowLabelValue(3,self.PList["X037"][1])
        self.grid.SetRowLabelValue(4,self.PList["X038"][1])
        self.grid.SetRowLabelValue(5,self.PList["X039"][1])
        self.grid.SetRowLabelValue(6,self.PList["X040"][1])
        self.grid.SetRowLabelValue(7,self.PList["X041"][1])
        self.grid.SetRowLabelValue(8,self.PList["X042"][1])

        self.grid.SetRowLabelAlignment(wx.LEFT, wx.BOTTOM)

        self.grid.SetCellSize(6, 0, 1, 3)
        self.grid.SetCellSize(6, 3, 1, 3)
        self.grid.SetCellSize(1, 4, 1, 2)
        self.grid.SetCellSize(2, 4, 4, 1)



        self.grid.SetCellValue(6, 0, self.PList["X049"][1])
        self.grid.SetCellValue(6, 3, self.PList["X050"][1])
        self.grid.SetCellValue(7, 0, self.PList["X051"][1])
        self.grid.SetCellValue(7, 1, self.PList["X052"][1])
        self.grid.SetCellValue(7, 2, self.PList["X053"][1])
        self.grid.SetCellValue(7, 3, self.PList["X054"][1])
        self.grid.SetCellValue(7, 4, self.PList["X055"][1])
        self.grid.SetCellValue(7, 5, self.PList["X056"][1])

        self.grid.SetReadOnly(6, 0, isReadOnly=True)
        self.grid.SetReadOnly(6, 3, isReadOnly=True)
        self.grid.SetReadOnly(7, 0, isReadOnly=True)
        self.grid.SetReadOnly(7, 1, isReadOnly=True)
        self.grid.SetReadOnly(7, 2, isReadOnly=True)
        self.grid.SetReadOnly(7, 3, isReadOnly=True)
        self.grid.SetReadOnly(7, 4, isReadOnly=True)
        self.grid.SetReadOnly(7, 5, isReadOnly=True)
        self.grid.SetReadOnly(1, 4, isReadOnly=True)
        self.grid.SetReadOnly(2, 4, isReadOnly=True)
        
        self.grid.SetCellAlignment(7, 0, wx.ALIGN_CENTRE, wx.ALIGN_BOTTOM)
        self.grid.SetCellAlignment(6, 0, wx.ALIGN_CENTRE, wx.ALIGN_BOTTOM)

        ###-- end of grid setup


#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		

    def OnButtonAddFuel(self, event):
        if self.main.activeQid <> 0 and self.choiceOfDBFuelType.GetStringSelection <> 'None':
            
            if len(Status.DB.qfuel.Questionnaire_id[self.main.activeQid].DBFuel_id[Status.DB.dbfuel.FuelName[str(self.choiceOfDBFuelType.GetStringSelection())][0].DBFuel_ID]) == 0:
                dbfid = Status.DB.dbfuel.FuelName[str(self.choiceOfDBFuelType.GetStringSelection())][0].DBFuel_ID
                print "INSERT"
                tmp = {
                    "Questionnaire_id":self.main.activeQid,
                    "FuelUnit":self.check(self.tc2.GetValue()),
                    "DBFuel_id":dbfid,
                    "MFuelYear":self.check(self.tc3.GetValue()), 
                    "FuelOwn":self.check(self.tc4.GetValue()),
                    "FuelTariff":self.check(self.tc5.GetValue()),
                    "FuelCostYear":self.check(self.tc6.GetValue())                   
                    }
                
                Status.DB.qfuel.insert(tmp)               
                Status.SQL.commit()
                self.fillFuelList()


            elif len(Status.DB.qfuel.Questionnaire_id[self.main.activeQid].DBFuel_id[Status.DB.dbfuel.FuelName[str(self.choiceOfDBFuelType.GetStringSelection())][0].DBFuel_ID]) == 1:
                dbfid = Status.DB.dbfuel.FuelName[str(self.choiceOfDBFuelType.GetStringSelection())][0].DBFuel_ID
                print "UPDATE"
                tmp = {
                    "FuelUnit":self.check(self.tc2.GetValue()),
                    "DBFuel_id":dbfid,
                    "MFuelYear":self.check(self.tc3.GetValue()), 
                    "FuelOwn":self.check(self.tc4.GetValue()),
                    "FuelTariff":self.check(self.tc5.GetValue()),
                    "FuelCostYear":self.check(self.tc6.GetValue())
                    }
                
                q = Status.DB.qfuel.DBFuel_id[dbfid].Questionnaire_id[self.main.activeQid][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillFuelList()
                          
            else:
                self.showError("FuelName have to be an uniqe value!")


    def OnButtonRemoveFuelFromList(self, event):
        event.Skip()


    def OnButtonStore(self, event):
        if self.main.activeQid <> 0:
            if len(Status.DB.qelectricity.Questionnaire_id[self.main.activeQid]) == 0:
                tmp = {
                    "Questionnaire_id":self.main.activeQid,
                    "PowerContrTot":self.check(self.grid.GetCellValue(1, 3)),
                    "PowerContrStd":self.check(self.grid.GetCellValue(1, 1)),
                    "PowerContrPeak":self.check(self.grid.GetCellValue(1, 0)),
                    "PowerContrVall":self.check(self.grid.GetCellValue(1, 2)),
                    "ElectricityTotYear":self.check(self.grid.GetCellValue(0, 3)),
                    "ElectricityPeakYear":self.check(self.grid.GetCellValue(0, 0)),
                    "ElectricityStandYear":self.check(self.grid.GetCellValue(0, 1)),
                    "ElectricityValleyYear":self.check(self.grid.GetCellValue(0, 2)),
                    "ElGenera":self.check(self.grid.GetCellValue(0, 4)),
                    "ElSales":self.check(self.grid.GetCellValue(0, 5)),
                    "ElectricityRef":self.check(self.grid.GetCellValue(8, 0)),
                    "ElectricityAC":self.check(self.grid.GetCellValue(8, 1)),
                    "ElectricityThOther":self.check(self.grid.GetCellValue(8, 2)),
                    "ElectricityMotors":self.check(self.grid.GetCellValue(8, 3)),
                    "ElectricityChem":self.check(self.grid.GetCellValue(8, 4)),
                    "ElectricityLight":self.check(self.grid.GetCellValue(8, 5)),
                    "ElTariffClassTot":self.check(self.grid.GetCellValue(2, 3)),
                    "ElTariffClassStd":self.check(self.grid.GetCellValue(2, 1)),
                    "ElTariffClassPeak":self.check(self.grid.GetCellValue(2, 0)),
                    "ElTariffClassTotVall":self.check(self.grid.GetCellValue(2, 2)),
                    "ElTariffClassCHP":self.check(self.grid.GetCellValue(2, 5)),
                    "ElTariffPowTot":self.check(self.grid.GetCellValue(3, 3)),
                    "ElTariffPowStd":self.check(self.grid.GetCellValue(3, 1)),
                    "ElTariffPowPeak":self.check(self.grid.GetCellValue(3, 0)),
                    "ElTariffPowVall":self.check(self.grid.GetCellValue(3, 2)),
                    "ElTariffPowCHP":self.check(self.grid.GetCellValue(3, 5)),
                    "ElTariffCTot":self.check(self.grid.GetCellValue(4, 3)),
                    "ElTariffCStd":self.check(self.grid.GetCellValue(4, 1)),
                    "ElTariffCPeak":self.check(self.grid.GetCellValue(4, 0)),
                    "ElTariffCVall":self.check(self.grid.GetCellValue(4, 2)),
                    "ETariffCHP":self.check(self.grid.GetCellValue(4, 5)),
                    "ElCostYearTot":self.check(self.grid.GetCellValue(5, 3)),
                    "ElCostYearStd":self.check(self.grid.GetCellValue(5, 1)),
                    "ElCostYearPeak":self.check(self.grid.GetCellValue(5, 0)),
                    "ElCostYearVall":self.check(self.grid.GetCellValue(5, 2)),
                    "ElSalesYearCHP":self.check(self.grid.GetCellValue(5, 5))
                    }
                
                Status.DB.qelectricity.insert(tmp)
                Status.SQL.commit()                      

            elif len(Status.DB.qelectricity.Questionnaire_id[self.main.activeQid]) == 1:
                q = Status.DB.qelectricity.Questionnaire_id[self.main.activeQid][0]
                tmp = {                    
                    "PowerContrTot":self.check(self.grid.GetCellValue(1, 3)),
                    "PowerContrStd":self.check(self.grid.GetCellValue(1, 1)),
                    "PowerContrPeak":self.check(self.grid.GetCellValue(1, 0)),
                    "PowerContrVall":self.check(self.grid.GetCellValue(1, 2)),
                    "ElectricityTotYear":self.check(self.grid.GetCellValue(0, 3)),
                    "ElectricityPeakYear":self.check(self.grid.GetCellValue(0, 0)),
                    "ElectricityStandYear":self.check(self.grid.GetCellValue(0, 1)),
                    "ElectricityValleyYear":self.check(self.grid.GetCellValue(0, 2)),
                    "ElGenera":self.check(self.grid.GetCellValue(0, 4)),
                    "ElSales":self.check(self.grid.GetCellValue(0, 5)),
                    "ElectricityRef":self.check(self.grid.GetCellValue(8, 0)),
                    "ElectricityAC":self.check(self.grid.GetCellValue(8, 1)),
                    "ElectricityThOther":self.check(self.grid.GetCellValue(8, 2)),
                    "ElectricityMotors":self.check(self.grid.GetCellValue(8, 3)),
                    "ElectricityChem":self.check(self.grid.GetCellValue(8, 4)),
                    "ElectricityLight":self.check(self.grid.GetCellValue(8, 5)),
                    "ElTariffClassTot":self.check(self.grid.GetCellValue(2, 3)),
                    "ElTariffClassStd":self.check(self.grid.GetCellValue(2, 1)),
                    "ElTariffClassPeak":self.check(self.grid.GetCellValue(2, 0)),
                    "ElTariffClassTotVall":self.check(self.grid.GetCellValue(2, 2)),
                    "ElTariffClassCHP":self.check(self.grid.GetCellValue(2, 5)),
                    "ElTariffPowTot":self.check(self.grid.GetCellValue(3, 3)),
                    "ElTariffPowStd":self.check(self.grid.GetCellValue(3, 1)),
                    "ElTariffPowPeak":self.check(self.grid.GetCellValue(3, 0)),
                    "ElTariffPowVall":self.check(self.grid.GetCellValue(3, 2)),
                    "ElTariffPowCHP":self.check(self.grid.GetCellValue(3, 5)),
                    "ElTariffCTot":self.check(self.grid.GetCellValue(4, 3)),
                    "ElTariffCStd":self.check(self.grid.GetCellValue(4, 1)),
                    "ElTariffCPeak":self.check(self.grid.GetCellValue(4, 0)),
                    "ElTariffCVall":self.check(self.grid.GetCellValue(4, 2)),
                    "ETariffCHP":self.check(self.grid.GetCellValue(4, 5)),
                    "ElCostYearTot":self.check(self.grid.GetCellValue(5, 3)),
                    "ElCostYearStd":self.check(self.grid.GetCellValue(5, 1)),
                    "ElCostYearPeak":self.check(self.grid.GetCellValue(5, 0)),
                    "ElCostYearVall":self.check(self.grid.GetCellValue(5, 2)),
                    "ElSalesYearCHP":self.check(self.grid.GetCellValue(5, 5))
                    }
                q.update(tmp)
                Status.SQL.commit()

                
    def OnFuelListBoxClick(self, event):
        q = Status.DB.qfuel.Questionnaire_id[self.main.activeQid].DBFuel_id[Status.DB.dbfuel.FuelName[str(self.fuelListBox.GetStringSelection())][0].DBFuel_ID][0]
        self.tc2.SetValue(str(q.FuelUnit))
        self.tc3.SetValue(str(q.MFuelYear))
        self.tc4.SetValue(str(q.FuelOwn))
        self.tc5.SetValue(str(q.FuelTariff))
        self.tc6.SetValue(str(q.FuelCostYear))
        self.choiceOfDBFuelType.SetSelection(self.choiceOfDBFuelType.FindString(str(self.fuelListBox.GetStringSelection())))
        event.Skip()

    def OnButtonClear(self, event):
        self.clear()
        event.Skip()


#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		


    def fillChoiceOfDBFuelType(self):
        self.choiceOfDBFuelType.Clear()
        self.choiceOfDBFuelType.Append ("None")
        for n in Status.DB.dbfuel.FuelName["%"]:
            self.choiceOfDBFuelType.Append (n.FuelName)
        self.choiceOfDBFuelType.SetSelection(0)

    def fillPage(self):
	if self.main.activeQid == 0:
	    return

	if len(Status.DB.qelectricity.Questionnaire_id[self.main.activeQid]) <= 0:
	    return

	q = Status.DB.qelectricity.Questionnaire_id[self.main.activeQid][0]
	self.gridPage2.SetCellValue(1, 3, str(q.PowerContrTot))
	self.gridPage2.SetCellValue(1, 1, str(q.PowerContrStd))
	self.gridPage2.SetCellValue(1, 0, str(q.PowerContrPeak))
	self.gridPage2.SetCellValue(1, 2, str(q.PowerContrVall))
	self.gridPage2.SetCellValue(0, 3, str(q.ElectricityTotYear))
	self.gridPage2.SetCellValue(0, 0, str(q.ElectricityPeakYear))
	self.gridPage2.SetCellValue(0, 1, str(q.ElectricityStandYear))
	self.gridPage2.SetCellValue(0, 2, str(q.ElectricityValleyYear))
	self.gridPage2.SetCellValue(0, 4, str(q.ElGenera))
	self.gridPage2.SetCellValue(0, 5, str(q.ElSales))
	self.gridPage2.SetCellValue(8, 0, str(q.ElectricityRef))
	self.gridPage2.SetCellValue(8, 1, str(q.ElectricityAC))
	self.gridPage2.SetCellValue(8, 2, str(q.ElectricityThOther))
	self.gridPage2.SetCellValue(8, 3, str(q.ElectricityMotors))
	self.gridPage2.SetCellValue(8, 4, str(q.ElectricityChem))
	self.gridPage2.SetCellValue(8, 5, str(q.ElectricityLight))
	self.gridPage2.SetCellValue(2, 3, str(q.ElTariffClassTot))
	self.gridPage2.SetCellValue(2, 1, str(q.ElTariffClassStd))
	self.gridPage2.SetCellValue(2, 0, str(q.ElTariffClassPeak))
	self.gridPage2.SetCellValue(2, 2, str(q.ElTariffClassTotVall))
	self.gridPage2.SetCellValue(2, 5, str(q.ElTariffClassCHP))
	self.gridPage2.SetCellValue(3, 3, str(q.ElTariffPowTot))
	self.gridPage2.SetCellValue(3, 1, str(q.ElTariffPowStd))
	self.gridPage2.SetCellValue(3, 0, str(q.ElTariffPowPeak))
	self.gridPage2.SetCellValue(3, 2, str(q.ElTariffPowVall))
	self.gridPage2.SetCellValue(3, 5, str(q.ElTariffPowCHP))
	self.gridPage2.SetCellValue(4, 3, str(q.ElTariffCTot))
	self.gridPage2.SetCellValue(4, 1, str(q.ElTariffCStd))
	self.gridPage2.SetCellValue(4, 0, str(q.ElTariffCPeak))
	self.gridPage2.SetCellValue(4, 2, str(q.ElTariffCVall))
	self.gridPage2.SetCellValue(4, 5, str(q.ETariffCHP))
	self.gridPage2.SetCellValue(5, 3, str(q.ElCostYearTot))
	self.gridPage2.SetCellValue(5, 1, str(q.ElCostYearStd))
	self.gridPage2.SetCellValue(5, 0, str(q.ElCostYearPeak))
	self.gridPage2.SetCellValue(5, 2, str(q.ElCostYearVall))
	self.gridPage2.SetCellValue(5, 5, str(q.ElSalesYearCHP))
	self.fillFuelList()

    def fillFuelList(self):
        self.fuelListBox.Clear()
        if len(Status.DB.qfuel.Questionnaire_id[self.main.activeQid]) > 0:
            for n in Status.DB.qfuel.Questionnaire_id[self.main.activeQid]:
                self.fuelListBox.Append (str(Status.DB.dbfuel.DBFuel_ID[n.DBFuel_id][0].FuelName))

    def showError(self, message):
        dlg = wx.MessageDialog(None, message, 'Error', wx.OK)
        ret = dlg.ShowModal()
        dlg.Destroy()

    def showInfo(self, message):
        dlg = wx.MessageDialog(None, message, 'Info', wx.OK)
        ret = dlg.ShowModal()
        dlg.Destroy()

    def check(self, value):
        if value <> "" and value <> "None":
            return value
        else:
            return 'NULL'

    def clear(self):
        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
        self.tc6.SetValue('')
        self.grid.SetCellValue(1, 3, '')
        self.grid.SetCellValue(1, 1, '')
        self.grid.SetCellValue(1, 0, '')
        self.grid.SetCellValue(1, 2, '')
        self.grid.SetCellValue(0, 3, '')
        self.grid.SetCellValue(0, 0, '')
        self.grid.SetCellValue(0, 1, '')
        self.grid.SetCellValue(0, 2, '')
        self.grid.SetCellValue(0, 4, '')
        self.grid.SetCellValue(0, 5, '')
        self.grid.SetCellValue(8, 0, '')
        self.grid.SetCellValue(8, 1, '')
        self.grid.SetCellValue(8, 2, '')
        self.grid.SetCellValue(8, 3, '')
        self.grid.SetCellValue(8, 4, '')
        self.grid.SetCellValue(8, 5, '')
        self.grid.SetCellValue(2, 3, '')
        self.grid.SetCellValue(2, 1, '')
        self.grid.SetCellValue(2, 0, '')
        self.grid.SetCellValue(2, 2, '')
        self.grid.SetCellValue(2, 5, '')
        self.grid.SetCellValue(3, 3, '')
        self.grid.SetCellValue(3, 1, '')
        self.grid.SetCellValue(3, 0, '')
        self.grid.SetCellValue(3, 2, '')
        self.grid.SetCellValue(3, 5, '')
        self.grid.SetCellValue(4, 3, '')
        self.grid.SetCellValue(4, 1, '')
        self.grid.SetCellValue(4, 0, '')
        self.grid.SetCellValue(4, 2, '')
        self.grid.SetCellValue(4, 5, '')
        self.grid.SetCellValue(5, 3, '')
        self.grid.SetCellValue(5, 1, '')
        self.grid.SetCellValue(5, 0, '')
        self.grid.SetCellValue(5, 2, '')
        self.grid.SetCellValue(5, 5, '')


if __name__ == '__main__':
    import pSQL
    import MySQLdb
    class Main(object):
	def __init__(self,qid):
	    self.activeQid = qid

    DBName = 'einstein'
    Status.SQL = MySQLdb.connect(host='localhost', user='root', passwd='tom.tom', db=DBName)
    Status.DB =  pSQL.pSQL(Status.SQL, DBName)

    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(800, 600), title="Einstein - panelQ2")
    main = Main(1)
    panel = PanelQ2(frame, main)

    frame.Show(True)
    app.MainLoop()
