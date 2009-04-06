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
#	PanelQ3: Process data
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
#                       Hans Schweiger      01/04/2009
#
#       Changes to previous version:
#       01/04/2009: HS  impossibility to save entries with empty name field
#
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008/2009
#	http://www.energyxperts.net/
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================
import wx
import os
import pSQL
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
HEIGHT_LEFT        =  29
LABEL_WIDTH_LEFT   = 260
HEIGHT_RIGHT       =  26
LABEL_WIDTH_RIGHT  = 400
DATA_ENTRY_WIDTH   = 100
UNITS_WIDTH        = 100

ENCODING = "latin-1"
def _U(text):
    return unicode(_(text),"utf-8")

class PanelQ3(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        self._init_ctrls(parent)
        self.__do_layout()
        self.selectedProcessName = None

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ3', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()

        # access to font properties object
        fp = FontProperties()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook)
        self.page1 = wx.Panel(self.notebook)
        self.page2 = wx.Panel(self.notebook)

        self.sizer_5_staticbox = wx.StaticBox(self.page0, -1, _U("Process list"))
        self.sizer_5_staticbox.SetForegroundColour(TITLE_COLOR)
        self.sizer_5_staticbox.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.sizer_7_staticbox = wx.StaticBox(self.page0, -1, _U("Processes description"))
        self.sizer_7_staticbox.SetForegroundColour(TITLE_COLOR)
        self.sizer_7_staticbox.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.sizer_8_staticbox = wx.StaticBox(self.page0, -1, _U("Schedule"))
        self.sizer_8_staticbox.SetForegroundColour(TITLE_COLOR)
        self.sizer_8_staticbox.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.sizer_11_staticbox = wx.StaticBox(self.page1, -1,_U("Waste heat (heat available for recovery)"))
        self.sizer_11_staticbox.SetForegroundColour(TITLE_COLOR)
        self.sizer_11_staticbox.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.sizer_12_staticbox = wx.StaticBox(self.page1, -1, _U("Waste heat recovery for this process"))
        self.sizer_12_staticbox.SetForegroundColour(TITLE_COLOR)
        self.sizer_12_staticbox.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.sizer_13_staticbox = wx.StaticBox(self.page1, -1,
                                               _U("Data of existing heat (or cold) supply to the process"))
        self.sizer_13_staticbox.SetForegroundColour(TITLE_COLOR)
        self.sizer_13_staticbox.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        # set font for titles
        # 1. save actual font parameters on the stack
        fp.pushFont()
        # 2. change size and weight
        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
        self.sizer_5_staticbox.SetFont(fp.getFont())
        self.sizer_7_staticbox.SetFont(fp.getFont())
        self.sizer_8_staticbox.SetFont(fp.getFont())
        self.sizer_11_staticbox.SetFont(fp.getFont())
        self.sizer_12_staticbox.SetFont(fp.getFont())
        self.sizer_13_staticbox.SetFont(fp.getFont())
        # 3. recover previous font state
        fp.popFont()

        # set field sizes for the left tab.
        # Each data entry class has several configurable parameters:
        # 1. The height. This is the same for all the widgets that make the class
        # 2. The width of the label
        # 3. The width of the entry widget
        # 4. The width of the unit chooser.
        #
        fs = FieldSizes(wHeight=HEIGHT_LEFT,wLabel=LABEL_WIDTH_LEFT,
                       wData=DATA_ENTRY_WIDTH,wUnits=UNITS_WIDTH)

        # set font for labels of left tab
        fp.pushFont()
        fp.changeFont(size=TYPE_SIZE_LEFT)

        #
        # left panel controls
        #

        # process list
        self.listBoxProcesses = wx.ListBox(self.page0,-1,choices=[])
        self.listBoxProcesses.SetFont(fp.getFont())
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxProcessesClick, self.listBoxProcesses)

        p1 = wx.StaticBitmap(bitmap=wx.Bitmap(os.path.join('img','Q3.png'),
                                             wx.BITMAP_TYPE_PNG),
                                             id=-1,
                                             parent=self.page2,
                                             pos=wx.Point(0, 0),
                                             size=wx.Size(800,600),
                                             style=wx.SUNKEN_BORDER)
        # Processes description
        #
        self.tc1 = TextEntry(self.page0,maxchars=255,value='',
                             label=_U("Process short name"),
                             tip=_U("Give an organizational diagram of the production process (e.g. the flux of crude milk in chease production or the the flux of car chasis in the automobile industry)"))
        self.tc1_1 = TextEntry(self.page0,maxchars=200,value='',
                             label=_U("Description"),
                             tip=_U("Give a short description of the process"))

        self.tc2 = ChoiceEntry(self.page0,
                               values=TRANSPROCTYPES.values(),
                               label=_U("Process type"),
                               tip=_U("Give a brief description of the process or the unitary operation, and specify if it is continuous or batch"))        

        self.tc3 = ChoiceEntry(self.page0,
                               values=[],
                               label=_U("Unit operation type"),
                               tip=_U("Select from predefined list"))       

        self.tc4 = ChoiceEntry(self.page0,
                               values=[],
                               label=_U("Product or process medium"),
                               tip=_U("The medium that is in direct contact with the treated product, e.g. air for drying, lye or water for washing, etc..."))           

        self.tc5 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Typical (final) temperature of the  process medium during operation"),
                              tip=_U("Give the temperature of the process medium and not that of the heat supplying medium."))


        self.tc6 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Inlet temperature of the process medium (before heat recovery)"),
                              tip=_U("Inlet temperature of the process medium before heat recovery"))


        self.tc7 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Start-up temperature of process medium (after breaks)"),
                              tip=_U("Temperature of the process equipment before heating up when process start-up begins"))



        self.tc8 = FloatEntry(self.page0,
                              ipart=10, decimals=1, minval=0., maxval=1.e+10, value=0.,
                              unitdict='VOLUMEORMASS',
                              label=_U("Daily inflow of process medium"),
                              tip=_U("Continuous process: Fluid flow rate times hours of circulation. Batch process with fluid renewal: volume times No. of batches."))


        self.tc9 = FloatEntry(self.page0,
                              ipart=10, decimals=1, minval=0., maxval=1.e+10, value=0.,
                              unitdict='VOLUME',
                              label=_U("Volume of the process medium within the equipment or storage"),
                              tip=_U("e.g. volume of liquid in a bottle for cleaning"))

        self.tc10 = FloatEntry(self.page0,
                              ipart=6, decimals=1, minval=0., maxval=1.e+10, value=0.,
                              unitdict='POWER',
                              label=_U("Power requirement of the process in operation"),
                              tip=_U("Power requierment during operation at steady state (thermal losses, evapoartion, endogenous chemical recations; without heating of circulating fluid)"))
        #
        # schedule
        #
        self.tc11 = FloatEntry(self.page0,
                              ipart=2, decimals=1, minval=0., maxval=24., value=0.,
                              unitdict = 'TIME',
                              label=_U("Hours of process operation per day"),
                              tip=_U("For batch processes: specify the total duration of process, e.g. 3 batches/day x 2 hrs/batch = 6 hrs. If possible, specify daily program."))

        self.tc12 = FloatEntry(self.page0,
                              ipart=2, decimals=1, minval=0., maxval=99., value=0.,
                              label=_U("Number of batches per day"),
                              tip=_U("For batch processes: specify the total duration of process, e.g. 3 batches/day x 2 hrs/batch = 6 hrs. If possible, specify daily program."))

        self.tc13 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict='TIME',
                              label=_U("Duration of 1 batch"),
                              tip=_U("For batch processes: specify the total duration of process, e.g. 3 batches/day x 2 hrs/batch = 6 hrs. If possible, specify daily program."))

        self.tc14 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=365., value=0.,
                              label=_U("Days of process operation per year"),
                              tip=_U("For batch processes: specify the total duration of process, e.g. 3 batches/day x 2 hrs/batch = 6 hrs. If possible, specify daily program."))


        # Right panel controls
        # make width of labels larger for this panel and change fontsize
        fp.changeFont(size=TYPE_SIZE_RIGHT)
        f = FieldSizes(wHeight=HEIGHT_RIGHT,wLabel=LABEL_WIDTH_RIGHT)

        #
        # waste heat
        #

        self.tc15_1 = ChoiceEntry(self.page1, 
                               values=[],
                               label=_U("Medium of outgoing waste heat flows"),
                               tip=_U("Specify media of waste heat flows (up to 3)")) 
        self.tc15 = FloatEntry(self.page1,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Temperature of outgoing (waste) heat flows"),
                              tip=_U("Temperature of the outgoing waste heat flow (e.g. water or hot humid air at the outlet of a drying process)"))

        self.tc15_2 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict='SPECIFICENTHALPY',
                              label=_U("Specific enthalpy of outgoing (waste) heat flows"),
                              tip=_U("Enthalpy of the outgoing waste heat flow (e.g. water or hot humid air at the outlet of a drying process)"))

        self.tc16 = FloatEntry(self.page1,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Final  temperature of outgoing (waste) heat flows"),
                              tip=_U("Minimum temperature to which the waste heat flow can be cooled. If there is no limit specify 0"))

        self.tc17 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+10, value=0.,
                              unitdict='VOLUME',
                              label=_U("Daily outflow of process medium"),
                              tip=_U("Can be different from the incoming flow if e.g. there is evaporation or some chemical reaction."))

        self.tc18 = ChoiceEntry(self.page1, 
                               values=TRANSYESNO.values(),
                               label=_U("Can heat be recovered from the outflowing medium?"),
                               tip=_U("If NO, specify why: e.g. contamination with substances which can affect the heat exchanger,..."))

        # waste heat recovery

        self.tc19 = ChoiceEntry(self.page1, 
                               values=TRANSYESNO.values(),
                               label=_U("Exists internal heat  recovery for the process?"),
                               tip=_U("If affirmative, specify the inlet temperature after heat recovery"))
        

