# -*- coding: iso-8859-15 -*-
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    SpreadsheetUtils.py : 
#							SpreadsheetDict: Dictionarys for Database Translation
# 							Utils: writing into the Database, transform lists and data
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by:     André Rattinger 29/03/2010
#
#------------------------------------------------------------------------------
#    (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#    http://www.energyxperts.net/
#
#    This program is free software: you can redistribute it or modify it under
#    the terms of the GNU general public license as published by the Free
#    Software Foundation (www.gnu.org).
#
#==============================================================================

import re

class SpreadsheetDict():

    @staticmethod
    def _U(text):
        try:
            return unicode(_(text),"utf-8")
        except:
            return _(text)

    @staticmethod
    def normDecimalPlace(number):
        """
        returns valid float values for the database
        """
        try:
            return float(str(number).replace(',', '.'))
        except:
            return "no valid number" 

    @staticmethod
    def parseDate(date):
        if date != None:
            split = re.split('\W+', date)
            #print split
            for elem in split:
                try:
                    int(elem)
                except:
                    return None, None
            if len(split)<4:
                return "2007-"+ split[0]+"-"+"01", "2007-"+ split[1]+"-"+"01"
            
            return "2007-"+ split[1]+"-"+split[0], "2007-"+ split[3]+"-"+split[2]
        else:
            return None, None
        
    @staticmethod
    def charDateParse(date):
        if date != None:
            split = re.split('\W+', date)
            return str(split[0]), str(split[1])
        else:
            return None, None
    @staticmethod
    def createQuestionnaireDictionary(Q1,db_conn):
        Q1dict = {}

        Q1dict['Name']= Q1[0]
        Q1dict['City']= Q1[2]
        Q1dict['Contact']= Q1[4]
        Q1dict['Role']= Q1[6]
        Q1dict['Address']= Q1[8]
        Q1dict['Phone']= Q1[10]
        Q1dict['Fax']= Q1[12]
        Q1dict['Email']= Q1[14]
        Q1dict['DescripIndustry']= Q1[16]
        Q1dict['Branch']= Q1[18]
        #Q1dict['NACE']=Q1[20]  
        Q1dict['SubBranch']=Q1[22]
        #Q1dict['SubNACE']=Q1[24]
        try:
            Q1dict['NEmployees']= int(Q1[26])
            Q1dict['Turnover']= float(Q1[27])
            Q1dict['ProdCost']= float(Q1[28])
            Q1dict['BaseYear']= float(Q1[29])
            Q1dict['Growth']= float(Q1[30])
            Q1dict['OMThermal']= float(Q1[32])
            Q1dict['OMElectrical']= float(Q1[33])
            Q1dict['HPerDayInd']= float(Q1[34])
            Q1dict['NShifts']= int(Q1[38])
            Q1dict['NDaysInd']= int(Q1[42])
        except:
            error = "Value-error"
        
        if Q1[31]=="no":
            Q1dict['Independent']= 0
        else: Q1dict['Independent']= 1
        #Q1dict['NoProdStart']= Q1[46]
        #Q1dict['NoProdStop']= Q1[47]
        
        Q1dict['PercentElTotcost']= Q1[50]
        Q1dict['PercentFuelTotcost']= Q1[51]
    
        #Q1dict['']= Q1[]
        
        return Q1dict
    
    @staticmethod
    def createNACEDictionary(Q1,db_conn):
        NACEDict = {}
        NACEDict['NACE']=Q1[20]  
        NACEDict['SubNACE']=Q1[24]  
        return NACEDict
    
    @staticmethod
    def createQProductDictionary(QProduct,db_conn):
        qproddict = {}
        qproddict['Product'] = QProduct[0]
        qproddict['ProductCode'] = QProduct[1]
        qproddict['QProdYear'] = QProduct[2]
        qproddict['ProdUnit'] = QProduct[3]
        qproddict['TurnoverProd'] = QProduct[4]
        qproddict['FuelProd'] = QProduct[5]
        qproddict['ElProd'] = QProduct[6]
        
        qproddict['AlternativeProposalNo'] = -1
        
        return qproddict
    
    @staticmethod
    def createQFuelDictionary(QFuel,db_conn):
        QFuelDict = {}
        try:
            DBFuelSel = db_conn.dbfuel.sql_select('FuelName = "' + str(QFuel[0])+ '"')
            QFuelDict['DBFuel_id'] = DBFuelSel[0]["DBFuel_ID"]
        except:
            pass
        QFuelDict['FuelUnit'] = QFuel[1]
        QFuelDict['MFuelYear'] = QFuel[2]
        QFuelDict['FECFuel'] = QFuel[3]
        QFuelDict['FuelTariff'] = QFuel[4]
        QFuelDict['FuelCostYear'] = QFuel[5]
        
        QFuelDict['AlternativeProposalNo'] = -1
        return QFuelDict
    
    @staticmethod
    def createQElectricityDictionary(Q2,db_conn):
        

        
        Q2dict = {}
        Q2dict['ElectricityPeakYear']= Q2[36]
        Q2dict['ElectricityStandYear']= Q2[37]
        Q2dict['ElectricityValleyYear']= Q2[38]
        Q2dict['ElectricityTotYear']= Q2[39]
        #Q2dict['']= Q2[40]
        #Q2dict['']= Q2[41]
        Q2dict['PowerContrPeak']= Q2[42]
        Q2dict['PowerContrStd']= Q2[43]
        Q2dict['PowerContrVall']= Q2[44]
        Q2dict['PowerContrTot']= Q2[45]
        #Q2[46] empty
        #Q2[47] empty
        Q2dict['ElTariffClassPeak']= Q2[48]
        Q2dict['ElTariffClassStd']= Q2[49]
        Q2dict['ElTariffClassTotVall']= Q2[50]
        Q2dict['ElTariffClassTot']= Q2[51]
        #Q2[52] empty
        Q2dict['ElTariffClassCHP']= Q2[53]
        Q2dict['ElTariffPowPeak']= Q2[54]
        Q2dict['ElTariffPowStd']= Q2[55]
        Q2dict['ElTariffPowVall']= Q2[56]
        Q2dict['ElTariffPowTot']= Q2[57]
        #Q2[58] none
        Q2dict['ElTariffPowCHP']= Q2[59]
        Q2dict['ElTariffCPeak']= Q2[60]
        Q2dict['ElTariffCStd']= Q2[61]
        Q2dict['ElTariffCVall']= Q2[62]
        Q2dict['ElTariffCTot']= Q2[63]
        #Q2[64] none
        Q2dict['ETariffCHP']= Q2[65]
        Q2dict['ElCostYearPeak']= Q2[66]
        Q2dict['ElCostYearStd']= Q2[67]
        Q2dict['ElCostYearVall']= Q2[68]
        Q2dict['ElCostYearTot']= Q2[69]
        #Q2[70] none
        Q2dict['ElSalesYearCHP']= Q2[71]
        #Q2[72] - Q[83] none
        Q2dict['ElectricityRef']= Q2[84]
        Q2dict['ElectricityAC']= Q2[85]
        Q2dict['ElectricityThOther']= Q2[86]
        Q2dict['ElectricityMotors']= Q2[87]
        Q2dict['ElectricityChem']= Q2[88]
        Q2dict['ElectricityLight']= Q2[89]
        
        Q2dict['AlternativeProposalNo'] = -1
        return Q2dict

    @staticmethod
    def createQProcessDictionary(Q3,db_conn):
        i =0
        for elem in Q3:
            print str(i) + " " + str(elem)
            i=i+1
        
        Q3dict = {}
        Q3dict['EquipIDFromDB'] = 1
        Q3dict['Process'] = Q3[0]
        Q3dict['Description'] = Q3[1]
        Q3dict['ProcType']= Q3[2]
        try:
            dbunitop = db_conn.dbunitoperation.sql_select("UnitOperation"+"='"+str(Q3[3])+"'")
            Q3dict['DBUnitOperation_id']= dbunitop[0]['DBUnitOperation_ID']
            dbfluid = db_conn.dbfluid.sql_select("FluidName"+"='"+str(Q3[4])+"'")
            # Test if all values e.g. Air Water Steam are correct or build exception or log
            Q3dict['ProcMedDBFluid_id']= dbfluid[0]['DBFluid_ID']
        except:
            pass
        
        Q3dict['PT']= SpreadsheetDict.normDecimalPlace(Q3[6])
        Q3dict['PTInFlow']= SpreadsheetDict.normDecimalPlace(Q3[7])
        Q3dict['PTInFlowRec']= SpreadsheetDict.normDecimalPlace(Q3[8])
        
        Q3dict['mInFlowNom']= SpreadsheetDict.normDecimalPlace(Q3[9])
        Q3dict['VInFlowCycle']= SpreadsheetDict.normDecimalPlace(Q3[10])
        Q3dict['VolProcMed']= SpreadsheetDict.normDecimalPlace(Q3[12])
        Q3dict['PTStartUp']= SpreadsheetDict.normDecimalPlace(Q3[13])
        Q3dict['QOpProc']= SpreadsheetDict.normDecimalPlace(Q3[15])
        Q3dict['HeatRecOK']= Q3[16]
        
        try:
            dbfluid = db_conn.dbfluid.sql_select("FluidName"+"='"+str(Q3[17])+"'")
            Q3dict['ProcMedOut']= dbfluid[0]['DBFluid_ID']
        except:
            pass
        #Q3dict['ProcMedOut']= Q3[17]
        
        Q3dict['PTOutFlow']= SpreadsheetDict.normDecimalPlace(Q3[18])
        Q3dict['HOutFlow']= SpreadsheetDict.normDecimalPlace(Q3[19])
        Q3dict['XOutFlow']= SpreadsheetDict.normDecimalPlace(Q3[20])
        Q3dict['PTFinal']= SpreadsheetDict.normDecimalPlace(Q3[21]) 
        
        Q3dict['mOutFlowNom']= SpreadsheetDict.normDecimalPlace(Q3[22])
        Q3dict['VOutFlowNom']= SpreadsheetDict.normDecimalPlace(Q3[23])
        Q3dict['HPerDayProc']= Q3[24]
        Q3dict['NBatch']= Q3[25]
        Q3dict['HBatch']= Q3[26]
        Q3dict['NDaysProc']= Q3[27]
        
        try:
            dbfluid = db_conn.dbfluid.sql_select("FluidName"+"='"+str(Q3[28])+"'")
            Q3dict['SupplyMedDBFluid_id']= dbfluid[0]['DBFluid_ID']
        except:
            pass
        Q3dict['PipeDuctProc']= Q3[29]
        Q3dict['TSupply']= Q3[30]
        Q3dict['SupplyMedFlow']= Q3[31]   
        Q3dict['UPH']= Q3[32]
        Q3dict['ScheduleTolerance']= Q3[33]
        Q3dict['StartUpDuration']= Q3[34]
        Q3dict['InFlowDuration']= Q3[34]
        Q3dict['HBatch']= Q3[35]+Q3[34]
        Q3dict['OutFlowDuration']= Q3[36]
        
        Q3dict['AlternativeProposalNo'] = -1
        
        return Q3dict
    
    @staticmethod
    def createProfilesDictionary(QProfiles,db_conn):
        QPdict = {}
        weekdays = ["monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                    "sunday"
                    ]
        QPdict['name'] = QProfiles[len(QProfiles)-1]
        for i in xrange(len(weekdays)):
            if QProfiles[i]=='X' or QProfiles[i]=='x':
                QPdict[weekdays[i]]=1
            else:
                QPdict[weekdays[i]]=0
                
        return QPdict
    
    # Database connect
    
    @staticmethod
    def createIntervalDictionary(QInterval,db_conn):
        return {"start" : QInterval[0],"stop" : QInterval[1], "scale" : 100}
    
    
    @staticmethod
    def createProfileIntervals(QProfiles, QIntervals, db_conn):
        i =0
