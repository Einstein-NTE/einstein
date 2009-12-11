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
#	CheckWHEE
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Consistency check of waste heat of electrical equipment data
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	17/06/2008
#	Last revised by:    Claudia Vannoni	3/07/2008
#                           Claudia Vannoni	30/07/2008
#       Changes in last update:
#                               
#	3/07/2008: priority
#       30/07/2008: deleted QWHEERec and Amb, considered in the matrix
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
class CheckWHEE():
#------------------------------------------------------------------------------
#   Carries out consistency checking for heat exchanger h
#------------------------------------------------------------------------------

    def __init__(self,n):     #function that is called at the beginning when object is created

# assign a variable to all intermediate/calculated values needed

        self.QWHEE1 = CCPar("QWHEE1")
        self.QWHEEYear = CCPar("QWHEEYear",priority = 2)
        self.QWHEEYear1 = CCPar("QWHEEYear1")
        self.HPerYear = CCPar("HPerYear")
        self.HPerYear1 = CCPar("HPerYear1")
        self.HPerDayWHEE1 = CCPar("HPerDayWHEE1")
        self.NDaysWHEE1 = CCPar("NDaysWHEE1")
        
        self.importData(n)

        if DEBUG in ["ALL","BASIC"]:
            self.showAll()

#------------------------------------------------------------------------------
    def importData(self,n):  
#------------------------------------------------------------------------------
#   imports data from SQL tables (from AlternativeProposalNo = -1)
#------------------------------------------------------------------------------

        self.WHEENo = n+1
        ANo = -1
        
#..............................................................................
# assign empty CCPar to all questionnaire parameters

        self.QWHEE = CCPar("QWHEE")
        self.HPerDayWHEE = CCPar("HPerDayWHEE")
        self.HPerDayWHEE.valMax = 24.0
        self.NDaysWHEE = CCPar("NDaysWHEE")
        self.NDaysWHEE.valMax = 365.
        
#..............................................................................
# reading data from table "qprocessdata"

        if ANo == -1:       
            qwheeTable = Status.DB.qwasteheatelequip.ProjectID[Status.PId].AlternativeProposalNo[ANo].WHEENo[self.WHEENo]

            if len(qwheeTable) > 0:
                qwhee = qwheeTable[0]

                self.QWHEE.setValue(qwhee.QWHEE)

                if qwhee.NDaysWHEE is not None:
                    self.NDaysWHEE.setValue(qwhee.NDaysWHEE,err=0.0)
                    
                self.HPerDayWHEE.setValue(qwhee.HPerDayWHEE)                

#------------------------------------------------------------------------------
    def exportData(self):  
#------------------------------------------------------------------------------
#   stores corrected data in SQL (under AlternativeProposalNo = 0)
#------------------------------------------------------------------------------

        ANo = 0
        
#..............................................................................
# writing data into SQL table 

        if ANo == 0:
            qwheeTable = Status.DB.qwasteheatelequip.ProjectID[Status.PId].AlternativeProposalNo[ANo].WHEENo[self.WHEENo]
            if len(qwheeTable) > 0:
                qwhee = qwheeTable[0]

                qwhee.QWHEE = check(self.QWHEE.val)
                qwhee.NDaysWHEE = check(self.NDaysWHEE.val)
                qwhee.HPerDayWHEE = check(self.HPerDayWHEE.val)
                
                Status.SQL.commit()
                


#------------------------------------------------------------------------------
    def showAll(self):
#------------------------------------------------------------------------------
#   plotting of values for debugging
#------------------------------------------------------------------------------
        
        print "====================="
        self.QWHEE.show()
        self.QWHEE1.show()
        self.QWHEEYear.show()
        self.QWHEEYear1.show()
        print "====================="
#------------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------
       self.QWHEE.screen()
       self.QWHEEYear.screen()
       self.NDaysWHEE.screen()
       self.HPerDayWHEE.screen()

#------------------------------------------------------------------------------
    def check(self):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   main function carrying out the check of the block
#------------------------------------------------------------------------------
        if DEBUG in ["ALL"]:
            print "-------------------------------------------------"
            print " Checking heat exchangers "
            print "-------------------------------------------------"

        for n in range(1):

            if DEBUG in ["ALL"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

                print "Step 1: calculating from left to right (CALC)"

            self.HPerYear1 = calcProd("HPerYearWHEE1",self.NDaysWHEE,self.HPerDayWHEE)
            self.QWHEEYear1 = calcProd("QWHEEYear1",self.QWHEE,self.HPerYear)

            pass     #here calcSum(self.QWHEE,sel.QWHEERec,self.QWHEEAmb)
            
            if DEBUG in ["ALL"]:
                self.showAll()

# Step 2: Cross check the variables

                print "Step 2: cross checking"

            self.ccheckAll()
            
            if DEBUG in ["ALL"]:
                self.showAll()

# Step 3: Adjust the variables (inverse of calculation routines)
            
                print "Step 3: calculating from right to left (ADJUST)"
            
            adjustProd(self.HPerYear1,self.NDaysWHEE,self.HPerDayWHEE)
            adjustProd(self.QWHEEYear1,self.QWHEE,self.HPerYear)
            
            if DEBUG in ["ALL"]:
                self.showAll()
            
# Step 4: Cross check again the variables

                print "Step 4: second cross checking"

            self.ccheckAll()
           

            if DEBUG in ["ALL"]:
                self.showAll()

        if DEBUG in ["ALL","BASIC"]:
            self.showAll()
        
#------------------------------------------------------------------------------
    def ccheckAll(self):    
#------------------------------------------------------------------------------
#   check block
#------------------------------------------------------------------------------
        ccheck1(self.QWHEE,self.QWHEE1)
        ccheck1(self.QWHEEYear,self.QWHEEYear1)
        ccheck1(self.HPerYear,self.HPerYear1)
        ccheck1(self.HPerDayWHEE,self.HPerDayWHEE1)
        ccheck1(self.NDaysWHEE,self.NDaysWHEE1)

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
    
    ccHX = CheckHX(1)       # creates an instance of class CCheck
    ccHX.check()
    ccHX.exportData(1)

    ccHX.screen()
    screen.show()
    
#==============================================================================

