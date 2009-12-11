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
#	HEAT PUMP - Module for heat pump selection and calculation
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Module for heat pump selection and calculation
#
#==============================================================================
#
#	EINSTEIN Version No.: 1.0
#	Created by: 	    Stoyan Danov, Hans Schweiger
#                           31/01/2008 - 12/10/2008
#
#       Update No. 001
#
#	Since Version 1.0 revised by:
#                           Hans Schweiger          21/10/2008
#
#       Changes to previous version:
#       21/10/2008: HS  TMaxSupply added in setEquipmentData
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
from einstein.modules.fluids import *
from einstein.modules.constants import *
from einstein.modules.messageLogger import *
from einstein.GUI.GUITools import *


#from einstein.modules.modules import Modules

EPS_COP = 1.e-4
EPS_TEMP = 1.e-4
EPS = 1.e-10
HPTDROP = 5

POWERRANGE = 0.8    #   range of power for heat pump preselection: 1 = only maximum possible power

class ModuleHP():

    equipments = None
    cascadeIndex = None
    
#------------------------------------------------------------------------------
    def __init__(self,keys):
#------------------------------------------------------------------------------
#..............................................................................
# getting list of equipment in SQL

#XXX HS2008-04-02: keys copied here similar to BB. doesn't do anything for the moment
        self.keys = keys

        self.DB = Status.DB
        self.sql = Status.SQL
    
        self.setupid = Status.SetUpId

        self.neweqs = 0 #new equips added

#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       initialisation of the panel
#------------------------------------------------------------------------------

        logTrack("ModuleHP (initPanel): starting")
        self.getUserDefinedParamHP() #returns to the GUI the default user-defined data to be shown in HP panel

        if Status.int.cascadeUpdateLevel < 0:
            Status.int.initCascadeArrays(0)

    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------
               
#............................................................................................
# 0. Prepare the system information necessary for starting work

        (HPList,HPTableDataList) = self.screenEquipments()

        logTrack("ModuleHP (updatePanel): cascade index %s update level %s"%\
                 (self.cascadeIndex,Status.int.cascadeUpdateLevel))

        if Status.int.cascadeUpdateLevel < self.cascadeIndex:
            logTrack("ModuleHP: calling run simulation")
            Status.mod.moduleEnergy.runSimulation(last=self.cascadeIndex)

#............................................................................................
# 1. List of equipments

        matrix = []
        for row in HPTableDataList:
            matrix.append(row)

        data = array(matrix)

        Status.int.setGraphicsData('HP Table',data)

#............................................................................................
# 2. XY Plot

        try:
            iTmax = Status.NT/2
            QD_plot = []
            QDres_plot = []
            QA_plot = []
            QAres_plot = []
            for i in range(iTmax):
                QD_plot.append(Status.int.QD_T_mod[self.cascadeIndex-1][i]/1000.0)
                QA_plot.append(Status.int.QA_T_mod[self.cascadeIndex-1][i]/1000.0)
                QDres_plot.append(Status.int.QD_T_mod[self.cascadeIndex][i]/1000.0)
                QAres_plot.append(Status.int.QA_T_mod[self.cascadeIndex][i]/1000.0)

            Status.int.setGraphicsData('HP Plot',
                                       [Status.int.T[0:(Status.NT/2)],
                                        QD_plot,
                                        QA_plot,
                                        QDres_plot,
                                        QAres_plot])
        except:
            logDebug("ModuleHP (updatePanel): error trying to send graphics data")

#............................................................................................
# 3. Configuration design assistant

        self.getUserDefinedParamHP() #returns to the GUI the default user-defined data to be shown in HP panel

#............................................................................................
# 4. additional information
        (TPinch,TGap) = self.calcTPinchAndTGap()
        info = []
        info.append(TPinch)  #first value to be displayed
        info.append(TGap)  #second value to be displayed

        Status.int.setGraphicsData('HP Info',info)

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
    def getUserDefinedParamHP(self):
#------------------------------------------------------------------------------
#   gets the user defined data from UHeatPump and stores it to interfaces to be shown in HP panel
#------------------------------------------------------------------------------

        uHProws = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]

        if len(uHProws) == 0:
#            print 'getUserDefinedParamHP: Status.PId =', Status.PId, 'Status.ANo =', Status.ANo, 'not defined'
#            print 'Error: confusion in PId and ANo'
            Status.int.setGraphicsData('HP Config',[True, 'compression',1500.0,60.0,100.0,-10.0,100.0])            

        else:
            uHP = uHProws[0]
            #returns to the GUI the default user-defined data to be shown in HP panel
            if uHP.UHPMaintain == 1:
                maintainExisting = True
            else:
                maintainExisting = False
            Status.int.setGraphicsData('HP Config',[maintainExisting,uHP.UHPType,uHP.UHPMinHop,uHP.UHPDTMax,
                                                     uHP.UHPmaxT,uHP.UHPminT,uHP.UHPTgenIn])