#        for elem in QProfiles:
#            print str(i) + " " + str(elem)
#            i=i+1
        profileID = []
        for i in xrange(3):
            try:
                profileID = db_conn.profiles.insert(SpreadsheetDict.createProfilesDictionary(QProfiles[i], db_conn))
                #profid = db_conn.profiles.sql_select("name"+"='"+QProfiles[i][-1]+"'")
                #profileID.append(profid[-1]['id'])
            except:
                pass
        intervalID = []
        
        for i in xrange(len(QIntervals)/2):
            try:
                interval = SpreadsheetDict.createIntervalDictionary([QIntervals[i],QIntervals[len(QIntervals)/2+i]], db_conn)
                intervalID = db_conn.intervals.insert(interval)
                #interid = db_conn.intervals.sql_select("LAST_INSERT_ID()")
                #intervalID.append(interid[-1]['id'])
            except:
                pass
        
        for j in xrange(30):
            try:
                db_conn.profile_intervals.insert({"profiles_id" : profileID[int(j/10)], "intervals_id" : intervalID[j]})
            except:
                pass
        
    @staticmethod
    def createProcessPeriodsDictionary(processName, db_conn, profileName):
        
        PPD = {}
        PPD['step']=1
        PPD['scale']=100
        
        try:
            periodsDict = {"start" : "2007-01-01", "stop" : "2007-12-31"}
            periodsSel = db_conn.periods.insert(periodsDict)
            #periodsSel = db_conn.periods.sql_select("LAST_INSERT_ID()")
            #periodsSel = periodsSel[-1]['id']

            PPD['periods_id']=periodsSel
            
            processid = db_conn.qprocessdata.sql_select("Process"+"='"+processName+"'")
            PPD['qprocessdata_QProcessData_ID']= processid[-1]['QProcessData_ID']
            PPID = db_conn.process_periods.insert(PPD)
            
            #PPID = db_conn.process_periods.sql_select("LAST_INSERT_ID()")
            #PPID = PPID[-1]['id']
            
            profilesID = db_conn.profiles.sql_select("name"+"='"+profileName+"'")
            profilesID = profilesID[-1]['id']
            
            db_conn.process_period_profiles.insert({'process_periods_id' : PPID, 'profiles_id' : profilesID})
        except:
            pass
        
    @staticmethod
    def createProcessScheduleCorrDictionary(Q3n, db_conn):

        for i in xrange(3):
            try:
                sourceID = db_conn.qprocessdata.sql_select("Process"+"='"+Q3n[111+i]+"'")
                sourceID = sourceID[-1]['QProcessData_ID']
                targetID = db_conn.qprocessdata.sql_select("Process"+"='"+Q3n[i]+"'")
                targetID = targetID[-1]['QProcessData_ID']
                db_conn.process_schedules_correlations.insert({'source' : sourceID, 'target' : targetID})
            except:
                pass
            
    @staticmethod
    def createQ4HDictionary(Q4H,db_conn):

        Q4Hdict = {}
        Q4Hdict["Equipment"] = Q4H[0]
        Q4Hdict["Manufact"] = Q4H[1]
        Q4Hdict["YearManufact"] = Q4H[2]
        Q4Hdict["Model"] = Q4H[3]
        Q4Hdict["EquipType"] = Q4H[4]
        Q4Hdict["NumEquipUnits"] = Q4H[5]
        Q4Hdict["HCGPnom"] = Q4H[8]
        try:
            DBFuelSel = db_conn.dbfuel.sql_select('FuelName = "' + str(Q4H[9])+ '"')
            Q4Hdict['DBFuel_id'] = DBFuelSel[0]["DBFuel_ID"]
        except:
            pass
        Q4Hdict["FuelConsum"] = Q4H[10]
        Q4Hdict["UnitsFuelConsum"] = Q4H[11]
        Q4Hdict["ElectriConsum"] = Q4H[12]
        Q4Hdict["HCGTEfficiency"] = Q4H[13]
        Q4Hdict["PartLoad"] = Q4H[14]
        Q4Hdict["TExhaustGas"] = Q4H[16]
        Q4Hdict["ExcessAirRatio"] = Q4H[17]
        Q4Hdict["ElectriProduction"] = Q4H[19]
        Q4Hdict["HCGEEfficiency"] = Q4H[20]
        Q4Hdict["PipeDuctEquip"] = Q4H[24]
        Q4Hdict["HeatSourceLT"] = Q4H[26]
        Q4Hdict["THeatSourceLT"] = Q4H[27]
        Q4Hdict["Refrigerant"] = Q4H[28]
        Q4Hdict["ThermalConsum"] = Q4H[30]
        Q4Hdict["THeatSourceHT"] = Q4H[31]
        Q4Hdict["HeatSourceHT"] = Q4H[32]
        Q4Hdict["HPerDayEq"] = Q4H[35]
        Q4Hdict["NDaysEq"] = Q4H[36]
        
        Q4Hdict['AlternativeProposalNo'] = -1
        return Q4Hdict
        
    @staticmethod
    def createQ4CDictionary(Q4C,db_conn):
        Q4Cdict = {}
        Q4Cdict["Equipment"] = Q4C[0]
        Q4Cdict["Manufact"] = Q4C[1]
        Q4Cdict["YearManufact"] = Q4C[2]
        Q4Cdict["Model"] = Q4C[3]
        Q4Cdict["EquipType"] = Q4C[4]
        Q4Cdict["NumEquipUnits"] = Q4C[5]
        Q4Cdict["HCGPnom"] = Q4C[8]
        Q4Cdict["Refrigerant"] = Q4C[9]
        Q4Cdict["ElectriConsum"] = Q4C[10]
        Q4Cdict["HCGTEfficiency"] = Q4C[11]
        Q4Cdict["PartLoad"] = Q4C[12]
        Q4Cdict["FuelConsum"] = Q4C[14]
        Q4Cdict["UnitsFuelConsum"] = Q4C[15]
        Q4Cdict["PipeDuctEquip"] = Q4C[19]
        Q4Cdict["DestinationWasteHeat"] = Q4C[21]
        Q4Cdict["TemperatureReCooling"] = Q4C[22]
        Q4Cdict["ThermalConsum"] = Q4C[23]
        Q4Cdict["THeatSourceHT"] = Q4C[24]
        Q4Cdict["HeatSourceHT"] = Q4C[25]
        Q4Cdict["HPerDayEq"] = Q4C[28]
        Q4Cdict["NDaysEq"] = Q4C[29]
        
        Q4Cdict['AlternativeProposalNo'] = -1
        return Q4Cdict
    
    @staticmethod
    def createQ5Dictionary(Q5,Questionnaire_ID, db_conn):
        Q5dict = {}
        Q5dict["Pipeduct"] = Q5[0]
        dbfluid = db_conn.dbfluid.sql_select("FluidName"+"='"+str(Q5[1])+"'")
        Q5dict["HeatDistMedium"]= dbfluid[0]['DBFluid_ID']
        
        #Q5dict["HeatDistMedium"] = Q5[1]
        Q5dict["DistribCircFlow"] = Q5[2]
        Q5dict["ToutDistrib"] = Q5[3]
        Q5dict["TreturnDistrib"] = Q5[4]
        Q5dict["PercentRecirc"] = Q5[5]
        Q5dict["Tfeedup"] = Q5[6]
        Q5dict["PressDistMedium"] = Q5[7]
        Q5dict["TotLengthDistPipe"] = Q5[8]
        Q5dict["UAPipe"] = Q5[9]
        Q5dict["DDistPipe"] = Q5[10]
        Q5dict["DeltaDistPipe"] = Q5[11]
        Q5dict["NumStorageUnits"] = Q5[14]
        Q5dict["VtotStorage"] = Q5[15]
        Q5dict["TypeStorage"] = Q5[16]
        Q5dict["PmaxStorage"] = Q5[17]
        Q5dict["TmaxStorage"] = Q5[18]
        Q5dict['AlternativeProposalNo'] = -1
        Q5dict['Questionnaire_id'] = Questionnaire_ID
        return Q5dict
    
    @staticmethod
    def createQ6Dictionary(Q6,db_conn):
        Q6dict={}
        Q6dict["HXName"] = Q6[0]
        Q6dict["HXType"] = Q6[1]
        Q6dict["QdotHX"] = Q6[2]
        Q6dict["HXLMTD"] = Q6[3]
        Q6dict["QHX"] = Q6[4]
        Q6dict["HXSource"] = Q6[5]
        Q6dict["HXTSourceInlet"] = Q6[6]
        Q6dict["HXhSourceInlet"] = Q6[7]
        Q6dict["HXTSourceOutlet"] = Q6[8]
        Q6dict["HXhSourceOutlet"] = Q6[9]
        Q6dict["HXSink"] = Q6[10]
        Q6dict["HXTSinkInlet"] = Q6[11]
        Q6dict["HXTSinkOutlet"] = Q6[12]
        Q6dict['AlternativeProposalNo'] = -1
        return Q6dict
    
    @staticmethod
    def createQ6EDictionary(Q6,db_conn):
        Q6dict={}
        Q6dict["WHEEName"] = Q6[16]
        Q6dict["WHEEEqType"] = Q6[17]
        Q6dict["WHEEWasteHeatType"] = Q6[18]
        Q6dict["QWHEE"] = Q6[19]
        Q6dict["WHEEMedium"] = Q6[20]
        Q6dict["WHEEFlow"] = Q6[21]
        Q6dict["WHEETOutlet"] = Q6[22]
        Q6dict["WHEEPresentUse"] = Q6[23]
        
        Q6dict["HPerDayWHEE"] = Q6[26]
        Q6dict["NBatchWHEE"] = Q6[27]
        Q6dict["HBatchWHEE"] = Q6[28]
        Q6dict["NDaysWHEE"] = Q6[29]
        Q6dict['AlternativeProposalNo'] = -1
        return Q6dict
    
    @staticmethod
    def createQ7Dictionary(Q7,db_conn):
        Q7dict = {}
        
        if str(Q7[0]).lower()=="yes":
            Q7dict["REInterest"] = 1
        elif str(Q7[0]).lower()=="no":
            Q7dict["REInterest"] = 0
            
        REReason = ""    
        for i in xrange(4):
            if(str(Q7[i]).upper() == "YES" or str(Q7[i]).upper() == "Y"):
                REReason+= "y"
            else:
                REReason+= "n"
                
        Q7dict["REReason"] = REReason
        if Q7[4]!="":
            Q7dict["REMotivation"] = Q7[4]
        Q7dict["Latitude"] = Q7[5]
        # Belongs to Surface Q7dict["ST_IT"] = Q7[6]
        Q7dict["BiomassFromProc"] = Q7[7]
        Q7dict["BiomassFromRegion"] = Q7[8]
        
        # inserted SQL Date causes exception in current "Renewable Energy" Tab
        
