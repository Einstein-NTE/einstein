# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleCHP (Combined Heat and Power)
#			
#------------------------------------------------------------------------------
#			
#	Module for calculation of boilers
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Hans Schweiger	05/09/2008
#                           based on ModuleBB
#	Last revised by:
#                           Hans Schweiger      03/10/2008
#                           Enrico Facci        12/10/2008
#
#       Changes to previous version:
#
#       03/10/08: HS    calculatOM added
#       12/10/08: EF    changes in setEquipmentsFromDB:  values for OM copied into the qgenerationhc DB.
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
from einstein.modules.messageLogger import *

CHPMAXTEMP = {
    "CHP engine": 90.0,
    "gas turbine": 250.0
    }

#============================================================================== 
#============================================================================== 
class ModuleCHP(object):
#============================================================================== 
#============================================================================== 

    CHPList = []
    
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

        (CHPList,CHPTableDataList) = self.screenEquipments()

        if Status.int.cascadeUpdateLevel < self.cascadeIndex:
            Status.mod.moduleEnergy.runSimulation(self.cascadeIndex)

#............................................................................................
# 1. List of equipments

        matrix = []
        for row in CHPTableDataList:
            matrix.append(row)

        data = array(matrix)

        Status.int.setGraphicsData('CHP Table',data)
#............................................................................................
# 2a. Preparing data

        QCHP = copy.deepcopy(Status.int.USHj_Tt[self.cascadeIndex-1][Status.NT+1])
        QCHP.sort(reverse=True)

        QD80C = copy.deepcopy(Status.int.QD_Tt_mod[self.cascadeIndex-1][int(80/Status.TemperatureInterval+0.5)])
        QD80C.sort(reverse=True)

        QD120C = copy.deepcopy(Status.int.QD_Tt_mod[self.cascadeIndex-1][int(120/Status.TemperatureInterval)])
        QD120C.sort(reverse=True)

        QD250C = copy.deepcopy(Status.int.QD_Tt_mod[self.cascadeIndex-1][int(250/Status.TemperatureInterval)])
        QD250C.sort(reverse=True)

        QDTot = copy.deepcopy(Status.int.QD_Tt_mod[self.cascadeIndex-1][Status.NT+1])
        QDTot.sort(reverse=True)

#............................................................................................
# 2b. XY Plot
        TimeIntervals=[]
        for it in range(Status.Nt+1):
            TimeIntervals.append(Status.TimeStep*(it+1)*Status.EXTRAPOLATE_TO_YEAR)

            Status.int.setGraphicsData('CHP Plot',[TimeIntervals,
                                                            QCHP,
                                                            QD80C,
                                                            QD120C,
                                                            QD250C,
                                                            QDTot])

#............................................................................................
# 3. Configuration design assistant

        config = self.getUserDefinedPars()
        Status.int.setGraphicsData('CHP Config',config)
        
#............................................................................................
# 4. additional information (Info field right side of panel)

        info = []

#xxxx dummy values. to be substituted by real ones ...        
        self.operatingHours = 1234.0
        self.eff_el_eq = 99.9
        self.minHOp = 2000.0
        
        info.append(self.operatingHours)  #first value to be displayed
        info.append(self.eff_el_eq)

        indexMinHOp = (int) (self.minHOp / (Status.TimeStep*Status.EXTRAPOLATE_TO_YEAR))
        indexMinHOp = min(indexMinHOp,Status.Nt-1)
        
        info.append(max(0,QD80C[indexMinHOp]))
        info.append(max(0,QD120C[indexMinHOp]))
        info.append(max(0,QD250C[indexMinHOp]))
        info.append(max(0,QDTot[indexMinHOp]))

        Status.int.setGraphicsData('CHP Info',info)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def getUserDefinedPars(self):
#------------------------------------------------------------------------------
#   gets the user defined data from UHeatPump and stores it to interfaces to be shown in HP panel
#------------------------------------------------------------------------------

        urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]

        if len(urows) == 0:
            dummy = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo} 
            Status.DB.uheatpump.insert(dummy)

            maintainExisting = True
            config = [1,"CHP Engine","Natural Gas",2000.0,0.55]            
            Status.int.setGraphicsData('CHP Config',config)

            self.setUserDefinedPars()

        else:
            u = urows[0]
            config = [u.CHPMaintain,
                      u.CHPType,
                      u.CHPFuelType,
                      u.CHPHOp,
                      u.CHPEff]

        self.minHOp = config[3]

        return config

#------------------------------------------------------------------------------
    def setUserDefinedPars(self):
