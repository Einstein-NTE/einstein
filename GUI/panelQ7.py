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
#   EINSTEIN Version No.: 1.0
#   Created by: 	Heiko Henning, Tom Sobota, Hans Schweiger, Stoyan Danov
#                       13/04/2008 - 13/10/2008
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
#	(C) copyleft energyXperts.NET (E4-Experts SL), Barcelona, Spain 2008/2009
#	http://www.energyxperts.net/
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license v3 as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================
import wx
from status import Status
from GUITools import *
from displayClasses import *
from units import *
from fonts import *
from einstein.modules.constants import *

# constants that control the default sizes
# 1. font sizes
TYPE_SIZE_LEFT    =   9
TYPE_SIZE_MIDDLE  =   9
TYPE_SIZE_RIGHT   =   9
TYPE_SIZE_TITLES  =  10

# 2. field sizes
HEIGHT_LEFT        =  29
LABEL_WIDTH_LEFT   = 260
HEIGHT_MIDDLE      =  29
LABEL_WIDTH_MIDDLE = 230
HEIGHT_RIGHT       =  26
LABEL_WIDTH_RIGHT  = 400
DATA_ENTRY_WIDTH   = 100
UNITS_WIDTH        = 120

def _U(text):
    return unicode(_(text),"utf-8")

