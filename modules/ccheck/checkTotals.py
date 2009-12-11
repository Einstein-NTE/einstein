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
#	CCheckTotals (Consistency Check)
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
#	Created by: 	    Hans Schweiger	10/05/2008
#	Last revised by:    
#                           
#
#       Changes in last update:
#                           ---
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

MAXBALANCEERROR = 1.e-3
NMAXITERATIONS = 5
INFINITE = 1.e99    # numerical value assigned to "infinite"

from math import *
from ccheckFunctions import *
from numpy import *

from einstein.GUI.status import *

#------------------------------------------------------------------------------
class CheckTotals():
#------------------------------------------------------------------------------
#   Carries out consistency checking for the totals of FEC/FET/PEC/PET/USH/UPH
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def __init__(self,name,FECi,FETi,USHj,UPH):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   init function is only called once at the beginning (every time that base
#   actions that should be carried out in each iteration -> initCheck()
#------------------------------------------------------------------------------

# assign a variable to all intermediate values needed
        self.NFuels = len(FETi) - 1
        self.NThProc = len(UPH)
        self.NEquipe = len(USHj)
        
        self.FETi = FETi
        self.FECi = FECi
        self.USHj = USHj
        self.UPHk = UPH

        self.FEC = CCPar("FEC",priority=2)
        self.FEC1 = CCPar("FEC1")
        self.FEO = CCPar("FEO",priority=2)
        self.FET = CCPar("FET",priority=1)
        self.FET1 = CCPar("FET1")
        self.USH = CCPar("USH",priority=1)
        self.USH1 = CCPar("USH1")
        self.UPH = CCPar("UPH",priority=1)
        self.UPH1 = CCPar("UPH1")

        self.importData()

        if DEBUG in ["ALL","BASIC","MAIN"]:
            self.showAll()
        
#------------------------------------------------------------------------------
    def importData(self):  
#------------------------------------------------------------------------------
#   imports data from SQL tables (from AlternativeProposalNo = -1)
#------------------------------------------------------------------------------

        ANo = -1
        
#..............................................................................
# reading data from table "cgeneraldata"
        cgeneraldataTable = Status.DB.cgeneraldata.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo]
        if len(cgeneraldataTable) > 0:
            cgeneraldata = cgeneraldataTable[0]

#------------------------------------------------------------------------------
    def exportData(self):  
#------------------------------------------------------------------------------
#   stores corrected data in SQL (under AlternativeProposalNo = 0)
#------------------------------------------------------------------------------

        ANo = 0
        
#..............................................................................
# writing data to table "cgeneraldata"
        if ANo == 0:
            cgeneraldataTable = Status.DB.cgeneraldata.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo]
            if len(cgeneraldataTable) > 0:
                logDebug("exporting data to cgeneraldata")
                
                cgeneraldata = cgeneraldataTable[0]

                cgeneraldata.FET = check(self.FET.val)
                cgeneraldata.FEO = check(self.FEO.val)
                cgeneraldata.FEC = check(self.FEC.val)
                cgeneraldata.USH = check(self.USH.val)
                cgeneraldata.UPH = check(self.UPH.val)                

                Status.SQL.commit()
                
            else:
                logDebug("CheckTotals (exportData): error writing data to cgeneraldata")


#------------------------------------------------------------------------------        
    def showAll(self):
#------------------------------------------------------------------------------
#   printing of variables just for debugging
#------------------------------------------------------------------------------
        print "====================="
        self.FEO.show()
        self.FEC.show()
        self.FET.show()
        self.FET1.show()
        self.USH.show()
        self.USH1.show()
        self.UPH.show()
        self.UPH1.show()                                 
        print "====================="
#------------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------

        self.FET.screen()
        self.USH.screen()
        self.UPH.screen()

#------------------------------------------------------------------------------
    def check(self):     
#------------------------------------------------------------------------------
#   main function carrying out the check of the block
#------------------------------------------------------------------------------
        if DEBUG in ["ALL","MAIN","BASIC"]:
            print "-------------------------------------------------"
            print " Checking Totals"
            print "-------------------------------------------------"

        for n in range(1):  #while no adjust, 1 cycle is enough !!!!

            if DEBUG in ["ALL","MAIN"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

            if DEBUG in ["ALL"]:
                print "Step 1: calculating from left to right (CALC)"
            
            self.FEC1 = calcRowSum("FEC1",self.FETi,self.NFuels+1)
            self.FET1 = calcRowSum("FET1",self.FETi,self.NFuels+1)
            self.USH1 = calcRowSum("USH1",self.USHj,self.NEquipe)
            self.UPH1 = calcRowSum("UPH1",self.UPHk,self.NThProc)
            self.FEO = calcDiff("FEO",self.FEC,self.FET)

            if DEBUG in ["ALL"]:
                self.showAll()

# Step 2: Cross check the variables

                print "Step 2: cross checking"

            self.ccheckAll()

            if DEBUG in ["ALL"]:
                self.showAll()

# Step 3: Adjust the variables (inverse of calculation routines)

                print "Step 3: calculating from right to left (ADJUST)"

#for the moment only calculation, no adjust
            pass
                        
            if DEBUG in ["ALL"]:
                self.showAll()

# Step 4: second cross check the variables

                print "Step 4: second cross checking"
               
            self.ccheckAll()    #not necessary while adjust is not implemented
                          
            if DEBUG in ["ALL"]:
                self.showAll()

# End of the cycle. Last print in DEBUG mode


        if DEBUG in ["ALL","BASIC","MAIN"]:
            self.showAll()
            
#------------------------------------------------------------------------------
    def ccheckAll(self):     
#------------------------------------------------------------------------------
#   ccheck block
#------------------------------------------------------------------------------
        ccheck1(self.FEC,self.FEC1)
        ccheck1(self.FET,self.FET1)
        ccheck1(self.USH,self.USH1)
        ccheck1(self.UPH,self.UPH1)

#==============================================================================

if __name__ == "__main__":

    NI = 2
    NJ = 3
    
    FECi = CCRow("FECi",NI)
    FECi[0].val = 2
    FECi[0].sqerr = 0.
    FECi[0].valMin = 1.9
    FECi[0].valMax = 2.1
    
    FECi[1].val = 4
    FECi[1].sqerr = 0.
    FECi[1].valMin = 3.9
    FECi[1].valMax = 4.1

    FECj = CCRow("FECj",NJ)
    FECj[0].val = 3
    FECj[0].valMin = 2.9
    FECj[0].valMax = 3.1
    FECj[0].sqerr = 0.001
    FECj[1].val = 2.5
    FECj[1].sqerr = 0.001
    FECj[1].valMin = 2.4
    FECj[1].valMax = 2.6
    FECj[2].val = None
    FECj[2].sqerr = INFINITE
    FECj[2].valMin = 0
    FECj[2].valMax = INFINITE

    CT = CheckTotals("FECi-FECj",FECi,FECj,FECLink)
    
    CT.check()
