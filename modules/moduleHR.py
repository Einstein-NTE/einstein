# -*- coding: cp1252 -*-
#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#   ModuleHR (Heat Recovery)
#           
#------------------------------------------------------------------------------
#           
#   Module for heat recovery calculations
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by: 	Florian Joebstl, Hans Schweiger
#                       04/09/2008 - 18/10/2008
#
#   Update No. 003
#
#   Since Version 1.0 revised by:
#                       Hans Schweiger          21/10/2008
#                       Bettina Slawitsch       24/10/2008
#                       Hans Schweiger          08/04/2009
#
#   Changes to previous version:
#
#   21/10/2008: HS  calculation of QD/QA and update of cascadeUpdateLevel
#                   in HX Design
#   24/10/2008: BS  update of HEX cost correlations and material properties
#   08/04/2009: HS  waste heat from equipments added into calculation of
#                   QWHAmb
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

import sys
from math import *
from numpy import *

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP
from einstein.modules.constants import *
from einstein.modules.messageLogger import *
from subprocess import *

from einstein.modules.exportHR import *
from einstein.modules.importHR import *
from einstein.modules.dataHR import *

from einstein.GUI.dialog_changeHX import *

from einstein.GUI.dialogGauge import DialogGauge


class ModuleHR(object):

    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel
        self.ConCondensation = False
        self.HiddenHX = []
        self.data = HRData(Status.PId,Status.ANo)
        self.data.loadDatabaseData()   
                  
#----------------------------------------------------------------------------------------------------
# GUI Interaction
#----------------------------------------------------------------------------------------------------
    def initPanel(self):                      
        if (Status.PId != self.data.pid)or(Status.ANo!=self.data.ano):
              self.data = HRData(Status.PId,Status.ANo)                                 
        self.__updatePanel()
            

    def __updatePanel(self):
        if (self.data!=None):
            self.data.loadDatabaseData()  
            self.__updateGridData()
            self.__updateReportData()
            self.__updateCurveData()


    def __updateGridData(self): 
        try:     
            dataList = []  
            index = 0
            for hx in self.data.hexers:
                try:
                    opcost = float(hx["OMVar"])+float(hx["OMFix"])
                    opcost_str = str(opcost)
                except:
                    opcost_str = ""
                name = hx["HXName"]
                
                if (index in self.HiddenHX):
                    name=name+" (hidden)"
                
                StorageSize = "%.2f" % float(hx["StorageSize"])
                Surface = "%.2f" % float(hx["Area"])
                TurnKeyPrice = "%.0f" % float(hx["TurnKeyPrice"])
                opcost_str = "%.2f" % float(opcost_str)
                
                row = [name,hx["QdotHX"],StorageSize,hx["HXSource"],hx["HXTSourceInlet"],hx["HXTSourceOutlet"],hx["HXSink"],hx["HXTSinkInlet"],hx["HXTSinkOutlet"],Surface,TurnKeyPrice,opcost_str]
                dataList.append(noneFilter(row))
                index+=1
            data = array(dataList)
            Status.int.setGraphicsData(self.keys[0], data)
        except:
            logDebug("(moduleHR.py) UpdateGridData: Create rows failed")        
        
    def __updateReportData(self): 
        try:     
            qTotal = 0.0
            qdotTotal = 0.0
            for hx in self.data.hexers:
                q = hx["QHX"]
                if q is not None:
                    qTotal += q

                qdot = hx["QdotHX"]
                if qdot is not None:
                    qdotTotal += qdot

            dataListReport = []  
            index = 0
            
            for hx in self.data.hexers:
                
                q = hx["QHX"]
                if qTotal > 0 and q is not None: qhxperc = 100.0*q/qTotal
                else: qhxperc = "---"
                
                row = [hx["HXName"],hx["QdotHX"],hx["HXSource"],hx["HXSink"],hx["QHX"],qhxperc]
                if index < 20:
                    dataListReport.append(noneFilter(row))
                elif index == 20:
                    logDebug("More than 20 HX in the system. Do not fit into the report")
                index+=1

            for i in range(index,20):
                row = [" "," "," "," "," "," "]
                dataListReport.append(row)

            row = [_("Total"),qdotTotal," "," ",qTotal,100.0]
            dataListReport.append(row)
            
            dataReport = array(dataListReport)

            key = "HX%02d"%Status.ANo
#            print "%s\n"%key,dataReport
            Status.int.setGraphicsData(key, dataReport)
            
        except:
            logDebug("(moduleHR.py) UpdateReportData: Create rows failed")        
        
    def __updateCurveData(self):                 
        # stores data for mathplot in panelHR         
        Status.int.hrdata = self.data
        
