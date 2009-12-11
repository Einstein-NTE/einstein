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
#                       30/04/2008 - 03/07/2008
#
#   Update No. 002
#
#   Since Version 1.0 revised by:
#
#                       Hans Schweiger  06/04/2009
#                       Hans Schweiger  24/07/2009
#               
#   01/04/2009  HS  Fix number of operating hours (4000 h) eliminated
#                   Clean-up: elimination of prints
#   24/07/2009  HS  Possibility for defining return temperature in open circuits
#                   introduced
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

#-----  Imports for standalone testing in any directory
if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath('../../..'))

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
class CheckPipe():
#------------------------------------------------------------------------------
#   Carries out consistency checking for pipeduct m
#------------------------------------------------------------------------------

    def __init__(self,m):     #function that is called at the beginning when object is created


        self.DistribCircFlow = CCPar("DistribCircFlow")
        self.PercentRecirc = CCPar("PercentRecirc",parType="X")
        self.Tfeedup = CCPar("Tfeedup",parType="T")
        self.TotLengthDistPipe = CCPar("TotLengthDistPipe") #one way
        self.DDistPipe = CCPar("DDistPipe")
        self.DeltaDistPipe = CCPar("DeltaDistPipe")
        

        self.TenvPipe = CCPar("TenvPipe",parType="T") 
        self.TrefPipe = CCPar("TrefPipe",parType="T")
        self.QHXPipe = CCPar("QHXPipe")# It comes from the matrix (and from calculation from questionnaire??)
        self.UPHProcm = CCPar("UPHProcm")# It comes from the matrix (and from calculation from questionnaire??)
        self.USHm = CCPar("USHm",priority=2)# It comes from the matrix (and from calculation from questionnaire??)
