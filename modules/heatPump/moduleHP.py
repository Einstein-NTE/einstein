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
#       Draft version
#
#==============================================================================
#
#	Version No.: 0.20
#	Created by: 	    Stoyan Danov	    31/01/2008
#	Revised by:         Hans Schweiger          22/03/2008
#                           Stoyan Danov            27/03/2008
#                           Stoyan Danov            01/04/2008
#                           Hans Schweiger          02/04/2008
#                           Hans Schweiger          03/04/2008
#                           Stoyan Danov            03/04/2008
#                           Stoyan Danov            04/04/2008
#                           Hans Schweiger          07/04/2008
#                           Stoyan Danov            09/04/2008
#                           Stoyan Danov            10/04/2008
#                           Hans Schweiger          13/04/2008
#                           Stoyan Danov            16/04/2008
#                           Hans Schweiger          18/04/2008
#                           Stoyan Danov            18/04/2008
#                           Stoyan Danov            22/04/2008
#                           Stoyan Danov            24/04/2008
#                           Hans Schweiger          29/04/2008
#                           Stoyan Danov            30/04/2008
#                           Hans Schweiger          30/04/2008
#   
#
#       Changes to previous version:
#       22/03/2008 general restructuring and clean-up
#       27/03/2008 screenEquipments(), initPanel(),initUserDefinedParamHP(), getUserDefinedParamHP()
#       01/04/2008 deleteE() - to be finished
#       02/04/2008  __init__: connnetion to sql/DB corrected
#                   initPanel: adaptation to new panel structure
#       03/04/2008 receives moduleEnergy from Modules
#       03/04/2008 SD: addEquipmentDummy, setEquipmentFromDB
#       04/04/2008 SD: initPanel - graphics to interfaces, screenEquipments add:if..or..or
#       07/04/2008 HS: adaptación init_panel / update_panel
#       09/04/2008 SD: screenEquipments, updatePanel: changes HPList-HPTableDataList - data shown in table, setEquipmentFromDB: new adds
#       10/04/2008 SD: setEquipmentFromDB - new parameters added (the commented are still missing in sql, to be added)
#       10/04/2008 SD: def setUserDefinedParamHP() - writes the user-defined parameters in UheatPump
#       13/04/2008 HS: getEqId added.
#                      deleteEquipment: rowNo as input instead of Id.
#                      cascadeIndex -> unified from 1...N
#       16/04/2008 SD: deleteFromCascade: activated sql.commit()
#                      designAssistant1: control (in Automatic preselection: if self.preselection ==[]: delete dummy equip added)
#       18/04/2008 HS/SD: Cancel mode passed to panel in design assitant 1
#                      changes in deleteEquipment + addEquipmentDummy (temporary
#                       storing of dummyEqId for posterior undo
#                      changes in DA1 (selection of panel mode) and DA2 (delete of dummy)
#                      introduction of default Equipment and HP Types in CONSTANTS
#                      use of functions getEquipmentClass and getEquipmentSubClass (defined in constants.py)
#                      some unused functions deleted (housekeeping)
#                      interfaces - instance imported from Status
#       18/04/2008 SD: getUserDefinedParamHP: control query added, avoid reference to empty list member
#       22/04/2008 SD: define: calcTPinchAndTGap() and call it in updatePanel() - fills HP Info fields in panel
#       24/04/2008 SD: screenEquipment(): changes in HPTableDataList - table data shown in panel
#                       setEquipmentFromDB(): activate updates, more controls
#                       calculateEnergyFlows(): assignment of exergetic COP from DB
#       29/04/2008 HS: call to initPanel and updatePanel eliminated in __init__
#       30/04/2008 SD: eliminating reference to C tables and related, functions affected:
#                       deleteEquipment,deleteFromCascade,addEquipmentDummy,setEquipmentFromDB,
#                       designAssistant1,designAssistant2,calculateEnergyFlows
#                   HS: some security featers added (setUserDefined)
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
from einstein.modules.constants import *

#from einstein.modules.modules import Modules

EPS_COP = 1.e-4
EPS_TEMP = 1.e-4
HPTDROP = 5

POWERRANGE = 0.8    #   range of power for heat pump preselection: 1 = only maximum possible power

