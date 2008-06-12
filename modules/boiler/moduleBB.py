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
#	Version No.: 0.09
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
#                           Enrico Facci        07/05/2008
#                           Enrico Facci        13/05/2008
#                           Hans Schweiger      15/04/2008
#                           Enrico Facci        26/05/2008
#                           Enrico Facci        06/06/2008
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
#       07/05/2008  sortBoiler modified and tested.
#       12/05/2008  function added: findBiggerBB. some changes in designAssistant, selectBB, designBB80 and calculateEnergyFlows.
#       16/05/2008  some small notes marked with ###HS2008-05-16
#                   (by the way eliminated some old comments that are no longer useful)
#                   => changes in updatePanel
#                   => "userDefinedPars"-Functions copied from HP (not working yet)
#       26/05/2008 some changes in functions sortBoiler, designAssistant, redundancy                   
#       06/06/2008 implemented function updatePannel. Some small changes in designAsssistant
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
        Status.mod.moduleEnergy.runSimulation()
        Status.int.printCascade()
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
# 2. Preparing data
        self.findmaxTemp(Status.int.QD_T)
        print "maximum temperature",self.maxTemp
        PowerSum80=0
        PowerSum140=0
        PowerSumTmax=0
        if self.maxTemp>80:
            if self.maxTemp>160: # the minimum temperature difference is now setted at 20°C but could even be a parameter
                for i in BBList:
                    if self.equipments.QGenerationHC_ID[i["equipeID"]][0]["TExhaustGas"]>80 and \
                                                        self.equipments.QGenerationHC_ID[i["equipeID"]][0]["TExhaustGas"]<=140:
                        PowerSum140 +=i["equipePnom"]
                    if self.equipments.QGenerationHC_ID[i["equipeID"]][0]["TExhaustGas"]>140:
                        PowerSumTmax += i["equipePnom"]
            else :
                for i in BBList:
                    if self.equipments.QGenerationHC_ID[i["equipeID"]][0]["TExhaustGas"]>80:
                        PowerSumTmax += i["equipePnom"]
            print "starting block for calculation of PowerSum80"
            for i in BBList:
                print "i = ",i
                print "TExhaustGas = ",self.equipments.QGenerationHC_ID[i["equipeID"]][0]["TExhaustGas"]
                if self.equipments.QGenerationHC_ID[i["equipeID"]][0]["TExhaustGas"]<=80:
                    PowerSum80 += i["equipePnom"]
                    print "PowerSum80",PowerSum80
        else:
            for i in BBList:
               PowerSumTmax += i["equipePnom"] 

        if len(BBList)==0:
            index=len(self.equipments)-1
        else:
            index = self.equipments.QGenerationHC_ID[BBList[0]["equipeID"]][0]["CascadeIndex"]
        print "length of QD_Tt_mod is", len(Status.int.QD_Tt_mod)
        print "the element we are looking at is", index
        QD80C=Status.int.QD_Tt_mod[index-1][int(80/Status.TemperatureInterval)]
        QD80C.sort(reverse=True)
        print "QD80C: ",QD80C
        print "the maximum power required at 80°C is",QD80C[0]
        if self.maxTemp>160: # the minimum temperature difference is now setted at 20°C but could even be a parameter
            QD140C=Status.int.QD_Tt_mod[index-1][int(140/Status.TemperatureInterval)]
            QD140C.sort(reverse=True)
            print "QD140C: ",QD140C
        else:
            QD140C=[]
            for i in range(len(QD80C)):
                QD140C.append(0)
        QDmaxTemp=Status.int.QD_Tt_mod[index-1][int(self.maxTemp/Status.TemperatureInterval)]
        QDmaxTemp.sort(reverse=True)
        print "QDmaxTemp: ",QDmaxTemp
        print "the maximum power required at maxTemp is",QDmaxTemp[0]                
#............................................................................................
# 2. XY Plot
        TimeIntervals=[]
        for it in range(Status.Nt+1):
            TimeIntervals.append(1.0*(it+1))
#        print "TimeInterval len is", len(TimeIntervals)
#        print "demand len is", len(QD80C)
        if self.maxTemp>160:
            try:
                Status.int.setGraphicsData('BB Plot',[TimeIntervals,
                                                            QD80C,
                                                            QD140C,
                                                            QDmaxTemp])
            except:
                pass
        else:
            if self.maxTemp>80:
                try:
                    Status.int.setGraphicsData('BB Plot',[TimeIntervals,
                                                                QD80C,
                                                                QD140C,
                                                                QDmaxTemp])
                except:
                    pass
            else:
                try:
                    Status.int.setGraphicsData('BB Plot',[TimeIntervals,
                                                                QD80C])
                except:
                    pass
#        try:

#####ENRICO, you should substitute this by the graphics you want to show
#            Status.int.setGraphicsData('BB Plot',[Status.int.T,
#                                                      Status.int.QD_T_mod[self.cascadeIndex],
#                                                      Status.int.QA_T_mod[self.cascadeIndex],
#                                                      Status.int.QD_T_mod[self.cascadeIndex+1],
#                                                      Status.int.QA_T_mod[self.cascadeIndex+1]])
###HS2008-05-16
# This is how it should look like:
# Time interval should be a list containing the time steps of the data file
# You can use 0,1,2,3 .... 8760 or just a subset, e.g. 0,10,20,...
#   CHD should be the demand curves, probably something like
#   for i in range(Status.Nt):
#       CHD1[it] = QD_Tt_mod[self.cascadeIndex_boiler1][NT1][it] #NT1 is the index of a given temperature level
#       CHD2[it] = QD_Tt_mod[self.cascadeIndex_boiler1][NT2][it] #NT1 is the index of a given temperature level
#       CHD3[it] = QD_Tt_mod[self.cascadeIndex_boiler1][NT3][it] #NT1 is the index of a given temperature level
#       ...
#       Supply1 = USHj_Tt[self.cascadeIndex_boiler1][it]
#       Supply2 = USHj_Tt[self.cascadeIndex_boiler2][it]
#       Supply3 = USHj_Tt[self.cascadeIndex_boiler3][it]
#
#   Take care: the length of TimeIntervals and the data lists CHD1..3,Supply1..3 should be identical.
#   Tell me how much curves you want to display. actually the GUI shows 4, and I don't know if it adapts automatically
#   to more than 4 (should be so, but I'm not sure. I'll check it in the meanwhile)
#
#            Status.int.setGraphicsData('BB Plot',[TimeIntervals,
#                                                      CHD1,
#                                                      CHD2,
#                                                      CHD3,
#                                                      Supply1,
#                                                      Supply2,
#                                                      Supply3])

#            pass
        
#        except:
#            pass
#............................................................................................
#this is just a test. you should substitute the 2nd - nth "TimeIntervals" by the right list
# i put it here out of the try-except, in order to SEE the error messages, if they occur
# afterwards should be returned to WITHIN the try-except.
#............................................................................................
#        TimeIntervals = []
#        CHD_80 = []
#        NT80 = int(ceil(80/Status.TemperatureInterval))
#        for it in range(Status.Nt):
#            TimeIntervals.append(1.0*(it+1))
#            CHD_80.append(Status.int.QD_Tt_mod[self.cascadeIndex][NT80][it]/Status.TimeStep)
#                          
#        CHD_80.sort()
#        CHD_80.reverse()
            
#        Status.int.setGraphicsData('BB Plot',[TimeIntervals,
#                                            CHD_80,
#                                            TimeIntervals,
#                                            TimeIntervals,
#                                            TimeIntervals])

#............................................................................................
#............................................................................................
# 3. Configuration design assistant

###HS2008-05-16: these are the values for the design assistant
# (Config field). Should later on be taken from U-table in SQL

        config = self.getUserDefinedPars()
        Status.int.setGraphicsData('BB Config',config)

    
#............................................................................................
# 4. additional information

###HS2008-05-16: here is what is displayed on the right side of the panel
# (Info field)
        info = []
        info.append(10)  #first value to be displayed
        info.append(max(0,(QD80C[0]-PowerSum80)))  #power for T-level
        if self.maxTemp>160:
            info.append(max(0,(QD140C[0]-QD80C[0]-PowerSum140)))  #power for T-level
            info.append(max(0,(QDmaxTemp[0]-QD140C[0]-PowerSummaxTemp)))  #power for T-level
        else:
            info.append(0)
            if self.maxTemp>80:
                info.append(max(0,(QDmaxTemp[0]-QD80C[0]-PowerSumTmax)))  #power for T-level
            else:
                info.append(0)


        Status.int.setGraphicsData('BB Info',info)

#------------------------------------------------------------------------------

###HS2008-05-16: these functions are just copied from HP module
### have to be adapted for boiler module
#------------------------------------------------------------------------------
    def getUserDefinedPars(self):
#------------------------------------------------------------------------------
#   gets the user defined data from UHeatPump and stores it to interfaces to be shown in HP panel
#------------------------------------------------------------------------------

        urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]

        if len(urows) == 0:
            print 'getUserDefinedParamBB: Status.PId =', Status.PId, 'Status.ANo =', Status.ANo, 'not defined'
            print 'Error: confusion in PId and ANo'
            maintainExisting = True
            config = [False,10,True,"Natural Gas",100,500,85]            

        else:
            u = urows[0]
            config = [u.BBMaintain,
                      u.BBSafety,
                      u.BBRedundancy,
                      u.BBFuelType,
                      u.BBHOp,
                      u.BBPmin,
                      u.BBEff]
            print "ModuleBB (getUserDefinedPars): config = ",config
        return config

#------------------------------------------------------------------------------
    def setUserDefinedPars(self):
#------------------------------------------------------------------------------

        config = Status.int.GData['BB Config']

        urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
        
        if len(urows)==0:
            print "ModuleBB(setUserDefinedParamHP): corrupt data base - no entry for uheatpump under current ANo"
            dummy = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo} 
            Status.DB.uheatpump.insert(dummy)
            urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
            
        u = urows[0]

#        row.MaintainExisting = UDList[0] # to add in UHeatPump
        u.BBMaintain = config[0]
        u.BBSafety = config[1]
        u.BBRedundancy = config[2]
        u.BBFuelType = config[3]
        u.BBHOp = config[4]
        u.BBPmin = config[5]
        u.BBEff = config[6]

        Status.SQL.commit()

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
    def deleteEquipment(self,rowNo,automatic=False):
#------------------------------------------------------------------------------
        """
        deletes the selected boiler in the current alternative
        """