# assign a variable to all intermediate/calculated values needed

        

        self.xForwIn = CCPar("xForwIn",parType="X")
        self.xForwOut = CCPar("xForwOut",parType="X")
        self.xRetIn = CCPar("xRetIn",parType="X")
        self.xRetOut = CCPar("xRetOut",parType="X")
        self.xRetRec = CCPar("xRetRec",parType="X")
        self.xFeedup = CCPar("xFeedup",parType="X")

        self.hForwIn1 = CCPar("hForwIn1")
        self.hForwOut1 = CCPar("hForwOut1")
        self.hForwOut2 = CCPar("hForwOut2")
        
        self.hRetIn = CCPar("hRetIn")
        self.hRetIn1 = CCPar("hRetIn1")
        self.hRetIn2 = CCPar("hRetIn2")
        self.hRetIn3 = CCPar("hRetIn3")
        self.hRetIn4 = CCPar("hRetIn4")

        self.hRetRec = CCPar("hRetRec")
        self.hRetRec1 = CCPar("hRetRec1")
        self.hRetRec2 = CCPar("hRetRec2")

        self.hRetOut = CCPar("hRetOut")
        self.hRetOut1 = CCPar("hRetOut1")
        self.hRetOut2 = CCPar("hRetOut2")
        self.hRetOut3 = CCPar("hRetOut3")
        self.hRetOut4 = CCPar("hRetOut4")

        self.hFeedUp1 = CCPar("hFeedUp1")

        self.hForwIn = CCPar("hForwIn")
        self.hForwIn1 = CCPar("hForwIn1")
        self.hForwIn2 = CCPar("hForwIn2")
        
        self.hForwOut = CCPar("hForwOut")
        self.hFeedUp = CCPar("hFeedUp")
        self.hFeedUp1 = CCPar("hFeedUp1")
        self.hFeedUp2 = CCPar("hFeedUp2")
        self.hFeedUp3 = CCPar("hFeedUp3")

        self.DhRetRecFeedup = CCPar("DhRetRecFeedup")
        self.DhRetRecFeedup1 = CCPar("DhRetRecFeedup1")
        self.DhRetRecFeedup2 = CCPar("DhRetRecFeedup2")
      
        self.DhRetRecFeedupPercent1 = CCPar("DhRetRecFeedupPercent1")
        self.DhRetRecFeedupPercent= CCPar("DhRetRecFeedupPercent")

        self.DhRetRecFeedupPercInv1 = CCPar("DhRetRecFeedupPercInv1")
        self.DhRetRecFeedupPercInv= CCPar("DhRetRecFeedupPercInv")
             
        self.DhForw = CCPar("DhForw")
        self.DhForw1 = CCPar("DhForw1")
        self.DhForw2 = CCPar("DhForw2")

        self.DhRet = CCPar("DhRet")            #auxiliary variable added for DTin = DTout + DTfwd + DTret
        self.DhRet1 = CCPar("DhRet1")

        self.DhIn = CCPar("DhIn")
        self.DhIn1 = CCPar("DhIn1")
        self.DhIn2 = CCPar("DhIn2")

        self.DhOut = CCPar("DhOut")
        self.DhOut1 = CCPar("DhOut1")
        self.DhOut2 = CCPar("DhOut1")

        self.DhRec1 = CCPar("DhRec1")
        self.DhWH1 = CCPar("DhWH1")

        self.DhRec = CCPar("DhRec")
        self.DhWH = CCPar("DhWH")

        self.ToutDistrib1 = CCPar("ToutDistrib1")
        self.ToutDistrib2 = CCPar("ToutDistrib2")
        self.TreturnDistrib1 = CCPar("TreturnDistrib1")
        self.TreturnDistrib2 = CCPar("TreturnDistrib2")

        self.TForwOut = CCPar("TForwOut",parType="T")
        self.TForwOut1 = CCPar("TForwOut1")

        self.TRetIn = CCPar("TRetIn",parType="T")
        self.TRetOut = CCPar("TRetOut",parType="T")
        self.TRetOut1 = CCPar("TRetOut1",parType="T")

        self.Tfeedup1 = CCPar("Tfeedup1")

        self.PercentRecirc1 = CCPar("PercentRecirc1")
        self.PercentRecirc2 = CCPar("PercentRecirc2")

        self.PercentFeedUp = CCPar("PercentFeedUp",parType="X")
        self.PercentFeedUp1 = CCPar("PercentFeedUp1")
        self.PercentFeedUp2 = CCPar("PercentFeedUp2")
        
        self.FeedUpFlow = CCPar("FeedUpFlow")
        self.FeedUpFlow1 = CCPar("FeedUpFlow1")
        self.FeedUpFlow2 = CCPar("FeedUpFlow2")
        
        self.DistribCircFlow1 = CCPar("DistribCircFlow1")
        self.DistribCircFlow2 = CCPar("DistribCircFlow2")
        self.DistribCircFlow3 = CCPar("DistribCircFlow3")
        self.DistribCircFlow4 = CCPar("DistribCircFlow4")
        self.DistribCircFlow5 = CCPar("DistribCircFlow5")

        
        self.RecFlow1 = CCPar("RecFlow1")
        self.RecFlow2 = CCPar("RecFlow2")
        self.RecFlow = CCPar("RecFlow")

        self.DTForwLoss1 = CCPar("DTForwLoss1")
        self.DTForwLoss2 = CCPar("DTForwLoss2")
        self.DTForwLoss = CCPar("DTForwLoss",parType="DT")

        self.DTRetLoss1 =CCPar("DTRetLoss1")
        self.DTRetLoss =CCPar("DTRetLoss",parType="DT")
        
        self.QdotLossForw1 = CCPar("QdotLossForw1")
        self.QdotLossRet1 = CCPar("QdotLossRet1")
        self.QdotLossRet2 = CCPar("QdotLossRet2")

        self.QdotLossForw2 = CCPar("QdotLossForw2")
        self.QdotLossRet2 = CCPar("QdotLossRet2")

        self.QdotLossForw = CCPar("QdotLossForw")
        self.QdotLossRet = CCPar("QdotLossRet")

        self.QdotWHPipe1 = CCPar("QWHdotPipe1")
        self.QdotWHPipe = CCPar("QWHdotPipe")
        self.QWHPipe = CCPar("QWHPipe",priority = 2)
        self.QWHPipe1 = CCPar("QWHPipe1")

        self.QdotLossPipe1 = CCPar("QdotLossPipe1")
        self.QdotLossPipe = CCPar("QdotLossPipe")

        self.QLossPipe = CCPar("QLossPipe")
        self.QLossPipe1 = CCPar("QLossPipe1")
        
         
        self.USHdotPipe1 = CCPar("USHdotPipe1")
        self.USHdotPipe = CCPar("USHdotPipe")
        self.USHPipe1 = CCPar("USHPipe1")
        self.USHPipe2 = CCPar("USHPipe2")
        self.USHPipe3 = CCPar("USHPipe3")
        self.USHPipe = CCPar("USHPipe")
        self.USHm1 = CCPar("USHm1")

        self.QHXPipe = CCPar("QHXPipe", priority = 2)
        self.QHXPipe1 = CCPar("QHXPipe1")

        self.UPHdotProcm1 = CCPar("UPHdotProcm1")
        self.UPHdotProcm2 = CCPar("UPHdotProcm2")
        self.UPHdotProcm = CCPar("UPHdotProcm")

        self.UPHProcm1 = CCPar("UPHProcm1")
        self.UPHProcm2 = CCPar("UPHProcm2")
        self.UPHProcm3 = CCPar("UPHProcm3")

        self.DoPipe = CCPar("DoPipe")
        
        self.HPerYearPipe1 = CCPar("HPerYearPipe1")
        self.HPerYearPipe2 = CCPar("HPerYearPipe2")
        self.HPerYearPipe = CCPar("HPerYearPipe")
        self.HPerYearPipe.valMax = 8760
        self.HDEffAvg = CCPar("HDEffAvg")
        
        self.UAPipe1 = CCPar("UAPipe1")
        self.UAPipe2 = CCPar("UAPipe2")
        self.UAPipe = CCPar("UAPipe")
        self.dUAPipe = CCPar("dUAPipe")

        self.ONE = CCOne()
        
        self.importData(m)

        if DEBUG in ["ALL","BASIC"]:
            self.showAllPipe()
