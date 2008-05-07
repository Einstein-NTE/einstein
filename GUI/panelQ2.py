# *-* coding: iso-8859-15 *-*
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
#	Version No.: 0.04
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger  02/05/2008
#                           Tom Sobota      02/05/2008
#                           Hans Schweiger  05/05/2008
#
#       Changes to previous version:
#       02/05/08:   HS  AlternativeProposalNo added in queries for table qproduct
#                   TS  Changes in layout
#       05/05/08:   HS  Event handlers changed; resize of grid so that it fits
#                       into the window
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
        self.__do_layout()
        
    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ2', parent=parent,
                             pos=wx.Point(0, 0), size=wx.Size(780, 580), style=wx.BK_DEFAULT|wx.BK_TOP)
        
        self.notebook = wx.Notebook(self, -1, style=0)

        self.page0 = wx.Panel(self.notebook)
        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page0, _('Fuel consumption and cost'))
        self.notebook.AddPage(self.page1, _('Electricity consumption and cost'))
        self.sizer_3_staticbox = wx.StaticBox(self.page0, -1, _("Fuels list"))
        self.sizer_3_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.fuelListBox = wx.ListBox(self.page0, -1, style=wx.LC_LIST|wx.SUNKEN_BORDER)
        self.Bind(wx.EVT_LISTBOX, self.OnFuelListBoxClick, self.fuelListBox)

        self.buttonRemoveFuelFromList = wx.Button(self.page0, -1, _("Remove from list"))
        self.buttonRemoveFuelFromList.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonRemoveFuelFromList, self.buttonRemoveFuelFromList)

        self.buttonAddFuel = wx.Button(self.page0, -1, _("Add fuel"))
        self.buttonAddFuel.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddFuel, self.buttonAddFuel)

        self.st1 = wx.StaticText(self.page0, -1, _("Fuels used"))
        self.choiceOfDBFuelType = wx.Choice(self.page0,-1,choices=[])
        self.st2 = wx.StaticText(self.page0, -1, _("Unit"))
        self.tc2 = wx.TextCtrl(self.page0, -1, "")
        self.st3 = wx.StaticText(self.page0, -1, _("Units/year"))
        self.tc3 = wx.TextCtrl(self.page0, -1, "")
        self.st4 = wx.StaticText(self.page0, -1, _("MWh / year (LCV)"))
        self.tc4 = wx.TextCtrl(self.page0, -1, "")
        self.st5 = wx.StaticText(self.page0, -1, _("Fuel price EUR/kWh LCV"))
        self.tc5 = wx.TextCtrl(self.page0, -1, "")
        self.st6 = wx.StaticText(self.page0, -1, _("Annual energy cost EUR/year"))
        self.tc6 = wx.TextCtrl(self.page0, -1, "")

        self.dummy1 = wx.StaticText(self.page0, -1, "")
        self.dummy2 = wx.StaticText(self.page0, -1, "")

        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        self.buttonOK = wx.Button(self,wx.ID_OK, 'OK')
        self.buttonOK.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)

        ###-- grid setup
        self.grid = wx.grid.Grid(self.page1, -1, size=(1,1))
        
        self.grid.EnableGridLines(True)
        self.grid.CreateGrid(9, 6)

        self.grid.SetDefaultColSize(100, resizeExistingCols=False)
        self.grid.SetDefaultRowSize(23, resizeExistingRows=False)

        self.grid.SetRowLabelSize(180)
        
        
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
        
        self.grid.SetColLabelValue(0,_('Peak'))
        self.grid.SetColLabelValue(1,_('Standard'))
        self.grid.SetColLabelValue(2,_('Valley'))
        self.grid.SetColLabelValue(3,_('TOTAL'))
        self.grid.SetColLabelValue(4,_('Self-generation'))
        self.grid.SetColLabelValue(5,_('Sales to grid'))

        self.grid.SetRowLabelValue(0,_('Annual consumption MWh/year'))
        self.grid.SetRowLabelValue(1,_('Contracted power kW'))
        self.grid.SetRowLabelValue(2,_('Tariff type'))
        self.grid.SetRowLabelValue(3,_('Tariff on installed power EUR/kW month'))
        self.grid.SetRowLabelValue(4,_('Tariff on consumption EUR/kWh'))
        self.grid.SetRowLabelValue(5,_('Annual electricity cost EUR/MWh'))
        self.grid.SetRowLabelValue(6,_('Electric consumption -'))
        self.grid.SetRowLabelValue(7,_('according type of use'))
        self.grid.SetRowLabelValue(8,_('Annual consumption MWh/year'))

        self.grid.SetRowLabelAlignment(wx.LEFT, wx.BOTTOM)

        self.grid.SetCellSize(6, 0, 1, 3)
        self.grid.SetCellSize(6, 3, 1, 3)
        self.grid.SetCellSize(1, 4, 1, 2)
        self.grid.SetCellSize(2, 4, 4, 1)



        self.grid.SetCellValue(6, 0, _('Electricity for thermal uses'))
        self.grid.SetCellValue(6, 3, _('Electricity for non-thermal uses'))
        self.grid.SetCellValue(7, 0, _('Refrigeration'))
        self.grid.SetCellValue(7, 1, _('Air Conditioning'))
        self.grid.SetCellValue(7, 2, _('Other uses'))
        self.grid.SetCellValue(7, 3, _('Motor and machines'))
        self.grid.SetCellValue(7, 4, _('Electro-chemics'))
        self.grid.SetCellValue(7, 5, _('Lighting'))

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


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizerPage1 = wx.BoxSizer(wx.VERTICAL)
        sizerPage0 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.FlexGridSizer(7, 2, 5, 2)
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.VERTICAL)
        sizer_3.Add(self.fuelListBox, 1, wx.EXPAND, 0)
        sizer_3.Add(self.buttonRemoveFuelFromList, 0, wx.ALIGN_RIGHT, 0)
        sizer_3.Add(self.buttonAddFuel, 0, wx.ALIGN_RIGHT, 2)
        sizerPage0.Add(sizer_3, 1, wx.EXPAND, 0)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)

        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL
        flagText = wx.ALIGN_CENTER_VERTICAL

        grid_sizer_1.Add(self.st1, 0, flagLabel, 0)
        grid_sizer_1.Add(self.choiceOfDBFuelType, 0, 0, 0)
        grid_sizer_1.Add(self.st2, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc2, 0, flagText, 0)
        grid_sizer_1.Add(self.st3, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc3, 0, flagText, 0)
        grid_sizer_1.Add(self.st4, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc4, 0, flagText, 0)
        grid_sizer_1.Add(self.st5, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc5, 0, flagText, 0)
        grid_sizer_1.Add(self.st6, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc6, 0, flagText, 0)

        sizerPage0.Add(grid_sizer_1, 2, wx.LEFT|wx.RIGHT|wx.EXPAND, 20)
        self.page0.SetSizer(sizerPage0)
        sizerPage1.Add(self.grid, 1, wx.EXPAND, 0)
        self.page1.SetSizer(sizerPage1)

        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)

        sizer_1.Add(self.notebook, 1, wx.EXPAND, 0)
        sizer_1.Add(sizerOKCancel, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer_1)
        self.Layout()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		

    def OnButtonAddFuel(self, event):
        self.clearFuelData()
        self.fillPage()

    def OnButtonRemoveFuelFromList(self, event):
        Status.prj.deleteFuel(self.selectedFuelID)
        self.clear()
        self.fillPage()
        event.Skip()


    def OnButtonOK(self, event):
        if self.notebook.GetSelection()==0:
            self.storeFuelData()
        else:
            self.storeElectricityData()

    def storeFuelData(self):
        fuelName = str(self.choiceOfDBFuelType.GetStringSelection())
        fuels = Status.DB.qfuel.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if Status.PId <> 0 and fuelName <> 'None':
            
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

            elif len(Status.DB.qfuel.Questionnaire_id[Status.PId].DBFuel_id[Status.DB.dbfuel.FuelName[str(self.choiceOfDBFuelType.GetStringSelection())][0].DBFuel_ID]) == 1:
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
                self.main.showError("Fuel name has to be a unique value!")

    def storeElectricityData(self):
        if Status.PId <> 0:
            if len(Status.DB.qelectricity.Questionnaire_id[Status.PId]) == 0:
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

            elif len(Status.DB.qelectricity.Questionnaire_id[Status.PId]) == 1:
                q = Status.DB.qelectricity.Questionnaire_id[Status.PId][0]
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
        try:
            self.selectedFuelName = str(self.fuelListBox.GetStringSelection())
            self.selectedFuelID = Status.DB.dbfuel.FuelName[self.selectedFuelName][0].DBFuel_ID
            q = Status.DB.qfuel.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].DBFuel_id[self.selectedFuelID][0]
            self.tc2.SetValue(str(q.FuelUnit))
            self.tc3.SetValue(str(q.MFuelYear))
            self.tc4.SetValue(str(q.FuelOwn))
            self.tc5.SetValue(str(q.FuelTariff))
            self.tc6.SetValue(str(q.FuelCostYear))
            self.choiceOfDBFuelType.SetSelection(self.choiceOfDBFuelType.FindString(self.selectedFuelName))
        except IndexError:
            # no data available
            self.clear()
        event.Skip()

    def OnButtonCancel(self, event):
        if self.notebook.GetSelection()==0:
            self.clearFuelData()
        else:
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

	q = Status.DB.qelectricity.Questionnaire_id[Status.PId][0]
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

    def check(self, value):
        if value <> "" and value <> "None":
            return value
        else:
            return 'NULL'

    def clearFuelData(self):
        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
        self.tc6.SetValue('')

    def clear(self):
        self.clearFuelData()
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
