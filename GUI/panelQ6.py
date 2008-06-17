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
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger
#       Modified by
#                           Tom Sobota 04/05/2008
#                           Stoyan Danov June 2008 ???
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
from displayClasses import *
#from einstein.modules.constants import HXTYPES
from GUITools import *

# constants that control the default field sizes

HEIGHT         =  27
LABELWIDTH     = 180
DATAENTRYWIDTH = 100
UNITSWIDTH     =  90


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

##        wx.Panel.__init__(self, id=-1, name='PanelQ6', parent=parent,
##              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=wx.BK_DEFAULT|wx.BK_TOP)
##        self.Hide()
        wx.Panel.__init__(self, id=-1, name='PanelQ6', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()

        self.notebook = wx.Notebook(self, -1, style=0)

        self.page0 = wx.Panel(self.notebook)
        self.page1 = wx.Panel(self.notebook)

        self.notebook.AddPage(self.page0, _('Heat recovery from thermal equipment'))
        self.notebook.AddPage(self.page1, _('Heat recovery from electrical equipment'))

        self.sizer_3_staticbox = wx.StaticBox(self.page0, -1, _("Heat exchangers list"))
        self.sizer_3_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_5_staticbox = wx.StaticBox(self.page0, -1, _("Heat exchanger data"))
        self.sizer_5_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_7_staticbox = wx.StaticBox(self.page0, -1, _("Heat source / sink"))
        self.sizer_7_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_8_staticbox = wx.StaticBox(self.page0, -1, _("Electrical equipment list"))
        self.sizer_8_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_9_staticbox = wx.StaticBox(self.page0, -1, _("Equipment data"))
        self.sizer_9_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_10_staticbox = wx.StaticBox(self.page0, -1, _("Schedule"))
        self.sizer_10_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
      

#..............................................................................
# layout page 0

#Substitute with static box: List of heat exchangers
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


#Substitute with static box: Heat exchanger data	
        self.stInfo2 = wx.StaticText(id=-1,
					  label=_("heat exchanger data"),
					  name='stInfo2',
					  parent=self.page0,
					  pos=wx.Point(272, 24),
					  style=0)
        self.stInfo2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.tc1 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Short name of heat exchanger"),
                             tip=_("Give a short name of the equipment"))

        self.tc2 = ChoiceEntry(self.page0,
                               values=[],
                               label=_("Heat exchanger type"),
                               tip=_("Specify the type of heat exchanger, e.g. shell-and-tube, plate, fin-and-tube, ..."))

        
        self.tc3 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='POWER',
                              label=_("Heat transfer rate"),
                              tip=_("Heat transfer rate for the specific working conditions"))

        self.tc4 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_("Log. Mean Temperature Diff. (LMTD)"),
                              tip=_("Between the fluids in the heat exchanger"))

        self.tc5 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='ENERGY',
                              label=_("Total heat transfered"),
                              tip=_("Total heat transferred per year"))

#In staticbox Heat source / sink
#on the left
        self.tc6 = ChoiceEntry(self.page0,
                               values=[],
                               label=_("Heat source (process [+outflow no.], equipment, ...)"),
                               tip=_("Indicate: Process, Equipment, Distribution line, Compressor, Electric motor, together with its number"))

        self.tc7 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_("Inlet temperature (source)"),
                              tip=_("Inlet temperature of the hot fluid"))

        self.tc8 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='SPECIFICENTHALPY',
                              label=_("Inlet specific enthalpy (source)"),
                              tip=_("Inlet enthalpy of the hot fluid"))

        self.tc9 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_("Outlet temperature (source)"),
                              tip=_("Outlet temperature of hot fluid"))

        self.tc10 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='SPECIFICENTHALPY',
                              label=_("Outlet specific enthalpy (source)"),
                              tip=_("Outlet enthalpy of the hot fluid"))

#on the right
        self.tc11 = ChoiceEntry(self.page0,
                               values=[],
                               label=_("Heat sink (process, pipe/duct)"),
                               tip=_("Indicate: Process or Distribution line and number. If heat exchange is via storage, it should be defined in the distribution line"))


        self.tc12 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_("Inlet temperature (sink)"),
                              tip=_("Inlet temperature of the cold fluid"))

        self.tc13 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_("Outlet temperature (sink)"),
                              tip=_("Inlet enthalpy of the cold fluid"))



        
#..............................................................................
# layout page 1

#Substitute with static box: List of electrical equipment
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

#Substitute with static box: Equipment data	
        self.stInfo102 = wx.StaticText(id=-1,
					  label="equipment data",
					  name='stInfo102',
					  parent=self.page1,
					  pos=wx.Point(272, 24),
					  style=0)
        self.stInfo102.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