#------------------------------------------------------------------------------
    def importData(self,m):  
#------------------------------------------------------------------------------
#   imports data from SQL tables (from AlternativeProposalNo = -1)
#------------------------------------------------------------------------------

        self.PipeDuctNo = m+1
        ANo = -1
        
#..............................................................................
# assign empty CCPar to all questionnaire parameters

        
        self.DistribCircFlow = CCPar("DistribCircFlow")
        self.ToutDistrib = CCPar("ToutDistrib",parType="T")
        self.TreturnDistrib = CCPar("TreturnDistrib",parType="T")
        self.PercentRecirc = CCPar("PercentRecirc",parType="X")
        self.Tfeedup = CCPar("Tfeedup",parType="T")
        self.TotLengthDistPipe = CCPar("TotLengthDistPipe") #one way
        self.DDistPipe = CCPar("DDistPipe")
        self.DeltaDistPipe = CCPar("DeltaDistPipe")
        

        self.TenvPipe = CCPar("TenvPipe",parType="T") 
        self.TrefPipe = CCPar("TrefPipe",parType="T")
        
        self.UPHProcm = CCPar("UPHProcm",priority=2)# It comes from the matrix (and from calculation from questionnaire??)
        self.USHm = CCPar("USHm",priority=2)# It comes from the matrix (and from calculation from questionnaire??)

        
#..............................................................................
# reading data from table "qdistributionhc"
#        try:
        qdistributionhcTable = Status.DB.qdistributionhc.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].PipeDuctNo[self.PipeDuctNo]
    
        if len(qdistributionhcTable) > 0:
            qdistributionhc = qdistributionhcTable[0]

            fluid = Fluid(qdistributionhc.HeatDistMedium)
            self.FluidCp = fluid.cp
            self.Fluid_hL = fluid.hL
            self.FluidTCond = fluid.TCond

            self.DistribCircFlow.setValue(qdistributionhc.DistribCircFlow)
            self.ToutDistrib.setValue(qdistributionhc.ToutDistrib)
            self.TreturnDistrib.setValue(qdistributionhc.TreturnDistrib)
            self.PercentRecirc.setValue(qdistributionhc.PercentRecirc)

            if self.PercentRecirc.val == 0.0:
                self.pipeType = "open"
            else:
                self.pipeType = "closed"
                
            self.Tfeedup.setValue(qdistributionhc.Tfeedup)
            self.TotLengthDistPipe.setValue(qdistributionhc.TotLengthDistPipe)
            self.UAPipe.setValue(qdistributionhc.UAPipe)
            self.DDistPipe.setValue(qdistributionhc.DDistPipe)
            self.DeltaDistPipe.setValue(qdistributionhc.DeltaDistPipe)

            self.TenvPipe.setValue(18,err=0.0)  #°C
            self.TrefPipe.setValue(0,err=0.0)   #°C, NOT USED
        else:
            self.FluidCp = 0.00116
            self.Fluid_hL = 0.0
            self.FluidTCond = INFINITE
            logTrack("CheckPipe(importData): error reading data from qdistributionhc in PipeNo: %s"%self.PipeDuctNo)
            
#        print "CheckPipe: TCond = %s"%self.FluidTCond       

#####TESTING ONLY: unknown HPerYearPipe gives problems !!!!
#        self.HPerYearPipe.setValue(4000.0,err=0.0)
#        logDebug("CheckPipe (importData): pipe operating hours fixed to 4000 h")

#calculate dUAPipe from DDistPipe and DoPipe only if it cannot be calculated by dUA = UA/LPipe
        if (self.UAPipe.val is None) or (self.TotLengthDistPipe is None):
            if self.DDistPipe.val is not None and self.DeltaDistPipe.val is not None:
                self.DoPipe.setValue (self.DDistPipe.val + (2*self.DeltaDistPipe.val))
                try: self.dUAPipe.setValue(0.000314 /(log(self.DoPipe.val) - log(self.DDistPipe.val)))
                except: pass
            else:   ####### for testing. IMPORTANT THAT THERE's A VALUE
                self.dUAPipe.setValue(0.0005)   # in kW/mK !!!!
                self.dUAPipe.sqerr = 0.25
                self.dUAPipe.valMin = 0.00025
                self.dUAPipe.valMax = 0.00075

                
#------------------------------------------------------------------------------
    def exportData(self):  
#------------------------------------------------------------------------------
#   stores corrected data in SQL (under AlternativeProposalNo = 0)
#------------------------------------------------------------------------------

        ANo = 0
