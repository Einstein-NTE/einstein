# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleCC (consistency check module)
#			
#------------------------------------------------------------------------------
#			
#	
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by: 	Claudia Vannoni, Hans Schweiger
#                       20/04/2008 - 18/08/2008
#
#   Update No. 001
#
#   Since Version 1.0 revised by:
#
#                       Hans Schweiger  06/04/2008
#               
#   06/04/2008  HS  Calculation of pipe operating hours added
#                   Clean-up: elimination of prints
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

from sys import *
from math import *
from numpy import *
from parameterList import *

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP
from einstein.modules.messageLogger import *

from ccheckFunctions import *
from checkMatrix import *
from checkCon import *
from checkProc import *
from checkEq import *
from checkFETfuel import *
from checkFETel import *
from checkPipe import *
from checkHX import *
from checkWHEE import *
from checkTotals import *
from connect import *

def _U(text):
    return unicode(_(text),"utf-8")

class ModuleCC(object):
    
#------------------------------------------------------------------------------
    def __init__(self):
#------------------------------------------------------------------------------
#   basic initialisation at the start-up of the tool
#------------------------------------------------------------------------------

        self.keys = ["CC Table","CC Info"] # the key to the data is sent by the panel

#..............................................................................
# creates an empty space for the different check-blocks

        self.ccFET = []
        self.NFET = 0
        
        self.ccEq = []
        self.NEquipe = 0
        
        self.ccProc = []
        self.NProc = 0

        self.ccPipe = []
        self.NPipeDuct = 0

        self.ccHX = []
        self.NHX = 0

        self.ccWHEE = []
        self.NWHEE = 0

        self.screen_priority = 2
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#   is called at entering the CC panel
#------------------------------------------------------------------------------

        self.parameterList = ParameterList().list
        self.updatePanel()
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#   function that updates the information on the CC panel on the GUI
#------------------------------------------------------------------------------

#..............................................................................
# export screening data

        logDebug("ModuleCC (updatePanel): screening with priority %s"%self.screen_priority)
        
        CCList = []
        nMissingVarsOfPriority=0
        
        for entry in CCScreen.screenList:

            if entry[4] <= self.screen_priority:

                if entry[4] == 1:
                    action = _U("Calculations w/o this are nonsense !!!")
                elif entry[4] == 2:
                    action = _U("Value required for detail analysis !!!")
                else:
                    action = _U("not strictly necessary")

                varName = str(entry[0])
                if varName in self.parameterList.keys():
                    description = self.parameterList[varName]
                else:
                    description = ""
#                print "ModuleCC (updatePanel): "
#                print self.parameterList
#                print MONTHS

                if entry[1] is not None:
                    val = '%9.2f'%entry[1]
                    if entry[2] >= 1.0:
                        err = '>100.00%'
                    else:
                        err = '%5.2f'%(100.0*pow(entry[2],0.5))+"%"
                else:
                    val = '---'
                    err = '---'

                if entry[4] == 1:
                    highlight = 1
                else:
                    highlight = 0
                    
                row = [entry[0]+"["+entry[3]+"]",
                       description,
                       val,
                       err,
                       action,
                       highlight]
                
                CCList.append(noneFilter(row))
                nMissingVarsOfPriority+=1

        if nMissingVarsOfPriority==0:
            if CCScreen.nScreened == 0:
                CCList.append(["","","","",""])
            else:
                CCList.append(["",_("CONGRATULATION: data set is sufficiently complete !!!"),"","",""])
            
        data = array(CCList)
        Status.int.setGraphicsData(self.keys[0], data)  #sends the data to the GUI

        nMissingVars = len(CCScreen.screenList)
        nScreenedVars = CCScreen.nScreened
        CCList = [nScreenedVars,"---",nMissingVarsOfPriority,self.screen_priority]

        Status.int.setGraphicsData(self.keys[1], CCList)  #sends the data to the GUI

#..............................................................................
# export conflict data to panel
        
        conflictReport = []

        conflictPairs = []
        n = len(conflict.conflictList)
        