#------------------------------------------------------------------------------
    def setUserDefinedParamHP(self):
#------------------------------------------------------------------------------

        UDList = Status.int.GData['HP Config']

        uhp = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
        
        if len(uhp)==0:
#            print "ModuleHP(setUserDefinedParamHP): corrupt data base - no entry for uheatpump under current ANo"
            dummy = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo} 
            Status.DB.uheatpump.insert(dummy)
            uhp = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
            
        row = uhp[0]

        if UDList[0] == True:
            maintainExisting = 1
        else:
            maintainExisting = 0
        row.UHPMaintain = check(maintainExisting) # to add in UHeatPump
        row.UHPType = check(UDList[1])
        row.UHPMinHop = check(UDList[2])
        row.UHPDTMax = check(UDList[3])
        row.UHPmaxT = check(UDList[4])
        row.UHPminT = check(UDList[5])
        row.UHPTgenIn = check(UDList[6])

        Status.SQL.commit()

#------------------------------------------------------------------------------
    def initUserDefinedParamHP(self):
#------------------------------------------------------------------------------
#   gets the default user defined data for HP from PSetUpData table. Stores them in UHeatPump.
#   to be executed only onece when new alternative is created
#------------------------------------------------------------------------------
        default = Status.DB.psetupdata.PSetUpData_ID[Status.SetUpId][0]
        uheatpump = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]

        uheatpump.UHPType = default.UHPType
        uheatpump.UHPMinHop = default.UHPMinHop
        uheatpump.UHPDTMax = default.UHPDTMax
        uheatpump.UHPmaxT = default.UHPmaxT
        uheatpump.UHPminT = default.UHPminT
        uheatpump.UHPTgenIn = default.UHPTgenIn

        self.sql.commit()
        