#----------------------------------------------------------------------------------------------------
# Public Methodes
#----------------------------------------------------------------------------------------------------   
                         
    def runHRDesign(self,exhx = True):        
        dlg = DialogGauge(Status.main,_("EINSTEIN heat recovery module"),_("calculating"))
        self.__runPE2(redesign = True,concondensation = self.ConCondensation, exhx = exhx)
        dlg.update(50.0)
        
        self.__doPostProcessing()
        dlg.update(99.0)

        self.__updatePanel()

### HS2008-10-21: this block is necessary in order to update global demand
# arrays that will be used in the system simulation
        Status.int.QD_Tt = Status.int.createQ_Tt()   
        Status.int.QA_Tt = Status.int.createQ_Tt()

        for iT in range(Status.NT+2):
            for it in range(Status.Nt):
                Status.int.QD_Tt[iT][it] = Status.int.USHTotal_Tt[iT][it]
                Status.int.QA_Tt[iT][it] = Status.int.QWHAmb_Tt[iT][it]

        Status.int.QD_T = Status.int.calcQ_T(Status.int.QD_Tt)
        Status.int.QA_T = Status.int.calcQ_T(Status.int.QA_Tt)

        logTrack("Aggregate demand = %s"%str(Status.int.QD_T))

        Status.int.initCascadeArrays(0) #start

### HS2008-10-21: END BLOCK
                      
        dlg.Destroy()

    def runHRModule(self,exhx = True):
        dlg = DialogGauge(Status.main,_("EINSTEIN heat recovery module"),_("calculating"))
        redesign_network_flag = None
        if Status.HRTool == "estimate":
            self.__estimativMethod()
        else:
            self.__runPE2(redesign = False,concondensation = self.ConCondensation)
            
            dlg.update(50.0)
            self.__doPostProcessing()               

        dlg.update(99.0)

        self.__updatePanel()

        dlg.Destroy()

#----------------------------------------------------------------------------------------------------
# Internal Calculations
#----------------------------------------------------------------------------------------------------  

    def __runPE2(self,redesign = True, concondensation = False , exhx = True):        
        if (redesign):
            logWarning(_("Redesigning HX network. This may take some time. (Tool: PE2)"))
            redesign_network_flag = "t"
        else:
            logWarning(_("Recalculating HX network. This may take some time.(Tool: PE2)"))
            redesign_network_flag = "f"
        
        if (concondensation):
            con_condensation_flag = "t"
        else:
            con_condensation_flag = "f"
                                            
        if Status.schedules.outOfDate == True:
            Status.schedules.create()   #creates the process and equipment schedules
                         
        XMLExportHRModule.export("inputHR.xml",Status.PId, Status.ANo,exhx)
        
        try:
            args = ['..\PE\ProcessEngineering.exe',"..\GUI\inputHR.xml","..\GUI\export.xml",redesign_network_flag,con_condensation_flag]
            retcode = call(args, shell=True)
            logDebug(_("External program returned: ")+str(retcode))
            if (retcode!=0):
                raise
        except:
            logError(_("Error in external program (ProcessEngineering.exe)"))                      
        else:    
            doc = XMLImportHRModule.importXML("export.xml")                      
            self.data = HRData(Status.PId,Status.ANo)
                        
            if (redesign):
                self.data.loadFromDocument(doc,overrideHX = True)
            else:
                self.data.loadFromDocument(doc,overrideHX = False)
                    

    
#------------------------------------------------------------------------------
    def __doPostProcessing(self):
#------------------------------------------------------------------------------
# starts all (internal) calculations
#------------------------------------------------------------------------------        

#   calculate aggregate heat demand and waste heat availability
        if Status.processData.outOfDate == True:
            Status.processData.createAggregateDemand()
            return #HR module is called again 
            
        UPH_Tt = Status.int.UPHTotal_Tt
        UPHw_Tt = Status.int.UPHwTotal_Tt

# Arrays that need to be calculated (output for further processing)

        QHXProc_Tt = Status.int.createQ_Tt()    # heat recovered for process heating
        USH_Tt = Status.int.createQ_Tt()        # heat demand at entry of pipes

        UPHProc_Tt = copy.deepcopy(UPH_Tt)      # initial value = UPH. will be reduced by QHX
        UPHProc_T = Status.int.calcQ_T(UPHProc_Tt)

        QWHAmb_Tt = copy.deepcopy(UPHw_Tt)      # initial value = UPHw (QWHProc) + QWHEq. will be reduced by QHX
