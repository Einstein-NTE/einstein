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
#	Version No.: 0.16
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger  02/05/2008
#                           Tom Sobota      02/05/2008
#                           Hans Schweiger  05/05/2008
#                           Hans Schweiger  10/05/2008
#                           Stoyan Danov    06/06/2008
#                           Hans Schweiger  10/06/2008
#                           Stoyan Danov    11/06/2008
#                           Hans Schweiger  12/06/2008
#                           Stoyan Danov    17/06/2008
#                           Stoyan Danov    18/06/2008
#                           Tom Sobota      21/06/2008
#                           Hans Schweiger  23/06/2008
#                           Hans Schweiger  03/07/2008
#                           Hans Schweiger  07/07/2008
#
#       Changes to previous version:
#       02/05/08:   HS  AlternativeProposalNo added in queries for table qproduct
#                   TS  Changes in layout
#       05/05/08:   HS  Event handlers changed; resize of grid so that it fits
#                       into the window
#       10/05/08:   HS  FuelOwn substituted by FECFuel
#       06/06/2008  SD  New label/tooltips according to new displayClasses defined;
#                       do_layout still not adapted
#       10/06/2008: HS  Adapted size of decimal numbers in order to bring it to run ...
#       11/06/2008: SD  changed tips, unitdict filling, tc1 - choice fuels DB arranged
#       12/06/2008: HS  unitdict adapted to new version of units
#       17/06/2008 SD   adapt to new unitdict
#       18/06/2008 SD   create display()
#                   HS  some clean-up of old comments.
#       21/06/2008 TS   general layout beautification. Adapt to font awareness.
#       23/06/2008  HS  small changes in eventhandlers (missing adaptations to
#                       new ChoiceEntry ...
#       03/07/2008: HS  adjustment of column with in table electricity; 
#       07/07/2008: HS  bug-fix: self.check substituted by GUITools->check
#                       the old one didn't work with Tom's new FloatEntry
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
from GUITools import *
from displayClasses import *
from units import *
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

