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
#	Version No.: 0.08
#	Created by: 	    Hans Schweiger	11/03/2008
#	Last revised by:    Tom Sobota          15/03/2008
#                           Enrico Facci /
#                           Hans Schweiger      24/03/2008
#                           Tom Sobota           1/04/2008
#                           Hans Schweiger      03/04/2008
#                           Enrico Facci        09/04/2008
#                           Stoyan Danov        16/04/2008
#                           Enrico Facci        24/04/2008
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
#       24/04/2008  functions added: designAssistant,automDeleteBoiler, designBB80, designBB140, designBBmaxTemp
#                   findmaxTemp. screenEquipments arranged in analogy with moduleHP.
#                   (HS: some clean-up of non-used functions and old comments)
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
#returns BBList to the GUI for displaying in window
        
        return (BBList)
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def screenEquipments(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------


        Status.int.getEquipmentCascade()
        self.BBList = []
        for row in Status.int.cascade:
        #    if row['equipeType'] == 'Heat pump' or row['equipeType'] == 'HeatPump' or row['equipeType'] == 'Heat Pump' or row['equipeType'] == 'HP COMP':
            if getEquipmentClass(row["equipeType"]) == "BB":
                self.BBList.append(row)

        BBTableDataList = []
        for row in Status.int.EquipTableDataList:
#            if row[2] == 'Heat pump' or row[2] == 'HeatPump' or row[2] == 'Heat Pump' or row[2] == 'HP COMP':
            if getEquipmentClass(row[2]) == "BB":
                BBTableDataList.append(row)

        #screen list and substitute None with "not available"
        for i in range(len(BBTableDataList)):
            for j in range(len(BBTableDataList[i])):
                if BBTableDataList[i][j] == None:
                    BBTableDataList[i][j] = 'not available'        

        if(len(self.BBList)>0):
            self.cascadeIndex = len(self.BBList) #by default sets selection to last BB in cascade
        else:
            self.cascadeIndex = 0
#XXXHS2008-04-02: he puesto cascadeIndex a 0 en vez de None: check que sea consistente esto ...

#        print '\n cascadeIndex =', self.cascadeIndex
        
        return (self.BBList,BBTableDataList)
        

        
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
    def add(self,BBId):
        """
        adds a new heat pump 
        """
        #--> add HP to the equipment list under current alternative
        print "add (BB): function not yet defined"

        self.calculateEnergyFlows(BBId)

        return "ok"



#------------------------------------------------------------------------------
    def getEqId(self,rowNo):
#------------------------------------------------------------------------------
#   gets the EqId from the rowNo in the BBList
#------------------------------------------------------------------------------

        BBId = self.BBList[rowNo]["equipeID"]
        return BBId

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def deleteEquipment(self,rowNo):
#------------------------------------------------------------------------------
        """
        deletes the selected boiler in the current alternative
        """
#------------------------------------------------------------------------------
        print "deleteBB: function not yet defined"

        if rowNo == None:   #indicates to delete last added equipment dummy
            BBid = self.dummyEqId
        else:
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
            
        self.sql.commit() #confirm storing to sql of new CascadeIndex #to be activated, SD

        print '\n deleteFromCascade():', 'new_cascade =', new_cascade


        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY EqNo ASC"%(Status.PId,Status.ANo)
        equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
##        print '\n \nequipments', equipments

        for i in range(len(equipments)): #assign new EqNo in QGenerationHC table
            equipments[i].EqNo = i+1

#        self.sql.commit() #to be activated, SD

        self.interface.deleteCascadeArrays(self.NEquipe)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def addEquipmentDummy(self):
#------------------------------------------------------------------------------
#       adds a new dummy equipment to the equipment list and returns the
#       position in the cascade 
#------------------------------------------------------------------------------

        print 'moduleBB (addEquipmentDummy): cascade Arrays initialised '
        self.cascadeIndex = self.NEquipe + 1
        EqNo = self.NEquipe + 1
        print 'ModuleBB (addEquipmentDummy): CascadeIndex', self.cascadeIndex
        print 'ModuleBB (addEquipmentDummy): EqNo', EqNo

        self.neweqs += 1 #No of last equip added
        NewEquipmentName = "New boiler %s"%(self.neweqs)

        EqNo = self.NEquipe + 1

        equipe = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo,"EqNo":EqNo,"Equipment":NewEquipmentName,"EquipType":"Boiler"}
        QGid = self.DB.qgenerationhc.insert(equipe)
        equipeC = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo,"QGenerationHC_id":QGid,"CascadeIndex":self.cascadeIndex}
        CGid = self.DB.cgenerationhc.insert(equipeC)

        self.dummyEqId = QGid #temporary storage of the equipment ID for undo if necessary
        
        Status.SQL.commit()

        Status.int.getEquipmentCascade()
        Status.int.addCascadeArrays()

        print "ModuleBB (addEquipmentDummy): new equip row created"
        print "ModuleBB (addEquipmentDummy): self.cascadeIndex", self.cascadeIndex

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

 
#------------------------------------------------------------------------------
    def sortBoiler (self): #xxx maybe other arguments needed !!!????
