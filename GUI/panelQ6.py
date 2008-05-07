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
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger
#       Modified by
#                           Tom Sobota 04/05/2008
#
#       Changes to previous versions:
#       03/05/08:   Change of button functions -> new version
#                   Several SQL listing and search functions moved to module Project
#                   (in order to separate GUI and technical modules)
#       04/05/2008      Changed position of OK/Quit buttons
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
#from einstein.modules.constants import HXTYPES
from GUITools import *


class PanelQ6(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        self._init_ctrls(parent)
        self.__do_layout()

        self.HXID = None
        self.WHEEID = None

        self.fillPage()

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Panel.__init__(self, id=-1, name='PanelQ6', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=wx.BK_DEFAULT|wx.BK_TOP)
        self.Hide()

        self.notebook = wx.Notebook(self, -1, style=0)

        self.page0 = wx.Panel(self.notebook)
        self.page1 = wx.Panel(self.notebook)

        self.notebook.AddPage(self.page0, _('Heat recovery from thermal equipment'))
        self.notebook.AddPage(self.page1, _('Heat recovery from electrical equipment'))

#..............................................................................
# layout page 0

        self.stInfo1 = wx.StaticText(id=-1,
					  label="list of heat exchangers",
					  name='stInfo1',
					  parent=self.page0,
					  pos=wx.Point(24, 24),
					  style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.listBoxHX = wx.ListBox(choices=[],
						       id=-1,
						       name='listBoxHXList',
						       parent=self.page0,
						       pos=wx.Point(24, 40),
						       size=wx.Size(200, 216),
						       style=0)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxHXListboxClick, self.listBoxHX)


        self.buttonOK = wx.Button(self,wx.ID_OK,"OK")
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,"Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        self.buttonHXDelete = wx.Button(id=-1,
						       label="delete HX",
						       name='buttonHXDelete',
						       parent=self.page0,
						       pos=wx.Point(24, 304),
						       size=wx.Size(200, 32),
						       style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonHXDelete, self.buttonHXDelete)

        self.buttonHXAdd = wx.Button(id=-1,
						    label="add HX",
						    name='buttonHXAdd',
						    parent=self.page0,
						    pos=wx.Point(24, 264),
						    size=wx.Size(200, 32),
						    style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonHXAdd, self.buttonHXAdd)

	
        self.stInfo2 = wx.StaticText(id=-1,
					  label="heat exchanger data",
					  name='stInfo2',
					  parent=self.page0,
					  pos=wx.Point(272, 24),
					  style=0)
        self.stInfo2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.st1 = wx.StaticText(id=-1,
				      label="short name of heat exchanger",
				      name='st1',
				      parent=self.page0,
				      pos=wx.Point(272, 48),
				      style=0)        

        self.tc1 = wx.TextCtrl(id=-1,
				    name='tc1',
				    parent=self.page0,
				    pos=wx.Point(272, 64),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')        

	
        self.st2 = wx.StaticText(id=-1,
				      label="heat exchanger type",
				      name='st2',
				      parent=self.page0,
				      pos=wx.Point(272, 88),
				      style=0)

        self.choiceOfHXType = wx.Choice(choices=[],
						id=-1,
						name='choiceOfHXType',
						parent=self.page0,
						pos=wx.Point(272, 104),
						size=wx.Size(200, 21),
						style=0)

        self.st3 = wx.StaticText(id=-1,
				      label="heat transfer rate [kW]",
				      name='st3',
				      parent=self.page0,
				      pos=wx.Point(272, 128),
				      style=0)

	self.tc3 = wx.TextCtrl(id=-1,
				    name='tc3',
				    parent=self.page0,
				    pos=wx.Point(272, 144),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st4 = wx.StaticText(id=-1,
				      label="log.mean temp.diff (LMTD) [K]",
				      name='st4',
				      parent=self.page0,
				      pos=wx.Point(272, 168),
				      style=0)

        self.tc4 = wx.TextCtrl(id=-1,
				    name='tc4',
				    parent=self.page0,
				    pos=wx.Point(272, 184),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st5 = wx.StaticText(id=-1,
				      label="total heat tranferred [MWh/year]",
				      name='st5',
				      parent=self.page0,
				      pos=wx.Point(272, 208),
				      style=0)

        self.tc5 = wx.TextCtrl(id=-1,
				    name='tc5',
				    parent=self.page0,
				    pos=wx.Point(272, 224),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')
        

        self.st6 = wx.StaticText(id=-1,
				      label="heat source",
				      name='st6',
				      parent=self.page0,
				      pos=wx.Point(272, 268),
				      style=0)
        self.st6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.choiceOfHXSource = wx.Choice(choices=[],
						id=-1,
						name='choiceOfHXSource',
						parent=self.page0,
						pos=wx.Point(272, 284),
						size=wx.Size(200, 21),
						style=0)
        

        self.st7 = wx.StaticText(id=-1,
				      label="inlet temperature (source) [ºC]",
				      name='st7',
				      parent=self.page0,
				      pos=wx.Point(272, 308),
				      style=0)

        self.tc7 = wx.TextCtrl(id=-1,
				    name='tc7',
				    parent=self.page0,
				    pos=wx.Point(272, 324),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st8 = wx.StaticText(id=-1,
				      label="inlet enthalpy (source) [kJ/kgK]",
				      name='st8',
				      parent=self.page0,
				      pos=wx.Point(272, 348),
				      style=0)

        self.tc8 = wx.TextCtrl(id=-1,
				    name='tc8',
				    parent=self.page0,
				    pos=wx.Point(272, 364),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st9 = wx.StaticText(id=-1,
				      label="outlet temperature (source) [ºC]",
				      name='st9',
				      parent=self.page0,
				      pos=wx.Point(272, 388),
				      style=0)

        self.tc9 = wx.TextCtrl(id=-1,
				    name='tc9',
				    parent=self.page0,
				    pos=wx.Point(272, 404),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st10 = wx.StaticText(id=-1,
				       label="outlet enthalpy (source) [kJ/kgK]",
				       name='st10',
				       parent=self.page0,
				       pos=wx.Point(272, 428),
				       style=0)

        self.tc10 = wx.TextCtrl(id=-1,
				     name='tc10',
				     parent=self.page0,
				     pos=wx.Point(272, 444),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st11 = wx.StaticText(id=-1,
				       label="heat sink",
				       name='st11',
				       parent=self.page0,
				       pos=wx.Point(512, 268),
				       style=0)
        self.st11.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.choiceOfHXSink = wx.Choice(choices=[],
						id=-1,
						name='choiceOfHXSink',
						parent=self.page0,
						pos=wx.Point(512, 284),
						size=wx.Size(200, 21),
						style=0)

        self.st12 = wx.StaticText(id=-1,
				       label="inlet temperature (sink) [ºC]",
				       name='st12',
				       parent=self.page0,
				       pos=wx.Point(512, 308),
				       style=0)
        
        self.tc12 = wx.TextCtrl(id=-1,
				     name='tc12',
				     parent=self.page0,
				     pos=wx.Point(512, 324),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st13 = wx.StaticText(id=-1,
				       label="outlet temperature (sink) [ºC]",
				       name='st13',
				       parent=self.page0,
				       pos=wx.Point(512, 388),
				       style=0)

        self.tc13 = wx.TextCtrl(id=-1,
				     name='tc13',
				     parent=self.page0,
				     pos=wx.Point(512, 404),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')

        
#..............................................................................
# layout page 1

        self.stInfo101 = wx.StaticText(id=-1,
					  label="list of electrical equipment",
					  name='stInfo101',
					  parent=self.page1,
					  pos=wx.Point(24, 24),
					  style=0)
        self.stInfo101.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.listBoxWHEE = wx.ListBox(choices=[],
						       id=-1,
						       name='listBoxWHEE',
						       parent=self.page1,
						       pos=wx.Point(24, 40),
						       size=wx.Size(200, 216),
						       style=0)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxWHEEListboxClick, self.listBoxWHEE)

        self.buttonWHEEDelete = wx.Button(id=-1,
						       label="delete WHEE",
						       name='buttonWHEEDelete',
						       parent=self.page1,
						       pos=wx.Point(24, 304),
						       size=wx.Size(200, 32),
						       style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonWHEEDelete, self.buttonWHEEDelete)

        self.buttonWHEEAdd = wx.Button(id=-1,
						    label="add WHEE",
						    name='buttonWHEEAdd',
						    parent=self.page1,
						    pos=wx.Point(24, 264),
						    size=wx.Size(200, 32),
						    style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonWHEEAdd, self.buttonWHEEAdd)

	
        self.stInfo102 = wx.StaticText(id=-1,
					  label="equipment data",
					  name='stInfo102',
					  parent=self.page1,
					  pos=wx.Point(272, 24),
					  style=0)
        self.stInfo102.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo103 = wx.StaticText(id=-1,
					  label="operation schedule",
					  name='stInfo103',
					  parent=self.page1,
					  pos=wx.Point(512, 24),
					  style=0)
        self.stInfo103.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))


        self.st101 = wx.StaticText(id=-1,
				       label="short name of electrical equipment",
				       name='st101',
				       parent=self.page1,
				       pos=wx.Point(272, 48),
				       style=0)

        self.tc101 = wx.TextCtrl(id=-1,
				     name='tc101',
				     parent=self.page1,
				     pos=wx.Point(272, 64),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st102 = wx.StaticText(id=-1,
				       label="equipment type",
				       name='st102',
				       parent=self.page1,
				       pos=wx.Point(272, 88),
				       style=0)

        self.choiceOfWHEEEqType = wx.Choice(choices=[],
						id=-1,
						name='choiceOfWHEEEqType',
						parent=self.page1,
						pos=wx.Point(272, 104),
						size=wx.Size(200, 21),
						style=0)


        self.st103 = wx.StaticText(id=-1,
				       label="waste heat type",
				       name='st103',
				       parent=self.page1,
				       pos=wx.Point(272, 128),
				       style=0)

        self.choiceOfWHEEWasteHeatType = wx.Choice(choices=[],
						id=-1,
						name='choiceOfWHEEWasteHEatType',
						parent=self.page1,
						pos=wx.Point(272, 144),
						size=wx.Size(200, 21),
						style=0)


        self.st104 = wx.StaticText(id=-1,
				       label="available waste heat [kW]",
				       name='st104',
				       parent=self.page1,
				       pos=wx.Point(272, 168),
				       style=0)

        self.tc104 = wx.TextCtrl(id=-1,
				     name='tc104',
				     parent=self.page1,
				     pos=wx.Point(272, 184),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st105 = wx.StaticText(id=-1,
				       label="heat carrier medium",
				       name='st105',
				       parent=self.page1,
				       pos=wx.Point(272, 208),
				       style=0)
	
        self.tc105 = wx.TextCtrl(id=-1,
				     name='tc105',
				     parent=self.page1,
				     pos=wx.Point(272, 224),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')        
	
	
        self.st106 = wx.StaticText(id=-1,
				       label="mass flow rate [kg/h]",
				       name='st106',
				       parent=self.page1,
				       pos=wx.Point(272, 248),
				       style=0)
        
        self.tc106 = wx.TextCtrl(id=-1,
				     name='tc106',
				     parent=self.page1,
				     pos=wx.Point(272, 264),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')

        self.st107 = wx.StaticText(id=-1,
				       label="waste heat temperature (outlet) [ºC]",
				       name='st107',
				       parent=self.page1,
				       pos=wx.Point(272, 288),
				       style=0)
        
        self.tc107 = wx.TextCtrl(id=-1,
				     name='tc107',
				     parent=self.page1,
				     pos=wx.Point(272, 304),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')
        self.st108 = wx.StaticText(id=-1,
				       label="present use of waste heat ?",
				       name='st108',
				       parent=self.page1,
				       pos=wx.Point(272, 328),
				       style=0)
        
        self.tc108 = wx.TextCtrl(id=-1,
				     name='tc108',
				     parent=self.page1,
				     pos=wx.Point(272, 344),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')
        
        self.st110 = wx.StaticText(id=-1,
				       label="daily hours of operation [h]",
				       name='st110',
				       parent=self.page1,
				       pos=wx.Point(512, 48),
				       style=0)
        
        self.tc110 = wx.TextCtrl(id=-1,
				     name='tc110',
				     parent=self.page1,
				     pos=wx.Point(512, 64),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st111 = wx.StaticText(id=-1,
				       label="batches per day",
				       name='st111',
				       parent=self.page1,
				       pos=wx.Point(512, 88),
				       style=0)
        
        self.tc111 = wx.TextCtrl(id=-1,
				     name='tc111',
				     parent=self.page1,
				     pos=wx.Point(512, 104),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')

        self.st112 = wx.StaticText(id=-1,
				       label="duration of one bacth [min.]",
				       name='st112',
				       parent=self.page1,
				       pos=wx.Point(512, 128),
				       style=0)
        
        self.tc112 = wx.TextCtrl(id=-1,
				     name='tc112',
				     parent=self.page1,
				     pos=wx.Point(512, 144),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')

        self.st113 = wx.StaticText(id=-1,
				       label="days of operation per year",
				       name='st113',
				       parent=self.page1,
				       pos=wx.Point(512, 168),
				       style=0)
        
        self.tc113 = wx.TextCtrl(id=-1,
				     name='tc113',
				     parent=self.page1,
				     pos=wx.Point(512, 184),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.notebook, 3, wx.EXPAND, 0)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)
        sizer_1.Add(sizerOKCancel, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer_1)
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
        self.clearHX()

    def OnButtonHXDelete(self, event):
        Status.prj.deleteHX(self.HXID)
        self.clearHX()
        self.fillPage()
        event.Skip()

    def OnButtonHXOK(self, event):
        hxName = check(self.tc1.GetValue())
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
        self.WHEEName = str(self.listBoxWHEE.GetStringSelection())
        self.WHEENo = self.WHEEList.index(self.WHEEName)+1

        whees = Status.DB.qwasteheatelequip.ProjectID[Status.PId].AlternativeProposalNo[Status.ANo].WHEEName[self.WHEEName]

        if len(whees) <>0:
            q = whees[0]
            self.WHEEID = q.QWasteHeatElEquip_ID
        
            self.tc101.SetValue(str(q.WHEEName))
            setChoice(self.choiceOfWHEEEqType,q.WHEEEqType)          
            setChoice(self.choiceOfWHEEWasteHeatType,q.WHEEWasteHeatType)          
            self.tc104.SetValue(str(q.QWHEE))
            self.tc105.SetValue(str(q.WHEEMedium))
            self.tc106.SetValue(str(q.WHEEFlow))
            self.tc107.SetValue(str(q.WHEETOutlet))
            self.tc108.SetValue(str(q.WHEEPresentUse))

            self.tc110.SetValue(str(q.HPerDayWHEE))
            self.tc111.SetValue(str(q.NBatchWHEE))
            self.tc112.SetValue(str(q.HBatchWHEE))
            self.tc113.SetValue(str(q.NDaysWHEE))

    def OnButtonWHEEAdd(self, event):
        self.clearWHEE()

    def OnButtonWHEEDelete(self, event):
        Status.prj.deleteWHEE(self.WHEEID)
        self.clearWHEE()
        self.fillPage()
        event.Skip()

    def OnButtonWHEEOK(self, event):
        wheeName = check(self.tc101.GetValue())
        whees = Status.DB.qwasteheatelequip.WHEEName[wheeName].ProjectID[Status.PId].AlternativeProposalNo[Status.ANo]
	if wheeName <> 'NULL' and len(whees) == 0:
            whee = Status.prj.addWHEEDummy()
        elif wheeName <> 'NULL' and len(whees) == 1:
            whee = whees[0]
        else:
#	    self.showError("HX name has to be a uniqe value!")
	    print "WHEE name has to be a uniqe value!"
	    return
                        
        tmp = {
            "WHEEName":check(self.tc101.GetValue()),
            "WHEEEqType":check(str(self.choiceOfWHEEEqType.GetStringSelection())),
            "WHEEWasteHeatType":check(str(self.choiceOfWHEEWasteHeatType.GetStringSelection())),
            "QWHEE":check(self.tc104.GetValue()), 
            "WHEEMedium":check(self.tc105.GetValue()), 
            "WHEEFlow":check(self.tc106.GetValue()), 
            "WHEETOutlet":check(self.tc107.GetValue()), 
            "WHEEPresentUse":check(self.tc108.GetValue()), 
            "HPerDayWHEE":check(self.tc110.GetValue()), 
            "NBatchWHEE":check(self.tc111.GetValue()), 
            "HBatchWHEE":check(self.tc112.GetValue()), 
            "NDaysWHEE":check(self.tc113.GetValue()), 
            }
        
        whee.update(tmp)
        
        Status.SQL.commit()

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

        try:
            fillChoice(self.choiceOfHXType,HXTYPES)
        except:
            pass
        sourceList = Status.prj.getEqList("Equipment")
        sourceList.extend(Status.prj.getPipeList("Pipeduct"))
        sourceList.extend(Status.prj.getProcessList("Process"))
        
        fillChoice(self.choiceOfHXSource,sourceList)

        sinkList = Status.prj.getEqList("Equipment")
        sinkList.extend(Status.prj.getPipeList("Pipeduct"))
        sinkList.extend(Status.prj.getProcessList("Process"))
        
        fillChoice(self.choiceOfHXSink,sinkList)
        
#------------------------------------------------------------------------------

    def clear(self):
        self.clearHX()
        self.clearWHEE()

    def clearHX(self):
        self.tc1.SetValue('')

        setChoice(self.choiceOfHXType,None)
        
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')

        self.tc7.SetValue('')
        self.tc8.SetValue('')
        self.tc9.SetValue('')
        self.tc10.SetValue('')

        self.tc12.SetValue('')
        self.tc13.SetValue('')

    def clearWHEE(self):
        self.tc101.SetValue('')
        setChoice(self.choiceOfWHEEEqType,None)
        setChoice(self.choiceOfWHEEWasteHeatType,None)

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

        
