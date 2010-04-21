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
#    PanelDBHeatPump: Database Design Assistant
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

from einstein.GUI.DBEditFrame import *

HEIGHT = 20
LABEL_WIDTH_LEFT = 140
DATA_ENTRY_WIDTH_LEFT = 195
UNITS_WIDTH = 0

VSEP = 4

def _U(text):
    return unicode(_(text), "utf-8")

class PanelDBHeatPumpNew(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self._init_ctrls(parent)
        self.__do_layout()
#        self.fillEquipmentList()

    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id = -1, name = 'PanelDBHeatPump', parent = parent,
              pos = wx.Point(0, 0), size = wx.Size(780, 580))
        self.Hide()

        # access to font properties object
        fp = FontProperties()

        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)

        self.notebook = wx.Notebook(self, -1, style = 0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page0, _U('Descriptive Data'))
        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page1, _U('Technical Data'))
        self.page2 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page2, _U('Heat source / sink'))
        self.page3 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page3, _U('Economic Parameters'))

        self.frame_descriptive_data = wx.StaticBox(self.page0, -1, _U("Descriptive data"))
        self.frame_equipment_list = wx.StaticBox(self.page0, -1, _U("List of heatpumps"))

        #
        # left tab controls
        # tab 0 - Descriptive Data
        #
#        self.frame1 = wx.StaticBox(id = wx.ID_ANY,
#              label = "Descriptive Data", name = 'frame1', parent = self)
#
#        self.frame1.SetForegroundColour(TITLE_COLOR)
#        self.frame1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
#
#        self.frame2 = wx.StaticBox(id = wxID_PANEL1STATICBOX2,
#              label = "List of heatpumps", name = 'frame2', parent = self)
#
#        self.frame2.SetForegroundColour(TITLE_COLOR)
#        self.frame2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

#        self.listBoxEquipment = wx.ListBox(choices = [], id = wxID_PANEL1LISTBOX1,
#              name = 'listBoxEquipment', parent = self)

        fp.pushFont()
        fp.changeFont(size = TYPE_SIZE_TITLES, weight = wx.BOLD)
#        self.frame1.SetFont(fp.getFont())
#        self.frame2.SetFont(fp.getFont())
        fp.popFont()

        fp.pushFont()
        fp.changeFont(size = TYPE_SIZE_LEFT)

        # right side: entries
        self.tc1 = TextEntry(self.page0, maxchars = 45, value = '',
                             label = _U("HPManufacturer"),
                             tip = _U("Heatpump Manufacturer"))

        self.tc2 = TextEntry(self.page0, maxchars = 45, value = '',
                             label = _U("HPModel"),
                             tip = _U("Heatpump Model"))

        self.tc3 = TextEntry(self.page0, maxchars = 45, value = '',
                             label = _U("HPType"),
                             tip = _U("Heatpump Type"))

        self.tc4 = TextEntry(self.page0, maxchars = 45, value = '',
                             label = _U("HPSubType"),
                             tip = _U("Heatpump Sub Type"))

        self.tc5 = TextEntry(self.page0, maxchars = 200, value = '',
                             label = _U("Reference"),
                             tip = _U("Source of data"))


        #
        # middle left tab controls
        # tab 1 - Technical data
        #