##XXX idea aparte:
##en vez de duplicar todas las columnas de la tabla en UHeatPump en PSetUp, no sería mejor crear una convención tipo
##PId = -1 en la tabla UHeatPump mismo = espacio reservado para los default values ????
### La definicion de la sql ahora no permute entrar PId negativo, SD, 28/03/2008, se tiene que cambiar


   
#------------------------------------------------------------------------------
    def screenEquipments(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

#............................................................................................
# 1. get equipment list and cascade tables
                 
        self.equipments = Status.prj.getEquipments()
        self.NEquipe = len(self.equipments)
        Status.int.getEquipmentCascade()

#............................................................................................
# 2. screen for existing heat pumps
                 
        self.HPList = []

        i = 0
        idx = 0
        for row in Status.int.cascade:
            i+=1
            if getEquipmentClass(row["equipeType"]) == "HP":
                self.HPList.append(row)
                idx = i
        self.cascadeIndex = idx #set to 0, if nothing is found !!!
        
        HPTableDataList = []
        for row in Status.int.EquipTableDataList:
#            if row[2] == 'Heat pump' or row[2] == 'HeatPump' or row[2] == 'Heat Pump' or row[2] == 'HP COMP':
            if getEquipmentClass(row[3]) == "HP":
                HPTableDataList.append(row)

        #screen list and substitute None with "not available"
        for i in range(len(HPTableDataList)):
            for j in range(len(HPTableDataList[i])):
                if HPTableDataList[i][j] == None:
                    HPTableDataList[i][j] = 'not available'        

        
        return (self.HPList,HPTableDataList)
        
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def calcTPinchAndTGap(self):
#------------------------------------------------------------------------------
#   calculates the temperature gap and Pinch temperature for the demand
#   seen by this module
#------------------------------------------------------------------------------

        index = max(self.cascadeIndex-1,0)
        iD = firstNonZero(Status.int.QD_T_mod[index])
        iA = lastNonZero(Status.int.QA_T_mod[index])
                 #HS2008-07-06: QD_T changed to QD_T_mod !!!

        TminD = (iD-1)*Status.TemperatureInterval
        TmaxA = (iA+1)*Status.TemperatureInterval

        TPinch = 0.5*(TminD + TmaxA)
        TGap = TminD - TmaxA

        return(TPinch,TGap)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#   AUXILIARY FUNCTIONS FOR MANAGING EQUIPMENT ENTRIES IN SQL
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
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
#        deletes the selected heat pump in the current alternative
#------------------------------------------------------------------------------

        if rowNo == None:   #indicates to delete last added equipment dummy
            HPid = self.dummyEqId
        else:
        #--> delete HP from the equipment list under current alternative #from C&QGenerationHC under ANo
            HPid = self.getEqId(rowNo)
                 
        logTrack("Module HP (delete): id to be deleted = %s"%HPid)

        Status.prj.deleteEquipment(HPid)        

        self.deleteFromCascade(Status.int.cascade, HPid) #actuallise the cascade list

        self.NEquipe -= 1

#------------------------------------------------------------------------------
    def deleteFromCascade(self, cascade, HPid):
#------------------------------------------------------------------------------
        """
        deletes from the actual list casade and re-assigns the CascadeIndex values in CGenerationHC table
        """
#-----------------------------------------------------------------------------

        idx = -1
        new_cascade = cascade
        for i in range(len(new_cascade)):
            if new_cascade[i]['equipeID'] == HPid:
                idx = i

        new_cascade.pop(idx)           

        for i in range(len(new_cascade)): #assign new CascadeIndex in QGenerationHC table
            eq = Status.DB.qgenerationhc.QGenerationHC_ID[new_cascade[i]['equipeID']][0] #SD change 30/04.2008
            eq.CascadeIndex = i+1 #SD change 30/04.2008
#            print '\n new_CascadeIndex', eq.CascadeIndex #SD change 30/04.2008
            
        self.sql.commit() #confirm storing to sql of new CascadeIndex #to be activated, SD

        equipments = Status.prj.getEquipments()

        Status.int.deleteCascadeArrays(self.NEquipe)


#------------------------------------------------------------------------------
    def addEquipmentDummy(self):
#------------------------------------------------------------------------------
#       adds a new dummy equipment to the equipment list and returns the
#       position in the cascade 
#------------------------------------------------------------------------------

        self.cascadeIndex = self.NEquipe + 1
        EqNo = self.NEquipe + 1

        self.neweqs += 1 #No of last equip added
        NewEquipmentName = "New heat pump %s"%(self.neweqs)
        
        logDebug("ModuleHP (addEquipmentDummy): take care. present version works well only for compression heat pumps !!!")
        
        self.equipe = Status.prj.addEquipmentDummy()
        self.dummyEqId = self.equipe.QGenerationHC_ID
        
        equipeData = {"Equipment":NewEquipmentName,"EquipType":"compression heat pump"}
        self.equipe.update(equipeData)

        Status.SQL.commit()

        Status.int.getEquipmentCascade()
        Status.int.addCascadeArrays()

        self.equipments = Status.prj.getEquipments()

        return(self.equipe) 

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def setEquipmentFromDB(self,equipe,modelID): #SD change 30/04.2008
#------------------------------------------------------------------------------
#   takes an equipment from the data base and stores it under a given Id in
#   the equipment data base
#------------------------------------------------------------------------------

        model = self.DB.dbheatpump.DBHeatPump_ID[modelID][0]

#        print "ModuleHP(setEquipmentFromDB): updating parameters in SQL"        
        if model.HPHeatCap != None: equipe.update({"HCGPnom":model.HPHeatCap})
        if model.HPHeatCOP != None: equipe.update({"HCGTEfficiency":model.HPHeatCOP}) #changed from HPThHeatCOP,SD
        if model.HPManufacturer != None: equipe.update({"Manufact":model.HPManufacturer})
        if model.HPYearUpdate != None: equipe.update({"YearManufact":model.HPYearUpdate})
        if model.HPModel != None: equipe.update({"Model":model.HPModel})
        equipe.update({"EquipType":getEquipmentType("HP",model.HPType)})
        equipe.update({"NumEquipUnits":1})
        if model.DBFuel_id != None: equipe.update({"DBFuel_id":model.DBFuel_id})
        if model.HPFuelConsum != None: equipe.update({"FuelConsum":model.HPFuelConsum})
        if model.HPUnitsFuelConsum != None: equipe.update({"UnitsFuelConsum":model.HPUnitsFuelConsum})
        if model.HPElectConsum != None: equipe.update({"ElectriConsum":model.HPElectConsum})
        if model.HPExHeatCOP != None:
            equipe.update({"HPExHeatCOP":model.HPExHeatCOP})
        else:
            COP = model.HPHeatCOP
            COPth = model.HPThHeatCOP
            if COP is not None and COPth is not None:
                if COP <= COPth and COPth > 0:
                    COPex = COP/COPth
                    logMessage("Exergetic efficiency of HP %s calculated to %s"% \
                               (equipe.Model,COPex))
                    equipe.update({"HPExHeatCOP":COPex})
                else:
                    logWarning("Error in efficiency data of the heat pump %s"%equipe.Model)
                
        equipe.update({"IsSelectedFromDB":1})
        equipe.update({"DatabaseNameSelection":"DBHeatPump"})
        if model.HPType != None: equipe.update({"EquipTypeFromDB":model.HPType})
        equipe.update({"EquipIDFromDB":model.DBHeatPump_ID})
        if model.HPCondTmax != None: equipe.update({"TMaxSupply":model.HPCondTmax})
        
#HS 2008-10-25: equipment parameters that are set defined by default if not specified
        
        equipe.FlowExhaustGas = 0.0
        equipe.TExhaustGas = 0.0

        if model.HPTurnKeyPrice is not None: equipe.update({"TurnKeyPrice":model.HPTurnKeyPrice})
        else:
            logDebug("ModuleHP: turn key price of heat pump model %s not specified"%equipe.Model)
            equipe.update({"TurnKeyPrice":0.0})

###### E.F. 12/10
        if model.HPOandMfix is not None: equipe.update({"OandMfix":model.HPOandMfix})
        else:
            logDebug("ModuleHP: fix costs for O and M of heat pump model %s not specified"%equipe.Model)
            equipe.update({"OandMfix":0.0})
        if model.HPOandMvar is not None: equipe.update({"OandMvar":model.HPOandMvar})
        else:
            logDebug("ModuleHP: variable costs for O and M of heat pump model %s not specified"%equipe.Model)
            equipe.update({"OandMvar":0.0})
######
            
        Status.SQL.commit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def getHPList(self,HPTypeUD):
#------------------------------------------------------------------------------
#   Create the lists (ascending order for HPHeatCap) which are needed for
#   the selection of a heat pump and the calculateEnergyFlows()
#------------------------------------------------------------------------------

        HPList = []
        HPListPNom = []
        sqlQuery = "HPType LIKE '%s' ORDER BY HPHeatCap ASC"%(HPTypeUD)
        subset = self.DB.dbheatpump.sql_select(sqlQuery) #this is a list of rows (dictionaries) in DBHeatPump
        DTMax = 0
        TCondMax = 0
        for i in range(len(subset)):
            HPList.append(subset[i].DBHeatPump_ID)
            HPListPNom.append(subset[i].HPHeatCap)
            DTMax = max(DTMax,subset[i].HPLimDT)
            TCondMax = max(TCondMax,subset[i].HPCondTmax)

#        print "ModuleHP (getHPList): ",HPList,HPListPNom,DTMax,TCondMax
        return (HPList,HPListPNom,DTMax,TCondMax)

#----------------------------------------------------------------------------
    def calculateCOPh_Carnot(self,Th,Tc,Tg = None):
#----------------------------------------------------------------------------
#   Calculates the theoretical Carnot COP.
#XXX Pending the application of temperature corrections for secondary fluids !!! -> corrected when argument passed:+-HPTDROP
#----------------------------------------------------------------------------

        if (Th<=Tc):
            COPh_Carnot = INFINITE
#            print 'pass1'
            
        elif Tg==None:                             # compression heat pumps
            COPh_Carnot = (Th+KELVIN)/(Th-Tc)
#            print "ModuleHP (calculateCOPh_Carnot): Th, Tc, COPh_Carnot: ",Th,Tc,COPh_Carnot
                
        else:                                       # absorption heat pumps
            COPh_Carnot = ((Tc+KELVIN)*(Tg-Th))/((Tg+KELVIN)*(Th-Tc))+1

#        print 'ModuleHP (calculateCOPh_Carnot): ',COPh_Carnot
        return COPh_Carnot

#------------------------------------------------------------------------------
    def getTMinD(self,Q_T):
#------------------------------------------------------------------------------
#   Looks for the minimum temperature in heat demand
#------------------------------------------------------------------------------
        iT = max(firstNonZero(Q_T) - 1,0)      #find the index, SD: -1: assume linear change in the last interval,06/05/2008
        return(Status.int.T[iT])        #find the T corresponding to index
        
#------------------------------------------------------------------------------
    def getTMaxA(self,Q_T):
#------------------------------------------------------------------------------
#   Looks for the minimum temperature in heat demand
#------------------------------------------------------------------------------
        iT = min(lastNonZero(Q_T) + 1,Status.NT+1)       #find the index, SD: +1: assume linear change in the last interval,06/05/2008
        return(Status.int.T[iT])        #find the T corresponding to index
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def designAssistant1(self):
#------------------------------------------------------------------------------
#
#        Design Assistant 1 - Function for selection of heat pump and calculation of the heat flows in it (annual, hourly) on base of
#        temperature and time dependent heat demand and availability curves. 
#------------------------------------------------------------------------------
            
        logTrack("ModuleHP (designAssistant1): starting")

#............................................................................................
#   add a new equipment as space holder to the equipment list
#   and move it to the top of the list

        equipe = self.addEquipmentDummy()
        equipeID = equipe.QGenerationHC_ID  #SD change 30/04.2008
        logTrack("ModuleHP (DA1): equipe before moving - %s %s %s"%\
              (equipe.Equipment,equipe.EqNo,equipe.CascadeIndex))
        
        Status.mod.moduleHC.cascadeMoveToTop(equipe.CascadeIndex)

        equipe = Status.prj.getEquipe(equipeID)
        logTrack("ModuleHP (DA1): equipe after moving - %s %s %s"%\
              (equipe.Equipment,equipe.EqNo,equipe.CascadeIndex))
        self.cascadeIndex = equipe.CascadeIndex

#............................................................................................
#   now prepare the 

        if Status.int.cascadeUpdateLevel < (self.cascadeIndex - 1):
            logDebug("ModuleHP (DA1): calling design assistant w/o having cascade updated")
            Status.mod.moduleEnergy.runSimulation(last=self.cascadeIndex - 1)

#............................................................................................
# get configuration of design assistant and do basic checking

        uTable = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(uTable) > 0:
            DA = uTable[0]
            DA_UHPType = DA.UHPType
            if DA_UHPType is None:
                DA_UHPType = HPTYPES[0]

            DA_UHPMinHop = DA.UHPMinHop
            if DA_UHPMinHop is None or DA_UHPMinHop <= 0.0:
                DA_UHPMinHop = 1500.0

            DA_UHPmaxT = DA.UHPmaxT
            if DA_UHPmaxT is None or DA_UHPmaxT <= 0.0:
                DA_UHPmaxT = 100.0
        else:
            logDebug("ModuleHP (DA1): no u-Table found")
            return("CANCEL",[])
        
        if DA.UHPMinHop > YEAR:        #check of user input
            logWarning('ModuleHP (DA1): Required working hours are greater than the hours of the year!')               
            DA_UHPType = HPTYPES[0]
            DA_UHPMinHop = 1500.0
            DA_UHPmaxT = 100.0
                       
        (HPList,HPListPNom,DTMaxInList,TCondMaxInList) = self.getHPList(DA_UHPType)  #get the sorted list of available heat pumps

#        print "ModuleHP (DA1): HPListPNom = ",HPListPNom
#............................................................................................
#   analyze heat demand for previous checks
        
        TMinD = self.getTMinD(Status.int.QD_T_mod[self.cascadeIndex-1])
        TMaxA = self.getTMaxA(Status.int.QA_T_mod[self.cascadeIndex-1])
        DTMin = TMinD - TMaxA   #minimum necessary temperature lift

#............................................................................................
#   preselect list of equipment that fulfils the criteria

        self.preselection = []

        if DTMin > DTMaxInList:
            logWarning("ModuleHP (DA1): Heat pump application impossible. "+\
                     "Temperature lift from QD-QA %s greater than limit value %s!"%(DTMin,DTMaxInList))                

        else:  #in the case heat pump application is possible: calculate all this...

            if DA_UHPmaxT > TCondMaxInList:
                logTrack('ModuleHP (designAssistant1): UHPmaxT = %s is higher than TCondMaxInList = %s'%\
                         (DA_UHPmaxT,TCondMaxInList))
                logTrack('ModuleHP (designAssistant1): The value of TCondMaxInList = %s will be used as initial estimate of Th0'%\
                         TCondMaxInList)
            
            #Start temperature for calculation Th0 = to the user-defined temperature
            Th0 = min(DA_UHPmaxT,TCondMaxInList)

            if Th0 is None:
                logDebug("ModuleHP (designAssistant1): WARNING -> Th0 = None was obtained")
                Th0 = 100.0
            
#............................................................................................
# Initial selection: maximum reasonable power for a heat pump
# From the annual Heat demand curve (QDa): calculate the necesary heating capacity (starting value)

            Qh0 = interpolateList(Th0/Status.TemperatureInterval,Status.int.QD_T_mod[self.cascadeIndex-1]) #calculates the annual energy demand for the Th_o from QDa
            dotQh0 = Qh0/DA_UHPMinHop #the initial heat capacity of the heat pump is obtained dividing by the hours of year #SD: *10 deleted,06/05/2008
            
            listIndex = findInListASC(dotQh0,HPListPNom)

            if listIndex < 0:
                logError('err005: Warning: There is no heat pump available in DB for this application')

#............................................................................................
# Check appropriateness for several heat pumps (preselection)

            PNomMax = 0                 #maximum possible heat pump capacity for desired operating hours
            while listIndex >= 0:       #decrease gradually until HOp >= MinHOp

                modelID = HPList[listIndex] #a row in the DBHeatPump corresponding to j
                                    
                self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list #SD change 30/04.2008

#                print "ModuleHP (DA1): equipe ID %s PNom %s"%\
#                      (modelID,equipe.HCGPnom)
                USHj = self.calculateEnergyFlows(equipe,self.cascadeIndex) #SD change 30/04.2008
                HOp = USHj/equipe.HCGPnom
#                print "ModuleHP (DA1): USH %s HOp %s"%\
#                      (USHj,HOp)
               
                if HOp >= DA_UHPMinHop:    #correction factor for simulations < 1 year
                    self.preselection.append(modelID)
                    PNomMax = max(PNomMax,equipe.HCGPnom)
                if equipe.HCGPnom < POWERRANGE*PNomMax:
                    break
                
                listIndex -= 1  #Select next smaller heat pump

        logTrack("ModuleHP (designAssistant1): preselected equipment: %s"%str(self.preselection))

#............................................................................................
# Automatic final selection:
#............................................................................................

        nSelected = len(self.preselection)
#        print "ModuleHP (designAssistant1): return to GUI for manual selection "
        if nSelected <= 0: #no equipment could be selected
            return("CANCEL",[])
        
        else:   #several options possible -> manual or automatic final selection

            if Status.UserInteractionLevel == "interactive" or Status.UserInteractionLevel == "semi-automatic":

                    return("MANUAL",self.preselection)  #"MANUAL" indicates to panel to open the dialog

            else:   
                maxCOP = 0
                for listIndex in self.preselection:
                    modelID = HPList[listIndex]
                    model = self.DB.dbheatpump.DBHeatPump_ID[modelID][0]
                    if (model.HPHeatCOP > maxCOP):
                        bestModelID = modelID
                        maxCOP = model.HPHeatCOP
                self.preselection = [bestModelID]
                return ("AUTOMATIC",self.preselection)
                                             
#------------------------------------------------------------------------------
    def designAssistant2(self,modelID):
#------------------------------------------------------------------------------
#
#        Design Assistant 2 - 
#------------------------------------------------------------------------------

        if (modelID == None or modelID < 0):
            logTrack("ModuleHP (DA2): user cancelled the selection of the heat pump")
            self.deleteEquipment(None)   

        else:                        
            self.setEquipmentFromDB(self.equipe,modelID) #add selected equipment to the equipment list #SD change 30/04.2008
            logTrack("ModuleHP (DA2): heat pump added. model no: %s"%modelID)
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,cascadeIndex): #SD change 30/04.2008
#------------------------------------------------------------------------------
#
# updates the energy flows in the newly added heat pump
#       
#------------------------------------------------------------------------------

        if Status.int.cascadeUpdateLevel < (cascadeIndex - 1):
            logDebug("ModuleHP (calculateEnergyFlows): cannot calulate without previously updating the previous levels")
            Status.mod.moduleEnergy.runSimulation(last=(cascadeIndex-1))
        Status.int.extendCascadeArrays(cascadeIndex)

        if cascadeIndex > 0 and cascadeIndex <= Status.NEquipe:
            logTrack("ModuleHP (calculateEnergyFlows): starting (cascade no: %s)"%cascadeIndex)
        else:
            logError("ModuleHP (calculateEnergyFlows): cannot simulate index %s: out of cascade [%s]"%\
                     (cascadeIndex,Status.NEquipe))
            return

