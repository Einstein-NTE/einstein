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
#                           Tom Sobota           1/04/2008
#                           Hans Schweiger      03/04/2008
#                           Enrico Facci        09/04/2008
#                           Stoyan Danov        16/04/2008
#
#       Changes to previous version:
#       2008-3-15 Added graphics functionality
#       2008-03-24  Incorporated "calculateEnergyFlows" from Enrico Facci
#                   - adapted __init__ and plots similar to moduleHP
#       1/04/2008   Adapted to new graphics interfase using numpy
#       03/04/2008  Link to modules via Modules
#       09/04/2008  addEquipmentDummy, setEquipmentFromDB
#       16/04/2008  setEquipmentFromDB: aranged & tested (it was indented incorrectly), 
#                   3 functions copied from moduleHP: getEqId,deleteEquipment,deleteFromCascade ->
#                   -> In order to activate deleteEquipment: screenEquipments should be arranged before
#                   (BBList in alalogy with HPList), see moduleHP
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
import einstein.modules.matPanel as mP

class ModuleBB(object):

    BBList = []
    
    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel
        self.interface = Interfaces()

        self.DB = Status.DB
        self.sql = Status.SQL

        self.neweqs = 0 #new equips added
        
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

        print "ModuleBB (updatePanel): data for panel are copied to interface"
        
        # plot to be displayed
	# this is how the data should be set up
	# (this data are just an example!)
        data = array([['Boiler 1', 2004, 'Type 1', 3000, 100, 120],
		      ['Boiler 2', 2006, 'Type 1', 4500, 120, 140],
                      ['Boiler 3', 2007, 'Type 2', 5000,  80, 130]])


        self.interface.setGraphicsData(self.keys[0], data)

        try:
	    #    self.interface.setGraphicsData('BB Plot',[self.interface.T,
	    #                                              self.interface.QD_T_mod[self.cascadeIndex],
	    #                                              self.interface.QA_T_mod[self.cascadeIndex],
	    #                                              self.interface.QD_T_mod[self.cascadeIndex+1],
	    #                                              self.interface.QA_T_mod[self.cascadeIndex+1]])
	    # info for text boxes in right side of panel
            self.interface.setGraphicsData('BB Info',{"noseque":55})

            # list of equipments in cascade for Table
            self.interface.setGraphicsData('BB List',self.interface.cascade)
        except:
            pass

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
        adds a new boiler 
        """
        #--> add HP to the equipment list under current alternative
        print "add (BB): function not yet defined"

        self.calculateEnergyFlows(BBId)

        return "ok"


#------------------------------------------------------------------------------
    def getEqId(self,rowNo):
#------------------------------------------------------------------------------
#   gets the EqId from the rowNo in the HPList
#------------------------------------------------------------------------------

        HPId = self.HPList[rowNo]["equipeID"]
        return HPId

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def deleteEquipment(self,rowNo):
#------------------------------------------------------------------------------
        """
        deletes the selected boiler in the current alternative
        """
#------------------------------------------------------------------------------
        print "deleteHP: function not yet defined"

        #--> delete BB from the equipment list under current alternative #from C&QGenerationHC under ANo
        BBid = self.getEqId(rowNo)
        print "Module BB (delete): id to be deleted = ",BBid
        
        eq = self.equipments.QGenerationHC_ID[BBid][0] #select the corresponding rows to HPid in both tables
        eqC = self.equipmentsC.QGenerationHC_id[BBid][0]

        eq.delete() #deletes the rows in both tables, to be activated later, SD
        eqC.delete()
        self.sql.commit()

        #actuallise the cascade list: define deleteFromCascade
        self.deleteFromCascade(self.interface.cascade, BBid)

        self.NEquipe -= 1

#------------------------------------------------------------------------------
    def deleteFromCascade(self, cascade, BBid):
#------------------------------------------------------------------------------
        """
        deletes from the actual list casade and re-assigns the CascadeIndex values in CGenerationHC table
        """
#-----------------------------------------------------------------------------

#        print '\n deleteFromCascade():', 'cascade =', cascade

        idx = -1
        new_cascade = cascade
        for i in range(len(new_cascade)):
            if new_cascade[i]['equipeID'] == BBid:
                idx = i

        new_cascade.pop(idx)           

        for i in range(len(new_cascade)): #assign new CascadeIndex in CGenerationHC table
            eqC = self.equipmentsC.QGenerationHC_id[new_cascade[i]['equipeID']][0]
            eqC.CascadeIndex = i+1
#            print '\n new_CascadeIndex', eqC.CascadeIndex
            
#        self.sql.commit() #confirm storing to sql of new CascadeIndex #to be activated, SD

#        print '\n deleteFromCascade():', 'new_cascade =', new_cascade


        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY EqNo ASC"%(Status.PId,Status.ANo)
        equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
##        print '\n \nequipments', equipments

        for i in range(len(equipments)): #assign new EqNo in QGenerationHC table
            equipments[i].EqNo = i+1

#        self.sql.commit() #to be activated, SD

        self.interface.deleteCascadeArrays(self.NEquipe)



###------------------------------------------------------------------------------
##    def delete(self,BBid):
##        """
##        deletes the selected boiler / burner in the current alternative
##        """
##        print "delete (BB): function not yet defined"
##
##        return "ok"
##
##        #--> delete HP from the equipment list under current alternative
        
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
#        self.cascadeIndex = 0
#        self.equipe = self.equipments[0]
#        self.equipeC = self.equipmentsC[0]
#        return(self.equipe,self.equipeC)

        self.neweqs += 1 #No of last equip added

        CascadeIndex = self.NEquipe + 1

        NewEquipmentName = "New boiler %s"%(self.neweqs)

        EqNo = self.NEquipe + 1
        print 'CascadeIndex', CascadeIndex
        dic = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo,"EqNo":EqNo,"Equipment":NewEquipmentName,"EquipType":"Boiler"}
        QGid = self.DB.qgenerationhc.insert(dic)
        dicC = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo,"QGenerationHC_id":QGid,"CascadeIndex":CascadeIndex}
        CGid = self.DB.cgenerationhc.insert(dicC)

        Status.SQL.commit()

        print "new equip row created"

        self.cascadeIndex = CascadeIndex - 1 #appoints the last (cascadeIndex starts from 0, CascadeIndex starts from 1)

        print "self.cascadeIndex", self.cascadeIndex

        self.equipe = self.equipments.QGenerationHC_ID[QGid][0]
        self.equipeC = self.equipmentsC.CGenerationHC_ID[CGid][0]
        return(self.equipe,self.equipeC)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def setEquipmentFromDB(self,equipe,equipeC,modelID):
#------------------------------------------------------------------------------
#   takes an equipment from the data base and stores it under a given Id in
#   the equipment data base
#------------------------------------------------------------------------------

        model = self.DB.dbboiler.DBBoiler_ID[modelID][0]

        equipe.update({"HCGPnom":model.BBPnom})
        equipe.update({"HCGTEfficiency":model.BBEfficiency})
        equipe.update({"Manufact":model.BoilerManufacturer})
        equipe.update({"Model":model.BoilerModel})

        equipe.update({"EquipTypeFromDB":model.BoilerType})
        equipe.update({"EquipIDFromDB":model.DBBoiler_ID})
        Status.SQL.commit()
            


        
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

    modelID = 1

    BBid = 90
    
    interf = Interfaces()

    keys = ["BB Table","BB Plot","BB UserDef"]
    mod = ModuleBB(keys)
    (equipe,equipeC) = mod.addEquipmentDummy() #SD: creates almost empty rows
    mod.setEquipmentFromDB(equipe,equipeC,modelID) #SD: fills the rows with data from DBBoiler
#    mod.calculateEnergyFlows(equipe,equipeC,mod.cascadeIndex)
                    

#    mod.designAssistant1()
#    mod.designAssistant2(12)
