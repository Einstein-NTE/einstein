# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleST (Boilers and Burners)
#			
#------------------------------------------------------------------------------
#			
#	Module for calculation of boilers
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	25/06/2008
#                           (based on ModuleST from Enrico Facci)
#	Last revised by:    
#
#       Changes to previous version:
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
from sunday import *

sunOnH = Intensity()
sunOnT = Intensity()
sunAnglesOnSurface = Angles()
dirSunOnT = [0.0,0.0,0.0]

#------------------------------------------------------------------------------		
def getDailyRadiation(I,day):
#------------------------------------------------------------------------------		
#   Calculates some (more or less) "reasonable" distribution of yearly solar
#   radiation
#   very very basic and only reasonable for European latitudes !!!
#------------------------------------------------------------------------------		

#       ***GETTING_STARTED***:
#   The SUNDAY functions are written radically in SI-units, this is J, W, s; no
#   hours, no kilos, no Megas ... !!!! => unit conversion from EINSTEIN-units
#   to Sunday (SI-) units is necessary

    kWh_to_J = 3.6e+6
    Hmean = I/365*kWh_to_J
    H = Hmean * (1.0 - 0.5*cos(2.0*math.pi*(day+10)/365))
    print "daily radiation = ",H
    return H
                 
#------------------------------------------------------------------------------		
def collectorEfficiency(GT,dT):
#------------------------------------------------------------------------------		
#   Calculates the collector efficiency at a given working point
#   GT: Solar radiation on tilted surface (SI - units: W/m2)
#   c1/c2 are in W/m2K, W/m2K2 !!!
#------------------------------------------------------------------------------		

#       ***GETTING_STARTED***:
#   Later on the incidence angle modifier and decomposition into direct
#   and diffuse radiation could be added
#   The necessary input values GbT, GdT and cos(theta) are already available
#   from the function SUN_HOURLY 

    if GT <= 0:
        return 0.0
    else:
        c0 = 0.80 # Collector parameters from the DB: As default STARTING value choose always:LowTempCollType=FPEinstein
        c1 = 3.50
        c2 = 0.010
        return c0 + (c1 + c2*dT)*dT/(GT)
                 
#============================================================================== 
#============================================================================== 
#============================================================================== 
class ModuleST(object):
#============================================================================== 
#============================================================================== 
#============================================================================== 

    STList = []
    
#------------------------------------------------------------------------------
    def __init__(self, keys = ["ST Table"]):
#------------------------------------------------------------------------------
#   init is called only once at the very beginning of the EINSTEIN session
#   at this moment no project data are available yet ...
#------------------------------------------------------------------------------
        self.keys = keys # the key to the data is sent by the panel


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#   initPanel is called when the user opens the DA panel
#   all the calculations should be carried out here that are necessary only
#   the first time. the rest should be done in "updatePanel"
#------------------------------------------------------------------------------

#HS2008-06-25: ACTIONS CANCELLED FOR FIRST TESTING PANEL ONLY ...
#        Status.int.initCascadeArrays(self.NEquipe)
#        Status.mod.moduleEnergy.runSimulation()
#        Status.int.printCascade()

#............................................................................................
#   call updatePanel in order to send all the data to the GUI and do the remaining
#   calculations

        self.updatePanel()
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#   Here all the information should be prepared so that it can be plotted on the panel
#   This function will be called from the GUI every time some information to
#   be displayed might have changed
#------------------------------------------------------------------------------

#............................................................................................
# 1. List of equipments

        (STList,STTableDataList) = self.screenEquipments()

        collectors = [["Buderus XY 007","flat plate collector",0.8,3.0,0.01,0.93]]
        data = array(collectors)

        Status.int.setGraphicsData('ST Table',data)
#............................................................................................
# 2. Preparing data

        Status.int.setGraphicsData('ST Plot',[[1,2,3,4],[2,4,6,8],[3,5,9,7],[4,3,2,3],[5,5,10,5]])

#............................................................................................
# 3. Configuration design assistant

        config = self.getUserDefinedPars()
        Status.int.setGraphicsData('ST Config',config)

    
