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
#	Version No.: 0.05
#	Created by: 	    Stoyan Danov	    31/01/2008
#	Revised by:         Hans Schweiger          22/03/2008
#                           Stoyan Danov            27/03/2008
#                           Stoyan Danov            01/04/2008
#                           Hans Schweiger          02/04/2008
#                           Hans Schweiger          03/04/2008
#   
#
#       Changes to previous version:
#       22/03/2008 general restructuring and clean-up
#       27/03/2008 screenEquipments(), initPanel(),initUserDefinedParamHP(), getUserDefinedParamHP()
#       01/04/2008 deleteE() - to be finished
#       02/04/2008  __init__: connnetion to sql/DB corrected
#                   initPanel: adaptation to new panel structure
#       03/04/2008 receives moduleEnergy from Modules
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
import einstein.modules.constants as CONST
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
        self.interface = Interfaces()

        self.DB = Status.DB
        self.sql = Status.SQL
    
        self.setupid = Status.SetUpId
        
        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        self.equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
        self.equipmentsC = self.DB.cgenerationhc.sql_select(sqlQuery)
        self.NEquipe = len(self.equipments)
        print "ModuleHP (__init__): %s equipes found"%self.NEquipe

#        self.initUserDefinedParamHP() #puts the user defined parameters from PSetUpData to UHeatPump
#XXX problems with this function in einsteinMain

#............................................................................................
#XXXHS2008-03-22: here for testing purposes.
#   -> initPanel should be activated by event handler on entry into panel

        self.initPanel()
        self.updatePanel()

#------------------------------------------------------------------------------
    def getUserDefinedParamHP(self):
