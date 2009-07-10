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
#                       08/03/2008 - 03/09/2008
#
#   Update No. 002
#
#   Since Version 1.0 revised by:
#
#                       Hans Schweiger  06/04/2009
#                       Hans Schweiger  11/06/2009
#               
#   06/04/2009  HS  Clean-up: elimination of prints
#   11/06/2009  HS  Calculation of QWHEq based on minimum temperature in off gas
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
        self.HPerYearEqNom3 = CCPar("HPerYearEqNom3")#
        self.HPerYearEqNom4 = CCPar("HPerYearEqNom4")#
        self.HPerDayEq1 = CCPar("HPerDayEq1")
        
        self.HCGPnom1 = CCPar("HCGPnom1")
        self.USHBoiler1 = CCPar("USHBoiler1")
        self.USHBoiler2 = CCPar("USHBoiler2")
        self.USHBoiler = CCPar("USHBoiler",priority=2)
        self.USHj = CCPar("USH",priority=2)
        self.USHj1 = CCPar("USH1")
        self.USHj2= CCPar("USH2")#
        self.USHj3= CCPar("USH3")#
        self.HCGTEfficiency1 = CCPar("HCGTEfficiency1")
        self.HCGTEfficiency2 = CCPar("HCGTEfficiency2")
        self.HCGTEfficiency3 = CCPar("HCGTEfficiency3")

        self.HCGEEfficiency1 = CCPar("HCGEEfficiency1")
        self.HCGEEfficiency2 = CCPar("HCGEEfficiency2")

        self.ConvLoss = CCPar("ConvLoss")
        self.ConvLoss1 = CCPar("ConvLoss1")
        self.ConvLoss2 = CCPar("ConvLoss2")
        self.LossFactEq1 = CCPar("LossFactEq1")
        self.QConvLoss = CCPar("QConvLoss")
        self.QConvLoss1 = CCPar("QConvLoss1")
        self.One = CCOne()
        self.One1 = CCOne()
        
        self.FETj1 = CCPar("FETj1")
        self.FETj2 = CCPar("FETj2")
        self.FETj3 = CCPar("FETj3")

        self.FETel_c_j1 = CCPar("FETel_c_j1") 
        self.FETel_c_j2 = CCPar("FETel_c_j2")
        self.FETel_c_j3 = CCPar("FETel_c_j3")

        self.FETel_j1 = CCPar("FETel_j1",parType="S")
        self.FETel_j2 = CCPar("FETel_j2",parType="S")
        
        self.FETFuel_j1 = CCPar("FETFuel_j1") 
        self.FETFuel_j2 = CCPar("FETFuel_j2")
        self.FETFuel_j3 = CCPar("FETFuel_j3")

        self.ElGen_j1 = CCPar("ElGen_j1")
        self.ElGen_j2 = CCPar("ElGen_j2")
        self.ElGen_j3 = CCPar("ElGen_j3")
        
        self.FuelConsum1 = CCPar("FuelConsum1")
        self.FuelConsum2 = CCPar("FuelConsum2")#
        self.FuelConsum3 = CCPar("FuelConsum3")#
        self.FuelConsum4 = CCPar("FuelConsum4")#
        self.ElectriConsum1 = CCPar("ElectriConsum1")
        self.ElectriConsum2 = CCPar("ElectriConsum2")
        self.ElectriProduction1 = CCPar("ElectriProduction1")

        self.QHXEq1 = CCPar("QHXEq1")
        self.QHXEq2 = CCPar("QHXEq2")

        self.FlowCombAir = CCPar("FlowCombAir")#
        self.FlowCombAir1 = CCPar("FlowCombAir1")#
        self.FlowExhaustGas = CCPar("FlowExhaustGas")#
        self.FlowExhaustGas1 = CCPar("FlowExhaustGas1")#
        self.TExhaustGas1= CCPar("TExhaustGas1",parType="T")#
        self.TExhaustGas2= CCPar("TExhaustGas2",parType="T")#
        self.TMinOffGas1 = CCPar("TMinOffGas1",parType="T")#
        
        self.DTExhaustGas = CCPar("DTExhaustGas",parType="DT")#
        self.DTExhaustGas1 = CCPar("DTExhaustGas1",parType="DT")#
        self.DTExhaustGas2 = CCPar("DTExhaustGas2",parType="DT")#
        self.DTOffGasUse = CCPar("DTOffGasUse",parType="DT")#
        self.DTOffGasUse1 = CCPar("DTOffGasUse1",parType="DT")#
        self.DTOffGasUse2 = CCPar("DTOffGasUse2",parType="DT")#
        self.OffGasUse = CCPar("OffGasUse",parType="X")
        self.OffGasUse1 = CCPar("OffGasUse1",parType="X")
        self.TEnvEq1 = CCPar("TEnvEq1")
        self.QExhaustGasdot = CCPar("QExhaustGasdot")#
        self.QExhaustGasdot1 = CCPar("QExhaustGasdot1")#
        self.QExhaustGas = CCPar("QExhaustGas")#
        self.QExhaustGas1 = CCPar("QExhaustGas1")#
        self.ExcessAirRatio1 = CCPar("ExcessAirRatio1")#

        self.QWHEq1 = CCPar("QWHEq1")#
        self.QWHEqdot = CCPar("QWHEqdot")
        self.QWHEqdot1 = CCPar("QWHEqdot1")
        
        self.QWHEqTot = CCPar("QWHEqTot")#
        self.QWHEqTot1 = CCPar("QWHEqTot1")#
        self.QWHEqTot2 = CCPar("QWHEqTot2")#
        self.QLossEq = CCPar("QLossEq")#
        self.QLossEq1 = CCPar("QLossEq1")#
        self.QLossEq2 = CCPar("QLossEq2")#
        self.QInputEq = CCPar("QInputEq")#
        self.QInputEq1 = CCPar("QInputEq1")#
        self.QOutEq = CCPar("QOutEq")#
        self.QOutEq1 = CCPar("QOutEq1")#

        self.PartLoad1 = CCPar("PartLoad1")
          

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
        self.ElectriProduction = CCPar("ElectriProduction",priority=2)
        
        self.FuelConsum = CCPar("FuelConsum")
        self.ElectriConsum = CCPar("ElectriConsum")
        self.NDaysEq = CCPar("NDaysEq")
        self.HPerDayEq = CCPar("HPerDayEq")
        self.PartLoad = CCPar("PartLoad",parType="X")
        self.HCGTEfficiency = CCPar("HCGTEfficiency")
        self.HCGEEfficiency = CCPar("HCGEEfficiency")

        self.TExhaustGas = CCPar("TExhaustGas", parType="T")#
        self.ExcessAirRatio = CCPar("ExcessAirRatio")#
        self.ExcessAirRatio.valMin = 1.0
        self.ExcessAirRatio.valMax = 2.0

        self.FETj = CCPar("FETj",priority=2)   # from/to the FET matrix
        self.FETel_c_j = CCPar("FETel_c_j")
        self.FETel_j = CCPar("FETel_j",priority=2,parType="S")
        self.ElGen_j = CCPar("ElGen_j",priority=2)

        self.FETFuel_j = CCPar("FETFuel_j")
        
        self.QHXEq = CCPar("QHXEq",priority=2 ) #from/to the heat recovery matrix
        self.QWHEq = CCPar("QWHEq")  #from/to the heat recovery matrix  #

        self.TEnvEq = CCPar("TEnvEq", parType="T")    #average ambient temp. Not defined into questionnaire as generic parameter but only into ST questionnaire
        self.LossFactEq = CCPar("LossFactEq",parType="X")  # %of losses with respect to USHj (not to USHBoiler)
        self.TMinOffGas = CCPar("TMinOffGas",parType = "T")   # percentage of OffGas that can be used as waste heat
        