#------------------------------------------------------------------------------

        config = Status.int.GData['CHP Config']

        urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
        
        if len(urows)==0:
            dummy = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo} 
            Status.DB.uheatpump.insert(dummy)
            urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
            
        u = urows[0]

        u.CHPMaintain = config[0]
        u.CHPType = config[1]
        u.CHPFuelType = config[2]
        u.CHPHOp = config[3]
        u.CHPEff = config[4]

        self.minHOp = config[3]

        Status.SQL.commit()

#------------------------------------------------------------------------------
    def screenEquipments(self,setIndex = True):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#------------------------------------------------------------------------------
        print "moduleCHP starting function 'screenEquipments'"
        self.equipments = Status.prj.getEquipments()
        Status.int.getEquipmentCascade()
        self.NEquipe = len(self.equipments)

        self.CHPList = []
        maxIndex = 1
        index = 0
        for row in Status.int.cascade:
            index += 1
            if getEquipmentClass(row["equipeType"]) == "CHP":
                self.CHPList.append(row)
                maxIndex = index

        if setIndex == True:
            self.cascadeIndex = maxIndex

        CHPTableDataList = []
        for row in Status.int.EquipTableDataList:
            if getEquipmentClass(row[3]) == "CHP":
                CHPTableDataList.append(row)

        #screen list and substitute None with "not available"
        for i in range(len(CHPTableDataList)):
            for j in range(len(CHPTableDataList[i])):
                if CHPTableDataList[i][j] == None:
                    CHPTableDataList[i][j] = 'not available'        
        print"ModuleCHP;screenEquipments: the list of bb is:",self.CHPList
        return (self.CHPList,CHPTableDataList)
        

        
#------------------------------------------------------------------------------
    def getEqId(self,rowNo):
#------------------------------------------------------------------------------
#   gets the EqId from the rowNo in the CHPList
#------------------------------------------------------------------------------

        CHPId = self.CHPList[rowNo]["equipeID"]
        return CHPId

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def deleteEquipment(self,rowNo,automatic=False):
#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------
        if automatic == False:
            if rowNo == None:   #indicates to delete last added equipment dummy
                CHPid = self.dummyEqId
            else:
            #--> delete CHP from the equipment list under current alternative #from C&QGenerationHC under ANo
                CHPid = self.getEqId(rowNo)
        else:
            CHPid= rowNo
        
        Status.prj.deleteEquipment(CHPid)
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
        NewEquipmentName = "New CHP %s"%(self.neweqs)

        equipeData = {"Equipment":NewEquipmentName,"EquipType":"CHP (specify subtype)"}
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
        model = self.DB.dbchp.DBCHP_ID[modelID][0]

        if model.CHPPt != None: equipe.update({"HCGPnom":model.CHPPt})
        
        if model.Eta_t != None:
            if model.Eta_t > 1.0 and model.Eta_t < 100.0:
                logTrack("ModuleCHP: Efficiency data should be stored internally as fractions of 1")
                eff = model.Eta_t/100.0
                model.update({"Eta_t":eff})
            else:
                eff = model.Eta_t
            equipe.update({"HCGTEfficiency":eff})
            
        if model.Eta_e != None:
            if model.Eta_e > 1.0 and model.Eta_e < 100.0:
                logTrack("ModuleCHP: Efficiency data should be stored internally as fractions of 1")
                eff = model.Eta_e/100.0
                model.update({"Eta_t":eff})
            else:
                eff = model.Eta_e
            equipe.update({"HCGEEfficiency":eff})
            
#        if model.BoilerTemp != None: equipe.update({"TMaxSupply":model.BoilerTemp})
#        if model.BoilerManufacturer != None: equipe.update({"Manufact":model.BoilerManufacturer})
        if model.CHPequip != None: equipe.update({"Model":model.CHPequip})
        equipe.update({"EquipType":getEquipmentType("CHP",model.CHPequip)})
        equipe.update({"NumEquipUnits":1})
        if model.CHPequip != None: equipe.update({"EquipTypeFromDB":model.CHPequip})
        if model.DBCHP_ID != None: equipe.update({"EquipIDFromDB":model.DBCHP_ID})
        equipe.update({"DBFuel_id":1})  #use Natural Gas as default -> should later on be adjusted to type of equipment

#        if model.CHPTurnKeyPrice is not None: equipe.update({"TurnKeyPrice":modelBoilerTurnKeyPrice})
#        else:
        logDebug("ModuleCHP: turn key price of CHP equipment model %s not specified"%equipe.Model)
        equipe.update({"TurnKeyPrice":0.0})
###### E.F. 12/10
        if model.OMRateFix is not None: equipe.update({"OandMfix":model.OMRateFix})
        else:
            logDebug("ModuleCHP: fix costs for O and M of CHP model %s not specified"%equipe.Model)
            equipe.update({"OandMfix":0.0})
        if model.OMRateVar is not None: equipe.update({"OandMvar":model.OMRateVar})
        else:
            logDebug("ModuleCHP: variable costs for O and M of CHP model %s not specified"%equipe.Model)
            equipe.update({"OandMvar":0.0})
