# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleST (Solar thermal systems)
#			
#------------------------------------------------------------------------------
#			
#	Module for calculation of solar thermal systems
#
#==============================================================================
#
#	Version No.: 0.11
#	Created by: 	    Hans Schweiger	25/06/2008
#                           (based on ModuleST from Enrico Facci)
#	Last revised by:    Enrico Facci &      05/07/2008
#                           Claudia Vannoni
#                           (...)
#                           Hans Schweiger      23/07/2008
#                           Enrico Facci        23/07/2008
#                           Hans Schweiger      24/07/2008
#
#       Changes to previous version:
#
#       05/07/2008  Changed nearly everything
#       09/07/2008: HS  changes in:
#                       - deleteEquipment
#                       - addEquipmentDummy
#                       - setEquipmentFromDB
#                       - deleteFromCascade (-> function completely eliminated,
#                               no longer necessary)
#       23/07/2008: HS  update adapting to corrections in "sunday"
#       24/07/2008: HS  biaxial incidence angle modifier
#
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
from einstein.modules.messageLogger import *

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
#    print "moduleST;getDailyRadiation: the daily radiation is ",H
    return H
                 
#------------------------------------------------------------------------------		
def collectorEfficiency(GT,dT,STc0,STc1,STc2):
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
#        STc0 = 0.80 # Collector parameters from the DB: As default STARTING value choose always:LowTempCollType=FPEinstein
#        STc1 = 3.50
#        STc2 = 0.010
        return STc0 - (STc1 + STc2*dT)*dT/(GT)
                 
#============================================================================== 
#------------------------------------------------------------------------------		
def collectorEfficiencyBiaxial(GbT,GdT,tanThetaL,tanThetaT,dT,STc0,STc1,STc2,K50L,K50T):
#------------------------------------------------------------------------------		
#   Calculates the collector efficiency at a given working point
#   GT: Solar radiation on tilted surface (SI - units: W/m2)
#   c1/c2 are in W/m2K, W/m2K2 !!!
#------------------------------------------------------------------------------		


    if (GbT+GdT) <= 0:
        return 0.0
    else:
        
        bT = - log(K50T)/pow(tan(2*pi*50.0/360.),2) 
        bL = - log(K50L)/pow(tan(2*pi*50.0/360.),2)
        
        KT = exp(-bT*pow(tanThetaT,2)) #transversal IAM
        KL = exp(-bL*pow(tanThetaL,2)) #longitudinal IAM

        c0_b = STc0*KT*KL
        c0_d = STc0*K50T*K50L             # 50º IAM supposed for diffuse radiation
        c0 = (c0_b*GbT + c0_d*GdT)/(GbT+GdT)    #weighted average between beam and diffuse

        return c0 - (STc1 + STc2*dT)*dT/(GbT + GdT)
                 
#============================================================================== 
#==============================================================================
class SolarCostFunction():

#------------------------------------------------------------------------------
    def __init__(self,c30,c300,c3000,unitPrice300,OM):
#------------------------------------------------------------------------------
        self.calculateCostCoefs(c30,c300,c3000)
        self.costRatio = float(unitPrice300) / c300
        self.OM = float(OM)
#------------------------------------------------------------------------------
    def calculate(self,Pnom):
#------------------------------------------------------------------------------
        C_turnKey = Pnom*(self.FixCost + self.AddCost * exp(-Pnom/self.Pref))
        C_col = C_turnKey * self.costRatio
        C_OM = Pnom*self.OM
        return (C_turnKey,C_col,C_OM)
        
    #------------------------------------------------------------------------------
    def calculateCostCoefs(self,c30,c300,c3000):
    #------------------------------------------------------------------------------
    #   calculates iteratively the coefficients of the cost function
    #   C = C0 + C1*exp(-Pnom/Pref)
    #------------------------------------------------------------------------------


    #..............................................................................
    #   Previous checks if curve is reasonable:

        if c30 < c300 or c300 < c3000:
            print "cost figures not reasonable"
            return (c300,0,300.0)

        if c3000/c300 < c300/c30:
            print "warning, unrealistic case, not in consistence with correlation"
            c300 = pow(c30*c3000,0.5)

    #..............................................................................
    #   Initial estimate:

        C0 = 0.9*c3000

    #..............................................................................
    #   xi = exp(-300/PRef)
    #   RSMALL = (C30 - C0)/(C300 - C0) = (xi**1/10/xi) = xi**-0.9)
    #   RLARGE = (C3000 - C0)/(C300 - C0) = (xi**9)
    #   -> xi_S = rsmall**(-1/0.9)
    #   -> xi_L = rlarge**(1/9.0)

        alpha = 0.5
        
        for i in range(1000):

            if (c300 > C0):
                rsmall = (c30 - C0)/(c300 - C0)
                xi = pow(rsmall,1.0/(0.1-1.0))
            else:
                xi = 1.0

            C1 = (c30 - c300)/(pow(xi,0.1) - xi)

            C0p = c3000 - C1*pow(xi,10.0)
            C0p = min(C0p,c3000)

            diff = (C0p  - C0)/C0
            C0 += alpha *(C0p-C0)

            print "C0: %s C1: %s xi: %s diff: %s "%(C0,C1,xi,diff)
            if diff < 1.e-6:
                break

        Pref = -300.0/log(xi)
        print "C0: %s C1: %s Pref: %s "%(C0,C1,Pref)

        print "C30 = %s"%(C0+C1*exp(-30.0/Pref))
        print "C300 = %s"%(C0+C1*exp(-300.0/Pref))
        print "C3000 = %s"%(C0+C1*exp(-3000.0/Pref))

        self.FixCost = C0
        self.AddCost = C1
        self.Pref = Pref
        
        return (C0,C1,Pref)
    
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
        self.atmosfericFlag = 0
        self.surfaceFlag = 0

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#   initPanel is called when the user opens the DA panel
#   all the calculations should be carried out here that are necessary only
#   the first time. the rest should be done in "updatePanel"
#------------------------------------------------------------------------------
        self.avAreaFactor=1.1
        self.generalData()
        self.screenSurfaces()
        self.calcSurfArea()
        (self.inclination,self.azimuth,self.shLoss)=self.defineCalcParams()
        self.guiSysPars = [0,0,0]
        self.TavCollMean = 0
        if Status.int.cascadeUpdateLevel < 0:
            Status.int.initCascadeArrays(0)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#   Here all the information should be prepared so that it can be plotted on the panel
#   This function will be called from the GUI every time some information to
#   be displayed might have changed
#------------------------------------------------------------------------------
        print "Updating Solar Thermal window"
        (STList,collectorList) = self.screenEquipments()
        print "---moduleST;updatePanel: the STList is----",STList
        if Status.int.cascadeUpdateLevel < self.cascadeIndex:
            Status.mod.moduleEnergy.runSimulation(last=self.cascadeIndex)

#............................................................................................
# 1. List of equipments

        data = array(collectorList)
