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
#	SCHEDULES
#			
#------------------------------------------------------------------------------
#			
#	Functions for management of time schedules
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Hans Schweiger	07/05/2008
#	Revised by:         Hans Schweiger      02/09/2008
#
#       Changes in last update:
#
#       02/09/08: HS    Security feature added -> avoid zero division in function
#                       normalize
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
from einstein.GUI.status import Status
from einstein.modules.constants import *
from einstein.modules.messageLogger import *

DEFAULTSCHEDULES = ["continuous","batch","batchCharge","batchDischarge"]
DEFAULTCHARGETIME = 0.2 #20% of batch duration

#------------------------------------------------------------------------------		
class Schedule():
#------------------------------------------------------------------------------		
#   class that defines the standard EINSTEIN format for schedules
#------------------------------------------------------------------------------		

    def __init__(self,name):     #by default assigns a constant profile throughout the year
        self.daily = [[(0.0,24.0)]]
        self.weekly = [(0.0,120.0)]
        self.monthly = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
        self.holidays = [(365,365)]
        self.NHolidays = 1
        self.NDays = 260
        self.HPerDay = 24.      #operating period for the present schedule
        self.NBatch = 1
        self.HBatch = 24.
        self.ScheduleType = "continuous"
        self.name = name
        self.HPerYear = self.NDays*self.HPerDay
        self.hop = 1.0          #yearly operation hours from normalisation calculations
                                #should be finally identical with self.HPerYear

        self.fav = None         #fav is stored as a vector, as calculation seems
                                #quite time-consuming (-> calc_fav) 
#------------------------------------------------------------------------------		
    def setPars(self,ScheduleType,NDays,HPerDay,NBatch,HBatch):
#------------------------------------------------------------------------------		
#   sets the global parameters of this schedule
#------------------------------------------------------------------------------		
        if ScheduleType in DEFAULTSCHEDULES: self.ScheduleType = ScheduleType
        else: ScheduleType = DEFAULTSCHEDULES[0]
        
        self.NDays = int(checkLimits(NDays,0,365,default=260))
        self.HPerDay = checkLimits(HPerDay,0.0,Status.HPerDayInd,default=Status.HPerDayInd)
        self.NBatch = int(checkLimits(NBatch,1,100,default=1))
        self.HBatch = checkLimits(HBatch,0,HPerDay,default=(self.HPerDay/self.NBatch))
        self.HPerYear = self.NDays*self.HPerDay

        self.setDefault(ScheduleType)
        self.build_fav()
        
#------------------------------------------------------------------------------		
    def f(self,time):
#------------------------------------------------------------------------------		
#   calculates the instantaneous value of the schedule at time 
#------------------------------------------------------------------------------		
        if time < 0.0 or time > YEAR: return 0.
        day = int(floor(time/DAY)) + 1

        if self.isHoliday(day):return 0.

        weekTime = time%WEEK
        fweek = 0.0
        for period in self.weekly:
            start,stop = period
            if weekTime >= start and weekTime <= stop:
                fweek = 1.
                break
            
        month = findFirstGE(day,MONTHSTARTDAY)
        fmonth =  self.monthly[month-1]
        
        return fweek*fmonth

#------------------------------------------------------------------------------		
    def calc_fav(self,time):
#------------------------------------------------------------------------------		
#   calculates the average value within the interval [time,time+Dt] 
#------------------------------------------------------------------------------		
        if time < 0.0 or time >= YEAR: return 0.
        day = int(floor(time/DAY)) + 1

        if self.isHoliday(day):return 0.

        weekTime = time%WEEK
        fweek = 0.0

        for period in self.weekly:
            start,stop = period
            if weekTime < stop:
                weekTime1 = weekTime + Status.TimeStep
                if weekTime1 > start:
                    if weekTime >= start and weekTime1 <= stop:     #time interval fully within period
                        fweek = 1.
                        break
                    elif weekTime >= start and weekTime1 > stop:    #time interval starts within period, but ends afterwards
                        fweek = (stop - weekTime)/Status.TimeStep
                        break
                    elif weekTime < start and weekTime1 <= stop:    #time interval starts before period, but ends within
                        fweek = (weekTime1 - start)/Status.TimeStep
                        break
            
        month = findFirstGE(day,MONTHSTARTDAY)
        fmonth =  self.monthly[month-1]

        return fweek*fmonth
        
#------------------------------------------------------------------------------		
    def isHoliday(self,day):
#------------------------------------------------------------------------------		
        for period in self.holidays:
            start,stop = period
            if day <= stop and day >= start: return True
            
        return False

#------------------------------------------------------------------------------		
    def normalize(self):