#------------------------------------------------------------------------------
#  sort boilers (self.equipmentsC) by temperature and by efficiency
#  Returns a list of boiler sorted by temperature and by efficiency and 3 more list of boiler (one of boiler
#    operating at T<=80°C, one of boiler operating at 80<T>=140, one of boiler till maxTemp).
#  function to be implemented
#------------------------------------------------------------------------------
        return bList80, bList140, bListmaxTemp
    
    
#------------------------------------------------------------------------------
    def automDeleteBoiler (self,minEfficencyAccepted=0.80):  #0.80 is a default value for minimum of efficiency
#------------------------------------------------------------------------------
# delete unefficient boiler
#------------------------------------------------------------------------------
        screenEqipments()
        for i in range (len (self.BBList)):
            if self.equipments[i].QGenerationHC_ID < minEfficencyAccepted:
#                 add the fuel criterion: if not biomass,biofuels?,gas methane ->delete ???
                deleteEquipment(self.equipments[i].QGenerationHC_ID)# The row number should be passed. is this right? 
                
                


#        i=0
#        a=[]    # a is an auxiliary variable
#        e=?     # position of the efficiency in the list of list of equipment 
#        while i<self.NEquipe +1:
#            if self.equipmentsC [i][e]>= minEfficiencyAccepted:
#                # add the fuel criterion: if not biomass,biofuels?,gas methane ->delete ???
#                a.append (self.equipmentsC [i][e])
#            i=i+1
#            return a
#        self.equipmentsC = a
# the equip should be deleted from the DB too
#        NEquip= len(self.equipmentsC) # better to use NEquip_mod?

#------------------------------------------------------------------------------
    def sortDemand(self,T):
#------------------------------------------------------------------------------
#       for each temperature sort the heat demand by power from max to min (the output is a monotonous descending function for each temperature level)
#       function to be implemented
#------------------------------------------------------------------------------
        return QDh_descending

#------------------------------------------------------------------------------
    def findmaxTemp(self,QDa):
#------------------------------------------------------------------------------
#       find the maximum temperature level of the heat demand
#       QDa is the annual heat demand by temperature
#------------------------------------------------------------------------------
        maxTemp=0
        for i in range(status.NT+1):
            if i>0:
                if QDa[i]>QDa[i-1]:
                    maxTemp=status.TemperatureInterval*(i+1) #temperatureInterval is defined in status.py
        return maxTemp

#------------------------------------------------------------------------------
    def selectBB(self,some_input_parameter):
#------------------------------------------------------------------------------
#    def selectBB(self,QDh_mod_descending[(maxTemp/status.TemperatureInterval)][1]):
#select the right bb from the database.
# function to be implemented
#------------------------------------------------------------------------------
        pass
        
#    def selectBB(self,power):
# select a boiler from the DB         
# function to be implemented


            
#------------------------------------------------------------------------------
    def designBB80(self):
#------------------------------------------------------------------------------
#    def designBB80(self,...):
# design a boiler sistem at 80°C
#------------------------------------------------------------------------------

        if self.interface.QD_T_mod[0][80/Status.TemperatureInterval] >= self.interface.QD_T_mod[0][maxTemp/Status.TemperatureInterval]:
            if QDh_descending[0]*securityMargin >= minPow:
                if QDh_descending[0]*securityMargin>=2*minPow:
                    if QDh_descending[0]*securityMargin < QDh_descending[minOpTime]*1.2 \
                       or (QDh_descending[0]*securityMargin - QDh_descending[minOpTime]) < minPow:

                        selectBB((QDh_descending[0]*securityMargin))  #select the right bb from the database.                        
#HS line not valid code                        selectBB((QDh_descending[0]*securityMargin),...)  #select the right bb from the database.
                        self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

#HS: elif requires a condition !!!                    elif:
                    else:
                        selectBB(QDh_descending[minOpTime])    #  select the base load boiler from DB
                        self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                        
                        if QDh_descending[0]*securityMargin - equipeC['HCGPnom']>= 2*minPow:
                            selectBB((QDh_descending[0]*securityMargin - equipeC['HCGPnom'])/2)
                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                        else:
#HS: elif requires a condition !!!                        elif:
                            selectBB(QDh_descending[0]*securityMargin - equipeC['HCGPnom'])
                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                else:
#HS: elif requires a condition !!!                elif:
                    selectBB(QD_descending[0]*securityMargin)
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

#HS: use "==" in comparisons in if, not "=" -> makes an assignment, not a comparison!!!
#HS: False is a standard key-word of python and has to be written uppercase
            if off==False:
#HS: here a condition is missing !!!
                what = True
                if what:#in the list of previously deleted equipmen exist a boiler with nominal power >= than all the bb in the equipment list :
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

                else:
#HS: elif requires a condition !!!                elif:
#HS: do not use python code for commenting
                    selectBB() #maximum nominal power of the boiler in list)
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

                
                        

                    

#------------------------------------------------------------------------------
    def designBB140(self):
#HS input list has to be defined !!!!    def designBB140(self,...):
#------------------------------------------------------------------------------
# design a boiler sistem at 140°C
#------------------------------------------------------------------------------

        if self.interface.QD_T_mod[0][140/Status.TemperatureInterval] >= self.interface.QD_T_mod[0][maxTemp/Status.TemperatureInterval]:
            if QDh_descending[0]*securityMargin >= minPow:
                if QDh_descending[0]*securityMargin>=2*minPow:
                    if QDh_descending[0]*securityMargin < QDh_descending[minOpTime]*1.2 or \
                    QDh_descending[0]*securityMargin -QDh_descending[minOpTime]<minPow:
                    
#HS TAKE CARE !!!! methods of the same class have to be called with the "self." before
#                   has probably to be corrected throughout the code ... !!!!
#                        selectBB((QDh_descending[0]*securityMargin)) # ,...)  #select the right bb from the database.
                        self.selectBB((QDh_descending[0]*securityMargin)) # ,...)  #select the right bb from the database.
                        self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

                    else:
#HS: elif requires a condition !!!                    elif:
                        self.selectBB(QDh_descending[minOpTime])    #  select the base load boiler from DB
                        self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

                        
                        if QDh_descending[0]*securityMargin - equipeC['HCGPnom']>= 2*minPow:
                            selectBB((QDh_descending[0]*securityMargin - equipeC['HCGPnom'])/2)
#twice the same ?? for being sure, if the first time fails ???                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                        else:
#HS: elif requires a condition !!!                        elif:
                            selectBB(QDh_descending[0]*securityMargin - equipeC['HCGPnom'])
                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                else:
#HS: elif requires a condition !!!                elif:
                    selectBB(QD_descending[0]*securityMargin)
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
#HS: off==False instead of off=false
            if off==False:
                what = True
                if what: #in the list of previously deleted equipmen exist a boiler with nominal power >= than all the bb in the equipment list :
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                else:
#HS: elif requires a condition !!!                elif:
                    selectBB() #maximum nominal power of the boiler in list)
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list


#------------------------------------------------------------------------------
    def designBBmaxTemp(self): #HS .........,maxTemp...):
#------------------------------------------------------------------------------
# design a boiler sistem at the maximum temperature of the heat demand
#------------------------------------------------------------------------------

        if QDh_descending[0]*securityMargin>=2*minPow:
            if QDh_descending[0]*securityMargin < QDh_descending[minOpTime]*1.2:
                selectBB((QDh_descending[0]*securityMargin)) #HS....,...)  #select the right bb from the database.
                self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

            else:
#HS            elif what????:
                selectBB(QDh_descending[minOpTime])    #  select the base load boiler from DB
                self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

                if QDh_descending[0]*securityMargin - equipeC['HCGPnom']>= 2*minPow:
                    selectBB((QDh_descending[0]*securityMargin - equipeC['HCGPnom'])/2)
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
#HS: elif requires a condition !!!                elif:
                else:
                    selectBB(QDh_descending[0]*securityMargin - equipeC['HCGPnom'])
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
#HS: elif requires a condition !!!        elif:
        else:
            selectBB(QD_descending[0]*securityMargin)
            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

#HSsame error than above ...
        if off==False:
            what = True
            if what: #HS ??? #in the list of previously deleted equipmen exist a boiler with nominal power >= than all the bb in the equipment list :
   #add the previously deleted boiler to the list for redundancy
                self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

#HS: elif requires a condition !!!            elif:
            else:
                selectBB() #maximum nominal power of the boiler in list)
                     #   select from the bb database a boiler to be used for redundancy
                self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
    
#------------------------------------------------------------------------------
    def designAssistant(self):
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


