# -*- coding: iso-8859-15 -*-
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	PanelQ6: Heat exchangers
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by: 	Heiko Henning, Tom Sobota, Hans Schweiger, Stoyan Danov
#                       04/05/2008 - 13/10/2008
#
#   Update No. 002
#
#   Since Version 1.0 revised by:
#                       Hans Schweiger      01/04/2009
#                       Hans Schweiger      06/07/2009
#
#       Changes to previous version:
#       01/04/2009: HS  impossibility to save entries with empty name field
#       06/07/2009: HS  small bug-fix: storage of WHEEMedium was not possible
#
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008,2009
#	http://www.energyxperts.net/
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================

import wx
import pSQL
from status import Status
from units import *
from displayClasses import *
#from einstein.modules.constants import HXTYPES
from GUITools import *
from fonts import *

ENCODING = "latin-1"

# constants that control the default sizes
# 1. font sizes
TYPE_SIZE_LEFT    =   9
TYPE_SIZE_MIDDLE  =   9
TYPE_SIZE_RIGHT   =   9
TYPE_SIZE_TITLES  =  10

# 2. field sizes
HEIGHT               =  32
HEIGHT_RIGHT         =  32

LABEL_WIDTH_LEFT     = 300
LABEL_WIDTH_RIGHT    = 300

DATA_ENTRY_WIDTH     = 100
DATA_ENTRY_WIDTH_LEFT= 100

UNITS_WIDTH          =  90

# 3. vertical separation between fields
VSEP_LEFT            =   2
VSEP_RIGHT           =   2


ORANGE = '#FF6000'
TITLE_COLOR = ORANGE

def _U(text):
    return unicode(_(text),"utf-8")

