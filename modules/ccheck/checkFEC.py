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
#	Version No.: 0.02
#	Created by: 	    Claudia Vannoni	10/04/2008
#	Last revised by:    Claudia Vannoni      10/04/2008
#
#       Changes in last update:
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

#------------------------------------------------------------------------------
class CheckFEC():
#------------------------------------------------------------------------------
#   Carries out consistency checking for fuel i
#------------------------------------------------------------------------------


    def __init__(self,i):     #function that is called at the beginning when object is created

# assign a variable to all intermediate values needed
        
        self.TOpProc1 = CCPar("TOpProc1") 
        

        self.import_data(i)

    def import_data(self,k):  #later on should import data from SQL. now simply sets to some value

# Old Step 0: Assign all a priori known values to variables.
#   -> here manually. in tool values substituted by import from SQL

        self.FluidCp = 0.001 # kWh/K*Kg # IMPORT Constant from the FluidDB
        self.FluidDensity = 1.03 # Kg/m3 # IMPORT Constant from the FluidDB
        

        self.PTInFlow = CCPar("PTInFlow")
        self.PTInFlow.val = 4
        self.PTInFlow.sqerr = 0.0

        

        #self.showAllUPH()

    def showAllFEC(self):
        
        print "====================="

        self.UPH.show()
        
                
        print "====================="
    
    def check(self):     #function that is called at the beginning when object is created
        for n in range(4):

            print "-------------------------------------------------"
            print "Ciclo %s"%n
            print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

            print "Step 1: calculating from left to right (CALC)"
            
            self.TOpProc1 = calcProd("TOpProc1",self.NDaysProc,self.HPerDayProc)
            self.DTLoss1 = calcDiff("DTLoss1",self.PT,self.TEnvProc)
            self.QOpProc1 = calcSum("QOpProc1",self.UAProc,self.QEvapProc)
            self.UPHcdotGross1 = calcFlow("UPHcdotGross1",self.FluidCp,self.VInFlowDay,self.PT,self.PTInFlow,self.DTUPHcGross)
            self.UPH1 = calcSum3("UPH1",self.UPHm,self.UPHc,self.UPHs)
                      
            #self.showAllFEC()

# Step 2: Cross check the variables

            print "Step 2: cross checking"

            ccheck1(self.TOpProc,self.TOpProc1)
            ccheck2(self.QHXdotProcInt,self.QHXdotProcInt1,self.QHXdotProcInt2)
                        

            #self.showAllFEC()
# Step 3: Adjust the variables (inverse of calculation routines)

            print "Step 3: calculating from right to left (ADJUST)"

            adjustSum(self.UPH2,self.UPHProc,self.QHXProc)
    #        adjustSum3(self.UPH1,self.UPHm,self.UPHc,self.UPHs)
            adjustProd(self.UPHs1,self.UPHsdot1,self.NBatchPerYear)
            adjustFlow(self.UPHsdot1,(self.FluidCp*self.FluidDensity),self.VolProcMed,self.PT,self.PTStartUp,self.DTUPHs)
            adjustDiff(self.DTLoss1,self.PT,self.TEnvProc)
                        
            #self.showAllFEC()
           
        self.UPHcGross = calcProd("UPHcGross",self.UPHcdotGross,self.NDaysProc)# Not adjusted
        self.QHXProcInt = calcProd("QHXProcInt",self.QHXdotProcInt,self.NDaysProc) # Not adjusted 

    #añadido este último show all. sino no se ven los ultimos dos resultados ...
        self.showAllFEC()


#==============================================================================
