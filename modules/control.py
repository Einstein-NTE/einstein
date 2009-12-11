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
#	CONTROL
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Auxiliary functions for the control of execution of the tool
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	    18/06/2008
#
#       Last modified by:   
#
#       Changes to previous version:
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
from einstein.GUI.status import *
from einstein.modules.messageLogger import *
from einstein.GUI.conflictFrame import *
from dialogGauge import DialogGauge

from einstein.modules.energyStats.moduleEA1 import *
from einstein.modules.energyStats.moduleEA2 import *
from einstein.modules.energyStats.moduleEA3 import *
from einstein.modules.energyStats.moduleEA4 import *
from einstein.modules.energyStats.moduleEA5 import *
from einstein.modules.moduleCS import *

from numpy import *
import wx #only needed for the constans ID_OK /ID_CANCEL !!!

#------------------------------------------------------------------------------		
def prepareDataForReport():
#------------------------------------------------------------------------------		
#   calls the functions necessary for writing the report
#------------------------------------------------------------------------------		

    dlg = DialogGauge(Status.main,"Report generation","preparing data")
    
#Title page
    (projectData,generalData) = Status.prj.getProjectData()
    reportTitle = unicode(projectData.Name,"utf-8")
    if projectData.City is not None: reportTitle += u", " + unicode(projectData.City,"utf-8")
    if projectData.Country is not None: reportTitle += u", " + unicode(projectData.Country,"utf-8")
    Status.int.setGraphicsData("TITLE", array([[reportTitle]]))
    print "Control (prepareDataForReport): Title = %s"%(reportTitle.encode("utf-8"))
    print "Type: ",type(reportTitle)
    print Status.int.GData["TITLE"]
    
    Status.prj.setActiveAlternative(0)  #select present state
    
    Status.mod.moduleEA.update()

    dlg.update(10)

#Cap. 2.1 - 2.3
    modEA1 = ModuleEA1(['EA1'])
    modEA1.initModule()

    modEA2 = ModuleEA2(['EA2'])
    modEA2.initPanel()

    modEA3 = ModuleEA3(['EA3_FET','EA3_USH'])
    modEA3.initModule()

    dlg.update(15)

    modEA4 = ModuleEA4(['EA4a_Table','EA4a_Plot'])
    modEA4.updatePanel()   
    modEA4 = ModuleEA4(['EA4b_Table','EA4b_Plot'])
    modEA4.updatePanel()   
    modEA4 = ModuleEA4(['EA4c_Table','EA4c_Plot'])
    modEA4.updatePanel()   

    modEA5 = ModuleEA5(['EA5_EI','EA5_SEC'])
    modEA5.initModule()

    dlg.update(20)


#Cap. 2.4
    Status.mod.moduleBM.initPanel(['BM1'])

    dlg.update(30)

    products = Status.mod.moduleBM.products
    if len(products) > 0:
        Status.mod.moduleBM.product = products[0]
    Status.mod.moduleBM.initPanel(['BM2'])

    dlg.update(40)

    processes = Status.mod.moduleBM.processes
    if len(processes) > 0:
        Status.mod.moduleBM.process = processes[0]
    Status.mod.moduleBM.initPanel(['BM3'])

    dlg.update(50)

#Cap. 3
    Status.mod.moduleA.updatePanel()

    for ANo in range(1,(Status.NoOfAlternatives+1)):
        Status.prj.setActiveAlternative(ANo)

        Status.mod.moduleEA.update()    #calculate for update of CS plots

        Status.mod.moduleHR.initPanel()
        Status.mod.moduleHC.updatePanel()

        dlg.update(50 + 20.0 * ANo / Status.NoOfAlternatives)
    dlg.update(70)
    
#Cap. 4
    modCS = ModuleCS(['CS1_Plot'])
    modCS.updatePanel()
    
    modCS = ModuleCS(['CS2_Plot'])
    modCS.updatePanel()
    
    modCS = ModuleCS(['CS3_Plot'])
    modCS.updatePanel()
    
    modCS = ModuleCS(['CS4_Plot'])
    modCS.updatePanel()
    
    modCS = ModuleCS(['CS5_Plot'])
    modCS.updatePanel()
    
    modCS = ModuleCS(['CS6_Plot'])
    modCS.updatePanel()
    
    modCS = ModuleCS(['CS7_Plot'])
    modCS.updatePanel()

    dlg.update(80)


#Cap. 5 and 6
    
    if Status.FinalAlternative is not None:
        Status.prj.setActiveAlternative(Status.FinalAlternative)
    else:
        Status.prj.setActiveAlternative(0)

    Status.mod.moduleEA.update()

#Chap. 5

    try:
        Status.mod.moduleTCA.runTCAModule()
    except:
        logTrack("prepareDataForReport: error in TCA module")

