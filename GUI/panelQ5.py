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
#	Version No.: 0.07
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger  02/05/2008
#                           Tom Sobota      03/05/2008
#                           Hans Schweiger  05/05/2008
#                           Tom Sobota      30/05/2008
#                           Stoyan Danov    10/06/2008
#                           Stoyan Danov    16/06/2008
#
#       Changes to previous version:
#       02/05/08:       AlternativeProposalNo added in queries for table qdistributionhc
#       03/05/2008      Changed display format
#       05/05/2008:     Event handlers changed
#       30/05/2008      Adapted to new display and data entry classes
#       10/06/2008      Text changes
#       16/06/2008      SD: OnListBoxDistributionListListboxClick - rearrange,
#                       ->changed to -> fluidName = fluidDict[int(p.HeatDistMedium)] because of key error,
#                       but problem to delete branch if Medium ==NULL !!! to arrange
#                           OnButtonOK, display() added, unitdict, digits values,
#                           changed IntEntry->FloatEntry tc7,tc10,tc13,tc14
#                           in OnButtonOK: -> VUnitStorage in turn of VtotStorage 
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
from units import *


# constants that control the default field sizes

HEIGHT         =  27
LABELWIDTH     = 180
DATAENTRYWIDTH = 100
UNITSWIDTH     =  90


