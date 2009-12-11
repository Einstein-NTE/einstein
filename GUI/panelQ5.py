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
#	PanelQ5: Pipes and ducts
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by: 	Heiko Henning, Tom Sobota, Hans Schweiger, Stoyan Danov
#                       02/05/2008 - 13/10/2008
#
#   Update No. 003
#
#   Since Version 1.0 revised by:
#                       Hans Schweiger      12/11/2008
#                       Hans Schweiger      01/04/2009
#                       Hans Schweiger      06/04/2009
#
#       Changes to previous version:
#       12/11/2008: HS  adaptation for full unicode support
#       01/04/2009: HS  impossibility to save entries with empty name field
#       06/04/2009: HS  pipe list sorted by PipeNo.
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
from units import *
from displayClasses import *
from fonts import *


# constants that control the default sizes
# 1. font sizes
TYPE_SIZE_LEFT    =   9
TYPE_SIZE_RIGHT   =   9
TYPE_SIZE_TITLES  =  10

# 2. field sizes
HEIGHT_LEFT       =  27
HEIGHT_RIGHT      =  27
LABEL_WIDTH_LEFT  = 250
LABEL_WIDTH_RIGHT = 180
DATA_ENTRY_WIDTH  = 100
UNITS_WIDTH       =  90

def _U(text):
    return unicode(_(text),"utf-8")

class PanelQ5(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        self._init_ctrls(parent)
        self.__do_layout()
        self.pipeID = None
        self.pipeName = None

        
    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ5', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()

        # access to font properties object
        fp = FontProperties()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook) # left panel
        self.page1 = wx.Panel(self.notebook) # right panel

        self.frame_distrib_list = wx.StaticBox(self.page0, -1, _U("Distribution list"))
        self.frame_distrib_heat_cold = wx.StaticBox(self.page0, -1, _U("Distribution of heat/cold"))
        self.frame_general_data = wx.StaticBox(self.page0, -1, _U("General data"))
        self.frame_temp_pressures = wx.StaticBox(self.page0, -1, _U("Temperatures, pressures and flow rates"))
        self.frame_piping_specs = wx.StaticBox(self.page0, -1, _U("Piping specifications"))
        self.frame_storage = wx.StaticBox(self.page1, -1, "Storage")

        # set font for titles
        # 1. save actual font parameters on the stack
        fp.pushFont()
        # 2. change size and weight
        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
        self.frame_distrib_list.SetFont(fp.getFont())
        self.frame_distrib_heat_cold.SetFont(fp.getFont())
        self.frame_general_data.SetFont(fp.getFont())
        self.frame_temp_pressures.SetFont(fp.getFont())
        self.frame_piping_specs.SetFont(fp.getFont())
        self.frame_storage.SetFont(fp.getFont())
        # 3. recover previous font state
        fp.popFont()


        fs = FieldSizes(wHeight=HEIGHT_LEFT,wLabel=LABEL_WIDTH_LEFT,
                       wData=DATA_ENTRY_WIDTH,wUnits=UNITS_WIDTH)


        # set font for labels of left tab
        fp.pushFont()
        fp.changeFont(size=TYPE_SIZE_LEFT)

        #
        # left panel controls
        #

        self.listBoxDistributionList = wx.ListBox(self.page0,-1,choices=[])
        self.listBoxDistributionList.SetFont(fp.getFont())
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxDistributionListListboxClick, self.listBoxDistributionList)


#In StaticBox "Distribution of heat/cold"
#In StaticBox "General data" within "Distribution of heat/cold"    
        self.tc1 = TextEntry(self.page0,maxchars=255,value='',
                             label=_U("Name of the branch / distribution system"),
                             tip=_U("Give some brief name or number of the distribution tube consistent with the hydraulic scheme"))
        
       
        self.tc3 = ChoiceEntry(self.page0,
                               values=[],
                               label=_U("Heat or cold distribution medium"),
                               tip=_U("e.g. air for drying process, vapour, hot water, refrigerant,..."))

        self.tc4 = FloatEntry(self.page0,
                              ipart=6,                       # max n. of characters left of decimal point
                              decimals=2,                    # max n. of characters right of decimal point
                              minval=0.,                     # min value accepted
                              maxval=999999.,                # max value accepted
                              value=0.,                      # initial value
                              unitdict='MASSORVOLUMEFLOW',            # values for the units chooser
                              #label=_U("Nominal production"), # label
                              label=_U("Nominal production or circulation rate (specify units)"),
                              tip=_U(" "))