#..............................................................................
# reading data from table "qgenerationhc"
#        try:
        if ANo == -1:       
            qgenerationhcTable = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].EqNo[self.EqNo]
            
            if len(qgenerationhcTable) > 0:
                qgenerationhc = qgenerationhcTable[0]

                fuel_number = qgenerationhc.DBFuel_id   #IMPORT from the fuelDB

                if fuel_number <= 0 or fuel_number is None or qgenerationhc.FuelConsum == 0:
                    self.mainSource = "Electricity"
                    self.FuelLCV = 0.0
                    self.OffgasHeatCapacity = 1.0 #
                    self.CombAir = 0.0 #
                    self.FuelConsum.setValue(0.0)
                    self.TExhaustGas.setValue(15.0, err=0.0)          #

                    self.ElectriConsum.setValue(qgenerationhc.ElectriConsum)
                    self.ExcessAirRatio.val = 1.0
                    self.TMinOffGas.setValue(15.0,err = 0.0)
                else:
                    self.mainSource = "Fuel"
                    eq_fuel = Fuel(fuel_number)
                    self.FuelLCV = eq_fuel.LCV
                    self.OffgasHeatCapacity = eq_fuel.OffgasHeatCapacity #
#                    print "heat capacity = ",self.OffgasHeatCapacity
                    self.CombAir = eq_fuel.CombAir #
                    self.FuelConsum.setValue(qgenerationhc.FuelConsum)
                    if qgenerationhc.ElectriConsum is None:
                        logWarning("CheckEq (importData): no electricity consumption specified for eq.no. %s. Zero assumed"%(j+1))
                        self.ElectriConsum.setValue(0)
                    else:
                        self.ElectriConsum.setValue(qgenerationhc.ElectriConsum)

                    self.TExhaustGas.setValue(qgenerationhc.TExhaustGas,err = 0.01) #high error. gives problems
                    TCond = max(eq_fuel.TCondOffGas(),0)
                    self.TMinOffGas.setValue(TCond,err = 0.0)
                    if (qgenerationhc.ExcessAirRatio is None) and (qgenerationhc.TExhaustGas is None):
                        self.ExcessAirRatio.setValue(1.05,err = 0.0)
                    else:
                        if qgenerationhc.ExcessAirRatio is not None: #extend limits if necessary, for direct combustion burners !!!!
                            self.ExcessAirRatio.valMax = max(qgenerationhc.ExcessAirRatio,self.ExcessAirRatio.valMax)
                        self.ExcessAirRatio.setValue (qgenerationhc.ExcessAirRatio)
                        

                self.HCGPnom.setValue(qgenerationhc.HCGPnom,err = 0.0)  #if specified, take as fixed
                self.NDaysEq.setValue(qgenerationhc.NDaysEq, err=0.0) #integer -> 0 error
                self.HPerDayEq.setValue(qgenerationhc.HPerDayEq, err = 0.0) #if specified, take as fixed
                self.PartLoad.setValue(qgenerationhc.PartLoad)
                self.HCGTEfficiency.setValue(qgenerationhc.HCGTEfficiency)
                    #
                
                self.TEnvEq.setValue(15.0, err=0.0)          #
                self.LossFactEq.setValue(0.01, err=1.0)  #  heat losses of vessel supposed between 0 and 2 %
                self.LossFactEq.valMax = 0.02

