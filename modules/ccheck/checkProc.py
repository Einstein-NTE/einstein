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
#                       Hans Schweiger  20/07/2009
#               
#   06/04/2009  HS  Clean-up: elimination of prints
#   20/07/2009  HS  Bug-fix: fluid properties in outgoing medium
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

#libraries necessary for SQL access:
from einstein.GUI.status import *
import einstein.GUI.pSQL as pSQL, MySQLdb

#------------------------------------------------------------------------------
class CheckProc():
#------------------------------------------------------------------------------
#   Carries out consistency checking for process k
#------------------------------------------------------------------------------

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
        self.PTStartUp1 = CCPar("PTStartUp1")
        self.PTOutFlow1 = CCPar("PTOutFlow1")
        self.PTOutFlow2 = CCPar("PTOutFlow2")
        self.PTOutFlow3 = CCPar("PTOutFlow3")
        self.PTOutFlowRec = CCPar("PTOutFlowRec",parType="T")
        self.PTOutFlowRec1 = CCPar("PTOUtFlowRec1")
        self.PTOutFlowRec2 = CCPar("PTOUtFlowRec2")
        self.PTOutFlowRec3 = CCPar("PTOUtFlowRec3")
        self.PTFinal = CCPar("PTFinal",parType = "T")
        self.PTFinal1 = CCPar("PTFinal1")
        self.PTFinal2 = CCPar("PTFinal2")

        self.hOutFlow1 = CCPar("hOutFlow1")
        self.hOutFlow2 = CCPar("hOutFlow2")
        self.hOutFlowRec = CCPar("hOutFlowRec")
        self.hOutFlowRec1 = CCPar("hOutFlowRec1")
        self.hFinal = CCPar("hFinal")
        self.hFinal1 = CCPar("hFinal1")
        self.dhOutFlow = CCPar("dhOutFlow")
        self.dhOutFlow1 = CCPar("dhOutFlow1")
        self.dhFinal = CCPar("dhFinal")
        self.dhFinal1 = CCPar("dhFinal1")

        self.xOutFlow = CCPar("xOutFlow",parType = "X")
        self.xOutFlow1 = CCPar("xOutFlow1",parType = "X")
        self.xOutFlowRec = CCPar("xOutFlowRec",parType = "X")
        self.xOutFlowRec1 = CCPar("xOutFlowRec1",parType = "X")
        self.xFinal = CCPar("xFinal",parType = "X")
        self.xFinal1 = CCPar("xFinal1",parType = "X")

        
        self.HPerYearProc1 = CCPar("HPerYearProc1")
        self.HPerYearProc = CCPar("HPerYearProc",priority=2)
        self.HPerYearProc.valMax = 8760
        self.DTLoss1=CCPar("DTLoss1")
        self.DTLoss=CCPar("DTLoss")
        self.VInFlowDay1 = CCPar("VInFlowDay1") 
        self.VInFlowDay2 = CCPar("VInFlowDay2") 
        self.VInFlowDay3 = CCPar("VInFlowDay3") 
        self.VOutFlow1 = CCPar("VOutFlow1")
        self.VOutFlow2 = CCPar("VOutFlow2")
        self.VolProcMed1 = CCPar("VolProcMed1")
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
        self.NDaysProc1 = CCPar("NDaysProc1")
        self.NDaysProc2 = CCPar("NDaysProc2")
        self.NDaysProc3 = CCPar("NDaysProc3")
        self.NDaysProc4 = CCPar("NDaysProc4")
        self.NBatchPerYear1 = CCPar("NBatchPerYear1")
        self.NBatchPerYear2 = CCPar("NBatchPerYear2")
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
        self.UPHw = CCPar("UPHw")# It is the waste heat of the outflow. In general it is QWHProc but if we have a vessel it does not
        self.UPHw1 = CCPar("UPHw1")
        self.UPHw_dot = CCPar("UPHw_dot")
        self.UPHw_dot1 = CCPar("UPHw_dot1")
        self.UPHProc = CCPar("UPHProc") 
        self.UPHProc1 = CCPar("UPHProc1")
        self.QHXProc1 = CCPar("QHXProc1")
        self.UAProc = CCPar("UAProc")
        self.UAProc1 = CCPar("UAProc1")
        self.QEvapProc = CCPar("QEvapProc")
        self.QEvapProc1 = CCPar("QEvapProc1")
        self.UPHcGross = CCPar("UPHcGross")
        self.QHXProcInt = CCPar("QHXProcInt")
        self.QHXProc = CCPar("QHXProc")# It comes from the matrix
        self.QWHProc = CCPar("QWHProc")# It comes from the matrix. In theory it is the sum UPHw and UPHmass (not existing yet)

        self.importData(k)

        if DEBUG in ["ALL","BASIC","MAIN"]:
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
        self.PTOutFlow = CCPar("PTOutFlow", parType="T")
        self.PTInFlowRec = CCPar("PTInFlowRec",parType="T")
        self.PTStartUp = CCPar("PTStartUp",parType="T")
        self.VInFlowDay = CCPar("VInFlowDay ")
        self.VOutFlow = CCPar("VOutFlow")
        self.hOutFlow = CCPar("hOutFlow")
        self.VolProcMed = CCPar("VolProcMed")
        self.NDaysProc = CCPar("NDaysProc")
        self.NDaysProc.valMax = 365
        self.HPerDayProc = CCPar("HPerDay")
        self.HPerDayProc.valMax = 24
        self.NBatch = CCPar("NBatch")
        self.TEnvProc = CCPar("TEnvProc",parType="T")# Now cannot be entered by questionnaire
        self.QOpProc = CCPar("QOpProc")
        self.UPH = CCPar("UPH") # Useful process heat asked into the questionnaire is UPH not UPHproc
        
        
