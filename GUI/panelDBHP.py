# -*- coding: iso-8859-15 -*-
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    PanelDBHP: Database Design Assistant
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by:     Manuel Wallner 08/03/2010
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
import pSQL
from status import Status
from displayClasses import *
from GUITools import *
from units import *
from fonts import *
from einstein.modules.messageLogger import *
from einstein.GUI.panelBaseDBEditor import *

def _U(text):
    return unicode(_(text),"utf-8")

class PanelDBHP(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self._init_ctrls(parent)
        self.__do_layout()
        self.fillEquipmentList()

    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelDBHP', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580))
        self.Hide()

        # access to font properties object
        fp = FontProperties()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = PanelBaseDBEditor(self.notebook, 'Descriptive Data', 'List of heatpumps',
                                       'Add Equipment', 'Delete Equipment')

        self.page1 = PanelBaseDBEditor(self.notebook, 'Technical Data', 'List of heatpumps',
                                       'Add Equipment', 'Delete Equipment')

        self.page2 = PanelBaseDBEditor(self.notebook, 'Heat source / sink', 'List of heatpumps',
                                       'Add Equipment', 'Delete Equipment')

        self.page3 = PanelBaseDBEditor(self.notebook, 'Economic Parameters', 'List of heatpumps',
                                       'Add Equipment', 'Delete Equipment')

        self.notebook.AddPage(self.page0, _U('Descriptive Data'))
        self.notebook.AddPage(self.page1, _U('Technical Data'))
        self.notebook.AddPage(self.page2, _U('Heat source / sink'))
        self.notebook.AddPage(self.page3, _U('Economic Parameters'))

        #
        # left tab controls
        # tab 0 - Descriptive Data
        #
        # right side: entries
        self.tc1 = TextEntry(self.page0,maxchars=45,value='',
                             label=_U("HPManufacturer"),
                             tip=_U("Heatpump Manufacturer"))

        self.tc2 = TextEntry(self.page0,maxchars=45,value='',
                             label=_U("HPModel"),
                             tip=_U("Heatpump Model"))

        self.tc3 = TextEntry(self.page0,maxchars=45,value='',
                             label=_U("HPType"),
                             tip=_U("Heatpump Type"))

        self.tc4 = TextEntry(self.page0,maxchars=45,value='',
                             label=_U("HPSubType"),
                             tip=_U("Heatpump Sub Type"))

        self.tc5 = TextEntry(self.page0,maxchars=200,value='',
                             label=_U("Reference"),
                             tip=_U("Source of data"))

        #
        # middle left tab controls
        # tab 1 - Technical data
        #
        #fp.changeFont(size=TYPE_SIZE_MIDDLE)
#        f = FieldSizes(wHeight=HEIGHT_MIDDLE,wLabel=LABEL_WIDTH_MIDDLE)

        self.tc6 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPHeatCap"),
                              tip=_U("Nominal heating capacity"))

        self.tc7 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPHeatCOP"),
                              tip=_U("Nominal COP for heating mode"))

        self.tc8 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPCoolCap"),
                              tip=_U("Nominal cooling capacity"))

        self.tc9 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPCoolCOP"),
                              tip=_U("Nominal COP for cooling mode"))

        self.tc10 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPFuelConsum"),
                              tip=_U("Nominal fuel consumption"))

        self.tc11 = ChoiceEntry(self.page1,
                               values=[],
                               label=_U("FuelType"),
                               tip=_U("Fuel type"))

        self.tc12 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPElectConsum"),
                              tip=_U("Nominal electrical power consumption"))

        self.tc13 = TextEntry(self.page1,maxchars=45,value='',
                             label=_U("HPWorkFluid"),
                             tip=_U("Refrigerant / absorbent refrigerant pair"))

        self.tc14 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPCondTinC"),
                              tip=_U("inlet temperature to the condenser (and absorber)"))

        self.tc15 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPGenTinC"),
                              tip=_U("inlet temperature to the generator"))

        self.tc16 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPEvapTinC"),
                              tip=_U("inlet temperature to the evaporator"))

        self.tc17 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPConstExCoolCOP"),
                              tip=_U("Temperature range around the nominal temperatures for which the constant exergetic COP approximation is valid (e.g. +-20 K)"))

        self.tc18 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPCondTinH"),
                              tip=_U("inlet temperature to the condenser (and absorber)"))

        self.tc19 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPGenTinH"),
                              tip=_U("inlet temperature to the generator"))

        self.tc20 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPEvapTinH"),
                              tip=_U("inlet temperature to the evaporator"))

        self.tc21 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPConstExHeatCOP"),
                              tip=_U("Temperature range around the nominal temperatures for which the constant exergetic COP approximation is valid (e.g. +-20 K)"))

        self.tc22 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPExCoolCOP"),
                              tip=_U("Calculated from the nominal and theoretical COP at the manufact. catalogue nominal conditions and applied as a constant in extrapolation for other working conditions (see next point)."))

        self.tc23 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPThCoolCOP"),
                              tip=_U("Carnot COP for cooling mode at nominal conditions (see next point)."))

        self.tc24 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPExHeatCOP"),
                              tip=_U("Calculated from the nominal and theoretical COP at the manufact. catalogue nominal conditions and applied as a constant in extrapolation for other working conditions (see next point)."))

        self.tc25 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPThHeatCOP"),
                              tip=_U("Carnot COP for heating mode at nominal conditions (see next point)."))

        #
        # middle right tab controls
        # tab 2. Heat source / sink
        #
        self.tc26 = ChoiceEntry(self.page2,
                               values=[],
                               label=_U("HPSourceSink"),
                               tip=_U("Heat source and sink"))

        self.tc27 = FloatEntry(self.page2,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPLimDT"),
                              tip=_U("Maximum acceptable temperature difference between evaporator and condenser temperatures (primary fluid: Tco - Tev) - working limit"))

        self.tc28 = FloatEntry(self.page2,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPCondTmax"),
                              tip=_U("Maximum condensing (and absorption) temperature (primary fluid) - working limit"))

        self.tc29 = FloatEntry(self.page2,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPEvapTmin"),
                              tip=_U("Minimum evaporating temperature (primary fluid) - working limit"))

        self.tc30 = ChoiceEntry(self.page2,
                               values=[],
                               label=_U("HPAbsHeatMed"),
                               tip=_U("Heat transport medium used for heat supply to the generator"))

        self.tc31 = FloatEntry(self.page2,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPGenTmin"),
                              tip=_U("Minimum required inlet temperature to the generator"))

        #
        # right tab controls
        # panel 3. Economic Parameters
        #
        #fp.changeFont(size=TYPE_SIZE_RIGHT)
