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
#                           Enrico Facci        05/05/2008
#                           Hans Schweiger      06/05/2008
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
#       05/05/2008  functions added: sortBoiler, redundancy, selectBB. Changes in designAssistant and designBB.
#       06/05/2008  Changes marked with ###HS in the text:
#                   - elimination of table cgenerationhc (now is in qgenerationhc)
#                   Status.int no longer used. substituted by Status.int
#                   Functions __init__, initPanel, updatePanel and
#                   screenEquipments modified in symmetry with moduleHP
#                   Function "setEquipmentFromDB" modified
#                   Bug corrections:    status.xxx -> Status.xxx
#                                       k=o -> k=0 (sortBoiler)
#                                       Status.ints -> Status.int (sortBoiler)
#                                       cascade[k].equipeType -> cascade[k]["equipeType"] (sortBoiler)
#                                       cascade[k].equipeID -> cascade[k]["equipeID"] (sortBoiler)
#                                       self.equipment -> self.equipments (sortBoiler)
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
from einstein.modules.constants import *

class ModuleBB(object):

    BBList = []
    
    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel
        Status.int = Interfaces()

        self.DB = Status.DB
        self.sql = Status.SQL

        self.neweqs = 0 #new equips added
        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        self.equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
        self.NEquipe = len(self.equipments)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

        Status.int.initCascadeArrays(self.NEquipe)        
        self.updatePanel()
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------

#............................................................................................
# 1. List of equipments

        (BBList,BBTableDataList) = self.screenEquipments()

        matrix = []
        for row in BBTableDataList:
            matrix.append(row)

        data = array(matrix)

        Status.int.setGraphicsData('BB Table',data)

#............................................................................................
# 2. XY Plot

        try:
            Status.int.setGraphicsData('BB Plot',[Status.int.T,
                                                      Status.int.QD_T_mod[self.cascadeIndex],
                                                      Status.int.QA_T_mod[self.cascadeIndex],
                                                      Status.int.QD_T_mod[self.cascadeIndex+1],
                                                      Status.int.QA_T_mod[self.cascadeIndex+1]])
        except:
            pass
#............................................................................................
# 3. Configuration design assistant

        config = [1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8]
        Status.int.setGraphicsData('BB Config',config)

    
#............................................................................................
# 4. additional information
        info = []
        info.append(99.99)  #first value to be displayed
        info.append(99.99)  #second value to be displayed

        Status.int.setGraphicsData('BB Info',info)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def screenEquipments(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#------------------------------------------------------------------------------


        Status.int.getEquipmentCascade()
        self.BBList = []
        for row in Status.int.cascade:
            if getEquipmentClass(row["equipeType"]) == "BB":
                self.BBList.append(row)

        BBTableDataList = []
        for row in Status.int.EquipTableDataList:
            if getEquipmentClass(row[3]) == "BB":
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
        return (self.BBList,BBTableDataList)
        

        
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
###HS: CGENERATIONHC ELIMINATED.        eqC = self.equipmentsC.QGenerationHC_id[BBid][0]

        eq.delete() #deletes the rows in both tables, to be activated later, SD
###HS: CGENERATIONHC ELIMINATED.        eqC.delete()
        self.sql.commit()

        #actuallise the cascade list: define deleteFromCascade
        self.deleteFromCascade(Status.int.cascade, BBid)

        self.NEquipe -= 1

#------------------------------------------------------------------------------
    def deleteFromCascade(self, cascade, BBid):
#------------------------------------------------------------------------------
        """
        deletes from the actual list casade and re-assigns the CascadeIndex values in QGenerationHC table
        """
#-----------------------------------------------------------------------------

#        print '\n deleteFromCascade():', 'cascade =', cascade

        idx = -1
        new_cascade = cascade
        for i in range(len(new_cascade)):
            if new_cascade[i]['equipeID'] == BBid:
                idx = i

        new_cascade.pop(idx)           

###HS: CGENERATIONHC CHANGED TO QGENERATIONHC
        for i in range(len(new_cascade)): #assign new CascadeIndex in CGenerationHC table
            eq = self.equipments.QGenerationHC_ID[new_cascade[i]['equipeID']][0]
            eq.CascadeIndex = i+1
#            print '\n new_CascadeIndex', eqC.CascadeIndex
            
        self.sql.commit() #confirm storing to sql of new CascadeIndex #to be activated, SD

        print '\n deleteFromCascade():', 'new_cascade =', new_cascade


        
        sqlQuery = "Questionnaire_ID = '%s' AND AlternativeProposalNo = '%s' ORDER BY EqNo ASC"%(Status.PId,Status.ANo)
        equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
##        print '\n \nequipments', equipments

        for i in range(len(equipments)): #assign new EqNo in QGenerationHC table
            equipments[i].EqNo = i+1

#        self.sql.commit() #to be activated, SD

        Status.int.deleteCascadeArrays(self.NEquipe)

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

        equipe = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo,"EqNo":EqNo,"Equipment":NewEquipmentName,"EquipType":"Boiler (specify subtype)","CascadeIndex":self.cascadeIndex}
        QGid = self.DB.qgenerationhc.insert(equipe)
