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
#	Version No.: 0.07
#	Created by: 	    Hans Schweiger	08/03/2008
#	Last revised by:    Claudia Vannoni      7/04/2008
#                           Claudia Vannoni      16/04/2008
#                           Hans Schweiger      19/04/2008
#                           Claudia Vannoni      25/04/2008
#                           Claudia Vannoni      27/04/2008
#              v0.07        Hans Schweiger      07/05/2008
#                           Claudia Vannoni      3/07/2008
#                           Hans Schweiger      04/07/2008
#                    
#
#       Changes in last update: 
#       v004:adjustSum3
#           Nones eliminated in initialisation of sqerr
#       19/04/2008: HS  PT1,2,3 and PTInFlow1 added as tmp-variables
#       v005: import from SQL, PT, ccheck of USHProc1
#       v0.06: small changes in labels,added the connection to the DB.
#       v0.07: importData - import of UPH instead of UPHProc
#               PTOutFlow1, VOutFlow and VOutFLow1 added
#               VInFlowDay3 eliminated
#       2/07/2008: VoutFlow,parameter list in screen, change of priority, import from FluidDb,
#                  Partype, constraints val max
#       04/07/2008: HS  Cross DT added in heat exchangers
#                       UPHw calculation added
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
from einstein.modules.fluids import *

#libraries necessary for SQL access:
from einstein.GUI.status import *
import einstein.GUI.pSQL as pSQL, MySQLdb

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


# assign a variable to all intermediate/calculated values needed
        
        self.PT1 = CCPar("PT1") 
        self.PT2 = CCPar("PT2")         
        self.PT3 = CCPar("PT3") 
        self.PT4 = CCPar("PT4") 
        self.PTInFlow1 = CCPar("PTInFlow1")
        self.PTInFlow2 = CCPar("PTInFlow2")
        self.PTInFlowRec1 = CCPar("PTInFlowRec1")
        self.PTInFlowRec2 = CCPar("PTInFlowRec2")
        self.PTInFlowRec3 = CCPar("PTInFlowRec3")
        self.PTOutFlow1 = CCPar("PTOutFlow1")
        self.PTOutFlow2 = CCPar("PTOutFlow2")
        self.PTOutFlow3 = CCPar("PTOutFlow3")
        self.PTOutFlowRec1 = CCPar("PTOUtFlowRec1")
        self.PTOutFlowRec2 = CCPar("PTOUtFlowRec2")
        self.PTFinal = CCPar("PTFinal",parType = "T")
        self.PTFinal1 = CCPar("PTFinal1")
        self.HPerYearProc1 = CCPar("HPerYearProc1")
        self.HPerYearProc = CCPar("HPerYearProc",priority=2)
        self.HPerYearProc.valMax = 8760
        self.DTLoss1=CCPar("DTLoss1")
        self.DTLoss=CCPar("DTLoss")
        self.VInFlowDay1 = CCPar("VInFlowDay1") 
        self.VInFlowDay2 = CCPar("VInFlowDay2") 
        self.VOutFlow1 = CCPar("VOutFlow1")
        self.VOutFlow2 = CCPar("VOutFlow2")
        self.QLoss = CCPar("QLoss")
        self.QLoss1 = CCPar("QLoss1")
        self.QOpProc1 = CCPar("QOpProc1")
        self.UPHm1 = CCPar("UPHm1")
        self.UPHm = CCPar("UPHm")
        self.DTUPHcGross1 = CCPar("DTUPHcGross1")
        self.DTUPHcGross = CCPar("DTUPHcGross",parType="DT")
        self.UPHcdotGross1 = CCPar("UPHcdotGross1")#For convention UPH and UPHc are net!
        self.UPHcdotGross = CCPar("UPHcdotGross")
        self.DTQHXIn = CCPar("DTQHXIn",parType="DT")
        self.DTQHXIn1 = CCPar("DTQHXIn1")
        self.DTQHXOut = CCPar("DTQHXOut",parType="DT")
        self.DTQHXOut1 = CCPar("DTQHXOut1")
        self.DTCrossHXLT = CCPar("DTCrossHXLT",parType="DT")
        self.DTCrossHXLT.valMin = 5.0   #engineering lower limit
        self.DTCrossHXLT1 = CCPar("DTCrossHXLT1")
        self.DTCrossHXHT = CCPar("DTCrossHXHT",parType="DT")
        self.DTCrossHXHT1 = CCPar("DTCrossHXHT1")
        self.DTCrossHXHT.valMin = 5.0   #engineering lower limit
        self.DTOutFlow = CCPar("DTOutFlow",parType="DT")
        self.DTOutFlow1 = CCPar("DTOutFlow1",parType="DT")
        self.QHXdotProcInt1 = CCPar("QHXdotProcInt1")
        self.QHXdotProcInt2 = CCPar("QHXdotProcInt2")
        self.QHXdotProcInt = CCPar("QHXdotProcInt")
        self.NBatchPerYear1 = CCPar("NBatchPerYear1")
        self.NBatchPerYear = CCPar("NBatchPerYear")
        self.DTUPHcNet1 = CCPar("DTUPHcNet1")
        self.DTUPHcNet = CCPar("DTUPHcNet",parType="DT")
        self.UPHcdot1 = CCPar("UPHcdot1")
        self.UPHcdot2 = CCPar("UPHcdot2")
        self.UPHcdot = CCPar("UPHcdot")
        self.UPHc1 = CCPar("UPHc1")
        self.UPHc = CCPar("UPHc")
        self.DTUPHs1 = CCPar("DTUPHs1")
        self.DTUPHs = CCPar("DTUPHs",parType="DT")
        self.UPHsdot1 = CCPar("UPHsdot1")
        self.UPHsdot = CCPar("UPHsdot")
        self.UPHs1 = CCPar("UPHs1")
        self.UPHs = CCPar("UPHs")
        self.UPH1 = CCPar("UPH1")
        self.UPH2 = CCPar("UPH2")
        self.UPH = CCPar("UPH")
        self.UPHw = CCPar("UPHw")
        self.UPHw1 = CCPar("UPHw1")
        self.UPHw_dot = CCPar("UPHw_dot")
        self.UPHw_dot1 = CCPar("UPHw_dot1")
        self.UPHProc1 = CCPar("UPHProc1")
        self.QHXProc1 = CCPar("QHXProc1")
        self.UAProc = CCPar("UAProc")
        self.QEvapProc = CCPar("QEvapProc")
        self.UPHcGross = CCPar("UPHcGross")
        self.QHXProcInt = CCPar("QHXProcInt")


        if TEST==True:
            self.importTestData(k)
        else:
            self.importData(k)

        if DEBUG in ["ALL","BASIC"]:
            self.showAllUPH()