#..............................................................................
# get equipment data from equipment list in SQL

        HPModel = equipe.Model
        HPType = equipe.EquipType
        PNom = equipe.HCGPnom
        TMax = equipe.TMaxSupply
        if TMax is None:
            TMax = 90.0
            logWarning("ModuleHP (calculateEnergyFlows): no TMax defined in HP data")
        DTMax = 60.0
        TMin = 0.0 + HPTDROP
### HERE HPLimDT and HPEvapTmin should be copied from the heat pump table
        
        if PNom is None:
            logError("ModuleHP (calculateEnergyFlows): nominal power not defined")
            PNom = 0.0
            
        COPh_nom = equipe.HCGTEfficiency

        if equipe.HPExHeatCOP is None or 'NULL': #SD change 30/04.2008
            COPex = 0.3
        else:
            COPex = equipe.HPExHeatCOP #SD change 30/04.2008

        Tg = None

        EquipmentNo = equipe.EqNo

#..............................................................................
# get demand data for CascadeIndex/EquipmentNo from Interfaces
# and create arrays for storing heat flow in equipment

        QD_Tt = copy.deepcopy(Status.int.QD_Tt_mod[cascadeIndex-1])
        QA_Tt = copy.deepcopy(Status.int.QA_Tt_mod[cascadeIndex-1])
        
        USHj_Tt = Status.int.createQ_Tt()
        USHj_t = Status.int.createQ_t()
        USHj_t_rem = USHj_t
        USHj_T = Status.int.createQ_T()
        
        QHXj_Tt = Status.int.createQ_Tt()
        QHXj_t = Status.int.createQ_t()
        QHXj_t_rem = QHXj_t
        QHXj_T = Status.int.createQ_T()

        QWHj_Tt = Status.int.createQ_Tt()
        QWHj_T = Status.int.createQ_T()


