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
#	Version No.: 0.05
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger  02/05/2008
#                           Tom Sobota      03/05/2008
#                           Hans Schweiger  05/05/2008
#
#       Changes to previous version:
#       02/05/08:       AlternativeProposalNo added in queries for table qdistributionhc
#       03/05/2008      Changed display format
#       05/05/2008:     Event handlers changed
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
from wx.lib.stattext import *
import pSQL
import HelperClass
from status import Status


# constants
LABELWIDTH=180
TEXTENTRYWIDTH=280


class Label(wx.lib.stattext.GenStaticText):
    # auxiliary class for labels (static text)
    # will show a short descriptive string and
    # generate a longer tooltip.
    # the tooltip is also associated to the text control
    #
    w0 = None
    w1 = None
    def __init__(self,parent,txtctrl,text,tip,width0=None,width1=None):
        wx.lib.stattext.GenStaticText.__init__(self,ID=-1,parent=parent,label='',
                                              style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
        self.SetLabel(text)
        self.SetToolTip(wx.ToolTip(tip))
        txtctrl.SetToolTip(wx.ToolTip(tip))
        h = self.GetMinHeight()
        if width0 is None:
            if Label.w0 is not None:
                self.SetMinSize((Label.w0, h))
        else:
            Label.w0 = width0
            self.SetMinSize((Label.w0, h))
        if width1 is None:
            if Label.w1 is not None:
                txtctrl.SetMinSize((Label.w1, h))
        else:
            txtctrl.SetMinSize((width1, h))
            Label.w1 = width1


class PanelQ5(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
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


        self.tc1 = wx.TextCtrl(self.page0,-1,'')
        self.st1 = Label(self.page0,self.tc1,_("Branch"),
                         _("Name of the branch / distribution system"),
                         LABELWIDTH, TEXTENTRYWIDTH)

        self.choiceOfSource = wx.Choice(self.page0,-1,choices=[])
        self.st2 = Label(self.page0,self.choiceOfSource,_("Heat comes from?"),
                         _("Heat or cold supply comes from equipment(s) no.:"))

	self.tc3 = wx.TextCtrl(self.page0,-1,'')
        self.st3 = Label(self.page0,self.tc3,_("Distribution medium"),
                         _("Heat or cold distribution medium"))

        self.tc4 = wx.TextCtrl(self.page0,-1,'')
        self.st4 = Label(self.page0,self.tc4,_("Nominal production"),
                         _("Nominal production or circulation rate(specify units) (mü/hkg/h)"))

        self.tc5 = wx.TextCtrl(self.page0,-1,'')
        self.st5 = Label(self.page0,self.tc5,_("Outlet temperature"),
                         _("Outlet temperature (to distribution) (ºC)"))

        self.tc6 = wx.TextCtrl(self.page0,-1,'')
        self.st6 = Label(self.page0,self.tc6,_("Return temperature"),
                         _("Return temperature (from distribution) (ºC)"))

        self.tc7 = wx.TextCtrl(self.page0,-1,'')
        self.st7 = Label(self.page0,self.tc7,_("% of recirculation"),
                         _("Percentage of recirculation (%)"))

        self.tc8 = wx.TextCtrl(self.page0,-1,'')
        self.st8 = Label(self.page0,self.tc8,_("Feed-up"),
                         _("Feed-up in open circuit (ºC)"))

        self.tc9 = wx.TextCtrl(self.page0,-1,'')
        self.st9 = Label(self.page0,self.tc9,_("Pressure"),
                         _("Pressure (bar)"))

        self.tc10 = wx.TextCtrl(self.page0,-1,'')
        self.st10 = Label(self.page0,self.tc10,_("% condensate recovery"),
                          _("Percentage of condensate recovery (steam boilers only) (%)"))

        self.tc11 = wx.TextCtrl(self.page0,-1,'')
        self.st11 = Label(self.page0,self.tc11,_("Total length of piping"),
                          _("Total length of distribution piping or ducts (one way) (m)"))

        self.tc12 = wx.TextCtrl(self.page0,-1,'')
        self.st12 = Label(self.page0,self.tc12,_("Total coef.heat losses"),
                          _("Total coefficient of heat losses for piping or ducts (kW/K)"))

        self.tc13 = wx.TextCtrl(self.page0,-1,'')
        self.st13 = Label(self.page0,self.tc13,_("Mean pipe diameter"),
                          _("Mean pipe diameter (mm)"))

        self.tc14 = wx.TextCtrl(self.page0,-1,'')
        self.st14 = Label(self.page0,self.tc14,_("Insulation thickness"),
                          _("Insulation thickness (mm)"))

        # right panel

        self.tc15 = wx.TextCtrl(self.page1,-1,'')
        self.st15 = Label(self.page1,self.tc15,_("Nº of storage units"),
                          _("Number of heat or cold storage units"))

        self.tc16 = wx.TextCtrl(self.page1,-1,'')
        self.st16 = Label(self.page1,self.tc16,_("Storage volume"),
                          _("Total volume of the storage (mü)"))

        self.tc17 = wx.TextCtrl(self.page1,-1,'')
        self.st17 = Label(self.page1,self.tc17,_("Type of storage"),
                          _("Type of storage / storage medium"))

        self.tc18 = wx.TextCtrl(self.page1,-1,'')
        self.st18 = Label(self.page1,self.tc18,_("Max pressure"),
                          _("Maximum pressure (bar)"))

        self.tc19 = wx.TextCtrl(self.page1,-1,'')
        self.st19 = Label(self.page1,self.tc19,_("Max temperature"),
                          _("Maximum temperature of the storage (ºC)"))



        self.buttonOK = wx.Button(self,wx.ID_OK,_("OK"))
        self.buttonOK.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,_("Cancel"))
        self.buttonCancel.SetMinSize((125, 32))
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
        grid_sizer_5 = wx.FlexGridSizer(5, 2, 3, 3)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(10, 2, 3, 3)# r,c,seph,sepv
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)

        # panel 0, left part, distribution list
        sizer_5.Add(self.listBoxDistributionList, 1, wx.EXPAND, 0)
        sizer_5.Add(self.buttonAddDistribution, 0, wx.ALIGN_RIGHT, 0)
        sizer_5.Add(self.buttonDeleteDistribution, 0, wx.ALIGN_RIGHT, 0)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)

        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_VERTICAL
        flagText = wx.ALIGN_CENTER_VERTICAL

        # panel 0, right part, distribution
        grid_sizer_1.Add(self.st1, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc1, 0, flagText, 2)
        grid_sizer_1.Add(self.st2, 0, flagLabel, 2)
        grid_sizer_1.Add(self.choiceOfSource, 0, flagText, 2)
        grid_sizer_1.Add(self.st3, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc3, 0, flagText, 2)
        grid_sizer_1.Add(self.st4, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc4, 0, flagText, 2)
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
        grid_sizer_1.Add(self.st11, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc11, 0, flagText, 2)
        grid_sizer_1.Add(self.st12, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc12, 0, flagText, 2)
        grid_sizer_1.Add(self.st13, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc13, 0, flagText, 2)
        grid_sizer_1.Add(self.st14, 0, flagLabel, 2)
        grid_sizer_1.Add(self.tc14, 0, flagText, 2)

        sizer_7.Add(grid_sizer_1, 1, wx.LEFT|wx.EXPAND, 40)
        sizer_6.Add(sizer_7, 3, wx.EXPAND, 0)#

        sizer_4.Add(sizer_6, 2, wx.EXPAND, 0)
        self.page0.SetSizer(sizer_4)

        #panel 1, storage
        grid_sizer_5.Add(self.st15, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc15, 0, flagText, 0)
        grid_sizer_5.Add(self.st16, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc16, 0, flagText, 0)
        grid_sizer_5.Add(self.st17, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc17, 0, flagText, 0)
        grid_sizer_5.Add(self.st18, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc18, 0, flagText, 0)
        grid_sizer_5.Add(self.st19, 0, flagLabel, 0)
        grid_sizer_5.Add(self.tc19, 0, flagText, 0)

        sizer_13.Add(grid_sizer_5, 1, wx.LEFT|wx.TOP|wx.EXPAND, 10)
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
        #self.tc2.SetValue(str(p.HeatFromQGenerationHC_id))   
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

    def OnButtonOK(self, event):
        if Status.PId == 0:
	    return

        pipeName = self.check(self.tc1.GetValue())
        pipes = Status.DB.qdistributionhc.Pipeduct[pipeName].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]

	if pipeName <> 'NULL' and len(pipes) == 0:

            newID = Status.prj.addPipeDummy()
            
	    tmp = {
		"Questionnaire_id":Status.PId,
		"Pipeduct":self.check(self.tc1.GetValue()),
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
		"TmaxStorage":self.check(self.tc19.GetValue())
		}

            q = Status.DB.qdistributionhc.QDistributionHC_ID[newID][0]
	    q.update(tmp)               
	    Status.SQL.commit()
	    self.fillPage()

	elif pipeName <> 'NULL' and len(pipes) == 1:

	    tmp = {
		"Pipeduct":self.check(self.tc1.GetValue()),
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
		"TmaxStorage":self.check(self.tc19.GetValue())
		}
	    
	    q = pipes[0]
	    q.update(tmp)               
	    Status.SQL.commit()
	    self.fillPage()
                          
	else:
	    self.showError("Pipeduct have to be an uniqe value!")

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
        #self.tc2.SetValue('')
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
        
        
