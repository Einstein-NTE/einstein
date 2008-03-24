# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleBB (Boilers and Burners)
#			
#------------------------------------------------------------------------------
#			
#	Module for calculation of boilers
#
#==============================================================================
#
#	Version No.: 0.05
#	Created by: 	    Hans Schweiger	11/03/2008
#	Last revised by:    Tom Sobota          15/03/2008
#                           Enrico Facci /
#                           Hans Schweiger      24/03/2008
#
#       Changes to previous version:
#       2008-3-15 Added graphics functionality
#       2008-03-24  Incorporated "calculateEnergyFlows" from Enrico Facci
#                   - adapted __init__ and plots similar to moduleHP
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
import wx


from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP

class ModuleBB():

    BBList = []
    
    def __init__(self):
        self.interface = Interfaces()

        self.DB = Status.DB
        self.sql = Status.SQL
        
        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        self.equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
        self.equipmentsC = self.DB.cgenerationhc.sql_select(sqlQuery)
        self.NEquipe = len(self.equipments)
        print "ModuleBB (__init__): %s equipes found"%self.NEquipe


#............................................................................................
#XXXHS2008-03-22: here for testing purposes.
#   -> initPanel should be activated by event handler on entry into panel

        self.initPanel()
        self.updatePanel()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

        BBList = self.screenEquipments()
        
#............................................................................................
#XXX FOR TESTING PURPOSES ONLY: load default demand
# here it should be assured that heat demand and availability for position in cascade
# of presently existing heat pumps is already defined

        self.interface.initCascadeArrays(self.NEquipe)
       
#............................................................................................
#returns HPList to the GUI for displaying in window
        
        return (BBList)
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def screenEquipments(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

        self.interface.getEquipmentCascade()
        self.cascadeIndex = 0
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------

        print "ModuleHP (updatePanel): data for panel are copied to interface"
        
# plot to be displayed
        self.interface.setGraphicsData('BB Plot',[self.interface.T,
                                        self.interface.QD_T_mod[self.cascadeIndex],
                                        self.interface.QA_T_mod[self.cascadeIndex],
                                        self.interface.QD_T_mod[self.cascadeIndex+1],
                                        self.interface.QA_T_mod[self.cascadeIndex+1]])
# info for text boxes in right side of panel
        self.interface.setGraphicsData('BB Info',{"noseque":55})

# list of equipments in cascade for Table
        self.interface.setGraphicsData('BB List',self.interface.cascade)

#------------------------------------------------------------------------------

    def exitModule(self,exit_option):
        """
        carries out any calculations necessary previous to displaying the HP
        design assitant window
        """
        if exit_option == "save":
            print "exitModule: here I should save the current configuration"
        elif exit_option == "cancel":
            print "exitModule: here I should retreive the previous configuration"
            

        print "exitModule: function not yet defined"

        return "ok"

#------------------------------------------------------------------------------

    def storeModulePars(self):
        """
        store Module parameters in the SQL or some other save space
        """
        print "storeModulePars: not yet defined"

        return "ok"


#------------------------------------------------------------------------------
    def add(self,BBId):
        """
        adds a new heat pump 
        """
        #--> add HP to the equipment list under current alternative
        print "add (BB): function not yet defined"

        self.calculateEnergyFlows(BBId)

        return "ok"

#------------------------------------------------------------------------------

    def delete(self,BBid):
        """
        deletes the selected boiler / burner in the current alternative
        """
        print "delete (BB): function not yet defined"

        return "ok"

        #--> delete HP from the equipment list under current alternative
        
#------------------------------------------------------------------------------
    def addEquipmentDummy(self):
#------------------------------------------------------------------------------
#       adds a new dummy equipment to the equipment list and returns the
#       position in the cascade 
#------------------------------------------------------------------------------

#XXX    Here some function adding a row to the QGenerationHC and CGenerationHC
#       in the SQL
#XXX    Cascade index should be set by default to something reasonable,
#       depending if the equipment is a base load equipment or a peak load one

#for the moment the HP Module works always on Eq. 0 / CI 0
        self.cascadeIndex = 0
        self.equipe = self.equipments[0]
        self.equipeC = self.equipmentsC[0]
        return(self.equipe,self.equipeC)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def retrieveDeleted(self):
        """
        returns a list of previously deleted equipment that can be retrieved
        """
        print "deleteHP: function not yet defined"

        return "ok"

        #--> delete HP from the equipment list under current alternative
        
#------------------------------------------------------------------------------

    def designAssistant1(self):
        """
        step 1 of the design assistant (from activation to 1st user interaction)
        """
        try:
            print "designAssistant1: function not yet implemented"
            return "ManualFinalAdjustment"
#..............................................................................
        except Exception, designAssistant1: #in case of an error
            print 'designAssistant1', designAssistant1
            return designAssistant1

#..............................................................................
        else:       #everything is fine
            return 0

#------------------------------------------------------------------------------

    def designAssistant2(self):
        """
        step 2 of the design assistant (after 1st user interaction)
        """
        try:
            print "designAssistant2: function not yet implemented"
            return "ok"
#..............................................................................
        except Exception, designAssistant2: #in case of an error
            print 'designAssistant2', designAssistant2
            return designAssistant2

#..............................................................................
        else:       #everything is fine
            return 0

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,equipeC,cascadeIndex):
#------------------------------------------------------------------------------
#   calculates the energy flows in the equipment identified by "cascadeIndex"
#------------------------------------------------------------------------------

        print "ModuleHP (calculateEnergyFlows): starting (cascade no: %s)"%cascadeIndex