class PanelQ6(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        self._init_ctrls(parent)
        self.__do_layout()

        self.HXID = None
        self.WHEEID = None

        self.HXNo = None
        self.WHEENo = None

        self.HXName = None
        self.WHEEName = None

        self.fillPage()

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Panel.__init__(self, id=-1, name='PanelQ6', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()

        # access to font properties object
        fp = FontProperties()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page0, _U('Heat recovery from thermal equipment'))

        self.page1 = wx.Panel(self.notebook)
        self.notebook.AddPage(self.page1, _U('Heat recovery from electrical equipment'))

        self.frame_exchangers_list = wx.StaticBox(self.page0, -1, _U("Heat exchangers list"))
        self.frame_exchangers_list.SetForegroundColour(TITLE_COLOR)
        self.frame_exchangers_list.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_exchanger_data = wx.StaticBox(self.page0, -1, _U("Heat exchanger data"))
        self.frame_exchanger_data.SetForegroundColour(TITLE_COLOR)
        self.frame_exchanger_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))


        self.frame_source_sink = wx.StaticBox(self.page0, -1, _U("Heat source / sink"))
        self.frame_source_sink.SetForegroundColour(TITLE_COLOR)
        self.frame_source_sink.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))


        self.frame_electrical_equipment_list = wx.StaticBox(self.page1, -1, _U("Electrical equipment list"))
        self.frame_electrical_equipment_list.SetForegroundColour(TITLE_COLOR)
        self.frame_electrical_equipment_list.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))


        self.frame_equipment_data = wx.StaticBox(self.page1, -1, _U("Equipment data"))
        self.frame_equipment_data.SetForegroundColour(TITLE_COLOR)
        self.frame_equipment_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))


        self.frame_schedule = wx.StaticBox(self.page1, -1, _U("Schedule"))
        self.frame_schedule.SetForegroundColour(TITLE_COLOR)
        self.frame_schedule.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))


        # set font for titles
        # 1. save actual font parameters on the stack
        fp.pushFont()
        # 2. change size and weight
        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
        self.frame_exchangers_list.SetFont(fp.getFont())
        self.frame_exchanger_data.SetFont(fp.getFont())
        self.frame_source_sink.SetFont(fp.getFont())
        self.frame_electrical_equipment_list.SetFont(fp.getFont())
        self.frame_schedule.SetFont(fp.getFont())
        self.frame_equipment_data.SetFont(fp.getFont())
        # 3. recover previous font state
        fp.popFont()
      
        fs = FieldSizes(wHeight=HEIGHT,wLabel=LABEL_WIDTH_LEFT,
                       wData=DATA_ENTRY_WIDTH_LEFT,wUnits=UNITS_WIDTH)

        #
        # left tab controls
        # tab 0 - Heat recovery from thermal equipment
        #
        fp.pushFont()
        fp.changeFont(size=TYPE_SIZE_LEFT)

        # left static box: List of heat exchangers

        self.listBoxHX = wx.ListBox(self.page0,-1,
                                    choices=[])
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxHXListboxClick, self.listBoxHX)




        # right top static box: Heat exchanger data	

        self.tc1 = TextEntry(self.page0,maxchars=255,value='',
                             label=_U("Short name of heat exchanger"),
                             tip=_U("Give a short name of the equipment"))

        self.tc2 = ChoiceEntry(self.page0,
                               values=[],
                               label=_U("Heat exchanger type"),
                               tip=_U("Specify the type of heat exchanger, e.g. shell-and-tube, plate, fin-and-tube, ..."))

        
        self.tc3 = FloatEntry(self.page0,
                              decimals=1, minval=0., maxval=1.e+12, value=0.,
                              unitdict='POWER',
                              label=_U("Heat transfer rate"),
                              tip=_U("Heat transfer rate for the specific working conditions"))

        self.tc4 = FloatEntry(self.page0,
                              decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Log. Mean Temperature Diff. (LMTD)"),
                              tip=_U("Between the fluids in the heat exchanger"))

        self.tc5 = FloatEntry(self.page0,
                              decimals=1, minval=0., maxval=1.e+12, value=0.,
                              unitdict='ENERGY',
                              label=_U("Total heat transfered"),
                              tip=_U("Total heat transferred per year"))

        # right bottom staticbox Heat source / sink

        self.tc6 = ChoiceEntry(self.page0,
                               values=[],
                               label=_U("Heat source (process [+outflow no.],\nequipment, ...)"),
                               tip=_U("Indicate: Process, Equipment, Distribution line, Compressor, Electric motor, together with its number"))

        self.tc7 = FloatEntry(self.page0,
                              decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Inlet temperature (source)"),
                              tip=_U("Inlet temperature of the hot fluid"))

        self.tc8 = FloatEntry(self.page0,
                              decimals=4, minval=0., maxval=99999., value=0.,
                              unitdict='SPECIFICENTHALPY',
                              label=_U("Inlet specific enthalpy (source)"),
                              tip=_U("Inlet enthalpy of the hot fluid"))

        self.tc9 = FloatEntry(self.page0,
                              decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Outlet temperature (source)"),
                              tip=_U("Outlet temperature of hot fluid"))

        self.tc10 = FloatEntry(self.page0,
                              decimals=4, minval=0., maxval=99999., value=0.,
                              unitdict='SPECIFICENTHALPY',
                              label=_U("Outlet specific enthalpy (source)"),
                              tip=_U("Outlet enthalpy of the hot fluid"))


        self.tc11 = ChoiceEntry(self.page0,
                               values=[],
                               label=_U("Heat sink (process, pipe/duct)"),
                               tip=_U("Indicate: Process or Distribution line and number. If heat exchange is via storage, it should be defined in the distribution line"))


        self.tc12 = FloatEntry(self.page0,
                               decimals=1, minval=0., maxval=999., value=0.,
                               unitdict='TEMPERATURE',
                               label=_U("Inlet temperature (sink)"),
                               tip=_U("Inlet temperature of the cold fluid"))

        self.tc13 = FloatEntry(self.page0,
                               decimals=1, minval=0., maxval=999., value=0.,
                               unitdict='TEMPERATURE',
                               label=_U("Outlet temperature (sink)"),
                               tip=_U("Inlet enthalpy of the cold fluid"))



        
        #
        # right tab controls
        # tab 1 - Heat recovery from electrical equipment
        #
        fp.changeFont(size=TYPE_SIZE_RIGHT)
        f = FieldSizes(wHeight=HEIGHT_RIGHT,wLabel=LABEL_WIDTH_RIGHT)


        # left static box: List of electrical equipment


        self.listBoxWHEE = wx.ListBox(self.page1,-1,choices=[])
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxWHEEListboxClick, self.listBoxWHEE)


        # right upper static box: Equipment data

        self.tc101 = TextEntry(self.page1,maxchars=255,value='',
                               label=_U("Short name of electrical equipment"),
                               tip=_U("Give a short name of the equipment"))

        self.tc102 = ChoiceEntry(self.page1,
                                 values=TRANSWHEEEQTYPES.values(),
                                 label=_U("Equipment type"),
                                 tip=_U("specify type of equipment, e.g. compressor, electric motor,..."))

        self.tc103 = ChoiceEntry(self.page1,
                                 values=TRANSWHEEWASTEHEATTYPES.values(),
                                 label=_U("Waste heat type"),
                                 tip=_U("Specify type of waste heat (e.g. Recooling of compressed air, cooling water of motor/compressor, ...)"))
        
        self.tc104 = FloatEntry(self.page1,
                                decimals=1, minval=0., maxval=1.e+12, value=0.,
                                unitdict='POWER',
                                label=_U("Available waste heat"),
                                tip=_U("Estimated quantity"))

        self.tc105 = ChoiceEntry(self.page1,
                                 values=[],
                                 label=_U("Medium"),
                                 tip=_U("Waste heat carrying medium (fluid)"))

        self.tc106 = FloatEntry(self.page1,
                                decimals=1, minval=0., maxval=1.e+12, value=0.,
                                unitdict='MASSORVOLUMEFLOW',
                                label=_U("Flow rate"),
                                tip=_U("Specify the flow rate of the waste heat carrying medium"))

        self.tc107 = FloatEntry(self.page1,
                                decimals=1, minval=0., maxval=999., value=0.,
                                unitdict='TEMPERATURE',
                                label=_U("Waste heat temperature"),
                                tip=_U("Specify the temperature of the waste heat medium at the outlet"))


        self.tc108 = ChoiceEntry(self.page1,
                                 values=TRANSYESNO.values(),
                                 label=_U("Present use of waste heat"),
                                 tip=_U("If yes, specify distribution pipe / duct or heat exchanger where waste heat is used at present"))

        # right lower static box Schedule

        self.tc110 = FloatEntry(self.page1,
                                decimals=1, minval=0., maxval=999., value=0.,
                                unitdict='TIME',
                                label=_U("Hours of  operation per day"),
                                tip=_U(" "))

        self.tc111 = FloatEntry(self.page1,
                                decimals=1, minval=0., maxval=99., value=0.,
                                label=_U("Number of batches per day"),
                                tip=_U(" "))

        self.tc112 = FloatEntry(self.page1,
                                decimals=1, minval=0., maxval=24., value=0.,
                                unitdict='TIME',
                                label=_U("Duration of 1 batch"),
                                tip=_U(" "))

        self.tc113 = FloatEntry(self.page1,
                                decimals=1, minval=0., maxval=365., value=0.,
                                label=_U("Days of operation per year"),
                                tip=_U(" "))

        #
        # buttons
        #
        self.buttonHXDelete = wx.Button(self.page0,-1,label="delete HX")
        self.Bind(wx.EVT_BUTTON, self.OnButtonHXDelete, self.buttonHXDelete)
        self.buttonHXDelete.SetMinSize((136, 32))
        self.buttonHXDelete.SetFont(fp.getFont())

        self.buttonHXAdd = wx.Button(self.page0,-1, label="add HX")
        self.Bind(wx.EVT_BUTTON, self.OnButtonHXAdd, self.buttonHXAdd)
        self.buttonHXAdd.SetMinSize((136, 32))
        self.buttonHXAdd.SetFont(fp.getFont())

        self.buttonWHEEDelete = wx.Button(self.page1,-1,label="delete WHEE")
        self.Bind(wx.EVT_BUTTON, self.OnButtonWHEEDelete, self.buttonWHEEDelete)
        self.buttonWHEEDelete.SetMinSize((136, 32))
        self.buttonWHEEDelete.SetFont(fp.getFont())

        self.buttonWHEEAdd = wx.Button(self.page1,-1,label="add WHEE")
        self.Bind(wx.EVT_BUTTON, self.OnButtonWHEEAdd, self.buttonWHEEAdd)
        self.buttonWHEEAdd.SetMinSize((136, 32))
        self.buttonWHEEAdd.SetFont(fp.getFont())

        self.buttonOK = wx.Button(self,wx.ID_OK,"")
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL, "")
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        # recover previous font parameters from the stack
        fp.popFont()


    def __do_layout(self):
        flagText = wx.ALIGN_CENTER_VERTICAL|wx.TOP

        # global sizer for panel. Contains notebook w/two tabs + buttons Cancel and Ok
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)
        
        # sizer for left tab
        # tab 0, Heat recovery from thermal equipment
        sizerPage0 = wx.BoxSizer(wx.HORIZONTAL)
        # left part: listbox
        sizerP0Left= wx.StaticBoxSizer(self.frame_exchangers_list, wx.VERTICAL)
        sizerP0Left.Add(self.listBoxHX, 1, wx.EXPAND, 0)
        sizerP0Left.Add(self.buttonHXAdd, 0, wx.ALIGN_RIGHT, 0)
        sizerP0Left.Add(self.buttonHXDelete, 0, wx.ALIGN_RIGHT, 0)
        sizerPage0.Add(sizerP0Left,2,wx.EXPAND|wx.TOP,10)

        # right part: data entries
        sizerP0Right= wx.BoxSizer(wx.VERTICAL)
        sizerP0RightTop= wx.StaticBoxSizer(self.frame_exchanger_data, wx.VERTICAL)
        sizerP0RightTop.Add(self.tc1, 0, flagText, VSEP_RIGHT)
        sizerP0RightTop.Add(self.tc2, 0, flagText, VSEP_RIGHT)
        sizerP0RightTop.Add(self.tc3, 0, flagText, VSEP_RIGHT)
        sizerP0RightTop.Add(self.tc4, 0, flagText, VSEP_RIGHT)
        sizerP0RightTop.Add(self.tc5, 0, flagText, VSEP_RIGHT)
        sizerP0Right.Add(sizerP0RightTop,5,wx.EXPAND,0)
        
        sizerP0RightBottom= wx.StaticBoxSizer(self.frame_source_sink, wx.VERTICAL)
        sizerP0RightBottom.Add(self.tc6, 0, flagText, VSEP_RIGHT)
        sizerP0RightBottom.Add(self.tc7, 0, flagText, VSEP_RIGHT)
        sizerP0RightBottom.Add(self.tc8, 0, flagText, VSEP_RIGHT)
        sizerP0RightBottom.Add(self.tc9, 0, flagText, VSEP_RIGHT)
        sizerP0RightBottom.Add(self.tc10, 0, flagText, VSEP_RIGHT)
        sizerP0RightBottom.Add(self.tc11, 0, flagText, VSEP_RIGHT)
        sizerP0RightBottom.Add(self.tc12, 0, flagText, VSEP_RIGHT)
        sizerP0RightBottom.Add(self.tc13, 0, flagText, VSEP_RIGHT)
        sizerP0Right.Add(sizerP0RightBottom,7,wx.EXPAND,0)
        sizerPage0.Add(sizerP0Right,5,wx.EXPAND|wx.TOP,10)
        self.page0.SetSizer(sizerPage0)

        # sizer for right tab
        # tab 1, Heat recovery from electrical equipment
        sizerPage1 = wx.BoxSizer(wx.HORIZONTAL)
        # left part: listbox
        sizerP1Left= wx.StaticBoxSizer(self.frame_electrical_equipment_list, wx.VERTICAL)
        sizerP1Left.Add(self.listBoxWHEE, 1, wx.EXPAND, 0)
        sizerP1Left.Add(self.buttonWHEEAdd, 0, wx.ALIGN_RIGHT, 0)
        sizerP1Left.Add(self.buttonWHEEDelete, 0, wx.ALIGN_RIGHT, 0)
        sizerPage1.Add(sizerP1Left,2,wx.EXPAND|wx.TOP,10)

        # right part: data entry
        sizerP1Right= wx.BoxSizer(wx.VERTICAL)
        sizerP1RightTop= wx.StaticBoxSizer(self.frame_equipment_data, wx.VERTICAL)
        sizerP1RightTop.Add(self.tc101, 0, flagText, VSEP_RIGHT)
        sizerP1RightTop.Add(self.tc102, 0, flagText, VSEP_RIGHT)
        sizerP1RightTop.Add(self.tc103, 0, flagText, VSEP_RIGHT)
        sizerP1RightTop.Add(self.tc104, 0, flagText, VSEP_RIGHT)
        sizerP1RightTop.Add(self.tc105, 0, flagText, VSEP_RIGHT)
        sizerP1RightTop.Add(self.tc106, 0, flagText, VSEP_RIGHT)
        sizerP1RightTop.Add(self.tc107, 0, flagText, VSEP_RIGHT)
        sizerP1RightTop.Add(self.tc108, 0, flagText, VSEP_RIGHT)
        sizerP1Right.Add(sizerP1RightTop,8,wx.EXPAND|wx.TOP,0)
        
        sizerP1RightBottom= wx.StaticBoxSizer(self.frame_schedule, wx.VERTICAL)
        sizerP1RightBottom.Add(self.tc110, 0, flagText, VSEP_RIGHT)
        sizerP1RightBottom.Add(self.tc111, 0, flagText, VSEP_RIGHT)
        sizerP1RightBottom.Add(self.tc112, 0, flagText, VSEP_RIGHT)
        sizerP1RightBottom.Add(self.tc113, 0, flagText, VSEP_RIGHT)
        sizerP1Right.Add(sizerP1RightBottom,4,wx.EXPAND|wx.TOP,0)
        sizerPage1.Add(sizerP1Right,5,wx.EXPAND|wx.TOP,10)

        self.page1.SetSizer(sizerPage1)

        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)

        sizerGlobal.Add(self.notebook, 3, wx.EXPAND, 0)
        sizerGlobal.Add(sizerOKCancel, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizerGlobal)
        self.Layout()