###HS: CGENERATIONHC ELIMINATED.
        self.dummyEqId = QGid #temporary storage of the equipment ID for undo if necessary
        
        Status.SQL.commit()

        Status.int.getEquipmentCascade()
        Status.int.addCascadeArrays()

        print "ModuleBB (addEquipmentDummy): new equip row created"
        print "ModuleBB (addEquipmentDummy): self.cascadeIndex", self.cascadeIndex

        self.equipe = self.equipments.QGenerationHC_ID[QGid][0]
###HS: CGENERATIONHC ELIMINATED.        self.equipeC = self.equipmentsC.CGenerationHC_ID[CGid][0]

        return(self.equipe)


#------------------------------------------------------------------------------

###HS: CGENERATIONHC ELIMINATED IN INPUT LIST.
#------------------------------------------------------------------------------
    def setEquipmentFromDB(self,equipe,modelID):
#------------------------------------------------------------------------------
#   takes an equipment from the data base and stores it under a given Id in
#   the equipment data base
#------------------------------------------------------------------------------

        model = self.DB.dbboiler.DBBoiler_ID[modelID][0]

        if model.BBPnom != None: equipe.update({"HCGPnom":model.BBPnom})
        if model.BBEfficiency != None: equipe.update({"HCGTEfficiency":model.BBEfficiency})
#        if model.BoilerTemp != None: equipe.update({"TMax":model.BoilerTemp})
        if model.BoilerManufacturer != None: equipe.update({"Manufact":model.BoilerManufacturer})
        if model.BoilerModel != None: equipe.update({"Model":model.BoilerModel})
        equipe.update({"EquipType":getEquipmentType("BB",model.BoilerType)})
        equipe.update({"NumEquipUnits":1})
        if model.BoilerType != None: equipe.update({"EquipTypeFromDB":model.BoilerType})
        if model.DBBoiler_ID != None: equipe.update({"EquipIDFromDB":model.DBBoiler_ID})
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
        
        EquipmentNo = Status.int.cascade[cascadeIndex]["equipeNo"]

        print 'ModuleBB (calculateEnergyFlows): Model = ', BBModel, ' Type = ', BBType, 'PNom = ', PNom