#        f = FieldSizes(wHeight=HEIGHT_RIGHT,wLabel=LABEL_WIDTH_RIGHT)

        self.tc32 = FloatEntry(self.page3,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPPrice"),
                              tip=_U("Equipment price at factory applied installer's discount"))

        self.tc33 = FloatEntry(self.page3,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPTurnKeyPrice"),
                              tip=_U("Price of installed equipment (including work, additional accessories, pumps, regulation, etc)"))

        self.tc34 = FloatEntry(self.page3,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPOandMfix"),
                              tip=_U("Annual operational and maintenance fixed costs (approximate average per kW heating)"))

        self.tc35 = FloatEntry(self.page3,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("HPOandMvar"),
                              tip=_U("Annual operational and maintenance variable costs dependant on usage (approximate average per MWh heating)"))

        self.tc36 = FloatEntry(self.page3,
                               ipart=4, decimals=0, minval=1900, maxval=2100, value=2010,
                               label=_U("HPYearUpdate"),
                               tip=_U("Year of last update of the economic data"))

        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, label='Cancel')
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        self.buttonOK = wx.Button(self, wx.ID_OK, label='OK')
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        #self.buttonOK.SetDefault()

        self.Bind(wx.EVT_BUTTON, self.OnButtonAddEquipment, self.page0.button1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteEquipment, self.page0.button2)
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxEquipmentClick, self.page0.listBoxEquipment)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged, self.notebook)

    def __do_layout(self):

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)

        self.page0.addControl(self.tc1)
        self.page0.addControl(self.tc2)
        self.page0.addControl(self.tc3)
        self.page0.addControl(self.tc4)
        self.page0.addControl(self.tc5)

        self.page1.addControl(self.tc6)
        self.page1.addControl(self.tc7)
        self.page1.addControl(self.tc8)
        self.page1.addControl(self.tc9)
        self.page1.addControl(self.tc10)
        self.page1.addControl(self.tc11)
        self.page1.addControl(self.tc12)
        self.page1.addControl(self.tc13)

        flagText = wx.TOP | wx.ALIGN_CENTER
        VSEP_LEFT= 2

        self.page1.addControl(self.tc14)
        self.page1.addControl(self.tc15)
        self.page1.addControl(self.tc16)
        self.page1.addControl(self.tc17)
        self.page1.addControl(self.tc18)
        self.page1.addControl(self.tc19)
        self.page1.addControl(self.tc20)
        self.page1.addControl(self.tc21)
        self.page1.addControl(self.tc22)
        self.page1.addControl(self.tc23)
        self.page1.addControl(self.tc24)
        self.page1.addControl(self.tc25)

        # prototype of 2-column layout
