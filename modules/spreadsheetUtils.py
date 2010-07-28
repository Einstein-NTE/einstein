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
import time
from GUITools import *
from units import *
from constants import *

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
            return None

    @staticmethod
    def parseDate(date):
        print type(date)
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
    def parseSpreadsheetDate(date):
        print type(date)
        if date != None:
            split = re.split('\W+', date)
            print split
            print "no split"
            
    
    @staticmethod
    def checkFilledState(Q):
        for i in xrange(len(Q)):
            if str(Q[i]).startswith('Zahl >') or str(Q[i]).startswith('decimals=1, minval'):
                Q[i]=None
        return Q
    
    @staticmethod
    def createQuestionnaireDictionary(Q1,db_conn):
        Q1dict = {}
        Q1 = SpreadsheetDict.checkFilledState(Q1)
        
        
        #Q1dict['Name']= check(Q1[0]) if Q1[0] is not None else time.strftime("%m/%d/%y %H:%M:%S", time.localtime())
        if Q1[0] is not None:
            name = str(Q1[0])
            timestr = " - " + time.strftime("%m/%d/%y %H:%M:%S", time.localtime())
            namelen = 45 - len(timestr)
            name = name[0:namelen:]
            name += timestr
            Q1dict['Name'] = check(name, 45)
        else:
            Q1dict['Name'] = check(time.strftime("%m/%d/%y %H:%M:%S", time.localtime()), 45)
        Q1dict['City']= check(Q1[2], 45)
        Q1dict['Contact']= check(Q1[4], 45)
        Q1dict['Role']= check(Q1[6], 45)
        Q1dict['Address']= check(Q1[8], 200)
        Q1dict['Phone']= check(Q1[10], 45)
        Q1dict['Fax']= check(Q1[12], 45)
        Q1dict['Email']= check(Q1[14], 45)
        Q1dict['DescripIndustry']= check(Q1[16], 200)
        Q1dict['Branch']= check(Q1[18], 100)
        #Q1dict['NACE']=check(Q1[20]  
        Q1dict['SubBranch']=check(Q1[22], 100)
        #Q1dict['SubNACE']=check(Q1[24]
        try:
            try: Q1dict['NEmployees']= check(int(Q1[26]))
            except: Q1dict['NEmployees']= check(None)
            try: Q1dict['Turnover']= check(float(Q1[27]) * UNITS["PRICE"]["MEUR"][0])
            except: Q1dict['Turnover']= check(None)
            try: Q1dict['ProdCost']= check(float(Q1[28]) * UNITS["PRICE"]["MEUR"][0])
            except: Q1dict['ProdCost']= check(None)
            try: Q1dict['BaseYear']= check(float(Q1[29]))
            except: Q1dict['BaseYear']= check(None)
            try: Q1dict['Growth']= check(float(Q1[30]))
            except: Q1dict['Growth']= check(None)
            try: Q1dict['OMThermal']= check(float(Q1[32]))
            except: Q1dict['OMThermal']= check(None)
            try: Q1dict['OMElectrical']= check(float(Q1[33]))
            except: Q1dict['OMElectrical']= check(None)
            try: Q1dict['HPerDayInd']= check(float(Q1[34]))
            except: Q1dict['HPerDayInd']= check(None)
            try: Q1dict['NShifts']= check(int(Q1[38]))
            except: Q1dict['NShifts']= check(None)
            try: Q1dict['NDaysInd']= check(int(Q1[42]))
            except: Q1dict['NDaysInd']= check(None)
        except:
            error = "Value-error"
        
        if Q1[31]=="no":
            Q1dict['Independent']= 0
        else: Q1dict['Independent']= 1
        #Q1dict['NoProdStart']= Q1[46]
        #Q1dict['NoProdStop']= Q1[47]
        
        Q1dict['PercentElTotcost']= check(Q1[50])
        Q1dict['PercentFuelTotcost']= check(Q1[51])
    
        #Q1dict['']= Q1[]
        
        return Q1dict
    
    @staticmethod
    def createNACEDictionary(Q1,db_conn):
        NACEDict = {}
        NACEDict['NACE']=check(Q1[20])  
        NACEDict['SubNACE']=check(Q1[24])
        return NACEDict
    
    @staticmethod
    def createQProductDictionary(QProduct,db_conn):
        qproddict = {}
        qproddict['Product'] = check(QProduct[0], 45)
        qproddict['ProductCode'] = check(QProduct[1], 45)
        qproddict['QProdYear'] = check(QProduct[2])
        qproddict['ProdUnit'] = check(QProduct[3], 45)
        try: qproddict['TurnoverProd'] = check(float(QProduct[4]) * UNITS["PRICE"]["MEUR"][0])
        except: qproddict['TurnoverProd'] = check(None)
        try: qproddict['FuelProd'] = check(float(QProduct[5]) * UNITS["ENERGY"]["MWh"][0])
        except: qproddict['TurnoverProd'] = check(None)
        try: qproddict['ElProd'] = check(float(QProduct[6]) * UNITS["ENERGY"]["MWh"][0])
        except: qproddict['TurnoverProd'] = check(None)
        
        qproddict['AlternativeProposalNo'] = -1
        
        return qproddict
    
    @staticmethod
    def createQFuelDictionary(QFuel,db_conn):
        QFuelDict = {}
        try:
            DBFuelSel = db_conn.dbfuel.sql_select('FuelName = "' + str(QFuel[0])+ '"')
            QFuelDict['DBFuel_id'] = DBFuelSel[0]["DBFuel_ID"]
        except:
            QFuelDict['DBFuel_id'] = check(None)
        QFuelDict['FuelUnit'] = check(QFuel[1], 45)
        QFuelDict['MFuelYear'] = check(QFuel[2])
        try: QFuelDict['FECFuel'] = check(float(QFuel[3]) * UNITS["ENERGY"]["MWh"][0])
        except: QFuelDict['FECFuel'] = check(None)
        QFuelDict['FuelTariff'] = check(QFuel[4])
        QFuelDict['FuelCostYear'] = check(QFuel[5])
        
        QFuelDict['AlternativeProposalNo'] = -1
        QFuelDict['FuelNo']=1
        return QFuelDict
    
    @staticmethod
    def createQElectricityDictionary(Q2,db_conn):
        