#..............................................................................
# get demand data for CascadeIndex/EquipmentNo from Interfaces
# and create arrays for storing heat flow in equipment

        QD_Tt = Status.int.QD_Tt_mod[cascadeIndex]
        QA_Tt = Status.int.QA_Tt_mod[cascadeIndex]
        
        USHj_Tt = Status.int.createQ_Tt()
        USHj_T = Status.int.createQ_T()

        
        QHXj_Tt = Status.int.createQ_Tt()
        QHXj_T = Status.int.createQ_T()

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
                if TMax >= Status.int.T[iT] :   #TMax is the max operating temperature of the boiler 
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
        Interfaces.QD_T_mod[cascadeIndex+1] = Status.int.calcQ_T(QD_Tt)
        Interfaces.QA_Tt_mod[cascadeIndex+1] = QA_Tt
        Interfaces.QA_T_mod[cascadeIndex+1] = Status.int.calcQ_T(QA_Tt)

# heat delivered by present equipment                            
        Interfaces.USHj_Tt[cascadeIndex] = USHj_Tt
        Interfaces.USHj_T[cascadeIndex] = Status.int.calcQ_T(USHj_Tt)

# waste heat absorbed by present equipment                            
        Interfaces.QHXj_Tt[cascadeIndex] = QHXj_Tt
        Interfaces.QHXj_T[cascadeIndex] = Status.int.calcQ_T(QHXj_Tt)

#        equipeC.USHj = USHj
#        equipeC.QHXj = QHXj    #XXX to be defined in data base

        print "Total energy supplied by equipment ",USHj, " MWh"
        print "Total waste heat input  ",QHXj, " MWh"

        return USHj    


#==============================================================================

 
#------------------------------------------------------------------------------
    def sortBoiler (self): 
#------------------------------------------------------------------------------
#   moove all the boilers to the end of the cascade.
#  sorts boilers by temperature and by efficiency
#------------------------------------------------------------------------------
####TAKE CARE: if you look for a property of the equipment at position k in the cascade, you have to look up for it by its ID:
# e.g. the equipment with myID can be found by
#            self.equipments.QGenerationHC_ID[myID][0]
#   and it's efficiency with
#   my_eta = self.equipments.QGenerationHC_ID[myID][0].HCGTEfficiency
#
#           you can also write the following in a more clearer way:
#
#   my_equipment = self.equipments.QGenerationHC_ID[myID][0]
#   my_eta = my_equipment.HCGTEfficiency
#
#
#   A shorter way to get the equipes already sorted into a table is
#        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY CascadeIndex ASC"%(Status.PId,Status.ANo)
#        all_my_equipments_sorted = self.DB.qgenerationhc.sql_select(sqlQuery)
#
#   Then you can access to the n'th equipment in the cascade just by
#   my_nth_equipe = all_my_equipments_sorted[n-1] -> listings in python are like in C, from 0 to n-1, not from 1 to n !!!
#
# as an example I try to re-write your code a little bit more efficiently:
#
#ORIGINAL CODE:
#        k=0
#        while k<len(Status.int.cascade):
#            if getEquipmentClass(Status.int.cascade[k]["equipeType"]) == "BB":
#                a=0
#                for h in range (k,len (Status.int.cascade)):
#
#                    if self.equipment[Status.int.cascade[k]["equipeID"]].HCGTEfficiency < self.equipments[Status.int.cascade[k].equipeID].HCGTEfficiency:
#                        a=h-k
#                for l in range(a):
#                    self.moduleHC.cascadeMoveDown(k+l)
#            if a>0:
#                k=k-1
#            k=k+1
#NEW CODE:

#first bring all your boilers in a listing for easier access

        boilerList = []
        for i in range(len(Status.int.cascade)):
            entry = Status.int.cascade[i]
            if entry["equipeType"]=="BB":
                eqID = entry["equipeID"]
                equipe = self.equipments.QGenerationHC_ID[eqID][0]
                efficiency = equipe.HCGTEfficiency
                boilerList.append({"equipeID":eqID,"efficency":efficiency})

        print "ModuleBB (sortBoiler): first step done - boilerList created"
        print boilerList