#Chap. 6.1 - 6.3
    modEA1 = ModuleEA1(['EA1'])
    modEA1.initModule()

    modEA2 = ModuleEA2(['EA2'])
    modEA2.initPanel()

    modEA3 = ModuleEA3(['EA3_FET','EA3_USH'])
    modEA3.initModule()

    modEA4 = ModuleEA4(['EA4a_Table','EA4a_Plot'])
    modEA4.updatePanel()   
    modEA4 = ModuleEA4(['EA4b_Table','EA4b_Plot'])
    modEA4.updatePanel()   
    modEA4 = ModuleEA4(['EA4c_Table','EA4c_Plot'])
    modEA4.updatePanel()   

    modEA5 = ModuleEA5(['EA5_EI','EA5_SEC'])
    modEA5.initModule()

    dlg.update(90)

#Cap. 6.4
    Status.mod.moduleBM.initPanel(['BM1'])

    dlg.update(93)

    products = Status.mod.moduleBM.products
    if len(products) > 0:
        Status.mod.moduleBM.product = products[0]
    Status.mod.moduleBM.initPanel(['BM2'])

    dlg.update(96)

    processes = Status.mod.moduleBM.processes
    if len(processes) > 0:
        Status.mod.moduleBM.process = processes[0]
    Status.mod.moduleBM.initPanel(['BM3'])

    dlg.update(99)

#Summary
    
    modCS = ModuleCS(['Summary'])
    modCS.updatePanel()


    dlg.update(100)
    dlg.Destroy()

#------------------------------------------------------------------------------		
def autoRun(parent):
#------------------------------------------------------------------------------		
#   calls the functions necessary for writing the report
#------------------------------------------------------------------------------		

    logTrack("Control (autoRun): starting")

#..............................................................................
# If there's no data, there's nothing to do ...

    if Status.StatusQ == 0:
        logError("Control (autoRun): sorry, but SOME data have to be filled in before starting")

#..............................................................................
# Consistency check ...

    if Status.StatusCC == 0:
        logMessage("Control (autoRun): starting consistency check")

        showMessage("Control (autoRun): first we start consistency check")

        Status.prj.copyQuestionnaire()
        nc = Status.mod.moduleCC.basicCheck()

        if nc > 0:
            checkOK = False
            if Status.UserInteractionLevel in ["semi-automatic","interactive"]:
                Status.mod.moduleCC.updatePanel()
                cf = conflictFrame(parent)
                cf.Show()
            else:
                showMessage("Control (autoRun): data conflicts detected.\n"+\
                            "Don't know yet what to do in this case, as I'm in automatic mode")
            Status.main.tree.SelectItem(Status.main.qCC,select=True)

        nc = Status.mod.moduleCC.basicCheck(estimate=True)

        if nc > 0:
            checkOK = False
            if Status.UserInteractionLevel in ["semi-automatic","interactive"]:
                Status.mod.moduleCC.updatePanel()
                cf = conflictFrame(parent)
                cf.Show()
            else:
                showMessage("Control (autoRun): data conflicts detected.\n"+\
                            "Don't know yet what to do in this case, as I'm in automatic mode")
            Status.main.tree.SelectItem(Status.main.qCC,select=True)
                   
        else:
            checkOK = True
            showMessage("Control (autoRun): congratulations. data are consistent.\n"+\
                        "now let's continue calculating some energy balances")
            
            Status.prj.setActiveAlternative(0,checked = True)
            Status.mod.moduleEA.update()
            Status.main.tree.SelectItem(Status.main.qEA4a, select=True)

    else:
        logTrack("Control (autoRun): project already checked")

    Status.mod.moduleEA.update()
    Status.main.tree.SelectItem(Status.main.qEA4b, select=True)


    if Status.NoOfAlternatives >= 5:
            showMessage("You already have a lot of alternative proposals in your study"+\
                        "Delete some of them and then call me again ...")
            return
        
#..............................................................................
# Benchmarking

    pass #for the future

#..............................................................................
# Now let's create some alternative proposals

#..............................................................................
# Alternative proposal 1: Heat recovery only

    ret = askConfirmation("First let's test the remaining heat recovery potential (Alternative 1)\n"+\
                          "The result will be used as base for system optimisation")
    
    if ret == wx.ID_NO:
        ret = askConfirmation("Do You want to interrupt the auto-design ?")
        if ret == wx.ID_YES:
            return

    shortName = "Heat recovery (HR)"
    description = "EINSTEIN default design of heat recovery system"
    basedOn = 0
        
    Status.prj.createNewAlternative(basedOn,shortName,description)

    if Status.HRTool == "PE2":
        Status.mod.moduleHR.runHRDesign()
    else:
        Status.mod.moduleHR.runHRModule()

# Finally check the boiler dimensioning for the remaining heat demand
#    Status.mod.moduleBB.designAssistant()

    Status.mod.moduleEA.update()
    Status.main.tree.SelectItem(Status.main.qEA4b, select=True)