#------------------------------------------------------------------------------

        if automatic == False:
            if rowNo == None:   #indicates to delete last added equipment dummy
                BBid = self.dummyEqId
            else:
            #--> delete BB from the equipment list under current alternative #from C&QGenerationHC under ANo
                BBid = self.getEqId(rowNo)
                print "Module BB (delete): id to be deleted = ",BBid
        else:
            BBid= rowNo
            print "Module BB (delete automaticly): id to be deleted = ",BBid
        
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

        equipe = {"Questionnaire_id":Status.PId,\
                  "AlternativeProposalNo":Status.ANo,\
                  "EqNo":EqNo,"Equipment":NewEquipmentName,\
                  "EquipType":"Boiler (specify subtype)","CascadeIndex":self.cascadeIndex}
        
        QGid = self.DB.qgenerationhc.insert(equipe)
###HS: CGENERATIONHC ELIMINATED.
        self.dummyEqId = QGid #temporary storage of the equipment ID for undo if necessary
        
        Status.SQL.commit()

        Status.int.getEquipmentCascade()
        Status.int.addCascadeArrays()

        print "ModuleBB (addEquipmentDummy): new equip row created"
        print "ModuleBB (addEquipmentDummy): self.cascadeIndex", self.cascadeIndex

###HS2008-05-16: added this three lines for security. had an error when adding an equipment in a project built from scratch. to be tested
#                   later on ...
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        self.equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
        self.NEquipe = len(self.equipments)

        self.equipe = self.equipments.QGenerationHC_ID[QGid][0]

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
        print "setting equipment from DB"
        if model.BBPnom != None: equipe.update({"HCGPnom":model.BBPnom})
        if model.BBEfficiency != None: equipe.update({"HCGTEfficiency":model.BBEfficiency})
#        if model.BoilerTemp != None: equipe.update({"TMax":model.BoilerTemp})
        if model.BoilerTemp != None: equipe.update({"TExhaustGas":model.BoilerTemp}) # This line has to be changed when an appropriate field will be insert in qgenerationhc
        if model.BoilerManufacturer != None: equipe.update({"Manufact":model.BoilerManufacturer})
        if model.BoilerModel != None: equipe.update({"Model":model.BoilerModel})
        equipe.update({"EquipType":getEquipmentType("BB",model.BoilerType)})
        equipe.update({"NumEquipUnits":1})
        if model.BoilerType != None: equipe.update({"EquipTypeFromDB":model.BoilerType})
        if model.DBBoiler_ID != None: equipe.update({"EquipIDFromDB":model.DBBoiler_ID})
        Status.SQL.commit()
        print "cascade index is:",
        print "demand before the add",self.cascadeIndex-1
        print Status.int.QD_Tt_mod[self.cascadeIndex-1][8]
        self.calculateEnergyFlows(equipe,self.cascadeIndex)
        print "demand after the add"
        print Status.int.QD_Tt_mod[self.cascadeIndex][8]
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
    def calculateEnergyFlows(self,equipe,cascadeIndex):
#------------------------------------------------------------------------------
#   calculates the energy flows in the equipment identified by "cascadeIndex"
#------------------------------------------------------------------------------

        print "ModuleBB (calculateEnergyFlows): starting (cascade no: %s)"%cascadeIndex
#..............................................................................
# get equipment data from equipment list in SQL

        BBModel = equipe.Model
        print equipe.Model
        BBType = equipe.EquipType
        PNom = equipe.HCGPnom
        COPh_nom = equipe.HCGTEfficiency
#XXX TOpMax or something similar should be defined in SQL        TMax = equipe.TOpMax
# for the moment set equal to TExhaustGas
        TMax = equipe.TExhaustGas
    
#XXX ENRICO: here other equipment parameters should be imported from SQL database
        self.screenEquipments()
        EquipmentNo = Status.int.cascade[cascadeIndex-1]["equipeNo"]

        print 'ModuleBB (calculateEnergyFlows): Model = ', BBModel, ' Type = ', BBType, 'PNom = ', PNom

#..............................................................................
# get demand data for CascadeIndex/EquipmentNo from Interfaces
# and create arrays for storing heat flow in equipment

        QD_Tt = copy.deepcopy(Status.int.QD_Tt_mod[cascadeIndex-1])
        QA_Tt = copy.deepcopy(Status.int.QA_Tt_mod[cascadeIndex-1])
        
        USHj_Tt = Status.int.createQ_Tt()
        USHj_T = Status.int.createQ_T()

        
        QHXj_Tt = Status.int.createQ_Tt()
        QHXj_T = Status.int.createQ_T()

#..............................................................................
# Start hourly loop

        USHj = 0
        QHXj = 0

        for it in range(Status.Nt):

#            print "time = ",it*Status.TimeStep

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
                QD_Tt[iT][it]= QD_Tt[iT][it]- USHj_Tt[iT][it]
            USHj += USHj_Tt[Status.NT+1][it]
#            print USHj_Tt[Status.NT+1][it]      #total heat supplied at present timestep
#........................................................................
# End of year reached. Store results in interfaces

        print "ModuleBB (calculateEnergyFlows): now storing final results"
        a=[]
       
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
            a=getEquipmentClass(entry["equipeType"])
            if a=="BB":
                eqID = entry["equipeID"]
                equipe = self.equipments.QGenerationHC_ID[eqID][0]
                efficiency = equipe.HCGTEfficiency
                temperature = equipe.TExhaustGas
                boilerList.append({"equipeID":eqID,"efficiency":efficiency,"temperature":temperature})
                print boilerList

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

        print "ModuleBB (sortBoiler): second step done - boilerList ordered by efficiency"
        print boilerList