class PanelQ5(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        self._init_ctrls(parent)
        self.__do_layout()

        
    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ5', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.page0 = wx.Panel(self.notebook) # left panel
        self.page1 = wx.Panel(self.notebook) # right panel

        self.sizer_5_staticbox = wx.StaticBox(self.page0, -1, _("Distribution list"))
        self.sizer_5_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_7_staticbox = wx.StaticBox(self.page0, -1, _("Distribution of heat/cold"))
        self.sizer_7_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_13_staticbox = wx.StaticBox(self.page1, -1, "Storage")
        self.sizer_13_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        # left panel
        
        self.listBoxDistributionList = wx.ListBox(self.page0,-1,choices=[])
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxDistributionListListboxClick, self.listBoxDistributionList)

        #
        # set default field sizes and font properties.
        # Each data entry class has 4 configurable parameters for field size:
        # 1. The height. This is the same for all the widgets that make the class
        # 2. The width of the label
        # 3. The width of the entry widget
        # 4. The width of the unit chooser.
        # and 7 parameters for font:
        # 1. fSize font size
        # 2. fFamily font family
        # 3. fStyle font style
        # 4. fWeight font weight
        # 5. fUnderline underlined or not
        # 6. fFacename font face
        # 7. fEncoding font encoding
        # All these parameters have reasonable defaults.
        #
        f = FieldSizes(wHeight=HEIGHT,wLabel=LABELWIDTH,wData=DATAENTRYWIDTH,wUnits=UNITSWIDTH,fSize=9)

        self.tc1 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Name of the branch / distribution system"),
                             tip=_("Give some brief name or number of the distribution tube consistent with the hydraulic scheme"))
        
       
        self.tc3 = ChoiceEntry(self.page0,
                               values=[],
                               label=_("Heat or cold distribution medium"),
                               tip=_("e.g air for drying process, vapour, hot water, refrigerant,..."))

        self.tc4 = FloatEntry(self.page0,
                              ipart=6,                       # max n. of characters left of decimal point
                              decimals=2,                    # max n. of characters right of decimal point
                              minval=0.,                     # min value accepted
                              maxval=999999.,                # max value accepted
                              value=0.,                      # initial value
                              unitdict=mergeDict(UNITS['VOLUMEFLOW'],UNITS['MASSFLOW']),            # values for the units chooser
                              #label=_("Nominal production"), # label
                              label=_("Nominal production or circulation rate (specify units)"),
                              tip=_(" "),
                              fontsize=6)

        self.tc5 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['TEMPERATURE'],
                              label=_("Outlet temperature (to distribution)"),
                              tip=_("Temperature of supply medium from equipment"))

        self.tc6 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['TEMPERATURE'],
                              label=_("Return temperature"),
                              tip=_("Temperature of return of the supply medium from distribution (e.g. return temperature of condensate in a vepour system)"))

        self.tc7 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict={},
                              label=_("Percentage of recirculation"),
                              tip=_("Specify the percentage of recirculation of the heat/cold supply medium (100% = totally closed circuit)"))


        self.tc8 = FloatEntry(self.page0,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['TEMPERATURE'],
                              label=_("Temperature of feed-up in open circuit"),
                              tip=_("Temperature of medium of distribution of heat/cold entering in open circuit (e.g. temperature of water entering from network...)"))

        self.tc9 = FloatEntry(self.page0,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict=UNITS['PRESSURE'],
                              label=_("Pressure of heat or cold distribution medium"),
                              tip=_("Working pressure for the heat/cold supply medium"))

        self.tc10 = FloatEntry(self.page0,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict={},
                              label=_("Percentage of condensate recovery (steam boilers only)"),
                              tip=_("Percentage of condensate returned to boiler"))

        self.tc11 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=999999., value=0.,
                              unitdict=UNITS['LENGTH'],
                              label=_("Total length of distribution piping or ducts (one way)"),
                              tip=_("Only distance one way"))

        self.tc12 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=999999., value=0.,
                              unitdict=UNITS['HEATTRANSFERCOEF'],
                              label=_("Total coefficient of heat losses for piping or ducts"),
                              tip=_("For the whole duct: go and return"))

        self.tc13 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=999999., value=0.,
                              unitdict=UNITS['LENGTH'],
                              label=_("Mean pipe diameter"),
                              tip=_(" "))

        self.tc14 = FloatEntry(self.page0,
                              ipart=6, decimals=2, minval=0., maxval=999999., value=0.,
                              unitdict=UNITS['LENGTH'],
                              label=_("Insulation thickness"),
                              tip=_(" "))

        # right panel

        self.tc15 = IntEntry(self.page1,
                             minval=0, maxval=100, value=0,
                             label=_("Number of storage units"),
                             tip=_("Specify the number of storage units of the same type"),
                             hasunits=False)

        self.tc16 = FloatEntry(self.page1,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict=UNITS['VOLUME'],
                              label=_("Volume of one storage unit"),
                              tip=_("Volume of the storage medium of a single single storage unit"))

        self.tc17 = ChoiceEntry(self.page1,
                               values=TRANSSTORAGETYPES.values(),
                               label=_("Type of heat storage"),
                               tip=_("Select from predefined list"))

        self.tc18 = FloatEntry(self.page1,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict=UNITS['PRESSURE'],
                              label=_("Pressure of heat storage medium"),
                              tip=_("Pressure of the process medium entering the storage unit if different from storage medium"))

        self.tc19 = FloatEntry(self.page1,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict=UNITS['TEMPERATURE'],
                              label=_("Maximum temperature of the storage"),
                              tip=_("The maximum temperature to which storage unit can be operated"))



        self.buttonOK = wx.Button(self,wx.ID_OK,_("OK"))
        #self.buttonOK.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,_("Cancel"))
        #self.buttonCancel.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        self.buttonDeleteDistribution = wx.Button(self.page0,-1,_("Delete distribution"))
        self.buttonDeleteDistribution.SetMinSize((136, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteDistribution, self.buttonDeleteDistribution)

        self.buttonAddDistribution = wx.Button(self.page0, -1, _("Add distribution"))
        self.buttonAddDistribution.SetMinSize((136, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddDistribution, self.buttonAddDistribution)



    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.StaticBoxSizer(self.sizer_13_staticbox, wx.VERTICAL)
        #grid_sizer_5 = wx.FlexGridSizer(5, 2, 3, 3)
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.VERTICAL)
        #grid_sizer_1 = wx.FlexGridSizer(10, 2, 3, 3)# r,c,seph,sepv
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)

        # panel 0, left part, distribution list
        sizer_5.Add(self.listBoxDistributionList, 1, wx.EXPAND, 0)
        sizer_5.Add(self.buttonAddDistribution, 0, wx.ALIGN_RIGHT, 0)
        sizer_5.Add(self.buttonDeleteDistribution, 0, wx.ALIGN_RIGHT, 0)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)

        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_VERTICAL
        flagText = wx.ALIGN_CENTER_VERTICAL

        # panel 0, right part, distribution
        sizer_11.Add(self.tc1, 0, flagText, 2)