#correct maximum value of efficiency for chillers and heat pumps
                self.EquipType = qgenerationhc.EquipType
                self.EquipeClass = getEquipmentClass(self.EquipType)
                if self.EquipeClass in ["CH","HP"]:
                    self.HCGTEfficiency.valMax = 20.0
                elif self.EquipeClass in ["BB"]:
                    self.HCGTEfficiency.valMax = 1.2
                    if self.HCGTEfficiency.val > 1.0:
                        logDebug("CheckEq (importData): boiler efficiencies > 100 % are not supported yet")
                elif self.EquipeClass in ["ST"]:
                    self.HCGTEfficiency.valMax = INFINITE
                else:
                    self.HCGTEfficiency.valMax = 1.0

                if self.EquipeClass == "CHP":
                    self.HCGEEfficiency.setValue(qgenerationhc.HCGEEfficiency)
                    self.ElectriProduction.setValue(qgenerationhc.ElectriProduction)
#                    self.ElGen_j.setValue(qgenerationhc.STAreaFactor)
                else:
                    self.HCGEEfficiency.setValue(0.0)
                    self.ElectriProduction.setValue(0.0)
                    self.ElGen_j.setValue(0.0)

                    self.FETj.parType = None
                    self.FETel_j.parType = None
            else:
                logTrack("CheckEq(importData): didn't find table entry in qgenerationhc for EqNo = %s"%self.EqNo)
                
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
        if ANo == 0:
            qgenerationhcTable = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].EqNo[self.EqNo]
            if len(qgenerationhcTable) > 0:
                qgenerationhc = qgenerationhcTable[0]

                qgenerationhc.HCGPnom = check(self.HCGPnom.val)
                qgenerationhc.FuelConsum = check(self.FuelConsum.val)
                qgenerationhc.ElectriConsum = check(self.ElectriConsum.val)
                qgenerationhc.ElectriProduction = check(self.ElectriProduction.val)
                qgenerationhc.NDaysEq = check(self.NDaysEq.val)
                qgenerationhc.HPerDayEq = check(self.HPerDayEq.val)
                qgenerationhc.PartLoad = check(self.PartLoad.val)
                
                qgenerationhc.HCGTEfficiency = check(self.HCGTEfficiency.val)
                qgenerationhc.HCGEEfficiency = check(self.HCGEEfficiency.val)

                qgenerationhc.HPerYearEq = check(self.HPerYearEq.val)        
                qgenerationhc.USHj = check(self.USHj.val)        
                qgenerationhc.FETj = check(self.FETj.val)
                qgenerationhc.FETFuel_j = check(self.FETFuel_j.val)
                qgenerationhc.FETel_j = check(self.FETel_j.val)
                qgenerationhc.QHXEq = check(self.QHXEq.val)

                qgenerationhc.QWHEq = check(self.QWHEq.val)#

                qgenerationhc.TExhaustGas = check(self.TExhaustGas.val)#
                qgenerationhc.ExcessAirRatio = check(self.ExcessAirRatio.val)#
                qgenerationhc.FlowExhaustGas = check(self.FlowExhaustGas.val)#       
                qgenerationhc.QExhaustGas = check(self.QExhaustGas.val)#

                if self.EquipeClass == "CHP":
                    qgenerationhc.STAreaFactor = check(self.ElGen_j.val)

            # self.USHBoiler not into the qgenerationhc and not exported yet   

                Status.SQL.commit()
                
    def showAllUSH(self):
        
        print "====================="
        self.HCGPnom.show()
        self.HCGPnom1.show()
        self.FuelConsum.show()
        self.FuelConsum1.show()#
        self.FuelConsum2.show()#
        self.FuelConsum3.show()#
        self.ElectriConsum.show()
        self.HPerYearEqNom.show()
        self.HPerYearEqNom1.show()#
        self.HPerYearEqNom2.show()#
        self.HPerYearEqNom3.show()#
        self.HPerYearEq.show()
        self.HPerDayEq.show()
        self.NDaysEq.show()
        self.PartLoad.show()
        self.HCGTEfficiency.show()
        self.ConvLoss.show()
        self.ConvLoss1.show()
        self.ConvLoss2.show()
        self.LossFactEq.show()
        self.USHj.show()
        self.USHj1.show()#
        self.USHj2.show()#
        self.USHj3.show()#
        self.USHBoiler.show()
        self.USHBoiler1.show()
        self.USHBoiler2.show()
        self.QHXEq.show()
        self.QHXEq1.show()#
        self.QHXEq2.show()#
        

        self.FETj.show()#
        self.FETj1.show()#
        self.FETj2.show()#
        self.FETj3.show()#
        
        self.FETel_j.show()#
        self.FETel_j1.show() #
        self.FETel_j2.show() #

        self.FETel_c_j.show()#
        self.FETel_c_j1.show() #
        self.FETel_c_j2.show() #
        self.FETFuel_j.show()# 
        self.FETFuel_j1.show()#
        self.FETFuel_j2.show()#
        self.FETFuel_j3.show()#
                
        self.ElectriConsum1.show()#
        self.ElectriConsum2.show()#

        self.ElectriProduction.show()#
        self.ElectriProduction1.show()#

        self.ElGen_j.show()#
        self.ElGen_j1.show()#
        self.ElGen_j2.show()#

        self.FlowCombAir1.show()#
        self.FlowCombAir.show()#
        self.FlowExhaustGas.show()#
        self.FlowExhaustGas1.show()#
        self.DTExhaustGas.show()#
        self.DTExhaustGas1.show()# 
        self.DTExhaustGas2.show()# 
        self.DTOffGasUse.show()# 
        self.DTOffGasUse1.show()# 
        self.QExhaustGasdot.show()#
        self.QExhaustGasdot1.show()#
        self.QExhaustGas.show()#
        self.QExhaustGas1.show()#

        self.QConvLoss.show()#
        self.QConvLoss1.show()#
        self.QWHEqTot.show()#
        self.QWHEqTot1.show()#
        self.QLossEq.show()#
        self.QLossEq1.show()#
        self.QInputEq.show()#
        self.QInputEq1.show()#
        self.QOutEq.show()#
        self.QOutEq1.show()#

        self.TExhaustGas.show()#
        self.TExhaustGas1.show()#
        self.ExcessAirRatio.show()#
        self.TMinOffGas.show()
        self.TMinOffGas1.show()
        self.OffGasUse.show()
        self.OffGasUse1.show()

              
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

        self.QWHEq.screen()#
        self.QExhaustGas.screen()#
        self.TExhaustGas.screen()#
        self.ExcessAirRatio.screen()#
        self.FlowExhaustGas.screen ()#