#then reorganise boilerList by temperature levels:
#   first level:

        for i in range(len(boilerList)):
            for j in range(i,len(boilerList)):
                if boilerList[i]["temperature"] <= 80 and boilerList[j]["temperature"]>80:
                    bi = boilerList[i]
                    bj = boilerList[j]
                    boilerList[i] = bj
                    boilerList[j] = bi

#   second level:

        for i in range(len(boilerList)):
            for j in range(i,len(boilerList)):
                if 80 < boilerList[i]["temperature"] <= 140 and (boilerList[j]["temperature"]<=80 or boilerList[j]["temperature"]>140):
                    bi = boilerList[i]
                    bj = boilerList[j]
                    boilerList[i] = bj
                    boilerList[j] = bi

#   second level:

        for i in range(len(boilerList)):
            for j in range(i,len(boilerList)):
                if  boilerList[i]["temperature"] > 140 and  boilerList[j]["temperature"]<=140:
                    bi = boilerList[i]
                    bj = boilerList[j]
                    boilerList[i] = bj
                    boilerList[j] = bi

        print "ModuleBB (sortBoiler): third step done - boilerList ordered by temperature and efficiency"
        print boilerList


#then move consecutively to the bottom of the cascade (move the one last, which you finally want to have at the bottom

        for i in range(len(boilerList)):
            eqID = boilerList[i]["equipeID"]
            equipe = self.equipments.QGenerationHC_ID[eqID][0]
            cascadeIndex = equipe.CascadeIndex
            if cascadeIndex < Status.int.NEquipe:
                Status.mod.moduleHC.cascadeMoveToBottom(cascadeIndex)

        print "ModuleBB (sortBoiler): fourth step done - shift in cascade carried out"
        print Status.int.cascade

#find the position in the cascade of the first and last boiler of each T level
        a=0
        b=0
        for i in range(len(boilerList)):
            if  boilerList[i]["temperature"] > 80 :
                a+=1
            if  boilerList[i]["temperature"] > 140 :
                b+=1

        self.firstBB = len(Status.int.cascade)-len(boilerList)
        self.firstBB140 = len(Status.int.cascade)-a
        if self.maxTemp >140:
            self.firstBBmaxTemp = len(Status.int.cascade)-b
        else:
            self.firstBBmaxTemp =len(Status.int.cascade)-a
        lastBB = len(Status.int.cascade)-1
            
#OR JUST CORRECTING YOUR CODE (don't understand it so I can't say if it should work or not ...):
                
#        k=0
#        while k<len(Status.int.cascade):
#            if getEquipmentClass(Status.int.cascade[k]["equipeType"]) == "BB":
#                a=0
#                for h in range (k,len (Status.int.cascade)):
#                    equipe_k = self.equipments.QGenerationHC_ID[Status.int.cascade[k]["equipeID"]][0]
#                    equipe_h = self.equipments.QGenerationHC_ID[Status.int.cascade[h]["equipeID"]][0]
#                    if equipe_h.HCGTEfficiency < equipe_k.HCGTEfficiency:   #check if h and k has to be changed !!!
#                        a=h-k
#                for l in range(a):
#                    Status.mod.moduleHC.cascadeMoveDown(k+l)
#            if a>0:
#                k=k-1
#            k=k+1

#        for i in range (len(Status.int.cascade)):
#            if getEquipmentClass(Status.int.cascade[i].equipeType)=="BB" and self.equipments[Status.int.cascade[i].equipeID].Temp <=90:
#            equipe = self.equipments.QGenerationHC_ID[Status.int.cascade[i]["equipeID"]][0]
#            if getEquipmentClass(Status.int.cascade[i]["equipeType"])=="BB" and equipe.Temp <=90:
#            if getEquipmentClass(Status.int.cascade[i]["equipeType"])=="BB" and equipe.TExhaustGas <=90:    #use TExhaustGas until we have an update of the SQL
#                Status.mod.moduleHC.cascadeMoveToBottom(i)
#                aa=Status.int.cascade[len(Status.int.cascade)-1]["equipeID"]  #aa is the ID of the last boiler at 80°C

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
    def automDeleteBoiler (self,minEfficencyAccepted=80):  #0.80 is a default value for minimum of efficiency
#------------------------------------------------------------------------------
# delete unefficient boiler
#------------------------------------------------------------------------------
        print"entered 'automDeleteBoiler' function" 
        self.screenEquipments()
        automatic=True
        for i in range (len (self.BBList)):
            print "controlling equipe", self.BBList[i]['equipeID']
            eff= self.equipments.QGenerationHC_ID[self.BBList[i]['equipeID']][0]['HCGTEfficiency']
            print "efficiency of the boiler number '%s'is:'%s'"%(i,eff)
            print "min efficiency accepted:",minEfficencyAccepted
            if eff < minEfficencyAccepted:
#                 add the fuel criterion: if not biomass,biofuels?,gas methane ->delete ???
                print "Module BB (): id to be deleted = ",self.BBList[i]['equipeID']
                self.deleteEquipment(self.BBList[i]['equipeID'],automatic)# The row number should be passed. is this right? 
                
                


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
                    self.maxTemp=Status.TemperatureInterval*(i+1) #temperatureInterval is defined in status.py
        print "maxtemp=", self.maxTemp


#------------------------------------------------------------------------------
    def redundancy(self):
#------------------------------------------------------------------------------
#       when redundancy is required provides suitable boilers.
#       N.B. the possibility of retriveing deleted boilers is not implemented yet.
#       N.B. The possibility that a boiler with nominal power > than biggerBB is in the list has to be considered.
#------------------------------------------------------------------------------      
        print "dimensioning reduntant boilers"
        self.maxPow80=0
        self.maxPow140=0
        self.maxPowTmax=0
        for k in range(len(Status.int.cascade)):
            if getEquipmentClass(Status.int.cascade[k]["equipeType"]) == "BB":
#                print "the equipment ID is:",Status.int.cascade[k]["equipeID"]
#                print "the corresponding temp. is:",self.equipments.QGenerationHC_ID[Status.int.cascade[k]["equipeID"]][0]['TExhaustGas']
                if self.equipments.QGenerationHC_ID[Status.int.cascade[k]["equipeID"]][0]['TExhaustGas'] <=90 and \
                   Status.int.cascade[k]["equipePnom"] > self.maxPow80:     # TExhaustGas to be sostituted with tthe operating temperature
                    self.maxPow80 =Status.int.cascade[k]["equipePnom"]
                elif 90< self.equipments.QGenerationHC_ID[Status.int.cascade[k]["equipeID"]][0]['TExhaustGas'] <= 150 and \
                     Status.int.cascade[k]["equipePnom"] > self.maxPow140:
                    self.maxPow140 =Status.int.cascade[k]["equipePnom"]
                elif Status.int.cascade[k]["equipePnom"] > self.maxPowTmax:
                    self.maxPowTmax =Status.int.cascade[k]["equipePnom"]
        if self.maxPow80>0:
            modelID =self.selectBB(self.maxPow80,80)
            equipe = self.addEquipmentDummy()
            self.setEquipmentFromDB(equipe,modelID)
        if self.maxPow140>0 and self.maxTemp>140:
            modelID =self.selectBB(self.maxPow140,140)
            equipe = self.addEquipmentDummy()
            self.setEquipmentFromDB(equipe,modelID)
        modelID =self.selectBB(self.maxPowTmax,self.maxTemp)
        equipe = self.addEquipmentDummy()
        self.setEquipmentFromDB(equipe,modelID)
        


#------------------------------------------------------------------------------
    def findBiggerBB(self):
#------------------------------------------------------------------------------
# finds the maximum power of the boiler in the DB (for each temperature level)
#------------------------------------------------------------------------------
        sqlQuery="BoilerTemp >='%s' ORDER BY BBPnom DESC" %(self.maxTemp)
        search= Status.DB.dbboiler.sql_select(sqlQuery)
        self.biggermaxTemp=search[0].BBPnom
        sqlQuery="140<=BoilerTemp <170 ORDER BY BBPnom DESC"
        search= Status.DB.dbboiler.sql_select(sqlQuery)
        self.bigger140=search[0].BBPnom
        sqlQuery="80<=BoilerTemp <120 ORDER BY BBPnom DESC"
        search= Status.DB.dbboiler.sql_select(sqlQuery)
        self.bigger80=search[0].BBPnom

#------------------------------------------------------------------------------
    def selectBB(self,Pow,Top):
#------------------------------------------------------------------------------
#  the query should consider the fuel too but at the moment the fuel column doesn't exist in mySQL.
#  we could give the possibility to choose the boiler to the user (in the interactive mode) in a 'selected' list. In this version we take the first  
#  element of the list
#------------------------------------------------------------------------------
        print "entered selectBB module"
        sqlQuery="BoilerTemp >= '%s'AND BBPnom >= '%s' ORDER BY BBPnom ASC" %(Top,Pow)       
        selected = Status.DB.dbboiler.sql_select(sqlQuery)
        for i in range(len(selected)):
            for j in range(i,len(selected)):
                if selected[j].BoilerTemp < selected[i].BoilerTemp:
                    bi = selected[i]
                    bj = selected[j]
                    selected[i] = bj
                    selected[j] = bi

        
        modelID =selected[0].DBBoiler_ID
        print "selectBB: the requested power is:", Pow 
        print "selectBB: the selected boiler ID is:", modelID
#        print "selectBB: the list of boiler is:"
#        print selected
        return modelID
        


            
#------------------------------------------------------------------------------
    def designBB80(self):
#------------------------------------------------------------------------------
#    def designBB80(self,...):
# design a boiler sistem at 80°C
#------------------------------------------------------------------------------
        added=0
        if Status.int.QD_T_mod[self.firstBB][int(80/Status.TemperatureInterval)] >= 0.1*Status.int.QD_T_mod[self.firstBB][int(self.maxTemp/Status.TemperatureInterval)]: #we design boiler at this temperature level only if the demand is bigger than the 10% of the total demand
            print "point AA reached"
            if self.QDh80[0]*self.securityMargin >= self.minPow:
                print "point AB reached"
                if self.QDh80[0]*self.securityMargin>=2*self.minPow:
                    print "point AC reached"
                    if self.QDh80[0]*self.securityMargin < self.QDh80[self.minOpTime]*1.3 \
                       or (self.QDh80[0]*self.securityMargin - self.QDh80[self.minOpTime]) < self.minPow:
                        print "point A reached"
                        modelID = self.selectBB((self.QDh80[0]*self.securityMargin),80)  #select the right bb from the database.                        