#        startdate, enddate = SpreadsheetDict.charDateParse(Q7[9])
#        Q7dict["PeriodBiomassRegionStart"] = startdate
#        Q7dict["PeriodBiomassRegionStop"] = enddate
#        startdate, enddate = SpreadsheetDict.parseDate(Q7[10])
#        Q7dict["PeriodBiomassProcStart"] = startdate
#        Q7dict["PeriodBiomassProcStop"] = enddate
        Q7dict["QBiomassProc"] = Q7[11]
        Q7dict["QBiomassRegion"] = Q7[12]
        Q7dict["LCVBiomassProc"] = Q7[13]
        Q7dict["LCVBiomassRegion"] = Q7[14]
        Q7dict["HumidBiomassProc"] = Q7[15]
        Q7dict["HumidBiomassRegion"] = Q7[16]
        Q7dict["PriceBiomassProc"] = Q7[17]
        Q7dict["PriceBiomassRegion"] = Q7[18]
        Q7dict["SpaceBiomassProc"] = Q7[21]
        
        Q7dict['AlternativeProposalNo'] = -1
        return Q7dict        
    
    
    @staticmethod
    def createQSurfDictionary(QSurfarea,db_conn):
        QSurfdict = {}
        QSurfdict['SurfAreaName'] = QSurfarea[0]
        QSurfdict['SurfArea'] = QSurfarea[1]
        QSurfdict['Inclination'] = QSurfarea[2]
        QSurfdict['AzimuthClass'] = QSurfarea[3]
        QSurfdict['Shading'] = QSurfarea[4]
        QSurfdict['Distance'] = QSurfarea[5]
        QSurfdict['RoofType'] = QSurfarea[6]
        QSurfdict['RoofStaticLoadCap'] = QSurfarea[7]
        if str(QSurfarea[8]).lower() == "yes": 
            QSurfdict['Sketch'] = 1
        elif str(QSurfarea[8]).lower()== "no":
            QSurfdict['Sketch'] = 0
    
        return QSurfdict
    
    @staticmethod
    def createQ8Dictionary(Q8,db_conn):
        Q8dict = {}
    
