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
#	Version No.: 1.0
#       (not included in base version 1.0)
#
#       Update 0.01
#	
#	Last revised by:
#                           11/06/2009  Hans Schweiger
#       Changes in last update:
#                               
#	11/06/2009 HS:  first version
#
#------------------------------------------------------------------------------		
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2009
#	www.energyxperts.net / info@energyxperts.net
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license v3 as published by the Free
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
class CheckECO():
#------------------------------------------------------------------------------
#   Carries out consistency checking for economic parameters
#------------------------------------------------------------------------------

    def __init__(self):     #function that is called at the beginning when object is created

# assign a variable to all intermediate/calculated values needed

        self.OMThermal1 = CCPar("OMThermal1")
        self.OMElectrical1 = CCPar("OMElectrical1")

        self.importData()

        if DEBUG in ["ALL","BASIC"]:
            self.showAll()

#------------------------------------------------------------------------------
    def importData(self):  
#------------------------------------------------------------------------------
#   imports data from SQL tables (from AlternativeProposalNo = -1)
#------------------------------------------------------------------------------

        ANo = -1
        
#..............................................................................
# assign empty CCPar to all questionnaire parameters

        self.OMThermal = CCPar("OMThermal",priority=1)
        self.OMElectrical = CCPar("OMElectrical")


        self.OMTotalTot = CCPar("OMTotalTot")
        self.OMHCGenDistTot = CCPar("OMHCGenDistTot")
        
#..............................................................................
# reading data from table "qprocessdata"

        if ANo == -1:       
            qq = Status.DB.cgeneraldata.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo]

            if len(qq) > 0:
                q = qq[0]

            qq = Status.DB.questionnaire.Questionnaire_ID[Status.PId]

            if len(qq) > 0:
                q = qq[0]

                self.OMTotalTot.setValue(q.OMTotalTot)
                self.OMHCGenDistTot.setValue(q.OMHCGenDistTot)                

                self.OMThermal.setValue(q.OMThermal)                
                self.OMElectrical.setValue(q.OMElectrical)

                if self.OMElectrical.val == None:
                    self.OMElectrical.setValue(0.0)

#------------------------------------------------------------------------------
    def exportData(self):  
#------------------------------------------------------------------------------
#   stores corrected data in SQL (under AlternativeProposalNo = 0)
#------------------------------------------------------------------------------

        ANo = 0
        
#..............................................................................
# writing data into SQL table 

        if ANo == 0:
            qq = Status.DB.cgeneraldata.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo]
            if len(qq) > 0:
                q = qq[0]

                q.OMThermal = check(self.OMThermal.val)
                q.OMElectrical = check(self.OMElectrical.val)
                
                Status.SQL.commit()
                
#------------------------------------------------------------------------------
    def showAll(self):
#------------------------------------------------------------------------------
#   plotting of values for debugging
#------------------------------------------------------------------------------
        
        print "====================="
        self.OMThermal.show()
        self.OMElectrical.show()
        print "====================="
#------------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------
        self.OMThermal.screen()
        self.OMElectrical.screen()

#------------------------------------------------------------------------------
    def check(self):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   main function carrying out the check of the block
#------------------------------------------------------------------------------
        if DEBUG in ["ALL"]:
            print "-------------------------------------------------"
            print " Checking ECONOMIC parameters "
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

#            ccheck2(self.OMThermal,self.OMThermal1,self.OMHCGenDistTot)
            pass
        
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

#------------------------------------------------------------------------------
    def estimate(self):  
#------------------------------------------------------------------------------
#   estimates some of the data that are not sufficiently precise
#   should be a subset of the data that are within screen
#   (not necessarily ALL data have to be estimated)
#------------------------------------------------------------------------------

# if nothing is specified, suppose that electricity sales and generation are 0
# could be improved later on looking whether there's some CHP in the system or
# not ...

        self.OMThermal.setEstimate(0,limits=(0,0))

# limits: optional and fix absolute minimum and maximum values
# sqerr: optional input that fixes the (stochastic) relative square error

        
#==============================================================================
if __name__ == "__main__":
    
    pass    
#==============================================================================