#..............................................................................
# Start hourly loop

        USHj = 0
        QHXj = 0
        QWHj = 0

        HPerYear = 0

        FETel_j = 0

        COPMin = 3.0    # This is the objective for design of HP power
                        # -> not MAXIMUM technically possible energy,
                        # but maximum energy at a reasonable COP
                        # criterion could be optimised ... e.g. if 80% of the energy
                        # delivered rises the COP to 4.0, better use this ?
                        # => minimise  E = Q_HP/COP_HP + (Q_total - QHP)/COP_backup_system
                        # -> dE/dQ_HP = (1/COP_HP - 1/COP_backup) - (dCOP/dQ_HP) * Q_HP/COP_HP**2

        for it in range(Status.Nt):

            if  QD_Tt[Status.NT+1][it] < EPS or QA_Tt[0][it] < EPS: #no demand or no availability
                Tc_i=0.0; COPh_i=0.0; COPht_i=0.0;
                dotQh_i=0.0; dotQw_i=0.0; dotQc_i=0.0
#..............................................................................
# create demand and availability profile for present time step

            else:
                QD_T = []
                QA_T = []
                
                for iT in range(Status.NT+2):
                    QD_T.append(QD_Tt[iT][it])
                    QA_T.append(QA_Tt[iT][it])