######


        Status.SQL.commit()
        logTrack("moduleCHP (setEquipmentFromDB): boiler added:'%s',type:'%s',Pow:'%s',T'%s'"%\
                 ("---",model.CHPequip,model.CHPPt,-1.0))
        self.calculateEnergyFlows(equipe,self.cascadeIndex)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,cascadeIndex):
#------------------------------------------------------------------------------
#   calculates the energy flows in the equipment identified by "cascadeIndex"
#------------------------------------------------------------------------------

        if Status.int.cascadeUpdateLevel < (cascadeIndex - 1):
            logDebug("ModuleCHP (calculateEnergyFlows): cannot calulate without previously updating the previous levels")
            Status.mod.moduleEnergy.runSimulation(last=(cascadeIndex-1))
        Status.int.extendCascadeArrays(cascadeIndex)

        if cascadeIndex > 0 and cascadeIndex <= Status.NEquipe:
            logTrack("ModuleCHP (calculateEnergyFlows): starting (cascade no: %s)"%cascadeIndex)
        else:
            logError("ModuleCHP (calculateEnergyFlows): cannot simulate index %s: out of cascade [%s]"%\
                     (cascadeIndex,Status.NEquipe))
            return
#..............................................................................
# get equipment data from equipment list in SQL

        CHPModel = equipe.Model
        CHPType = equipe.EquipType
        PNom = equipe.HCGPnom
        COPh_nom = equipe.HCGTEfficiency
        COPe = equipe.HCTEEfficiency
        TMax = equipe.TMaxSupply
        EquipmentNo = equipe.EqNo

        if PNom is None:
            PNom = 0.0
            logWarning("ModuleCHP (calculateEnergyFlows): No nominal power specified for equipe no. %s"%\
                 (EquipmentNo))

        if COPe is None:
            COPe = 0.0
            logWarning("ModuleCHP (calculateEnergyFlows): No electrical efficiency specified for equipe no. %s"%\
                 (EquipmentNo))

        if TMax is None:
            TMax = INFINITE
            logDebug("ModuleCHP (calculateEnergyFlows): no Tmax specified for equipe no. %s"%EquipmentNo)
  
        logTrack("ModuleCHP (calculateEnergyFlows): Model = %s Type = %s PNom = %s"%\
                 (CHPModel,CHPType,PNom))

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

        logTrack("ModuleCHP (calculateEnergyFlows): Total energy supplied by equipment %s MWh"%(USHj*Status.EXTRAPOLATE_TO_YEAR))
        logTrack("ModuleCHP (calculateEnergyFlows): Total waste heat input  %s MWh"%(QHXj*Status.EXTRAPOLATE_TO_YEAR))

        Status.int.cascadeUpdateLevel = cascadeIndex

#........................................................................
# Global results (annual energy flows)

        Status.int.USHj[cascadeIndex-1] = USHj*Status.EXTRAPOLATE_TO_YEAR

        if COPh_nom > 0:
            FETFuel_j = USHj*Status.EXTRAPOLATE_TO_YEAR/COPh_nom
            print "ModuelCHP (cEF): converting USH [%s] to FET [%s]"%\
                  (USHj*Status.EXTRAPOLATE_TO_YEAR,FETFuel_j*Status.EXTRAPOLATE_TO_YEAR)
        else:
            FETFuel_j = 0.0
            showWarning("Strange boiler with COP = 0.0")

        FETel_j = - FETFuel_j*COPe #electricity generation by the CHP plant
        
        Status.int.FETFuel_j[cascadeIndex-1] = FETFuel_j
        Status.int.FETel_j[cascadeIndex-1] = FETel_j
        Status.int.HPerYearEq[cascadeIndex-1] = HPerYear*Status.EXTRAPOLATE_TO_YEAR
        
        logMessage("Boiler: eq.no.:%s energy flows [MWh] USH: %s FETFuel: %s FETel: %s QD: %s HPerYear: %s "%\
                   (equipe.EqNo,\
                    USHj*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
                    FETFuel_j*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
                    FETel_j*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
                    QD*Status.EXTRAPOLATE_TO_YEAR/1000.0,\
                    HPerYear*Status.EXTRAPOLATE_TO_YEAR/1000.0))

        self.calculateOM(equipe,USHj*Status.EXTRAPOLATE_TO_YEAR)
        
        return USHj    


#==============================================================================

 
#------------------------------------------------------------------------------
    def designAssistant1(self):
#------------------------------------------------------------------------------
#   auto-design of CHP plant - step 1: pre-selection
#------------------------------------------------------------------------------