#        index = 0
#        for elem in Q2:
#            print str(index) + ". " + str(elem)
#            index+=1
        
        Q2dict = {}
        try: Q2dict['ElectricityPeakYear']= check(float(Q2[36]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityPeakYear']= check(None)
        try: Q2dict['ElectricityStandYear']= check(float(Q2[37]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityStandYear']= check(None)
        try: Q2dict['ElectricityValleyYear']= check(float(Q2[38]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityValleyYear']= check(None)
        try: Q2dict['ElectricityTotYear']= check(float(Q2[39]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityValleyYear']= check(None)
        try: Q2dict['ElGenera']= check(float(Q2[40]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityValleyYear']= check(None)
        try: Q2dict['ElSales']= check(float(Q2[41]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityValleyYear']= check(None)
        Q2dict['PowerContrPeak']= check(Q2[42])
        Q2dict['PowerContrStd']= check(Q2[43])
        Q2dict['PowerContrVall']= check(Q2[44])
        Q2dict['PowerContrTot']= check(Q2[45])
        #Q2[46] empty
        #Q2[47] empty
        Q2dict['ElTariffClassPeak']= check(Q2[48], 45)
        Q2dict['ElTariffClassStd']= check(Q2[49], 45)
        Q2dict['ElTariffClassTotVall']= check(Q2[50], 45)
        Q2dict['ElTariffClassTot']= check(Q2[51], 45)
        #Q2[52] empty
        Q2dict['ElTariffClassCHP']= check(Q2[53], 45)
        Q2dict['ElTariffPowPeak']= check(Q2[54])
        Q2dict['ElTariffPowStd']= check(Q2[55])
        Q2dict['ElTariffPowVall']= check(Q2[56])
        Q2dict['ElTariffPowTot']= check(Q2[57])
        #Q2[58] none
        Q2dict['ElTariffPowCHP']= check(Q2[59])
        try: Q2dict['ElTariffCPeak']= check(float(Q2[60]) / UNITS["ENERGYTARIFF"]["%s/MWh"%CURRENCY][0])
        except: Q2dict['ElTariffCPeak']= check(None)
        try: Q2dict['ElTariffCStd']= check(float(Q2[61]) / UNITS["ENERGYTARIFF"]["%s/MWh"%CURRENCY][0])
        except: Q2dict['ElTariffCPeak']= check(None)
        try: Q2dict['ElTariffCVall']= check(float(Q2[62]) / UNITS["ENERGYTARIFF"]["%s/MWh"%CURRENCY][0])
        except: Q2dict['ElTariffCPeak']= check(None)
        try: Q2dict['ElTariffCTot']= check(float(Q2[63]) / UNITS["ENERGYTARIFF"]["%s/MWh"%CURRENCY][0])
        except: Q2dict['ElTariffCTot']= check(None)
        #Q2[64] none
        try: Q2dict['ETariffCHP']= check(float(Q2[65]) / UNITS["ENERGYTARIFF"]["%s/MWh"%CURRENCY][0])
        except: Q2dict['ETariffCHP']= check(None)
        Q2dict['ElCostYearPeak']= check(Q2[66])
        Q2dict['ElCostYearStd']= check(Q2[67])
        Q2dict['ElCostYearVall']= check(Q2[68])
        Q2dict['ElCostYearTot']= check(Q2[69])
        #Q2[70] none
        Q2dict['ElSalesYearCHP']= check(Q2[71])
        #Q2[72] - Q[83] none
        try: Q2dict['ElectricityRef']= check(float(Q2[84]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityRef']= check(None)
        try: Q2dict['ElectricityAC']= check(float(Q2[85]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityRef']= check(None)
        try: Q2dict['ElectricityThOther']= check(float(Q2[86]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityRef']= check(None)
        try: Q2dict['ElectricityMotors']= check(float(Q2[87]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityRef']= check(None)
        try: Q2dict['ElectricityChem']= check(float(Q2[88]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityRef']= check(None)
        try: Q2dict['ElectricityLight']= check(float(Q2[89]) * UNITS["ENERGY"]["MWh"][0])
        except: Q2dict['ElectricityRef']= check(None)
        
        Q2dict['AlternativeProposalNo'] = -1
        return Q2dict

    @staticmethod
    def createQProcessDictionary(Q3,db_conn):
#        i =0
#        for elem in Q3:
#            print str(i) + " " + str(elem)
#            i=i+1
        
        Q3dict = {}
        #Q3dict['EquipIDFromDB'] = 1
        Q3dict['Process'] = check(Q3[0], 45)
        Q3dict['Description'] = check(Q3[1], 200)
        Q3dict['ProcType']= check(Q3[2], 45)
        try:
            dbunitop = db_conn.dbunitoperation.sql_select("UnitOperation"+"='"+str(Q3[3])+"'")
            Q3dict['DBUnitOperation_id']= dbunitop[0]['DBUnitOperation_ID']
        except:
            Q3dict['DBUnitOperation_id'] = check(None)
        try:
            dbfluid = db_conn.dbfluid.sql_select("FluidName"+"='"+str(Q3[4])+"'")
            # Test if all values e.g. Air Water Steam are correct or build exception or log
            Q3dict['ProcMedDBFluid_id']= dbfluid[0]['DBFluid_ID']
        except:
            Q3dict['ProcMedDBFluid_id'] = check(None)
        
        Q3dict['PT']= check(SpreadsheetDict.normDecimalPlace(Q3[6]))
        Q3dict['PTInFlow']= check(SpreadsheetDict.normDecimalPlace(Q3[7]))
        Q3dict['PTInFlowRec']= check(SpreadsheetDict.normDecimalPlace(Q3[8]))
        
        Q3dict['mInFlowNom']= check(SpreadsheetDict.normDecimalPlace(Q3[9]))
        Q3dict['VInFlowCycle']= check(SpreadsheetDict.normDecimalPlace(Q3[10]))
        Q3dict['VolProcMed']= check(SpreadsheetDict.normDecimalPlace(Q3[12]))
        Q3dict['PTStartUp']= check(SpreadsheetDict.normDecimalPlace(Q3[13]))
        Q3dict['QOpProc']= check(SpreadsheetDict.normDecimalPlace(Q3[15]))
        Q3dict['HeatRecOK']= check(Q3[16], 4)
        
        try:
            dbfluid = db_conn.dbfluid.sql_select("FluidName"+"='"+str(Q3[17])+"'")
            Q3dict['ProcMedOut']= dbfluid[0]['DBFluid_ID']
        except:
            Q3dict['ProcMedOut'] = check(None)
        #Q3dict['ProcMedOut']= Q3[17]
        
        Q3dict['PTOutFlow']= check(SpreadsheetDict.normDecimalPlace(Q3[18]))
        try: Q3dict['HOutFlow']= check(float(SpreadsheetDict.normDecimalPlace(Q3[19])) * UNITS["SPECIFICENTHALPY"]["kJ/kg"][0])
        except: Q3dict['HOutFlow']= check(None)
        Q3dict['XOutFlow']= check(SpreadsheetDict.normDecimalPlace(Q3[20]))
        Q3dict['PTFinal']= check(SpreadsheetDict.normDecimalPlace(Q3[21]))
        
        Q3dict['mOutFlowNom']= check(SpreadsheetDict.normDecimalPlace(Q3[22]))
        Q3dict['VOutFlowNom']= check(SpreadsheetDict.normDecimalPlace(Q3[23]))
        Q3dict['HPerDayProc']= check(Q3[24])
        Q3dict['NBatch']= check(Q3[25])
        Q3dict['HBatch']= check(Q3[26])
        Q3dict['NDaysProc']= check(Q3[27])
        
        try:
            dbfluid = db_conn.dbfluid.sql_select("FluidName"+"='"+str(Q3[28])+"'")
            Q3dict['SupplyMedDBFluid_id']= dbfluid[0]['DBFluid_ID']
        except:
            Q3dict['SupplyMedDBFluid_id'] = check(None)
        Q3dict['PipeDuctProc']= check(Q3[29], 45)
        Q3dict['TSupply']= check(Q3[30])
        Q3dict['SupplyMedFlow']= check(Q3[31])
        try: Q3dict['UPH']= check(float(Q3[32]) * UNITS["ENERGY"]["MWh"][0])
        except: Q3dict['UPH']= check(None)
        Q3dict['ScheduleTolerance']= check(Q3[33])
        Q3dict['StartUpDuration']= check(Q3[34])
        Q3dict['InFlowDuration']= check(Q3[34])
        #Q3dict['HBatch']= check(Q3[35]+Q3[34])
        Q3dict['OutFlowDuration']= check(Q3[36])
        
        Q3dict['AlternativeProposalNo'] = -1
        Q3dict['ProcNo'] = 1
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
        return {"start" : check(QInterval[0]),"stop" : check(QInterval[1]), "scale" : 100}
    
    
    @staticmethod
    def createProfileIntervals(QProfiles, QIntervals, db_conn):
        i =0
#        for elem in QProfiles:
#            print str(i) + " " + str(elem)
#            i=i+1
        profileID = []
        for i in xrange(3):
            try:
                profileID.append(db_conn.profiles.insert(SpreadsheetDict.createProfilesDictionary(QProfiles[i], db_conn)))
                #profid = db_conn.profiles.sql_select("name"+"='"+QProfiles[i][-1]+"'")
                #profileID.append(profid[-1]['id'])
            except:
                print "Profile not inserted"
        intervalID = []
        
        for i in xrange(len(QIntervals)/2):
            try:
                interval = SpreadsheetDict.createIntervalDictionary([QIntervals[i],QIntervals[len(QIntervals)/2+i]], db_conn)
                intervalID.append(db_conn.intervals.insert(interval))
                #interid = db_conn.intervals.sql_select("LAST_INSERT_ID()")
                #intervalID.append(interid[-1]['id'])
            except:
                print "Interval not inserted"
        
        for j in xrange(30):
            try:
                db_conn.profile_intervals.insert({"profiles_id" : profileID[int(j/10)], "intervals_id" : intervalID[j]})
            except:
                print "ProfileIntervals not inserted"
        
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
            print "createProcessPeriodsDictionary"
        
    @staticmethod
    def createProcessScheduleCorrDictionary(Q3n, db_conn):

        for i in xrange(3):
            try:
                sourceID = db_conn.qprocessdata.sql_select("Process"+"='"+Q3n[111+i]+"'")
                sourceID = sourceID[-1]['QProcessData_ID']
                targetID = db_conn.qprocessdata.sql_select("Process"+"='"+Q3n[i]+"'")
                targetID = targetID[-1]['QProcessData_ID']
                db_conn.process_schedules_correlations.insert(check({'source' : sourceID, 'target' : targetID}))
            except:
                pass
            
    @staticmethod
    def createQ4HDictionary(Q4H,db_conn, quest_id):

        Q4Hdict = {}
        Q4Hdict["Equipment"] = check(Q4H[0], 45)
        Q4Hdict["Manufact"] = check(Q4H[1], 45)
        Q4Hdict["YearManufact"] = check(Q4H[2])
        Q4Hdict["Model"] = check(Q4H[3], 45)
        Q4Hdict["EquipType"] = check(Q4H[4], 45)
        Q4Hdict["NumEquipUnits"] = check(Q4H[5])
        Q4Hdict["HCGPnom"] = check(Q4H[8])
        try:
            DBFuelSel = db_conn.dbfuel.sql_select('FuelName = "' + str(Q4H[9])+ '"')
            Q4Hdict['DBFuel_id'] = check(DBFuelSel[0]["DBFuel_ID"])
        except:
            Q4Hdict['DBFuel_id'] = check(None)
        Q4Hdict["FuelConsum"] = check(Q4H[10])
        Q4Hdict["UnitsFuelConsum"] = check(Q4H[11], 45)
        Q4Hdict["ElectriConsum"] = check(Q4H[12])
        Q4Hdict["HCGTEfficiency"] = check(Q4H[13])
        Q4Hdict["PartLoad"] = check(Q4H[14])
        Q4Hdict["TExhaustGas"] = check(Q4H[16])
        Q4Hdict["ExcessAirRatio"] = check(Q4H[17])
        Q4Hdict["ElectriProduction"] = check(Q4H[19])
        Q4Hdict["HCGEEfficiency"] = check(Q4H[20])
        
        try:
            Pipeduct = db_conn.qdistributionhc.sql_select('Questionnaire_id = "' 
                                                          + str(quest_id)+ '"'
                                                          + ' AND Pipeduct = "' 
                                                          + str(Q4H[24])+ '"')
            Q4Hdict["PipeDuctEquip"] = Pipeduct[0]["QDistributionHC_ID"]
        except:
            Q4Hdict["PipeDuctEquip"] = check(None)
        
        #Q4Hdict["PipeDuctEquip"] = check(Q4H[24], 45)
        
        
        Q4Hdict["HeatSourceLT"] = check(Q4H[26], 200)
        Q4Hdict["THeatSourceLT"] = check(Q4H[27])
        
        #Q4Hdict["Refrigerant"] = check(Q4H[28])
        try:
            DBFluidSel = db_conn.dbfluid.sql_select('FluidName = "' + str(Q4H[28])+ '"')
            Q4Hdict['Refrigerant'] = DBFluidSel[0]["DBFluid_ID"]
        except:
            Q4Hdict['Refrigerant'] = check(None)
        Q4Hdict["ThermalConsum"] = check(Q4H[30])
        Q4Hdict["THeatSourceHT"] = check(Q4H[31])
        Q4Hdict["HeatSourceHT"] = check(Q4H[32], 200)
        Q4Hdict["HPerDayEq"] = check(Q4H[35])
        Q4Hdict["NDaysEq"] = check(Q4H[36])
        
        Q4Hdict['AlternativeProposalNo'] = -1
        return Q4Hdict
        
    @staticmethod
    def createQ4CDictionary(Q4C,db_conn, quest_id):
        Q4Cdict = {}
        Q4Cdict["Equipment"] = check(Q4C[0], 45)
        Q4Cdict["Manufact"] = check(Q4C[1], 45)
        Q4Cdict["YearManufact"] = check(Q4C[2])
        Q4Cdict["Model"] = check(Q4C[3], 45)
        Q4Cdict["EquipType"] = check(Q4C[4], 45)
        Q4Cdict["NumEquipUnits"] = check(Q4C[5])
        Q4Cdict["HCGPnom"] = check(Q4C[8])
        
        try:
            DBFluidSel = db_conn.dbfluid.sql_select('FluidName = "' + str(Q4C[9])+ '"')
            Q4Cdict['Refrigerant'] = DBFluidSel[0]["DBFluid_ID"]
        except:
            Q4Cdict['Refrigerant'] = check(None)
        
        #Q4Cdict["Refrigerant"] = check(Q4C[9])
        
        Q4Cdict["ElectriConsum"] = check(Q4C[10])
        Q4Cdict["HCGTEfficiency"] = check(Q4C[11])
        Q4Cdict["PartLoad"] = check(Q4C[12])
        Q4Cdict["FuelConsum"] = check(Q4C[14])
        Q4Cdict["UnitsFuelConsum"] = check(Q4C[15], 45)
        
        try:
            Pipeduct = db_conn.qdistributionhc.sql_select('Questionnaire_id = "' 
                                                          + str(quest_id)+ '"'
                                                          + ' AND Pipeduct = "' 
                                                          + str(Q4C[19])+ '"')
            Q4Cdict["PipeDuctEquip"] = Pipeduct[0]["QDistributionHC_ID"]
        except:
            Q4Cdict["PipeDuctEquip"] = check(None)
        
        #Q4Cdict["PipeDuctEquip"] = check(Q4C[19], 45)
        Q4Cdict["DestinationWasteHeat"] = check(Q4C[21], 200)
        Q4Cdict["TemperatureReCooling"] = check(Q4C[22])
        Q4Cdict["ThermalConsum"] = check(Q4C[23])
        Q4Cdict["THeatSourceHT"] = check(Q4C[24])
        Q4Cdict["HeatSourceHT"] = check(Q4C[25], 200)
        Q4Cdict["HPerDayEq"] = check(Q4C[28])
        Q4Cdict["NDaysEq"] = check(Q4C[29])
        
        Q4Cdict['AlternativeProposalNo'] = -1
        return Q4Cdict
    
    @staticmethod
    def createQ5Dictionary(Q5,Questionnaire_ID, db_conn):
        Q5dict = {}
        Q5dict["Pipeduct"] = check(Q5[0], 45)
        try:
            dbfluid = db_conn.dbfluid.sql_select("FluidName"+"='"+str(Q5[1])+"'")
            Q5dict["HeatDistMedium"]= dbfluid[0]['DBFluid_ID']
        except:
            Q5dict["HeatDistMedium"] = check(None)
        
        #Q5dict["HeatDistMedium"] = check(Q5[1])
        Q5dict["DistribCircFlow"] = check(Q5[2])
        Q5dict["ToutDistrib"] = check(Q5[3])
        Q5dict["TreturnDistrib"] = check(Q5[4])
        try: Q5dict["PercentRecirc"] = check(float(Q5[5]) * UNITS["FRACTION"]["%"][0])
        except: Q5dict["PercentRecirc"] = check(None)
        Q5dict["Tfeedup"] = check(Q5[6])
        Q5dict["PressDistMedium"] = check(Q5[7])
        Q5dict["TotLengthDistPipe"] = check(Q5[8])
        Q5dict["UAPipe"] = check(Q5[9])
        try: Q5dict["DDistPipe"] = check(float(Q5[10]) * UNITS["LENGTH"]["mm"][0])
        except: Q5dict["DDistPipe"] = check(None)
        try: Q5dict["DeltaDistPipe"] = check(float(Q5[11]) * UNITS["LENGTH"]["mm"][0])
        except: Q5dict["DeltaDistPipe"] = check(None)
        Q5dict["NumStorageUnits"] = check(Q5[14])
        Q5dict["VUnitStorage"] = check(Q5[15])
        Q5dict["TypeStorage"] = check(Q5[16], 45)
        Q5dict["PmaxStorage"] = check(Q5[17])
        Q5dict["TmaxStorage"] = check(Q5[18])
        Q5dict['AlternativeProposalNo'] = -1
        Q5dict['Questionnaire_id'] = check(Questionnaire_ID)
        
        #Q5dict['PipeDuctNo'] = 1
        return Q5dict
    
    @staticmethod
    def createQ6Dictionary(Q6,db_conn):
        Q6dict={}
        Q6dict["HXName"] = check(Q6[0], 300)
        Q6dict["HXType"] = check(Q6[1], 300)
        Q6dict["QdotHX"] = check(Q6[2])
        try: Q6dict["HXLMTD"] = check(float(Q6[3]) + UNITS["TEMPERATURE"]["K"][1])
        except: Q6dict["HXLMTD"] = check(None)
        try: Q6dict["QHX"] = check(float(Q6[4]) * UNITS["ENERGY"]["MWh"][0])
        except: Q6dict["QHX"] = check(None)
        Q6dict["HXSource"] = check(Q6[5], 300)
        Q6dict["HXTSourceInlet"] = check(Q6[6])
        try: Q6dict["HXhSourceInlet"] = check(float(Q6[7]) * UNITS["SPECIFICENTHALPY"]["kJ/kg"][0])
        except: Q6dict["HXhSourceInlet"] = check(None)
        Q6dict["HXTSourceOutlet"] = check(Q6[8])
        try: Q6dict["HXhSourceOutlet"] = check(float(Q6[9]) * UNITS["SPECIFICENTHALPY"]["kJ/kg"][0])
        except: Q6dict["HXhSourceOutlet"] = check(None)
        Q6dict["HXSink"] = check(Q6[10], 300)
        Q6dict["HXTSinkInlet"] = check(Q6[11])
        Q6dict["HXTSinkOutlet"] = check(Q6[12])
        Q6dict['AlternativeProposalNo'] = -1
        return Q6dict
    
    @staticmethod
    def createQ6EDictionary(Q6,db_conn):
        Q6dict={}
        Q6dict["WHEEName"] = check(Q6[16], 45)
        Q6dict["WHEEEqType"] = check(Q6[17], 45)
        Q6dict["WHEEWasteHeatType"] = check(Q6[18], 45)
        Q6dict["QWHEE"] = check(Q6[19])
        #Q6dict["WHEEMedium"] = check(Q6[20])
        
        try:
            DBFluidSel = db_conn.dbfluid.sql_select('FluidName = "' + str(Q6[20])+ '"')
            Q6dict["WHEEMedium"] = DBFluidSel[0]["DBFluid_ID"]
        except:
            Q6dict["WHEEMedium"] = check(None)
        
        Q6dict["WHEEFlow"] = check(Q6[21])
        Q6dict["WHEETOutlet"] = check(Q6[22])
        Q6dict["WHEEPresentUse"] = check(Q6[23], 45)
        
        Q6dict["HPerDayWHEE"] = check(Q6[26])
        Q6dict["NBatchWHEE"] = check(Q6[27])
        Q6dict["HBatchWHEE"] = check(Q6[28])
        Q6dict["NDaysWHEE"] = check(Q6[29])
        Q6dict['AlternativeProposalNo'] = -1
        Q6dict['WHEENo'] = 1
        return Q6dict
    
    @staticmethod
    def createQ7Dictionary(Q7,db_conn):
        Q7dict = {}
        
        index = 0
        
        for elem in Q7:
            print str(index)+": "+str(elem)
            index+=1
        
        try:
            if str(Q7[0]).lower()=="yes":
                Q7dict["REInterest"] = 1
            else:
                Q7dict["REInterest"] = 0
        except:
            Q7dict["REInterest"] = 0

        REReason = ""    
        for i in xrange(4):
            if(str(Q7[i]).upper() == "YES" or str(Q7[i]).upper() == "Y"):
                REReason+= "y"
            else:
                REReason+= "n"
                
        Q7dict["REReason"] = check(REReason)
        if Q7[4]!="":
            Q7dict["REMotivation"] = check(Q7[4], 45)
        Q7dict["Latitude"] = check(Q7[5])
        # Belongs to Surface Q7dict["ST_IT"] = check(Q7[6])
        Q7dict["BiomassFromProc"] = check(Q7[7], 45)
        Q7dict["BiomassFromRegion"] = check(Q7[8], 45)
        
        # inserted SQL Date causes exception in current "Renewable Energy" Tab
        # varchar(6) in Database..cant insert Date Type
        #Q7dict["PeriodBiomassRegionStart"] = SpreadsheetDict.toMysqlDate(Q7[10])#10
        #Q7dict["PeriodBiomassRegionStop"] = SpreadsheetDict.toMysqlDate(Q7[12])#12
        Q7dict["PeriodBiomassProcStart"] = SpreadsheetDict.toMysqlDate(Q7[9])
        Q7dict["PeriodBiomassProcStop"] = SpreadsheetDict.toMysqlDate(Q7[11])

        Q7dict["QBiomassProc"] = check(Q7[13])
        Q7dict["QBiomassRegion"] = check(Q7[14])
        Q7dict["LCVBiomassProc"] = check(Q7[15])
        Q7dict["LCVBiomassRegion"] = check(Q7[16])
        Q7dict["HumidBiomassProc"] = check(Q7[17])
        Q7dict["HumidBiomassRegion"] = check(Q7[18])
        Q7dict["PriceBiomassProc"] = check(Q7[19])
        Q7dict["PriceBiomassRegion"] = check(Q7[20])
        Q7dict["SpaceBiomassProc"] = check(Q7[23])
        
        Q7dict['AlternativeProposalNo'] = -1
        return Q7dict        
    
    
    @staticmethod
    def createQSurfDictionary(QSurfarea,db_conn):
        QSurfdict = {}
        QSurfdict['SurfAreaName'] = check(QSurfarea[0], 45)
        QSurfdict['SurfArea'] = check(QSurfarea[1])
        QSurfdict['Inclination'] = check(QSurfarea[2])
        QSurfdict['AzimuthClass'] = check(QSurfarea[3], 4)
        QSurfdict['Shading'] = check(QSurfarea[4], 20)
        QSurfdict['Distance'] = check(QSurfarea[5])
        QSurfdict['RoofType'] = check(QSurfarea[6], 45)
        QSurfdict['RoofStaticLoadCap'] = check(QSurfarea[7])
        if str(QSurfarea[8]).lower() == "yes": 
            QSurfdict['Sketch'] = 1
        else:
            QSurfdict['Sketch'] = 0
    
        return QSurfdict
    
    @staticmethod
    def toMysqlDate(date):
        try:
            date = str(date).split(' ')
            time = date[1]
            date = str(date[0]).split('/')
            datetime = date[2]+'-'+date[0]+'-'+date[1]+' '+time
            return datetime
        except:
            return '00-00-00 00:00:00'
        
    @staticmethod
    def createQ8Dictionary(Q8,db_conn):
        Q8dict = {}
        
        Q8dict['BuildName'] = check(Q8[0], 45)
        Q8dict['BuildConstructSurface'] = check(Q8[1])
        Q8dict['BuildUsefulSurface'] = check(Q8[2])
        Q8dict['BuildUsage'] = check(Q8[3], 45)
        
        Q8dict['BuildHoursOccup'] = check(Q8[5])
        Q8dict['BuildDaysInUse'] = check(Q8[6])
        # Date Q8dict[''] = check(Q8[7])
        
        Q8dict['BuildMaxHP'] = check(Q8[10])
        Q8dict['BuildMaxCP'] = check(Q8[11])
        try: Q8dict['BuildAnnualHeating'] = check(float(Q8[12]) * UNITS["ENERGY"]["MWh"][0])
        except: Q8dict['BuildAnnualHeating'] = check(None)
        try: Q8dict['BuildAnnualAirCond'] = check(float(Q8[13]) * UNITS["ENERGY"]["MWh"][0])
        except: Q8dict['BuildAnnualAirCond'] = check(None)
        try: Q8dict['BuildDailyDHW'] = check(float(Q8[14]) / UNITS["VOLUME"]["l"][0])
        except: Q8dict['BuildDailyDHW'] = check(None)
        Q8dict['BuildTHeating'] = check(Q8[15])
        Q8dict['BuildTAirCond'] = check(Q8[16])
     
        Q8dict['BuildHolidaysPeriodStart_1'] = SpreadsheetDict.toMysqlDate(Q8[7])
        Q8dict['BuildHolidaysPeriodStop_1'] = SpreadsheetDict.toMysqlDate(Q8[8])
        Q8dict['BuildHeatingPeriodStart'] = SpreadsheetDict.toMysqlDate(Q8[17])
        Q8dict['BuildHeatingPeriodStop'] = SpreadsheetDict.toMysqlDate(Q8[18])
        Q8dict['BuildAirCondPeriodStart'] = SpreadsheetDict.toMysqlDate(Q8[19])
        Q8dict['BuildAirCondPeriodStop'] = SpreadsheetDict.toMysqlDate(Q8[20])
#        datestart, dateend = SpreadsheetDict.parseDate(Q8[7])
#        if datestart != None:
#            Q8dict['BuildHolidaysPeriodStart_1'] = datestart
#        if dateend != None:
#            Q8dict['BuildHolidaysPeriodStop_1'] = dateend
#            
#        SpreadsheetDict.parseSpreadsheetDate(Q8[8])
#        # date Q8dict[''] = Q8[16]
#        # date Q8dict[''] = Q8[17]
#        datestart, dateend = SpreadsheetDict.parseDate(Q8[17])
#        if datestart != None:
#            Q8dict['BuildHeatingPeriodStart'] = datestart
#        if dateend != None:
#            Q8dict['BuildHeatingPeriodStop'] = dateend
#            
#        SpreadsheetDict.parseSpreadsheetDate(Q8[18])
#            
#        datestart, dateend = SpreadsheetDict.parseDate(Q8[19])
#        if datestart != None:
#            Q8dict['BuildAirCondPeriodStart'] = datestart
#        if dateend != None:
#            Q8dict['BuildAirCondPeriodStop'] = dateend
#        
#        SpreadsheetDict.parseSpreadsheetDate(Q8[20])
        
        Q8dict['AlternativeProposalNo'] = -1
        
        return Q8dict
    
    @staticmethod
    def createQ9dictionary(Q9,db_conn):
        Q9 = SpreadsheetDict.checkFilledState(Q9)
        Q9dict = {}
        try: Q9dict["InflationRate"] = check(float(Q9[0]) * UNITS["FRACTION"]["%"][0])
        except: Q9dict["InflationRate"] = check(None)
        try: Q9dict["FuelPriceRate"] = check(float(Q9[1]) * UNITS["FRACTION"]["%"][0])
        except: Q9dict["FuelPriceRate"] = check(None)
        try: Q9dict["InterestExtFinancing"] = check(float(Q9[2]) * UNITS["FRACTION"]["%"][0])
        except: Q9dict["InterestExtFinancing"] = check(None)
        try: Q9dict["PercentExtFinancing"] = check(float(Q9[3]) * UNITS["FRACTION"]["%"][0])
        except: Q9dict["PercentExtFinancing"] = check(None)
        try: Q9dict["CompSpecificDiscountRate"] = check(float(Q9[4]) * UNITS["FRACTION"]["%"][0])
        except: Q9dict["CompSpecificDiscountRate"] = check(None)
        Q9dict["AmortisationTime"] = check(Q9[5])
        Q9dict["OMGenTot"] = check(Q9[6])
        Q9dict["OMGenUtilities"] = check(Q9[7])
        Q9dict["OMGenLabour"] = check(Q9[8])
        Q9dict["OMGenExternal"] = check(Q9[9])
        Q9dict["OMGenRegulatory"] = check(Q9[10])
        Q9dict["OMBuildTot"] = check(Q9[12])
        Q9dict["OMBuildUtilities"] = check(Q9[13])
        Q9dict["OMBuildLabour"] = check(Q9[14])
        Q9dict["OMBuildExternal"] = check(Q9[15])
        Q9dict["OMBuildRegulatory"] = check(Q9[16])
        Q9dict["OMMachEquipTot"] = check(Q9[18])
        Q9dict["OMMachEquipUtilities"] = check(Q9[19])
        Q9dict["OMMachEquipLabour"] = check(Q9[20])
        Q9dict["OMMachEquipExternal"] = check(Q9[21])
        Q9dict["OMMachEquipRegulatory"] = check(Q9[22])
        
        Q9dict["OMHCGenDistTot"] = check(Q9[24])
        Q9dict["OMHCGenDistUtilities"] = check(Q9[25])
        Q9dict["OMHCGenDistLabour"] = check(Q9[26])
        Q9dict["OMHCGenDistExternal"] = check(Q9[27])
        Q9dict["OMHCGenDistRegulatory"] = check(Q9[28])
        
        Q9dict["OMTotalTot"] = check(Q9[30])
        Q9dict["OMTotalUtilities"] = check(Q9[31])
        Q9dict["OMTotalLabour"] = check(Q9[32])
        Q9dict["OMTotalExternal"] = check(Q9[33])
        Q9dict["OMTotalRegulatory"] = check(Q9[34])
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
    
    @staticmethod
    def sprojectdict(questionnaire_id, salternatives):
        sp = {}
        sp['ProjectID']= questionnaire_id
        sp['NoOfAlternatives']=-1
        sp['ActiveAlternative']=-1
        sp['FinalAlternative']=0
        sp['WriteProtected']=0
        sp['StatusQ']=EINSTEIN_NOTOK
        sp['StatusCC']=EINSTEIN_NOTOK
        sp['StatusCA']=EINSTEIN_NOTOK
        sp['StatusR']=EINSTEIN_NOTOK
        sp['LanguageReport']='english'
        sp['UnitsReport']='SI-kWh'
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
            for key in Dict.keys():
                Dict[key] = check(Dict[key])
            #print Dict
            db_table.insert(Dict)
            list = []
    
    
    
    @staticmethod
    def parseError(errorname):
        return "Parsing failed because of: " + str(errorname)+ "! Please check your data and try again."
    
    
    def writeToDB(self,lists):
        Q1, Q2, QProduct, QFuel, Q3, QRenewables, QSurf, QProfiles, QIntervals, Q9Questionnaire, Q4_8, latitude = lists

        errorlog = []
        
#        profile_id = []
#        try:
#            for i in xrange(3):
#                profile_id.append(self.__md.profiles.insert(SpreadsheetDict.createProfilesDictionary(QProfiles[i], self.__md)))
#    
#            for i in xrange(len(QIntervals)/2):
#                self.__md.intervals.insert(SpreadsheetDict.createIntervalDictionary([QIntervals[i],QIntervals[len(QIntervals)/2+i]], self.__md))
#        except:
#            errorlog.append("Schedule Profiles or Intervals could not be inserted")
#            #return self.parseError(self.__sheetnames[3])
        try:
            SpreadsheetDict.createProfileIntervals(QProfiles, QIntervals, self.__md)
        except:
            errorlog.append("Profile Intervals could not be inserted")
#        try:
        Q1dict = SpreadsheetDict.createQuestionnaireDictionary(Q1, self.__md)
        Q9dict = SpreadsheetDict.createQ9dictionary(Q9Questionnaire, self.__md)
        NaceDict = SpreadsheetDict.createNACEDictionary(Q1, self.__md)
        try:
            strNace = "CodeNACE = '"+str(Q1[20])+"' AND CodeNACESub ='"+str(int(Q1[24]))+"'"
        except:
            strNace = ""
            errorlog.append("NACECode not found")
        dbnacecodeid = self.__md.dbnacecode.sql_select(strNace)
        
        Q1dict.update(Q9dict)
        try:
            Q1dict.update({'DBNaceCode_id':check(dbnacecodeid[0]['DBNaceCode_ID']),
                           'Branch' : check(dbnacecodeid[0]['NameNACE']),
                           'SubBranch' : check(dbnacecodeid[0]['NameNACEsub'])})
        except:
            Q1dict.update({'DBNaceCode_id':check(None),
                           'Branch' : check(None),
                           'SubBranch' : check(None)})
            errorlog.append("NACECode Branch and Sub-Branch not found")
        try:
            Questionnaire_ID = self.__md.questionnaire.insert(Q1dict)
        except:
            self.printLog(errorlog)
            return self.parseError(self.__sheetnames[0])
        
        quest_id = 'Questionnaire_id'
        
        try:
            q2dict = SpreadsheetDict.createQElectricityDictionary(Q2, self.__md)
            q2dict[quest_id]=Questionnaire_ID
            self.__md.qelectricity.insert(q2dict)
        except:
            errorlog.append(str(self.__sheetnames[1])+" could not be inserted")
            #return self.parseError(self.__sheetnames[1])
        
        Areas = ["Q4H_", "Q4C_", "Q5_", "Q6_", "Q8_"]

        for i in xrange(0,25,5):
            try:
                self.__md.qdistributionhc.insert(SpreadsheetDict.createQ5Dictionary(Q4_8[i+2], Questionnaire_ID, self.__md))
            except:
                errorlog.append("Q5 Dictionary could not be inserted")
                #return self.parseError(self.__sheetnames[6])


        for i in xrange(0,25,5):
            try:
                Q4Hdict = SpreadsheetDict.createQ4HDictionary(Q4_8[i],self.__md, Questionnaire_ID)
                Q4Hdict[quest_id]=Questionnaire_ID
                self.__md.qgenerationhc.insert(Q4Hdict)
            except:
                errorlog.append("Q4H Dictionary could not be inserted")
                #return self.parseError(self.__sheetnames[4])
                
            try:    
                Q4Cdict = SpreadsheetDict.createQ4CDictionary(Q4_8[i+1], self.__md, Questionnaire_ID)
                Q4Cdict[quest_id]=Questionnaire_ID
                self.__md.qgenerationhc.insert(Q4Cdict)
            except:
                errorlog.append("Q4C Dictionary could not be inserted")
                #return self.parseError(self.__sheetnames[5])
            
            
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
                errorlog.append("Q6 and Q6E Dictionary could not be inserted")
                #return self.parseError(self.__sheetnames[7])
                
#            try:
            print "Number: " + str(i)
            Q8dict = SpreadsheetDict.createQ8Dictionary(Q4_8[i+4], self.__md)
            Q8dict[quest_id]=Questionnaire_ID
            self.__md.qbuildings.insert(Q8dict)
#            except:
#                errorlog.append("Q8 Dictionary could not be inserted")
                #return self.parseError(self.__sheetnames[9])
                
                
                
#        try:
        QRenewables = SpreadsheetDict.createQ7Dictionary(QRenewables, self.__md)
        QRenewables[quest_id] = Questionnaire_ID
        self.__md.qrenewables.insert(QRenewables)
#        except:
#            errorlog.append(str(self.__sheetnames[8]) + " could not be inserted")
            #return self.parseError(self.__sheetnames[8])
        
        try:
            self.splitColumns(3, 5, QProduct, {}, Questionnaire_ID ,SpreadsheetDict.createQProductDictionary,self.__md.qproduct)
    #        self.splitColumns(6, 6, QFuel, {}, Questionnaire_ID ,SpreadsheetDict.createQFuelDictionary,self.__md.qfuel)
            self.splitColumns(4, 4, QSurf, {'ST_IT':latitude[1], 'ProjectID':Questionnaire_ID}, "", SpreadsheetDict.createQSurfDictionary, self.__md.qsurfarea)

            # Code to skip a specific amount of columns
            index =0
            Q3n = []
            for i in range(0,len(Q3),3):
                Q3n.append(Q3[i]) 
                index+=1
            
            self.splitColumns(3, 3, Q3n, {}, Questionnaire_ID, SpreadsheetDict.createQProcessDictionary,self.__md.qprocessdata)
        
            for i in xrange(3):
                SpreadsheetDict.createProcessPeriodsDictionary(Q3n[i], self.__md, QProfiles[i][-1])
        
            SpreadsheetDict.createProcessScheduleCorrDictionary(Q3n, self.__md)
            qf = self.splitColumns(6, 6, QFuel, {}, Questionnaire_ID ,SpreadsheetDict.createQFuelDictionary,self.__md.qfuel)

        except:
            errorlog.append("Error occured at QProduct, QFuel or QSurfarea")
#            return self.parseError("QProduct, QFuel or QSurfarea")

#        except:
#            pass
#        try:
            #self.__md.cgeneraldata.insert({'Questionnaire_id' : Questionnaire_ID, 'AlternativeProposalNo' : -1})
        
        try:
            salternatives = self.__md.salternatives.insert({'ProjectID' : Questionnaire_ID, 
                                                            'AlternativeProposalNo' : -1, 
                                                            'ShortName' : 'New Proposal', 
                                                            'Description' : 'data set', 
                                                            'StatusEnergy' : 0})
            
            self.__md.cgeneraldata.insert({'AlternativeProposalNo':-1, 
                                           'Questionnaire_id':Questionnaire_ID,                              
                                           'NFuels':0,
                                           'NEquipe':0,
                                           'NPipeDuct':0,
                                           'NThProc':0,
                                           'NProducts':0,
                                           'NHX':0,
                                           'NWHEE':0})
            self.__md.sproject.insert(SpreadsheetDict.sprojectdict(Questionnaire_ID, salternatives))
        except:
            errorlog.append("Inserting into salternatives and sproject failed")
            self.printLog(errorlog)
            return "Couldn't create new Project! Check the Data in your Questionnaire and try again"
        
        #self.__md.sproject.insert(SpreadsheetDict.createsprojectDictionary(Questionnaire_ID))
        
        
        self.printLog(errorlog)
        
        if len(errorlog)==0:
            return "New Project created!"
        
        return "New Project created! Check Project if all Data is inserted"
        

    def printLog(self, errorlog):
        for elem in errorlog:
            print elem
    
    
    
    