#        for i in range(n):
#            index = n - i - 1
#            entry = conflict.conflictList[index]

        for entry in conflict.conflictList:
            
            pair = str(entry[2])+"/"+str(entry[6])
                                         
            if pair not in conflictPairs:
                conflictPairs.append(pair)

                listedVarName = str(entry[2])
                nameParts = listedVarName.split('[')
                if len(nameParts) > 0:
                    varName = nameParts[0]
                    if varName in self.parameterList.keys():
                        description = self.parameterList[varName]
                    else:
                        description = ""
                else:
                    description = ""

                row0 = [str(entry[2])+" [<>"+str(entry[6])+"]",entry[10],description]

                origin1 = ""
                for parname in entry[3]:
                    origin1 = origin1 + str(parname) + "; "

                if entry[4] is not None:
                    row1 = ["%12.2f"%entry[4],
                            "+/- "+"%5.2f"%(entry[5]*100.0)+"%",
                            origin1]
                else:
                    row1 = ["---",
                            "+/- "+"%5.2f"%(entry[5]*100.0)+"%",
                            origin1]
                    

                origin2 = ""
                for parname in entry[7]:
                    origin2 = origin2 + str(parname) + "; "

                if entry[8] is not None:
                    row2 = ["%12.2f"%entry[8],
                            "+/- "+"%5.2f"%(entry[9]*100.0)+"%",
                            origin2]
                else:
                    row2 = ["---",
                            "+/- "+"%5.2f"%(entry[9]*100.0)+"%",
                            origin2]
                    
                       
                conflictReport.append(noneFilter(row0))
                conflictReport.append(noneFilter(row1))
                conflictReport.append(noneFilter(row2))
                                         
        data = array(conflictReport)
        Status.int.setGraphicsData("CC Conflict", data)  #sends the data to the GUI

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def setPriorityLevel(self,level):
#------------------------------------------------------------------------------
#   is called at entering the CC panel
#------------------------------------------------------------------------------
        logDebug("ModuleCC: setting priority level to %s"%level)
        self.screen_priority = level
        self.updatePanel()
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def getQuestionnaireData(self):
#------------------------------------------------------------------------------
#   function that gets the data from the questionnaire
#------------------------------------------------------------------------------

#..............................................................................
# creates an empty space for the different check-blocks

        self.ccFET = []
        
        self.ccEq = []
        
        self.ccProc = []

        self.ccPipe = []

        self.ccHX = []

        self.ccWHEE = []


        logDebug("ModuleCC (getQuestionnaireData): running in new general mode (import connections from SQL)")

#..............................................................................
# import data on link of fuels and equipment

        getConnections()

#..............................................................................
# import data on fuel and electricity consumption (FET)

        self.NFET = Status.NFET
        NI = self.NFET-1
        
        self.FETFuel_i = CCRow("FETi",NI)
        self.FECi = CCRow("FETi",NI)
        self.ElGenera = CCPar("ElGenera")

        self.ccFETel = CheckFETel()
        
        for i in range(NI):      
            self.ccFET.append(CheckFETfuel(i+1))

#..............................................................................
# import data on existing equipment 

        self.NEquipe = Status.NEquipe
        NJ = self.NEquipe
        self.USHj = CCRow("USHj",NJ)     #note: this is a ROW of USH values, and not identical with the USHj variable within checkEq !!!
        self.FETj = CCRow("FETj",NJ)     #creates the space for intermediate storge towards matrix
        self.FETFuel_j = CCRow("FETFuel_j",NJ)     #creates the space for intermediate storge towards matrix
        self.FETel_c_j = CCRow("FETel_c_j",NJ)     #creates the space for intermediate storge towards matrix
        self.FETel_c = CCPar("FETel_c")     #creates the space for intermediate storge towards matrix
        self.ElGen_j = CCRow("ElGen_j",NJ)
        self.ElGen = CCPar("ElGen")     #creates the space for intermediate storge towards matrix

        self.QHXEq = CCRow("QHXEq",NJ)      # incoming waste heat from heat recovery
        self.QWHEq = CCRow("QWHEq",NJ)    # outgoing waste heat to be recovered

        self.ElGen_j = CCRow("ElGen_j",NJ)
        
        for j in range(NJ):
            self.ccEq.append(CheckEq(j))     # añade un objeto checkEq con todas las variables necesarias a la lista

