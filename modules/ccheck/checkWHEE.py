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
#	Last revised by:    
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
        self.QWHEERec = CCPar("QWHEERec")
        self.QWHEERec1 = CCPar("QWHEERec1")
        self.QWHEEAmb = CCPar("QWHEEAmb")
        self.QWHEEAmb1 = CCPar("QWHEEAmb1")

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

        self.QWHEE = CCPar("QWHEE",priority=2)
        
#..............................................................................
# reading data from table "qprocessdata"

        if ANo == -1:       
            qwheeTable = Status.DB.qwasteheatelequip.ProjectID[Status.PId].AlternativeProposalNo[ANo].WHEENo[self.WHEENo]

            if len(qwheeTable) > 0:
                qwhee = qwheeTable[0]

                self.QWHEE.setValue(qwhee.QWHEE)                

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

                qwhee.QWHEE = self.QWHEE.val
                
                Status.SQL.commit()
                


#------------------------------------------------------------------------------
    def showAll(self):
#------------------------------------------------------------------------------
#   plotting of values for debugging
#------------------------------------------------------------------------------
        
        print "====================="
        self.QWHEE.show()
        self.QWHEE1.show()
        print "====================="
#------------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------
        self.QWHEE.screen()

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

            self.QWHEE1 = calcSum("QWHEE1",self.QWHEERec,self.QWHEEAmb)
            
            if DEBUG in ["ALL"]:
                self.showAll()

# Step 2: Cross check the variables

                print "Step 2: cross checking"

            ccheck1(self.QWHEE,self.QWHEE1)
            ccheck1(self.QWHEERec,self.QWHEERec1)
            ccheck1(self.QWHEEAmb,self.QWHEEAmb1)
            
            if DEBUG in ["ALL"]:
                self.showAll()

# Step 3: Adjust the variables (inverse of calculation routines)

                print "Step 3: calculating from right to left (ADJUST)"
            
            adjustSum(self.QWHEE1,self.QWHEERec,self.QWHEEAmb)

            if DEBUG in ["ALL"]:
                self.showAll()
            
# Step 4: Cross check again the variables

                print "Step 4: second cross checking"

            ccheck1(self.QWHEE,self.QWHEE1)
            ccheck1(self.QWHEERec,self.QWHEERec1)
            ccheck1(self.QWHEEAmb,self.QWHEEAmb1)

            if DEBUG in ["ALL"]:
                self.showAll()

        if DEBUG in ["ALL","BASIC"]:
            self.showAll()
        
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

