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
#from einstein.GUI.panelBaseDBEditor import *

#from einstein.GUI.DBEditFrame import *

HEIGHT = 20
LABEL_WIDTH_LEFT = 140
DATA_ENTRY_WIDTH_LEFT = 195
UNITS_WIDTH = 0

VSEP = 4

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

colLabels = "HPManufacturer", "HPModel", "HPType", "HPSubType", "HPSourceSink"#, "Reference", "HPWorkFluid"

class PanelDBHeatPumpNew(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self._init_ctrls(parent)
        self._init_grid()
        self.__do_layout()
#        self.grid.AutoSize()
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
        self.notebook.AddPage(self.page0, _U('Summary table'))
        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page1, _U('Descriptive Data'))
        self.page2 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page2, _U('Technical Data'))
        self.page3 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page3, _U('Heat source / sink'))
        self.page4 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page4, _U('Economic Parameters'))

        #self.frame_summary_table = wx.StaticBox(self.page0, -1, _U("Summary table"))
        self.frame_descriptive_data = wx.StaticBox(self.page1, -1, _U("Descriptive data"))
#        self.frame_equipment_list = wx.StaticBox(self.page1, -1, _U("List of heatpumps"))

        #
        # tab 0 - Summary table
        #
        self.grid = wx.grid.Grid(name = 'summarytable', parent = self.page0,
                                 pos = wx.Point(42, 32), style = 0)#, size = wx.Size(500, 300))

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
#        fp.changeFont(size = TYPE_SIZE_TITLES, weight = wx.BOLD)
#        self.frame1.SetFont(fp.getFont())
#        self.frame2.SetFont(fp.getFont())
        fp.popFont()

        fp.pushFont()
#        fp.changeFont(size = TYPE_SIZE_LEFT)

        # right side: entries
        self.tc1 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("HPManufacturer"),
                             tip = _U("Heatpump Manufacturer"))

        self.tc2 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("HPModel"),
                             tip = _U("Heatpump Model"))

        self.tc3 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("HPType"),
                             tip = _U("Heatpump Type"))

        self.tc4 = TextEntry(self.page1, maxchars = 45, value = '',
                             label = _U("HPSubType"),
                             tip = _U("Heatpump Sub Type"))

        self.tc5 = TextEntry(self.page1, maxchars = 200, value = '',
                             label = _U("Reference"),
                             tip = _U("Source of data"))


        #
        # middle left tab controls
        # tab 1 - Technical data
        #