#        self.__getQWHEqTotal()                  # calculates the total equipment waste heat flow
#        QWHAmb_Tt = Status.int.createQ_Tt()
        print "UPH_T = %r"%UPHProc_T

        UPHw_T = Status.int.calcQ_T(UPHw_Tt)
        print "UPHw_T = %r"%UPHw_T
        
        for iT in range(Status.NT+2):
            for it in range(Status.Nt):
                QWHAmb_Tt[iT][it] += Status.int.QWHEqTotal_Tt[iT][it]
        
        QWHAmb_T = Status.int.calcQ_T(QWHAmb_Tt)
        print "QWHAmb_T = %r"%QWHAmb_T
        
#..............................................................................
# read in PE2 result - remaining yearly demand and calculate QHX_T by difference

        QHX_T_res = Status.int.createQ_T()

        self.__calcQD_T()
        self.__calcQA_T()

        for iT in range(Status.NT+2):
            QHX_T_res[iT] = max(Status.int.UPHTotal_T[iT] - self.data.QD_T[iT],0.0)
            iTw = min(iT+2,Status.NT+1)
            QHX_T_res[iT] = min(QHX_T_res[iT],QWHAmb_T[2])     #necessary, because waste heat from
                                                                #exhaust gas not available ...       

        print "QD_T = %r"%self.data.QD_T
        print "QHX_T_res = %r"%QHX_T_res

#..............................................................................
# now distribute QHX_T to the time intervals

        dQHX_T =Status.int.createQ_T()   #exchanged heat correspon
                
        for timeShift in range(0,25):  # maximum one day time shift ... if that's not enough send error message !!!

            dQHX_Tt = self.__maxHRPotential(UPHProc_Tt,QWHAmb_Tt,timeShift)

            dQHXmax_T = Status.int.calcQ_T(dQHX_Tt)    # maximum heat recovery as reference for calculating fR
            print "dQHXmax(%s) = %r"%(timeShift,dQHXmax_T)

            dQHX_T[0] = 0

            for iT in range(1,Status.NT+2):
                dQHX_T[iT] = min(dQHXmax_T[iT],QHX_T_res[iT])
                maxSlopeD = max(UPHProc_T[iT] - UPHProc_T[iT-1],0.0)

                iTw = iT+2

                if iTw <= Status.NT+2:
                    maxSlopeA = max(QWHAmb_T[iTw-1],0.0)
                else:
                    maxSlopeA = 0.0
                
                maxSlope = min(maxSlopeA,maxSlopeD)

                dQHX_T[iT] = min(dQHX_T[iT],dQHX_T[iT-1]+maxSlope)

                if dQHXmax_T[iT] > 0:
                    fR = dQHX_T[iT]/dQHXmax_T[iT]
                else:
                    fR = 0.0

                for it in range(Status.Nt):
                    dQHX_Tt[iT][it] *= fR #correction real vs. theoretical (maximum) heat recovery
                    QHXProc_Tt[iT][it] += dQHX_Tt[iT][it]
                    UPHProc_Tt[iT][it] -= dQHX_Tt[iT][it]


            UPHProc_T = Status.int.calcQ_T(UPHProc_Tt)
            dQHX_T = Status.int.calcQ_T(dQHX_Tt)    # real heat recovery corresponding to this time shift

# substract exchanged heat from 
            for iT in range(Status.NT+2):
                QHX_T_res[iT] -= dQHX_T[iT]
                QHX_T_res[iT] = max(QHX_T_res[iT],0.0)

            for it in range(Status.Nt):

                itw = (it + Status.Nt - timeShift)%Status.Nt
                
                for iTw in range(Status.NT+2):
                    iT = max(iTw-2,0)
                    QWHAmb_Tt[iTw][itw] -= (dQHX_Tt[Status.NT+1][it] - dQHX_Tt[iT][it])

            QWHAmb_T = Status.int.calcQ_T(QWHAmb_Tt)

########## HS2008-10-18: restrict number of iterations (timeShifts)as otherwise calculation time
# gets unnecessarily long
# there are small numeric errors between PE2 and Einstein, and Exhaust Gas is not yet in EINSTEIN's
# internal waste heat treatment, so ... in order to survive for the moment ...
# XXX XXX 2B CHECKED 2B CHECKED 2B CHECKED 2B CHECKED 2B CHECKED 2B CHECKED 2B CHECKED 2B CHECKED 

            if QHX_T_res[Status.NT+1] < 0.01*UPHProc_T[Status.NT+1]:
                break

            elif timeShift == 24:
                logDebug("ModuleHR (__doPostProcessing): time shift of 168 hours not enough for realising PE2 HR potential")
            
#..............................................................................
# settings of the conversion UPH -> USH

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
                           
