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
#	PanelQ2: Questionnaire on energy consumption
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by: 	Heiko Henning, Tom Sobota, Hans Schweiger, Stoyan Danov
#                       February 2008 - 13/10/2008
#
#   Update No. 001
#
#   Since Version 1.0 revised by:
#
#                       Hans Schweiger  06/04/2008
#               
#   06/04/2008  HS  Small bug-fix: increase of maximum value for fuel cost
#
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008, 2009
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
from GUITools import *
from units import *
from displayClasses import *
from fonts import *

# constants that control the default sizes
# 1. font sizes
TYPE_SIZE_LEFT    =   9
TYPE_SIZE_RIGHT   =   9
TYPE_SIZE_TITLES  =  10

# 2. field sizes
HEIGHT_LEFT       =  27
LABEL_WIDTH_LEFT  = 220
DATA_ENTRY_WIDTH  = 100
UNITS_WIDTH       = 110

ORANGE = '#FF6000'
TITLE_COLOR = ORANGE

def _U(text):
    return unicode(_(text),"utf-8")

#------------------------------------------------------------------------------
def scale(val,fscale):
    try:
        x = float(val)*fscale
    except:
        x = val
    return x

#------------------------------------------------------------------------------
class PanelQ2(wx.Panel):
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def __init__(self, parent, main):
#------------------------------------------------------------------------------
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)
        self.__do_layout()
       
#------------------------------------------------------------------------------
    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