#                print "QD(t)",QD_T
#                print "QA(t)",QA_T

#..............................................................................
# start estimates for Th,Tc and COP

                dQMax = PNom*Status.TimeStep

                Th_max = min(interpolateTable(dQMax,QD_T,Status.int.T),TMax)
                dotQ_max = min(interpolateTable(TMax,Status.int.T,QD_T),dQMax/Status.TimeStep)
                
                Th_i = Th_max
                Tc_i = max(interpolateTable(0.8*dQMax,QA_T,Status.int.T),Th_i - DTMax)
                Tc_i = max(Tc_i,TMin)
                            
                COPh_i = COPex*self.calculateCOPh_Carnot(Th_i + HPTDROP,Tc_i - HPTDROP,Tg)

                alpha = 0.1 #(subrelaxation coefficient)

                nits = 0

                COPh0_i = INFINITE; Tc0_i = Tc_i + INFINITE

                dotQh_i = dotQ_max
                dotQh_i2 = dotQ_max
                
                while fabs(COPh_i - COPh0_i) > EPS_COP or fabs(Tc_i - Tc0_i) > EPS_TEMP: 
        
                    COPh0_i = COPh_i;
                    Tc0_i = Tc_i 
                                    
                    dotQw_i = (dotQh_i/COPh_i)              #heat pump input power (mechanical or thermal)
                    dotQc_i = dotQh_i - dotQw_i             #heat pump cooling power

                    Th_i = interpolateTable(dotQh_i*Status.TimeStep,QD_T,Status.int.T)
                    Tc_i = interpolateTable(dotQc_i*Status.TimeStep,QA_T,Status.int.T)

                    dotQh_i *= min(max(0.95,1 + alpha*(COPh_i - COPMin)),1.05)

                    if (Th_i - Tc_i) > DTMax or Th_i > TMax or Tc_i < TMin:
                        dotQh_i *= 0.9

                    COPh_i = COPex*self.calculateCOPh_Carnot(Th_i+HPTDROP,Tc_i-HPTDROP,Tg)
                    COPh_i = min(COPh_i,10.0)               #practical limit for COP at small temp. lift

                    dotQh_i = min(dotQh_i,dotQ_max)         #limit to maximum nominal power and maximum demand at TMax