#then reorganise boilerList by efficiencies (maybe there are more intelligent ways to do this, but here's one ...:
# if you want the most efficient on top [n-1] instead on bottom [0], just change the sign of the comparison from > to <

        for i in range(len(boilerList)):
            for j in range(i,len(boilerList)):
                if boilerList[j]["efficiency"] > boilerList[i]["efficiency"]:
                    bi = boilerList[i]
                    bj = boilerList[j]
                    boilerList[i] = bj
                    boilerList[j] = bi

        print "ModuleBB (sortBoiler): seceond step done - boilerList ordered"
        print boilerList

#then move consecutively to the bottom of the cascade (move the one last, which you finally want to have at the bottom

        for i in range(len(boilerList)):
            eqID = boilerList[i]["equipeID"]
            equipe = self.equipments.QGenerationHC_ID[eqID][0]
            cascadeIndex = equipe.CascadeIndex
            Status.mod.moduleHC.cascadeMoveToBottom(cascadeIndex)

        print "ModuleBB (sortBoiler): third step done - shift in cascade carried out"
        print Status.int.cascade

#OR JUST CORRECTING YOUR CODE (don't understand it so I can't say if it should work or not ...):
                
        k=0
        while k<len(Status.int.cascade):
            if getEquipmentClass(Status.int.cascade[k]["equipeType"]) == "BB":
                a=0
                for h in range (k,len (Status.int.cascade)):
                    equipe_k = self.equipments.QGenerationHC_ID[Status.int.cascade[k]["equipeID"]][0]
                    equipe_h = self.equipments.QGenerationHC_ID[Status.int.cascade[h]["equipeID"]][0]
                    if equipe_h.HCGTEfficiency < equipe_k.HCGTEfficiency:   #check if h and k has to be changed !!!
                        a=h-k
                for l in range(a):
                    Status.mod.moduleHC.cascadeMoveDown(k+l)
            if a>0:
                k=k-1
            k=k+1

        for i in range (len(Status.int.cascade)):
#            if getEquipmentClass(Status.int.cascade[i].equipeType)=="BB" and self.equipments[Status.int.cascade[i].equipeID].Temp <=90:
            equipe = self.equipments.QGenerationHC_ID[Status.int.cascade[i]["equipeID"]][0]
#            if getEquipmentClass(Status.int.cascade[i]["equipeType"])=="BB" and equipe.Temp <=90:
            if getEquipmentClass(Status.int.cascade[i]["equipeType"])=="BB" and equipe.TExhaustGas <=90:    #use TExhaustGas until we have an update of the SQL
                Status.mod.moduleHC.cascadeMoveToBottom(i)
                aa=Status.int.cascade[len(Status.int.cascade)-1]["equipeID"]  #aa is the ID of the last boiler at 80°C

#####TAKE CARE: return means, that the function stops here !!!!
#            return aa
#        for i in range (len(Status.int.cascade)):
#            if getEquipmentClass(Status.int.cascade[i].equipeType)=="BB" and self.equipments[Status.int.cascade[i].equipeID].Temp >90 and \
#               self.equipments[Status.int.cascade[i].equipeID].Temp <=150:                           
#                Status.int.cascadeMoveToBottom(i)
#                bb=Status.int.cascade[len(Status.int.cascade)-1].equipeID #  #bb is the ID of the last boiler at 140°C
#        for i in range (len(Status.int.cascade)):
#            if getEquipmentClass(Status.int.cascade[i].equipeType)=="BB" and self.equipments[Status.int.cascade[i].equipeID].Temp >150:
#                Status.int.cascadeMoveToBottom(i)
#                cc=Status.int.cascade[len(Status.int.cascade)-1].equipeID #  #bb is the ID of the last boiler at maxTemp
#            return cc
#        self.firstBB = 0
#        for i in range (len(Status.int.cascade)):
#            if getEquipmentClass(Status.int.cascade[i].equipeType)=="BB" :
#                self.firstBB = i
#            break
            
#        self.lastBB80=self.equipments[aa].CascadeIndex
#        self.lastBB140=self.equipments[bb].CascadeIndex
#        self.lastBB=self.equipments[cc].CascadeIndex


    
    