#        sizer_11.Add(self.tc2, 0, flagText, 2)
        sizer_11.Add(self.tc3, 0, flagText, 2)
        sizer_11.Add(self.tc4, 0, flagText, 2)
        sizer_11.Add(self.tc5, 0, flagText, 2)
        sizer_11.Add(self.tc6, 0, flagText, 2)
        sizer_11.Add(self.tc7, 0, flagText, 2)
        sizer_11.Add(self.tc8, 0, flagText, 2)
        sizer_11.Add(self.tc9, 0, flagText, 2)
        sizer_11.Add(self.tc10, 0, flagText, 2)
        sizer_11.Add(self.tc11, 0, flagText, 2)
        sizer_11.Add(self.tc12, 0, flagText, 2)
        sizer_11.Add(self.tc13, 0, flagText, 2)
        sizer_11.Add(self.tc14, 0, flagText, 2)

        sizer_7.Add(sizer_11, 1, wx.LEFT|wx.EXPAND, 40)
        sizer_6.Add(sizer_7, 3, wx.EXPAND, 0)#

        sizer_4.Add(sizer_6, 2, wx.EXPAND, 0)
        self.page0.SetSizer(sizer_4)

        #panel 1, storage
        sizer_15.Add(self.tc15, 0, flagText, 0)
        sizer_15.Add(self.tc16, 0, flagText, 0)
        sizer_15.Add(self.tc17, 0, flagText, 0)
        sizer_15.Add(self.tc18, 0, flagText, 0)
        sizer_15.Add(self.tc19, 0, flagText, 0)

        sizer_13.Add(sizer_15, 1, wx.LEFT|wx.TOP|wx.EXPAND, 10)
        sizer_10.Add(sizer_13, 1, wx.EXPAND, 0)
        self.page1.SetSizer(sizer_10)
        self.notebook.AddPage(self.page0, _('Distribution'))
        self.notebook.AddPage(self.page1, _('Storage'))
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


    def OnListBoxDistributionListListboxClick(self, event):
        self.pipeName = str(self.listBoxDistributionList.GetStringSelection())
        pipes = Status.DB.qdistributionhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].Pipeduct[self.pipeName]

        p = pipes[0]
        self.pipeNo = p.PipeDuctNo
        self.pipeID = p.QDistributionHC_ID
        
        self.tc1.SetValue(str(p.Pipeduct))
#        self.tc2.SetValue(str(p.HeatFromQGenerationHC_id)) #SD: parameter excluded)  

        fluidDict = Status.prj.getFluidDict()        
        if p.HeatDistMedium is not None:
            #fluidName = fluidDict[p.HeatDistMedium]#SD
            fluidName = fluidDict[int(p.HeatDistMedium)] #SD key must be immutable type, changed to -> int       
            self.tc3.SetValue(fluidName)  

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
        self.tc16.SetValue(str(p.VUnitStorage))
        if p.TypeStorage in TRANSSTORAGETYPES: self.tc17.SetValue(TRANSSTORAGETYPES[str(p.TypeStorage)])#SD
        self.tc18.SetValue(str(p.PmaxStorage))
        self.tc19.SetValue(str(p.TmaxStorage))


    def OnButtonOK(self, event):
        #TS20080530 tc2 getvalue is missing.
        if Status.PId == 0:
	    return
        pipeName = self.check(self.tc1.GetValue())
        pipes = Status.DB.qdistributionhc.Pipeduct[pipeName].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]

	if pipeName != 'NULL' and len(pipes) == 0:
            pipe = Status.prj.addPipeDummy()     

        elif pipeName != 'NULL' and len(pipes) == 1:
            pipe = pipes[0]
        else:
	    print "PanelQ5 (ButtonOK): Branch name has to be a uniqe value!"
	    return

	print 'PanelQ5 (ButtonOK): pipe =', pipe
	print 'PanelQ5 (ButtonOK): pipes =', pipes

	fluidDict = Status.prj.getFluidDict()#SD

	tmp = {
		"Questionnaire_id":Status.PId,
		"Pipeduct":self.check(self.tc1.GetValue()),
		"HeatDistMedium":check(findKey(fluidDict,self.tc3.entry.GetStringSelection())), #SD               
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
		"VUnitStorage":self.check(self.tc16.GetValue()),
                "TypeStorage":check(findKey(TRANSSTORAGETYPES,self.tc17.entry.GetStringSelection())),#SD
		"PmaxStorage":self.check(self.tc18.GetValue()), 
		"TmaxStorage":self.check(self.tc19.GetValue())
	}
	pipe.update(tmp)               
	Status.SQL.commit()
	self.fillPage()
                          

    def OnButtonCancel(self, event):
        self.clear()
        event.Skip()

    def OnButtonDeleteDistribution(self, event):
        Status.prj.deletePipe(self.pipeID)
        self.clear()
        self.fillPage()
        event.Skip()

    def OnButtonAddDistribution(self, event):
        self.clear()
        
#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

#SD2008-6-16
    def display(self):
        self.fillChoiceOfHDMedium()
        self.clear()
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
        pipes = Status.DB.qdistributionhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(pipes) > 0:
            for pipe in pipes:
                self.listBoxDistributionList.Append (str(pipe.Pipeduct))


    def check(self, value):
        if value <> "" and value <> "None":
            return value
        else:
            return 'NULL'

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
        self.tc10.SetValue('')
        self.tc11.SetValue('')
        self.tc12.SetValue('')
        self.tc13.SetValue('')
        self.tc14.SetValue('')
        self.tc15.SetValue('')
        self.tc16.SetValue('')
        self.tc17.SetValue('')
        self.tc18.SetValue('')
        self.tc19.SetValue('')
        
        