#            if (MaintainExistingEquipment == False):
#                deleteAllBoilers()
                        
        screenEqipments()
        for i in range (len (self.BBList)):
            
#HS blocks in a cycle have to be indented ...
            automDeleteBoiler()   # delete unefficient boiler
#HS cycle ends here, is this right ????
       
        sortBoiler()     # sort boilers by temperature (ascending) and by efficiency (descending)

        findmaxTemp(QDa)
                        
        exBP=0       #   power of the boiler in the cascade operating at 80°C
        for row in self.interface.cascade:

#HS error = instead of ==. corrected
#for the equipe types please use the standard type lists in constants.py. Stoyan explains you ...
#if you need additional types, just join them there ... !!!!
            
            if row['equipeType'] in ["boiler","Boiler"] and row['T']<=80:
                exBP += row['equipePnom']

        
        b= (max (self.interface.QD_Tt_mod [0][80/Status.TemperatureInterval]) * securityMargin) - exBP #   minimum power of the new boilers at 80°C
        c=[]
        for it in range (Status.Nt):
            c[it]= min (b, self.interface.QD_Tt[0][80/Status.TemperatureInterval][it])

        self.QDh80=c  # demand to be supplied by new boilers at 80°C

        sortDemand(80)
        designBB80()

        calculateCascade()

            
        
                        
        exBP=0       #   power of the boiler in the cascade operating at 140°C
        for row in self.interface.cascade:
#HS == vs. = error. please use default equipetype-list in constants.py !!!
            if row['equipeType'] in ["boiler","Boiler"] and row['T']<=140:
                exBP += row['equipePnom']

        cI= len(self.interface.QD_Tt_mod) +1     
        b= (max (self.interface.QD_Tt_mod[cI][140/Status.TemperatureInterval]) * securityMargin) - exBP #   minimum power of the new boilers at 140°C
        c=[]
        for it in range (Status.Nt):
            c[it]= min (b, self.interface.QD_Tt[cI][140/Status.TemperatureInterval][it])

        self.QDh140=c  # demand to be supplied by new boilers at 140°C

        sortDemand(140)               
        designBB140()

        calculateCascade()

        exBP=0       #   power of the boiler in the cascade operating at maxTemp
        for row in self.interface.cascade:

#HS == vs. = error. please use default equipetype-list in constants.py !!!
            if row['equipeType'] in ["boiler","Boiler"]:
                exBP += row['equipePnom']

        cI= len(self.interface.QD_Tt_mod)+1     
        b= (max (self.interface.QD_Tt_mod[cI][maxTemp/Status.TemperatureInterval]) * securityMargin) - exBP #   minimum power of the new boilers at maxTemp°C
        c=[]
        for it in range (Status.Nt):
            c[it]= min (b, self.interface.QD_Tt[cI][maxTemp/Status.TemperatureInterval][it])

        self.QDhmaxTemp=c  # demand to be supplied by new boilers at maxTemp°C

        sortDemand(maxTemp)               
        designBBmaxTemp()

        calculateCascade()


#..............................................................................                       

#        for k in (80,140,maxTemp)
                        
#           calculateCascade()

# QDh_mod represent the residual heat demand to be supplied by new boilers
#            sortDemand(QDh_mod,k) # sort the heat demand by number of hours

 #           for i in range (status.NT+1):
#                QDh_mod_descending[i][1]=QDh_mod_descending[i][1]*securityMargin  # for each temperature level only the first element (correspondig
#                                                                             # to 1 hour demand)is moltiplied for the security margin
#..............................................................................
#   At the moment I have considered 3 the heat demand temprature levels: 80, 140, maxTemp°C                                                                             
#..............................................................................
#            if k=80:
#                designBB80()
#            elif if k=140:
#                        designBB140()
#                 elif:
#                        designBBmaxTemp()
                
#            sortBoiler()

#            calculateCascade()
                        
      
        
        

        
    
#==============================================================================


if __name__ == "__main__":
    print "Testing ModuleBB"
    import einstein.GUI.pSQL as pSQL, MySQLdb
    from einstein.modules.interfaces import *
    from einstein.modules.energy.moduleEnergy import *
    stat = Status("testModuleBB")

    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    
    Status.PId = 2
    Status.ANo = 0

    interf = Interfaces()
    
    keys = ["BB Table","BB Plot","BB UserDef"]
    mod = ModuleBB(keys)
    (equipe,equipeC) = mod.addEquipmentDummy()
    mod.calculateEnergyFlows(equipe,equipeC,mod.cascadeIndex)
                    

#    mod.designAssistant1()
#    mod.designAssistant2(12)