#------------------------------------------------------------------------------
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

        self.notebook.AddPage(self.page0, _('Fuel consumption and cost'))#SD put this later in do_layout
        self.notebook.AddPage(self.page1, _('Electricity consumption and cost'))

        self.sizer_3_staticbox = wx.StaticBox(self.page0, -1, _("Fuels list"))
        self.sizer_3_staticbox.SetForegroundColour(TITLE_COLOR)
        self.sizer_3_staticbox.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.sizer_5_staticbox = wx.StaticBox(self.page0, -1, _("Fuel consumption data"))
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

        self.buttonRemoveFuelFromList = wx.Button(self.page0, -1, _("Remove from list"))
        self.buttonRemoveFuelFromList.SetMinSize((125, 32))
        self.buttonRemoveFuelFromList.SetFont(fp.getFont())
        self.Bind(wx.EVT_BUTTON, self.OnButtonRemoveFuelFromList, self.buttonRemoveFuelFromList)

        self.buttonAddFuel = wx.Button(self.page0, -1, _("Add fuel"))
        self.buttonAddFuel.SetMinSize((125, 32))
        self.buttonAddFuel.SetFont(fp.getFont())
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddFuel, self.buttonAddFuel)

        self.tc1 = ChoiceEntry(self.page0, 
                               values=[],
                               label=_("Fuels used"),
                               tip=_(" "))
        
        self.tc3 = FloatEntry(self.page0,
                              ipart=10, decimals=2, minval=0., maxval=1.0e+9, value=0.,
                              unitdict='MASSORVOLUMEFLOW',
                              label=_("Annual consumption (fuel units)"),
                              tip=_("If possible, provide the monthly data in separate sheet and/or the fuel bills. \
Specify the energy equivalent in base of LCV (lower calorific value)"))  
        
        
        self.tc4 = FloatEntry(self.page0,
                              ipart=10, decimals=2, minval=0., maxval=1.0e+9, value=0.,
                              unitdict='ENERGY',
                              label=_("Annual consumption (LCV)"),
                              tip=_(" "))  
        
        self.tc5 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=999999., value=0.,
                              unitdict='ENERGYTARIFF',
                              label=_("Fuel price(LCV)"),
                              tip=_("Specify expenditures without VAT"))  
        
        self.tc6 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=99999., value=0.,
                              unitdict='PRICE',
                              label=_("Annual energy cost"),
                              tip=_("Total cost"))  

        # fillers
        self.dummy1 = wx.StaticText(self.page0, -1, "")
        self.dummy2 = wx.StaticText(self.page0, -1, "")

        # OK/Cancel buttons
        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))
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
        
        self.grid.SetColLabelValue(0,_('Peak'))
        self.grid.SetColLabelValue(1,_('Standard'))
        self.grid.SetColLabelValue(2,_('Valley'))
        self.grid.SetColLabelValue(3,_('TOTAL'))
        self.grid.SetColLabelValue(4,_('Self-generation'))
        self.grid.SetColLabelValue(5,_('Sales to grid'))

        self.grid.SetRowLabelValue(0,_('Annual consumption [MWh]'))
        self.grid.SetRowLabelValue(1,_('Contracted power [kW]'))
        self.grid.SetRowLabelValue(2,_('Tariff type'))
        self.grid.SetRowLabelValue(3,_('Tariff installed power [EUR/kW.month]'))
        self.grid.SetRowLabelValue(4,_('Tariff on consumption [EUR/kWh]'))
        self.grid.SetRowLabelValue(5,_('Annual electricity cost [EUR]'))
        self.grid.SetRowLabelValue(6,_('Electric consumption -'))
        self.grid.SetRowLabelValue(7,_('according type of use'))
        self.grid.SetRowLabelValue(8,_('Annual consumption [MWh]'))

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
        fuelName = str(self.tc1.GetValue(text=True))
        dbfuels = Status.DB.dbfuel.FuelName[fuelName]
        if len(dbfuels) > 0:
            dbfid = dbfuels[0].DBFuel_ID
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
                self.main.showError("Fuel name has to be a unique value!")

    def storeElectricityData(self):
        if Status.PId <> 0:
            if len(Status.DB.qelectricity.Questionnaire_id[Status.PId]) == 0:
                tmp = {
                    "Questionnaire_id":Status.PId,
                    "AlternativeProposalNo":Status.ANo,
                    "PowerContrTot":check(self.grid.GetCellValue(1, 3)),
                    "PowerContrStd":check(self.grid.GetCellValue(1, 1)),
                    "PowerContrPeak":check(self.grid.GetCellValue(1, 0)),
                    "PowerContrVall":check(self.grid.GetCellValue(1, 2)),
                    "ElectricityTotYear":check(self.grid.GetCellValue(0, 3)),
                    "ElectricityPeakYear":check(self.grid.GetCellValue(0, 0)),
                    "ElectricityStandYear":check(self.grid.GetCellValue(0, 1)),
                    "ElectricityValleyYear":check(self.grid.GetCellValue(0, 2)),
                    "ElGenera":check(self.grid.GetCellValue(0, 4)),
                    "ElSales":check(self.grid.GetCellValue(0, 5)),
                    "ElectricityRef":check(self.grid.GetCellValue(8, 0)),
                    "ElectricityAC":check(self.grid.GetCellValue(8, 1)),
                    "ElectricityThOther":check(self.grid.GetCellValue(8, 2)),
                    "ElectricityMotors":check(self.grid.GetCellValue(8, 3)),
                    "ElectricityChem":check(self.grid.GetCellValue(8, 4)),
                    "ElectricityLight":check(self.grid.GetCellValue(8, 5)),
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
                
                Status.DB.qelectricity.insert(tmp)
                Status.SQL.commit()                      

            elif len(Status.DB.qelectricity.Questionnaire_id[Status.PId]) == 1:
                q = Status.DB.qelectricity.Questionnaire_id[Status.PId][0]
                tmp = {                    
                    "PowerContrTot":check(self.grid.GetCellValue(1, 3)),
                    "PowerContrStd":check(self.grid.GetCellValue(1, 1)),
                    "PowerContrPeak":check(self.grid.GetCellValue(1, 0)),
                    "PowerContrVall":check(self.grid.GetCellValue(1, 2)),
                    "ElectricityTotYear":check(self.grid.GetCellValue(0, 3)),
                    "ElectricityPeakYear":check(self.grid.GetCellValue(0, 0)),
                    "ElectricityStandYear":check(self.grid.GetCellValue(0, 1)),
                    "ElectricityValleyYear":check(self.grid.GetCellValue(0, 2)),
                    "ElGenera":check(self.grid.GetCellValue(0, 4)),
                    "ElSales":check(self.grid.GetCellValue(0, 5)),
                    "ElectricityRef":check(self.grid.GetCellValue(8, 0)),
                    "ElectricityAC":check(self.grid.GetCellValue(8, 1)),
                    "ElectricityThOther":check(self.grid.GetCellValue(8, 2)),
                    "ElectricityMotors":check(self.grid.GetCellValue(8, 3)),
                    "ElectricityChem":check(self.grid.GetCellValue(8, 4)),
                    "ElectricityLight":check(self.grid.GetCellValue(8, 5)),
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
            self.selectedFuelName = str(self.fuelListBox.GetStringSelection())
            self.selectedFuelID = Status.DB.dbfuel.FuelName[self.selectedFuelName][0].DBFuel_ID
            q = Status.DB.qfuel.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].DBFuel_id[self.selectedFuelID][0]
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

	if len(Status.DB.qelectricity.Questionnaire_id[Status.PId]) > 0:
	    
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
        print "PanelQ2: Trying to fill fuel list"
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
