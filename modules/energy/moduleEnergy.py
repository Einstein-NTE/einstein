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
#	Version No.: 0.12
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
from einstein.modules.interfaces import *
from einstein.modules.heatPump.moduleHP import ModuleHP
import einstein.modules.matPanel as mP

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
    def initPanel(self):
#------------------------------------------------------------------------------
        
        """
        carries out any calculations necessary previous to displaying the BB
        design assitant window
        """
#------------------------------------------------------------------------------
        # send data to GUI panel
        #
        # grid: Energetic performance
        #
        data = array([['Steam boiler',   100.0,    2.0,  5.0],
                      ['CHP',            280.0,    3.0,  3.0],
                      ['Gas burner',      65.0,    4.0,  2.4],
                      ['Chiller',        105.0,    5.0,  1.8],
                      ['Chiller',         35.0,    6.0,  7.3],
                      ['Total',          585.0,   20.0, 19.5],
                      ['Energy savings',  65.0,   10.0,  3.0]])

        Status.int.setGraphicsData(self.keys[0], data)

        #print "ModuleEnergy graphics data initialization"
        #print "Interfaces.GData[%s] contains:\n%s\n" % (self.keys[0],repr(Interfaces.GData[self.keys[0]]))

#............................................................................................
# 2. Plot dayly demand and supply

        TimeIntervals=[]

        self.getEquipmentList()
        NEquipe = self.NEquipe

        print "ModuleEnergy (initPanel): no USH data available"
        print "NEquipe: %s Length of USH array: %s "%(NEquipe,len(Status.int.USHj_t))
        print Status.int.USHj_t

        if len(Status.int.USHj_t) < NEquipe:
            
            days = []
            vals = []
            for i in range(365):
                days.append(1.0*i)
                vals.append(0.0)
            dataList = [days,vals]
            
        else:   
        
            USHj_daily = []
            USHj_sum = []
            days = []
            
            for j in range(NEquipe):
                USHj_daily.append([])
                USHj_sum.append(0.0)

#            QD_daily = []
#            QD_sum = 0.0
                
            nday = 0.0
            for it in range(Status.Nt):
                
                for j in range(NEquipe):
                    
                    USHj_sum[j] += Status.int.USHj_t[j][it]
#                QD_sum += Status.int.QD_Tt[Status.NT+1][it]
                    
                if ((it+1)%24) == 0:  #end of the day
                    for j in range(NEquipe):
                        USHj_daily[j].append(USHj_sum[j])
                        USHj_sum[j] = 0.0
#                    QD_daily.append(QD_sum)
#                    QD_sum = 0.0
                    nday+=1.0
                    
                    days.append(nday)

            dataList = [days]
            for j in range(NEquipe):
                dataList.append(USHj_daily[j])
        data = array(dataList)
       
        Status.int.setGraphicsData("ENERGY Plot1", data)
        
        return "ok"

#------------------------------------------------------------------------------
    def getEquipmentList(self):
#------------------------------------------------------------------------------
#   gets the equipment list
#------------------------------------------------------------------------------

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        self.equipments = Status.DB.qgenerationhc.sql_select(sqlQuery)
#        self.equipmentsC = Status.DB.qgenerationhc.sql_select(sqlQuery)
        self.NEquipe = len(self.equipments)
        print "ModuleEnergy (getEquipmentList): %s equipes found" % self.NEquipe

        Interfaces.cascade = []
        for j in range(self.NEquipe):
            equipe = self.equipments[j]
            Interfaces.cascade.append({"equipeID":equipe.QGenerationHC_ID,"equipeNo":j})
        print 'ModuleEnergy(getEquipmentList) Status.int.cascade', Status.int.cascade #SD, 16.05.2008

#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,cascadeIndex):
#------------------------------------------------------------------------------
#   dummy function for calculation of energy flows in any equipment
#------------------------------------------------------------------------------

        print "ModuleEnergy(calculateEnergyFlows): dummy function"

        PNom = equipe.HCGPnom
        if PNom is None: PNom = 0
        
        EqName = equipe.Equipment
        EquipmentNo = Status.int.cascade[cascadeIndex-1]["equipeNo"]
        
        NT = Status.NT
        DT = Status.TemperatureInterval
        Nt = Status.Nt
        Dt = Status.TimeStep
        
        print EqName, ": PNom = ",PNom, " kW"

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

#..............................................................................
# outer iterative cycle: over all time steps
        for it in range(Nt):   

