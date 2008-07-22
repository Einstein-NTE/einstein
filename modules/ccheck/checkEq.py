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
#                           Claudia Vannoi      3/07/2008
#
#               Changes in last update:
#                               sqerr NONE eliminated
#       20/04/2008: HS  Variable HCGTEfficiency1 added. 2nd cross check
#       26/04/2008: SQL import and export, ccheck, labels
#	3/07/2008: parameters in screen list, priorities, import from DBFuel,constraints val max
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
from einstein.modules.fluids import *
from einstein.modules.messageLogger import *

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
        self.HPerYearEq.valMax = 8760
        self.HPerYearEq1 = CCPar("HPerYear1")
        self.HPerYearEqNom = CCPar("HPerYearEqNom")
        self.HPerYearEqNom.valMax = 8760
        self.HPerYearEqNom1 = CCPar("HPerYearEqNom1")
        self.HPerYearEqNom2 = CCPar("HPerYearEqNom2")
        self.HCGPnom1 = CCPar("HCGPnom1")
        self.USHBoiler1 = CCPar("USHBoiler1")
        self.USHBoiler2 = CCPar("USHBoiler2")
        self.USHBoiler = CCPar("USHBoiler",priority=2)
        self.USHj = CCPar("USH",priority=2)
        self.USHj1 = CCPar("USH1")
        self.HCGTEfficiency1 = CCPar("HCGTEfficiency1")
        self.HCGTEfficiency2 = CCPar("HCGTEfficiency2")
        self.FETj1 = CCPar("FETj1") 

        self.FETel_j1 = CCPar("FETel_j1") 
        self.FETel_j2 = CCPar("FETel_j2") 
        self.FETFuel_j1 = CCPar("FETFuel_j1") 
        self.FETFuel_j2 = CCPar("FETFuel_j2")
        
        self.FuelConsum1 = CCPar("FuelConsum1")
        self.ElectriConsum1 = CCPar("ElectriConsum1")
        self.ElectriConsum2 = CCPar("ElectriConsum2")

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

        
        self.HCGPnom = CCPar("HCGPnom",priority=2)
        self.FuelConsum = CCPar("FuelConsum")
        self.ElectriConsum = CCPar("ElectriConsum")
        self.NDaysEq = CCPar("NDaysEq")
        self.HPerDayEq = CCPar("HPerDayEq")
        self.PartLoad = CCPar("PartLoad",parType="X")
        self.HCGTEfficiency = CCPar("HCGTEfficiency")

        self.FETj = CCPar("FETj",priority=2)   # from the FET matrix
        self.FETel_j = CCPar("FETel_j") 
        self.FETFuel_j = CCPar("FETFuel_j") 
        self.QHXEq = CCPar("QHXEq",priority=2 ) #from the heat recovery matrix

#..............................................................................
# reading data from table "qprocessdata"
#        try:
        if ANo == -1:       
            qgenerationhcTable = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].EqNo[self.EqNo]
            
            if len(qgenerationhcTable) > 0:
                qgenerationhc = qgenerationhcTable[0]

                fuel_number = qgenerationhc.DBFuel_id   #IMPORT from the fuelDB

                if fuel_number <= 0 or fuel_number is None:
                    self.mainSource = "Electricity"
                    self.FuelLCV = 0.0
                    self.FuelConsum.setValue(0)
                    self.ElectriConsum.setValue(qgenerationhc.ElectriConsum)
                else:
                    self.mainSource = "Fuel"
                    eq_fuel = Fuel(fuel_number)
                    self.FuelLCV = eq_fuel.LCV
                    self.FuelConsum.setValue(qgenerationhc.FuelConsum)
                    if qgenerationhc.ElectriConsum is None:
                        logWarning("CheckEq (importData): no electricity consumption specified for eq.no. %s. Zero assumed"%(j+1))
                        self.ElectriConsum.setValue(0)
                    else:
                        self.ElectriConsum.setValue(qgenerationhc.ElectriConsum)

                self.HCGPnom.setValue(qgenerationhc.HCGPnom)
                self.NDaysEq.setValue(qgenerationhc.NDaysEq)
                self.HPerDayEq.setValue(qgenerationhc.HPerDayEq)
                self.PartLoad.setValue(qgenerationhc.PartLoad)
                self.HCGTEfficiency.setValue(qgenerationhc.HCGTEfficiency)
                
                self.QHXEq.setValue(0)          #from the heat recovery matrix

#correct maximum value of efficiency for chillers and heat pumps
                self.EquipeType = qgenerationhc.EquipType
                self.EquipeClass = getEquipmentClass(self.EquipeType)
                if self.EquipeClass in ["CH","HP"]:
                    self.HCGTEfficiency.valMax = 20.0
                elif self.EquipeClass in ["BB"]:
                    self.HCGTEfficiency.valMax = 1.2
                elif self.EquipeClass in ["ST"]:
                    self.HCGTEfficiency.valMax = INFINITE
                else:
                    self.HCGTEfficiency.valMax = 1.0
            else:
                logTrack("CheckEq(importData): didn't find table entry in qgenerationhc for EqNo = "%self.EqNo)
                
