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
#	Version No.: 0.02
#	Created by:         Claudia Vannoni     20/04/2008
#                           Claudia Vannoni     2/05/2008
#
#       Changes to previous version:
#	v0.02 CV Add CCPipe, Add Matrix and links between matrix
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

from checkMatrix import *
from checkProc import *
from checkEq import *
from checkFETfuel import *
from checkFETel import *
from checkPipe import *
from checkTotals import *

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

        print "ModuleCC (updatePanel): screening with priority ",self.screen_priority        
        CCList = []
        nMissingVarsOfPriority=0
        for entry in CCScreen.screenList:
            if entry[4] <= self.screen_priority:

                if entry[4] == 1:
                    action = "Calculations w/o this are nonsense !!!"
                elif entry[4] == 2:
                    action = "Value required for detail analysis !!!"
                else:
                    action = "not strictly necessary"
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
        print "ModuleCC: setting priority level to ",level
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
        self.NFET = 0
        
        self.ccEq = []
        self.NEquipe = 0
        
        self.ccProc = []
        self.NProc = 0

        self.ccPipe = []
        self.NPipeDuct = 0 

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


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def basicCheck(self,matrixCheck = True):
#------------------------------------------------------------------------------
#   runs the first basic Check
#   (basic = still without estimation procedures for missing data)
#------------------------------------------------------------------------------

#        cycle = Status.cycle.initCycle()
#        while not cycle.converged():

        if DEBUG in ["ALL","BASIC"]:
            print "===================================================="
            print "ModuleCC: getting Test data"
            print "===================================================="
        
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

                for m in range(1,NM):
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

                for k in range(1,NK):
                    self.ccProc[k].UPHProc.update(self.UPHProck[k])

#..............................................................................
# If any matrix conflict appears, break immediately.

                if conflict.nConflicts > 0: break
        
#..............................................................................
# At the end of the checking, screen the modules

        screen.reset()

        for i in range(0,NI):       #then check all the Nfuels = NI-1 fuels
            screen.setDataGroup("Fuel",i)
            self.ccFET[i].screen()
        for j in range(0,NJ):       
            screen.setDataGroup("Eq.",j+1)
            self.ccEq[j].screen()
        for k in range(0,NK):       
            screen.setDataGroup("Proc.",k+1)
            self.ccProc[k].screen()

        if VERSION != "M2_DEMO":
            for m in range(0,NM):      
                screen.setDataGroup("Pipe",m+1)
                self.ccPipe[m].screen()

        screen.setDataGroup("Totals",0)
        self.totals.screen()
            
        if DEBUG in ["ALL","MAIN","BASIC"]:
            screen.show()
            conflict.show()

#..............................................................................
# And finally export all the data

        for i in range(0,NI):       #then check all the Nfuels = NI-1 fuels
            self.ccFET[i].exportData()
        for j in range(0,NJ):       
            self.ccEq[j].exportData()
        for k in range(0,NK):       
            screen.setDataGroup("Proc.",k+1)
            self.ccProc[k].exportData()

        if VERSION != "M2_DEMO":
            for m in range(0,NM):      
                screen.setDataGroup("Pipe",m+1)
                self.ccPipe[m].exportData()
        self.totals.exportData()

        return conflict.nConflicts

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
