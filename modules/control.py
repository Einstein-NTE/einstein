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

#------------------------------------------------------------------------------		
def prepareDataForReport():
#------------------------------------------------------------------------------		
#   calls the functions necessary for writing the report
#------------------------------------------------------------------------------		

    Status.mod.moduleEA.update()
    print "Control (prepareData): here I should do something more ..."

#### opci�n 1 llamar a initPanels de los m�dulos CS y EA

    #mod = ModuleCS(["La Llave que toca"])
    #mod.initPanel()    #as� el m�dulo te deja en GData exactamente lo mismo
    #                   #como si manualmente abrir�as el panel
    # para que esto funcione, tienes que poner arriba:
    #   from einstein.modules.moduleCS import ModuleCS

#### opci�n 2 llamar a initPanels de m�dulos que est�n en Status.mod (modules.py)

    #Status.mod.moduleHP.initPanel() #te hace lo mismo como si manualmente abrir�as el PanelHP
    #Status.mod.moduleHP.updatePanel() 

#### opci�n 3 escribir algo manualmente a GData:

    mis_datos = [["uno","dos","tres","cuatro","cinco"],
                 [8,3,2,5,9]]

    Status.int.GData["MyKey"] = mis_datos #(o = copy.deepcopy(mis_datos), si estos se pueden modificar en otro sitio
    print "Control (prepareDataForReport): GData[%s]:\n%s"%("MyKey",Status.int.GData["MyKey"])

    # equivalente a

    Status.int.setGraphicsData('MyKey',mis_datos)


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

    showMessage("First let's test the remaining heat recovery potential (Alternative 1)\n"+\
                "The result will be used as base for system optimisation")
    
    shortName = "Heat recovery (HR)"
    description = "EINSTEIN default design of heat recovery system"
    basedOn = 0
        
    Status.prj.createNewAlternative(basedOn,shortName,description)

    Status.mod.moduleHR.simulateHR()

# Finally check the boiler dimensioning for the remaining heat demand
#    Status.mod.moduleBB.designAssistant()

    Status.mod.moduleEA.update()
    Status.main.tree.SelectItem(Status.main.qEA4b, select=True)

#..............................................................................
# Alternative proposal 2: Heat recovery + solar system

    showMessage("Now let's try to install a solar system (Alternative 2)\n"+\
                "In the present Version, a fixed size of 500 kW will be the first try")
    
    shortName = "Solar thermal"
    description = "EINSTEIN default design of a solar thermal system"
    basedOn = 1
        
    Status.prj.createNewAlternative(basedOn,shortName,description)

    Status.mod.moduleHR.simulateHR()

    Status.mod.moduleST.initPanel()
    Status.mod.moduleST.updatePanel()
#    Status.mod.moduleST.designAssistant1()
    
    equipe = Status.mod.moduleST.addEquipmentDummy()
    equipe.HCGPnom = 500.0
    equipe.ST_SysEff = 0.9
    equipe.ST_Volume = 25.0
    equipe.ST_C0 = 0.80
    equipe.ST_C1 = 3.80
    equipe.ST_C2 = 0.01
    equipe.ST_K50L = 0.95
    equipe.ST_K50T = 0.95
    Status.SQL.commit()

#    Status.int.GData.update({'ST SysPars':[500.,0.9,25.0]})
#    Status.mod.moduleST.setSolarSystemPars()

    Status.mod.moduleST.updatePanel()

#    Status.mod.moduleBB.designAssistant()

    Status.mod.moduleEA.update()
    Status.main.tree.SelectItem(Status.main.qST, select=True)

#..............................................................................
# Alternative proposal 3: Heat recovery + heat pump

    showMessage("Now let's try to install a heat pump (Alternative 3)\n")
    
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

#    Status.mod.moduleBB.designAssistant()

    Status.mod.moduleEA.update()
    Status.main.tree.SelectItem(Status.main.qHP, select=True)

#..............................................................................
# Alternative proposal 4: New boiler cascade

    showMessage("Now let's try to install a new boiler cascade (Alternative 4)\n")
    
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

    showMessage("Now let's try to combine everything (Alternative 5)\n")
    
    shortName = "EINSTEIN Super Mix"
    description = "EINSTEIN default design of a new boiler cascade"
    basedOn = 3
        
    Status.prj.createNewAlternative(basedOn,shortName,description)

    Status.mod.moduleST.initPanel()
    Status.mod.moduleST.updatePanel()
    
    equipe = Status.mod.moduleST.addEquipmentDummy()
    equipe.HCGPnom = 500.0
    equipe.ST_SysEff = 0.9
    equipe.ST_Volume = 25.0
    equipe.ST_C0 = 0.80
    equipe.ST_C1 = 3.80
    equipe.ST_C2 = 0.01
    equipe.ST_K50L = 0.95
    equipe.ST_K50T = 0.95
    Status.SQL.commit()

#    Status.int.GData.update({'ST SysPars':[500.,0.9,25.0]})
#    Status.mod.moduleST.setSolarSystemPars()

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
