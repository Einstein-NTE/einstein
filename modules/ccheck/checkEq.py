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
#	Version No.: 0.05
#	Created by: 	    Hans Schweiger	08/03/2008
#	Last revised by:    Claudia Vannoni     7/04/2008
#                           Claudia Vannoni     16/04/2008
#                           Hans Schweiger      20/04/2008
#                           Claudia Vannoni     27/04/2008
#       Changes in last update:
#                               sqerr NONE eliminated
#       20/04/2008: HS  Variable HCGTEfficiency1 added. 2nd cross check
#       26/04/2008: SQL import and export, ccheck, labels
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

#libraries necessary for SQL access:
from einstein.GUI.status import *
import einstein.GUI.pSQL as pSQL, MySQLdb

#------------------------------------------------------------------------------
class CheckEq():
#------------------------------------------------------------------------------
#   Carries out consistency checking for equipe j
#------------------------------------------------------------------------------

    def __init__(self,j):     #function that is called at the beginning when object is created

# assign a variable to all intermediate/calculated values needed

        self.HPerYearEq = CCPar("HPerYearEq")
        self.HPerYearEq1 = CCPar("HPerYear1")
        self.HPerYearEqNom = CCPar("HPerYearEqNom")
        self.HPerYearEqNom1 = CCPar("HPerYearEqNom1")
        self.HCGPnom1 = CCPar("HCGPnom1")
        self.USHBoiler1 = CCPar("USHBoiler1")
        self.USHBoiler2 = CCPar("USHBoiler2")
        self.USHBoiler = CCPar("USHBoiler")
        self.USHj = CCPar("USH",priority=2)
        self.USHj1 = CCPar("USH1")
        self.HCGTEfficiency1 = CCPar("HCGTEfficiency1")
        self.FETj1 = CCPar("FETj1") 
        self.QHXEq1 = CCPar("QHXEq1") 
        
        if TEST==True:
            self.importTestData(j)
        else:
            self.importData(j)

        if DEBUG in ["ALL","BASIC"]:
            self.showAllUSH()

#------------------------------------------------------------------------------
    def importData(self,j):  
#------------------------------------------------------------------------------
#   imports data from SQL tables (from AlternativeProposalNo = -1)
#------------------------------------------------------------------------------

        self.EqNo = j+1
        ANo = -1
        
#..............................................................................
# assign empty CCPar to all questionnaire parameters

        self.FuelLCV = 10       #IMPORT this parameter from the fuelDB

        self.HCGPnom = CCPar("HCGPnom",priority=2)
        self.FuelConsum = CCPar("FuelConsum")
        self.NDaysEq = CCPar("NDaysEq")
        self.HPerDayEq = CCPar("HPerDayEq")
        self.PartLoad = CCPar("PartLoad")
        self.HCGTEfficiency = CCPar("HCGTEfficiency")

        self.FETj = CCPar("FETj",priority=2)   # from the FET matrix
        self.QHXEq = CCPar("QHXEq") #from the heat recovery matrix

#..............................................................................
# reading data from table "qprocessdata"
#        try:
        if ANo == -1:       
            qgenerationhcTable = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].EqNo[self.EqNo]

            print "CheckEq: importing data"
            print qgenerationhcTable[0]
            
            if len(qgenerationhcTable) > 0:
                qgenerationhc = qgenerationhcTable[0]


                self.HCGPnom.setValue(qgenerationhc.HCGPnom)
                self.FuelConsum.setValue(qgenerationhc.FuelConsum)
                self.NDaysEq.setValue(qgenerationhc.NDaysEq)
                self.HPerDayEq.setValue(qgenerationhc.HPerDayEq)
                self.PartLoad.setValue(qgenerationhc.PartLoad)
                self.HCGTEfficiency.setValue(qgenerationhc.HCGTEfficiency)
                
                self.QHXEq.setValue(0)          #from the heat recovery matrix

#        except:
            print "CheckEq(importData): error reading data from qgenerationhc"
            pass

#------------------------------------------------------------------------------
    def exportData(self):  
#------------------------------------------------------------------------------
#   stores corrected data in SQL (under AlternativeProposalNo = 0)
#------------------------------------------------------------------------------

        ANo = 0
        
