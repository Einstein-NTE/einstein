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
#    PanelDBSolarthermal: Database Design Assistant
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

# constants that control the default sizes
# 1. font sizes
TYPE_SIZE_LEFT    =   9
TYPE_SIZE_MIDDLE  =   9
TYPE_SIZE_RIGHT   =   9
TYPE_SIZE_TITLES  =  10

# 2. field sizes
HEIGHT               =  32
HEIGHT_MIDDLE        =  32
HEIGHT_RIGHT         =  32

LABEL_WIDTH_LEFT     = 250
LABEL_WIDTH_MIDDLE   = 420
LABEL_WIDTH_RIGHT    = 300

DATA_ENTRY_WIDTH     = 100
DATA_ENTRY_WIDTH_LEFT= 200

UNITS_WIDTH          =  90

# 3. vertical separation between fields
VSEP_LEFT            =   2
VSEP_MIDDLE          =   4
VSEP_RIGHT           =   4

def _U(text):
    return unicode(_(text),"utf-8")

class PanelDBSolarthermal(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self._init_ctrls(parent)
        self.__do_layout()

    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelDBSolarthermal', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580))
        self.Hide()

        # access to font properties object
        fp = FontProperties()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page0, _U('Descriptive Data'))

        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page1, _U('Technical Data'))

        self.page2 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page2, _U('Economic Parameters'))

        self.frame_descriptive_data = wx.StaticBox(self.page0, -1,_U("Descriptive Data"))
        self.frame_descriptive_data.SetForegroundColour(TITLE_COLOR)
        self.frame_descriptive_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_technical_data = wx.StaticBox(self.page1, -1, _U("Technical Data"))
        self.frame_technical_data.SetForegroundColour(TITLE_COLOR)
        self.frame_technical_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_economix = wx.StaticBox(self.page2, -1, _U("Economic Parameters"))
        self.frame_economix.SetForegroundColour(TITLE_COLOR)
        self.frame_economix.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        # set font for titles
        # 1. save actual font parameters on the stack
        fp.pushFont()
        # 2. change size and weight
        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
        self.frame_descriptive_data.SetFont(fp.getFont())
        self.frame_technical_data.SetFont(fp.getFont())
        self.frame_economix.SetFont(fp.getFont())
        # 3. recover previous font state
        fp.popFont()

#        fs = FieldSizes(wHeight=HEIGHT,wLabel=LABEL_WIDTH_LEFT,
#                       wData=DATA_ENTRY_WIDTH_LEFT,wUnits=UNITS_WIDTH)

        #
        # left tab controls
        # tab 0 - Descriptive Data
        #
        fp.pushFont()
        fp.changeFont(size=TYPE_SIZE_LEFT)

        #right side: entries
        self.tc1 = TextEntry(self.page0,maxchars=20,value='',
                             label=_U("STManufacturer"),
                             tip=_U("Solarthermal Manufacturer"))

        self.tc2 = TextEntry(self.page0,maxchars=20,value='',
                             label=_U("STModel"),
                             tip=_U("Solarthermal Model"))

        self.tc3 = TextEntry(self.page0,maxchars=45,value='',
                             label=_U("STType"),
                             tip=_U("Solarthermal Type"))

        self.tc4 = TextEntry(self.page0,maxchars=200,value='',
                             label=_U("STReference"),
                             tip=_U("Source of data"))

        #
        # middle left tab controls
        # tab 1 - Technical data
        #
        #fp.changeFont(size=TYPE_SIZE_MIDDLE)
#        f = FieldSizes(wHeight=HEIGHT_MIDDLE,wLabel=LABEL_WIDTH_MIDDLE)

        self.tc5 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STPnomColl"),
                              tip=_U(""))

        self.tc6 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STc0"),
                              tip=_U("Optical efficiency"))

        self.tc7 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STc1"),
                              tip=_U("Linear thermal loss coefficient"))

        self.tc8 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STc2"),
                              tip=_U("Quadratic thermal loss coefficient"))

        self.tc9 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("K50L"),
                              tip=unicode("Incidence angle correction factor at 50º (longitudinal)", 'latin-1'))

        self.tc10 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("K50L"),
                              tip=unicode("Incidence angle correction factor at 50º (longitudinal)", 'latin-1'))

        self.tc11 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("K50T"),
                              tip=unicode("Incidence angle correction factor at 50º (transversal)", 'latin-1'))

        self.tc12 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STMassFlowRate"),
                              tip=_U("Recommended collector mass flow rate"))

        self.tc13 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STLengthGross"),
                              tip=_U(""))

        self.tc14 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STHeightGross"),
                              tip=_U(""))

        self.tc15 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STAreaGross"),
                              tip=_U(""))

        self.tc16 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STLengthAper"),
                              tip=_U(""))

        self.tc17 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STHeightAper"),
                              tip=_U(""))

        self.tc18 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STAreaAper"),
                              tip=_U(""))

        self.tc19 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STAreaFactor"),
                              tip=_U(""))

        self.tc20 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STWeightFactor"),
                              tip=_U(""))

        #
        # right tab controls
        # panel 2. Economic Parameters
        #
        #fp.changeFont(size=TYPE_SIZE_RIGHT)