#        collectors = [["Buderus XY 007","flat plate collector",0.8,3.0,0.01,0.93]]
#        data = array(collectors)

        Status.int.setGraphicsData('ST Table',data)
#............................................................................................
# 2. Preparing data

#        Status.int.setGraphicsData('ST Plot',[[1,2,3,4],[2,4,6,8],[3,5,9,7],[4,3,2,3],[5,5,10,5]])

        Tmax = 200.0
        iTmax = int(Tmax/Status.TemperatureInterval + 0.5)
        index=self.findIndex()
        print "ModuleST: index =",index,"cascadeIndex=",self.cascadeIndex
        
        if len(STList)>0:
            Status.int.setGraphicsData('ST Plot',[Status.int.T[0:iTmax],
                                                  Status.int.QD_T_mod[index][0:iTmax],
                                                  Status.int.USHj_T[index][0:iTmax]])
        else:
            Status.int.setGraphicsData('ST Plot',[Status.int.T[0:iTmax],
                                                  Status.int.QD_T[0:iTmax]])
            #HS2008-07-10: security feature if no ST existing. -> send global demand
#............................................................................................
# 3. Configuration design assistant

        config = noneFilter(self.getUserDefinedPars())
        Status.int.setGraphicsData('ST Config',config)

    
#............................................................................................
# 4. additional information

        if len(STList)>0:
            yi= Status.int.USHj_T[index][iTmax]/(STList[0][0])
            sf=Status.int.USHj_T[index][iTmax]*100/Status.int.QD_T_mod[index][iTmax]
            print "ModuleST; updatePanel: the heat supplyed in a year by the solar system is:",Status.int.USHj_T[index][iTmax]
        else:
            yi=0
            sf=0
        if self.TavCollMean == 0:
            TC = "--"
        else:
            if len(STList) > 0:
                TC =self.TavCollMean
            else:
                TC = "--"
        info = [self.latitude,self.usableSurfacesArea,self.grossSurfArea,sf,yi,TC,0]
        Status.int.setGraphicsData('ST Info',info)

#        info = [0,0,0,0,0,0,0]
#        Status.int.setGraphicsData('ST Info',info)

#............................................................................................
# 5. System parameters to GUI


        if len(STList) > 0:
            sysPars = noneFilter(STList[0])
        else:
            sysPars = self.guiSysPars
        Status.int.setGraphicsData('ST SysPars',sysPars)

        print "ST window updated"    

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def getUserDefinedPars(self):
#------------------------------------------------------------------------------
#   gets the user defined data from UHeatPump and stores it to interfaces to be shown in HP panel
#------------------------------------------------------------------------------

        urows = Status.DB.uheatpump.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]

        if len(urows) == 0:
            print 'getUserDefinedParamST: Status.PId =', Status.PId, 'Status.ANo =', Status.ANo, 'not defined'
            print 'Error: confusion in PId and ANo'

            dummy = {"Questionnaire_id":Status.PId,"AlternativeProposalNo":Status.ANo} 
            Status.DB.uheatpump.insert(dummy)

            config = [0.5,STTYPES[0],500.0]            
            Status.int.setGraphicsData('ST Config',config)

            self.setUserDefinedPars()

        else:
            u = urows[0]
            config = noneFilter([u.STSolFra,
                      u.STCollType,
                      u.STMinYield])
            print "ModuleST (getUserDefinedPars): config = ",config

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

        u.STSolFra = config[0]
        u.STCollType = config[1]
        u.STMinYield = config[2]

        Status.SQL.commit()

#------------------------------------------------------------------------------
    def setSolarSystemPars(self):
#------------------------------------------------------------------------------

        sysPars = Status.int.GData['ST SysPars']

        equipments = Status.DB.qgenerationhc.\
                      Questionnaire_id[Status.PId].\
                      AlternativeProposalNo[Status.ANo].\
                      CascadeIndex[self.cascadeIndex]
        (STList,collectorList) = self.screenEquipments()
        if len (STList)>0:
            if len(equipments) > 0:
                equipe = equipments[0]
                equipe.HCGPnom = sysPars[0]
                equipe.ST_SysEff = sysPars[1]        
                equipe.ST_Volume = sysPars[2]

        else:
            self.guiSysPars[0] = sysPars[0]
            self.guiSysPars[1] = sysPars[1]
            self.guiSysPars[2] = sysPars[2]
            
        Status.int.changeInCascade(self.cascadeIndex)
       
        Status.SQL.commit()