#------------------------------------------------------------------------------
class PanelQ7(wx.Panel):
#------------------------------------------------------------------------------
    def __init__(self, parent, main):
	self.main = main
	logDebug("PanelQ7 created")
        self._init_ctrls(parent)
        self.__do_layout()
        self.selectedSurfaceName = None
        self.selectedSurfaceID = None

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ7', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()

        # access to font properties object
        fp = FontProperties()


        # page 0
        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook, -1)
        self.page1 = wx.Panel(self.notebook, -1)
        self.page2 = wx.Panel(self.notebook, -1)

        self.frame_main_motivation = wx.StaticBox(self.page0, -1, "Main motivation for renewable energy use")
        self.frame_main_motivation.SetForegroundColour(TITLE_COLOR)
        self.frame_main_motivation.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_surfaceslist = wx.StaticBox(self.page1, -1, _U("Solar energy surfaces"))
        self.frame_surfaceslist.SetForegroundColour(TITLE_COLOR)
        self.frame_surfaceslist.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_surfacedata = wx.StaticBox(self.page1, -1, _U("Surface  data"))
        self.frame_surfacedata.SetForegroundColour(TITLE_COLOR)
        self.frame_surfacedata.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_weatherdata = wx.StaticBox(self.page1, -1, "Weather data")
        self.frame_weatherdata.SetForegroundColour(TITLE_COLOR)
        self.frame_weatherdata.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_biomass_processes = wx.StaticBox(self.page2, -1, "Availability of biomass from the processes")
        self.frame_biomass_processes.SetForegroundColour(TITLE_COLOR)
        self.frame_biomass_processes.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_biomass_region = wx.StaticBox(self.page2, -1, "Availability of biomass from the region")
        self.frame_biomass_region.SetForegroundColour(TITLE_COLOR)
        self.frame_biomass_region.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        # set font for titles
        # 1. save actual font parameters on the stack
        fp.pushFont()
        # 2. change size and weight
        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
        self.frame_surfaceslist.SetFont(fp.getFont())
        self.frame_surfacedata.SetFont(fp.getFont())
        self.frame_weatherdata.SetFont(fp.getFont())
        self.frame_main_motivation.SetFont(fp.getFont())
        self.frame_biomass_processes.SetFont(fp.getFont())
        self.frame_biomass_region.SetFont(fp.getFont())
        # 3. recover previous font state
        fp.popFont()
        # set field sizes for the left tab.
        fs = FieldSizes(wHeight=HEIGHT_LEFT,wLabel=LABEL_WIDTH_LEFT,
                       wData=DATA_ENTRY_WIDTH,wUnits=UNITS_WIDTH)

        # set font for labels of left tab
        fp.pushFont()
        fp.changeFont(size=TYPE_SIZE_LEFT)

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
        self.tc1.SetFont(fp.getFont())


        # recover previous font state
        fp.popFont()

        # page 1 ------------------------------------------------------------------------------
        # set field sizes for the center tab.
        fs = FieldSizes(wHeight=HEIGHT_MIDDLE,wLabel=LABEL_WIDTH_MIDDLE,
                       wData=DATA_ENTRY_WIDTH,wUnits=UNITS_WIDTH)

        # set font for labels of center tab
        fp.pushFont()
        fp.changeFont(size=TYPE_SIZE_MIDDLE)
        
        # process list
        self.listBoxEnergy = wx.ListBox(self.page1,-1,choices=[])
        self.listBoxEnergy.SetFont(fp.getFont())
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxEnergy, self.listBoxEnergy)

        self.tc6_0 = TextEntry(self.page1,maxchars=255,value='',
                             label=_U("Short name of the available area"),
                             tip=_U("Define a short name for each surface area available for installation in order to clearly identify them"))

        self.tc6 = FloatEntry(self.page1,
                              decimals=0, minval=0., maxval=1e+9,
                              unitdict='AREA',label=_U("Available area"),\
                              tip=_U("If there are different surfaces available, give the measure of each surface area"))

        self.tc7 = FloatEntry(self.page1,
                              decimals=1, minval=0., maxval=90.,
                              unitdict='ANGLE',
                              label=_U("Inclination of the area"),
                              tip=_U("Positioning of the area (inclination in degrees)"))
                                  

        self.tc8 = ChoiceEntry(self.page1,
                              values=ORIENTATIONS.values(),
                              label=_U("Orientation of the roof, ground,\nwall area (to south)"),
			      tip=_U("Give the surface  inclination with respect to the  horizontal ( i.e. tilt angle, in degrees only)"))

        self.tc9 = ChoiceEntry(self.page1,
                             values=SHADINGTYPES.values(),
                             label=_U("Shading problems?"),
                             tip=_U("Consider shadows due to other buildings, trees, obstacles all over the year, in winter time or in early morning/late afternoon"))

        self.tc10 = FloatEntry(self.page1,
                               decimals=2, minval=0., maxval=1e+9,
                               unitdict='LENGTH',
                               label=_U("Distance between the roof, ground, wall area(s) and the technical room or process"),
			       tip=_U("Estimate the piping length (single way) from  the roof, ground,wall area to the technical room or to the process"))

        self.tc11 = ChoiceEntry(self.page1,
                              values=ROOFTYPES.values(),
                              label=_U("Type of roof"),
                              tip=_U("Specify the type of roof, e.g. composite sandwich panels, etc..."))

        # determinar dónde está esta unidad (kg/mü). en units no la encuentro.
        self.tc12 = FloatEntry(self.page1,
                               decimals=2, minval=0., maxval=99999.,
                               label=_U("Static load capacity of the roof"),
                               tip=_U("The additional weight of a solar collector field is about 25-30 kg/m2"))

        self.tc13 = ChoiceEntry(self.page1,
                                values=TRANSYESNO.values(),
                                label=_U("Is a plant/drawing of building(s)\nand surface(s) available?"),
                                tip=_U("Enclose the plant of the building(s) and/or a drawing of the surface(s)"))


        self.tc1_21 = FloatEntry(self.page1,
                        decimals=2, minval=-90.0, maxval=90.0,
                        unitdict='ANGLE',label=_U("Geographic latitude"),\
                        tip=_U("Insert the latitude in degree only. E.g.  Rome's latitude is 41,90 degrees"))
        self.tc1_22 = FloatEntry(self.page1,
                        decimals=1, minval=0., maxval=3000.,
                        unitdict='ENERGYFLOW',label=_U("Solar radiation on horizontal"),\
                        tip=_U("Annual total solar radiation on horizontal"))
        self.tc1_23 = FloatEntry(self.page1,
                                 decimals=1, minval=0., maxval=300.,
                                 unitdict='TEMPERATURE',label=_U("Yearly average ambient temperature"),
                                 tip=_U("Yearly average ambient temperature"))

        # recover previous font state
        fp.popFont()

        # page 2

        # set field sizes for the right tab.
        fs = FieldSizes(wHeight=HEIGHT_RIGHT,wLabel=LABEL_WIDTH_RIGHT,
                       wData=DATA_ENTRY_WIDTH,wUnits=UNITS_WIDTH)

        # set font for labels of right tab
        fp.pushFont()
        fp.changeFont(size=TYPE_SIZE_RIGHT)

        self.tc14 = TextEntry(self.page2,maxchars=255,value='',
                             label=_U("Type of biomass available from processes"),
                             tip=_U("Specify if the availability is continuous or during some specific season of the year"))

        self.tc15_1 = DateEntry(self.page2,
                              value='',
                              label=_U("Start of period of year the biomass is available"),
                              tip=_U("Specify if the availability is continuous or during some specific season of the year"))

        self.tc15_2 = DateEntry(self.page2,
                              value='',
                              label=_U("Stop of period of year the biomass is available"),
                              tip=_U("Specify if the availability is continuous or during some specific season of the year"))


        self.tc16 = FloatEntry(self.page2,
                              ipart=3, decimals=1, minval=0., maxval=365, value=0.,
                              unitdict=None,
                              label=_U("Number of days biomass is produced"),
                              tip=_U(" "))

        self.tc17 = FloatEntry(self.page2,
                              decimals=1, minval=0., maxval=1e+9, value=0.,
                              unitdict='MASS',
                              label=_U("Daily quantity of biomass"),
                              tip=_U(" "))


        self.tc18 = FloatEntry(self.page2,
                              decimals=1, minval=0., maxval=1e+9, value=0.,
                              unitdict='VOLUME',
                              label=_U("Space availability to stock biomass?"),
                              tip=_U("Specify the volume"))

        self.tc19 = FloatEntry(self.page2,
                              decimals=1, minval=0., maxval=1e+9, value=0.,
                              unitdict='ENERGY',
                              label=_U("LCV biomass"),
                              tip=_U(" "))

        self.tc20 = FloatEntry(self.page2,
                              decimals=1, minval=0., maxval=1e+9, value=0.,
                              unitdict=None,
                              label=_U("Humidity"),
                              tip=_U("Specify the percentage of humidity in biomass"))

        self.tc21 = TextEntry(self.page2,maxchars=255,value='',
                             label=_U("Type of biomass available"),
                             tip=_U(" "))

        self.tc22 = FloatEntry(self.page2,
                              decimals=1, minval=0., maxval=1e+9, value=0.,
                              unitdict='ENERGYTARIFF',
                              label=_U("Unit price of biomass"),
                              tip=_U(" "))

        self.tc23_1 = DateEntry(self.page2,
                              value='',
                              label=_U("Start of period of year the biomass is available"),
                              tip=_U("Specify if the availability is continuous or during some specific season of the year"))

        self.tc23_2 = DateEntry(self.page2,
                              value='',
                              label=_U("Stop of period of year the biomass is available"),
                              tip=_U("Specify if the availability is continuous or during some specific season of the year"))

        self.tc24 = FloatEntry(self.page2,
                              decimals=1, minval=0., maxval=365, value=0.,
                              unitdict=None,
                              label=_U("Number of days biomass is produced"),
                              tip=_U(" "))

        self.buttonAddEnergy = wx.Button(self.page1,-1,_U("Add surface"))
        self.buttonAddEnergy.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddEnergy, self.buttonAddEnergy)
        self.buttonAddEnergy.SetFont(fp.getFont())

        self.buttonDeleteEnergy = wx.Button(self.page1,-1,_U("Delete surface"))
        self.buttonDeleteEnergy.SetMinSize((125, 32))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteEnergy, self.buttonDeleteEnergy)
        self.buttonDeleteEnergy.SetFont(fp.getFont())

        self.buttonOK = wx.Button(self,wx.ID_OK,"OK")
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,"Cancel")
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        fp.popFont()



    def __do_layout(self):
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)
        #
        # tab 0 Main motivation
        #
        sizerPage0 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.StaticBoxSizer(self.frame_main_motivation, wx.VERTICAL)
        sizer_5.Add(self.checkBox1, 0, wx.ALL, 10)
        sizer_5.Add(self.checkBox2, 0, wx.ALL, 10)
        sizer_5.Add(self.checkBox3, 0, wx.ALL, 10)
        sizer_5.Add(self.checkBox4, 0, wx.ALL, 10)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add(self.checkBox5, 0, wx.ALL, 10)
        sizer_6.Add(self.tc1, 0, wx.ALL, 4)
        sizer_5.Add(sizer_6, 1, wx.EXPAND, 0)
        sizerPage0.Add(sizer_5, 1, wx.ALL|wx.EXPAND, 2)
        self.page0.SetSizer(sizerPage0)
        #
        # tab 1 Solar thermal energy
        #
        sizerPage1 = wx.BoxSizer(wx.HORIZONTAL)
        # tab 1 left part
        sizer_p1_left = wx.StaticBoxSizer(self.frame_surfaceslist, wx.VERTICAL)
        sizer_p1_left.Add(self.listBoxEnergy,  1, wx.EXPAND,0) 
        sizer_p1_left.Add(self.buttonAddEnergy, 0, wx.ALIGN_RIGHT, 0)
        sizer_p1_left.Add(self.buttonDeleteEnergy, 0, wx.ALIGN_RIGHT, 2)
        sizerPage1.Add(sizer_p1_left, 1, wx.TOP|wx.EXPAND, 10)
        # tab 1 right part
        sizer_p1_right = wx.BoxSizer(wx.VERTICAL)
        sizer_p1_top_right = wx.StaticBoxSizer(self.frame_surfacedata, wx.VERTICAL)
        sizer_p1_top_right.Add(self.tc6_0, 0, wx.ALL, 2)
        sizer_p1_top_right.Add(self.tc6, 0, wx.ALL, 2)
        sizer_p1_top_right.Add(self.tc7, 0, wx.ALL, 2)
        sizer_p1_top_right.Add(self.tc8, 0, wx.ALL, 2)        
        sizer_p1_top_right.Add(self.tc9, 0, wx.ALL, 2)        
        sizer_p1_top_right.Add(self.tc10, 0, wx.ALL, 2)
        sizer_p1_top_right.Add(self.tc11, 0, wx.ALL, 2)
        sizer_p1_top_right.Add(self.tc12, 0, wx.ALL, 2)
        sizer_p1_top_right.Add(self.tc13, 0, wx.ALL, 2)        
        sizer_p1_right.Add(sizer_p1_top_right, 8, wx.TOP|wx.EXPAND, 10)

        sizer_p1_bottom_right = wx.StaticBoxSizer(self.frame_weatherdata, wx.VERTICAL)
        sizer_p1_bottom_right.Add(self.tc1_21, 0, wx.ALL, 2)
        sizer_p1_bottom_right.Add(self.tc1_22, 0, wx.ALL, 2)
        sizer_p1_bottom_right.Add(self.tc1_23, 0, wx.ALL, 2)
        sizer_p1_right.Add(sizer_p1_bottom_right, 3, wx.TOP|wx.EXPAND, 10)

        sizerPage1.Add(sizer_p1_right, 2, wx.ALL|wx.EXPAND, 0)
        self.page1.SetSizer(sizerPage1)
        #
        # tab 2 Biomass
        #
        sizerPage2 = wx.BoxSizer(wx.VERTICAL)

        sizer_p2_top = wx.StaticBoxSizer(self.frame_biomass_processes, wx.VERTICAL)
        sizer_p2_top.Add(self.tc21, 0, 0, 0)
        sizer_p2_top.Add(self.tc22, 0, 0, 0)
        sizer_p2_top.Add(self.tc23_1, 0, 0, 0)
        sizer_p2_top.Add(self.tc23_2, 0, 0, 0)
        sizer_p2_top.Add(self.tc24, 0, 0, 0)
        sizerPage2.Add(sizer_p2_top, 5, wx.EXPAND|wx.TOP, 20)

        sizer_p2_bottom = wx.StaticBoxSizer(self.frame_biomass_region, wx.VERTICAL)
        sizer_p2_bottom.Add(self.tc14, 0, 0, 0)
        sizer_p2_bottom.Add(self.tc15_1, 0, 0, 0)
        sizer_p2_bottom.Add(self.tc15_2, 0, 0, 0)
        sizer_p2_bottom.Add(self.tc16, 0, 0, 0)
        sizer_p2_bottom.Add(self.tc17, 0, 0, 0)
        sizer_p2_bottom.Add(self.tc18, 0, 0, 0)
        sizer_p2_bottom.Add(self.tc19, 0, 0, 0)
        sizer_p2_bottom.Add(self.tc20, 0, 0, 0)
        sizerPage2.Add(sizer_p2_bottom, 8, wx.EXPAND|wx.TOP, 20)

        self.page2.SetSizer(sizerPage2)
        self.notebook.AddPage(self.page0, "Main motivation")
        self.notebook.AddPage(self.page1, "Solar thermal energy")
        self.notebook.AddPage(self.page2, "Biomass")
        sizerGlobal.Add(self.notebook, 1, wx.EXPAND, 0)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.ALIGN_RIGHT, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.ALIGN_RIGHT, 2)
        sizerGlobal.Add(sizerOKCancel, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizerGlobal)
        self.Layout()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------
    def OnListBoxEnergy(self,event):
