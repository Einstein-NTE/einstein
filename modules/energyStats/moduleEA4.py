# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA4- Process heat- Yearly data
#			
#==============================================================================
#
#	Version No.: 0.06
#	Created by: 	    Tom Sobota	    21/03/2008
#       Revised by:         Tom Sobota      29/03/2008
#                           Stoyan Danov    07/04/2008
#                           Stoyan Danov    11/04/2008
#                           Stoyan Danov    02/05/2008
#                           Hans Schweiger  08/05/2008
#                           Stoyan Danov    02/07/2008
#
#       Changes to previous version:
#       29/3/2008          Adapted to numpy arrays
#       07/04/2008          Adapted to use data from sql, not checked
#       11/04/2008: SD: Dummy data added for displaying temporaly, to avoid problems with None.
#                       Return to original state later!
#       02/05/2008: SD: sqlQuery -> to initModule; sejf.interfaces -> Status.int,None resistance,avoid ZeroDivision
#       08/05/2008: HS  Generation of GDATA table PROCESS for report
#       02/07/2008: SD: add total row in data, fill graphics data panelEA4b from default demand (interfaces)
#                       or from dummydata3, initModule commented (dummy data sent to panels EA4a & EA4b) ->to be arranged later
#       06/07/2008: HS  Eliminate dummy data, calculate and send real data to GUI
#                       restructuring and clean-up
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
from numpy import *

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
from einstein.GUI.numCtrl import *
import copy

def _U(text):
    return unicode(_(text),"utf-8")

#============================================================================== 
#============================================================================== 
class ModuleEA4(object):
#============================================================================== 
#============================================================================== 

#------------------------------------------------------------------------------
    def __init__(self, keys):
#------------------------------------------------------------------------------
#       initialisation of the module (at Tool start-up)
#------------------------------------------------------------------------------
        
        self.keys = keys
    
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       calculations at entry to the panel
#------------------------------------------------------------------------------
        
        pass
    
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       calculations for refresh of panel
#------------------------------------------------------------------------------

        PId = Status.PId
        ANo = Status.ANo


#..............................................................................
# First get yearly totals and write to Panel EA4a

        self.qprocessdata = Status.prj.getProcesses()   #sqlqueries centralised in project-functions
        processes = self.qprocessdata

        Process = []
        PT = []
        PST = []
        UPHk = 0.0
        UPH = []
        UPHc = []
        UPHm = []
        UPHs = []
        
        TotalUPH = 0.0
        for process in processes:
            Process.append(unicode(process.Process,"utf-8"))
            PT.append(process.PT)
            PST.append(process.TSupply)
            
            if process.UPH is not None: UPH.append(process.UPH/1000.)
            else: UPH.append(0.0)
            if process.UPHc is not None: UPHc.append(process.UPHc/1000.)
            else: UPHc.append(0.0)
            if process.UPHm is not None: UPHm.append(process.UPHm/1000.)
            else: UPHm.append(0.0)
            if process.UPHs is not None: UPHs.append(process.UPHs/1000.)
            else: UPHs.append(0.0)
            
            if process.UPH is None:
                TotalUPH += 0.0
            else:
                TotalUPH += process.UPH/1000.0  #conversion to MWh !!!!

        PT = noneFilter(PT)
        PST = noneFilter(PST)
        UPH = noneFilter(UPH)
        UPHc = noneFilter(UPHc)
        UPHs = noneFilter(UPHs)
        UPHm = noneFilter(UPHm)
        

        UPHPercentage = []
        if TotalUPH > 0.0: 
            for k in range(len(processes)):
                UPHPercentage.append(UPH[k]*100.0/TotalUPH)
        else:
            for k in range(len(processes)):
                UPHPercentage.append(0.0)

#..............................................................................
# finish the table columns, add total, percentage total

        Process.append(_U('Total'))
        PT.append(' ')
        PST.append(' ')
        UPH.append(TotalUPH)
        UPHc.append(' ')
        UPHs.append(' ')
        UPHm.append(' ')
        UPHPercentage.append(100.0)

#..............................................................................
# here data are prepared for the GUI and the report

#..............................................................................
# Data for Panel EA4a: annual values

        if self.keys[0] == "EA4a_Table":

