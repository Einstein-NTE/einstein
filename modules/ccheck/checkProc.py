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
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	08/03/2008
#	Last revised by:    Claudia Vannoni      7/04/2008
#                           Claudia Vannoni      16/04/2008
#                           Hans Schweiger      19/04/2008
#
#       Changes in last update: 
#       v004:adjustSum3
#           Nones eliminated in initialisation of sqerr
#       19/04/2008: HS  PT1,2,3 and PTInFlow1 added as tmp-variables
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



#------------------------------------------------------------------------------
class CheckProc():
#------------------------------------------------------------------------------
#   Carries out consistency checking for process k
#------------------------------------------------------------------------------
#UPHw not included yet
#QHXProc: recovered heat as input to the process k (source= matrix of ducts/processes). Not calculated yet
#UPHtotQ: total UPH from different sources = UPHProc+ QHXProc (the definition as to redefined into the questionnaire).
# Pay attention: both values used here per process k comes from matrix . At present assigned here.


    def __init__(self,k):     #function that is called at the beginning when object is created

# assign a variable to all intermediate values needed
        
        self.PT1 = CCPar("PT1") #HS2008-04-18 additional variable added
        self.PT2 = CCPar("PT2") #HS2008-04-18 additional variable added        
        self.PT3 = CCPar("PT3") #HS2008-04-18 additional variable added
        self.PTInFlow1 = CCPar("PTInFlow1") #HS2008-04-19 added
        self.TOpProc1 = CCPar("TOpProc1") 
        self.DTLoss1=CCPar("DTLoss1")
        self.DTLoss=CCPar("DTLoss")
        self.VInFlowDay1 = CCPar("VInFlowDay1") #HS2008-04-19 additional variable added
        self.VInFlowDay2 = CCPar("VInFlowDay1") #HS2008-04-19 additional variable added
        self.VInFlowDay3 = CCPar("VInFlowDay1") #HS2008-04-19 additional variable added
        self.QLoss = CCPar("QLoss")
        self.QLoss1 = CCPar("QLoss1")
        self.QOpProc1 = CCPar("QOpProc1")
        self.UPHm1 = CCPar("UPHm1")
        self.UPHm = CCPar("UPHm")
        self.DTUPHcGross1 = CCPar("DTUPHcGross1")
        self.DTUPHcGross = CCPar("DTUPHcGross")
        self.UPHcdotGross1 = CCPar("UPHcdotGross1")#For convention UPH and UPHc are net!
        self.UPHcdotGross = CCPar("UPHcdotGross")
        self.DTQHX1 = CCPar("DTQHX1")
        self.DTQHX2 = CCPar("DTQHX2")
        self.DTQHX = CCPar("DTQHX")
        self.QHXdotProcInt1 = CCPar("QHXdotProcInt1")
        self.QHXdotProcInt2 = CCPar("QHXdotProcInt2")
        self.QHXdotProcInt = CCPar("QHXdotProcInt")
        self.NBatchPerYear1 = CCPar("NBatchPerYear1")
        self.NBatchPerYear = CCPar("NBatchPerYear")
        self.DTUPHcNet1 = CCPar("DTUPHcNet1")
        self.DTUPHcNet = CCPar("DTUPHcNet")
        self.UPHcdot1 = CCPar("UPHcdot1")
        self.UPHcdot2 = CCPar("UPHcdot2")
        self.UPHcdot = CCPar("UPHcdot")
        self.UPHc1 = CCPar("UPHc1")
        self.UPHc = CCPar("UPHc")
        self.DTUPHs1 = CCPar("DTUPHs1")
        self.DTUPHs = CCPar("DTUPHs")
        self.UPHsdot1 = CCPar("UPHsdot1")
        self.UPHsdot = CCPar("UPHsdot")
        self.UPHs1 = CCPar("UPHs1")
        self.UPHs = CCPar("UPHs")
        self.UPH1 = CCPar("UPH1")
        self.UPH2 = CCPar("UPH2")
        self.UPH = CCPar("UPH")
        
        self.UPHcGross = CCPar("UPHcGross")
        self.QHXProcInt = CCPar("QHXProcInt")


        if TEST:
            self.importTestData(k)
        else:
#            self.importData()
            pass

    def importTestData(self,k):  #later on should import data from SQL. now simply sets to some value

        if TESTCASE == 2:       #original test case Kla - first version of FECel
            self.FluidCp = 0.001 # kWh/K*Kg # IMPORT Constant from the FluidDB
            self.FluidDensity = 1.03 # Kg/m3 # IMPORT Constant from the FluidDB
            

            self.PTInFlow = CCPar("PTInFlow")
            self.PTInFlow.val = 4
            self.PTInFlow.sqerr = 0.0

            self.PT = CCPar("PT")
            self.PT.val = 72
            self.PT.sqerr = 0.05

            self.PTOutFlow = CCPar("PTOutFlow") # assumed to be Tpor
            self.PTOutFlow.val = 37
            self.PTOutFlow.sqerr = 0.5

            self.PTpo = CCPar("PTpo") # It si not defined in the questionnaire. it has to be estimated
            self.PTpo.val = 35
            self.PTpo.sqerr = 0.5

            self.PTInFlowRec = CCPar("PTInFlowRec")
            self.PTInFlowRec.val = 50
            self.PTInFlowRec.sqerr = 0.5

            self.PTStartUp = CCPar("PTStartUp")
            self.PTStartUp.val = None
            self.PTStartUp.sqerr = INFINITE
            
            self.VInFlowDay = CCPar("VInFlowDay ")
            self.VInFlowDay.val = 4000
            self.VInFlowDay.sqerr = 0.0
            
            self.VolProcMed = CCPar("VolProcMed")
            self.VolProcMed.val = 15
            self.VolProcMed.sqerr = 0.1   #
            
            self.NDaysProc = CCPar("NDaysProc")
            self.NDaysProc.val = 260 # 5 days/week
            self.NDaysProc.sqerr = 0.0  #example: big uncertainty in operating hours

            self.HPerDayProc = CCPar("HPerDay")
            self.HPerDayProc.val = 10
            self.HPerDayProc.sqerr = 0.3  #example: uncertainty in operating hours

            self.NBatch = CCPar("NBatch")
            self.NBatch.val = 5
            self.NBatch.sqerr = 0.0

            self.TOpProc = CCPar("TOpProc")
            self.TOpProc.val = 6000
            self.TOpProc.sqerr = 0.5  #example: big uncertainty in operating hours

            self.UAProc = CCPar("UAProc")
            self.UAProc.val = 100
            self.UAProc.sqerr = 0.7

            self.TEnvProc = CCPar("TEnvProc")
            self.TEnvProc.val = 20
            self.TEnvProc.sqerr = 0.0

            self.QEvapProc = CCPar("QEvapProc")
            self.QEvapProc.val = 30000
            self.QEvapProc.sqerr = INFINITE
            
            self.QOpProc = CCPar("QOpProc")
            self.QOpProc.val = 50000
            self.QOpProc.sqerr = INFINITE
            
            self.UPHProc = CCPar("UPHProc")
            self.UPHProc.val = 5e+6
            self.UPHProc.sqerr = 0.05    #example: quantity of heat required is well known

            self.QHXProc = CCPar("QHXProc")# It comes from the matrix not from the questionnaire
            self.QHXProc.val = 1.e+6
            self.QHXProc.sqerr = 0

        elif TESTCASE == 3:       #original test case Kla - first version of FECel

            if (k==0):
                self.FluidCp = 0.001 # kWh/K*Kg # IMPORT Constant from the FluidDB
                self.FluidDensity = 1.03 # Kg/m3 # IMPORT Constant from the FluidDB
                

                self.PTInFlow = CCPar("PTInFlow")
                self.PTInFlow.val = 4
                self.PTInFlow.sqerr = 0.0

                self.PT = CCPar("PT")
                self.PT.val = 72
                self.PT.sqerr = 0.0

                self.PTOutFlow = CCPar("PTOutFlow") # assumed to be Tpor
                self.PTOutFlow.val = None
                self.PTOutFlow.sqerr = INFINITE

                self.PTpo = CCPar("PTpo") # It si not defined in the questionnaire. it has to be estimated
                self.PTpo.val = 50
                self.PTpo.sqerr = 0.0

                self.PTInFlowRec = CCPar("PTInFlowRec")
                self.PTInFlowRec.val = 50
                self.PTInFlowRec.sqerr = 0.0

                self.PTStartUp = CCPar("PTStartUp")
                self.PTStartUp.val = None
                self.PTStartUp.sqerr = INFINITE
                
                self.VInFlowDay = CCPar("VInFlowDay ")
                self.VInFlowDay.val = None
                self.VInFlowDay.sqerr = INFINITE
                
                self.VolProcMed = CCPar("VolProcMed")
                self.VolProcMed.val = 0.0
                self.VolProcMed.sqerr = 0.0   #
                
                self.NDaysProc = CCPar("NDaysProc")
                self.NDaysProc.val = 250 # 5 days/week
                self.NDaysProc.sqerr = 0.0  #example: big uncertainty in operating hours

                self.HPerDayProc = CCPar("HPerDay")
                self.HPerDayProc.val = 16
                self.HPerDayProc.sqerr = 0.0  #example: uncertainty in operating hours

                self.NBatch = CCPar("NBatch")
                self.NBatch.val = 5
                self.NBatch.sqerr = 0.0

                self.TOpProc = CCPar("TOpProc")
                self.TOpProc.val = 4000
                self.TOpProc.sqerr = 0.0  #example: big uncertainty in operating hours

                self.UAProc = CCPar("UAProc")
                self.UAProc.val = 0.0
                self.UAProc.sqerr = 0.0

                self.TEnvProc = CCPar("TEnvProc")
                self.TEnvProc.val = 20
                self.TEnvProc.sqerr = 0.0

                self.QEvapProc = CCPar("QEvapProc")
                self.QEvapProc.val = None
                self.QEvapProc.sqerr = INFINITE
                
                self.QOpProc = CCPar("QOpProc")
                self.QOpProc.val = 0.0
                self.QOpProc.sqerr = 0.0
                
                self.UPHProc = CCPar("UPHProc")
                self.UPHProc.val = 5000
                self.UPHProc.sqerr = 0.0    #example: quantity of heat required is well known

                self.QHXProc = CCPar("QHXProc")# It comes from the matrix not from the questionnaire
                self.QHXProc.val = 0
                self.QHXProc.sqerr = 0

            elif (k==1):
                self.FluidCp = 0.001 # kWh/K*Kg # IMPORT Constant from the FluidDB
                self.FluidDensity = 1.03 # Kg/m3 # IMPORT Constant from the FluidDB
                

                self.PTInFlow = CCPar("PTInFlow")
                self.PTInFlow.val = 4
                self.PTInFlow.sqerr = 0.0

                self.PT = CCPar("PT")
                self.PT.val = 72
                self.PT.sqerr = 0.0

                self.PTOutFlow = CCPar("PTOutFlow") # assumed to be Tpor
                self.PTOutFlow.val = None
                self.PTOutFlow.sqerr = INFINITE

                self.PTpo = CCPar("PTpo") # It si not defined in the questionnaire. it has to be estimated
                self.PTpo.val = 50
                self.PTpo.sqerr = 0.0

                self.PTInFlowRec = CCPar("PTInFlowRec")
                self.PTInFlowRec.val = 50
                self.PTInFlowRec.sqerr = 0.0

                self.PTStartUp = CCPar("PTStartUp")
                self.PTStartUp.val = None
                self.PTStartUp.sqerr = INFINITE
                
                self.VInFlowDay = CCPar("VInFlowDay ")
                self.VInFlowDay.val = None
                self.VInFlowDay.sqerr = INFINITE
                
                self.VolProcMed = CCPar("VolProcMed")
                self.VolProcMed.val = 0.0
                self.VolProcMed.sqerr = 0.0   #
                
                self.NDaysProc = CCPar("NDaysProc")
                self.NDaysProc.val = 250 # 5 days/week
                self.NDaysProc.sqerr = 0.0  #example: big uncertainty in operating hours

                self.HPerDayProc = CCPar("HPerDay")
                self.HPerDayProc.val = 16
                self.HPerDayProc.sqerr = 0.0  #example: uncertainty in operating hours

                self.NBatch = CCPar("NBatch")
                self.NBatch.val = 5
                self.NBatch.sqerr = 0.0

                self.TOpProc = CCPar("TOpProc")
                self.TOpProc.val = 4000
                self.TOpProc.sqerr = 0.0  #example: big uncertainty in operating hours

                self.UAProc = CCPar("UAProc")
                self.UAProc.val = 0.0
                self.UAProc.sqerr = 0.0

                self.TEnvProc = CCPar("TEnvProc")
                self.TEnvProc.val = 20
                self.TEnvProc.sqerr = 0.0

                self.QEvapProc = CCPar("QEvapProc")
                self.QEvapProc.val = None
                self.QEvapProc.sqerr = INFINITE
                
                self.QOpProc = CCPar("QOpProc")
                self.QOpProc.val = 0.0
                self.QOpProc.sqerr = 0.0
                
                self.UPHProc = CCPar("UPHProc")
                self.UPHProc.val = 2000
                self.UPHProc.sqerr = 0.0    #example: quantity of heat required is well known

                self.QHXProc = CCPar("QHXProc")# It comes from the matrix not from the questionnaire
                self.QHXProc.val = 0
                self.QHXProc.sqerr = 0
                
            elif (k==2):
                self.FluidCp = 0.001 # kWh/K*Kg # IMPORT Constant from the FluidDB
                self.FluidDensity = 1.03 # Kg/m3 # IMPORT Constant from the FluidDB
                

                self.PTInFlow = CCPar("PTInFlow")
                self.PTInFlow.val = 4
                self.PTInFlow.sqerr = 0.0

                self.PT = CCPar("PT")
                self.PT.val = 72
                self.PT.sqerr = 0.0

                self.PTOutFlow = CCPar("PTOutFlow") # assumed to be Tpor
                self.PTOutFlow.val = None
                self.PTOutFlow.sqerr = INFINITE

                self.PTpo = CCPar("PTpo") # It si not defined in the questionnaire. it has to be estimated
                self.PTpo.val = 50
                self.PTpo.sqerr = 0.0

                self.PTInFlowRec = CCPar("PTInFlowRec")
                self.PTInFlowRec.val = 50
                self.PTInFlowRec.sqerr = 0.0

                self.PTStartUp = CCPar("PTStartUp")
                self.PTStartUp.val = None
                self.PTStartUp.sqerr = INFINITE
                
                self.VInFlowDay = CCPar("VInFlowDay ")
                self.VInFlowDay.val = None
                self.VInFlowDay.sqerr = INFINITE
                
                self.VolProcMed = CCPar("VolProcMed")
                self.VolProcMed.val = 0.0
                self.VolProcMed.sqerr = 0.0   #
                
                self.NDaysProc = CCPar("NDaysProc")
                self.NDaysProc.val = 250 # 5 days/week
                self.NDaysProc.sqerr = 0.0  #example: big uncertainty in operating hours

                self.HPerDayProc = CCPar("HPerDay")
                self.HPerDayProc.val = 16
                self.HPerDayProc.sqerr = 0.0  #example: uncertainty in operating hours

                self.NBatch = CCPar("NBatch")
                self.NBatch.val = 5
                self.NBatch.sqerr = 0.0

                self.TOpProc = CCPar("TOpProc")
                self.TOpProc.val = 4000
                self.TOpProc.sqerr = 0.0  #example: big uncertainty in operating hours

                self.UAProc = CCPar("UAProc")
                self.UAProc.val = 0.0
                self.UAProc.sqerr = 0.0

                self.TEnvProc = CCPar("TEnvProc")
                self.TEnvProc.val = 20
                self.TEnvProc.sqerr = 0.0

                self.QEvapProc = CCPar("QEvapProc")
                self.QEvapProc.val = None
                self.QEvapProc.sqerr = INFINITE
                
                self.QOpProc = CCPar("QOpProc")
                self.QOpProc.val = 0.0
                self.QOpProc.sqerr = 0.0
                
                self.UPHProc = CCPar("UPHProc")
                self.UPHProc.val = None
                self.UPHProc.sqerr = INFINITE    #example: quantity of heat required is well known

                self.QHXProc = CCPar("QHXProc")# It comes from the matrix not from the questionnaire
                self.QHXProc.val = 0.0
                self.QHXProc.sqerr = 0.0

        else:
            print "CheckUSH: WARNING - don't have input data for this test case no. ",TESTCASE

        if DEBUG in ["ALL"]:
            self.showAllUPH()

    def showAllUPH(self):
        print "====================="
        self.UPH.show()
        self.UPH1.show()
        self.UPH2.show()
        self.UPHm.show()
        self.UPHs.show()
        self.UPHc.show()
        self.UPHc1.show()
        self.UPHcdot.show()
        self.UPHcdotGross.show()
        self.UPHcGross.show()
        self.DTUPHcGross.show()
        self.UPHcGross.show()
        self.QHXProcInt.show()
        self.QOpProc.show()
        self.QOpProc1.show()
        self.VolProcMed.show()
        self.TOpProc.show()
        self.TOpProc1.show()
        self.HPerDayProc.show()
        self.NDaysProc.show()
        self.VInFlowDay.show()
        self.PTInFlow.show()
        self.PTInFlow1.show()
        self.PT.show()
        self.PT1.show()
        self.PT2.show()
        self.PT3.show()
        self.PTInFlowRec.show()
        self.PTOutFlow.show()
        self.PTStartUp.show()
        self.PTpo.show()
        self.NBatch.show()
        self.UAProc.show()
        self.QEvapProc.show()
        self.TEnvProc.show()  
        self.DTLoss1.show()
        self.DTLoss.show()
        self.QLoss.show()
        self.QLoss1.show()
        self.UPHm1.show()
        self.DTUPHcGross1.show()
        self.DTUPHcGross.show()
        self.UPHcdotGross1.show()#For convention UPH and UPHc are net!
        self.DTQHX1.show()
        self.DTQHX2.show()
        self.DTQHX.show()
        self.QHXdotProcInt1.show()
        self.QHXdotProcInt2.show()
        self.QHXdotProcInt.show()
        self.NBatchPerYear1.show()
        self.NBatchPerYear.show()
        self.DTUPHcNet1.show()
        self.DTUPHcNet.show()
        self.UPHcdot1.show()
        self.UPHcdot2.show()
        self.UPHcdot.show()
        self.DTUPHs1.show()
        self.DTUPHs.show()
        self.UPHsdot1.show()
        self.UPHsdot.show()
        self.UPHs1.show()
                
        print "====================="
    
    def check(self):     #function that is called at the beginning when object is created
        if DEBUG in ["ALL"]:
            print "-------------------------------------------------"
            print " Process checking"
            print "-------------------------------------------------"

        for n in range(5):

            if DEBUG in ["ALL"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

            if DEBUG in ["ALL"]:
                print "-------------------------------------------------"
                print "Step 1: calculating from left to right (CALC)"
                print "-------------------------------------------------"
                
            self.TOpProc1 = calcProd("TOpProc1",self.NDaysProc,self.HPerDayProc)
            self.DTLoss1 = calcDiff("DTLoss1",self.PT,self.TEnvProc)
            self.QLoss1 = calcProd("QLoss1",self.UAProc,self.DTLoss)
            # UA: add suggestion how to calculate
            self.QOpProc1 = calcSum("QOpProc1",self.QLoss,self.QEvapProc)
            self.UPHm1 = calcProd("UPHm1",self.QOpProc,self.TOpProc)
            self.UPHcdotGross1 = calcFlow("UPHcdotGross1",self.FluidCp,self.VInFlowDay,self.PT1,self.PTInFlow,self.DTUPHcGross,self.DTUPHcGross1)
            self.QHXdotProcInt1 = calcFlow("QHXdotProcInt1",self.FluidCp,self.VInFlowDay1,self.PTpo,self.PTOutFlow,self.DTQHX,self.DTQHX1)
            self.QHXdotProcInt2 = calcFlow("QHXdotProcInt2",self.FluidCp,self.VInFlowDay2,self.PTInFlowRec,self.PTInFlow1,self.DTQHX,self.DTQHX2)
            self.UPHcdot1 = calcDiff("UPHcdot1",self.UPHcdotGross,self.QHXdotProcInt)
            self.UPHcdot2 = calcFlow("UPHcdot2",self.FluidCp,self.VInFlowDay3,self.PT2,self.PTInFlowRec,self.DTUPHcNet,self.DTUPHcNet1)
            self.UPHc1 = calcProd("UPHc1",self.UPHcdot,self.NDaysProc)
            self.UPHsdot1 = calcFlow("UPHsdot1",(self.FluidCp*self.FluidDensity),self.VolProcMed,self.PT3,self.PTStartUp,self.DTUPHs,self.DTUPHs1)
            self.NBatchPerYear1 =calcProd("NbatchPeryear1",self.NDaysProc,self.NBatch)
            self.UPHs1 = calcProd("UPHs1",self.UPHsdot,self.NBatchPerYear)
            self.UPH1 = calcSum3("UPH1",self.UPHm,self.UPHc,self.UPHs)
            self.UPH2 = calcSum("UPH2",self.UPHProc,self.QHXProc)

          
            if DEBUG in ["ALL"]:
                self.showAllUPH()

# Step 2: Cross check the variables

                print "-------------------------------------------------"
                print "Step 2: cross checking"
                print "-------------------------------------------------"
                
            ccheck3(self.PT,self.PT1,self.PT2,self.PT3)  #HS2008-04-18 -> brings into coincidence the different PT's
            ccheck1(self.PTInFlow,self.PTInFlow1)
            ccheck3(self.VInFlowDay,self.VInFlowDay1,self.VInFlowDay2,self.VInFlowDay3)
            
            ccheck1(self.TOpProc,self.TOpProc1)
            ccheck1(self.DTLoss,self.DTLoss1)
            ccheck1(self.QLoss,self.QLoss1)
            ccheck1(self.QOpProc,self.QOpProc1)
            ccheck1(self.UPHm,self.UPHm1)
            ccheck1(self.UPHcdotGross,self.UPHcdotGross1)
            ccheck2(self.QHXdotProcInt,self.QHXdotProcInt1,self.QHXdotProcInt2)
            ccheck2(self.UPHcdot,self.UPHcdot1,self.UPHcdot2)
            ccheck1(self.UPHc,self.UPHc1)
            ccheck1(self.UPHsdot,self.UPHsdot1)
            ccheck1(self.NBatchPerYear,self.NBatchPerYear1)
            ccheck1(self.UPHs,self.UPHs1)
            ccheck2(self.UPH,self.UPH1,self.UPH2)
            

            if DEBUG in ["ALL"]:
                self.showAllUPH()

# Step 3: Adjust the variables (inverse of calculation routines)
                print "-------------------------------------------------"
                print "Step 3: calculating from right to left (ADJUST)"
                print "-------------------------------------------------"
                
            adjustSum(self.UPH2,self.UPHProc,self.QHXProc)
            adjustSum3(self.UPH1,self.UPHm,self.UPHc,self.UPHs)
            adjustProd(self.UPHs1,self.UPHsdot1,self.NBatchPerYear)
            adjustProd(self.NBatchPerYear1,self.NDaysProc,self.NBatch)
            adjustFlow(self.UPHsdot1,(self.FluidCp*self.FluidDensity),self.VolProcMed,self.PT3,self.PTStartUp,self.DTUPHs,self.DTUPHs1)
            adjustProd(self.UPHc1,self.UPHcdot,self.NDaysProc)
            adjustFlow(self.UPHcdot2,self.FluidCp,self.VInFlowDay3,self.PT2,self.PTInFlowRec,self.DTUPHcNet,self.DTUPHcNet1)
            adjustDiff(self.UPHcdot1,self.UPHcdotGross,self.QHXdotProcInt)
            adjustFlow(self.QHXdotProcInt2,self.FluidCp,self.VInFlowDay2,self.PTInFlowRec,self.PTInFlow1,self.DTQHX,self.DTQHX2)
            adjustFlow(self.QHXdotProcInt1,self.FluidCp,self.VInFlowDay1,self.PTpo,self.PTOutFlow,self.DTQHX,self.DTQHX1)
            adjustFlow(self.UPHcdotGross1,self.FluidCp,self.VInFlowDay,self.PT1,self.PTInFlow,self.DTUPHcGross,self.DTUPHcGross1)
            adjustProd(self.UPHm1,self.QOpProc,self.TOpProc)
            adjustSum(self.QOpProc1,self.QLoss,self.QEvapProc)
            adjustProd(self.QLoss1,self.UAProc,self.DTLoss)
            adjustDiff(self.DTLoss1,self.PT,self.TEnvProc)
            adjustProd(self.TOpProc1,self.NDaysProc,self.HPerDayProc)
            
            if DEBUG in ["ALL"]:
                self.showAllUPH()
           
# Step 4: Second cross check of the variables

                print "-------------------------------------------------"
                print "Step 4: cross checking"
                print "-------------------------------------------------"
                
            ccheck3(self.PT,self.PT1,self.PT2,self.PT3)  #HS2008-04-18 -> brings into coincidence the different PT's
            ccheck1(self.PTInFlow,self.PTInFlow1)
            ccheck3(self.VInFlowDay,self.VInFlowDay1,self.VInFlowDay2,self.VInFlowDay3)
            
            ccheck1(self.TOpProc,self.TOpProc1)
            ccheck1(self.DTLoss,self.DTLoss1)
            ccheck1(self.QLoss,self.QLoss1)
            ccheck1(self.QOpProc,self.QOpProc1)
            ccheck1(self.UPHm,self.UPHm1)
            ccheck1(self.UPHcdotGross,self.UPHcdotGross1)
            ccheck2(self.QHXdotProcInt,self.QHXdotProcInt1,self.QHXdotProcInt2)
            ccheck2(self.UPHcdot,self.UPHcdot1,self.UPHcdot2)
            ccheck1(self.UPHc,self.UPHc1)
            ccheck1(self.UPHsdot,self.UPHsdot1)
            ccheck1(self.NBatchPerYear,self.NBatchPerYear1)
            ccheck1(self.UPHs,self.UPHs1)
            ccheck2(self.UPH,self.UPH1,self.UPH2)
            

            if DEBUG in ["ALL"]:
                self.showAllUPH()

# Arrived at the end

        self.UPHcGross = calcProd("UPHcGross",self.UPHcdotGross,self.NDaysProc)# Not adjusted
        self.QHXProcInt = calcProd("QHXProcInt",self.QHXdotProcInt,self.NDaysProc) # Not adjusted 

    #añadido este último show all. sino no se ven los ultimos dos resultados ...
        if DEBUG in ["ALL","BASIC"]:
            self.showAllUPH()


#==============================================================================
if __name__ == "__main__":
    
    ccProc = CheckProc(2)       # creates an instance of class CCheck
    ccProc.check()
