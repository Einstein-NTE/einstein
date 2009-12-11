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
#   Created by: 	Claudia Vannoni, Hans Schweiger
#                       17/04/2008 - 16/09/2008
#
#   Update No. 002
#
#   Since Version 1.0 revised by:
#
#                       Hans Schweiger  06/04/2009
#                       Hans Schweiger  11/06/2009
#               
#   06/04/2009  HS  Clean-up: elimination of some prints
#   11/06/2009  HS  Some checks on tariffs and costs
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

#libraries necessary for SQL access:
from einstein.GUI.status import *
import einstein.GUI.pSQL as pSQL, MySQLdb

#------------------------------------------------------------------------------
class CheckFETel():
#------------------------------------------------------------------------------
#   Carries out consistency checking 
#------------------------------------------------------------------------------

    def __init__(self):     #function that is called at the beginning when object is created

# assign a variable to all intermediate/calculated values needed
        
        self.ElectricityNet = CCPar("ElectricityNet") 
        self.ElectricityNet1 = CCPar("ElectricityNet1")
        
        self.ElectricityGen1 = CCPar("ElectricityGen1")
        self.ElectricityGen2 = CCPar("ElectricityGen2")
        self.ElectricityGen3 = CCPar("ElectricityGen3")
        
        self.ElectricitySales1 = CCPar("ElectricitySales1")
        self.ElectricitySales2 = CCPar("ElectricitySales2")
        
        self.ElectricityTotYear1 = CCPar("ElectricityTotYear1")
        self.ElectricityTotYear2 = CCPar("ElectricityTotYear2")
        self.ElectricityTotYear3 = CCPar("ElectricityTotYear2")

        self.ElectricityMotors1 = CCPar("ElectricityMotors1")
        self.ElectricityChem1 = CCPar("ElectricityChem1")
        self.ElectricityLight1 = CCPar("ElectricityLight1")
        self.ElectricityRef1 = CCPar("ElectricityRef1")
        self.ElectricityAC1 = CCPar("ElectricityAC1")
        self.ElectricityThOther1 = CCPar("ElectricityThOther1")

        self.FECel_c1 = CCPar("FECel_c1")
        self.FECel_c = CCPar("FECel_c",priority=1)
        self.FECel = CCPar("FECel",priority=1,parType="S")
        self.FECel1 = CCPar("FECel1",parType="S")
        self.FEOel1 = CCPar("FEOel1")
        self.FEOel = CCPar("FEOel")
        
        self.FETel_c1 = CCPar("FETel_c1")
        self.FETel_c2 = CCPar("FETel_c2")
        self.FETel_c3 = CCPar("FETel_c3")
        self.FETel_c = CCPar("FETel_c",priority=1)

        self.FETel = CCPar("FETel",priority=1,parType="S")
        self.FETel1 = CCPar("FETel1",parType="S")

        self.ElTariffCTot1 = CCPar("ElTariffCTot1")
        self.ETariffCHP1 = CCPar("ETariffCHP1")

        self.ElCostYearTot1 = CCPar("ElCostYearTot1")
        self.ElSalesYearCHP1 = CCPar("ElSalesYearCHP1")
        
        self.importData(0)

        if DEBUG in ["ALL","BASIC","MAIN"]:
            self.showAllFETel()


#------------------------------------------------------------------------------
    def importData(self,i):  
#------------------------------------------------------------------------------
#   imports data from SQL tables (from AlternativeProposalNo = -1)
#------------------------------------------------------------------------------

        ANo = -1
        
#..............................................................................
# assign empty CCPar to all questionnaire parameters

        self.ElectricityGen = CCPar("ElectricityGen")
        self.ElectricitySales = CCPar("ElectricitySales")
        self.ElectricityTotYear = CCPar("ElectricityTotYear")

        self.ElectricityMotors = CCPar("ElectricityMotors")
        self.ElectricityChem = CCPar("ElectricityChem")
        self.ElectricityLight = CCPar("ElectricityLight")
        self.ElectricityRef = CCPar("ElectricityRef")
        self.ElectricityAC = CCPar("ElectricityAC")
        self.ElectricityThOther = CCPar("ElectricityThOther")

        self.ElTariffCTot = CCPar("ElTariffCTot", priority = 2)
        self.ElTariffPowTot = CCPar("ElTariffPowTot")
        self.ETariffCHP = CCPar("ETariffCHP", priority = 2)

        self.ElCostYearTot = CCPar("ElCostYearTot", priority = 1)
        self.ElSalesYearCHP = CCPar("ElSalesYearCHP", priority = 1)

