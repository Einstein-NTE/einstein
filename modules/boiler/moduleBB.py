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
#   EINSTEIN Version No.: 1.0
#   Created by: 	Claudia Vannoni, Enrico Facci, Hans Schweiger
#                       11/03/2008 - 16/10/2008
#
#   Update No. 004
#
#   Since Version 1.0 revised by:
#                       Enrico Facci        26/10/2008
#                       Enrico Facci        04/11/2008
#                       Enrico Facci        10/06/2009
#                       Hans Schweiger      11/06/2009
#
#   04/11/08: EF    small change in SelectBB and some bugs fixed
#   10/06/09: EF    changes in BB auto-design - calculations of redundancy
#   11/06/09: HS    calculation of TCondOffGas added in cEF
#
#------------------------------------------------------------------------------		
#   (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008,2009
#   www.energyxperts.net / info@energyxperts.net
#
#   This program is free software: you can redistribute it or modify it under
#   the terms of the GNU general public license v3 as published by the Free
#   Software Foundation (www.gnu.org).
#
#============================================================================== 

from sys import *
from math import *
from numpy import *
import copy

from einstein.modules.fluids import *
from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP
from einstein.modules.constants import *
from einstein.modules.messageLogger import *

#============================================================================== 
#============================================================================== 
class ModuleBB(object):
#============================================================================== 
#============================================================================== 

    BBList = []
    
    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel

        self.DB = Status.DB
        self.sql = Status.SQL

        self.neweqs = 0 #new equips added
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

        if Status.int.cascadeUpdateLevel < 0:
            Status.int.initCascadeArrays(0)
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------

#............................................................................................
# get list of equipments and boilers in the system
# and update the energetic calculation up to the level needed for representation

        (BBList,BBTableDataList) = self.screenEquipments()

        if Status.int.cascadeUpdateLevel < self.cascadeIndex:
            Status.mod.moduleEnergy.runSimulation(self.cascadeIndex)
#        print"ModuleBB; updatePanel: there are '%s' equipments and the lenght of the QD_Tt_mod is'%s" % (len(self.equipments),len(Status.int.QD_Tt_mod))
#............................................................................................
# 1. List of equipments

        matrix = []
        for row in BBTableDataList:
            matrix.append(row)

        data = array(matrix)

        Status.int.setGraphicsData('BB Table',data)
#............................................................................................
# 2. Preparing data
        self.findmaxTemp(Status.int.QD_T)
#        print "ModuleBB; updatePanel: maximum temperature",self.maxTemp
        PowerSum80=0
        PowerSum140=0
        PowerSumTmax=0

        if self.maxTemp > 80:
            if self.maxTemp>160: # the minimum temperature difference is now setted at 20°C but could even be a parameter
                for i in BBList:
                    bbs = Status.DB.qgenerationhc.QGenerationHC_ID[i["equipeID"]]
                    if len(bbs) > 0:
                        bb = bbs[0]
                        if bb.TMaxSupply > 80 and bb.TMaxSupply <= 140:
                            PowerSum140 += i["equipePnom"]
                        if bb.TMaxSupply > 140:
                            PowerSumTmax += i["equipePnom"]
            else :
                for i in BBList:
                    bbs = Status.DB.qgenerationhc.QGenerationHC_ID[i["equipeID"]]
#                    bbs = self.equipments.QGenerationHC_ID[i["equipeID"]]  #HS2008-07-03: changed. gave some strange SQL error
                    if len(bbs) > 0:
                        bb = bbs[0]
                        if bb.TMaxSupply > 80:
                            PowerSumTmax += i["equipePnom"]
                            
            for i in BBList:
                bbs = Status.DB.qgenerationhc.QGenerationHC_ID[i["equipeID"]]
                if len(bbs) > 0:
                    bb = bbs[0]
                    if bb.TMaxSupply <=80:
                        PowerSum80 += i["equipePnom"]
        else:
            for i in BBList:
               PowerSumTmax += i["equipePnom"] 

        if len(BBList)==0:
            index=max(len(self.equipments)+1,1)     #HS2008-07-06. bug-fix. assures that index >= 0
                                                  #even if there's NO equipment at all 
        else:
            bbs = Status.DB.qgenerationhc.QGenerationHC_ID[BBList[0]["equipeID"]]
            if len(bbs) > 0:
                bb = bbs[0]
                index = bb.CascadeIndex

        QD80C = copy.deepcopy(Status.int.QD_Tt_mod[index-1][int(80/Status.TemperatureInterval+0.5)])
        QD80C.sort(reverse=True)

#        if self.maxTemp>160: # the minimum temperature difference is now setted at 20°C but could even be a parameter
#            QD140C=Status.int.QD_Tt_mod[index-1][int(140/Status.TemperatureInterval)]
#            QD140C.sort(reverse=True)
#        else:
#            QD140C=[]
#            for i in range(len(QD80C)):
#                QD140C.append(0)
        QD140C=copy.deepcopy(Status.int.QD_Tt_mod[index-1][int(140/Status.TemperatureInterval)])
        QD140C.sort(reverse=True)
        
        iT_maxTemp = int(self.maxTemp/Status.TemperatureInterval)
        QDmaxTemp=copy.deepcopy(Status.int.QD_Tt_mod[index-1][iT_maxTemp])
        QDmaxTemp.sort(reverse=True)
        QResidualMaxTemp=copy.deepcopy(Status.int.QD_Tt_mod[self.cascadeIndex][iT_maxTemp])
#        QResidualMaxTemp=Status.int.QD_Tt_mod[self.cascadeIndex][iT_maxTemp]- Status.int.QD_Tt_mod[self.cascadeIndex][int(140/Status.TemperatureInterval+0.5)]
        QResidualMaxTemp.sort(reverse=True)

