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
#	ModuleEnergy
#			
#------------------------------------------------------------------------------
#			
#	Module for simulation of energy flows in the system
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by: 	Hans Schweiger, Tom Sobota, Enrico Facci, Stoyan Danov
#                       13/03/2008 - 02/08/2008
#
#   Update No. 001
#
#   Since Version 1.0 revised by:
#                       Hans Schweiger          21/07/2009
#
#   21/07/2009: HS  Iterative cycle in runSimulation introduced
#	
#------------------------------------------------------------------------------		
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008, 2009
#	www.energyxperts.net / info@energyxperts.net
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license v3 as published by the Free
#	Software Foundation (www.gnu.org).
#
#============================================================================== 

from sys import *
from math import *
from numpy import *
import copy

from einstein.modules.constants import *
from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.messageLogger import *
from einstein.GUI.dialogGauge import DialogGauge

#============================================================================== 
#============================================================================== 
class ModuleEnergy(object):
#============================================================================== 
#============================================================================== 

#------------------------------------------------------------------------------
    def __init__(self, keys):
#------------------------------------------------------------------------------
        self.keys = keys
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
        logTrack("ModuleEnergy (initPanel)")
        pass #there's nothing to do at panel start-up
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#        carries out any calculations necessary previous to displaying the BB
#        design assitant window
#------------------------------------------------------------------------------

#............................................................................................
# Plot global energy data

        Status.mod.moduleEA.update()

        (projectData,generalData) = Status.prj.getProjectData()

        PET = generalData.PET
        if PET is not None: PET /= 1000.0
        else: PET = "---"
        
        PETFuels = generalData.PETFuels
        if PETFuels is not None: PETFuels /= 1000.0
        else: PETFuels = "---"
        
        PETel = generalData.PETel
        if PETel is not None: PETel /= 1000.0
        else: PETel = "---"
        
        USH = generalData.USH
        if USH is not None: USH /= 1000.0
        else: USH = "---"
        
        UPH = generalData.UPH
        if UPH is not None: UPH /= 1000.0
        else: UPH = "---"
        
        
        row = [PET,PETFuels,PETel,USH,UPH]
        data = array([row])
        
        Status.int.setGraphicsData("ENERGY", data)


#............................................................................................
# Plot weekly heat supply

        TimeIntervals=[]

        equipments = Status.prj.getEquipments(cascade=True)
        NEquipe = len(equipments)

        USHj_weekly = []
        for equipe in equipments:
            USHj_weekly.append([unicode(equipe.Equipment,"utf-8")])
        

        if Status.int.cascadeUpdateLevel < NEquipe:    #cascade not up to date -> show zero line
            
            weeks = []
            vals = []
            for i in range(53): 
                weeks.append(1.0*i)
                vals.append(0.0)
            dataList = [weeks,vals]
            
        else:   
        
            USHj_sum = []
            weeks = ["week"]
            
            for j in range(NEquipe):
                USHj_sum.append(0.0)    #reset of the sum for each equipment

            nweek = 0.0
            for it in range(Status.Nt):
                
                for j in range(NEquipe):
                    
                    USHj_sum[j] += Status.int.USHj_t[j][it]/1000.0
                    
                if ((it+1)%168) == 0:  #end of the week

                    for j in range(1,NEquipe):
                        USHj_sum[j] += USHj_sum[j-1]  #sum one above the other

                    for j in range(NEquipe):
                        USHj_weekly[j].append(USHj_sum[j]*Status.EXTRAPOLATE_TO_YEAR)  #append twice, for
                        USHj_weekly[j].append(USHj_sum[j]*Status.EXTRAPOLATE_TO_YEAR)  #start and stop time of the week
                        USHj_sum[j] = 0.0                   #reset sum

                    weeks.append(nweek)
                    nweek+=1.0   
                    weeks.append(nweek)

            dataList = [weeks]
            for j in range(NEquipe):
                dataList.append(USHj_weekly[j])

        data = array(dataList)
       
        Status.int.setGraphicsData("ENERGY Plot1", data)
        
