# -*- coding: cp1252 -*-
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
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger
#
#       Changes to previous versions:
#       03/05/08:   Change of button functions -> new version
#                   Several SQL listing and search functions moved to module Project
#                   (in order to separate GUI and technical modules)
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
import HelperClass
from status import Status
from einstein.modules.constants import HXTYPES
from GUITools import *


class PanelQ6(wx.Notebook):
    def __init__(self, parent, main):
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)

        self.HXID = None
        self.WHEEID = None

        self.fillPage()

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Notebook.__init__(self, id=-1, name='PanelQ6', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.BK_DEFAULT|wx.BK_TOP)

        page0 = wx.Panel(self)
        page1 = wx.Panel(self)

        self.AddPage(page0, _('Heat recovery from thermal equipment'))
        self.AddPage(page1, _('Heat recovery from electrical equipment'))

#..............................................................................
# layout page 0

        self.stInfo1 = wx.StaticText(id=-1,
					  label="list of heat exchangers",
					  name='stInfo1',
					  parent=page0,
					  pos=wx.Point(24, 24),
					  style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.listBoxHX = wx.ListBox(choices=[],
						       id=-1,
						       name='listBoxHXList',
						       parent=page0,
						       pos=wx.Point(24, 40),
						       size=wx.Size(200, 216),
						       style=0)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxHXListboxClick, self.listBoxHX)


        self.buttonHXOK = wx.Button(id=-1,
					  label="OK",
					  name='buttonHXOK',
					  parent=page0,
					  pos=wx.Point(512, 504),
					  size=wx.Size(200, 32),
					  style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonHXOK, self.buttonHXOK)

        self.buttonHXDelete = wx.Button(id=-1,
						       label="delete HX",
						       name='buttonHXDelete',
						       parent=page0,
						       pos=wx.Point(24, 304),
						       size=wx.Size(200, 32),
						       style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonHXDelete, self.buttonHXDelete)

        self.buttonHXAdd = wx.Button(id=-1,
						    label="add HX",
						    name='buttonHXAdd',
						    parent=page0,
						    pos=wx.Point(24, 264),
						    size=wx.Size(200, 32),
						    style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonHXAdd, self.buttonHXAdd)

	
        self.stInfo2 = wx.StaticText(id=-1,
					  label="heat exchanger data",
					  name='stInfo2',
					  parent=page0,
					  pos=wx.Point(272, 24),
					  style=0)
        self.stInfo2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.st1 = wx.StaticText(id=-1,
				      label="short name of heat exchanger",
				      name='st1',
				      parent=page0,
				      pos=wx.Point(272, 48),
				      style=0)        

        self.tc1 = wx.TextCtrl(id=-1,
				    name='tc1',
				    parent=page0,
				    pos=wx.Point(272, 64),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')        

	
        self.st2 = wx.StaticText(id=-1,
				      label="heat exchanger type",
				      name='st2',
				      parent=page0,
				      pos=wx.Point(272, 88),
				      style=0)

        self.choiceOfHXType = wx.Choice(choices=[],
						id=-1,
						name='choiceOfHXType',
						parent=page0,
						pos=wx.Point(272, 104),
						size=wx.Size(200, 21),
						style=0)

        self.st3 = wx.StaticText(id=-1,
				      label="heat transfer rate [kW]",
				      name='st3',
				      parent=page0,
				      pos=wx.Point(272, 128),
				      style=0)

	self.tc3 = wx.TextCtrl(id=-1,
				    name='tc3',
				    parent=page0,
				    pos=wx.Point(272, 144),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st4 = wx.StaticText(id=-1,
				      label="log.mean temp.diff (LMTD) [K]",
				      name='st4',
				      parent=page0,
				      pos=wx.Point(272, 168),
				      style=0)

        self.tc4 = wx.TextCtrl(id=-1,
				    name='tc4',
				    parent=page0,
				    pos=wx.Point(272, 184),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st5 = wx.StaticText(id=-1,
				      label="total heat tranferred [MWh/year]",
				      name='st5',
				      parent=page0,
				      pos=wx.Point(272, 208),
				      style=0)

        self.tc5 = wx.TextCtrl(id=-1,
				    name='tc5',
				    parent=page0,
				    pos=wx.Point(272, 224),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')
        

        self.st6 = wx.StaticText(id=-1,
				      label="heat source",
				      name='st6',
				      parent=page0,
				      pos=wx.Point(272, 268),
				      style=0)
        self.st6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.choiceOfHXSource = wx.Choice(choices=[],
						id=-1,
						name='choiceOfHXSource',
						parent=page0,
						pos=wx.Point(272, 284),
						size=wx.Size(200, 21),
						style=0)
        

        self.st7 = wx.StaticText(id=-1,
				      label="inlet temperature (source) [ºC]",
				      name='st7',
				      parent=page0,
				      pos=wx.Point(272, 308),
				      style=0)

        self.tc7 = wx.TextCtrl(id=-1,
				    name='tc7',
				    parent=page0,
				    pos=wx.Point(272, 324),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st8 = wx.StaticText(id=-1,
				      label="inlet enthalpy (source) [kJ/kgK]",
				      name='st8',
				      parent=page0,
				      pos=wx.Point(272, 348),
				      style=0)

        self.tc8 = wx.TextCtrl(id=-1,
				    name='tc8',
				    parent=page0,
				    pos=wx.Point(272, 364),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st9 = wx.StaticText(id=-1,
				      label="outlet temperature (source) [ºC]",
				      name='st9',
				      parent=page0,
				      pos=wx.Point(272, 388),
				      style=0)

        self.tc9 = wx.TextCtrl(id=-1,
				    name='tc9',
				    parent=page0,
				    pos=wx.Point(272, 404),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st10 = wx.StaticText(id=-1,
				       label="outlet enthalpy (source) [kJ/kgK]",
				       name='st10',
				       parent=page0,
				       pos=wx.Point(272, 428),
				       style=0)

        self.tc10 = wx.TextCtrl(id=-1,
				     name='tc10',
				     parent=page0,
				     pos=wx.Point(272, 444),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st11 = wx.StaticText(id=-1,
				       label="heat sink",
				       name='st11',
				       parent=page0,
				       pos=wx.Point(512, 268),
				       style=0)
        self.st11.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.choiceOfHXSink = wx.Choice(choices=[],
						id=-1,
						name='choiceOfHXSink',
						parent=page0,
						pos=wx.Point(512, 284),
						size=wx.Size(200, 21),
						style=0)

        self.st12 = wx.StaticText(id=-1,
				       label="inlet temperature (sink) [ºC]",
				       name='st12',
				       parent=page0,
				       pos=wx.Point(512, 308),
				       style=0)
        
        self.tc12 = wx.TextCtrl(id=-1,
				     name='tc12',
				     parent=page0,
				     pos=wx.Point(512, 324),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st13 = wx.StaticText(id=-1,
				       label="outlet temperature (sink) [ºC]",
				       name='st13',
				       parent=page0,
				       pos=wx.Point(512, 388),
				       style=0)

        self.tc13 = wx.TextCtrl(id=-1,
				     name='tc13',
				     parent=page0,
				     pos=wx.Point(512, 404),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')

        
#..............................................................................
# layout page 1

        self.stInfo101 = wx.StaticText(id=-1,
					  label="list of electrical equipment",
					  name='stInfo101',
					  parent=page1,
					  pos=wx.Point(24, 24),
					  style=0)
        self.stInfo101.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.listBoxWHEE = wx.ListBox(choices=[],
						       id=-1,
						       name='listBoxWHEE',
						       parent=page1,
						       pos=wx.Point(24, 40),
						       size=wx.Size(200, 216),
						       style=0)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxWHEEListboxClick, self.listBoxWHEE)

        self.buttonWHEEOK = wx.Button(id=-1,
					  label="OK",
					  name='buttonWHEEOK',
					  parent=page1,
					  pos=wx.Point(512, 504),
					  size=wx.Size(200, 32),
					  style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonWHEEOK, self.buttonWHEEOK)

        self.buttonWHEEDelete = wx.Button(id=-1,
						       label="delete WHEE",
						       name='buttonWHEEDelete',
						       parent=page1,
						       pos=wx.Point(24, 304),
						       size=wx.Size(200, 32),
						       style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonWHEEDelete, self.buttonWHEEDelete)

        self.buttonWHEEAdd = wx.Button(id=-1,
						    label="add WHEE",
						    name='buttonWHEEAdd',
						    parent=page1,
						    pos=wx.Point(24, 264),
						    size=wx.Size(200, 32),
						    style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonWHEEAdd, self.buttonWHEEAdd)

	
        self.stInfo102 = wx.StaticText(id=-1,
					  label="equipment data",
					  name='stInfo102',
					  parent=page1,
					  pos=wx.Point(272, 24),
					  style=0)
        self.stInfo102.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo103 = wx.StaticText(id=-1,
					  label="operation schedule",
					  name='stInfo103',
					  parent=page1,
					  pos=wx.Point(512, 24),
					  style=0)
        self.stInfo103.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))


        self.st101 = wx.StaticText(id=-1,
				       label="short name of electrical equipment",
				       name='st101',
				       parent=page1,
				       pos=wx.Point(272, 48),
				       style=0)

        self.tc101 = wx.TextCtrl(id=-1,
				     name='tc101',
				     parent=page1,
				     pos=wx.Point(272, 64),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st102 = wx.StaticText(id=-1,
				       label="equipment type",
				       name='st102',
				       parent=page1,
				       pos=wx.Point(272, 88),
				       style=0)

        self.tc102 = wx.TextCtrl(id=-1,
				     name='tc102',
				     parent=page1,
				     pos=wx.Point(272, 104),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st103 = wx.StaticText(id=-1,
				       label="waste heat type",
				       name='st103',
				       parent=page1,
				       pos=wx.Point(272, 128),
				       style=0)

        self.tc103 = wx.TextCtrl(id=-1,
				     name='tc103',
				     parent=page1,
				     pos=wx.Point(272, 144),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st104 = wx.StaticText(id=-1,
				       label="available waste heat [kW]",
				       name='st104',
				       parent=page1,
				       pos=wx.Point(272, 168),
				       style=0)

        self.tc104 = wx.TextCtrl(id=-1,
				     name='tc104',
				     parent=page1,
				     pos=wx.Point(272, 184),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st105 = wx.StaticText(id=-1,
				       label="heat carrier medium",
				       name='st105',
				       parent=page1,
				       pos=wx.Point(272, 208),
				       style=0)
	
        self.tc105 = wx.TextCtrl(id=-1,
				     name='tc105',
				     parent=page1,
				     pos=wx.Point(272, 224),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')        
	
	
        self.st106 = wx.StaticText(id=-1,
				       label="mass flow rate [kg/h]",
				       name='st106',
				       parent=page1,
				       pos=wx.Point(272, 248),
				       style=0)
        
        self.tc106 = wx.TextCtrl(id=-1,
				     name='tc106',
				     parent=page1,
				     pos=wx.Point(272, 264),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')

        self.st107 = wx.StaticText(id=-1,
				       label="waste heat temperature (outlet) [ºC]",
				       name='st107',
				       parent=page1,
				       pos=wx.Point(272, 288),
				       style=0)
        
        self.tc107 = wx.TextCtrl(id=-1,
				     name='tc107',
				     parent=page1,
				     pos=wx.Point(272, 304),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')
        self.st108 = wx.StaticText(id=-1,
				       label="present use of waste heat ?",
				       name='st108',
				       parent=page1,
				       pos=wx.Point(272, 328),
				       style=0)
        
        self.tc108 = wx.TextCtrl(id=-1,
				     name='tc108',
				     parent=page1,
				     pos=wx.Point(272, 344),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')
        
        self.st110 = wx.StaticText(id=-1,
				       label="daily hours of operation [h]",
				       name='st110',
				       parent=page1,
				       pos=wx.Point(512, 48),
				       style=0)
        
        self.tc110 = wx.TextCtrl(id=-1,
				     name='tc110',
				     parent=page1,
				     pos=wx.Point(512, 64),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st111 = wx.StaticText(id=-1,
				       label="batches per day",
				       name='st111',
				       parent=page1,
				       pos=wx.Point(512, 88),
				       style=0)
        
        self.tc111 = wx.TextCtrl(id=-1,
				     name='tc111',
				     parent=page1,
				     pos=wx.Point(512, 104),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')

        self.st112 = wx.StaticText(id=-1,
				       label="duration of one bacth [min.]",
				       name='st112',
				       parent=page1,
				       pos=wx.Point(512, 128),
				       style=0)
        
        self.tc112 = wx.TextCtrl(id=-1,
				     name='tc112',
				     parent=page1,
				     pos=wx.Point(512, 144),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')

        self.st113 = wx.StaticText(id=-1,
				       label="days of operation per year",
				       name='st113',
				       parent=page1,
				       pos=wx.Point(512, 168),
				       style=0)
        
        self.tc113 = wx.TextCtrl(id=-1,
				     name='tc113',
				     parent=page1,
				     pos=wx.Point(512, 184),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')

#------------------------------------------------------------------------------
# GUI actions - 1. Heat exchanger page
#------------------------------------------------------------------------------		


    def OnListBoxHXListboxClick(self, event):
        self.HXName = str(self.listBoxHX.GetStringSelection())
        self.HXNo = self.HXList.index(self.HXName)+1

        hxes = Status.DB.qheatexchanger.ProjectID[Status.PId].AlternativeProposalNo[Status.ANo].HXName[self.HXName]

        if len(hxes) <>0:
            q = hxes[0]
            self.HXID = q.QHeatExchanger_ID
            
            self.tc1.SetValue(str(q.HXName))
            setChoice(self.choiceOfHXType,q.HXType)          
            self.tc3.SetValue(str(q.QdotHX))
            self.tc4.SetValue(str(q.HXLMTD))
            self.tc5.SetValue(str(q.QHX))
            setChoice(self.choiceOfHXSource,q.HXSource)          
            self.tc7.SetValue(str(q.HXTSourceInlet))
            self.tc8.SetValue(str(q.HXhSourceInlet))
            self.tc9.SetValue(str(q.HXTSourceOutlet))
            self.tc10.SetValue(str(q.HXhSourceOutlet))
            setChoice(self.choiceOfHXSink,q.HXSink)          
            self.tc12.SetValue(str(q.HXTSinkInlet))
            self.tc13.SetValue(str(q.HXTSinkOutlet))


    def OnButtonHXAdd(self, event):
        self.clear()
        self.fillPage
        #event.Skip()

    def OnButtonHXDelete(self, event):
        Status.prj.deleteHX(self.HXID)
        self.clear()
        self.fillPage()
        event.Skip()

    def OnButtonHXOK(self, event):
        if Status.PId == 0:
	    return

        hxName = self.check(self.tc1.GetValue())
        hxes = Status.DB.qheatexchanger.HXName[hxName].ProjectID[Status.PId].AlternativeProposalNo[Status.ANo]
	if hxName <> 'NULL' and len(hxes) == 0:
            hx = Status.prj.addHXDummy()
        elif hxName <> 'NULL' and len(hxes) == 1:
            hx = hxes[0]
        else:
#	    self.showError("HX name has to be a uniqe value!")
	    print "HX name has to be a uniqe value!"
	    return
                        
        tmp = {
            "HXName":check(self.tc1.GetValue()),
            "HXType":check(str(self.choiceOfHXType.GetStringSelection())),
            "QdotHX":check(self.tc3.GetValue()), 
            "HXLMTD":check(self.tc4.GetValue()), 
            "QHX":check(self.tc5.GetValue()), 
            "HXSource":check(str(self.choiceOfHXSource.GetStringSelection())), 
            "HXTSourceInlet":check(self.tc7.GetValue()), 
            "HXhSourceInlet":check(self.tc8.GetValue()), 
            "HXTSourceOutlet":check(self.tc9.GetValue()), 
            "HXhSourceOutlet":check(self.tc10.GetValue()), 
            "HXSink":check(str(self.choiceOfHXSink.GetStringSelection())), 
            "HXTSinkInlet":check(self.tc12.GetValue()), 
            "HXTSinkOutlet":check(self.tc13.GetValue()), 
            }
        
        hx.update(tmp)
        
        Status.SQL.commit()
                          
#------------------------------------------------------------------------------
# GUI actions - 2. WHEE page
#------------------------------------------------------------------------------		


    def OnListBoxWHEEListboxClick(self, event):
        self.pipeName = str(self.listBoxHXList.GetStringSelection())
        pipes = Status.DB.qdistributionhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].Pipeduct[self.pipeName]

        p = pipes[0]
        self.pipeNo = p.PipeDuctNo
        self.pipeID = p.QDistributionHC_ID
        
        self.tc1.SetValue(str(p.Pipeduct))
        #self.tc2.SetValue(str(p.HeatFromQGenerationHC_id))
        if len(Status.DB.qgenerationhc.QGenerationHC_ID[p.HeatFromQGenerationHC_id]) <> 0:
            self.choiceOfEquipment.SetSelection(\
		self.choiceOfEquipment.FindString(\
		    str(Status.DB.qgenerationhc.QGenerationHC_ID[p.HeatFromQGenerationHC_id][0].Equipment)))
            
        self.tc3.SetValue(str(p.HeatDistMedium))
        self.tc4.SetValue(str(p.DistribCircFlow))
        self.tc5.SetValue(str(p.ToutDistrib))
        self.tc6.SetValue(str(p.TreturnDistrib))
        self.tc7.SetValue(str(p.PercentRecirc))
        self.tc8.SetValue(str(p.Tfeedup))
        self.tc9.SetValue(str(p.PressDistMedium))
        self.tc10.SetValue(str(p.PercentCondRecovery))
        self.tc11.SetValue(str(p.TotLengthDistPipe))
        self.tc12.SetValue(str(p.UDistPipe))
        self.tc13.SetValue(str(p.DDistPipe))
        self.tc14.SetValue(str(p.DeltaDistPipe))		
        self.tc15.SetValue(str(p.NumStorageUnits)) 
        self.tc16.SetValue(str(p.VtotStorage))
        self.tc17.SetValue(str(p.TypeStorage))
        self.tc18.SetValue(str(p.PmaxStorage))
        self.tc19.SetValue(str(p.TmaxStorage))
        #event.Skip()

    def OnButtonWHEEAdd(self, event):
        self.clear()
        #event.Skip()

    def OnButtonWHEEDelete(self, event):
        Status.prj.deletePipe(self.pipeID)
        self.clear()
        self.fillPage()
        event.Skip()

    def OnButtonWHEEOK(self, event):
        if Status.PId == 0:
	    return

        pipeName = self.check(self.tc1.GetValue())
        pipes = Status.DB.qdistributionhc.Pipeduct[pipeName].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
	if pipeName <> 'NULL' and len(pipes) == 0:

            newID = Status.prj.addPipeDummy()
            
            eqTable = Status.DB.qgenerationhc.Equipment[str(self.choiceOfEquipment.GetStringSelection())].\
                      Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
            if len(eqTable) >0: qgid = eqTable[0].QGenerationHC_ID
            else: qgid = None
        
	    tmp = {
		"Questionnaire_id":Status.PId,
		"Pipeduct":self.check(self.tc1.GetValue()),
		"HeatFromQGenerationHC_id":qgid,
		"HeatDistMedium":self.check(self.tc3.GetValue()), 
		"DistribCircFlow":self.check(self.tc4.GetValue()), 
		"ToutDistrib":self.check(self.tc5.GetValue()), 
		"TreturnDistrib":self.check(self.tc6.GetValue()), 
		"PercentRecirc":self.check(self.tc7.GetValue()), 
		"Tfeedup":self.check(self.tc8.GetValue()), 
		"PressDistMedium":self.check(self.tc9.GetValue()), 
		"PercentCondRecovery":self.check(self.tc10.GetValue()), 
		"TotLengthDistPipe":self.check(self.tc11.GetValue()), 
		"UDistPipe":self.check(self.tc12.GetValue()), 
		"DDistPipe":self.check(self.tc13.GetValue()), 
		"DeltaDistPipe":self.check(self.tc14.GetValue()), 		
		"NumStorageUnits":self.check(self.tc15.GetValue()),  
		"VtotStorage":self.check(self.tc16.GetValue()), 
		"TypeStorage":self.check(self.tc17.GetValue()), 
		"PmaxStorage":self.check(self.tc18.GetValue()), 
		"TmaxStorage":self.check(self.tc19.GetValue()),
		"IsAlternative":0
		}

            q = Status.DB.qdistributionhc.QDistributionHC_ID[newID][0]
	    q.update(tmp)               
	    Status.SQL.commit()

	elif pipeName <> 'NULL' and len(pipes) == 1:

            eqTable = Status.DB.qgenerationhc.Equipment[\
		str(self.choiceOfEquipment.GetStringSelection())].\
		Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]

            if len(eqTable) >0: qgid = eqTable[0].QGenerationHC_ID                       
            else: qgid = None

            tmp = {
		"HXName":self.check(self.tc1.GetValue()),
		"HXType":self.check(str(self.choiceHXType.GetSelection())),
		"QdotHX":self.check(self.tc3.GetValue()), 
		"HXLMTD":self.check(self.tc4.GetValue()), 
		"QHX":self.check(self.tc5.GetValue()), 
		"HXSource":self.check(str(self.choiceHXSource.GetSelection())), 
		"HXTSourceInlet":self.check(self.tc7.GetValue()), 
		"HXhSourceInlet":self.check(self.tc8.GetValue()), 
		"HXTSourceOutlet":self.check(self.tc9.GetValue()), 
		"HXhSourceOutlet":self.check(self.tc10.GetValue()), 
		"HXSink":self.check(self.tc11.GetValue()), 
		"HXTSinkInlet":self.check(self.tc12.GetValue()), 
		"HXTSinkOutlet":self.check(self.tc13.GetValue()), 
                }
	    
	    q = pipes[0]
	    q.update(tmp)               
	    Status.SQL.commit()
	    self.fillPage()
                          
	else:
#	    self.showError("Pipeduct have to be an uniqe value!")
            print "PanelQ6: HX name has to be a uniqe value!"
            pass

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

    def fillchoiceOfEquipment(self):
        self.choiceOfEquipment.Clear()
        self.choiceOfEquipment.Append("None")
        if Status.PId <> 0:
            equipments = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
            if len(equipments) <> 0:
                for equipe in equipments:
                    self.choiceOfEquipment.Append(equipe.Equipment)
        self.choiceOfEquipment.SetSelection(0)


#------------------------------------------------------------------------------
    def fillPage(self):
#------------------------------------------------------------------------------
#   screens the SQL tables and fills the lists of HX's and WHEE's
#------------------------------------------------------------------------------
        self.HXList = Status.prj.getHXList("HXName")

        self.listBoxHX.Clear()
        for hx in self.HXList:
            self.listBoxHX.Append(str(hx))

        self.WHEEList = Status.prj.getWHEEList("WHEEName")

        self.listBoxWHEE.Clear()
        for whee in self.WHEEList:
            self.listBoxWHEE.Append(str(whee))

        fillChoice(self.choiceOfHXType,HXTYPES)

        sourceList = Status.prj.getEqList("Equipment")
        sourceList.extend(Status.prj.getPipeList("Pipeduct"))
        sourceList.extend(Status.prj.getProcessList("Process"))
        
        fillChoice(self.choiceOfHXSource,sourceList)

        sinkList = Status.prj.getEqList("Equipment")
        sinkList.extend(Status.prj.getPipeList("Pipeduct"))
        sinkList.extend(Status.prj.getProcessList("Process"))
        
        fillChoice(self.choiceOfHXSink,sinkList)
        
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def check(self, value):
#------------------------------------------------------------------------------
#   auxiliary function. substitutes ""'s and None's by 'NULL'
#   (should be moved some day to a separate file with sql-tools ...)
#------------------------------------------------------------------------------
        if value <> "" and value <> "None":
            return value
        else:
            return 'NULL'
#------------------------------------------------------------------------------

    def clear(self):
        self.tc1.SetValue('')
        #self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')

        self.tc7.SetValue('')
        self.tc8.SetValue('')
        self.tc9.SetValue('')
        self.tc10.SetValue('')

        self.tc12.SetValue('')
        self.tc13.SetValue('')

        self.tc101.SetValue('')

        self.tc103.SetValue('')
        self.tc104.SetValue('')
        self.tc105.SetValue('')
        self.tc106.SetValue('')
        self.tc107.SetValue('')
        self.tc108.SetValue('')

        self.tc110.SetValue('')
        self.tc111.SetValue('')
        self.tc112.SetValue('')
        self.tc113.SetValue('')
        
#==============================================================================

        