#                    print "HP:",it,COPh_i,dotQh_i,dotQc_i,dotQw_i,"Th",Th_i,"Tc",Tc_i
                    nits +=1
                    if nits > 30:
                        break


#..............................................................................

            
            USHj_t[it] = dotQh_i*Status.TimeStep
            QHXj_t[it] = dotQc_i*Status.TimeStep
            FETel_j += dotQw_i * Status.TimeStep
#            print "HP:",it,FETel_j,dotQh_i,dotQc_i,dotQw_i

            if dotQh_i > 0:
                HPerYear += Status.TimeStep

            USHj += USHj_t[it]
            QHXj += QHXj_t[it]
             
#..............................................................................
# temperature resolution of delivered and consumed heat
# => at the moment this is done by supplying heat to the lowest temperature
# level where there is a demand, and consuming waste heat at the highest level
# this is optimum for the single equipment, but not for the system !!!
            
            for iT in range(Status.NT+2):   #+1 = the > 400 ºC case
                USHj_Tt[iT][it] = min(QD_Tt[iT][it],USHj_t[it])     #from low to high T
                QD_Tt[iT][it] -= USHj_Tt[iT][it]

            for iT in range((Status.NT+1),-1,-1):
                QHXj_Tt[iT][it] = min(QA_Tt[iT][it],QHXj_t[it])
                QA_Tt[iT][it] -= QHXj_Tt[iT][it]