# table in EA4a: UPH by process

            TableColumnList1 = [Process, UPH, UPHPercentage,UPHc,UPHm,UPHs,PT,PST]

            matrix1 = transpose(TableColumnList1)
#            print 'moduleEA4: matrix1 =', matrix1
            data1 = array(matrix1)

            Status.int.setGraphicsData("EA4a_Table", data1)

# table in EA4a: for report

            reportMatrix1 = []
            for i in range(len(matrix1)-1):
                if i < 10:
                    reportMatrix1.append(matrix1[i])
            for i in range(len(matrix1)-1,10):
                reportMatrix1.append([" "," "," "," "," "," "," "," "])
            reportMatrix1.append(matrix1[len(matrix1)-1])

            reportData1 = array(reportMatrix1)

            if Status.ANo == 0:
                Status.int.setGraphicsData("EA4a_REPORT", reportData1)
#                print "EA4a_REPORT",reportData1
            elif Status.ANo == Status.FinalAlternative:
                Status.int.setGraphicsData("EA4a_REPORT_F", reportData1)
#                print "EA4a_REPORT_F",reportData1

#..............................................................................
# Data for Panel EA4b: temperature dependent plots

        if self.keys[0] == "EA4b_Table":

#            Status.mod.moduleHR.simulateHR()        #loads UPHProcTotal and USHTotal
            Status.mod.moduleHR.runHRModule()        #loads UPHProcTotal and USHTotal

            UPHTotal = Status.int.UPHTotal_T[Status.NT+1]/1000.0
            UPHProcTotal = Status.int.UPHProcTotal_T[Status.NT+1]/1000.0
            USHTotal = Status.int.USHTotal_T[Status.NT+1]/1000.0

# first determine maximum temperature level up to which supply is still varying (supply is the highest T-level !!!)

            iTmax = Status.NT
            for iT in range(Status.NT+1):
                if Status.int.USHTotal_T[iT]/1000.0 >= USHTotal*0.9999:
                    iTmax = min(iT + 8,Status.NT)
                    break
            iTmax = max(20,iTmax)     # minimum plot up to 100 ºC

# prepare data for table

            Title = []
            UPH = []
            dUPH = []
            UPHPerc = []
            UPHPercCum = []
            UPHProc = []
            dUPHProc = []
            UPHProcPerc = []
            UPHProcPercCum = []
            USH = []
            dUSH = []
            USHPerc = []
            USHPercCum = []

            TLevels = [60.0,80.0,100.0,120.0,140.0,180.0,220.0,300.0,400.0,10000.0]
            Titles = [u"    <  60 ºC",
                      u" 60 -  80 ºC",
                      u" 80 - 100 ºC",
                      u"100 - 120 ºC",
                      u"120 - 140 ºC",
                      u"140 - 180 ºC",
                      u"180 - 220 ºC",
                      u"220 - 300 ºC",
                      u"300 - 400 ºC",
                      u"    > 400 ºC",
                      _U("Total")]

            for i in range(len(TLevels)):
                T = TLevels[i]
                iT = int(floor(T/Status.TemperatureInterval + 0.5))
                iT = min(iT,Status.NT+1)
                
                UPH.append(Status.int.UPHTotal_T[iT]/1000.0)
                UPHPercCum.append(100*UPH[i]/max(UPHTotal,0.001))
                if i == 0:
                    UPHPerc.append(UPHPercCum[i])
                    dUPH.append(UPH[i])
                else:
                    UPHPerc.append(UPHPercCum[i] - UPHPercCum[i-1])
                    dUPH.append(UPH[i]-UPH[i-1])
                                  
                UPHProc.append(Status.int.UPHProcTotal_T[iT]/1000.0)
                UPHProcPercCum.append(100*UPHProc[i]/max(UPHProcTotal,0.001))
                if i == 0:
                    UPHProcPerc.append(UPHProcPercCum[i])
                    dUPHProc.append(UPH[i])
                else:
                    UPHProcPerc.append(UPHProcPercCum[i] - UPHProcPercCum[i-1])
                    dUPHProc.append(UPHProc[i]-UPHProc[i-1])

                USH.append(Status.int.USHTotal_T[iT]/1000.0)
                
                USHPercCum.append(100*USH[i]/max(USHTotal,0.001))
                if i == 0:
                    USHPerc.append(USHPercCum[i])
                    dUSH.append(USH[i])
                else:
                    USHPerc.append(USHPercCum[i] - USHPercCum[i-1])
                    dUSH.append(USH[i]-USH[i-1])