#..............................................................................
# reading data from table "qprocessdata"
        qprocessdataTable = Status.DB.qprocessdata.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].ProcNo[self.ProcNo]
        
#        print "CheckProc (importData): lengh %s ProcNo = %s"%(len(qprocessdataTable),self.ProcNo)
        if len(qprocessdataTable) > 0:
            qprocessdata = qprocessdataTable[0]

            fluid_number = qprocessdata.ProcMedDBFluid_id   #IMPORT from the FluidDB
            proc_fluid = Fluid(fluid_number)

#            print proc_fluid
            
            self.FluidCp = proc_fluid.cp
            self.FluidDensity = proc_fluid.rho
            self.FluidRhoCp = self.FluidCp * self.FluidDensity

            self.PTInFlow.setValue(qprocessdata.PTInFlow)
            self.PT.setValue(qprocessdata.PT,err=0.0)   #if specified, take as fixed
            self.PTOutFlow.setValue(qprocessdata.PTOutFlow)

# if no temperature or enthalpy for Outflow is specified, start with PT as initial estimate
# but leave error range from 0 to infinite !!!!

            if qprocessdata.PTOutFlow is None and qprocessdata.HOutFlow is None:
                self.PTOutFlow.val = self.PT.val
                self.PTOutFlowRec.val = self.PT.val
                
            self.hOutFlow.setValue(qprocessdata.HOutFlow)
                
            self.PTInFlowRec.setValue(qprocessdata.PTInFlowRec) 
            self.PTStartUp.setValue(qprocessdata.PTStartUp)
            self.VInFlowDay.setValue(qprocessdata.VInFlowDay) 
            self.VOutFlow.setValue(qprocessdata.VOutFlow) 
            self.VolProcMed.setValue(qprocessdata.VolProcMed) 
            self.NDaysProc.setValue(qprocessdata.NDaysProc,err=0.0) #number -> exact value
            self.HPerDayProc.setValue(qprocessdata.HPerDayProc)

