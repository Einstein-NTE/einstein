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
#   Module for design of heat recovery system (HX network)
#
#==============================================================================
#
#   Version No.: 0.04
#   Created by:         Hans Schweiger  10/06/2008
#   Last revised by:
#                       Hans Schweiger  23/06/2008
#                       Hans Schweiger  02/07/2008
#                       Florian Joebstl 02/09/2008
#
#   Changes to previous version:
#
#   23/06/2008: HS  Query of fluids and fuels used in export XML
#   02/07/2008: HS  Function getHXData added -> obtains Fluid ID's in HX
#   02/09/2008: FJ  Call to PE2 external module
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
from einstein.modules.messageLogger import *
from subprocess import *

from einstein.modules.exportHR import *
from einstein.modules.importHR import *
from einstein.modules.dataHR import *

from einstein.GUI.dialog_changeHX import *

class ModuleHR(object):

    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel
        self.ExHX = True
        self.data = None

#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------
        Status.int.getEquipmentCascade() ##old code, dont know what its for...
        self.cascadeIndex = 0                  
        self.updatePanel()
            
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------
        if (self.data!=None):
            self.updateGridData()
            self.updateCurveData()

#------------------------------------------------------------------------------
    def updateGridData(self):
#------------------------------------------------------------------------------
# generates rows for the grid 
#------------------------------------------------------------------------------      
        dataList = []  
        for hx in self.data.hexers:
            opcost = float(hx["OMVar"])+float(hx["OMFix"])
            row = [hx["QdotHX"],hx["StorageSize"],hx["HXSource"],hx["HXTSourceInlet"],hx["HXTSourceOutlet"],hx["HXSink"],hx["HXTSinkInlet"],hx["HXTSinkOutlet"],hx["Area"],hx["TurnKeyPrice"],opcost]
            dataList.append(noneFilter(row))
        data = array(dataList)
        Status.int.setGraphicsData(self.keys[0], data)        
        
#------------------------------------------------------------------------------
    def updateCurveData(self):                 
#------------------------------------------------------------------------------
# stores data for mathplot in panelHR
#------------------------------------------------------------------------------  
        #Status.int.setGraphicsData(self.keys[1], self.data.curves)
        Status.int.hcg = self.data.curves
        #Status.int.yed = ...     
 
#------------------------------------------------------------------------------
    def deleteHX(self,index):   
#------------------------------------------------------------------------------
#called when "Delete HX"-Button pressed
#1) generates and adds 2 new streams
#2) deletes selected hx
#3) updates panel
#------------------------------------------------------------------------------    
        try:
            self.data.deleteHexAndGenStreams(index)           
            self.calcQdaList()
            self.updatePanel()
        except:
            print "deleting failed."

#------------------------------------------------------------------------------
    def changeHX(self,index):
#------------------------------------------------------------------------------
#
#todo...
#------------------------------------------------------------------------------
        try:
            dlg = DlgChangeHX(None)
            dlg.ShowModal()
        
            if (dlg.recalc):
                print "Recalc hx:"
                hx = self.data.hexers[index]
                
                WallThickness = 0.001
                Lambda        = 15.0
                AlphaL        = dlg.AlphaLiquid()
                AlphaG        = dlg.AlphaGas()
                AlphaC        = dlg.AlphaPC()
                
                if (dlg.MaterialType == HXConsts.MAT_TYPE_CS):
                    Lamda = 50.0                
                if (dlg.MaterialType == HXConsts.MAT_TYPE_CU):
                    Lamda = 80.0
                
                hot = Stream()
                hot.generateHotStreamFromHEX(hx)
                cold = Stream()
                cold.generateColdStreamFromHEX(hx)

                types = ['sst_liquid','sst_gaseous','sst_condensation']
                deltas = [ [10, 15, 7.5 ],[15,20,12.5],[7.5,12.5,5]]
                        
                hoti = types.index(hx["StreamStatusSource"])
                coldi= types.index(hx["StreamStatusSink"])
                delta_t_min = deltas[hoti][coldi]
                
                delta_T_in  = abs(hot.StartTemp - cold.EndTemp)   #?????
                delta_T_out = abs(hot.EndTemp   - cold.StartTemp) #?????                
                delta_T_max = max(delta_T_in,delta_T_out)
                delta_T_min = min(delta_T_in,delta_T_out)
                
                delta_T_logaritmic = (delta_T_max - delta_T_min)/log(delta_T_max / delta_T_min)
                
                #TODO....                
                
                #save db
                #load from db
                #update panel
        except e:
            print e
            pass
        

    def indexExists(self,index):
        if (len(self.data.hexers)>index):
            return True
        else:
            return False
                                    
