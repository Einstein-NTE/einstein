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
#	PanelQ7: Renewable energies
#
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota      06/05/2008
#
#       Changes to previous version:
#       06/05/2008      Changed display logic
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


class PanelQ7(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        self._init_ctrls(parent)
        self.__do_layout()

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ7', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()


        self.buttonOK = wx.Button(self,wx.ID_OK,"OK")
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,"Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)


        # page 0
        self.notebook = wx.Notebook(self, -1, style=0)
        self.page2 = wx.Panel(self.notebook, -1)
        self.page1 = wx.Panel(self.notebook, -1)
        self.page0 = wx.Panel(self.notebook, -1)

        self.sizer_5_staticbox = wx.StaticBox(self.page0, -1, "Main motivation for renewable energy use")
        self.sizer_5_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.sizer_7_staticbox = wx.StaticBox(self.page1, -1, "Solar thermal energy")
        self.sizer_7_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.sizer_8_staticbox = wx.StaticBox(self.page2, -1, "Biomass")
        self.sizer_8_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.sizer_10_staticbox = wx.StaticBox(self.page2, -1, "Availability of biomass from the processes")
        self.sizer_10_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.sizer_11_staticbox = wx.StaticBox(self.page2, -1, "Availability of biomass from the region")
        self.sizer_11_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.checkBox1 = wx.CheckBox(self.page0, -1, "Are you interested in the use of renewable energy?")
        self.checkBox2 = wx.CheckBox(self.page0, -1, "Possibility of saving fuel cost")
        self.checkBox3 = wx.CheckBox(self.page0, -1, "Contribution to a more ecologic supply")
        self.checkBox4 = wx.CheckBox(self.page0, -1,
                                     "Using solar energy helps for a better marketing of your products")

        self.checkBox5 = wx.CheckBox(self.page0, -1, "Other")
        self.tc1 = wx.TextCtrl(self.page0, -1,"Please explain here additional motives",
                               style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE)
        self.tc1.SetMinSize((650, 60))
        self.tc1.SetMaxSize((650, 60))


        # page 1
        self.labelRoof = wx.StaticText(self.page1, -1, "Roof")
        self.labelRoof.SetFont(wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.BOLD, 0, ""))
        self.labelGround = wx.StaticText(self.page1, -1, "Ground")
        self.labelGround.SetFont(wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.BOLD, 0, ""))
        
        self.tc6_1 = wx.TextCtrl(self.page1,-1,'')
        self.tc6_2 = wx.TextCtrl(self.page1,-1,'')
        self.st6 = Label(self.page1,[self.tc6_1,self.tc6_2],_("Available area"),
                         [_("Available area roof (m2)"),
                          _("Available area ground (m2)")],
                         200,160)

        self.tc7_1 = wx.TextCtrl(self.page1,-1,'')
        self.tc7_2 = wx.TextCtrl(self.page1,-1,'')
        self.st7 = Label(self.page1,[self.tc7_1,self.tc7_2],_("Inclination of the area"),
				 [_("Positioning of the roof area (inclination in degrees)"),
				 _("Positioning of the ground area (inclination in degrees)")])
                                  

        self.tc8_1 = wx.TextCtrl(self.page1,-1,'')
        self.tc8_2 = wx.TextCtrl(self.page1,-1,'')
        self.st8 = Label(self.page1,[self.tc8_1,self.tc8_2],_("Orientation of the area"),
				 [_("positioning of the roof area (orientation to the south)"),
                                  _("positioning of the ground area (orientation to the south)")])

        self.tc9_1 = wx.TextCtrl(self.page1,-1,'')
        self.tc9_2 = wx.TextCtrl(self.page1,-1,'')
        self.st9 = Label(self.page1,[self.tc9_1,self.tc9_2],_("Shading problems?"),
                         [_("Shading problems on roof?"),
                         _("Shading problems on ground?")])

        self.tc10_1 = wx.TextCtrl(self.page1,-1,'')
        self.tc10_2 = wx.TextCtrl(self.page1,-1,'')
        self.st10 = Label(self.page1,[self.tc10_1,self.tc10_2],_("Distance to process"),
				  [_("Distance to the technical room or process roof (m)"),
				  _("Distance to the technical room or process ground (m)")])

        self.tc11 = wx.TextCtrl(self.page1,-1,'')
        self.st11 = Label(self.page1,self.tc11,_("Type of roof"), _("Type of roof"))

        self.tc12 = wx.TextCtrl(self.page1,-1,'')
        self.st12 = Label(self.page1,self.tc12,_("Static load capacity"),
				  _("Static load capacity of the roof(s) (kg/mü)"))

        self.Choice1 = wx.Choice(self.page1, -1, choices=["No", "Yes"])
        self.st13 = Label(self.page1,self.Choice1,_("Scheme of building?"),
                          _("Enclosing of drawing or scheme of building? (yes/no)"))


        # page 2

        self.tc14 = wx.TextCtrl(self.page2,-1,'')
        self.st14 = Label(self.page2,self.tc14,_("Type of biomass"),
                          _("Type of biomass available from processes"),180,70)

        self.tc15_1 = wx.TextCtrl(self.page2,-1,'')
        self.tc15_2 = wx.TextCtrl(self.page2,-1,'')
        self.st15 = Label(self.page2,[self.tc15_1,self.tc15_2],_("Period of year"),
                          [_("Start of period of year the biomass is available (dd/mm-dd/mm)"),
                           _("End of period of year the biomass is available (dd/mm-dd/mm)")])

        self.tc16 = wx.TextCtrl(self.page2,-1,'')
        self.st16 = Label(self.page2,self.tc16,_("Duration of production"),
                          _("Number of days biomass is produced (days)"))

        self.tc17 = wx.TextCtrl(self.page2,-1,'')
        self.st17 = Label(self.page2,self.tc17,_("Daily quantity"),
                          _("Daily quantity of biomass (t/day)"))

        self.tc18 = wx.TextCtrl(self.page2,-1,'')
        self.st18 = Label(self.page2,self.tc18,_("Space availability"),
                          _("Space availability to stock biomass (m3)"))

        self.tc19 = wx.TextCtrl(self.page2,-1,'')
        self.st19 = Label(self.page2,self.tc19,_("LCV biomass"),
                          _("LCV biomass (kWh/kg)"))

        self.tc20 = wx.TextCtrl(self.page2,-1,'')
        self.st20 = Label(self.page2,self.tc20,_("Humidity"),
                          _("Humidity (%)"))



        self.tc21 = wx.TextCtrl(self.page2,-1,'')
        self.st21 = Label(self.page2,self.tc21,_("Type of biomass"),
                          _("Type of biomass available from the region"))

        self.tc22 = wx.TextCtrl(self.page2,-1,'')
        self.st22 = Label(self.page2,self.tc22,_("Unit price"),
                          _("Unit price of biomass (EUR/t)"))

        self.tc23_1 = wx.TextCtrl(self.page2,-1,'')
        self.tc23_2 = wx.TextCtrl(self.page2,-1,'')
        self.st23 = Label(self.page2,[self.tc23_1,self.tc23_2],_("Period of availability"),
                          [_("Start of period of year the biomass is available (dd/mm-dd/mm)"),
                           _("End of period of year the biomass is available (dd/mm-dd/mm)")])

        self.tc24 = wx.TextCtrl(self.page2,-1,'')
        self.st24 = Label(self.page2,self.tc24,_("Duration of biomass prod."),
                          _("Number of days the biomass is produced (days)"))

        self.dummy1 = wx.StaticText(self.page1, -1, "")
        self.dummy2 = wx.StaticText(self.page1, -1, "")
        self.dummy3 = wx.StaticText(self.page1, -1, "")
        self.dummy4 = wx.StaticText(self.page1, -1, "")

    def __do_layout(self):
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.StaticBoxSizer(self.sizer_8_staticbox, wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.StaticBoxSizer(self.sizer_11_staticbox, wx.VERTICAL)
        grid_sizer_3 = wx.FlexGridSizer(4, 2, 2, 3)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.StaticBoxSizer(self.sizer_10_staticbox, wx.VERTICAL)
        grid_sizer_2 = wx.FlexGridSizer(7, 2, 2, 2)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(8, 3, 2, 2)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.checkBox1, 0, wx.ALL, 10)
        sizer_5.Add(self.checkBox2, 0, wx.ALL, 10)
        sizer_5.Add(self.checkBox3, 0, wx.ALL, 10)
        sizer_5.Add(self.checkBox4, 0, wx.ALL, 10)
        sizer_6.Add(self.checkBox5, 0, wx.ALL, 10)
        sizer_6.Add(self.tc1, 0, wx.ALL, 4)
        sizer_5.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_5, 1, wx.ALL|wx.EXPAND, 2)
        self.page0.SetSizer(sizer_2)
        grid_sizer_1.Add(self.dummy1, 0, 0, 0)
        grid_sizer_1.Add(self.labelRoof, 0, 0, 0)
        grid_sizer_1.Add(self.labelGround, 0, 0, 0)

        grid_sizer_1.Add(self.st6, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.tc6_1, 0, 0, 0)
        grid_sizer_1.Add(self.tc6_2, 0, 0, 0)

        grid_sizer_1.Add(self.st7, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.tc7_1, 0, 0, 0)
        grid_sizer_1.Add(self.tc7_2, 0, 0, 0)

        grid_sizer_1.Add(self.st8, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.tc8_1, 0, 0, 0)
        grid_sizer_1.Add(self.tc8_2, 0, 0, 0)
        
        grid_sizer_1.Add(self.st9, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.tc9_1, 0, 0, 0)
        grid_sizer_1.Add(self.tc9_2, 0, 0, 0)
        
        grid_sizer_1.Add(self.st10, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.tc10_1, 0, 0, 0)
        grid_sizer_1.Add(self.tc10_2, 0, 0, 0)
        
        grid_sizer_1.Add(self.st11, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.tc11, 0, 0, 0)
        grid_sizer_1.Add(self.dummy2, 0, 0, 0)
        
        grid_sizer_1.Add(self.st12, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.tc12, 0, 0, 0)
        grid_sizer_1.Add(self.dummy3, 0, 0, 0)
        
        grid_sizer_1.Add(self.st13, 0, 0, 0)
        grid_sizer_1.Add(self.Choice1, 0, 0, 0)
        grid_sizer_1.Add(self.dummy4, 0, 0, 0)
        
        sizer_7.Add(grid_sizer_1, 1, wx.ALL|wx.EXPAND, 20)
        self.page1.SetSizer(sizer_7)
        
        grid_sizer_2.Add(self.st14, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.tc14, 0, 0, 0)

        grid_sizer_2.Add(self.st15, 0, wx.ALIGN_RIGHT, 0)
        sizer_12.Add(self.tc15_1, 0, 0, 0)
        sizer_12.Add(self.tc15_2, 0, wx.LEFT, 2)
        grid_sizer_2.Add(sizer_12, 1, wx.EXPAND, 1)

        grid_sizer_2.Add(self.st16, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.tc16, 0, 0, 0)
        
        grid_sizer_2.Add(self.st17, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.tc17, 0, 0, 0)
        
        grid_sizer_2.Add(self.st18, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.tc18, 0, 0, 0)
        
        grid_sizer_2.Add(self.st19, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.tc19, 0, 0, 0)
        
        grid_sizer_2.Add(self.st20, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_2.Add(self.tc20, 0, 0, 0)
        sizer_10.Add(grid_sizer_2, 1, wx.ALL|wx.EXPAND, 20)
        sizer_9.Add(sizer_10, 1, wx.EXPAND, 0)

        grid_sizer_3.Add(self.st21, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_3.Add(self.tc21, 0, 0, 0)
        
        grid_sizer_3.Add(self.st22, 0, wx.ALIGN_RIGHT, 0)
        grid_sizer_3.Add(self.tc22, 0, 0, 0)
        
        grid_sizer_3.Add(self.st23, 0, wx.ALIGN_RIGHT, 0)
        sizer_13.Add(self.tc23_1, 0, 0, 0)
        sizer_13.Add(self.tc23_2, 0, wx.LEFT, 2)
        grid_sizer_3.Add(sizer_13, 1, wx.EXPAND, 0)
        
        grid_sizer_3.Add(self.st24, 0, 0, 0)
        grid_sizer_3.Add(self.tc24, 0, 0, 0)
        
        sizer_11.Add(grid_sizer_3, 1, wx.ALL|wx.EXPAND, 20)
        sizer_9.Add(sizer_11, 1, wx.EXPAND, 0)
        sizer_8.Add(sizer_9, 1, wx.EXPAND, 0)
        self.page2.SetSizer(sizer_8)
        self.notebook.AddPage(self.page0, "Main motivation")
        self.notebook.AddPage(self.page1, "Solar thermal energy")
        self.notebook.AddPage(self.page2, "Biomass")
        sizer_3.Add(self.notebook, 1, wx.EXPAND, 0)
        sizer_4.Add(self.buttonCancel, 0, wx.ALL|wx.ALIGN_RIGHT, 2)
        sizer_4.Add(self.buttonOK, 0, wx.ALL|wx.ALIGN_RIGHT, 2)
        sizer_3.Add(sizer_4, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer_3)
        self.Layout()




#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------

    def OnButtonCancel(self, event):
        event.Skip()

    def OnButtonOK(self, event):
        if Status.PId != 0:
            tmp = {
                "SurfAreaRoof":self.check(self.tc6_1.GetValue()),
                "SurfAreaGround":self.check(self.tc6_2.GetValue()),
                "InclinationRoof":self.check(self.tc7_1.GetValue()),
                "InclinationGround":self.check(self.tc7_2.GetValue()),
                "OrientationRoof":self.check(self.tc8_1.GetValue()),
                "OrientationGround":self.check(self.tc8_2.GetValue()),
                "ShadingRoof":self.check(self.tc9_1.GetValue()),
                "ShadingGround":self.check(self.tc9_2.GetValue()),
                "DistanceToRoof":self.check(self.tc10_1.GetValue()),
                "DistanceToGround":self.check(self.tc10_2.GetValue()),
                "RoofType":self.check(self.tc11.GetValue()),
                "RoofStaticLoadCap":self.check(self.tc12.GetValue()),
                "BiomassFromProc":self.check(self.tc14.GetValue()),
                "PeriodBiomassProcStart":self.check(self.tc15_1.GetValue()),
                "PeriodBiomassProcStop":self.check(self.tc15_2.GetValue()),
                "NDaysBiomassProc":self.check(self.tc16.GetValue()),
                "QBiomassProcDay":self.check(self.tc17.GetValue()),
                "SpaceBiomassProc":self.check(self.tc18.GetValue()),
                "LCVBiomassProc":self.check(self.tc19.GetValue()),
                "HumidBiomassProc":self.check(self.tc20.GetValue()),
                "BiomassFromRegion":self.check(self.tc21.GetValue()),
                "PriceBiomassRegion":self.check(self.tc22.GetValue()),
                "PeriodBiomassRegionStart":self.check(self.tc23_1.GetValue()),
                "PeriodBiomassRegionStop":self.check(self.tc23_2.GetValue()),
                "NDaysBiomassRegion":self.check(self.tc24.GetValue())
                }

            if len(Status.DB.qrenewables.Questionnaire_id[Status.PId]) == 0:
                # register does not exist, so store also id
                tmp["Questionnaire_id"] = Status.PId

                Status.DB.qrenewables.insert(tmp)
                Status.SQL.commit()

            else:
                # register does exist
                q = Status.DB.qrenewables.Questionnaire_id[Status.PId][0]
                q.update(tmp)
                Status.SQL.commit()
        event.Skip()


#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------


    def clear(self):
        self.checkBox1.SetValue(False)
        self.checkBox2.SetValue(False)
        self.checkBox3.SetValue(False)
        self.checkBox4.SetValue(False)
        self.checkBox5.SetValue(False)
        self.Choice1.GetCurrentSelection()
        self.tc6_1.Clear()
        self.tc6_2.Clear()
        self.tc7_1.Clear()
        self.tc7_2.Clear()
        self.tc8_1.Clear()
        self.tc8_2.Clear()
        self.tc9_1.Clear()
        self.tc9_2.Clear()
        self.tc10_1.Clear()
        self.tc10_2.Clear()
        self.tc11.Clear()
        self.tc12.Clear()
        self.tc14.Clear()
        self.tc15_1.Clear()
        self.tc15_2.Clear()
        self.tc16.Clear()
        self.tc17.Clear()
        self.tc18.Clear()
        self.tc19.Clear()
        self.tc20.Clear()
        self.tc21.Clear()
        self.tc22.Clear()
        self.tc23_1.Clear()
        self.tc23_2.Clear()
        self.tc24.Clear()



    def fillPage(self):
	if Status.PId == 0:
	    return

	if len(Status.DB.qrenewables.Questionnaire_id[Status.PId]) > 0:
	    p = Status.DB.qrenewables.Questionnaire_id[Status.PId][0]
	    if p.REInterest is None:
		self.checkBox1.SetValue(False)
	    else:
		self.checkBox1.SetValue(bool(p.REInterest))

	    if p.EnclBuildGroundSketch is None:
		self.checkBox5.SetValue(False)
	    else:
		self.checkBox5.SetValue(bool(p.EnclBuildGroundSketch))

	    self.tc6_1.SetValue(str(p.SurfAreaRoof))
	    self.tc6_2.SetValue(str(p.SurfAreaGround))
	    self.tc7_1.SetValue(str(p.InclinationRoof))
	    self.tc7_2.SetValue(str(p.InclinationGround))
	    self.tc8_1.SetValue(str(p.OrientationRoof))
	    self.tc8_2.SetValue(str(p.OrientationGround))
	    self.tc9_1.SetValue(str(p.ShadingRoof))
	    self.tc9_2.SetValue(str(p.ShadingGround))
	    self.tc10_1.SetValue(str(p.DistanceToRoof))
	    self.tc10_2.SetValue(str(p.DistanceToGround))
	    self.tc11.SetValue(str(p.RoofType))
	    self.tc12.SetValue(str(p.RoofStaticLoadCap))
	    self.tc14.SetValue(str(p.BiomassFromProc))
	    self.tc15_1.SetValue(str(p.PeriodBiomassProcStart))
	    self.tc15_2.SetValue(str(p.PeriodBiomassProcStop))
	    self.tc16.SetValue(str(p.NDaysBiomassProc))
	    self.tc17.SetValue(str(p.QBiomassProcDay))
	    self.tc18.SetValue(str(p.SpaceBiomassProc))
	    self.tc19.SetValue(str(p.LCVBiomassProc))
	    self.tc20.SetValue(str(p.HumidBiomassProc))
	    self.tc21.SetValue(str(p.BiomassFromRegion))
	    self.tc22.SetValue(str(p.PriceBiomassRegion))
	    self.tc23_1.SetValue(str(p.PeriodBiomassRegionStart))
	    self.tc23_2.SetValue(str(p.PeriodBiomassRegionStop))
	    self.tc24.SetValue(str(p.NDaysBiomassRegion))