#..............................................................................
# import data on existing processes

        self.NThProc = Status.NThProc
        NK = self.NThProc
        self.UPHProck = CCRow("UPHProck",NK)     #note: this is a ROW of USH values, and not identical with the USHj variable within checkEq !!!
        self.QHXk = CCRow("QHXk",NK)        #CHECK!!!!!!!!!!!!!!: Probably to be eliminated -> substitute by QHX or QWH
        self.QHXProc = CCRow("QHXProc",NK)      # incoming waste heat from heat recovery
        self.QWHProc = CCRow("QWHProc",NK)    # outgoing waste heat to be recovered

        for k in range(NK):
            self.ccProc.append(CheckProc(k))  # añade un objeto checkProc con todas las variables necesarias a la listac


#..............................................................................
# import data on existing pipeducts

        self.NPipeDuct = Status.NPipeDuct
        NM = self.NPipeDuct
        self.UPHProcm = CCRow("UPHProcm",NM)     #note: this is a ROW of USH values, and not identical with the USHj variable within checkEq !!!
        self.USHm = CCRow("USHm",NM) 
        self.QHXPipe = CCRow("QHXPipe",NM)        # incoming waste heat from heat recovery
        self.QWHPipe = CCRow("QWHPipe",NM)        # outgoing waste heat to be recovered

        for m in range(NM):
            self.ccPipe.append(CheckPipe(m))  # añade un objeto checkProc con todas las variables necesarias a la listac

#..............................................................................
# import data on existing heat exchangers

        self.NHX = Status.NHX
        NH = self.NHX
        self.QWH = CCRow("QWH",NH)     
        self.QHX = CCRow("QHX",NH)          

        for h in range(NH):
            self.ccHX.append(CheckHX(h))  # añade un objeto checkProc con todas las variables necesarias a la listac

#..............................................................................
# import data on existing WHEEs

        self.NWHEE = Status.NWHEE
        NN = self.NWHEE
        self.QWHEE = CCRow("QWHEE",NN)     

        for n in range(NN):
            self.ccWHEE.append(CheckWHEE(n))  # añade un objeto checkProc con todas las variables necesarias a la listac

#..............................................................................
# import data on link of fuels and equipment

        self.FETFuelMatrix = CheckMatrix("FETFuel",self.FETFuel_i,self.FETFuel_j,Status.FETFuelLink)
        self.FETel_cMatrix = CheckMatrix("FETel_c",[self.FETel_c],self.FETel_c_j,Status.FETelLink)
        self.ElGenMatrix = CheckMatrix("ElGen",[self.ElGen],self.ElGen_j,Status.FETelLink)

#..............................................................................
# import data on link of equipment and pipes

        self.USHMatrix = CheckMatrix("USH",self.USHj,self.USHm,Status.USHLink)   

#..............................................................................
# import data on link of  pipes and processes

        self.UPHMatrix = CheckMatrix("UPHProc",self.UPHProcm,self.UPHProck,Status.UPHLink) 

#..............................................................................
# import data on link of heat exchangers inlet / outlet with equipments, pipes and processes

        self.QWHEqCon = CheckCon("QWHEq-Con",self.QWH,self.QWHEq,Status.QWHEqLink,ambient=True)
        self.QWHPipeCon = CheckCon("QWHPipe-Con",self.QWH,self.QWHPipe,Status.QWHPipeLink,ambient=True)
        self.QWHProcCon = CheckCon("QWHProc-Con",self.QWH,self.QWHProc,Status.QWHProcLink,ambient=True)
        self.QWHEECon = CheckCon("QWHEE-Con",self.QWH,self.QWHEE,Status.QWHEELink,ambient=True)

        self.QHXEqCon = CheckCon("QHXEq-Con",self.QHX,self.QHXEq,Status.QHXEqLink)
        self.QHXPipeCon = CheckCon("QHXPipe-Con",self.QHX,self.QHXPipe,Status.QHXPipeLink)
        self.QHXProcCon = CheckCon("QHXProc-Con",self.QHX,self.QHXProc,Status.QHXProcLink)