#------------------------------------------------------------------------------
# GUI actions - 0. OK/Cancel buttons
#------------------------------------------------------------------------------		

    def OnButtonCancel(self, event):
        if self.notebook.GetSelection()==0:
            self.clearHX()
        else:
            self.clearWHEE()
            
    def OnButtonOK(self, event):
        if self.notebook.GetSelection()==0:
            self.OnButtonHXOK(event)
        else:
            self.OnButtonWHEEOK(event)
            

#------------------------------------------------------------------------------
# GUI actions - 1. Heat exchanger page
#------------------------------------------------------------------------------		


    def OnListBoxHXListboxClick(self, event):
        self.HXName = self.listBoxHX.GetStringSelection()
        if self.HXName in self.HXList:
            self.HXNo = self.HXList.index(self.HXName)+1
        else:
            self.HXNo = None

        self.display()

    def OnButtonHXAdd(self, event):
        self.clearHX()

    def OnButtonHXDelete(self, event):
        Status.prj.deleteHX(self.HXID)
        self.clearHX()
        self.fillPage()
        event.Skip()

    def OnButtonHXOK(self, event):
        hxName = self.tc1.GetValue()

# assure that a name has been entered before continuing
        if len(hxName) == 0 or hxName is None:
            showWarning(_("You have to enter a name for the new heat exchanger before saving"))
            return

        hxes = Status.DB.qheatexchanger.HXName[check(hxName)].ProjectID[Status.PId].AlternativeProposalNo[Status.ANo]
	if len(hxes) == 0:
            hx = Status.prj.addHXDummy()
            self.HXName = hxName
        elif len(hxes) == 1:
            hx = hxes[0]
        else:
	    showError("HX name has to be a uniqe value!")
	    return
        
        tmp = {
            "HXName":check(self.tc1.GetValue()),
            "HXType":check(findKey(Status.TRANS.HXTYPES,self.tc2.GetValue(text=True))),
            "QdotHX":check(self.tc3.GetValue()), 
            "HXLMTD":check(self.tc4.GetValue()), 
            "QHX":check(self.tc5.GetValue()), 
            "HXSource":check(self.tc6.GetValue(text=True)), 
            "HXTSourceInlet":check(self.tc7.GetValue()), 
            "HXhSourceInlet":check(self.tc8.GetValue()), 
            "HXTSourceOutlet":check(self.tc9.GetValue()), 
            "HXhSourceOutlet":check(self.tc10.GetValue()), 
            "HXSink":check(self.tc11.GetValue(text=True)), 
            "HXTSinkInlet":check(self.tc12.GetValue()), 
            "HXTSinkOutlet":check(self.tc13.GetValue()), 
            }
        
        hx.update(tmp)
        
        Status.SQL.commit()
        self.display()

                          