#        index = 0
#        for elem in Q8:
#            print str(index) + ". " + str(elem)
#            index+=1
    
        Q8dict['BuildName'] = Q8[0]
        Q8dict['BuildConstructSurface'] = Q8[1]
        Q8dict['BuildUsefulSurface'] = Q8[2]
        Q8dict['BuildUsage'] = Q8[3]
        
        Q8dict['BuildHoursOccup'] = Q8[5]
        Q8dict['BuildDaysInUse'] = Q8[6]
        # Date Q8dict[''] = Q8[7]
        
        Q8dict['BuildMaxHP'] = Q8[9]
        Q8dict['BuildMaxCP'] = Q8[10]
        Q8dict['BuildAnnualHeating'] = Q8[11]
        Q8dict['BuildAnnualAirCond'] = Q8[12]
        Q8dict['BuildDailyDHW'] = Q8[13]
        Q8dict['BuildTHeating'] = Q8[14]
        Q8dict['BuildTAirCond'] = Q8[15]
        
        datestart, dateend = SpreadsheetDict.parseDate(Q8[7])
        if datestart != None:
            Q8dict['BuildHolidaysPeriodStart_1'] = datestart
        if dateend != None:
            Q8dict['BuildHolidaysPeriodStop_1'] = dateend
        # date Q8dict[''] = Q8[16]
        # date Q8dict[''] = Q8[17]
        datestart, dateend = SpreadsheetDict.parseDate(Q8[16])
        if datestart != None:
            Q8dict['BuildHeatingPeriodStart'] = datestart
        if dateend != None:
            Q8dict['BuildHeatingPeriodStop'] = dateend
            
        datestart, dateend = SpreadsheetDict.parseDate(Q8[17])
        if datestart != None:
            Q8dict['BuildAirCondPeriodStart'] = datestart
        if dateend != None:
            Q8dict['BuildAirCondPeriodStop'] = dateend
        
        Q8dict['AlternativeProposalNo'] = -1
        
        return Q8dict
    
    @staticmethod
    def createQ9dictionary(Q9,db_conn):
        Q9dict = {}
        Q9dict["InflationRate"] = Q9[0]
        Q9dict["FuelPriceRate"] = Q9[1]
        Q9dict["InterestExtFinancing"] = Q9[2]
        Q9dict["PercentExtFinancing"] = Q9[3]
        Q9dict["CompSpecificDiscountRate"] = Q9[4]
        Q9dict["AmortisationTime"] = Q9[5]
        Q9dict["OMGenTot"] = Q9[6]
        Q9dict["OMGenUtilities"] = Q9[7]
        Q9dict["OMGenLabour"] = Q9[8]
        Q9dict["OMGenExternal"] = Q9[9]
        Q9dict["OMGenRegulatory"] = Q9[10]
        Q9dict["OMBuildTot"] = Q9[12]
        Q9dict["OMBuildUtilities"] = Q9[13]
        Q9dict["OMBuildLabour"] = Q9[14]
        Q9dict["OMBuildExternal"] = Q9[15]
        Q9dict["OMBuildRegulatory"] = Q9[16]
        Q9dict["OMMachEquipTot"] = Q9[18]
        Q9dict["OMMachEquipUtilities"] = Q9[19]
        Q9dict["OMMachEquipLabour"] = Q9[20]
        Q9dict["OMMachEquipExternal"] = Q9[21]
        Q9dict["OMMachEquipRegulatory"] = Q9[22]
        
        Q9dict["OMHCGenDistTot"] = Q9[24]
        Q9dict["OMHCGenDistUtilities"] = Q9[25]
        Q9dict["OMHCGenDistLabour"] = Q9[26]
        Q9dict["OMHCGenDistExternal"] = Q9[27]
        Q9dict["OMHCGenDistRegulatory"] = Q9[28]
        
        Q9dict["OMTotalTot"] = Q9[30]
        Q9dict["OMTotalUtilities"] = Q9[31]
        Q9dict["OMTotalLabour"] = Q9[32]
        Q9dict["OMTotalExternal"] = Q9[33]
        Q9dict["OMTotalRegulatory"] = Q9[34]
        if str(Q9[36]).lower() == "yes":
            Q9dict["EnergyManagExisting"] = 1
        elif str(Q9[36]).lower()=="no": 
            Q9dict["EnergyManagExisting"] = 0
        if str(Q9[37]).lower() == "yes":
            Q9dict["EnergyManagExternal"] = 1
        elif str(Q9[37]).lower()=="no":
            Q9dict["EnergyManagExternal"] = 0
        return Q9dict

    @staticmethod
    def createsprojectDictionary(questionnaire_id):
        sp = {}
        sp['ProjectID']=questionnaire_id
        sp['NoOfAlternatives'] = 0
        sp['ActiveAlternative'] = -1