#------------------------------------------------------------------------------
    def getEquipmentList(self):
#------------------------------------------------------------------------------
#   gets the equipment list
#------------------------------------------------------------------------------

        self.equipments = Status.prj.getEquipments()
        self.NEquipe = len(self.equipments)
        logTrack("ModuleEnergy (getEquipmentList): %s equipes found" % self.NEquipe)

        Status.int.getEquipmentCascade()

#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,cascadeIndex):
#------------------------------------------------------------------------------
#   dummy function for calculation of energy flows in any equipment
#------------------------------------------------------------------------------

        Status.int.extendCascadeArrays(cascadeIndex)

        PNom = equipe.HCGPnom
        if PNom is None:
            logTrack("ModuleEnergy (cEF-dummy): no equipment capacity specified")
            PNom = 0

        COPh_nom = equipe.HCGTEfficiency
        if COPh_nom is None:
            logTrack("ModuleEnergy (cEF-dummy): no equipment COP specified")
            COPh_nom = 0.90
        
        EqName = equipe.Equipment
        EquipmentNo = Status.int.cascade[cascadeIndex-1]["equipeNo"]
        
        NT = Status.NT
        DT = Status.TemperatureInterval
        Nt = Status.Nt
        Dt = Status.TimeStep
        
#..............................................................................
# get demand data for CascadeIndex/EquipmentNo from Interfaces
# and create arrays for storing heat flow in equipment

        QD_Tt = copy.deepcopy(Status.int.QD_Tt_mod[cascadeIndex-1])
        QA_Tt = copy.deepcopy(Status.int.QA_Tt_mod[cascadeIndex-1])
        
        USHj_Tt = Status.int.createQ_Tt()
        USHj_t = Status.int.createQ_t()
        USHj_T = Status.int.createQ_T()

        
        QHXj_Tt = Status.int.createQ_Tt()
        QHXj_t = Status.int.createQ_t()
        QHXj_T = Status.int.createQ_T()

        QWHj_Tt = Status.int.createQ_Tt()
        QWHj_t = Status.int.createQ_t()
        QWHj_T = Status.int.createQ_T()

#..............................................................................
# start simulation

        USHj = 0
        QHXj = 0
        QWHj = 0

        HPerYear = 0

#..............................................................................
# outer iterative cycle: over all time steps
        for it in range(Nt):   

#..............................................................................
# inner iterative cycle: temperature intervals
            for iT in range(NT+2):   #+1 = the > 400 ºC case
                USHj_Tt[iT][it] = min(QD_Tt[iT][it],PNom*Dt) #just max(demand,nom.power) 
                QHXj_Tt[iT][it] = 0
                QWHj_Tt[iT][it] = 0

            USHj += USHj_Tt[NT+1][it]
            QHXj += QHXj_Tt[NT+1][it]
            QWHj += QWHj_Tt[NT+1][it]

            if USHj_Tt[NT+1][it] > 0:
                HPerYear += Dt
#..............................................................................
# end simulation. 

#..............................................................................
# storing results in Interfaces

# remaining heat demand and availability for next equipment in cascade
        Status.int.QD_Tt_mod[cascadeIndex] = QD_Tt
        Status.int.QD_T_mod[cascadeIndex] = Status.int.calcQ_T(QD_Tt)
        Status.int.QA_Tt_mod[cascadeIndex] = QA_Tt
        Status.int.QA_T_mod[cascadeIndex] = Status.int.calcQ_T(QA_Tt)

# heat delivered by present equipment                            
        Status.int.USHj_Tt[cascadeIndex-1] = USHj_Tt
        Status.int.USHj_T[cascadeIndex-1] = Status.int.calcQ_T(USHj_Tt)
        Status.int.USHj_t[cascadeIndex-1] = copy.deepcopy(USHj_Tt[Status.NT+1])

# waste heat absorbed by present equipment                            
        Status.int.QHXj_Tt[cascadeIndex-1] = QHXj_Tt
        Status.int.QHXj_T[cascadeIndex-1] = Status.int.calcQ_T(QHXj_Tt)
        Status.int.QHXj_t[cascadeIndex-1] = copy.deepcopy(QHXj_Tt[Status.NT+1])

