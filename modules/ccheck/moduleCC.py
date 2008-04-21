# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleCC (consistency check module)
#			
#------------------------------------------------------------------------------
#			
#	
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by:         Claudia Vannoni     20/04/2008
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

from sys import *
from math import *
from numpy import *

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP

from checkMatrix import *
from checkProc import *
from checkEq import *
from checkFETfuel import *
from checkFETel import *

class ModuleCC(object):
    
#------------------------------------------------------------------------------
    def __init__(self):
#------------------------------------------------------------------------------
#   basic initialisation at the start-up of the tool
#------------------------------------------------------------------------------

        self.keys = "CC" # the key to the data is sent by the panel

        self.DB = Status.DB
        self.sql = Status.SQL

#..............................................................................
# creates an empty space for the different check-blocks

        self.ccFET = []
        self.NFET = 0
        
        self.ccEq = []
        self.NEquipe = 0
        
        self.ccProc = []
        self.NProc = 0
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#   is called at entering the CC panel
#------------------------------------------------------------------------------

        self.updatePanel()
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#   function that updates the information on the CC panel on the GUI
#------------------------------------------------------------------------------

        CCList =["some text","dont know what to display at the GUI","???"]
            
        data = array(CCList)
        Status.int.setGraphicsData(self.keys[0], data)  #sends the data to the GUI

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def getQuestionnaireData(self):
#------------------------------------------------------------------------------
#   function that gets the data from the questionnaire
#------------------------------------------------------------------------------

#   should define the same data set as getTestData, but taking the values from
#   the questionnaire.

        pass
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def getTestData(self):
#------------------------------------------------------------------------------
#   function that substitutes getQuestionnaireData for testing purposes
#   independent of SQL
#------------------------------------------------------------------------------

#..............................................................................
# import data on fuel and electricity consumption (FET)

        self.NFET = 2
        NI = self.NFET
        self.FETi = CCRow("FETi",NI)

        self.ccFET.append(CheckFETel())     
        for i in range(1,NI):      
            self.ccFET.append(CheckFETfuel(i))

#..............................................................................
# import data on existing equipment 

        self.NEquipe = 2
        NJ = self.NEquipe
        self.USHj = CCRow("USHj",NJ)     #note: this is a ROW of USH values, and not identical with the USHj variable within checkEq !!!
        self.FETj = CCRow("FETj",NJ)     #creates the space for intermediate storge towards matrix

        for j in range(NJ):
            self.ccEq.append(CheckEq(j))     # añade un objeto checkEq con todas las variables necesarias a la lista

#..............................................................................
# import data on existing processes

        self.NThProc = 3
        NK = self.NThProc
        self.UPHk = CCRow("UPHk",NK)     #note: this is a ROW of USH values, and not identical with the USHj variable within checkEq !!!
        self.QHXk = CCRow("QHXk",NK)     #creates the space for intermediate storge towards matrix

        for k in range(NK):
            self.ccProc.append(CheckProc(k))  # añade un objeto checkProc con todas las variables necesarias a la listac

#..............................................................................
# import data on link of fuels and equipment

        FETLink = arange(NI*NJ).reshape(NJ,NI)  # reshape(rows,cols)
        
        FETLink[0][0] = 0
        FETLink[1][0] = 0
        FETLink[0][1] = 1
        FETLink[1][1] = 1

        self.FETMatrix = CheckMatrix("FET Matrix",self.FETi,self.FETj,FETLink)

#..............................................................................
# import data on link of equipment and processes

        UPHLink = arange(NJ*NK).reshape(NK,NJ)  # reshape(rows,cols)

        UPHLink[0][0] = 1
        UPHLink[1][0] = 0
        UPHLink[2][0] = 0
        UPHLink[0][1] = 1
        UPHLink[1][1] = 1
        UPHLink[2][1] = 1

        self.UPHMatrix = CheckMatrix("UPH Matrix",self.USHj,self.UPHk,UPHLink)   


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def basicCheck(self):
#------------------------------------------------------------------------------
#   runs the first basic Check
#   (basic = still without estimation procedures for missing data)
#------------------------------------------------------------------------------

#        cycle = Status.cycle.initCycle()
#        while not cycle.converged():

        if DEBUG in ["ALL","BASIC"]:
            print "===================================================="
            print "ModuleCC: getting Test data"
            print "===================================================="
        
        self.getTestData()
        
        if DEBUG in ["ALL","BASIC"]:
            print "===================================================="
            print "ModuleCC: starting cycle"
            print "===================================================="
        
        NCycles = 100
        for cycle in range(NCycles):
#..............................................................................
# Step 1: do an independent checking of all the blocks as initialisation
#         (saves computing time for the start-up of the matrix-algorithm)

#..............................................................................
# check of fuel and electricity consumption (FEC)

            if DEBUG in ["ALL","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking fuels (FET)"
                print "===================================================="

            NI = self.NFET
            
            print "checking electricity consumption"
            self.ccFET[0].check()
            self.FETi[0].update(self.ccFET[0].FETel)

            for i in range(1,NI):       #then check all the Nfuels = NI-1 fuels

                print "checking fuel no. %s"%i
                self.ccFET[i].check()
                self.FETi[i].update(self.ccFET[i].FETFuel)
            
#..............................................................................
# check of equipment

            if DEBUG in ["ALL","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking equipment (USH)"
                print "===================================================="

            NJ = self.NEquipe

            for j in range(NJ):
                print "checking equipment no. %s"%j
                self.ccEq[j].check()               # ejecuta la función check para equipo j

                self.USHj[j].update(self.ccEq[j].USH)      #obtain results 
                self.FETj[j].update(self.ccEq[j].FETj)
        
#..............................................................................
# check of pipes and ducts
#       self.NPipeDuct = 2
#        for m in range(self.NPipeDuct):
#            print "checking pipe/duct no. %s"%m
#            self.ccPipeDuct.append(CheckProc(k))  # añade un objeto checkProc con todas las variables necesarias a la listac
#            self.ccPipeDuct[m].check()             # ejecuta la función check para proceso k


#..............................................................................
# check of thermal processes

            if DEBUG in ["ALL","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking processes (UPH)"
                print "===================================================="

            NK = self.NThProc

            for k in range(self.NThProc):
                print "checking process no. %s"%k
                self.ccProc[k].check()             # ejecuta la función check para proceso k

                self.UPHk[k].update(self.ccProc[k].UPH)      #obtain results 

#..............................................................................
# Step 2: now check the link of all the blocks via the matrix checking function

#..............................................................................
# link of fuels and equipment

            self.FETMatrix.check()

            self.ccFET[0].FETel.update(self.FETi[0])
            for i in range(1,NI):
                self.ccFET[i].FETFuel.update(self.FETi[i])

            for j in range(NJ):
                self.ccEq[j].FETj.update(self.FETj[j])

        
#..............................................................................
# link of equipment and processes

            self.UPHMatrix.check()

            for j in range(NJ):
                self.ccEq[j].USH.update(self.USHj[j])

            for k in range(1,NK):
                self.ccProc[k].UPH.update(self.UPHk[k])

#==============================================================================

if __name__ == "__main__":

    CC = ModuleCC()       # creates an instance of class CCheck
    CC.basicCheck()
