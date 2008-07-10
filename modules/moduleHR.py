# -*- coding: cp1252 -*-
#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#   ModuleHC (Heat and Cold Supply)
#           
#------------------------------------------------------------------------------
#           
#   Module for design of HC Supply cascade
#
#==============================================================================
#
#   Version No.: 0.03
#   Created by:         Hans Schweiger  10/06/2008
#   Last revised by:
#                       Hans Schweiger  23/06/2008
#                       Hans Schweiger  02/07/2008
#
#   Changes to previous version:
#
#   23/06/2008: HS  Query of fluids and fuels used in export XML
#   02/07/2008: HS  Function getHXData added -> obtains Fluid ID's in HX
#   
#------------------------------------------------------------------------------     
#   (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#   www.energyxperts.net / info@energyxperts.net
#
#   This program is free software: you can redistribute it or modify it under
#   the terms of the GNU general public license as published by the Free
#   Software Foundation (www.gnu.org).
#
#============================================================================== 

from sys import *
from math import *
from numpy import *


from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP
from einstein.modules.constants import *
from einstein.modules.exportdata import *

from einstein.modules.messageLogger import *

class ModuleHR(object):

    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

        self.DB = Status.DB
        self.sql = Status.SQL
        
        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        self.hx = Status.DB.qheatexchanger.sql_select(sqlQuery)
        self.NHX = len(self.hx)

        Status.int.getEquipmentCascade()
        self.cascadeIndex = 0

        self.updatePanel()
            
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------

        dataList = []
        for i in range(self.NHX):
            row = {"equipeNo":1,"equipeType":"hx","equipePnom":1000}
            dataList.append(noneFilter([i+1,row["equipeNo"],"myname",row["equipeType"],row["equipePnom"],"???"]))
        data = array(dataList)

        Status.int.setGraphicsData(self.keys[0], data)

        try:
            Status.int.setGraphicsData('HR Info',{"noseque":55})
        except:
            pass

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def getHXData(self):
#------------------------------------------------------------------------------
#       obtains the data of the HX fluids
#------------------------------------------------------------------------------

        hxes = Status.prj.getHXes()
        equipments = Status.prj.getEquipments()
        pipes = Status.prj.getPipes()
        processes = Status.prj.getProcesses()
        whees = Status.prj.getWHEEs()

        for hx in hxes:
            source = hx.HXSource
            sink = hx.HXSink
            sourceOK = False
            sinkOK = False

            print "----------------------------------------------"
            print "ModuleHR (getHXData): checking HX %s with Source= %s and Sink= %s"%\
                  (hx.HXName,hx.HXSource,hx.HXSink)

            for eq in equipments:
                if (sourceOK==True and sinkOK==True): break

                print "Equipment %s: "%eq.Equipment
                if source == eq.Equipment:
                    hx.FluidIDSource = None
                    sourceOK = True
                    
                if sink == eq.Equipment:
                    hx.FluidIDSink = None
                    sinkOK = True

                print "sourceID/sinkID: %s,%s"%(hx.FluidIDSource,hx.FluidIDSink)
            
            for pipe in pipes:
                if (sourceOK==True and sinkOK==True): break
                print "Pipe %s: "%pipe.Pipeduct
                if source == pipe.Pipeduct:
                    hx.FluidIDSource = pipe.HeatDistMedium
                    sourceOK = True

                if sink == pipe.Pipeduct:
                    hx.FluidIDSink = pipe.HeatDistMedium
                    sinkOK = True

                print "sourceID/sinkID: %s,%s"%(hx.FluidIDSource,hx.FluidIDSink)
            
            for process in processes:
                if (sourceOK==True and sinkOK==True): break
                print "process %s: "%process.Process
                if source == process.Process:
                    hx.FluidIDSource = process.ProcMedOut
                    sourceOK = True
                    
                if sink == process.Process:
                    hx.FluidIDSink = process.ProcMedDBFluid_id
                    sinkOK = True

                print "sourceID/sinkID: %s,%s"%(hx.FluidIDSource,hx.FluidIDSink)
                    
            for whee in whees:                         #WHEE can only be source, not sink !!!
                if (sourceOK==True and sinkOK==True): break
                print "whee %s: "%whee.WHEEName
                if source == whee.WHEEName:
                    hx.FluidIDSource = whee.WHEEMedium
                    sourceOK = True

                print "sourceID/sinkID: %s,%s"%(hx.FluidIDSource,hx.FluidIDSink)

            if sinkOK == False:
                logWarning("ModuleHR (getHXData): couldn't find a sink ID for HX %s"%hx.HXName)
                
            if sourceOK == False:
                logWarning("ModuleHR (getHXData): couldn't find a source ID for HX %s"%hx.HXName)
                
#------------------------------------------------------------------------------
    def runHRModule(self):