# waste heat produced by present equipment

        Status.int.QWHj_Tt[cascadeIndex-1] = QWHj_Tt
        Status.int.QWHj_T[cascadeIndex-1] = Status.int.calcQ_T(QWHj_Tt)
        Status.int.QWHj_t[cascadeIndex-1] = copy.deepcopy(QWHj_Tt[Status.NT+1])

        Status.int.cascadeUpdateLevel = cascadeIndex

#........................................................................
# Global results (annual energy flows)

        Status.int.USHj[cascadeIndex-1] = USHj*Status.EXTRAPOLATE_TO_YEAR
        Status.int.QWHj[cascadeIndex-1] = QWHj*Status.EXTRAPOLATE_TO_YEAR
        Status.int.QHXj[cascadeIndex-1] = QHXj*Status.EXTRAPOLATE_TO_YEAR

        if COPh_nom > 0:
            FETFuel_j = USHj/COPh_nom
        else:
            FETFuel_j = 0.0
            showWarning("Strange boiler with COP = 0.0")
        FETel_j = 0.0
        
        Status.int.FETFuel_j[cascadeIndex-1] = FETFuel_j
        Status.int.FETel_j[cascadeIndex-1] = 0.0
        Status.int.HPerYearEq[cascadeIndex-1] = HPerYear*Status.EXTRAPOLATE_TO_YEAR

        logMessage("Dummy: eq.no.:%s USH: %s FETFuel: %s FETel: %s HPerYear: %s [MWh]"%\
                   (equipe.EqNo,\
                    USHj*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
                    0.0,\
                    FETel_j*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
                    HPerYear*Status.EXTRAPOLATE_TO_YEAR/1000.0))

        self.calculateOM(equipe,USHj*Status.EXTRAPOLATE_TO_YEAR)
        
        
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def runSimulation(self,first=None,last=None,loop=True):
#------------------------------------------------------------------------------
# updates the energy flows for the full equipment cascade
#------------------------------------------------------------------------------
        logTrack("ModuleEnergy (runSimulation): starting")
        NT = Status.NT

        self.getEquipmentList()
            
#..............................................................................
# initialising storage space for energy flows in cascade
# assigning total heat demand and availability to the first row in cascade

        if (first == None) or (first < 1):
            first = 1

        first = max(first,Status.int.cascadeUpdateLevel+1)    #avoid unnecessary calculations

        if last == None or last > self.NEquipe:
            last = self.NEquipe

        Status.int.extendCascadeArrays(self.NEquipe)

        logTrack("ModuleEnergy (runSimulation): simulating from %s to %s"%(first,last))
#..............................................................................
# now calculate the cascade
# call the calculation modules for each equipment

        dlg = DialogGauge(Status.main,_("EINSTEIN system simulation"),_("calculating energy flows"))

        for cascadeIndex in range(first,last+1):
            
            equipeID = Status.int.cascade[cascadeIndex-1]["equipeID"]

            equipe = Status.DB.qgenerationhc.QGenerationHC_ID[equipeID][0]            
            equipeClass = getEquipmentClass(equipe.EquipType)

            logTrack("=================================\nModuleEnergy (runSimulation): %s - %s [%s: %s]"%\
                     (cascadeIndex,equipe.Equipment,equipeClass,equipe.EquipType))
            
            if equipeClass == "HP":
                Status.mod.moduleHP.calculateEnergyFlows(equipe,cascadeIndex)
                
            elif equipeClass == "BB":
                Status.mod.moduleBB.calculateEnergyFlows(equipe,cascadeIndex)
                
            elif equipeClass == "ST":
                Status.mod.moduleST.calculateEnergyFlows(equipe,cascadeIndex)
                
            elif equipeClass == "CHP":
                Status.mod.moduleCHP.calculateEnergyFlows(equipe,cascadeIndex)
                
            else:
                logTrack("WARNING: equipment type not yet forseen in system simulation module")
                logTrack("running calculateEnergyFlows-dummy")
                self.calculateEnergyFlows(equipe,cascadeIndex)

            logTrack("ModuleEnergy (runSimulation): end simulation=====================================")

            dlg.update(100.0*(cascadeIndex-first+1)/(last-first+1))