class ModuleHP():

    equipments = None
    cascadeIndex = None
    
    def __init__(self,keys):
#..............................................................................
# getting list of equipment in SQL

#XXX HS2008-04-02: keys copied here similar to BB. doesn't do anything for the moment
        self.keys = keys

        self.DB = Status.DB
        self.sql = Status.SQL
    
        self.setupid = Status.SetUpId

        self.neweqs = 0 #new equips added
        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        self.equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
        self.NEquipe = len(self.equipments)

#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       initialisation of the panel
#------------------------------------------------------------------------------

        #creates space/lists for storing the modified QD,QA, assigns total D,A in all positions
        Status.int.initCascadeArrays(self.NEquipe) 

        print 'moduleHP (initPanel): cascade Arrays initialised '


        self.getUserDefinedParamHP() #returns to the GUI the default user-defined data to be shown in HP panel

        self.updatePanel()
        print 'moduleHP (initPanel): reached the end '
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------
                
#............................................................................................
# 1. List of equipments

        (HPList,HPTableDataList) = self.screenEquipments()

        matrix = []
        for row in HPTableDataList:
            matrix.append(row)

        data = array(matrix)

        Status.int.setGraphicsData('HP Table',data)

#............................................................................................
# 2. XY Plot

        try:
            Status.int.setGraphicsData('HP Plot',[Status.int.T,
                                                      Status.int.QD_T_mod[self.cascadeIndex],
                                                      Status.int.QA_T_mod[self.cascadeIndex],
                                                      Status.int.QD_T_mod[self.cascadeIndex+1],
                                                      Status.int.QA_T_mod[self.cascadeIndex+1]])
        except:
            pass

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
            print 'getUserDefinedParamHP: Status.PId =', Status.PId, 'Status.ANo =', Status.ANo, 'not defined'
            print 'Error: confusion in PId and ANo'
            maintainExisting = True
            Status.int.setGraphicsData('HP Config',[maintainExisting, 'not available',0.0,0.0,0.0,0.0,0.0])            

        else:
            uHP = uHProws[0]
            #returns to the GUI the default user-defined data to be shown in HP panel
            maintainExisting = True
            Status.int.setGraphicsData('HP Config',[maintainExisting, uHP.UHPType,uHP.UHPMinHop,uHP.UHPDTMax,
                                                     uHP.UHPmaxT,uHP.UHPminT,uHP.UHPTgenIn])

#------------------------------------------------------------------------------
    def setUserDefinedParamHP(self):
#------------------------------------------------------------------------------

        UDList = Status.int.GData['HP Config']

        uhp = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
        
        if len(uhp)==0:
            print "ModuleHP(setUserDefinedParamHP): corrupt data base - no entry for uheatpump under current ANo"
            dummy = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo} 
            Status.DB.uheatpump.insert(dummy)
            uhp = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo] #row in UHeatPump
            
        row = uhp[0]