#        print "CheckPipe (exportData): exporting data to qdistributionhc",self.PipeDuctNo
                
        
#..............................................................................
# writing data into table " qdistributionhc"

        if ANo == 0:
            qdistributionhcTable = Status.DB.qdistributionhc.Questionnaire_id[Status.PId].AlternativeProposalNo[ANo].PipeDuctNo[self.PipeDuctNo]
            if len(qdistributionhcTable) > 0:
#                print "exporting data to qdistributionhc"
                qdistributionhc = qdistributionhcTable[0]

                qdistributionhc.DistribCircFlow = check(self.DistribCircFlow.val)
                qdistributionhc.ToutDistrib = check(self.ToutDistrib.val)
                qdistributionhc.TreturnDistrib = check(self.TreturnDistrib.val)
                qdistributionhc.PercentRecirc = check(self.PercentRecirc.val)
                qdistributionhc.Tfeedup = check(self.Tfeedup.val)
                qdistributionhc.TotLengthDistPipe = check(self.TotLengthDistPipe.val)
                qdistributionhc.DDistPipe = check(self.DDistPipe.val)
                qdistributionhc.DeltaDistPipe = check(self.DeltaDistPipe.val)
        
#                qdistributionhc.HPerYearPipe = check(self.HPerYearPipe.val)
                qdistributionhc.HDEffAvg = check(self.HDEffAvg.val)
                qdistributionhc.QHXPipe = check(self.QHXPipe.val)
                qdistributionhc.QWHPipe = check(self.QWHPipe.val)
                qdistributionhc.UAPipe = check(self.UAPipe.val)
                qdistributionhc.UPHProcm = check(self.UPHProcm.val)
                qdistributionhc.USHm = check(self.USHm.val)
                qdistributionhc.USHPipe = check(self.USHPipe.val)
                qdistributionhc.QLossPipe = check(self.QLossPipe.val)

                #qdistributionhc.TenvPipe = check(self.TenvPipe .val)
                #qdistributionhc.TrefPipe =  check(self.TrefPipe.val)

                #qdistributionhc.QLossPipe = check(self.QLossPipe.val)
                     
                Status.SQL.commit()
            else:
                 logTrack("CheckPipe (exportData): no corresponding entry found in qdistributionhc")
                
#------------------------------------------------------------------------------

    def showAllPipe(self):
        print "====================="

        self.xForwIn.show()
        self.xForwOut.show()
        self.xRetIn.show()
        self.xRetOut.show()
        self.xRetRec.show()
        self.xFeedup.show()

#        self.hForwIn1.show()

        self.hForwOut.show()
#        self.hForwOut1.show()
#        self.hForwOut2.show()
        
        self.hRetIn.show()
#        self.hRetIn1.show()
#        self.hRetIn2.show()
#        self.hRetIn3.show()

        self.hRetRec.show()
#        self.hRetRec1.show()

        self.hRetOut.show()
#        self.hRetOut1.show()
#        self.hRetOut2.show()
#        self.hRetOut3.show()

        self.hForwIn.show()
#        self.hForwIn1.show()
#        self.hForwIn2.show()
        
        self.hFeedUp.show()
#        self.hFeedUp1.show()
#        self.hFeedUp2.show()
#        self.hFeedUp3.show()

#        self.DhRetRecFeedup1.show()
#        self.DhRetRecFeedupPercent1.show()

#        self.DhRetRecFeedupPercInv1.show()
             
        self.DhForw.show()
#        self.DhForw1.show()

        self.DhRec.show()
#        self.DhRec1.show()

        self.DhIn.show()
#        self.DhIn1.show()

        self.DhOut.show()
#        self.DhOut1.show()

        self.DhWH.show()
#        self.DhWH1.show()

        self.ToutDistrib.show()
#        self.ToutDistrib1.show()
#        self.ToutDistrib2.show()

        self.TreturnDistrib.show()
#        self.TreturnDistrib1.show()
#        self.TreturnDistrib2.show()

        self.TForwOut.show()
#        self.TForwOut1.show()

        self.TRetIn.show()

        self.TRetOut.show()

        self.Tfeedup.show()
#        self.Tfeedup1.show()

        self.PercentRecirc.show()
#        self.PercentRecirc1.show()
#        self.PercentRecirc2.show()

        self.PercentFeedUp.show()
#        self.PercentFeedUp1.show()

        self.DistribCircFlow.show()
#        self.DistribCircFlow1.show()
#        self.DistribCircFlow2.show()
#        self.DistribCircFlow3.show()

#        self.RecFlow1.show()
#        self.RecFlow2.show()
        self.RecFlow.show()

#        self.FeedUpFlow1.show()
        self.FeedUpFlow.show()

#        self.DTForwLoss1.show()
        self.DTForwLoss.show()

        self.DTRetLoss1.show()
        self.DTRetLoss.show()
        
        self.QdotLossForw.show()
#        self.QdotLossForw1.show()
#        self.QdotLossForw2.show()

        self.QdotLossRet.show()
#        self.QdotLossRet1.show()
#        self.QdotLossRet2.show()

        self.QdotWHPipe.show()