#------------------------------------------------------------------------------		
        fsum = 0.0
        ftot = 0.0
        for it in range(Status.Nt):
            fsum += self.fav[it]
            ftot += Status.TimeStep

        fsum *= YEAR/ftot
        self.hop = fsum

        if fsum > 0:
            for it in range(Status.Nt):
                self.fav[it] /= fsum
        else:
            logDebug("Schedule (normalize): WARNING - schedule is 0 in all time steps")

        if fabs(self.hop-self.HPerYear) > 1.0:
            logDebug("Schedule (normalize): WARNING - normalized operating hours (%s) different from specified in HPerYear (%s)"\
                     %(self.hop,self.HPerYear))

        return fsum

        
#------------------------------------------------------------------------------		
    def build_fav(self):
#------------------------------------------------------------------------------		
#   calculates the vector with average values for all timesteps
#------------------------------------------------------------------------------		
        self.fav = []
        for it in range(Status.Nt):
            time = Status.TimeStep*it
            self.fav.append(self.calc_fav(time))

        self.normalize()


#------------------------------------------------------------------------------		
    def setDefault(self,scheduleType):
#------------------------------------------------------------------------------		
#   based on the basic schedule parameters (basic Q) assigns a detailed
#   default schedule
#------------------------------------------------------------------------------		
        if scheduleType == "continuous":
            
#..............................................................................		
# Continuous process (is the same as batch with NBatch = 1 and HBatch = HPerDay
#                       --> maybe can be completely eliminated in the future)

            start = 12.0 - 0.5 * self.HPerDay
            stop = 12.0 + 0.5 * self.HPerDay
            self.daily = [[(start,stop)]]

        elif scheduleType == "batch":

#..............................................................................		
# Batch process

            if self.NBatch > 0 and self.HBatch*self.NBatch <= self.HPerDay:
                TPeriod = Status.HPerDayInd / self.NBatch
            else:
                TPeriod = self.HBatch*self.NBatch
                logWarning("WARNING: batch duration larger than industry operating time")

            tStartDay = 12.0 - 0.5 * Status.HPerDayInd

            self.daily = [[]]
            for i in range(self.NBatch):
                start = tStartDay + TPeriod*i
                stop = start + self.HBatch
                self.daily[0].append((start,stop))

            self.HPerDay = self.NBatch*self.HBatch
        
#..............................................................................		
# Charge of batch process: first DEFAULTCHARGETIME % of process duration

        elif scheduleType == "batchCharge":
            if self.NBatch > 0 and self.HBatch*self.NBatch <= self.HPerDay:
                TPeriod = Status.HPerDayInd / self.NBatch
            else:
                TPeriod = self.HBatch*self.NBatch
                logWarning("WARNING: batch duration larger than industry operating time")

            tStartDay = 12.0 - 0.5 * Status.HPerDayInd

            self.daily = [[]]
            for i in range(self.NBatch):
                start = tStartDay + TPeriod*i
                stop = start + DEFAULTCHARGETIME*self.HBatch
                self.daily[0].append((start,stop))

            self.HPerDay = self.NBatch*self.HBatch*DEFAULTCHARGETIME

#..............................................................................		
# Charge of batch process: first DEFAULTCHARGETIME % of process duration after process stop

        elif scheduleType == "batchDischarge":
            if self.NBatch > 0 and self.HBatch*self.NBatch <= self.HPerDay:
                TPeriod = Status.HPerDayInd / self.NBatch
            else:
                TPeriod = self.HBatch*self.NBatch
                logWarning("WARNING: batch duration larger than industry operating time")

            tStartDay = 12.0 - 0.5 * Status.HPerDayInd

            self.daily = [[]]
            for i in range(self.NBatch):
                start = (tStartDay + TPeriod*i + self.HBatch)%DAY
                stop = (start + DEFAULTCHARGETIME*self.HBatch)%DAY

#### take care: the %DAY controls to avoid that processes discharge AFTER 24:00 h of a day
#### this works well only for 7 days operation without holidays
#### as this is a quite strange special case, should not give problems for the moment
#### but should be improved !!!
                
                self.daily[0].append((start,stop))

            self.HPerDay = self.NBatch*self.HBatch*DEFAULTCHARGETIME

#..............................................................................		
# Now extend daily to weekly profile

        self.NDaysPerWeek = (self.NDays - self.NHolidays - 1.0)/52.0

        self.weekly = []
        for i in range(7):
            tmax = self.NDaysPerWeek * 24.0
            
            for dayinterval in self.daily[0]:
                (start,stop) = dayinterval
                start += 24.0*i
                stop += 24.0*i
                if start < tmax:
                    stop = min(stop,tmax)
                    self.weekly.append((start,stop))
                else:
                    break

        logTrack("Schedule (setDefault): weekly profile created: %s"%self.weekly)
        
#------------------------------------------------------------------------------		
class Schedules(object):
#------------------------------------------------------------------------------		
#   Module that handles all project schedules
#------------------------------------------------------------------------------		
    
