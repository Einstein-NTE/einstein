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
#	MODULES
#			
#------------------------------------------------------------------------------
#			
#	Instances of modules for global access
#
#==============================================================================
#
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	03/04/2008
#	Revised by:         Hans Schweiger      08/04/2008
#                           Hans Schweiger      10/06/2008
#                           Hans Schweiger      18/06/2008
#
#       Changes in last update:
#       08/04/08    Benchmark module included
#       10/06/08    HR module added
#       18/06/08    EA module added
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

from einstein.modules.ccheck.moduleCC import ModuleCC
from einstein.modules.moduleBM import ModuleBM
from einstein.modules.moduleA import ModuleA
from einstein.modules.energy.moduleEnergy import ModuleEnergy
from einstein.modules.moduleHR import ModuleHR
from einstein.modules.moduleHC import ModuleHC
from einstein.modules.chp.moduleCHP import ModuleCHP
from einstein.modules.solar.moduleST import ModuleST
from einstein.modules.heatPump.moduleHP import ModuleHP
from einstein.modules.boiler.moduleBB import ModuleBB
from einstein.modules.energyStats.moduleEA import ModuleEA
from einstein.modules.moduleTCA import ModuleTCA
from einstein.modules.modulePO import ModulePO
from einstein.modules.messageLogger import *

class Modules(object):
    
#------------------------------------------------------------------------------		
    def __init__(self):
#------------------------------------------------------------------------------		

        logDebug("Modules (__init__): creating module instances")

        self.moduleCC = ModuleCC()
        
        keys = ['BM Table'] 
        self.moduleBM = ModuleBM(keys)
        
        keys = ['A Table'] 
        self.moduleA = ModuleA(keys)
        
        keys = ['ENERGY','ENERGY Plot1'] 
        self.moduleEnergy = ModuleEnergy(keys)

        keys = ['HR Table'] 
        self.moduleHR = ModuleHR(keys)
        
        keys = ['HC Table'] 
        self.moduleHC = ModuleHC(keys)
        
        keys = ['CHP Table'] 
        self.moduleCHP = ModuleCHP(keys)

        keys = ['ST Table'] 
        self.moduleST = ModuleST(keys)
        
        keys = ['HP Table'] 
        self.moduleHP = ModuleHP(keys)
        
        keys = ['BB Table'] 
        self.moduleBB = ModuleBB(keys)

        self.moduleEA = ModuleEA()
       
        keys = ["TCA","TCA_UNVIABLE","TCA_CRITERIA","TCA_RATING"]
        self.moduleTCA = ModuleTCA(keys)

        keys = []
        self.modulePO = ModulePO(keys)
#------------------------------------------------------------------------------		
