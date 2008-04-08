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
#	Version No.: 0.02
#	Created by: 	    Hans Schweiger	03/04/2008
#	Revised by:         Hans Schweiger      08/04/2008
#
#       Changes in last update:
#       08/04/08    Benchmark module included
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

from einstein.modules.moduleBM import ModuleBM
from einstein.modules.moduleA import ModuleA
from einstein.modules.energy.moduleEnergy import ModuleEnergy
from einstein.modules.moduleHC import ModuleHC
from einstein.modules.heatPump.moduleHP import ModuleHP
from einstein.modules.boiler.moduleBB import ModuleBB

class Modules(object):
    
#------------------------------------------------------------------------------		
    def __init__(self):
#------------------------------------------------------------------------------		
        keys = ['BM Table'] 
        print "Modules (__init__): BM - starting"
        self.moduleBM = ModuleBM(keys)
        print "Modules (__init__): BM",self.moduleBM
        
        keys = ['A Table'] 
        print "Modules (__init__): A - starting"
        self.moduleA = ModuleA(keys)
        print "Modules (__init__): A",self.moduleA
        
        keys = ['ENERGY'] 
        print "Modules (__init__): energy - starting"
        self.moduleEnergy = ModuleEnergy(keys)
        print "Modules (__init__): energy",self.moduleEnergy

        keys = ['HC Table'] 
        print "Modules (__init__): HC - starting"
        self.moduleHC = ModuleHC(keys)
        print "Modules (__init__): HC",self.moduleHC
        
        keys = ['HP Table'] 
        print "Modules (__init__): HP - starting"
        self.moduleHP = ModuleHP(keys)
        print "Modules (__init__): HP",self.moduleHP
        
        keys = ['BB Table'] 
        print "Modules (__init__): BB - starting"
        self.moduleBB = ModuleBB(keys)
        print "Modules (__init__): energy",self.moduleBB
       
#------------------------------------------------------------------------------		
