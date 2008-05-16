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
#	Version No.: 0.07
#	Created by: 	    Hans Schweiger	13/03/2008
#	Last revised by:    Tom Sobota          17/03/2008
#                           Hans Schweiger      20/03/2008
#                           Tom Sobota          31/03/2008
#                           Hans Schweiger      02/04/2008
#                           Hans Schweiger      03/04/2008
#                           Hans Schweiger      13/04/2008
#                           Hans Schweiger      18/04/2008
#                           Stoyan Danov        14/05/2008
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

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
from einstein.modules.heatPump.moduleHP import ModuleHP
import einstein.modules.matPanel as mP

def drawEnergyDemand(self):
    # draws Energy Demand graphic
    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    # this is just an example curve
    # the curve takes it's data from the dictionary Interfaces.GData, with the key 'Energy_ED'
    self.subplot.plot(Interfaces.GData['Energy_ED'][0],
                      Interfaces.GData['Energy_ED'][1],
                      'go-', label='QD', linewidth=2)
    self.subplot.plot(Interfaces.GData['Energy_ED'][2],
                      Interfaces.GData['Energy_ED'][3],
                      'rs',  label='QA')
    self.subplot.axis([0, 100, 0, 1e+8])
    self.subplot.legend()

class ModuleEnergy(object):

    def __init__(self, keys):
        self.keys = keys
        
#..............................................................................
# getting list of equipment in SQL

        self.getEquipmentList()

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
    def exitModule(self,exit_option):
#------------------------------------------------------------------------------
        """
        carries out any calculations necessary previous to displaying the HP
        design assitant window
        """
#------------------------------------------------------------------------------
        if exit_option == "save":
            print "exitModule: here I should save the current configuration"
        elif exit_option == "cancel":
            print "exitModule: here I should retreive the previous configuration"
            

        print "exitModule: function not yet defined"

        return "ok"

#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,equipeC,cascadeIndex):
#------------------------------------------------------------------------------
#   dummy function for calculation of energy flows in any equipment
#------------------------------------------------------------------------------

        print "ModuleEnergy(calculateEnergyFlows): dummy function"

        PNom = equipe.HCGPnom
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

        QD_Tt = Status.int.QD_Tt_mod[cascadeIndex-1]
        QA_Tt = Status.int.QA_Tt_mod[cascadeIndex-1]
        
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
    def runSimulation(self):
#------------------------------------------------------------------------------
# updates the energy flows for the full equipment cascade
#------------------------------------------------------------------------------
        try:
            print "ModuleEnergy (runSimulation): QD_T", Status.int.QD_T
            NT = Status.NT
            print "Running system simulation..."

            self.getEquipmentList()
            
#..............................................................................
# initialising storage space for energy flows in cascade
# assigning total heat demand and availability to the first row in cascade

            Interfaces.QD_Tt_mod = []      
            Interfaces.QD_T_mod = []
            Interfaces.QA_Tt_mod = []       
            Interfaces.QA_T_mod = []

            Interfaces.USHj_Tt = []
            Interfaces.USHj_T = []
            Interfaces.QHXj_Tt = []
            Interfaces.QHXj_T = []

            Interfaces.QD_Tt_mod.append(Status.int.QD_Tt)       
            Interfaces.QD_T_mod.append(Status.int.QD_T)
            Interfaces.QA_Tt_mod.append(Status.int.QA_Tt)      
            Interfaces.QA_T_mod.append(Status.int.QA_T)

            for j in range(self.NEquipe):
                Interfaces.QD_Tt_mod.append(Status.int.createQ_Tt())      
                Interfaces.QD_T_mod.append(Status.int.createQ_T())
                Interfaces.QA_Tt_mod.append(Status.int.createQ_Tt())    
                Interfaces.QA_T_mod.append(Status.int.createQ_T())

                Interfaces.USHj_Tt.append(Status.int.createQ_Tt())
                Interfaces.USHj_T.append(Status.int.createQ_T())
                Interfaces.QHXj_Tt.append(Status.int.createQ_Tt())
                Interfaces.QHXj_T.append(Status.int.createQ_T())
                                       

#..............................................................................
# now calculate the cascade
# call the calculation modules for each equipment

            for cascadeIndex in range(1,self.NEquipe+1):
                equipeID = Status.int.cascade[cascadeIndex-1]["equipeID"]

                equipe = self.equipments.QGenerationHC_ID[equipeID][0]
#                equipeC = self.equipmentsC.QGenerationHC_ID[equipeID][0]
                print "ModuleEnergy (runSimulation) [%s]: "%cascadeIndex,equipe.EquipType
  
                if equipe.EquipType == "HP COMP" or equipe.EquipType == "HP THERMAL" or equipe.EquipType == "compression heat pump":
                    print "======================================"
                    print "heat pump"
                    print "ModuleEnergy (runSimulation): equipe =", equipe, "cascadeIndex", cascadeIndex
                    Status.mod.moduleHP.calculateEnergyFlows(equipe,cascadeIndex)
                    print "end heat pump"
                    print "======================================"
                elif equipe.EquipType == "Boiler":
                    print "boiler"
                else:
                    print "equipment type not yet forseen in system simulation module"
                    self.calculateEnergyFlows(equipe,cascadeIndex)

                print "ModuleEnergy (runSimulation): end simulation"

              
#..............................................................................
        except Exception, runSimulation: #in case of an error
            print 'run Simulation', runSimulation
            return runSimulation

#..............................................................................
        else:       #everything is fine
            return 0

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