#............................................................................................
# 2. XY Plot
        TimeIntervals=[]
        for it in range(Status.Nt+1):
            TimeIntervals.append(Status.TimeStep*(it+1)*Status.EXTRAPOLATE_TO_YEAR)

        try:

            if self.maxTemp>160:
                
                Status.int.setGraphicsData('BB Plot',[TimeIntervals,
                                                            QD80C,
                                                            QD140C,
                                                            QDmaxTemp])
            elif self.maxTemp>80:
                Status.int.setGraphicsData('BB Plot',[TimeIntervals,
                                                            QD80C,
                                                            QD140C,
                                                            QDmaxTemp])
            else:
                Status.int.setGraphicsData('BB Plot',[TimeIntervals,
                                                            QD80C])
        except:
            logDebug("ModuleBB (updatePanel): problems sending data for BB Plot")

#............................................................................................
# 3. Configuration design assistant

        config = self.getUserDefinedPars()
        Status.int.setGraphicsData('BB Config',config)
        
#............................................................................................
# 4. additional information (Info field right side of panel)
#        print"moduleBB;updatePanel: info to be displayed:",self.maxTemp,QResidualMaxTemp[0],QD80C[0],QD140C[0]-QD80C[0],QDmaxTemp[0]
        info = []
        info.append(self.maxTemp)  #first value to be displayed
        info.append(QResidualMaxTemp[0])
#        info.append(max(0,QResidualMaxTemp[0]))
        info.append(max(0,QD80C[0]))
        info.append(max(0,(QD140C[0]-QD80C[0])))
        info.append(max(0,QDmaxTemp[0]))

        
#        info.append(max(0,(QD80C[0]-PowerSum80)))  #power for T-level
#        
#        if self.maxTemp>160:
#            info.append(max(0,(QD140C[0]-QD80C[0]-PowerSum140)))  #power for T-level
#            info.append(max(0,QResidualMaxTemp[0]))
##            info.append(max(0,(QDmaxTemp[0]-QD140C[0]-PowerSumTmax)))  #power for T-level
#        else:
#            info.append(0)
#            if self.maxTemp>80:
#                info.append(max(0,QResidualMaxTemp[0]))
##                info.append(max(0,(QDmaxTemp[0]-QD80C[0]-PowerSumTmax)))  #power for T-level
#            else:
#                info.append(0)


        Status.int.setGraphicsData('BB Info',info)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def getUserDefinedPars(self):
#------------------------------------------------------------------------------
#   gets the user defined data from UHeatPump and stores it to interfaces to be shown in HP panel
#------------------------------------------------------------------------------

        urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]

        if len(urows) == 0:
#            print 'getUserDefinedParamBB: Status.PId =', Status.PId, 'Status.ANo =', Status.ANo, 'not defined'
#            print 'Error: confusion in PId and ANo'
            dummy = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo} 
            Status.DB.uheatpump.insert(dummy)

            maintainExisting = True
            config = [1,10,0,"Natural Gas",100,500,80]            
            Status.int.setGraphicsData('BB Config',config)

            self.setUserDefinedPars()

        else:
            u = urows[0]
            config = [u.BBMaintain,
                      u.BBSafety,
                      u.BBRedundancy,
                      u.BBFuelType,
                      u.BBHOp,
                      u.BBPmin,
                      u.BBEff]
#            print "ModuleBB (getUserDefinedPars): config = ",config
        return config

#------------------------------------------------------------------------------
    def setUserDefinedPars(self):
#------------------------------------------------------------------------------

        config = Status.int.GData['BB Config']

        urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
        
        if len(urows)==0:
#            print "ModuleBB(setUserDefinedParamHP): corrupt data base - no entry for uheatpump under current ANo"
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
    def screenEquipments(self,setIndex = True):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#------------------------------------------------------------------------------
        self.equipments = Status.prj.getEquipments()
        Status.int.getEquipmentCascade()
        self.NEquipe = len(self.equipments)

        self.BBList = []
        maxIndex = self.NEquipe
        index = 0
        for row in Status.int.cascade:
            index += 1
            if getEquipmentClass(row["equipeType"]) == "BB":
                self.BBList.append(row)
                maxIndex = index

        if setIndex == True:
            self.cascadeIndex = maxIndex

        BBTableDataList = []
        for row in Status.int.EquipTableDataList:
            if getEquipmentClass(row[3]) == "BB":
                BBTableDataList.append(row)

        #screen list and substitute None with "not available"
        for i in range(len(BBTableDataList)):
            for j in range(len(BBTableDataList[i])):
                if BBTableDataList[i][j] == None:
                    BBTableDataList[i][j] = 'not available'        
#        print"ModuleBB;screenEquipments: the list of bb is:",self.BBList
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
#
#------------------------------------------------------------------------------
        if automatic == False:
            if rowNo == None:   #indicates to delete last added equipment dummy
                BBid = self.dummyEqId
            else:
            #--> delete BB from the equipment list under current alternative #from C&QGenerationHC under ANo
                BBid = self.getEqId(rowNo)
#                print "Module BB (delete): id to be deleted = ",BBid
        else:
            BBid= rowNo
#            print "Module BB (delete automaticly): id to be deleted = ",BBid
        
        Status.prj.deleteEquipment(BBid)
        self.screenEquipments()

#------------------------------------------------------------------------------
    def addEquipmentDummy(self):
#------------------------------------------------------------------------------
#       adds a new dummy equipment to the equipment list and returns the
#       position in the cascade 
#------------------------------------------------------------------------------
        self.equipe = Status.prj.addEquipmentDummy()
        self.dummyEqId = self.equipe.QGenerationHC_ID

        self.neweqs += 1 #No of last equip added
        NewEquipmentName = "New boiler %s"%(self.neweqs)

        equipeData = {"Equipment":NewEquipmentName,"EquipType":"Boiler (specify subtype)"}
        self.equipe.update(equipeData)
        Status.SQL.commit()

        self.screenEquipments()
        self.cascadeIndex = self.NEquipe
        
        return(self.equipe)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def setEquipmentFromDB(self,equipe,modelID):
