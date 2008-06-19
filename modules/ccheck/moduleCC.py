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
#	Version No.: 0.03
#	Created by:         Claudia Vannoni     20/04/2008
#                           Claudia Vannoni     02/05/2008
#                           Hans Schweiger      13/06/2008
#
#       Changes to previous version:
#	v0.02 CV Add CCPipe, Add Matrix and links between matrix
#       13/06/2008 HS   Connections between sub-systems imported from SQL
#                       Very basic version of CheckHX added. Not yet coupled
#                       to the rest.
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

from sys import *
from math import *
from numpy import *

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP
from einstein.modules.messageLogger import *

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

        self.updatePanel()
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#   function that updates the information on the CC panel on the GUI
#------------------------------------------------------------------------------

#..............................................................................
# export screening data

        format_percentage = '%3.2f'

        logDebug("ModuleCC (updatePanel): screening with priority %s"%self.screen_priority)       
        CCList = []
        nMissingVarsOfPriority=0
        for entry in CCScreen.screenList:
            if entry[4] <= self.screen_priority:

                if entry[4] == 1:
                    action = _("Calculations w/o this are nonsense !!!")
                elif entry[4] == 2:
                    action = _("Value required for detail analysis !!!")
                else:
                    action = _("not strictly necessary")
                row = [entry[0]+"["+entry[3]+"]",
                       "here should be the description",
                       entry[1],
                       entry[2]+"%",
                       action]
                CCList.append(noneFilter(row))
                nMissingVarsOfPriority+=1

        if nMissingVarsOfPriority==0:
            CCList.append(["","","","",""])
            
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

                row0 = [str(entry[2])+"<>"+str(entry[6]),entry[10],""]

                origin1 = ""
                for parname in entry[3]:
                    origin1 = origin1 + str(parname) + "; "

                row1 = ["%10.4f"%entry[4],
                        "+/- "+"%5.3f"%entry[5]+"%",
                        origin1]

                origin2 = ""
                for parname in entry[7]:
                    origin2 = origin2 + str(parname) + "; "

                row2 = ["%10.4f"%entry[8],
                        "+/- "+"%5.3f"%entry[9]+"%",
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
        logDebug("ModuleCC: setting priority level to "%level)
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

        if Status.UserInteractionLevel == "automatic":
            #predefined testCase. to be eliminated once the general case works well

            logDebug("ModuleCC (getQuestionnaireData): running in fix test-case-mode")

#..............................................................................
# import data on fuel and electricity consumption (FET)

            self.NFET = 2
            NI = self.NFET
            self.FETi = CCRow("FETi",NI)

            self.ccFET.append(CheckFETel())     
            for i in range(1,NI):      
                self.ccFET.append(CheckFETfuel(i))

#..............................................................................
# import data on existing equipment 

            self.NEquipe = 2
            NJ = self.NEquipe
            self.USHj = CCRow("USHj",NJ)     #note: this is a ROW of USH values, and not identical with the USHj variable within checkEq !!!
            self.FETj = CCRow("FETj",NJ)     #creates the space for intermediate storge towards matrix

            for j in range(NJ):
                self.ccEq.append(CheckEq(j))     # añade un objeto checkEq con todas las variables necesarias a la lista

#..............................................................................
# import data on existing processes

            self.NThProc = 3
            NK = self.NThProc
            self.UPHProck = CCRow("UPHProck",NK)     #note: this is a ROW of USH values, and not identical with the USHj variable within checkEq !!!
            self.QHXk = CCRow("QHXk",NK)     #creates the space for intermediate storge towards matrix

            for k in range(NK):
                self.ccProc.append(CheckProc(k))  # añade un objeto checkProc con todas las variables necesarias a la listac


#..............................................................................
# import data on existing pipeducts

            self.NPipeDuct = 3
            NM = self.NPipeDuct
            self.UPHProcm = CCRow("UPHProcm",NM)     #note: this is a ROW of USH values, and not identical with the USHj variable within checkEq !!!
            self.QHXPipe = CCRow("QHXPipe",NM)          #creates the space for intermediate storge towards matrix
            self.USHm = CCRow("USHm",NM) 

            for m in range(NM):
                self.ccPipe.append(CheckPipe(m))  # añade un objeto checkProc con todas las variables necesarias a la listac

#..............................................................................
# import data on link of fuels and equipment

            FETLink = arange(NI*NJ).reshape(NJ,NI)  # reshape(rows,cols)
            
            FETLink[0][0] = 0
            FETLink[1][0] = 0
            FETLink[0][1] = 1
            FETLink[1][1] = 1

            self.FETMatrix = CheckMatrix("FET Matrix",self.FETi,self.FETj,FETLink)

#..............................................................................
# import data on link of equipment and pipes

            USHLink = arange(NJ*NM).reshape(NM,NJ)  # reshape(rows,cols)

            USHLink[0][0] = 1
            USHLink[1][0] = 0
            USHLink[2][0] = 0
            USHLink[0][1] = 1
            USHLink[1][1] = 1
            USHLink[2][1] = 1

            self.USHMatrix = CheckMatrix("USH Matrix",self.USHj,self.USHm,USHLink)   


#..............................................................................
# import data on link of  pipes and processes

            UPHLink = arange(NM*NK).reshape(NK,NM)  # reshape(rows,cols)

            UPHLink[0][0] = 1
            UPHLink[1][0] = 0
            UPHLink[2][0] = 0
            UPHLink[0][1] = 0
            UPHLink[1][1] = 1
            UPHLink[2][1] = 0
            UPHLink[0][2] = 0
            UPHLink[1][2] = 0
            UPHLink[2][2] = 1

            self.UPHMatrix = CheckMatrix("UPH Matrix",self.UPHProcm,self.UPHProck,UPHLink) 

#..............................................................................
# import data on existing totals

            self.UPHk = CCRow("UPHk",NK) 
            self.totals = CheckTotals("Totals",self.FETi,self.USHj,self.UPHk) # añade un objeto checkProc con todas las variables necesarias a la listac

        else:
            # general case: uses the information from the SQL
            # eliminate "else" and raise one level once this is the only option

            logDebug("ModuleCC (getQuestionnaireData): running in new general mode (import connections from SQL)")

#..............................................................................
# import data on link of fuels and equipment

            getConnections()

#..............................................................................
# import data on fuel and electricity consumption (FET)

            self.NFET = Status.NFET
            NI = self.NFET
            self.FETi = CCRow("FETi",NI)

            self.ccFET.append(CheckFETel())     
            for i in range(1,NI):      
                self.ccFET.append(CheckFETfuel(i))

#..............................................................................
# import data on existing equipment 

            self.NEquipe = Status.NEquipe
            NJ = self.NEquipe
            self.USHj = CCRow("USHj",NJ)     #note: this is a ROW of USH values, and not identical with the USHj variable within checkEq !!!
            self.FETj = CCRow("FETj",NJ)     #creates the space for intermediate storge towards matrix
            self.QHXEq = CCRow("QHXEq",NJ)      # incoming waste heat from heat recovery
            self.QWHEq = CCRow("QWHEq",NJ)    # outgoing waste heat to be recovered

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

            self.FETMatrix = CheckMatrix("FET Matrix",self.FETi,self.FETj,Status.FETLink)

#..............................................................................
# import data on link of equipment and pipes

            self.USHMatrix = CheckMatrix("USH Matrix",self.USHj,self.USHm,Status.USHLink)   

#..............................................................................
# import data on link of  pipes and processes

            self.UPHMatrix = CheckMatrix("UPH Matrix",self.UPHProcm,self.UPHProck,Status.UPHLink) 

#..............................................................................
# import data on link of heat exchangers inlet / outlet with equipments, pipes and processes

            self.QWHEqCon = CheckCon("QWHEq Con",self.QWH,self.QWHEq,Status.QWHEqLink)
            self.QWHPipeCon = CheckCon("QWHPipe Con",self.QWH,self.QWHPipe,Status.QWHPipeLink)
            self.QWHProcCon = CheckCon("QWHProc Con",self.QWH,self.QWHProc,Status.QWHProcLink)
            self.QWHEECon = CheckCon("QWHEE Con",self.QWH,self.QWHEE,Status.QWHEELink)

            self.QHXEqCon = CheckCon("QWHEq Con",self.QHX,self.QHXEq,Status.QHXEqLink)
            self.QHXPipeCon = CheckCon("QWHPipe Con",self.QHX,self.QHXPipe,Status.QHXPipeLink)
            self.QHXProcCon = CheckCon("QWHProc Con",self.QHX,self.QHXProc,Status.QHXProcLink)

#..............................................................................
# import data on existing totals

            self.UPHk = CCRow("UPHk",NK) 
            self.totals = CheckTotals("Totals",self.FETi,self.USHj,self.UPHk) # añade un objeto checkProc con todas las variables necesarias a la listac


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def basicCheck(self,matrixCheck = True,continueCheck = False):
#------------------------------------------------------------------------------
#   runs the first basic Check
#   (basic = still without estimation procedures for missing data)
#   continueCheck: continues a check after data estimate, without reloading
#   data from questionnaire ...
#------------------------------------------------------------------------------

#        cycle = Status.cycle.initCycle()
#        while not cycle.converged():

        if DEBUG in ["ALL","BASIC"]:
            logDebug("====================================================")
            logDebug("ModuleCC: getting Test data")
            logDebug("====================================================")
        
        if continueCheck == False:
            self.getQuestionnaireData()

#..............................................................................
# reset the counters of conflicts before starting

        conflict.reset()
        
#..............................................................................
        if DEBUG in ["ALL","BASIC"]:
            print "===================================================="
            print "ModuleCC: starting cycle"
            print "===================================================="
        
        NCycles = 10
        for cycle in range(NCycles):
#..............................................................................
# Step 1: do an independent checking of all the blocks as initialisation
#         (saves computing time for the start-up of the matrix-algorithm)

#..............................................................................
# check of fuel and electricity consumption (FEC)

            if DEBUG in ["ALL","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking fuels (FET)"
                print "===================================================="

            NI = self.NFET
            
            print "checking electricity consumption"
            conflict.setDataGroup("Electricity","-")
            
            self.ccFET[0].check()
            self.FETi[0].update(self.ccFET[0].FETel)

            for i in range(1,NI):       #then check all the Nfuels = NI-1 fuels

                print "checking fuel no. %s"%i
                conflict.setDataGroup("Fuel",i)

                self.ccFET[i].check()
                self.FETi[i].update(self.ccFET[i].FETFuel)
            
#..............................................................................
# check of equipment

            if DEBUG in ["ALL","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking equipment (USH)"
                print "===================================================="

            NJ = self.NEquipe

            for j in range(NJ):
                print "checking equipment no. %s"%j
                conflict.setDataGroup("Equipment",j+1)

                self.ccEq[j].check()               # ejecuta la función check para equipo j

                self.USHj[j].update(self.ccEq[j].USHj)      #obtain results 
                self.FETj[j].update(self.ccEq[j].FETj)
# here data should be passed to the correspoinding inputs in CheckEq
#               self.QHXEq[j].update(self.ccEq[j].QHXEqRec)
#               self.QWHEq[j].update(self.ccEq[j].QWHEqRec)

#..............................................................................
# check of pipes

            if DEBUG in ["ALL","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking Pipes (Pipe)"
                print "===================================================="

            NM = self.NPipeDuct

            for m in range(NM):

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#   PIPE CHECK TEMPORARILY DEACTIVATED FOR DEMO
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                
                if VERSION=="M2_DEMO":
                    ccheck1(self.USHm[m],self.UPHProcm[m]) #just set 0 losses, UPH=USH
                    print "M2_DEMO SHORT CUT===================="
                    self.USHm[m].show()
                    self.UPHProcm[m].show()
                    
                else:
                    conflict.setDataGroup("Pipe/Duct",m+1)

                    print "checking pipe no. %s"%m
                    self.ccPipe[m].check()               # ejecuta la función check para pipe m


                    self.USHm[m].update(self.ccPipe[m].USHm)      #obtain results 
                    self.UPHProcm[m].update(self.ccPipe[m].UPHProcm)
# here data should be passed to the correspoinding inputs in CheckPipe
#                   self.QHXPipe[m].update(self.ccPipe[m].QHXPipeRec)
#                   self.QWHPipe[m].update(self.ccPipe[m].QWHPipeRec)

#..............................................................................
# check of thermal processes

            if DEBUG in ["ALL","MAIN","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking processes (UPH)"
                print "===================================================="

            NK = self.NThProc

            for k in range(self.NThProc):
                print "checking process no. %s"%k
                conflict.setDataGroup("Process",k+1)

                self.ccProc[k].check()             # ejecuta la función check para proceso k

                self.UPHProck[k].update(self.ccProc[k].UPHProc)      #obtain results 
                self.UPHk[k].update(self.ccProc[k].UPH)      #obtain results 

# here data should be passed to the correspoinding inputs in CheckProc
#               self.QHXProc[k].update(self.ccProc[k].QHXProcRec)
#               self.QWHProc[k].update(self.ccProc[k].QWHProcRec)

#..............................................................................
# check of heat exchangers

            if DEBUG in ["ALL","MAIN","BASIC"]:
                print "===================================================="
                print "ModuleCC: checking heat exchangers (QHX)"
                print "===================================================="

            NH = self.NHX

            for h in range(self.NHX):
                logDebug("checking HX no. %s"%h)
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
                print "checking WHEE no. %s"%n
                conflict.setDataGroup("WHEE",n+1)

                self.ccWHEE[n].check()             # ejecuta la función check para proceso k

                self.QWHEE[n].update(self.ccWHEE[n].QWHEERec)      #obtain results 

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

                conflict.setDataGroup("FET matrix","-")

                self.FETMatrix.check()

                self.ccFET[0].FETel.update(self.FETi[0])
                for i in range(1,NI):
                    self.ccFET[i].FETFuel.update(self.FETi[i])

                for j in range(NJ):
                    self.ccEq[j].FETj.update(self.FETj[j])

#..............................................................................
# If any matrix conflict appears, break immediately.

                if conflict.nConflicts > 0: break
        
#..............................................................................
# link of equipment and pipes

                if DEBUG in ["ALL","MAIN","BASIC"]:
                    print "===================================================="
                    print "ModuleCC: checking USH matrix"
                    print "===================================================="

                conflict.setDataGroup("USH matrix","-")

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

                conflict.setDataGroup("UPH matrix","-")

                self.UPHMatrix.check()

                for m in range(NM):
                    self.ccPipe[m].UPHProcm.update(self.UPHProcm[m])

                for k in range(NK):
                    self.ccProc[k].UPHProc.update(self.UPHProck[k])

#..............................................................................
# If any matrix conflict appears, break immediately.

                if conflict.nConflicts > 0: break
        
#..............................................................................
# link of heat exchanger with the rest

                if DEBUG in ["ALL","MAIN","BASIC"]:
                    print "===================================================="
                    print "ModuleCC: checking Heat exchanger connections"
                    print "===================================================="

                conflict.setDataGroup("QHWEq Con","-")
                self.QWHEqCon.check()

                conflict.setDataGroup("QHWPipe Con","-")
                self.QWHPipeCon.check()

                conflict.setDataGroup("QHWProc Con","-")
                self.QWHProcCon.check()

                conflict.setDataGroup("QWHEE Con","-")
                self.QWHEECon.check()

                conflict.setDataGroup("QHXEq Con","-")
                self.QHXEqCon.check()

                conflict.setDataGroup("QHXPipe Con","-")
                self.QHXPipeCon.check()

                conflict.setDataGroup("QHXProc Con","-")
                self.QHXProcCon.check()

                for j in range(NJ):
                    pass
# here data should be passed to the correspoinding inputs in CheckEq
#                    self.ccEq[j].QHXEqRec.update(self.QHXEq[j])
#                    self.ccEq[j].QWHEqRec.update(self.QWHEq[j])

                for m in range(NM):
                    pass
# here data should be passed to the correspoinding inputs in CheckPipe
#                    self.ccPipe[m].QHXPipeRec.update(self.QHXPipe[m])
#                    self.ccPipe[m].QWHPipeRec.update(self.QWHPipe[m])

                for k in range(NK):
                    pass
# here data should be passed to the correspoinding inputs in CheckEq
#                    self.ccProc[k].QHXProcRec.update(self.QHXProc[k])
#                    self.ccProc[k].QWHProcRec.update(self.QWHProc[k])

                for n in range(NN):
                    self.ccWHEE[n].QWHEERec.update(self.QWHEE[n])

                for h in range(NH):
                    self.ccHX[h].QWH.update(self.QWH[h])
                    self.ccHX[h].QHX.update(self.QHX[h])

# here data should be passed to the correspoinding inputs in CheckEq
#                    self.ccProc[k].QHXProcRec.update(self.QHXProc[k])
#                    self.ccProc[k].QWHProcRec.update(self.QWHProc[k])


#..............................................................................
# If any matrix conflict appears, break immediately.

                if conflict.nConflicts > 0: break
        
#..............................................................................
# At the end of the checking, screen the modules

        screen.reset()

        for i in range(NI):       #then check all the Nfuels = NI-1 fuels
            screen.setDataGroup("Fuel",i)
            self.ccFET[i].screen()
        for j in range(NJ):       
            screen.setDataGroup("Eq.",j+1)
            self.ccEq[j].screen()
        for k in range(NK):       
            screen.setDataGroup("Proc.",k+1)
            self.ccProc[k].screen()

        if VERSION != "M2_DEMO":
            for m in range(NM):      
                screen.setDataGroup("Pipe",m+1)
                self.ccPipe[m].screen()

        for h in range(NH):       
            screen.setDataGroup("HX",h+1)
            self.ccHX[h].screen()
        
        screen.setDataGroup("Totals",0)
        self.totals.screen()
            
        if DEBUG in ["ALL","MAIN","BASIC"]:
            screen.show()
            conflict.show()

#..............................................................................
# And finally export all the data

        for i in range(NI):       #then check all the Nfuels = NI-1 fuels
            self.ccFET[i].exportData()
        for j in range(NJ):       
            self.ccEq[j].exportData()
        for k in range(NK):       
            self.ccProc[k].exportData()

        if VERSION != "M2_DEMO":
            for m in range(0,NM):      
                self.ccPipe[m].exportData()

        for h in range(NH):       
            self.ccHX[h].exportData()

        self.totals.exportData()

        return conflict.nConflicts

#==============================================================================
#------------------------------------------------------------------------------
    def dataEstimate(self):
#------------------------------------------------------------------------------
#   calls the functions "estimate()" of all the checkers ...
#------------------------------------------------------------------------------

        for i in range(NI):       #then check all the Nfuels = NI-1 fuels
#            self.ccFET[i].estimate()
            pass
        self.ccFET[0].estimate() #for the moment estimate implemented only in
                                    #FETel as an example
        
        for j in range(NJ):       
#            self.ccEq[j].estimate()
            pass
        
        for k in range(NK):       
#            self.ccProc[k].estimate()
            pass

        if VERSION != "M2_DEMO":
            for m in range(NM):      
#                self.ccPipe[m].estimate()
                pass

        for h in range(NH):       
#            self.ccHX[h].estimate()
            pass
        self.basicCheck(continueCheck = True)

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