#..............................................................................
# import data on existing totals

        self.UPHk = CCRow("UPHk",NK) 
        self.totals = CheckTotals("Totals",self.FECi,self.FETFuel_i,self.USHj,self.UPHk)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def basicCheck(self,matrixCheck = True,continueCheck = False,estimate = False):
#------------------------------------------------------------------------------
#   runs the first basic Check
#   (basic = still without estimation procedures for missing data)
#   continueCheck: continues a check after data estimate, without reloading
#   data from questionnaire ...
#------------------------------------------------------------------------------

        global CHECKMODE

        logTrack("ModuleCC (basicCheck): estimate = %s;continue = %s"%\
                 (estimate,continueCheck))
#        print "ModuleCC (basicCheck): estimate = %s;continue = %s"%\
#                 (estimate,continueCheck)
        
        if DEBUG in ["ALL","BASIC"]:
            logDebug("====================================================")
            logDebug("ModuleCC: getting Test data")
            logDebug("====================================================")
        
        if continueCheck == False and estimate == False:
            self.getQuestionnaireData()

#..............................................................................
# reset the counters of conflicts before starting

        conflict.reset()
        
#..............................................................................
        
        NCycles = 100        #maximum number of cycles
        NBestCycles = 10     #run the first cycles in CHECKMODE = "BEST", the
                            #remaining ones in "MEAN"

        balanceCtrl = 0.1   #initial setting: lagged value of (rel.) imbalance
            
        for ncycle in range(NCycles):

            if ncycle < NBestCycles:
                setCheckMode("BEST")
            else:
                setCheckMode("MEAN")

            cycle.initTotalBalance()

            if estimate == True:
                self.dataEstimate()

            if DEBUG in ["ALL","BASIC","MAIN"]:
                print "===================================================="
                print "ModuleCC: starting cycle no. %s"%(ncycle+1)
                print "===================================================="

#..............................................................................
# Step 1: do an independent checking of all the blocks as initialisation
#         (saves computing time for the start-up of the matrix-algorithm)