#------------------------------------------------------------------------------		
    def __init__(self):
#------------------------------------------------------------------------------		
        self.outOfDate = True
       
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def create(self):
#------------------------------------------------------------------------------		

        (projectData,generalData) = Status.prj.getProjectData()
        Status.HPerDayInd = projectData.HPerDayInd

        self.calculateProcessSchedules()
        self.calculateEquipmentSchedules()
        self.calculateWHEESchedules()

        self.outOfDate = False
       
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def calculateProcessSchedules(self):
#------------------------------------------------------------------------------		
#   calulates the Schedules of the processes
#------------------------------------------------------------------------------		

        logTrack("Schedules (calcProcS): running")
        
        processes = Status.prj.getProcesses()

        self.procOpSchedules = []
        self.procStartUpSchedules = []
        self.procInFlowSchedules = []
        self.procOutFlowSchedules = []
        
        for process in processes:

#..............................................................................
# check if data are correct

            if process.ProcType == "continuous":
                if process.NBatch != 1 or process.HBatch != process.HPerDayProc:
                    logDebug("Schedules (calculate): error in process schedule")
                    process.HBatch = process.HPerDayProc
                    process.NBatch = 1
                    Status.SQL.commit()

#..............................................................................
# schedule for process operation
                    
            newSchedule = Schedule("Process No.%s (%s): Operation"%(process.ProcNo,process.Process))

            if process.ProcType == "continuous":
                scheduleType = "continuous"
            else:
                scheduleType = "batch"
            newSchedule.setPars(scheduleType,
                                   process.NDaysProc,
                                   process.HPerDayProc,
                                   process.NBatch,
                                   process.HBatch)
            self.procOpSchedules.append(newSchedule)
            
#..............................................................................
# schedule for process start-up

            newSchedule = Schedule("Process No.%s (%s): Start-Up"%(process.ProcNo,process.Process))
            
            if process.ProcType == "continuous":
                scheduleType = "batchCharge"
            else:
                scheduleType = "batchCharge"
                
            newSchedule.setPars(scheduleType,
                                   process.NDaysProc,
                                   process.HPerDayProc,
                                   process.NBatch,
                                   process.HBatch)
            self.procStartUpSchedules.append(newSchedule)

#..............................................................................
# schedule for process in-flows (for the moment only ONE !!!)

            newSchedule = Schedule("Process No.%s (%s): InFlow 1"%(process.ProcNo,process.Process))
            
            if process.ProcType == "continuous":
                scheduleType = "continuous"
            else:
                scheduleType = "batchCharge"
                
            newSchedule.setPars(scheduleType,
                                   process.NDaysProc,
                                   process.HPerDayProc,
                                   process.NBatch,
                                   process.HBatch)
            self.procInFlowSchedules.append(newSchedule)

            newSchedule = Schedule("Process No.%s (%s): OutFlow 1"%(process.ProcNo,process.Process))
            if process.ProcType == "continuous":
                scheduleType = "continuous"
            else:
                scheduleType = "batchDischarge"
            newSchedule.setPars(scheduleType,
                                   process.NDaysProc,
                                   process.HPerDayProc,
                                   process.NBatch,
                                   process.HBatch)
            self.procOutFlowSchedules.append(newSchedule)
       
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def calculateEquipmentSchedules(self):
#------------------------------------------------------------------------------		
#   calulates the Schedules of the processes
#------------------------------------------------------------------------------		

        logTrack("Schedules (calcEquipeSchedules): running")
        
        equipments = Status.prj.getEquipments()

        self.equipmentSchedules = []
        
        for equipe in equipments:

#..............................................................................
# schedule for equipment operation
                    
            newSchedule = Schedule("Equipe No.%s (%s)"%(equipe.EqNo,equipe.Equipment))

            newSchedule.setPars("continuous",
                                equipe.NDaysEq,
                                equipe.HPerDayEq,
                                1,
                                equipe.HPerDayEq)
            self.equipmentSchedules.append(newSchedule)
            
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def calculateWHEESchedules(self):
#------------------------------------------------------------------------------		
#   calulates the Schedules of the electrical equipment w. waste heat
#------------------------------------------------------------------------------		

        logTrack("Schedules (calcWHEESchedules): running")
        
        whees = Status.prj.getWHEEs()

        self.WHEESchedules = []
        
        for whee in whees:

#..............................................................................
# schedule for equipment operation
                    
            newSchedule = Schedule("WHEE No.%s (%s)"%(whee.WHEENo,whee.WHEEName))

            newSchedule.setPars("continuous",
                                whee.NDaysWHEE,
                                whee.HPerDayWHEE,
                                whee.NBatchWHEE,
                                whee.HBatchWHEE)
            self.equipmentSchedules.append(newSchedule)
            
#------------------------------------------------------------------------------		
    