#..............................................................................
# writing data into table "qgenerationhc"
#        try:
        if ANo == 0:
            qgenerationhcTable = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].EqNo[self.EqNo]
            if len(qgenerationhcTable) > 0:
                print "importing data into qgenerationhc"
                qgenerationhc = qgenerationhcTable[0]

                qgenerationhc.HCGPnom = self.HCGPnom.val
                qgenerationhc.FuelConsum = self.FuelConsum.val
                qgenerationhc.NDaysEq = self.NDaysEq.val
                qgenerationhc.HPerDayEq = self.HPerDayEq.val
                qgenerationhc.PartLoad = self.PartLoad.val
                qgenerationhc.HCGTEfficiency = self.HCGTEfficiency.val

                qgenerationhc.HPerYearEq = self.HPerYearEq.val        
                qgenerationhc.USHj = self.USHj.val        
                qgenerationhc.FETj = self.FETj.val
                qgenerationhc.QHXEq = self.QHXEq.val

            # self.USHBoiler not into the qprocessdat DB and not exported yet   

                Status.SQL.commit()
                
#        except:
            print "CheckEq (exportData): error writing data to qgenerationhc"
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
            
            self.PartLoad = CCPar("PartLoad")
            self.PartLoad.val = 0.5
            self.PartLoad.sqerr = 0.5  #example: big uncertainty in operating hours

            self.HCGTEfficiency = CCPar("HCGTEfficiency")
            self.HCGTEfficiency.val = 0.8
            self.HCGTEfficiency.sqerr = 0.03    #efficiency rather well known ...

            self.FETj = CCPar("FETj")
            self.FETj.val = None
            self.FETj.sqerr = INFINITE    

            self.QHXEq = CCPar("QHXEq")
            self.QHXEq.val = 1.e+6
            self.QHXEq.sqerr = 0.01

        elif TESTCASE == 3:       #global checking of algorithm

            if (j==0):
                self.FuelLCV = 10 #IMPORT this parameter from the fuelDB 
                
                self.HCGPnom = CCPar("HCGPnom")
                self.HCGPnom.val = 2.0
                self.HCGPnom.sqerr = 0.001   #example: nominal power is exactly given (manufacturer parameter !)€
                
                self.FuelConsum = CCPar("FuelConsum")
                self.FuelConsum.val = None
                self.FuelConsum.sqerr = INFINITE  #
                
                self.NDaysEq = CCPar("NDaysEq")
                self.NDaysEq.val = 250 # 5 days/week
                self.NDaysEq.sqerr = 0.001  #example: big uncertainty in operating hours

                self.HPerDayEq = CCPar("HPerDayEq")
                self.HPerDayEq.val = 16
                self.HPerDayEq.sqerr = 0.001  #example: uncertainty in operating hours
                
                self.PartLoad = CCPar("PartLoad")
                self.PartLoad.val = None
                self.PartLoad.sqerr = INFINITE  #example: big uncertainty in operating hours
                               
                self.HCGTEfficiency = CCPar("HCGTEfficiency")
                self.HCGTEfficiency.val = 0.8
                self.HCGTEfficiency.sqerr = 0.001    #efficiency rather well known ...
                
                self.FETj = CCPar("FETj")
                self.FETj.val = None
                self.FETj.sqerr = INFINITE
                
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
                
                self.PartLoad = CCPar("PartLoad")
                self.PartLoad.val = None
                self.PartLoad.sqerr = INFINITE  #example: big uncertainty in operating hours

                self.HCGTEfficiency = CCPar("HCGTEfficiency")
                self.HCGTEfficiency.val = 0.8
                self.HCGTEfficiency.sqerr = 0.001    #efficiency rather well known ...
                
                self.FETj = CCPar("FETj")
                self.FETj.val = None
                self.FETj.sqerr = INFINITE
                
                self.QHXEq = CCPar("QHXEq") 
                self.QHXEq.val = 0
                self.QHXEq.sqerr = 0.01

        else:
            print "CheckUSH: WARNING - don't have input data for this test case no. ",TESTCASE

        if DEBUG in ["ALL"]:
            self.showAllUSH()

    def showAllUSH(self):
        
        print "====================="
        self.HCGPnom.show()
        self.HCGPnom1.show()
        self.FuelConsum.show()
        self.HPerYearEqNom.show()
        self.HPerYearEqNom1.show()
        self.HPerYearEq.show()
        self.HPerYearEq1.show()
        self.HPerDayEq.show()
        self.NDaysEq.show()
        self.PartLoad.show()
        self.FETj.show()
        self.FETj1.show()
        self.HCGTEfficiency.show()
        self.HCGTEfficiency1.show()
        self.USHj.show()
        self.USHj1.show()
        self.USHBoiler1.show()
        self.USHBoiler2.show()
        self.USHBoiler.show()
        self.QHXEq.show()
        self.QHXEq1.show() 
        
        print "====================="
