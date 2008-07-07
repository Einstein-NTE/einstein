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
#	PROCESSES
#			
#------------------------------------------------------------------------------
#			
#	Functions for calculation and temperature decomposition of
#       process heat demands
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	07/05/2008
#	Revised by:         ---
#
#       Changes in last update:
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

from math import *
from einstein.auxiliary.auxiliary import *
from einstein.modules.constants import *
from einstein.GUI.status import Status
from einstein.modules.messageLogger import *


#------------------------------------------------------------------------------		
class Processes(object):
#------------------------------------------------------------------------------		
#   Module that handles all project schedules
#------------------------------------------------------------------------------		
    
#------------------------------------------------------------------------------		
    def __init__(self):
#------------------------------------------------------------------------------		
        pass
       
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def createYearlyDemand(self):
#------------------------------------------------------------------------------		
#       is created automatically in an alternative after cchecking or
#       after selecting a new alternative that is already cchecked
#------------------------------------------------------------------------------		

        logTrack("Processes (createYearlyDemand): starting")
        
        (projectData,generalData) = Status.prj.getProjectData()

        processes = Status.prj.getProcesses()

        UPH_T = []
        UPHs_T = []
        UPHm_T = []
        UPHc_T = []
        UPHw_T = []
        UPHTotal_T = Status.int.createQ_T()
        UPHwTotal_T = Status.int.createQ_T()

        for process in processes:

            UPH_T.append(Status.int.createQ_T())
            UPHc_T.append(Status.int.createQ_T())
            UPHm_T.append(Status.int.createQ_T())
            UPHs_T.append(Status.int.createQ_T())
            UPHw_T.append(Status.int.createQ_T())

            k = process.ProcNo - 1

            UPHc = checkLimits(process.UPHc,0.0,INFINITE,0.0)
            distUPHc = self.createTempDist(process.PT,T0=process.PTInFlowRec)
            
            UPHm = checkLimits(process.UPHm,0.0,INFINITE,0.0)
            distUPHm = self.createTempDist(process.PT)

            UPHs = checkLimits(process.UPHs,0.0,INFINITE,0.0)
            distUPHs = self.createTempDist(process.PT,T0=process.PTStartUp)

            UPHw = checkLimits(process.UPHw,0.0,INFINITE,0.0)
            distUPHw = self.createInvTempDist(process.PTOutFlowRec,T0=process.PTFinal)

            NT = Status.NT

            for iT in range(NT+2): #NT + 1 + 1 -> additional value for T > Tmax
                UPHc_T[k][iT] = UPHc*distUPHc[iT]
                UPHm_T[k][iT] = UPHm*distUPHm[iT]
                UPHs_T[k][iT] = UPHs*distUPHs[iT]
                UPH_T[k][iT] = UPHc_T[k][iT] + UPHm_T[k][iT] + UPHs_T[k][iT]
                UPHw_T[k][iT] = UPHw*distUPHw[iT]
                UPHTotal_T[iT] += UPH_T[k][iT]
                UPHwTotal_T[iT] += UPHw_T[k][iT]
                 
        Status.int.UPH_T = UPH_T   
        Status.int.UPHc_T = UPHc_T   
        Status.int.UPHm_T = UPHm_T   
        Status.int.UPHs_T = UPHs_T   
        Status.int.UPHw_T = UPHw_T
        Status.int.UPHTotal_T = UPHTotal_T
        Status.int.UPHwTotal_T = UPHwTotal_T

        logMessage("Processes (createYearlyDemand): yearly heat demand = %s yearly waste heat availability = %s"%\
              (Status.int.UPHTotal_T[NT+1],Status.int.UPHwTotal_T[0]))

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def createAggregateDemand(self):
#------------------------------------------------------------------------------		

        logMessage(_("Processes (createAggregateDemand): Creating time and temperature dependent heat demand"))
        
        (projectData,generalData) = Status.prj.getProjectData()
        Status.HPerDayInd = projectData.HPerDayInd

        if Status.processData.outOfDate == False:
            logTrack("Processes (createAggregateDemand): WARNING - someone wants to create demand profile which is already up to date")

        if Status.schedules.outOfDate == True:
            logMessage("Processes (createAggregateDemand): creating process schedules")
            Status.schedules.create()

        processes = Status.prj.getProcesses()

        UPH_Tt = []
        UPHw_Tt =[]

        UPHTotal_Tt = Status.int.createQ_Tt()
        UPHwTotal_Tt = Status.int.createQ_Tt()

        for process in processes:
            k = process.ProcNo - 1

            UPH_Tt.append(Status.int.createQ_Tt())
            UPHw_Tt.append(Status.int.createQ_Tt())
            
            scheduleC = Status.schedules.procInFlowSchedules[k]
            scheduleM = Status.schedules.procOpSchedules[k]
            scheduleS = Status.schedules.procStartUpSchedules[k]
            scheduleW = Status.schedules.procOutFlowSchedules[k]

            print "Processes: schedule = ",scheduleW.fav
            print "Processes: UPHw_T[k] = ",Status.int.UPHw_T[k]
            
            distUPHw = self.createInvTempDist(process.PTOutFlowRec,T0=process.PTFinal)

            NT = Status.NT
            Nt = Status.Nt

            for it in range(Nt):
                time = Status.TimeStep*it
                fC = scheduleC.fav[it]
                fM = scheduleM.fav[it]
                fS = scheduleS.fav[it]
                fW = scheduleW.fav[it]

                for iT in range(NT+2): #NT + 1 + 1 -> additional value for T > Tmax
                    UPH_Tt[k][iT][it] = Status.int.UPHc_T[k][iT]*fC +\
                                        Status.int.UPHm_T[k][iT]*fM +\
                                        Status.int.UPHs_T[k][iT]*fS
                    UPHw_Tt[k][iT][it] = Status.int.UPHw_T[k][iT]*fW

                    UPHTotal_Tt[iT][it] += UPH_Tt[k][iT][it]
                    UPHwTotal_Tt[iT][it] += UPHw_Tt[k][iT][it]

            print "Processes: UPHwTotal = ",UPHwTotal_Tt[Status.NT+1]
                 
        Status.int.UPH_Tt = UPH_Tt    
        Status.int.UPHw_Tt = UPHw_Tt

        Status.int.UPHTotal_Tt = UPHTotal_Tt    
        Status.int.UPHwTotal_Tt = UPHwTotal_Tt
                           
