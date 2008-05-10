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
        self.PTInFlow1 = CCPar("PTInFlow1")
        self.PTInFlowRec1 = CCPar("PTInFlowRec1")
        self.PTOutFlow1 = CCPar("PTInFlow1")
        self.HperYearProc1 = CCPar("HperYearProc1")
        self.HperYearProc = CCPar("HperYearProc",priority=2)
        self.DTLoss1=CCPar("DTLoss1")
        self.DTLoss=CCPar("DTLoss")
        self.VInFlowDay1 = CCPar("VInFlowDay1") 
        self.VInFlowDay2 = CCPar("VInFlowDay2") 
        self.VOutFlow1 = CCPar("VOutFlow1")
        self.QLoss = CCPar("QLoss")
        self.QLoss1 = CCPar("QLoss1")
        self.QOpProc1 = CCPar("QOpProc1")
        self.UPHm1 = CCPar("UPHm1")
        self.UPHm = CCPar("UPHm",priority=2)
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
        self.UPHc = CCPar("UPHc",priority=2)
        self.DTUPHs1 = CCPar("DTUPHs1")
        self.DTUPHs = CCPar("DTUPHs")
        self.UPHsdot1 = CCPar("UPHsdot1")
        self.UPHsdot = CCPar("UPHsdot")
        self.UPHs1 = CCPar("UPHs1")
        self.UPHs = CCPar("UPHs")
        self.UPH1 = CCPar("UPH1")
        self.UPH2 = CCPar("UPH2")
        self.UPH = CCPar("UPH",priority=2)
        self.UPHProc1 = CCPar("UPHProc1")
        self.QHXProc1 = CCPar("QHXProc1")
        self.UAProc = CCPar("UAProc")
        self.QEvapProc = CCPar("UAProc")
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

        self.FluidCp = 0.001 # kWh/K*Kg # IMPORT Constant from the FluidDB
        self.FluidDensity = 1030 # Kg/m3 # IMPORT Constant from the FluidDB

        self.PTInFlow = CCPar("PTInFlow")
        self.PT = CCPar("PT",priority=2)
        self.PTOutFlow = CCPar("PTOutFlow")# assumed to be Tpor
        self.PTOutFlowRec = CCPar("PTOutFlowRec") # It is not defined in the questionnaire. it has to be estimated
        self.PTInFlowRec = CCPar("PTInFlowRec")
        self.PTStartUp = CCPar("PTStartUp")
        self.VInFlowDay = CCPar("VInFlowDay ")
        self.VOutFlow = CCPar("VOutFlow")
        self.VolProcMed = CCPar("VolProcMed")
        self.NDaysProc = CCPar("NDaysProc")
        self.HPerDayProc = CCPar("HPerDay")
        self.NBatch = CCPar("NBatch")
        self.TEnvProc = CCPar("TEnvProc")
        self.QOpProc = CCPar("QOpProc")
        self.UPHProc = CCPar("UPHProc")

        self.QHXProc = CCPar("QHXProc")# It comes from the matrix (and from calculation from questionnaire??)
        
        
#..............................................................................
# reading data from table "qprocessdata"
        try:
            qprocessdataTable = Status.DB.qprocessdata.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].ProcNo[self.ProcNo]
            
            if len(qprocessdataTable) > 0:
                qprocessdata = qprocessdataTable[0]


                self.PTInFlow.setValue(qprocessdata.PTInFlow)
                self.PT.setValue(qprocessdata.PT)
                self.PTOutFlow.setValue(qprocessdata.PTOutFlow)
#                self.PTOutFlowRec.setValue(qprocessdata.PTOutFlowRec)  #does not exist yet
                self.PTInFlowRec.setValue(qprocessdata.PTInFlowRec) 
                self.PTStartUp.setValue(qprocessdata.PTStartUp)
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
                qprocessdata.VInFlowDay = self.VInFlowDay.val
                qprocessdata.VolProcMed = self.VolProcMed.val
                qprocessdata.NDaysProc = self.NDaysProc.val
                qprocessdata.HPerDayProc = self.HPerDayProc.val
                qprocessdata.NBatch = self.NBatch.val
                qprocessdata.TEnvProc = self.TEnvProc.val
                qprocessdata.QOpProc = self.QOpProc.val
                qprocessdata.UPHProc = self.UPHProc.val