#In StaticBox "Temperatures and pressures" within "Distribution of heat/cold" 
        self.tc5 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Outlet temperature (to distribution)"),
                              tip=_U("Temperature of supply medium from equipment"))

        self.tc6 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Return temperature"),
                              tip=_U("Temperature of return of the supply medium from distribution (e.g. return temperature of condensate in a vapour system)"))

        self.tc7 = FloatEntry(self.page0,
                              ipart=4, decimals=3, minval=0., maxval=100., value=0.,
                              unitdict=None,
                              label=_U("Rate of recirculation"),
                              tip=_U("Specify the rate of recirculation of the heat/cold supply medium (100% = totally closed circuit)"))


        self.tc8 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Temperature of feed-up in open circuit"),
                              tip=_U("Temperature of medium of distribution of heat/cold entering in open circuit (e.g. temperature of water entering from network...)"))

        self.tc9 = FloatEntry(self.page0,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict='PRESSURE',
                              label=_U("Pressure of heat or cold distribution medium"),
                              tip=_U("Working pressure for the heat/cold supply medium"))


#In StaticBox "Piping specifications" within "Distribution of heat/cold" 
        self.tc11 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=999999., value=0.,
                              unitdict='LENGTH',
                              label=_U("Total length of distribution piping or ducts (one way)"),
                              tip=_U("Only distance one way"))

        self.tc12 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=1.e+12, value=0.,
                              unitdict='HEATTRANSFERCOEF',
                              label=_U("Total coefficient of heat losses for piping or ducts"),
                              tip=_U("For the whole duct: go and return"))

        self.tc13 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=999999., value=0.,
                              unitdict='LENGTH',
                              label=_U("Mean pipe diameter"),
                              tip=_U(" "))

        self.tc14 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=999999., value=0.,
                              unitdict='LENGTH',
                              label=_U("Insulation thickness"),
                              tip=_U(" "))
        #
        # Right panel controls
        #
        fp.changeFont(size=TYPE_SIZE_RIGHT)
        f = FieldSizes(wHeight=HEIGHT_RIGHT,wLabel=LABEL_WIDTH_RIGHT)

        self.tc15 = IntEntry(self.page1,
                             minval=0, maxval=100, value=0,
                             label=_U("Number of storage units"),
                             tip=_U("Specify the number of storage units of the same type"))

        self.tc16 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=1.e+12, value=0.,
                              unitdict='VOLUME',
                              label=_U("Volume of one storage unit"),
                              tip=_U("Volume of the storage medium of a single single storage unit"))

        self.tc17 = ChoiceEntry(self.page1,
                               values=TRANSSTORAGETYPES.values(),
                               label=_U("Type of heat storage"),
                               tip=_U("Select from predefined list"))

        self.tc18 = FloatEntry(self.page1,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict='PRESSURE',
                              label=_U("Pressure of heat storage medium"),
                              tip=_U("Pressure of the process medium entering the storage unit if different from storage medium"))

        self.tc19 = FloatEntry(self.page1,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_U("Maximum temperature of the storage"),
                              tip=_U("The maximum temperature to which storage unit can be operated"))



        self.buttonOK = wx.Button(self,wx.ID_OK,_U("OK"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,_U("Cancel"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        self.buttonDeleteDistribution = wx.Button(self.page0,-1,_U("Delete distribution"))
        self.buttonDeleteDistribution.SetMinSize((136, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteDistribution, self.buttonDeleteDistribution)
        self.buttonDeleteDistribution.SetFont(fp.getFont())

        self.buttonAddDistribution = wx.Button(self.page0, -1, _U("Add distribution"))
        self.buttonAddDistribution.SetMinSize((136, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddDistribution, self.buttonAddDistribution)
        self.buttonAddDistribution.SetFont(fp.getFont())



    def __do_layout(self):
        # global sizer for panel. Contains notebook w/two tabs + buttons Cancel and Ok
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)
        # sizer for left tab
        sizerPage0 = wx.BoxSizer(wx.HORIZONTAL)

        # panel 0, left part, distribution list
        sizer_dl = wx.StaticBoxSizer(self.frame_distrib_list, wx.VERTICAL)
        sizer_dl.Add(self.listBoxDistributionList, 1, wx.EXPAND, 0)
        sizer_dl.Add(self.buttonAddDistribution, 0, wx.ALIGN_RIGHT, 0)
        sizer_dl.Add(self.buttonDeleteDistribution, 0, wx.ALIGN_RIGHT, 0)
        sizerPage0.Add(sizer_dl, 1, wx.EXPAND|wx.TOP, 20)

        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_VERTICAL
        flagText = wx.ALIGN_CENTER_VERTICAL

        # panel 0, right part, distribution
        sizer_gd = wx.StaticBoxSizer(self.frame_general_data, wx.VERTICAL)
        sizer_gd.Add(self.tc1, 0, flagText, 2)
        sizer_gd.Add(self.tc3, 0, flagText, 2)
        sizer_gd.Add(self.tc4, 0, flagText, 2)
        
        sizer_tp = wx.StaticBoxSizer(self.frame_temp_pressures, wx.VERTICAL)
        sizer_tp.Add(self.tc5, 0, flagText, 2)
        sizer_tp.Add(self.tc6, 0, flagText, 2)
        sizer_tp.Add(self.tc7, 0, flagText, 2)
        sizer_tp.Add(self.tc8, 0, flagText, 2)
        sizer_tp.Add(self.tc9, 0, flagText, 2)
        
        sizer_ps = wx.StaticBoxSizer(self.frame_piping_specs, wx.VERTICAL)
        sizer_ps.Add(self.tc11, 0, flagText, 2)
        sizer_ps.Add(self.tc12, 0, flagText, 2)
        sizer_ps.Add(self.tc13, 0, flagText, 2)
        sizer_ps.Add(self.tc14, 0, flagText, 2)

        sizer_hc = wx.StaticBoxSizer(self.frame_distrib_heat_cold, wx.VERTICAL)
        sizer_hc.Add(sizer_gd, 3, wx.EXPAND|wx.ALL, 4)
        sizer_hc.Add(sizer_tp, 5, wx.EXPAND|wx.ALL, 4)
        sizer_hc.Add(sizer_ps, 4, wx.EXPAND|wx.ALL, 4)

        sizerPage0.Add(sizer_hc, 2, wx.EXPAND|wx.TOP, 20)
        self.page0.SetSizer(sizerPage0)

        #panel 1, storage
        sizer_st = wx.StaticBoxSizer(self.frame_storage, wx.VERTICAL)
        sizer_st.Add(self.tc15, 0, flagText, 0)
        sizer_st.Add(self.tc16, 0, flagText, 0)
        sizer_st.Add(self.tc17, 0, flagText, 0)
        sizer_st.Add(self.tc18, 0, flagText, 0)
        sizer_st.Add(self.tc19, 0, flagText, 0)
        self.page1.SetSizer(sizer_st)
        
        self.notebook.AddPage(self.page0, _U('Distribution'))
        self.notebook.AddPage(self.page1, _U('Storage'))
        sizerGlobal.Add(self.notebook, 1, wx.EXPAND, 0)

        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)
        sizerGlobal.Add(sizerOKCancel, 0, wx.TOP|wx.ALIGN_RIGHT, 0)

        self.SetSizer(sizerGlobal)
        self.Layout()


#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		


    def OnListBoxDistributionListListboxClick(self, event):
        self.pipeName = self.listBoxDistributionList.GetStringSelection()
        pipes = Status.DB.qdistributionhc.\
                Questionnaire_id[Status.PId].\
                AlternativeProposalNo[Status.ANo].\
                Pipeduct[check(self.pipeName)]

        if len(pipes) > 0:
            p = pipes[0]
        else:
            logDebug("PanelQ5 (ListBoxClick): no pipe with name %s in database"%self.pipeName)
            return
        
        self.pipeNo = p.PipeDuctNo
        self.pipeID = p.QDistributionHC_ID
        
        self.tc1.SetValue(p.Pipeduct)
#        self.tc2.SetValue(str(p.HeatFromQGenerationHC_id)) #SD: parameter excluded)  

        fluidDict = Status.prj.getFluidDict()
        
        if p.HeatDistMedium is not None:
            fluidID = int(p.HeatDistMedium)
            setUnitsFluidDensity(fluidID)
            #fluidName = fluidDict[p.HeatDistMedium]#SD
            fluidName = fluidDict[fluidID] #SD key must be immutable type, changed to -> int       
            self.tc3.SetValue(fluidName)  

        self.tc4.SetValue(str(p.DistribCircFlow))
        self.tc5.SetValue(str(p.ToutDistrib))
        self.tc6.SetValue(str(p.TreturnDistrib))
        self.tc7.SetValue(str(p.PercentRecirc))
        self.tc8.SetValue(str(p.Tfeedup))
        self.tc9.SetValue(str(p.PressDistMedium))
##        self.tc10.SetValue(str(p.PercentCondRecovery))
        self.tc11.SetValue(str(p.TotLengthDistPipe))
        self.tc12.SetValue(str(p.UAPipe))
        self.tc13.SetValue(str(p.DDistPipe))
        self.tc14.SetValue(str(p.DeltaDistPipe))		
        self.tc15.SetValue(str(p.NumStorageUnits)) 
        self.tc16.SetValue(str(p.VUnitStorage))
        if p.TypeStorage in TRANSSTORAGETYPES: self.tc17.SetValue(TRANSSTORAGETYPES[p.TypeStorage])#SD
        self.tc18.SetValue(str(p.PmaxStorage))
        self.tc19.SetValue(str(p.TmaxStorage))


    def OnButtonOK(self, event):

        if Status.PId == 0:
	    return
        pipeName = self.tc1.GetValue()

# assure that a name has been entered before continuing
        if len(pipeName) == 0 or pipeName is None:
            showWarning(_("You have to enter a name for the new pipe before saving"))
            return

        pipes = Status.DB.qdistributionhc.\
                Pipeduct[check(pipeName)].\
                Questionnaire_id[Status.PId].\
                AlternativeProposalNo[Status.ANo]

        logTrack("PanelQ5 (OK Button): data entry confirmed for pipe %s"%pipeName)

	if len(pipes) == 0:
            pipe = Status.prj.addPipeDummy()     

        elif len(pipes) == 1:
            pipe = pipes[0]
        else:
	    self.main.showError(_U("PanelQ5 (ButtonOK): Branch name has to be a uniqe value!"))
	    return


	fluidDict = Status.prj.getFluidDict()
        fluidID = findKey(fluidDict,self.tc3.GetValue(text=True))
        if fluidID is not None:
            setUnitsFluidDensity(fluidID)
	
	massFlow = self.tc4.GetValue()

	tmp = {
		"Questionnaire_id":Status.PId,
		"Pipeduct":check(pipeName),
                
		"HeatDistMedium":check(fluidID),                
		"DistribCircFlow":check(massFlow), 
		"ToutDistrib":check(self.tc5.GetValue()), 
		"TreturnDistrib":check(self.tc6.GetValue()), 
		"PercentRecirc":check(self.tc7.GetValue()), 
		"Tfeedup":check(self.tc8.GetValue()), 
		"PressDistMedium":check(self.tc9.GetValue()),
                
		"TotLengthDistPipe":check(self.tc11.GetValue()), 
		"UAPipe":check(self.tc12.GetValue()), 
		"DDistPipe":check(self.tc13.GetValue()), 
		"DeltaDistPipe":check(self.tc14.GetValue()), 		
		"NumStorageUnits":check(self.tc15.GetValue()),  
		"VUnitStorage":check(self.tc16.GetValue()),
                "TypeStorage":check(findKey(TRANSSTORAGETYPES,self.tc17.GetValue(text=True))),
		"PmaxStorage":check(self.tc18.GetValue()), 
		"TmaxStorage":check(self.tc19.GetValue())
	}
	pipe.update(tmp)               
	Status.SQL.commit()
	
	self.pipeName = pipeName
	self.fillPage()
                          
    def OnButtonCancel(self, event):
        self.clear()
        event.Skip()

    def OnButtonDeleteDistribution(self, event):
        logTrack("PanelQ5 (DELETE Button): deleting pipe ID %s"%self.pipeID)
        Status.prj.deletePipe(self.pipeID)
        self.clear()
        self.fillPage()
        event.Skip()

    def OnButtonAddDistribution(self, event):
        self.clear()
        
#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

    def display(self):
        self.clear()
        self.fillChoiceOfHDMedium()
        self.tc17.SetValue(TRANSSTORAGETYPES.values())
        self.fillPage()
        self.Show()


    def fillChoiceOfHDMedium(self):
        fluidDict = Status.prj.getFluidDict()
        fluidNames = fluidDict.values()
        self.tc3.entry.Clear()
        for name in fluidNames:
            self.tc3.entry.Append(name)
    
##

    def fillPage(self):
        self.listBoxDistributionList.Clear()

        pipeList = Status.prj.getPipeList("Pipeduct")
        for pipeName in pipeList:
            self.listBoxDistributionList.Append(pipeName)
            
        if self.pipeName is not None:
            self.listBoxDistributionList.SetStringSelection(self.pipeName)

    def clear(self):
        self.tc1.SetValue('')
#        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
        self.tc6.SetValue('')
        self.tc7.SetValue('')
        self.tc8.SetValue('')
        self.tc9.SetValue('')
##        self.tc10.SetValue('')
        self.tc11.SetValue('')
        self.tc12.SetValue('')
        self.tc13.SetValue('')
        self.tc14.SetValue('')
        self.tc15.SetValue('')
        self.tc16.SetValue('')
##        self.tc17.SetValue('')
        self.tc18.SetValue('')
        self.tc19.SetValue('')
        
        