#..............................................................................
# End of year reached. Store results in interfaces

        Status.int.QD_Tt_mod[cascadeIndex] = QD_Tt
        Status.int.QD_T_mod[cascadeIndex] = Status.int.calcQ_T(QD_Tt)
        Status.int.QA_Tt_mod[cascadeIndex] = QA_Tt
        Status.int.QA_T_mod[cascadeIndex] = Status.int.calcQ_T(QA_Tt)

        Status.int.USHj_Tt[cascadeIndex-1] = USHj_Tt
        Status.int.USHj_T[cascadeIndex-1] = Status.int.calcQ_T(USHj_Tt)
        Status.int.USHj_t[cascadeIndex-1] = copy.deepcopy(USHj_Tt[Status.NT+1])

        Status.int.QHXj_Tt[cascadeIndex-1] = QHXj_Tt
        Status.int.QHXj_T[cascadeIndex-1] = Status.int.calcQ_T(QHXj_Tt)
        Status.int.QHXj_t[cascadeIndex-1] = copy.deepcopy(QHXj_Tt[Status.NT+1])

# waste heat produced by present equipment

        Status.int.QWHj_Tt[cascadeIndex-1] = QWHj_Tt
        Status.int.QWHj_T[cascadeIndex-1] = Status.int.calcQ_T(QWHj_Tt)
        Status.int.QWHj_t[cascadeIndex-1] = copy.deepcopy(QWHj_Tt[Status.NT+1])

#........................................................................

        Status.int.cascadeUpdateLevel = cascadeIndex

#........................................................................
# Global results (annual energy flows)

        USHj *= Status.EXTRAPOLATE_TO_YEAR
        QHXj *= Status.EXTRAPOLATE_TO_YEAR
        QWHj *= Status.EXTRAPOLATE_TO_YEAR
        FETel_j *= Status.EXTRAPOLATE_TO_YEAR
        HPerYear *= Status.EXTRAPOLATE_TO_YEAR

        
        Status.int.USHj[cascadeIndex-1] = USHj
        Status.int.QWHj[cascadeIndex-1] = QWHj   # not considering the latent heat(condensing water)
        Status.int.QHXj[cascadeIndex-1] = QHXj
        
        Status.int.FETFuel_j[cascadeIndex-1] = 0.0
        Status.int.FETel_j[cascadeIndex-1] = FETel_j

        Status.int.HPerYearEq[cascadeIndex-1] = HPerYear

#        logDebug("ModuleHP: eq.no.:%s USH: %s [MWh] FETFuel: %s [MWh] FETel: %s [MWh] HPerYear: %s [h]"%\
#                   (equipe.EqNo,\
#                    USHj/1000.0,\
#                    0.0,\
#                    FETel_j/1000.0,\
#                    HPerYear))
                   
        self.calculateOM(equipe,USHj)
        
        return USHj   
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
    print "Testing ModuleHP"
    import einstein.GUI.pSQL as pSQL, MySQLdb
    from einstein.modules.interfaces import *
    from einstein.modules.energy.moduleEnergy import *
    stat = Status("testModuleHP")

    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    
    Status.PId = 2
    Status.ANo = 0
    Status.SetUpId = 1 #this is PSetUpData_ID

##    HPid = 31
    
    interf = Interfaces()

    Status.int = Interfaces()

#    modE = ModuleEnergy()
#    modE.runSimulation()
    keys = ["HP Table","HP Plot","HP UserDef"]
    mod = ModuleHP(keys)
##    mod.updatePanel()
    mod.initPanel()
##    mod.calcTPinchAndTGap()
##    equipe = mod.addEquipmentDummy() #SD change 30/04.2008
##    mod.setEquipmentFromDB(equipe,HPid) #SD change 30/04.2008
##    mod.designAssistant1()
##    mod.designAssistant2(12)

##    Interfaces.setGraphicsData(interf,'HP Config',[99., 'HP COMP',99.,99.,99.,99.,99.])
##    mod.setUserDefinedParamHP()

    # Step 1 design assistant: gets a preselected list of possible heat pumps

##    (mode,HPList) = mod.designAssistant1()
        
#..............................................................................
# In interactive mode open DB Edidor Heat pump and select manually

    print 'Mode of selection:', mode

    if (mode == "MANUAL"):

        print 'Select heat pump from preselected list' # title for the dialogs
        print 'preselected HPList =', HPList

        if len(HPList) > 0:
            HPId = HPList[0]
        else:
            HPId = -1
            print "PanelHP: no HP selected after DA1 -> check whether this works"

    elif (mode == "AUTOMATIC"):
        HPId = HPList[0]    #in automatic mode just take first in the list

    elif (mode == "CANCEL"):
        HPId = -1 #make designAssistant2 to understand that
    else:
        print "PanelHP (DesignAssistant-Button): erroneous panel mode: ",mode

##..............................................................................
## Step 2 design assistant: add selected equipment to the list and update display

    print 'Selected HPId =', HPId
    
    mod.designAssistant2(HPId)

#==============================================================================