#------------------------------------------------------------------------------
# GUI actions - 2. WHEE page
#------------------------------------------------------------------------------		


    def OnListBoxWHEEListboxClick(self, event):
        self.WHEEName = self.listBoxWHEE.GetStringSelection()
        if self.WHEEName in self.WHEEList:
            self.WHEENo = self.WHEEList.index(self.WHEEName)+1
        else:
            self.WHEENo = None

        self.display()
        
    def OnButtonWHEEAdd(self, event):
        self.clearWHEE()

    def OnButtonWHEEDelete(self, event):
        Status.prj.deleteWHEE(self.WHEEID)
        self.clearWHEE()
        self.fillPage()
        event.Skip()

    def OnButtonWHEEOK(self, event):
        wheeName = self.tc101.GetValue()

# assure that a name has been entered before continuing
        if len(wheeName) == 0 or wheeName is None:
            showWarning(_("You have to enter a name for the new equipment before saving"))
            return

        whees = Status.DB.qwasteheatelequip.WHEEName[check(wheeName)].ProjectID[Status.PId].AlternativeProposalNo[Status.ANo]
	if len(whees) == 0:
            whee = Status.prj.addWHEEDummy()
            self.WHEEName = wheeName
        elif len(whees) == 1:
            whee = whees[0]
        else:
	    showError("Name has to be a uniqe value!")
	    return
	
        fluidDict = Status.prj.getFluidDict()
                        
        tmp = {
            "WHEEName":check(self.tc101.GetValue()),
            "WHEEEqType":check(findKey(TRANSWHEEEQTYPES,self.tc102.GetValue(text=True))),
            "WHEEWasteHeatType":check(findKey(TRANSWHEEWASTEHEATTYPES,self.tc103.GetValue(text=True))),
            "QWHEE":check(self.tc104.GetValue()), 
            "WHEEMedium":check(findKey(fluidDict,self.tc105.GetValue(text=True))),
            "WHEEFlow":check(self.tc106.GetValue()), 
            "WHEETOutlet":check(self.tc107.GetValue()),
            
            "WHEEPresentUse":check(findKey(TRANSYESNO,self.tc108.GetValue(text=True))),
            
            "HPerDayWHEE":check(self.tc110.GetValue()), 
            "NBatchWHEE":check(self.tc111.GetValue()), 
            "HBatchWHEE":check(self.tc112.GetValue()), 
            "NDaysWHEE":check(self.tc113.GetValue()), 
            }
        
        whee.update(tmp)
        
        Status.SQL.commit()
        self.display()

