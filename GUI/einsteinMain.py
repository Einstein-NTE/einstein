#!/usr/bin/env python
# -*- coding: cp1252 -*-

#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	EINSTEIN Main 
#			
#------------------------------------------------------------------------------
#			
#	GUI Main routines
#
#==============================================================================
#
#	Version No.: 0.60
#	Created by: 	    Heiko Henning (Imsai e-soft)	February 2008
#	Revisions:          Tom Sobota                          12/03/2008
#                           Hans Schweiger                      22/03/2008
#                           Tom Sobota                          23/03/2008
#                           Hans Schweiger                      24/03/2008
#
#       Change list:
#       12/03/2008- panel Energy added
#       13/03/2008  Changed global refs. to DB, SQL ... to references in Status
#                   Changed global refs to database params to locals
#                   Deleted all references to DataBridge
#       22/03/2008  Small changes due to changes in interface
#       23/03/2008  Added panels EA1 - EA6, EM1. Added a subtree for Yearly, Monthly and Daily
#                   statistics
#       24/03/2008  Small changes in calls to PanelBB
#	
#------------------------------------------------------------------------------		
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	www.energyxperts.net / info@energyxperts.net
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================

#-----  Imports
import wx
import wx.grid
import pSQL, MySQLdb
import exceptions
import HelperClass
import BridgeClass

#--- popup frames
from status import Status #processing status of the tool

#--- popup frames
import DBEditFrame
import PreferencesFrame

#--- Module Frames
#HS2008-03-12 panelEnergy added
from panelCCheck import *
from panelHP import *
from panelBB import *
from panelEnergy import *
#TS2008-03-23 panelEA1-EA6, EM1 added
from panelEA1 import *
from panelEA2 import *
from panelEA3 import *
from panelEA4 import *
from panelEA5 import *
from panelEA6 import *
from panelEM1 import *


#-----  Global variables 
PList = {}      # PList stores the Parameterlist

#----- Constants
qPageSize = (800, 600) # this would be better in Status?




#------------------------------------------------------------------------------		
class EinsteinFrame(wx.Frame):
#------------------------------------------------------------------------------		
#   Main frame definition
#------------------------------------------------------------------------------		
    
    def __init__(self, parent, id, title):
        ############################################
        #
        # Database connexion
        #
        ############################################

        doLog = HelperClass.LogHelper()
        conf = HelperClass.ConfigHelper()
        doLog.LogThis('Starting program')

        global activeQid
        self.activeQid = 0
        DBHost = conf.get('DB', 'DBHost')
        DBUser = conf.get('DB', 'DBUser')
        DBPass = conf.get('DB', 'DBPass')
        DBName = conf.get('DB', 'DBName')
        LANGUAGE = conf.get('GUI', 'LANGUAGE')
        doLog.LogThis('Reading config done')
        
        #----- Connect to the Database
        Status.SQL = MySQLdb.connect(host=DBHost, user=DBUser, passwd=DBPass, db=DBName)
        Status.DB =  pSQL.pSQL(Status.SQL, DBName)
        print "database assigned to status variable " + repr(Status.DB)
        
        doLog.LogThis('Connected to database %s @ %s' % (DBName, DBHost))

        #----- Import the Parameterfile
        global PList
        ParamList = HelperClass.ParameterDataHelper()
        PList = ParamList.ReadParameterData()
        doLog.LogThis('Import Parameterfile done')


        ############################################
        #
        # UI generation
        #
        ############################################

        #----- Initialise the Frame
        wx.Frame.__init__(self, parent, id, title, size=(1024, 740), pos=(0,0))
        #----- add statusbar
        self.CreateStatusBar()



        #----- add menu
        self.menuBar = wx.MenuBar()
        
        self.menuFile = wx.Menu()
        self.menuView = wx.Menu()
        self.menuDatabase = wx.Menu()
        self.menuSettings = wx.Menu()        
        self.menuHelp = wx.Menu()

        self.submenuPrint = wx.Menu()
        self.submenuEditDB = wx.Menu()
                
        self.subnenuEquipments = wx.Menu()
        self.submenuUserLevel = wx.Menu()
        self.submenuClassification = wx.Menu()
        

        self.PrintFullReport = self.submenuPrint.Append(-1, "full report")
        self.PrintQuestionnaire = self.submenuPrint.Append(-1, "questionnaire")

        self.NewProject = self.menuFile.Append(-1, PList["X103"][1])
        self.OpenProject = self.menuFile.Append(-1, "&Open Project")
        self.ImportProject = self.menuFile.Append(-1, PList["X104"][1])
        self.ExportProject = self.menuFile.Append(-1, PList["X105"][1])
        self.menuFile.AppendSeparator()
        self.ImportQ = self.menuFile.Append(-1, PList["X106"][1])
        self.menuFile.AppendSeparator()
        self.Print = self.menuFile.AppendMenu(-1, "&Print", self.submenuPrint)
        self.menuFile.AppendSeparator()
        self.ExitApp = self.menuFile.Append(-1, PList["X107"][1])

        self.PresentState = self.menuView.AppendRadioItem(-1, "Present state")
        self.Aternative1 = self.menuView.AppendRadioItem(-1, "Alternative 1")
        

        self.EditDBCHP = self.subnenuEquipments.Append(-1, PList["X111"][1])
        self.EditDBHeatPump = self.subnenuEquipments.Append(-1, PList["X112"][1])
        self.EditDBChiller = self.subnenuEquipments.Append(-1, PList["X117"][1])
        self.EditDBBoiler = self.subnenuEquipments.Append(-1, PList["X115"][1])
        self.EditDBStorage = self.subnenuEquipments.Append(-1, PList["X116"][1])
        self.EditDBSolarEquip = self.subnenuEquipments.Append(-1, PList["X116"][1])

        self.EditSubDB = self.menuDatabase.AppendMenu(-1, "Equipments", self.subnenuEquipments)
        self.EditDBFuel = self.menuDatabase.Append(-1, PList["X114"][1])
        self.EditDBFluid = self.menuDatabase.Append(-1, PList["X113"][1])
        self.EditDBBenchmark = self.menuDatabase.Append(-1, PList["X108"][1])
        self.EditDBBAT = self.menuDatabase.Append(-1, "Best available technologies")
        
        self.EditDBNaceCode = self.submenuClassification.Append(-1, PList["X109"][1])
        self.EditDBUnitOperation = self.submenuClassification.Append(-1, PList["X110"][1])       
               

        self.UserSelectLevel1 = self.submenuUserLevel.AppendRadioItem(-1, PList["X120"][1])
        self.UserSelectLevel2 = self.submenuUserLevel.AppendRadioItem(-1, PList["X121"][1])
        self.UserSelectLevel3 = self.submenuUserLevel.AppendRadioItem(-1, PList["X122"][1])
        self.UserLevel = self.menuSettings.AppendMenu(-1, PList["X123"][1], self.submenuUserLevel)
        self.Classification = self.menuSettings.AppendMenu(-1, "Classification", self.submenuClassification)
        self.Preferences = self.menuSettings.Append(-1, PList["X119"][1])
        self.Language = self.menuSettings.Append(-1, "Language")

        self.HelpHelp = self.menuHelp.Append(-1, PList["X126"][1])
        self.menuHelp.AppendSeparator()
        self.HelpAbout = self.menuHelp.Append(-1, PList["X127"][1])

        self.menuBar.Append(self.menuFile, PList["X128"][1])
        self.menuBar.Append(self.menuView, "View")
        self.menuBar.Append(self.menuDatabase, "Database")
        self.menuBar.Append(self.menuSettings, PList["X130"][1])
        self.menuBar.Append(self.menuHelp, PList["X132"][1])
        
        self.SetMenuBar(self.menuBar)

        
        #----- add the widgets ...
        self.panel1=wx.Panel (self, -1)
        self.panel1.SetBackgroundColour ("white")

        #----- create splitter windows
        self.splitter = wx.SplitterWindow(self, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)
        self.splitter2 = wx.SplitterWindow(self.splitter, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)
        self.mainpanel = wx.Panel(self.splitter, -1)
        self.leftpanel2 = wx.Panel(self.splitter2, -1, style=wx.WANTS_CHARS) # this ist main gui panel containing qPages
        self.mainpanel.SetBackgroundColour ("white")
        self.splitter2.SetBackgroundColour (wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE))

        #----- create tree control
        self.tree = wx.TreeCtrl(self.mainpanel, -1, wx.Point(0, 0), wx.Size(200, 740),
                                wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        self.qRoot = self.tree.AddRoot(PList["X001"][1])
        self.qPage0 = self.tree.AppendItem (self.qRoot, PList["X018"][1],0)
        self.qPage1 = self.tree.AppendItem (self.qPage0, PList["X010"][1],0)
        self.qPage2 = self.tree.AppendItem (self.qPage0, PList["X011"][1],0)
        self.qPage3 = self.tree.AppendItem (self.qPage0, PList["X012"][1],0)
        self.qPage4 = self.tree.AppendItem (self.qPage0, PList["X013"][1],0)
        self.qPage5 = self.tree.AppendItem (self.qPage0, PList["X014"][1],0)
        self.qPage5_1 = self.tree.AppendItem (self.qPage0, "Heat recovery",0)
        self.qPage6 = self.tree.AppendItem (self.qPage0, PList["X015"][1],0)
        self.qPage7 = self.tree.AppendItem (self.qPage0, PList["X016"][1],0)
        self.qPage8 = self.tree.AppendItem (self.qPage0, PList["X017"][1],0)
        
        self.qDataCheck = self.tree.AppendItem (self.qRoot, PList["X133"][1])
        self.qDataCheckPage1 = self.tree.AppendItem (self.qDataCheck, PList["X134"][1])
        self.qDataCheckPage2 = self.tree.AppendItem (self.qDataCheck, PList["X135"][1])
        self.qDataCheckPage3 = self.tree.AppendItem (self.qDataCheck, "Check list for visit")
        
        #
        # statistics subtree
        #
        self.qStatistics = self.tree.AppendItem (self.qRoot, PList["X136"][1])
        self.qStatisticsAnnual = self.tree.AppendItem (self.qStatistics, 'Annual data')
        self.qStatisticsMonthly = self.tree.AppendItem (self.qStatistics, 'Monthly data')
        self.qStatisticsHourly = self.tree.AppendItem (self.qStatistics, 'Hourly performance data')
        # annual statistics subtree
        self.qStatisticYPage1 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X137"][1])
        self.qStatisticYPage2 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X138"][1])
        self.qStatisticYPage3 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X139"][1])
        self.qStatisticYPage4 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X140"][1])
        self.qStatisticYPage5 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X141"][1])
        self.qStatisticYPage6 = self.tree.AppendItem (self.qStatisticsAnnual, PList["X142"][1])
        # monthly statistics subtree
        self.qStatisticMPage1 = self.tree.AppendItem (self.qStatisticsMonthly, 'Monthly demand')
        self.qStatisticMPage2 = self.tree.AppendItem (self.qStatisticsMonthly, 'Monthly supply')
        # hourly statistics subtree
        self.qStatisticHPage1 = self.tree.AppendItem (self.qStatisticsHourly, 'Hourly demand')
        self.qStatisticHPage2 = self.tree.AppendItem (self.qStatisticsHourly, 'Hourly supply')

        
        self.qBenchmarkCheck = self.tree.AppendItem (self.qRoot, PList["X143"][1])
        self.qBenchmarkCheckPage1 = self.tree.AppendItem (self.qBenchmarkCheck, PList["X144"][1])
        self.qBenchmarkCheckPage2 = self.tree.AppendItem (self.qBenchmarkCheck, "Global energy intensity")
        self.qBenchmarkCheckPage3 = self.tree.AppendItem (self.qBenchmarkCheck, "SEC by product")
        self.qBenchmarkCheckProduct = self.tree.AppendItem (self.qBenchmarkCheckPage3, "product name")
        self.qBenchmarkCheckPage4 = self.tree.AppendItem (self.qBenchmarkCheck, "SEC by process")
        self.qBenchmarkCheckProcess = self.tree.AppendItem (self.qBenchmarkCheckPage4, "process name")
        

        self.qOptimisationProposals = self.tree.AppendItem (self.qRoot, PList["X145"][1])
        #Design
        self.qOptiProDesign = self.tree.AppendItem (self.qOptimisationProposals, PList["X146"][1])
        
        #Process optimisation
        self.qOptiProProcess = self.tree.AppendItem (self.qOptiProDesign, "Process optimisation")
        #Process optimisation interface 1
        self.qOptiProProcess1 = self.tree.AppendItem(self.qOptiProProcess, "Process optimisation interface 1")
                #Process optimisation interface 2
        self.qOptiProProcess2 = self.tree.AppendItem(self.qOptiProProcess, "Process optimisation interface 2")
            #Pinch analysis
        self.qOptiProPinch = self.tree.AppendItem(self.qOptiProDesign, "Pinch analysis")
                #Pinch interface 1
        self.qOptiProPinch1 = self.tree.AppendItem(self.qOptiProPinch, "Pinch interface 1")
                #Pinch interface 2
        self.qOptiProPinch2 = self.tree.AppendItem(self.qOptiProPinch, "Pinch interface 2")
            #HX network
        self.qOptiProHX = self.tree.AppendItem (self.qOptiProDesign, "HX network")

            #H&C Supply
        self.qOptiProSupply = self.tree.AppendItem (self.qOptiProDesign, "H&C Supply")
                #H&C Storage
        self.qOptiProSupply1 = self.tree.AppendItem (self.qOptiProSupply, "H&C Storage")
                #CHP
        self.qOptiProSupply2 = self.tree.AppendItem (self.qOptiProSupply, "CHP")
                #Solar Thermal
        self.qOptiProSupply3 = self.tree.AppendItem (self.qOptiProSupply, "Solar Thermal")
                #Heat Pumps
        self.qOptiProSupply4 = self.tree.AppendItem (self.qOptiProSupply, "Heat Pumps")
                #Biomass
        self.qOptiProSupply5 = self.tree.AppendItem (self.qOptiProSupply, "Biomass")
                #Chillers
        self.qOptiProSupply6 = self.tree.AppendItem (self.qOptiProSupply, "Chillers")
                #Boilers & burners
        self.qOptiProSupply7 = self.tree.AppendItem (self.qOptiProSupply, "Boilers & burners")
        
            #H&C Distribution
        self.qOptiProDistribution = self.tree.AppendItem (self.qOptiProDesign, "H&C Distribution")

        #Energy performance
        self.qOptiProEnergy = self.tree.AppendItem (self.qOptimisationProposals, "Energy performance")
            #Detailed energy flows 1
#HS2008-03-12: subdivision energy cancelled out
#        self.qOptiProEnergy1 = self.tree.AppendItem (self.qOptiProEnergy, "Detailed energy flows 1")
            #Detailed energy flows 2
#        self.qOptiProEnergy2 = self.tree.AppendItem (self.qOptiProEnergy, "Detailed energy flows 2")

        #Economic analysis
        self.qOptiProEconomic = self.tree.AppendItem (self.qOptimisationProposals, "Economic analysis")
            #Economics 1
        self.qOptiProEconomic1 = self.tree.AppendItem (self.qOptiProEconomic, "Economics 1")
            #Economics 2
        self.qOptiProEconomic2 = self.tree.AppendItem (self.qOptiProEconomic, "Economics 2")


        #Comparative analysis
        self.qOptiProComparative = self.tree.AppendItem (self.qOptimisationProposals, "Comparative analysis")
            #Comparative study – Detail Info 1
        self.qOptiProComparative1 = self.tree.AppendItem (self.qOptiProComparative, "Comparative study – Detail Info 1")
            #Comparative study – Detail Info 2
        self.qOptiProComparative2 = self.tree.AppendItem (self.qOptiProComparative, "Comparative study – Detail Info 2")
            #Comparative study – Detail Info 3
        self.qOptiProComparative3 = self.tree.AppendItem (self.qOptiProComparative, "Comparative study – Detail Info 3")


        self.qFinalReport = self.tree.AppendItem (self.qRoot, PList["X147"][1])
        self.qFinalReportPage1 = self.tree.AppendItem (self.qFinalReport, PList["X148"][1])
        self.qFinalReportPage2 = self.tree.AppendItem (self.qFinalReport, PList["X149"][1])
        self.qFinalReportPrint = self.tree.AppendItem (self.qFinalReport, PList["X150"][1])
        
        self.tree.Expand(self.qRoot)
        self.tree.Expand(self.qPage0)
        self.tree.Expand(self.qDataCheck)
        self.tree.Expand(self.qStatistics)
        self.tree.Expand(self.qBenchmarkCheck)
        self.tree.Expand(self.qOptimisationProposals)
        self.tree.Expand(self.qFinalReport)


        self.DoLayout ()

        
        
        #----- binding the EVENTS

        
        #--- binding the menu
        self.Bind(wx.EVT_MENU, self.OnButtonNewQuestionnairePage0, self.NewProject)
        self.Bind(wx.EVT_MENU, self.OnMenuOpenProject, self.OpenProject)
        self.Bind(wx.EVT_MENU, self.OnMenuExit, self.ExitApp)

        self.Bind(wx.EVT_MENU, self.OnMenuEditDBBenchmark, self.EditDBBenchmark)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBNaceCode, self.EditDBNaceCode)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBUnitOperation, self.EditDBUnitOperation)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBCHP, self.EditDBCHP)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBHeatPump, self.EditDBHeatPump)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBFluid, self.EditDBFluid)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBFuel, self.EditDBFuel)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBBoiler, self.EditDBBoiler)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBSolarEquip, self.EditDBSolarEquip)
        self.Bind(wx.EVT_MENU, self.OnMenuEditDBChiller, self.EditDBChiller)     
        



        #--- binding the Tree
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelChanged, self.tree)

        #--- bindings Page 0
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListBoxQuestionnaresPage0ListboxDclick, self.listBoxQuestionnaresPage0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonOpenQuestionnairePage0, self.buttonOpenQuestionnairePage0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteQuestionnairePage0, self.buttonDeleteQuestionnairePage0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonNewQuestionnairePage0, self.buttonNewQuestionnairePage0)

        #--- bindings Page 1 
        self.Bind(wx.EVT_BUTTON, self.OnButtonStoreDataPage1, self.buttonStoreDataPage1)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxProductsPage1ListboxClick, self.listBoxProductsPage1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddProductPage1, self.buttonAddProductPage1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteProductPage1, self.buttonDeleteProductPage1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClearPage1, self.buttonClearPage1)

        #--- bindings Page 2  
        self.Bind(wx.EVT_LISTBOX, self.OnFuelListBoxListboxClickPage2, self.fuelListBoxPage2)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddFuelPage2, self.buttonAddFuelPage2)
        self.Bind(wx.EVT_BUTTON, self.OnButtonRemoveFuelFromListPage2, self.buttonRemoveFuelFromListPage2)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClearPage2, self.buttonClearPage2)
        self.Bind(wx.EVT_BUTTON, self.OnButtonStorePage2, self.buttonStorePage2)

        #--- bindings Page 3
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddProcessPage3, self.buttonAddProcessPage3)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxProcessesPage3ListboxClick, self.listBoxProcessesPage3)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteProcessPage3, self.buttonDeleteProcessPage3)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClearPage3, self.buttonClearPage3)

        #--- bindings Page 4
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxEquipmentListPage4ListboxClick, self.listBoxEquipmentListPage4)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteEquipmentPage4Button, self.buttonDeleteEquipmentPage4)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddEquipmentPage4Button, self.buttonAddEquipmentPage4)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClearPage4Button, self.buttonClearPage4)

        #--- bindings Page 5
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxDistributionListPage5ListboxClick, self.listBoxDistributionListPage5)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClearPage5, self.buttonClearPage5)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteDistributionPage5, self.buttonDeleteDistributionPage5)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddDistributionPage5, self.buttonAddDistributionPage5)

        #--- bindings Page 6
        self.Bind(wx.EVT_BUTTON, self.OnButtonStoreDataPage6, self.buttonStoreDataPage6)

        #--- bindings Page 7
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxBuildingListPage7ListboxClick, self.listBoxBuildingListPage7)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClearPage7, self.buttonClearPage7)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteBuildingPage7, self.buttonDeleteBuildingPage7)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddBuildingPage7, self.buttonAddBuildingPage7)

        #--- bindings Page 8
        self.Bind(wx.EVT_BUTTON, self.OnButtonStoreDataPage8, self.buttonStoreDataPage8)

        #--- bindings pageDataCheck
###HS2008-03-07        self.Bind(wx.EVT_BUTTON, self.OnButtonDataCheck, self.buttonDataCheck)        

#------------------------------------------------------------------------------		
    def DoLayout (self):
#------------------------------------------------------------------------------		
#       Layout of main frame and panels 
#------------------------------------------------------------------------------		
        
        # add other widgets
        self.help = wx.TextCtrl(self.splitter2, -1, style = wx.TE_MULTILINE|wx.TE_READONLY | wx.HSCROLL)
        
        # sizers
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        panelsizer = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
      
        # add widgets to sizers
        panelsizer.Add(self.splitter, 1, wx.EXPAND, 0)
        sizer1.Add(self.tree, 1, wx.EXPAND)
        #sizer2.Add(self.staticBoxPage0, 1, wx.BOTTOM|wx.EXPAND|wx.ALIGN_BOTTOM, 60 )
    
        # set sizers
        self.mainpanel.SetSizer(sizer1)
        self.leftpanel2.SetSizer(sizer2)
        self.SetSizer(panelsizer)
        mainsizer.Layout()
        self.Layout()

        # set splitters
        self.splitter.SplitVertically(self.mainpanel, self.splitter2, 200)
        self.splitter2.SplitHorizontally(self.leftpanel2, self.help, -80)
        self.splitter.SetSashPosition (200)