#        row.MaintainExisting = UDList[0] # to add in UHeatPump
        row.UHPType = UDList[1]
        row.UHPMinHop = UDList[2]
        row.UHPDTMax = UDList[3]
        row.UHPmaxT = UDList[4]
        row.UHPminT = UDList[5]
        row.UHPTgenIn = UDList[6]

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
#------------------------------------------------------------------------------

        Status.int.getEquipmentCascade()
        self.HPList = []
        for row in Status.int.cascade:
            if getEquipmentClass(row["equipeType"]) == "HP":
                self.HPList.append(row)

        HPTableDataList = []
        for row in Status.int.EquipTableDataList:
            if getEquipmentClass(row[3]) == "HP":
                HPTableDataList.append(row)

        #screen list and substitute None with "not available"
        for i in range(len(HPTableDataList)):
            for j in range(len(HPTableDataList[i])):
                if HPTableDataList[i][j] == None:
                    HPTableDataList[i][j] = 'not available'        

        if(len(self.HPList)>0):
            self.cascadeIndex = len(self.HPList) #by default sets selection to last HP in cascade
        else:
            self.cascadeIndex = 0
        return (self.HPList,HPTableDataList)
        
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def calcTPinchAndTGap(self):
#------------------------------------------------------------------------------
        iD = firstNonZero(Status.int.QD_T)

        iA = lastNonZero(Status.int.QA_T)

        TminD = (iD-1)*Status.TemperatureInterval
        TmaxA = (iA+1)*Status.TemperatureInterval

        TPinch = 0.5*(TminD + TmaxA)
        TGap = TminD - TmaxA

        return(TPinch,TGap)

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
        deletes the selected heat pump in the current alternative
        """
#------------------------------------------------------------------------------
        print "deleteEquipment: start"

        if rowNo == None:   #indicates to delete last added equipment dummy
            HPid = self.dummyEqId
        else:
        #--> delete HP from the equipment list under current alternative #from C&QGenerationHC under ANo
            HPid = self.getEqId(rowNo)
            print "Module HP (delete): id to be deleted = ",HPid
        
        eq = self.equipments.QGenerationHC_ID[HPid][0] #select the corresponding rows to HPid in both tables
#        eqC = self.equipmentsC.QGenerationHC_id[HPid][0] #SD change 30/04.2008

        eq.delete() #deletes the rows in both tables
#        eqC.delete() #SD change 30/04.2008
        self.sql.commit()

        self.deleteFromCascade(Status.int.cascade, HPid) #actuallise the cascade list

        self.NEquipe -= 1

#------------------------------------------------------------------------------
    def deleteFromCascade(self, cascade, HPid):
#------------------------------------------------------------------------------
        """
        deletes from the actual list casade and re-assigns the CascadeIndex values in CGenerationHC table
        """
#-----------------------------------------------------------------------------

#        print '\n deleteFromCascade():', 'cascade =', cascade

        idx = -1
        new_cascade = cascade
        for i in range(len(new_cascade)):
            if new_cascade[i]['equipeID'] == HPid:
                idx = i

        new_cascade.pop(idx)           

        for i in range(len(new_cascade)): #assign new CascadeIndex in QGenerationHC table
            eq = self.equipments.QGenerationHC_ID[new_cascade[i]['equipeID']][0] #SD change 30/04.2008
            eq.CascadeIndex = i+1 #SD change 30/04.2008
            print '\n new_CascadeIndex', eq.CascadeIndex #SD change 30/04.2008
            
        self.sql.commit() #confirm storing to sql of new CascadeIndex #to be activated, SD

        print '\n deleteFromCascade():', 'new_cascade =', new_cascade


        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY EqNo ASC"%(Status.PId,Status.ANo)
        equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
##        print '\n \nequipments', equipments

        for i in range(len(equipments)): #assign new EqNo in QGenerationHC table
            equipments[i].EqNo = i+1

        self.sql.commit() #to be activated, SD

        Status.int.deleteCascadeArrays(self.NEquipe)


#------------------------------------------------------------------------------
    def addEquipmentDummy(self):
#------------------------------------------------------------------------------
#       adds a new dummy equipment to the equipment list and returns the
#       position in the cascade 
#------------------------------------------------------------------------------

        print 'moduleHP (addEquipmentDummy): cascade Arrays initialised '
        self.cascadeIndex = self.NEquipe + 1
        EqNo = self.NEquipe + 1
        print 'ModuleHP (addEquipmentDummy): CascadeIndex', self.cascadeIndex
        print 'ModuleHP (addEquipmentDummy): EqNo', EqNo

        self.neweqs += 1 #No of last equip added
        NewEquipmentName = "New heat pump %s"%(self.neweqs)
        
        EqNo = self.NEquipe + 1
        print 'ModuleHP (addEquipmentDummy): CascadeIndex', self.cascadeIndex
        print 'ModuleHP (addEquipmentDummy): EqNo', EqNo
        equipe = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo,"EqNo":EqNo,"Equipment":NewEquipmentName,
                  "EquipType":"HeatPump (specify subtype)","CascadeIndex":self.cascadeIndex} #SD change 30/04.2008
        QGid = self.DB.qgenerationhc.insert(equipe)

        self.dummyEqId = QGid #temporary storage of the equipment ID for undo if necessary
        
        Status.SQL.commit()

        Status.int.getEquipmentCascade()
        Status.int.addCascadeArrays()

        print "ModuleHP (addEquipmentDummy): new equip row created"
        print "ModuleHP (addEquipmentDummy): self.cascadeIndex", self.cascadeIndex
        print "ModuleHP (addEquipmentDummy): dummyEqId", self.dummyEqId

        self.equipe = self.equipments.QGenerationHC_ID[QGid][0]

        return(self.equipe) #SD change 30/04.2008

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def setEquipmentFromDB(self,equipe,modelID): #SD change 30/04.2008
#------------------------------------------------------------------------------
#   takes an equipment from the data base and stores it under a given Id in
#   the equipment data base
#------------------------------------------------------------------------------

        model = self.DB.dbheatpump.DBHeatPump_ID[modelID][0]

        print "ModuleHP(setEquipmentFromDB): updating parameters in SQL"        
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
        if model.HPExHeatCOP != None: equipe.update({"HPExHeatCOP":model.HPExHeatCOP})
        equipe.update({"IsSelectedFromDB":1})
        equipe.update({"DatabaseNameSelection":"DBHeatPump"})
        if model.HPType != None: equipe.update({"EquipTypeFromDB":model.HPType})
        equipe.update({"EquipIDFromDB":model.DBHeatPump_ID})

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

        print "ModuleHP (getHPList): ",HPList,HPListPNom,DTMax,TCondMax
        return (HPList,HPListPNom,DTMax,TCondMax)

#----------------------------------------------------------------------------
    def calculateCOPh_Carnot(self,Th,Tc,Tg = None):
#----------------------------------------------------------------------------
#   Calculates the theoretical Carnot COP.
#XXX Pending the application of temperature corrections for secondary fluids !!! -> corrected when argument passed:+-HPTDROP
#----------------------------------------------------------------------------

        if (Th<=Tc):
            COPh_Carnot = INFINITE
            
        elif Tg==None:                              # compression heat pumps
                COPh_Carnot = (Th+KELVIN)/(Th-Tc)
                print "Th, Tc, COPh_Carnot: ",Th,Tc,COPh_Carnot
                
        else:                                       # absorption heat pumps
            COPh_Carnot = ((Tc+KELVIN)*(Tg-Th))/((Tg+KELVIN)*(Th-Tc))+1

        return COPh_Carnot

#------------------------------------------------------------------------------
    def getTMinD(self,Q_T):
#------------------------------------------------------------------------------
#   Looks for the minimum temperature in heat demand
#------------------------------------------------------------------------------
        iT = firstNonZero(Q_T)      #find the index
        return(Status.int.T[iT])        #find the T corresponding to index
        
#------------------------------------------------------------------------------
    def getTMaxA(self,Q_T):
#------------------------------------------------------------------------------
#   Looks for the minimum temperature in heat demand
#------------------------------------------------------------------------------
        iT = lastNonZero(Q_T)       #find the index
        return(Status.int.T[iT])        #find the T corresponding to index
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def designAssistant1(self):
#------------------------------------------------------------------------------
#
#        Design Assistant 1 - Function for selection of heat pump and calculation of the heat flows in it (annual, hourly) on base of
#        temperature and time dependent heat demand and availability curves. 
#------------------------------------------------------------------------------
        
        try:
            #Define errors: Display warnings in GUI
            err001 = 1 #deactivated at the moment, SD 17/03/2008
            err002 = 2
            err003 = 3
            err004 = 4
            err005 = 5
            print "ModuleHP (designAssistant1): starting"
            
#............................................................................................
# get configuration of design assistant and do basic checking

            DA = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]
            print "ModuleHP (designAssistant1) DA parameters: ",DA
#....
            if DA.UHPMinHop > YEAR:        #check of user input   
                print 'err002: Display warning: Required working hours are greater than the hours of the year!'
#                return err002
                            
            (HPList,HPListPNom,DTMaxInList,TCondMaxInList) = self.getHPList(DA.UHPType)  #get the sorted list of available heat pumps
            print "ModuleHP (designAssistant1) List of heat pumps: ",len(HPList)

#............................................................................................
#   add a new equipment as space holder to the equipment list

#            if (MaintainExistingEquipment == False):
#                deleteAllHeatPumps()

            equipe = self.addEquipmentDummy() #SD change 30/04.2008

#............................................................................................
#   analyze heat demand for previous checks

            TMinD = self.getTMinD(Status.int.QD_T_mod[self.cascadeIndex-1])
            TMaxA = self.getTMaxA(Status.int.QA_T_mod[self.cascadeIndex-1])
            DTMin = TMinD - TMaxA   #minimum necessary temperature lift

            print "ModuleHP (designAssistant1): TMinD,TMaxA,DTMin",TMinD,TMaxA,DTMin

#............................................................................................
#   preselect list of equipment that fulfils the criteria

            self.preselection = []
            
            if DTMin > DTMaxInList:
                print 'err003: Display warning: Heat pump application impossible. Temperature lift from QD-QA greater than limit value'
                print DTMin,DTMaxInList 
#                return err003
                pass
        
            else:  #in the case heat pump application is possible: calculate all this...

                if DA.UHPmaxT > TCondMaxInList:
                    print 'err004: Display warning: User-defined maximum condensing temperature lower than limit temperature for all heat pumps in DB'
                    print DA.UHPmaxT,TCondMaxInList
#                    return err004
                
                #Start temperature for calculation Th0 = to the user-defined temperature
                Th0 = min(DA.UHPmaxT,TCondMaxInList)
                print 'Th0 = ',Th0,Th0/Status.TemperatureInterval
                
#............................................................................................
# Initial selection: maximum reasonable power for a heat pump
# From the annual Heat demand curve (QDa): calculate the necesary heating capacity (starting value)

                Qh0 = interpolateList(Th0/Status.TemperatureInterval,Status.int.QD_T_mod[self.cascadeIndex-1]) #calculates the annual energy demand for the Th_o from QDa
                dotQh0 = Qh0/YEAR*10       #the initial heat capacity of the heat pump is obtained dividing by the hours of year

                print 'ModuleHP (designAssistant1): Initial Annual energy demand Qh0 =', Qh0
                print 'ModuleHP (designAssistant1): Estimated initially heat capacity (from QDa) dotQh0 =', dotQh0
                
                listIndex = findInListASC(dotQh0,HPListPNom)

                if listIndex < 0:
                    print 'err005: Display warning: There is no heat pump available in DB for this application'
#                    return err005

                print 'ModuleHP (designAssistant1): ListIndex =', listIndex, 'dotQh0 = ', dotQh0


#............................................................................................
# Check appropriateness for several heat pumps (preselection)

                PNomMax = 0                 #maximum possible heat pump capacity for desired operating hours
                while listIndex >= 0:       #decrease gradually until HOp >= MinHOp

                    modelID = HPList[listIndex] #a row in the DBHeatPump corresponding to j
                    print 'ModuleHP (designAssistant1): modelID = ', modelID
                                        
                    self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list #SD change 30/04.2008
                    print "ModuleHP (designAssistant1): equipment stored"
                    
                    USHj = self.calculateEnergyFlows(equipe,self.cascadeIndex) #SD change 30/04.2008
                    HOp = USHj/equipe.HCGPnom

                    print "\nModuleHP (designAssistant1): USH: ",USHj," HOp: ",HOp
                    print "ModuleHP (designAssistant1): UHPMinHop: ",DA.UHPMinHop
                   
                    if (HOp >= DA.UHPMinHop):
                        self.preselection.append(modelID)
                        PNomMax = max(PNomMax,equipe.HCGPnom)
                    if equipe.HCGPnom < POWERRANGE*PNomMax:
                        break
                    
                    listIndex -= 1  #Select next smaller heat pump

            print "ModuleHP (designAssistant1): preselected equipment: ",self.preselection

#............................................................................................
# Automatic final selection:

            nSelected = len(self.preselection)
            print "ModuleHP (designAssistant1): return to GUI for manual selection "
            if nSelected <= 0: #no equipment could be selected
                return("CANCEL",self.preselection)
            
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
                                             
#............................................................................................
        except Exception, designAssistant1: #in case of an error
            print 'design assistant 1', designAssistant1
            return ("CANCEL",None) #default in case of error: cancel everything

#------------------------------------------------------------------------------
    def designAssistant2(self,modelID):
#------------------------------------------------------------------------------
#
#        Design Assistant 2 - 
#------------------------------------------------------------------------------

        if (modelID == None or modelID < 0):
            print "user cancelled the selection of the heat pump"
            self.deleteEquipment(None)   #delete the dummy equipment previously created

        else:                        
            self.setEquipmentFromDB(self.equipe,modelID) #add selected equipment to the equipment list #SD change 30/04.2008
            print "ModuleHP: heat pump added. model no: ",modelID

#        Status.mod.moduleEnergy.runSimulation()
        self.updatePanel()
                                
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,cascadeIndex): #SD change 30/04.2008
#------------------------------------------------------------------------------
#
# updates the energy flows in the newly added heat pump
#       
#------------------------------------------------------------------------------

        print "ModuleHP (calculateEnergyFlows): starting (cascade no: %s)"%cascadeIndex
#..............................................................................
# get equipment data from equipment list in SQL

        HPModel = equipe.Model
        print "ModuleHP (calculateEnergyFlows): model",equipe.Model
        HPType = equipe.EquipType
        print "ModuleHP (calculateEnergyFlows): type",equipe.EquipType
        PNom = equipe.HCGPnom
        print "ModuleHP (calculateEnergyFlows): PNom",equipe.HCGPnom
        COPh_nom = equipe.HCGTEfficiency
        print "ModuleHP (calculateEnergyFlows): COP",equipe.HCGTEfficiency
        if equipe.HPExHeatCOP is None or 'NULL': #SD change 30/04.2008
            print 'Exergetic COP (heating) =', equipe.HPExHeatCOP #SD change 30/04.2008
            COPex = 0.3
        else:
            COPex = equipe.HPExHeatCOP #SD change 30/04.2008

        for i in range(cascadeIndex+1):
            print "cascade[%s]: "%i,Status.int.cascade[i-1]["equipeNo"]
        
        EquipmentNo = Status.int.cascade[cascadeIndex-1]["equipeNo"]
        print "ModuleHP (calculateEnergyFlows): eqno",EquipmentNo

#..............................................................................
# design assistant parameters
#XXXXXXXX
# the need for accessing to parameters of the desing assistant should be eliminated
# calculation results for a given equipment under given demand/supply conditions
# should be independent of design assistant selections
# in fact the values at present are only used for initial value settings in iterative
# loops, that can also be done using other equipment parameters

        DA = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]

#XXX to be substituted by something like:
#
#           HPThMax = equipe.HPThMax ...
#           HPTcMin = equipe.HPTcMin

        if getEquipmentSubClass(HPType) == "compression":
            Tg = None
        else:
            Tg = DA.UHPTgenIn
               
        print 'ModuleHP (calculateEnergyFlows): HPModel = ', HPModel, ' HPType = ', HPType

#..............................................................................
# get demand data for CascadeIndex/EquipmentNo from Interfaces
# and create arrays for storing heat flow in equipment

        QD_Tt = Status.int.QD_Tt_mod[cascadeIndex-1]
        QA_Tt = Status.int.QA_Tt_mod[cascadeIndex-1]
        
        USHj_Tt = Status.int.createQ_Tt()
        USHj_t = Status.int.createQ_t()
        USHj_t_rem = USHj_t
        USHj_T = Status.int.createQ_T()

        
        QHXj_Tt = Status.int.createQ_Tt()
        QHXj_t = Status.int.createQ_t()
        QHXj_t_rem = QHXj_t
        QHXj_T = Status.int.createQ_T()

#..............................................................................
# Start hourly loop

        USHj = 0
        QHXj = 0

        for it in range(Status.Nt):

            print "time = ",it*Status.TimeStep
#..............................................................................
# create demand and availability profile for present time step

            QD_T = []
            QA_T = []
            for iT in range(Status.NT+2):
                QD_T.append(QD_Tt[iT][it])
                QA_T.append(QA_Tt[iT][it])

            print "demand profiles created"


#..............................................................................
# start estimates for Th,Tc and COP

#           
#           HPThMax = equipe.HPThMax ...
#           HPTcMin = equipe.HPTcMin

            Th_i = min(DA.UHPmaxT,interpolateTable((PNom*Status.TimeStep),QD_T,Status.int.T))
            Tc_i = max(DA.UHPminT,Th_i-DA.UHPDTMax)  
            COPh_i = COPex*self.calculateCOPh_Carnot(Th_i + HPTDROP,Tc_i - HPTDROP,Tg)

            print "initial estimates (Th,Tc,Tg,COP): ",Th_i,Tc_i,Tg,COPh_i

#..............................................................................
# Special case: zero demand -> assign Q = 0 and go to next timestep
            if  QD_T[Status.NT+1] == 0.0:
                Tc_i=0.0; COPh_i=0.0; COPht_i=0.0;
                dotQh_i=0.0; dotQw_i=0.0; dotQc_i=0.0

#..............................................................................
# Second loop: adjust DTMax

            else:
                Tc_i = - INFINITE
                while fabs(Th_i - Tc_i) > DA.UHPDTMax: #while-loop 2 start

#..............................................................................
# Inner loop: adjust COP and Tc_i

                    COPh0_i = INFINITE; Tc0_i = Tc_i + INFINITE
                    while fabs(COPh_i - COPh0_i) > EPS_COP or fabs(Tc_i - Tc0_i) > EPS_TEMP: #while-loop 3 start
                        
                        COPh0_i = COPh_i;
                        Tc0_i = Tc_i 
                                        
                        dotQh_i = interpolateTable(Th_i,Status.int.T,QD_T)/Status.TimeStep  #gets heat demand corresponding to Th_i
                        dotQw_i = (dotQh_i/COPh_i)              #heat pump input power (mechanical or thermal)
                        dotQc_i = dotQh_i - dotQw_i             #heat pump cooling power

                        Tc_i = interpolateTable(dotQc_i*C,QA_T,Status.int.T) #calc. the temp. corresp. to dotQc_i in QAh[i] curve

                        if Tc_i == 0.0:     #no heat availability -> assign Fpl_i=0
                            break #goes out of the while-loop 3/ continues in the while-loop 2

                        COPh_i = COPex*self.calculateCOPh_Carnot(Th_i+HPTDROP,Tc_i-HPTDROP,Tg)

#..............................................................................
# End inner loop: determination of Tc and COP

                #checking if Th_i=0 and Tc_i=0, if yes skips -> Th_i = Th_i - 1.0
                    if Tc_i == 0.0:
                        break #goes out of while-loop 2 / continues in for-loop

                    Th_i = Th_i - 1.0   #reduce Th and continue iteration

# End second loop: determination of Th
#..............................................................................

            print dotQh_i,dotQc_i,dotQw_i,COPh_i
            
            USHj_t[it] = dotQh_i*Status.TimeStep
            QHXj_t[it] = dotQc_i*Status.TimeStep

            USHj += USHj_t[it]
            QHXj += QHXj_t[it]
             
#..............................................................................
# temperature resolution of delivered and consumed heat
# XXX at the moment this is done by supplying heat to the lowest temperature
# level where there is a demand, and consuming waste heat at the highest level
# this is optimum for the single equipment, but not for the system !!!
            
            USHj_t_rem[it] = USHj_t[it]     #remaining heat to be distributed
                            
            for iT in range(Status.NT+2):   #+1 = the > 400 ºC case
                USHj_Tt[iT][it] = min(QD_Tt[iT][it],USHj_t_rem[it])     #from low to high T
                USHj_t_rem[it] -= USHj_Tt[iT][it]   

                QD_Tt[iT][it] -= USHj_Tt[iT][it]
                

            QHXj_t_rem[it] = QHXj_t[it]     #remaining heat to be distributed

            for iT in range((Status.NT+1),-1,-1):
                QHXj_Tt[iT][it] = min(QA_Tt[iT][it],QHXj_t_rem[it])
                QHXj_t_rem[it] -= QHXj_Tt[iT][it]

                QA_Tt[iT][it] -= QHXj_Tt[iT][it]

#..............................................................................
# End of year reached. Store results in interfaces

        print "ModuleHP (calculateEnergyFlows): now storing final results"
        
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

#        equipe.USHj = USHj #SD change 30/04.2008: from table C->Q
#        equipe.QHXEq = QHXj #SD change 30/04.2008, also name changed (QHXEq)

        print "Total energy supplied by equipment ",USHj, " MWh"
        print "Total waste heat input  ",QHXj, " MWh"

        return USHj


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



