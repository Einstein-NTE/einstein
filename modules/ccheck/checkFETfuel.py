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
#   EINSTEIN Version No.: 1.0
#   Created by: 	Hans Schweiger, Stoyan Danov
#                       10/04/2008 - 03/09/2008
#
#   Update No. 001
#
#   Since Version 1.0 revised by:
#
#                       Hans Schweiger  06/04/2008
#               
#   06/04/2008  HS  Clean-up: elimination of prints
#	
#------------------------------------------------------------------------------		
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008,2009
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
from einstein.modules.fluids import *

#libraries necessary for SQL access:
from einstein.GUI.status import *
import einstein.GUI.pSQL as pSQL, MySQLdb

#------------------------------------------------------------------------------
class CheckFETfuel():
#------------------------------------------------------------------------------
#   Carries out consistency checking for fuel i
#------------------------------------------------------------------------------


    def __init__(self,i):     #function that is called at the beginning when object is created

#        print "CheckFETfuel: __INIT__ running"

# assign a variable to all intermediate/calculated values needed

        self.FETFuel = CCPar("FETFuel",priority=2)
        self.FETFuel1 = CCPar("FETFuel1") 
        self.FECFuel1 = CCPar("FECFuel1") 
        self.FECFuel2 = CCPar("FECFuel2")

        self.FuelTariff1 = CCPar("FuelTariff1")
        self.FuelCostYear1 = CCPar("FuelCostYear1")
        
        self.importData(i)

        if DEBUG in ["ALL","BASIC"]:
            self.showAllFETfuel()
#------------------------------------------------------------------------------
    def importData(self,i):  
#------------------------------------------------------------------------------
#   imports data from SQL tables (from AlternativeProposalNo = -1)
#   i = 1 ... NFuels: number of fuel
#------------------------------------------------------------------------------

        self.FuelNo = i
#        print "CheckFETfuel: importing data"
        ANo = -1
        
#..............................................................................
# assign empty CCPar to all questionnaire parameters

        
        self.MFuelYear = CCPar("MFuelYear") 
        self.FECFuel = CCPar("FECFuel", priority = 1)
        self.FEOFuel = CCPar("FEOFuel") #FEOfuel assigned only here=0: missed in the questionnaire but present in the list of the parameters

        self.FuelTariff = CCPar("FuelTariff", priority = 1)
        self.FuelCostYear = CCPar("FuelCostYear",priority = 1)

#..............................................................................
# reading data from table "qfuel"
#        print "CheckFETFuel: trying to read database"
        try:
            qfuelTable = Status.DB.qfuel.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].FuelNo[i]
#            print "CheckFETFuel: number of fuels = ",len(qfuelTable)
            
            if len(qfuelTable) > 0:
                qfuel = qfuelTable[0]

                fuel_number = qfuel.DBFuel_id   #IMPORT from the fuelDB
                fet_fuel = Fuel(fuel_number)
                self.FuelLCV = fet_fuel.LCV
                #self.FuelLCV = 10 # kWh/unit # IMPORT Constant from the FuelDB

                self.MFuelYear.setValue(qfuel.MFuelYear,err=0.0) #if specified, take as exact
                self.FECFuel.setValue(qfuel.FECFuel)
                
                self.FEOFuel.val = 0
                self.FEOFuel.sqerr = 0.0
                logDebug("checkFuel (importData): FEO = 0.0 assumed")

                self.FuelTariff.setValue(qfuel.FuelTariff)
                self.FuelCostYear.setValue(qfuel.FuelCostYear)
                
        except:
            self.FuelLCV = 0.0
            print "CheckFETfuel(importData): error reading data from qfuel"
            pass

#------------------------------------------------------------------------------
    def exportData(self):  
#------------------------------------------------------------------------------
#   stores corrected data in SQL (under AlternativeProposalNo = 0)
#------------------------------------------------------------------------------

        ANo = 0
        