#------------------------------------------------------------------------------
#   gets the user defined data from UHeatPump and stores it to interfaces to be shown in HP panel
#------------------------------------------------------------------------------

        uHP = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]

        #returns to the GUI the default user-defined data to be shown in HP panel
        self.interface.setGraphicsData('HP UserDef',[uHP.UHPType,uHP.UHPMinHop,uHP.UHPDTMax,
                                                     uHP.UHPmaxT,uHP.UHPminT,uHP.UHPTgenIn])


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
    def initPanel(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

        HPList = self.screenEquipments()

        print 'test initPanel: HPList =', HPList
        print 'moduleHP (initPanel): ci = ',self.cascadeIndex
        
#............................................................................................
#XXX FOR TESTING PURPOSES ONLY: load default demand
# here it should be assured that heat demand and availability for position in cascade
# of presently existing heat pumps is already defined

        #creates space/lists for storing the modified QD,QA, assigns total D,A in all positions
        self.interface.initCascadeArrays(self.NEquipe) 

        print 'moduleHP (initPanel): cascade Arrays initialised '

        #returns HPList to the GUI for displaying in HP panel, table: Existing Heat Pumps
        self.interface.setGraphicsData('HP Table',[HPList,["o","o","r","r","r","r"]]) 
#XXX ["o","o","r","r","r","r"] indicates which columns should de shown in the panel: "o" oculto, "r" read only
#XXX es esto tu idea Hans? SD,28/03/2008

#XXX        self.cascadeIndex = 0 #indicates first in list of modyfied demand and availability: total D,A to be shown in plot
#XXX esto sobreescribe el posicionamento de cascadeIndex que has hecho en screenEquipments !!! realmente quieres eso ... ???
#XXX si, cuando se inicia el panel queria que mostrara las curvas totales, mientras que si se utiliza en otro lugar,
#XXX que apunte a las ultimas, no se si sera necesario llamar screenEquipments en otro lugar, por si acaso...SD,28/03/2008

        #returns to the GUI the lists to dislay the plot in HP panel. Initially shows the total heat demand and availability 
        self.interface.setGraphicsData('HP Plot',[self.interface.T, 
                                                      self.interface.QD_T_mod[self.cascadeIndex],
                                                      self.interface.QA_T_mod[self.cascadeIndex],
                                                      self.interface.QD_T_mod[self.cascadeIndex+1],
                                                      self.interface.QA_T_mod[self.cascadeIndex+1]])

        #returns to the GUI the pinch temperature and the temperature gap to be shown in HP panel (below graphic)
        #XXX Define where they come from.....SD,27.03.2008
#        self.interface.setGraphicsData('HP Info',[ TPinch, TGap])

#        self.initUserDefinedParamHP() #puts the user defined parameters from PSetUpData to UHeatPump
#XXX problems with this function in einsteinMain

        self.getUserDefinedParamHP() #returns to the GUI the default user-defined data to be shown in HP panel

        print 'moduleHP (initPanel): reached the end '
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def screenEquipments(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

        self.interface.getEquipmentCascade()
        HPList = []
        for row in self.interface.cascade:
            if row['equipeType'] == 'Heat pump':
                HPList.append(row)

        if(len(HPList)>0):
            self.cascadeIndex = len(HPList)-1 #by default sets selection to last HP in cascade
        else:
            self.cascadeIndex = 0
#XXXHS2008-04-02: he puesto cascadeIndex a 0 en vez de None: check que sea consistente esto ...

#        print '\n cascadeIndex =', self.cascadeIndex
        
        return HPList
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------

        print "ModuleHP (updatePanel): data for panel are copied to interface"

        print self.interface.T
        print self.interface.QD_T
        print self.interface.QA_T
        print self.interface.QD_T_mod[self.cascadeIndex]
        print self.interface.QA_T_mod[self.cascadeIndex]
        
#XXX TESTING ONLY TESTING ONLY TESTING ONLY
        print "ModuleHP (updatePanel): setting HP list dummy for testing"
        
        # plot to be displayed
	# this is how the data should be set up
	# (this data are just an example!)
        data = array([['HP 1', 2004, 'Type 1', 3000, 100, 120],
		      ['HP 2', 2006, 'Type 1', 4500, 120, 140],
                      ['HP 3', 2007, 'Type 2', 5000,  80, 130]])


        print "ModuleHP (updatePanel): key = ",self.keys[0]
        self.interface.setGraphicsData(self.keys[0], data)

        # plot to be displayed
        try:
            self.interface.setGraphicsData('HP Plot',[self.interface.T,
                                                      self.interface.QD_T_mod[self.cascadeIndex],
                                                      self.interface.QA_T_mod[self.cascadeIndex],
                                                      self.interface.QD_T_mod[self.cascadeIndex+1],
                                                      self.interface.QA_T_mod[self.cascadeIndex+1]])
        except:
            pass
# info for text boxes in right side of panel
        self.interface.setGraphicsData('HP Info',{"noseque":55})

# list of equipments in cascade for Table
        self.interface.setGraphicsData('HP List',self.interface.cascade)

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def exitFrame(exit_option):
#------------------------------------------------------------------------------
        """
        carries out any calculations necessary previous to displaying the HP
        design assitant window
        """
#------------------------------------------------------------------------------
        #if exit_option == "save":
            # save current HP configuration
        #elif exit_option == "nosave":
            # restore HP configuration before entering the window from back-up

        print "exitFrame: function not yet defined"

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def add(HPid):
#------------------------------------------------------------------------------
        """
        adds a new heat pump 
        """
#------------------------------------------------------------------------------

        #--> add HP to the equipment list under current alternative
        self.calculateEnergyFlows(HPid)

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def deleteE(self,HPid):
#------------------------------------------------------------------------------
        """
        deletes the selected heat pump in the current alternative
        """
#------------------------------------------------------------------------------
        print "deleteHP: function not yet defined"

        #--> delete HP from the equipment list under current alternative #from C&QGenerationHC under ANo
        
        eq = self.equipments.QGenerationHC_ID[HPid][0] #select the corresponding rows to HPid in both tables
        eqC = self.equipmentsC.QGenerationHC_id[HPid][0]

        eq.delete() #deletes the rows in both tables, to be activated later, SD
        eqC.delete()
        self.sql.commit()

        #actuallise the cascade list: define deleteFromCascade
        self.deleteFromCascade(self.interface.cascade, HPid)

        #actuallize the CascadeIndex & EqNo in C,QGen..HC tables

        #change self.cascadeIndex -> to appoint the next in list
        

#------------------------------------------------------------------------------
    def deleteFromCascade(self, cascade, HPid):
#------------------------------------------------------------------------------
        """
        deletes from the actual list casade and re-assigns the CascadeIndex values in CGenerationHC table
        """
#-----------------------------------------------------------------------------

        print '\n deleteFromCascade():', 'cascade =', cascade

        idx = -1
        new_cascade = cascade
        for i in range(len(new_cascade)):
            if new_cascade[i]['equipeID'] == HPid:
                idx = i

        new_cascade.pop(idx)           

        for i in range(len(new_cascade)): #assign new CascadeIndex in CGenerationHC table
            eqC = self.equipmentsC.QGenerationHC_id[new_cascade[i]['equipeID']][0]
            eqC.CascadeIndex = i+1
            print '\n new_CascadeIndex', eqC.CascadeIndex
            
#        self.sql.commit() #confirm storing to sql of new CascadeIndex #to be activated, SD

        print '\n deleteFromCascade():', 'new_cascade =', new_cascade


        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY EqNo ASC"%(Status.PId,Status.ANo)
        equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
##        print '\n \nequipments', equipments

        for i in range(len(equipments)): #assign new EqNo in QGenerationHC table
            equipments[i].EqNo = i+1

#        self.sql.commit() #to be activated, SD




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
        print 'moduleHP (addEquipmentDummy): cascade Arrays initialised '

        self.cascadeIndex = 0
        self.equipe = self.equipments[0]
        self.equipeC = self.equipmentsC[0]
        return(self.equipe,self.equipeC)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def setEquipmentFromDB(self,equipe,modelID):
#------------------------------------------------------------------------------
#   takes an equipment from the data base and stores it under a given Id in
#   the equipment data base
#------------------------------------------------------------------------------

        model = self.DB.dbheatpump.DBHeatPump_ID[modelID][0]
        equipe.Model = model.HPModel
        equipe.EquipType = "HP " + model.HPType
        equipe.HCGPnom = model.HPHeatCap
        equipe.HCGTEfficiency = model.HPHeatCOP

        print "HP Model: ",model.HPModel, "Type: ",model.HPType," Cap.: ",model.HPHeatCap
        
#        Status.DB.commit()
#XXX TO BE CHECKED ...

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
        return (HPList,HPListPNom,DTMax,TCondMax)

#----------------------------------------------------------------------------
    def calculateCOPh_Carnot(self,Th,Tc,Tg = None):
#----------------------------------------------------------------------------
#   Calculates the theoretical Carnot COP.
#XXX Pending the application of temperature corrections for secondary fluids !!!
#----------------------------------------------------------------------------

        if (Th<=Tc):
            COPh_Carnot = CONST.INFINITE
            
        elif Tg==None:                              # compression heat pumps
                COPh_Carnot = (Th+CONST.KELVIN)/(Th-Tc)
                print "COP: ",Th,Tc,COPh_Carnot
                
        else:                                       # absorption heat pumps
            COPh_Carnot = ((Tc+CONST.KELVIN)*(Tg-Th))/((Tg+CONST.KELVIN)*(Th-Tc))+1

        return COPh_Carnot

#------------------------------------------------------------------------------
    def getTMinD(self,Q_T):
#------------------------------------------------------------------------------
#   Looks for the minimum temperature in heat demand
#------------------------------------------------------------------------------
        iT = firstNonZero(Q_T)      #find the index
        return(self.interface.T[iT])        #find the T corresponding to index
        
#------------------------------------------------------------------------------
    def getTMaxA(self,Q_T):
#------------------------------------------------------------------------------
#   Looks for the minimum temperature in heat demand
#------------------------------------------------------------------------------
        iT = lastNonZero(Q_T)       #find the index
        return(self.interface.T[iT])        #find the T corresponding to index
        
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
            if DA.UHPMinHop > CONST.YEAR:        #check of user input   
                print 'err002: Display warning: Required working hours are greater than the hours of the year!'
#                return err002
                            
            (HPList,HPListPNom,DTMaxInList,TCondMaxInList) = self.getHPList(DA.UHPType)  #get the sorted list of available heat pumps
            print "ModuleHP (designAssistant1) List of heat pumps: ",len(HPList)

#............................................................................................
#   add a new equipment as space holder to the equipment list

#            if (MaintainExistingEquipment == False):
#                deleteAllHeatPumps()

            (equipe,equipeC) = self.addEquipmentDummy()

#............................................................................................
#   analyze heat demand for previous checks

            TMinD = self.getTMinD(self.interface.QD_T_mod[self.cascadeIndex])
            TMaxA = self.getTMaxA(self.interface.QA_T_mod[self.cascadeIndex])
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

                Qh0 = interpolateList(Th0/Status.TemperatureInterval,self.interface.QD_T_mod[self.cascadeIndex]) #calculates the annual energy demand for the Th_o from QDa
                dotQh0 = Qh0/CONST.YEAR*10       #the initial heat capacity of the heat pump is obtained dividing by the hours of year

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
                                        
                    self.setEquipmentFromDB(equipe,modelID)   #assign model from DB to current equipment in equipment list
                    print "ModuleHP (designAssistant1): equipment stored"
                    
                    USHj = self.calculateEnergyFlows(equipe,equipeC,self.cascadeIndex)
                    HOp = USHj/equipe.HCGPnom

                    print "ModuleHP (designAssistant1): USH: ",USHj," HOp: ",HOp
                    
                    if (HOp >= DA.UHPMinHop):
                        self.preselection.append(modelID)
                        PNomMax = max(PNomMax,equipe.HCGPnom)
                    if equipe.HCGPnom < POWERRANGE*PNomMax:
                        break
                    
                    listIndex -= 1  #Select next smaller heat pump

            print "ModuleHP (designAssistant1): preselected equipment: ",self.preselection

#............................................................................................
# Automatic final selection:

            if Status.InteractionLevel == "interactive" or Status.InteractionLevel == "semi-automatic":
                print "ModuleHP (designAssistant1): return to GUI for manual selection "
                return("MANUAL",self.preselection)

            else:   
                maxCOP = 0
                for listIndex in self.preselection:
                    modelID = HPList[listIndex]
                    model = self.DB.dbheatpump.DBHeatPump_ID[modelID][0]
                    if (model.HPHeatCOP > maxCOP):
                        bestModelID = modelID
                        maxCOP = model.HPHeatCOP
                self.preselection = [bestModelID]
                print "ModuleHP (designAssistant1): return to GUI (equipment automatically selected)",self.preselection
                return ("AUTOMATIC",self.preselection)
                                                    
#............................................................................................
        except Exception, designAssistant1: #in case of an error
            print 'design assistant 1', designAssistant1
            return designAssistant1

#............................................................................................
        else:       #everything is fine
            return ("ERROR",None)
        print 'The program will be terminated. Exit'        


#------------------------------------------------------------------------------
    def designAssistant2(self,modelID):
#------------------------------------------------------------------------------
#
#        Design Assistant 2 - 
#------------------------------------------------------------------------------

        if (modelID == None):
            print "user cancelled the selection of the heat pump"
#XXX Function to be defined           deleteEquipment(equipe)

        else:                        
            self.setEquipmentFromDB(self.equipe,modelID) #add selected equipment to the equipment list
            print "ModuleHP: heat pump added. model no: ",modelID

        Status.mod.moduleEnergy.runSimulation()
        self.updatePanel()
                                
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,equipeC,cascadeIndex):
#------------------------------------------------------------------------------
#
# updates the energy flows in the newly added heat pump
#       
#------------------------------------------------------------------------------

        print "ModuleHP (calculateEnergyFlows): starting (cascade no: %s)"%cascadeIndex
#..............................................................................
# get equipment data from equipment list in SQL

        HPModel = equipe.Model
        print equipe.Model
        HPType = equipe.EquipType
        PNom = equipe.HCGPnom
        COPh_nom = equipe.HCGTEfficiency
#        COPex = equipeC.HCGCOPex       XXX To be introduced in DB
        COPex = 0.3 

        EquipmentNo = self.interface.cascade[cascadeIndex]["equipeNo"]

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

        if equipe.EquipType == "HP COMP":
            Tg = None
        else:
            Tg = DA.UHPTgenIn
               
        print 'ModuleHP (calculateEnergyFlows): HPModel = ', HPModel, ' HPType = ', HPType

#..............................................................................
# get demand data for CascadeIndex/EquipmentNo from Interfaces
# and create arrays for storing heat flow in equipment

        QD_Tt = self.interface.QD_Tt_mod[cascadeIndex]
        QA_Tt = self.interface.QA_Tt_mod[cascadeIndex]
        
        USHj_Tt = self.interface.createQ_Tt()
        USHj_t = self.interface.createQ_t()
        USHj_t_rem = USHj_t
        USHj_T = self.interface.createQ_T()

        
        QHXj_Tt = self.interface.createQ_Tt()
        QHXj_t = self.interface.createQ_t()
        QHXj_t_rem = QHXj_t
        QHXj_T = self.interface.createQ_T()

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

            Th_i = min(DA.UHPmaxT,interpolateTable((PNom*Status.TimeStep),QD_T,self.interface.T))
            Tc_i = max(DA.UHPminT,Th_i-DA.UHPDTMax)  
            COPh_i = COPex*self.calculateCOPh_Carnot(Th_i + HPTDROP,Tc_i - HPTDROP,Tg)

            print "initial estimates (Th,Tc,COP): ",Th_i,Tc_i,Tg,COPh_i

#..............................................................................
# Special case: zero demand -> assign Q = 0 and go to next timestep
            if  QD_T[Status.NT+1] == 0.0:
                Tc_i=0.0; COPh_i=0.0; COPht_i=0.0;
                dotQh_i=0.0; dotQw_i=0.0; dotQc_i=0.0

#..............................................................................
# Second loop: adjust DTMax

            else:
                Tc_i = - CONST.INFINITE
                while fabs(Th_i - Tc_i) > DA.UHPDTMax: #while-loop 2 start

#..............................................................................
# Inner loop: adjust COP and Tc_i

                    COPh0_i = CONST.INFINITE; Tc0_i = Tc_i + CONST.INFINITE
                    while fabs(COPh_i - COPh0_i) > EPS_COP or fabs(Tc_i - Tc0_i) > EPS_TEMP: #while-loop 3 start
                        
                        COPh0_i = COPh_i;
                        Tc0_i = Tc_i 
                                        
                        dotQh_i = interpolateTable(Th_i,self.interface.T,QD_T)  #gets heat demand corresponding to Th_i
                        dotQw_i = (dotQh_i/COPh_i)              #heat pump input power (mechanical or thermal)
                        dotQc_i = dotQh_i - dotQw_i             #heat pump cooling power

                        Tc_i = interpolateTable(dotQc_i*Status.TimeStep,QA_T,self.interface.T) #calc. the temp. corresp. to dotQc_i in QAh[i] curve

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

    HPid = 6
    
    interf = Interfaces()

#    modE = ModuleEnergy()
#    modE.runSimulation()

    mod = ModuleHP()
    mod.initPanel()
#    mod.deleteE(HPid)
##    mod.designAssistant1()
##    mod.designAssistant2(12)