#............................................................................................
# 4. additional information

        info = [0,0,0,0,0,0,0]
        Status.int.setGraphicsData('ST Info',info)

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
            print 'getUserDefinedParamST: Status.PId =', Status.PId, 'Status.ANo =', Status.ANo, 'not defined'
            print 'Error: confusion in PId and ANo'
            maintainExisting = True
            config = []            

        else:
            u = urows[0]
            config = [u.STMaintain,
                      u.STSafety,
                      u.STRedundancy,
                      u.STFuelType,
                      u.STHOp,
                      u.STPmin,
                      u.STEff]
            print "ModuleST (getUserDefinedPars): config = ",config

####  FOR TESTING OF GUI. SHOULD BE ELIMINATED AND READ FROM UHEATPUMP !!!
            
        config = [0.5,0,500,1200,0.9,40]
        return config

#------------------------------------------------------------------------------
    def setUserDefinedPars(self):
#------------------------------------------------------------------------------

        config = Status.int.GData['ST Config']

        urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
        
        if len(urows)==0:
            print "ModuleST(setUserDefinedParamHP): corrupt data base - no entry for uheatpump under current ANo"
            dummy = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo} 
            Status.DB.uheatpump.insert(dummy)
            urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
            
        u = urows[0]

#        row.MaintainExisting = UDList[0] # to add in UHeatPump
        u.STMaintain = config[0]
        u.STSafety = config[1]
        u.STRedundancy = config[2]
        u.STFuelType = config[3]
        u.STHOp = config[4]
        u.STPmin = config[5]
        u.STEff = config[6]

        Status.SQL.commit()

#------------------------------------------------------------------------------
    def screenEquipments(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#------------------------------------------------------------------------------


        Status.int.getEquipmentCascade()
        self.STList = []
        for row in Status.int.cascade:
            if getEquipmentClass(row["equipeType"]) == "ST":
                self.STList.append(row)

        STTableDataList = []
        for row in Status.int.EquipTableDataList:
            if getEquipmentClass(row[3]) == "ST":
                STTableDataList.append(row)

        #screen list and substitute None with "not available"
        for i in range(len(STTableDataList)):
            for j in range(len(STTableDataList[i])):
                if STTableDataList[i][j] == None:
                    STTableDataList[i][j] = 'not available'        

        if(len(self.STList)>0):
            self.cascadeIndex = len(self.STList) #by default sets selection to last ST in cascade
        else:
            self.cascadeIndex = 0
        return (self.STList,STTableDataList)
        

        
#------------------------------------------------------------------------------
    def getEqId(self,rowNo):
#------------------------------------------------------------------------------
#   gets the EqId from the rowNo in the STList
#------------------------------------------------------------------------------

        STId = self.STList[rowNo]["equipeID"]
        return STId

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
                STid = self.dummyEqId
            else:
            #--> delete ST from the equipment list under current alternative #from C&QGenerationHC under ANo
                STid = self.getEqId(rowNo)
                print "Module ST (delete): id to be deleted = ",STid
        else:
            STid= rowNo
            print "Module ST (delete automaticly): id to be deleted = ",STid
        
        eq = self.equipments.QGenerationHC_ID[STid][0] #select the corresponding rows to HPid in both tables
###HS: CGENERATIONHC ELIMINATED.        eqC = self.equipmentsC.QGenerationHC_id[STid][0]

        eq.delete() #deletes the rows in both tables, to be activated later, SD
###HS: CGENERATIONHC ELIMINATED.        eqC.delete()
        self.sql.commit()

        #actuallise the cascade list: define deleteFromCascade
        self.deleteFromCascade(Status.int.cascade, STid)

        self.NEquipe -= 1

#------------------------------------------------------------------------------
    def deleteFromCascade(self, cascade, STid):
#------------------------------------------------------------------------------
        """
        deletes from the actual list casade and re-assigns the CascadeIndex values in QGenerationHC table
        """
#-----------------------------------------------------------------------------

#        print '\n deleteFromCascade():', 'cascade =', cascade

        idx = -1
        new_cascade = cascade
        for i in range(len(new_cascade)):
            if new_cascade[i]['equipeID'] == STid:
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

        self.cascadeIndex = self.NEquipe + 1
        EqNo = self.NEquipe + 1

        self.neweqs += 1 #No of last equip added
        NewEquipmentName = "Solar thermal system"

        EqNo = self.NEquipe + 1

        equipe = {"Questionnaire_id":Status.PId,\
                  "AlternativeProposalNo":Status.ANo,\
                  "EqNo":EqNo,"Equipment":NewEquipmentName,\
                  "EquipType":"Solar thermal system (specify subtype)","CascadeIndex":self.cascadeIndex}
        
        QGid = self.DB.qgenerationhc.insert(equipe)

        self.dummyEqId = QGid #temporary storage of the equipment ID for undo if necessary
        
        Status.SQL.commit()

        Status.int.getEquipmentCascade()
        Status.int.addCascadeArrays()

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        self.equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
        self.NEquipe = len(self.equipments)

        self.equipe = self.equipments.QGenerationHC_ID[QGid][0]

        return(self.equipe)


#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def setEquipmentFromDB(self,equipe,modelID):
#------------------------------------------------------------------------------
#   takes an equipment from the data base and stores it under a given Id in
#   the equipment data base
#------------------------------------------------------------------------------

        model = self.DB.dSToiler.DSToiler_ID[modelID][0]
        print "setting equipment from DB"
        if model.STPnom != None: equipe.update({"HCGPnom":model.STPnom})
        if model.STEfficiency != None: equipe.update({"HCGTEfficiency":model.STEfficiency})
#        if model.BoilerTemp != None: equipe.update({"TMax":model.BoilerTemp})
        if model.BoilerTemp != None: equipe.update({"TExhaustGas":model.BoilerTemp}) # This line has to be changed when an appropriate field will be insert in qgenerationhc
        if model.BoilerManufacturer != None: equipe.update({"Manufact":model.BoilerManufacturer})
        if model.BoilerModel != None: equipe.update({"Model":model.BoilerModel})
        equipe.update({"EquipType":getEquipmentType("ST",model.BoilerType)})
        equipe.update({"NumEquipUnits":1})
        if model.BoilerType != None: equipe.update({"EquipTypeFromDB":model.BoilerType})
        if model.DSToiler_ID != None: equipe.update({"EquipIDFromDB":model.DSToiler_ID})
        Status.SQL.commit()
        print "cascade index is:",
        print "demand before the add",self.cascadeIndex-1
        print Status.int.QD_Tt_mod[self.cascadeIndex-1][8]
        self.calculateEnergyFlows(equipe,self.cascadeIndex)
        print "demand after the add"
        print Status.int.QD_Tt_mod[self.cascadeIndex][8]
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,cascadeIndex):
#------------------------------------------------------------------------------
#   calculates the energy flows in the equipment identified by "cascadeIndex"
#------------------------------------------------------------------------------

        print "ModuleST (calculateEnergyFlows): starting (cascade no: %s)"%cascadeIndex