#..............................................................................
# Alternative proposal 2: Heat recovery + solar system

    ret = askConfirmation("Now let's try to install a solar system (Alternative 2)\n")

    if ret == wx.ID_NO:
        ret = askConfirmation("Do You want to interrupt the auto-design ?")
        if ret == wx.ID_YES:
            return
    
    shortName = "Solar thermal"
    description = "EINSTEIN default design of a solar thermal system"
    basedOn = 1
        
    Status.prj.createNewAlternative(basedOn,shortName,description)

    Status.mod.moduleHR.runHRModule()

    Status.mod.moduleST.initPanel()
    Status.mod.moduleST.updatePanel()
    Status.int.GData.update({'ST Config':[50.,"<any>",300.0]})
    Status.mod.moduleST.setUserDefinedPars()
    Status.mod.moduleST.designAssistant1()
    
    Status.mod.moduleST.updatePanel()

    Status.mod.moduleBB.initPanel() #preparation sequence of HP Module
    Status.mod.moduleBB.updatePanel()

    Status.mod.moduleBB.designAssistant()
    Status.mod.moduleBB.updatePanel()

    Status.mod.moduleEA.update()
    Status.main.tree.SelectItem(Status.main.qST, select=True)

#..............................................................................
# Alternative proposal 3: Heat recovery + heat pump

    ret = askConfirmation("Now let's try to install a heat pump (Alternative 3)\n")
    
    if ret == wx.ID_NO:
        ret = askConfirmation("Do You want to interrupt the auto-design ?")
        if ret == wx.ID_YES:
            return

    shortName = "Heat pump"
    description = "EINSTEIN default design of a heat pump based system"
    basedOn = 1
        
    Status.prj.createNewAlternative(basedOn,shortName,description)

    Status.mod.moduleHP.initPanel() #preparation sequence of HP Module
    Status.mod.moduleHP.updatePanel()

    (mode,HPList) = Status.mod.moduleHP.designAssistant1()

    if len(HPList) > 0:  
        HPId = HPList[0]    #in automatic mode just take first in the list
        logMessage(_("Control (autoRun): %s possible HP models found")%len(HPList))
    else:
        HPId = -1
        logMessage(_("Control (autoRun): no heat pump application possible"))
    
    Status.mod.moduleHP.designAssistant2(HPId)
    Status.mod.moduleHP.updatePanel()

# Finally check the boiler dimensioning for the remaining heat demand

    Status.mod.moduleBB.initPanel() #preparation sequence of HP Module
    Status.mod.moduleBB.updatePanel()

    Status.mod.moduleBB.designAssistant()
    Status.mod.moduleBB.updatePanel()

    Status.mod.moduleEA.update()
    Status.main.tree.SelectItem(Status.main.qHP, select=True)

#..............................................................................
# Alternative proposal 4: New boiler cascade

    ret = askConfirmation("Now let's try to install a new boiler cascade (Alternative 4)\n")
    
    if ret == wx.ID_NO:
        ret = askConfirmation("Do You want to interrupt the auto-design ?")
        if ret == wx.ID_YES:
            return

    shortName = "Boiler cascade"
    description = "EINSTEIN default design of a new boiler cascade"
    basedOn = 1
        
    Status.prj.createNewAlternative(basedOn,shortName,description)

    Status.mod.moduleBB.initPanel() #preparation sequence of HP Module
    Status.mod.moduleBB.updatePanel()

    Status.mod.moduleBB.designAssistant()
    Status.mod.moduleBB.updatePanel()

# Finally check the boiler dimensioning for the remaining heat demand

#    Status.mod.moduleBB.designAssistant()

    Status.mod.moduleEA.update()
    Status.main.tree.SelectItem(Status.main.qBB, select=True)

#..............................................................................
# Alternative proposal 5: And now lets mix up everything

    ret = askConfirmation("Now let's try to combine everything (Alternative 5)\n")
    
    if ret == wx.ID_NO:
        ret = askConfirmation("Do You want to interrupt the auto-design ?")
        if ret == wx.ID_YES:
            return

    shortName = "EINSTEIN Super Mix"
    description = "EINSTEIN default design of a new boiler cascade"
    basedOn = 3
        
    Status.prj.createNewAlternative(basedOn,shortName,description)

    Status.mod.moduleST.initPanel()
    Status.mod.moduleST.updatePanel()
    Status.int.GData.update({'ST Config':[50.,"<any>",300.0]})
    Status.mod.moduleST.setUserDefinedPars()
    Status.mod.moduleST.designAssistant1()
    
    Status.mod.moduleST.updatePanel()

    Status.mod.moduleBB.initPanel() #preparation sequence of HP Module
    Status.mod.moduleBB.updatePanel()

    Status.mod.moduleBB.designAssistant()
    Status.mod.moduleBB.updatePanel()

    Status.mod.moduleEA.update()
#    Status.main.tree.SelectItem(Status.main.qEA3, select=True)

#..............................................................................
# End of the journey

    Status.main.tree.SelectItem(Status.main.qCS1, select=True)
    
    showMessage("We arrived at the end of the journey\n"+\
                "Have a look on the results ...")
    

#============================================================================== 