#        fs = FieldSizes(wHeight = HEIGHT, wLabel = 100,
#                        wData = DATA_ENTRY_WIDTH_LEFT, wUnits = UNITS_WIDTH)
#
#        self.tc6 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPHeatCap"),
#                              tip = _U("Nominal heating capacity"))
#
#        self.tc7 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPHeatCOP"),
#                              tip = _U("Nominal COP for heating mode"))
#
#        self.tc8 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPCoolCap"),
#                              tip = _U("Nominal cooling capacity"))
#
#        self.tc9 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPCoolCOP"),
#                              tip = _U("Nominal COP for cooling mode"))
#
#        self.tc10 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPFuelConsum"),
#                              tip = _U("Nominal fuel consumption"))
#
#        self.tc11 = ChoiceEntry(self.page2,
#                               values = [],
#                               label = _U("FuelType"),
#                               tip = _U("Fuel type"))
#
#        self.tc12 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPElectConsum"),
#                              tip = _U("Nominal electrical power consumption"))
#
#        self.tc13 = TextEntry(self.page2, maxchars = 45, value = '',
#                             label = _U("HPWorkFluid"),
#                             tip = _U("Refrigerant / absorbent refrigerant pair"))
#
#        self.tc14 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPCondTinC"),
#                              tip = _U("inlet temperature to the condenser (and absorber)"))
#
#        self.tc15 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPGenTinC"),
#                              tip = _U("inlet temperature to the generator"))
#
#        self.tc16 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPEvapTinC"),
#                              tip = _U("inlet temperature to the evaporator"))
#
#        self.tc17 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPConstExCoolCOP"),
#                              tip = _U("Temperature range around the nominal temperatures for which the constant exergetic COP approximation is valid (e.g. +-20 K)"))
#
#        self.tc18 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPCondTinH"),
#                              tip = _U("inlet temperature to the condenser (and absorber)"))
#
#        self.tc19 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPGenTinH"),
#                              tip = _U("inlet temperature to the generator"))
#
#        self.tc20 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPEvapTinH"),
#                              tip = _U("inlet temperature to the evaporator"))
#
#        self.tc21 = FloatEntry(self.page2,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPConstExHeatCOP"),
#                              tip = _U("Temperature range around the nominal temperatures for which the constant exergetic COP approximation is valid (e.g. +-20 K)"))
#
#        self.tc22 = StaticTextEntry(self.page2, maxchars = 255, value = '',
#                              label = _U("HPExCoolCOP"),
#                              tip = _U("Calculated from the nominal and theoretical COP at the manufact. catalogue nominal conditions and applied as a constant in extrapolation for other working conditions (see next point)."))
#
#        self.tc23 = StaticTextEntry(self.page2, maxchars = 255, value = '',
#                              label = _U("HPThCoolCOP"),
#                              tip = _U("Carnot COP for cooling mode at nominal conditions (see next point)."))
#
#        self.tc24 = StaticTextEntry(self.page2, maxchars = 255, value = '',
#                              label = _U("HPExHeatCOP"),
#                              tip = _U("Calculated from the nominal and theoretical COP at the manufact. catalogue nominal conditions and applied as a constant in extrapolation for other working conditions (see next point)."))
#
#        self.tc25 = StaticTextEntry(self.page2, maxchars = 255, value = '',
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
#        self.tc26 = ChoiceEntry(self.page3,
#                               values = [],
#                               label = _U("HPSourceSink"),
#                               tip = _U("Heat source and sink"))
#
#        self.tc27 = FloatEntry(self.page3,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPLimDT"),
#                              tip = _U("Maximum acceptable temperature difference between evaporator and condenser temperatures (primary fluid: Tco - Tev) - working limit"))
#
#        self.tc28 = FloatEntry(self.page3,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPCondTmax"),
#                              tip = _U("Maximum condensing (and absorption) temperature (primary fluid) - working limit"))
#
#        self.tc29 = FloatEntry(self.page3,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPEvapTmin"),
#                              tip = _U("Minimum evaporating temperature (primary fluid) - working limit"))
#
#        self.tc30 = ChoiceEntry(self.page3,
#                               values = [],
#                               label = _U("HPAbsHeatMed"),
#                               tip = _U("Heat transport medium used for heat supply to the generator"))
#
#        self.tc31 = FloatEntry(self.page3,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPGenTmin"),
#                              tip = _U("Minimum required inlet temperature to the generator"))
#
#        #
#        # right tab controls
#        # panel 3. Economic Parameters
#        #
#        self.tc32 = FloatEntry(self.page4,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPPrice"),
#                              tip = _U("Equipment price at factory applied installer's discount"))
#
#        self.tc33 = FloatEntry(self.page4,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPTurnKeyPrice"),
#                              tip = _U("Price of installed equipment (including work, additional accessories, pumps, regulation, etc)"))
#
#        self.tc34 = FloatEntry(self.page4,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPOandMfix"),
#                              tip = _U("Annual operational and maintenance fixed costs (approximate average per kW heating)"))
#
#        self.tc35 = FloatEntry(self.page4,
#                              ipart = 6, decimals = 1, minval = 0., maxval = 1.e+12, value = 0.,
#                              label = _U("HPOandMvar"),
#                              tip = _U("Annual operational and maintenance variable costs dependant on usage (approximate average per MWh heating)"))
#
#        self.tc36 = FloatEntry(self.page4,
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

#        self.Bind(wx.EVT_BUTTON, self.OnButtonAddEquipment, self.page1.button1)
#        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteEquipment, self.page1.button2)
#        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)
#        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
#        self.Bind(wx.EVT_LISTBOX, self.OnListBoxEquipmentClick, self.page1.listBoxEquipment)
#        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged, self.notebook)

    def _init_grid(self):
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.grid.CreateGrid(0, len(colLabels))

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(20)
        self.grid.SetRowLabelSize(30)
        self.grid.SetDefaultColSize(120)

        self.grid.EnableEditing(False)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        for i in range(len(colLabels)):
            self.grid.SetColLabelValue(i, _U(colLabels[i]))

        self.grid.SetGridCursor(0, 0)
    
        self.fillEquipmentList()

    def __do_layout(self):
        flagText = wx.TOP