#------------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------
        self.HCGPnom.screen()
        self.FuelConsum.screen()
        self.NDaysEq.screen()
        self.HPerDayEq.screen()
        self.PartLoad.screen()
        self.HCGTEfficiency.screen()

        self.HPerYearEq.screen()        
        self.USHj.screen()       
        self.FETj.screen()
        self.QHXEq.screen()

#------------------------------------------------------------------------------
    def check(self):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   main function carrying out the check of the block
#------------------------------------------------------------------------------
        if DEBUG in ["ALL"]:
            print "-------------------------------------------------"
            print " Process checking"
            print "-------------------------------------------------"


        for n in range(1):

            if DEBUG in ["ALL"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

                print "Step 1: calculating from left to right (CALC)"
            
            self.HPerYearEq1 = calcProd("HPerYearEq1",self.HPerDayEq,self.NDaysEq)
            self.HPerYearEqNom1 = calcProd("HPerYearEqNom1",self.HPerYearEq,self.PartLoad)
            self.HCGPnom1 = calcProdC("HCGPnom1",self.FuelLCV,self.FuelConsum,self.HCGTEfficiency)
            self.USHBoiler1 = calcProd("USHBoiler1",self.HCGPnom,self.HPerYearEqNom)
            self.USHBoiler2 = calcProd("USHBoiler2",self.FETj,self.HCGTEfficiency1)
            self.USHj1 = calcSum("USHj1",self.USHBoiler,self.QHXEq)

            if DEBUG in ["ALL"]:
                self.showAllUSH()

# Step 2: Cross check the variables

                print "Step 2: cross checking"

            ccheck1(self.HCGTEfficiency,self.HCGTEfficiency1)
            
            
            ccheck1(self.HPerYearEq,self.HPerYearEq1)
            ccheck1(self.HPerYearEqNom,self.HPerYearEqNom1)
            ccheck1(self.HCGPnom,self.HCGPnom1)
            ccheck1(self.FETj,self.FETj1)
            ccheck2(self.USHBoiler,self.USHBoiler1,self.USHBoiler2)
            ccheck1(self.QHXEq,self.QHXEq1)
            ccheck1(self.USHj,self.USHj1)

            if DEBUG in ["ALL"]:
                self.showAllUSH()

# Step 3: Adjust the variables (inverse of calculation routines)

                print "Step 3: calculating from right to left (ADJUST)"
            
            adjustSum(self.USHj1,self.USHBoiler,self.QHXEq)
            adjustProd(self.USHBoiler1,self.HCGPnom,self.HPerYearEqNom)
            adjustProd(self.USHBoiler2,self.FETj,self.HCGTEfficiency1)
            adjustProdC(self.HCGPnom1,self.FuelLCV,self.FuelConsum,self.HCGTEfficiency)
            adjustProd(self.HPerYearEqNom1,self.HPerYearEq,self.PartLoad)
            adjustProd(self.HPerYearEq1,self.HPerDayEq,self.NDaysEq)


            if DEBUG in ["ALL"]:
                self.showAllUSH()
            
# Step 4: Cross check again the variables

                print "Step 4: second cross checking"

            ccheck1(self.HCGTEfficiency,self.HCGTEfficiency1)

            ccheck1(self.HPerYearEq,self.HPerYearEq1)
            ccheck1(self.HPerYearEqNom,self.HPerYearEqNom1)
            ccheck1(self.HCGPnom,self.HCGPnom1)
            ccheck1(self.FETj,self.FETj1)
            ccheck2(self.USHBoiler,self.USHBoiler1,self.USHBoiler2)
            ccheck1(self.QHXEq,self.QHXEq1)
            ccheck1(self.USHj,self.USHj1)

            if DEBUG in ["ALL"]:
                self.showAllUSH()

        if DEBUG in ["ALL","BASIC"]:
            self.showAllUSH()
        
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
    
    ccEq = CheckEq(1)       # creates an instance of class CCheck
    ccEq.check()
    ccEq.exportData(1)

    ccEq.screen()
    screen.show()
    
#==============================================================================