#------------------------------------------------------------------------------
    def importData(self,k):  
#------------------------------------------------------------------------------
#   imports data from SQL tables (from AlternativeProposalNo = -1)
#------------------------------------------------------------------------------

        self.ProcNo = k+1
        ANo = -1
        
#..............................................................................
# assign empty CCPar to all questionnaire parameters

        
        self.PTInFlow = CCPar("PTInFlow",parType="T")
        self.PT = CCPar("PT",priority=2)
        self.PTOutFlow = CCPar("PTOutFlow", parType="T")# assumed to be Tpor
        self.PTOutFlowRec = CCPar("PTOutFlowRec",parType="T") # It is not defined in the questionnaire. it has to be estimated
        self.PTInFlowRec = CCPar("PTInFlowRec",parType="T")
        self.PTStartUp = CCPar("PTStartUp",parType="T")
        self.VInFlowDay = CCPar("VInFlowDay ")
        self.VOutFlow = CCPar("VOutFlow")
        self.VolProcMed = CCPar("VolProcMed")
        self.NDaysProc = CCPar("NDaysProc")
        self.NDaysProc.valMax = 365
        self.HPerDayProc = CCPar("HPerDay")
        self.HPerDayProc.valMax = 24
        self.NBatch = CCPar("NBatch")
        self.TEnvProc = CCPar("TEnvProc",parType="T")
        self.QOpProc = CCPar("QOpProc")
        self.UPHProc = CCPar("UPHProc")

        self.QHXProc = CCPar("QHXProc")# It comes from the matrix (and from calculation from questionnaire??)
        
        