#------------------------------------------------------------------------------
#   takes an equipment from the data base and stores it under a given Id in
#   the equipment data base
#------------------------------------------------------------------------------
        model = self.DB.dbboiler.DBBoiler_ID[modelID][0]

        if model.BBPnom != None: equipe.update({"HCGPnom":model.BBPnom})
        
        if model.BBEfficiency != None:
            if model.BBEfficiency > 1.3 and model.BBEfficiency < 130.0:
                logTrack("ModuleBB: Efficiency data should be stored internally as fractions of 1")
                eff = model.BBEfficiency/100.0
                model.update({"BBEfficiency":eff})
            else:
                eff = model.BBEfficiency
            equipe.update({"HCGTEfficiency":eff})
            
        if model.BoilerTemp is not None: equipe.update({"TMaxSupply":model.BoilerTemp})
        if model.BoilerManufacturer != None: equipe.update({"Manufact":model.BoilerManufacturer})
        if model.BoilerModel is not None: equipe.update({"Model":model.BoilerModel})
        equipe.update({"EquipType":getEquipmentType("BB",model.BoilerType)})
        equipe.update({"NumEquipUnits":1})
        if model.BoilerType is not None: equipe.update({"EquipTypeFromDB":model.BoilerType})
        if model.DBBoiler_ID is not None: equipe.update({"EquipIDFromDB":model.DBBoiler_ID})
        equipe.update({"DBFuel_id":1})  #use Natural Gas as default -> should later on be adjusted to type of equipment
        equipe.update({"ExcessAirRatio":1.1})
        if model.BoilerTurnKeyPrice is not None: equipe.update({"TurnKeyPrice":model.BoilerTurnKeyPrice})
        else:
            logDebug("ModuleBB: turn key price of boiler model %s not specified"%equipe.Model)
            equipe.update({"TurnKeyPrice":0.0})

#HS 2008-10-25: equipment parameters that are set defined by default if not specified
        fuel_number = equipe.DBFuel_id   #IMPORT from the fuelDB
        eq_fuel = Fuel(fuel_number)

        try:
            equipe.FuelConsum = equipe.HCGPnom/(eq_fuel.LCV * equipe.HCGTEfficiency)
        except:
            pass

        try:
            equipe.FlowExhaustGas = equipe.FuelConsum*(1.0 + eq_fuel.CombAir*equipe.ExcessAirRatio)
        except:
            pass

        try:
            equipe.ElectriConsum = 0.01*equipe.HCGPnom
        except:
            pass

        try:
            LossFactEq = 0.01
            TExhaustGas = eq_fuel.LCV*(1.0 - equipe.HCGTEfficiency - LossFactEq) \
                          /((1.0 + eq_fuel.CombAir) * equipe.ExcessAirRatio * eq_fuel.OffgasHeatCapacity)
            equipe.TExhaustGas = TExhaustGas
        except:
            pass

#        print "ModuleBB (setEqFromDB): FuelConsum %s ElectriConsum %s FlowExhaustGas %s TExhaustGas %s"% \
#              (equipe.FuelConsum,equipe.ElectriConsum,equipe.FlowExhaustGas,equipe.TExhaustGas)



###### E.F. 12/10
        if model.BoilerOandMfix is not None: equipe.update({"OandMfix":model.BoilerOandMfix})
        else:
            logDebug("ModuleBB: fix costs for O and M of boiler model %s not specified"%equipe.Model)
            equipe.update({"OandMfix":0.0})
        if model.BoilerOandMvar is not None: equipe.update({"OandMvar":model.BoilerOandMvar})
        else:
            logDebug("ModuleBB: variable costs for O and M of boiler model %s not specified"%equipe.Model)
            equipe.update({"OandMvar":0.0})
######

            
        Status.SQL.commit()
        logTrack("moduleBB (setEquipmentFromDB): boiler added:'%s',type:'%s',Pow:'%s',T'%s'"%\
                 (model.BoilerManufacturer,model.BoilerType,model.BBPnom,model.BoilerTemp))
        self.calculateEnergyFlows(equipe,self.cascadeIndex)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,cascadeIndex):
#------------------------------------------------------------------------------
#   calculates the energy flows in the equipment identified by "cascadeIndex"
#------------------------------------------------------------------------------
        if Status.int.cascadeUpdateLevel < (cascadeIndex - 1):
            logDebug("ModuleBB (calculateEnergyFlows): cannot calulate without previously updating the previous levels")
            Status.mod.moduleEnergy.runSimulation(last=(cascadeIndex-1))
        Status.int.extendCascadeArrays(cascadeIndex)

        if cascadeIndex > 0 and cascadeIndex <= Status.NEquipe:
            logTrack("ModuleBB (calculateEnergyFlows): starting (cascade no: %s)"%cascadeIndex)
        else:
            logError("ModuleBB (calculateEnergyFlows): cannot simulate index %s: out of cascade [%s]"%\
                     (cascadeIndex,Status.NEquipe))
            return
#..............................................................................
# get equipment data from equipment list in SQL

        BBModel = equipe.Model
        BBType = equipe.EquipType
        PNom = equipe.HCGPnom
        PEl = equipe.ElectriConsum
        COPh_nom = equipe.HCGTEfficiency
        TMax = equipe.TMaxSupply
        EquipmentNo = equipe.EqNo

        if PNom is None:
            PNom = 0.0
            logWarning("ModuleBB (calculateEnergyFlows): No nominal power specified for equipe no. %s"%\
                 (EquipmentNo))

        if PEl is None:
            PEl = 0.01 * PNom
            logWarning("ModuleBB (calculateEnergyFlows): No electrical consumption specified for equipe no. %s"%\
                 (EquipmentNo))

        if TMax is None:
            TMax = INFINITE
            logDebug("ModuleBB (calculateEnergyFlows): no Tmax specified for equipe no. %s"%EquipmentNo)
  
        logTrack("ModuleBB (calculateEnergyFlows): Model = %s Type = %s PNom = %s"%\
                 (BBModel,BBType,PNom))