#        self.QdotWHPipe1.show()
        
        self.QdotLossPipe.show()
#        self.QdotLossPipe1.show()
         
        self.USHdotPipe.show()
#        self.USHdotPipe1.show()

#        self.QHXPipe1.show()

        self.UPHdotProcm.show()
        self.UPHdotProcm1.show()
        self.UPHdotProcm2.show()

        self.DoPipe.show()
               
        self.UAPipe.show()
        self.UAPipe1.show()
        self.UAPipe2.show()
        self.dUAPipe.show()
       

        self.TotLengthDistPipe.show()
        self.DDistPipe.show()
        self.DeltaDistPipe.show()

        self.HPerYearPipe.show()
        self.HDEffAvg.show()

        self.QHXPipe.show()
        self.QHXPipe1.show()

        self.QWHPipe.show()
        self.QWHPipe1.show()
        
        self.USHm.show()
        self.USHm1.show()

        self.USHPipe.show()
        self.USHPipe1.show()
        self.USHPipe2.show()
        self.USHPipe3.show()

        self.QLossPipe.show()

        self.QWHPipe.show()
        #self.QLossPipe.screen

        self.UPHProcm.show()
        self.UPHProcm1.show()
        self.UPHProcm2.show()
        self.UPHProcm3.show()


        print "====================="
#-----------------------------------------------------------------------------
    def screen(self):  
#------------------------------------------------------------------------------
#   screens all variables in the block
#------------------------------------------------------------------------------

        if iszero(self.PercentFeedUp):
            self.Tfeedup.priority = 99

        if iszero(self.PercentRecirc):
            self.TreturnDistrib.priority = 99
            
        self.DistribCircFlow.screen()
        self.ToutDistrib.screen()
        self.TreturnDistrib.screen()
        self.PercentRecirc.screen()
        self.Tfeedup.screen()
        self.TotLengthDistPipe.screen()
        self.DDistPipe.screen()
        self.DeltaDistPipe.screen()

        self.HPerYearPipe.screen()
        self.HDEffAvg.screen()
        self.QHXPipe.screen()
        self.QWHPipe.screen()
        self.QLossPipe.screen
        self.UAPipe.screen()
        self.UPHProcm.screen()
        self.USHm.screen()
    
#------------------------------------------------------------------------------
    def check(self):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   main function carrying out the check of the block
#------------------------------------------------------------------------------

        if DEBUG in ["ALL","MAIN"]:
            print "-------------------------------------------------"
            print " PipeDucts checking"
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
              

#..............................................................................
# writing data into table " qdistributionhc"

            self.hForwIn1 = calcH("hForwIn1",
                                  self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                                  self.ToutDistrib1,self.xForwIn) #ToutDistrib1
            self.hForwOut1 = calcH("hForwOut1",self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                                   self.TForwOut1,self.xForwOut)#TForwOut1
            self.hRetIn1 = calcH("hRetIn1",self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                                 self.TRetIn,self.xRetIn)
            self.hRetRec1 = calcH("hRetRec1",self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                                  self.TreturnDistrib1,self.xRetIn)#TreturnDistrib1
            self.hRetOut1 = calcH("hRetOut1",self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                                  self.TRetOut,self.xRetOut)
            self.hFeedUp1 = calcH("hFeedUp1",self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                                  self.Tfeedup,self.xFeedup)


            self.PercentFeedUp1 = calcDiff("PercentFeedUp1",self.ONE,self.PercentRecirc)#hFeedUp,hRetRec

#
# The following block is based on the equation:
#
#   hRetOut = %FeedUp*hFeedUp + %Recirc*hRetRec
#           = hFeedUp + %Recirc*(hRetRec - hFeedUp) =: hFeedUp + DhRetRecFeedUp%
#           = hRetRec + %FeedUp*(hFeedUp - hRedRec) = hRetRec - %FeedUp*(hRedRec - hFeedUp) =: hFeedUp - DhRetRecFeedUp%INV
            self.DhRetRecFeedup1 = calcDiff("DhRetRecFeedup1",self.hRetRec,self.hFeedUp)#hFeedUp,hRetRec
            self.DhRetRecFeedupPercent1 = calcProd("DhRetRecFeedupPercent1",self.DhRetRecFeedup,self.PercentRecirc1)#PercentRecirc1
            self.DhRetRecFeedupPercInv1 = calcProd("DhRetRecFeedupPercInv1",self.DhRetRecFeedup2,self.PercentFeedUp)#PercentRecirc1
            self.hRetOut2 = calcSum("hRetOut2",self.DhRetRecFeedupPercent,self.hFeedUp1)#hFeedUp2
            self.hRetOut3 = calcDiff("hRetOut3",self.hRetRec,self.DhRetRecFeedupPercInv)#hFeedUp2

            self.DhForw1 = calcDiff("DhForw1",self.hForwIn,self.hForwOut)#hForwIn, hForwOut
            self.DhRet1 = calcDiff("DhRet1",self.hRetIn4,self.hRetOut4)
           
            self.DhIn1 = calcDiff("DhIn1",self.hForwIn2,self.hRetOut)#hForwIn2
            self.DhOut1 = calcDiff("DhOut1",self.hForwOut2,self.hRetIn)#hForwOut2,hRetIn
            self.DhRec1 = calcDiff("DhRec1",self.hRetIn2,self.hRetRec2) #hRetIn2, hRetRec2
            self.DhWH1 = calcDiff("DhWH1",self.hRetIn3,self.hFeedUp2) #hFeedUp3,hRetIn3
            self.DhIn2 = calcSum3("DhIn2",self.DhForw,self.DhOut,self.DhRet)

            self.RecFlow1 = calcProd ("RecFlow1",self.DistribCircFlow,self.PercentRecirc2)#PercentRecirc2
            self.FeedUpFlow2 = calcProd ("FeedUpFlow2",self.DistribCircFlow,self.PercentFeedUp2)#PercentRecirc2
