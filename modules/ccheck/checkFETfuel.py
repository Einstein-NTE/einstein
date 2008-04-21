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
#	Version No.: 0.01
#	Created by: 	    Claudia Vannoni	10/04/2008
#	Last revised by:    Claudia Vannoni      17/04/2008
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
class CheckFETfuel():
#------------------------------------------------------------------------------
#   Carries out consistency checking for fuel i
#------------------------------------------------------------------------------


    def __init__(self,i):     #function that is called at the beginning when object is created

# assign a variable to all intermediate values needed

        self.FETFuel = CCPar("FETFuel")
        self.FETFuel1 = CCPar("FETFuel1") 
        self.FECFuel1 = CCPar("FECFuel1") 
        
        if TEST:
            self.importTestData(i)
        else:
#            self.importData()
            pass

    def importTestData(self,i):  #later on should import data from SQL. now simply sets to some value

        if TESTCASE == 2:       #original test case Kla - first version of FECel
            self.FuelLCV = 10 # kWh/unit # IMPORT Constant from the FuelDB
                    
            self.FECFuel = CCPar("FECFuel")
            self.FECFuel.val = 600
            self.FECFuel.sqerr = 0.0101

            self.MFuelYear = CCPar("MFuelYear")
            self.MFuelYear.val = 55
            self.MFuelYear.sqerr = 0.01

            self.FEOFuel = CCPar("FEOFuel") #FEOfuel assigned only here=0: missed in the questionnaire but present in the list of the parameters
            self.FEOFuel.val = 0
            self.FEOFuel.sqerr = 0.0

        elif TESTCASE == 3:       #global checking of algorithm
            self.FuelLCV = 10 # kWh/unit # IMPORT Constant from the FuelDB
                    
            self.FECFuel = CCPar("FECFuel")
            self.FECFuel.val = 10000
            self.FECFuel.sqerr = 0.001

            self.MFuelYear = CCPar("MFuelYear")
            self.MFuelYear.val = 1000
            self.MFuelYear.sqerr = 0.001

            self.FEOFuel = CCPar("FEOFuel") #FEOfuel assigned only here=0: missed in the questionnaire but present in the list of the parameters
            self.FEOFuel.val = 0
            self.FEOFuel.sqerr = 0.0
        else:
            print "CheckFETfuel: WARNING - don't have input data for this test case no. ",TESTCASE

        if DEBUG in ["ALL"]:
            self.showAllFETfuel()

    def showAllFETfuel(self):
        
        print "====================="

        self.FETFuel.show()
        self.FETFuel1.show()
        self.FECFuel1.show()
        self.FECFuel.show()
        self.MFuelYear.show()
        self.FEOFuel.show()
                
        print "====================="
    
    def check(self):     #function that is called at the beginning when object is created
        for n in range(10):
            if DEBUG in ["ALL"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence
            if DEBUG in ["ALL"]:
                print "Step 1: calculating from left to right (CALC)"
            
            self.FECFuel1 = calcK("FECFuel1",self.FuelLCV,self.MFuelYear)
            self.FETFuel1 = calcDiff("FETFuel1",self.FECFuel,self.FEOFuel)
            
            if DEBUG in ["ALL"]:          
                self.showAllFETfuel()

# Step 2: Cross check the variables

            if DEBUG in ["ALL"]:
                print "Step 2: cross checking"

            ccheck1(self.FETFuel,self.FETFuel1)
            ccheck1(self.FECFuel,self.FECFuel1)
                                    
            if DEBUG in ["ALL"]:
                self.showAllFETfuel()
                
# Step 3: Adjust the variables (inverse of calculation routines)

            if DEBUG in ["ALL"]:
                print "Step 3: calculating from right to left (ADJUST)"

            adjustDiff(self.FETFuel1,self.FECFuel,self.FEOFuel)
            adjustcalcK(self.FECFuel1,self.FuelLCV,self.MFuelYear)
                        
            if DEBUG in ["ALL"]:
                self.showAllFETfuel()
                

# Step 4: Second cross check the variables: added in order to provisionally solve the calcDiff/adjustDiff problem

            if DEBUG in ["ALL"]:
                print "Step 4: cross checking"

            ccheck1(self.FETFuel,self.FETFuel1)
            ccheck1(self.FECFuel,self.FECFuel1)
                                    
            if DEBUG in ["ALL"]:
                self.showAllFETfuel()
                
        
    #añadido este último show all. sino no se ven los ultimos dos resultados ...
        if DEBUG in ["ALL","BASIC"]:
            self.showAllFETfuel()


#==============================================================================

if __name__ == "__main__":
    
    ccFETfuel = CheckFETfuel(0)       # creates an instance of class CCheck
    ccFETfuel.check()