#..............................................................................
# update the pointer to the last calculated cascade

        dlg.Destroy()
                          
        Status.int.cascadeUpdateLevel = last

#..............................................................................
# if a full cascade has been calculated, calculate the balances

        logTrack("ModuleEnergy (runSimulation): arrived at the end. %s [%s]"%\
                 (last,self.NEquipe))

        if last == self.NEquipe:

            uncoveredDemand = Status.int.QD_T_mod[last][Status.NT+1]
            totalDemand = Status.int.QD_T_mod[0][Status.NT+1]
            if uncoveredDemand > 0.005*totalDemand:
                showWarning("Revise your design.\nCurrent equipment capacity is not sufficient for covering the demand\n"+\
                            "Remaining heat demand: %s [MWh]"%(uncoveredDemand/1000.0))
                
            logTrack("ModuleEnergy (runSimulation): updating Energy balances")

            (projectData,generalData) = Status.prj.getProjectData()

            if loop == True:
                for i in range(10):

                    USH0 = Status.int.USHTotal
                    QWHEq0 = Status.int.QWHEqTotal

                    Status.mod.moduleEA.calculateEquipmentEnergyBalances()
                    Status.prj.setStatus("Energy")  #probably redundant, already done in cEEB
                    self.getEquipmentTotals()

                    USH = Status.int.USHTotal
                    QWHEq = Status.int.QWHEqTotal

                    logTrack("ModuleEnergy - iterative cycle i %s (USH): %s -> %s (QWH): %s -> %s"% \
                                          (i,USH0,USH,QWHEq0,QWHEq))

                    if abs(QWHEq - QWHEq0) < 0.0001*(USH + USH0):
                        break
                    else:
                        Status.mod.moduleHR.runHRModule()   # update waste heat calculations
                        self.runSimulation(1,self.NEquipe,loop=False)
                    
#------------------------------------------------------------------------------
    def calculateOM(self,equipe,USH):
#------------------------------------------------------------------------------

        OMFix = equipe.OandMfix
        OMVar = equipe.OandMvar

        try:
            OM = OMFix + OMVar*USH
        except:
            logWarning(_("OM costs for equipment %s could not be calculated")%equipe.Equipment)
            OM = 0.0

        equipe.OandM = OM

        Status.SQL.commit()
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def getEquipmentTotals(self):
#------------------------------------------------------------------------------
#..............................................................................
#   estimate equipment waste heat from annual QWHj and equipment schedules

        Status.int.QWHEqTotal_Tt = Status.int.createQ_Tt()
        
        equipments = Status.prj.getEquipments()
        for equipe in equipments:
            j = equipe.EqNo - 1
            for iT in range(Status.NT+2):
                for it in range(Status.Nt):
                    Status.int.QWHEqTotal_Tt[iT][it] += Status.int.QWHj_Tt[j][iT][it]

        Status.int.QWHEqTotal_t = copy.deepcopy(Status.int.QWHEqTotal_Tt[0])
        Status.int.QWHEqTotal_T = Status.int.calcQ_T(Status.int.QWHEqTotal_Tt)
        Status.int.QWHEqTotal = Status.int.QWHEqTotal_T[0]        
              
#==============================================================================

if __name__ == "__main__":
    print "Testing moduleEnergy"
    import einstein.GUI.pSQL as pSQL, MySQLdb
    from einstein.modules.myInterfaces import *
    sql = MySQLdb.connect(user="root", db="einstein")
    DB = pSQL.pSQL(sql, "einstein")
    stat = Status("testModuleEnergy")
    Status.DB = DB

    interf = Interfaces(80,8760)

    print "instantiating moduleEnergy"
    mod = ModuleEnergy()
    mod.runSimulation()