######################################################################################        

        #----- set Panel Pages

        ####----PAGE Title
        self.pageTitle = wx.Panel(id=-1, name='pageTitle', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageTitle.Show()
        self.st1Titel = wx.StaticText(id=-1,
              label='Welcome to EINSTEIN Energie audit Programm',
              name='st1Titel', parent=self.pageTitle, pos=wx.Point(295, 293),
              size=wx.Size(222, 13), style=0)
        self.st1Titel.Center(wx.BOTH)
        self.st1Titel.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        
        ####--- End of PAGE 0

        
     
        ####----PAGE 0

        self.Page0 = wx.Panel(id=-1, name='Page0',
              parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
        self.Page0.Hide()

        self.listBoxQuestionnaresPage0 = wx.ListBox(choices=[],
              id=-1,
              name='listBoxQuestionnaresPage0', parent=self.Page0,
              pos=wx.Point(32, 64), size=wx.Size(131, 312), style=0)

        self.buttonNewQuestionnairePage0 = wx.Button(id=-1,
              label='new questionnaire', name='buttonNewQuestionnairePage0',
              parent=self.Page0, pos=wx.Point(224, 72), size=wx.Size(120, 23),
              style=0)

        self.buttonOpenQuestionnairePage0 = wx.Button(id=-1,
              label='open questionnaire', name='buttonOpenQuestionnairePage0',
              parent=self.Page0, pos=wx.Point(224, 112), size=wx.Size(120, 23),
              style=0)        

        self.buttonDeleteQuestionnairePage0 = wx.Button(id=-1,
              label='delete questionnaire',
              name='buttonDeleteQuestionnairePage0', parent=self.Page0,
              pos=wx.Point(224, 152), size=wx.Size(120, 23), style=0)        

        self.stInfo1Page0 = wx.StaticText(id=-1, label='Questionnaire list', name='stInfo1Page0', parent=self.Page0, pos=wx.Point(32, 48), style=0)
        self.stInfo1Page0.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        ####--- End of PAGE 0


        ####----PAGE 1

        self.Page1 = wx.Panel(id=-1, name='Page1', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

        self.Page1.Hide()

        self.stInfo3Page1 = wx.StaticText(id=-1, label=PList["X020"][1], name='stInfo3Page1', parent=self.Page1, pos=wx.Point(248, 384), style=0)
        self.stInfo3Page1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo1Page1 = wx.StaticText(id=-1, label=PList["X021"][1], name='stInfo1Page1', parent=self.Page1, pos=wx.Point(16, 24), style=0)
        self.stInfo1Page1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo2Page1 = wx.StaticText(id=-1, label=PList["X022"][1], name='stInfo2Page1', parent=self.Page1, pos=wx.Point(248, 24), style=0)
        self.stInfo2Page1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        

        self.st1Page1 = wx.StaticText(id=-1, label=PList["0101"][1], name='st1Page1', parent=self.Page1, pos=wx.Point(16, 48), style=0)

        self.tc1Page1 = wx.TextCtrl(id=-1,
              name='tc1Page1', parent=self.Page1, pos=wx.Point(16, 64),
              size=wx.Size(200, 21), style=0, value='')

        self.st2Page1 = wx.StaticText(id=-1, label=PList["0102"][1], name='st2Page1', parent=self.Page1, pos=wx.Point(16, 88), style=0)

        self.tc2Page1 = wx.TextCtrl(id=-1,
              name='tc2Page1', parent=self.Page1, pos=wx.Point(16, 104),
              size=wx.Size(200, 21), style=0, value='')

        self.st3Page1 = wx.StaticText(id=-1, label=PList["0108"][1], name='st3Page1', parent=self.Page1, pos=wx.Point(16, 128), style=0)

        self.tc3Page1 = wx.TextCtrl(id=-1,
              name='tc3Page1', parent=self.Page1, pos=wx.Point(16, 144),
              size=wx.Size(200, 21), style=0, value='')

        self.st4Page1 = wx.StaticText(id=-1, label=PList["0109"][1], name='st4Page1', parent=self.Page1, pos=wx.Point(16, 168), style=0)

        self.tc4Page1 = wx.TextCtrl(id=-1,
              name='tc4Page1', parent=self.Page1, pos=wx.Point(16, 184),
              size=wx.Size(200, 21), style=0, value='')

        self.st5Page1 = wx.StaticText(id=-1, label=PList["0110"][1], name='st5Page1', parent=self.Page1, pos=wx.Point(16, 208), style=0)

        self.tc5Page1 = wx.TextCtrl(id=-1,
              name='tc5Page1', parent=self.Page1, pos=wx.Point(16, 224),
              size=wx.Size(200, 56), style=wx.TE_MULTILINE, value='')

        self.st6Page1 = wx.StaticText(id=-1, label=PList["0111"][1], name='st6Page1', parent=self.Page1, pos=wx.Point(16, 286), style=0)

        self.tc6Page1 = wx.TextCtrl(id=-1,
              name='tc6Page1', parent=self.Page1, pos=wx.Point(16, 304),
              size=wx.Size(200, 21), style=0, value='')

        self.st7Page1 = wx.StaticText(id=-1, label=PList["0112"][1], name='st7Page1', parent=self.Page1, pos=wx.Point(16, 328), style=0)

        self.tc7Page1 = wx.TextCtrl(id=-1,
              name='tc7Page1', parent=self.Page1, pos=wx.Point(16, 344),
              size=wx.Size(200, 21), style=0, value='')

        self.st8Page1 = wx.StaticText(id=-1, label=PList["0113"][1], name='st8Page1', parent=self.Page1, pos=wx.Point(16, 368), style=0)

        self.tc8Page1 = wx.TextCtrl(id=-1,
              name='tc8Page1', parent=self.Page1, pos=wx.Point(16, 384),
              size=wx.Size(200, 21), style=0, value='')

        self.st9Page1 = wx.StaticText(id=-1, label=PList["0103"][1], name='st9Page1', parent=self.Page1, pos=wx.Point(16, 408), style=0)

        self.tc9Page1 = wx.TextCtrl(id=-1,
              name='tc9Page1', parent=self.Page1, pos=wx.Point(16, 424),
              size=wx.Size(200, 56), style=wx.TE_MULTILINE, value='')

        self.st10Page1 = wx.StaticText(id=-1, label=PList["0104"][1], name='st10Page1', parent=self.Page1, pos=wx.Point(16, 488), style=0)

        self.tc10Page1 = wx.TextCtrl(id=-1,
              name='tc10Page1', parent=self.Page1, pos=wx.Point(16, 504),
              size=wx.Size(200, 21), style=0, value='')

        self.st11Page1 = wx.StaticText(id=-1, label=PList["0106"][1], name='st11Page1', parent=self.Page1, pos=wx.Point(16, 528), style=0)

        self.st14Page1 = wx.StaticText(id=-1, label=PList["0201"][1], name='st14Page1', parent=self.Page1, pos=wx.Point(248, 48), style=0)

        self.tc14Page1 = wx.TextCtrl(id=-1,
              name='tc14Page1', parent=self.Page1, pos=wx.Point(248, 64),
              size=wx.Size(200, 21), style=0, value='')

        self.st15Page1 = wx.StaticText(id=-1, label=PList["0202"][1] + ' ' + PList["0202"][2], name='st15Page1', parent=self.Page1, pos=wx.Point(248, 88), style=0)

        self.tc15Page1 = wx.TextCtrl(id=-1,
              name='tc15Page1', parent=self.Page1, pos=wx.Point(248, 104),
              size=wx.Size(200, 21), style=0, value='')

        self.st16Page1 = wx.StaticText(id=-1, label=PList["0203"][1] + ' ' + PList["0203"][2], name='st16Page1', parent=self.Page1, pos=wx.Point(248, 128), style=0)

        self.tc16Page1 = wx.TextCtrl(id=-1,
              name='tc16Page1', parent=self.Page1, pos=wx.Point(248, 144),
              size=wx.Size(200, 21), style=0, value='')

        self.st17Page1 = wx.StaticText(id=-1, label=PList["0204"][1], name='st17Page1', parent=self.Page1, pos=wx.Point(248, 168), style=0)

        self.tc17Page1 = wx.TextCtrl(id=-1,
              name='tc17Page1', parent=self.Page1, pos=wx.Point(248, 184),
              size=wx.Size(200, 21), style=0, value='')

        self.st18Page1 = wx.StaticText(id=-1, label=PList["0205"][1] + ' ' + PList["0205"][2], name='st18Page1', parent=self.Page1, pos=wx.Point(248, 208), style=0)

        self.tc18Page1 = wx.TextCtrl(id=-1,
              name='tc18Page1', parent=self.Page1, pos=wx.Point(248, 224),
              size=wx.Size(200, 21), style=0, value='')

        self.st19Page1 = wx.StaticText(id=-1, label=PList["0206"][1] + ' ' + PList["0206"][2], name='st19Page1', parent=self.Page1, pos=wx.Point(248, 248), style=0)

        self.tc19Page1 = wx.TextCtrl(id=-1, 
              name='tc19Page1', parent=self.Page1, pos=wx.Point(248, 264),
              size=wx.Size(200, 21), style=0, value='')

        self.st20Page1 = wx.StaticText(id=-1, label=PList["0207"][1] + ' ' + PList["0207"][2], name='st20Page1', parent=self.Page1, pos=wx.Point(248, 288), style=0)

        self.tc20Page1 = wx.TextCtrl(id=-1,
              name='tc20Page1', parent=self.Page1, pos=wx.Point(248, 304),
              size=wx.Size(200, 21), style=0, value='')

        self.st21Page1 = wx.StaticText(id=-1, label=PList["0208"][1] + ' ' + PList["0208"][2], name='st21Page1', parent=self.Page1, pos=wx.Point(248, 328), style=0)

        self.tc21Page1 = wx.TextCtrl(id=-1,
              name='tc21Page1', parent=self.Page1, pos=wx.Point(248, 344),
              size=wx.Size(200, 21), style=0, value='')

        self.st22Page1 = wx.StaticText(id=-1, label=PList["0210"][1] + ' ' + PList["0210"][2], name='st22Page1', parent=self.Page1, pos=wx.Point(248, 408), style=0)

        self.tc22Page1 = wx.TextCtrl(id=-1,
              name='tc22Page1', parent=self.Page1, pos=wx.Point(248, 424),
              size=wx.Size(200, 21), style=0, value='')

        self.st23Page1 = wx.StaticText(id=-1, label=PList["0211"][1], name='st23Page1', parent=self.Page1, pos=wx.Point(248, 448), style=0)

        self.tc23Page1 = wx.TextCtrl(id=-1,
              name='tc23Page1', parent=self.Page1, pos=wx.Point(248, 464),
              size=wx.Size(200, 21), style=0, value='')

        self.st24Page1 = wx.StaticText(id=-1, label=PList["0212"][1] + ' ' + PList["0212"][2], name='st24Page1', parent=self.Page1, pos=wx.Point(248, 488), style=0)

        self.tc24Page1 = wx.TextCtrl(id=-1,
              name='tc24Page1', parent=self.Page1, pos=wx.Point(248, 504),
              size=wx.Size(200, 21), style=0, value='')

        self.st25_1Page1 = wx.StaticText(id=-1, label=PList["0213"][1], name='st25Page1', parent=self.Page1, pos=wx.Point(248, 528), style=0)

        self.tc25_1Page1 = wx.TextCtrl(id=-1,
              name='tc25_1Page1', parent=self.Page1, pos=wx.Point(248, 544),
              size=wx.Size(96, 21), style=0, value='')

        self.tc25_2Page1 = wx.TextCtrl(id=-1,
              name='tc25_2Page1', parent=self.Page1, pos=wx.Point(352, 544),
              size=wx.Size(96, 21), style=0, value='')

        self.choiceOfNaceCodePage1 = wx.Choice(choices=[],
              id=-1, name='choiceOfNaceCodePage1', parent=self.Page1, pos=wx.Point(16,544),
              size=wx.Size(200, 21), style=0)

        self.buttonStoreDataPage1 = wx.Button(id=-1,
              label=PList["X019"][1], name='buttonStoreDataPage1',
              parent=self.Page1, pos=wx.Point(592, 552), size=wx.Size(104, 23),
              style=0)

        

        self.listBoxProductsPage1 = wx.ListBox(choices=[],
              id=-1,
              name='listBoxProductsPage1', parent=self.Page1, pos=wx.Point(496,
              416), size=wx.Size(200, 96), style=0)


        self.stInfo6Page1 = wx.StaticText(id=-1, label=PList["X023"][1], name='stInfo6Page1', parent=self.Page1, pos=wx.Point(496, 400), style=0)
        self.stInfo6Page1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.st27Page1 = wx.StaticText(id=-1, label=PList["0217"][1], name='st27Page1', parent=self.Page1, pos=wx.Point(496, 88), style=0)

        self.tc27Page1 = wx.TextCtrl(id=-1,
              name='tc27Page1', parent=self.Page1, pos=wx.Point(496, 104),
              size=wx.Size(200, 21), style=0, value='')

        self.st28Page1 = wx.StaticText(id=-1, label=PList["0218"][1] + ' ' + PList["0218"][2], name='st28Page1', parent=self.Page1, pos=wx.Point(496, 128), style=0)

        self.tc28Page1 = wx.TextCtrl(id=-1,
              name='tc28Page1', parent=self.Page1, pos=wx.Point(496, 144),
              size=wx.Size(200, 21), style=0, value='')

        self.st29Page1 = wx.StaticText(id=-1, label=PList["0219"][1], name='st29Page1', parent=self.Page1, pos=wx.Point(496, 168), style=0)

        self.tc29Page1 = wx.TextCtrl(id=-1,
              name='tc29Page1', parent=self.Page1, pos=wx.Point(496, 184),
              size=wx.Size(200, 21), style=0, value='')

        self.st32Page1 = wx.StaticText(id=-1, label=PList["0443"][1], name='st32Page1', parent=self.Page1, pos=wx.Point(496, 320), style=0)

        self.tc31Page1 = wx.TextCtrl(id=-1,
              name='tc31Page1', parent=self.Page1, pos=wx.Point(496, 296),
              size=wx.Size(200, 21), style=0, value='')

        self.st26Page1 = wx.StaticText(id=-1, label=PList["0216"][1], name='st26Page1', parent=self.Page1, pos=wx.Point(496, 48), style=0)

        self.tc26Page1 = wx.TextCtrl(id=-1,
              name='tc26Page1', parent=self.Page1, pos=wx.Point(496, 64),
              size=wx.Size(200, 21), style=0, value='')

        self.stInfo4Page1 = wx.StaticText(id=-1, label=PList["X024"][1], name='stInfo4Page1', parent=self.Page1, pos=wx.Point(496, 24), style=0)
        self.stInfo4Page1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.buttonAddProductPage1 = wx.Button(id=-1, label=PList["X025"][1], name='buttonAddProductPage1',
              parent=self.Page1, pos=wx.Point(608, 368), size=wx.Size(91, 16),
              style=0)


        self.st31Page1 = wx.StaticText(id=-1, label=PList["0444"][1], name='st31Page1', parent=self.Page1, pos=wx.Point(496, 280), style=0)

        self.tc32Page1 = wx.TextCtrl(id=-1,
              name='tc32Page1', parent=self.Page1, pos=wx.Point(496, 336),
              size=wx.Size(200, 21), style=0, value='')

        self.st30Page1 = wx.StaticText(id=-1, label=PList["0220"][1] + ' ' + PList["0220"][2], name='st30Page1', parent=self.Page1, pos=wx.Point(496, 208), style=0)

        self.tc30Page1 = wx.TextCtrl(id=-1,
              name='tc30Page1', parent=self.Page1, pos=wx.Point(496, 224),
              size=wx.Size(200, 21), style=0, value='')

        self.stInfo5Page1 = wx.StaticText(id=-1, label=PList["X026"][1], name='stInfo5Page1', parent=self.Page1, pos=wx.Point(496, 256), style=0)
        self.stInfo5Page1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.buttonDeleteProductPage1 = wx.Button(id=-1, label=PList["X027"][1], name='buttonDeleteProductPage1',
              parent=self.Page1, pos=wx.Point(608, 520), size=wx.Size(83, 16), style=0)


        self.buttonClearPage1 = wx.Button(id=-1, label=PList["X028"][1], name='buttonClearPage1', parent=self.Page1,
              pos=wx.Point(496, 368), size=wx.Size(75, 16), style=0)


        ####--- End of PAGE 1


        ####----PAGE 2
        self.Page2 = wx.Panel(id=-1, name='Page2', parent=self.leftpanel2, pos=wx.Point(0,
              0), size=wx.Size(800, 600), style=0)

        self.Page2.Hide()

        #self.tc1Page2 = wx.TextCtrl(id=-1, name='tc1Page2', parent=self.Page2,
        #      pos=wx.Point(248, 64), size=wx.Size(200, 21), style=0, value='')

        self.st1Page2 = wx.StaticText(id=-1, label=PList["0401"][1], name='st1Page2', parent=self.Page2, pos=wx.Point(248, 48), style=0)
        self.choiceOfDBFuelTypePage2 = wx.Choice(choices=[],
              id=-1, name='choiceOfDBFuelTypePage2', parent=self.Page2, pos=wx.Point(248, 64),
              size=wx.Size(200, 21), style=0)

        self.st2Page2 = wx.StaticText(id=-1, label=PList["0402"][1], name='st2Page2', parent=self.Page2, pos=wx.Point(248, 88), style=0)

        self.tc2Page2 = wx.TextCtrl(id=-1, name='tc2Page2', parent=self.Page2,
              pos=wx.Point(248, 104), size=wx.Size(200, 21), style=0, value='')

        self.st3Page2 = wx.StaticText(id=-1, label=PList["0403"][2], name='st3Page2', parent=self.Page2, pos=wx.Point(248, 128), style=0)

        self.tc3Page2 = wx.TextCtrl(id=-1, name='tc3Page2', parent=self.Page2,
              pos=wx.Point(248, 144), size=wx.Size(200, 21), style=0, value='')

        self.st4Page2 = wx.StaticText(id=-1, label=PList["0404"][2], name='st4Page2', parent=self.Page2, pos=wx.Point(472, 48), style=0)

        self.tc4Page2 = wx.TextCtrl(id=-1, name='tc4Page2', parent=self.Page2,
              pos=wx.Point(472, 64), size=wx.Size(200, 21), style=0, value='')

        self.st5Page2 = wx.StaticText(id=-1, label=PList["0405"][1] + " " + PList["0405"][2], name='st5Page2', parent=self.Page2, pos=wx.Point(472, 88), style=0)

        self.tc5Page2 = wx.TextCtrl(id=-1, name='tc5Page2', parent=self.Page2,
              pos=wx.Point(472, 104), size=wx.Size(200, 21), style=0, value='')

        self.st6Page2 = wx.StaticText(id=-1, label=PList["0406"][1] + " " + PList["0406"][2], name='st6Page2', parent=self.Page2, pos=wx.Point(472, 128), style=0)

        self.tc6Page2 = wx.TextCtrl(id=-1, name='tc6Page2', parent=self.Page2,
              pos=wx.Point(472, 144), size=wx.Size(200, 21), style=0, value='')

        self.stInfo1Page2 = wx.StaticText(id=-1, label=PList["X029"][1], name='stInfo1Page2', parent=self.Page2, pos=wx.Point(32, 24), style=0)
        self.stInfo1Page2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.fuelListBoxPage2 = wx.ListBox(choices=[], id=-1, name='fuelListBoxPage2',
              parent=self.Page2, pos=wx.Point(32, 64), size=wx.Size(160, 112),
              style=0)


        self.stInfo2Page2 = wx.StaticText(id=-1, label=PList["X030"][1], name='stInfo2Page2', parent=self.Page2, pos=wx.Point(32, 48), style=0)
        self.stInfo2Page2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.buttonAddFuelPage2 = wx.Button(id=-1, label=PList["X031"][1],
              name='buttonAddFuelPage2', parent=self.Page2, pos=wx.Point(592,
              176), size=wx.Size(75, 16), style=0)


        self.buttonRemoveFuelFromListPage2 = wx.Button(id=-1,
              label=PList["X032"][1], name='buttonRemoveFuelFromListPage2',
              parent=self.Page2, pos=wx.Point(88, 184), size=wx.Size(104, 16),
              style=0)

        self.scrolledWindowPage2 = wx.ScrolledWindow(id=-1,
              name='scrolledWindowPage2', parent=self.Page2, pos=wx.Point(0,
              268), size=wx.Size(790, 260), style=wx.HSCROLL)
        self.scrolledWindowPage2.SetScrollbars(1,1, 950,240)

        self.buttonStorePage2 = wx.Button(id=-1, label=PList["X019"][1],
              name='buttonStorePage2', parent=self.Page2, pos=wx.Point(696,
              560), size=wx.Size(75, 23), style=0)


        self.stInfo3Page2 = wx.StaticText(id=-1, label=PList["X033"][1], name='stInfo3Page2', parent=self.Page2, pos=wx.Point(32, 240), style=0)
        self.stInfo3Page2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.buttonClearPage2 = wx.Button(id=-1, label=PList["X028"][1],
              name='buttonClearPage2', parent=self.Page2, pos=wx.Point(248,
              176), size=wx.Size(75, 16), style=0)



        ###-- start grid page 2
        self.gridPage2 = wx.grid.Grid(id=-1, name='gridPage2', parent=self.scrolledWindowPage2,
                                      pos=wx.Point(0, 0), size=wx.Size(940, 240), style=0)
        
        self.gridPage2.EnableGridLines(True)
        self.gridPage2.CreateGrid(9, 6)

        self.gridPage2.SetDefaultColSize(120, resizeExistingCols=False)
        self.gridPage2.SetDefaultRowSize(23, resizeExistingRows=False)

        self.gridPage2.SetRowLabelSize(220)
        
        
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour("light gray")
        attr.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.gridPage2.SetAttr(7, 0, attr)
        self.gridPage2.SetAttr(7, 1, attr)
        self.gridPage2.SetAttr(7, 2, attr)
        self.gridPage2.SetAttr(7, 3, attr)
        self.gridPage2.SetAttr(7, 4, attr)
        self.gridPage2.SetAttr(7, 5, attr)
        

        attr2 = wx.grid.GridCellAttr()
        attr2.SetBackgroundColour("light gray")
        attr2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.gridPage2.SetAttr(6, 0, attr2)
        self.gridPage2.SetAttr(6, 3, attr2)

        

        attr3 = wx.grid.GridCellAttr()
        attr3.SetBackgroundColour("light gray")
        attr3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.gridPage2.SetAttr(2, 4, attr3)


        attr4 = wx.grid.GridCellAttr()
        attr4.SetBackgroundColour("light gray")
        attr4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.gridPage2.SetAttr(1, 4, attr4)
        
        
        
        self.gridPage2.SetColLabelValue(0,PList["X043"][1])
        self.gridPage2.SetColLabelValue(1,PList["X044"][1])
        self.gridPage2.SetColLabelValue(2,PList["X045"][1])
        self.gridPage2.SetColLabelValue(3,PList["X046"][1])
        self.gridPage2.SetColLabelValue(4,PList["X047"][1])
        self.gridPage2.SetColLabelValue(5,PList["X048"][1])

        self.gridPage2.SetRowLabelValue(0,PList["X034"][1])
        self.gridPage2.SetRowLabelValue(1,PList["X035"][1])
        self.gridPage2.SetRowLabelValue(2,PList["X036"][1])
        self.gridPage2.SetRowLabelValue(3,PList["X037"][1])
        self.gridPage2.SetRowLabelValue(4,PList["X038"][1])
        self.gridPage2.SetRowLabelValue(5,PList["X039"][1])
        self.gridPage2.SetRowLabelValue(6,PList["X040"][1])
        self.gridPage2.SetRowLabelValue(7,PList["X041"][1])
        self.gridPage2.SetRowLabelValue(8,PList["X042"][1])

        self.gridPage2.SetRowLabelAlignment(wx.LEFT, wx.BOTTOM)

        self.gridPage2.SetCellSize(6, 0, 1, 3)
        self.gridPage2.SetCellSize(6, 3, 1, 3)
        self.gridPage2.SetCellSize(1, 4, 1, 2)
        self.gridPage2.SetCellSize(2, 4, 4, 1)



        self.gridPage2.SetCellValue(6, 0, PList["X049"][1])
        self.gridPage2.SetCellValue(6, 3, PList["X050"][1])
        self.gridPage2.SetCellValue(7, 0, PList["X051"][1])
        self.gridPage2.SetCellValue(7, 1, PList["X052"][1])
        self.gridPage2.SetCellValue(7, 2, PList["X053"][1])
        self.gridPage2.SetCellValue(7, 3, PList["X054"][1])
        self.gridPage2.SetCellValue(7, 4, PList["X055"][1])
        self.gridPage2.SetCellValue(7, 5, PList["X056"][1])

        self.gridPage2.SetReadOnly(6, 0, isReadOnly=True)
        self.gridPage2.SetReadOnly(6, 3, isReadOnly=True)
        self.gridPage2.SetReadOnly(7, 0, isReadOnly=True)
        self.gridPage2.SetReadOnly(7, 1, isReadOnly=True)
        self.gridPage2.SetReadOnly(7, 2, isReadOnly=True)
        self.gridPage2.SetReadOnly(7, 3, isReadOnly=True)
        self.gridPage2.SetReadOnly(7, 4, isReadOnly=True)
        self.gridPage2.SetReadOnly(7, 5, isReadOnly=True)
        self.gridPage2.SetReadOnly(1, 4, isReadOnly=True)
        self.gridPage2.SetReadOnly(2, 4, isReadOnly=True)

        
        self.gridPage2.SetCellAlignment(7, 0, wx.ALIGN_CENTRE, wx.ALIGN_BOTTOM)
        self.gridPage2.SetCellAlignment(6, 0, wx.ALIGN_CENTRE, wx.ALIGN_BOTTOM)


        ###-- end grid page 2
        
        


        ####--- End of PAGE 2



        ####----PAGE 3


        self.Page3 = wx.Panel(id=-1,
              name='Page3', parent=self.leftpanel2, pos=wx.Point(0, 0),
              size=wx.Size(800, 600), style=0)
        self.Page3.Hide()

        self.tc1Page3 = wx.TextCtrl(id=-1, name='tc1Page3',
              parent=self.Page3, pos=wx.Point(16, 352), size=wx.Size(200, 21),
              style=0, value='')

        self.st1Page3 = wx.StaticText(id=-1, label=PList["0301"][1] + ' ' + PList["0301"][2], name='st1Page3', parent=self.Page3, pos=wx.Point(16, 336), style=0)

        self.st2Page3 = wx.StaticText(id=-1, label=PList["0303"][1] + ' ' + PList["0303"][2], name='st2Page3', parent=self.Page3, pos=wx.Point(16, 376), style=0)

        self.tc2Page3 = wx.TextCtrl(id=-1, name='tc2Page3',
              parent=self.Page3, pos=wx.Point(16, 392), size=wx.Size(200, 21),
              style=0, value='')


        self.st3Page3 = wx.StaticText(id=-1, label=PList["0302"][1] + ' ' + PList["0302"][2], name='st3Page3', parent=self.Page3, pos=wx.Point(16, 416), style=0)

        #self.tc3Page3 = wx.TextCtrl(id=-1, name='tc3Page3',
        #      parent=self.Page3, pos=wx.Point(16, 432), size=wx.Size(200, 21),
        #      style=0, value='')
        self.choiceOfDBUnitOperationPage3 = wx.Choice(choices=[],
              id=-1, name='choiceOfDBUnitOperationPage3', parent=self.Page3, pos=wx.Point(16, 432),
              size=wx.Size(200, 21), style=0)

        self.st4Page3 = wx.StaticText(id=-1, label=PList["0304"][1] + ' ' + PList["0304"][2], name='st4Page3', parent=self.Page3, pos=wx.Point(16, 456), style=0)

        #self.tc4Page3 = wx.TextCtrl(id=-1, name='tc4Page3',
        #      parent=self.Page3, pos=wx.Point(16, 472), size=wx.Size(200, 21),
        #      style=0, value='')
        self.choiceOfPMDBFluidPage3 = wx.Choice(choices=[],
              id=-1, name='choiceOfPMDBFluidPage3', parent=self.Page3, pos=wx.Point(16, 472),
              size=wx.Size(200, 21), style=0)        

        self.st5Page3 = wx.StaticText(id=-1, label=PList["0305"][1] + ' ' + PList["0305"][2], name='st5Page3', parent=self.Page3, pos=wx.Point(16, 496), style=0)

        self.tc5Page3 = wx.TextCtrl(id=-1, name='tc5Page3',
              parent=self.Page3, pos=wx.Point(16, 512), size=wx.Size(200, 21),
              style=0, value='')

        self.st6Page3 = wx.StaticText(id=-1, label=PList["0306"][1] + ' ' + PList["0306"][2], name='st6Page3', parent=self.Page3, pos=wx.Point(16, 536), style=0)

        self.tc6Page3 = wx.TextCtrl(id=-1, name='tc6Page3',
              parent=self.Page3, pos=wx.Point(16, 552), size=wx.Size(200, 21),
              style=0, value='')

        self.st7Page3 = wx.StaticText(id=-1, label=PList["0307"][1] + ' ' + PList["0307"][2], name='st7Page3', parent=self.Page3, pos=wx.Point(240, 40), style=0)

        self.tc7Page3 = wx.TextCtrl(id=-1, name='tc7Page3',
              parent=self.Page3, pos=wx.Point(240, 56), size=wx.Size(200, 21),
              style=0, value='')

        self.st8Page3 = wx.StaticText(id=-1, label=PList["0308"][1] + ' ' + PList["0308"][2], name='st8Page3', parent=self.Page3, pos=wx.Point(240, 80), style=0)

        self.tc8Page3 = wx.TextCtrl(id=-1, name='tc8Page3',
              parent=self.Page3, pos=wx.Point(240, 96), size=wx.Size(200, 21),
              style=0, value='')

        self.st9Page3 = wx.StaticText(id=-1, label=PList["0309"][1] + ' ' + PList["0309"][2], name='st9Page3', parent=self.Page3, pos=wx.Point(240, 120), style=0)

        self.tc9Page3 = wx.TextCtrl(id=-1, name='tc9Page3',
              parent=self.Page3, pos=wx.Point(240, 136), size=wx.Size(200, 21),
              style=0, value='')

        self.st10Page3 = wx.StaticText(id=-1, label=PList["0310"][1] + ' ' + PList["0310"][2], name='st10Page3', parent=self.Page3, pos=wx.Point(240, 160), style=0)

        self.tc10Page3 = wx.TextCtrl(id=-1, name='tc10Page3',
              parent=self.Page3, pos=wx.Point(240, 176), size=wx.Size(200, 21),
              style=0, value='')

        self.st11Page3 = wx.StaticText(id=-1, label=PList["0312"][1] + ' ' + PList["0312"][2], name='st11Page3', parent=self.Page3, pos=wx.Point(240, 232), style=0)

        self.tc11Page3 = wx.TextCtrl(id=-1, name='tc11Page3',
              parent=self.Page3, pos=wx.Point(240, 248), size=wx.Size(200, 21),
              style=0, value='')

        self.st12Page3 = wx.StaticText(id=-1, label=PList["0313"][1] + ' ' + PList["0313"][2], name='st12Page3', parent=self.Page3, pos=wx.Point(240, 272), style=0)

        self.tc12Page3 = wx.TextCtrl(id=-1, name='tc12Page3',
              parent=self.Page3, pos=wx.Point(240, 288), size=wx.Size(200, 21),
              style=0, value='')

        self.st13Page3 = wx.StaticText(id=-1, label=PList["0314"][1] + ' ' + PList["0314"][2], name='st13Page3', parent=self.Page3, pos=wx.Point(240, 312), style=0)

        self.tc13Page3 = wx.TextCtrl(id=-1, name='tc13Page3',
              parent=self.Page3, pos=wx.Point(240, 328), size=wx.Size(200, 21),
              style=0, value='')

        self.st14Page3 = wx.StaticText(id=-1, label=PList["0315"][1] + ' ' + PList["0315"][2], name='st14Page3', parent=self.Page3, pos=wx.Point(240, 352), style=0)

        self.tc14Page3 = wx.TextCtrl(id=-1, name='tc14Page3',
              parent=self.Page3, pos=wx.Point(240, 368), size=wx.Size(200, 21),
              style=0, value='')

        self.st15Page3 = wx.StaticText(id=-1, label=PList["0317"][1] + ' ' + PList["0317"][2], name='st15Page3', parent=self.Page3, pos=wx.Point(240, 432), style=0)

        self.tc15Page3 = wx.TextCtrl(id=-1, name='tc15Page3',
              parent=self.Page3, pos=wx.Point(240, 448), size=wx.Size(200, 21),
              style=0, value='')

        self.st16Page3 = wx.StaticText(id=-1, label=PList["0318"][1] + ' ' + PList["0318"][2], name='st16Page3', parent=self.Page3, pos=wx.Point(240, 472), style=0)

        self.tc16Page3 = wx.TextCtrl(id=-1, name='tc16Page3',
              parent=self.Page3, pos=wx.Point(240, 488), size=wx.Size(200, 21),
              style=0, value='')

        self.st17Page3 = wx.StaticText(id=-1, label=PList["0319"][1] + ' ' + PList["0319"][2], name='st17Page3', parent=self.Page3, pos=wx.Point(240, 512), style=0)

        self.tc17Page3 = wx.TextCtrl(id=-1, name='tc17Page3',
              parent=self.Page3, pos=wx.Point(240, 528), size=wx.Size(200, 21),
              style=0, value='')

        self.st18Page3 = wx.StaticText(id=-1, label=PList["0320"][1] + ' ' + PList["0320"][2], name='st18Page3', parent=self.Page3, pos=wx.Point(240, 552), style=0)

        self.tc18Page3 = wx.TextCtrl(id=-1, name='tc18Page3',
              parent=self.Page3, pos=wx.Point(240, 568), size=wx.Size(200, 21),
              style=0, value='')

        self.st19Page3 = wx.StaticText(id=-1, label=PList["0322"][1] + ' ' + PList["0322"][2], name='st19Page3', parent=self.Page3, pos=wx.Point(488, 40), style=0)

        self.tc19Page3 = wx.TextCtrl(id=-1, name='tc19Page3',
              parent=self.Page3, pos=wx.Point(488, 56), size=wx.Size(200, 21),
              style=0, value='')

        self.st20Page3 = wx.StaticText(id=-1, label=PList["0323"][1] + ' ' + PList["0323"][2], name='st20Page3', parent=self.Page3, pos=wx.Point(488, 80), style=0)

        self.tc20Page3 = wx.TextCtrl(id=-1, name='tc20Page3',
              parent=self.Page3, pos=wx.Point(488, 96), size=wx.Size(200, 21),
              style=0, value='')

        self.st21Page3 = wx.StaticText(id=-1, label=PList["0324"][1] + ' ' + PList["0324"][2], name='st21Page3', parent=self.Page3, pos=wx.Point(488, 120), style=0)

        self.tc21Page3 = wx.TextCtrl(id=-1, name='tc21Page3',
              parent=self.Page3, pos=wx.Point(488, 136), size=wx.Size(200, 21),
              style=0, value='')

        self.st22Page3 = wx.StaticText(id=-1, label=PList["0327"][1] + ' ' + PList["0327"][2], name='st22Page3', parent=self.Page3, pos=wx.Point(488, 216), style=0)

        #self.tc22Page3 = wx.TextCtrl(id=-1, name='tc22Page3',
        #      parent=self.Page3, pos=wx.Point(488, 232), size=wx.Size(200, 21),
        #      style=0, value='')

        self.choiceOfSMDBFluidPage3 = wx.Choice(choices=[],
              id=-1, name='choiceOfSMDBFluidPage3', parent=self.Page3, pos=wx.Point(488, 232),
              size=wx.Size(200, 21), style=0)

        self.st23Page3 = wx.StaticText(id=-1, label=PList["0328"][1] + ' ' + PList["0328"][2], name='st23Page3', parent=self.Page3, pos=wx.Point(488, 256), style=0)

        self.tc23Page3 = wx.TextCtrl(id=-1, name='tc23Page3',
              parent=self.Page3, pos=wx.Point(488, 272), size=wx.Size(200, 21),
              style=0, value='')

        self.st24Page3 = wx.StaticText(id=-1, label=PList["0329"][1] + ' ' + PList["0329"][2], name='st24Page3', parent=self.Page3, pos=wx.Point(488, 296), style=0)

        self.tc24Page3 = wx.TextCtrl(id=-1, name='tc24Page3',
              parent=self.Page3, pos=wx.Point(488, 312), size=wx.Size(200, 21),
              style=0, value='')

        self.st25Page3 = wx.StaticText(id=-1, label=PList["0330"][1] + ' ' + PList["0330"][2], name='st25Page3', parent=self.Page3, pos=wx.Point(488, 336), style=0)

        self.tc25Page3 = wx.TextCtrl(id=-1, name='tc25Page3',
              parent=self.Page3, pos=wx.Point(488, 352), size=wx.Size(200, 21),
              style=0, value='')

        self.st26Page3 = wx.StaticText(id=-1, label=PList["0331"][1] + ' ' + PList["0331"][2], name='st26Page3', parent=self.Page3, pos=wx.Point(488, 376), style=0)

        self.tc26Page3 = wx.TextCtrl(id=-1, name='tc26Page3',
              parent=self.Page3, pos=wx.Point(488, 392), size=wx.Size(200, 21),
              style=0, value='')

        self.stInfo2Page3 = wx.StaticText(id=-1, label=PList["0300"][1], name='stInfo2Page3', parent=self.Page3, pos=wx.Point(16, 312), style=0)
        self.stInfo2Page3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo3Page3 = wx.StaticText(id=-1, label=PList["0311"][1], name='stInfo3Page3', parent=self.Page3, pos=wx.Point(240, 208), style=0)
        self.stInfo3Page3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo4Page3 = wx.StaticText(id=-1, label=PList["0316"][1], name='stInfo4Page3', parent=self.Page3, pos=wx.Point(240, 408), style=0)
        self.stInfo4Page3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo5Page3 = wx.StaticText(id=-1, label=PList["0321"][1], name='stInfo5Page3', parent=self.Page3, pos=wx.Point(488, 16), style=0)
        self.stInfo5Page3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        
        self.stInfo6Page3 = wx.StaticText(id=-1, label=PList["0326"][1], name='stInfo6Page3', parent=self.Page3, pos=wx.Point(488, 192), style=0)
        self.stInfo6Page3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.buttonAddProcessPage3 = wx.Button(id=-1,
              label=PList["X057"][1], name='buttonAddProcessPage3',
              parent=self.Page3, pos=wx.Point(600, 568), size=wx.Size(83, 15),
              style=0)


        self.listBoxProcessesPage3 = wx.ListBox(choices=[],
              id=-1, name='listBoxProcessesPage3',
              parent=self.Page3, pos=wx.Point(16, 40), size=wx.Size(200, 216),
              style=0)


        self.stInfo1Page3 = wx.StaticText(id=-1,
              label=PList["X059"][1], name='stInfo1Page3', parent=self.Page3,
              pos=wx.Point(16, 24), size=wx.Size(64, 13), style=0)
        self.stInfo1Page3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.buttonDeleteProcessPage3 = wx.Button(id=-1,
              label=PList["X058"][1], name='buttonDeleteProcessPage3',
              parent=self.Page3, pos=wx.Point(136, 264), size=wx.Size(83, 16),
              style=0)


        self.buttonClearPage3 = wx.Button(id=-1,
              label=PList["X028"][1], name='buttonClearPage3', parent=self.Page3,
              pos=wx.Point(488, 568), size=wx.Size(75, 16), style=0)




        ####--- End of PAGE 3


        
        ####----PAGE 4

        self.Page4 = wx.Panel(id=-1, name='Page4',
              parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
        self.Page4.Hide()


        self.stInfo1Page4 = wx.StaticText(id=-1, label=PList["X060"][1], name='stInfo1Page4', parent=self.Page4, pos=wx.Point(24, 24), style=0)
        self.stInfo1Page4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo2Page4 = wx.StaticText(id=-1, label=PList["0500"][1], name='stInfo2Page4', parent=self.Page4, pos=wx.Point(272, 24), style=0)
        self.stInfo2Page4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))


        self.listBoxEquipmentListPage4 = wx.ListBox(choices=[],
              id=-1,
              name='listBoxEquipmentListPage4', parent=self.Page4,
              pos=wx.Point(24, 40), size=wx.Size(200, 216), style=0)


        self.buttonDeleteEquipmentPage4 = wx.Button(id=-1,
              label=PList["X061"][1], name='buttonDeleteEquipmentPage4',
              parent=self.Page4, pos=wx.Point(120, 264), size=wx.Size(107, 16),
              style=0)

        self.buttonAddEquipmentPage4 = wx.Button(id=-1,
              label=PList["X062"][1], name='buttonAddEquipmentPage4',
              parent=self.Page4, pos=wx.Point(584, 464), size=wx.Size(123, 16),
              style=0)

        self.buttonClearPage4 = wx.Button(id=-1,
              label=PList["X028"][1], name='buttonClearPage4', parent=self.Page4,
              pos=wx.Point(272, 464), size=wx.Size(120, 16), style=0)


        

        self.st1Page4 = wx.StaticText(id=-1, label=PList["0501"][1] + ' ' + PList["0501"][2], name='st1Page4', parent=self.Page4, pos=wx.Point(272, 48), style=0)

        self.tc1Page4 = wx.TextCtrl(id=-1, name='tc1Page4',
              parent=self.Page4, pos=wx.Point(272, 64), size=wx.Size(200, 21),
              style=0, value='')


        self.st2Page4 = wx.StaticText(id=-1, label=PList["0502"][1] + ' ' + PList["0502"][2], name='st2Page4', parent=self.Page4, pos=wx.Point(272, 88), style=0)

        self.tc2Page4 = wx.TextCtrl(id=-1, name='tc2Page4',
              parent=self.Page4, pos=wx.Point(272, 104), size=wx.Size(200, 21),
              style=0, value='')


        self.st3Page4 = wx.StaticText(id=-1, label=PList["0503"][1] + ' ' + PList["0503"][2], name='st3Page4', parent=self.Page4, pos=wx.Point(272, 128), style=0)

        self.tc3Page4 = wx.TextCtrl(id=-1, name='tc3Page4',
              parent=self.Page4, pos=wx.Point(272, 144), size=wx.Size(200, 21),
              style=0, value='')


        self.st4Page4 = wx.StaticText(id=-1, label=PList["0504"][1] + ' ' + PList["0504"][2], name='st4Page4', parent=self.Page4, pos=wx.Point(272, 168), style=0)

        self.tc4Page4 = wx.TextCtrl(id=-1, name='tc4Page4',
              parent=self.Page4, pos=wx.Point(272, 184), size=wx.Size(200, 21),
              style=0, value='')


        self.st5Page4 = wx.StaticText(id=-1, label=PList["0505"][1] + ' ' + PList["0505"][2], name='st5Page4', parent=self.Page4, pos=wx.Point(272, 208), style=0)

        self.tc5Page4 = wx.TextCtrl(id=-1, name='tc5Page4',
              parent=self.Page4, pos=wx.Point(272, 224), size=wx.Size(200, 21),
              style=0, value='')


        self.st6Page4 = wx.StaticText(id=-1, label=PList["0506"][1] + ' ' + PList["0506"][2], name='st6Page4', parent=self.Page4, pos=wx.Point(272, 248), style=0)

        self.tc6Page4 = wx.TextCtrl(id=-1, name='tc6Page4',
              parent=self.Page4, pos=wx.Point(272, 264), size=wx.Size(200, 21),
              style=0, value='')


        self.st7Page4 = wx.StaticText(id=-1, label=PList["0507"][1] + ' ' + PList["0507"][2], name='st7Page4', parent=self.Page4, pos=wx.Point(272, 288), style=0)

        #self.tc7Page4 = wx.TextCtrl(id=-1, name='tc7Page4',
        #      parent=self.Page4, pos=wx.Point(272, 304), size=wx.Size(200, 21),
        #      style=0, value='')
        self.choiceOfDBFuelPage4 = wx.Choice(choices=[],
              id=-1, name='choiceOfDBFuelPage4', parent=self.Page4, pos=wx.Point(272, 304),
              size=wx.Size(200, 21), style=0)


        self.st8Page4 = wx.StaticText(id=-1, label=PList["0521"][1] + ' ' + PList["0521"][2], name='st8Page4', parent=self.Page4, pos=wx.Point(272, 328), style=0)

        self.tc8Page4 = wx.TextCtrl(id=-1, name='tc8Page4',
              parent=self.Page4, pos=wx.Point(272, 344), size=wx.Size(200, 21),
              style=0, value='')


        self.st9Page4 = wx.StaticText(id=-1, label=PList["0508"][1] + ' ' + PList["0508"][2], name='st9Page4', parent=self.Page4, pos=wx.Point(272, 368), style=0)

        self.tc9Page4 = wx.TextCtrl(id=-1, name='tc9Page4',
              parent=self.Page4, pos=wx.Point(272, 384), size=wx.Size(200, 21),
              style=0, value='')


        self.st10Page4 = wx.StaticText(id=-1, label=PList["0509"][1] + ' ' + PList["0509"][2], name='st10Page4', parent=self.Page4, pos=wx.Point(272, 408), style=0)

        self.tc10Page4 = wx.TextCtrl(id=-1, name='tc10Page4',
              parent=self.Page4, pos=wx.Point(272, 424), size=wx.Size(200, 21),
              style=0, value='')


        self.st11Page4 = wx.StaticText(id=-1, label=PList["0510"][1] + ' ' + PList["0510"][2], name='st11Page4', parent=self.Page4, pos=wx.Point(512, 48), style=0)

        self.tc11Page4 = wx.TextCtrl(id=-1, name='tc11Page4',
              parent=self.Page4, pos=wx.Point(512, 64), size=wx.Size(200, 21),
              style=0, value='')


        self.st12Page4 = wx.StaticText(id=-1, label=PList["0511"][1] + ' ' + PList["0511"][2], name='st12Page4', parent=self.Page4, pos=wx.Point(512, 88), style=0)

        self.tc12Page4 = wx.TextCtrl(id=-1, name='tc12Page4',
              parent=self.Page4, pos=wx.Point(512, 104), size=wx.Size(200, 21),
              style=0, value='')


        self.st13Page4 = wx.StaticText(id=-1, label=PList["0512"][1] + ' ' + PList["0512"][2], name='st13Page4', parent=self.Page4, pos=wx.Point(512, 128), style=0)

        self.tc13Page4 = wx.TextCtrl(id=-1, name='tc13Page4',
              parent=self.Page4, pos=wx.Point(512, 144), size=wx.Size(200, 21),
              style=0, value='')


        self.st14Page4 = wx.StaticText(id=-1, label=PList["0514"][1] + ' ' + PList["0514"][2], name='st14Page4', parent=self.Page4, pos=wx.Point(512, 168), style=0)

        self.tc14Page4 = wx.TextCtrl(id=-1, name='tc14Page4',
              parent=self.Page4, pos=wx.Point(512, 184), size=wx.Size(200, 21),
              style=0, value='')


        self.st15Page4 = wx.StaticText(id=-1, label=PList["0513"][1] + ' ' + PList["0513"][2], name='st15Page4', parent=self.Page4, pos=wx.Point(512, 208), style=0)

        self.tc15Page4 = wx.TextCtrl(id=-1, name='tc15Page4',
              parent=self.Page4, pos=wx.Point(512, 224), size=wx.Size(200, 21),
              style=0, value='')


        self.st16Page4 = wx.StaticText(id=-1, label=PList["0515"][1] + ' ' + PList["0515"][2], name='st16Page4', parent=self.Page4, pos=wx.Point(512, 248), style=0)

        self.tc16Page4 = wx.TextCtrl(id=-1, name='tc16Page4',
              parent=self.Page4, pos=wx.Point(512, 264), size=wx.Size(200, 21),
              style=0, value='')


        self.st17Page4 = wx.StaticText(id=-1, label=PList["0516"][1] + ' ' + PList["0516"][2], name='st17Page4', parent=self.Page4, pos=wx.Point(512, 288), style=0)

        self.tc17Page4 = wx.TextCtrl(id=-1, name='tc17Page4',
              parent=self.Page4, pos=wx.Point(512, 304), size=wx.Size(200, 21),
              style=0, value='')


        self.st18Page4 = wx.StaticText(id=-1, label=PList["0517"][1] + ' ' + PList["0517"][2], name='st18Page4', parent=self.Page4, pos=wx.Point(512, 328), style=0)

        self.tc18Page4 = wx.TextCtrl(id=-1, name='tc18Page4',
              parent=self.Page4, pos=wx.Point(512, 344), size=wx.Size(200, 21),
              style=0, value='')


        self.st19Page4 = wx.StaticText(id=-1, label=PList["0518"][1] + ' ' + PList["0518"][2], name='st19Page4', parent=self.Page4, pos=wx.Point(512, 368), style=0)

        self.tc19Page4 = wx.TextCtrl(id=-1, name='tc19Page4',
              parent=self.Page4, pos=wx.Point(512, 384), size=wx.Size(200, 21),
              style=0, value='')


        self.st20Page4 = wx.StaticText(id=-1, label=PList["0520"][1] + ' ' + PList["0520"][2], name='st20Page4', parent=self.Page4, pos=wx.Point(512, 408), style=0)

        self.tc20Page4 = wx.TextCtrl(id=-1, name='tc20Page4',
              parent=self.Page4, pos=wx.Point(512, 424), size=wx.Size(200, 21),
              style=0, value='')







        ####--- End of PAGE 4



        ####----PAGE 5

        self.Page5 = wx.Panel(id=-1, name='Page5',
              parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

        self.Page5.Hide()


        self.listBoxDistributionListPage5 = wx.ListBox(choices=[],
              id=-1, name='listBoxDistributionListPage5', parent=self.Page5,
              pos=wx.Point(24, 40), size=wx.Size(200, 216), style=0)



        self.stInfo1Page5 = wx.StaticText(id=-1, label=PList["X063"][1], name='stInfo1Page5', parent=self.Page5, pos=wx.Point(24, 24), style=0)
        self.stInfo1Page5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo2Page5 = wx.StaticText(id=-1, label=PList["0600"][1], name='stInfo2Page5', parent=self.Page5, pos=wx.Point(272, 24), style=0)
        self.stInfo2Page5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo3Page5 = wx.StaticText(id=-1, label=PList["0615"][1], name='stInfo3Page5', parent=self.Page5, pos=wx.Point(512, 224), style=0)
        self.stInfo3Page5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))



        self.buttonClearPage5 = wx.Button(id=-1,
              label=PList["X028"][1], name='buttonClearPage5', parent=self.Page5,
              pos=wx.Point(272, 464), size=wx.Size(120, 16), style=0)

        self.buttonDeleteDistributionPage5 = wx.Button(id=-1,
              label=PList["X064"][1], name='buttonDeleteDistributionPage5',
              parent=self.Page5, pos=wx.Point(136, 264), size=wx.Size(91, 16),
              style=0)

        self.buttonAddDistributionPage5 = wx.Button(id=-1,
              label=PList["X065"][1], name='buttonAddDistributionPage5',
              parent=self.Page5, pos=wx.Point(584, 464), size=wx.Size(123, 16),
              style=0)



        self.st1Page5 = wx.StaticText(id=-1, label=PList["0601"][1] + ' ' + PList["0601"][2], name='st1Page5', parent=self.Page5, pos=wx.Point(272, 48), style=0)        

        self.tc1Page5 = wx.TextCtrl(id=-1, name='tc1Page5',
              parent=self.Page5, pos=wx.Point(272, 64), size=wx.Size(200, 21),
              style=0, value='')        


        self.st2Page5 = wx.StaticText(id=-1, label=PList["0602"][1] + ' ' + PList["0602"][2], name='st2Page5', parent=self.Page5, pos=wx.Point(272, 88), style=0)

        #self.tc2Page5 = wx.TextCtrl(id=-1, name='tc2Page5',
        #      parent=self.Page5, pos=wx.Point(272, 104), size=wx.Size(200, 21),
        #      style=0, value='')
        self.choiceOfEquipmentPage5 = wx.Choice(choices=[],
              id=-1, name='choiceOfEquipmentPage5', parent=self.Page5, pos=wx.Point(272, 104),
              size=wx.Size(200, 21), style=0)

        self.st3Page5 = wx.StaticText(id=-1, label=PList["0603"][1] + ' ' + PList["0603"][2], name='st3Page5', parent=self.Page5, pos=wx.Point(272, 128), style=0)

        self.tc3Page5 = wx.TextCtrl(id=-1, name='tc3Page5',
              parent=self.Page5, pos=wx.Point(272, 144), size=wx.Size(200, 21),
              style=0, value='')


        self.st4Page5 = wx.StaticText(id=-1, label=PList["0604"][1] + ' ' + PList["0604"][2], name='st4Page5', parent=self.Page5, pos=wx.Point(272, 168), style=0)

        self.tc4Page5 = wx.TextCtrl(id=-1, name='tc4Page5',
              parent=self.Page5, pos=wx.Point(272, 184), size=wx.Size(200, 21),
              style=0, value='')


        self.st5Page5 = wx.StaticText(id=-1, label=PList["0605"][1] + ' ' + PList["0605"][2], name='st5Page5', parent=self.Page5, pos=wx.Point(272, 208), style=0)

        self.tc5Page5 = wx.TextCtrl(id=-1, name='tc5Page5',
              parent=self.Page5, pos=wx.Point(272, 224), size=wx.Size(200, 21),
              style=0, value='')
        

        self.st6Page5 = wx.StaticText(id=-1, label=PList["0606"][1] + ' ' + PList["0606"][2], name='st6Page5', parent=self.Page5, pos=wx.Point(272, 248), style=0)

        self.tc6Page5 = wx.TextCtrl(id=-1, name='tc6Page5',
              parent=self.Page5, pos=wx.Point(272, 264), size=wx.Size(200, 21),
              style=0, value='')
        

        self.st7Page5 = wx.StaticText(id=-1, label=PList["0607"][1] + ' ' + PList["0607"][2], name='st7Page5', parent=self.Page5, pos=wx.Point(272, 288), style=0)

        self.tc7Page5 = wx.TextCtrl(id=-1, name='tc7Page5',
              parent=self.Page5, pos=wx.Point(272, 304), size=wx.Size(200, 21),
              style=0, value='')


        self.st8Page5 = wx.StaticText(id=-1, label=PList["0608"][1] + ' ' + PList["0608"][2], name='st8Page5', parent=self.Page5, pos=wx.Point(272, 328), style=0)

        self.tc8Page5 = wx.TextCtrl(id=-1, name='tc8Page5',
              parent=self.Page5, pos=wx.Point(272, 344), size=wx.Size(200, 21),
              style=0, value='')


        self.st9Page5 = wx.StaticText(id=-1, label=PList["0609"][1] + ' ' + PList["0609"][2], name='st9Page5', parent=self.Page5, pos=wx.Point(272, 368), style=0)

        self.tc9Page5 = wx.TextCtrl(id=-1, name='tc9Page5',
              parent=self.Page5, pos=wx.Point(272, 384), size=wx.Size(200, 21),
              style=0, value='')


        self.st10Page5 = wx.StaticText(id=-1, label=PList["0610"][1] + ' ' + PList["0610"][2], name='st10Page5', parent=self.Page5, pos=wx.Point(272, 408), style=0)

        self.tc10Page5 = wx.TextCtrl(id=-1, name='tc10Page5',
              parent=self.Page5, pos=wx.Point(272, 424), size=wx.Size(200, 21),
              style=0, value='')


        self.st11Page5 = wx.StaticText(id=-1, label=PList["0611"][1] + ' ' + PList["0611"][2], name='st11Page5', parent=self.Page5, pos=wx.Point(512, 48), style=0)

        self.tc11Page5 = wx.TextCtrl(id=-1, name='tc11Page5',
              parent=self.Page5, pos=wx.Point(512, 64), size=wx.Size(200, 21),
              style=0, value='')        


        self.st12Page5 = wx.StaticText(id=-1, label=PList["0612"][1] + ' ' + PList["0612"][2], name='st12Page5', parent=self.Page5, pos=wx.Point(512, 88), style=0)
        
        self.tc12Page5 = wx.TextCtrl(id=-1, name='tc12Page5',
              parent=self.Page5, pos=wx.Point(512, 104), size=wx.Size(200, 21),
              style=0, value='')


        self.st13Page5 = wx.StaticText(id=-1, label=PList["0613"][1] + ' ' + PList["0613"][2], name='st13Page5', parent=self.Page5, pos=wx.Point(512, 128), style=0)

        self.tc13Page5 = wx.TextCtrl(id=-1, name='tc13Page5',
              parent=self.Page5, pos=wx.Point(512, 144), size=wx.Size(200, 21),
              style=0, value='')

        
        self.st14Page5 = wx.StaticText(id=-1, label=PList["0614"][1] + ' ' + PList["0614"][2], name='st14Page5', parent=self.Page5, pos=wx.Point(512, 168), style=0)

        self.tc14Page5 = wx.TextCtrl(id=-1, name='tc14Page5',
              parent=self.Page5, pos=wx.Point(512, 184), size=wx.Size(200, 21),
              style=0, value='')


        self.st15Page5 = wx.StaticText(id=-1, label=PList["0616"][1] + ' ' + PList["0616"][2], name='st15Page5', parent=self.Page5, pos=wx.Point(512, 248), style=0)

        self.tc15Page5 = wx.TextCtrl(id=-1, name='tc15Page5',
              parent=self.Page5, pos=wx.Point(512, 264), size=wx.Size(200, 21),
              style=0, value='')


        self.st16Page5 = wx.StaticText(id=-1, label=PList["0617"][1] + ' ' + PList["0617"][2], name='st16Page5', parent=self.Page5, pos=wx.Point(512, 288), style=0)

        self.tc16Page5 = wx.TextCtrl(id=-1, name='tc16Page5',
              parent=self.Page5, pos=wx.Point(512, 304), size=wx.Size(200, 21),
              style=0, value='')


        self.st17Page5 = wx.StaticText(id=-1, label=PList["0618"][1] + ' ' + PList["0618"][2], name='st17Page5', parent=self.Page5, pos=wx.Point(512, 328), style=0)

        self.tc17Page5 = wx.TextCtrl(id=-1, name='tc17Page5',
              parent=self.Page5, pos=wx.Point(512, 344), size=wx.Size(200, 21),
              style=0, value='')


        self.st18Page5 = wx.StaticText(id=-1, label=PList["0619"][1] + ' ' + PList["0619"][2], name='st18Page5', parent=self.Page5, pos=wx.Point(512, 368), style=0)

        self.tc18Page5 = wx.TextCtrl(id=-1, name='tc18Page5',
              parent=self.Page5, pos=wx.Point(512, 384), size=wx.Size(200, 21),
              style=0, value='')        


        self.st19Page5 = wx.StaticText(id=-1, label=PList["0620"][1] + ' ' + PList["0620"][2], name='st19Page5', parent=self.Page5, pos=wx.Point(512, 408), style=0)
        
        self.tc19Page5 = wx.TextCtrl(id=-1, name='tc19Page5',
              parent=self.Page5, pos=wx.Point(512, 424), size=wx.Size(200, 21),
              style=0, value='')



        ####--- End of PAGE 5



        ####----PAGE 6


        

        self.Page6 = wx.Panel(id=-1, name='Page6',
              parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(831, 516), style=0)
        
        self.Page6.Hide()


        self.buttonStoreDataPage6 = wx.Button(id=-1,
              label=PList["X019"][1], name='buttonStoreDataPage6',
              parent=self.Page6, pos=wx.Point(640, 472), size=wx.Size(83, 23),
              style=0)
        

        self.stInfo1Page6 = wx.StaticText(id=-1, label=PList["0901"][1], name='stInfo1Page6', parent=self.Page6, pos=wx.Point(16, 24), style=0)
        self.stInfo1Page6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo2Page6 = wx.StaticText(id=-1, label=PList["X066"][1], name='stInfo2Page6', parent=self.Page6, pos=wx.Point(16, 128), style=0)
        self.stInfo2Page6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo3Page6 = wx.StaticText(id=-1, label=PList["X067"][1], name='stInfo3Page6', parent=self.Page6, pos=wx.Point(72, 152), style=0)
        self.stInfo3Page6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo4Page6 = wx.StaticText(id=-1, label=PList["X068"][1], name='stInfo4Page6', parent=self.Page6, pos=wx.Point(192, 152), style=0)
        self.stInfo4Page6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo5Page6 = wx.StaticText(id=-1, label=PList["X069"][1], name='stInfo5Page6', parent=self.Page6, pos=wx.Point(360, 128), style=0)
        self.stInfo5Page6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo6Page6 = wx.StaticText(id=-1, label=PList["X070"][1], name='stInfo6Page6', parent=self.Page6, pos=wx.Point(360, 152), size=wx.Size(128, 26), style=0)
        self.stInfo6Page6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo7Page6 = wx.StaticText(id=-1, label=PList["X071"][1], name='stInfo7Page6', parent=self.Page6, pos=wx.Point(576, 152), size=wx.Size(128, 26), style=0)
        self.stInfo7Page6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))




        self.st1Page6 = wx.StaticText(id=-1, label=PList["X072"][1], name='st1Page6', parent=self.Page6, pos=wx.Point(24, 48), style=0)        

        self.checkBox1Page6 = wx.CheckBox(id=-1,
              label='', name='checkBox1Page6', parent=self.Page6,
              pos=wx.Point(24, 64), size=wx.Size(24, 16), style=0)
        self.checkBox1Page6.SetValue(False)
        self.checkBox1Page6.SetAutoLayout(True)
        

        self.st2Page6 = wx.StaticText(id=-1, label=PList["X073"][1], name='st2Page6', parent=self.Page6, pos=wx.Point(24, 80), style=0)

        self.checkBox2Page6 = wx.CheckBox(id=-1,
              label='', name='checkBox2Page6', parent=self.Page6,
              pos=wx.Point(24, 96), size=wx.Size(24, 16), style=0)
        self.checkBox2Page6.SetValue(False)
        self.checkBox2Page6.SetAutoLayout(True)
        

        self.st3Page6 = wx.StaticText(id=-1, label=PList["X074"][1], name='st3Page6', parent=self.Page6, pos=wx.Point(290, 48), style=0)

        self.checkBox3Page6 = wx.CheckBox(id=-1,
              label='', name='checkBox3Page6', parent=self.Page6,
              pos=wx.Point(290, 64), size=wx.Size(24, 16), style=0)
        self.checkBox3Page6.SetValue(False)
        self.checkBox3Page6.SetAutoLayout(True)


        self.st4Page6 = wx.StaticText(id=-1, label=PList["X075"][1], name='st4Page6', parent=self.Page6, pos=wx.Point(290, 80), style=0)

        self.checkBox4Page6 = wx.CheckBox(id=-1,
              label='', name='checkBox4Page6', parent=self.Page6,
              pos=wx.Point(290, 96), size=wx.Size(24, 16), style=0)
        self.checkBox4Page6.SetValue(False)
        self.checkBox4Page6.SetAutoLayout(True)



        
        self.st5Page6 = wx.StaticText(id=-1, label=PList["X076"][1], name='st5Page6', parent=self.Page6, pos=wx.Point(608, 48), style=0)

        self.tc1Page6 = wx.TextCtrl(id=-1, name='tc1Page6',
              parent=self.Page6, pos=wx.Point(608, 64), size=wx.Size(168, 48),
              style=wx.TE_MULTILINE, value='')

        
        

        self.st6Page6 = wx.StaticText(id=-1, label=PList["X077"][1] + " " + PList["X077"][2], name='st6Page6', parent=self.Page6, pos=wx.Point(16, 168), style=0)

        self.st7Page6 = wx.StaticText(id=-1, label=PList["X078"][1] + " " + PList["X078"][2], name='st7Page6', parent=self.Page6, pos=wx.Point(16, 208), style=0)

        self.st8Page6 = wx.StaticText(id=-1, label=PList["X079"][1] + " " + PList["X079"][2], name='st8Page6', parent=self.Page6, pos=wx.Point(16, 248), style=0)

        self.st9Page6 = wx.StaticText(id=-1, label=PList["X080"][1] + " " + PList["X080"][2], name='st9Page6', parent=self.Page6, pos=wx.Point(16, 288), style=0)

        self.st10Page6 = wx.StaticText(id=-1, label=PList["X081"][1] + " " + PList["X081"][2], name='st10Page6', parent=self.Page6, pos=wx.Point(16, 328), style=0)

        self.st11Page6 = wx.StaticText(id=-1, label=PList["0914"][1] + " " + PList["0914"][2], name='st11Page6', parent=self.Page6, pos=wx.Point(16, 368), style=0)

        self.st12Page6 = wx.StaticText(id=-1, label=PList["0915"][1] + " " + PList["0915"][2], name='st12Page6', parent=self.Page6, pos=wx.Point(16, 408), style=0)



        self.st13Page6 = wx.StaticText(id=-1, label=PList["0916"][1] + " " + PList["0916"][2], name='st13Page6', parent=self.Page6, pos=wx.Point(16, 456), style=0)

        self.checkBox5Page6 = wx.CheckBox(id=-1,
              label='', name='checkBox5Page6', parent=self.Page6,
              pos=wx.Point(16, 472), size=wx.Size(16, 13), style=0)
        self.checkBox5Page6.SetValue(False)

        

        self.st14Page6 = wx.StaticText(id=-1, label=PList["0921"][1] + " " + PList["0921"][2], name='st14Page6', parent=self.Page6, pos=wx.Point(360, 192), style=0)

        self.st15Page6 = wx.StaticText(id=-1, label=PList["X082"][1] + " " + PList["X082"][2], name='st15Page6', parent=self.Page6, pos=wx.Point(360, 232), style=0)

        self.st16Page6 = wx.StaticText(id=-1, label=PList["0924"][1] + " " + PList["0924"][2], name='st16Page6', parent=self.Page6, pos=wx.Point(360, 272), style=0)

        self.st17Page6 = wx.StaticText(id=-1, label=PList["0925"][1] + " " + PList["0925"][2], name='st17Page6', parent=self.Page6, pos=wx.Point(360, 312), style=0)

        self.st18Page6 = wx.StaticText(id=-1, label=PList["0926"][1] + " " + PList["0926"][2], name='st18Page6', parent=self.Page6, pos=wx.Point(360, 352), style=0)

        self.st19Page6 = wx.StaticText(id=-1, label=PList["0927"][1] + " " + PList["0927"][2], name='st19Page6', parent=self.Page6, pos=wx.Point(360, 392), style=0)

        self.st20Page6 = wx.StaticText(id=-1, label=PList["0928"][1] + " " + PList["0928"][2], name='st20Page6', parent=self.Page6, pos=wx.Point(360, 432), style=0)

        self.st21Page6 = wx.StaticText(id=-1, label=PList["0929"][1] + " " + PList["0929"][2], name='st21Page6', parent=self.Page6, pos=wx.Point(576, 192), style=0)

        self.st22Page6 = wx.StaticText(id=-1, label=PList["0930"][1] + " " + PList["0930"][2], name='st22Page6', parent=self.Page6, pos=wx.Point(576, 232), style=0)
        
        self.st23Page6 = wx.StaticText(id=-1, label=PList["X083"][1] + " " + PList["X083"][2], name='st23Page6', parent=self.Page6, pos=wx.Point(576, 272), style=0)

        self.st24Page6 = wx.StaticText(id=-1, label=PList["0933"][1] + " " + PList["0933"][2], name='st24Page6', parent=self.Page6, pos=wx.Point(576, 312), style=0)

        

        self.tc6_1Page6 = wx.TextCtrl(id=-1,
              name='tc6_1Page6', parent=self.Page6, pos=wx.Point(16, 184),
              size=wx.Size(128, 21), style=0, value='')

        self.tc6_2Page6 = wx.TextCtrl(id=-1,
              name='tc6_2Page6', parent=self.Page6, pos=wx.Point(152, 184),
              size=wx.Size(128, 21), style=0, value='')

        self.tc7_1Page6 = wx.TextCtrl(id=-1,
              name='tc7_1Page6', parent=self.Page6, pos=wx.Point(16, 224),
              size=wx.Size(128, 21), style=0, value='')
        
        self.tc7_2Page6 = wx.TextCtrl(id=-1,
              name='tc7_2Page6', parent=self.Page6, pos=wx.Point(152, 224),
              size=wx.Size(128, 21), style=0, value='')

        self.tc8_1Page6 = wx.TextCtrl(id=-1,
              name='tc8_1Page6', parent=self.Page6, pos=wx.Point(16, 264),
              size=wx.Size(128, 21), style=0, value='')

        self.tc8_2Page6 = wx.TextCtrl(id=-1,
              name='tc8_2Page6', parent=self.Page6, pos=wx.Point(152, 264),
              size=wx.Size(128, 21), style=0, value='')

        self.tc9_1Page6 = wx.TextCtrl(id=-1,
              name='tc9_1Page6', parent=self.Page6, pos=wx.Point(16, 304),
              size=wx.Size(128, 21), style=0, value='')

        self.tc9_2Page6 = wx.TextCtrl(id=-1,
              name='tc9_2Page6', parent=self.Page6, pos=wx.Point(152, 304),
              size=wx.Size(128, 21), style=0, value='')

        self.tc10_1Page6 = wx.TextCtrl(id=-1,
              name='tc10_1Page6', parent=self.Page6, pos=wx.Point(16, 344),
              size=wx.Size(128, 21), style=0, value='')

        self.tc10_2Page6 = wx.TextCtrl(id=-1,
              name='tc10_2Page6', parent=self.Page6, pos=wx.Point(152, 344),
              size=wx.Size(128, 21), style=0, value='')

        self.tc11Page6 = wx.TextCtrl(id=-1, name='tc11Page6',
              parent=self.Page6, pos=wx.Point(16, 384), size=wx.Size(128, 21),
              style=0, value='')

        self.tc12Page6 = wx.TextCtrl(id=-1, name='tc12Page6',
              parent=self.Page6, pos=wx.Point(16, 424), size=wx.Size(128, 21),
              style=0, value='')



        self.tc14Page6 = wx.TextCtrl(id=-1, name='tc14Page6',
              parent=self.Page6, pos=wx.Point(360, 208), size=wx.Size(150, 21),
              style=0, value='')



        self.tc15_1Page6 = wx.TextCtrl(id=-1, name='tc15_1Page6',
              parent=self.Page6, pos=wx.Point(360, 248), size=wx.Size(72, 21), style=0, value='')
        self.tc15_2Page6 = wx.TextCtrl(id=-1, name='tc15_2Page6',
              parent=self.Page6, pos=wx.Point(438, 248), size=wx.Size(72, 21), style=0, value='')


        self.tc16Page6 = wx.TextCtrl(id=-1, name='tc16Page6',
              parent=self.Page6, pos=wx.Point(360, 288), size=wx.Size(150, 21),
              style=0, value='')



        self.tc17Page6 = wx.TextCtrl(id=-1, name='tc17Page6',
              parent=self.Page6, pos=wx.Point(360, 328), size=wx.Size(150, 21),
              style=0, value='')



        self.tc18Page6 = wx.TextCtrl(id=-1, name='tc18Page6',
              parent=self.Page6, pos=wx.Point(360, 368), size=wx.Size(150, 21),
              style=0, value='')


        self.tc19Page6 = wx.TextCtrl(id=-1, name='tc19Page6',
              parent=self.Page6, pos=wx.Point(360, 408), size=wx.Size(150, 21),
              style=0, value='')



        self.tc20Page6 = wx.TextCtrl(id=-1, name='tc20Page6',
              parent=self.Page6, pos=wx.Point(360, 448), size=wx.Size(150, 21),
              style=0, value='')



        self.tc21Page6 = wx.TextCtrl(id=-1, name='tc21Page6',
              parent=self.Page6, pos=wx.Point(576, 208), size=wx.Size(150, 21),
              style=0, value='')


        self.tc22Page6 = wx.TextCtrl(id=-1, name='tc22Page6',
              parent=self.Page6, pos=wx.Point(576, 248), size=wx.Size(150, 21),
              style=0, value='')


        self.tc23_1Page6 = wx.TextCtrl(id=-1,
              name='tc23_1Page6', parent=self.Page6, pos=wx.Point(576, 288),
              size=wx.Size(72, 21), style=0, value='')

        self.tc23_2Page6 = wx.TextCtrl(id=-1,
              name='tc23_2Page6', parent=self.Page6, pos=wx.Point(656, 288),
              size=wx.Size(72, 21), style=0, value='')



        self.tc24Page6 = wx.TextCtrl(id=-1, name='tc24Page6',
              parent=self.Page6, pos=wx.Point(576, 328), size=wx.Size(150, 21),
              style=0, value='')




        ####--- End of PAGE 6



        ####----PAGE 7

        self.Page7 = wx.Panel(id=-1, name='Page7',
              parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
        
        self.Page7.Hide()

        self.stInfo1Page7 = wx.StaticText(id=-1,
              label=PList["X084"][1], name='stInfo1Page7', parent=self.Page7,
              pos=wx.Point(24, 24), size=wx.Size(64, 13), style=0)
        self.stInfo1Page7.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo2Page7 = wx.StaticText(id=-1,
              label=PList["X085"][1], name='stInfo2Page7',
              parent=self.Page7, pos=wx.Point(272, 24), size=wx.Size(157, 13),
              style=0)
        self.stInfo2Page7.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        
        
        self.listBoxBuildingListPage7 = wx.ListBox(choices=[], id=-1,
              name='listBoxBuildingListPage7', parent=self.Page7,
              pos=wx.Point(24, 40), size=wx.Size(200, 216), style=0)


        self.buttonClearPage7 = wx.Button(id=-1,
              label=PList["X028"][1], name='buttonClearPage7', parent=self.Page7,
              pos=wx.Point(272, 464), size=wx.Size(120, 16), style=0)

        self.buttonDeleteBuildingPage7 = wx.Button(id=-1,
              label=PList["X086"][1], name='buttonDeleteBuildingPage7',
              parent=self.Page7, pos=wx.Point(128, 264), size=wx.Size(99, 16),
              style=0)

        self.buttonAddBuildingPage7 = wx.Button(id=-1,
              label=PList["X087"][1], name='buttonAddBuildingPage7',
              parent=self.Page7, pos=wx.Point(584, 464), size=wx.Size(123, 16),
              style=0)
        

        

        self.st1Page7 = wx.StaticText(id=-1, label=PList["0802"][1] + " " + PList["0802"][2], name='st1Page7', parent=self.Page7, pos=wx.Point(272, 48), style=0)
        
        self.tc1Page7 = wx.TextCtrl(id=-1, name='tc1Page7',
              parent=self.Page7, pos=wx.Point(272, 64), size=wx.Size(200, 21),
              style=0, value='')



        self.st2Page7 = wx.StaticText(id=-1, label=PList["0803"][1] + " " + PList["0803"][2], name='st2Page7', parent=self.Page7, pos=wx.Point(272, 88), style=0)

        self.tc2Page7 = wx.TextCtrl(id=-1, name='tc2Page7',
              parent=self.Page7, pos=wx.Point(272, 104), size=wx.Size(200, 21),
              style=0, value='')



        self.st3Page7 = wx.StaticText(id=-1, label=PList["0804"][1] + " " + PList["0804"][2], name='st3Page7', parent=self.Page7, pos=wx.Point(272, 128), style=0)

        self.tc3Page7 = wx.TextCtrl(id=-1, name='tc3Page7',
              parent=self.Page7, pos=wx.Point(272, 144), size=wx.Size(200, 21),
              style=0, value='')



        self.st4Page7 = wx.StaticText(id=-1, label=PList["0805"][1] + " " + PList["0805"][2], name='st4Page7', parent=self.Page7, pos=wx.Point(272, 168), style=0)

        self.tc4Page7 = wx.TextCtrl(id=-1, name='tc4Page7',
              parent=self.Page7, pos=wx.Point(272, 184), size=wx.Size(200, 21),
              style=0, value='')        


        
        self.st5Page7 = wx.StaticText(id=-1, label=PList["0807"][1] + " " + PList["0807"][2], name='st5Page7', parent=self.Page7, pos=wx.Point(272, 208), style=0)

        self.tc5Page7 = wx.TextCtrl(id=-1, name='tc5Page7',
              parent=self.Page7, pos=wx.Point(272, 224), size=wx.Size(200, 21),
              style=0, value='')





        self.st6Page7 = wx.StaticText(id=-1, label=PList["0808"][1] + " " + PList["0808"][2], name='st6Page7', parent=self.Page7, pos=wx.Point(272, 248), style=0)

        self.tc6Page7 = wx.TextCtrl(id=-1, name='tc6Page7',
              parent=self.Page7, pos=wx.Point(272, 264), size=wx.Size(200, 21),
              style=0, value='')




        self.st7Page7 = wx.StaticText(id=-1, label=PList["0809"][1] + " " + PList["0809"][2], name='st7Page7', parent=self.Page7, pos=wx.Point(272, 288), style=0)

        self.tc7Page7 = wx.TextCtrl(id=-1, name='tc7Page7',
              parent=self.Page7, pos=wx.Point(272, 304), size=wx.Size(200, 21),
              style=0, value='')




        self.st8Page7 = wx.StaticText(id=-1, label=PList["0810"][1] + " " + PList["0810"][2], name='st8Page7', parent=self.Page7, pos=wx.Point(272, 328), style=0)

        self.tc8Page7 = wx.TextCtrl(id=-1, name='tc8Page7',
              parent=self.Page7, pos=wx.Point(272, 344), size=wx.Size(200, 21),
              style=0, value='')




        self.st9Page7 = wx.StaticText(id=-1, label=PList["0811"][1] + " " + PList["0811"][2], name='st9Page7', parent=self.Page7, pos=wx.Point(272, 368), style=0)

        self.tc9Page7 = wx.TextCtrl(id=-1, name='tc9Page7',
              parent=self.Page7, pos=wx.Point(272, 384), size=wx.Size(200, 21),
              style=0, value='')

        

        self.st10Page7 = wx.StaticText(id=-1, label=PList["0812"][1] + " " + PList["0812"][2], name='st10Page7', parent=self.Page7, pos=wx.Point(272, 408), style=0)

        self.tc10Page7 = wx.TextCtrl(id=-1, name='tc10Page7',
              parent=self.Page7, pos=wx.Point(272, 424), size=wx.Size(200, 21),
              style=0, value='')




        self.st11Page7 = wx.StaticText(id=-1, label=PList["0813"][1] + " " + PList["0813"][2], name='st11Page7', parent=self.Page7, pos=wx.Point(512, 48), style=0)

        self.tc11Page7 = wx.TextCtrl(id=-1, name='tc11Page7',
              parent=self.Page7, pos=wx.Point(512, 64), size=wx.Size(200, 21),
              style=0, value='')




        self.st12Page7 = wx.StaticText(id=-1, label=PList["0814"][1] + " " + PList["0814"][2], name='st12Page7', parent=self.Page7, pos=wx.Point(512, 88), style=0)

        self.tc12_1Page7 = wx.TextCtrl(id=-1,
              name='tc12_1Page7', parent=self.Page7, pos=wx.Point(512, 104),
              size=wx.Size(96, 21), style=0, value='')

        self.tc12_2Page7 = wx.TextCtrl(id=-1,
              name='tc12_2Page7', parent=self.Page7, pos=wx.Point(616, 104),
              size=wx.Size(96, 21), style=0, value='')



        
        self.st13Page7 = wx.StaticText(id=-1, label=PList["0815"][1] + " " + PList["0815"][2], name='st13Page7', parent=self.Page7, pos=wx.Point(512, 128), style=0)

        self.tc13_1Page7 = wx.TextCtrl(id=-1,
              name='tc13_1Page7', parent=self.Page7, pos=wx.Point(512, 144),
              size=wx.Size(96, 21), style=0, value='')      

        self.tc13_2Page7 = wx.TextCtrl(id=-1,
              name='tc13_2Page7', parent=self.Page7, pos=wx.Point(616, 144),
              size=wx.Size(96, 21), style=0, value='')




        self.st14Page7 = wx.StaticText(id=-1, label=PList["0816"][1] + " " + PList["0816"][2], name='st14Page7', parent=self.Page7, pos=wx.Point(512, 168), style=0)

        self.tc14_1Page7 = wx.TextCtrl(id=-1,
              name='tc14_1Page7', parent=self.Page7, pos=wx.Point(512, 184),
              size=wx.Size(96, 21), style=0, value='')        

        self.tc14_2Page7 = wx.TextCtrl(id=-1,
              name='tc14_2Page7', parent=self.Page7, pos=wx.Point(616, 184),
              size=wx.Size(96, 21), style=0, value='')





        


        ####--- End of PAGE 7









        ####----PAGE 8


        

        self.Page8 = wx.Panel(id=-1, name='Page8',
              parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
        
        self.Page8.Hide()
        

        self.buttonStoreDataPage8 = wx.Button(id=-1,
              label=PList["X019"][1], name='buttonStoreDataPage8',
              parent=self.Page8, pos=wx.Point(664, 544), size=wx.Size(75, 23),
              style=0)

        
        self.stInfo1Page8 = wx.StaticText(id=-1, label=PList["1000"][1], name='stInfo1Page8', parent=self.Page8, pos=wx.Point(8, 24), style=0)
        self.stInfo1Page8.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        #self.stInfo2Page8 = wx.StaticText(id=-1, label=PList["X088"][1], name='stInfo2Page8', parent=self.Page8, pos=wx.Point(264, 64), style=0)

        #self.stInfo3Page8 = wx.StaticText(id=-1, label=PList["X089"][1], name='stInfo3Page8', parent=self.Page8, pos=wx.Point(264, 120), style=0)

        self.stInfo4_1Page8 = wx.StaticText(id=-1, label=PList["X090"][1], name='stInfo4_1Page8', parent=self.Page8, pos=wx.Point(392, 56), style=0)
        
        self.stInfo4_2Page8 = wx.StaticText(id=-1, label=PList["X091"][1], name='stInfo4_2Page8', parent=self.Page8, pos=wx.Point(600, 56), style=0)


        self.stInfo5Page8 = wx.StaticText(id=-1, label=PList["X092"][1], name='stInfo5Page8', parent=self.Page8, pos=wx.Point(8, 272), style=0)
        self.stInfo5Page8.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo6Page8 = wx.StaticText(id=-1, label=PList["X093"][1], name='stInfo6Page8', parent=self.Page8, pos=wx.Point(16, 328), style=0)

        self.stInfo7Page8 = wx.StaticText(id=-1, label=PList["X094"][1], name='stInfo7Page8', parent=self.Page8, pos=wx.Point(16, 352), style=0)

        self.stInfo8Page8 = wx.StaticText(id=-1, label=PList["X095"][1], name='stInfo8Page8', parent=self.Page8, pos=wx.Point(16, 376), style=0)

        self.stInfo9Page8 = wx.StaticText(id=-1, label=PList["X096"][1], name='stInfo9Page8', parent=self.Page8, pos=wx.Point(16, 400), style=0)

        self.stInfo10Page8 = wx.StaticText(id=-1, label=PList["X097"][1], name='stInfo10Page8', parent=self.Page8, pos=wx.Point(16, 424), style=0)

        self.stInfo11Page8 = wx.StaticText(id=-1, label=PList["X098"][1], name='stInfo11Page8', parent=self.Page8, pos=wx.Point(264, 288), style=0)
        self.stInfo11Page8.SetMaxSize(wx.Size(88, 40))

        self.stInfo12Page8 = wx.StaticText(id=-1, label=PList["X099"][1], name='stInfo12Page8', parent=self.Page8, pos=wx.Point(368, 288), style=0)
        self.stInfo12Page8.SetMaxSize(wx.Size(88, 40))

        self.stInfo13Page8 = wx.StaticText(id=-1, label=PList["X100"][1], name='stInfo13Page8', parent=self.Page8, pos=wx.Point(464, 288), style=0)
        self.stInfo13Page8.SetMaxSize(wx.Size(88, 40))

        self.stInfo14Page8 = wx.StaticText(id=-1, label=PList["X101"][1], name='stInfo14Page8', parent=self.Page8, pos=wx.Point(560, 288), style=0)
        self.stInfo14Page8.SetMaxSize(wx.Size(88, 40))

        self.stInfo15Page8 = wx.StaticText(id=-1, label=PList["X102"][1], name='stInfo15Page8', parent=self.Page8, pos=wx.Point(8, 472), style=0)
        self.stInfo15Page8.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))




    

        self.st1Page8 = wx.StaticText(id=-1, label=PList["1001"][1] + ' ' + PList["1001"][2], name='st1Page8', parent=self.Page8, pos=wx.Point(16, 48), style=0)

        self.tc1Page8 = wx.TextCtrl(id=-1, name='tc1Page8',
              parent=self.Page8, pos=wx.Point(16, 64), size=wx.Size(100, 21),
              style=0, value='')



        self.st2Page8 = wx.StaticText(id=-1, label=PList["1002"][1] + ' ' + PList["1002"][2], name='st2Page8', parent=self.Page8, pos=wx.Point(16, 88), style=0)

        self.tc2Page8 = wx.TextCtrl(id=-1, name='tc2Page8',
              parent=self.Page8, pos=wx.Point(16, 104), size=wx.Size(100, 21),
              style=0, value='')

        

        self.st3Page8 = wx.StaticText(id=-1, label=PList["1003"][1] + ' ' + PList["1003"][2], name='st3Page8', parent=self.Page8, pos=wx.Point(16, 128), style=0)

        self.tc3Page8 = wx.TextCtrl(id=-1, name='tc3Page8',
              parent=self.Page8, pos=wx.Point(16, 144), size=wx.Size(100, 21),
              style=0, value='')



        self.st4Page8 = wx.StaticText(id=-1, label=PList["1004"][1] + ' ' + PList["1004"][2], name='st4Page8', parent=self.Page8, pos=wx.Point(16, 168), style=0)

        self.tc4Page8 = wx.TextCtrl(id=-1, name='tc4Page8',
              parent=self.Page8, pos=wx.Point(16, 184), size=wx.Size(100, 21),
              style=0, value='')



        self.st5Page8 = wx.StaticText(id=-1, label=PList["1005"][1] + ' ' + PList["1005"][2], name='st5Page8', parent=self.Page8, pos=wx.Point(16, 208), style=0)

        self.tc5Page8 = wx.TextCtrl(id=-1, name='tc5Page8',
              parent=self.Page8, pos=wx.Point(16, 224), size=wx.Size(100, 21),
              style=0, value='')





        


        self.tc6_1Page8 = wx.TextCtrl(id=-1,
              name='tc6_1Page8', parent=self.Page8, pos=wx.Point(392, 72),
              size=wx.Size(200, 21), style=0, value='')

        self.tc6_2Page8 = wx.TextCtrl(id=-1,
              name='tc6_2Page8', parent=self.Page8, pos=wx.Point(600, 72),
              size=wx.Size(150, 21), style=0, value='')


        self.tc7_1Page8 = wx.TextCtrl(id=-1,
              name='tc7_1Page8', parent=self.Page8, pos=wx.Point(392, 96),
              size=wx.Size(200, 21), style=0, value='')

        self.tc7_2Page8 = wx.TextCtrl(id=-1,
              name='tc7_2Page8', parent=self.Page8, pos=wx.Point(600, 96),
              size=wx.Size(150, 21), style=0, value='')
        

        self.tc8_1Page8 = wx.TextCtrl(id=-1,
              name='tc8_1Page8', parent=self.Page8, pos=wx.Point(392, 120),
              size=wx.Size(200, 21), style=0, value='')

        self.tc8_2Page8 = wx.TextCtrl(id=-1,
              name='tc8_2Page8', parent=self.Page8, pos=wx.Point(600, 120),
              size=wx.Size(150, 21), style=0, value='')
        

        self.tc9_1Page8 = wx.TextCtrl(id=-1,
              name='tc9_1Page8', parent=self.Page8, pos=wx.Point(392, 144),
              size=wx.Size(200, 21), style=0, value='')
        
        self.tc9_2Page8 = wx.TextCtrl(id=-1,
              name='tc9_2Page8', parent=self.Page8, pos=wx.Point(600, 144),
              size=wx.Size(150, 21), style=0, value='')








        self.tc10_1Page8 = wx.TextCtrl(id=-1,
              name='tc10_1Page8', parent=self.Page8, pos=wx.Point(248, 328),
              size=wx.Size(100, 21), style=0, value='')        

        self.tc10_2Page8 = wx.TextCtrl(id=-1,
              name='tc10_2Page8', parent=self.Page8, pos=wx.Point(352, 328),
              size=wx.Size(100, 21), style=0, value='')

        self.tc10_3Page8 = wx.TextCtrl(id=-1,
              name='tc10_3Page8', parent=self.Page8, pos=wx.Point(456, 328),
              size=wx.Size(100, 21), style=0, value='')

        self.tc10_4Page8 = wx.TextCtrl(id=-1,
              name='tc10_4Page8', parent=self.Page8, pos=wx.Point(560, 328),
              size=wx.Size(100, 21), style=0, value='')




        self.tc11_1Page8 = wx.TextCtrl(id=-1,
              name='tc11_1Page8', parent=self.Page8, pos=wx.Point(248, 352),
              size=wx.Size(100, 21), style=0, value='')

        self.tc11_2Page8 = wx.TextCtrl(id=-1,
              name='tc11_2Page8', parent=self.Page8, pos=wx.Point(352, 352),
              size=wx.Size(100, 21), style=0, value='')        

        self.tc11_3Page8 = wx.TextCtrl(id=-1,
              name='tc11_3Page8', parent=self.Page8, pos=wx.Point(456, 352),
              size=wx.Size(100, 21), style=0, value='')
        
        self.tc11_4Page8 = wx.TextCtrl(id=-1,
              name='tc11_4Page8', parent=self.Page8, pos=wx.Point(560, 352),
              size=wx.Size(100, 21), style=0, value='')




        self.tc12_1Page8 = wx.TextCtrl(id=-1,
              name='tc12_1Page8', parent=self.Page8, pos=wx.Point(248, 376),
              size=wx.Size(100, 21), style=0, value='')

        self.tc12_2Page8 = wx.TextCtrl(id=-1,
              name='tc12_2Page8', parent=self.Page8, pos=wx.Point(352, 376),
              size=wx.Size(100, 21), style=0, value='')

        self.tc12_3Page8 = wx.TextCtrl(id=-1,
              name='tc12_3Page8', parent=self.Page8, pos=wx.Point(456, 376),
              size=wx.Size(100, 21), style=0, value='')

        self.tc12_4Page8 = wx.TextCtrl(id=-1,
              name='tc12_4Page8', parent=self.Page8, pos=wx.Point(560, 376),
              size=wx.Size(100, 21), style=0, value='')





        self.tc13_1Page8 = wx.TextCtrl(id=-1,
              name='tc13_1Page8', parent=self.Page8, pos=wx.Point(248, 400),
              size=wx.Size(100, 21), style=0, value='')

        self.tc13_2Page8 = wx.TextCtrl(id=-1,
              name='tc13_2Page8', parent=self.Page8, pos=wx.Point(352, 400),
              size=wx.Size(100, 21), style=0, value='')

        self.tc13_3Page8 = wx.TextCtrl(id=-1,
              name='tc13_3Page8', parent=self.Page8, pos=wx.Point(456, 400),
              size=wx.Size(100, 21), style=0, value='')

        self.tc13_4Page8 = wx.TextCtrl(id=-1,
              name='tc13_4Page8', parent=self.Page8, pos=wx.Point(560, 400),
              size=wx.Size(100, 21), style=0, value='')




        self.tc14_1Page8 = wx.TextCtrl(id=-1,
              name='tc14_1Page8', parent=self.Page8, pos=wx.Point(248, 424),
              size=wx.Size(100, 21), style=0, value='')

        self.tc14_2Page8 = wx.TextCtrl(id=-1,
              name='tc14_2Page8', parent=self.Page8, pos=wx.Point(352, 424),
              size=wx.Size(100, 21), style=0, value='')

        self.tc14_3Page8 = wx.TextCtrl(id=-1,
              name='tc14_3Page8', parent=self.Page8, pos=wx.Point(456, 424),
              size=wx.Size(100, 21), style=0, value='')        

        self.tc14_4Page8 = wx.TextCtrl(id=-1,
              name='tc14_4Page8', parent=self.Page8, pos=wx.Point(560, 424),
              size=wx.Size(100, 21), style=0, value='')



        self.st6Page8 = wx.StaticText(id=-1, label=PList["1028"][1] + ' ' + PList["1028"][2], name='st6Page8', parent=self.Page8, pos=wx.Point(16, 496), style=0)

        self.checkBox6Page8 = wx.CheckBox(id=-1,
              label='', name='checkBox6Page8', parent=self.Page8,
              pos=wx.Point(24, 512), size=wx.Size(16, 13), style=0)
        self.checkBox6Page8.SetValue(False)

        self.st7Page8 = wx.StaticText(id=-1, label=PList["1029"][1] + ' ' + PList["1029"][2], name='st7Page8', parent=self.Page8, pos=wx.Point(16, 536), style=0)

        self.checkBox7Page8 = wx.CheckBox(id=-1,
              label='', name='checkBox7Page8', parent=self.Page8,
              pos=wx.Point(24, 552), size=wx.Size(16, 13), style=0)
        self.checkBox7Page8.SetValue(False)


        ####--- End of PAGE 8






        ####----PAGE pageDataCheck
        self.pageDataCheck = wx.Panel(id=-1, name='pageDataCheck', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageDataCheck.Hide()
        ####--- End of pageDataCheck

###HS2008-03-07: Page substituted by PanelCCheck

        ####----PAGE pageDataCheckPage1
        self.pageDataCheckPage1 = PanelCC(id=-1, name='pageDataCheckPage1', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0, sql = Status.SQL, db = Status.DB) #TS 2008-03-13
        #self.pageDataCheckPage1 = PanelCC(id=-1, name='pageDataCheckPage1', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0, sql = MySql, db = DB)
        self.pageDataCheckPage1.Hide()
        ####--- End of pageDataCheckPage1



        ####----PAGE pageDataCheckPage2
        self.pageDataCheckPage2 = wx.Panel(id=-1, name='pageDataCheckPage2', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageDataCheckPage2.Hide()
        ####--- End of pageDataCheckPage2



        ####----PAGE pageStatistics
        self.pageStatistics = wx.Panel(id=-1, name='pageStatistics', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageStatistics.Hide()
        ####--- End of pageStatistics


        ####----PAGE pageStatisticPages

        #TS2008-03-23 changed this, added panels EA1-EA6, EM1

        #self.pageStatisticPages = wx.Panel(id=-1, name='pageStatisticPages', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        #self.pageStatisticPages.Hide()
        self.panelEA1 = PanelEA1(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA1')
        self.panelEA1.Hide()

        self.panelEA2 = PanelEA2(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA2')
        self.panelEA2.Hide()
        
        self.panelEA3 = PanelEA3(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA3')
        self.panelEA3.Hide()
        
        self.panelEA4 = PanelEA4(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA4')
        self.panelEA4.Hide()
        
        self.panelEA5 = PanelEA5(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA5')
        self.panelEA5.Hide()

        self.panelEA6 = PanelEA6(parent=self.leftpanel2, id=-1, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, name='pageEA6')
        self.panelEA6.Hide()

        self.panelEM1 = PanelEM1(id=-1, name='pageEM1', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL)
        self.panelEM1.Hide()

        ####--- End of pageStatisticPages


        ####----PAGE pageBenchmarkCheck
        self.pageBenchmarkCheck = wx.Panel(id=-1, name='pageBenchmarkCheck', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageBenchmarkCheck.Hide()
        ####--- End of pageBenchmarkCheck



        ####----PAGE pageHeatRecoveryTargets
        #self.pageHeatRecoveryTargets = wx.Panel(id=-1, name='pageHeatRecoveryTargets', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        #self.pageHeatRecoveryTargets.Hide()
        ####--- End of pageHeatRecoveryTargets



        ####----PAGE pageOptimisationProposals
        self.pageOptimisationProposals = wx.Panel(id=-1, name='pageOptimisationProposals', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageOptimisationProposals.Hide()
        ####--- End of pageOptimisationProposals

###HS2008-03-07: Heat Pump page definition and lay-out moved to file

        ####--- Page HeatPump
        self.pageHeatPump = PanelHP(id=-1, name='pageHeatPump', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL, sql = Status.SQL, db = Status.DB)
        self.pageHeatPump.Hide()
#        self.drawPageHeatPump()
        ####--- End op pageHeatPump

        ####--- Page Boilers
        self.pageBB = PanelBB(id=-1, name='pageBB', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL)
        self.pageBB.Hide()
        ####--- End op pageHeatPump

#HS2008-03-12: added
        ####--- Panel Energy
        self.panelEnergy = PanelEnergy(id=-1, name='panelEnergy', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=wx.TAB_TRAVERSAL)
        self.panelEnergy.Hide()
        ####--- End op panelEnergy

        ####----PAGE pageFinalReport
        self.pageFinalReport = wx.Panel(id=-1, name='pageFinalReport', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageFinalReport.Hide()
        ####--- End of pageFinalReport


        ####----PAGE pageDataCheck
        self.pageDataCheck = wx.Panel(id=-1, name='pageDataCheck', parent=self.leftpanel2, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)        
        self.pageDataCheck.Hide()
        ####--- End of pageDataCheck


        

        

#==============================================================================
#--- Eventhandlers Application
#==============================================================================

#------------------------------------------------------------------------------		
#--- Eventhandlers Menu
#------------------------------------------------------------------------------		

    def OnMenuOpenProject(self, event):
        self.tree.SelectItem(self.qPage0, select=True)

    def OnMenuExit(self, event):
        wx.Exit()
    

    def OnMenuEditDBBenchmark(self, event):
        frameEditDBBenchmark = DBEditFrame.wxFrame(None, "Edit DBBenchmark", Status.DB.dbbenchmark, Status.SQL)
        frameEditDBBenchmark.Show()
    def OnMenuEditDBNaceCode(self, event):
        frameEditDBNaceCode = DBEditFrame.wxFrame(None, "Edit DBNaceCode", Status.DB.dbnacecode, Status.SQL)
        frameEditDBNaceCode.Show()
    def OnMenuEditDBUnitOperation(self, event):
        frameEditDBUnitOperation = DBEditFrame.wxFrame(None, "Edit DBUnitOperation", Status.DB.dbunitoperation, Status.SQL)
        frameEditDBUnitOperation.Show()
    def OnMenuEditDBCHP(self, event):
        frameEditDBCHP = DBEditFrame.wxFrame(None, "Edit DBCHP", Status.DB.dbchp, Status.SQL)
        frameEditDBCHP.Show()
    def OnMenuEditDBHeatPump(self, event):
        frameEditDBHeatPump = DBEditFrame.wxFrame(None, "Edit DBHeatPump", Status.DB.dbheatpump, Status.SQL)
        frameEditDBHeatPump.Show()
    def OnMenuEditDBFluid(self, event):
        frameEditDBFluid = DBEditFrame.wxFrame(None, "Edit DBFluid", Status.DB.dbfluid, Status.SQL)
        frameEditDBFluid.Show()
    def OnMenuEditDBFuel(self, event):
        frameEditDBFuel = DBEditFrame.wxFrame(None, "Edit DBFuel", Status.DB.dbfuel, Status.SQL)
        frameEditDBFuel.Show()
    def OnMenuEditDBBoiler(self, event):
        frameEditDBBoiler = DBEditFrame.wxFrame(None, "Edit DBBoiler", Status.DB.dbboiler, Status.SQL)
        frameEditDBBoiler.Show()
    def OnMenuEditDBSolarEquip(self, event):
        frameEditDBSolarEquip = DBEditFrame.wxFrame(None, "Edit DBSolarEquip", Status.DB.dbsolarequip, Status.SQL)
        frameEditDBSolarEquip.Show()
    def OnMenuEditDBChiller(self, event):
        frameEditDBChiller = DBEditFrame.wxFrame(None, "Edit DBChiller", Status.DB.dbchiller, Status.SQL)
        frameEditDBChiller.Show() 


       

    def OnMenuPreferences(self, event):
        framePreferences = PreferencesFrame.wxFrame(None)
        framePreferences.Show()
        #event.Skip()
        
#------------------------------------------------------------------------------		
#--- Eventhandlers Tree
#------------------------------------------------------------------------------		
        
    def OnTreeSelChanged(self, event):
        global qPageSize
        self.item = event.GetItem()
        select = self.tree.GetItemText(self.item)

        #if self.item:
        #    str1 = "Selected item = %s\n" % select
        #    self.help.SetValue(str1)

        #PageTitle
        if select == "Einstein":
            self.hidePages()
            self.pageTitle.Show()
        #Page0
        elif select == PList["X018"][1]:
            self.hidePages()
            self.Page0.Show()
            self.help.SetValue(PList["0101"][1])
            self.getQuestionnaireList()
        #Page1
        elif select == PList["X010"][1]:
            self.hidePages()
            self.Page1.Show()
            self.help.SetValue(PList["0101"][1])
            self.clearPage1()
            self.fillChoiceOfNaceCodePage1()
            if self.activeQid <> 0: self.fillPage("Page1")
        #Page2    
        elif select == PList["X011"][1]:
            self.hidePages()
            self.Page2.Show()
            self.help.SetValue(PList["0102"][1])
            self.clearPage2()
            self.fillChoiceOfDBFuelTypePage2()
            if self.activeQid <> 0: self.fillPage("Page2")
        #Page3
        elif select == PList["X012"][1]:
            self.hidePages()
            self.Page3.Show()
            self.help.SetValue(PList["0102"][1])
            self.fillChoiceOfDBUnitOperationPage3()
            self.fillChoiceOfPMDBFluidPage3()
            self.fillChoiceOfSMDBFluidPage3()
            self.clearPage3()
            if self.activeQid <> 0: self.fillPage("Page3")
            
        #Page4
        elif select == PList["X013"][1]:
            self.hidePages()
            self.Page4.Show()
            self.help.SetValue(PList["0102"][1])
            self.fillChoiceOfDBFuelPage4()
            self.clearPage4()
            if self.activeQid <> 0: self.fillPage("Page4")
        #Page5
        elif select == PList["X014"][1]:
            self.hidePages()
            self.Page5.Show()
            self.help.SetValue(PList["0102"][1])
            self.clearPage5()
            self.fillchoiceOfEquipmentPage5()
            if self.activeQid <> 0: self.fillPage("Page5")
        #Page6
        elif select == PList["X015"][1]:
            self.hidePages()
            self.Page6.Show()
            self.help.SetValue(PList["0102"][1])
            self.clearPage6()
            if self.activeQid <> 0: self.fillPage("Page6")
        #Page7
        elif select == PList["X016"][1]:
            self.hidePages()
            self.Page7.Show()
            self.help.SetValue(PList["0102"][1])
            self.clearPage7()
            if self.activeQid <> 0: self.fillPage("Page7")
        #Page8
        elif select == PList["X017"][1]:
            self.hidePages()
            self.Page8.Show()
            self.help.SetValue(PList["0102"][1])
            self.clearPage8()
            if self.activeQid <> 0: self.fillPage("Page8")
        #qDataCheck
        elif select == PList["X133"][1]:
            self.hidePages()
            self.pageDataCheck.Show()        
        #qDataCheckPage1
        elif select == PList["X134"][1]:
            self.hidePages()
            self.pageDataCheckPage1.Show()        
        #qDataCheckPage2
        elif select == PList["X135"][1]:
            self.hidePages()
            self.pageDataCheckPage2.Show()
        #qStatistics
        elif select == PList["X136"][1]:
            self.hidePages()
            self.pageStatistics.Show()
        #qStatisticYPage1 'Primary energy - Yearly'
        elif select == PList["X137"][1]:
            self.hidePages()
            self.panelEA1.Show()
        #qStatisticYPage2 'Final energy by fuels - Yearly'
        elif select == PList["X138"][1]:
            self.hidePages()
            self.panelEA2.Show()
        #qStatisticYPage3 'Final energy by equipment - Yearly'
        elif select == PList["X139"][1]:
            self.hidePages()
            self.panelEA3.Show()
        #qStatisticYPage4 'Process heat - Yearly'
        elif select == PList["X140"][1]:
            self.hidePages()
            self.panelEA4.Show()
        #qStatisticYPage5 'Energy intensity - Yearly'
        elif select == PList["X141"][1]:
            self.hidePages()
            self.panelEA5.Show()
        #qStatisticYPage6 'Production of CO2 - Yearly'
        elif select == PList["X142"][1]:
            self.hidePages()
            self.panelEA6.Show()
        #qStatisticMPage1 'Energy performance - Monthly'
        elif select == 'Monthly demand':
            self.hidePages()
            self.panelEM1.Show()
        #
        #
        #qBenchmarkCheck
        elif select == PList["X143"][1]:
            self.hidePages()
            self.pageBenchmarkCheck.Show()
        #qOptimisationProposals
        elif select == PList["X145"][1]:
            self.hidePages()
            self.pageOptimisationProposals.Show()
        #qFinalReport
        elif select == PList["X147"][1]:
            self.hidePages()
            self.pageFinalReport.Show()
        #qFinalReportPage1
        elif select == PList["X148"][1]:
            self.hidePages()
            self.pageFinalReport.Show()
        #qFinalReportPage2
        elif select == PList["X149"][1]:
            self.hidePages()
            self.pageFinalReport.Show()
        #qPrintReport
        elif select == PList["X150"][1]:
            self.hidePages()
            self.pageFinalReport.Show()
        #pageHeatPump
        elif select == "Heat Pumps":
            ret = self.OnEnterHeatPumpPage()
            if  ret == 0:
                self.hidePages()
                self.pageHeatPump.modHP.initPanel()
                self.pageHeatPump.Show()
            else:
                self.showInfo("OnEnterHeatPumpPage return %s" %(ret))
###HS2008-03-07
        #pageBoilers
        elif select == "Boilers & burners":
            ###TS2008-03-11 Boiler Page activated
            self.hidePages()
            self.pageBB.modBB.initPanel()
            self.pageBB.Show()
###HS2008-03-12
        #panelEnergy
        elif select == "Energy performance":
            ###TS2008-03-11 Boiler Page activated
            self.hidePages()
            self.panelEnergy.mod.initPanel()
            self.panelEnergy.Show()
        else:
            self.hidePages()
            
            
    ########## DrawPages
###HS2008-03-07 -> drawPageHeatPump eliminated (-> moved to FrameHP        


#------------------------------------------------------------------------------
#--- Eventhandlers Page 0
#------------------------------------------------------------------------------		

    def OnListBoxQuestionnaresPage0ListboxDclick(self, event):
        self.selectQuestionnaire()
        #event.Skip()

    def OnButtonNewQuestionnairePage0(self, event):
        self.activeQid = 0
        self.tree.SelectItem(self.qPage1, select=True)
        #event.Skip()

    def OnButtonOpenQuestionnairePage0(self, event):
        self.selectQuestionnaire()
        #event.Skip()

    def OnButtonDeleteQuestionnairePage0(self, event):
        event.Skip()


#------------------------------------------------------------------------------		
#--- Eventhandlers Page Q1
#------------------------------------------------------------------------------		

    def OnButtonStoreDataPage1(self, event):
        if self.activeQid == 0:
            if self.check(self.tc1Page1.GetValue()) <> 'NULL' and len(Status.DB.questionnaire.Name[self.check(self.tc1Page1.GetValue())]) == 0:
                self.activeQid = Status.DB.questionnaire.insert({"Name":self.check(self.tc1Page1.GetValue())})
                Status.SQL.commit()            
                
                tmp = {
                    "City":self.check(self.tc2Page1.GetValue()),
                    "DescripIndustry":self.check(self.tc9Page1.GetValue()),
                    "Branch":self.check(self.tc10Page1.GetValue()),                                      
                    "Contact":self.check(self.tc3Page1.GetValue()),
                    "Role":self.check(self.tc4Page1.GetValue()),
                    "Address":self.check(self.tc5Page1.GetValue()),
                    "Phone":self.check(self.tc6Page1.GetValue()),
                    "Fax":self.check(self.tc7Page1.GetValue()),
                    "Email":self.check(self.tc8Page1.GetValue()),
                    "NEmployees":self.check(self.tc14Page1.GetValue()),
                    "Turnover":self.check(self.tc15Page1.GetValue()),
                    "ProdCost":self.check(self.tc16Page1.GetValue()),
                    "BaseYear":self.check(self.tc17Page1.GetValue()),
                    "Growth":self.check(self.tc18Page1.GetValue()),
                    "Independent":self.check(self.tc19Page1.GetValue()),
                    "OMThermal":self.check(self.tc20Page1.GetValue()),
                    "OMElectrical":self.check(self.tc21Page1.GetValue()),
                    "HPerDayInd":self.check(self.tc22Page1.GetValue()),
                    "NShifts":self.check(self.tc23Page1.GetValue()),
                    "NDaysInd":self.check(self.tc24Page1.GetValue()),
                    "NoProdStart":self.check(self.tc25_1Page1.GetValue()),
                    "NoProdStop":self.check(self.tc25_2Page1.GetValue())
                    }
                
                if str(self.choiceOfNaceCodePage1.GetStringSelection()) <> 'None':
                    tmp["DBNaceCode_id"] = Status.DB.dbnacecode.CodeNACE[str(self.choiceOfNaceCodePage1.GetStringSelection())][0].DBNaceCode_ID
                
                q = Status.DB.questionnaire.Questionnaire_ID[self.activeQid][0]
                q.update(tmp)
                Status.SQL.commit()
                          
            else:
                self.showError("Name have to be an uniqe value!")
                
        elif self.activeQid <> 0:
            
            if self.check(self.tc1Page1.GetValue()) <> 'NULL' and Status.DB.questionnaire.Name[self.check(self.tc1Page1.GetValue())][0].Questionnaire_ID == self.activeQid:
                tmp = {
                    "Name":self.check(self.tc1Page1.GetValue()),
                    "City":self.check(self.tc2Page1.GetValue()),
                    "DescripIndustry":self.check(self.tc9Page1.GetValue()),
                    "Branch":self.check(self.tc10Page1.GetValue()),                                      
                    "Contact":self.check(self.tc3Page1.GetValue()),
                    "Role":self.check(self.tc4Page1.GetValue()),
                    "Address":self.check(self.tc5Page1.GetValue()),
                    "Phone":self.check(self.tc6Page1.GetValue()),
                    "Fax":self.check(self.tc7Page1.GetValue()),
                    "Email":self.check(self.tc8Page1.GetValue()),
                    "NEmployees":self.check(self.tc14Page1.GetValue()),
                    "Turnover":self.check(self.tc15Page1.GetValue()),
                    "ProdCost":self.check(self.tc16Page1.GetValue()),
                    "BaseYear":self.check(self.tc17Page1.GetValue()),
                    "Growth":self.check(self.tc18Page1.GetValue()),
                    "Independent":self.check(self.tc19Page1.GetValue()),
                    "OMThermal":self.check(self.tc20Page1.GetValue()),
                    "OMElectrical":self.check(self.tc21Page1.GetValue()),
                    "HPerDayInd":self.check(self.tc22Page1.GetValue()),
                    "NShifts":self.check(self.tc23Page1.GetValue()),
                    "NDaysInd":self.check(self.tc24Page1.GetValue()),
                    "NoProdStart":self.check(self.tc25_1Page1.GetValue()),
                    "NoProdStop":self.check(self.tc25_2Page1.GetValue())
                    }
                
                if str(self.choiceOfNaceCodePage1.GetStringSelection()) <> 'None':
                    tmp["DBNaceCode_id"] = Status.DB.dbnacecode.CodeNACE[str(self.choiceOfNaceCodePage1.GetStringSelection())][0].DBNaceCode_ID
                
                q = Status.DB.questionnaire.Questionnaire_ID[self.activeQid][0]
                q.update(tmp)
                Status.SQL.commit()
                          
            else:
                self.showError("Name have to be an uniqe value!")
            
    

        


    def OnButtonAddProductPage1(self, event):
        if self.activeQid <> 0:
            if self.check(self.tc26Page1.GetValue()) <> 'NULL' and len(Status.DB.qproduct.Product[self.tc26Page1.GetValue()].Questionnaire_id[self.activeQid]) == 0:
                tmp = {
                    "Questionnaire_id":self.activeQid,
                    "Product":self.check(self.tc26Page1.GetValue()),
                    "ProductCode":self.check(self.tc27Page1.GetValue()),
                    "QProdYear":self.check(self.tc28Page1.GetValue()),
                    "ProdUnit":self.check(self.tc29Page1.GetValue()),
                    "TurnoverProd":self.check(self.tc30Page1.GetValue()),
                    "ElProd":self.check(self.tc32Page1.GetValue()),
                    "FuelProd":self.check(self.tc31Page1.GetValue())
                    }

                Status.DB.qproduct.insert(tmp)               
                Status.SQL.commit()
                self.fillProductList()

            elif self.check(self.tc26Page1.GetValue()) <> 'NULL' and len(Status.DB.qproduct.Product[self.tc26Page1.GetValue()].Questionnaire_id[self.activeQid]) == 1:
                tmp = {
                    "Product":self.check(self.tc26Page1.GetValue()),
                    "ProductCode":self.check(self.tc27Page1.GetValue()),
                    "QProdYear":self.check(self.tc28Page1.GetValue()),
                    "ProdUnit":self.check(self.tc29Page1.GetValue()),
                    "TurnoverProd":self.check(self.tc30Page1.GetValue()),
                    "ElProd":self.check(self.tc32Page1.GetValue()),
                    "FuelProd":self.check(self.tc31Page1.GetValue())
                    }
                q = Status.DB.qproduct.Product[self.tc26Page1.GetValue()].Questionnaire_id[self.activeQid][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillProductList()
                          
            else:
                self.showError("Product have to be an uniqe value!")
                
      

                

    def OnListBoxProductsPage1ListboxClick(self, event):
        p = Status.DB.qproduct.Questionnaire_id[self.activeQid].Product[str(self.listBoxProductsPage1.GetStringSelection())][0]
        self.tc26Page1.SetValue(str(p.Product))
        self.tc27Page1.SetValue(str(p.ProductCode))
        self.tc28Page1.SetValue(str(p.QProdYear))
        self.tc29Page1.SetValue(str(p.ProdUnit))
        self.tc30Page1.SetValue(str(p.TurnoverProd))
        self.tc32Page1.SetValue(str(p.ElProd))
        self.tc31Page1.SetValue(str(p.FuelProd))
        #event.Skip()

    def OnButtonDeleteProductPage1(self, event):
        event.Skip()

    def OnButtonClearPage1(self, event):
        self.clearPage1()
        #event.Skip()






#------------------------------------------------------------------------------		
#--- Eventhandlers Page 2
#------------------------------------------------------------------------------		

    def OnButtonAddFuelPage2(self, event):
        if self.activeQid <> 0 and self.choiceOfDBFuelTypePage2.GetStringSelection <> 'None':
            
            if len(Status.DB.qfuel.Questionnaire_id[self.activeQid].DBFuel_id[Status.DB.dbfuel.FuelName[str(self.choiceOfDBFuelTypePage2.GetStringSelection())][0].DBFuel_ID]) == 0:
                dbfid = Status.DB.dbfuel.FuelName[str(self.choiceOfDBFuelTypePage2.GetStringSelection())][0].DBFuel_ID
                print "INSERT"
                tmp = {
                    "Questionnaire_id":self.activeQid,
                    "FuelUnit":self.check(self.tc2Page2.GetValue()),
                    "DBFuel_id":dbfid,
                    "MFuelYear":self.check(self.tc3Page2.GetValue()), 
                    "FuelOwn":self.check(self.tc4Page2.GetValue()),
                    "FuelTariff":self.check(self.tc5Page2.GetValue()),
                    "FuelCostYear":self.check(self.tc6Page2.GetValue())                   
                    }
                
                Status.DB.qfuel.insert(tmp)               
                Status.SQL.commit()
                self.fillFuelList()


            elif len(Status.DB.qfuel.Questionnaire_id[self.activeQid].DBFuel_id[Status.DB.dbfuel.FuelName[str(self.choiceOfDBFuelTypePage2.GetStringSelection())][0].DBFuel_ID]) == 1:
                dbfid = Status.DB.dbfuel.FuelName[str(self.choiceOfDBFuelTypePage2.GetStringSelection())][0].DBFuel_ID
                print "UPDATE"
                tmp = {
                    "FuelUnit":self.check(self.tc2Page2.GetValue()),
                    "DBFuel_id":dbfid,
                    "MFuelYear":self.check(self.tc3Page2.GetValue()), 
                    "FuelOwn":self.check(self.tc4Page2.GetValue()),
                    "FuelTariff":self.check(self.tc5Page2.GetValue()),
                    "FuelCostYear":self.check(self.tc6Page2.GetValue())
                    }
                
                q = Status.DB.qfuel.DBFuel_id[dbfid].Questionnaire_id[self.activeQid][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillFuelList()
                          
            else:
                self.showError("FuelName have to be an uniqe value!")






        

    def OnButtonRemoveFuelFromListPage2(self, event):
        event.Skip()


        

    def OnButtonStorePage2(self, event):
        if self.activeQid <> 0:
            if len(Status.DB.qelectricity.Questionnaire_id[self.activeQid]) == 0:
                tmp = {
                    "Questionnaire_id":self.activeQid,
                    "PowerContrTot":self.check(self.gridPage2.GetCellValue(1, 3)),
                    "PowerContrStd":self.check(self.gridPage2.GetCellValue(1, 1)),
                    "PowerContrPeak":self.check(self.gridPage2.GetCellValue(1, 0)),
                    "PowerContrVall":self.check(self.gridPage2.GetCellValue(1, 2)),
                    "ElectricityTotYear":self.check(self.gridPage2.GetCellValue(0, 3)),
                    "ElectricityPeakYear":self.check(self.gridPage2.GetCellValue(0, 0)),
                    "ElectricityStandYear":self.check(self.gridPage2.GetCellValue(0, 1)),
                    "ElectricityValleyYear":self.check(self.gridPage2.GetCellValue(0, 2)),
                    "ElGenera":self.check(self.gridPage2.GetCellValue(0, 4)),
                    "ElSales":self.check(self.gridPage2.GetCellValue(0, 5)),
                    "ElectricityRef":self.check(self.gridPage2.GetCellValue(8, 0)),
                    "ElectricityAC":self.check(self.gridPage2.GetCellValue(8, 1)),
                    "ElectricityThOther":self.check(self.gridPage2.GetCellValue(8, 2)),
                    "ElectricityMotors":self.check(self.gridPage2.GetCellValue(8, 3)),
                    "ElectricityChem":self.check(self.gridPage2.GetCellValue(8, 4)),
                    "ElectricityLight":self.check(self.gridPage2.GetCellValue(8, 5)),
                    "ElTariffClassTot":self.check(self.gridPage2.GetCellValue(2, 3)),
                    "ElTariffClassStd":self.check(self.gridPage2.GetCellValue(2, 1)),
                    "ElTariffClassPeak":self.check(self.gridPage2.GetCellValue(2, 0)),
                    "ElTariffClassTotVall":self.check(self.gridPage2.GetCellValue(2, 2)),
                    "ElTariffClassCHP":self.check(self.gridPage2.GetCellValue(2, 5)),
                    "ElTariffPowTot":self.check(self.gridPage2.GetCellValue(3, 3)),
                    "ElTariffPowStd":self.check(self.gridPage2.GetCellValue(3, 1)),
                    "ElTariffPowPeak":self.check(self.gridPage2.GetCellValue(3, 0)),
                    "ElTariffPowVall":self.check(self.gridPage2.GetCellValue(3, 2)),
                    "ElTariffPowCHP":self.check(self.gridPage2.GetCellValue(3, 5)),
                    "ElTariffCTot":self.check(self.gridPage2.GetCellValue(4, 3)),
                    "ElTariffCStd":self.check(self.gridPage2.GetCellValue(4, 1)),
                    "ElTariffCPeak":self.check(self.gridPage2.GetCellValue(4, 0)),
                    "ElTariffCVall":self.check(self.gridPage2.GetCellValue(4, 2)),
                    "ETariffCHP":self.check(self.gridPage2.GetCellValue(4, 5)),
                    "ElCostYearTot":self.check(self.gridPage2.GetCellValue(5, 3)),
                    "ElCostYearStd":self.check(self.gridPage2.GetCellValue(5, 1)),
                    "ElCostYearPeak":self.check(self.gridPage2.GetCellValue(5, 0)),
                    "ElCostYearVall":self.check(self.gridPage2.GetCellValue(5, 2)),
                    "ElSalesYearCHP":self.check(self.gridPage2.GetCellValue(5, 5))
                    }
                
                Status.DB.qelectricity.insert(tmp)
                Status.SQL.commit()                      

            elif len(Status.DB.qelectricity.Questionnaire_id[self.activeQid]) == 1:
                q = Status.DB.qelectricity.Questionnaire_id[self.activeQid][0]
                tmp = {                    
                    "PowerContrTot":self.check(self.gridPage2.GetCellValue(1, 3)),
                    "PowerContrStd":self.check(self.gridPage2.GetCellValue(1, 1)),
                    "PowerContrPeak":self.check(self.gridPage2.GetCellValue(1, 0)),
                    "PowerContrVall":self.check(self.gridPage2.GetCellValue(1, 2)),
                    "ElectricityTotYear":self.check(self.gridPage2.GetCellValue(0, 3)),
                    "ElectricityPeakYear":self.check(self.gridPage2.GetCellValue(0, 0)),
                    "ElectricityStandYear":self.check(self.gridPage2.GetCellValue(0, 1)),
                    "ElectricityValleyYear":self.check(self.gridPage2.GetCellValue(0, 2)),
                    "ElGenera":self.check(self.gridPage2.GetCellValue(0, 4)),
                    "ElSales":self.check(self.gridPage2.GetCellValue(0, 5)),
                    "ElectricityRef":self.check(self.gridPage2.GetCellValue(8, 0)),
                    "ElectricityAC":self.check(self.gridPage2.GetCellValue(8, 1)),
                    "ElectricityThOther":self.check(self.gridPage2.GetCellValue(8, 2)),
                    "ElectricityMotors":self.check(self.gridPage2.GetCellValue(8, 3)),
                    "ElectricityChem":self.check(self.gridPage2.GetCellValue(8, 4)),
                    "ElectricityLight":self.check(self.gridPage2.GetCellValue(8, 5)),
                    "ElTariffClassTot":self.check(self.gridPage2.GetCellValue(2, 3)),
                    "ElTariffClassStd":self.check(self.gridPage2.GetCellValue(2, 1)),
                    "ElTariffClassPeak":self.check(self.gridPage2.GetCellValue(2, 0)),
                    "ElTariffClassTotVall":self.check(self.gridPage2.GetCellValue(2, 2)),
                    "ElTariffClassCHP":self.check(self.gridPage2.GetCellValue(2, 5)),
                    "ElTariffPowTot":self.check(self.gridPage2.GetCellValue(3, 3)),
                    "ElTariffPowStd":self.check(self.gridPage2.GetCellValue(3, 1)),
                    "ElTariffPowPeak":self.check(self.gridPage2.GetCellValue(3, 0)),
                    "ElTariffPowVall":self.check(self.gridPage2.GetCellValue(3, 2)),
                    "ElTariffPowCHP":self.check(self.gridPage2.GetCellValue(3, 5)),
                    "ElTariffCTot":self.check(self.gridPage2.GetCellValue(4, 3)),
                    "ElTariffCStd":self.check(self.gridPage2.GetCellValue(4, 1)),
                    "ElTariffCPeak":self.check(self.gridPage2.GetCellValue(4, 0)),
                    "ElTariffCVall":self.check(self.gridPage2.GetCellValue(4, 2)),
                    "ETariffCHP":self.check(self.gridPage2.GetCellValue(4, 5)),
                    "ElCostYearTot":self.check(self.gridPage2.GetCellValue(5, 3)),
                    "ElCostYearStd":self.check(self.gridPage2.GetCellValue(5, 1)),
                    "ElCostYearPeak":self.check(self.gridPage2.GetCellValue(5, 0)),
                    "ElCostYearVall":self.check(self.gridPage2.GetCellValue(5, 2)),
                    "ElSalesYearCHP":self.check(self.gridPage2.GetCellValue(5, 5))
                    }
                q.update(tmp)
                Status.SQL.commit()

                
        





        

    def OnFuelListBoxListboxClickPage2(self, event):
        q = Status.DB.qfuel.Questionnaire_id[self.activeQid].DBFuel_id[Status.DB.dbfuel.FuelName[str(self.fuelListBoxPage2.GetStringSelection())][0].DBFuel_ID][0]
        self.tc2Page2.SetValue(str(q.FuelUnit))
        self.tc3Page2.SetValue(str(q.MFuelYear))
        self.tc4Page2.SetValue(str(q.FuelOwn))
        self.tc5Page2.SetValue(str(q.FuelTariff))
        self.tc6Page2.SetValue(str(q.FuelCostYear))
        self.choiceOfDBFuelTypePage2.SetSelection(self.choiceOfDBFuelTypePage2.FindString(str(self.fuelListBoxPage2.GetStringSelection())))
        #event.Skip()

    def OnButtonClearPage2(self, event):
        self.clearPage2()
        #event.Skip()


#------------------------------------------------------------------------------		
#--- Eventhandlers Page 3
#------------------------------------------------------------------------------		

    def OnButtonAddProcessPage3(self, event):
        if self.activeQid <> 0:
            if self.check(self.tc1Page3.GetValue()) <> 'NULL' and len(Status.DB.qprocessdata.Process[self.tc1Page3.GetValue()].Questionnaire_id[self.activeQid]) == 0:
                dbuid = Status.DB.dbunitoperation.UnitOperation[str(self.choiceOfDBUnitOperationPage3.GetStringSelection())][0].DBUnitOperation_ID
                dbpmfid = Status.DB.dbfluid.FluidName[str(self.choiceOfPMDBFluidPage3.GetStringSelection())][0].DBFluid_ID
                dbsmfid = Status.DB.dbfluid.FluidName[str(self.choiceOfSMDBFluidPage3.GetStringSelection())][0].DBFluid_ID                       
        
                tmp = {
                    "Questionnaire_id":self.activeQid,
                    "Process":self.check(self.tc1Page3.GetValue()),
                    "DBUnitOperation_id":dbuid,
                    "ProcType":self.check(self.tc2Page3.GetValue()),	
                    "ProcMedDBFluid_id":dbpmfid,
                    "PT":self.check(self.tc5Page3.GetValue()), 
                    "PTInFlow":self.check(self.tc6Page3.GetValue()), 
                    "PTStartUp":self.check(self.tc7Page3.GetValue()), 
                    "VInFlowDay":self.check(self.tc8Page3.GetValue()), 
                    "VolProcMed":self.check(self.tc9Page3.GetValue()), 
                    "UAProc":self.check(self.tc10Page3.GetValue()), 
                    "HPerDayProc":self.check(self.tc11Page3.GetValue()), 
                    "NBatch":self.check(self.tc12Page3.GetValue()), 
                    "HBatch":self.check(self.tc13Page3.GetValue()), 
                    "NDaysProc":self.check(self.tc14Page3.GetValue()), 	
                    "PTOutFlow":self.check(self.tc15Page3.GetValue()), 
                    "PTFinal":self.check(self.tc16Page3.GetValue()), 
                    "VOutFlow":self.check(self.tc17Page3.GetValue()), 
                    "HeatRecOK":self.check(self.tc18Page3.GetValue()), 
                    "HeatRecExist":self.check(self.tc19Page3.GetValue()), 
                    "SourceWasteHeat":self.check(self.tc20Page3.GetValue()), 	
                    "PTInFlowRec":self.check(self.tc21Page3.GetValue()), 
                    "SupplyMedDBFluid_id":dbsmfid,
                    "PipeDuctProc":self.check(self.tc23Page3.GetValue()), 
                    "TSupply":self.check(self.tc24Page3.GetValue()), 
                    "SupplyMedFlow":self.check(self.tc25Page3.GetValue()), 
                    "UPHtotQ":self.check(self.tc26Page3.GetValue()) 
                    }

                Status.DB.qprocessdata.insert(tmp)               
                Status.SQL.commit()
                self.fillProcessList()

            elif self.check(self.tc1Page3.GetValue()) <> 'NULL' and len(Status.DB.qprocessdata.Process[self.tc1Page3.GetValue()].Questionnaire_id[self.activeQid]) == 1:
                dbuid = Status.DB.dbunitoperation.UnitOperation[str(self.choiceOfDBUnitOperationPage3.GetStringSelection())][0].DBUnitOperation_ID
                dbpmfid = Status.DB.dbfluid.FluidName[str(self.choiceOfPMDBFluidPage3.GetStringSelection())][0].DBFluid_ID
                dbsmfid = Status.DB.dbfluid.FluidName[str(self.choiceOfSMDBFluidPage3.GetStringSelection())][0].DBFluid_ID                       
        
                tmp = {
                    "Process":self.check(self.tc1Page3.GetValue()),
                    "DBUnitOperation_id":dbuid,
                    "ProcType":self.check(self.tc2Page3.GetValue()),	
                    "ProcMedDBFluid_id":dbpmfid,
                    "PT":self.check(self.tc5Page3.GetValue()), 
                    "PTInFlow":self.check(self.tc6Page3.GetValue()), 
                    "PTStartUp":self.check(self.tc7Page3.GetValue()), 
                    "VInFlowDay":self.check(self.tc8Page3.GetValue()), 
                    "VolProcMed":self.check(self.tc9Page3.GetValue()), 
                    "UAProc":self.check(self.tc10Page3.GetValue()), 
                    "HPerDayProc":self.check(self.tc11Page3.GetValue()), 
                    "NBatch":self.check(self.tc12Page3.GetValue()), 
                    "HBatch":self.check(self.tc13Page3.GetValue()), 
                    "NDaysProc":self.check(self.tc14Page3.GetValue()), 	
                    "PTOutFlow":self.check(self.tc15Page3.GetValue()), 
                    "PTFinal":self.check(self.tc16Page3.GetValue()), 
                    "VOutFlow":self.check(self.tc17Page3.GetValue()), 
                    "HeatRecOK":self.check(self.tc18Page3.GetValue()), 
                    "HeatRecExist":self.check(self.tc19Page3.GetValue()), 
                    "SourceWasteHeat":self.check(self.tc20Page3.GetValue()), 	
                    "PTInFlowRec":self.check(self.tc21Page3.GetValue()), 
                    "SupplyMedDBFluid_id":dbsmfid,
                    "PipeDuctProc":self.check(self.tc23Page3.GetValue()), 
                    "TSupply":self.check(self.tc24Page3.GetValue()), 
                    "SupplyMedFlow":self.check(self.tc25Page3.GetValue()), 
                    "UPHtotQ":self.check(self.tc26Page3.GetValue()) 
                    }
                q = Status.DB.qprocessdata.Process[self.tc1Page3.GetValue()].Questionnaire_id[self.activeQid][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillProcessList()
                          
            else:
                self.showError("Process have to be an uniqe value!")



    def OnButtonDeleteProcessPage3(self, event):
        event.Skip()

    def OnListBoxProcessesPage3ListboxClick(self, event):
        q = Status.DB.qprocessdata.Questionnaire_id[self.activeQid].Process[str(self.listBoxProcessesPage3.GetStringSelection())][0]
        self.tc1Page3.SetValue(str(q.Process))
        self.tc2Page3.SetValue(str(q.ProcType))
        self.tc5Page3.SetValue(str(q.PT))
        self.tc6Page3.SetValue(str(q.PTInFlow))
        self.tc7Page3.SetValue(str(q.PTStartUp))
        self.tc8Page3.SetValue(str(q.VInFlowDay))
        self.tc9Page3.SetValue(str(q.VolProcMed))
        self.tc10Page3.SetValue(str(q.UAProc))
        self.tc11Page3.SetValue(str(q.HPerDayProc))
        self.tc12Page3.SetValue(str(q.NBatch))
        self.tc13Page3.SetValue(str(q.HBatch))
        self.tc14Page3.SetValue(str(q.NDaysProc))		
        self.tc15Page3.SetValue(str(q.PTOutFlow))
        self.tc16Page3.SetValue(str(q.PTFinal))
        self.tc17Page3.SetValue(str(q.VOutFlow))
        self.tc18Page3.SetValue(str(q.HeatRecOK))
        self.tc19Page3.SetValue(str(q.HeatRecExist))
        self.tc20Page3.SetValue(str(q.SourceWasteHeat))	
        self.tc21Page3.SetValue(str(q.PTInFlowRec))
        self.tc23Page3.SetValue(str(q.PipeDuctProc))
        self.tc24Page3.SetValue(str(q.TSupply))
        self.tc25Page3.SetValue(str(q.SupplyMedFlow))
        self.tc26Page3.SetValue(str(q.UPHtotQ))
        if q.DBUnitOperation_id <> None:
            self.choiceOfDBUnitOperationPage3.SetSelection(self.choiceOfDBUnitOperationPage3.FindString(str(Status.DB.dbunitoperation.DBUnitOperation_ID[q.DBUnitOperation_id][0].UnitOperation)))
        if q.ProcMedDBFluid_id <> None:
            self.choiceOfPMDBFluidPage3.SetSelection(self.choiceOfPMDBFluidPage3.FindString(str(Status.DB.dbfluid.DBFluid_ID[q.ProcMedDBFluid_id][0].FluidName)))
        if q.SupplyMedDBFluid_id <> None:
            self.choiceOfSMDBFluidPage3.SetSelection(self.choiceOfSMDBFluidPage3.FindString(str(Status.DB.dbfluid.DBFluid_ID[q.SupplyMedDBFluid_id][0].FluidName)))
        #event.Skip()

    def OnButtonClearPage3(self, event):
        self.clearPage3()
        #event.Skip()



#------------------------------------------------------------------------------		
#--- Eventhandlers Page 4
#------------------------------------------------------------------------------		

    
    def OnListBoxEquipmentListPage4ListboxClick(self, event):
        q = Status.DB.qgenerationhc.Questionnaire_id[self.activeQid].Equipment[str(self.listBoxEquipmentListPage4.GetStringSelection())][0]
        self.tc1Page4.SetValue(str(q.Equipment))
        self.tc2Page4.SetValue(str(q.Manufact))
        self.tc3Page4.SetValue(str(q.YearManufact))
        self.tc4Page4.SetValue(str(q.Model))
        self.tc5Page4.SetValue(str(q.EquipType))
        self.tc6Page4.SetValue(str(q.NumEquipUnits))
        self.tc9Page4.SetValue(str(q.HCGPnom))
        self.tc10Page4.SetValue(str(q.FuelConsum))
        self.tc11Page4.SetValue(str(q.UnitsFuelConsum))
        self.tc12Page4.SetValue(str(q.ElectriConsum))
        self.tc13Page4.SetValue(str(q.HCGTEfficiency))
        self.tc14Page4.SetValue(str(q.HCGEEfficiency))
        self.tc15Page4.SetValue(str(q.ElectriProduction))
        self.tc16Page4.SetValue(str(q.TExhaustGas))
        self.tc17Page4.SetValue(str(q.PartLoad))
        self.tc18Page4.SetValue(str(q.HPerDayEq))
        self.tc19Page4.SetValue(str(q.NDaysEq))
        self.tc20Page4.SetValue(str(q.PipeDuctEquip))
        self.tc8Page4.SetValue(str(q.CoolTowerType))
        if q.DBFuel_id <> None:
            self.choiceOfDBFuelPage4.SetSelection(self.choiceOfDBFuelPage4.FindString(str(Status.DB.dbfuel.DBFuel_ID[q.DBFuel_id][0].FuelName)))
        #event.Skip()

    def OnButtonDeleteEquipmentPage4Button(self, event):
        event.Skip()



    def OnButtonAddEquipmentPage4Button(self, event):        
        if self.activeQid <> 0:
            if self.check(self.tc1Page4.GetValue()) <> 'NULL' and len(Status.DB.qgenerationhc.Equipment[self.tc1Page4.GetValue()].Questionnaire_id[self.activeQid]) == 0:
                dbfid = Status.DB.dbfuel.FuelName[str(self.choiceOfDBFuelPage4.GetStringSelection())][0].DBFuel_ID                      
        
                tmp = {
                    "Questionnaire_id":self.activeQid,
                    "Equipment":self.check(self.tc1Page4.GetValue()), 
                    "Manufact":self.check(self.tc2Page4.GetValue()), 
                    "YearManufact":self.check(self.tc3Page4.GetValue()), 
                    "Model":self.check(self.tc4Page4.GetValue()), 
                    "EquipType":self.check(self.tc5Page4.GetValue()), 
                    "NumEquipUnits":self.check(self.tc6Page4.GetValue()),
                    "DBFuel_id":dbfid,
                    "HCGPnom":self.check(self.tc9Page4.GetValue()), 
                    "FuelConsum":self.check(self.tc10Page4.GetValue()), 
                    "UnitsFuelConsum":self.check(self.tc11Page4.GetValue()), 
                    "ElectriConsum":self.check(self.tc12Page4.GetValue()), 
                    "HCGTEfficiency":self.check(self.tc13Page4.GetValue()), 
                    "HCGEEfficiency":self.check(self.tc14Page4.GetValue()), 
                    "ElectriProduction":self.check(self.tc15Page4.GetValue()), 
                    "TExhaustGas":self.check(self.tc16Page4.GetValue()), 
                    "PartLoad":self.check(self.tc17Page4.GetValue()), 
                    "HPerDayEq":self.check(self.tc18Page4.GetValue()), 
                    "NDaysEq":self.check(self.tc19Page4.GetValue()), 
                    "PipeDuctEquip":self.check(self.tc20Page4.GetValue()), 
                    "CoolTowerType":self.check(self.tc8Page4.GetValue()),
                    "IsAlternative":0
                    }

                Status.DB.qgenerationhc.insert(tmp)               
                Status.SQL.commit()
                self.fillEquipmentList()

            elif self.check(self.tc1Page4.GetValue()) <> 'NULL' and len(Status.DB.qgenerationhc.Equipment[self.tc1Page4.GetValue()].Questionnaire_id[self.activeQid]) == 1:
                dbfid = Status.DB.dbfuel.FuelName[str(self.choiceOfDBFuelPage4.GetStringSelection())][0].DBFuel_ID                       
        
                tmp = {
                    "Equipment":self.check(self.tc1Page4.GetValue()), 
                    "Manufact":self.check(self.tc2Page4.GetValue()), 
                    "YearManufact":self.check(self.tc3Page4.GetValue()), 
                    "Model":self.check(self.tc4Page4.GetValue()), 
                    "EquipType":self.check(self.tc5Page4.GetValue()), 
                    "NumEquipUnits":self.check(self.tc6Page4.GetValue()),
                    "DBFuel_id":dbfid,
                    "HCGPnom":self.check(self.tc9Page4.GetValue()), 
                    "FuelConsum":self.check(self.tc10Page4.GetValue()), 
                    "UnitsFuelConsum":self.check(self.tc11Page4.GetValue()), 
                    "ElectriConsum":self.check(self.tc12Page4.GetValue()), 
                    "HCGTEfficiency":self.check(self.tc13Page4.GetValue()), 
                    "HCGEEfficiency":self.check(self.tc14Page4.GetValue()), 
                    "ElectriProduction":self.check(self.tc15Page4.GetValue()), 
                    "TExhaustGas":self.check(self.tc16Page4.GetValue()), 
                    "PartLoad":self.check(self.tc17Page4.GetValue()), 
                    "HPerDayEq":self.check(self.tc18Page4.GetValue()), 
                    "NDaysEq":self.check(self.tc19Page4.GetValue()), 
                    "PipeDuctEquip":self.check(self.tc20Page4.GetValue()), 
                    "CoolTowerType":self.check(self.tc8Page4.GetValue()),
                    "IsAlternative":0
                    }
                q = Status.DB.qgenerationhc.Equipment[self.tc1Page4.GetValue()].Questionnaire_id[self.activeQid][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillEquipmentList()
                          
            else:
                self.showError("Equipment have to be an uniqe value!")
        
        

    def OnButtonClearPage4Button(self, event):
        self.clearPage4()
        #event.Skip()


#------------------------------------------------------------------------------		
#--- Eventhandlers Page 5
#------------------------------------------------------------------------------		


    def OnListBoxDistributionListPage5ListboxClick(self, event):
        p = Status.DB.qdistributionhc.Questionnaire_id[self.activeQid].Pipeduct[str(self.listBoxDistributionListPage5.GetStringSelection())][0]
        self.tc1Page5.SetValue(str(p.Pipeduct))
        #self.tc2Page5.SetValue(str(p.HeatFromQGenerationHC_id))
        if len(Status.DB.qgenerationhc.QGenerationHC_ID[p.HeatFromQGenerationHC_id]) <> 0:
            self.choiceOfEquipmentPage5.SetSelection(self.choiceOfEquipmentPage5.FindString(str(Status.DB.qgenerationhc.QGenerationHC_ID[p.HeatFromQGenerationHC_id][0].Equipment)))
            
        self.tc3Page5.SetValue(str(p.HeatDistMedium))
        self.tc4Page5.SetValue(str(p.DistribCircFlow))
        self.tc5Page5.SetValue(str(p.ToutDistrib))
        self.tc6Page5.SetValue(str(p.TreturnDistrib))
        self.tc7Page5.SetValue(str(p.PercentRecirc))
        self.tc8Page5.SetValue(str(p.Tfeedup))
        self.tc9Page5.SetValue(str(p.PressDistMedium))
        self.tc10Page5.SetValue(str(p.PercentCondRecovery))
        self.tc11Page5.SetValue(str(p.TotLengthDistPipe))
        self.tc12Page5.SetValue(str(p.UDistPipe))
        self.tc13Page5.SetValue(str(p.DDistPipe))
        self.tc14Page5.SetValue(str(p.DeltaDistPipe))		
        self.tc15Page5.SetValue(str(p.NumStorageUnits)) 
        self.tc16Page5.SetValue(str(p.VtotStorage))
        self.tc17Page5.SetValue(str(p.TypeStorage))
        self.tc18Page5.SetValue(str(p.PmaxStorage))
        self.tc19Page5.SetValue(str(p.TmaxStorage))
        #event.Skip()

    def OnButtonClearPage5(self, event):
        self.clearPage5()
        #event.Skip()

    def OnButtonDeleteDistributionPage5(self, event):
        event.Skip()

    def OnButtonAddDistributionPage5(self, event):
        if self.activeQid <> 0:
            if self.check(self.tc1Page5.GetValue()) <> 'NULL' and len(Status.DB.qdistributionhc.Pipeduct[self.tc1Page5.GetValue()].Questionnaire_id[self.activeQid]) == 0:
                qgid = Status.DB.qgenerationhc.Equipment[str(self.choiceOfEquipmentPage5.GetStringSelection())][0].QGenerationHC_ID                      
        
                tmp = {
                    "Questionnaire_id":self.activeQid,
                    "Pipeduct":self.check(self.tc1Page5.GetValue()),
                    "HeatFromQGenerationHC_id":qgid,
                    "HeatDistMedium":self.check(self.tc3Page5.GetValue()), 
                    "DistribCircFlow":self.check(self.tc4Page5.GetValue()), 
                    "ToutDistrib":self.check(self.tc5Page5.GetValue()), 
                    "TreturnDistrib":self.check(self.tc6Page5.GetValue()), 
                    "PercentRecirc":self.check(self.tc7Page5.GetValue()), 
                    "Tfeedup":self.check(self.tc8Page5.GetValue()), 
                    "PressDistMedium":self.check(self.tc9Page5.GetValue()), 
                    "PercentCondRecovery":self.check(self.tc10Page5.GetValue()), 
                    "TotLengthDistPipe":self.check(self.tc11Page5.GetValue()), 
                    "UDistPipe":self.check(self.tc12Page5.GetValue()), 
                    "DDistPipe":self.check(self.tc13Page5.GetValue()), 
                    "DeltaDistPipe":self.check(self.tc14Page5.GetValue()), 		
                    "NumStorageUnits":self.check(self.tc15Page5.GetValue()),  
                    "VtotStorage":self.check(self.tc16Page5.GetValue()), 
                    "TypeStorage":self.check(self.tc17Page5.GetValue()), 
                    "PmaxStorage":self.check(self.tc18Page5.GetValue()), 
                    "TmaxStorage":self.check(self.tc19Page5.GetValue()),
                    "IsAlternative":0
                    }

                Status.DB.qdistributionhc.insert(tmp)               
                Status.SQL.commit()
                self.fillDistributionList()

            elif self.check(self.tc1Page5.GetValue()) <> 'NULL' and len(Status.DB.qdistributionhc.Pipeduct[self.tc1Page5.GetValue()].Questionnaire_id[self.activeQid]) == 1:
                qgid = Status.DB.qgenerationhc.Equipment[str(self.choiceOfEquipmentPage5.GetStringSelection())][0].QGenerationHC_ID                       
        
                tmp = {
                    "Pipeduct":self.check(self.tc1Page5.GetValue()),
                    "HeatFromQGenerationHC_id":qgid,
                    "HeatDistMedium":self.check(self.tc3Page5.GetValue()), 
                    "DistribCircFlow":self.check(self.tc4Page5.GetValue()), 
                    "ToutDistrib":self.check(self.tc5Page5.GetValue()), 
                    "TreturnDistrib":self.check(self.tc6Page5.GetValue()), 
                    "PercentRecirc":self.check(self.tc7Page5.GetValue()), 
                    "Tfeedup":self.check(self.tc8Page5.GetValue()), 
                    "PressDistMedium":self.check(self.tc9Page5.GetValue()), 
                    "PercentCondRecovery":self.check(self.tc10Page5.GetValue()), 
                    "TotLengthDistPipe":self.check(self.tc11Page5.GetValue()), 
                    "UDistPipe":self.check(self.tc12Page5.GetValue()), 
                    "DDistPipe":self.check(self.tc13Page5.GetValue()), 
                    "DeltaDistPipe":self.check(self.tc14Page5.GetValue()), 		
                    "NumStorageUnits":self.check(self.tc15Page5.GetValue()),  
                    "VtotStorage":self.check(self.tc16Page5.GetValue()), 
                    "TypeStorage":self.check(self.tc17Page5.GetValue()), 
                    "PmaxStorage":self.check(self.tc18Page5.GetValue()), 
                    "TmaxStorage":self.check(self.tc19Page5.GetValue()),
                    "IsAlternative":0
                    }
                q = Status.DB.qdistributionhc.Pipeduct[self.tc1Page5.GetValue()].Questionnaire_id[self.activeQid][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillDistributionList()
                          
            else:
                self.showError("Pipeduct have to be an uniqe value!")




#------------------------------------------------------------------------------		
#--- Eventhandlers Page 6
#------------------------------------------------------------------------------		

    def OnButtonStoreDataPage6(self, event):
        
        if self.activeQid <> 0:
            if len(Status.DB.qrenewables.Questionnaire_id[self.activeQid]) == 0:
 
                tmp = {
                    "Questionnaire_id":self.activeQid,
                    "SurfAreaRoof":self.check(self.tc6_1Page6.GetValue()), 
                    "SurfAreaGround":self.check(self.tc6_2Page6.GetValue()), 	
                    "InclinationRoof":self.check(self.tc7_1Page6.GetValue()), 
                    "InclinationGround":self.check(self.tc7_2Page6.GetValue()), 
                    "OrientationRoof":self.check(self.tc8_1Page6.GetValue()), 
                    "OrientationGround":self.check(self.tc8_2Page6.GetValue()), 
                    "ShadingRoof":self.check(self.tc9_1Page6.GetValue()), 
                    "ShadingGround":self.check(self.tc9_2Page6.GetValue()), 
                    "DistanceToRoof":self.check(self.tc10_1Page6.GetValue()), 
                    "DistanceToGround":self.check(self.tc10_2Page6.GetValue()), 
                    "RoofType":self.check(self.tc11Page6.GetValue()), 
                    "RoofStaticLoadCap":self.check(self.tc12Page6.GetValue()),	
                    "BiomassFromProc":self.check(self.tc14Page6.GetValue()), 
                    "PeriodBiomassProcStart":self.check(self.tc15_1Page6.GetValue()), 
                    "PeriodBiomassProcStop":self.check(self.tc15_2Page6.GetValue()), 
                    "NDaysBiomassProc":self.check(self.tc16Page6.GetValue()), 
                    "QBiomassProcDay":self.check(self.tc17Page6.GetValue()), 
                    "SpaceBiomassProc":self.check(self.tc18Page6.GetValue()), 
                    "LCVBiomassProc":self.check(self.tc19Page6.GetValue()), 
                    "HumidBiomassProc":self.check(self.tc20Page6.GetValue()), 	
                    "BiomassFromRegion":self.check(self.tc21Page6.GetValue()), 
                    "PriceBiomassRegion":self.check(self.tc22Page6.GetValue()), 
                    "PeriodBiomassRegionStart":self.check(self.tc23_1Page6.GetValue()), 
                    "PeriodBiomassRegionStop":self.check(self.tc23_2Page6.GetValue()), 
                    "NDaysBiomassRegion":self.check(self.tc24Page6.GetValue())
                    }                
           
                Status.DB.qrenewables.insert(tmp)
                Status.SQL.commit()
       
            else:

                tmp = {
                    "SurfAreaRoof":self.check(self.tc6_1Page6.GetValue()), 
                    "SurfAreaGround":self.check(self.tc6_2Page6.GetValue()), 	
                    "InclinationRoof":self.check(self.tc7_1Page6.GetValue()), 
                    "InclinationGround":self.check(self.tc7_2Page6.GetValue()), 
                    "OrientationRoof":self.check(self.tc8_1Page6.GetValue()), 
                    "OrientationGround":self.check(self.tc8_2Page6.GetValue()), 
                    "ShadingRoof":self.check(self.tc9_1Page6.GetValue()), 
                    "ShadingGround":self.check(self.tc9_2Page6.GetValue()), 
                    "DistanceToRoof":self.check(self.tc10_1Page6.GetValue()), 
                    "DistanceToGround":self.check(self.tc10_2Page6.GetValue()), 
                    "RoofType":self.check(self.tc11Page6.GetValue()), 
                    "RoofStaticLoadCap":self.check(self.tc12Page6.GetValue()),	
                    "BiomassFromProc":self.check(self.tc14Page6.GetValue()), 
                    "PeriodBiomassProcStart":self.check(self.tc15_1Page6.GetValue()), 
                    "PeriodBiomassProcStop":self.check(self.tc15_2Page6.GetValue()), 
                    "NDaysBiomassProc":self.check(self.tc16Page6.GetValue()), 
                    "QBiomassProcDay":self.check(self.tc17Page6.GetValue()), 
                    "SpaceBiomassProc":self.check(self.tc18Page6.GetValue()), 
                    "LCVBiomassProc":self.check(self.tc19Page6.GetValue()), 
                    "HumidBiomassProc":self.check(self.tc20Page6.GetValue()), 	
                    "BiomassFromRegion":self.check(self.tc21Page6.GetValue()), 
                    "PriceBiomassRegion":self.check(self.tc22Page6.GetValue()), 
                    "PeriodBiomassRegionStart":self.check(self.tc23_1Page6.GetValue()), 
                    "PeriodBiomassRegionStop":self.check(self.tc23_2Page6.GetValue()), 
                    "NDaysBiomassRegion":self.check(self.tc24Page6.GetValue())
                    }                
              
                q = Status.DB.qrenewables.Questionnaire_id[self.activeQid][0]
                q.update(tmp)
                Status.SQL.commit()
                          



#------------------------------------------------------------------------------		
#--- Eventhandlers Page 7
#------------------------------------------------------------------------------		

    def OnListBoxBuildingListPage7ListboxClick(self, event):
        q = Status.DB.qbuildings.Questionnaire_id[self.activeQid].BuildName[str(self.listBoxBuildingListPage7.GetStringSelection())][0]
        self.tc1Page7.SetValue(str(q.BuildName))
        self.tc2Page7.SetValue(str(q.BuildConstructSurface))
        self.tc3Page7.SetValue(str(q.BuildUsefulSurface))
        self.tc4Page7.SetValue(str(q.BuildUsage))
        self.tc5Page7.SetValue(str(q.BuildMaxHP))
        self.tc6Page7.SetValue(str(q.BuildMaxCP))
        self.tc7Page7.SetValue(str(q.BuildAnnualHeating))
        self.tc8Page7.SetValue(str(q.BuildAnnualAirCond))
        self.tc9Page7.SetValue(str(q.BuildDailyDHW))
        self.tc10Page7.SetValue(str(q.BuildHoursOccup))
        self.tc11Page7.SetValue(str(q.BuildDaysInUse))
        self.tc12_1Page7.SetValue(str(q.BuildHolidaysPeriodStart))
        self.tc12_2Page7.SetValue(str(q.BuildHolidaysPeriodStop))
        self.tc13_1Page7.SetValue(str(q.BuildHeatingPeriodStart))
        self.tc13_2Page7.SetValue(str(q.BuildHeatingPeriodStop))
        self.tc14_1Page7.SetValue(str(q.BuildAirCondPeriodStart))
        self.tc14_2Page7.SetValue(str(q.BuildAirCondPeriodStop))
        #event.Skip()

    def OnButtonClearPage7(self, event):
        self.clearPage7()
        #event.Skip()

    def OnButtonDeleteBuildingPage7(self, event):
        event.Skip()

    def OnButtonAddBuildingPage7(self, event):
        if self.activeQid <> 0:
            if self.check(self.tc1Page7.GetValue()) <> 'NULL' and len(Status.DB.qbuildings.BuildName[self.tc1Page7.GetValue()].Questionnaire_id[self.activeQid]) == 0:

                tmp = {
                    "Questionnaire_id":self.activeQid,
                    "BuildName":self.check(self.tc1Page7.GetValue()), 
                    "BuildConstructSurface":self.check(self.tc2Page7.GetValue()), 
                    "BuildUsefulSurface":self.check(self.tc3Page7.GetValue()), 
                    "BuildUsage":self.check(self.tc4Page7.GetValue()),
                    "BuildMaxHP":self.check(self.tc5Page7.GetValue()), 
                    "BuildMaxCP":self.check(self.tc6Page7.GetValue()), 
                    "BuildAnnualHeating":self.check(self.tc7Page7.GetValue()), 
                    "BuildAnnualAirCond":self.check(self.tc8Page7.GetValue()), 
                    "BuildDailyDHW":self.check(self.tc9Page7.GetValue()), 
                    "BuildHoursOccup":self.check(self.tc10Page7.GetValue()), 
                    "BuildDaysInUse":self.check(self.tc11Page7.GetValue()), 
                    "BuildHolidaysPeriodStart":self.check(self.tc12_1Page7.GetValue()), 
                    "BuildHolidaysPeriodStop":self.check(self.tc12_2Page7.GetValue()), 
                    "BuildHeatingPeriodStart":self.check(self.tc13_1Page7.GetValue()), 
                    "BuildHeatingPeriodStop":self.check(self.tc13_2Page7.GetValue()), 
                    "BuildAirCondPeriodStart":self.check(self.tc14_1Page7.GetValue()), 
                    "BuildAirCondPeriodStop":self.check(self.tc14_2Page7.GetValue())
                    }

                Status.DB.qbuildings.insert(tmp)               
                Status.SQL.commit()
                self.fillBuildingList()

            elif self.check(self.tc1Page7.GetValue()) <> 'NULL' and len(Status.DB.qbuildings.BuildName[self.tc1Page7.GetValue()].Questionnaire_id[self.activeQid]) == 1:

                tmp = {
                    "BuildName":self.check(self.tc1Page7.GetValue()), 
                    "BuildConstructSurface":self.check(self.tc2Page7.GetValue()), 
                    "BuildUsefulSurface":self.check(self.tc3Page7.GetValue()), 
                    "BuildUsage":self.check(self.tc4Page7.GetValue()),
                    "BuildMaxHP":self.check(self.tc5Page7.GetValue()), 
                    "BuildMaxCP":self.check(self.tc6Page7.GetValue()), 
                    "BuildAnnualHeating":self.check(self.tc7Page7.GetValue()), 
                    "BuildAnnualAirCond":self.check(self.tc8Page7.GetValue()), 
                    "BuildDailyDHW":self.check(self.tc9Page7.GetValue()), 
                    "BuildHoursOccup":self.check(self.tc10Page7.GetValue()), 
                    "BuildDaysInUse":self.check(self.tc11Page7.GetValue()), 
                    "BuildHolidaysPeriodStart":self.check(self.tc12_1Page7.GetValue()), 
                    "BuildHolidaysPeriodStop":self.check(self.tc12_2Page7.GetValue()), 
                    "BuildHeatingPeriodStart":self.check(self.tc13_1Page7.GetValue()), 
                    "BuildHeatingPeriodStop":self.check(self.tc13_2Page7.GetValue()), 
                    "BuildAirCondPeriodStart":self.check(self.tc14_1Page7.GetValue()), 
                    "BuildAirCondPeriodStop":self.check(self.tc14_2Page7.GetValue())
                    }
                q = Status.DB.qbuildings.BuildName[self.tc1Page7.GetValue()].Questionnaire_id[self.activeQid][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillBuildingList()
                          
            else:
                self.showError("BuildingName have to be an uniqe value!")


#------------------------------------------------------------------------------		
#--- Eventhandlers Page 8
#------------------------------------------------------------------------------		

    def OnButtonStoreDataPage8(self, event):
        if self.activeQid <> 0 and len(Status.DB.questionnaire.Questionnaire_ID[self.activeQid]) == 1:            
            tmp = {
                "InflationRate":self.check(self.tc1Page8.GetValue()),
                "FuelPriceRate":self.check(self.tc2Page8.GetValue()),
                "InterestExtFinancing":self.check(self.tc3Page8.GetValue()),
                "PercentExtFinancing":self.check(self.tc4Page8.GetValue()),
                "AmortisationTime":self.check(self.tc5Page8.GetValue()),
                "OMGenTot":self.check(self.tc10_1Page8.GetValue()),
                "OMGenOP":self.check(self.tc10_2Page8.GetValue()),
                "OMGenEP":self.check(self.tc10_3Page8.GetValue()),
                "OMGenFung":self.check(self.tc10_4Page8.GetValue()),
                "OMBuildTot":self.check(self.tc11_1Page8.GetValue()),
                "OMBuildOP":self.check(self.tc11_2Page8.GetValue()),
                "OMBuildEP":self.check(self.tc11_3Page8.GetValue()),
                "OMBiuildFung":self.check(self.tc11_4Page8.GetValue()),
                "OMMachEquipTot":self.check(self.tc12_1Page8.GetValue()),
                "OMMachEquipOP":self.check(self.tc12_2Page8.GetValue()),
                "OMMachEquipEP":self.check(self.tc12_3Page8.GetValue()),
                "OMMachEquipFung":self.check(self.tc12_4Page8.GetValue()),
                "OMHCGenDistTot":self.check(self.tc13_1Page8.GetValue()),
                "OMHCGenDistOP":self.check(self.tc13_2Page8.GetValue()),
                "OMHCGenDistEP":self.check(self.tc13_3Page8.GetValue()),
                "OMHCGenDistFung":self.check(self.tc13_4Page8.GetValue()),
                "OMTotalTot":self.check(self.tc14_1Page8.GetValue()),
                "OMTotalOP":self.check(self.tc14_2Page8.GetValue()),
                "OMTotalEP":self.check(self.tc14_3Page8.GetValue()),
                "OMTotalFung":self.check(self.tc14_4Page8.GetValue())               
                  }                
              
            q = Status.DB.questionnaire.Questionnaire_ID[self.activeQid][0]
            q.update(tmp)
            Status.SQL.commit()


#------------------------------------------------------------------------------		
#--- Eventhandlers DataCheck
#------------------------------------------------------------------------------		
    def OnButtonDataCheck(self, event):
        if self.activeQid <> 0:
            #ret = self.ModBridge.FunctionOneDataCheck(Status.SQL, DB, self.activeQid)
            #self.showInfo("Return of FunctionOneDataCheck %s" %(ret))
            pass
        else:
            self.showError("Select Questionnaire first!")

#------------------------------------------------------------------------------		
#--- Eventhandlers DataCheck
#------------------------------------------------------------------------------		
    def OnEnterHeatPumpPage(self):
        if self.activeQid <> 0:
            #ret = self.ModBridge.StartPageHeatPump(Status.SQL, DB, self.activeQid)
            #self.showInfo("Return of StartPageHeatPump %s" %(ret))
            return 0
        else:
            self.showError("Select Questionnaire first!")
            return 1


#------------------------------------------------------------------------------		
# Auxiliary Functions
#------------------------------------------------------------------------------		

    def hidePages(self):
        self.pageTitle.Hide()
        self.Page0.Hide()
        self.Page1.Hide()
        self.Page2.Hide()
        self.Page3.Hide()
        self.Page4.Hide()
        self.Page5.Hide()
        self.Page6.Hide()
        self.Page7.Hide()
        self.Page8.Hide()
        self.pageDataCheck.Hide()
        self.pageDataCheckPage1.Hide()
        self.pageDataCheckPage2.Hide()
        self.pageStatistics.Hide()
        self.panelEA1.Hide()
        self.panelEA2.Hide()
        self.panelEA3.Hide()
        self.panelEA4.Hide()
        self.panelEA5.Hide()
        self.panelEA6.Hide()
        self.panelEM1.Hide()
        self.pageBenchmarkCheck.Hide()
        #self.pageHeatRecoveryTargets.Hide()
        self.pageOptimisationProposals.Hide()
        self.pageFinalReport.Hide()
        self.pageHeatPump.Hide()
        self.pageBB.Hide()
        self.panelEnergy.Hide()

    def showError(self, message):
        dlg = wx.MessageDialog(None, message, 'Error', wx.OK)
        ret = dlg.ShowModal()
        dlg.Destroy()

    def showInfo(self, message):
        dlg = wx.MessageDialog(None, message, 'Info', wx.OK)
        ret = dlg.ShowModal()
        dlg.Destroy()

    def check(self, value):
        if value <> "" and value <> "None":
            return value
        else:
            return 'NULL'

    def getQuestionnaireList(self):
        self.listBoxQuestionnaresPage0.Clear()
        for n in Status.DB.questionnaire.Name["%"]:
            self.listBoxQuestionnaresPage0.Append (n.Name)

    def fillChoiceOfNaceCodePage1(self):
        self.choiceOfNaceCodePage1.Clear()
        self.choiceOfNaceCodePage1.Append ("None")
        for n in Status.DB.dbnacecode.CodeNACE["%"]:
            self.choiceOfNaceCodePage1.Append (n.CodeNACE)
        self.choiceOfNaceCodePage1.SetSelection(0)

    def fillChoiceOfDBFuelTypePage2(self):
        self.choiceOfDBFuelTypePage2.Clear()
        self.choiceOfDBFuelTypePage2.Append ("None")
        for n in Status.DB.dbfuel.FuelName["%"]:
            self.choiceOfDBFuelTypePage2.Append (n.FuelName)
        self.choiceOfDBFuelTypePage2.SetSelection(0)

    def fillChoiceOfDBUnitOperationPage3(self):
        self.choiceOfDBUnitOperationPage3.Clear()
        self.choiceOfDBUnitOperationPage3.Append ("None")
        for n in Status.DB.dbunitoperation.UnitOperation["%"]:
            self.choiceOfDBUnitOperationPage3.Append (n.UnitOperation)
        self.choiceOfDBUnitOperationPage3.SetSelection(0)

    def fillChoiceOfPMDBFluidPage3(self):
        self.choiceOfPMDBFluidPage3.Clear()
        self.choiceOfPMDBFluidPage3.Append ("None")
        for n in Status.DB.dbfluid.FluidName["%"]:
            self.choiceOfPMDBFluidPage3.Append (n.FluidName)
        self.choiceOfPMDBFluidPage3.SetSelection(0)

    def fillChoiceOfSMDBFluidPage3(self):
        self.choiceOfSMDBFluidPage3.Clear()
        self.choiceOfSMDBFluidPage3.Append ("None")
        for n in Status.DB.dbfluid.FluidName["%"]:
            self.choiceOfSMDBFluidPage3.Append (n.FluidName)
        self.choiceOfSMDBFluidPage3.SetSelection(0)

    def fillChoiceOfDBFuelPage4(self):
        self.choiceOfDBFuelPage4.Clear()
        self.choiceOfDBFuelPage4.Append ("None")
        for n in Status.DB.dbfuel.FuelName["%"]:
            self.choiceOfDBFuelPage4.Append (n.FuelName)
        self.choiceOfDBFuelPage4.SetSelection(0)

    def fillchoiceOfEquipmentPage5(self):
        self.choiceOfEquipmentPage5.Clear()
        self.choiceOfEquipmentPage5.Append("None")
        if self.activeQid <> 0:
            if len(Status.DB.qgenerationhc.Questionnaire_id[self.activeQid]) <> 0:
                for n in Status.DB.qgenerationhc.Questionnaire_id[self.activeQid]:
                    self.choiceOfEquipmentPage5.Append(n.Equipment)
        self.choiceOfEquipmentPage5.SetSelection(0)

    def selectQuestionnaire(self):
        self.activeQid = Status.DB.questionnaire.Name[self.listBoxQuestionnaresPage0.GetStringSelection()][0].Questionnaire_ID
        status.PId = self.activeQid
        self.activeANo = 1
###HS2008-03-11 Test -> ANo should be initialised to zero
        status.ANo = self.activeANo
        
        self.tree.SelectItem(self.qPage1, select=True)
        #self.tc1Page1.SetValue(self.listBoxQuestionnaresPage0.GetStringSelection())
        #self.tc1Page1.SetValue(str(self.activeQid))


#============================================================================== 				
# Routines for clearing and filling questionnaire pages
#==============================================================================

    def clearPage1(self):
        self.tc1Page1.SetValue('')
        self.tc2Page1.SetValue('')
        self.tc9Page1.SetValue('')
        self.tc10Page1.SetValue('')
        self.tc3Page1.SetValue('')
        self.tc4Page1.SetValue('')
        self.tc5Page1.SetValue('')
        self.tc6Page1.SetValue('')
        self.tc7Page1.SetValue('')
        self.tc8Page1.SetValue('')
        self.tc14Page1.SetValue('')
        self.tc15Page1.SetValue('')
        self.tc16Page1.SetValue('')
        self.tc17Page1.SetValue('')
        self.tc18Page1.SetValue('')
        self.tc19Page1.SetValue('')
        self.tc20Page1.SetValue('')
        self.tc21Page1.SetValue('')
        self.tc22Page1.SetValue('')
        self.tc23Page1.SetValue('')
        self.tc24Page1.SetValue('')
        self.tc25_1Page1.SetValue('')
        self.tc25_2Page1.SetValue('')
        self.tc26Page1.SetValue('')
        self.tc27Page1.SetValue('')
        self.tc28Page1.SetValue('')
        self.tc29Page1.SetValue('')
        self.tc30Page1.SetValue('')
        self.tc32Page1.SetValue('')
        self.tc31Page1.SetValue('')
        
        

    def clearPage2(self):
        self.tc2Page2.SetValue('')
        self.tc3Page2.SetValue('')
        self.tc4Page2.SetValue('')
        self.tc5Page2.SetValue('')
        self.tc6Page2.SetValue('')
        self.gridPage2.SetCellValue(1, 3, '')
        self.gridPage2.SetCellValue(1, 1, '')
        self.gridPage2.SetCellValue(1, 0, '')
        self.gridPage2.SetCellValue(1, 2, '')
        self.gridPage2.SetCellValue(0, 3, '')
        self.gridPage2.SetCellValue(0, 0, '')
        self.gridPage2.SetCellValue(0, 1, '')
        self.gridPage2.SetCellValue(0, 2, '')
        self.gridPage2.SetCellValue(0, 4, '')
        self.gridPage2.SetCellValue(0, 5, '')
        self.gridPage2.SetCellValue(8, 0, '')
        self.gridPage2.SetCellValue(8, 1, '')
        self.gridPage2.SetCellValue(8, 2, '')
        self.gridPage2.SetCellValue(8, 3, '')
        self.gridPage2.SetCellValue(8, 4, '')
        self.gridPage2.SetCellValue(8, 5, '')
        self.gridPage2.SetCellValue(2, 3, '')
        self.gridPage2.SetCellValue(2, 1, '')
        self.gridPage2.SetCellValue(2, 0, '')
        self.gridPage2.SetCellValue(2, 2, '')
        self.gridPage2.SetCellValue(2, 5, '')
        self.gridPage2.SetCellValue(3, 3, '')
        self.gridPage2.SetCellValue(3, 1, '')
        self.gridPage2.SetCellValue(3, 0, '')
        self.gridPage2.SetCellValue(3, 2, '')
        self.gridPage2.SetCellValue(3, 5, '')
        self.gridPage2.SetCellValue(4, 3, '')
        self.gridPage2.SetCellValue(4, 1, '')
        self.gridPage2.SetCellValue(4, 0, '')
        self.gridPage2.SetCellValue(4, 2, '')
        self.gridPage2.SetCellValue(4, 5, '')
        self.gridPage2.SetCellValue(5, 3, '')
        self.gridPage2.SetCellValue(5, 1, '')
        self.gridPage2.SetCellValue(5, 0, '')
        self.gridPage2.SetCellValue(5, 2, '')
        self.gridPage2.SetCellValue(5, 5, '')
        
        

    def clearPage3(self):
        self.tc1Page3.SetValue('')
        self.tc2Page3.SetValue('')
        self.tc5Page3.SetValue('')
        self.tc6Page3.SetValue('')
        self.tc7Page3.SetValue('')
        self.tc8Page3.SetValue('')
        self.tc9Page3.SetValue('')
        self.tc10Page3.SetValue('')
        self.tc11Page3.SetValue('')
        self.tc12Page3.SetValue('')
        self.tc13Page3.SetValue('')
        self.tc14Page3.SetValue('')
        self.tc15Page3.SetValue('')
        self.tc16Page3.SetValue('')
        self.tc17Page3.SetValue('')
        self.tc18Page3.SetValue('')
        self.tc19Page3.SetValue('')
        self.tc20Page3.SetValue('')
        self.tc21Page3.SetValue('')
        self.tc23Page3.SetValue('')
        self.tc24Page3.SetValue('')
        self.tc25Page3.SetValue('')
        self.tc26Page3.SetValue('')
        
        

    def clearPage4(self):
        self.tc1Page4.SetValue('')
        self.tc2Page4.SetValue('')
        self.tc3Page4.SetValue('')
        self.tc4Page4.SetValue('')
        self.tc5Page4.SetValue('')
        self.tc6Page4.SetValue('')
        self.tc9Page4.SetValue('')
        self.tc10Page4.SetValue('')
        self.tc11Page4.SetValue('')
        self.tc12Page4.SetValue('')
        self.tc13Page4.SetValue('')
        self.tc14Page4.SetValue('')
        self.tc15Page4.SetValue('')
        self.tc16Page4.SetValue('')
        self.tc17Page4.SetValue('')
        self.tc18Page4.SetValue('')
        self.tc19Page4.SetValue('')
        self.tc20Page4.SetValue('')
        self.tc8Page4.SetValue('')
        
        

    def clearPage5(self):
        self.tc1Page5.SetValue('')
        #self.tc2Page5.SetValue('')
        self.tc3Page5.SetValue('')
        self.tc4Page5.SetValue('')
        self.tc5Page5.SetValue('')
        self.tc6Page5.SetValue('')
        self.tc7Page5.SetValue('')
        self.tc8Page5.SetValue('')
        self.tc9Page5.SetValue('')
        self.tc10Page5.SetValue('')
        self.tc11Page5.SetValue('')
        self.tc12Page5.SetValue('')
        self.tc13Page5.SetValue('')
        self.tc14Page5.SetValue('')
        self.tc15Page5.SetValue('')
        self.tc16Page5.SetValue('')
        self.tc17Page5.SetValue('')
        self.tc18Page5.SetValue('')
        self.tc19Page5.SetValue('')
        
        

    def clearPage6(self):
        self.checkBox1Page6.SetValue(False)
        self.checkBox2Page6.SetValue(False)
        self.checkBox3Page6.SetValue(False)
        self.checkBox4Page6.SetValue(False)
        self.checkBox5Page6.SetValue(False)
        self.tc6_1Page6.SetValue('')
        self.tc6_2Page6.SetValue('')
        self.tc7_1Page6.SetValue('')
        self.tc7_2Page6.SetValue('')
        self.tc8_1Page6.SetValue('')
        self.tc8_2Page6.SetValue('')
        self.tc9_1Page6.SetValue('')
        self.tc9_2Page6.SetValue('')
        self.tc10_1Page6.SetValue('')
        self.tc10_2Page6.SetValue('')
        self.tc11Page6.SetValue('')
        self.tc12Page6.SetValue('')
        self.tc14Page6.SetValue('')
        self.tc15_1Page6.SetValue('')
        self.tc15_2Page6.SetValue('')
        self.tc16Page6.SetValue('')
        self.tc17Page6.SetValue('')
        self.tc18Page6.SetValue('')
        self.tc19Page6.SetValue('')
        self.tc20Page6.SetValue('')
        self.tc21Page6.SetValue('')
        self.tc22Page6.SetValue('')
        self.tc23_1Page6.SetValue('')
        self.tc23_2Page6.SetValue('')
        self.tc24Page6.SetValue('')
        

    def clearPage7(self):
        self.tc1Page7.SetValue('')
        self.tc2Page7.SetValue('')
        self.tc3Page7.SetValue('')
        self.tc4Page7.SetValue('')
        self.tc5Page7.SetValue('')
        self.tc6Page7.SetValue('')
        self.tc7Page7.SetValue('')
        self.tc8Page7.SetValue('')
        self.tc9Page7.SetValue('')
        self.tc10Page7.SetValue('')
        self.tc11Page7.SetValue('')
        self.tc12_1Page7.SetValue('')
        self.tc12_2Page7.SetValue('')
        self.tc13_1Page7.SetValue('')
        self.tc13_2Page7.SetValue('')
        self.tc14_1Page7.SetValue('')
        self.tc14_2Page7.SetValue('')


    def clearPage8(self):
        self.checkBox6Page8.SetValue(False)
        self.checkBox7Page8.SetValue(False)
        self.tc1Page8.SetValue('')
        self.tc2Page8.SetValue('')
        self.tc3Page8.SetValue('')
        self.tc4Page8.SetValue('')
        self.tc5Page8.SetValue('')
        self.tc10_1Page8.SetValue('')
        self.tc10_2Page8.SetValue('')
        self.tc10_3Page8.SetValue('')
        self.tc10_4Page8.SetValue('')
        self.tc11_1Page8.SetValue('')
        self.tc11_2Page8.SetValue('')
        self.tc11_3Page8.SetValue('')
        self.tc11_4Page8.SetValue('')
        self.tc12_1Page8.SetValue('')
        self.tc12_2Page8.SetValue('')
        self.tc12_3Page8.SetValue('')
        self.tc12_4Page8.SetValue('')
        self.tc13_1Page8.SetValue('')
        self.tc13_2Page8.SetValue('')
        self.tc13_3Page8.SetValue('')
        self.tc13_4Page8.SetValue('')
        self.tc14_1Page8.SetValue('')
        self.tc14_2Page8.SetValue('')
        self.tc14_3Page8.SetValue('')
        self.tc14_4Page8.SetValue('')
        

    def fillProductList(self):
        self.listBoxProductsPage1.Clear()
        if len(Status.DB.qproduct.Questionnaire_id[self.activeQid]) > 0:
            for n in Status.DB.qproduct.Questionnaire_id[self.activeQid]:
                self.listBoxProductsPage1.Append (n.Product)


    def fillFuelList(self):
        self.fuelListBoxPage2.Clear()
        if len(Status.DB.qfuel.Questionnaire_id[self.activeQid]) > 0:
            for n in Status.DB.qfuel.Questionnaire_id[self.activeQid]:
                self.fuelListBoxPage2.Append (str(Status.DB.dbfuel.DBFuel_ID[n.DBFuel_id][0].FuelName))


    def fillProcessList(self):
        self.listBoxProcessesPage3.Clear()
        if len(Status.DB.qprocessdata.Questionnaire_id[self.activeQid]) > 0:
            for n in Status.DB.qprocessdata.Questionnaire_id[self.activeQid]:
                self.listBoxProcessesPage3.Append (str(n.Process))

    def fillEquipmentList(self):
        self.listBoxEquipmentListPage4.Clear()
        if len(Status.DB.qgenerationhc.Questionnaire_id[self.activeQid]) > 0:
            for n in Status.DB.qgenerationhc.Questionnaire_id[self.activeQid]:
                self.listBoxEquipmentListPage4.Append (str(n.Equipment))


    def fillDistributionList(self):
        self.listBoxDistributionListPage5.Clear()
        if len(Status.DB.qdistributionhc.Questionnaire_id[self.activeQid]) > 0:
            for n in Status.DB.qdistributionhc.Questionnaire_id[self.activeQid]:
                self.listBoxDistributionListPage5.Append (str(n.Pipeduct))


    def fillBuildingList(self):
        self.listBoxBuildingListPage7.Clear()
        if len(Status.DB.qbuildings.Questionnaire_id[self.activeQid]) > 0:
            for n in Status.DB.qbuildings.Questionnaire_id[self.activeQid]:
                self.listBoxBuildingListPage7.Append (str(n.BuildName))
        
        


    def fillPage(self, page):

        if page == "Page1":
            q = Status.DB.questionnaire.Questionnaire_ID[self.activeQid][0]
            self.tc1Page1.SetValue(str(q.Name))
            self.tc2Page1.SetValue(str(q.City))
            self.tc9Page1.SetValue(str(q.DescripIndustry))
            self.tc10Page1.SetValue(str(q.Branch))
            self.tc3Page1.SetValue(str(q.Contact))
            self.tc4Page1.SetValue(str(q.Role))
            self.tc5Page1.SetValue(str(q.Address))
            self.tc6Page1.SetValue(str(q.Phone))
            self.tc7Page1.SetValue(str(q.Fax))
            self.tc8Page1.SetValue(str(q.Email))
            self.tc14Page1.SetValue(str(q.NEmployees))
            self.tc15Page1.SetValue(str(q.Turnover))
            self.tc16Page1.SetValue(str(q.ProdCost))
            self.tc17Page1.SetValue(str(q.BaseYear))
            self.tc18Page1.SetValue(str(q.Growth))
            self.tc19Page1.SetValue(str(q.Independent))
            self.tc20Page1.SetValue(str(q.OMThermal))
            self.tc21Page1.SetValue(str(q.OMElectrical))
            self.tc22Page1.SetValue(str(q.HPerDayInd))
            self.tc23Page1.SetValue(str(q.NShifts))
            self.tc24Page1.SetValue(str(q.NDaysInd))
            self.tc25_1Page1.SetValue(str(q.NoProdStart))
            self.tc25_2Page1.SetValue(str(q.NoProdStop))
            if q.DBNaceCode_id <> None:
                self.choiceOfNaceCodePage1.SetSelection(self.choiceOfNaceCodePage1.FindString(str(Status.DB.dbnacecode.DBNaceCode_ID[q.DBNaceCode_id][0].CodeNACE)))
            self.fillProductList()


        if page == "Page2":
            if len(Status.DB.qelectricity.Questionnaire_id[self.activeQid]) > 0:
                q = Status.DB.qelectricity.Questionnaire_id[self.activeQid][0]
                self.gridPage2.SetCellValue(1, 3, str(q.PowerContrTot))
                self.gridPage2.SetCellValue(1, 1, str(q.PowerContrStd))
                self.gridPage2.SetCellValue(1, 0, str(q.PowerContrPeak))
                self.gridPage2.SetCellValue(1, 2, str(q.PowerContrVall))
                self.gridPage2.SetCellValue(0, 3, str(q.ElectricityTotYear))
                self.gridPage2.SetCellValue(0, 0, str(q.ElectricityPeakYear))
                self.gridPage2.SetCellValue(0, 1, str(q.ElectricityStandYear))
                self.gridPage2.SetCellValue(0, 2, str(q.ElectricityValleyYear))
                self.gridPage2.SetCellValue(0, 4, str(q.ElGenera))
                self.gridPage2.SetCellValue(0, 5, str(q.ElSales))
                self.gridPage2.SetCellValue(8, 0, str(q.ElectricityRef))
                self.gridPage2.SetCellValue(8, 1, str(q.ElectricityAC))
                self.gridPage2.SetCellValue(8, 2, str(q.ElectricityThOther))
                self.gridPage2.SetCellValue(8, 3, str(q.ElectricityMotors))
                self.gridPage2.SetCellValue(8, 4, str(q.ElectricityChem))
                self.gridPage2.SetCellValue(8, 5, str(q.ElectricityLight))
                self.gridPage2.SetCellValue(2, 3, str(q.ElTariffClassTot))
                self.gridPage2.SetCellValue(2, 1, str(q.ElTariffClassStd))
                self.gridPage2.SetCellValue(2, 0, str(q.ElTariffClassPeak))
                self.gridPage2.SetCellValue(2, 2, str(q.ElTariffClassTotVall))
                self.gridPage2.SetCellValue(2, 5, str(q.ElTariffClassCHP))
                self.gridPage2.SetCellValue(3, 3, str(q.ElTariffPowTot))
                self.gridPage2.SetCellValue(3, 1, str(q.ElTariffPowStd))
                self.gridPage2.SetCellValue(3, 0, str(q.ElTariffPowPeak))
                self.gridPage2.SetCellValue(3, 2, str(q.ElTariffPowVall))
                self.gridPage2.SetCellValue(3, 5, str(q.ElTariffPowCHP))
                self.gridPage2.SetCellValue(4, 3, str(q.ElTariffCTot))
                self.gridPage2.SetCellValue(4, 1, str(q.ElTariffCStd))
                self.gridPage2.SetCellValue(4, 0, str(q.ElTariffCPeak))
                self.gridPage2.SetCellValue(4, 2, str(q.ElTariffCVall))
                self.gridPage2.SetCellValue(4, 5, str(q.ETariffCHP))
                self.gridPage2.SetCellValue(5, 3, str(q.ElCostYearTot))
                self.gridPage2.SetCellValue(5, 1, str(q.ElCostYearStd))
                self.gridPage2.SetCellValue(5, 0, str(q.ElCostYearPeak))
                self.gridPage2.SetCellValue(5, 2, str(q.ElCostYearVall))
                self.gridPage2.SetCellValue(5, 5, str(q.ElSalesYearCHP))
                self.fillFuelList()


        if page == "Page3":
            self.fillProcessList()


        if page == "Page4":
            self.fillEquipmentList()            



        if page == "Page5":
            self.fillDistributionList()


        if page == "Page6":
            if len(Status.DB.qrenewables.Questionnaire_id[self.activeQid]) > 0:
                p = Status.DB.qrenewables.Questionnaire_id[self.activeQid][0]
                if p.REInterest == None:
                    self.checkBox1Page6.SetValue(False)
                else:
                    self.checkBox1Page6.SetValue(bool(p.REInterest))

                if p.EnclBuildGroundSketch == None:
                    self.checkBox5Page6.SetValue(False)
                else:
                    self.checkBox5Page6.SetValue(bool(p.EnclBuildGroundSketch))
                
                self.tc6_1Page6.SetValue(str(p.SurfAreaRoof))
                self.tc6_2Page6.SetValue(str(p.SurfAreaGround))
                self.tc7_1Page6.SetValue(str(p.InclinationRoof))
                self.tc7_2Page6.SetValue(str(p.InclinationGround))
                self.tc8_1Page6.SetValue(str(p.OrientationRoof))
                self.tc8_2Page6.SetValue(str(p.OrientationGround))
                self.tc9_1Page6.SetValue(str(p.ShadingRoof))
                self.tc9_2Page6.SetValue(str(p.ShadingGround))
                self.tc10_1Page6.SetValue(str(p.DistanceToRoof))
                self.tc10_2Page6.SetValue(str(p.DistanceToGround))
                self.tc11Page6.SetValue(str(p.RoofType))
                self.tc12Page6.SetValue(str(p.RoofStaticLoadCap))                
                self.tc14Page6.SetValue(str(p.BiomassFromProc))
                self.tc15_1Page6.SetValue(str(p.PeriodBiomassProcStart))
                self.tc15_2Page6.SetValue(str(p.PeriodBiomassProcStop))
                self.tc16Page6.SetValue(str(p.NDaysBiomassProc))
                self.tc17Page6.SetValue(str(p.QBiomassProcDay))
                self.tc18Page6.SetValue(str(p.SpaceBiomassProc))
                self.tc19Page6.SetValue(str(p.LCVBiomassProc))
                self.tc20Page6.SetValue(str(p.HumidBiomassProc))
                self.tc21Page6.SetValue(str(p.BiomassFromRegion))
                self.tc22Page6.SetValue(str(p.PriceBiomassRegion))
                self.tc23_1Page6.SetValue(str(p.PeriodBiomassRegionStart))
                self.tc23_2Page6.SetValue(str(p.PeriodBiomassRegionStop))
                self.tc24Page6.SetValue(str(p.NDaysBiomassRegion))                

        if page == "Page7":
            self.fillBuildingList()
            


        if page == "Page8":
            q = Status.DB.questionnaire.Questionnaire_ID[self.activeQid][0]
            self.tc1Page8.SetValue(str(q.InflationRate))
            self.tc2Page8.SetValue(str(q.FuelPriceRate))
            self.tc3Page8.SetValue(str(q.InterestExtFinancing))
            self.tc4Page8.SetValue(str(q.PercentExtFinancing))
            self.tc5Page8.SetValue(str(q.AmortisationTime))
            self.tc10_1Page8.SetValue(str(q.OMGenTot))
            self.tc10_2Page8.SetValue(str(q.OMGenOP))
            self.tc10_3Page8.SetValue(str(q.OMGenEP))
            self.tc10_4Page8.SetValue(str(q.OMGenFung))
            self.tc11_1Page8.SetValue(str(q.OMBuildTot))
            self.tc11_2Page8.SetValue(str(q.OMBuildOP))
            self.tc11_3Page8.SetValue(str(q.OMBuildEP))
            self.tc11_4Page8.SetValue(str(q.OMBiuildFung))
            self.tc12_1Page8.SetValue(str(q.OMMachEquipTot))
            self.tc12_2Page8.SetValue(str(q.OMMachEquipOP))
            self.tc12_3Page8.SetValue(str(q.OMMachEquipEP))
            self.tc12_4Page8.SetValue(str(q.OMMachEquipFung))
            self.tc13_1Page8.SetValue(str(q.OMHCGenDistTot))
            self.tc13_2Page8.SetValue(str(q.OMHCGenDistOP))
            self.tc13_3Page8.SetValue(str(q.OMHCGenDistEP))
            self.tc13_4Page8.SetValue(str(q.OMHCGenDistFung))
            self.tc14_1Page8.SetValue(str(q.OMTotalTot))
            self.tc14_2Page8.SetValue(str(q.OMTotalOP))
            self.tc14_3Page8.SetValue(str(q.OMTotalEP))
            self.tc14_4Page8.SetValue(str(q.OMTotalFung))
            
            if q.EnergyManagExisting == None:
                self.checkBox6Page8.SetValue(False)
            else:
                self.checkBox6Page8.SetValue(bool(q.EnergyManagExisting))

            if q.EnergyManagExternal == None:
                self.checkBox7Page8.SetValue(False)
            else:
                self.checkBox7Page8.SetValue(bool(q.EnergyManagExternal))

                
#============================================================================== 				
#------------------------------------------------------------------------------		
#   Application start
#------------------------------------------------------------------------------		
        
if __name__ == '__main__':
    from einstein.modules.interfaces import Interfaces

    Status.PId=2 # just for testing!
    Status.ANo=0

    app = wx.PySimpleApp()
    frame = EinsteinFrame(parent=None, id=-1, title="Einstein")
    interf = Interfaces()       #HS2008-03-22: NT and Nt no longer needed as arguments
#HS2008-03-22 - eliminated:    interf.chargeCurvesQDQA()
    interf = None
    frame.Show(True)
    app.MainLoop()

#==============================================================================