#..............................................................................
# reading data from table "qprocessdata"
        try:
            qprocessdataTable = Status.DB.qprocessdata.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].ProcNo[self.ProcNo]
            
            if len(qprocessdataTable) > 0:
                qprocessdata = qprocessdataTable[0]

                fluid_number = qprocessdata.ProcMedDBFluid_id   #IMPORT from the FluidDB
                proc_fluid = Fluid(fluid_number)
                self.FluidCp = proc_fluid.cp
                self.FluidDensity = proc_fluid.rho
                #self.FluidCp = 0.001 # kWh/K*Kg # IMPORT Constant from the FluidDB
                #self.FluidDensity = 1000 # Kg/m3 # IMPORT Constant from the FluidDB

                self.PTInFlow.setValue(qprocessdata.PTInFlow)
                self.PT.setValue(qprocessdata.PT)
                self.PTOutFlow.setValue(qprocessdata.PTOutFlow)
                self.PTOutFlowRec.setValue(qprocessdata.PTOutFlowRec)
                self.PTInFlowRec.setValue(qprocessdata.PTInFlowRec) 
                self.PTStartUp.setValue(qprocessdata.PTStartUp)
                self.PTFinal.setValue(qprocessdata.PTFinal)
                self.VInFlowDay.setValue(qprocessdata.VInFlowDay) 
                self.VOutFlow.setValue(qprocessdata.VOutFlow) 
                self.VolProcMed.setValue(qprocessdata.VolProcMed) 
                self.NDaysProc.setValue(qprocessdata.NDaysProc)
                self.HPerDayProc.setValue(qprocessdata.HPerDayProc) 
                self.NBatch.setValue(qprocessdata.NBatch) 
                self.TEnvProc.setValue(qprocessdata.TEnvProc)
                self.QOpProc.setValue(qprocessdata.QOpProc) 
                self.UPH.setValue(qprocessdata.UPH) 

                self.QHXProc.setValue(0.0)  
               
        except:
            print "CheckProc(importData): error reading data from qprocessdata"
            pass

#------------------------------------------------------------------------------
    def exportData(self):  
#------------------------------------------------------------------------------
#   stores corrected data in SQL (under AlternativeProposalNo = 0)
#------------------------------------------------------------------------------

        ANo = 0
        