#..............................................................................
# reading data from table "cgeneraldata"
        cgeneraldataTable = Status.DB.cgeneraldata.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo]
        if len(cgeneraldataTable) > 0:
            cgeneraldata = cgeneraldataTable[0]

            pass

# to be checked where's the right place for those parameters ... 
#            self.ElectricityGen.setValue(cgeneraldata.ElectricityGen)
#            self.ElectricitySales.setValue(cgeneraldata.ElectricitySales)
                

#..............................................................................
# reading data from table "qelectricity"

        qelectricityTable = Status.DB.qelectricity.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo]
        if len(qelectricityTable) > 0:
            qelectricity = qelectricityTable[0]

            self.ElectricityGen.setValue(qelectricity.ElGenera)
            self.ElectricitySales.setValue(qelectricity.ElSales)

            self.ElectricityTotYear.setValue(qelectricity.ElectricityTotYear)
            self.ElectricityMotors.setValue(qelectricity.ElectricityMotors)
            self.ElectricityChem.setValue(qelectricity.ElectricityChem)
            self.ElectricityLight.setValue(qelectricity.ElectricityLight)
            self.ElectricityRef.setValue(qelectricity.ElectricityRef)
            self.ElectricityAC.setValue(qelectricity.ElectricityAC)
            self.ElectricityThOther.setValue(qelectricity.ElectricityThOther)

            self.ElTariffCTot.setValue(qelectricity.ElTariffCTot)
            self.ElTariffPowTot.setValue(qelectricity.ElTariffPowTot)
            self.ETariffCHP.setValue(qelectricity.ETariffCHP)

            self.ElCostYearTot.setValue(qelectricity.ElCostYearTot)
            self.ElSalesYearCHP.setValue(qelectricity.ElSalesYearCHP)

                
#..............................................................................
# check if calculation of FECel is principally possible

        if (self.ElectricityTotYear.val is None) or \
           (self.ElectricityGen.val is None) or \
           (self.ElectricitySales.val is None):
            if (self.ElectricityMotors.val is None) or \
               (self.ElectricityLight.val is None) or \
               (self.ElectricityChem.val is None):
                logWarning(_("WARNING: No data available for electricity consumption for non-thermal uses. Set to 0 !!!"))
                if (self.ElectricityMotors.val is None): self.ElectricityMotors.setValue(0.0)
                if (self.ElectricityLight.val is None): self.ElectricityLight.setValue(0.0)
                if (self.ElectricityChem.val is None): self.ElectricityChem.setValue(0.0)
#                self.FEOel.setValue(0.0)

#------------------------------------------------------------------------------
    def exportData(self):  
#------------------------------------------------------------------------------
#   stores corrected data in SQL (under AlternativeProposalNo = 0)
#------------------------------------------------------------------------------

        ANo = 0
        
#..............................................................................
# writing data to table "cgeneraldata"
#        try:
        if ANo == 0:
            cgeneraldataTable = Status.DB.cgeneraldata.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo]
            if len(cgeneraldataTable) > 0:
#                print "exporting data to cgeneraldata"
                cgeneraldata = cgeneraldataTable[0]

                cgeneraldata.ElectricityGen = check(self.ElectricityGen.val)
                cgeneraldata.ElectricitySales = check(self.ElectricitySales.val)

                cgeneraldata.FECel = check(self.FECel.val)
                cgeneraldata.FEOel = check(self.FEOel.val)
                cgeneraldata.FETel = check(self.FETel.val)
                
                Status.SQL.commit()