#                qprocessdata.HperYearProc = self.HperYearProc.val
                qprocessdata.UAProc = self.UAProc.val
                qprocessdata.QEvapProc = self.QEvapProc.val
                qprocessdata.UPHcGross = self.UPHcGross.val
                qprocessdata.QHXProcInt = self.QHXProcInt.val
                qprocessdata.UPHm = self.UPHm.val
                qprocessdata.UPHs = self.UPHs.val
                qprocessdata.UPHc = self.UPHc.val
                qprocessdata.UPH = self.UPH.val


        # QLoss, UPHcdotGross, UPHcdot, QHXdotProcInt, NBatchPerYear, UPHsdot not into the qprocessdat DB and not exported yet 
         
                                       

                Status.SQL.commit()
                
#        except:
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

            self.HperYearProc = CCPar("HperYearProc")
            self.HperYearProc.val = None
            self.HperYearProc.sqerr = INFINITE  

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

                self.HperYearProc = CCPar("HperYearProc")
                self.HperYearProc.val = None
                self.HperYearProc.sqerr = INFINITE  

                
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

                self.HperYearProc = CCPar("HperYearProc")
                self.HperYearProc.val = None
                self.HperYearProc.sqerr = INFINITE  

                
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

                self.HperYearProc = CCPar("HperYearProc")
                self.HperYearProc.val = None
                self.HperYearProc.sqerr = INFINITE  

                
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
        self.HperYearProc.show()
        self.HperYearProc1.show()
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

        self.PTInFlow.screen()
        self.PT.screen()
        self.PTOutFlow.screen()
        self.PTOutFlowRec.screen() #do not exist yet
        self.PTInFlowRec.screen()
        self.PTStartUp.screen()
        self.VInFlowDay.screen()
        self.VolProcMed.screen()
        self.NDaysProc.screen()
        self.HPerDayProc.screen()
        self.NBatch.screen()
        self.TEnvProc.screen()
        self.QOpProc.screen()
        self.UPHProc.screen()
        self.HperYearProc.screen()
        self.UAProc.screen()
        self.QEvapProc.screen()
        self.UPHcGross.screen()
        self.QHXProcInt.screen()
        self.UPHm.screen()
        self.UPHs.screen()
        self.UPHc.screen()
        self.UPH.screen()
    
#------------------------------------------------------------------------------
    def check(self):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   main function carrying out the check of the block
#------------------------------------------------------------------------------

        if DEBUG in ["ALL"]:
            print "-------------------------------------------------"
            print " Process checking"
            print "-------------------------------------------------"

        for n in range(5):

            if DEBUG in ["ALL","MAIN"]:
                print "-------------------------------------------------"
                print "Ciclo %s"%n
                print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

            if DEBUG in ["ALL","MAIN"]:
                print "-------------------------------------------------"
                print "Step 1: calculating from left to right (CALC)"
                print "-------------------------------------------------"
                
            self.HperYearProc1 = calcProd("HperYearProc1",self.NDaysProc,self.HPerDayProc)
            self.DTLoss1 = calcDiff("DTLoss1",self.PT,self.TEnvProc)
            self.QLoss1 = calcProd("QLoss1",self.UAProc,self.DTLoss)
            # UA: add suggestion how to calculate
            self.QOpProc1 = calcSum("QOpProc1",self.QLoss,self.QEvapProc)
            self.UPHm1 = calcProd("UPHm1",self.QOpProc,self.HPerDayProc)
            self.UPHcdotGross1 = calcFlow("UPHcdotGross1",self.FluidCp,self.VInFlowDay,self.PT1,self.PTInFlow,self.DTUPHcGross,self.DTUPHcGross1)
            self.QHXdotProcInt1 = calcFlow("QHXdotProcInt1",self.FluidCp,self.VOutFlow,self.PTOutFlowRec,self.PTOutFlow,self.DTQHX,self.DTQHX1)
            self.QHXdotProcInt2 = calcFlow("QHXdotProcInt2",self.FluidCp,self.VInFlowDay2,self.PTInFlowRec,self.PTInFlow1,self.DTQHX,self.DTQHX2)
            self.UPHcdot1 = calcDiff("UPHcdot1",self.UPHcdotGross,self.QHXdotProcInt)
            self.UPHcdot2 = calcFlow("UPHcdot2",self.FluidCp,self.VInFlowDay1,self.PT2,self.PTInFlowRec1,self.DTUPHcNet,self.DTUPHcNet1)
            self.UPHc1 = calcProd("UPHc1",self.UPHcdot,self.NDaysProc)
            self.UPHsdot1 = calcFlow("UPHsdot1",(self.FluidCp*self.FluidDensity),self.VolProcMed,self.PT3,self.PTStartUp,self.DTUPHs,self.DTUPHs1)
            self.NBatchPerYear1 =calcProd("NbatchPeryear1",self.NDaysProc,self.NBatch)
            self.UPHs1 = calcProd("UPHs1",self.UPHsdot,self.NBatchPerYear)
            self.UPH1 = calcSum3("UPH1",self.UPHm,self.UPHc,self.UPHs)
            self.UPH2 = calcSum("UPH2",self.UPHProc,self.QHXProc)

          
            if DEBUG in ["ALL","MAIN"]:
                self.showAllUPH()

