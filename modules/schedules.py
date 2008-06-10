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
from einstein.GUI.status import Status

YEAR = 8760.0
DAY = 24.0
WEEK = DAY*7
MONTHSTARTDAY = [0,31,59,90,120,151,181,212,243,273,304,334]
DEFAULTSCHEDULES = ["continuous","batch","batchCharge","batchDischarge"]
DEFAULTCHARGETIME = 0.2 #20% of batch duration

#------------------------------------------------------------------------------		
class Schedule():
#------------------------------------------------------------------------------		
#   class that defines the standard EINSTEIN format for schedules
#------------------------------------------------------------------------------		

    def __init__(self):     #by default assigns a constant profile throughout the year
        self.daily = [[(0.0,24.0)]]
        self.weekly = [(0.0,120.0)]
        self.monthly = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
        self.holidays = []
        self.NHolidays = 1
        self.NDays = 260
        self.HPerDay = 24.      #operating period for the present schedule
        self.NBatch = 1
        self.HBatch = 24.
        self.ScheduleType = "continuous"

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
    def favg(self,time):
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
            weekTime1 = weekTime + Status.TimeStep
            if weekTime >= start and weekTime1 <= stop:     #time interval fully within period
                fweek = 1.
                break
            elif weekTime >= start and weekTime1 > stop:    #time interval ends after period
                fweek = (stop - weekTime)/Status.TimeStep
                break
            elif weekTime < start and weekTime1 <= stop:
                fweek = (weekTime1 - start)/Status.TimeStep
                break
            
        month = findFirstGE(day,MONTHSTARTDAY)
        fmonth =  self.monthly[month-1]

        return fweek*fmonth
        
    def isHoliday(self,day):
        for period in self.holidays:
            start,stop = period
            if day <= stop and day >= start: return True
        return False

        
#------------------------------------------------------------------------------		
    def getSchedule(self):
#------------------------------------------------------------------------------		
#   calculates the vector with average values for all timesteps
#------------------------------------------------------------------------------		
        schedule = []
        for it in range(Status.Nt):
            time = Status.TimeStep*it
            schedule.append(self.favg(time))
#### TAKE CARE: -> should fractions be allowed, if timeSteps are large ??? 

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
                print "Schedule (setDefault): ERROR in schedule parameters"

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
                print "Schedule (setDefault): ERROR in schedule parameters"

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
                print "Schedule (setDefault): ERROR in schedule parameters"

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

        print ("weekly profile created")
        print self.weekly
        
#------------------------------------------------------------------------------		
class Schedules(object):
#------------------------------------------------------------------------------		
#   Module that handles all project schedules
#------------------------------------------------------------------------------		
    
#------------------------------------------------------------------------------		
    def __init__(self):
#------------------------------------------------------------------------------		
        pass
       
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def create(self):
#------------------------------------------------------------------------------		
        (projectData,generalData) = Status.prj.getProjectData()
        Status.HPerDayInd = projectData.HPerDayInd

        self.calculateProcessSchedules()
        self.calculateEquipmentSchedules()
        self.calculateWHEESchedules()

       
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def calculateProcessSchedules(self):
#------------------------------------------------------------------------------		
#   calulates the Schedules of the processes
#------------------------------------------------------------------------------		

        print ("Schedules (calcProcS): running")
        
        processes = Status.prj.getProcesses()

        self.procOpSchedules = []
        self.procStartUpSchedules = []
        self.procInFlowSchedules = []
        self.procOutFlowSchedules = []
        
        for process in processes:

            print ("Schedules (calcProcS): process no. %s: ")%process.ProcNo,process.Process

#..............................................................................
# check if data are correct

            if process.ProcType == "continuous":
                if process.NBatch != 1 or process.HBatch != process.HPerDayProc:
                    print "Schedules (calculate): error in process schedule"
                    process.HBatch = process.HPerDayProc
                    process.NBatch = 1
                    Status.SQL.commit()

#..............................................................................
# schedule for process operation
                    
            newSchedule = Schedule()

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

            newSchedule = Schedule()
            
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

            newSchedule = Schedule()
            
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

            newSchedule = Schedule()
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

        print ("Schedules (calcEquipeSchedules): running")
        
        equipments = Status.prj.getEquipments()

        self.equipmentSchedules = []
        
        for equipe in equipments:

            print ("Schedules (calcEquipeSchedules): eq. no. %s: ")%equipe.EqNo,equipe.Equipment

#..............................................................................
# schedule for equipment operation
                    
            newSchedule = Schedule()

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

        print ("Schedules (calcWHEESchedules): running")
        
        whees = Status.prj.getWHEEs()

        self.WHEESchedules = []
        
        for whee in whees:

            print ("Schedules (calcEquipeSchedules): eq. no. %s: ")%whee.WHEENo,whee.WHEEName

#..............................................................................
# schedule for equipment operation
                    
            newSchedule = Schedule()

            newSchedule.setPars("continuous",
                                whee.NDaysWHEE,
                                whee.HPerDayWHEE,
                                whee.NBatchWHEE,
                                whee.HBatchWHEE)
            self.equipmentSchedules.append(newSchedule)
            
#------------------------------------------------------------------------------		
    