#........................................................................
# f_QWH: proportion waste heat vs. USH

        LossFactEq = 0.01
        if COPh_nom > 0:
            f_QWH = max (0,1. - COPh_nom -  LossFactEq)/COPh_nom
        else:
            f_QWH = 0

# temperature distribution of waste heat. assumed as fix

        TExhaustGas = equipe.TExhaustGas
        if TExhaustGas == None:
            logDebug("Boiler exhaust gas temperature not specified. 200 ºC assumed")
            TExhaustGas = 200

        fuel = Fuel(equipe.DBFuel_id)
        TMinOffGas = max(fuel.TCondOffGas(),0)
        dTtot = max(TExhaustGas-TMinOffGas,1.e-10)

        f_QWH_T = []

        for iT in range(Status.NT+2):
            
            dT = max(iT*Status.TemperatureInterval - TMinOffGas,0.)
            f_QWH_T.append(f_QWH*max(0.0,1.0-dT/dTtot))
            

#..............................................................................
# get demand data for CascadeIndex/EquipmentNo from Interfaces
# and create arrays for storing heat flow in equipment

        QD_Tt = copy.deepcopy(Status.int.QD_Tt_mod[cascadeIndex-1])
        QA_Tt = copy.deepcopy(Status.int.QA_Tt_mod[cascadeIndex-1])
        
        USHj_Tt = Status.int.createQ_Tt()
        USHj_T = Status.int.createQ_T()

        QHXj_Tt = Status.int.createQ_Tt()
        QHXj_T = Status.int.createQ_T()

        QWHj_Tt = Status.int.createQ_Tt()
        QWHj_T = Status.int.createQ_T()

#..............................................................................
# Start hourly loop

        USHj = 0
        QHXj = 0
        QWHj = 0
        HPerYear = 0
        QD = 0

        for it in range(Status.Nt):

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
            if USHj_Tt[Status.NT+1][it]>0:
                HPerYear += Status.TimeStep

            QD += QD_Tt[Status.NT+1][it]

            for iT in range(Status.NT+2):
                QWHj_Tt[iT][it] = USHj_Tt[Status.NT+1][it]*f_QWH_T[iT]
            QWHj += QWHj_Tt[0][it]

#..............................................................................
# End of year reached. Store results in interfaces
       
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

        logTrack("ModuleBB (calculateEnergyFlows): Total energy supplied by equipment %s MWh"%(USHj*Status.EXTRAPOLATE_TO_YEAR))
        logTrack("ModuleBB (calculateEnergyFlows): Total waste heat input  %s MWh"%(QHXj*Status.EXTRAPOLATE_TO_YEAR))

        Status.int.cascadeUpdateLevel = cascadeIndex

#........................................................................
# Global results (annual energy flows)

        USHj *= Status.EXTRAPOLATE_TO_YEAR
        QWHj *= Status.EXTRAPOLATE_TO_YEAR
        HPerYear *= Status.EXTRAPOLATE_TO_YEAR
        Status.int.USHj[cascadeIndex-1] = USHj

        if COPh_nom > 0:
            FETFuel_j = USHj/COPh_nom
        else:
            FETFuel_j = 0.0
            showWarning("Strange boiler with COP = 0.0")

        if PNom > 0:
            FETel_j = FETFuel_j*PEl/PNom
        else:
            FETel_j = 0
        
        Status.int.FETFuel_j[cascadeIndex-1] = FETFuel_j
        Status.int.FETel_j[cascadeIndex-1] = FETel_j
        Status.int.HPerYearEq[cascadeIndex-1] = HPerYear
        
        Status.int.QWHj[cascadeIndex-1] = QWHj   # not considering the latent heat(condensing water)
        Status.int.QHXj[cascadeIndex-1] = 0.0

#        logMessage("Boiler: eq.no.:%s energy flows [MWh] USH: %s FETFuel: %s FETel: %s QD: %s HPerYear: %s "%\
#                   (equipe.EqNo,\
#                    USHj*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
#                    FETFuel_j*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
#                    FETel_j*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
#                    QD*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
#                    HPerYear*Status.EXTRAPOLATE_TO_YEAR/1000.0))

        self.calculateOM(equipe,USHj)
        
#........................................................................       
        return USHj    


#==============================================================================

 
#------------------------------------------------------------------------------
    def sortBoiler (self): 
#------------------------------------------------------------------------------
#   moove all the boilers to the end of the cascade.
#  sorts boilers by temperature and by efficiency
#------------------------------------------------------------------------------
#first bring all your boilers in a listing for easier access
        boilerList = []
        for i in range(len(Status.int.cascade)):
            entry = Status.int.cascade[i]
            a=getEquipmentClass(entry["equipeType"])
            if a=="BB":
                eqID = entry["equipeID"]
                equipe = Status.DB.qgenerationhc.QGenerationHC_ID[eqID][0]
                efficiency = equipe.HCGTEfficiency
                temperature = equipe.TMaxSupply
                boilerList.append({"equipeID":eqID,"efficiency":efficiency,"temperature":temperature})

#then reorganise boilerList by efficiencies (maybe there are more intelligent ways to do this, but here's one ...:
# if you want the most efficient on top [n-1] instead on bottom [0], just change the sign of the comparison from > to <

        for i in range(len(boilerList)):
            for j in range(i,len(boilerList)):
                if boilerList[j]["efficiency"] > boilerList[i]["efficiency"]:
                    bi = boilerList[i]
                    bj = boilerList[j]
                    boilerList[i] = bj
                    boilerList[j] = bi
                    