#..............................................................................
# writing data to table "qelectricity"

        qelectricityTable = Status.DB.qelectricity.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo]
        if len(qelectricityTable) > 0:
            qelectricity = qelectricityTable[0]

            qelectricity.ElectricityTotYear = check(self.ElectricityTotYear.val)
            qelectricity.ElGenera = check(self.ElectricityGen.val)
            qelectricity.ElSales = check(self.ElectricitySales.val)
            
            qelectricity.ElectricityMotors = check(self.ElectricityMotors.val)
            qelectricity.ElectricityChem = check(self.ElectricityChem.val)
            qelectricity.ElectricityLight = check(self.ElectricityLight.val)
            qelectricity.ElectricityRef = check(self.ElectricityRef.val)
            qelectricity.ElectricityAC = check(self.ElectricityAC.val)
            qelectricity.ElectricityThOther = check(self.ElectricityThOther.val)
            qelectricity.ElGenera = check(self.ElectricityGen.val)

            qelectricity.ElTariffCTot = check(self.ElTariffCTot.val)
            qelectricity.ElTariffPowTot = check(self.ElTariffPowTot.val)
            qelectricity.ETariffCHP = check(self.ETariffCHP.val)

            qelectricity.ElCostYearTot = check(self.ElCostYearTot.val)
            qelectricity.ElSalesYearCHP = check(self.ElSalesYearCHP.val)


            Status.SQL.commit()
                

        
#------------------------------------------------------------------------------
    def showAllFETel(self):
#------------------------------------------------------------------------------
#   function for debug-plotting
#------------------------------------------------------------------------------

        print "====================="
        self.ElectricityNet.show()
        self.ElectricityNet1.show()
        self.ElectricityGen.show()
        self.ElectricitySales.show()
        self.ElectricityTotYear.show()
        self.FECel1.show()
        self.FECel.show()
        self.FECel_c1.show()
        self.FECel_c.show()
        self.ElectricityMotors.show()
        self.ElectricityChem.show()
        self.ElectricityLight.show()
        self.ElectricityRef.show()
        self.ElectricityAC.show()
        self.ElectricityThOther.show()
        self.FEOel1.show()
        self.FEOel.show()
        self.FETel_c1.show()
        self.FETel_c2.show()
        self.FETel_c.show()
        self.FETel1.show()
        self.FETel.show()
                  
        print "====================="
    
#------------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------

        self.ElectricityNet.screen()
        self.ElectricityGen.screen()
        self.ElectricitySales.screen()
        self.ElectricityTotYear.screen()

        self.ElectricityMotors.screen()
        self.ElectricityChem.screen()
        self.ElectricityLight.screen()
        self.ElectricityRef.screen()
        self.ElectricityAC.screen()
        self.ElectricityThOther.screen()
        
        self.FEOel.screen()
        self.FETel.screen()
        self.FECel.screen()

        self.ElTariffCTot.screen()

        self.ElCostYearTot.screen()
        self.ElSalesYearCHP.screen()

#------------------------------------------------------------------------------
    def check(self):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   main function carrying out the check of the block