#        except:
#            print "CheckEq(importData): error reading data from qgenerationhc PId"
#            pass

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

                qgenerationhc.HCGPnom = check(self.HCGPnom.val)
                qgenerationhc.FuelConsum = check(self.FuelConsum.val)
                qgenerationhc.ElectriConsum = check(self.ElectriConsum.val)
                qgenerationhc.NDaysEq = check(self.NDaysEq.val)
                qgenerationhc.HPerDayEq = check(self.HPerDayEq.val)
                qgenerationhc.PartLoad = check(self.PartLoad.val)
                qgenerationhc.HCGTEfficiency = check(self.HCGTEfficiency.val)

                qgenerationhc.HPerYearEq = check(self.HPerYearEq.val)        
                qgenerationhc.USHj = check(self.USHj.val)        
                qgenerationhc.FETj = check(self.FETj.val)
                qgenerationhc.FETFuel_j = check(self.FETFuel_j.val)
                qgenerationhc.FETel_j = check(self.FETel_j.val)
                qgenerationhc.QHXEq = check(self.QHXEq.val)

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
        self.ElectriConsum.show()
        self.HPerYearEqNom.show()
        self.HPerYearEq.show()
        self.HPerDayEq.show()
        self.NDaysEq.show()
        self.PartLoad.show()
        self.FETj.show()
        self.FETFuel_j.show()
        self.FETel_j.show()
        self.HCGTEfficiency.show()
        self.USHj.show()
        self.USHBoiler.show()
        self.QHXEq.show()
        
        print "====================="
#------------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------

########## Change of priority for parameters not needed

        if iszero(self.HCGPnom):
            self.FuelConsum.priority = 99
            
#................................................................................
        self.HCGPnom.screen()
        self.FuelConsum.screen()
        self.NDaysEq.screen()
        self.HPerDayEq.screen()
        self.PartLoad.screen()
        self.HCGTEfficiency.screen()

        self.HPerYearEq.screen()        
        self.USHj.screen()
        self.USHBoiler.screen()
        self.FETj.screen()
        self.QHXEq.screen()

#------------------------------------------------------------------------------
    def check(self):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   main function carrying out the check of the block
#------------------------------------------------------------------------------
        print "CheckEq - TESTPRINT TESTPRINT"
        print "track of USHj"
        self.USHj.show()
        print self.USHj.track

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
            self.USHBoiler1 = calcProd("USHBoiler1",self.HCGPnom,self.HPerYearEqNom)
            self.FETel_j1 = calcProd("FETel_j",self.ElectriConsum2,self.HPerYearEqNom2)
            
            if self.mainSource == "Fuel":
                print "CheckEq (calcs): fuel as main source"
                self.USHBoiler2 = calcProd("USHBoiler2",self.FETFuel_j,self.HCGTEfficiency1)
                self.HCGPnom1 = calcProdC("HCGPnom1",self.FuelLCV,self.FuelConsum,self.HCGTEfficiency)
            else:
                self.USHBoiler2 = calcProd("USHBoiler2",self.FETel_j,self.HCGTEfficiency1)
                self.HCGPnom1 = calcProd("HCGPnom1",self.ElectriConsum,self.HCGTEfficiency)
                
            self.USHj1 = calcSum("USHj1",self.USHBoiler,self.QHXEq)
            self.FETj1 = calcSum("FETj1",self.FETFuel_j,self.FETel_j)

            if DEBUG in ["ALL"]:
                self.showAllUSH()

# Step 2: Cross check the variables

                print "Step 2: cross checking"

            self.ccheckAll()

            if DEBUG in ["ALL"]:
                self.showAllUSH()

# Step 3: Adjust the variables (inverse of calculation routines)

                print "Step 3: calculating from right to left (ADJUST)"
            
            adjustSum(self.FETj1,self.FETFuel_j,self.FETel_j)
            adjustSum(self.USHj1,self.USHBoiler,self.QHXEq)
            adjustProd(self.USHBoiler1,self.HCGPnom,self.HPerYearEqNom)

            if self.mainSource == "Fuel":
                adjustProd(self.USHBoiler2,self.FETFuel_j2,self.HCGTEfficiency1)
                adjustProdC(self.HCGPnom1,self.FuelLCV,self.FuelConsum,self.HCGTEfficiency)
            else:
                adjustProd(self.USHBoiler2,self.FETel_j2,self.HCGTEfficiency1)
                adjustProd(self.HCGPnom1,self.ElectriConsum,self.HCGTEfficiency)
                
            adjustProd(self.FETel_j1,self.ElectriConsum2,self.HPerYearEqNom2)
            adjustProd(self.HPerYearEqNom1,self.HPerYearEq,self.PartLoad)
            adjustProd(self.HPerYearEq1,self.HPerDayEq,self.NDaysEq)


            if DEBUG in ["ALL"]:
                self.showAllUSH()
            
# Step 4: Cross check again the variables

                print "Step 4: second cross checking"

            self.ccheckAll()
            
            if DEBUG in ["ALL"]:
                self.showAllUSH()

        if DEBUG in ["ALL","BASIC","MAIN"]:
            self.showAllUSH()
        
#------------------------------------------------------------------------------
    def ccheckAll(self):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------

            ccheck2(self.HCGTEfficiency,self.HCGTEfficiency1,self.HCGTEfficiency2)

            ccheck1(self.HPerYearEq,self.HPerYearEq1)
            ccheck2(self.HPerYearEqNom,self.HPerYearEqNom1,self.HPerYearEqNom2)
            ccheck1(self.HCGPnom,self.HCGPnom1)
            ccheck1(self.FETj,self.FETj1)
            ccheck2(self.FETFuel_j,self.FETFuel_j1,self.FETFuel_j2)
            ccheck2(self.FETel_j,self.FETel_j1,self.FETel_j2)
            ccheck1(self.FuelConsum,self.FuelConsum1)
            ccheck2(self.ElectriConsum,self.ElectriConsum1,self.ElectriConsum2)
            ccheck2(self.USHBoiler,self.USHBoiler1,self.USHBoiler2)
            ccheck1(self.QHXEq,self.QHXEq1)
            ccheck1(self.USHj,self.USHj1)

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