#..............................................................................
# writing data into table " qfuel"
        if ANo == 0:
            qfuelTable = Status.DB.qfuel.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].FuelNo[self.FuelNo]
            if len(qfuelTable) > 0:
                qfuel = qfuelTable[0]

                qfuel.MFuelYear = check(self.MFuelYear.val)
                qfuel.FEOFuel = check(self.FEOFuel.val)
                qfuel.FECFuel = check(self.FECFuel.val)
                qfuel.FETFuel = check(self.FETFuel.val)

                qfuel.FuelTariff = check(self.FuelTariff.val)
                qfuel.FuelCostYear = check(self.FuelCostYear.val)
                
                Status.SQL.commit()
                
    def showAllFETfuel(self):
        
        print "====================="
      
        self.MFuelYear.show()
        self.FECFuel1.show()
        self.FECFuel.show()
        self.FEOFuel.show()
        self.FETFuel.show()
        self.FETFuel1.show()
                
        print "====================="
#-----------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------

#        print "CheckFETFuel (screen): screening"
        self.MFuelYear.screen()
        self.FECFuel.screen()
        self.FEOFuel.screen()
        self.FETFuel.screen()
        self.FuelCostYear.screen()
        self.FuelTariff.screen()

#------------------------------------------------------------------------------
    def check(self):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   main function carrying out the check of the block
#------------------------------------------------------------------------------

#        print "CheckFETfuel: starting check with"
#        self.FECFuel.show()
#        self.MFuelYear.show()
        
        if DEBUG in ["ALL"]:
            print "-------------------------------------------------"
            print " FETfuel checking"
            print "-------------------------------------------------"

        
        for n in range(1):
            
            if DEBUG in ["ALL"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence
            if DEBUG in ["ALL"]:
                print "Step 1: calculating from left to right (CALC)"
            
            self.FECFuel1 = calcK("FECFuel1",self.FuelLCV,self.MFuelYear)
            self.FETFuel1 = calcDiff("FETFuel1",self.FECFuel,self.FEOFuel)
            self.FuelCostYear1 = calcProd("FuelCostYear1",self.FuelTariff,self.FECFuel)
            
            if DEBUG in ["ALL"]:          
                self.showAllFETfuel()

# Step 2: Cross check the variables

            if DEBUG in ["ALL"]:
                print "Step 2: cross checking"

            ccheck1(self.FETFuel,self.FETFuel1)
            ccheck2(self.FECFuel,self.FECFuel1,self.FECFuel2)
            ccheck1(self.FuelTariff,self.FuelTariff1)
            ccheck1(self.FuelCostYear,self.FuelCostYear1)
                                    
            if DEBUG in ["ALL"]:
                self.showAllFETfuel()
                
# Step 3: Adjust the variables (inverse of calculation routines)

            if DEBUG in ["ALL"]:
                print "Step 3: calculating from right to left (ADJUST)"

            adjustProd(self.FuelCostYear1,self.FuelTariff,self.FECFuel2)
            adjustDiff(self.FETFuel1,self.FECFuel,self.FEOFuel)
            adjustcalcK(self.FECFuel1,self.FuelLCV,self.MFuelYear)
                        
            if DEBUG in ["ALL"]:
                self.showAllFETfuel()
                

# Step 4: Second cross check the variables: added in order to provisionally solve the calcDiff/adjustDiff problem

            if DEBUG in ["ALL"]:
                print "Step 4: cross checking"

            ccheck1(self.FETFuel,self.FETFuel1)
            ccheck2(self.FECFuel,self.FECFuel1,self.FECFuel2)
            ccheck1(self.FuelTariff,self.FuelTariff1)
            ccheck1(self.FuelCostYear,self.FuelCostYear1)
                                    
            if DEBUG in ["ALL"]:
                self.showAllFETfuel()
                
        
    #añadido este último show all. sino no se ven los ultimos dos resultados ...
        if DEBUG in ["ALL","BASIC"]:
            self.showAllFETfuel()


#------------------------------------------------------------------------------
    def estimate(self):  
#------------------------------------------------------------------------------
#   estimates some of the data that are not sufficiently precise
#   should be a subset of the data that are within screen
#   (not necessarily ALL data have to be estimated)
#------------------------------------------------------------------------------

        self.FuelTariff.setEstimate(0.04,limits = (0.02,0.06))

#==============================================================================
if __name__ == "__main__":
    
# direct connecting to SQL database w/o GUI. for testing only
    stat = Status("testCheckProc")
    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    Status.PId = 41
    Status.ANo = -1
#..............................................................................
    
    screen = CCScreen()
    
    ccFETfuel = CheckFETfuel(1)       # creates an instance of class CCheck
    ccFETfuel.check()
    ccFETfuel.exportData(1)

    ccFETfuel.screen()
    screen.show()
    
#==============================================================================