#        sizerP1NWCLeft = wx.BoxSizer(wx.VERTICAL)
#        sizerP1NWCLeft.Add(self.tc14, 0, flagText, VSEP_LEFT)
#        sizerP1NWCLeft.Add(self.tc15, 0, flagText, VSEP_LEFT)
#        sizerP1NWCLeft.Add(self.tc16, 0, flagText, VSEP_LEFT)
#        sizerP1NWCLeft.Add(self.tc17, 0, flagText, VSEP_LEFT)
#
#        sizerP1NWCRight = wx.BoxSizer(wx.VERTICAL)
#        sizerP1NWCRight.Add(self.tc18, 0, flagText, VSEP_LEFT)
#        sizerP1NWCRight.Add(self.tc19, 0, flagText, VSEP_LEFT)
#        sizerP1NWCRight.Add(self.tc20, 0, flagText, VSEP_LEFT)
#        sizerP1NWCRight.Add(self.tc21, 0, flagText, VSEP_LEFT)
#
#        sizerNominalWorkingConditions = wx.BoxSizer(wx.HORIZONTAL)
#        sizerNominalWorkingConditions.Add(sizerP1NWCLeft, 0, flagText, VSEP_LEFT)
#        sizerNominalWorkingConditions.Add(sizerP1NWCRight, 0, flagText, VSEP_LEFT)
#
#        self.page1.addControl(sizerNominalWorkingConditions)
#
#        sizerP1ELeft = wx.BoxSizer(wx.VERTICAL)
#        sizerP1ELeft.Add(self.tc22, 0, flagText, VSEP_LEFT)
#        sizerP1ELeft.Add(self.tc23, 0, flagText, VSEP_LEFT)
#
#        sizerP1ERight = wx.BoxSizer(wx.VERTICAL)
#        sizerP1ERight.Add(self.tc24, 0, flagText, VSEP_LEFT)
#        sizerP1ERight.Add(self.tc25, 0, flagText, VSEP_LEFT)
#
#        sizerEfficiency = wx.BoxSizer(wx.HORIZONTAL)
#        sizerEfficiency.Add(sizerP1ELeft, 0, flagText, VSEP_LEFT)
#        sizerEfficiency.Add(sizerP1ERight, 0, flagText, VSEP_LEFT)
#
#        self.page1.addControl(sizerEfficiency)

        self.page2.addControl(self.tc26)
        self.page2.addControl(self.tc27)
        self.page2.addControl(self.tc28)
        self.page2.addControl(self.tc29)
        self.page2.addControl(self.tc30)
        self.page2.addControl(self.tc31)

        self.page3.addControl(self.tc32)
        self.page3.addControl(self.tc33)
        self.page3.addControl(self.tc34)
        self.page3.addControl(self.tc35)
        self.page3.addControl(self.tc36)

        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.EXPAND, 0)
        sizerOKCancel.Add(self.buttonOK, 0, wx.EXPAND | wx.LEFT, 4)

        sizerGlobal.Add(self.notebook, 1, wx.EXPAND, 0)
        sizerGlobal.Add(sizerOKCancel, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizerGlobal)
        self.Layout()
        self.Show()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------

    def OnButtonAddEquipment(self, event):
        self.clear()
        self.page0.listBoxEquipment.DeselectAll()
        self.page1.listBoxEquipment.DeselectAll()
        self.page2.listBoxEquipment.DeselectAll()
        self.page3.listBoxEquipment.DeselectAll()
        self.notebook.ChangeSelection(0)

    def OnButtonDeleteEquipment(self, event):
        self.equipeName = self.page0.listBoxEquipment.GetStringSelection()
        logTrack("PanelDBHP (DELETE Button): deleting heatpump ID %s"%self.equipeName)

        sqlQuery = "SELECT * FROM dbheatpump WHERE DBHeatPump_ID = '%s'"%self.equipeName
        result = Status.DB.sql_query(sqlQuery)

        if len(result) > 0:
            sqlQuery = "DELETE FROM dbheatpump WHERE DBHeatPump_ID = '%s'"%self.equipeName
            Status.DB.sql_query(sqlQuery)

        self.clearPage0()

    def OnButtonCancel(self, event):
        self.clearPage0()

    def OnButtonOK(self, event):
        if self.allFieldsEmpty():
            return

        tmp = {
               "HPManufacturer":check(self.tc1.GetValue()),
               "HPModel":check(self.tc2.GetValue()),
               "HPType":check(self.tc3.GetValue()),
               "HPSubType":check(self.tc4.GetValue()),
#               "Reference":check(self.tc5.GetValue()),
               "HPHeatCap":check(self.tc6.GetValue()),
               "HPHeatCOP":check(self.tc7.GetValue()),
               "HPCoolCap":check(self.tc8.GetValue()),
               "HPCoolCOP":check(self.tc9.GetValue()),
               "HPFuelConsum":check(self.tc10.GetValue()),
#               "FuelType":check(self.tc11.GetValue()),
               "HPElectConsum":check(self.tc12.GetValue()),
               "HPWorkFluid":check(self.tc13.GetValue()),
               "HPCondTinC":check(self.tc14.GetValue()),
               "HPGenTinC":check(self.tc15.GetValue()),
               "HPEvapTinC":check(self.tc16.GetValue()),
               "HPConstExCoolCOP":check(self.tc17.GetValue()),
               "HPCondTinH":check(self.tc18.GetValue()),
               "HPGenTinH":check(self.tc19.GetValue()),
               "HPEvapTinH":check(self.tc20.GetValue()),
               "HPConstExHeatCOP":check(self.tc21.GetValue()),
               "HPExCoolCOP":check(self.tc22.GetValue()),
               "HPThCoolCOP":check(self.tc23.GetValue()),
               "HPExHeatCOP":check(self.tc24.GetValue()),
               "HPThHeatCOP":check(self.tc25.GetValue()),
#               "HPSourceSink":check(self.tc26.GetValue()),
               "HPLimDT":check(self.tc27.GetValue()),
               "HPCondTmax":check(self.tc28.GetValue()),
               "HPEvapTmin":check(self.tc29.GetValue()),
               "HPAbsHeatMed":check(self.tc30.GetValue()),
               "HPGenTmin":check(self.tc31.GetValue()),
               "HPPrice":check(self.tc32.GetValue()),
               "HPTurnKeyPrice":check(self.tc33.GetValue()),
               "HPOandMfix":check(self.tc34.GetValue()),
               "HPOandMvar":check(self.tc35.GetValue()),
               "HPYearUpdate":check(self.tc36.GetValue())
            }
        if len(self.page0.listBoxEquipment.GetSelections()) +\
           len(self.page1.listBoxEquipment.GetSelections()) +\
           len(self.page2.listBoxEquipment.GetSelections()) +\
           len(self.page3.listBoxEquipment.GetSelections()) == 0:
            retval = Status.DB.dbheatpump.insert(tmp)
            self.fillEquipmentList()
            self.page0.listBoxEquipment.SetStringSelection(str(retval))
        else:
            self.equipeName = self.page0.listBoxEquipment.GetStringSelection()
            equipments = Status.DB.dbheatpump.DBHeatPump_ID[check(self.equipeName)]

            if len(equipments) > 0:
                equipe = equipments[0]

            equipe.update(tmp)
            self.page0.listBoxEquipment.SetStringSelection(str(self.equipeName))

    def OnListBoxEquipmentClick(self, event):
        self.equipeName = event.String
        self.page0.listBoxEquipment.SetStringSelection(self.equipeName)
        self.page1.listBoxEquipment.SetStringSelection(self.equipeName)
        self.page2.listBoxEquipment.SetStringSelection(self.equipeName)
        self.page3.listBoxEquipment.SetStringSelection(self.equipeName)

        equipments = Status.DB.dbheatpump.DBHeatPump_ID[check(self.equipeName)]

        if len(equipments) > 0:
            equipe = equipments[0]
        else:
            logDebug("PanelDB (ListBoxClick): equipe %s not found in database"%self.equipeName)
            return

        self.display(equipe)
        event.Skip()

    def OnNotebookPageChanged(self, event):
        old = event.OldSelection
        selection = ''

        if old == 0:
            selection = self.page0.listBoxEquipment.GetStringSelection()
        elif old == 1:
            selection = self.page1.listBoxEquipment.GetStringSelection()
        if old == 2:
            selection = self.page2.listBoxEquipment.GetStringSelection()
        elif old == 3:
            selection = self.page3.listBoxEquipment.GetStringSelection()

        self.page0.listBoxEquipment.SetStringSelection(selection)
        self.page1.listBoxEquipment.SetStringSelection(selection)
        self.page2.listBoxEquipment.SetStringSelection(selection)
        self.page3.listBoxEquipment.SetStringSelection(selection)

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------

    def display(self,q=None):
        self.clear()

        if q is not None:
            self.tc1.SetValue(q.HPManufacturer) if q.HPManufacturer is not None else ''
            self.tc2.SetValue(q.HPModel) if q.HPModel is not None else ''
            self.tc3.SetValue(q.HPType) if q.HPType is not None else ''
            self.tc4.SetValue(str(q.HPSubType)) if q.HPSubType is not None else ''