#        fs = FieldSizes(wHeight = HEIGHT, wLabel = 100,
#                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)
#
#        self.tc6 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPHeatCap"),
#                              tip = _U("Nominal heating capacity"))
#
#        self.tc7 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPHeatCOP"),
#                              tip = _U("Nominal COP for heating mode"))
#
#        self.tc8 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPCoolCap"),
#                              tip = _U("Nominal cooling capacity"))
#
#        self.tc9 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPCoolCOP"),
#                              tip = _U("Nominal COP for cooling mode"))
#
#        self.tc10 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPFuelConsum"),
#                              tip = _U("Nominal fuel consumption"))
#
#        self.tc11 = ChoiceEntry(self.page1,
#                               values = [],
#                               label = _U("FuelType"),
#                               tip = _U("Fuel type"))
#
#        self.tc12 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPElectConsum"),
#                              tip = _U("Nominal electrical power consumption"))
#
#        self.tc13 = TextEntry(self.page1, maxchars = 45, value = '',
#                             label = _U("HPWorkFluid"),
#                             tip = _U("Refrigerant / absorbent refrigerant pair"))
#
#        self.tc14 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPCondTinC"),
#                              tip = _U("inlet temperature to the condenser (and absorber)"))
#
#        self.tc15 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPGenTinC"),
#                              tip = _U("inlet temperature to the generator"))
#
#        self.tc16 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPEvapTinC"),
#                              tip = _U("inlet temperature to the evaporator"))
#
#        self.tc17 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPConstExCoolCOP"),
#                              tip = _U("Temperature range around the nominal temperatures for which the constant exergetic COP approximation is valid (e.g. +-20 K)"))
#
#        self.tc18 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPCondTinH"),
#                              tip = _U("inlet temperature to the condenser (and absorber)"))
#
#        self.tc19 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPGenTinH"),
#                              tip = _U("inlet temperature to the generator"))
#
#        self.tc20 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPEvapTinH"),
#                              tip = _U("inlet temperature to the evaporator"))
#
#        self.tc21 = FloatEntry(self.page1,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPConstExHeatCOP"),
#                              tip = _U("Temperature range around the nominal temperatures for which the constant exergetic COP approximation is valid (e.g. +-20 K)"))
#
#        self.tc22 = StaticTextEntry(self.page1, maxchars = 255, value = '',
#                              label = _U("HPExCoolCOP"),
#                              tip = _U("Calculated from the nominal and theoretical COP at the manufact. catalogue nominal conditions and applied as a constant in extrapolation for other working conditions (see next point)."))
#
#        self.tc23 = StaticTextEntry(self.page1, maxchars = 255, value = '',
#                              label = _U("HPThCoolCOP"),
#                              tip = _U("Carnot COP for cooling mode at nominal conditions (see next point)."))
#
#        self.tc24 = StaticTextEntry(self.page1, maxchars = 255, value = '',
#                              label = _U("HPExHeatCOP"),
#                              tip = _U("Calculated from the nominal and theoretical COP at the manufact. catalogue nominal conditions and applied as a constant in extrapolation for other working conditions (see next point)."))
#
#        self.tc25 = StaticTextEntry(self.page1, maxchars = 255, value = '',
#                              label = _U("HPThHeatCOP"),
#                              tip = _U("Carnot COP for heating mode at nominal conditions (see next point)."))
#
#        fs = FieldSizes(wHeight = HEIGHT, wLabel = LABEL_WIDTH_LEFT,
#                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)
#
#        #
#        # middle right tab controls
#        # tab 2. Heat source / sink
#        #
#        self.tc26 = ChoiceEntry(self.page2,
#                               values = [],
#                               label = _U("HPSourceSink"),
#                               tip = _U("Heat source and sink"))
#
#        self.tc27 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPLimDT"),
#                              tip = _U("Maximum acceptable temperature difference between evaporator and condenser temperatures (primary fluid: Tco - Tev) - working limit"))
#
#        self.tc28 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPCondTmax"),
#                              tip = _U("Maximum condensing (and absorption) temperature (primary fluid) - working limit"))
#
#        self.tc29 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPEvapTmin"),
#                              tip = _U("Minimum evaporating temperature (primary fluid) - working limit"))
#
#        self.tc30 = ChoiceEntry(self.page2,
#                               values = [],
#                               label = _U("HPAbsHeatMed"),
#                               tip = _U("Heat transport medium used for heat supply to the generator"))
#
#        self.tc31 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPGenTmin"),
#                              tip = _U("Minimum required inlet temperature to the generator"))
#
#        #
#        # right tab controls
#        # panel 3. Economic Parameters
#        #
#        self.tc32 = FloatEntry(self.page3,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPPrice"),
#                              tip = _U("Equipment price at factory applied installer's discount"))
#
#        self.tc33 = FloatEntry(self.page3,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPTurnKeyPrice"),
#                              tip = _U("Price of installed equipment (including work, additional accessories, pumps, regulation, etc)"))
#
#        self.tc34 = FloatEntry(self.page3,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPOandMfix"),
#                              tip = _U("Annual operational and maintenance fixed costs (approximate average per kW heating)"))
#
#        self.tc35 = FloatEntry(self.page3,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPOandMvar"),
#                              tip = _U("Annual operational and maintenance variable costs dependant on usage (approximate average per MWh heating)"))
#
#        self.tc36 = FloatEntry(self.page3,
#                               ipart = 4, decimals = 0, minval = 1900, maxval = 2100, value = 2010,
#                               label = _U("HPYearUpdate"),
#                               tip = _U("Year of last update of the economic data"))

        #
        # buttons
        #
        self.buttonAddEquipment = wx.Button(self, -1, label = _U("Add equipment"))
        self.buttonDeleteEquipment = wx.Button(self, -1, label = _U("Delete equipment"))
        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, label = 'Cancel')
        self.buttonOK = wx.Button(self, wx.ID_OK, label = 'OK')
        self.buttonOK.SetDefault()

