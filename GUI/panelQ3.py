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
#	Version No.: 0.06
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger  02/05/2008
#                           Tom Sobota      04/05/2008
#                           Hans Schweiger  05/05/2008
#                           Hans Schweiger  07/05/2008
#
#       Changes to previous version:
#       02/05/08:       AlternativeProposalNo added in queries for table qproduct
#       04/05/2008      Changed display format etc.
#       05/05/2008: HS  Event handlers changed
#       07/05/2008: HS  Safety features added against corrupt strings or Nones
#                       in checkboxes and fluid selectors
#                       UPHtotQ substituted by UPH
#                       UAProc substitutde by QOpProc
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
import pSQL
from status import Status
from GUITools import *
from displayClasses import *

# constants
LABELWIDTH=180
TEXTENTRYWIDTH=280
    
class PanelQ3(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        self._init_ctrls(parent)
        self.__do_layout()

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ3', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()
        self.notebook = wx.Notebook(self, -1, style=0)

        self.page0 = wx.Panel(self.notebook)
        self.page1 = wx.Panel(self.notebook)

        self.sizer_5_staticbox = wx.StaticBox(self.page0, -1, _("Process list"))
        self.sizer_5_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_7_staticbox = wx.StaticBox(self.page0, -1, _("Processes description"))
        self.sizer_7_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_8_staticbox = wx.StaticBox(self.page0, -1, _("Schedule"))
        self.sizer_8_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_11_staticbox = wx.StaticBox(self.page1, -1,_("Waste heat (heat available for recovery)"))
        self.sizer_11_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_12_staticbox = wx.StaticBox(self.page1, -1, _("Waste heat recovery for this process"))
        self.sizer_12_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_13_staticbox = wx.StaticBox(self.page1, -1,
                                               _("Data of existing heat (or cold) supply to the process"))
        self.sizer_13_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        #
        # left panel controls
        #

        # process list
        self.listBoxProcesses = wx.ListBox(self.page0,-1,choices=[])
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxProcessesClick, self.listBoxProcesses)

        #
        # Processes description
        #
        self.tc1 = wx.TextCtrl(self.page0,-1,'')
        self.st1 = Label(self.page0,self.tc1,_("Short name"),
                         _("Short name of the process"), LABELWIDTH, TEXTENTRYWIDTH)

        self.tc2 = wx.TextCtrl(self.page0,-1,'')
        self.st2 = Label(self.page0,self.tc2,_("Process type"),
                         _("Process type continuous / batch"))

        self.choiceOfDBUnitOperation = wx.Choice(self.page0,-1,choices=[])
        self.st3 = Label(self.page0,self.choiceOfDBUnitOperation,_("Unit operation type"),
                         _("Unit operation type"))

        self.choiceOfPMDBFluid = wx.Choice(self.page0,-1,choices=[])
        self.st4 = Label(self.page0,self.choiceOfPMDBFluid,_("Process medium"),
                         _("Product or process medium (water, oil, air, lye ...)"))

        self.tc5 = wx.TextCtrl(self.page0,-1,'')
        self.st5 = Label(self.page0,self.tc5,_("Typical temperature"),
                         _("Typical (final) temperature of the process medium during operation in ºC"))

        self.tc6 = wx.TextCtrl(self.page0,-1,'')
        self.st6 = Label(self.page0,self.tc6,_("Inlet temperature"),
                                 _("Inlet temperature of the process medium (before heat recovery) in ºC"))

        self.tc7 = wx.TextCtrl(self.page0,-1,'')
        self.st7 = Label(self.page0,self.tc7,_("Start-up temperature"),
                                 _("Start-up temperature of process medium after breaks in ºC"))

        self.tc8 = wx.TextCtrl(self.page0,-1,'')
        self.st8 = Label(self.page0,self.tc8,_("Daily inflow"),
                                 _("Daily inflow of process medium (m3)"))

        self.tc9 = wx.TextCtrl(self.page0,-1,'')
        self.st9 = Label(self.page0,self.tc9,_("Volume process medium"),
                                 _("Volume of the process medium within the equipment or storage (m3)"))

        self.tc10 = wx.TextCtrl(self.page0,-1,'')
        self.st10 = Label(self.page0,self.tc10,_("Power requirement"),
                                  _("Power requirement of the process in operation (kW)"))

        #
        # schedule
        #
        self.tc11 = wx.TextCtrl(self.page0,-1,'')
        self.st11 = Label(self.page0,self.tc11,_("Hours per day"),
				  _("Hours of process operation per day (hrs/day)"))

        self.tc12 = wx.TextCtrl(self.page0,-1,'')
        self.st12 = Label(self.page0,self.tc12,_("Number of batches"),
				  _("Number of batches per day"))

        self.tc13 = wx.TextCtrl(self.page0,-1,'')
        self.st13 = Label(self.page0,self.tc13,_("Duration of 1 batch"),
                                  _("Duration of 1 batch (h)"))


        self.tc14 = wx.TextCtrl(self.page0,-1,'')
        self.st14 = Label(self.page0,self.tc14,_("Days of operation"),
				  _("Days of operation per year (days / year)"))


        # Right panel controls

        #
        # waste heat
        #
        self.tc15 = wx.TextCtrl(self.page1,-1,'')
        self.st15 = Label(self.page1,self.tc15,_("Outlet temperature"),
				  _("Outlet temperature of waste heat flows (ºC)"))

        self.tc16 = wx.TextCtrl(self.page1,-1,'')
        self.st16 = Label(self.page1,self.tc16,_("Final temperature"),
				  _("Final temperature of waste heat flows (ºC)"))

        self.tc17 = wx.TextCtrl(self.page1,-1,'')
        self.st17 = Label(self.page1,self.tc17,_("Daily outflow"),
				  _("Daily outflow of process medium (mü)"))

        self.choiceHeatRecovered = wx.Choice(self.page1,-1,choices=[_('No'),_('Yes')])
        self.st18 = Label(self.page1,self.choiceHeatRecovered,_("Can heat be recovered?"),
				  _("Can heat be recovered from the outflowing medium ? (yes/no)"))

        # waste heat recovery

        self.choiceExistsHeat = wx.Choice(self.page1,-1,choices=[_('No'),_('Yes')])
        self.st19 = Label(self.page1,self.choiceExistsHeat,_("Exists heat?"),
				  _("Exists heat from heat recovery for the process ? (yes/no)"))

        self.tc20 = wx.TextCtrl(self.page1,-1,'')
        self.st20 = Label(self.page1,self.tc20,_("Source of waste heat"),
				  _("Source of waste heat"))

        self.tc21 = wx.TextCtrl(self.page1,-1,'')
        self.st21 = Label(self.page1,self.tc21,_("Inlet temperature"),
				  _("Inlet temperature of the process medium (after heat recovery) (ºC)"))


        # Data of existing heat ...
        
        self.choiceOfSMDBFluid = wx.Choice(self.page1,-1,choices=[])
        self.st22 = Label(self.page1,self.choiceOfSMDBFluid,_("H/C supply medium"),
				  _("Heat or cold supply medium (water, steam, air)"))

        self.tc23 = wx.TextCtrl(self.page1,-1,'')
        self.st23 = Label(self.page1,self.tc23,_("H/C supply to process"),
				  _("Heat or cold supply to the process from distribution line / branch No."))

        self.tc24 = wx.TextCtrl(self.page1,-1,'')
        self.st24 = Label(self.page1,self.tc24,_("Temp. of supply"),
				  _("Temperature of the heat or cold supply (ºC)"))

        self.tc25 = wx.TextCtrl(self.page1,-1,'')
        self.st25 = Label(self.page1,self.tc25,_("Flow rate"),
				  _("Flow rate (mü/h)"))

        self.tc26 = wx.TextCtrl(self.page1,-1,'')
        self.st26 = Label(self.page1,self.tc26,_("UPH"),
				  _("UPH from questionnaire (annual) (MWh / year)"))


        self.buttonAddProcess = wx.Button(self.page0,-1,_("Add process"))
        self.buttonAddProcess.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddProcess, self.buttonAddProcess)

        self.buttonDeleteProcess = wx.Button(self.page0,-1,_("Delete process"))
        self.buttonDeleteProcess.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteProcess, self.buttonDeleteProcess)

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,_("Cancel"))
        #self.buttonCancel.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        self.buttonOK = wx.Button(self,wx.ID_OK,_("OK"))
        #self.buttonOK.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.StaticBoxSizer(self.sizer_13_staticbox, wx.VERTICAL)
        grid_sizer_5 = wx.FlexGridSizer(5, 2, 3, 3)
        sizer_12 = wx.StaticBoxSizer(self.sizer_12_staticbox, wx.VERTICAL)
        grid_sizer_4 = wx.FlexGridSizer(3, 2, 3, 3)
        sizer_11 = wx.StaticBoxSizer(self.sizer_11_staticbox, wx.VERTICAL)
        grid_sizer_3 = wx.FlexGridSizer(4, 2, 3, 3)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.StaticBoxSizer(self.sizer_8_staticbox, wx.VERTICAL)
        grid_sizer_2 = wx.FlexGridSizer(4, 2, 3, 3)
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(10, 2, 3, 3)
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)
        sizer_5.Add(self.listBoxProcesses, 1, wx.EXPAND, 0)
        sizer_5.Add(self.buttonAddProcess, 0, wx.ALIGN_RIGHT, 0)
        sizer_5.Add(self.buttonDeleteProcess, 0, wx.ALIGN_RIGHT, 0)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)

        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_VERTICAL
        flagText = wx.ALIGN_CENTER_VERTICAL

        grid_sizer_1.Add(self.st1, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc1, 0, flagText, 2)
        grid_sizer_1.Add(self.st2, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc2, 0, flagText, 2)
        grid_sizer_1.Add(self.st3, 0, flagLabel, 2)
        grid_sizer_1.Add(self.choiceOfDBUnitOperation, 0, flagText, 2)
        grid_sizer_1.Add(self.st4, 0, flagLabel, 2)
        grid_sizer_1.Add(self.choiceOfPMDBFluid, 0, flagText, 2)
        grid_sizer_1.Add(self.st5, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc5, 0, flagText, 2)
        grid_sizer_1.Add(self.st6, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc6, 0, flagText, 2)
        grid_sizer_1.Add(self.st7, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc7, 0, flagText, 2)
        grid_sizer_1.Add(self.st8, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc8, 0, flagText, 2)
        grid_sizer_1.Add(self.st9, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc9, 0, flagText, 2)
        grid_sizer_1.Add(self.st10, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc10, 0, flagText, 2)

        sizer_7.Add(grid_sizer_1, 1, wx.LEFT|wx.EXPAND, 40)
        sizer_6.Add(sizer_7, 2, wx.EXPAND, 0)

        grid_sizer_2.Add(self.st11, 0, flagLabel, 0)
        grid_sizer_2.Add(self.tc11, 0, flagText, 0)
        grid_sizer_2.Add(self.st12, 0, flagLabel, 0)
        grid_sizer_2.Add(self.tc12, 0, flagText, 0)
        grid_sizer_2.Add(self.st13, 0, flagLabel, 0)
        grid_sizer_2.Add(self.tc13, 0, flagText, 0)
        grid_sizer_2.Add(self.st14, 0, flagLabel, 0)
        grid_sizer_2.Add(self.tc14, 0, flagText, 0)

        sizer_8.Add(grid_sizer_2, 1, wx.LEFT|wx.EXPAND, 40)
        sizer_6.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_6, 2, wx.EXPAND, 0)
        self.page0.SetSizer(sizer_4)
        
        grid_sizer_3.Add(self.st15, 0, flagLabel, 0)
        grid_sizer_3.Add(self.tc15, 0, flagText, 0)
        grid_sizer_3.Add(self.st16, 0, flagLabel, 0)
        grid_sizer_3.Add(self.tc16, 0, flagText, 0)
        grid_sizer_3.Add(self.st17, 0, flagLabel, 0)
        grid_sizer_3.Add(self.tc17, 0, flagText, 0)
        grid_sizer_3.Add(self.st18, 0, flagLabel, 0)
        grid_sizer_3.Add(self.choiceHeatRecovered, 0, flagText, 0)

        sizer_11.Add(grid_sizer_3, 1, wx.LEFT|wx.TOP|wx.EXPAND, 10)
        sizer_10.Add(sizer_11, 1, wx.EXPAND, 0)
        
        grid_sizer_4.Add(self.st19, 0, flagLabel, 0)
        grid_sizer_4.Add(self.choiceExistsHeat, 0, flagText, 0)
        grid_sizer_4.Add(self.st20, 0, flagLabel, 0)
        grid_sizer_4.Add(self.tc20, 0, flagText, 0)
        grid_sizer_4.Add(self.st21, 0, flagLabel, 0)
        grid_sizer_4.Add(self.tc21, 0, flagText, 0)

        sizer_12.Add(grid_sizer_4, 1, wx.LEFT|wx.TOP|wx.EXPAND, 10)
        sizer_10.Add(sizer_12, 1, wx.EXPAND, 0)
        
        grid_sizer_5.Add(self.st22, 0, flagLabel, 0)
        grid_sizer_5.Add(self.choiceOfSMDBFluid, 0, flagText, 0)
        grid_sizer_5.Add(self.st23, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc23, 0, flagText, 0)
        grid_sizer_5.Add(self.st24, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc24, 0, flagText, 0)
        grid_sizer_5.Add(self.st25, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc25, 0, flagText, 0)
        grid_sizer_5.Add(self.st26, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc26, 0, flagText, 0)

        sizer_13.Add(grid_sizer_5, 1, wx.LEFT|wx.TOP|wx.EXPAND, 10)
        sizer_10.Add(sizer_13, 1, wx.EXPAND, 0)
        self.page1.SetSizer(sizer_10)
        self.notebook.AddPage(self.page0, _('Process data'))
        self.notebook.AddPage(self.page1, _('Heat supply and waste heat'))
        sizer_2.Add(self.notebook, 1, wx.EXPAND, 0)
        sizer_3.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizer_3.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)
        sizer_2.Add(sizer_3, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		


    def OnButtonAddProcess(self, event):
        self.clear()

    def OnButtonDeleteProcess(self, event):
        Status.prj.deleteProcess(self.selectedProcessID)
        self.clear()
        self.fillPage()

    def OnListBoxProcessesClick(self, event):
        self.selectedProcessName = str(self.listBoxProcesses.GetStringSelection())
        processes = Status.DB.qprocessdata.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        q = processes.Process[self.selectedProcessName][0]
        self.selectedProcessID = q.QProcessData_ID

        self.tc1.SetValue(str(q.Process))
        self.tc2.SetValue(str(q.ProcType))
        self.tc5.SetValue(str(q.PT))
        self.tc6.SetValue(str(q.PTInFlow))
        self.tc7.SetValue(str(q.PTStartUp))
        self.tc8.SetValue(str(q.VInFlowDay))
        self.tc9.SetValue(str(q.VolProcMed))
        self.tc10.SetValue(str(q.QOpProc))
        self.tc11.SetValue(str(q.HPerDayProc))
        self.tc12.SetValue(str(q.NBatch))
        self.tc13.SetValue(str(q.HBatch))
        self.tc14.SetValue(str(q.NDaysProc))		
        self.tc15.SetValue(str(q.PTOutFlow))
        self.tc16.SetValue(str(q.PTFinal))
        self.tc17.SetValue(str(q.VOutFlow))
        setChoice(self.choiceHeatRecovered,q.HeatRecOK)
        setChoice(self.choiceExistsHeat,q.HeatRecExist)
        self.tc20.SetValue(str(q.SourceWasteHeat))	
        self.tc21.SetValue(str(q.PTInFlowRec))
        self.tc23.SetValue(str(q.PipeDuctProc))
        self.tc24.SetValue(str(q.TSupply))
        self.tc25.SetValue(str(q.SupplyMedFlow))
        self.tc26.SetValue(str(q.UPH))
        if q.DBUnitOperation_id is not None:
            dbunitoperation = Status.DB.dbunitoperation.DBUnitOperation_ID[q.DBUnitOperation_id]
            if len(dbunitoperation)>0:
                unitOp = str(dbunitoperation[0].UnitOperation)
                setChoice(self.choiceOfDBUnitOperation,unitOp)
                
        if q.ProcMedDBFluid_id is not None:
            dbfluids = Status.DB.dbfluid.DBFluid_ID[q.ProcMedDBFluid_id]
            if len(dbfluids)>0:
                fluidName = str(dbfluids[0].FluidName)
                setChoice(self.choiceOfPMDBFluid,fluidName)
                
        if q.SupplyMedDBFluid_id is not None:
            dbfluids = Status.DB.dbfluid.DBFluid_ID[q.SupplyMedDBFluid_id]
            if len(dbfluids)>0:
                fluidName = str(dbfluids[0].FluidName)
                setChoice(self.choiceOfSMDBFluid,fluidName)

    def OnButtonCancel(self, event):
        self.clear()
        self.fillPage

    def OnButtonOK(self, event):
        if Status.PId == 0:
	    return

        processName = self.check(self.tc1.GetValue())
        processes = Status.DB.qprocessdata.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
	if processName != 'NULL' and \
		len(processes.Process[processName]) == 0:

            selectedUnitOps = Status.DB.dbunitoperation.UnitOperation[\
		str(self.choiceOfDBUnitOperation.GetStringSelection())]
            if len(selectedUnitOps) > 0:
                dbuid = selectedUnitOps[0].DBUnitOperation_ID
            else: dbuid = None
            
            selectedFluids = Status.DB.dbfluid.FluidName[\
		str(self.choiceOfPMDBFluid.GetStringSelection())]
            if len(selectedFluids) > 0:
                dbpmfid = Status.DB.dbfluid.FluidName[\
                    str(self.choiceOfPMDBFluid.GetStringSelection())][0].DBFluid_ID
            else: dbpmfid = None
            
            selectedFluids = Status.DB.dbfluid.FluidName[\
		str(self.choiceOfSMDBFluid.GetStringSelection())]
            if len(selectedFluids) > 0:
                dbsmfid = selectedFluids[0].DBFluid_ID                       
            else: dbsmfid = None

            newID = Status.prj.addProcessDummy()
                        
	    tmp = {
		"Questionnaire_id":Status.PId,
		"AlternativeProposalNo":Status.ANo,
		"Process":self.check(self.tc1.GetValue()),
		"DBUnitOperation_id":dbuid,
		"ProcType":self.check(self.tc2.GetValue()),	
		"ProcMedDBFluid_id":dbpmfid,
		"PT":self.check(self.tc5.GetValue()), 
		"PTInFlow":self.check(self.tc6.GetValue()), 
		"PTStartUp":self.check(self.tc7.GetValue()), 
		"VInFlowDay":self.check(self.tc8.GetValue()), 
		"VolProcMed":self.check(self.tc9.GetValue()), 
		"QOpProc":self.check(self.tc10.GetValue()), 
		"HPerDayProc":self.check(self.tc11.GetValue()), 
		"NBatch":self.check(self.tc12.GetValue()), 
		"HBatch":self.check(self.tc13.GetValue()), 
		"NDaysProc":self.check(self.tc14.GetValue()), 	
		"PTOutFlow":self.check(self.tc15.GetValue()), 
		"PTFinal":self.check(self.tc16.GetValue()), 
		"VOutFlow":self.check(self.tc17.GetValue()), 
                "HeatRecOK":self.check(self.choiceHeatRecovered.GetSelection()),
		"HeatRecExist":self.check(self.choiceExistsHeat.GetSelection()), 
		"SourceWasteHeat":self.check(self.tc20.GetValue()), 	
		"PTInFlowRec":self.check(self.tc21.GetValue()), 
		"SupplyMedDBFluid_id":dbsmfid,
		"PipeDuctProc":self.check(self.tc23.GetValue()), 
		"TSupply":self.check(self.tc24.GetValue()), 
		"SupplyMedFlow":self.check(self.tc25.GetValue()), 
		"UPH":self.check(self.tc26.GetValue()) 
		}

            q = Status.DB.qprocessdata.QProcessData_ID[newID][0]
            q.update(tmp)               

	    Status.SQL.commit()
	    self.fillPage()

	elif processName <> 'NULL' and \
		len(processes.Process[processName]) == 1:

            selectedUnitOps = Status.DB.dbunitoperation.UnitOperation[\
		str(self.choiceOfDBUnitOperation.GetStringSelection())]
            if len(selectedUnitOps) > 0:
                dbuid = selectedUnitOps[0].DBUnitOperation_ID
            else: dbuid = None
            
            selectedFluids = Status.DB.dbfluid.FluidName[\
		str(self.choiceOfPMDBFluid.GetStringSelection())]
            if len(selectedFluids) > 0:
                dbpmfid = Status.DB.dbfluid.FluidName[\
                    str(self.choiceOfPMDBFluid.GetStringSelection())][0].DBFluid_ID
            else: dbpmfid = None
            
            selectedFluids = Status.DB.dbfluid.FluidName[\
		str(self.choiceOfSMDBFluid.GetStringSelection())]
            if len(selectedFluids) > 0:
                dbsmfid = selectedFluids[0].DBFluid_ID                       
            else: dbsmfid = None
        
	    tmp = {
		"Process":self.check(self.tc1.GetValue()),
		"DBUnitOperation_id":dbuid,
		"ProcType":self.check(self.tc2.GetValue()),	
		"ProcMedDBFluid_id":dbpmfid,
		"PT":self.check(self.tc5.GetValue()), 
		"PTInFlow":self.check(self.tc6.GetValue()), 
		"PTStartUp":self.check(self.tc7.GetValue()), 
		"VInFlowDay":self.check(self.tc8.GetValue()), 
		"VolProcMed":self.check(self.tc9.GetValue()), 
		"QOpProc":self.check(self.tc10.GetValue()), 
		"HPerDayProc":self.check(self.tc11.GetValue()), 
		"NBatch":self.check(self.tc12.GetValue()), 
		"HBatch":self.check(self.tc13.GetValue()), 
		"NDaysProc":self.check(self.tc14.GetValue()), 	
		"PTOutFlow":self.check(self.tc15.GetValue()), 
		"PTFinal":self.check(self.tc16.GetValue()), 
		"VOutFlow":self.check(self.tc17.GetValue()), 
		"HeatRecOK":self.check(self.choiceHeatRecovered.GetSelection()), 
		"HeatRecExist":self.check(self.choiceExistsHeat.GetSelection()), 
		"SourceWasteHeat":self.check(self.tc20.GetValue()),
		"PTInFlowRec":self.check(self.tc21.GetValue()), 
		"SupplyMedDBFluid_id":dbsmfid,
		"PipeDuctProc":self.check(self.tc23.GetValue()), 
		"TSupply":self.check(self.tc24.GetValue()), 
		"SupplyMedFlow":self.check(self.tc25.GetValue()), 
		"UPH":self.check(self.tc26.GetValue()) 
		}
	    q = Status.DB.qprocessdata.Process[processName].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]
	    q.update(tmp)               
	    Status.SQL.commit()
	    self.fillPage()
                          
	else:
	    self.main.showError("Process have to be an uniqe value!")