##                             pos=wx.Point(0, 0), size=wx.Size(780, 580), style=wx.BK_DEFAULT|wx.BK_TOP)
        wx.Panel.__init__(self, id=-1, name='PanelQ2', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()
        
        # access to font properties object
        fp = FontProperties()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook.SetFont(fp.getFont())
        self.page0 = wx.Panel(self.notebook)
        self.page1 = wx.Panel(self.notebook)

        self.notebook.AddPage(self.page0, _U('Fuel consumption and cost'))#SD put this later in do_layout
        self.notebook.AddPage(self.page1, _U('Electricity consumption and cost'))

        self.sizer_3_staticbox = wx.StaticBox(self.page0, -1, _U("Fuels list"))
        self.sizer_3_staticbox.SetForegroundColour(TITLE_COLOR)
        self.sizer_3_staticbox.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.sizer_5_staticbox = wx.StaticBox(self.page0, -1, _U("Fuel consumption data"))
        self.sizer_5_staticbox.SetForegroundColour(TITLE_COLOR)
        self.sizer_5_staticbox.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        # set font for titles
        # 1. save actual font parameters on the stack
        fp.pushFont()
        # 2. change size and weight
        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
        self.sizer_3_staticbox.SetFont(fp.getFont())
        self.sizer_5_staticbox.SetFont(fp.getFont())
        # 3. recover previous font state
        fp.popFont()

        # set field sizes for the left tab.
        fs = FieldSizes(wHeight=HEIGHT_LEFT,wLabel=LABEL_WIDTH_LEFT,
                       wData=DATA_ENTRY_WIDTH,wUnits=UNITS_WIDTH)

        # set font for labels of left tab
        fp.pushFont()
        fp.changeFont(size=TYPE_SIZE_LEFT)

        self.fuelListBox = wx.ListBox(self.page0, -1, style=wx.LC_LIST|wx.SUNKEN_BORDER)#SD added
        self.fuelListBox.SetFont(fp.getFont())
        self.Bind(wx.EVT_LISTBOX, self.OnFuelListBoxClick, self.fuelListBox)

        self.buttonRemoveFuelFromList = wx.Button(self.page0, -1, _U("Remove from list"))
        self.buttonRemoveFuelFromList.SetMinSize((125, 32))
        self.buttonRemoveFuelFromList.SetFont(fp.getFont())
        self.Bind(wx.EVT_BUTTON, self.OnButtonRemoveFuelFromList, self.buttonRemoveFuelFromList)

        self.buttonAddFuel = wx.Button(self.page0, -1, _U("Add fuel"))
        self.buttonAddFuel.SetMinSize((125, 32))
        self.buttonAddFuel.SetFont(fp.getFont())
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddFuel, self.buttonAddFuel)

        self.tc1 = ChoiceEntry(self.page0, 
                               values=[],
                               label=_U("Fuels used"),
                               tip=_U(" "))
        
        self.tc3 = FloatEntry(self.page0,
                              ipart=10, decimals=2, minval=0., maxval=1.0e+12, value=0.,
                              unitdict='MASSORVOLUME',
                              label=_U("Annual consumption (fuel units)"),
                              tip=_U("If possible, provide the monthly data in separate sheet and/or the fuel bills. Specify the energy equivalent in base of LCV (lower calorific value)"))  
        
        self.tc4 = FloatEntry(self.page0,
                              ipart=10, decimals=2, minval=0., maxval=1.0e+12, value=0.,
                              unitdict='ENERGY',
                              label=_U("Annual consumption (LCV)"),
                              tip=_U(" "))  
        
        self.tc5 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=999999., value=0.,
                              unitdict='ENERGYTARIFF',
                              label=_U("Fuel price(LCV)"),
                              tip=_U("Specify expenditures without VAT"))  
        
        self.tc6 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=1.0e+12, value=0.,
                              unitdict='PRICE',
                              label=_U("Annual energy cost"),
                              tip=_U("Total cost"))  

        # fillers
        self.dummy1 = wx.StaticText(self.page0, -1, "")
        self.dummy2 = wx.StaticText(self.page0, -1, "")

        # OK/Cancel buttons
        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, _U("Cancel"))
        self.buttonCancel.SetFont(fp.getFont())
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        self.buttonOK = wx.Button(self,wx.ID_OK, 'OK')
        self.buttonOK.SetDefault()
        self.buttonOK.SetFont(fp.getFont())
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)

        # Right panel controls
        fp.changeFont(size=TYPE_SIZE_RIGHT)

        ###-- grid setup
        self.grid = wx.grid.Grid(self.page1, -1, size=(1,1))
        
        self.grid.EnableGridLines(True)
        self.grid.CreateGrid(9, 6)

        self.grid.SetDefaultColSize(90, resizeExistingCols=False)
        self.grid.SetDefaultRowSize(23, resizeExistingRows=False)

        self.grid.SetRowLabelSize(215)
        
        
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour("light gray")
        attr.SetFont(fp.getFont())
        self.grid.SetAttr(7, 0, attr)
        self.grid.SetAttr(7, 1, attr)
        self.grid.SetAttr(7, 2, attr)
        self.grid.SetAttr(7, 3, attr)
        self.grid.SetAttr(7, 4, attr)
        self.grid.SetAttr(7, 5, attr)
        

        attr2 = wx.grid.GridCellAttr()
        attr2.SetBackgroundColour("light gray")
        attr2.SetFont(fp.getFont())
        self.grid.SetAttr(6, 0, attr2)
        self.grid.SetAttr(6, 3, attr2)

        attr3 = wx.grid.GridCellAttr()
        attr3.SetBackgroundColour("light gray")
        attr3.SetFont(fp.getFont())
        self.grid.SetAttr(2, 4, attr3)


        attr4 = wx.grid.GridCellAttr()
        attr4.SetBackgroundColour("light gray")
        attr4.SetFont(fp.getFont())
        self.grid.SetAttr(1, 4, attr4)
        
        self.grid.SetColLabelValue(0,_U('Peak'))
        self.grid.SetColLabelValue(1,_U('Standard'))
        self.grid.SetColLabelValue(2,_U('Valley'))
        self.grid.SetColLabelValue(3,_U('TOTAL'))
        self.grid.SetColLabelValue(4,_U('Self-generation'))
        self.grid.SetColLabelValue(5,_U('Sales to grid'))

        self.grid.SetRowLabelValue(0,_U('Annual consumption [MWh]'))
        self.grid.SetRowLabelValue(1,_U('Contracted power [kW]'))
        self.grid.SetRowLabelValue(2,_U('Tariff type'))
        self.grid.SetRowLabelValue(3,_U('Tariff installed power [EUR/kW.month]'))
        self.grid.SetRowLabelValue(4,_U('Tariff on consumption [EUR/kWh]'))
        self.grid.SetRowLabelValue(5,_U('Annual electricity cost [EUR]'))
        self.grid.SetRowLabelValue(6,_U('Electric consumption -'))
        self.grid.SetRowLabelValue(7,_U('according type of use'))
        self.grid.SetRowLabelValue(8,_U('Annual consumption [MWh]'))

        self.grid.SetRowLabelAlignment(wx.LEFT, wx.BOTTOM)

        self.grid.SetCellSize(6, 0, 1, 3)
        self.grid.SetCellSize(6, 3, 1, 3)
        self.grid.SetCellSize(1, 4, 1, 2)
        self.grid.SetCellSize(2, 4, 4, 1)

        self.grid.SetCellValue(6, 0, _U('Electricity for thermal uses'))
        self.grid.SetCellValue(6, 3, _U('Electricity for non-thermal uses'))
        self.grid.SetCellValue(7, 0, _U('Refrigeration'))
        self.grid.SetCellValue(7, 1, _U('Air Conditioning'))
        self.grid.SetCellValue(7, 2, _U('Other uses'))
        self.grid.SetCellValue(7, 3, _U('Motor and machines'))
        self.grid.SetCellValue(7, 4, _U('Electro-chemics'))
        self.grid.SetCellValue(7, 5, _U('Lighting'))

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
        # global sizer for panel. Contains notebook w/two tabs + buttons Cancel and Ok
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        # sizer for left tab
        sizerPage0 = wx.BoxSizer(wx.HORIZONTAL)
        # sizer for right tab
        sizerPage1 = wx.BoxSizer(wx.VERTICAL)

        # left part of left tab: Fuel listbox + buttons Add and Remove
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.VERTICAL)
        sizer_3.Add(self.fuelListBox, 1, wx.EXPAND,0)
        sizer_3.Add(self.buttonAddFuel, 0, wx.ALIGN_RIGHT, 2)
        sizer_3.Add(self.buttonRemoveFuelFromList, 0, wx.ALIGN_RIGHT, 0)
        sizerPage0.Add(sizer_3, 1, wx.EXPAND|wx.TOP, 20)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)

        # right part of left tab: data entry widgets
        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL
        flagText = wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT

        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)
        sizer_5.Add(self.tc1, 0, flagText, 2)
        sizer_5.Add(self.tc3, 0, flagText, 2)
        sizer_5.Add(self.tc4, 0, flagText, 2)
        sizer_5.Add(self.tc5, 0, flagText, 2)
        sizer_5.Add(self.tc6, 0, flagText, 2)

        sizerPage0.Add(sizer_5, 2, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 20)
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
        if self.checkIfAllowed()==False:
            return
        self.clearFuelData()
        self.fillPage()

    def OnButtonRemoveFuelFromList(self, event):
        if self.checkIfAllowed()==False:
            return

        Status.prj.deleteFuel(self.selectedFuelID)
        self.clear()
        self.fillPage()
        event.Skip()


    def OnButtonOK(self, event):
        if self.checkIfAllowed()==False:
            return

        if self.notebook.GetSelection()==0:
            self.storeFuelData()
        else:
            self.storeElectricityData()

    def storeFuelData(self):
        fuelName = self.tc1.GetValue(text=True)
        dbfuels = Status.DB.dbfuel.FuelName[check(fuelName)]
        if len(dbfuels) > 0:
            dbfid = dbfuels[0].DBFuel_ID
            setUnitsFuelDensity(dbfid)
        else:
            dbfid = -1
        fuels = Status.DB.qfuel.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].DBFuel_id[dbfid]

        if Status.PId <> 0 and fuelName <> 'None':
            if len(fuels) == 0:
                newID = Status.prj.addFuelDummy()
                tmp = {
                    "DBFuel_id":dbfid,
                    "MFuelYear":check(self.tc3.GetValue()), 
                    "FECFuel":check(self.tc4.GetValue()),
                    "FuelTariff":check(self.tc5.GetValue()),
                    "FuelCostYear":check(self.tc6.GetValue())
                    }
                
                q = Status.DB.qfuel.QFuel_ID[newID][0]
                q.update(tmp)               
                Status.SQL.commit()
                
                self.fillFuelList()

            elif len(fuels) == 1:
                tmp = {
                    "DBFuel_id":dbfid,
                    "MFuelYear":check(self.tc3.GetValue()), 
                    "FECFuel":check(self.tc4.GetValue()),
                    "FuelTariff":check(self.tc5.GetValue()),
                    "FuelCostYear":check(self.tc6.GetValue())
                    }
                
                q = Status.DB.qfuel.DBFuel_id[dbfid].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillFuelList()
                          
            else:
                self.main.showError(_U("Fuel name has to be a unique value!"))

    def storeElectricityData(self):
        if Status.PId <> 0:

            elTable = Status.DB.qelectricity.\
                   Questionnaire_id[Status.PId].\
                   AlternativeProposalNo[Status.ANo]
            
            if len(elTable) == 0:

                logDebug("PanelQ2: no electricity table available in project")
                
                tmp = {
                    "Questionnaire_id":Status.PId,
                    "AlternativeProposalNo":Status.ANo}
                
                Status.DB.qelectricity.insert(tmp)
                Status.SQL.commit()                      

            elTable = Status.DB.qelectricity.\
                   Questionnaire_id[Status.PId].\
                   AlternativeProposalNo[Status.ANo]
            
            if len(elTable) >= 1:

                q = elTable[0]
                tmp = {                    
                    "PowerContrTot":check(self.grid.GetCellValue(1, 3)),
                    "PowerContrStd":check(self.grid.GetCellValue(1, 1)),
                    "PowerContrPeak":check(self.grid.GetCellValue(1, 0)),
                    "PowerContrVall":check(self.grid.GetCellValue(1, 2)),
                    "ElectricityTotYear":check(scale(self.grid.GetCellValue(0, 3),1000.0)),
                    "ElectricityPeakYear":check(scale(self.grid.GetCellValue(0, 0),1000.0)),
                    "ElectricityStandYear":check(scale(self.grid.GetCellValue(0, 1),1000.0)),
                    "ElectricityValleyYear":check(scale(self.grid.GetCellValue(0, 2),1000.0)),
                    "ElGenera":check(scale(self.grid.GetCellValue(0, 4),1000.0)),
                    "ElSales":check(scale(self.grid.GetCellValue(0, 5),1000.0)),
                    "ElectricityRef":check(scale(self.grid.GetCellValue(8, 0),1000.0)),
                    "ElectricityAC":check(scale(self.grid.GetCellValue(8, 1),1000.0)),
                    "ElectricityThOther":check(scale(self.grid.GetCellValue(8, 2),1000.0)),
                    "ElectricityMotors":check(scale(self.grid.GetCellValue(8, 3),1000.0)),
                    "ElectricityChem":check(scale(self.grid.GetCellValue(8, 4),1000.0)),
                    "ElectricityLight":check(scale(self.grid.GetCellValue(8, 5),1000.0)),
                    "ElTariffClassTot":check(self.grid.GetCellValue(2, 3)),
                    "ElTariffClassStd":check(self.grid.GetCellValue(2, 1)),
                    "ElTariffClassPeak":check(self.grid.GetCellValue(2, 0)),
                    "ElTariffClassTotVall":check(self.grid.GetCellValue(2, 2)),
                    "ElTariffClassCHP":check(self.grid.GetCellValue(2, 5)),
                    "ElTariffPowTot":check(self.grid.GetCellValue(3, 3)),
                    "ElTariffPowStd":check(self.grid.GetCellValue(3, 1)),
                    "ElTariffPowPeak":check(self.grid.GetCellValue(3, 0)),
                    "ElTariffPowVall":check(self.grid.GetCellValue(3, 2)),
                    "ElTariffPowCHP":check(self.grid.GetCellValue(3, 5)),
                    "ElTariffCTot":check(self.grid.GetCellValue(4, 3)),
                    "ElTariffCStd":check(self.grid.GetCellValue(4, 1)),
                    "ElTariffCPeak":check(self.grid.GetCellValue(4, 0)),
                    "ElTariffCVall":check(self.grid.GetCellValue(4, 2)),
                    "ETariffCHP":check(self.grid.GetCellValue(4, 5)),
                    "ElCostYearTot":check(self.grid.GetCellValue(5, 3)),
                    "ElCostYearStd":check(self.grid.GetCellValue(5, 1)),
                    "ElCostYearPeak":check(self.grid.GetCellValue(5, 0)),
                    "ElCostYearVall":check(self.grid.GetCellValue(5, 2)),
                    "ElSalesYearCHP":check(self.grid.GetCellValue(5, 5))
                    }

                q.update(tmp)
                Status.SQL.commit()

                
    def OnFuelListBoxClick(self, event):
        try:
            self.selectedFuelName = self.fuelListBox.GetStringSelection()
            self.selectedFuelID = Status.DB.dbfuel.FuelName[check(self.selectedFuelName)][0].DBFuel_ID
            setUnitsFuelDensity(self.selectedFuelID)
            
            q = Status.DB.qfuel.\
                Questionnaire_id[Status.PId].\
                AlternativeProposalNo[Status.ANo].\
                DBFuel_id[self.selectedFuelID][0]
            
            self.tc3.SetValue(str(q.MFuelYear))
            self.tc4.SetValue(str(q.FECFuel))
            self.tc5.SetValue(str(q.FuelTariff))
            self.tc6.SetValue(str(q.FuelCostYear))
            self.tc1.SetValue(self.selectedFuelName)
            
        except IndexError:
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

    def display(self):
        self.fillChoiceOfDBFuelType()
        self.clear()
        self.Hide()
        self.fillPage()
        self.Show()


    def fillChoiceOfDBFuelType(self):