#HS substituted diff by sum            self.FeedUpFlow1 = calcDiff("FeedUpFlow1",self.DistribCircFlow1,self.RecFlow) #DistribCircFlow1, RecFlow
            self.DistribCircFlow1 = calcSum("DistribCircFlow1",self.FeedUpFlow1,self.RecFlow) #DistribCircFlow1, RecFlow

            self.QdotLossForw1 = calcProd("QdotLossForw1",self.DhForw,self.DistribCircFlow4)#DistribCircFlow

            if self.pipeType == "open":
                self.QdotLossRet1.setValue(0.0)
                self.QdotLossRet2.setValue(0.0)
            else:
                self.QdotLossRet1 = calcProd("QdotLossRet1",self.DhRec,self.RecFlow2) #calculated from DHRec, RecFlow2
                self.QdotLossRet2 = calcProdC("QdotLossRet2",0.5,self.UAPipe2,self.DTRetLoss)#DTForwLoss2
                self.DTRetLoss1 = calcDiff("DTRetLoss1",self.TreturnDistrib2,self.TenvPipe) #TreturnDistrib2
                
            self.QdotWHPipe1 = calcProd("QdotWHPipe1",self.DhWH,self.FeedUpFlow)
            self.USHdotPipe1 = calcProd("USHdotPipe1",self.DhIn,self.DistribCircFlow2)#DistribCircFlow2
            self.UPHdotProcm1 = calcProd("UPHdotProcm1",self.DhOut,self.DistribCircFlow3)#DistribCircFlow3

            self.UAPipe1 = calcProdC("UAPipe1",2.0,self.dUAPipe,self.TotLengthDistPipe)
            self.DTForwLoss1 = calcDiff("DTForwLoss1",self.ToutDistrib2,self.TenvPipe) #ToutDistrib2
            self.QdotLossForw2 = calcProdC("QdotLossForw2",0.5,self.UAPipe,self.DTForwLoss)#DTForwLoss

            self.QdotLossPipe1 = calcSum("QdotLossPipe1",self.QdotLossForw,self.QdotLossRet)

            self.USHdotPipe2 = calcSum3("USHdotPipe2",self.QdotLossPipe,self.UPHdotProcm,self.QdotWHPipe)#UPHdotProcm
            self.USHPipe1 = calcProd("USHPipe1",self.USHdotPipe,self.HPerYearPipe1) # HPerYearPipe
            self.USHPipe2 = calcSum("USHPipe2",self.USHm,self.QHXPipe)

            self.UPHProcm1 = calcProd("UPHProcm1",self.UPHdotProcm2,self.HPerYearPipe2) # HPerYearPipe, UPHdotProcm2

            self.UPHProcm2 = calcProd("USHProcm2",self.USHPipe,self.HDEffAvg)
            self.USHPipe3 = calcSum3("USHPipe3",self.QLossPipe1,self.UPHProcm3,self.QWHPipe1)#UPHdotProcm
         
   
            if DEBUG in ["ALL","MAIN"]:
                self.showAllPipe()

# Step 2: Cross check the variables

                print "-------------------------------------------------"
                print "Step 2: cross checking"
                print "-------------------------------------------------"
                
            self.ccheckAll()                
            
            if DEBUG in ["ALL","MAIN"]:
                self.showAllPipe()