#            self.tc5.SetValue(str(q.Reference)) if q.Reference is not None else ''
            self.tc6.SetValue(str(q.HPHeatCap)) if q.HPHeatCap is not None else ''
            self.tc7.SetValue(str(q.HPHeatCOP)) if q.HPHeatCOP is not None else ''
            self.tc8.SetValue(str(q.HPCoolCap)) if q.HPCoolCap is not None else ''
            self.tc9.SetValue(str(q.HPCoolCOP)) if q.HPCoolCOP is not None else ''
            self.tc10.SetValue(str(q.HPFuelConsum)) if q.HPFuelConsum is not None else ''
#            self.tc11.SetValue(str(q.FuelType)) if q.FuelType is not None else ''
            self.tc12.SetValue(str(q.HPElectConsum)) if q.HPElectConsum is not None else ''
            self.tc13.SetValue(str(q.HPWorkFluid)) if q.HPWorkFluid is not None else ''
            self.tc14.SetValue(str(q.HPCondTinC)) if q.HPCondTinC is not None else ''
            self.tc15.SetValue(str(q.HPGenTinC)) if q.HPGenTinC is not None else ''
            self.tc16.SetValue(str(q.HPEvapTinC)) if q.HPEvapTinC is not None else ''
            self.tc17.SetValue(str(q.HPConstExCoolCOP)) if q.HPConstExCoolCOP is not None else ''
            self.tc18.SetValue(str(q.HPCondTinH)) if q.HPCondTinH is not None else ''
            self.tc19.SetValue(str(q.HPGenTinH)) if q.HPGenTinH is not None else ''
            self.tc20.SetValue(str(q.HPEvapTinH)) if q.HPEvapTinH is not None else ''
            self.tc21.SetValue(str(q.HPConstExHeatCOP)) if q.HPConstExHeatCOP is not None else ''
            self.tc22.SetValue(str(q.HPExCoolCOP)) if q.HPExCoolCOP is not None else ''
            self.tc23.SetValue(str(q.HPThCoolCOP)) if q.HPThCoolCOP is not None else ''
            self.tc24.SetValue(str(q.HPExHeatCOP)) if q.HPExHeatCOP is not None else ''
            self.tc25.SetValue(str(q.HPThHeatCOP)) if q.HPThHeatCOP is not None else ''