#        f = FieldSizes(wHeight=HEIGHT_RIGHT,wLabel=LABEL_WIDTH_RIGHT)

        self.tc21 = FloatEntry(self.page2,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STUnitPrice300kW"),
                              tip=_U(""))

        self.tc22 = FloatEntry(self.page2,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STUnitTurnKeyPrice30kW"),
                              tip=_U(""))

        self.tc23 = FloatEntry(self.page2,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STUnitTurnKeyPrice300kW"),
                              tip=_U(""))

        self.tc24 = FloatEntry(self.page2,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STUnitTurnKeyPrice3000kW"),
                              tip=_U(""))

        self.tc25 = FloatEntry(self.page2,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              label=_U("STOMUnitFix"),
                              tip=_U(""))

        self.tc26 = FloatEntry(self.page2,
                               ipart=4, decimals=0, minval=1900, maxval=2100, value=2010,
                               label=_U("STYearUpdate"),
                               tip=_U("Year of last update of the economic data"))

        #
        # buttons
        #
        self.buttonCancel = wx.Button(self,wx.ID_CANCEL, label='Cancel')
#        self.Bind(wx.EVT_BUTTON,self.OnButtonCancel, self.buttonCancel)

        self.buttonOK = wx.Button(self,wx.ID_OK, label='OK')
#        self.Bind(wx.EVT_BUTTON,self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        # recover previous font parameters from the stack
        fp.popFont()


    def __do_layout(self):
        flagText = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP

        # global sizer for panel.
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)

        # sizer for left tab
        # tab 0, general information
        sizerPage0 = wx.StaticBoxSizer(self.frame_descriptive_data, wx.VERTICAL)
        sizerPage0.Add(self.tc1, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc2, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc3, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc4, 0, flagText, VSEP_LEFT)

        self.page0.SetSizer(sizerPage0)

        # sizer for middle left tab
        # tab 1, technical data
        sizerPage1 = wx.StaticBoxSizer(self.frame_technical_data, wx.VERTICAL)
        sizerPage1.Add(self.tc5, 0, flagText, VSEP_LEFT)
        sizerPage1.Add(self.tc6, 0, flagText, VSEP_LEFT)
        sizerPage1.Add(self.tc7, 0, flagText, VSEP_LEFT)
        sizerPage1.Add(self.tc8, 0, flagText, VSEP_LEFT)
        sizerPage1.Add(self.tc9, 0, flagText, VSEP_LEFT)
        sizerPage1.Add(self.tc10, 0, flagText, VSEP_LEFT)
        sizerPage1.Add(self.tc11, 0, flagText, VSEP_LEFT)
        sizerPage1.Add(self.tc12, 0, flagText, VSEP_LEFT)

        sizerP1Left = wx.BoxSizer(wx.VERTICAL)
        sizerP1Left.Add(self.tc13, 0, flagText, VSEP_LEFT)
        sizerP1Left.Add(self.tc14, 0, flagText, VSEP_LEFT)
        sizerP1Left.Add(self.tc15, 0, flagText, VSEP_LEFT)

        sizerP1Right = wx.BoxSizer(wx.VERTICAL)
        sizerP1Right.Add(self.tc16, 0, flagText, VSEP_LEFT)
        sizerP1Right.Add(self.tc17, 0, flagText, VSEP_LEFT)
        sizerP1Right.Add(self.tc18, 0, flagText, VSEP_LEFT)

        sizerP1 = wx.BoxSizer(wx.HORIZONTAL)
        sizerP1.Add(sizerP1Left, 0, flagText, VSEP_LEFT)
        sizerP1.Add(sizerP1Right, 0, flagText, VSEP_LEFT)

        sizerPage1.Add(sizerP1, 0, flagText, VSEP_LEFT)

        sizerPage1.Add(self.tc19, 0, flagText, VSEP_LEFT)
        sizerPage1.Add(self.tc20, 0, flagText, VSEP_LEFT)

        self.page1.SetSizer(sizerPage1)

        # sizer for right tab
        # tab 3, schedule
        sizerpage2 = wx.StaticBoxSizer(self.frame_economix, wx.VERTICAL)
        sizerpage2.Add(self.tc21, 0, flagText, VSEP_LEFT)
        sizerpage2.Add(self.tc22, 0, flagText, VSEP_LEFT)
        sizerpage2.Add(self.tc23, 0, flagText, VSEP_LEFT)
        sizerpage2.Add(self.tc24, 0, flagText, VSEP_LEFT)
        sizerpage2.Add(self.tc25, 0, flagText, VSEP_LEFT)
        sizerpage2.Add(self.tc26, 0, flagText, VSEP_LEFT)

        self.page2.SetSizer(sizerpage2)

        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)

        sizerGlobal.Add(self.notebook, 1, wx.EXPAND, 0)
        sizerGlobal.Add(sizerOKCancel, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizerGlobal)
        self.Layout()

    def display(self,q=None):
        self.Show()