#        self.Bind(wx.EVT_BUTTON, self.OnButtonAddEquipment, self.page0.button1)
#        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteEquipment, self.page0.button2)
#        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)
#        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
#        self.Bind(wx.EVT_LISTBOX, self.OnListBoxEquipmentClick, self.page0.listBoxEquipment)
#        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged, self.notebook)

    def __do_layout(self):
        flagText = wx.TOP

        bla = DBEditFrame(None, "Edit DBCHP", 'dbchp', 0, True)

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)

        sizerPage0 = wx.StaticBoxSizer(self.frame_descriptive_data, wx.HORIZONTAL)

        sizerPage0Left = wx.StaticBoxSizer(self.frame_equipment_list, wx.VERTICAL)
        
        #sizerPage0Left.Add(self.listBoxEquipment, 1, wx.EXPAND, 0)
        #sizerPage0Left.Add(self.buttonAddEquipment, 0, wx.ALIGN_RIGHT | wx.TOP, 4)
        #sizerPage0Left.Add(self.buttonDeleteEquipment, 0, wx.ALIGN_RIGHT | wx.TOP, 4)

        sizerPage0Right = wx.BoxSizer(wx.VERTICAL)
        sizerPage0Right.Add(self.tc1, 0, flagText, VSEP)
        sizerPage0Right.Add(self.tc2, 0, flagText, VSEP)
        sizerPage0Right.Add(self.tc3, 0, flagText, VSEP)
        sizerPage0Right.Add(self.tc4, 0, flagText, VSEP)
        sizerPage0Right.Add(self.tc5, 0, flagText, VSEP)

        sizerPage0.Add(sizerPage0Left, 0.5, wx.EXPAND | wx.TOP, 10)
        sizerPage0.Add(sizerPage0Right, 1, wx.EXPAND | wx.TOP, 10)

        self.page0.SetSizer(sizerPage0)

#        self.page1.addControl(self.tc6)
#        self.page1.addControl(self.tc7)
#        self.page1.addControl(self.tc8)
#        self.page1.addControl(self.tc9)
#        self.page1.addControl(self.tc10)
#        self.page1.addControl(self.tc11)
#        self.page1.addControl(self.tc12)
#        self.page1.addControl(self.tc13)
#
#        self.page1.addControlBottomLeft(self.tc14)
#        self.page1.addControlBottomLeft(self.tc15)
#        self.page1.addControlBottomLeft(self.tc16)
#        self.page1.addControlBottomLeft(self.tc17)
#
#        self.page1.addControlBottomRight(self.tc18)
#        self.page1.addControlBottomRight(self.tc19)
#        self.page1.addControlBottomRight(self.tc20)
#        self.page1.addControlBottomRight(self.tc21)
#
#        self.page1.addControlBottomLeft(self.tc22)
#        self.page1.addControlBottomLeft(self.tc23)
#        self.page1.addControlBottomRight(self.tc24)
#        self.page1.addControlBottomRight(self.tc25)
#
#        self.page2.addControl(self.tc26)
#        self.page2.addControl(self.tc27)
#        self.page2.addControl(self.tc28)
#        self.page2.addControl(self.tc29)
#        self.page2.addControl(self.tc30)
#        self.page2.addControl(self.tc31)
#
#        self.page3.addControl(self.tc32)
#        self.page3.addControl(self.tc33)
#        self.page3.addControl(self.tc34)
#        self.page3.addControl(self.tc35)
#        self.page3.addControl(self.tc36)
#
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel.Add(self.buttonCancel, 1, wx.EXPAND, 0)
        sizerOKCancel.Add(self.buttonOK, 1, wx.EXPAND | wx.LEFT, 4)
#
        sizerGlobal.Add(self.notebook, 1, wx.EXPAND, 0)
        sizerGlobal.Add(sizerOKCancel, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizerGlobal)
        self.Layout()
        self.Show()













    def display(self):
        pass