#then reorganise boilerList by temperature levels:
#   first level:

        for i in range(len(boilerList)):
            for j in range(i,len(boilerList)):
                if boilerList[i]["temperature"] > 80 and boilerList[j]["temperature"]<=80:
                    bi = boilerList[i]
                    bj = boilerList[j]
                    boilerList[i] = bj
                    boilerList[j] = bi

#   second level:

#        for i in range(len(boilerList)):
#            for j in range(i,len(boilerList)):
#                if 80 < boilerList[i]["temperature"] <= 140 and (boilerList[j]["temperature"]<=80     or boilerList[j]["temperature"]>140):
#                    bi = boilerList[i]
#                    bj = boilerList[j]
#                    boilerList[i] = bj
#                    boilerList[j] = bi

#   second level:

        for i in range(len(boilerList)):
            for j in range(i,len(boilerList)):
                if  boilerList[i]["temperature"] > 140 and  boilerList[j]["temperature"]<=140:
                    bi = boilerList[i]
                    bj = boilerList[j]
                    boilerList[i] = bj
                    boilerList[j] = bi


#then move consecutively to the bottom of the cascade (move the one last, which you finally want to have at the bottom

        for i in range(len(boilerList)):
            eqID = boilerList[i]["equipeID"]
            equipe = Status.DB.qgenerationhc.QGenerationHC_ID[eqID][0]
            cascadeIndex = equipe.CascadeIndex
            if cascadeIndex < Status.int.NEquipe:
                Status.mod.moduleHC.cascadeMoveToBottom(cascadeIndex)

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
            
    
#------------------------------------------------------------------------------
    def automDeleteBoiler (self,minEfficencyAccepted=0.80):  #0.80 is a default value for minimum of efficiency
#------------------------------------------------------------------------------
# delete unefficient boiler
#------------------------------------------------------------------------------
        self.screenEquipments()
        automatic=True
        for i in range (len (self.BBList)):
#            print "controlling equipe", self.BBList[i]['equipeID']
            eff= Status.DB.qgenerationhc.QGenerationHC_ID[self.BBList[i]['equipeID']][0]['HCGTEfficiency']
#            print "efficiency of the boiler number '%s'is:'%s'"%(i,eff)
#            print "min efficiency accepted:",minEfficencyAccepted
            if eff < minEfficencyAccepted:
#                 add the fuel criterion: if not biomass,biofuels?,gas methane ->delete ???
#                print "Module BB (): id to be deleted = ",self.BBList[i]['equipeID']
                self.dummyEqId = self.BBList[i]['equipeID']
                self.deleteEquipment(None)        #(self.BBList[i]['equipeID'],automatic)# The row number should be passed. is this right? 
                
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

        QDcrit = 0.99*QDa[Status.NT+1]
        
        for i in range(1,Status.NT+1):
            if QDa[i]>QDa[i-1] and QDa[i-1] < QDcrit:
                self.maxTemp=Status.TemperatureInterval*i #temperatureInterval is defined in status.py

#------------------------------------------------------------------------------
    def redundancy(self):
#------------------------------------------------------------------------------
#       when redundancy is required provides suitable boilers.
#       N.B. the possibility of retriveing deleted boilers is not implemented yet.
#       N.B. The possibility that a boiler with nominal power > than biggerBB is in the list has to be considered.
#------------------------------------------------------------------------------      
        self.maxPow80=0
        self.maxPow140=0
        self.maxPowTmax=0
        for k in range(len(Status.int.cascade)):

#HS2008-07-05: here some abbreviations
            equipeID = Status.int.cascade[k]["equipeID"]
            
            if getEquipmentClass(Status.int.cascade[k]["equipeType"]) == "BB":
                equipe = Status.DB.qgenerationhc.QGenerationHC_ID[equipeID][0]
                Pnom = Status.int.cascade[k]["equipePnom"]
                if equipe['TMaxSupply'] <=90 and \
                   Pnom > self.maxPow80:     # TMaxSupply to be sostituted with tthe operating temperature
                    self.maxPow80 = Pnom
                elif 90 < equipe['TMaxSupply'] <= 150 and \
                     Pnom > self.maxPow140:
                    self.maxPow140 = Pnom
                elif equipe['TMaxSupply']>150 and\
                     Pnom > self.maxPowTmax:
                    self.maxPowTmax = Pnom
#        print"moduleBB;Function redundancy: the power of the redundant boiler are", self.maxPow80,self.maxPow140,self.maxPowTmax
        if self.maxPow80>0:
            modelID =self.selectBB(max(self.minPow,self.maxPow80),80)
            equipe = self.addEquipmentDummy()
            self.setEquipmentFromDB(equipe,modelID)
        if self.maxPow140>0:  #and self.maxTemp>140:
            modelID =self.selectBB(max(self.minPow,self.maxPow140),140)
            equipe = self.addEquipmentDummy()
            self.setEquipmentFromDB(equipe,modelID)
        if self.maxPowTmax>0:
            modelID =self.selectBB(max(self.minPow,self.maxPowTmax),self.maxTemp)
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
        Power = max(self.minPow,Pow)
        sqlQuery="BoilerTemp >= '%s'AND BBPnom >= '%s' ORDER BY BBPnom ASC" %(Top,Power)       
        selected = Status.DB.dbboiler.sql_select(sqlQuery)
        for i in range(len(selected)):
            for j in range(i,len(selected)):
                if selected[j].BoilerTemp < selected[i].BoilerTemp:
                    bi = selected[i]
                    bj = selected[j]
                    selected[i] = bj
                    selected[j] = bi

        i=0
        goodEf=False
        while i<len(selected) and goodEf == False:
            if selected[i].BBEfficiency >= self.minEff:
                goodEf = True
            i= i+1
        if goodEf == True:
            modelID =selected[(i-1)].DBBoiler_ID
        else:
            modelID =selected[0].DBBoiler_ID
            showWarning(_("in the database no boiler with the desired efficiency has be found")) 
                                  