#..............................................................................
# from UPHext to USH: shift in temperature (10 K) and divide by distribution efficiency

        for it in range(Status.Nt):
            
            USH_Tt[0][it] = 0
            USH_Tt[1][it] = 0
            for iT in range(2,Status.NT+2):
                USH_Tt[iT][it] = UPHProc_Tt[iT-2][it]*fDist

#..............................................................................
#..............................................................................
#..............................................................................

# Assignment to global arrays in Interfaces

        Status.int.USHTotal_Tt = USH_Tt
        Status.int.UPHProcTotal_Tt = UPHProc_Tt
        Status.int.QHXProcTotal_Tt = QHXProc_Tt
        Status.int.QWHAmb_Tt = QWHAmb_Tt

        Status.int.USHTotal_T = Status.int.calcQ_T(USH_Tt)
        Status.int.UPHProcTotal_T = Status.int.calcQ_T(UPHProc_Tt)
        Status.int.QHXProcTotal_T = Status.int.calcQ_T(QHXProc_Tt)
        Status.int.QWHAmb_T = Status.int.calcQ_T(QWHAmb_Tt)

        print "ModuleHR (__doPostProc.): USHTotal_T = ",Status.int.USHTotal_T
        print "ModuleHR (__doPostProc.): UPHProcTotal_T = ",Status.int.UPHProcTotal_T
        print "ModuleHR (__doPostProc.): QHXProcTotal_T = ",Status.int.QHXProcTotal_T
        print "ModuleHR (__doPostProc.): QWHAmb_T = ",Status.int.QWHAmb_T
            
#------------------------------------------------------------------------------
    def __maxHRPotential(self,UPH_Tt,QWH_Tt,timeShift):
#------------------------------------------------------------------------------
#       returns a vector with the maximum heat recovery potential
#       for a given time and temperature shift
#       for simplicity at the moment temperature shift = fix:
#       10 K (2 temperature intervals)
#------------------------------------------------------------------------------

        QHX_Tt = Status.int.createQ_Tt()    # heat recovered for process heating
        
#..............................................................................
#..............................................................................
#..............................................................................

        for it in range(Status.Nt):

            itw = (it + Status.Nt - timeShift)%Status.Nt

#..............................................................................

#first invert QWH curve and shift 2 temperature intervals (DTmin)

            QWH_max = QWH_Tt[2][itw]   
            
            for iT in range(Status.NT):
                QHX_Tt[iT][it] = (QWH_max - QWH_Tt[iT+2][itw])  #maximum available energy
            QHX_Tt[Status.NT][it]   = QHX_Tt[Status.NT-1][it]         #includes shift by DTmin
            QHX_Tt[Status.NT+1][it] = QHX_Tt[Status.NT-1][it]

#then shift so that QHX always < UPH -> = Hot Composite Curve
            shift = 0.0
            for iT in range(Status.NT+2):
                shift = max(shift,QHX_Tt[iT][it]-UPH_Tt[iT][it])      #assure that QHXProc < UPH

            for iT in range(Status.NT+2):
                QHX_Tt[iT][it] = max(0.0,QHX_Tt[iT][it]-shift)          # = shift of HCC in Q
            
        return QHX_Tt        

