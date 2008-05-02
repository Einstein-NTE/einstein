#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	PanelQ0: Tool main page (page 0) -> project selection
#
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger 02/05/2008
#
#       Changes to previous version:
#       02/05/08:       AlternativeProposalNo added in queries for table qproduct
#
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	http://www.energyxperts.net/
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================

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
              name='buttonStore', parent=self, pos=wx.Point(600,
              520), size=wx.Size(192, 32), style=0)
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
				 size=wx.Size(800, 240),
				 style=0)
        
        self.grid.EnableGridLines(True)
        self.grid.CreateGrid(9, 6)

        self.grid.SetDefaultColSize(100, resizeExistingCols=False)
        self.grid.SetDefaultRowSize(23, resizeExistingRows=False)

        self.grid.SetRowLabelSize(200)
        
        
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
        fuelName = str(self.choiceOfDBFuelType.GetStringSelection())
        fuels = Status.DB.qfuel.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if Status.PId <> 0 and fuelName <> 'None':
            dbfid = Status.DB.dbfuel.FuelName[fuelName][0].DBFuel_ID
            if len(fuels.DBFuel_id[dbfid]) == 0:
                newID = Status.prj.addFuelDummy()
                tmp = {
                    "FuelUnit":self.check(self.tc2.GetValue()),
                    "DBFuel_id":dbfid,
                    "MFuelYear":self.check(self.tc3.GetValue()), 
                    "FuelOwn":self.check(self.tc4.GetValue()),
                    "FuelTariff":self.check(self.tc5.GetValue()),
                    "FuelCostYear":self.check(self.tc6.GetValue())
                    }
                
                q = Status.DB.qfuel.QFuel_ID[newID][0]
                q.update(tmp)               
                Status.SQL.commit()
                
                self.fillFuelList()


            elif len(fuels.DBFuel_id[dbfid]) == 1:
                tmp = {
                    "FuelUnit":self.check(self.tc2.GetValue()),
                    "DBFuel_id":dbfid,
                    "MFuelYear":self.check(self.tc3.GetValue()), 
                    "FuelOwn":self.check(self.tc4.GetValue()),
                    "FuelTariff":self.check(self.tc5.GetValue()),
                    "FuelCostYear":self.check(self.tc6.GetValue())
                    }
                
                q = Status.DB.qfuel.DBFuel_id[dbfid].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillFuelList()
                          
            else:
                self.showError("FuelName have to be an uniqe value!")


    def OnButtonRemoveFuelFromList(self, event):
        print "PanelQ2 (remove fuel): removing fuel no ",self.selectedFuelID
        Status.prj.deleteFuel(self.selectedFuelID)
        self.clear()
        self.fillPage()


    def OnButtonStore(self, event):
        if Status.PId <> 0:
            if len(Status.DB.qelectricity.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]) == 0:
                tmp = {
                    "Questionnaire_id":Status.PId,
                    "AlternativeProposalNo":Status.ANo,
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

            elif len(Status.DB.qelectricity.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]) == 1:
                q = Status.DB.qelectricity.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]
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
        self.selectedFuelName = str(self.fuelListBox.GetStringSelection())
        self.selectedFuelID = Status.DB.dbfuel.FuelName[self.selectedFuelName][0].DBFuel_ID
        q = Status.DB.qfuel.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].DBFuel_id[self.selectedFuelID][0]
        self.tc2.SetValue(str(q.FuelUnit))
        self.tc3.SetValue(str(q.MFuelYear))
        self.tc4.SetValue(str(q.FuelOwn))
        self.tc5.SetValue(str(q.FuelTariff))
        self.tc6.SetValue(str(q.FuelCostYear))
        self.choiceOfDBFuelType.SetSelection(self.choiceOfDBFuelType.FindString(self.selectedFuelName))
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
	if Status.PId == 0:
	    return

	if len(Status.DB.qelectricity.Questionnaire_id[Status.PId]) <= 0:
	    return

	q = Status.DB.qelectricity.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]
	self.grid.SetCellValue(1, 3, str(q.PowerContrTot))
	self.grid.SetCellValue(1, 1, str(q.PowerContrStd))
	self.grid.SetCellValue(1, 0, str(q.PowerContrPeak))
	self.grid.SetCellValue(1, 2, str(q.PowerContrVall))
	self.grid.SetCellValue(0, 3, str(q.ElectricityTotYear))
	self.grid.SetCellValue(0, 0, str(q.ElectricityPeakYear))
	self.grid.SetCellValue(0, 1, str(q.ElectricityStandYear))
	self.grid.SetCellValue(0, 2, str(q.ElectricityValleyYear))
	self.grid.SetCellValue(0, 4, str(q.ElGenera))
	self.grid.SetCellValue(0, 5, str(q.ElSales))
	self.grid.SetCellValue(8, 0, str(q.ElectricityRef))
	self.grid.SetCellValue(8, 1, str(q.ElectricityAC))
	self.grid.SetCellValue(8, 2, str(q.ElectricityThOther))
	self.grid.SetCellValue(8, 3, str(q.ElectricityMotors))
	self.grid.SetCellValue(8, 4, str(q.ElectricityChem))
	self.grid.SetCellValue(8, 5, str(q.ElectricityLight))
	self.grid.SetCellValue(2, 3, str(q.ElTariffClassTot))
	self.grid.SetCellValue(2, 1, str(q.ElTariffClassStd))
	self.grid.SetCellValue(2, 0, str(q.ElTariffClassPeak))
	self.grid.SetCellValue(2, 2, str(q.ElTariffClassTotVall))
	self.grid.SetCellValue(2, 5, str(q.ElTariffClassCHP))
	self.grid.SetCellValue(3, 3, str(q.ElTariffPowTot))
	self.grid.SetCellValue(3, 1, str(q.ElTariffPowStd))
	self.grid.SetCellValue(3, 0, str(q.ElTariffPowPeak))
	self.grid.SetCellValue(3, 2, str(q.ElTariffPowVall))
	self.grid.SetCellValue(3, 5, str(q.ElTariffPowCHP))
	self.grid.SetCellValue(4, 3, str(q.ElTariffCTot))
	self.grid.SetCellValue(4, 1, str(q.ElTariffCStd))
	self.grid.SetCellValue(4, 0, str(q.ElTariffCPeak))
	self.grid.SetCellValue(4, 2, str(q.ElTariffCVall))
	self.grid.SetCellValue(4, 5, str(q.ETariffCHP))
	self.grid.SetCellValue(5, 3, str(q.ElCostYearTot))
	self.grid.SetCellValue(5, 1, str(q.ElCostYearStd))
	self.grid.SetCellValue(5, 0, str(q.ElCostYearPeak))
	self.grid.SetCellValue(5, 2, str(q.ElCostYearVall))
	self.grid.SetCellValue(5, 5, str(q.ElSalesYearCHP))
	self.fillFuelList()

    def fillFuelList(self):
        self.fuelListBox.Clear()
        fuels = Status.DB.qfuel.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(fuels) > 0:
            for n in fuels:
                dbfid = n.DBFuel_id
                try:
                    fuelName = str(Status.DB.dbfuel.DBFuel_ID[n.DBFuel_id][0].FuelName)
                except:
                    fuelName = "unknown fuel"
                self.fuelListBox.Append(fuelName)

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