#if 24.0 hours are specified, suppose that this value is exact.
            if self.HPerDayProc.val > 23.99:
                self.HPerDayProc.setValue(24.0,err=0.0)
                
            if qprocessdata.NBatch is None:
                self.NBatch.setValue(1.0,err=0.0)   # if no number is specified, suppose 1 !!!
            else:
                self.NBatch.setValue(qprocessdata.NBatch,err=0.0) #number -> exact value

            if (qprocessdata.HeatRecOK == "yes"):
                self.HeatRecOK = True
                if qprocessdata.PTFinal is None:
                    logMessage(_("No limit specified for cooling of outgoing streams. 0 ºC is assumed"))
                    self.self.PTFinal.setValue(0.0)
                else:
                    self.PTFinal.setValue(qprocessdata.PTFinal) #reads in PT final only if heat recovery is possible !!!
            elif(qprocessdata.HeatRecOK == "no"):
                self.HeatRecOK = False
            else:
                logWarning(_("Possibility of heat recovery for process no. %s (%s)is not specified.\nYES is assumed.")%\
                            (self.ProcNo,qprocessdata.Process))
                self.HeatRecOK = True
                if qprocessdata.PTFinal is None:
                    logMessage(_("Process No. %s: no final temperature specified for outflowing medium. ")+\
                               _("zero assumed !"))
                    self.self.PTFinal.setValue(0.0)
                else:
                    self.PTFinal.setValue(qprocessdata.PTFinal) #reads in PT final only if heat recovery is possible !!!
                
            if qprocessdata.TEnvProc is None:
                self.TEnvProc.setValue(18.0)
            else:
                self.TEnvProc.setValue(qprocessdata.TEnvProc)
            self.QOpProc.setValue(qprocessdata.QOpProc) 
            self.UPH.setValue(qprocessdata.UPH,err=0.0) #if specified, take exact value 

            if isequal(self.PTInFlow.val,self.PTInFlowRec.val) or \
               (self.PTInFlowRec.val is None) or \
               (self.PT.val < self.PTInFlow.val + 5.0):
                self.internalHR = False
            else:
                self.internalHR = True

            if (self.PTFinal.val is None) and (self.HeatRecOK == True): #should be superfluous now ...
                self.PTFinal.setValue(0.0)  #set to zero if nothing is specified !!!
                if self.VOutFlow.val > 0 or self.VOutFlow.val is None:
                    logMessage(_("Process No. %s: no final temperature specified for outflowing medium. ")+\
                               _("zero assumed !"))

            if self.HeatRecOK == True or self.internalHR == True:   # fluid pars only needed in this case

                fluid_number_w = qprocessdata.ProcMedOut   #IMPORT from the FluidDB
                proc_fluid_w = Fluid(fluid_number_w)

                self.FluidCp_w = proc_fluid_w.cp
                self.FluidDensity_w = proc_fluid_w.rho
                self.FluidRhoCp_w = self.FluidCp_w * self.FluidDensity_w
                self.Fluid_hL_w = proc_fluid_w.hL
                self.FluidTCond_w = proc_fluid_w.TCond

               
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
#                print "exporting data to qprocessdata"
                qprocessdata = qprocessdataTable[0]

        
                qprocessdata.PTInFlow = check(self.PTInFlow.val)
                qprocessdata.PT = check(self.PT.val)
                qprocessdata.PTOutFlow = check(self.PTOutFlow.val)
                qprocessdata.PTOutFlowRec = check(self.PTOutFlowRec.val)
                qprocessdata.HOutFlow = check(self.hOutFlow.val)
                qprocessdata.PTInFlowRec = check(self.PTInFlowRec.val)
                qprocessdata.PTStartUp = check(self.PTStartUp.val)
                qprocessdata.PTFinal = check(self.PTFinal.val)
                qprocessdata.VInFlowDay = check(self.VInFlowDay.val)
                qprocessdata.VolProcMed = check(self.VolProcMed.val)
                qprocessdata.NDaysProc = check(self.NDaysProc.val)
                qprocessdata.HPerDayProc = check(self.HPerDayProc.val)
                qprocessdata.NBatch = check(self.NBatch.val)
                qprocessdata.TEnvProc = check(self.TEnvProc.val)
                qprocessdata.QOpProc = check(self.QOpProc.val)
                qprocessdata.UPHProc = check(self.UPHProc.val)
                qprocessdata.HPerYearProc = check(self.HPerYearProc.val)
                qprocessdata.UAProc = check(self.UAProc.val)
                qprocessdata.QEvapProc = check(self.QEvapProc.val)
                qprocessdata.UPHcGross = check(self.UPHcGross.val)
                qprocessdata.QHXProcInt = check(self.QHXProcInt.val)
                qprocessdata.UPHm = check(self.UPHm.val)
                qprocessdata.UPHs = check(self.UPHs.val)
                qprocessdata.UPHc = check(self.UPHc.val)
                qprocessdata.UPH = check(self.UPH.val)
                qprocessdata.UPHw = check(self.UPHw.val)
                qprocessdata.QWHProc = check(self.QWHProc.val)
                qprocessdata.QHXProc = check(self.QHXProc.val)

                if self.HeatRecOK == True:
                    qprocessdata.HeatRecOK = "yes"
                else:
                    qprocessdata.HeatRecOK = "no"

                Status.SQL.commit()
                
            else:
                print "CheckProc (exportData): error writing data to qprocessdata"
            pass




    def showAllUPH(self):
        print "====================="

        self.UPH.show()
        self.UPH1.show()
        self.UPH2.show()
        self.UPHm.show()
        self.UPHm1.show()
        self.UPHs.show()
        self.UPHw.show()
        self.UPHw1.show()
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
        self.UPHw_dot.show()
        self.UPHw_dot1.show()
        self.QHXProcInt.show()
        self.DTUPHcGross.show()
        self.QOpProc.show()
        self.QOpProc1.show()
        self.VolProcMed.show()
        self.HPerYearProc.show()
        self.HPerYearProc1.show()
        self.HPerDayProc.show()
        self.NDaysProc.show()
        self.NDaysProc1.show()
        self.NDaysProc2.show()
        self.NDaysProc3.show()
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
        self.hOutFlow.show
        self.PTStartUp.show()
        self.PTFinal.show()
        self.hFinal.show()
        self.PTOutFlowRec.show()
        self.hOutFlowRec.show
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
        self.DTQHXIn.show()
        self.DTQHXOut.show()
        self.QHXdotProcInt1.show()
        self.QHXdotProcInt2.show()
        self.QHXdotProcInt.show()
        self.NBatchPerYear1.show()
        self.NBatchPerYear2.show()
        self.NBatchPerYear.show()
        self.DTUPHcNet1.show()
        self.DTUPHcNet.show()
        self.DTUPHs1.show()
        self.DTUPHs.show()
        self.QWHProc.show()
        self.QHXProc.show()
        print "HeatRecOK: ",self.HeatRecOK
        

        print "====================="