#------------------------------------------------------------------------------
# Matrix and List calculation
#------------------------------------------------------------------------------    
    def __calcQD_T(self): 

        streams = self.data.streams[:]
        hidden  = self.data.getStreamsFromHiddenHX(self.HiddenHX)
        for stream in hidden:
            streams.append(stream)
           
        QD_T = []
        temperature_step = 5;
        for temperature in xrange(0, 406, temperature_step):
            QD_T.append(0)
    
        temperature_step = 5;
        for temperature in xrange(0, 406, temperature_step):
            for stream in streams:
                if (stream.HotColdType == "cold"):
                    if  ((temperature - stream.StartTemp) > 0) and (stream.HeatType == "sensible"):  
                        if (temperature <= stream.EndTemp):                                                                                                                                  
                            QD_T[temperature / temperature_step] += stream.HeatLoad / abs(stream.EndTemp - stream.StartTemp) * abs(temperature - stream.StartTemp) * stream.OperatingHours
                        else:
                            QD_T[temperature / temperature_step] += stream.HeatLoad * stream.OperatingHours
                    else:
                        if (stream.HeatType == "latent")  and ((temperature - stream.StartTemp) >= 0):
                            QD_T[temperature / temperature_step] += stream.HeatLoad * stream.OperatingHours
                        
        self.data.QD_T = QD_T
        
    def __calcQA_T(self):      
        streams = self.data.streams[:]
        hidden  = self.data.getStreamsFromHiddenHX(self.HiddenHX)
        for stream in hidden:
            streams.append(stream)
          
        QA_T = []
        temperature_step = 5;
        for temperature in xrange(0, 406, temperature_step):
            QA_T.append(0)
    
        temperature_step = 5;
        for temperature in xrange(406, 0, -temperature_step):
            for stream in streams:                
                if (stream.HotColdType == "hot"):
                    if  ((temperature - stream.StartTemp) <= 0) and (stream.HeatType == "sensible"):  
                        if (temperature >= stream.EndTemp):                                                                                                                                  
                            QA_T[temperature / temperature_step] += stream.HeatLoad / abs(stream.EndTemp - stream.StartTemp) * abs(temperature - stream.StartTemp) * stream.OperatingHours
                        else:
                            QA_T[temperature / temperature_step] += stream.HeatLoad * stream.OperatingHours
                    else:
                        if (stream.HeatType == "latent")  and ((temperature - stream.StartTemp) <= 0):
                            QA_T[temperature / temperature_step] += stream.HeatLoad * stream.OperatingHours
                        
        self.data.QA_T = QA_T
   
    
    def __calcQD_Tt(self):
        streams = self.data.streams[:]
        hidden  = self.data.getStreamsFromHiddenHX(self.HiddenHX)
        for stream in hidden:
            streams.append(stream)
            
        temperature_step = 5
        time_step        = 1
        
        QD_Tt = []

        for hours in xrange(0,8760,time_step):
            QD_Tt.append([])
            for temperature in xrange(0,406,temperature_step):
                QD_Tt[hours/time_step].append(0)
        
        for hours in xrange(0,8760,time_step):
            for temperature in xrange(0,406,temperature_step):
                for stream in streams:                
                    if (stream.HotColdType == "cold"):
                        if (hours < stream.OperatingHours):                            
                            if  ((temperature - stream.StartTemp) > 0) and (stream.HeatType == "sensible"):  
                                if (temperature <= stream.EndTemp):
                                    QD_Tt[hours/time_step][temperature/temperature_step]+= stream.HeatLoad / abs(stream.EndTemp - stream.StartTemp) * abs(temperature - stream.StartTemp) * stream.OperatingHours / (stream.OperatingHours / time_step)                                       
                                else:
                                    QD_Tt[hours/time_step][temperature/temperature_step]+= stream.HeatLoad * stream.OperatingHours / (stream.OperatingHours / time_step)
                            else:
                                if (stream.HeatType == "latent")  and ((temperature - stream.StartTemp) >= 0):
                                    QD_Tt[hours/time_step][temperature/temperature_step]+= stream.HeatLoad * stream.OperatingHours / (stream.OperatingHours / time_step)
        self.data.QD_Tt = QD_Tt     
#        self.debugPrint("QD_Tt.csv", QD_Tt)     
    
    
    def __calcQA_Tt(self):
        streams = self.data.streams[:]
        hidden  = self.data.getStreamsFromHiddenHX(self.HiddenHX)
        for stream in hidden:
            streams.append(stream)
            
        temperature_step = 5
        time_step        = 1
        
        QA_Tt = []
        
        for hours in xrange(0,8760,time_step):
            QA_Tt.append([])
            for temperature in xrange(0,406,temperature_step):
                QA_Tt[hours/time_step].append(0)
                
        for hours in xrange(0,8760,time_step):  
            for temperature in xrange(406,0,-temperature_step):                      
                for stream in streams:                
                    if (stream.HotColdType == "hot"):
                        if (hours < stream.OperatingHours):                            
                            if  ((temperature - stream.StartTemp) <= 0) and (stream.HeatType == "sensible"):  
                                if (temperature >= stream.EndTemp):
                                    QA_Tt[hours/time_step][temperature/temperature_step]+= stream.HeatLoad / abs(stream.EndTemp - stream.StartTemp) * abs(temperature - stream.StartTemp) * stream.OperatingHours / (stream.OperatingHours / time_step)                                       
                                else:
                                    QA_Tt[hours/time_step][temperature/temperature_step]+= stream.HeatLoad * stream.OperatingHours / (stream.OperatingHours / time_step)
                            else:
                                if (stream.HeatType == "latent")  and ((temperature - stream.StartTemp) <= 0):
                                    QA_Tt[hours/time_step][temperature/temperature_step]+= stream.HeatLoad * stream.OperatingHours / (stream.OperatingHours / time_step)
        self.data.QA_Tt = QA_Tt
        #self.debugPrint("QA_Tt.csv", QA_Tt)   


#------------------------------------------------------------------------------
    def ShowHideHX(self,index):   
