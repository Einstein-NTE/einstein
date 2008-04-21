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
#	Last revised by:    Claudia Vannoni     7/04/2008
#                           Claudia Vannoni     16/04/2008
#                           Hans Schweiger      20/04/2008
#       Changes in last update:
#                               sqerr NONE eliminated
#       20/04/2008: HS  Variable HCGTEfficiency1 added. 2nd cross check
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
class CheckEq():
#------------------------------------------------------------------------------
#   Carries out consistency checking for equipe j
#------------------------------------------------------------------------------

    def __init__(self,j):     #function that is called at the beginning when object is created

# assign a variable to all intermediate values needed

        self.TOp1 = CCPar("TOp1")
        self.TOpNom1 = CCPar("TOpNom1")
        self.HCGPnom1 = CCPar("HCGPnom1")

        self.USHBoiler1 = CCPar("USHBoiler1")
        self.USHBoiler2 = CCPar("USHBoiler2")
        self.USHBoiler = CCPar("USHBoiler")

        self.USH1 = CCPar("USH1")

        self.HCGTEfficiency1 = CCPar("HCGTEfficiency1")

        if TEST:
            self.importTestData(j)
        else:
#            self.importData()
            pass

    def importTestData(self,j):  #later on should import data from SQL. now simply sets to some value

        if TESTCASE == 2:       #original test case Kla - first version of FECel
            self.FuelLCV = 50 #IMPORT this parameter from the fuelDB 
            
            self.HCGPnom = CCPar("HCGPnom")
            self.HCGPnom.val = 1000
            self.HCGPnom.sqerr = 0.0   #example: nominal power is exactly given (manufacturer parameter !)€
            
            self.FuelConsum = CCPar("FuelConsum")
            self.FuelConsum.val = 1300
            self.FuelConsum.sqerr = 0.1   #
            
            self.NDaysEq = CCPar("NDaysEq")
            self.NDaysEq.val = 260 # 5 days/week
            self.NDaysEq.sqerr = 0.0  #example: big uncertainty in operating hours

            self.HPerDayEq = CCPar("HPerDayEq")
            self.HPerDayEq.val = 10
            self.HPerDayEq.sqerr = 0.  #example: uncertainty in operating hours

            self.TOp = CCPar("TOp")
            self.TOp.val = 6000
            self.TOp.sqerr = 0.5  #example: big uncertainty in operating hours

            self.PartLoad = CCPar("PartLoad")
            self.PartLoad.val = 0.5
            self.PartLoad.sqerr = 0.5  #example: big uncertainty in operating hours

            self.TOpNom = CCPar("TOpNom")
            self.TOpNom.val = 4000
            self.TOpNom.sqerr = 0.5  #example: big uncertainty in operating hours
            
            self.USH = CCPar("USH")
            self.USH.val = 5e+6
            self.USH.sqerr = 0.05    #example: quantity of heat produced is well known

            self.FETj = CCPar("FETj")
            self.FETj.val = None
            self.FETj.sqerr = INFINITE    #example: fuel consumption can approximately estimated from fuel balances

            self.HCGTEfficiency = CCPar("HCGTEfficiency")
            self.HCGTEfficiency.val = 0.8
            self.HCGTEfficiency.sqerr = 0.03    #efficiency rather well known ...

            self.QHXEq = CCPar("QHXEq")
            self.QHXEq.val = 1.e+6
            self.QHXEq.sqerr = 0

        elif TESTCASE == 3:       #global checking of algorithm

            if (j==0):
                self.FuelLCV = 10 #IMPORT this parameter from the fuelDB 
                
                self.HCGPnom = CCPar("HCGPnom")
                self.HCGPnom.val = 2.0
                self.HCGPnom.sqerr = 0.0   #example: nominal power is exactly given (manufacturer parameter !)€
                
                self.FuelConsum = CCPar("FuelConsum")
                self.FuelConsum.val = None
                self.FuelConsum.sqerr = INFINITE  #
                
                self.NDaysEq = CCPar("NDaysEq")
                self.NDaysEq.val = 250 # 5 days/week
                self.NDaysEq.sqerr = 0.0  #example: big uncertainty in operating hours

                self.HPerDayEq = CCPar("HPerDayEq")
                self.HPerDayEq.val = 16
                self.HPerDayEq.sqerr = 0.0  #example: uncertainty in operating hours

                self.TOp = CCPar("TOp")
                self.TOp.val = None
                self.TOp.sqerr = INFINITE  #example: big uncertainty in operating hours

                self.PartLoad = CCPar("PartLoad")
                self.PartLoad.val = None
                self.PartLoad.sqerr = INFINITE  #example: big uncertainty in operating hours

                self.TOpNom = CCPar("TOpNom")
                self.TOpNom.val = None
                self.TOpNom.sqerr = INFINITE  #example: big uncertainty in operating hours
                
                self.USH = CCPar("USH")
                self.USH.val = 4000.
                self.USH.sqerr = 0.001    #example: quantity of heat produced is well known

                self.FETj = CCPar("FETj")
                self.FETj.val = None
                self.FETj.sqerr = INFINITE    #example: fuel consumption can approximately estimated from fuel balances

                self.HCGTEfficiency = CCPar("HCGTEfficiency")
                self.HCGTEfficiency.val = 0.8
                self.HCGTEfficiency.sqerr = 0.001    #efficiency rather well known ...

                self.QHXEq = CCPar("QHXEq")
                self.QHXEq.val = 0
                self.QHXEq.sqerr = 0
                
            elif (j==1):
                self.FuelLCV = 10 #IMPORT this parameter from the fuelDB 
                
                self.HCGPnom = CCPar("HCGPnom")
                self.HCGPnom.val = 2.0
                self.HCGPnom.sqerr = 0.0   #example: nominal power is exactly given (manufacturer parameter !)€
                
                self.FuelConsum = CCPar("FuelConsum")
                self.FuelConsum.val = None
                self.FuelConsum.sqerr = INFINITE  #
                
                self.NDaysEq = CCPar("NDaysEq")
                self.NDaysEq.val = 250 # 5 days/week
                self.NDaysEq.sqerr = 0.0  #example: big uncertainty in operating hours

                self.HPerDayEq = CCPar("HPerDayEq")
                self.HPerDayEq.val = 16
                self.HPerDayEq.sqerr = 0.0  #example: uncertainty in operating hours

                self.TOp = CCPar("TOp")
                self.TOp.val = None
                self.TOp.sqerr = INFINITE  #example: big uncertainty in operating hours

                self.PartLoad = CCPar("PartLoad")
                self.PartLoad.val = None
                self.PartLoad.sqerr = INFINITE  #example: big uncertainty in operating hours

                self.TOpNom = CCPar("TOpNom")
                self.TOpNom.val = None
                self.TOpNom.sqerr = INFINITE  #example: big uncertainty in operating hours
                
                self.USH = CCPar("USH")
                self.USH.val = None
                self.USH.sqerr = INFINITE    #example: quantity of heat produced is well known

                self.FETj = CCPar("FETj")
                self.FETj.val = None
                self.FETj.sqerr = INFINITE    #example: fuel consumption can approximately estimated from fuel balances

                self.HCGTEfficiency = CCPar("HCGTEfficiency")
                self.HCGTEfficiency.val = 0.8
                self.HCGTEfficiency.sqerr = 0.001    #efficiency rather well known ...

                self.QHXEq = CCPar("QHXEq")
                self.QHXEq.val = 0
                self.QHXEq.sqerr = 0

        else:
            print "CheckUSH: WARNING - don't have input data for this test case no. ",TESTCASE

        if DEBUG in ["ALL"]:
            self.showAllUSH()

    def showAllUSH(self):
        
        print "====================="
        self.HCGPnom.show()
        self.HCGPnom1.show()
        self.FuelConsum.show()
        self.TOpNom.show()
        self.TOpNom1.show()
        self.TOp.show()
        self.TOp1.show()
        self.HPerDayEq.show()
        self.NDaysEq.show()
        self.PartLoad.show()
        self.FETj.show()
        self.HCGTEfficiency.show()
        self.HCGTEfficiency1.show()
        self.USH.show()
        self.USH1.show()
        self.USHBoiler1.show()
        self.USHBoiler2.show()
        self.USHBoiler.show()
        print "====================="

    def check(self):
        for n in range(4):

            if DEBUG in ["ALL"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

                print "Step 1: calculating from left to right (CALC)"
            
            self.TOp1 = calcProd("TOp1",self.HPerDayEq,self.NDaysEq)
            self.TOpNom1 = calcProd("TOpnom1",self.TOp,self.PartLoad)
            self.HCGPnom1 = calcProdC("HCGPnom1",self.FuelLCV,self.FuelConsum,self.HCGTEfficiency)
            self.USHBoiler1 = calcProd("USH1",self.HCGPnom,self.TOpNom)
            self.USHBoiler2 = calcProd("USH2",self.FETj,self.HCGTEfficiency1)
            self.USH1 = calcSum("USH1",self.USHBoiler,self.QHXEq)

            if DEBUG in ["ALL"]:
                self.showAllUSH()

# Step 2: Cross check the variables

                print "Step 2: cross checking"

            ccheck1(self.HCGTEfficiency,self.HCGTEfficiency1)
            ccheck1(self.TOp,self.TOp1)
            ccheck1(self.TOpNom,self.TOpNom1)
            ccheck1(self.HCGPnom,self.HCGPnom1)
            ccheck2(self.USHBoiler,self.USHBoiler1,self.USHBoiler2)
            ccheck1(self.USH,self.USH1)

            if DEBUG in ["ALL"]:
                self.showAllUSH()

# Step 3: Adjust the variables (inverse of calculation routines)

                print "Step 3: calculating from right to left (ADJUST)"
            
            adjustSum(self.USH1,self.USHBoiler,self.QHXEq)
            adjustProd(self.USHBoiler1,self.HCGPnom,self.TOpNom)
            adjustProd(self.USHBoiler2,self.FETj,self.HCGTEfficiency1)
            adjustProdC(self.HCGPnom1,self.FuelLCV,self.FuelConsum,self.HCGTEfficiency)
            adjustProd(self.TOpNom1,self.TOp,self.PartLoad)
            adjustProd(self.TOp1,self.HPerDayEq,self.NDaysEq)


            if DEBUG in ["ALL"]:
                self.showAllUSH()
            
# Step 4: Cross check again the variables

                print "Step 4: cross checking"

            ccheck1(self.HCGTEfficiency,self.HCGTEfficiency1)
            ccheck1(self.TOp,self.TOp1)
            ccheck1(self.TOpNom,self.TOpNom1)
            ccheck1(self.HCGPnom,self.HCGPnom1)
            ccheck2(self.USHBoiler,self.USHBoiler1,self.USHBoiler2)
            ccheck1(self.USH,self.USH1)

            if DEBUG in ["ALL"]:
                self.showAllUSH()

        if DEBUG in ["ALL","BASIC"]:
            self.showAllUSH()
        
#==============================================================================
if __name__ == "__main__":
    
    ccEq = CheckEq(0)       # creates an instance of class CCheck
    ccEq.check()
