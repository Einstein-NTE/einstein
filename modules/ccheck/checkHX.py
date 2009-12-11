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
#	CheckHX
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Consistency check of heat exchanger data
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	13/06/2008
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
class CheckHX():
#------------------------------------------------------------------------------
#   Carries out consistency checking for heat exchanger h
#------------------------------------------------------------------------------

    def __init__(self,h):     #function that is called at the beginning when object is created

# assign a variable to all intermediate/calculated values needed

        self.QWH = CCPar("QWH")

        self.importData(h)

        if DEBUG in ["ALL","BASIC"]:
            self.showAll()

#------------------------------------------------------------------------------
    def importData(self,h):  
#------------------------------------------------------------------------------
#   imports data from SQL tables (from AlternativeProposalNo = -1)
#------------------------------------------------------------------------------

        self.HXNo = h+1
        ANo = -1
        
#..............................................................................
# assign empty CCPar to all questionnaire parameters

        self.QHX = CCPar("QHX",priority=2)
        
#..............................................................................
# reading data from table "qprocessdata"

        if ANo == -1:       
            qheatexchangerTable = Status.DB.qheatexchanger.ProjectID[Status.PId].AlternativeProposalNo[ANo].HXNo[self.HXNo]

            if len(qheatexchangerTable) > 0:
                qheatexchanger = qheatexchangerTable[0]

                self.QHX.setValue(qheatexchanger.QHX)                

#------------------------------------------------------------------------------
    def exportData(self):  
#------------------------------------------------------------------------------
#   stores corrected data in SQL (under AlternativeProposalNo = 0)
#------------------------------------------------------------------------------

        ANo = 0
        
#..............................................................................
# writing data into SQL table 

        if ANo == 0:
            qheatexchangerTable = Status.DB.qheatexchanger.ProjectID[Status.PId].AlternativeProposalNo[ANo].HXNo[self.HXNo]
            if len(qheatexchangerTable) > 0:
                qheatexchanger = qheatexchangerTable[0]

                qheatexchanger.QHX = check(self.QHX.val)
                
                Status.SQL.commit()
                


#------------------------------------------------------------------------------
    def showAll(self):
#------------------------------------------------------------------------------
#   plotting of values for debugging
#------------------------------------------------------------------------------
        
        print "====================="
        self.QHX.show()
        self.QWH.show()
        print "====================="
#------------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------
        self.QHX.screen()

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

            pass #for the moment nothing to be calculates

            if DEBUG in ["ALL"]:
                self.showAll()

# Step 2: Cross check the variables

                print "Step 2: cross checking"

            ccheck1(self.QHX,self.QWH)
            
            if DEBUG in ["ALL"]:
                self.showAll()

# Step 3: Adjust the variables (inverse of calculation routines)

                print "Step 3: calculating from right to left (ADJUST)"
            
            pass    #for the moment nothing to adjust

            if DEBUG in ["ALL"]:
                self.showAll()
            
# Step 4: Cross check again the variables

                print "Step 4: second cross checking"

            #ccheck1(self.QHX,self.QWH)  #second ccheck is superfluous, as none of the three data is adjusted

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