#..............................................................................
# writing data into table " qprocessdata"
#        try:
        if ANo == 0:
            qprocessdataTable = Status.DB.qprocessdata.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].ProcNo[self.ProcNo]
            if len(qprocessdataTable) > 0:
                print "exporting data to qprocessdata"
                qprocessdata = qprocessdataTable[0]

        
                qprocessdata.PTInFlow = self.PTInFlow.val
                qprocessdata.PT = self.PT.val
                qprocessdata.PTOutFlow = self.PTOutFlow.val
                qprocessdata.PTOutFlowRec = self.PTOutFlowRec.val #do not exist yet
                qprocessdata.PTInFlowRec = self.PTInFlowRec.val
                qprocessdata.PTStartUp = self.PTStartUp.val
                qprocessdata.PTFinal = self.PTFinal.val
                qprocessdata.VInFlowDay = self.VInFlowDay.val
                qprocessdata.VolProcMed = self.VolProcMed.val
                qprocessdata.NDaysProc = self.NDaysProc.val
                qprocessdata.HPerDayProc = self.HPerDayProc.val
                qprocessdata.NBatch = self.NBatch.val
                qprocessdata.TEnvProc = self.TEnvProc.val
                qprocessdata.QOpProc = self.QOpProc.val
                qprocessdata.UPHProc = self.UPHProc.val
                qprocessdata.HPerYearProc = self.HPerYearProc.val
                qprocessdata.UAProc = self.UAProc.val
                qprocessdata.QEvapProc = self.QEvapProc.val
                qprocessdata.UPHcGross = self.UPHcGross.val
                qprocessdata.QHXProcInt = self.QHXProcInt.val
                qprocessdata.UPHm = self.UPHm.val
                qprocessdata.UPHs = self.UPHs.val
                qprocessdata.UPHc = self.UPHc.val
                qprocessdata.UPH = self.UPH.val
                qprocessdata.UPHw = self.UPHw.val
                                       

                Status.SQL.commit()
                
            else:
                print "CheckProc (exportData): error writing data to qprocessdata"
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

            self.PTOutFlowRec = CCPar("PTOutFlowRec") # It is not defined in the questionnaire. it has to be estimated
            self.PTOutFlowRec.val = 35
            self.PTOutFlowRec.sqerr = 0.5

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

            self.HPerYearProc = CCPar("HPerYearProc")
            self.HPerYearProc.val = None
            self.HPerYearProc.sqerr = INFINITE  

            self.TEnvProc = CCPar("TEnvProc")
            self.TEnvProc.val = 20
            self.TEnvProc.sqerr = 0.0

            self.QEvapProc = CCPar("QEvapProc")# not into questionnaire only for test
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

                self.PTOutFlowRec = CCPar("PTOutFlowRec") # It si not defined in the questionnaire. it has to be estimated
                self.PTOutFlowRec.val = 50
                self.PTOutFlowRec.sqerr = 0.0

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

                self.HPerYearProc = CCPar("HPerYearProc")
                self.HPerYearProc.val = None
                self.HPerYearProc.sqerr = INFINITE  

                
                self.TEnvProc = CCPar("TEnvProc")
                self.TEnvProc.val = 20
                self.TEnvProc.sqerr = 0.0

                                
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

                self.PTOutFlowRec = CCPar("PTOutFlowRec") # It si not defined in the questionnaire. it has to be estimated
                self.PTOutFlowRec.val = 50
                self.PTOutFlowRec.sqerr = 0.0

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

                self.HPerYearProc = CCPar("HPerYearProc")
                self.HPerYearProc.val = None
                self.HPerYearProc.sqerr = INFINITE  

                
                self.TEnvProc = CCPar("TEnvProc")
                self.TEnvProc.val = 20
                self.TEnvProc.sqerr = 0.0

                                
                self.QOpProc = CCPar("QOpProc")
                self.QOpProc.val = 0.0
                self.QOpProc.sqerr = 0.0
                
                self.UPHProc = CCPar("UPHProc")
                self.UPHProc.val = 2000
                self.UPHProc.sqerr = 0.0    #example: quantity of heat required is well known

                self.QHXProc = CCPar("QHXProc")# It comes from the matrix not from the questionnaire
                self.QHXProc.val = None
                self.QHXProc.sqerr = INFINITE

                
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

                self.PTOutFlowRec = CCPar("PTOutFlowRec") # It si not defined in the questionnaire. it has to be estimated
                self.PTOutFlowRec.val = 50
                self.PTOutFlowRec.sqerr = 0.0

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

                self.HPerYearProc = CCPar("HPerYearProc")
                self.HPerYearProc.val = None
                self.HPerYearProc.sqerr = INFINITE  

                
                self.TEnvProc = CCPar("TEnvProc")
                self.TEnvProc.val = 20
                self.TEnvProc.sqerr = 0.0

                
                self.QOpProc = CCPar("QOpProc")
                self.QOpProc.val = 0.0
                self.QOpProc.sqerr = 0.0
                
                self.UPHProc = CCPar("UPHProc")# It comes from the questionnaire
                self.UPHProc.val = None
                self.UPHProc.sqerr = INFINITE


                self.QHXProc = CCPar("QHXProc")# It comes from the matrix 
                self.QHXProc.val = None
                self.QHXProc.sqerr = INFINITE

        else:
            print "CheckUPH: WARNING - don't have input data for this test case no. ",TESTCASE

        if DEBUG in ["ALL"]:
            self.showAllUPH()

    def showAllUPH(self):
        print "====================="

        self.UPH.show()
        self.UPH1.show()
        self.UPH2.show()
        self.UPHm.show()
        self.UPHm1.show()
        self.UPHs.show()
        self.UPHs1.show()
        self.UPHsdot.show()
        self.UPHsdot1.show()
        self.UPHProc.show()
        self.UPHProc1.show()
        self.QHXProc.show()
        self.QHXProc1.show()
        self.UPHc.show()
        self.UPHc1.show()
        self.UPHcdot.show()
        self.UPHcdot1.show()
        self.UPHcdot2.show()
        self.UPHcdotGross.show()
        self.UPHcdotGross1.show()#For convention UPH and UPHc are net!
        self.UPHcGross.show()
        self.QHXProcInt.show()
        self.DTUPHcGross.show()
        self.QOpProc.show()
        self.QOpProc1.show()
        self.VolProcMed.show()
        self.HPerYearProc.show()
        self.HPerYearProc1.show()
        self.HPerDayProc.show()
        self.NDaysProc.show()
        self.VInFlowDay.show()
        self.VInFlowDay1.show()
        self.VInFlowDay2.show()
        self.VOutFlow.show()
        self.VOutFlow1.show()
        self.PTInFlow.show()
        self.PTInFlow1.show()
        self.PT.show()
        self.PT1.show()
        self.PT2.show()
        self.PT3.show()
        self.PTInFlowRec.show()
        self.PTInFlowRec1.show()
        self.PTOutFlow.show()
        self.PTStartUp.show()
        self.PTOutFlowRec.show()
        self.NBatch.show()
        self.UAProc.show()
        self.QEvapProc.show()
        self.TEnvProc.show()  
        self.DTLoss1.show()
        self.DTLoss.show()
        self.QLoss.show()
        self.QLoss1.show()
        self.DTUPHcGross1.show()
        self.DTUPHcGross.show()
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
        self.DTUPHs1.show()
        self.DTUPHs.show()
        

        print "====================="