# add last row for totals
            UPH.append(UPHTotal)
            dUPH.append(UPHTotal)
            UPHPerc.append(100.0)
            UPHPercCum.append(100.0)

            UPHProc.append(UPHProcTotal)
            dUPHProc.append(UPHProcTotal)
            UPHProcPerc.append(100.0)
            UPHProcPercCum.append(100.0)

            USH.append(USHTotal)
            dUSH.append(USHTotal)
            USHPerc.append(100.0)
            USHPercCum.append(100.0)
            
#..............................................................................

# data for EA4b table

            for i in range(len(dUPH)):
                dUPH[i] = convertDoubleToString(dUPH[i],nDecimals = 2)
                UPHPerc[i] = convertDoubleToString(UPHPerc[i],nDecimals = 2)
                UPHPercCum[i] = convertDoubleToString(UPHPercCum[i],nDecimals = 2)
                dUSH[i] = convertDoubleToString(dUSH[i],nDecimals = 2)
                USHPerc[i] = convertDoubleToString(USHPerc[i],nDecimals = 2)
                USHPercCum[i] = convertDoubleToString(USHPercCum[i],nDecimals = 2)

            data1 = array(transpose([Titles,dUPH,UPHPerc,UPHPercCum,dUSH,USHPerc,USHPercCum]))
            Status.int.setGraphicsData(self.keys[0],data1)


            if Status.ANo == 0:
                Status.int.setGraphicsData("EA4b_REPORT", data1)
            elif Status.ANo == Status.FinalAlternative:
                Status.int.setGraphicsData("EA4b_REPORT_F", data1)
                                  
# data for EA4b plot

            UPH_plot = []
            UPHproc_plot = []
            USH_plot = []
            
            for iT in range(iTmax):
                UPH_plot.append(Status.int.UPHTotal_T[iT]/1000.0)
                UPHproc_plot.append(Status.int.UPHProcTotal_T[iT]/1000.0)
                USH_plot.append(Status.int.USHTotal_T[iT]/1000.0)

            Status.int.setGraphicsData(self.keys[1],[Status.int.T[0:iTmax],
                                                     UPH_plot,
                                                     UPHproc_plot,
                                                     USH_plot])


#add identical values as dummies to the plot. -> fixed array size needed for report !!!
                
            TT = copy.deepcopy(Status.int.T[0:iTmax])
            UPH_rep = copy.deepcopy(UPH_plot)
            UPHproc_rep = copy.deepcopy(UPHproc_plot)
            USH_rep = copy.deepcopy(USH_plot)
            
            for iT in range(iTmax,(Status.NT+1)):
                TT.append(Status.int.T[iTmax-1])
                UPH_rep.append(Status.int.UPHTotal_T[iTmax-1]/1000.0)
                UPHproc_rep.append(Status.int.UPHProcTotal_T[iTmax-1]/1000.0)
                USH_rep.append(Status.int.USHTotal_T[iTmax-1]/1000.0)

            dataList = [TT,UPH_rep,UPHproc_rep,USH_rep]

            if Status.ANo == 0:
                Status.int.setGraphicsData("EA4b_PLOT_REPORT",array(transpose(dataList)))
#                print "EA4b_PLOT_REPORT",array(transpose(dataList))

            elif Status.ANo == Status.FinalAlternative:
                Status.int.setGraphicsData("EA4b_PLOT_REPORT_F",array(transpose(dataList)))
#                print "EA4b_PLOT_REPORT_F",array(transpose(dataList))
                

#..............................................................................
# Data for Panel EA4c: cumulative heat demand curve

        if self.keys[0] == "EA4c_Table":

            Status.mod.moduleHR.runHRModule()        #loads UPHProcTotal and USHTotal