#------------------------------------------------------------------------------
    def check(self):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   main function carrying out the check of the block
#------------------------------------------------------------------------------
#        print "CheckEq - TESTPRINT TESTPRINT"
#        print "track of USHj"
#        self.USHj.show()
#        print self.USHj.track

        if DEBUG in ["ALL","MAIN"]:
            print "-------------------------------------------------"
            print " Equipment checking"
            print "-------------------------------------------------"


        for n in range(1):

            if DEBUG in ["ALL","MAIN"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

                print "Step 1: calculating from left to right (CALC)"
            

            self.FlowCombAir1 = calcProdC("FlowCombAir1",self.CombAir,self.FuelConsum,self.ExcessAirRatio) # 
            self.FlowExhaustGas1 = calcSum("FlowExhaustGas1",self.FlowCombAir,self.FuelConsum1)#
            self.QExhaustGasdot1 = calcFlow("QExhaustGasdot1",self.OffgasHeatCapacity,self.FlowExhaustGas,self.TExhaustGas1,
                                            self.TEnvEq,self.DTExhaustGas,self.DTExhaustGas1)#
            self.HPerYearEq1 = calcProd("HPerYearEq1",self.HPerDayEq,self.NDaysEq)
            self.HPerYearEqNom1 = calcProd("HPerYearEqNom1",self.HPerYearEq,self.PartLoad)
            self.USHBoiler1 = calcProd("USHBoiler1",self.HCGPnom,self.HPerYearEqNom)
            self.FETel_c_j1 = calcProd("FETel_c_j1",self.ElectriConsum2,self.HPerYearEqNom2)
            self.FETel_j1 = calcDiff("FETel_j1",self.FETel_c_j,self.ElGen_j,parType="S")
            self.QExhaustGas1 = calcProd("QExhaustGas1",self.QExhaustGasdot,self.HPerYearEqNom3)#
            
            if self.mainSource == "Fuel":
#                print "CheckEq (calcs): fuel as main source"
                self.USHBoiler2 = calcProd("USHBoiler2",self.FETFuel_j,self.HCGTEfficiency1)
                self.HCGPnom1 = calcProdC("HCGPnom1",self.FuelLCV,self.FuelConsum2,self.HCGTEfficiency)#

                self.DTOffGasUse1 = calcProd("DTOffGasUse1",self.OffGasUse,self.DTExhaustGas)
                self.DTOffGasUse2 = calcDiff("DTOffGasUse2",self.TExhaustGas,self.TMinOffGas)
                self.QWHEq1 = calcProd("QWHEq1",self.OffGasUse,self.QWHEqTot)
            else:
                self.USHBoiler2 = calcProd("USHBoiler2",self.FETel_c_j,self.HCGTEfficiency1)
                self.HCGPnom1 = calcProd("HCGPnom1",self.ElectriConsum,self.HCGTEfficiency)

                self.DTOffGasUse1.setValue(0.0)
                self.DTOffGasUse2.setValue(0.0)
                self.QWHEq1.setValue(0.0)
                
            self.USHj1 = calcSum("USH1",self.USHBoiler,self.QHXEq)
            self.FETj1 = calcSum("FETj1",self.FETFuel_j,self.FETel_j,parType="S")

            self.QLossEq1= calcProd("QLossEq1",self.LossFactEq,self.USHj2)#
            self.QOutEq1 = calcSum("QOutEq1",self.QLossEq,self.USHj3)#
            self.QInputEq1 = calcSum("QInputEq1",self.FETj2,self.QHXEq1)#
            self.QWHEqTot1 = calcDiff("QWHEqTot1",self.QInputEq,self.QOutEq)

            if self.EquipeClass in ["BB"]:
#                print "checkEq in mode BB"
                self.QConvLoss1 = calcProd("QConvLoss1",self.ConvLoss,self.FETj3)
                self.QWHEqTot2 = calcDiff("QWHEqTot2",self.QConvLoss,self.QLossEq2)#

            elif self.EquipeClass == "CHP":
                self.ElGen_j1 = calcProd("ElGen_j1",self.ElectriProduction,self.HPerYearEqNom)
                self.ElGen_j2 = calcProd("ElGen_j2",self.FETFuel_j,self.HCGEEfficiency)
                self.ElectriProduction1 = calcProdC("ElectriProduction1",self.FuelLCV,self.FuelConsum2,self.HCGEEfficiency)
                   

            if DEBUG in ["ALL","MAIN"]:
                self.showAllUSH()

# Step 2: Cross check the variables

                print "Step 2: cross checking"

            self.ccheckAll()

            if DEBUG in ["ALL","MAIN"]:
                self.showAllUSH()

# Step 3: Adjust the variables (inverse of calculation routines)

                print "Step 3: calculating from right to left (ADJUST)"
            
            if self.EquipeClass in ["BB"]:
#                print "adjust in mode BB"
                adjustDiff(self.QWHEqTot2,self.QConvLoss,self.QLossEq2)#
                adjustProd(self.QConvLoss1,self.ConvLoss,self.FETj3)
                adjustSum(self.One,self.HCGTEfficiency2,self.ConvLoss2)

            adjustDiff(self.QWHEqTot1,self.QInputEq,self.QOutEq) #
            adjustSum(self.QInputEq1,self.FETj2,self.QHXEq1)#
            adjustSum(self.QOutEq1,self.QLossEq,self.USHj3)#
            adjustProd(self.QLossEq1,self.LossFactEq,self.USHj2)#

            adjustSum(self.FETj1,self.FETFuel_j,self.FETel_j)
            adjustSum(self.USHj1,self.USHBoiler,self.QHXEq)
            adjustProd(self.USHBoiler1,self.HCGPnom,self.HPerYearEqNom)

            if self.mainSource == "Fuel":

                adjustProd(self.QWHEq1,self.OffGasUse,self.QWHEqTot)
                adjustProd(self.DTOffGasUse1,self.OffGasUse,self.DTExhaustGas2)
                adjustDiff(self.DTOffGasUse2,self.TExhaustGas2,self.TMinOffGas)

                adjustProd(self.USHBoiler2,self.FETFuel_j2,self.HCGTEfficiency1)
                adjustProdC(self.HCGPnom1,self.FuelLCV,self.FuelConsum4,self.HCGTEfficiency)#
            else:
                adjustProd(self.USHBoiler2,self.FETel_c_j2,self.HCGTEfficiency1)
                adjustProd(self.HCGPnom1,self.ElectriConsum,self.HCGTEfficiency)

                self.OffGasUse.setValue(0.0)
                
            adjustProd(self.QExhaustGas1,self.QExhaustGasdot,self.HPerYearEqNom3)#
            adjustDiff(self.FETel_j1,self.FETel_c_j3,self.ElGen_j)
            adjustProd(self.FETel_c_j1,self.ElectriConsum2,self.HPerYearEqNom2)
            adjustProd(self.HPerYearEqNom1,self.HPerYearEq,self.PartLoad)
            adjustProd(self.HPerYearEq1,self.HPerDayEq,self.NDaysEq)

            adjustFlow(self.QExhaustGasdot1,self.OffgasHeatCapacity,self.FlowExhaustGas,self.TExhaustGas1,
                                            self.TEnvEq,self.DTExhaustGas,self.DTExhaustGas1)#
            adjustSum(self.FlowExhaustGas1,self.FlowCombAir,self.FuelConsum3)#
            adjustProdC(self.FlowCombAir1,self.CombAir,self.FuelConsum,self.ExcessAirRatio)

            if self.EquipeClass == "CHP":
                adjustProd(self.ElGen_j1,self.ElectriProduction,self.HPerYearEqNom4)
                adjustProd(self.ElGen_j2,self.FETFuel_j3,self.HCGEEfficiency)
                adjustProdC(self.ElectriProduction1,self.FuelLCV,self.FuelConsum2,self.HCGEEfficiency2)

            

            if DEBUG in ["ALL","MAIN"]:
                self.showAllUSH()
            
# Step 4: Cross check again the variables

                print "Step 4: second cross checking"

            self.ccheckAll()
            
            if DEBUG in ["ALL","MAIN"]:
                self.showAllUSH()

        if DEBUG in ["ALL","BASIC"]:
            self.showAllUSH()
        
#------------------------------------------------------------------------------
    def ccheckAll(self):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------

            ccheck3(self.HCGTEfficiency,self.HCGTEfficiency1,self.HCGTEfficiency2,self.HCGTEfficiency3)
            ccheck2(self.HCGEEfficiency,self.HCGEEfficiency1,self.HCGEEfficiency2)
            ccheck2(self.ConvLoss,self.ConvLoss1,self.ConvLoss2)#
            
            ccheck1(self.FlowCombAir,self.FlowCombAir1)#
            ccheck1(self.ExcessAirRatio,self.ExcessAirRatio1)#
            ccheck1(self.FlowExhaustGas,self.FlowExhaustGas1)#
            ccheck1(self.QExhaustGasdot,self.QExhaustGasdot1)#
            ccheck2(self.TExhaustGas,self.TExhaustGas1,self.TExhaustGas2)#
            ccheck1(self.TEnvEq,self.TEnvEq1)#
            ccheck1(self.HPerYearEq,self.HPerYearEq1)
            ccheck1(self.HPerDayEq,self.HPerDayEq1)
            ccheck4(self.HPerYearEqNom,self.HPerYearEqNom1,self.HPerYearEqNom2,self.HPerYearEqNom3,self.HPerYearEqNom4)
            ccheck1(self.HCGPnom,self.HCGPnom1)
            ccheck3(self.FETj,self.FETj1,self.FETj2,self.FETj3)#
            ccheck3(self.FETFuel_j,self.FETFuel_j1,self.FETFuel_j2,self.FETFuel_j3)
            ccheck3(self.FETel_c_j,self.FETel_c_j1,self.FETel_c_j2,self.FETel_c_j3)
            ccheck2(self.FETel_j,self.FETel_j1,self.FETel_j2)
            ccheck4(self.FuelConsum,self.FuelConsum1,self.FuelConsum2,self.FuelConsum3,self.FuelConsum4)#
            ccheck2(self.ElectriConsum,self.ElectriConsum1,self.ElectriConsum2)
            ccheck2(self.USHBoiler,self.USHBoiler1,self.USHBoiler2)
            ccheck2(self.QHXEq,self.QHXEq1,self.QHXEq2)#
            ccheck3(self.USHj,self.USHj1,self.USHj2,self.USHj3)#
            ccheck1(self.QConvLoss,self.QConvLoss1)#
            ccheck1(self.LossFactEq,self.LossFactEq1)#
            ccheck2(self.QLossEq,self.QLossEq1,self.QLossEq2)#
            ccheck1(self.QInputEq,self.QInputEq1)#
            ccheck1(self.QOutEq,self.QOutEq1)#
            ccheck4(self.QWHEqTot,self.QWHEqTot1,self.QWHEqTot2,self.QExhaustGas,self.QExhaustGas1)#It is done provisional. It is supposed the 2parameters to be same.To be modified
            ccheck1(self.QWHEq,self.QWHEq1)
            ccheck2(self.DTOffGasUse,self.DTOffGasUse1,self.DTOffGasUse2)
            ccheck1(self.OffGasUse,self.OffGasUse1)
            ccheck1(self.TMinOffGas,self.TMinOffGas1)
            ccheck2(self.DTExhaustGas,self.DTExhaustGas1,self.DTExhaustGas2)
            ccheck1(self.PartLoad,self.PartLoad1)#

            ccheck1(self.ElectriProduction,self.ElectriProduction1)
            ccheck3(self.ElGen_j,self.ElGen_j1,self.ElGen_j2,self.ElGen_j3)

#------------------------------------------------------------------------------
    def estimate(self):  
#------------------------------------------------------------------------------
#   estimates some of the data that are not sufficiently precise
#   should be a subset of the data that are within screen
#   (not necessarily ALL data have to be estimated)
#------------------------------------------------------------------------------

        if self.EquipeClass in ["BB"]:
            self.HCGTEfficiency.setEstimate(0.85,limits=(0.7,0.95))
                        
        elif self.EquipeClass in ["CH"]:
            self.HCGTEfficiency.setEstimate(3.5,limits=(2.5,5.0))
            
        elif self.EquipeClass in ["HP"]:
            self.HCGTEfficiency.setEstimate(5.0,limits=(2.0,8.0))
            
        elif self.EquipeClass in ["CHP"]:
            self.HCGTEfficiency.setEstimate(0.55,limits=(0.4,0.9))
            self.HCGEEfficiency.setEstimate(0.35,limits=(0.1,0.6))
            
        self.PartLoad.setEstimate(0.5,limits=(0.1,0.9))


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