#-----------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------

########## Change of priority for parameters not needed

        if iszero(self.VInFlowDay):
            self.PTInFlow.priority = 99
            self.PTInFlowrec.priority = 99
        if iszero(self.VOutFlow):
            self.PTOutFlow.priority = 99
            self.PTOutFlowRec.priority = 99
        if iszero(self.VolProcMed):
            self.PTStartUp.priority = 99
        if iszero(self.QOpProc):
            self.TEnvProc.priority = 99
            self.UAProc.priority = 99
#................................................................................
        self.UPH.screen()
        self.UPHc.screen()
        self.UPHm.screen()
        self.UPHs.screen()
        self.UPHw.screen()

        self.UPHProc.screen()
        self.QHXProc.screen()

        self.UPHcGross.screen()
        self.QHXProcInt.screen()

        self.PT.screen()
        self.PTInFlow.screen()
        self.PTOutFlow.screen()
        self.PTInFlowRec.screen()
        self.PTOutFlowRec.screen() #do not exist yet
        self.PTStartUp.screen()

        self.VInFlowDay.screen()
        self.VOutFlow.screen()
        self.VolProcMed.screen()

        self.HPerYearProc.screen()
        self.NDaysProc.screen()
        self.HPerDayProc.screen()
        self.NBatch.screen()

        self.TEnvProc.screen()
        self.QOpProc.screen()
        self.UAProc.screen()
        self.QEvapProc.screen()
        
#------------------------------------------------------------------------------
    def definePriority(self,mainProcess):
#------------------------------------------------------------------------------
#   changes the priority in function of the importance of the process
#------------------------------------------------------------------------------

        if mainProcess == True:
            
            self.UPH.priority = 1
            self.UPHProc.priority = 1
            self.UPHs.priority = 1
            self.UPHc.priority = 1
            self.UPHm.priority = 1 
            self.UPHw.priority = 1 
            self.PT.priority = 1
            self.QOpProc.priority = 1

            if self.PTInFlow.priority < 99: self.PTInFlow.priority = 1
            if self.PTInFlowRec.priority < 99: self.PTInFlowRec.priority = 1
            if self.PTStartUp.priority < 99: self.PTStartUp.priority = 1