#------------------------------------------------------------------------------
    def automDeleteBoiler (self,minEfficencyAccepted=0.80):  #0.80 is a default value for minimum of efficiency
#------------------------------------------------------------------------------
# delete unefficient boiler
#------------------------------------------------------------------------------
        self.screenEquipments()
        for i in range (len (self.BBList)):
            if self.equipments[i].QGenerationHC_ID < minEfficencyAccepted:
#                 add the fuel criterion: if not biomass,biofuels?,gas methane ->delete ???
                self.deleteEquipment(self.equipments[i].QGenerationHC_ID)# The row number should be passed. is this right? 
                
                


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
        for i in range(Status.NT+1):
            if i>0:
                if QDa[i]>QDa[i-1]:
                    maxTemp=Status.TemperatureInterval*(i+1) #temperatureInterval is defined in status.py
        return maxTemp


#------------------------------------------------------------------------------
    def redundancy(self):
#------------------------------------------------------------------------------
#       when redundancy is required provides suitable boilers.
#       N.B. the possibility of retriveing deleted boilers is not implemented yet.
#------------------------------------------------------------------------------      

        self.maxPow80=0
        self.maxPow140=0
        self.maxPowTmax=0
        for k in range(len(Status.int.cascade)):
            if getEquipmentClass(Status.int.cascade.equipeType) == "BB":
                if self.equipments[Status.int.cascade[k].equipeID].Temp <=90 and \
                   Status.int.cascade[k].Pnom > self.maxPow80:
                    self.maxPow80 =Status.int.cascade[k].Pnom
                elif 90< self.equipments[Status.int.cascade[k].equipeID].Temp <= 150 and \
                     Status.int.cascade[k].Pnom > self.maxPow140:
                    self.maxPow140 =Status.int.cascade[k].Pnom
                elif Status.int.cascade[k].Pnom > self.maxPowTmax:
                    self.maxPowTmax =Status.int.cascade[k].Pnom
        if self.maxPow80>0:
            self.selectBB(self.maxPow80)
            self.setEquipmentFromDB(equipe,equipeC,modelID)
        if self.maxPow140>0:
            self.selectBB(self.maxPow140)
            self.setEquipmentFromDB(equipe,equipeC,modelID)
        self.selectBB(self.maxPowTmax)
        self.setEquipmentFromDB(equipe,equipeC,modelID)




#------------------------------------------------------------------------------
    def selectBB(self,Pow,Top):
#------------------------------------------------------------------------------
#  the query should consider the fuel too but at the moment the fuel column doesn't exist in mySQL.
#  we could give the possibility to choose the boiler to the user (in the interactive mode) in the 'selected' list. In this version we take the first  
#  element of the list
#------------------------------------------------------------------------------

        sqlQuery="BoilerTemp >= '%s'AND BBPnom >= '%s' ORDER BY BoilerTemp AND BBPnom ASC" %(Top,Pow)       
        selected = Status.DB.dbboiler.sql_select(sqlQuery)
        modelID =selected[0].DBBoiler_ID
        return (modelID)
        


            
#------------------------------------------------------------------------------
    def designBB80(self):
#------------------------------------------------------------------------------
#    def designBB80(self,...):
# design a boiler sistem at 80°C
#------------------------------------------------------------------------------

        if Status.int.QD_T_mod[0][80/Status.TemperatureInterval] >= Status.int.QD_T_mod[0][maxTemp/Status.TemperatureInterval]:
            if self.QDh80[0]*securityMargin >= minPow:
                if self.QDh80[0]*securityMargin>=2*minPow:
                    if self.QDh80[0]*securityMargin < self.QDh80[minOpTime]*1.2 \
                       or (self.QDh80[0]*securityMargin - self.QDh80[minOpTime]) < minPow:

                        self.selectBB((self.QDh80[0]*securityMargin))  #select the right bb from the database.                        