#------------------------------------------------------------------------------
    def fillPage(self):
#------------------------------------------------------------------------------
#   screens the SQL tables and fills the lists of HX's and WHEE's
#------------------------------------------------------------------------------
        self.HXList = Status.prj.getHXList("HXName")

        self.listBoxHX.Clear()
        for hx in self.HXList:
            self.listBoxHX.Append(hx)

        if self.HXName is not None:
            self.listBoxHX.SetStringSelection(self.HXName)

        self.WHEEList = Status.prj.getWHEEList("WHEEName")

        self.listBoxWHEE.Clear()
        for whee in self.WHEEList:
            if whee is not None:
                self.listBoxWHEE.Append(whee)

        if self.WHEEName is not None: self.listBoxWHEE.SetStringSelection(self.WHEEName)

        fillChoice(self.tc2.entry,Status.TRANS.HXTYPES.values())

        self.sourceList = Status.prj.getEqList("Equipment")
        self.sourceList.extend(Status.prj.getPipeList("Pipeduct"))
        self.sourceList.extend(Status.prj.getProcessList("Process"))
        self.sourceList.extend(Status.prj.getWHEEList("WHEEName"))
        
        try:
            fillChoice(self.tc6.entry,self.sourceList)
        except:
            pass

        self.sinkList = Status.prj.getEqList("Equipment")
        self.sinkList.extend(Status.prj.getPipeList("Pipeduct"))
        self.sinkList.extend(Status.prj.getProcessList("Process"))
        
        fillChoice(self.tc11.entry,self.sinkList)

        fluidDict = Status.prj.getFluidDict()
        self.tc105.SetValue(fluidDict.values())