#..............................................................................
# set status-flag (required BEFORE call to runHRModule !!!)

        Status.int.cascadeUpdateLevel = 0 #indicates that demand profile is created !!!
        Status.processData.outOfDate = False
        
#..............................................................................
#   now run HR module for calculating heat recovery and effective demand at pipe entry

        Status.mod.moduleHR.runHRModule()

#..............................................................................
# to be improved here. pass from demand in terms of UPH to demand in terms of USHm
# for the moment just set identical ...
                           
        Status.int.QD_Tt = Status.int.createQ_Tt()   
        Status.int.QA_Tt = Status.int.createQ_Tt()

        for iT in range(Status.NT+2):
            for it in range(Status.Nt):
                Status.int.QD_Tt[iT][it] = Status.int.USHTotal_Tt[iT][it]
                Status.int.QA_Tt[iT][it] = Status.int.QWHAmb_Tt[iT][it]

        Status.int.QD_T = Status.int.calcQ_T(Status.int.QD_Tt)
        Status.int.QA_T = Status.int.calcQ_T(Status.int.QA_Tt)

        Status.int.cascadeUpdateLevel = 0 #indicates that demand profile is created !!!

        showMessage("New FEATURE: calculation of heat demand from process data\n"+\
                    "For testing in the old mode using default heat demand set"+\
                    "user interaction level to ""automatic""")
        if Status.UserInteractionLevel == "automatic":
            Status.int.setDefaultDemand()

        print "Processes (calculateAggregateDemand): cascadeUpdateLevel set to 0"

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def changeInProcess(self):
#------------------------------------------------------------------------------		
#       function that is called from anywhere in the tool, whenever process data
#       of the present alternative are changed
#------------------------------------------------------------------------------		
        self.outOfDate = True
        Status.schedules.outOfDate = True
        Status.int.changeInCascade(0)
        logTrack("Processes (changeInProcess): process data changed")
        
#------------------------------------------------------------------------------		
    def createTempDist(self,PT,T0=None,C=None):
#------------------------------------------------------------------------------		
#   creates a linear ASCENDING temperature distribution between T0 and T,
#   or a step distribution, if T0 = None
#------------------------------------------------------------------------------		
        T = Status.int.T
        NT = Status.NT
        
        dist = []
        
        if T0 == None or T0 >= PT:
            for iT in range(NT+1):
                if PT > T[iT]:
                    dist.append(0.0)
                else:
                    dist.append(1.0)
            dist.append(1.0)    #last entry for T > Tmax

        else:
            for iT in range(NT+1):
                dist.append(cutInterval(T[iT],T0,PT))
            dist.append(1.0)    #last entry for T > Tmax

        return dist
                
#------------------------------------------------------------------------------		
    def createInvTempDist(self,PT,T0=None,C=None):
#------------------------------------------------------------------------------		
#   creates a linear DESCENDING temperature distribution between T0 and T,
#   or a step distribution, if T0 = None
#------------------------------------------------------------------------------		

        NT = Status.NT
        dist = self.createTempDist(PT,T0=T0,C=C)
        
        for iT in range(NT+2):
            dist[iT] = 1.0 - dist[iT]
        return dist

#------------------------------------------------------------------------------		