#        self.tc20 = ChoiceEntry(self.page1,
#                                values=TRANSYESNO.values(),
#                               label=_U("Source of waste heat"),
#                               tip=_U("Specify the heat source (e.g. heat lossed from process X, flue gases from  boiler Y, etc)"))

        self.tc21 = FloatEntry(self.page1,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Inlet temperature of the process medium  (after heat recovery)"),
                              tip=_U("Inlet temperature (towards the system) of the process medium after the heat recovery"))
        


        # Data of existing heat ...
        
        self.tc22 = ChoiceEntry(self.page1, 
                               values=[],
                               label=_U("Medium supplying heat or cold to the process (water, steam, air)"),
                               tip=_U("Medium supplying heat or cold to the process (up to 3)"))


        self.tc23 = ChoiceEntry(self.page1,
                             values = [],
                             label=_U("Heat or cold supply to the process from distribution line / branch No."),
                             tip=_U("Specify the distribution(supply) line of heat/cold feeding the process, using the nomenclature of the hydraulic scheme"))

        self.tc24 = FloatEntry(self.page1,
                               ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                               unitdict='TEMPERATURE',
                               label=_U("Temperature of the incoming medium supplying heat or cold to the process/heat exchanger"),
                               tip=_U("Temperature of the supplying medium at heat exchangers inlet"),
                               fontsize=TYPE_SIZE_RIGHT-1)

        self.tc25 = FloatEntry(self.page1,
                               ipart=6, decimals=1, minval=0., maxval=999999., value = 0.,
                               unitdict='MASSFLOW',
                               label=_U("Flow rate of the heat supply medium (close to process)"),
                               tip=_U("Mass flow of the heat/cold supplyind medium"))

        self.tc26 = FloatEntry(self.page1,
                               ipart=10, decimals=2, minval=0., maxval=999999999., value=0.,
                               unitdict='ENERGY',
                               label=_U("Total yearly process heat consumption"),
                               tip=_U("Only for the process"))

        fp.popFont()
        self.buttonAddProcess = wx.Button(self.page0,-1,_U("Add process"))
        self.buttonAddProcess.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddProcess, self.buttonAddProcess)
        self.buttonAddProcess.SetFont(fp.getFont())

        self.buttonDeleteProcess = wx.Button(self.page0,-1,_U("Delete process"))
        self.buttonDeleteProcess.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteProcess, self.buttonDeleteProcess)
        self.buttonDeleteProcess.SetFont(fp.getFont())

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,_U("Cancel"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)
        self.buttonCancel.SetFont(fp.getFont())

        self.buttonOK = wx.Button(self,wx.ID_OK,_U("OK"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()
        self.buttonOK.SetFont(fp.getFont())


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.StaticBoxSizer(self.sizer_11_staticbox, wx.VERTICAL)
        sizer_12 = wx.StaticBoxSizer(self.sizer_12_staticbox, wx.VERTICAL)

        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.StaticBoxSizer(self.sizer_13_staticbox, wx.VERTICAL)
        sizer_25 = wx.BoxSizer(wx.VERTICAL)
        sizer_24 = wx.BoxSizer(wx.VERTICAL)

        sizer_23 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.StaticBoxSizer(self.sizer_8_staticbox, wx.VERTICAL)
        sizer_22 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.VERTICAL)
        sizer_21 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)
        sizer_5.Add(self.listBoxProcesses, 1, wx.EXPAND, 0)
        sizer_5.Add(self.buttonAddProcess, 0, wx.ALIGN_RIGHT, 0)
        sizer_5.Add(self.buttonDeleteProcess, 0, wx.ALIGN_RIGHT, 0)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)

        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM
        flagText = wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM
        # Left tab. Processes description
        sizer_21.Add(self.tc1, 0, flagText, 1)
        sizer_21.Add(self.tc1_1, 0, flagText, 1)
        sizer_21.Add(self.tc2, 0, flagText, 1)
        sizer_21.Add(self.tc3, 0, flagText, 1)
        sizer_21.Add(self.tc4, 0, flagText, 1)
        sizer_21.Add(self.tc5, 0, flagText, 1)
        sizer_21.Add(self.tc6, 0, flagText, 1)
        sizer_21.Add(self.tc7, 0, flagText, 1)
        sizer_21.Add(self.tc8, 0, flagText, 1)
        sizer_21.Add(self.tc9, 0, flagText, 1)
        sizer_21.Add(self.tc10, 0, flagText, 1)

        sizer_7.Add(sizer_21, 1, wx.LEFT|wx.EXPAND, 40)
        sizer_6.Add(sizer_7, 2, wx.EXPAND, 0)

        # Left tab. Schedule
        sizer_22.Add(self.tc11, 0, flagText, 1)
        sizer_22.Add(self.tc12, 0, flagText, 1)
        sizer_22.Add(self.tc13, 0, flagText, 1)
        sizer_22.Add(self.tc14, 0, flagText, 1)

        sizer_8.Add(sizer_22, 1, wx.LEFT|wx.EXPAND, 40)
        sizer_6.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_4.Add(sizer_6, 2, wx.EXPAND, 0)
        self.page0.SetSizer(sizer_4)
        
        # Right tab. Heat available for recovery
        sizer_23.Add(self.tc18,   0, flagText, 1)
        sizer_23.Add(self.tc15_1, 0, flagText, 1)
        sizer_23.Add(self.tc15,   0, flagText, 1)
        sizer_23.Add(self.tc15_2, 0, flagText, 1)
        sizer_23.Add(self.tc16,   0, flagText, 1)
        sizer_23.Add(self.tc17,   0, flagText, 1)

        sizer_11.Add(sizer_23, 1, wx.LEFT|wx.TOP|wx.EXPAND, 10)
        sizer_10.Add(sizer_11, 1, wx.EXPAND, 0)
        
        # Right tab. Recovery for this process
        sizer_24.Add(self.tc19, 0, flagText, 1)