#------------------------------------------------------------------------------
        self.selectedSurfaceName = self.listBoxEnergy.GetStringSelection()

        self.fillPageSurface()
            
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def OnButtonAddEnergy(self,event):
#------------------------------------------------------------------------------
        self.clear()
        event.Skip()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def OnButtonDeleteEnergy(self,event):
#------------------------------------------------------------------------------
        Status.prj.deleteSurface(self.selectedSurfaceID)
        Status.mod.moduleST.resetST()   #surface calculation no longer up to date
        self.display()
        event.Skip()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def OnButtonCancel(self, event):
        event.Skip()

#------------------------------------------------------------------------------
    def OnButtonOK(self, event):
#------------------------------------------------------------------------------

        logDebug("PanelQ7 (OK button): confirming data")
        
        if Status.PId != 0:
#..............................................................................
# general data on interest in renewables

            if self.notebook.GetSelection()==0:
                logTrack("PanelQ7 (OK button): writing general and biomass data")
                
                tmp = {
                    "Latitude":check(self.tc1_21.GetValue()),
                    "ST_I":check(self.tc1_22.GetValue()),
                    "TAmb":check(self.tc1_23.GetValue()),
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
#..............................................................................
# surface data

            elif self.notebook.GetSelection()==1:
                logTrack("PanelQ7 (OK button): writing surface specific data")
                
                self.selectedSurfaceName = self.tc6_0.GetValue()

# assure that a name has been entered before continuing
                if len(self.selectedSurfaceName) == 0 or self.selectedSurfaceName is None:
                    showWarning(_("You have to enter a name for the new surface before saving"))
                    return

                surfaces = Status.DB.qsurfarea.ProjectID[Status.PId].\
                            SurfAreaName[check(self.selectedSurfaceName)]

                if len(surfaces) == 0:
                    surface = Status.prj.addSurfaceDummy()
                elif len(surfaces) == 1:
                    surface = surfaces[0]
                else:
                    showWarning("PanelQ7 (ButtonOK): surface name has to be a uniqe value!")
                    return

                orientation = findKey(ORIENTATIONS,self.tc8.GetValue(text=True))
                if orientation in AZIMUTH.keys():
                    azimuth = AZIMUTH[orientation]
                else:
                    azimuth = None
                    
                tmp = {
                    "SurfAreaName":check(self.tc6_0.GetValue()),
                    "SurfArea":check(self.tc6.GetValue()),
                    "Inclination":check(self.tc7.GetValue()),
                    "Azimuth":check(azimuth),
                    "AzimuthClass":check(orientation),
                    "Shading":check(findKey(SHADINGTYPES,self.tc9.GetValue(text=True))),
                    "Distance":check(self.tc10.GetValue()),
                    "RoofType":check(findKey(ROOFTYPES,self.tc11.GetValue(text=True))),
                    "RoofStaticLoadCap":check(self.tc12.GetValue())
    #                "EnclBuildGroundSketch":check(findKey(TRANSYESNO,self.tc13.GetValue(text=True))),
                   }

                surface.update(tmp)
                Status.SQL.commit()

                Status.mod.moduleST.resetST()   #surface calculation no longer up to date


#..............................................................................
# biomass data

            else:
                logTrack("PanelQ7 (OK button): writing general and biomass data")
                
                tmp = {
                    "BiomassFromProc":check(self.tc14.GetValue()),
                    "PeriodBiomassProcStart":check(self.tc15_1.GetValue()),
                    "PeriodBiomassProcStop":check(self.tc15_2.GetValue()),
                    "NDaysBiomassProc":check(self.tc16.GetValue()),
                    "QBiomassProcDay":check(self.tc17.GetValue()),
                    "SpaceBiomassProc":check(self.tc18.GetValue()),
                    "LCVBiomassProc":check(self.tc19.GetValue()),
                    "HumidBiomassProc":check(self.tc20.GetValue()),
                    "BiomassFromRegion":check(self.tc21.GetValue()),
                    "PriceBiomassRegion":check(self.tc22.GetValue()),
                    "PeriodBiomassRegionStart":check(self.tc23_1.GetValue()),
                    "PeriodBiomassRegionStop":check(self.tc23_2.GetValue()),
                    "NDaysBiomassRegion":check(self.tc24.GetValue())
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
            logDebug("PanelQ7 (OK button): now filling page again")

            self.fillPage()

            logDebug("PanelQ7 (OK button): and back")
        event.Skip()

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def display(self):
#------------------------------------------------------------------------------
        self.clear()
        self.fillPage()
        self.Show()


#------------------------------------------------------------------------------
    def clear(self):
#------------------------------------------------------------------------------

        self.tc1_21.Clear()
        self.tc1_22.Clear()
        self.tc1_23.Clear()
        
#        self.checkBox1.SetValue(False)
#        self.checkBox2.SetValue(False)
#        self.checkBox3.SetValue(False)
#        self.checkBox4.SetValue(False)
#        self.checkBox5.SetValue(False)
        self.tc6_0.Clear()
        self.tc6.Clear()
        self.tc7.Clear()

        self.tc10.Clear()

        self.tc12.Clear()


#        self.tc1_21.Clear()
#        self.tc1_22.Clear()
#        self.tc1_23.Clear()

#        self.tc14.Clear()
#        self.tc16.Clear()
#        self.tc17.Clear()
#        self.tc18.Clear()
#        self.tc19.Clear()
#        self.tc20.Clear()
#        self.tc21.Clear()
#        self.tc22.Clear()
#        self.tc24.Clear()



#------------------------------------------------------------------------------
    def fillPage(self):
#------------------------------------------------------------------------------
	if Status.PId == 0:
	    return

	if len(Status.DB.qrenewables.Questionnaire_id[Status.PId]) > 0:
	    p = Status.DB.qrenewables.Questionnaire_id[Status.PId][0]
	    if p.REInterest is None:
		self.checkBox1.SetValue(False)
	    else:
		self.checkBox1.SetValue(bool(p.REInterest))

            self.tc1_21.SetValue(str(p.Latitude))
	    self.tc1_22.SetValue(str(p.ST_I))
	    self.tc1_23.SetValue(str(p.TAmb))
	    
	    self.tc14.SetValue(p.BiomassFromProc)
	    self.tc15_1.SetValue(p.PeriodBiomassProcStart)
	    self.tc15_2.SetValue(p.PeriodBiomassProcStop)
	    self.tc16.SetValue(str(p.NDaysBiomassProc))
	    self.tc17.SetValue(str(p.QBiomassProcDay))
	    self.tc18.SetValue(str(p.SpaceBiomassProc))
	    self.tc19.SetValue(str(p.LCVBiomassProc))
	    self.tc20.SetValue(str(p.HumidBiomassProc))
	    self.tc21.SetValue(p.BiomassFromRegion)
	    self.tc22.SetValue(str(p.PriceBiomassRegion))
	    self.tc23_1.SetValue(p.PeriodBiomassRegionStart)
	    self.tc23_2.SetValue(p.PeriodBiomassRegionStop)
	    self.tc24.SetValue(str(p.NDaysBiomassRegion))

        surfaceList = Status.prj.getSurfaceList("SurfAreaName")
        
        self.listBoxEnergy.Clear()
        for surface in surfaceList:
            self.listBoxEnergy.Append(surface)

        if len(surfaceList) > 0:
            if self.selectedSurfaceName == None:
                self.selectedSurfaceName = surfaceList[0]
            self.listBoxEnergy.SetStringSelection(self.selectedSurfaceName)
            self.fillPageSurface()

#------------------------------------------------------------------------------
    def fillPageSurface(self):
#------------------------------------------------------------------------------

        surfaces = Status.DB.qsurfarea.ProjectID[Status.PId].\
                    SurfAreaName[check(self.selectedSurfaceName)]
        
        if len(surfaces) > 0:
            self.selectedSurfaceID = surfaces[0].id

	    p = surfaces[0]

	    self.tc6_0.SetValue(p.SurfAreaName)
	    self.tc6.SetValue(str(p.SurfArea))
	    self.tc7.SetValue(str(p.Inclination))
	    if p.AzimuthClass in ORIENTATIONS.keys():
                self.tc8.SetValue(ORIENTATIONS[str(p.AzimuthClass)])
                
	    if p.Shading in SHADINGTYPES.keys():
                self.tc9.SetValue(SHADINGTYPES[str(p.Shading)])
                
	    self.tc10.SetValue(str(p.Distance))
	    
	    if p.RoofType in ROOFTYPES.keys():
                self.tc11.SetValue(ROOFTYPES[str(p.RoofType)])
                
	    self.tc12.SetValue(str(p.RoofStaticLoadCap))

	    if p.Sketch in TRANSYESNO.keys():
                self.tc13.SetValue(TRANSYESNO[str(p.Sketch)])

        else:
            self.selectedSurfaceID = None
	    
#==============================================================================