#        modelID =selected[0].DBBoiler_ID
#        print "selectBB: the requested power is:", Pow 
#        print "selectBB: the selected boiler ID is:", modelID
#        print "selectBB: the list of boiler is:"
#        print selected
        return modelID
        


            
#------------------------------------------------------------------------------
    def designBB80(self):
#------------------------------------------------------------------------------
#    def designBB80(self,...):
# design a boiler sistem at 80°C
#------------------------------------------------------------------------------
        print "moduleBB starting function 'designBB80'"
        added=0
        if Status.int.QD_T_mod[self.firstBB][int(80/Status.TemperatureInterval)] >= 0.1*Status.int.QD_T_mod[self.firstBB][int(self.maxTemp/Status.TemperatureInterval)]: #we design boiler at this temperature level only if the demand is bigger than the 10% of the total demand
            print "point AA reached"
            if self.QDh80[0]*self.securityMargin >= self.minPow:
                print "point AB reached"
                if self.QDh80[0]*self.securityMargin>=2*self.minPow:
                    print "point AC reached"
                    if self.QDh80[0]*self.securityMargin < self.QDh80[int((self.minOpTime)*Status.Nt/8760)]*1.3 \
                       or (self.QDh80[0]*self.securityMargin - self.QDh80[int((self.minOpTime)*Status.Nt/8760)]) < self.minPow:
                        print "point A reached"
                        modelID = self.selectBB((self.QDh80[0]*self.securityMargin),80)  #select the right bb from the database.                        
#HS line not valid code                        selectBB((QDh_descending[0]*securityMargin),...)  #select the right bb from the database.
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
#HS: elif requires a condition !!!                    elif:
                    else:
                        if self.QDh80[int((self.minOpTime)*Status.Nt/8760)]>self.bigger80:
                            for i in range (int(self.QDh80[int((self.minOpTime)*Status.Nt/8760)]/self.bigger80)):
                                print "point B reached"
                                modelID =self.selectBB(self.bigger80,80)
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)
                            added += int(self.QDh80[int((self.minOpTime)*Status.Nt/8760)]/self.bigger80)*self.bigger80
                        else:
                            print "point C reached; the demand at 1000hours, at the minOpTime and the minOpTime itself are:", self.QDh80[1000],\
                                  self.QDh80[int((self.minOpTime)*Status.Nt/8760)], self.minOpTime
                            print "point CC reached; the length of self.QDh80 is: ", len(self.QDh80)
                            modelID =self.selectBB(self.QDh80[int((self.minOpTime)*Status.Nt/8760)],80) #aggiungere condizione sul rendimento
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
                                added += self.DB.dbboiler.DBBoiler_ID[modelID][0].BBPnom                                                    #EF 05/06/2009
                                if self.QDh80[0]*self.securityMargin - added >= 0:                                                          #EF 05/06/2009
                                    equipe = self.addEquipmentDummy()
                                    self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                        else:
#HS: elif requires a condition !!!                        elif:
                            print "point G reached; added and self.QDh80[0]*self.securityMargin are: ",added , self.QDh80[0]*self.securityMargin
                            if added < self.QDh80[0]*self.securityMargin:                                                       #EF 26/10/2008
                                modelID=self.selectBB(min((self.QDh80[0]*self.securityMargin - added),self.minPow),80)          #EF 26/10/2008
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                else:
#HS: elif requires a condition !!!                elif:
                    print "point H reached"
                    print "moduleBB;designBB: looking for a boiler with T>'%s' and Pow>'%s'"%(80,self.QDh80[0]*self.securityMargin)
                    modelID=self.selectBB(self.QDh80[0]*self.securityMargin,80)
                    equipe = self.addEquipmentDummy()
                    self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list

        print "point i reached"
        self.sortBoiler()                
                        

                    

#------------------------------------------------------------------------------
    def designBB140(self):
#HS input list has to be defined !!!!    def designBB140(self,...):
#------------------------------------------------------------------------------
# design a boiler sistem at 140°C
#------------------------------------------------------------------------------
        print "moduleBB starting function 'designBB140'"
        added=0
        if Status.int.QD_T_mod[self.firstBB140][int(140/Status.TemperatureInterval)] >= 0.1*Status.int.QD_T_mod[self.firstBB][int(self.maxTemp/Status.TemperatureInterval)]:
            print"point A1 reached"
            if self.QDh140[0]*self.securityMargin >= self.minPow:
                print "point A2 reached"
                if self.QDh140[0]*self.securityMargin>=2*self.minPow:
                    print "point A3 reached"
                    if self.QDh140[0]*self.securityMargin < self.QDh140[int((self.minOpTime)*Status.Nt/8760)]*1.3 or \
                    self.QDh140[0]*self.securityMargin -self.QDh140[int((self.minOpTime)*Status.Nt/8760)]<self.minPow:
                        print "point A4 reached"
                    
#HS TAKE CARE !!!! methods of the same class have to be called with the "self." before
#                   has probably to be corrected throughout the code ... !!!!
#                        selectBB((QDh_descending[0]*securityMargin)) # ,...)  #select the right bb from the database.
                        modelID=self.selectBB((self.QDh140[0]*self.securityMargin),140) # ,...)  #select the right bb from the database.
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list

                    else:
#HS: elif requires a condition !!!                    elif:
                        if self.QDh140[int((self.minOpTime)*Status.Nt/8760)]>self.bigger140:
                            for i in range (int(self.QDh140[int((self.minOpTime)*Status.Nt/8760)]/self.bigger140)):
                                print "point B1 reached"
                                modelID =self.selectBB(self.bigger140,140)
                                equipe = self.addEquipmentDummy()
                                self.setEquipmentFromDB(equipe,modelID)
                            added += int(self.QDh140[int((self.minOpTime)*Status.Nt/8760)]/self.bigger140)*self.bigger140
                        else:
                            print "point C1 reached"
                            modelID =self.selectBB(self.QDh140[int((self.minOpTime)*Status.Nt/8760)],140)  #  select the base load boiler from DB
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
                                added += self.DB.dbboiler.DBBoiler_ID[modelID][0].BBPnom                                                    #EF 05/06/2009
                                if self.QDh140[0]*self.securityMargin - added >= 0:                                                         #EF 05/06/2009
                                    equipe = self.addEquipmentDummy()
                                    self.setEquipmentFromDB(equipe,modelID)
                            
                        else:
                            print "point G1 reached"
                            if added < self.QDh140[0]*self.securityMargin:                                                 #EF 26/10/2008     
                                modelID=self.selectBB(min((self.QDh140[0]*self.securityMargin - added),self.minPow),140)    #EF 26/10/2008
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
        print "moduleBB starting function 'designBBmaxTemp'"
        added=0
        if self.QDhmaxTemp[0]*self.securityMargin>=2*self.minPow:
            if self.QDhmaxTemp[0]*self.securityMargin < self.QDhmaxTemp[int((self.minOpTime)*Status.Nt/8760)]*1.3 \
               or (self.QDhmaxTemp[0]*self.securityMargin - self.QDhmaxTemp[int((self.minOpTime)*Status.Nt/8760)]) < self.minPow:
                modelID = self.selectBB(max((self.QDhmaxTemp[0]*self.securityMargin),self.minPow),self.maxTemp) #HS....,...)  #select the right bb from the database.
                equipe = self.addEquipmentDummy()
                self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list

            else:
                if self.QDhmaxTemp[int((self.minOpTime)*Status.Nt/8760)]>self.biggermaxTemp:
                    for i in range (int(self.QDhmaxTemp[int((self.minOpTime)*Status.Nt/8760)]/self.biggermaxTemp)):
                        modelID =self.selectBB(self.biggermaxTemp,self.maxTemp)
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)
                    added += int(self.QDhmaxTemp[int((self.minOpTime)*Status.Nt/8760)]/self.biggermaxTemp)*self.biggermaxTemp
                else:
                    modelID =self.selectBB(max(self.QDhmaxTemp[int((self.minOpTime)*Status.Nt/8760)],self.minPow),self.maxTemp)
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
                        modelID =self.selectBB(max((self.QDhmaxTemp[0]*self.securityMargin - added),self.minPow),self.maxTemp)
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)
                    else:
                        modelID=self.selectBB(max(((self.QDhmaxTemp[0]*self.securityMargin - added)/2),self.minPow),self.maxTemp)
                        equipe = self.addEquipmentDummy()
                        self.setEquipmentFromDB(equipe,modelID)
                        added += self.DB.dbboiler.DBBoiler_ID[modelID][0].BBPnom                                                    #EF 05/06/2009
                        if self.QDhmaxTemp[0]*self.securityMargin - added >= 0:                                                     #EF 05/06/2009
                            equipe = self.addEquipmentDummy()
                            self.setEquipmentFromDB(equipe,modelID)

                   
                else:
                    modelID=self.selectBB(max((self.QDhmaxTemp[0]*self.securityMargin - added),self.minPow),self.maxTemp)
                    equipe = self.addEquipmentDummy()
                    self.setEquipmentFromDB(equipe,modelID)

        else:
            modelID=self.selectBB(max(self.QDhmaxTemp[0]*self.securityMargin,self.minPow),self.maxTemp)
            equipe = self.addEquipmentDummy()
            self.setEquipmentFromDB(equipe,modelID)


        self.sortBoiler()
    
#------------------------------------------------------------------------------
    def designAssistant(self):
#------------------------------------------------------------------------------
#   auto-design of boiler cascade
#------------------------------------------------------------------------------

#............................................................................................
# getting configuration parameters of DA
        print "moduleBB starting function 'designAssistant'"

        DATable = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(DATable) > 0:
            DA = DATable[0]
        else:
            logTrack("ModuleBB (design assistant): WARNING - no DA configuration parameters available")
            return

        if DA.BBRedundancy == True:
            pass
        
#        self.securityMargin=1.2      #  N.B. securityMargin should be choosen by the user!!! At the moment is setted to 1.2############
#        self.minPow =100             #  N.B. minPow should be an imput from the boiler window!!! At the moment is setted to 100kW
#        self.minOpTime=100          #  N.B. minOpTime should be an imput from the boiler window!!! At the moment is setted to 100 hours:for testing Nt is 168 corresponding to 1 week.
        try:                   ####  E.F. 29/07
            self.securityMargin = 1+DA.BBSafety/100  
        except:
            self.securityMargin = 1.2
        print "ModuleBB (design assistant): securityMargin =", self.securityMargin
        if DA.BBMaintain != None:
            self.Maintain= DA.BBMaintain
        else:
            self.Maintain = 1
        print "ModuleBB (design assistant): maintain =", self.Maintain
        if DA.BBRedundancy!= None:
            self.redund= DA.BBRedundancy
        else:
            self.redund= 0
        print "ModuleBB (design assistant): redoundancy =", self.redund
        if DA.BBPmin!= None:
            self.minPow = DA.BBPmin
        else:
            self.minPow = 200
        print "ModuleBB (design assistant): minPow =", self.minPow

        if DA.BBHOp!= None:
            self.minOpTime = DA.BBHOp
        else:
            self.minOpTime = 100
        print "ModuleBB (design assistant): minOpTime =", self.minOpTime
        if DA.BBEff != None:
            self.minEff= DA.BBEff/100
        else:
            self.minEff = 80
        if DA.BBFuelType != "Natural Gas":
            showWarning(_("In the present version only Natural Gas boilers has been collected in the DB"))
        
#        self.screenEquipments()
#HS 2008-07-06: this should not be necessary. should be updated

        if self.Maintain == 0:
            for row in self.BBList:
                self.dummyEqId = row['equipeID']
                self.deleteEquipment(None)

        else:
            self.automDeleteBoiler(self.minEff)   # delete unefficient boiler