#-----------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------

########## Change of priority for parameters not needed

        if iszero(self.VInFlowDay):
            self.PTInFlow.priority = 99
            self.PTInFlowRec.priority = 99
        if iszero(self.VOutFlow) or (self.HeatRecOK == False):
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
        # self.QWHProc.screen() Now it coincides with UPHw

        self.UPHProc.screen()
        self.QHXProc.screen()

        self.UPHcGross.screen()
        self.QHXProcInt.screen()

        self.PT.screen()
        self.PTInFlow.screen()
        self.PTOutFlow.screen()
        self.PTInFlowRec.screen()
        self.PTOutFlowRec.screen() 
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
            if self.QHXProc.priority < 99: self.QHXProc.priority = 2
            #if self.QWHProc.priority < 99: self.QWHProc.priority = 2 Now it coincides with UPHw. Assigned priority 2 coherent with the QHX
            if self.HPerYearProc.priority < 99: self.HPerYearProc.priority = 2
            
            if self.NBatch.priority < 99: self.NBatch.priority = 3
            if self.NDaysProc.priority < 99: self.NDaysProc.priority = 3
            if self.HPerDayProc.priority < 99: self.HPerDayProc.priority = 3
            if self.UPHcGross.priority < 99: self.UPHcGross.priority = 3
            if self.QHXProcInt.priority < 99: self.QHXProcInt.priority = 3
            if self.TEnvProc.priority < 99: self.TEnvProc.priority = 3
            if self.UAProc.priority < 99: self.UAProc.priority = 3
            if self.QEvapProc.priority < 99: self.QEvapProc.priority = 3
            
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
            #if self.QWHProc.priority < 99: self.QWHProc.priority = 3
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

            cycle.initCheckBalance()

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
            self.UPHm1 = calcProd("UPHm1",self.QOpProc,self.HPerYearProc)
            
            self.UPHcdotGross1 = calcFlow("UPHcdotGross1",self.FluidRhoCp,self.VInFlowDay,
                                          self.PT1,self.PTInFlow,
                                          self.DTUPHcGross,self.DTUPHcGross1)
            if self.internalHR == True:
#                self.QHXdotProcInt1 = calcFlow("QHXdotProcInt1",self.FluidRhoCp_w,self.VOutFlow,
#                                               self.PTOutFlowRec,self.PTOutFlow,
#                                               self.DTQHXOut,self.DTQHXOut1)

                self.dhOutFlow1 = calcDiff("dhOutFlow1",self.hOutFlowRec,self.hOutFlow)
                self.QHXdotProcInt1 = calcProdC("QHXdotProcInt1",self.FluidDensity_w, \
                                                self.dhOutFlow,self.VOutFlow)
                self.QHXdotProcInt2 = calcFlow("QHXdotProcInt2",self.FluidRhoCp,self.VInFlowDay2,
                                               self.PTInFlowRec,self.PTInFlow1,
                                               self.DTQHXIn,self.DTQHXIn1)
            else:
                self.QHXdotProcInt1.setValue(0.0)
                self.QHXdotProcInt2.setValue(0.0)
                self.DTQHXOut.setValue(0.0)
                self.DTQHXOut1.setValue(0.0)

                
            self.UPHcdot1 = calcDiff("UPHcdot1",self.UPHcdotGross,self.QHXdotProcInt)
            self.UPHcdot2 = calcFlow("UPHcdot2",self.FluidRhoCp,self.VInFlowDay1,
                                     self.PT2,self.PTInFlowRec1,
                                     self.DTUPHcNet,self.DTUPHcNet1)
            self.UPHc1 = calcProd("UPHc1",self.UPHcdot,self.NDaysProc1)
            
            self.UPHsdot1 = calcFlow("UPHsdot1",self.FluidRhoCp,self.VolProcMed,
                                     self.PT3,self.PTStartUp,
                                     self.DTUPHs,self.DTUPHs1)
            self.NBatchPerYear1 =calcProd("NbatchPeryear1",self.NDaysProc2,self.NBatch)
            self.UPHs1 = calcProd("UPHs1",self.UPHsdot,self.NBatchPerYear2)
            
            self.UPH1 = calcSum3("UPH1",self.UPHm,self.UPHc,self.UPHs)
            self.UPH2 = calcSum("UPH2",self.UPHProc,self.QHXProc)

            if self.internalHR == True:
                self.DTCrossHXLT1 = calcDiff("DTCrossHXLT",self.PTOutFlow,self.PTInFlow)
                self.DTCrossHXHT1 = calcDiff("DTCrossHXHT",self.PTOutFlowRec,self.PTInFlowRec)

            if self.HeatRecOK == True:
#                self.UPHw_dot1 = calcFlow("UPHw_dot1",self.FluidRhoCp_w,self.VOutFlow,
#                                          self.PTOutFlow,self.PTFinal,
#                                          self.DTOutFlow,self.DTOutFlow1)

                self.dhFinal1 = calcDiff("dhFinal1",self.hOutFlow,self.hFinal)
                self.UPHw_dot1 = calcProdC("UPHw_dot1",self.FluidDensity_w, \
                                                self.dhFinal,self.VOutFlow)

                self.hOutFlowRec1 = calcH("hOutFlow1",self.FluidCp_w,
                          self.FluidCp_w,
                          self.Fluid_hL_w,
                          self.FluidTCond_w,
                          self.PTOutFlowRec,self.xOutFlowRec)

                self.hOutFlow1 = calcH("hOutFlow1",self.FluidCp_w,
                          self.FluidCp_w,
                          self.Fluid_hL_w,
                          self.FluidTCond_w,
                          self.PTOutFlow,self.xOutFlow)

                self.hFinal1 = calcH("hFinal1",self.FluidCp_w,
                          self.FluidCp_w,
                          self.Fluid_hL_w,
                          self.FluidTCond_w,
                          self.PTFinal,self.xFinal)


            else:
                self.UPHw_dot1.setValue(0.0)
                
            self.UPHw1 = calcProd("UPHw1",self.UPHw_dot,self.NDaysProc3)
                        
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
                
            if self.HeatRecOK == True:
#                adjustFlow(self.UPHw_dot1,self.FluidRhoCp_w,self.VOutFlow2,
#                           self.PTOutFlow,self.PTFinal,self.DTOutFlow,self.DTOutFlow1)

                adjustH(self.hOutFlowRec1,self.FluidCp_w,
                          self.FluidCp_w,
                          self.Fluid_hL_w,
                          self.FluidTCond_w,
                          self.PTOutFlowRec3,self.xOutFlowRec)

                adjustH(self.hOutFlow1,self.FluidCp_w,
                          self.FluidCp_w,
                          self.Fluid_hL_w,
                          self.FluidTCond_w,
                          self.PTOutFlow3,self.xOutFlow)

                adjustH(self.hFinal1,self.FluidCp_w,
                          self.FluidCp_w,
                          self.Fluid_hL_w,
                          self.FluidTCond_w,
                          self.PTFinal2,self.xFinal)
                
                adjustDiff(self.dhFinal1,self.hOutFlow,self.hFinal)
                adjustProdC(self.UPHw_dot1,self.FluidDensity_w,self.dhFinal,self.VOutFlow2)

            else:
                self.PTFinal.update(self.PTOutFlow) #for security (link with HR module): -> zero UPHw !!!
                self.PTFinal1.update(self.PTOutFlow) #avoid conflicts !!!
                
            adjustProd(self.UPHw1,self.UPHw_dot,self.NDaysProc3)

            if self.internalHR == True:
                adjustDiff(self.DTCrossHXHT,self.PTOutFlowRec,self.PTInFlowRec)
                adjustDiff(self.DTCrossHXLT,self.PTOutFlow2,self.PTInFlow2)

                adjustFlow(self.QHXdotProcInt2,self.FluidRhoCp,self.VInFlowDay2,
                           self.PTInFlowRec2,self.PTInFlow1,self.DTQHXIn,self.DTQHXIn1)
                
                adjustDiff(self.dhOutFlow1,self.hOutFlowRec,self.hOutFlow2)
                adjustProdC(self.QHXdotProcInt1,self.FluidDensity_w,self.dhOutFlow,self.VOutFlow)
                
            adjustSum(self.UPH2,self.UPHProc,self.QHXProc)
            adjustSum3(self.UPH1,self.UPHm,self.UPHc,self.UPHs)
            
            adjustProd(self.UPHs1,self.UPHsdot,self.NBatchPerYear2)
            adjustProd(self.NBatchPerYear1,self.NDaysProc2,self.NBatch)
            adjustFlow(self.UPHsdot1,self.FluidRhoCp,self.VolProcMed,
                       self.PT3,self.PTStartUp,self.DTUPHs,self.DTUPHs1)
            
            adjustProd(self.UPHc1,self.UPHcdot,self.NDaysProc1)
            adjustFlow(self.UPHcdot2,self.FluidRhoCp,self.VInFlowDay1,
                       self.PT2,self.PTInFlowRec1,self.DTUPHcNet,self.DTUPHcNet1)
            
            adjustDiff(self.UPHcdot1,self.UPHcdotGross,self.QHXdotProcInt)
            
            adjustFlow(self.UPHcdotGross1,self.FluidRhoCp,self.VInFlowDay,
                       self.PT1,self.PTInFlow,self.DTUPHcGross,self.DTUPHcGross1)
            
            adjustProd(self.UPHm1,self.QOpProc,self.HPerYearProc)
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

        cycle.checkTotalBalance()
 
#------------------------------------------------------------------------------
    def ccheckAll(self):    