#.............................................................................
# heat exchanger data
        hxes = Status.DB.qheatexchanger.\
               ProjectID[Status.PId].\
               AlternativeProposalNo[Status.ANo].\
               HXName[check(self.HXName)]

        if len(hxes) <>0:
            q = hxes[0]
            self.HXID = q.QHeatExchanger_ID
            
            self.tc1.SetValue(q.HXName)

            if str(q.HXType) in Status.TRANS.HXTYPES.keys():
                self.tc2.SetValue(TRANSHXTYPES[str(q.HXType)])
                
            self.tc3.SetValue(str(q.QdotHX))
            self.tc4.SetValue(str(q.HXLMTD))
            self.tc5.SetValue(str(q.QHX))

            if q.HXSource is not None:
                hxsource = unicode(q.HXSource,"utf-8")
                if hxsource in self.sourceList: self.tc6.SetValue(hxsource)
                
            self.tc7.SetValue(str(q.HXTSourceInlet))
            self.tc8.SetValue(str(q.HXhSourceInlet))
            self.tc9.SetValue(str(q.HXTSourceOutlet))
            self.tc10.SetValue(str(q.HXhSourceOutlet))
            
            if q.HXSink is not None:
                hxsink = unicode(q.HXSink,"utf-8")
                if hxsink in self.sinkList: self.tc11.SetValue(hxsink)
                
            self.tc12.SetValue(str(q.HXTSinkInlet))
            self.tc13.SetValue(str(q.HXTSinkOutlet))