#HS line not valid code                        selectBB((QDh_descending[0]*securityMargin),...)  #select the right bb from the database.
                        self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

#HS: elif requires a condition !!!                    elif:
                    else:
                        self.selectBB(self.QDh80[minOpTime])    #  select the base load boiler from DB
                        self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                        
                        if self.QDh80[0]*securityMargin - equipeC['HCGPnom']>= 2*minPow:
                            selectBB((self.QDh80[0]*securityMargin - equipeC['HCGPnom'])/2)
                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                        else:
#HS: elif requires a condition !!!                        elif:
                            self.selectBB(self.QDh80[0]*securityMargin - equipeC['HCGPnom'])
                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                else:
#HS: elif requires a condition !!!                elif:
                    self.selectBB(self.QDh80[0]*securityMargin)
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list


        self.sortBoiler()                
                        

                    

#------------------------------------------------------------------------------
    def designBB140(self):
#HS input list has to be defined !!!!    def designBB140(self,...):
#------------------------------------------------------------------------------
# design a boiler sistem at 140°C
#------------------------------------------------------------------------------

        if Status.int.QD_T_mod[0][140/Status.TemperatureInterval] >= Status.int.QD_T_mod[0][maxTemp/Status.TemperatureInterval]:
            if self.QDh140[0]*securityMargin >= minPow:
                if self.QDh140[0]*securityMargin>=2*minPow:
                    if self.QDh140[0]*securityMargin < self.QDh140[minOpTime]*1.2 or \
                    self.QDh140[0]*securityMargin -self.QDh140[minOpTime]<minPow:
                    
#HS TAKE CARE !!!! methods of the same class have to be called with the "self." before
#                   has probably to be corrected throughout the code ... !!!!
#                        selectBB((QDh_descending[0]*securityMargin)) # ,...)  #select the right bb from the database.
                        self.self.selectBB((self.QDh140[0]*securityMargin)) # ,...)  #select the right bb from the database.
                        self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

                    else:
#HS: elif requires a condition !!!                    elif:
                        self.selectBB(self.QDh140[minOpTime])    #  select the base load boiler from DB
                        self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

                        
                        if self.QDh140[0]*securityMargin - equipeC['HCGPnom']>= 2*minPow:
                            self.selectBB((self.QDh140[0]*securityMargin - equipeC['HCGPnom'])/2)
#twice the same ?? for being sure, if the first time fails ???                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                        else:
#HS: elif requires a condition !!!                        elif:
                            self.selectBB(self.QDh140[0]*securityMargin - equipeC['HCGPnom'])
                            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                else:
#HS: elif requires a condition !!!                elif:
                    self.selectBB(self.QDh140[0]*securityMargin)
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

        self.sortBoiler()
#------------------------------------------------------------------------------
    def designBBmaxTemp(self): #HS .........,maxTemp...):
#------------------------------------------------------------------------------
# design a boiler sistem at the maximum temperature of the heat demand
#------------------------------------------------------------------------------

        if self.QDhmaxTemp[0]*securityMargin>=2*minPow:
            if self.QDhmaxTemp[0]*securityMargin < self.QDhmaxTemp[minOpTime]*1.2:
                self.selectBB((self.QDhmaxTemp[0]*securityMargin)) #HS....,...)  #select the right bb from the database.
                self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

            else:

                self.selectBB(self.QDhmaxTemp[minOpTime])    #  select the base load boiler from DB
                self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

                if self.QDhmaxTemp[0]*securityMargin - equipeC['HCGPnom']>= 2*minPow:
                    self.selectBB((self.QDhmaxTemp[0]*securityMargin - equipeC['HCGPnom'])/2)
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

                else:
                    self.selectBB(self.QDhmaxTemp[0]*securityMargin - equipeC['HCGPnom'])
                    self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list

        else:
            self.selectBB(self.QDhmaxTemp[0]*securityMargin)
            self.setEquipmentFromDB(equipe,equipeC,modelID)   #assign model from DB to current equipment in equipment list


        self.sortBoiler()
    