#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		


    def fillChoiceOfDBUnitOperation(self):
        self.choiceOfDBUnitOperation.Clear()
        self.choiceOfDBUnitOperation.Append ("None")
        for n in Status.DB.dbunitoperation.UnitOperation["%"]:
            self.choiceOfDBUnitOperation.Append (n.UnitOperation)
        self.choiceOfDBUnitOperation.SetSelection(0)

    def fillChoiceOfPMDBFluid(self):
        self.choiceOfPMDBFluid.Clear()
        self.choiceOfPMDBFluid.Append ("None")
        for n in Status.DB.dbfluid.FluidName["%"]:
            self.choiceOfPMDBFluid.Append (n.FluidName)
        self.choiceOfPMDBFluid.SetSelection(0)

    def fillChoiceOfSMDBFluid(self):
        self.choiceOfSMDBFluid.Clear()
        self.choiceOfSMDBFluid.Append ("None")
        for n in Status.DB.dbfluid.FluidName["%"]:
            self.choiceOfSMDBFluid.Append (n.FluidName)
        self.choiceOfSMDBFluid.SetSelection(0)

    def fillPage(self):
        self.listBoxProcesses.Clear()
        processes = Status.DB.qprocessdata.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(processes) > 0:
            for n in processes:
                self.listBoxProcesses.Append (str(n.Process))

    def check(self, value):
        if value <> "" and value <> "None":
            return value
        else:
            return 'NULL'

    def clear(self):
        self.tc1.SetValue('')
        self.tc2.SetValue('')
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
        #self.tc18.SetValue('')
        #self.tc19.SetValue('')
        self.tc20.SetValue('')
        self.tc21.SetValue('')
        self.tc23.SetValue('')
        self.tc24.SetValue('')
        self.tc25.SetValue('')
        self.tc26.SetValue('')
        setChoice(self.choiceOfDBUnitOperation,None)
        setChoice(self.choiceOfPMDBFluid,None)
        setChoice(self.choiceOfSMDBFluid,None)
        


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
        