#..............................................................................
# get equipment data from equipment list in SQL

        STModel = equipe.Model
        print equipe.Model
        STType = equipe.EquipType
        PNom = equipe.HCGPnom
        COPh_nom = equipe.HCGTEfficiency
#XXX TOpMax or something similar should be defined in SQL        TMax = equipe.TOpMax
# for the moment set equal to TExhaustGas
        TMax = equipe.TExhaustGas
    
#XXX ENRICO: here other equipment parameters should be imported from SQL database
        self.screenEquipments()
        EquipmentNo = Status.int.cascade[cascadeIndex-1]["equipeNo"]

        print 'ModuleST (calculateEnergyFlows): Model = ', STModel, ' Type = ', STType, 'PNom = ', PNom

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

#       ***GETTING_STARTED***:
#   This are the required input data for the calculation of the radiation
#   on tilted surface. are used as input values in the function prep_sun


###Claudia: I changed another time to lower-case letters, as usually we use the convention of lower case
### letters for local python variables. first letter uppercase is usually used for classes.

        latitude = 41.4
        inclination = 30
        azimuth = 15.0
        I = 1750.0    #yearly radiation in kWh/m2a

#       ***GETTING_STARTED***:
#   The area should be imported from the QGenerationHC equipment parameters
#   A solar system should be entered like any other heat supply equipment
#   into the QGenerationHC - Table. We should think about how to match the
#   parameters there with characteristic solar parameters
#   e.g. PNom for solar systems = the nominal solar system power
#   -> SurfaceAreaSol = PNom / 0.7

        SurfAreaSol = 100.0
        
        systemEfficiency = 0.90         #accounting for all the thermal losses in the solar system
                                    #including pipe and tank losses
    