#        bla = DBEditFrame(None, "Edit DBCHP", 'dbchp', 0, True)

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)

        #sizerPage0 = wx.StaticBoxSizer(self.frame_summary_table, wx.VERTICAL)

        #sizerPage0.Add(self.grid, .75, wx.EXPAND | wx.TOP | wx.LEFT, 50)

        sizerPage0 = wx.BoxSizer(wx.VERTICAL)
        sizerPage0.Add(self.grid, 1, wx.EXPAND | wx.ALL, 62)

        self.page0.SetSizer(sizerPage0)

        sizerPage1 = wx.StaticBoxSizer(self.frame_descriptive_data, wx.HORIZONTAL)

#        sizerPage1Left = wx.StaticBoxSizer(self.frame_equipment_list, wx.VERTICAL)
        
        #sizerPage1Left.Add(self.listBoxEquipment, 1, wx.EXPAND, 0)
        #sizerPage1Left.Add(self.buttonAddEquipment, 0, wx.ALIGN_RIGHT | wx.TOP, 4)
        #sizerPage1Left.Add(self.buttonDeleteEquipment, 0, wx.ALIGN_RIGHT | wx.TOP, 4)

        sizerPage1Right = wx.BoxSizer(wx.VERTICAL)
        sizerPage1Right.Add(self.tc1, 0, flagText, VSEP)
        sizerPage1Right.Add(self.tc2, 0, flagText, VSEP)
        sizerPage1Right.Add(self.tc3, 0, flagText, VSEP)
        sizerPage1Right.Add(self.tc4, 0, flagText, VSEP)
        sizerPage1Right.Add(self.tc5, 0, flagText, VSEP)

#        sizerPage1.Add(sizerPage1Left, 0.5, wx.EXPAND | wx.TOP, 10)
        sizerPage1.Add(sizerPage1Right, 1, wx.EXPAND | wx.TOP, 10)

        self.page1.SetSizer(sizerPage1)

#        self.page2.addControl(self.tc6)
#        self.page2.addControl(self.tc7)
#        self.page2.addControl(self.tc8)
#        self.page2.addControl(self.tc9)
#        self.page2.addControl(self.tc10)
#        self.page2.addControl(self.tc11)
#        self.page2.addControl(self.tc12)
#        self.page2.addControl(self.tc13)
#
#        self.page2.addControlBottomLeft(self.tc14)
#        self.page2.addControlBottomLeft(self.tc15)
#        self.page2.addControlBottomLeft(self.tc16)
#        self.page2.addControlBottomLeft(self.tc17)
#
#        self.page2.addControlBottomRight(self.tc18)
#        self.page2.addControlBottomRight(self.tc19)
#        self.page2.addControlBottomRight(self.tc20)
#        self.page2.addControlBottomRight(self.tc21)
#
#        self.page2.addControlBottomLeft(self.tc22)
#        self.page2.addControlBottomLeft(self.tc23)
#        self.page2.addControlBottomRight(self.tc24)
#        self.page2.addControlBottomRight(self.tc25)
#
#        self.page3.addControl(self.tc26)
#        self.page3.addControl(self.tc27)
#        self.page3.addControl(self.tc28)
#        self.page3.addControl(self.tc29)
#        self.page3.addControl(self.tc30)
#        self.page3.addControl(self.tc31)
#
#        self.page4.addControl(self.tc32)
#        self.page4.addControl(self.tc33)
#        self.page4.addControl(self.tc34)
#        self.page4.addControl(self.tc35)
#        self.page4.addControl(self.tc36)
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
        self.Show()

    def fillEquipmentList(self):
        equipments = Status.DB.dbheatpump.get_table()
        for equipe in equipments:
#            print equipe.DBHeatPump_ID
            fields = ', '.join([f for f in colLabels])
            sqlQuery = "SELECT %s FROM dbheatpump WHERE DBHeatPump_ID = %s"%(fields,equipe.DBHeatPump_ID)
            #print sqlQuery
            result = Status.DB.sql_query(sqlQuery)
            #print result
            #print
            if len(result) > 0:
                self.grid.AppendRows(1, True)
                for i in range(len(colLabels)):
                    self.grid.SetCellValue(self.grid.GetNumberRows() - 1, i, str(result[i]))
                #nrRows = self.grid.GetNumberRows()
                #nrCols = self.grid.GetNumberCols()
            
            #print nrCols,len(result)
            
#            self.grid.SetCellValue(nrRows - 1, 0, str(result[0]))
#            self.grid.SetCellValue(nrRows - 1, 1, str(result[1]))
#            self.grid.SetCellValue(nrRows - 1, 2, str(result[2]))
#            self.grid.SetCellValue(nrRows - 1, 3, str(result[3]))
#            self.grid.SetCellValue(nrRows - 1, 4, str(result[4]))





