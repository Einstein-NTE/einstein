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
    def createAggregateDemand(self):
#------------------------------------------------------------------------------		
        (projectData,generalData) = Status.prj.getProjectData()
        Status.HPerDayInd = projectData.HPerDayInd

        processes = Status.prj.getProcesses()

        QD_Tt = Status.int.createQ_Tt()
        QA_Tt = Status.int.createQ_Tt()

        for process in processes:
            k = process.ProcNo - 1

            UPHc = checkLimits(process.UPHc,0.0,INFINITE,0.0)
            scheduleC = Status.schedules.procInFlowSchedules[k]
            distUPHc = self.createTempDist(process.PT,T0=process.PTInFlowRec)
            
            UPHm = checkLimits(process.UPHm,0.0,INFINITE,0.0)
            scheduleM = Status.schedules.procOpSchedules[k]
            distUPHm = self.createTempDist(process.PT)

            UPHs = checkLimits(process.UPHs,0.0,INFINITE,0.0)
            scheduleS = Status.schedules.procStartUpSchedules[k]
            distUPHs = self.createTempDist(process.PT,T0=process.PTStartUp)

            UPHw = checkLimits(process.UPHw,0.0,INFINITE,0.0)
            scheduleW = Status.schedules.procOutFlowSchedules[k]
            distUPHw = self.createInvTempDist(process.PTOutFlowRec,T0=process.PTFinal)

            print "Processes (createAggregateDemand) - process %s: ",process.Process,k+1,UPHc,UPHm,UPHs,UPHw            
            NT = Status.NT
            Nt = Status.Nt

            for iT in range(NT+2): #NT + 1 + 1 -> additional value for T > Tmax
                for it in range(Nt+1):
                    time = Status.TimeStep*it
                    QD_Tt[iT][it] += UPHc*distUPHc[iT]*scheduleC.favg(time)
                    QD_Tt[iT][it] += UPHm*distUPHm[iT]*scheduleM.favg(time)
                    QD_Tt[iT][it] += UPHs*distUPHs[iT]*scheduleS.favg(time)
                    QA_Tt[iT][it] += UPHw*distUPHw[iT]*scheduleW.favg(time)
                 
        Status.int.QD_Tt = QD_Tt    
        Status.int.QA_Tt = QA_Tt

#now calculate annual values
        Status.int.QD_T = Status.int.calcQ_T(QD_Tt)
        Status.int.QA_T = Status.int.calcQ_T(QA_Tt)

#------------------------------------------------------------------------------		
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
            dist.append(1.0)

        else:
            for iT in range(0,NT+1):
                dist.append(cutInterval(T[iT],T0,PT))
            dist.append(1.0)

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