#            self.tc26.SetValue(str(q.HPSourceSink)) if q.HPSourceSink is not None else ''
            self.tc27.SetValue(str(q.HPLimDT)) if q.HPLimDT is not None else ''
            self.tc28.SetValue(str(q.HPCondTmax)) if q.HPCondTmax is not None else ''
            self.tc29.SetValue(str(q.HPEvapTmin)) if q.HPEvapTmin is not None else ''
            self.tc30.SetValue(str(q.HPAbsHeatMed)) if q.HPAbsHeatMed is not None else ''
            self.tc31.SetValue(str(q.HPGenTmin)) if q.HPGenTmin is not None else ''
            self.tc32.SetValue(str(q.HPPrice)) if q.HPPrice is not None else ''
            self.tc33.SetValue(str(q.HPTurnKeyPrice)) if q.HPTurnKeyPrice is not None else ''
            self.tc34.SetValue(str(q.HPOandMfix)) if q.HPOandMfix is not None else ''
            self.tc35.SetValue(str(q.HPOandMvar)) if q.HPOandMvar is not None else ''
            self.tc36.SetValue(str(q.HPYearUpdate)) if q.HPYearUpdate is not None else ''
        self.Show()

    def clear(self):
        self.tc1.SetValue('')
        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
        self.tc6.SetValue('')
        self.tc7.SetValue('')
        self.tc8.SetValue('')
        self.tc9.SetValue('')
        self.tc10.SetValue('')
        self.tc11.SetValue('')
        self.tc12.SetValue('')
        self.tc13.SetValue('')
        self.tc14.SetValue('')
        self.tc15.SetValue('')
        self.tc16.SetValue('')
        self.tc17.SetValue('')
        self.tc18.SetValue('')
        self.tc19.SetValue('')
        self.tc20.SetValue('')
        self.tc21.SetValue('')
        self.tc22.SetValue('')
        self.tc23.SetValue('')
        self.tc24.SetValue('')
        self.tc25.SetValue('')
        self.tc26.SetValue('')
        self.tc27.SetValue('')
        self.tc28.SetValue('')
        self.tc29.SetValue('')
        self.tc30.SetValue('')
        self.tc31.SetValue('')
        self.tc32.SetValue('')
        self.tc33.SetValue('')
        self.tc34.SetValue('')
        self.tc35.SetValue('')
        self.tc36.SetValue('')

    def fillEquipmentList(self):
        self.page0.clearListBox()
        self.page1.clearListBox()
        self.page2.clearListBox()
        self.page3.clearListBox()

        equipments = Status.DB.dbheatpump.get_table()

        for equipe in equipments:
            self.page0.addListBoxElement(equipe.DBHeatPump_ID)
            self.page1.addListBoxElement(equipe.DBHeatPump_ID)
            self.page2.addListBoxElement(equipe.DBHeatPump_ID)
            self.page3.addListBoxElement(equipe.DBHeatPump_ID)

    def clearPage0(self):
        self.clear()
        self.page0.listBoxEquipment.DeselectAll()
        self.page1.listBoxEquipment.DeselectAll()
        self.page2.listBoxEquipment.DeselectAll()
        self.page3.listBoxEquipment.DeselectAll()
        self.fillEquipmentList()
        self.notebook.ChangeSelection(0)

    def allFieldsEmpty(self):
        if len(self.tc1.GetValue()) == 0 and\
           len(self.tc2.GetValue()) == 0 and\
           len(self.tc3.GetValue()) == 0 and\
           len(self.tc4.GetValue()) == 0 and\
           len(self.tc5.GetValue()) == 0 and\
           self.tc6.GetValue() is None and\
           self.tc7.GetValue() is None and\
           self.tc8.GetValue() is None and\
           self.tc9.GetValue() is None and\
           self.tc10.GetValue() is None and\
           self.tc11.GetValue() < 0 and\
           self.tc12.GetValue() is None and\
           len(self.tc13.GetValue()) == 0 and\
           self.tc14.GetValue() is None and\
           self.tc15.GetValue() is None and\
           self.tc16.GetValue() is None and\
           self.tc17.GetValue() is None and\
           self.tc18.GetValue() is None and\
           self.tc19.GetValue() is None and\
           self.tc20.GetValue() is None and\
           self.tc21.GetValue() is None and\
           self.tc22.GetValue() is None and\
           self.tc23.GetValue() is None and\
           self.tc24.GetValue() is None and\
           self.tc25.GetValue() is None and\
           self.tc26.GetValue() < 0 and\
           self.tc27.GetValue() is None and\
           self.tc28.GetValue() is None and\
           self.tc29.GetValue() is None and\
           self.tc30.GetValue() < 0 and\
           self.tc31.GetValue() is None and\
           self.tc32.GetValue() is None and\
           self.tc33.GetValue() is None and\
           self.tc34.GetValue() is None and\
           self.tc35.GetValue() is None and\
           self.tc36.GetValue() is None:
            return True
        else:
            return False