#------------------------------------------------------------------------------
    def runHRModule(self):
#------------------------------------------------------------------------------
#   runs the calculations on the external HR module
#   1) create schedules (?OldCode?)
#   2) getHXData        (?OldCode?)
#   3) exports data into xml
#   4) calls external calculation
#   5) imports results from xml
#   6) store hxs in database
#   7) runSimulateHR
#   8) updatePanel 
#------------------------------------------------------------------------------
        if Status.schedules.outOfDate == True:
            Status.schedules.create()   #creates the process and equipment schedules

        #self.getHXData()
        #(fluidIDs,fuelIDs) = Status.prj.getFluidAndFuelList()     
                         
        XMLExportHRModule.export("inputHR.xml",Status.PId, Status.ANo,self.ExHX)
        # TODO call external calc
        try:
            retcode = call(['..\PE\ProcessEngineering.exe',"..\GUI\inputHR.xml","..\GUI\export.xml"], shell=True)
            print "External program returned: "+str(retcode)
            if (retcode!=0):
                raise
        except:
            print "Error in external program. EXIT "
                
        doc = XMLImportHRModule.importXML("export.xml")
                      
        self.data = HRData(Status.PId,Status.ANo)
        self.data.loadFromDocument(doc)
        
        self.calcQdaList()
        self.calcQaaList()
        
        self.simulateHR()
    
        self.updatePanel()
    
    
    
    def calcQdaList(self):        
        list_qda_ = []
        temperature_step = 5;
        for temperature in xrange(0, 406, temperature_step):
            list_qda_.append(0)
    
        print len(self.data.streams)
        temperature_step = 5;
        for temperature in xrange(0, 406, temperature_step):
            for stream in self.data.streams:                
                if (stream.HotColdType == "cold"):
                    if  ((temperature - stream.StartTemp) > 0) and ((temperature - stream.EndTemp) <= 0) and (stream.HeatType == "sensible"):                                                                                                                                    
                        list_qda_[temperature / temperature_step] += stream.HeatLoad / abs(stream.EndTemp - stream.StartTemp) * abs(temperature - stream.StartTemp) * stream.OperatingHours
                    else:
                        if (stream.HeatType == "latent")  and ((temperature - stream.EndTemp) <= 5) and ((temperature - stream.StartTemp) >= 0):
                            list_qda_[temperature / temperature_step] += stream.HeatLoad * stream.OperatingHours
                        
        Status.int.yed = list_qda_
        #print list_qda_
        
    def calcQaaList(self):        
        list_qaa_ = []
    
    #    temperature_step = 5;
     #   for temperature in xrange(0, 406, temperature_step):
    #        list_qaa_.append([])
    #        for stream in self.data.streams:
    #            if (stream.HotColdType == "cold"):
    #                if  ((temperature - stream.StartTemp) > 0) and (stream.HeatType == "sensible"):                                                                                                            
    #                    list_qda_[temperature / temperature_step].append(stream.HeatLoad / abs(stream.EndTemp - stream.StartTemp) * abs(temperature - stream.StartTemp) * stream.OperatingHours)  
    #                else:
    #                    if (stream.HeatType == "latent")  and ((temperature - stream.StartTemp) >= 0):
    #                        list_qda_[temperature / temperature_step].append( stream.HeatLoad * stream.OperatingHours)
                        
       # Status.int.yed.list_qaa_ = list_qaa_

   
    
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
        print("SIMULATE HR!!!")
        if Status.processData.outOfDate == True:
            Status.processData.createAggregateDemand()
            return ###????
            
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
            
        
    