#Substitute with static box: Schedule
        self.stInfo103 = wx.StaticText(id=-1,
					  label="operation schedule",
					  name='stInfo103',
					  parent=self.page1,
					  pos=wx.Point(512, 24),
					  style=0)
        self.stInfo103.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

#In static box: Equipment data

        self.tc101 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Short name of electrical equipment"),
                             tip=_("Give a short name of the equipment"))

        self.tc102 = ChoiceEntry(self.page1,
                               values=[],
                               label=_("Equipment type"),
                               tip=_("specify type of equipment, e.g. compressor, electric motor,..."))

        self.tc103 = ChoiceEntry(self.page1,
                               values=[],
                               label=_("Waste heat type"),
                               tip=_("Specify type of waste heat (e.g. Recooling of compressed air, cooling water of motor/compressor, ...)"))
        
        self.tc104 = FloatEntry(self.page1,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='POWER',
                              label=_("Available waste heat"),
                              tip=_("Estimated quantity"))

        self.tc105 = ChoiceEntry(self.page1,
                               values=[],
                               label=_("Medium"),
                               tip=_("Waste heat carrying medium (fluid)"))

        self.tc106 = FloatEntry(self.page1,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='MASSORVOLUMEFLOW',
                              label=_("Flow rate"),
                              tip=_("Specify the flow rate of the waste heat carrying medium"))

        self.tc107 = FloatEntry(self.page1,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_("Waste heat temperature"),
                              tip=_("Specify the temperature of the waste heat medium at the outlet"))


        self.tc108 = ChoiceEntry(self.page1,
                               values=TRANSYESNO.values(),
                               label=_("Present use of waste heat"),
                               tip=_("If yes, specify distribution pipe / duct or heat exchanger where waste heat is used at present"))

#In static box Schedule

        self.tc110 = FloatEntry(self.page1,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TIME',
                              label=_("Hours of  operation per day"),
                              tip=_(""))

        self.tc111 = FloatEntry(self.page1,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              label=_("Number of batches per day"),
                              tip=_(""))

        self.tc112 = FloatEntry(self.page1,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TIME',
                              label=_("Duration of 1 batch"),
                              tip=_(""))

        self.tc113 = FloatEntry(self.page1,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              label=_("Days of operation per year"),
                              tip=_(""))


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

        self.fillPage()

        hxes = Status.DB.qheatexchanger.ProjectID[Status.PId].AlternativeProposalNo[Status.ANo].HXName[self.HXName]

        if len(hxes) <>0:
            q = hxes[0]
            self.HXID = q.QHeatExchanger_ID
            
            self.tc1.SetValue(str(q.HXName))
            if str(q.HXType) in TRANSHXTYPES.values(): self.tc2.SetValue(str(q.HXType))          
            self.tc3.SetValue(str(q.QdotHX))
            self.tc4.SetValue(str(q.HXLMTD))
            self.tc5.SetValue(str(q.QHX))
            if str(q.HXSource) in self.sourceList: self.tc6.SetValue(str(q.HXSource))          
            self.tc7.SetValue(str(q.HXTSourceInlet))
            self.tc8.SetValue(str(q.HXhSourceInlet))
            self.tc9.SetValue(str(q.HXTSourceOutlet))
            self.tc10.SetValue(str(q.HXhSourceOutlet))
            if str(q.HXSink) in self.sinkList: self.tc11.SetValue(str(q.HXSink))          
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
            "HXType":check(self.tc2.GetValue(text=True)),
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
        self.fillPage()

                          
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
            if str(q.WHEEEqType) in TRANSWHEEEQTYPES.values(): self.tc102.SetValue(str(q.WHEEEqType))          
            if str(q.WHEEWasteHeatType) in TRANSWHEEWASTEHEATTYPES.values(): self.tc103.SetValue(str(q.WHEEWasteHeatType))          
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
            "WHEEEqType":check(self.tc102.GetValue(text=True)),
            "WHEEWasteHeatType":check(self.tc103.GetValue(text=True)),
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
        self.fillPage()

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
            fillChoice(self.tc2.entry,TRANSHXTYPES)
        except:
            pass
        self.sourceList = Status.prj.getEqList("Equipment")
        self.sourceList.extend(Status.prj.getPipeList("Pipeduct"))
        self.sourceList.extend(Status.prj.getProcessList("Process"))
        self.sourceList.extend(Status.prj.getWHEEList("WHEEName"))
        
        fillChoice(self.tc6.entry,self.sourceList)

        self.sinkList = Status.prj.getEqList("Equipment")
        self.sinkList.extend(Status.prj.getPipeList("Pipeduct"))
        self.sinkList.extend(Status.prj.getProcessList("Process"))
        
        fillChoice(self.tc11.entry,self.sinkList)
        
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

    def clearWHEE(self):
        self.tc101.SetValue('')
        self.tc102.SetValue('')
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

        