#------------------------------------------------------------------------------
    def screenEquipments(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#------------------------------------------------------------------------------

        equipments = Status.prj.getEquipments(cascade=True)
        print "ModuleST; screenEquipments: all the equipments in this project are:",equipments
        self.NEquipe=len(equipments)
        STList=[]
        collectorList=[]
#        e=equipments[0]
#        print "ModuleST; screenEquipments: the first equipment is a:", getEquipmentClass(e.EquipType)
        self.equipeIDs=[]
        self.cascadeIndex = 0
        for equipe in equipments:
            if getEquipmentClass(equipe.EquipType) == "ST":
                collectorTable = [equipe.Model,
                                  equipe.EquipType,
                                  equipe.ST_C0,
                                  equipe.ST_C1,
                                  equipe.ST_C2,
                                  equipe.ST_K50L,
                                  equipe.ST_K50T]
                systemTable = [equipe.HCGPnom,
                               equipe.ST_SysEff,
                               equipe.ST_Volume]
                self.equipeIDs.append(equipe.QGenerationHC_ID)
                STList.append(systemTable)
                collectorList.append(collectorTable)
                self.cascadeIndex = equipe.CascadeIndex
        if len(STList)>1:
            logMessage(_("pay attenction more than one solar system"))
        return (STList,collectorList)
        

        
#------------------------------------------------------------------------------
    def getEqId(self,rowNo):
#------------------------------------------------------------------------------
#   gets the EqId from the rowNo in the STList
#------------------------------------------------------------------------------

        STId = self.equipeIDs[rowNo]
        return STId

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def deleteEquipment(self,rowNo,automatic=False):
#------------------------------------------------------------------------------
        """
        deletes the selected boiler in the current alternative
        """
#------------------------------------------------------------------------------
#HS2008-07-09: CHANGES FOR DEMO !!!!
        if automatic == False:
            if rowNo == None:   #indicates to delete last added equipment dummy
                if self.dummyEqId is None:
                    return
                else:
                    STid = self.dummyEqId
            else:
                STid = self.getEqId(rowNo)
                print "Module ST (delete): id to be deleted = ",STid
        else:
            STid= rowNo
            print "Module ST (delete automaticly): id to be deleted = ",STid
        
        Status.prj.deleteEquipment(STid)
        self.screenEquipments()
        self.guiSysPars = [0,0,0]
        self.updatePanel()
        self.avAreaFactor=1.1

#------------------------------------------------------------------------------
    def addEquipmentDummy(self):
#------------------------------------------------------------------------------
#       adds a new dummy equipment to the equipment list and returns the
#       position in the cascade 
#------------------------------------------------------------------------------

        (STList,collectorList) = self.screenEquipments()
        if len(STList)>0:
            self.dummyEqId = None
            equipments = Status.DB.qgenerationhc.\
                      Questionnaire_id[Status.PId].\
                      AlternativeProposalNo[Status.ANo].\
                      CascadeIndex[self.cascadeIndex]
            if len(equipments)>0:
                self.equipe=equipments[0]
                return self.equipe

            else: print " module ST: addEquipmentDummy error!!!!!"

        self.equipe = Status.prj.addEquipmentDummy()
        self.dummyEqId = self.equipe.QGenerationHC_ID
        if self.equipe.CascadeIndex >1:
            Status.mod.moduleHC.cascadeMoveToTop(self.equipe.CascadeIndex) 
        
        self.equipe = Status.prj.getEquipe(self.dummyEqId) #after having moved, the equipe - table has to be updated !!!
        self.cascadeIndex = self.equipe.CascadeIndex

        NewEquipmentName = "Solar thermal system"

        equipeData = {"Equipment":NewEquipmentName,\
                      "EquipType":"solar thermal (flat-plate)"} # by default assign any valid equipe type.
                                                                # should be updated in setEquipmentFromDB
        self.equipe.update(equipeData)
        Status.SQL.commit()

        
        self.setSolarSystemPars()

        sysPars = Status.int.GData['ST SysPars']
        if sysPars[0]==None:
            power=self.SurfAreaSol*0.7
        elif sysPars[0]> self.TotNetSurfArea*0.7:
            power=self.TotNetSurfArea*0.7
            showWarning(_("The power of the solar system has been reduced because the suitable surfaces are too small to supply the required one.")) 
        else:
            power=sysPars[0]
        self.equipe.HCGPnom = power
        
        Status.SQL.commit()

        self.screenEquipments()
        
        return(self.equipe)


#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def setEquipmentFromDB(self,equipe,modelID):
#------------------------------------------------------------------------------
#   takes an equipment from the data base and stores it under a given Id in
#   the equipment data base
#------------------------------------------------------------------------------

        models = Status.DB.dbsolarthermal.DBSolarThermal_ID[modelID]
        if len(models) > 0:
            model = models[0]
        else:
            logTrack("ModuleST: selected model ID %s not in database"%modelID)
            
        logTrack("ModuleST: setting equipment from DB")
#        logTrack("ModuleST: Pnom %s Eff: %s "%((self.SurfAreaSol*0.7),self.etaSelected))

#        equipe.update({"HCGPnom":(self.SurfAreaSol*0.7)})        
#        equipe.update({"HCGTEfficiency":self.etaSelected})

        if model.STManufacturer != None: equipe.update({"Manufact":model.STManufacturer})
        if model.STModel != None: equipe.update({"Model":model.STModel})
        logTrack("ModuleST: setting equipment type from %s"%model.STType)
        logTrack("ModuleST: setting equipment type to %s"%getEquipmentType("ST",model.STType))
        
        equipe.update({"EquipType":getEquipmentType("ST",model.STType)})
        
        equipe.update({"NumEquipUnits":1})
        logTrack("ModuleST: selected model = %s"%str(model))
        logTrack("ModuleST: model type = %s"%str(model.STType))
        
        logTrack("ModuleST: dummy equipe = %s"%str(equipe))
        
        if model.STType != None: equipe.update({"EquipTypeFromDB":str(model.STType)})
        if model.STc0 != None: equipe.update({"ST_C0":model.STc0})
        if model.STc1 != None: equipe.update({"ST_C1":model.STc1})
        if model.STc2 != None: equipe.update({"ST_C2":model.STc2})
        if model.K50L != None: equipe.update({"ST_K50L":model.K50L})
        if model.K50T != None: equipe.update({"ST_K50T":model.K50T})
        if model.DBSolarThermal_ID != None: equipe.update({"EquipIDFromDB":model.DBSolarThermal_ID})
        if model.STAreaGross != None and model.STAreaAper != None:
            self.avAreaFactor = model.STAreaGross/model.STAreaAper
        
        Status.SQL.commit()
        logTrack("ModuleST: dummy equipe after commit of everything %s"%str(equipe))


        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def calculateEnergyFlows(self,equipe,cascadeIndex):
#------------------------------------------------------------------------------
#   calculates the energy flows in the equipment identified by "cascadeIndex"
#------------------------------------------------------------------------------

        logTrack("ModuleST (calculateEnergyFlows): starting (cascade no: %s)"%cascadeIndex)

        if Status.int.cascadeUpdateLevel < (cascadeIndex - 1):
            logDebug("ModuleBB (calculateEnergyFlows): cannot calulate without previously updating the previous levels")
            Status.mod.moduleEnergy.runSimulation(last=(cascadeIndex-1))

#..............................................................................
# get equipment data from equipment list in SQL

        STModel = equipe.Model
        print equipe.Model
        STType = equipe.EquipType
        PNom = equipe.HCGPnom

####HS2008-07-09: SECURITY FEATURE ADDED
        if PNom is None or PNom == 0:
            logDebug("ModuleST (calcEn.Flows): equipe with PNom = None or PNom = 0 detected\nCan't do anything with this !!!")
            return
            
        COPh_nom = equipe.HCGTEfficiency

#XXX TOpMax or something similar should be defined in SQL        TMax = equipe.TOpMax
# for the moment set equal to TExhaustGas
#        TMax = equipe.TExhaustGas
        Tmax=200

#XXX ENRICO: here other equipment parameters should be imported from SQL database
        self.screenEquipments()
#        print "ModuleST,calcEnergyFlows. The cascadeIndex-1 is:", cascadeIndex-1
#        EquipmentNo = Status.int.cascade[cascadeIndex-1]["equipeNo"]

#        print 'ModuleST (calculateEnergyFlows): Model = ', STModel, ' Type = ', STType, 'PNom = ', PNom

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

#        (inclination,azimuth,shLoss)=self.defineCalcParams()
########################################################################################################3
########################################################################################################3
########################################################################################################3
########################################################################################################3

        if self.atmosfericFlag != 1:
            self.generalData()
        if self.surfaceFlag != 1:
            self.screenSurfaces()
            self.calcSurfArea()
            (self.inclination,self.azimuth,self.shLoss)=self.defineCalcParams()
#HS 2008-07-09: geographic data not found. here re-activated as a dummy
#        self.latitude = 41.4
#        self.inclination = 30
#        self.azimuth = 15.0
########################################################################################################3
########################################################################################################3
########################################################################################################3
########################################################################################################3

#        I=Status.DB.qrenewables.Questionnaire_id[Status.PId][0].ST_I
#        if I== None or I <100 or I >3000:
#            if self.Lat=None:
#                I=1300
#            else:
#                    I=1300   # Here a function from Claudia to calculate I(Lat)
########################################################################################################3
########################################################################################################3
########################################################################################################3
########################################################################################################3
#HS 2008-07-09: self.ST_IDefault seems not yet to be working. for the moment a fix number
#        I = 1500
# now self.ST_IDefault should be Found
        I = self.ST_IDefault
########################################################################################################3
########################################################################################################3
########################################################################################################3
########################################################################################################3

########################################################################################################3
########################################################################################################3
########################################################################################################3
########################################################################################################3
#HS 2008-07-09: self.TAmb was not found below. for the moment a fixed number
#        self.TAmb = 20
########################################################################################################3
########################################################################################################3
########################################################################################################3
########################################################################################################3

#       ***GETTING_STARTED***:
#   The area should be imported from the QGenerationHC equipment parameters
#   A solar system should be entered like any other heat supply equipment
#   into the QGenerationHC - Table. We should think about how to match the
#   parameters there with characteristic solar parameters
#   e.g. PNom for solar systems = the nominal solar system power
#   -> SurfaceAreaSol = PNom / 0.7

#        SurfAreaSol = 100.0       #E.F. this is self.totNetSurfArea


###HS2008-07-09: Changede equipe.HCGPnom to PNom. => once imported to a local variable, better
# use the local variable from this on. also necessary for the new security feature !!!!!

        SurfAreaSol = PNom/0.7
        if equipe.ST_SysEff != None and 0< equipe.ST_SysEff <1:
            systemEfficiency = equipe.ST_SysEff
        else:
            systemEfficiency = 0.90
#   N.B. In questo caso sarebbe bene mettere uno showWorning fuori dal calculateEnergyFlows che avvisa che l'efficienza del sistema è stata assunta 0.9
#        systemEfficiency = 0.90         #accounting for all the thermal losses in the solar system
                                    #including pipe and tank losses

        ST_C0=equipe.ST_C0
        ST_C1=equipe.ST_C1
        ST_C2=equipe.ST_C2
        
        if equipe.ST_K50T > 0 and equipe.ST_K50T is not None: ST_K50T = equipe.ST_K50T
        else: ST_K50T = 0.95
        
        if equipe.ST_K50L > 0 and equipe.ST_K50L is not None: ST_K50L = equipe.ST_K50L
        else: ST_K50L = 0.95
    
#       ***GETTING_STARTED***:
#   These are the parameters for storage modelling:

        TStorage = 20.0                 #initial temperature of the storage at 1st of January 0:00
        TStorageMax = 250.0             #maximum allowed temperature in the storage
        if equipe.ST_Volume != None:
            if equipe.ST_Volume < 0.01* equipe.HCGPnom:
                storageVolume = 0.01* equipe.HCGPnom
                showWarning(_("The heat storage volume is very small. For internal calculation it has been setted to 0.01 m^3/kW"))
            else:
                storageVolume = equipe.ST_Volume
        else:
            storageVolume = 0.05*SurfAreaSol       #in m3. for the moment fixed to 50 l/m2. can be an equipment parameter
            equipe.ST_Volume = storageVolume
            Status.SQL.commit()
#        storageVolume = 0.05*SurfAreaSol       #in m3. for the moment fixed to 50 l/m2. can be an equipment parameter
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
        annualGbT =0
        annualGdT =0
        HPerYear = 0
        annualDemand=0
        totalSolarEnergy =0
#        print "moduleST;calculateEnergyFlows: number of time intervals evaluated: ",Status.Nt
        for it in range(Status.Nt):

        
            time_in_h = it * TIMESTEP
            time_in_s = time_in_h * HOUR

            nday = int(ceil(time_in_h/24.0))

#            print "DAY: %s Hour: %s Sec: %s"%(nday,time_in_h,time_in_s)

#.............................................................................
# recalculate solar data for a new day

#       ***GETTING_STARTED***:
#   The function PREP_SUN prepares the radiation calculations for a given day
#   in the year

            if nday > oldDay:
                oldDay = nday
#HS2008-07-10: Multiplication with EXTRAPOLATE_TO_YEAR added. so a full solar year will be
#               simulated also if calculation time is less than 8760 !!!
                nday_solar = int(nday*Status.EXTRAPOLATE_TO_YEAR + 0.1)
#                print "ModuleST (calculateEnergyFlows): new day %s, I = %s"%(nday,I)
                sunOnH.t = getDailyRadiation(I,nday_solar)
#                print "ModuleST (calculateEnergyFlows): sunOnH = ",sunOnH

                prep_sun(self.latitude,
                         self.inclination,
                         self.azimuth,
                         nday_solar,
                         sunAnglesOnSurface,
                         sunOnH)

#.............................................................................
# now get instantaneous radiation (in W/m2)
#HS 2008-07-23 RADIATION CALCULATION CORRECTED !!!!

            GT_W = sun_hourly(sunAnglesOnSurface,sunOnH,time_in_s)

            
            GbT = GT_W.b / 1000.    #conversion to kW/m2
            GdT = GT_W.d / 1000.
            GT = GT_W.t / 1000.

# calculation of tan(incidence_angle). needed later on for efficiency calculation.

            print "ModuleST (cEF): dirSunOnT = ",GT_W.n
            if GT_W.n[2] <= 0:
                tanThetaT = INFINITE
                tanThetaL = INFINITE
            else:
                tanThetaT = fabs(GT_W.n[0]/GT_W.n[2])
                tanThetaL = fabs(GT_W.n[1]/GT_W.n[2])
            print "ModuleST (cEF): tanThetaT %s tanThetaL %s"%(tanThetaT,tanThetaL)
                
            annualGbT += GbT * TIMESTEP
            annualGdT += GdT * TIMESTEP
#.............................................................................
# calculate maximum solar system output, heat demand and storage capacity

#   The working temperature of the solar system is the temperature
#   of the storage tank at the beginning of the time-step plus a Delta_T
#   accounting for the heat exchanger in the primary loop

            deltaT_primary = 7.0
            TStorage = QStorage/CStorage
            TavCollector = TStorage + deltaT_primary    #=working temperature of the collector in the present time step
            
            DeltaT = TavCollector - self.TAmb

# Moved this out from here: assignment of constant parameters has to be done only once, not every timestep
#            ST_C0=equipe.ST_C0
#            ST_C1=equipe.ST_C1
#            ST_C2=equipe.ST_C2
#            ST_K50T = equipe.ST_K50T
#            ST_K50L = equipe.ST_K50L

            eff = collectorEfficiencyBiaxial(GT_W.b,GT_W.b,tanThetaL,tanThetaT,DeltaT,ST_C0,ST_C1,ST_C2,ST_K50L,ST_K50T)

            dotQuSolarMax = eff*systemEfficiency*SurfAreaSol*GT*self.shLoss
                                                    #*shadingFactor!!!  if shaded then add shading factor.ADD an IF!
            dotQuSolarMax = max(dotQuSolarMax,0)    #HS2008-07-10: Security feature for negative efficiency
                                #maximum instantaneous power the solar system may deliver
            print"ModuleST; calculateEnergyFlows: the istant. eff. is'%s', the deltaT is'%s' and GH.t is'%s'"%\
                            (eff,DeltaT,GT_W.t)
#            print"ModuleST; calculateEnergyFlows: the istantaneous deltaT is",DeltaT


#       ***GETTING_STARTED***:
#   general Note: I used the "dot" to distinguish between power and energy.
#   we could adapt the calculations using the energy-fraction in time interval: dQ = dotQ*TIMESTEP
#   as is used in the EINSTEIN - arrays ...
#   dotQDemand should be set to the heat demand below TStorage (dotQDemand * TIMESTEP = QD_Tt[TStorage])

            iTmax = (int(floor(Tmax/Status.TemperatureInterval+0.5)))
            dotQDemand = QD_Tt[iTmax][it]/Status.TimeStep

#       ***GETTING_STARTED***:
#   the minimum temperature of demand indicates to what temperature the storage can be cooled down.
#   if we have heat demand only above e.g. 60ºC, we cannot cool down the storage lower than this,
#   as heat can not be transferred from cold to hot (at least not yet, maybe EINSTEIN succeeds to do it)

            iTmin = NT+1
            for i in range(NT+1):
                if QD_Tt[i][it] > 0:
                    iTmin = i
                    break

            TMinDemand = iTmin*Status.TemperatureInterval

            QStorageCapacity = max(QStorageMax - QStorage,0.0)   #maximum amount of heat that still can be fed into the storage
            dotQuSolar = min(dotQDemand+QStorageCapacity/TIMESTEP,dotQuSolarMax)
                                                        #solar production constrained by demand + remaining storage capacity

            QStorageMin = CStorage*TMinDemand           #minimum heat that has to remain within the storage, as it can't be cooled down further
            dotQuSupply = min(dotQDemand,dotQuSolar + max((QStorage - QStorageMin)/TIMESTEP,0))
                                                        #supply constrained by solar production + available heat stored at T > TMinDemand

            if dotQuSolar > 0:
                HPerYear += Status.TimeStep
                
            USHj_t = dotQuSupply*TIMESTEP
            annualDemand += dotQDemand * TIMESTEP    

#       ***GETTING_STARTED***:
#   note: the remaining problem is to decide at WHAT temperature the solar system does supply heat (from USHj_t to USHj_Tt)
#   -> let's use the simplest possible solution (although it's not the most efficient one ...):
#   fill up the demand from below (-> see heat pump example, I think there the same strategy
#   is applied. you can copy ...

            for iT in range(NT+2):
                USHj_Tt[iT][it] = min(USHj_t,QD_Tt[iT][it])
                QD_Tt[iT][it] -= USHj_Tt[iT][it]

# now update heat stored in tank
            QStorage += (dotQuSolar - dotQuSupply)*TIMESTEP

#            print "ModuleST (energyFlows): it=%s QsolMax=%s QD =%s USH=%s QStorage=%s"%\
#                  (it,dotQuSolarMax,dotQDemand,dotQuSupply,QStorage)

            QavColl += dotQuSolar
            QTavColl += dotQuSolar*TavCollector

            USHj += USHj_t
            totalSolarEnergy += GT*TIMESTEP
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

        self.TavCollMean = QTavColl/max(QavColl,0.000000001)

#........................................................................
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

#        equipeC.USHj = USHj
#        equipeC.QHXj = QHXj    #XXX to be defined in data base
#        print "Total energy demand ",annualDemand, " kWh"
        print "ModuleST; calulateEnegyFlows. Total energy supplied by equipment: ",USHj, " kWh"
        print "ModuleST; calulateEnegyFlows. Total energy supplied by the sun: ",totalSolarEnergy*Status.EXTRAPOLATE_TO_YEAR, " kWh/m^2year"
#        print "Total waste heat input  ",QHXj, " kWh"
        print "ModuleST; calulateEnegyFlows. Radiation annualGbT is '%s' and annualGdT is'%s'" % (annualGbT*Status.EXTRAPOLATE_TO_YEAR,annualGdT*Status.EXTRAPOLATE_TO_YEAR)
        Status.int.cascadeUpdateLevel = cascadeIndex

#........................................................................
# Global results (annual energy flows)

        Status.int.USHj[cascadeIndex-1] = USHj*Status.EXTRAPOLATE_TO_YEAR

        FETFuel_j = 0.0

        Status.int.FETFuel_j[cascadeIndex-1] = FETFuel_j*Status.EXTRAPOLATE_TO_YEAR
        Status.int.FETel_j[cascadeIndex-1] = 0.02*USHj*Status.EXTRAPOLATE_TO_YEAR
        Status.int.HPerYearEq[cascadeIndex-1] = HPerYear

        return USHj*Status.EXTRAPOLATE_TO_YEAR    


#==============================================================================
#==============================================================================
#==============================================================================
    def resetST(self):
        self.atmosfericFlag = 0
        self.surfaceFlag = 0
#==============================================================================
    def generalData(self):
        
        renTable = Status.DB.qrenewables.Questionnaire_id[Status.PId]
        if len (renTable)>0 and renTable[0].Latitude!=None:
            self.latitude=renTable[0].Latitude
        else:
            self.latitude=45
#........................................................................
# Function from Claudia to calculate the radiatin
        if len (renTable)>0 and renTable[0].ST_I != None:
            if 100 < renTable[0].ST_I <3000:
                self.ST_IDefault = renTable[0].ST_I
            else:
                self.ST_IDefault = -0.0002*pow(self.latitude,4.0)+0.2547*pow(self.latitude,3.0)-31.055*pow(self.latitude,2.0)+1245.4*self.latitude-14419
        else:
            self.ST_IDefault = -0.0002*pow(self.latitude,4.0)+0.2547*pow(self.latitude,3.0)-31.055*pow(self.latitude,2.0)+1245.4*self.latitude-14419

#........................................................................

        if  len (renTable)>0 and renTable[0].TAmb!=None:
            self.TAmb = renTable[0].TAmb
        else:
            self.TAmb = -0.0143*pow(self.latitude,2.0) + 0.4668*self.latitude+20.5
        self.surfAreaFactorDef=0.0042*pow(self.latitude,2.0)-0.3044*self.latitude+8
        print "ModuleST;generalData. The radiation is:", self.ST_IDefault
        self.atmosfericFlag=1
#==============================================================================
    def defineCalcParams(self):
        MININCLINATION=20
        
        
        if len(self.usableSurfaces)==1:
            if self.usableSurfaces[0]["inclination"]!= None and   self.usableSurfaces[0]["inclination"]>MININCLINATION:
                inclinationOpt=self.usableSurfaces[0]["inclination"]
            else:
                inclinationOpt=self.latitude -10

            if self.usableSurfaces[0]["azimuth"] != None:
                azimuthOpt = self.usableSurfaces[0]["azimuth"]
            else:
                azimuthOpt = 0
            if self.allShaded==1:
                shLoss=0.8
            else:
                shLoss=1
        else:
            azimuthOpt = 0
            shLoss=1
            inclinationOpt=self.latitude -10

        self.surfaceFlag = 1
        return (inclinationOpt,azimuthOpt,shLoss)
            

#------------------------------------------------------------------------------

    def screenSurfaces(self):
#------------------------------------------------------------------------------


        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' "%(Status.PId,Status.ANo)
        self.renewablesTable = Status.DB.qrenewables.sql_select(sqlQuery)  # This DB doesn't exist jet!!
        self.surfaces=[0]
        if len(self.renewablesTable) > 0:
            self.renewables = self.renewablesTable[0]
            self.latitude = self.renewables[i].Latitude
            self.radiation = self.renewables.ST_I
            
        else:
            #xxxx here some security feature, if no table entry exists for latitude and radiation ... -
            pass

        sqlQuery = "ProjectId = '%s'"%(Status.PId)
        self.qsurfareas= Status.DB.qsurfarea.sql_select(sqlQuery)  # This DB doesn't exist jet!!

        self.surfaces=[]
        for qsurfarea in self.qsurfareas:
             self.surfaces.append({"surfAreaName":qsurfarea.SurfAreaName,\
                                   "surfArea":qsurfarea.SurfArea,\
                                   "inclination":qsurfarea.Inclination,\
                                   "azimuth":qsurfarea.Azimuth,\
                                   "azimuthClass":qsurfarea.AzimuthClass,\
                                   "shading":qsurfarea.Shading,\
                                   "distance":qsurfarea.Distance,\
                                   "roofType":qsurfarea.RoofType,\
                                   "roofStaticLoadCap":qsurfarea.RoofStaticLoadCap,\
                                   "enclBuildGroundSketch":qsurfarea.Sketch,\
                                   "ST_ibT":qsurfarea.ST_IbT,\
                                   "ST_IT":qsurfarea.ST_IT})

#if inclination, azimuth, azimuthClass, shading are None we assume some default value!!!

        for i in range(len(self.surfaces)):
            if self.surfaces[i]["inclination"] == None:
                self.surfaces[i]["inclination"] = 0
            if self.surfaces[i]["azimuth"] == None:
                self.surfaces[i]["azimuth"] =0
            if self.surfaces[i]["azimuthClass"] == None:
                self.surfaces[i]["azimuthClass"] = "S"
                                  
        self.NSurfaces= len(self.surfaces)
        
#------------------------------------------------------------------------------
    def calcNetSurfAreaFactor (self,i,MININCLINATION):
        NetSurfAreaFactorSloped=1.2
        if self.surfaces[i]["azimuthClass"]=="S" and  self.surfaces[i]["inclination"]>MININCLINATION:
            self.NetSurfAreaFactor=NetSurfAreaFactorSloped
        else:
            self.NetSurfAreaFactor=0.0042*pow(self.latitude,2.0)-0.3044*self.latitude+8
#------------------------------------------------------------------------------        
    def checkNetSurfArea(self,i):
        MINSURFACE = 20
        NetSurfAreaPartial=self.surfaces[i]["surfArea"]/self.NetSurfAreaFactor
        if NetSurfAreaPartial>=MINSURFACE:
            f1=1
        else:
            f1=0
            logMessage(_("In '%s' the surface available for the collectors mounting is too small.")%(self.surfaces[i]["surfAreaName"]))
        return (f1,NetSurfAreaPartial)
#------------------------------------------------------------------------------
    def checkDistance(self,i):
        DISTANCECONSTRAINT= 1500
        DistanceFactor=(-2*0.0000001*pow(self.surfaces[i]["surfArea"],2))+(0.0022*self.surfaces[i]["surfArea"])+0.3938
        MaxDistance=self.surfaces[i]["surfArea"]/(DistanceFactor*self.NetSurfAreaFactor)
        if self.surfaces[i]["distance"]!=None and self.surfaces[i]["distance"] > min(DISTANCECONSTRAINT , MaxDistance):
            f2=0
            logMessage(_("Distance between the solar field'%s' and the technical room or process is too long")%\
                       (self.surfaces[i]["surfAreaName"]))
        else:
            f2=1
        return (f2)
#------------------------------------------------------------------------------
    def checkOrientation(self,i):
        MININCLINATION = 20
        if self.surfaces[i]["azimuthClass"]==("N" or "NE" or "NW"):
            if self.surfaces[i]["inclination"]<MININCLINATION:
                f3=1
            else:
                f3=0
                logMessage(_("Area '%s' oriented to North:not suitable.")%\
                       (self.surfaces[i]["surfAreaName"]))
        else:
            f3=1
        return (f3)       
#------------------------------------------------------------------------------
    def checkShading(self,i):
        if self.surfaces[i]["shading"] == "Yes,fully shaded": #==SHADINGTYPES.keys()[2]
            f4=0
            fs=1
            logMessage(_("Area '%s' shaded: not suitable for collectors mounting.")%(self.surfaces[i]["surfAreaName"]))
        else:
            f4=1
            if self.surfaces[i]["shading"] == "Yes,partially shaded" :
                fs=1
            else:
                fs=0
        return (f4,fs)          
#------------------------------------------------------------------------------
    def checkLoad(self,i):
        if self.surfaces[i]["roofStaticLoadCap"] ==None:
            f5=1
            if self.surfaces[i]["roofType"] in ["Corrugated metal roof","Composite sandwich panels","Other"]:
                logMessage(_("Check the static load capacity of the roof '%s'and the collectors mounting feasibility.")%(self.surfaces[i]["surfAreaName"]))
        elif self.surfaces[i]["roofStaticLoadCap"]>=MINSTATICROOF:
            f5=1
        else:
            f5=0
        return(f5)
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def calcSurfArea(self):

        MINSURFACE=20  # The minimum area considered is 20 m^2
        DISTANCECONSTRAINT=1500
        MININCLINATION=20
        MAXINCLINATION = 90
        self.MINTOTNETSURFAREA = 40
        NetSurfAreaFactorSloped=1.2
        MINSTATICROOF= 25 
        self.allShaded=1
        self.usableSurfacesArea=0
        self.usableSurfaces=[]
        self.usableSurfacesData=[]
        self.TotAvailSurfArea=0
        self.grossSurfArea=0
        self.screenSurfaces()
        
        for i in range(self.NSurfaces):
#            if latitude: if>70 and >20°data entering error
            if self.surfaces[i]["inclination"]>MAXINCLINATION:
                showWarning(_("Check surface '%s' inclination: out of range.")%(self.surfaces[i]["surfAreaName"]))
            self.calcNetSurfAreaFactor(i,MININCLINATION)
            (f1,NetSurfAreaPartial)=self.checkNetSurfArea(i)
            f2=self.checkDistance(i)
            f3=self.checkOrientation(i)
            f4,fs=self.checkShading(i)
            if self.surfaces[i]["roofType"] in ["Corrugated metal roof","Composite sandwich panels","Other","Concrete roof","Tilted roof"]:
                f5=self.checkLoad(i)
            else:
                f5=1
            self.grossSurfArea += NetSurfAreaPartial*f1*f2*f3*f4*f5
            self.TotAvailSurfArea += self.surfaces[i]["surfArea"]
            self.usableSurfacesArea += self.surfaces[i]["surfArea"]*f1*f2*f3*f4*f5
            if f1*f2*f3*f4*f5==1:
                self.allShaded= self.allShaded*fs
                self.usableSurfaces.append(self.surfaces[i])
                self.usableSurfacesData.append({"NetSurfAreaFactor":self.NetSurfAreaFactor,"NetSurfAreaPartial":NetSurfAreaPartial})
        avAreaFactor=self.avAreaFactor
        self.TotNetSurfArea=self.grossSurfArea/avAreaFactor
        if self.TotNetSurfArea < self.MINTOTNETSURFAREA:
            showWarning(_("The surface available for the collectors mounting is quite small."))
            enoughSurface= "No"
        else:
            enoughSurface= "Yes"
        logTrack ("The list of aveilable surfaces is:'%s'"% self.surfaces)
        logTrack ("The list of usable surfaces is:'%s'"% self.usableSurfaces)
        logMessage(_("The surfaces have a total area of '%s' and a usable (net) area of '%s'"% (self.TotAvailSurfArea,self.TotNetSurfArea)))
        return enoughSurface

                
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def findIndex(self):
        index=0
        Status.int.getEquipmentCascade()
        i=0
        self.STExistance=0
        for row in Status.int.cascade:
            if getEquipmentClass(row["equipeType"]) == "ST" and index==0:
                self.existingSTSystem = row
                index= i
                print ("A solar sistem exist and its position in cascade is:", index+1)
                self.STExistance=1
            i += 1
        return (index)
        
#------------------------------------------------------------------------------
#          if Status.UserInteractionLevel == "interactive" or Status.UserInteractionLevel == "semi-automatic":


#------------------------------------------------------------------------------
    def selectST(self,GT,dT):

        print(" ModuleST: selectST is starting")

#------------------------------------------------------------------------------
#       here a selection among all the collectors based on efficiency.
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
        config = noneFilter(self.getUserDefinedPars())
        if config[1] in ("Flat-plate collector", "Evacuated tube collector", "Concentrating collector"):
            if config[1] =="Flat-plate collector":
                sqlQuery="STManufacturer = '%s' AND STType = '%s'"%("Einstein","Flat-plate collector")
                possibleCollector = Status.DB.dbsolarthermal.sql_select(sqlQuery)
            if config[1] =="Evacuated tube collector":
                sqlQuery="STManufacturer = '%s' AND STType = '%s'"%("Einstein","Evacuated tube collector")
                possibleCollector = Status.DB.dbsolarthermal.sql_select(sqlQuery)
            if config[1] =="Concentrating collector":
                sqlQuery="STManufacturer = '%s' AND STType = '%s'"%("Einstein","Concentrating collector")
                possibleCollector = Status.DB.dbsolarthermal.sql_select(sqlQuery)
        else:
            sqlQuery="STManufacturer = '%s'"%("Einstein")
            possibleCollector = Status.DB.dbsolarthermal.sql_select(sqlQuery)
#------------------------------------------------------------------------------
        self.a=0
        STc0=possibleCollector[0].STc0
        STc1=possibleCollector[0].STc1
        STc2=possibleCollector[0].STc2
        self.etaSelected=collectorEfficiency(GT,dT,STc0,STc1,STc2)
        for i in range (1,len(possibleCollector)):
            STc0=possibleCollector[i].STc0
            STc1=possibleCollector[i].STc1
            STc2=possibleCollector[i].STc2
            etaCollector=collectorEfficiency(GT,dT,STc0,STc1,STc2)
            if etaCollector>self.etaSelected:
                self.etaSelected=etaCollector
                self.a=i
        selectedCollector=possibleCollector[self.a]
        self.avAreaFactor = selectedCollector.STAreaGross/selectedCollector.STAreaAper
        return selectedCollector
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

    def preDimensioning(self):

        print (" ModuleST: preDimensioning is starting") 

        self.solFraDefault=0.5
        self.Tmax=200
        SolFra=self.solFraDefault  # Later on solarFra will be entered from the GUI. Right?
        QuSolarUnitary=500
        deltaT_Primary=7
        
        index=self.findIndex()
        self.QD_Tmax=Status.int.QD_T_mod[index][int(self.Tmax/Status.TemperatureInterval+0.5)]
        QDTav=self.QD_Tmax*SolFra
        print ("the cumulative heat demand QD_T for the ST system is:", Status.int.QD_T_mod[index])
        i=0
        while Status.int.QD_T_mod[index][i]< QDTav:
            i+=1
        self.Tav= i*Status.TemperatureInterval
        print ("The temperature corresponding to half of the demand at 200°C is:",self.Tav)
        USHSolTot= QDTav
        self.SurfAreaSol=USHSolTot /QuSolarUnitary
        if self.TotNetSurfArea/self.SurfAreaSol<1:
            self.SurfAreaSol=self.TotNetSurfArea
            self.QDT=self.SurfAreaSol*QuSolarUnitary/SolFra
            QDTav=self.QDT*SolFra
            i=0
            while Status.int.QD_T_mod[index][i]< QDTav:
                i +=1
            self.Tav= i*Status.TemperatureInterval

        else:
            self.QDT=self.QD_Tmax
        self.TavCollector= self.Tav + deltaT_Primary

# NB       if da userDefinedPars arriva una potenza più picola ridurre direttamente qui la superficie...
        print ("The solar area is:",self.SurfAreaSol)
        print ("corresponding to '%s' kWh" % self.QDT)
        print ("The temperature corresponding to half of the demand is:",self.Tav)
# Data now calculated in self.generalData
#        renTable = Status.DB.qrenewables.Questionnaire_id[Status.PId]
#        if len(renTable) > 0:
#            self.Lat = renTable[0].Latitude
#            self.TAmb = renTable[0].TAmb
                       
#        else:
#            self.Lat = 45
#            self.TAmb = 20
#            print "ERROR: No line in sql for this project!"
        
#        if self.TAmb == None or self.TAmb < -20 or self.TAmb >40:
#            self.TAmb=20
#        if self.Lat == None or  self.Lat <20 or self.Lat>75:
#            self.Lat=45
        
 
        
#==============================================================================    

    def designAssistant1(self):

        print "ModuleST (designAssistant1): starting"
        index=self.findIndex()   # Index = cascadeIndex-1

        config=self.getUserDefinedPars()       

        if config[0]!= None:
            self.desiredSolarFraction=config[0]/100
        else:
            self.desiredSolarFraction= 0.5
        if config[2]!= None:
            self.QuSolarUnitaryMin= config[2]
        else:
            self.QuSolarUnitaryMin=300
#        test=self.QuSolarUnitaryMin*1.02
        if self.STExistance==1:
            showWarning(_("A solar thermal system is in use! in order to design a new one you should delete the existent."))
        else:    
            enoughSurface=self.calcSurfArea()
            logTrack ("ModuleST designAssistant: reached pointA")
            if enoughSurface=="Yes":
                logTrack ("ModuleST designAssistant: reached pointB")
                self.preDimensioning()

                GT=800
                dT=self.Tav-self.TAmb    
                selectedCollector=self.selectST(GT,dT)

                equipe=self.addEquipmentDummy()
                modelID=selectedCollector.DBSolarThermal_ID
                self.setEquipmentFromDB(equipe,modelID)
                equipe.HCGPnom = self.SurfAreaSol*0.7
                equipe.ST_Volume = self.SurfAreaSol*0.05
                equipe.ST_SysEff = 0.9
                Status.SQL.commit()
#                Status.mod.moduleHC.cascadeMoveToTop(self.NEquipe+1)

                USHj=self.calculateEnergyFlows(equipe,1)


                SolFraCalc=USHj/self.QD_Tmax
                logTrack ("ModuleST designAssistant: reached pointC")
                while abs (self.TavCollMean -self.Tav)>10 :
                    logTrack ("ModuleST designAssistant: reached pointD")
                    self.Tav=self.TavCollMean
                    GT=800
                    dT=self.Tav-self.TAmb
                    selectedCollector=self.selectST(GT,dT)
                    modelID=selectedCollector.DBSolarThermal_ID
#                    equipe.CascadeIndex=1
                    self.setEquipmentFromDB(equipe,modelID)
                    USHj=self.calculateEnergyFlows(equipe,1)
                SolFraCalc=USHj/self.QD_Tmax
                logTrack ("ModuleST designAssistant: reached pointE")

                nMaxiter=3
                n=1
                while n< nMaxiter:
                    logTrack ("ModuleST designAssistant: reached pointF")
                    USHj=self.calculateEnergyFlows(equipe,1)
                    logTrack ("The total energy supplyed by the solar system is:'%s'" % USHj)
                    logTrack ("At the averege temperature of:'%s'" % self.TavCollMean)
                    SolFraCalc=USHj/self.QD_Tmax
                    A=equipe.HCGPnom/0.7
                    logTrack ("The aperture area is:'%s'" % A)
                    QuSolarUnitary=USHj/A
                    logTrack ("The QuSolarUnitary is:'%s'" % QuSolarUnitary)
                    if QuSolarUnitary < self.QuSolarUnitaryMin:
                        logTrack ("ModuleST designAssistant: reached pointG")
                        A=A*QuSolarUnitary/(self.QuSolarUnitaryMin*1.02)
                        A=max(A,self.MINTOTNETSURFAREA/self.avAreaFactor)
                        logTrack ("The new aperture area is:'%s'" % A)
                        equipe.HCGPnom = A*0.7
                        equipe.ST_Volume = A*0.05
                        Status.SQL.commit()
                        n +=1
                        if A == self.MINTOTNETSURFAREA/self.avAreaFactor : pass
                        continue
                    else:
#                        test2=A*QuSolarUnitary/(self.QuSolarUnitaryMin*1.02)
                        if abs(SolFraCalc-self.desiredSolarFraction) > 0.05:   #  In this way we reduce the solar fraction when it exceed 0.5: even if the QuSolarUnitary is good enough
                            logTrack ("ModuleST designAssistant: reached pointH")
                            logTrack ("ModuleST designAssistant: SolFraCalc= '%s' self.desiredSolarFraction='%s'" %(SolFraCalc,self.desiredSolarFraction))
                            A1 = A*QuSolarUnitary/self.QuSolarUnitaryMin
                            A2 = A*self.desiredSolarFraction/SolFraCalc
                            k=0.8
                            A3 = k*A2+(1-k)*A
                            A4= min (A3,self.TotNetSurfArea)
                            A5= selectedCollector.STAreaAper * int((A4/selectedCollector.STAreaAper)+0.5)
#                            if A4/selectedCollector.STAreaAper - int(A4/selectedCollector.STAreaAper) >0.5:
#                                A5 = selectedCollector.STAreaGross*int(A4/selectedCollector.STAreaAper)
#                            else:
#                                A5 = selectedCollector.STAreaGross*(int(A4/selectedCollector.STAreaAper)+1)
                            A = min(A1,A5)
                            A = max(A,self.MINTOTNETSURFAREA/self.avAreaFactor)
                            equipe.HCGPnom = A*0.7
                            Status.SQL.commit()
                            n +=1
                            if A==self.MINTOTNETSURFAREA/self.avAreaFactor: pass
                            continue
                        else:
                            break

                    n +=1
                
                logTrack ("ModuleST designAssistant: reached pointI")
                A=equipe.HCGPnom/0.7
                NColl=int((A/selectedCollector.STAreaAper)+0.1)
                equipe.HCGPnom = NColl*selectedCollector.STAreaAper*0.7
                Status.SQL.commit()
                USHj=self.calculateEnergyFlows(equipe,1)
                logTrack ("ModuleST designAssistant: reached pointL")
#------------------------------------------------------------------------------
#   Here all the data to be displayed or registered are calculated.

                k30 = selectedCollector.STUnitTurnKeyPrice30kW
                k300 = selectedCollector.STUnitTurnKeyPrice300kW
                k3000 = selectedCollector.STUnitTurnKeyPrice3000kW
                unitPrice300= selectedCollector.STUnitPrice300kW
                OM = selectedCollector.STOMUnitFix
                scf = SolarCostFunction(k30,k300,k3000,unitPrice300,OM)

                (equipe.TurnKeyPrice,equipe.Price,equipe.OandMfix) = scf.calculate(equipe.HCGPnom)
                equipe.ST_Volume = 0.05*equipe.HCGPnom/0.7
                Status.SQL.commit()
                logTrack ("ModuleST designAssistant: reached pointM")

                print ("The total heat supplied by the solar system in a year is:'%s'kWh"% USHj)
                SF=USHj/self.QD_Tmax
                print "It corresponds to a solar fraction of:",SF
                print ("The nominal power of the solar system is:'%s'kW" % equipe.HCGPnom)
                QuSolarUnitary=USHj/equipe.HCGPnom
                print ("The yield of the solar system is:'%s'kWh/kw" %QuSolarUnitary)
                print ("The averege working temperature of the system is'%s'°C" %self.TavCollMean)
                print ("The collector is a '%s' of the '%s' "%(equipe.EquipTypeFromDB,equipe.Manufact))
                GT=800
                dT=self.TavCollMean- self.TAmb
                STc0 = selectedCollector.STc0
                STc1 = selectedCollector.STc1
                STc2 = selectedCollector.STc2
                eta = collectorEfficiency(GT,dT,STc0,STc1,STc2)
                print "Its efficiency is:", eta
                storVol = equipe.ST_Volume
                print "The volume of the solar storage is:", storVol
                logTrack ("ModuleST designAssistant: reached pointN")
            else:
                showWarning(_("The suitable surfaces are quite small. Einstein suggests not to install a solar system"))


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