########## here some verifications are redundant but they do not affect the results
            
            if self.PTOutFlow.priority < 99: self.PTOutFlow.priority = 2
            if self.PTOutFlowRec.priority < 99: self.PTOutFlowRec.priority = 2
            if self.VInFlowDay.priority < 99: self.VInFlowDay.priority = 2
            if self.VOutFlow.priority < 99: self.VOutFlow.priority = 2
            if self.VolProcMed.priority < 99: self.VolProcMed.priority = 2
            if self.TEnvProc.priority < 99: self.TEnvProc.priority = 2
            if self.UAProc.priority < 99: self.UAProc.priority = 2
            if self.QEvapProc.priority < 99: self.QEvapProc.priority = 2
            if self.QHXProc.priority < 99: self.QHXProc.priority = 2
            if self.HPerYearProc.priority < 99: self.HPerYearProc.priority = 2

            if self.NBatch.priority < 99: self.NBatch.priority = 3
            if self.NDaysProc.priority < 99: self.NDaysProc.priority = 3
            if self.HPerDayProc.priority < 99: self.HPerDayProc.priority = 3
            if self.UPHcGross.priority < 99: self.UPHcGross.priority = 3
            if self.QHXProcInt.priority < 99: self.QHXProcInt.priority = 3
        
#### sense of the if: -> if the value is not needed, because massflow = 0, then priority should remain 99 = not needed

        else:
            
            self.UPH.priority = 2
            self.UPHProc.priority = 2
            self.UPHs.priority = 2
            self.UPHc.priority = 2
            self.UPHm.priority = 2 
            self.UPHw.priority = 2 
            self.PT.priority = 2
            self.QOpProc.priority = 2

            if self.PTInFlow.priority < 99: self.PTInFlow.priority = 2
            if self.PTInFlowRec.priority < 99: self.PTInFlowRec.priority = 2
            if self.PTStartUp.priority < 99: self.PTStartUp.priority = 2

########## here some verifications are redundant but they do not affect the results
            
            if self.PTOutFlow.priority < 99: self.PTOutFlow.priority = 3
            if self.PTOutFlowRec.priority < 99: self.PTOutFlowRec.priority = 3
            if self.VInFlowDay.priority < 99: self.VInFlowDay.priority = 3
            if self.VOutFlow.priority < 99: self.VOutFlow.priority = 3
            if self.VolProcMed.priority < 99: self.VolProcMed.priority = 3
            if self.TEnvProc.priority < 99: self.TEnvProc.priority = 3
            if self.UAProc.priority < 99: self.UAProc.priority = 3
            if self.QEvapProc.priority < 99: self.QEvapProc.priority = 3
            if self.QHXProc.priority < 99: self.QHXProc.priority = 3
            if self.HPerYearProc.priority < 99: self.HPerYearProc.priority = 3
            if self.NBatch.priority < 99: self.NBatch.priority = 3
            if self.NDaysProc.priority < 99: self.NDaysProc.priority = 3
            if self.HPerDayProc.priority < 99: self.HPerDayProc.priority = 3
            if self.UPHcGross.priority < 99: self.UPHcGross.priority = 3
            if self.QHXProcInt.priority < 99: self.QHXProcInt.priority = 3

          