#SD2008-06-11
        fuelDict = Status.prj.getFuelDict()
        fuelNames = fuelDict.values()
        self.tc1.entry.Clear()
        for name in fuelNames:
            self.tc1.entry.Append(name)        

    def fillPage(self):
	if Status.PId == 0:
	    return

        elTable = Status.DB.qelectricity.\
               Questionnaire_id[Status.PId].\
               AlternativeProposalNo[Status.ANo]

	if len(elTable) > 0:
	    
            q = elTable[0]
            self.grid.SetCellValue(1, 3, str(q.PowerContrTot))
            self.grid.SetCellValue(1, 1, str(q.PowerContrStd))
            self.grid.SetCellValue(1, 0, str(q.PowerContrPeak))
            self.grid.SetCellValue(1, 2, str(q.PowerContrVall))
            self.grid.SetCellValue(0, 3, str(scale(q.ElectricityTotYear,0.001)))
            self.grid.SetCellValue(0, 0, str(scale(q.ElectricityPeakYear,0.001)))
            self.grid.SetCellValue(0, 1, str(scale(q.ElectricityStandYear,0.001)))
            self.grid.SetCellValue(0, 2, str(scale(q.ElectricityValleyYear,0.001)))
            self.grid.SetCellValue(0, 4, str(scale(q.ElGenera,0.001)))
            self.grid.SetCellValue(0, 5, str(scale(q.ElSales,0.001)))
            self.grid.SetCellValue(8, 0, str(scale(q.ElectricityRef,0.001)))
            self.grid.SetCellValue(8, 1, str(scale(q.ElectricityAC,0.001)))
            self.grid.SetCellValue(8, 2, str(scale(q.ElectricityThOther,0.001)))
            self.grid.SetCellValue(8, 3, str(scale(q.ElectricityMotors,0.001)))
            self.grid.SetCellValue(8, 4, str(scale(q.ElectricityChem,0.001)))
            self.grid.SetCellValue(8, 5, str(scale(q.ElectricityLight,0.001)))
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

        else:
            logDebug("PanelQ2 (fillPage): electricity table not found")

	self.fillFuelList()

    def fillFuelList(self):
        self.fuelListBox.Clear()
        fuels = Status.DB.qfuel.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(fuels) > 0:
            for n in fuels:
                dbfid = n.DBFuel_id
                try:
                    fuelName = unicode(Status.DB.dbfuel.DBFuel_ID[n.DBFuel_id][0].FuelName,"utf-8")
                except:
                    fuelName = "unknown fuel"
                self.fuelListBox.Append(fuelName)

    def clearFuelData(self):
##        self.tc2.SetValue('')
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

    def checkIfAllowed(self):
	if Status.ANo >= 0:
            showWarning(_U("In the present version of EINSTEIN it is not allowed to modify\n")+\
                        _U("fuel consumption in the checked state or alternative proposals. This is a RESULT of calculation\n")+\
                        _U("Workaround for studying fuel substitution: add all fuels You want to consider already in the original state\n")+\
                        _U("and set original consumption of these additional fuels to 0"))
            return False
        else:   
            return True


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