#------------------------------------------------------------------------------
#called when "Show/HideHX"-Button pressed
#1) adds or removes the index of the hx to the/fromthe hide list
#2) redo result postprocessing
#------------------------------------------------------------------------------    
        try:
            if index in self.HiddenHX:
                self.HiddenHX.remove(index)
            else: 
                self.HiddenHX.append(index)
            #self.data.deleteHexAndGenStreams(index)                       
        except:
            logError(_("Could not delete HEX"))
            logDebug("(moduleHR.py) deleteHX: deleting failed.")
        try:
            self.__doPostProcessing()  
            self.__updatePanel()
        except:
            logError(_("Recalculation failed."))
            
     
#------------------------------------------------------------------------------
    def changeHX(self,index):
#------------------------------------------------------------------------------
# recalculates cost values for HEX
# uses values from DlgChangeHX
# changes HXType, TurnKeyPrice and OMFix of a single HEX
#------------------------------------------------------------------------------
        try:
            try:
                hx = self.data.hexers[index]
                dlg = DlgChangeHX(None)
            
                types = ['sst_liquid','sst_gaseous','sst_condensation']
                hoti = types.index(hx["StreamStatusSource"])
                coldi= types.index(hx["StreamStatusSink"])
            
                dlg.LockChoices(hoti,coldi)
                dlg.ShowModal()
            except:
                logError(_("SteamStatusSink/StreamStatusSource not defined. Can't do recalculation"))
                return
        
            if (dlg.recalc):
#                print "Recalc hx:"
                #calculation of hx cost             
                wall_thickness = 0.001
                Lambda         = 15.0
                AlphaL         = dlg.AlphaLiquid()
                AlphaG         = dlg.AlphaGas()
                AlphaC         = dlg.AlphaPC()
                
                material_type = dlg.MaterialType()
                if (material_type == HXConsts.MAT_TYPE_CS):
                    Lambda = 50.0                
                if (material_type == HXConsts.MAT_TYPE_CU):
                    Lambda = 80.0
                
                hot = Stream()
                hot.generateHotStreamFromHEX(hx)
                cold = Stream()
                cold.generateColdStreamFromHEX(hx)
                
                deltas = [ [10.0, 15.0, 7.5 ],[15.0,20.0,12.5],[7.5,12.5,5.0]]   #0=liquid, 1=gas, 2=cont
                alphas = [AlphaL,AlphaG,AlphaC]                        #0=liquid, 1=gas, 2=cont                                                      
                alpha_hot_stream  = alphas[hoti]
                alpha_cold_stream = alphas[coldi]                                              
                
                delta_T_in  = abs(hot.StartTemp - cold.EndTemp)   
                delta_T_out = abs(hot.EndTemp   - cold.StartTemp)                 
                delta_T_max = max(delta_T_in,delta_T_out)
                delta_T_min = min(delta_T_in,delta_T_out)
                
                delta_T_logaritmic = (delta_T_max - delta_T_min)/log10(delta_T_max / delta_T_min)
                
                one_div_k = 1 / alpha_hot_stream + wall_thickness / Lambda + 1 / alpha_cold_stream
                k         = 1 / one_div_k
                area_value= float(hx["QdotHX"]) / ((k / 1000) * delta_T_logaritmic)
                
                hxtype = dlg.HXType(hoti,coldi)
                
                if (hxtype == HXConsts.HX_TYPE_P):
#                    print "PLATE"
                    K1 =  4.6656
                    K2 = -0.1557
                    K3 =  0.1547
                    C1 =  0
                    C2 =  0
                    C3 =  0
                    B1 =  0.96
                    B2 =  1.21       
                    material_factor = 0
                    if (material_type == "SS"):
                        material_factor = 2.45                                    
                    if (material_type == HXConsts.MAT_TYPE_CS):
                        material_factor = 1.00
                    if (material_type == HXConsts.MAT_TYPE_NI):
                        material_factor = 2.68             
                    if (material_type == HXConsts.MAT_TYPE_CU):
                        material_factor = 1.35 
                                
                elif (hxtype == HXConsts.HX_TYPE_S):  
