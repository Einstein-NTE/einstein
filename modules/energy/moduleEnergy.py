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
#	Version No.: 0.15
#	Created by: 	    Hans Schweiger	13/03/2008
#	Last revised by:    Tom Sobota          17/03/2008
#                           Hans Schweiger      20/03/2008
#                           Tom Sobota          31/03/2008
#                           Hans Schweiger      02/04/2008
#                           Hans Schweiger      03/04/2008
#                           Hans Schweiger      13/04/2008
#                           Hans Schweiger      18/04/2008
#                           Stoyan Danov        14/05/2008
#                           Enrico Facci        11/06/2008
#                           Hans Schweiger      26/06/2008
#                           Hans Schweiger      28/06/2008
#                           Hans Schweiger      03/07/2008
#                           Hans Schweiger      10/07/2008
#                           Hans Schweiger      02/08/2008
#
#       Changes to previous version:
#       16/03/2008 Graphics implementation
#       17/03/2008 Changes to graphics.
#       20/03/2008 Adaptation to changes in interfaces and module HP
#       31/03/2008 Adaptation to new numpy-based graphics
#       02/04/2008 Small change in instantiatio of ModuleHP (key included)
#       03/04/2008 Link to modules via parent (= Modules)
#       13/04/2008 CascadeIndex corrected: now from 1 to N
#       18/04/2008 Reference to Status.int
#       14/05/2008 runSimulation reperence to C tables eliminated
#       11/06/2008 modified runSimulation (getEquipmentClass, activated
#                  calculateEnergyFlows for boilers
#       26/06/2008: HS  solar thermal system (ST) added in runSimulation
#                       try-except eliminated in runSimulation for better
#                       debugging
#       28/06/2008: possibility for simulating from first to last introduced
#                   in run simulation
#       03/07/2008: check and update of cascadeUpdateLevel incorporated
#       10/07/2008: adaptation to new panel and solar system simulation
#       02/08/2008: clean-up of prints in runSimulation and cEF
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
            USHj_weekly.append([str(equipe.Equipment)])
        

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
                        USHj_weekly[j].append(USHj_sum[j])  #append twice, for
                        USHj_weekly[j].append(USHj_sum[j])  #start and stop time of the week
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

#..............................................................................
# start simulation

        USHj = 0
        QHXj = 0

        HPerYear = 0

#..............................................................................
# outer iterative cycle: over all time steps
        for it in range(Nt):   

#..............................................................................
# inner iterative cycle: temperature intervals
            for iT in range(NT+2):   #+1 = the > 400 ºC case
                USHj_Tt[iT][it] = min(QD_Tt[iT][it],PNom*Dt) #just max(demand,nom.power) 
                QHXj_Tt[iT][it] = 0

            USHj += USHj_Tt[NT+1][it]
            QHXj += QHXj_Tt[NT+1][it]

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

        Status.int.cascadeUpdateLevel = cascadeIndex

#........................................................................
# Global results (annual energy flows)

        Status.int.USHj[cascadeIndex-1] = USHj*Status.EXTRAPOLATE_TO_YEAR

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
    def runSimulation(self,first=None,last=None):
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
            Status.mod.moduleEA.calculateEquipmentEnergyBalances()
            Status.prj.setStatus("Energy")
    
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