#------------------------------------------------------------------------------
    def designAssistant(self):
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


#            if (MaintainExistingEquipment == False):
#                deleteAllBoilers()
                        
        self.screenEquipments()
 
        self.automDeleteBoiler()   # delete unefficient boiler

        self.findmaxTemp(Status.int.QD_T)
       
        self.sortBoiler()     # sort boilers by temperature (ascending) and by efficiency (descending)
                        
        exBP=0       #   power of the boiler in the cascade operating at 80°C
        for row in Status.int.cascade:

#for the equipe types please use the standard type lists in constants.py. Stoyan explains you ...
#if you need additional types, just join them there ... !!!!
            
            if getEquipmentClass(row["equipeType"]) == "BB" and row['Temp']<=80:
                exBP += row['equipePnom']

        
        b= (max (Status.int.QD_Tt_mod [self.firstBB][80/Status.TemperatureInterval]) * securityMargin) - exBP #   minimum power of the new boilers at 80°C
        c=[]
        for it in range (Status.Nt):
            c[it]= min (b, Status.int.QD_Tt[self.firstBB][80/Status.TemperatureInterval][it])

        self.QDh80=c  # demand to be supplied by new boilers at 80°C

        self.QDh80.sort(reverse=True)
        self.designBB80()

        for k in range (self.firstBB , self.lastBB80+1):
            calculateEnergyFlows(equipe,k)

            
        
                        
        exBP=0       #   power of the boiler in the cascade operating at 140°C
        for row in Status.int.cascade:

            if getEquipmentClass(row["equipeType"]) == "BB" and row['Temp']<=140:
                exBP += row['equipePnom']

             
        b= (max (Status.int.QD_Tt_mod[self.lastBB80 +1][140/Status.TemperatureInterval]) * securityMargin) - exBP #   minimum power of the new boilers at 140°C
        c=[]
        for it in range (Status.Nt):
            c[it]= min (b, Status.int.QD_Tt[self.lastBB80 +1][140/Status.TemperatureInterval][it])

        self.QDh140=c  # demand to be supplied by new boilers at 140°C

        self.QDh140.sort(reverse=True)
#        self.sortDemand(140)               
        self.designBB140()

        for k in range (self.lastBB80+1 , self.lastBB140+1):
            calculateEnergyFlows(equipe,k)


        exBP=0       #   power of the boiler in the cascade operating at maxTemp
        for row in Status.int.cascade:


            if getEquipmentClass(row["equipeType"]) == "BB":
                exBP += row['equipePnom']

        cI= len(Status.int.QD_Tt_mod)+1     
        b= (max (Status.int.QD_Tt_mod[self.lastBB140 +1][maxTemp/Status.TemperatureInterval]) * securityMargin) - exBP #   minimum power of the new boilers at maxTemp°C
        c=[]
        for it in range (Status.Nt):
            c[it]= min (b, Status.int.QD_Tt[self.lastBB140 +1][maxTemp/Status.TemperatureInterval][it])

        self.QDhmaxTemp=c  # demand to be supplied by new boilers at maxTemp°C

        self.QDhmaxTemp.sort(reverse=True)
#        self.sortDemand(maxTemp)               
        self.designBBmaxTemp()

        for k in range (self.lastBB140+1 , self.lastBB+1):
            calculateEnergyFlows(equipe,k)


        if off== False:
            self.redundancy()
            


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

    Status.int = Interfaces()
    
    keys = ["BB Table","BB Plot","BB UserDef"]
    mod = ModuleBB(keys)
    equipe = mod.addEquipmentDummy()
    mod.calculateEnergyFlows(equipe,mod.cascadeIndex)
                    

#    mod.designAssistant1()
#    mod.designAssistant2(12)