#                    print "SHELL"              
                    K1 =  3.9912
                    K2 =  0.0668
                    K3 =  0.243
                    C1 =  -0.4045
                    C2 =  0.1859
                    C3 =  0
                    B1 =  1.75
                    B2 =  1.55
                    
                    material_factor = 0
                    if (material_type == "SS"):                      
                        material_factor = 2.73                
                    if (material_type == HXConsts.MAT_TYPE_CS):
                        material_factor = 1.00
                    if (material_type == HXConsts.MAT_TYPE_NI):
                        material_factor = 3.73             
                    if (material_type == HXConsts.MAT_TYPE_CU):
                        material_factor = 1.69  
                 
                
                purchased_cost = pow(10,K1 + K2 * log10(area_value)+ K3 * log10(area_value)*log10(area_value))
                pressure_value  = dlg.PressureValue()
                pressure_factor = pow(10,C1 + C2*log10(pressure_value) + C3*log10(pressure_value)*log10(pressure_value))
                
                bare_module_factor = B1 + B2 * material_factor * pressure_factor
                cepci_2001 = 394.3
                cepci_2008 = 539.7
                USD_EUR_ratio = 1.55
                
                v2001_USD_cost = purchased_cost*bare_module_factor
                v2008_USD_cost = v2001_USD_cost * cepci_2008 / cepci_2001
                v2008_EUR_cost = v2008_USD_cost / USD_EUR_ratio 
                                                
                add_perc_cost = dlg.AdditionalCostPercent()
                v2008_EUR_cost_new = v2008_EUR_cost - 0.22*v2008_EUR_cost + (0.22+add_perc_cost/100.0) * v2008_EUR_cost

                if (v2008_EUR_cost_new / area_value > 5000):                    
                    x = area_value/50000.0
                    v2008_EUR_cost_new = v2008_EUR_cost_new * 0.4 * exp(-x)
                if (area_value < 10):
                    v2008_EUR_cost_new = area_value * 2000;                        
                if (area_value < 1):                    
                    v2008_EUR_cost_new = area_value * 10000;

                HEX_OMcost = v2008_EUR_cost_new / 15 \
                             + 0.004*v2008_EUR_cost_new \
                             + 0.01*v2008_EUR_cost_new
                
#                print "pressure_factor:" + str(pressure_factor)
#                print "pressure_value:" + str(pressure_value)
#                print "purcase_cost:" + str(purchased_cost)
#                print "bare_module_factor: " + str(bare_module_factor)
#                print "2008_EUR_cost: "+str(v2008_EUR_cost)
#                print "2008_EUR_cost_new (TurnKeyPrice): "+str(v2008_EUR_cost_new)  
#                print "OMFix[EUR]:"+str(HEX_OMcost)
             
                #store new information in Database
                query = "UPDATE qheatexchanger SET HXType='%s', TurnKeyPrice=%s, OMFix=%s, Area=%s" % (hxtype,v2008_EUR_cost_new,HEX_OMcost,area_value)
                query +="WHERE QHeatExchanger_ID=%s;" % (hx["QHeatExchanger_ID"])
                Status.DB.sql_query(query)
                
                #updateInformation in panel                                                                           
                self.__updatePanel()

        except Exception, inst:
            logTrack("error in HEX recalculation")
            logTrack(type(inst))
            logTrack(inst.args)
            logTrack(inst)
            logError(_("Recalculation of HEX failed."))         



#------------------------------------------------------------------------------
    def __estimativMethod(self):
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
            return
            
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

#first invert UPHw curve and shift 2 temperature intervals (DTmin)

            UPHw_max = UPHw_Tt[2][it]   
            
            for iT in range(Status.NT):
                QHXProc_Tt[iT][it] = fHR*(UPHw_max - UPHw_Tt[iT+2][it])  #maximum available energy
            QHXProc_Tt[Status.NT][it]   = QHXProc_Tt[Status.NT-1][it]         #includes shift by DTmin
            QHXProc_Tt[Status.NT+1][it] = QHXProc_Tt[Status.NT-1][it]

#then shift so that QHXProc always < UPH -> = Hot Composite Curve
            shift = 0.0
            for iT in range(Status.NT+2):
                shift = max(shift,QHXProc_Tt[iT][it]-UPH_Tt[iT][it])      #assure that QHXProc < UPH

            for iT in range(Status.NT+2):
                QHXProc_Tt[iT][it] = max(0.0,QHXProc_Tt[iT][it]-shift)                                        # = shift of HCC in Q
            
#substract recovered heat from total available waste heat -> QHWAmb
            QHXProc_max = QHXProc_Tt[Status.NT+1][it]
            QWHAmb_Tt[0][it] = UPHw_Tt[0][it]
            QWHAmb_Tt[1][it] = UPHw_Tt[1][it]
            for iT in range(2,Status.NT+2):
                QWHAmb_Tt[iT][it] = UPHw_Tt[iT][it] - (QHXProc_max-QHXProc_Tt[iT-2][it])

#substract recovered heat from demand -> UPHProc
            for iT in range(Status.NT+2):
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
    def __doPostProcessing_OldStuff(self):