#------------------------------------------------------------------------------
#   check block
#------------------------------------------------------------------------------

        ccheck4(self.PT,self.PT1,self.PT2,self.PT3,self.PT4)  
        ccheck2(self.PTInFlow,self.PTInFlow1,self.PTInFlow2)
        ccheck3(self.PTInFlowRec,self.PTInFlowRec1,self.PTInFlowRec2,self.PTInFlowRec3)
        ccheck1(self.PTStartUp,self.PTStartUp1)
        ccheck1(self.VolProcMed,self.VolProcMed1)
        ccheck3(self.VInFlowDay,self.VInFlowDay1,self.VInFlowDay2,self.VInFlowDay3)
        ccheck1(self.VOutFlow,self.VOutFlow1)
        ccheck3(self.PTOutFlow,self.PTOutFlow1,self.PTOutFlow2,self.PTOutFlow3)
        ccheck3(self.PTOutFlowRec,self.PTOutFlowRec1,self.PTOutFlowRec2,self.PTOutFlowRec3)
        ccheck1(self.DTCrossHXLT,self.DTCrossHXLT1)
        ccheck1(self.DTCrossHXHT,self.DTCrossHXHT1)
        
        ccheck1(self.HPerYearProc,self.HPerYearProc1)
        ccheck1(self.DTLoss,self.DTLoss1)
        ccheck1(self.QLoss,self.QLoss1)
        ccheck1(self.QOpProc,self.QOpProc1)
        ccheck1(self.QEvapProc,self.QEvapProc1)
        ccheck1(self.UPHm,self.UPHm1)
        ccheck1(self.UPHcdotGross,self.UPHcdotGross1)
        ccheck2(self.QHXdotProcInt,self.QHXdotProcInt1,self.QHXdotProcInt2)
        ccheck2(self.UPHcdot,self.UPHcdot1,self.UPHcdot2)
        ccheck1(self.UPHc,self.UPHc1)
        ccheck1(self.UPHsdot,self.UPHsdot1)
        ccheck4(self.NDaysProc,self.NDaysProc1,self.NDaysProc2,self.NDaysProc3,self.NDaysProc4)
        ccheck2(self.NBatchPerYear,self.NBatchPerYear1,self.NBatchPerYear2)
        ccheck1(self.UPHs,self.UPHs1)
        ccheck1(self.UPHProc,self.UPHProc1)
        ccheck1(self.QHXProc,self.QHXProc1)
        ccheck2(self.UPH,self.UPH1,self.UPH2)

        ccheck1(self.UPHw,self.UPHw1)
        ccheck1(self.UPHw_dot,self.UPHw_dot1)
        ccheck1(self.DTOutFlow,self.DTOutFlow1)
        ccheck2(self.PTFinal,self.PTFinal1,self.PTFinal2)
        ccheck1(self.UPHw,self.QWHProc)#At the moment they are the same. Change it next future when vessel heat recovery will be implemented
        ccheck1(self.UAProc,self.UAProc1)

        ccheck2(self.hOutFlow,self.hOutFlow1,self.hOutFlow2)
        ccheck1(self.hOutFlowRec,self.hOutFlowRec1)
        ccheck1(self.hFinal,self.hFinal1)
        ccheck1(self.dhOutFlow,self.dhOutFlow1)
        ccheck1(self.dhFinal,self.dhFinal1)
        
        ccheck1(self.xOutFlow,self.xOutFlow1)
        ccheck1(self.xOutFlowRec,self.xOutFlowRec1)
        ccheck1(self.xFinal,self.xFinal1)
        
#------------------------------------------------------------------------------
    def estimate(self):  
#------------------------------------------------------------------------------
#   estimates some of the data that are not sufficiently precise
#   should be a subset of the data that are within screen
#   (not necessarily ALL data have to be estimated)
#------------------------------------------------------------------------------

        self.PTOutFlowRec.setEstimate(self.PT.val,limits=(self.PT.valMin,self.PT.valMax))        
        self.VOutFlow.setEstimate(self.VInFlowDay.val,limits=(self.VInFlowDay.valMin,self.VInFlowDay.valMax))
        self.PTInFlow.setEstimate(15.0,limits = (5.0,35.0))

#        if self.internalHR == True:
        if (self.PT.val - self.PTInFlow.val > 5.0):

            self.DTCrossHXHT.setEstimate(10.0,limits = (5.0,999.0))
            self.DTCrossHXLT.setEstimate(10.0,limits = (5.0,999.0))

        else:
            self.PTInFlowRec.update(self.PTInFlow)
            self.internalHR = False


        if self.NBatch.val > 0 and (self.NBatch.val is not None):
            vol1 = self.VInFlowDay.val / self.NBatch.val
        else:
            vol1 = 0.0
            
        if self.VolProcMed.val is not None:
            vol2 = self.VolProcMed.val
        else:
            vol2 = 0.0
            
        vol = max(vol1,vol2)

        if vol < INFINITE:
        
            surface = 10.0 * pow(vol,2.0/3)
            UAmin = 0.0004 * surface * 0.1  #0.4 W/m2K well insulated vessel
            UA = 0.008 * surface
            UAmax = 0.002 * surface * 1.0   #2.0 W/m2K badly insulated equipment
            
            self.UAProc.setEstimate(UA,limits=(UAmin,UAmax))

            # estimate of Evaporation losses

        QLossMax = UAmax*self.DTLoss.valMax
        
        if self.QOpProc.valMax <= QLossMax:    # maintenance can be fully explained by
                                                # thermal losses
            self.QEvapProc.setEstimate(0.0,limits = (0.0,0.0))
            
# WARNING: this apriori assumption can give problems in cases with evaporation !!!!

        
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