#        sp['WriteProtected'] = 0
#        sp['StatusQ'] = 0
        sp['StatusCC'] = 0
#        sp['StatusCA'] = 0
#        sp['StatusR'] = 0 
#        sp['LanguageReport'] = 'en'
#        sp['UnitsReport'] = 'SI-kWh'
        return sp
        
    
class Utils():
    
    def __init__(self,md,sheetnames):
        self.__md = md
        self.__sheetnames = sheetnames
    
    @staticmethod    
    def tupleToList(tuple):
        data = []
        for elem in tuple:
            data.append(elem.GetValue())
        return data
    
    def splitColumns(self,nr_of_elements, columns, parsed_list,dict,Questionnaire_id,createDictionary,db_table):
        """
        Splits columns of the excel import and inserts them into the Database
        nr_of_elements: Number of Columns that should be inserted into the database (count from left)
        columns: Existing Columns 
        parsed_list: Parsed list from the Excel Worksheet
        dict: additional Dictionary that should be included
        createDictionary: Function that creates the Database Dictionary from the input list
        db_table: pSQL Database Table
        Example Usage: 
        splitExcelColumns(4, 6, QFuel, Questionnaire_ID, createQFuelDictionary,md.qfuel)
        """
        list = []
        for i in xrange(nr_of_elements):
            for j in xrange(0+i,len(parsed_list),columns):
                list.append(parsed_list[j])
            Dict = createDictionary(list,self.__md)
            if Questionnaire_id != "":
                Dict['Questionnaire_id']= Questionnaire_id
            Dict.update(dict)
            db_table.insert(Dict)
            list = []
    
    
    
    @staticmethod
    def parseError(errorname):
        return "Parsing failed because of: " + str(errorname)+ "! Please check your data and try again."
    
    
    def writeToDB(self,lists):
        Q1, Q2, QProduct, QFuel, Q3, QRenewables, QSurf, QProfiles, QIntervals, Q9Questionnaire, Q4_8, latitude = lists


        #try:
#        for i in xrange(3):
#            self.__md.profiles.insert(SpreadsheetDict.createProfilesDictionary(QProfiles[i], self.__md))
#
#        for i in xrange(len(QIntervals)/2):
#            self.__md.intervals.insert(SpreadsheetDict.createIntervalDictionary([QIntervals[i],QIntervals[len(QIntervals)/2+i]], self.__md))
        #except:
         #   return self.parseError(self.__sheetnames[3])
        
        SpreadsheetDict.createProfileIntervals(QProfiles, QIntervals, self.__md)
        
        try:
            Q1dict = SpreadsheetDict.createQuestionnaireDictionary(Q1, self.__md)
            Q9dict = SpreadsheetDict.createQ9dictionary(Q9Questionnaire, self.__md)
            NaceDict = SpreadsheetDict.createNACEDictionary(Q1, self.__md)
            strNace = "CodeNACE = '"+str(Q1[20])+"' AND CodeNACESub ='"+str(int(Q1[24]))+"'"
            dbnacecodeid = self.__md.dbnacecode.sql_select(strNace)
            
            Q1dict.update(Q9dict)
            Q1dict.update({'DBNaceCode_id':dbnacecodeid[0]['DBNaceCode_ID'], 
                           'Branch' : dbnacecodeid[0]['NameNACE'], 
                           'SubBranch' : dbnacecodeid[0]['NameNACEsub']})
            Questionnaire_ID = self.__md.questionnaire.insert(Q1dict)
        except:
            return self.parseError(self.__sheetnames[0])
        
        quest_id = 'Questionnaire_id'
        
        try:
            q2dict = SpreadsheetDict.createQElectricityDictionary(Q2, self.__md)
            q2dict[quest_id]=Questionnaire_ID
            self.__md.qelectricity.insert(q2dict)
        except:
            return self.parseError(self.__sheetnames[1])
        
        Areas = ["Q4H_", "Q4C_", "Q5_", "Q6_", "Q8_"]



        for i in xrange(0,25,5):
            try:
                Q4Hdict = SpreadsheetDict.createQ4HDictionary(Q4_8[i],self.__md)
                Q4Hdict[quest_id]=Questionnaire_ID
                self.__md.qgenerationhc.insert(Q4Hdict)
            except:
                pass
                #return self.parseError(self.__sheetnames[4])
                
            try:    
                Q4Cdict = SpreadsheetDict.createQ4CDictionary(Q4_8[i+1], self.__md)
                Q4Cdict[quest_id]=Questionnaire_ID
                self.__md.qgenerationhc.insert(Q4Cdict)
            except:
                pass
                #return self.parseError(self.__sheetnames[5])
            
            try:
                self.__md.qdistributionhc.insert(SpreadsheetDict.createQ5Dictionary(Q4_8[i+2], Questionnaire_ID, self.__md))
            except:
                pass
                #return self.parseError(self.__sheetnames[6])
            
            try:
                projectid = {'ProjectID':Questionnaire_ID}
                Q6Dict = SpreadsheetDict.createQ6Dictionary(Q4_8[i+3], self.__md)
                Q6Dict.update(projectid)
                self.__md.qheatexchanger.insert(Q6Dict)
                #self.__md.qheatexchanger.insert(SpreadsheetDict.createQ6Dictionary(Q4_8[i+3], self.__md))
                Q6EDict = SpreadsheetDict.createQ6EDictionary(Q4_8[i+3], self.__md)
                Q6EDict.update(projectid)
                self.__md.qwasteheatelequip.insert(Q6EDict)
            except:
                pass
                #return self.parseError(self.__sheetnames[7])
                
            try:
                Q8dict = SpreadsheetDict.createQ8Dictionary(Q4_8[i+4], self.__md)
                Q8dict[quest_id]=Questionnaire_ID
                self.__md.qbuildings.insert(Q8dict)
            except:
                pass
                #return self.parseError(self.__sheetnames[9])
                
                
                
        try:
            QRenewables = SpreadsheetDict.createQ7Dictionary(QRenewables, self.__md)
            QRenewables[quest_id] = Questionnaire_ID
            self.__md.qrenewables.insert(QRenewables)
        except:
            return self.parseError(self.__sheetnames[8])
        
        
        self.splitColumns(3, 5, QProduct, {}, Questionnaire_ID ,SpreadsheetDict.createQProductDictionary,self.__md.qproduct)
        self.splitColumns(6, 6, QFuel, {}, Questionnaire_ID ,SpreadsheetDict.createQFuelDictionary,self.__md.qfuel)
        
        self.splitColumns(4, 4, QSurf, {'ST_IT':latitude[1], 'ProjectID':Questionnaire_ID}, "", SpreadsheetDict.createQSurfDictionary, self.__md.qsurfarea)

        try:
            # Code to skip a specific amount of columns
            index =0
            Q3n = []
            for i in range(0,len(Q3),3):
                Q3n.append(Q3[i]) 
                index+=1
                
            self.splitColumns(3, 3, Q3n, {}, Questionnaire_ID, SpreadsheetDict.createQProcessDictionary,self.__md.qprocessdata)
            #except:
            #    return self.parseError("QProduct, QFuel or QSurfarea")
            for i in xrange(3):
                SpreadsheetDict.createProcessPeriodsDictionary(Q3n[i], self.__md, QProfiles[i][-1])
            
            SpreadsheetDict.createProcessScheduleCorrDictionary(Q3n, self.__md)
        except:
            pass
        print Questionnaire_ID
        self.__md.cgeneraldata.insert({'Questionnaire_id' : Questionnaire_ID, 'AlternativeProposalNo' : -1})
        self.__md.salternatives.insert({'ProjectID' : Questionnaire_ID, 'AlternativeProposalNo' : -1, 'ShortName' : 'New Proposal', 'Description' : 'data set'})
        #self.__md.sproject.insert(SpreadsheetDict.createsprojectDictionary(Questionnaire_ID))

        return "Parsing successful!"
        

    
    
    
    
    