#------------------------------------------------------------------------------
# starts all (internal) calculations
#------------------------------------------------------------------------------        
        self.__calcQD_T()
        self.__calcQA_T()
        self.__calcQD_Tt()
        self.__calcQA_Tt()

#------------------------------------------------------------------------------
#   HS: From here on necessary functions of the original simulateHR
#------------------------------------------------------------------------------
        if Status.processData.outOfDate == True:
            Status.processData.createAggregateDemand()
            return ###????
            
# Arrays that need to be calculated (output for further processing)

        QHXProc_Tt = Status.int.createQ_Tt()    # heat recovered for process heating
        UPHProc_Tt = Status.int.createQ_Tt()    # heat supplied externally to processes
        USH_Tt = Status.int.createQ_Tt()        # heat demand at entry of pipes
        QWHAmb_Tt = Status.int.createQ_Tt()     # remaining waste heat that currently is dissipated

# Results imported from previous calculations (in calculateAggregateDemand)

        UPH_Tt = Status.int.UPHTotal_Tt
        UPHw_Tt = Status.int.UPHwTotal_Tt

#..............................................................................
# importation of PE results on heat recovery

#HS: Florian - the order of temperature and time index in our arrays are changed
# maybe all this can be quite simplified ...

        QDInData = 0.0
        QAInData = 0.0
        for iT in range(Status.NT+2):
            for it in range(Status.Nt):
                UPHProc_Tt[iT][it] = self.data.QD_Tt[it][iT]    # heat supplied externally to processes
                QWHAmb_Tt[iT][it] = self.data.QA_Tt[it][iT]      # remaining waste heat that currently is dissipated

#                print ("[%2d][%4d] QD %s QA %s "%(iT,it,self.data.QD_Tt[it][iT],self.data.QA_Tt[it][iT]))

                if iT == (Status.NT+1):
                    QDInData += self.data.QD_Tt[it][iT]

                if iT == 0:
                    QAInData += self.data.QA_Tt[it][iT]
                
#        print "ModuleHR (doPostProcessing): QD %s QA %s "%(QDInData/1000,QAInData/1000)
#..............................................................................
# settings of the conversion UPH -> USH

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

# calculating QHXProc by difference: UPH = UPHProc + QHXProc
        for it in range(Status.Nt):
            for iT in range(Status.NT+2):
                QHXProc_Tt[iT][it] = UPH_Tt[iT][it] - UPHProc_Tt[iT][it]
                           
#..............................................................................
# from UPHext to USH: shift in temperature (10 K) and divide by distribution efficiency

            USH_Tt[0][it] = 0
            USH_Tt[1][it] = 0
            for iT in range(2,Status.NT+2):
                USH_Tt[iT][it] = UPHProc_Tt[iT-2][it]*fDist

#..............................................................................
#..............................................................................
#..............................................................................

# Assignment to global arrays in Interfaces

        Status.int.USHTotal_Tt = USH_Tt
        Status.int.UPHProcTotal_Tt = UPHProc_Tt
        Status.int.QHXProcTotal_Tt = QHXProc_Tt
        Status.int.QWHAmb_Tt = QWHAmb_Tt

        Status.int.USHTotal_T = Status.int.calcQ_T(USH_Tt)
        Status.int.UPHProcTotal_T = Status.int.calcQ_T(UPHProc_Tt)
        Status.int.QHXProcTotal_T = Status.int.calcQ_T(QHXProc_Tt)
        Status.int.QWHAmb_T = Status.int.calcQ_T(QWHAmb_Tt)
        
#------------------------------------------------------------------------------
    def __getQWHEqTotal(self):
#------------------------------------------------------------------------------
# calculates the total of waste heat for the equipments
#------------------------------------------------------------------------------        

        Status.int.QWHEqTotal_Tt = Status.int.createQ_Tt()
        
        for j in range(Status.NEquipe):
            for iT in range(Status.NT+2):
                for it in range(Status.Nt):
                    Status.int.QWHEqTotal_Tt[iT][it] += Status.int.QWHj_Tt[j][iT][it]
                    
        Status.int.QWHEqTotal_T = Status.int.calcQ_T(Status.int.QWHEqTotal_Tt)
                    
#------------------------------------------------------------------------------
# Helpers
#------------------------------------------------------------------------------
    def indexExists(self,index):
        if (len(self.data.hexers)>index):
            return True
        else:
            return False
                            
                            
    def debugPrint(self,name,obj):
        saveout = sys.stdout
        fsock = open(name,'w')
        sys.stdout = fsock
        for row in obj:
            strrow = ""
            for value in row:     
                strrow=strrow+str(value)+","
            print strrow
        sys.stdout = saveout
        fsock.close()   
  