#------------------------------------------------------------------------------
#       runs the calculations on the external HR module
#------------------------------------------------------------------------------

        if Status.schedules.outOfDate == True:
            Status.schedules.create()   #creates the process and equipment schedules

        self.getHXData()

        (fluidIDs,fuelIDs) = Status.prj.getFluidAndFuelList()                         
        ex = ExportDataHR(pid=Status.PId, ano=Status.ANo,fuels=fuelIDs, fluids=fluidIDs)

#        self.runHR()
#        self.importDataFromHR()

        self.simulateHR()

        pass
#------------------------------------------------------------------------------
    def simulateHR(self):
#------------------------------------------------------------------------------
#       simulates the action of the HR module while the module is not yet
#       available
#       starting point: USHTotal_Tt -> process heat demand at process entry
#                       USHwTotal_Tt -> waste heat demand
#
#       QHX = min(fHR*USHw_Tt,QHXmax)
#------------------------------------------------------------------------------

        if Status.processData.outOfDate == True:
            Status.processData.createAggregateDemand()
            
        QHXProc_Tt = Status.int.createQ_Tt()    # heat recovered for process heating
        UPHProc_Tt = Status.int.createQ_Tt()    # heat supplied externally to processes
        USH_Tt = Status.int.createQ_Tt()        # heat demand at entry of pipes
        QWHAmb_Tt = Status.int.createQ_Tt()     # remaining waste heat that currently is dissipated

        UPH_Tt = Status.int.UPHTotal_Tt
        UPHw_Tt = Status.int.UPHwTotal_Tt

#..............................................................................
# settings of the conversion

        if Status.ANo > 0:
            fHR = 0.8   # fraction of potential heat recovery that is really recovered
        else:
            fHR = 0.0
        logWarning("Test version. REAL HX network is not taken into consideration !!!!")

        (projectData,generalData) = Status.prj.getProjectData()
        if generalData is not None:
            DistributionEfficiency = generalData.HDEffAvg
        else:
            logDebug("SimulateHR: error reading distribution efficiency from cgeneraldata")
            DistributionEfficiency = 0.9
            
        fDist = 1./max(DistributionEfficiency,0.1)  #distribution efficiency < 10% doesn't make much sense
        
#..............................................................................
#..............................................................................
#..............................................................................

        for it in range(Status.Nt):

#..............................................................................
        
            QHXmax = 0
            for iT in range(Status.NT+1,-1,-1):
                QHXmax = max(QHXmax,min(fHR*UPHw_Tt[iT][it],UPH_Tt[iT][it]))
                QHXProc_Tt[iT][it] = min(QHXmax,fHR*UPHw_Tt[iT][it])
                QWHAmb_Tt[iT][it] = UPHw_Tt[iT][it] - QHXProc_Tt[iT][it]

            QHXProc_it = QHXProc_Tt[0][it]
            
            for iT in range(Status.NT+2):
                QHXProc_Tt[iT][it] = QHXProc_it - QHXProc_Tt[iT][it]    #from descending to ascending cumulative
                UPHProc_Tt[iT][it] = UPH_Tt[iT][it] - QHXProc_Tt[iT][it] 
                           
#..............................................................................
# from UPHext to USH: shift in temperature (10 K) and divide by distribution efficiency

            USH_Tt[0][it] = 0
            USH_Tt[1][it] = 0
            for iT in range(2,Status.NT+2):
                USH_Tt[iT][it] = UPHProc_Tt[iT-2][it]*fDist

#..............................................................................
#..............................................................................
#..............................................................................
                
        Status.int.USHTotal_Tt = USH_Tt
        Status.int.UPHProcTotal_Tt = UPHProc_Tt
        Status.int.QHXProcTotal_Tt = QHXProc_Tt
        Status.int.QWHAmb_Tt = QWHAmb_Tt

        Status.int.USHTotal_T = Status.int.calcQ_T(USH_Tt)
        Status.int.UPHProcTotal_T = Status.int.calcQ_T(UPHProc_Tt)
        Status.int.QHXProcTotal_T = Status.int.calcQ_T(QHXProc_Tt)
        Status.int.QWHAmb_T = Status.int.calcQ_T(QWHAmb_Tt)
            
        
#------------------------------------------------------------------------------

if __name__ == "__main__":
    print "Testing ModuleHR"
    import einstein.GUI.pSQL as pSQL, MySQLdb
    from einstein.modules.interfaces import *
    from einstein.modules.energy.moduleEnergy import *
    stat = Status("testModuleHC")

    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    
    Status.PId = 99
    Status.ANo = 0
    Status.SetUpId = 1 #this is PSetUpData_ID
    
    Status.int = Interfaces()
    keys = ["HP Table","HP Plot","HP UserDef"]

    mod = ModuleHC(keys)
    