# Step 2: Cross check the variables

                print "-------------------------------------------------"
                print "Step 2: cross checking"
                print "-------------------------------------------------"
                
            ccheck3(self.PT,self.PT1,self.PT2,self.PT3)
            ccheck1(self.PTInFlow,self.PTInFlow1)
            ccheck1(self.PTInFlowRec,self.PTInFlowRec1)
            ccheck2(self.VInFlowDay,self.VInFlowDay1,self.VInFlowDay2)
            ccheck1(self.VOutFlow,self.VOutFlow1)
            ccheck1(self.PTOutFlow,self.PTOutFlow1)
            
            ccheck1(self.HperYearProc,self.HperYearProc1)
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
            ccheck1(self.PTOutFlow,self.PTOutFlow1)
            

            if DEBUG in ["ALL","MAIN"]:
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
            adjustFlow(self.UPHcdot2,self.FluidCp,self.VInFlowDay1,self.PT2,self.PTInFlowRec,self.DTUPHcNet,self.DTUPHcNet1)
            adjustDiff(self.UPHcdot1,self.UPHcdotGross,self.QHXdotProcInt)
            adjustFlow(self.QHXdotProcInt2,self.FluidCp,self.VInFlowDay2,self.PTInFlowRec,self.PTInFlow1,self.DTQHX,self.DTQHX2)
            adjustFlow(self.QHXdotProcInt1,self.FluidCp,self.VOutFlow,self.PTOutFlowRec,self.PTOutFlow,self.DTQHX,self.DTQHX1)
            adjustFlow(self.UPHcdotGross1,self.FluidCp,self.VInFlowDay,self.PT1,self.PTInFlow,self.DTUPHcGross,self.DTUPHcGross1)
            adjustProd(self.UPHm1,self.QOpProc,self.HPerDayProc)
            adjustSum(self.QOpProc1,self.QLoss,self.QEvapProc)
            adjustProd(self.QLoss1,self.UAProc,self.DTLoss)
            adjustDiff(self.DTLoss1,self.PT,self.TEnvProc)
            adjustProd(self.HperYearProc1,self.NDaysProc,self.HPerDayProc)
            
            if DEBUG in ["ALL","MAIN"]:
                self.showAllUPH()
           
# Step 4: Second cross check of the variables

                print "-------------------------------------------------"
                print "Step 4: cross checking"
                print "-------------------------------------------------"
                
            ccheck3(self.PT,self.PT1,self.PT2,self.PT3)  
            ccheck1(self.PTInFlow,self.PTInFlow1)
            ccheck1(self.PTInFlowRec,self.PTInFlowRec1)
            ccheck2(self.VInFlowDay,self.VInFlowDay1,self.VInFlowDay2)
            ccheck1(self.VOutFlow,self.VOutFlow1)
            ccheck1(self.PTOutFlow,self.PTOutFlow1)
            
            ccheck1(self.HperYearProc,self.HperYearProc1)
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

            if DEBUG in ["ALL","MAIN"]:
                self.showAllUPH()

# Arrived at the end

        self.UPHcGross = calcProd("UPHcGross",self.UPHcdotGross,self.NDaysProc)# Not adjusted
        self.QHXProcInt = calcProd("QHXProcInt",self.QHXdotProcInt,self.NDaysProc) # Not adjusted 

    #añadido este último show all. sino no se ven los ultimos dos resultados ...
        if DEBUG in ["ALL","BASIC"]:
            self.showAllUPH()


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