#..............................................................................
# check of fuel and electricity consumption (FEC)

            if DEBUG in ["ALL","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking fuels (FET)"
                print "===================================================="

            NI = self.NFET-1
            
            if DEBUG in ["ALL"]:
                print "checking electricity consumption"

            conflict.setDataGroup("Electricity","-")
            
            self.ccFETel.check()
            
            self.FETel_c.update(self.ccFETel.FETel_c)
            self.ElGenera.update(self.ccFETel.ElectricityGen)

            for i in range(NI):       #then check all the Nfuels = NI-1 fuels

                if DEBUG in ["ALL"]:
                    print "checking fuel no. %s"%(i+1)

                conflict.setDataGroup("Fuel",i)
                
                self.ccFET[i].check()
                self.FETFuel_i[i].update(self.ccFET[i].FETFuel)
                self.FECi[i].update(self.ccFET[i].FECFuel)
            
#..............................................................................
# check of equipment

            if DEBUG in ["ALL","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking equipment (USH)"
                print "===================================================="

            NJ = self.NEquipe

            for j in range(NJ):
                if DEBUG in ["ALL"]:
                    print "checking equipment no. %s"%j
                conflict.setDataGroup("Equipment",j+1)

                self.ccEq[j].check()               # ejecuta la función check para equipo j

                self.USHj[j].update(self.ccEq[j].USHj)      #obtain results 
                self.FETj[j].update(self.ccEq[j].FETj)
                self.FETFuel_j[j].update(self.ccEq[j].FETFuel_j)
                
                self.FETel_c_j[j].update(self.ccEq[j].FETel_c_j)
                self.ElGen_j[j].update(self.ccEq[j].ElGen_j)
                
                self.QHXEq[j].update(self.ccEq[j].QHXEq)
                self.QWHEq[j].update(self.ccEq[j].QWHEq)

#..............................................................................
# check of pipes

            if DEBUG in ["ALL","MAIN","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking Pipes (Pipe)"
                print "===================================================="

            NM = self.NPipeDuct

            for m in range(NM):

                conflict.setDataGroup("Pipe/Duct",m+1)

                if DEBUG in ["ALL"]:
                    print "checking pipe no. %s"%m
                self.ccPipe[m].check()               # ejecuta la función check para pipe m


                self.USHm[m].update(self.ccPipe[m].USHm)      #obtain results 
                self.UPHProcm[m].update(self.ccPipe[m].UPHProcm)

                self.QHXPipe[m].update(self.ccPipe[m].QHXPipe) 
                self.QWHPipe[m].update(self.ccPipe[m].QWHPipe) # if necessary change in QWHPipeRec

#..............................................................................
# check of thermal processes

            if DEBUG in ["ALL","MAIN","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking processes (UPH)"
                print "===================================================="

            NK = self.NThProc

            for k in range(self.NThProc):
                if DEBUG in ["ALL"]:
                    print "checking process no. %s"%k
                    
                conflict.setDataGroup("Process",k+1)

                self.ccProc[k].check()             # ejecuta la función check para proceso k

                self.UPHProck[k].update(self.ccProc[k].UPHProc)      #obtain results 
                self.UPHk[k].update(self.ccProc[k].UPH)      #obtain results 

                self.QHXProc[k].update(self.ccProc[k].QHXProc)
                self.QWHProc[k].update(self.ccProc[k].QWHProc)

#..............................................................................
# check of heat exchangers

            if DEBUG in ["ALL","MAIN","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking heat exchangers (QHX)"
                print "===================================================="

            NH = self.NHX

            for h in range(self.NHX):
                if DEBUG in ["ALL"]:
                    print ("checking HX no. %s"%h)
                    
                conflict.setDataGroup("HX",h+1)

                self.ccHX[h].check()             # ejecuta la función check para proceso k

                self.QHX[h].update(self.ccHX[h].QHX)      #obtain results 
                self.QWH[h].update(self.ccHX[h].QWH)      #obtain results 

#..............................................................................
# check of whees

            if DEBUG in ["ALL","MAIN","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking WHEEs (QWHEE)"
                print "===================================================="

            NN = self.NWHEE

            for n in range(self.NWHEE):
                if DEBUG in ["ALL"]:
                    print "checking WHEE no. %s"%n
                conflict.setDataGroup("WHEE",n+1)

                self.ccWHEE[n].check()             # ejecuta la función check para proceso k

                self.QWHEE[n].update(self.ccWHEE[n].QWHEE)      #obtain results 

#..............................................................................
# check of totals

            if DEBUG in ["ALL","MAIN","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking Totals"
                print "===================================================="

            conflict.setDataGroup("Total",0)

            self.totals.check()             # ejecuta la función check para proceso k

#..............................................................................
# Before going to matrix check, assure that there are no data conflicts

            if conflict.nConflicts > 0: break

#..............................................................................
# Step 2: now check the link of all the blocks via the matrix checking function

            if matrixCheck == True:
#..............................................................................
# link of fuels and equipment

                if DEBUG in ["ALL","MAIN","BASIC"]:
                    print "===================================================="
                    print "ModuleCC: checking FET matrix"
                    print "===================================================="

                conflict.setDataGroup("FET","-")

#                self.FETMatrix.check()
                self.FETFuelMatrix.check()
                self.FETel_cMatrix.check()
                self.ElGenMatrix.check()

                self.ccFETel.FETel_c.update(self.FETel_c)
                self.ccFETel.ElectricityGen.update(self.ElGen)
                for i in range(NI):
                    self.ccFET[i].FETFuel.update(self.FETFuel_i[i])

                for j in range(NJ):
#                    self.ccEq[j].FETj.update(self.FETj[j])
                    self.ccEq[j].FETFuel_j.update(self.FETFuel_j[j])
                    self.ccEq[j].FETel_c_j.update(self.FETel_c_j[j])
                    self.ccEq[j].ElGen_j.update(self.ElGen_j[j])

#..............................................................................
# If any matrix conflict appears, break immediately.

                if conflict.nConflicts > 0: break
        
#..............................................................................
# link of equipment and pipes

                if DEBUG in ["ALL","MAIN","BASIC"]:
                    print "===================================================="
                    print "ModuleCC: checking USH matrix"
                    print "===================================================="

                conflict.setDataGroup("USH","-")

                self.USHMatrix.check()

                for j in range(NJ):
                    self.ccEq[j].USHj.update(self.USHj[j])

                for m in range(NM):
                    self.ccPipe[m].USHm.update(self.USHm[m])

#..............................................................................
# If any matrix conflict appears, break immediately.

                if conflict.nConflicts > 0: break
        
#..............................................................................
# link of pipes and processes

                if DEBUG in ["ALL","MAIN","BASIC"]:
                    print "===================================================="
                    print "ModuleCC: checking UPH matrix"
                    print "===================================================="

                conflict.setDataGroup("UPHproc","-")

                self.UPHMatrix.check()

                for m in range(NM):
                    self.ccPipe[m].UPHProcm.update(self.UPHProcm[m])

                for k in range(NK):
                    self.ccProc[k].UPHProc.update(self.UPHProck[k])

#..............................................................................
# If any matrix conflict appears, break immediately.

                if conflict.nConflicts > 0: break
        
#..............................................................................
# Check operating hours of pipes
# Suppositions: (a) minimum hour = minimum hours of connected process with maximum
#               duration
#               (b) maximum hours = hours of industry operation / sum of process

                for m in range(NM):
                    hopdaymax = 0
                    ndaymax = 0
                    hopmin = self.ccPipe[m].HPerYearPipe.valMin
                    for k in range(NK):
                        if Status.UPHLink[k][m] == 1:
                            hopmin = max(self.ccProc[k].HPerYearProc.valMin, hopmin)
                            ndaymax = max(self.ccProc[k].NDaysProc.valMax,ndaymax)
                            hopdaymax += self.ccProc[k].HPerDayProc.valMax
                            
                    hopdaymax = min(24.0,hopdaymax)
                    ndaymax = min(365.,ndaymax)
                    hopmax = ndaymax*hopdaymax

                    self.ccPipe[m].HPerYearPipe.valMin = max(self.ccPipe[m].HPerYearPipe.valMin, hopmin)
                    self.ccPipe[m].HPerYearPipe.valMax = min(self.ccPipe[m].HPerYearPipe.valMax, hopmax)
                    self.ccPipe[m].HPerYearPipe.val = 0.5*(self.ccPipe[m].HPerYearPipe.valMin + self.ccPipe[m].HPerYearPipe.valMax)
                    self.ccPipe[m].HPerYearPipe.constrain()

#..............................................................................
# link of heat exchanger with the rest

                if DEBUG in ["ALL","MAIN","BASIC"]:
                    print "===================================================="
                    print "ModuleCC: checking Heat exchanger connections"
                    print "===================================================="

                conflict.setDataGroup("QHWEq","-")
                self.QWHEqCon.check()

                conflict.setDataGroup("QHWPipe","-")
                self.QWHPipeCon.check()

                conflict.setDataGroup("QHWProc","-")
                self.QWHProcCon.check()

                conflict.setDataGroup("QWHEE","-")
                self.QWHEECon.check()

                conflict.setDataGroup("QHXEq","-")
                self.QHXEqCon.check()

                conflict.setDataGroup("QHXPipe","-")
                self.QHXPipeCon.check()

                conflict.setDataGroup("QHXProc","-")
                self.QHXProcCon.check()

                for j in range(NJ):
                  
                    self.ccEq[j].QHXEq.update(self.QHXEq[j])
                    self.ccEq[j].QWHEq.update(self.QWHEq[j])

                for m in range(NM):
                    self.ccPipe[m].QHXPipe.update(self.QHXPipe[m])
                    self.ccPipe[m].QWHPipe.update(self.QWHPipe[m]) #to be changed in QWHPipeRec if necessary

                for k in range(NK):
                    
                    self.ccProc[k].QHXProc.update(self.QHXProc[k])
                    self.ccProc[k].QWHProc.update(self.QWHProc[k])

                for n in range(NN):
                    self.ccWHEE[n].QWHEE.update(self.QWHEE[n])

                for h in range(NH):
                    self.ccHX[h].QWH.update(self.QWH[h])
                    self.ccHX[h].QHX.update(self.QHX[h])

#..............................................................................
# If any matrix conflict appears, break immediately.

                if conflict.nConflicts > 0: break
        
#..............................................................................
# END OF CYCLE: check convergence

            balanceCtrl = balanceCtrl + 0.5*(cycle.getMeanTotalBalance()-balanceCtrl)
            if DEBUG in ["ALL","MAIN","BASIC"]:
                print "GLOBAL CYCLE CONVERGENCE: %s [lagged: %s]| %s "%\
                      (cycle.getMeanTotalBalance(),balanceCtrl,\
                       cycle.getMaxTotalBalance())

            if ncycle%1 == 0 or balanceCtrl <= 1.e-3:
                logMessage("Consistency check: maximum remaining balance error %6.2f percent"%(balanceCtrl*100))

            if balanceCtrl <= 1.e-3:
                logTrack("ModuleCC (basic check): convergence reached at %s cycles"%(ncycle+1))
                break

            if ncycle == NCycles-1 and balanceCtrl > 5.e-3:
                logTrack("Consistency check calculations did not converge. Data may not be fully balanced")
#                showWarning("Consistency check calculations did not converge. Data may not be fully balanced")

            
#..............................................................................
# At the end of the checking, screen the modules

        self.selectMainProcesses()

        screen.reset()

        screen.setDataGroup("FETel",0)
        self.ccFETel.screen()
        
        for i in range(NI):       #then check all the Nfuels = NI-1 fuels
            screen.setDataGroup("FET",i+1)
            self.ccFET[i].screen()
        for j in range(NJ):       
            screen.setDataGroup("Eq.",j+1)
            self.ccEq[j].screen()
        for k in range(NK):       
            screen.setDataGroup("Proc.",k+1)
            self.ccProc[k].screen()
        for m in range(NM):      
            screen.setDataGroup("Pipe",m+1)
            self.ccPipe[m].screen()
        for h in range(NH):       
            screen.setDataGroup("HX",h+1)
            self.ccHX[h].screen()       
        for n in range(NN):       
            screen.setDataGroup("WHEE",n+1)
            self.ccWHEE[n].screen()

        screen.setDataGroup("Totals",0)
        self.totals.screen()
            
        if DEBUG in ["ALL","MAIN","BASIC"]:
            screen.show()
            conflict.show()

#..............................................................................
# And finally export all the data

        logTrack("ModuleCC (basicCheck): exporting results to SQL")
#        print NI,NJ,NK,NM,NH,NN
        
        self.ccFETel.exportData()
        for i in range(NI):       #then check all the Nfuels = NI-1 fuels
            self.ccFET[i].exportData()
        for j in range(NJ):       
            self.ccEq[j].exportData()
        for k in range(NK):       
            self.ccProc[k].exportData()
        for m in range(NM):
#            print "ModuleCC (basicCheck): exporting pipe %s data"%(m+1)
            self.ccPipe[m].exportData()
        for h in range(NH):       
            self.ccHX[h].exportData()
        for n in range(NN):       
            self.ccWHEE[n].exportData()

        self.totals.exportData()

        return conflict.nConflicts

#==============================================================================
#------------------------------------------------------------------------------
    def dataEstimate(self):
#------------------------------------------------------------------------------
#   calls the functions "estimate()" of all the checkers ...
#------------------------------------------------------------------------------

#       self.ccFETel.estimate()
        NI = self.NFET-1
        for i in range(NI):       #then check all the Nfuels = NI-1 fuels
#            self.ccFET[i].estimate()
            pass
        screen.setDataGroup("FETel",0)
        self.ccFETel.estimate() #for the moment estimate implemented only in
                                    #FETel as an example
        
        NJ = self.NEquipe
        for j in range(NJ):       
            self.ccEq[j].estimate()
        
        NK = self.NThProc
        for k in range(NK):       
            screen.setDataGroup("Proc.",k+1)
            self.ccProc[k].estimate()

        NM = self.NPipeDuct
        for m in range(NM):      
#                self.ccPipe[m].estimate()
            pass

        NH = self.NHX
        for h in range(NH):       
#            self.ccHX[h].estimate()
            pass

        NN = self.NWHEE
        for n in range(NN):       
#            self.ccWHEE[n].estimate()
            pass


#------------------------------------------------------------------------------
    def selectMainProcesses(self):
#------------------------------------------------------------------------------
#   decides which of the processes are the most relevant ones
#------------------------------------------------------------------------------

        UPHTotal = self.totals.UPH
        if UPHTotal.val is None:
            f_Ok = 0.0
            f_Ok_min = 0.0
            return

        NK = self.NThProc
        
        UPH = CCRow("UPHk",NK)

        UPH_Ok = 0
        UPH_Ok_min = 0
        UPH_Ok_max = 0
        
        UPH_None = 0

        procList = []
        for k in range(NK):
            UPH[k] = self.ccProc[k].UPH

            if UPH[k].sqerr < MAX_SQERR:
                UPH_Ok += UPH[k].val
                UPH_Ok_min += UPH[k].valMin
                UPH_Ok_max += UPH[k].valMax
                procList.append((UPH[k].valMax,UPH[k].val,k))
            else:
                if UPH[k].val is not None:
                    UPH_None += UPH[k].val
                    procList.append((UPH[k].valMax,UPH[k].val,k))
                else:
                    UPH_None += UPH[k].valMax
                    procList.append((UPH[k].valMax,UPH[k].valMax,k))
            
        if UPHTotal.val > 0:
            f_Ok = UPH_Ok/UPHTotal.val
            f_Ok_min = UPH_Ok_min/UPHTotal.val
        else:
            f_Ok = 1.0
            f_Ok_min = 1.0
#        print "ModuleCC (selectMainProcesses): fraction of processes with desired accuracy on\n total heat demand = %s (%s)"%(f_Ok,f_Ok_min)

#..............................................................................
# sorts the processes by UPH
# while SUM(UPH_estimated) < 30% of estimated Total (sum of the smallest) or
#       SUM(UPH_maximum)   < 40% of estimated Total , those processes are
# considered as secondary processes.

        UPH_Sum = 0
        UPHMax_Sum = 0
        mainProcess = False
        
        procList.sort()
        for proc in procList:
            
            UPHMax_Sum += proc[0]
            UPH_Sum += proc[1]
            k = proc[2]
#            print "ModuleCC (selectMainProcesses): k %s UPH_Sum %s UPHMax_Sum %s:"%(k,UPH_Sum,UPHMax_Sum)
            if (UPH_Sum > 0.3*UPHTotal.val) or \
               (UPHMax_Sum > 0.4*UPHTotal.val):
                mainProcess = True

            self.ccProc[k].definePriority(mainProcess)
            
#------------------------------------------------------------------------------
#==============================================================================
#==============================================================================
#==============================================================================
if __name__ == "__main__":

# direct connecting to SQL database w/o GUI. for testing only
    stat = Status("testModuleCC")
    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    Status.PId = 2
    Status.ANo = 0

#..............................................................................
    
    CC = ModuleCC()       # creates an instance of class CCheck
    CC.basicCheck()