#------------------------------------------------------------------------------
        if DEBUG in ["ALL","MAIN","BASIC"]:
            print "-------------------------------------------------"
            print " Checking FETel"
            print "-------------------------------------------------"

        for n in range(1):

            if DEBUG in ["ALL","MAIN"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

            if DEBUG in ["ALL","MAIN"]:
                print "Step 1: calculating from left to right (CALC)"
            
            self.ElectricityNet1 = calcDiff("ElectricityNet1",self.ElectricityGen,self.ElectricitySales)
            self.FECel_c1 = calcSum("FECel1",self.ElectricityNet,self.ElectricityTotYear)
            self.FECel = calcDiff("FECel",self.ElectricityTotYear,self.ElectricityGen,parType="S")

            self.FEOel1 = calcSum3("FEOel1",self.ElectricityMotors,self.ElectricityChem,self.ElectricityLight)
            self.FETel_c1 = calcDiff("FETel_c1",self.FECel_c,self.FEOel)
            self.FETel_c2 = calcSum3("FETel_c2",self.ElectricityRef,self.ElectricityAC,self.ElectricityThOther)
            self.FETel1 = calcDiff("FETel",self.FETel_c,self.ElectricityGen,parType="S")

            self.ElCostYearTot1 = calcProd("ElCostYearTot1",self.ElTariffCTot,self.ElectricityTotYear)
#### WARNING: power term not yet included in calculations !!!! ###
            
            self.ElSalesYearCHP1 = calcProd("ElSalesYearCHP1",self.ETariffCHP,self.ElectricitySales)

                      
            if DEBUG in ["ALL","MAIN"]:
                self.showAllFETel()

# Step 2: Cross check the variables

                print "Step 2: cross checking"

            self.ccheckAll()

            if DEBUG in ["ALL","MAIN"]:
                self.showAllFETel()

# Step 3: Adjust the variables (inverse of calculation routines)

                print "Step 3: calculating from right to left (ADJUST)"

            adjustProd(self.ElCostYearTot1,self.ElTariffCTot,self.ElectricityTotYear)
            adjustProd(self.ElSalesYearCHP1,self.ETariffCHP,self.ElectricitySales)

            adjustDiff(self.FETel1,self.FETel_c2,self.ElectricityGen3)
            adjustSum3(self.FETel_c2,self.ElectricityRef,self.ElectricityAC,self.ElectricityThOther)
            adjustDiff(self.FETel_c1,self.FECel_c,self.FEOel)
            adjustSum3(self.FEOel1,self.ElectricityMotors,self.ElectricityChem,self.ElectricityLight)
            
            adjustDiff(self.FECel,self.ElectricityTotYear2,self.ElectricityGen2)
            adjustSum(self.FECel_c1,self.ElectricityNet,self.ElectricityTotYear)
            adjustDiff(self.ElectricityNet1,self.ElectricityGen,self.ElectricitySales)

                        
            if DEBUG in ["ALL","MAIN"]:
                self.showAllFETel()

# Step 4: second cross check the variables

                print "Step 4: second cross checking"
               
            self.ccheckAll()
            
            if DEBUG in ["ALL","MAIN"]:
                self.showAllFETel()
        

# End of the cycle. Last print in DEBUG mode


        if DEBUG in ["ALL","BASIC","MAIN"]:
            self.showAllFETel()

#------------------------------------------------------------------------------
    def ccheckAll(self):     
#------------------------------------------------------------------------------
#   ccheck block
#------------------------------------------------------------------------------
        ccheck1(self.ElectricityNet,self.ElectricityNet1)
        ccheck3(self.ElectricityTotYear,self.ElectricityTotYear1,self.ElectricityTotYear2,self.ElectricityTotYear3)
        ccheck2(self.ElectricityGen,self.ElectricityGen1,self.ElectricityGen2)
        ccheck2(self.ElectricitySales,self.ElectricitySales1,self.ElectricitySales2)

        ccheck1(self.ElectricityMotors,self.ElectricityMotors1)
        ccheck1(self.ElectricityChem,self.ElectricityChem1)
        ccheck1(self.ElectricityLight,self.ElectricityLight1)
        ccheck1(self.ElectricityRef,self.ElectricityRef1)
        ccheck1(self.ElectricityAC,self.ElectricityAC1)
        ccheck1(self.ElectricityThOther,self.ElectricityThOther1)

        ccheck1(self.FECel_c,self.FECel_c1)
        ccheck1(self.FECel,self.FECel1)
        ccheck1(self.FEOel,self.FEOel1)
        ccheck2(self.FETel_c,self.FETel_c1,self.FETel_c2)
        ccheck1(self.FETel,self.FETel1)

        ccheck1(self.ElTariffCTot,self.ElTariffCTot1)
        ccheck1(self.ETariffCHP,self.ETariffCHP1)

        ccheck1(self.ElCostYearTot,self.ElCostYearTot1)
        ccheck1(self.ElSalesYearCHP,self.ElSalesYearCHP1)
                          
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

        self.ElectricityGen.setEstimate(0,limits=(0,0))
        self.ElectricitySales.setEstimate(0,limits=(0,0))
        self.FEOel.setEstimate(0,limits=(0,0))
        
        self.ElTariffCTot.setEstimate(0.08,limits=(0.05,0.15))
        self.ETariffCHP.setEstimate(0.10,limits=(0.07,0.17))

# limits: optional and fix absolute minimum and maximum values
# sqerr: optional input that fixes the (stochastic) relative square error

#==============================================================================

if __name__ == "__main__":

# direct connecting to SQL database w/o GUI. for testing only
    stat = Status("testCheckFETel")
    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    Status.PId = 41
    Status.ANo = -1
#..............................................................................
    
    screen = CCScreen()
    
    ccFETel = CheckFETel()       # creates an instance of class CCheck
    ccFETel.check()
    ccFETel.exportData()

    ccFETel.screen()
    screen.show()
    
#==============================================================================