#..............................................................................
# inner iterative cycle: temperature intervals
            print "time = ",it
            for iT in range(NT+2):   #+1 = the > 400 ºC case
                USHj_Tt[iT][it] = min(QD_Tt[iT][it],PNom*Dt) #just max(demand,nom.power) 
                QHXj_Tt[iT][it] = 0
            USHj += USHj_Tt[NT+1][it]
            QHXj += QHXj_Tt[NT+1][it]
            print "USH = ",USHj_Tt[NT+1][it]
#..............................................................................
# end simulation. 

#..............................................................................
# storing results in Interfaces

# remaining heat demand and availability for next equipment in cascade
        Interfaces.QD_Tt_mod[cascadeIndex] = QD_Tt
        Interfaces.QD_T_mod[cascadeIndex] = Status.int.calcQ_T(QD_Tt)
        Interfaces.QA_Tt_mod[cascadeIndex] = QA_Tt
        Interfaces.QA_T_mod[cascadeIndex] = Status.int.calcQ_T(QA_Tt)

# heat delivered by present equipment                            
        Interfaces.USHj_Tt[cascadeIndex-1] = USHj_Tt
        Interfaces.USHj_T[cascadeIndex-1] = Status.int.calcQ_T(USHj_Tt)

# waste heat absorbed by present equipment                            
        Interfaces.QHXj_Tt[cascadeIndex-1] = QHXj_Tt
        Interfaces.QHXj_T[cascadeIndex-1] = Status.int.calcQ_T(QHXj_Tt)

#        equipeC.USHj = USHj
#        equipeC.QHXj = QHXj    #XXX to be defined in data base

        print "Total energy supplied by equipment ",USHj, " MWh"
        print "Total waste heat input  ",QHXj, " MWh"

        print "Total energy supplied by equipment ",USHj, " MWh"

        
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def runSimulation(self,first=None,last=None):
#------------------------------------------------------------------------------
# updates the energy flows for the full equipment cascade
#------------------------------------------------------------------------------
        print "ModuleEnergy (runSimulation): QD_T", Status.int.QD_T
        NT = Status.NT
        print "Running system simulation..."

        self.getEquipmentList()
            
#..............................................................................
# initialising storage space for energy flows in cascade
# assigning total heat demand and availability to the first row in cascade

        if (first == None) or (first < 1):
            first = 1

        first = max(first,Status.int.cascadeUpdateLevel)    #avoid unnecessary calculations

        if last == None or last > self.NEquipe:
            last = self.NEquipe

        Status.int.extendCascadeArrays(self.NEquipe)

#..............................................................................
# now calculate the cascade
# call the calculation modules for each equipment

        for cascadeIndex in range(first,last+1):
            equipeID = Status.int.cascade[cascadeIndex-1]["equipeID"]

            equipe = self.equipments.QGenerationHC_ID[equipeID][0]
#                equipeC = self.equipmentsC.QGenerationHC_ID[equipeID][0]
            print "ModuleEnergy (runSimulation) [%s] equipeType = : "%cascadeIndex,equipe.EquipType
            
            equipeClass = getEquipmentClass(equipe.EquipType)
            print "ModuleEnergy (runSimulation): equipe type/class = ",equipe.EquipType,equipeClass
            
#                if equipe.EquipType == "HP COMP" or equipe.EquipType == "HP THERMAL" or equipe.EquipType == "compression heat pump":
            if equipeClass == "HP":
                print "======================================"
                print "heat pump"
                print "ModuleEnergy (runSimulation): equipe =", equipe, "cascadeIndex", cascadeIndex
                Status.mod.moduleHP.calculateEnergyFlows(equipe,cascadeIndex)
                print "end heat pump"
                print "======================================"
            elif equipeClass == "BB":
                print "boiler"
                print "ModuleEnergy (runSimulation): equipe =", equipe, "cascadeIndex", cascadeIndex
                Status.mod.moduleBB.calculateEnergyFlows(equipe,cascadeIndex)
                print "boiler"
                print "end boiler"
                print "======================================"
            elif equipeClass == "ST":
                print "solar thermal"
                print "ModuleEnergy (runSimulation): equipe =", equipe, "cascadeIndex", cascadeIndex
                Status.mod.moduleST.calculateEnergyFlows(equipe,cascadeIndex)
                print "end solar thermal"
                print "======================================"
            else:
                print "equipment type not yet forseen in system simulation module"
                print "running calculateEnergyFlows-dummy"
                self.calculateEnergyFlows(equipe,cascadeIndex)

            print "ModuleEnergy (runSimulation): end simulation"

#..............................................................................
# update the pointer to the last calculated cascade

        Status.int.cascadeUpdateLevel = last
    
              
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