#HS line not valid code                        selectBB((QDh_descending[0]*securityMargin),...)  #select the right bb from the database.
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
#HS: elif requires a condition !!!                    elif:
                    else:
                        if self.QDh80[self.minOpTime]>self.bigger80:
                            for i in range (int(self.QDh80[self.minOpTime]/self.bigger80)):
                                print "point B reached"
                                modelID =self.selectBB(self.bigger80,80)
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)
                            added += int(self.QDh80[self.minOpTime]/self.bigger80)*self.bigger80
                        else:
                            print "point C reached"
                            modelID =self.selectBB(self.QDh80[self.minOpTime],80) #aggiungere condizione sul rendimento
                            equipe = self.addEquipmentDummy()
                            self.setEquipmentFromDB(equipe,modelID)
                            added += self.DB.dbboiler.DBBoiler_ID[modelID][0].BBPnom
                        print "power of the last bb group added"
                        print added
                        if self.QDh80[0]*self.securityMargin - added >= 2*self.minPow:
                            if self.QDh80[0]*self.securityMargin - added >= self.bigger80:
                                for i in range (int((self.QDh80[0]*self.securityMargin - added)/self.bigger80)):
                                    print "point D reached"
                                    modelID =self.selectBB(self.bigger80,80)
                                    equipe = self.addEquipmentDummy()
                                    self.setEquipmentFromDB(equipe,modelID)
                                print "point E reached"
                                added += int((self.QDh80[0]*self.securityMargin - added)/self.bigger80)*self.bigger80
                                modelID =self.selectBB((self.QDh80[0]*self.securityMargin - added),80)
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)
                            else:
                                print "point F reached"
                                modelID=self.selectBB(((self.QDh80[0]*self.securityMargin - added)/2),80)  #sempre aggiungere anche il criterio di efficienza
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                        else:
#HS: elif requires a condition !!!                        elif:
                            print "point G reached"
                            self.selectBB((self.QDh80[0]*self.securityMargin - added),80)
                            equipe = self.addEquipmentDummy()
                            self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                else:
#HS: elif requires a condition !!!                elif:
                    print "point H reached"
                    self.selectBB(self.QDh80[0]*self.securityMargin,80)
                    equipe = self.addEquipmentDummy()
                    self.setEquipmentFromDB(equipe,self.modelID)   #assign model from DB to current equipment in equipment list

        print "point i reached"
        self.sortBoiler()                
                        

                    

#------------------------------------------------------------------------------
    def designBB140(self):
#HS input list has to be defined !!!!    def designBB140(self,...):
#------------------------------------------------------------------------------
# design a boiler sistem at 140°C
#------------------------------------------------------------------------------
        added=0
        if Status.int.QD_T_mod[self.firstBB140][int(140/Status.TemperatureInterval)] >= 0.1*Status.int.QD_T_mod[self.firstBB][int(self.maxTemp/Status.TemperatureInterval)]:
            print"point A1 reached"
            if self.QDh140[0]*self.securityMargin >= self.minPow:
                print "point A2 reached"
                if self.QDh140[0]*self.securityMargin>=2*self.minPow:
                    print "point A3 reached"
                    if self.QDh140[0]*self.securityMargin < self.QDh140[self.minOpTime]*1.3 or \
                    self.QDh140[0]*self.securityMargin -self.QDh140[self.minOpTime]<self.minPow:
                        print "point A4 reached"
                    
#HS TAKE CARE !!!! methods of the same class have to be called with the "self." before
#                   has probably to be corrected throughout the code ... !!!!
#                        selectBB((QDh_descending[0]*securityMargin)) # ,...)  #select the right bb from the database.
                        modelID=self.selectBB((self.QDh140[0]*self.securityMargin),140) # ,...)  #select the right bb from the database.
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list

                    else:
#HS: elif requires a condition !!!                    elif:
                        if self.QDh140[self.minOpTime]>self.bigger140:
                            for i in range (int(self.QDh140[self.minOpTime]/self.bigger140)):
                                print "point B1 reached"
                                modelID =self.selectBB(self.bigger140,140)
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)
                            added += int(self.QDh140[self.minOpTime]/self.bigger140)*self.bigger140
                        else:
                            print "point C1 reached"
                            modelID =self.selectBB(self.QDh140[self.minOpTime],140)  #  select the base load boiler from DB
                            equipe = self.addEquipmentDummy()
                            self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                            added += self.DB.dbboiler.DBBoiler_ID[modelID][0].BBPnom
                        print "power of the last bb group added"
                        print added
                      
                        if self.QDh140[0]*self.securityMargin - added>= 2*self.minPow:
                            if self.QDh80[0]*self.securityMargin - added >= self.bigger80:
                                for i in range (int((self.QDh140[0]*self.securityMargin - added)/self.bigger140)):
                                    print "point D1 reached"
                                    modelID =self.selectBB(self.bigger140,140)
                                    equipe = self.addEquipmentDummy()
                                    self.setEquipmentFromDB(equipe,modelID)
                                print "point E1 reached"
                                added += int((self.QDh140[0]*self.securityMargin - added)/self.bigger140)*self.bigger140
                                modelID =self.selectBB((self.QDh140[0]*self.securityMargin - added),140)
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)
                            else:
                                print "point F1 reached"
                                modelID=self.selectBB(((self.QDh140[0]*self.securityMargin - added)/2),140)  #sempre aggiungere anche il criterio di efficienza
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                                self.setEquipmentFromDB(equipe,modelID)
                            
                        else:
                            print "point G1 reached"
                            self.selectBB((self.QDh140[0]*self.securityMargin - added),140)
                            equipe = self.addEquipmentDummy()
                            self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list

                else:
                    print "point H1 reached"
                    self.selectBB(self.QDh140[0]*self.securityMargin,140)
                    equipe = self.addEquipmentDummy()
                    self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list

        print "point i1 reached"
        self.sortBoiler()