#------------------------------------------------------------------------------
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

            if DEBUG in ["ALL","MAIN"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

            if DEBUG in ["ALL","MAIN"]:
                print "-------------------------------------------------"
                print "Step 1: calculating from left to right (CALC)"
                print "-------------------------------------------------"
                
            self.HPerYearProc1 = calcProd("HPerYearProc1",self.NDaysProc,self.HPerDayProc)
            self.DTLoss1 = calcDiff("DTLoss1",self.PT,self.TEnvProc)
            self.QLoss1 = calcProd("QLoss1",self.UAProc,self.DTLoss)
            # UA: add suggestion how to calculate
            self.QOpProc1 = calcSum("QOpProc1",self.QLoss,self.QEvapProc)
            self.UPHm1 = calcProd("UPHm1",self.QOpProc,self.HPerDayProc)
            self.UPHcdotGross1 = calcFlow("UPHcdotGross1",self.FluidCp,self.VInFlowDay,self.PT1,self.PTInFlow,self.DTUPHcGross,self.DTUPHcGross1)
            self.QHXdotProcInt1 = calcFlow("QHXdotProcInt1",self.FluidCp,self.VOutFlow,self.PTOutFlowRec,self.PTOutFlow,self.DTQHXOut,self.DTQHXOut1)
            self.QHXdotProcInt2 = calcFlow("QHXdotProcInt2",self.FluidCp,self.VInFlowDay2,self.PTInFlowRec,self.PTInFlow1,self.DTQHXIn,self.DTQHXIn1)
            self.UPHcdot1 = calcDiff("UPHcdot1",self.UPHcdotGross,self.QHXdotProcInt)
            self.UPHcdot2 = calcFlow("UPHcdot2",self.FluidCp,self.VInFlowDay1,self.PT2,self.PTInFlowRec1,self.DTUPHcNet,self.DTUPHcNet1)
            self.UPHc1 = calcProd("UPHc1",self.UPHcdot,self.NDaysProc)
            self.UPHsdot1 = calcFlow("UPHsdot1",(self.FluidCp*self.FluidDensity),self.VolProcMed,self.PT3,self.PTStartUp,self.DTUPHs,self.DTUPHs1)
            self.NBatchPerYear1 =calcProd("NbatchPeryear1",self.NDaysProc,self.NBatch)
            self.UPHs1 = calcProd("UPHs1",self.UPHsdot,self.NBatchPerYear)
            self.UPH1 = calcSum3("UPH1",self.UPHm,self.UPHc,self.UPHs)
            self.UPH2 = calcSum("UPH2",self.UPHProc,self.QHXProc)
            self.DTCrossHXLT1 = calcDiff("DTCrossHXLT",self.PTOutFlow,self.PTInFlow)
            self.DTCrossHXHT1 = calcDiff("DTCrossHXHT",self.PTOutFlowRec,self.PTInFlowRec)

            self.UPHw_dot1 = calcFlow("UPHw_dot1",self.FluidCp,self.VOutFlow,self.PTOutFlow,self.PTFinal,self.DTOutFlow,self.DTOutFlow1)
            self.UPHw1 = calcProd("UPHw1",self.UPHw_dot,self.NBatchPerYear)
                        
            if DEBUG in ["ALL","MAIN"]:
                self.showAllUPH()

# Step 2: Cross check the variables

                print "-------------------------------------------------"
                print "Step 2: cross checking"
                print "-------------------------------------------------"
                
            self.ccheckAll()            

            if DEBUG in ["ALL","MAIN"]:
                self.showAllUPH()

# Step 3: Adjust the variables (inverse of calculation routines)
                print "-------------------------------------------------"
                print "Step 3: calculating from right to left (ADJUST)"
                print "-------------------------------------------------"
                
            adjustFlow(self.UPHw_dot1,self.FluidCp,self.VOutFlow2,self.PTOutFlow3,self.PTFinal,self.DTOutFlow,self.DTOutFlow1)
            adjustProd(self.UPHw1,self.UPHw_dot,self.NBatchPerYear)

            adjustDiff(self.DTCrossHXHT,self.PTOutFlowRec,self.PTInFlowRec)
            adjustDiff(self.DTCrossHXLT,self.PTOutFlow2,self.PTInFlow2)
            adjustSum(self.UPH2,self.UPHProc,self.QHXProc)
            adjustSum3(self.UPH1,self.UPHm,self.UPHc,self.UPHs)
            adjustProd(self.UPHs1,self.UPHsdot1,self.NBatchPerYear)
            adjustProd(self.NBatchPerYear1,self.NDaysProc,self.NBatch)
            adjustFlow(self.UPHsdot1,(self.FluidCp*self.FluidDensity),self.VolProcMed,self.PT3,self.PTStartUp,self.DTUPHs,self.DTUPHs1)
            adjustProd(self.UPHc1,self.UPHcdot,self.NDaysProc)
            adjustFlow(self.UPHcdot2,self.FluidCp,self.VInFlowDay1,self.PT2,self.PTInFlowRec1,self.DTUPHcNet,self.DTUPHcNet1)
            adjustDiff(self.UPHcdot1,self.UPHcdotGross,self.QHXdotProcInt)
            adjustFlow(self.QHXdotProcInt2,self.FluidCp,self.VInFlowDay2,self.PTInFlowRec2,self.PTInFlow1,self.DTQHXIn,self.DTQHXIn1)
            adjustFlow(self.QHXdotProcInt1,self.FluidCp,self.VOutFlow,self.PTOutFlowRec1,self.PTOutFlow,self.DTQHXOut,self.DTQHXOut1)
            adjustFlow(self.UPHcdotGross1,self.FluidCp,self.VInFlowDay,self.PT1,self.PTInFlow,self.DTUPHcGross,self.DTUPHcGross1)
            adjustProd(self.UPHm1,self.QOpProc,self.HPerDayProc)
            adjustSum(self.QOpProc1,self.QLoss,self.QEvapProc)
            adjustProd(self.QLoss1,self.UAProc,self.DTLoss)
            adjustDiff(self.DTLoss1,self.PT,self.TEnvProc)
            adjustProd(self.HPerYearProc1,self.NDaysProc,self.HPerDayProc)
            

            if DEBUG in ["ALL","MAIN"]:
                self.showAllUPH()
           
# Step 4: Second cross check of the variables

                print "-------------------------------------------------"
                print "Step 4: cross checking"
                print "-------------------------------------------------"
                
            self.ccheckAll()
            
            if DEBUG in ["ALL","MAIN"]:
                self.showAllUPH()

# Arrived at the end

        self.UPHcGross = calcProd("UPHcGross",self.UPHcdotGross,self.NDaysProc)# Not adjusted
        self.QHXProcInt = calcProd("QHXProcInt",self.QHXdotProcInt,self.NDaysProc) # Not adjusted 

    #añadido este último show all. sino no se ven los ultimos dos resultados ...
        if DEBUG in ["ALL","BASIC"]:
            self.showAllUPH()
#------------------------------------------------------------------------------
    def ccheckAll(self):    
#------------------------------------------------------------------------------
#   check block
#------------------------------------------------------------------------------

        ccheck4(self.PT,self.PT1,self.PT2,self.PT3,self.PT4)  
        ccheck2(self.PTInFlow,self.PTInFlow1,self.PTInFlow2)
        ccheck3(self.PTInFlowRec,self.PTInFlowRec1,self.PTInFlowRec2,self.PTInFlowRec3)
        ccheck2(self.VInFlowDay,self.VInFlowDay1,self.VInFlowDay2)
        ccheck1(self.VOutFlow,self.VOutFlow1)
        ccheck2(self.PTOutFlow,self.PTOutFlow1,self.PTOutFlow2)
        ccheck2(self.PTOutFlowRec,self.PTOutFlowRec1,self.PTOutFlowRec2)
        ccheck1(self.DTCrossHXLT,self.DTCrossHXLT1)
        ccheck1(self.DTCrossHXHT,self.DTCrossHXHT1)
        
        ccheck1(self.HPerYearProc,self.HPerYearProc1)
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
        ccheck1(self.UPHProc,self.UPHProc1)
        ccheck1(self.QHXProc,self.QHXProc1)
        ccheck2(self.UPH,self.UPH1,self.UPH2)

        ccheck1(self.UPHw,self.UPHw1)
        ccheck1(self.UPHw_dot,self.UPHw_dot1)
        ccheck1(self.DTOutFlow,self.DTOutFlow1)
        ccheck1(self.PTFinal,self.PTFinal1)


#------------------------------------------------------------------------------
    def estimate(self):  
#------------------------------------------------------------------------------
#   estimates some of the data that are not sufficiently precise
#   should be a subset of the data that are within screen
#   (not necessarily ALL data have to be estimated)
#------------------------------------------------------------------------------

        self.PTOutFlowRec.setEstimate(self.PT,limits=(self.PT.valMin,self.PT.valMax))
        self.VOutFlow.setEstimate(self.VInFlowDay,limits=(self.VInFlowDay.valMin,self.VInFlowDay.valMax))
        self.PTInFlow.setEstimate(15.0,limits = (5.0,35.0))
        self.DTCrossHXHT.setEstimate(10.0,limits = (5.0,20.0))
        self.DTCrossHXLT.setEstimate(10.0,limits = (5.0,20.0))
        
# limits: optional and fix absolute minimum and maximum values
# sqerr: optional input that fixes the (stochastic) relative square error

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
    
    ccProc = CheckProc(1)       # creates an instance of class CCheck
    ccProc.check()
    ccProc.exportData(1)

    ccProc.screen()
    screen.show()
    
#==============================================================================