# Step 3: Adjust the variables (inverse of calculation routines)
                print "-------------------------------------------------"
                print "Step 3: calculating from right to left (ADJUST)"
                print "-------------------------------------------------"
  
            adjustSum3(self.USHPipe3,self.QLossPipe1,self.UPHProcm3,self.QWHPipe1)#UPHdotProcm
            adjustProd(self.UPHProcm2,self.USHPipe,self.HDEffAvg)
            adjustProd(self.UPHProcm1,self.UPHdotProcm2,self.HPerYearPipe2) 
            adjustSum(self.USHPipe2,self.USHm,self.QHXPipe)
            adjustProd(self.USHPipe1,self.USHdotPipe,self.HPerYearPipe1)
            adjustSum3(self.USHdotPipe2,self.QdotLossPipe,self.UPHdotProcm,self.QdotWHPipe)
            adjustSum(self.QdotLossPipe1,self.QdotLossForw,self.QdotLossRet)

            if self.pipeType == "closed":
                adjustProdC(self.QdotLossRet2,0.5,self.UAPipe2,self.DTRetLoss)
                adjustDiff(self.DTRetLoss1,self.TreturnDistrib2,self.TenvPipe,GTZero=True)
                            
            adjustProdC(self.QdotLossForw2,0.5,self.UAPipe,self.DTForwLoss)
            adjustDiff(self.DTForwLoss1,self.ToutDistrib2,self.TenvPipe,GTZero=True)
            adjustProdC(self.UAPipe1,2.0,self.dUAPipe,self.TotLengthDistPipe)
            adjustProd(self.UPHdotProcm1,self.DhOut,self.DistribCircFlow3)
            adjustProd(self.USHdotPipe1,self.DhIn,self.DistribCircFlow2)
            adjustProd(self.QdotWHPipe1,self.DhWH,self.FeedUpFlow)

            if self.pipeType == "open":
                self.DhRec.setValue(0.0)
            else:
                adjustProd(self.QdotLossRet1,self.DhRec,self.RecFlow2)
                
            adjustProd(self.QdotLossForw1,self.DhForw,self.DistribCircFlow4)
            adjustSum(self.DistribCircFlow1,self.FeedUpFlow1,self.RecFlow)
            adjustProd(self.FeedUpFlow2,self.DistribCircFlow5,self.PercentFeedUp2)#PercentRecirc2
            adjustProd (self.RecFlow1,self.DistribCircFlow,self.PercentRecirc2)
            adjustDiff(self.DhWH1,self.hRetIn3,self.hFeedUp2)
            adjustDiff(self.DhRec1,self.hRetIn2,self.hRetRec2)
            adjustDiff(self.DhOut1,self.hForwOut2,self.hRetIn)
            adjustSum3(self.DhIn2,self.DhForw2,self.DhOut2,self.DhRet)
            adjustDiff(self.DhIn1,self.hForwIn2,self.hRetOut)
            adjustDiff(self.DhRet1,self.hRetIn4,self.hRetOut4)
            adjustDiff(self.DhForw1,self.hForwIn,self.hForwOut)


            adjustDiff(self.hRetOut3,self.hRetRec,self.DhRetRecFeedupPercInv)#hFeedUp2
            adjustSum(self.hRetOut2,self.DhRetRecFeedupPercent,self.hFeedUp2)
            adjustProd(self.DhRetRecFeedupPercInv1,self.DhRetRecFeedup2,self.PercentFeedUp)#PercentRecirc1
            adjustProd(self.DhRetRecFeedupPercent1,self.DhRetRecFeedup,self.PercentRecirc1)
            adjustDiff(self.DhRetRecFeedup1,self.hRetRec,self.hFeedUp)
            adjustDiff(self.PercentFeedUp1,self.ONE,self.PercentRecirc)#hFeedUp,hRetRec

            adjustH(self.hFeedUp1,self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                    self.Tfeedup,self.xFeedup)
            
            adjustH(self.hRetOut1,self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                    self.TRetOut1,self.xForwOut)
            
            adjustH(self.hRetRec1,self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                    self.TreturnDistrib1,self.xRetIn)
            
            adjustH(self.hRetIn1,self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                    self.TRetIn,self.xRetIn)
            
            adjustH(self.hForwOut1,self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                    self.TForwOut1,self.xForwOut)
            
            adjustH(self.hForwIn1,self.FluidCp,
                                  self.FluidCp,
                                  self.Fluid_hL,
                                  self.FluidTCond,
                    self.ToutDistrib1,self.xForwIn) 
            
            
            if DEBUG in ["ALL","MAIN"]:
                self.showAllPipe()
           
# Step 4: Second cross check of the variables

                print "-------------------------------------------------"
                print "Step 4: cross checking"
                print "-------------------------------------------------"

            self.ccheckAll()                

            if DEBUG in ["ALL","MAIN"]:
                self.showAllPipe()

# Arrived at the end


        # self.dUAPipe: recalc Do,DeltaDistPipe,Ddistr...
            # self.DoPipe.setValue (DDistPipe + (2*DeltaDistPipe))
            # self.dUAPipe.setValue(0.314 /(logDoPipe - logDDistPipe))
        
        self.QWHPipe = calcProd("QWHPipe",self.QdotWHPipe,self.HPerYearPipe)# Not adjusted
        self.QLossPipe =calcProd("QLossPipe",self.QdotLossPipe,self.HPerYearPipe)# Not adjusted
         

    #añadido este último show all. sino no se ven los ultimos dos resultados ...
        if DEBUG in ["ALL","BASIC","MAIN"]:
            self.showAllPipe()

            print "-------------------------------------------------"
            print "Cycle balance: mean %s max %s "%(cycle.getMeanBalance(),cycle.getMaxBalance())
            print "-------------------------------------------------"

        return cycle.getMeanBalance()
    