#       ***GETTING_STARTED***:
#   These are the parameters for storage modelling:

        TStorage = 20.0                 #initial temperature of the storage at 1st of January 0:00
        TStorageMax = 250.0             #maximum allowed temperature in the storage
        storageVolume = 0.05*SurfAreaSol       #in m3. for the moment fixed to 50 l/m2. can be an equipment parameter
        CStorage = 1.16*storageVolume   #heat capacity of the storage in kW/K
        QStorage = CStorage*TStorage    #total heat stored in the tank (reference temperature = 0ºC)
        QStorageMax = CStorage*TStorageMax #maximum amount of heat that can be stored in the tank (ref. = 0ºC)
                 

        QavColl = 0    #these two values only for calculating the weighted mean of the average collector
        QTavColl = 0    #temperature during the year

        oldDay = 0

#.............................................................................
#.............................................................................
#.............................................................................
#.............................................................................
#.............................................................................
#.............................................................................
# HERE THE CYCLE OF CALCULATE ENERGY FLOWS STARTS
#.............................................................................
#.............................................................................
#.............................................................................
#.............................................................................
#.............................................................................

        USHj = 0
        QHXj = 0

        TIMESTEP = Status.TimeStep
        NT = Status.NT
        
        for it in range(Status.Nt):


        
            time_in_h = it * TIMESTEP
            time_in_s = time_in_h * HOUR
            nday = int(ceil(time_in_h/24.0))

            print "DAY: %s Hour: %s Sec: %s"%(nday,time_in_h,time_in_s)

#.............................................................................
# recalculate solar data for a new day

#       ***GETTING_STARTED***:
#   The function PREP_SUN prepares the radiation calculations for a given day
#   in the year

            if nday > oldDay:
                oldDay = nday
                print "ModuleST (calculateEnergyFlows): new day %s, I = %s"%(nday,I)
                sunOnH.t = getDailyRadiation(I,nday)
                print "ModuleST (calculateEnergyFlows): sunOnH = ",sunOnH
                prep_sun(latitude,inclination,azimuth,nday,sunAnglesOnSurface,sunOnH)

#.............................................................................
# now get instantaneous radiation (in W/m2)

            GH = sun_hourly(sunAnglesOnSurface,sunOnH,time_in_s,sunOnT,dirSunOnT)
            
            GbT = GH.b / 1000.    #conversion to kW/m2
            GdT = GH.d / 1000.
            GT = GH.t / 1000.

#XXXX THERE's SOME PROBLEM IN SUNDAY WITH THE CALCULATION OF GT
# FOR THE MOMENT RADIATION ON HORIZONTAL IS USED
#            GbT = sunOnT.b / 1000.    #conversion to kW/m2
#            GdT = sunOnT.d / 1000.
#            GT = sunOnT.t / 1000.

#.............................................................................
# calculate maximum solar system output, heat demand and storage capacity

#       ***GETTING_STARTED***:
#   The working temperature of the solar system is the temperature
#   of the storage tank at the beginning of the time-step plus a Delta_T
#   accounting for the heat exchanger in the primary loop

            deltaT_primary = 7.0
            TStorage = QStorage/CStorage
            TavCollector = TStorage + deltaT_primary    #=working temperature of the collector in the present time step
            TEnv = 20.0
            DeltaT = TavCollector - TEnv
                     
            dotQuSolarMax = collectorEfficiency(GH.t,DeltaT)*systemEfficiency*SurfAreaSol*GT #if shaded then add shading factor.ADD an IF!
                                #maximum instantaneous power the solar system may deliver

#       ***GETTING_STARTED***:
#   general Note: I used the "dot" to distinguish between power and energy.
#   we could adapt the calculations using the energy-fraction in time interval: dQ = dotQ*TIMESTEP
#   as is used in the EINSTEIN - arrays ...
#   dotQDemand should be set to the heat demand below TStorage (dotQDemand * TIMESTEP = QD_Tt[TStorage])

            dotQDemand = QD_Tt[NT+1][it]
            #XXXXHAS TO BE SUBSTITUTED BY DEMAND ONLY UP TO TMAX !!!XXX