#.............................................................................
# WHEE data

        whees = Status.DB.qwasteheatelequip.\
                ProjectID[Status.PId].\
                AlternativeProposalNo[Status.ANo].\
                WHEEName[check(self.WHEEName)]

        if len(whees) <>0:
            q = whees[0]
            self.WHEEID = q.QWasteHeatElEquip_ID
        
            self.tc101.SetValue(q.WHEEName)
            
            if str(q.WHEEEqType) in TRANSWHEEEQTYPES.keys():
                self.tc102.SetValue(TRANSWHEEEQTYPES[q.WHEEEqType])
                
            if str(q.WHEEWasteHeatType) in TRANSWHEEWASTEHEATTYPES.keys():
                self.tc103.SetValue(TRANSWHEEWASTEHEATTYPES[str(q.WHEEWasteHeatType)])
                
            self.tc104.SetValue(str(q.QWHEE))
            
            fluidDict = Status.prj.getFluidDict()

            if q.WHEEMedium is not None:
                WHEEMediumID = int(q.WHEEMedium)
            else:
                WHEEMediumID = None
                
            if WHEEMediumID in fluidDict.keys():
                fluidName = fluidDict[WHEEMediumID]
                self.tc105.SetValue(fluidName)
            else:
                self.tc105.SetValue("None")
                
            setUnitsFluidDensity(q.WHEEMedium)
                
            self.tc106.SetValue(str(q.WHEEFlow))
            self.tc107.SetValue(str(q.WHEETOutlet))
            
            if str(q.WHEEPresentUse) in TRANSYESNO.keys():
                self.tc108.SetValue(TRANSYESNO[str(q.WHEEPresentUse)])

            self.tc110.SetValue(str(q.HPerDayWHEE))
            self.tc111.SetValue(str(q.NBatchWHEE))
            self.tc112.SetValue(str(q.HBatchWHEE))
            self.tc113.SetValue(str(q.NDaysWHEE))
        
#------------------------------------------------------------------------------

    def display(self):
        self.clear()
        self.fillPage()
        self.Show()

    def clear(self):
        self.clearHX()
        self.clearWHEE()

    def clearHX(self):
        self.tc1.SetValue('')
#        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
#        self.tc6.SetValue('')
        self.tc7.SetValue('')
        self.tc8.SetValue('')
        self.tc9.SetValue('')
        self.tc10.SetValue('')
#        self.tc11.SetValue('')
        self.tc12.SetValue('')
        self.tc13.SetValue('')

    def clearWHEE(self):
        self.tc101.SetValue('')
#        self.tc102.SetValue('')
#        self.tc103.SetValue('')
        self.tc104.SetValue('')
#        self.tc105.SetValue('')
        self.tc106.SetValue('')
        self.tc107.SetValue('')
#        self.tc108.SetValue('')

        self.tc110.SetValue('')
        self.tc111.SetValue('')
        self.tc112.SetValue('')
        self.tc113.SetValue('')

        
#==============================================================================

        