#        sizer_24.Add(self.tc20, 0, flagText, 1)
        sizer_24.Add(self.tc21, 0, flagText, 1)

        sizer_12.Add(sizer_24, 1, wx.LEFT|wx.TOP|wx.EXPAND, 10)
        sizer_10.Add(sizer_12, 0, wx.EXPAND, 0)
        
        # Right tab. Data of existing supply
        sizer_25.Add(self.tc22, 0, flagText, 1)
        sizer_25.Add(self.tc23, 0, flagText, 1)
        sizer_25.Add(self.tc24, 0, flagText, 1)
        sizer_25.Add(self.tc25, 0, flagText, 1)
        sizer_25.Add(self.tc26, 0, flagText, 1)

        sizer_13.Add(sizer_25, 1, wx.LEFT|wx.TOP|wx.EXPAND, 10)
        sizer_10.Add(sizer_13, 1, wx.EXPAND, 0)
        self.page1.SetSizer(sizer_10)
        self.notebook.AddPage(self.page0, _U('Process data'))
        self.notebook.AddPage(self.page1, _U('Heat supply and waste heat'))
        self.notebook.AddPage(self.page2, _U('Temperatures and flow rates'))
        sizer_2.Add(self.notebook, 1, wx.EXPAND, 0)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)
        sizer_2.Add(sizerOKCancel, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		


    def OnButtonAddProcess(self, event):
        self.clear()
        self.selectedProcessName = None

    def OnButtonDeleteProcess(self, event):
        
        if self.checkIfAllowed()==False:
            return
        
        Status.prj.deleteProcess(self.selectedProcessID)
        self.clear()
        self.selectedProcessName = None
        self.display()

    def OnListBoxProcessesClick(self, event):
        self.selectedProcessName = self.listBoxProcesses.GetStringSelection()
        print "PanelQ3: selected Process Name = %r"%self.selectedProcessName
#        self.selectedProcessName = "ätsch bätsch process"
#        print "PanelQ3: selected Process Name = %r"%self.selectedProcessName
#        self.selectedProcessName = u"ätsch bätsch process"
#        print "PanelQ3: selected Process Name = %r"%self.selectedProcessName
        self.showProcess()

    def showProcess(self):

        print "PanelQ3 (showProcess): selected Process Name = %r"%self.selectedProcessName
        if self.selectedProcessName is not None:
            processes = Status.DB.qprocessdata.\
                        Questionnaire_id[Status.PId].\
                        AlternativeProposalNo[Status.ANo].\
                        Process[self.selectedProcessName.encode("utf-8")]
        else:
            processes = []
        
        if len(processes) == 0:
            print "PanelQ3 (showProcess): process not found in DB"
            return
        else:
            q = processes[0]
            print "PanelQ3 (showProcess): process found in DB"
        
        self.selectedProcessID = q.QProcessData_ID

        fluidDict = Status.prj.getFluidDict()
        unitOpDict = Status.prj.getUnitOpDict()

        print "PanelQ3 (showProcess): now writing tc1 = %r"%q.Process
        self.tc1.SetValue(q.Process)
        self.tc1_1.SetValue(q.Description)
        if q.ProcType in TRANSPROCTYPES.keys():
            self.tc2.SetValue(TRANSPROCTYPES[q.ProcType])
        else:
            self.tc2.SetValue("None")

        if q.DBUnitOperation_id in unitOpDict.keys():
            unitOp = unitOpDict[q.DBUnitOperation_id]
            self.tc3.SetValue(unitOp)
        else:
            self.tc3.SetValue("None")

        if q.ProcMedDBFluid_id in fluidDict.keys():
            fluidName = fluidDict[q.ProcMedDBFluid_id]
            self.tc4.SetValue(fluidName)
        else:
            self.tc4.SetValue("None")
            
        self.tc5.SetValue(str(q.PT))
        self.tc6.SetValue(str(q.PTInFlow))
        self.tc7.SetValue(str(q.PTStartUp))

        setUnitsFluidDensity(q.ProcMedDBFluid_id)
        self.tc8.SetValue(str(q.VInFlowDay))
        
        self.tc9.SetValue(str(q.VolProcMed))
        self.tc10.SetValue(str(q.QOpProc))
        self.tc11.SetValue(str(q.HPerDayProc))
        self.tc12.SetValue(str(q.NBatch))
        self.tc13.SetValue(str(q.HBatch))
        self.tc14.SetValue(str(q.NDaysProc))		
        self.tc15.SetValue(str(q.PTOutFlow))

        if q.ProcMedOut in fluidDict.keys():
            fluidName = fluidDict[q.ProcMedOut]
            self.tc15_1.SetValue(fluidName)
        else:
            self.tc15_1.SetValue("None")

        self.tc15_2.SetValue(str(q.HOutFlow))
        self.tc16.SetValue(str(q.PTFinal))

###        setUnitsFluidDensity(q.ProcMedOut) works only with One fluid per panel !!!
        self.tc17.SetValue(str(q.VOutFlow))
        
        if q.HeatRecOK in TRANSYESNO:
            self.tc18.SetValue(TRANSYESNO[str(q.HeatRecOK)])
        else:
            self.tc18.SetValue("None")
            
        if q.HeatRecExist in TRANSYESNO:
            self.tc19.SetValue(TRANSYESNO[str(q.HeatRecExist)])
        else:
            self.tc19.SetValue("None")

#        self.tc20.SetValue(q.SourceWasteHeat)
        if q.HeatRecExist in TRANSYESNO:
            if str(q.HeatRecExist) == "yes":
                self.tc21.SetValue(str(q.PTInFlowRec))
            else:
                self.tc21.SetValue(str(q.PTInFlow))

        fluidDict = Status.prj.getFluidDict()        
        if q.SupplyMedDBFluid_id in fluidDict.keys():
            fluidName = fluidDict[q.SupplyMedDBFluid_id]
            self.tc22.SetValue(fluidName)
        else:
            self.tc22.SetValue("None")

        self.tc23.SetValue(q.PipeDuctProc)
        self.tc24.SetValue(str(q.TSupply))
        self.tc25.SetValue(str(q.SupplyMedFlow))
        self.tc26.SetValue(str(q.UPH))

    def OnButtonCancel(self, event):
        self.clear()
        self.display()

    def OnButtonOK(self, event):

        if Status.PId == 0:
	    return

        if self.checkIfAllowed()==False:
            return
        
        processName = self.tc1.GetValue()
        logTrack("PanelQ3 (ok-button): adding process %r"%processName)

# assure that a name has been entered before continuing
        if len(processName) == 0 or processName is None:
            showWarning(_("You have to enter a name for the new process before saving"))
            return
        
        processes = Status.DB.qprocessdata.Questionnaire_id[Status.PId].\
                    AlternativeProposalNo[Status.ANo].\
                    Process[check(processName)]

	if len(processes) == 0:
            process = Status.prj.addProcessDummy()
        elif len(processes) == 1:
            process = processes[0]
        else:
#	    self.showError("HX name has to be a uniqe value!")
	    print "PanelQ3 (ButtonOK): Process name has to be a uniqe value!"
	    return

        unitOpDict = Status.prj.getUnitOpDict()          
        fluidDict = Status.prj.getFluidDict()
            
        setUnitsFluidDensity(findKey(fluidDict,self.tc4.GetValue(text=True)))
        vIn = self.tc8.GetValue()
        
###        setUnitsFluidDensity(findKey(fluidDict,self.tc15_1.GetValue(text=True)))
### only one fluid per panel can be changed between mass/volume ...
        
        vOut = self.tc17.GetValue()
        if findKey(TRANSYESNO,self.tc19.entry.GetStringSelection()) == "no":
            ptInflowRec = check(self.tc6.GetValue())
        else:
            ptInflowRec = check(self.tc21.GetValue())        

        tmp = {
            "Questionnaire_id":Status.PId,
            "AlternativeProposalNo":Status.ANo,
            "Process":check(self.tc1.GetValue()),
            "Description":check(self.tc1_1.GetValue()),
            "DBUnitOperation_id":check(findKey(unitOpDict,self.tc3.GetValue(text=True))),
            "ProcType":check(findKey(TRANSPROCTYPES,self.tc2.GetValue(text=True))),             
            "ProcMedDBFluid_id":check(findKey(fluidDict,self.tc4.GetValue(text=True))),
            "PT":check(self.tc5.GetValue()), 
            "PTInFlow":check(self.tc6.GetValue()), 
            "PTStartUp":check(self.tc7.GetValue()), 
            "VInFlowDay":check(vIn), 
            "VolProcMed":check(self.tc9.GetValue()), 
            "QOpProc":check(self.tc10.GetValue()), 
            "HPerDayProc":check(self.tc11.GetValue()), 
            "NBatch":check(self.tc12.GetValue()), 
            "HBatch":check(self.tc13.GetValue()), 
            "NDaysProc":check(self.tc14.GetValue()),
            "ProcMedOut":check(findKey(fluidDict,self.tc15_1.GetValue(text=True))),
            "PTOutFlow":check(self.tc15.GetValue()),
            "HOutFlow":check(self.tc15_2.GetValue()),
            "PTFinal":check(self.tc16.GetValue()), 
            "VOutFlow":check(vOut), 
            "HeatRecOK":check(findKey(TRANSYESNO,self.tc18.entry.GetStringSelection())),
            "HeatRecExist":check(findKey(TRANSYESNO,self.tc19.entry.GetStringSelection())),
#            "SourceWasteHeat":check(findKey(TRANSYESNO,self.tc20.entry.GetStringSelection())), 	
            "PTInFlowRec":ptInflowRec, 
            "SupplyMedDBFluid_id":check(findKey(fluidDict,self.tc22.entry.GetStringSelection())),
            "PipeDuctProc":check(self.tc23.GetValue(text=True)), 
            "TSupply":check(self.tc24.GetValue()), 
            "SupplyMedFlow":check(self.tc25.GetValue()), 
            "UPH":check(self.tc26.GetValue()) 
        }
        process.update(tmp)               

        print "PanelQ3 (ok-button): process table updated with: ",tmp
        Status.SQL.commit()
        print "PanelQ3 (ok-button): what arrived is this: ",process

        Status.processData.changeInProcess()

        self.selectedProcessName = processName
        self.display()

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

    def display(self):
#        print "PanelQ3 (display): filling page"
        self.fillPage()
#        print "PanelQ3 (display): showing process"
        self.showProcess()
        self.Show()

    def fillChoiceOfDBUnitOperation(self): # tc3
        unitOpDict = Status.prj.getUnitOpDict()
        unitOpList = unitOpDict.values()
        unitOpList.sort()
        self.tc3.SetValue(unitOpList)
            
    def fillChoiceOfPMDBFluid(self):
        fluidDict = Status.prj.getFluidDict()
        self.tc4.SetValue(fluidDict.values())

    def fillChoiceOfODBFluid(self):
        fluidDict = Status.prj.getFluidDict()
        self.tc15_1.SetValue(fluidDict.values())

    def fillChoiceOfSMDBFluid(self):
        fluidDict = Status.prj.getFluidDict()
        self.tc22.SetValue(fluidDict.values())

    def fillChoiceOfPipe(self):
        pipeList = Status.prj.getPipeList("Pipeduct")
#        print "PanelQ3: pipeList = %r"%pipeList
        self.tc23.SetValue(pipeList)

    def fillChoiceOfHX(self):
        hxList = Status.prj.getHXList("HXName")
#        self.tc20.SetValue(hxList)


    def fillPage(self):
        self.clear()
        self.fillChoiceOfDBUnitOperation()
        self.fillChoiceOfPMDBFluid()
        self.fillChoiceOfODBFluid()
        self.fillChoiceOfSMDBFluid()
        self.fillChoiceOfPipe()
        self.fillChoiceOfHX()
        self.tc2.SetValue(TRANSPROCTYPES.values())
        self.tc18.SetValue(TRANSYESNO.values())
        self.tc19.SetValue(TRANSYESNO.values())
        self.listBoxProcesses.Clear()
        processList = Status.prj.getProcessList("Process")
        for process in processList:
            self.listBoxProcesses.Append(process)
            print "PanelQ3: adding process %r to list"%process
	try: self.listBoxProcesses.SetStringSelection(self.selectedProcessName)
	except: pass
	print "PanelQ3: process List = ",processList

    def clear(self):
        self.tc1.SetValue('')
#        self.tc2.SetValue('')
#        self.tc3.SetValue('')
#        self.tc4.SetValue('')
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
        self.tc15_1.SetValue('')
        self.tc15_2.SetValue('')
        self.tc16.SetValue('')
        self.tc17.SetValue('')
        self.tc18.SetValue('')
        self.tc19.SetValue('')
#        self.tc20.SetValue('')
        self.tc21.SetValue('')
        self.tc22.SetValue('')
        self.tc23.SetValue('')
        self.tc24.SetValue('')
        self.tc25.SetValue('')
        self.tc26.SetValue('')

    def checkIfAllowed(self):
	if Status.ANo >= 0:
            showWarning(_U("In the present version of EINSTEIN it is not allowed to modify\n")+\
                        _U("processes in the checked state or alternative proposals. Go to the original data view\n")+\
                        _U("Workaround for studying process optimisation: create a copy of your project\nand modify on this copy in original state"))
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
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(800, 600), title="Einstein - panelQ3")
    main = Main(1)
    panel = PanelQ3(frame, main)

    frame.Show(True)
    app.MainLoop()
        