#       ***GETTING_STARTED***:
#   the minimum temperature of demand indicates to what temperature the storage can be cooled down.
#   if we have heat demand only above e.g. 60ºC, we cannot cool down the storage lower than this,
#   as heat can not be transferred from cold to hot (at least not yet, maybe EINSTEIN succeeds to do it)
        
            TMinDemand = 50.0

            QStorageCapacity = QStorageMax - QStorage   #maximum amount of heat that still can be fed into the storage
            dotQuSolar = min(dotQDemand+QStorageCapacity/TIMESTEP,dotQuSolarMax)
                                                        #solar production constrained by demand + remaining storage capacity

            QStorageMin = CStorage*TMinDemand           #minimum heat that has to remain within the storage, as it can't be cooled down further
            dotQuSupply = min(dotQDemand,dotQuSolar + max((QStorage - QStorageMin)/TIMESTEP,0))
                                                        #supply constrained by solar production + available heat stored at T > TMinDemand

            USHj = dotQuSupply*TIMESTEP

            print "ModuleST (energyFlows): it=%s QsolMax=%s QD =%s USH=%s"%(it,dotQuSolarMax,dotQDemand,dotQuSupply)
#       ***GETTING_STARTED***:
#   note: the remaining problem is to decide at WHAT temperature the solar system does supply heat (from USHj_t to USHj_Tt)
#   -> let's use the simplest possible solution (although it's not the most efficient one ...):
#   fill up the demand from below (-> see heat pump example, I think there the same strategy
#   is applied. you can copy ...

            for iT in range(NT+2):
                USHj_Tt[iT][it] = min(USHj,QD_Tt[iT][it])
                QD_Tt[iT][it]= QD_Tt[iT][it]- USHj_Tt[iT][it]

            USHj += USHj_Tt[Status.NT+1][it]

# now update heat stored in tank
            QStorage += (dotQuSolar - dotQuSupply)*TIMESTEP

            print "----------------------------------------------"
            print "GT %10.4f dotQuSolar %10.4f"%(GT,dotQuSolar)

            QavColl += dotQuSolar
            QTavColl += dotQuSolar*TavCollector

#.............................................................................
#.............................................................................
#.............................................................................
#.............................................................................
#.............................................................................
#.............................................................................
#.............................................................................
#.............................................................................
#.............................................................................
# end of the year reached. now some final calculations

        TavCollMean = QTavColl/max(QavColl,0.000000001)

#........................................................................
# End of year reached. Store results in interfaces

        print "ModuleST (calculateEnergyFlows): now storing final results"
       
# remaining heat demand and availability for next equipment in cascade
        Interfaces.QD_Tt_mod[cascadeIndex] = QD_Tt
        Interfaces.QD_T_mod[cascadeIndex] = Status.int.calcQ_T(QD_Tt)
        Interfaces.QA_Tt_mod[cascadeIndex] = QA_Tt
        Interfaces.QA_T_mod[cascadeIndex] = Status.int.calcQ_T(QA_Tt)

# heat delivered by present equipment

        Interfaces.USHj_Tt[cascadeIndex-1] = USHj_Tt
        Interfaces.USHj_T[cascadeIndex-1] = Status.int.calcQ_T(USHj_Tt)
        Interfaces.USHj_t[cascadeIndex-1] = copy.deepcopy(USHj_Tt[Status.NT+1])

# waste heat absorbed by present equipment

        Interfaces.QHXj_Tt[cascadeIndex-1] = QHXj_Tt
        Interfaces.QHXj_T[cascadeIndex-1] = Status.int.calcQ_T(QHXj_Tt)

#        equipeC.USHj = USHj
#        equipeC.QHXj = QHXj    #XXX to be defined in data base

        print "Total energy supplied by equipment ",USHj, " MWh"
        print "Total waste heat input  ",QHXj, " MWh"

        return USHj    


#==============================================================================

#==============================================================================


if __name__ == "__main__":
    print "Testing ModuleST"
    import einstein.GUI.pSQL as pSQL, MySQLdb
    from einstein.modules.interfaces import *
    from einstein.modules.energy.moduleEnergy import *    

    stat = Status("testModuleST")

    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    
    Status.PId = 2
    Status.ANo = 0

    interf = Interfaces()

    Status.int = Interfaces()
    
    keys = ["ST Table","ST Plot","ST UserDef"]
    mod = ModuleST(keys)
    equipe = mod.addEquipmentDummy()
    mod.calculateEnergyFlows(equipe,mod.cascadeIndex)
                    

#    mod.designAssistant1()
#    mod.designAssistant2(12)