#............................................................................................
# first do some sorting ...

#        self.findmaxTemp(Status.int.QD_T)
#HS2008-07-06: CHECK CHECK CHECK -> should this not be the REAL demand seen by the boiler cascade ???
        self.findmaxTemp(Status.int.QD_T_mod[self.cascadeIndex-1])
        
        self.findBiggerBB()       
        self.sortBoiler()     # sort boilers by temperature (ascending) and by efficiency (descending)
                                

#............................................................................................
# after shifting, the equipment cascade has to be updated, as the modified demand is used
# in the following

        if Status.int.cascadeUpdateLevel < self.NEquipe:
            Status.mod.moduleEnergy.runSimulation()
            
#............................................................................................
# low temperature boiler look-up
        exBP=0       #   power of the boiler in the cascade operating at 80°C

        for row in Status.int.cascade:
            bbs = Status.DB.qgenerationhc.QGenerationHC_ID[row["equipeID"]]
            if len(bbs) > 0:
                equipTry= bbs[0]
                if getEquipmentClass(row["equipeType"]) == "BB" and equipTry.TMaxSupply <=80:
                    exBP += row['equipePnom']

        logTrack("ModuleBB: power of the boilers at 80°C present in the cascade at the moment %s"%exBP)

        if self.firstBB < 0 or self.firstBB > self.NEquipe-1:
            logDebug("MoudleBB (DA): error in no. of firstBB: %s (NEquipe = %s)"%(self.firstBB,self.NEquipe))
            
        iT80 = int(80/Status.TemperatureInterval + 0.5)
#        zz=int(80/Status.TemperatureInterval)
#HS2008-07-06: zz substituted by iT80. is more self-understanding

        QDmax = maxInList(Status.int.QD_Tt_mod[self.firstBB][iT80])
#        yy= maxInList(Status.int.QD_Tt_mod[self.firstBB][iT80])
#HS2008-07-06. idem yy -> QDmax

        b=max((QDmax  - exBP),0)
        b1= max(((QDmax  * self.securityMargin) - exBP),0) #   minimum power of the new boilers at 80°C
        c=[]
        print "moduleBB, design assistant: the length of Status.Nt is: ", Status.Nt
        for it in range (Status.Nt):
            c.append ( min (b, Status.int.QD_Tt_mod[self.firstBB][iT80][it]))

        self.QDh80=c  # demand to be supplied by new boilers at 80°C

        self.QDh80.sort(reverse=True)
        print 'moduleBB, design assistant: QDmax, b, self.QDh80[0], exBP are:', QDmax, b, self.QDh80[0], exBP
        print "moduleBB, design assistant: the length of self.QDh80 is: ", len(self.QDh80)
        if self.QDh80[0]>0:
            self.designBB80()

#............................................................................................
# 140 ºC boilers
            
        if self.maxTemp>160:   # N.B. The difference between temperature levels is now setted in 20°C but in the future could be a parameter.      
                        
            exBP=0       #   power of the boiler in the cascade operating at 140°C
            for row in Status.int.cascade:
                bbs = Status.DB.qgenerationhc.QGenerationHC_ID[row["equipeID"]]
                if len(bbs) > 0:
                    equipTry= bbs[0]
                    if getEquipmentClass(row["equipeType"]) == "BB" and 90 <= equipTry.TMaxSupply <=140:
                        exBP += row['equipePnom']

            iT140 =int(140/Status.TemperatureInterval + 0.5)
            QDmax = maxInList(Status.int.QD_Tt_mod [self.firstBB140][iT140])
            b=max((QDmax  - exBP),0) #   minimum power of the new boilers at 140°C
            c=[]
            for it in range (Status.Nt):
                c.append ( min (b, Status.int.QD_Tt_mod[self.firstBB140][iT140][it]))

            self.QDh140=c  # demand to be supplied by new boilers at 140°C
            self.QDh140.sort(reverse=True)

            if self.QDh140[0]>0:
                self.designBB140()
        
#............................................................................................
# maxTemp boilers


#        exBP=0       #   power of the boiler in the cascade operating at maxTemp
#        for row in Status.int.cascade:
#            bbs = Status.DB.qgenerationhc.QGenerationHC_ID[row["equipeID"]]
#            if len(bbs) > 0:
#                equipTry= bbs[0]

#            if getEquipmentClass(row["equipeType"]) == "BB":
#                exBP += row['equipePnom']

#        cI= len(Status.int.QD_Tt_mod)+1
#        
#        iTmax =int(self.maxTemp/Status.TemperatureInterval + 0.5)
#        QDmax = maxInList(Status.int.QD_Tt_mod [self.firstBBmaxTemp][iTmax])
#        b=max((QDmax  - exBP),0) #   minimum power of the new boilers at maxTemp°C
#        c=[]
#        for it in range (Status.Nt):
#            c.append ( min (b, Status.int.QD_Tt_mod[self.firstBBmaxTemp][iTmax][it]))

#        self.QDhmaxTemp=c  # demand to be supplied by new boilers at maxTemp°C

#        self.QDhmaxTemp.sort(reverse=True)
#        print "moduleBB;designAssistant:self.QDhmaxTemp[0]=",self.QDhmaxTemp[0]
#        if self.QDhmaxTemp[0]>0:
#            self.designBBmaxTemp()

#............................................................................................
        iT_maxTemp= int((self.maxTemp/Status.TemperatureInterval)+0.5)
        self.QDhmaxTemp = copy.deepcopy(Status.int.QD_Tt_mod[self.cascadeIndex][iT_maxTemp])
        self.QDhmaxTemp.sort(reverse=True)
        if self.QDhmaxTemp[0]>0:
            self.designBBmaxTemp()




        self.sortBoiler()
        if self.redund == 1:
            self.redundancy()
        
#        self.updatePanel()    #updatePanel should be called only from the Panel !!!

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