#............................................................................................
# getting configuration parameters of DA
        print "moduleCHP starting function 'designAssistant'"

        DATable = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(DATable) > 0:
            DA = DATable[0]
        else:
            logTrack("ModuleCHP (design assistant): WARNING - no DA configuration parameters available")
            return

        if DA.CHPMaintain != None:
            self.Maintain= DA.CHPMaintain
        else:
            self.Maintain = 1

        if DA.CHPHOp!= None:
            self.minHOp = DA.CHPHOp
        else:
            self.minHOp = 2000.0

        if DA.CHPEff != None:
            self.minEff= DA.CHPEff
        else:
            self.minEff = 0.55

        if DA.CHPFuelType != "Natural Gas":
            pass
        
        if self.Maintain == 0:
            for row in self.CHPList:
                self.dummyEqId = row['equipeID']
                self.deleteEquipment(None)

#............................................................................................
# after shifting, the equipment cascade has to be updated, as the modified demand is used
# in the following

        if Status.int.cascadeUpdateLevel < self.NEquipe:
            Status.mod.moduleEnergy.runSimulation()

#............................................................................................
# get maximum temperature for heat demand
            
        self.CHPType = DA.CHPType

        if self.CHPType is None:
            self.CHPType = "CHP engine"
#xxxx here an auto-selection of the type might be foreseen, depending on the demand profile

        if self.CHPType in CHPMAXTEMP.keys():
            self.Tmax = CHPMAXTEMP[self.CHPType]
        else:
            logDebug("ModuleCHP: CHPType %s not found in CHPMAXTEMP"%self.CHPType)
            self.Tmax = 90.0

# demand at cascade-index 1 !!!! CHP by default as base load equipment
        QD_Tmax = copy.deepcopy(Status.int.QD_Tt_mod[0][int(self.Tmax/Status.TemperatureInterval+0.5)])
        QD_Tmax.sort(reverse=True)

        indexMinHOp = (int) (self.minHOp / (Status.TimeStep*Status.EXTRAPOLATE_TO_YEAR))
        indexMinHOp = min(indexMinHOp,Status.Nt-1)

        QDmax = QD_Tmax[indexMinHOp]/Status.TimeStep

#............................................................................................
#   preselect list of equipment that fulfils the criteria

        self.preselection = []

#............................................................................................
# Initial selection: maximum reasonable power for a CHP Equipment
# From the annual Heat demand curve (QDa): calculate the necesary heating capacity (starting value)

        listIndexH = findInListASC(1.4*QDmax,CHPListPNom)
        listIndexL = findInListASC(0.7*QDmax,CHPListPNom)

        if listIndexH < 0:
            showWarning(_("There is no appropriate CHP available in DB for this application")+\
                        _("\n(thermal power approx) %s kW")%QDmax)
            self.preselection = []
        else:
            self.preselection = IDList[max(listIndexL,0):(listIndexH+1)]

#............................................................................................
# Automatic final selection:
#............................................................................................

        nSelected = len(self.preselection)
        if nSelected <= 0: #no equipment could be selected
            return("CANCEL",[])
        
        else:   #several options possible -> manual or automatic final selection

            if Status.UserInteractionLevel == "interactive" or Status.UserInteractionLevel == "semi-automatic":

                    return("MANUAL",self.preselection)  #"MANUAL" indicates to panel to open the dialog

            else:   
                listIndex = findInListASC(QDmax,CHPListPNom)
                self.preselection = [IDList[listIndex]]
                return ("AUTOMATIC",self.preselection)
                                             
#------------------------------------------------------------------------------
    def designAssistant2(self,modelID):
#------------------------------------------------------------------------------
##        Design Assistant 2 - final selection
#------------------------------------------------------------------------------

        if (modelID == None or modelID < 0):
            logTrack("ModuleCHP (DA2): user cancelled the selection of the heat pump")
            self.deleteEquipment(None)   

        else:                        
            self.setEquipmentFromDB(self.equipe,modelID) #add selected equipment to the equipment list #SD change 30/04.2008
            logTrack("ModuleCHP (DA2): heat pump added. model no: %s"%modelID)
        
#------------------------------------------------------------------------------
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
    print "Testing ModuleCHP"
    import einstein.GUI.pSQL as pSQL, MySQLdb
    from einstein.modules.interfaces import *
    from einstein.modules.energy.moduleEnergy import *    

    stat = Status("testModuleCHP")

    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    
    Status.PId = 2
    Status.ANo = 0

    interf = Interfaces()

    Status.int = Interfaces()
    
    keys = ["CHP Table","CHP Plot","CHP UserDef"]
    mod = ModuleCHP(keys)
    equipe = mod.addEquipmentDummy()
    mod.calculateEnergyFlows(equipe,mod.cascadeIndex)
                    

#    mod.designAssistant1()
#    mod.designAssistant2(12)