#------------------------------------------------------------------------------
    def designBBmaxTemp(self): #HS .........,maxTemp...):
#------------------------------------------------------------------------------
# design a boiler sistem at the maximum temperature of the heat demand
#------------------------------------------------------------------------------
        added=0
        if self.QDhmaxTemp[0]*self.securityMargin>=2*self.minPow:
            if self.QDhmaxTemp[0]*self.securityMargin < self.QDhmaxTemp[self.minOpTime]*1.3 \
               or (self.QDhmaxTemp[0]*self.securityMargin - self.QDhmaxTemp[self.minOpTime]) < self.minPow:
                modelID = self.selectBB((self.QDhmaxTemp[0]*self.securityMargin),self.maxTemp) #HS....,...)  #select the right bb from the database.
                equipe = self.addEquipmentDummy()
                self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list

            else:
                if self.QDhmaxTemp[self.minOpTime]>self.biggermaxTemp:
                    for i in range (int(self.QDhmaxTemp[self.minOpTime]/self.biggermaxTemp)):
                        modelID =self.selectmaxTemp(self.biggermaxTemp,self.maxTemp)
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)
                    added += int(self.QDhmaxTemp[self.minOpTime]/self.biggermaxTemp)*self.biggermaxTemp
                else:
                    modelID =self.selectBB(self.QDhmaxTemp[self.minOpTime],self.maxTemp)
                    equipe = self.addEquipmentDummy()
                    self.setEquipmentFromDB(equipe,modelID)
                    added += self.DB.dbboiler.DBBoiler_ID[modelID][0].BBPnom


                if self.QDhmaxTemp[0]*self.securityMargin - added >= 2*self.minPow:
                    if self.QDhmaxTemp[0]*self.securityMargin - added >= self.biggermaxTemp:
                        for i in range (int((self.QDhmaxTemp[0]*self.securityMargin - added)/self.biggermaxTemp)):
                            modelID =self.selectBB(self.biggermaxTemp,self.maxTemp)
                            equipe = self.addEquipmentDummy()
                            self.setEquipmentFromDB(equipe,modelID)
                        added += int((self.QDhmaxTemp[0]*self.securityMargin - added)/self.biggermaxTemp)*self.biggermaxTemp
                        modelID =self.selectBB((self.QDhmaxTemp[0]*self.securityMargin - added),self.maxTemp)
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)
                    else:
                        modelID=self.selectBB(((self.QDhmaxTemp[0]*self.securityMargin - added)/2),maxTemp)
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)

                   
                else:
                    modelID=self.selectBB((self.QDhmaxTemp[0]*self.securityMargin - added),self.maxTemp)
                    equipe = self.addEquipmentDummy()
                    self.setEquipmentFromDB(equipe,modelID)

        else:
            modelID=self.selectBB(self.QDhmaxTemp[0]*self.securityMargin,self.maxTemp)
            equipe = self.addEquipmentDummy()
            self.setEquipmentFromDB(equipe,modelID)


        self.sortBoiler()
    
#------------------------------------------------------------------------------
    def designAssistant(self):
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

        DATable = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(DATable) > 0:
            DA = DATable[0]
        else:
            print "ModuleBB (design assistant): WARNING - no DA configuration parameters available"
            return

        if DA.BBRedundancy == True:
            pass
        
#            if (MaintainExistingEquipment == False):
#                deleteAllBoilers()
        self.securityMargin=1.2      #  N.B. securityMargin should be choosen by the user!!! At the moment is setted to 1.2############
        self.minPow =100             #  N.B. minPow should be an imput from the boiler window!!! At the moment is setted to 100kW
        self.minOpTime=100          #  N.B. minOpTime should be an imput from the boiler window!!! At the moment is setted to 100 hours:for testing Nt is 168 corresponding to 1 week.
        self.screenEquipments()
 
        self.automDeleteBoiler()   # delete unefficient boiler

        self.findmaxTemp(Status.int.QD_T)
        self.findBiggerBB()       
        self.sortBoiler()     # sort boilers by temperature (ascending) and by efficiency (descending)
                                
        exBP=0       #   power of the boiler in the cascade operating at 80°C
        for row in Status.int.cascade:
            equipTry= Status.DB.qgenerationhc.QGenerationHC_ID[row["equipeID"]][0]
            print equipTry["HCGPnom"]
            if getEquipmentClass(row["equipeType"]) == "BB" and equipTry["TExhaustGas"]<=80:
                exBP += row['equipePnom']
        print "power of the boilers at 80°C present in the cascade at the moment", exBP
        zz=int(80/Status.TemperatureInterval)