# prepare data for table
            TLevels = [10000.0,80.0,120.0,250.0,400.0]
            Titles = [u"  Total  ",
                      u" <  80 ºC",
                      u" < 120 ºC",
                      u" < 250 ºC",
                      u" < 400 ºC"]

            tLevels = [4000.0,2000.0,0]
            
            it_baseLoad = int(Status.Nt * tLevels[0]/YEAR)
            it_mediumLoad = int(Status.Nt * tLevels[1]/YEAR)
            it_peakLoad = int(Status.Nt * tLevels[2]/YEAR)
            
            USH = []
            baseLoad = []
            mediumLoad = []
            peakLoad = []
            energy_baseLoad = []
            energy_mediumLoad = []
            energy_peakLoad = []
            
            for i in range(len(TLevels)):
                T = TLevels[i]
                iT = int(floor(T/Status.TemperatureInterval + 0.5))
                iT = min(iT,Status.NT+1)
                
                USH.append(copy.deepcopy(Status.int.USHTotal_Tt[iT]))  #copy, in order not to sort the original list
                USH[i].sort()
                USH[i].reverse()

                baseLoad.append(USH[i][it_baseLoad])
                mediumLoad.append(USH[i][it_mediumLoad])
                peakLoad.append(USH[i][it_peakLoad])

                energy_baseLoad.append(0.0)
                energy_mediumLoad.append(0.0)
                energy_peakLoad.append(0.0)

                for it in range(Status.Nt):
                    energy_baseLoad[i] += min(baseLoad[i],USH[i][it])
                    energy_mediumLoad[i] += min(mediumLoad[i],USH[i][it])
                    energy_peakLoad[i] += min(peakLoad[i],USH[i][it])

                energy_peakLoad[i] -= energy_mediumLoad[i]
                energy_mediumLoad[i] -= energy_baseLoad[i]
                
                baseLoad[i] /= Status.TimeStep      #convert to power
                mediumLoad[i] /= Status.TimeStep
                peakLoad[i] /= Status.TimeStep

                energy_baseLoad[i] *= Status.EXTRAPOLATE_TO_YEAR/1000.0           #convert to MWh
                energy_mediumLoad[i] *= Status.EXTRAPOLATE_TO_YEAR/1000.0  
                energy_peakLoad[i] *= Status.EXTRAPOLATE_TO_YEAR/1000.0  
            
# now determine maximum number of operating hours

            itMax = lastNonZero(USH[0])
            tMax = itMax * Status.TimeStep
            itMax = int((500.0/Status.TimeStep) * ceil(tMax/500.0)  +0.5)  #round
            itMax = min(itMax,Status.Nt-1)
                            
#..............................................................................
            
# data for EA4c table

            dataList =[Titles,baseLoad,energy_baseLoad,mediumLoad,energy_mediumLoad,peakLoad,energy_peakLoad]
            data = array(transpose(dataList))
            Status.int.setGraphicsData(self.keys[0],data)

            if Status.ANo == 0:
                Status.int.setGraphicsData("EA4c_REPORT",data)
            elif Status.ANo == Status.FinalAlternative:
                Status.int.setGraphicsData("EA4c_REPORT_F",data)
                                  
# data for EA4c plot

            time = ["t"]
            for it in range(itMax+1):
                time.append(it * YEAR / Status.Nt)

            dataList = [time[0:itMax+1]]
            for i in range(len(TLevels)):
                row = [Titles[i]]
                row.extend(USH[i][0:itMax])
                dataList.append(row)
            data = array(dataList)
            Status.int.setGraphicsData(self.keys[1],data)

# data for EA4c plot in report

#            print "ModuleEA4c: generating data for report"
            timeReport = ["t"]

            DATAPOINTS = 100
            
            step = max(1.0, 1.0 * itMax / DATAPOINTS)
            
            for itr in range(DATAPOINTS):
                it = int(step*itr)
                timeReport.append(it*YEAR/Status.Nt)

#            print "step = %s itMax = %s Status.Nt = %s"%(step,itMax,Status.Nt)
#            print timeReport

            dataListReport = [timeReport]
            for i in range(len(TLevels)):
                row = [Titles[i]]
                for itr in range(DATAPOINTS):
                    it = int(step*itr)
                    USH[i][itr] = USH[i][it]
                row.extend(USH[i][0:DATAPOINTS])
                dataListReport.append(row)
            dataReport = array(transpose(dataListReport))
#            print "Data for EA4c_PLOT_REPORT\n",dataReport

            if Status.ANo == 0:
                Status.int.setGraphicsData("EA4c_PLOT_REPORT",dataReport)
            elif Status.ANo == Status.FinalAlternative:
                Status.int.setGraphicsData("EA4c_PLOT_REPORT_F",dataReport)
            
#==============================================================================