#------------------------------------------------------------------------------
    def ccheckAll(self):     
#------------------------------------------------------------------------------
#   check centralised here (instead of repeating twice the same
#------------------------------------------------------------------------------

            ccheck1(self.Tfeedup,self.Tfeedup1)
            ccheck2(self.HPerYearPipe,self.HPerYearPipe1,self.HPerYearPipe2)
            ccheck2(self.UAPipe,self.UAPipe1,self.UAPipe2)
            ccheck1(self.TForwOut,self.TForwOut1)
            ccheck1(self.TRetOut,self.TRetOut1)
            ccheck2(self.ToutDistrib,self.ToutDistrib1,self.ToutDistrib2)
            ccheck2(self.TreturnDistrib,self.TreturnDistrib1,self.TreturnDistrib2)
            ccheck3(self.hFeedUp,self.hFeedUp1,self.hFeedUp2,self.hFeedUp3)
            ccheck2(self.PercentRecirc,self.PercentRecirc1,self.PercentRecirc2)
            ccheck2(self.PercentFeedUp,self.PercentFeedUp1,self.PercentFeedUp2)

            ccheck2(self.hForwIn,self.hForwIn1,self.hForwIn2)
            ccheck2(self.hRetIn,self.hRetIn1,self.hRetIn2)
            ccheck2(self.hRetIn,self.hRetIn3,self.hRetIn4)
            ccheck2(self.hRetRec,self.hRetRec1,self.hRetRec2)
            ccheck5(self.DistribCircFlow,self.DistribCircFlow1,self.DistribCircFlow2,self.DistribCircFlow3,\
                    self.DistribCircFlow4,self.DistribCircFlow5)
            ccheck2(self.RecFlow,self.RecFlow1,self.RecFlow2)
            ccheck2(self.DTForwLoss,self.DTForwLoss1,self.DTForwLoss2)
            ccheck2(self.UPHdotProcm,self.UPHdotProcm1,self.UPHdotProcm2)

                   
            ccheck2(self.hForwOut,self.hForwOut1,self.hForwOut2)
            ccheck2(self.hRetOut,self.hRetOut1,self.hRetOut2)
            ccheck2(self.hRetOut,self.hRetOut3,self.hRetOut4)
            ccheck2(self.DhRetRecFeedup,self.DhRetRecFeedup1,self.DhRetRecFeedup2)
            ccheck1(self.DhRetRecFeedupPercent,self.DhRetRecFeedupPercent1)
            ccheck1(self.DhRetRecFeedupPercInv,self.DhRetRecFeedupPercInv1)

            ccheck2(self.DhForw,self.DhForw1,self.DhForw2)
            ccheck1(self.DhRet,self.DhRet1)
            ccheck1(self.DhIn,self.DhIn1)
            ccheck2(self.DhOut,self.DhOut1,self.DhOut2)
            ccheck1(self.DhRec,self.DhRec1)
            ccheck1(self.DhWH,self.DhWH1)

            ccheck2(self.FeedUpFlow,self.FeedUpFlow1,self.FeedUpFlow2)
            ccheck2(self.QdotLossForw,self.QdotLossForw1,self.QdotLossForw2)
            ccheck2(self.QdotLossRet,self.QdotLossRet1,self.QdotLossRet2)
            ccheck1(self.QdotWHPipe,self.QdotWHPipe1)
            ccheck2(self.USHdotPipe,self.USHdotPipe1,self.USHdotPipe2)

            ccheck1(self.DTRetLoss,self.DTRetLoss1)
            ccheck1(self.QdotLossPipe,self.QdotLossPipe1)

            ccheck1(self.USHm,self.USHm1)
            ccheck1(self.QWHPipe,self.QWHPipe1)
            ccheck1(self.QLossPipe,self.QLossPipe1)
            ccheck3(self.UPHProcm,self.UPHProcm1,self.UPHProcm2,self.UPHProcm3)
            ccheck1(self.QHXPipe,self.QHXPipe1)
            ccheck3(self.USHPipe,self.USHPipe1,self.USHPipe2,self.USHPipe3)

#==============================================================================
if __name__ == "__main__":
    
# direct connecting to SQL database w/o GUI. for testing only
    stat = Status("testCheckProc")
    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    Status.PId = 41
    Status.ANo = -1
#..............................................................................
    
    m = 0
    conflict.setDataGroup("pipe",m+1)

    ccPipe = CheckPipe(m)       # creates an instance of class CCheck
#    ccPipe.UPHProcm.setValue(5000000)
    ccPipe.check()
#    ccPipe.exportData(1)

    screen.setDataGroup("pipe",m+1)
    ccPipe.screen()
    screen.show()
    
#==============================================================================