#        print zz
        print "the first boiler in cascade is"
        print self.firstBB
#        print Status.int.QD_Tt_mod [0][8]        
#        print Status.int.QD_Tt_mod [0][zz]
        yy= maxInList(Status.int.QD_Tt_mod [self.firstBB][zz])
        print "print the maximum pawer of the demand at 80°C"
        print yy
        b=max((yy  - exBP),0)
        b1= max(((yy * self.securityMargin) - exBP),0) #   minimum power of the new boilers at 80°C
        c=[]
        for it in range (Status.Nt):
            c.append ( min (b, Status.int.QD_Tt_mod[self.firstBB][zz][it]))

        self.QDh80=c  # demand to be supplied by new boilers at 80°C

        self.QDh80.sort(reverse=True)
        print "the demand at 80°C to be supplied by new boilers"
        print self.QDh80
        print "lenght of the demand array (QDh80)"
        print len(self.QDh80)
        if self.QDh80[0]>0:
            self.designBB80()
        print" reached point L"
#        for k in range (self.firstBB , self.firstBB140):
#            equipe = Status.DB.qgenerationhc.CascadeIndex[k][0]   #self.equipments.QGenerationHC_ID[{"CascadeIndex"}][0]
#            self.calculateEnergyFlows(equipe,k)

            
        if self.maxTemp>160:   # N.B. The difference between temperature levels is now setted in 20°C but in the future could be a parameter.      
                        
            exBP=0       #   power of the boiler in the cascade operating at 140°C
            for row in Status.int.cascade:
                equipTry= Status.DB.qgenerationhc.QGenerationHC_ID[row["equipeID"]][0]
                if getEquipmentClass(row["equipeType"]) == "BB" and 90 <= equipTry["TExhaustGas"]<=140:
                    exBP += row['equipePnom']

            zz=int(140/Status.TemperatureInterval)
            yy= maxInList(Status.int.QD_Tt_mod [self.firstBB140][zz])
            b=max((yy  - exBP),0) #   minimum power of the new boilers at 140°C
            c=[]
            for it in range (Status.Nt):
                c.append ( min (b, Status.int.QD_Tt_mod[self.firstBB140][zz][it]))

            self.QDh140=c  # demand to be supplied by new boilers at 140°C
#            print "The total demand at 80°C is:", Status.int.QD_Tt_mod[self.firstBB][8]
#            print "The total demand at 140°C is:", Status.int.QD_Tt_mod[self.firstBB][14]
            print " the residual demand at 140°C" 
            print self.QDh140
            self.QDh140.sort(reverse=True)

            print "The lenght of the demand (temperature levels)is", len (Status.int.QD_T_mod[self.firstBB140])
            print "the maxTemp is", self.maxTemp
            if self.QDh140[0]>0:
                self.designBB140()
        
#            for k in range (self.firstBB140 , self.firstBBmaxTemp):
#                equipe = Status.DB.qgenerationhc.CascadeIndex[k][0]   #self.equipments.QGenerationHC_ID[{"CascadeIndex"}][0]
#                self.calculateEnergyFlows(equipe,k)


        exBP=0       #   power of the boiler in the cascade operating at maxTemp
        for row in Status.int.cascade:
            equipTry= Status.DB.qgenerationhc.QGenerationHC_ID[row["equipeID"]][0]

            if getEquipmentClass(row["equipeType"]) == "BB":
                exBP += row['equipePnom']

        cI= len(Status.int.QD_Tt_mod)+1
        zz=int(self.maxTemp/Status.TemperatureInterval)
        print "The maximum temperature is:", self.maxTemp
        print "the annual energy at 3 temperature level 'around' the max temp is:", Status.int.QD_T[int(self.maxTemp/Status.TemperatureInterval)-1],\
        Status.int.QD_T[int(self.maxTemp/Status.TemperatureInterval)]#,Status.int.QD_T[int(self.maxTemp/Status.TemperatureInterval)+1]
        print "the cascade index of the first boiler at max temp is:",self.firstBBmaxTemp
        yy= maxInList(Status.int.QD_Tt_mod [self.firstBBmaxTemp][zz])
        b=max((yy  - exBP),0) #   minimum power of the new boilers at maxTemp°C
        c=[]
        for it in range (Status.Nt):
            c.append ( min (b, Status.int.QD_Tt_mod[self.firstBBmaxTemp][zz][it]))

        self.QDhmaxTemp=c  # demand to be supplied by new boilers at maxTemp°C

        self.QDhmaxTemp.sort(reverse=True)
        print "the demand at max temp. is:", self.QDhmaxTemp
        if self.QDhmaxTemp[0]>0:
            self.designBBmaxTemp()

#        for k in range (self.firstBBmaxTemp , self.lastBB+1):
#            equipe = Status.DB.qgenerationhc.CascadeIndex[k][0]
#            self.calculateEnergyFlows(equipe,k)

        print "set of boiler designed"
        off= False
        print "can we accept to stop the production?",off
        if off== False:
            self.redundancy()
        
        self.updatePanel()    
        print "ModuleBB (design assistant) reached the end"

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
