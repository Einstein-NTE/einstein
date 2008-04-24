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
#	CCheck (Consistency Check)
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Functions for consistency checking of data
#
#==============================================================================
#
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	08/03/2008
#	Last revised by:    Hans Schweiger      17/03/2008
#                           Claudia Vannoni     17/04/2008
#                           Hans Schweiger      18/04/2008
#
#       17/04/2008: CV  Changes in last update: FETFuel
#       18/04/2008: HS  CheckFETel activated
#
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

EPSILON = 1.e-3     # required accuracy for function "isequal"
INFINITE = 1.e99    # numerical value assigned to "infinite"

from math import *
from ccheckFunctions import *
from checkProc import *
from checkEq import *
from checkFETfuel import *
from checkFETel import *

#------------------------------------------------------------------------------
class CCheck():
#------------------------------------------------------------------------------
#   Main class for carrying out consistency checking
#------------------------------------------------------------------------------

    def __init__(self):    
        self.ccEq = []
        self.ccProc = []
        self.ccFETfuel = []
        self.ccFETel = []

    def calculate(self):
        self.NEquip = 2
        for j in range(self.NEquip):
            break
            print "checking equipment no. %s"%j
            self.ccEq.append(CheckEq(j))     # añade un objeto checkEq con todas las variables necesarias a la lista
            self.ccEq[j].check()               # ejecuta la función check para equipo j

        self.NThProc = 2            
        for k in range(self.NThProc):
            print "checking process no. %s"%k
            self.ccProc.append(CheckProc(k))  # añade un objeto checkProc con todas las variables necesarias a la listac
            self.ccProc[k].check()             # ejecuta la función check para proceso k

        self.Nfuels = 3            
        for i in range(self.Nfuels):
            print "checking process no. %s"%i
            self.ccFETfuel.append(CheckFETfuel(i))  # añade un objeto checkProc con todas las variables necesarias a la listac
            self.ccFETfuel[i].check()             # ejecuta la función check para proceso k

        self.ccFETel = CheckFETel()
        self.ccFETel.check
        

#       self.NPipeDuct = 2
#        for m in range(self.NPipeDuct):
#            print "checking pipe/duct no. %s"%m
#            self.ccPipeDuct.append(CheckProc(k))  # añade un objeto checkProc con todas las variables necesarias a la listac
#            self.ccPipeDuct[m].check()             # ejecuta la función check para proceso k

#==============================================================================

if __name__ == "__main__":
    
    CC = CCheck()       # creates an instance of class CCheck
    CC.calculate()
    
#==============================================================================