#..............................................................................
# get equipment data from equipment list in SQL

        BBModel = equipe.Model
        print equipe.Model
        BBType = equipe.EquipType
        PNom = equipe.HCGPnom
        COPh_nom = equipe.HCGTEfficiency
#XXX TOpMax or something similar should be defined in SQL        TMax = equipe.TOpMax
# for the moment set some value manually
        TMax = 95
    
#XXX ENRICO: here other equipment parameters should be imported from SQL database
        
        EquipmentNo = self.interface.cascade[cascadeIndex]["equipeNo"]

        print 'ModuleBB (calculateEnergyFlows): Model = ', BBModel, ' Type = ', BBType, 'PNom = ', PNom

#..............................................................................
# get demand data for CascadeIndex/EquipmentNo from Interfaces
# and create arrays for storing heat flow in equipment

        QD_Tt = self.interface.QD_Tt_mod[cascadeIndex]
        QA_Tt = self.interface.QA_Tt_mod[cascadeIndex]
        
        USHj_Tt = self.interface.createQ_Tt()
        USHj_T = self.interface.createQ_T()

        
        QHXj_Tt = self.interface.createQ_Tt()
        QHXj_T = self.interface.createQ_T()

#..............................................................................
# Start hourly loop

        USHj = 0
        QHXj = 0

        for it in range(Status.Nt):

            print "time = ",it*Status.TimeStep

#..............................................................................
# Calculate heat delivered by the given equipment for each time interval
            for iT in range (Status.NT+2):
                QHXj_Tt[iT][it] = 0     #for the moment no waste heat considered
                if TMax >= self.interface.T[iT] :   #TMax is the max operating temperature of the boiler 
                    USHj_Tt[iT][it] = min(QD_Tt[iT][it],PNom*Status.TimeStep)     #from low to high T
                else:
                    if (iT > 0):
                        USHj_Tt[iT][it] = USHj_Tt[iT-1][it]     #no additional heat supply at high temp.
                    else:
                        USHj_Tt[iT][it] = 0
            USHj += USHj_Tt[Status.NT+1][it]
            print USHj_Tt[Status.NT+1][it]      #total heat supplied at present timestep
#........................................................................
# End of year reached. Store results in interfaces

        print "ModuleBB (calculateEnergyFlows): now storing final results"
        
# remaining heat demand and availability for next equipment in cascade
        Interfaces.QD_Tt_mod[cascadeIndex+1] = QD_Tt
        Interfaces.QD_T_mod[cascadeIndex+1] = self.interface.calcQ_T(QD_Tt)
        Interfaces.QA_Tt_mod[cascadeIndex+1] = QA_Tt
        Interfaces.QA_T_mod[cascadeIndex+1] = self.interface.calcQ_T(QA_Tt)

# heat delivered by present equipment                            
        Interfaces.USHj_Tt[cascadeIndex] = USHj_Tt
        Interfaces.USHj_T[cascadeIndex] = self.interface.calcQ_T(USHj_Tt)

# waste heat absorbed by present equipment                            
        Interfaces.QHXj_Tt[cascadeIndex] = QHXj_Tt
        Interfaces.QHXj_T[cascadeIndex] = self.interface.calcQ_T(QHXj_Tt)

#        equipeC.USHj = USHj
#        equipeC.QHXj = QHXj    #XXX to be defined in data base

        print "Total energy supplied by equipment ",USHj, " MWh"
        print "Total waste heat input  ",QHXj, " MWh"

        return USHj    

#==============================================================================

if __name__ == "__main__":
    print "Testing ModuleBB"
    import einstein.GUI.pSQL as pSQL, MySQLdb
    from einstein.modules.interfaces import *
    from einstein.modules.energy.moduleEnergy import *
    stat = Status("testModuleHP")

    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    
    Status.PId = 2
    Status.ANo = 0

    interf = Interfaces()

    mod = ModuleBB()
    (equipe,equipeC) = mod.addEquipmentDummy()
    mod.calculateEnergyFlows(equipe,equipeC,mod.cascadeIndex)
                    

#    mod.designAssistant1()
#    mod.designAssistant2(12)
