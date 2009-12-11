# -*- coding: cp1252 -*-
#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#   TCAData
#           
#------------------------------------------------------------------------------
#           
#   Manages data storage for the ModuleTCA (Total Cost Assessment)
#
#==============================================================================
#
#   Version No.: 0.03
#   Created by:        Florian Joebstl 17/09/2008
#   Last revised by:   Florian Joebstl 23/09/2008
#                       Hans Schweiger  28/11/2008
#                       Hans Schweiger 11/02/2009
#
#   17/09/08 FJ Fixed bug in storeTCAGeneral so that no data is overwritten
#   28/11/08 HS conversion to unicode (name of energy costs)
#               functions __getTCA... and __storeTCA adapted to unicode (description)
#   04/12/08 HS all other __store functions changed (adaptation to unicode)
#   11/02/09 HS small bug detected and corrected (Stauts -> Status)
#   
#------------------------------------------------------------------------------


from einstein.GUI.status import *
from einstein.modules.constants import *
from einstein.modules.messageLogger import *
from einstein.GUI.GUITools import check
import math

class TCAData(object):
        
    def __init__(self,pid,ano):
        #print "Init TCA Data (%s,%s)" % (pid,ano)
        self.pid = pid
        self.ano = ano
        self.tcaid = None   #will be set after generaldata is loaded
        self.ResultPresent = False
            
#--------------------------------------------------------------------------------------------
# Public Methodes
#--------------------------------------------------------------------------------------------                                 
    def loadTCAData(self):
        #print "Load Data (%s,%s)" % (self.pid,self.ano)
        #General Data
        if (self.__getTCAGeneralData() == False):          
            self.__setTCAGeneralDataDefault()            
            self.__storeTCAGeneralDataEntry()
            if (self.__getTCAGeneralData()==False):
                print "TCA FALSE"
        #Investments
        if (self.__getTCAInvestmentData() == False):
            self.__setTCAInvestmentDataDefault()
            self.__storeTCAInvestmentDataEntry()
            self.__getTCAInvestmentData()
        #EnergyDemand
        if (self.__getTCAEnergyData() == False):
            self.__setTCAEnergyDataDefault()
            self.__storeTCAEnergyDataEntry()
            self.__getTCAEnergyData()
        #Non reocuring costs
        if (self.__getTCANonData() == False):
            self.__setTCANonDataDefault()
            self.__storeTCANonDataEntry()
            self.__getTCANonData()
        #Contingencies
        if (self.__getTCAContingenciesData() == False):
            self.__setTCAContingenciesDataDefault()
            self.__storeTCAContingenciesDataEntry()
            self.__getTCAContingenciesData()
        #Detailed Operating Cost
        if (self.__getTCADetailedOpCostData() == False):
            self.__setTCADetailedOpCostDataDefault()
            self.__storeTCADetailedOpCostDataEntry()
            self.__getTCADetailedOpCostData()
        #Detailed Revenues  
        if (self.__getTCARevenueData() == False):
            self.__setTCARevenueDataDefault()
            self.__storeTCARevenueDataEntry()
            self.__getTCARevenueData()

    def storeTCAData(self):
        #print "Store Data"        
        self.__storeTCAGeneralDataEntry()
        
        self.__deleteTCAInvestmentDataEntry()  
        self.__deleteTCAEnergyDataEntry()
        self.__deleteTCANonDataEntry()
        self.__deleteTCAContingenciesDataEntry()
        self.__deleteTCADetailedOpCostDataEntry()
        self.__deleteTCARevenueDataEntry()
        
        self.__storeTCAInvestmentDataEntry()  
        self.__storeTCAEnergyDataEntry()
        self.__storeTCANonDataEntry()
        self.__storeTCAContingenciesDataEntry()
        self.__storeTCADetailedOpCostDataEntry() 
        self.__storeTCARevenueDataEntry()     
    
    def resetTCAData(self):
        print "Reset Data %s %s" % (self.pid,self.ano)     
        if (self.tcaid == None):            
            if (self.__getTCAGeneralData()==False):
                print "get failed"  
        if (self.tcaid != None):                   
            self.__deleteTCAInvestmentDataEntry()  
            self.__deleteTCAEnergyDataEntry()
            self.__deleteTCANonDataEntry()
            self.__deleteTCAContingenciesDataEntry()
            self.__deleteTCADetailedOpCostDataEntry()
            self.__deleteTCARevenueDataEntry()
            self.__deleteTCAGeneralDataEntry() 
        
                       
          
    def setResult(self,name,npv,mirr,bcr,annuity,paybackperiod,additionalcost,additionalcostpersavePE,display):
        try:
            self.name = name
            self.npv = npv[:]
            self.mirr = mirr[:]
            self.bcr = bcr[:]
            self.annuity = annuity
            self.display = display
            self.TIC = self.cashflow.TotalInvestmentCapital
            self.EIC = self.cashflow.EffectiveInvestmentCapital  
            self.PP  = paybackperiod 
            self.totalfunding = self.cashflow.TotalFundings
            self.energycost = self.getTotalEnergyCost()
            self.totalenergydemand = self.getTotalEnergyDemand()
            self.additionalcost = additionalcost
            self.additionalcostpersavePE = additionalcostpersavePE
            
            #TODO - calc this
            self.totalopcost = self.__gettotalopcost()
            
            self.totaleinergycost = self.energycost + self.annuity + self.totalopcost
            self.ResultPresent = True
        except Exception, inst:
            print type(inst)
            print inst.args
            print inst
            
    
    def setResultInvalid(self,name,display):
        self.name = name
        self.display = display
        self.ResultPresent = False
        
    def storeCurrentProcessInformationToCGeneral(self):
        #Store function for the current process
        
        self.energycost = self.getTotalEnergyCost()
#        query = """UPDATE cgeneraldata 
#                   SET EnergyCost = %s, OMThermal = %s                            
#                   WHERE Questionnaire_id = %s AND AlternativeProposalNo=%s"""
#        query = query % (self.energycost,self.totalopcost,self.pid,self.ano)
#        #print query                
#        Status.DB.sql_query(query)
# insert command subsituted by the following. -> has no problems with non-ascii characters in description !!!
        table =  Status.DB.cgeneraldata.Questionnaire_id[self.pid].AlternativeProposalNo[self.ano]
        if len(table) > 0:
            table[0].update({"EnergyCost":self.energycost,
                             "OMThermal":self.totalopcost})
            Status.SQL.commit()        
        
    def storeResultToCGeneralData(self):
        #store function for proposals
        try:
            if (self.ResultPresent):
                #mirr = self.mirr[int(math.ceil(self.PP))] #mirr at payback period
                mirr = self.mirr[len(self.mirr)-1]  #mirr at the final year 
                bcr = self.bcr[len(self.mirr)-1]          
#                query = """UPDATE cgeneraldata 
#                   SET TotalInvCost = %s, OwnInvCost = %s , Subsidies  = %s , RevenueReplaceEquipment = %s, IRR  = %s, PayBack  = %s, BCR  = %s, EnergyCost = %s, OMThermal = %s, Amortization = %s, EnergySystemCost=%s, AddCost=%s, AddCostperSavedPE=%s                              
#                   WHERE Questionnaire_id = %s AND AlternativeProposalNo=%s"""
#                query = query % (self.TIC,self.EIC,self.totalfunding,self.revenue,mirr,self.PP,bcr,self.energycost,self.totalopcost,self.annuity,self.totaleinergycost,self.additionalcost,self.additionalcostpersavePE,self.pid,self.ano)
#                #print query
#                Status.DB.sql_query(query)
                table =  Status.DB.cgeneraldata.Questionnaire_id[self.pid].AlternativeProposalNo[self.ano]
                if len(table) > 0:
                    table[0].update({"TotalInvCost": self.TIC,
                                     "OwnInvCost": self.EIC,
                                     "Subsidies": self.totalfunding,
                                     "RevenueReplaceEquipment": self.revenue,
                                     "IRR": mirr,
                                     "PayBack": self.PP,
                                     "BCR": bcr,
                                     "EnergyCost": self.energycost,
                                     "OMThermal": self.totalopcost,
                                     "Amortization": self.annuity,
                                     "EnergySystemCost": self.totaleinergycost,
                                     "AddCost": self.additionalcost,
                                     "AddCostperSavedPE": self.additionalcostpersavePE})
                    Status.SQL.commit()        

        except Exception, inst:
            print "storeResultToCGeneral"
            print type(inst)
            print inst.args
            print inst
#--------------------------------------------------------------------------------------------
# General Data
#--------------------------------------------------------------------------------------------     
    def __setTCAGeneralDataDefault(self):
        #print "Set Default Data (General)"
        query = """SELECT InflationRate,FuelPriceRate,InterestExtFinancing,CompSpecificDiscountRate, PercentExtFinancing, AmortisationTime, OMTotalTot
                   FROM `questionnaire` WHERE Questionnaire_id=%s"""
        query = query % (self.pid) 
        #print query         
        result = Status.DB.sql_query(query)        
        if (len(result)>0):
            #print "result form questionnaire"
            self.tcaid     = None
            self.Inflation = result[0]
            if (self.Inflation==None):
                self.Inflation = 0.0
            self.NIR       = result[2]
            if (self.NIR==None):
                self.NIR = 0.0
            self.CSDR      = result[3]
            if (self.CSDR==None):
                self.CSDR = 0.0
            self.DEP       = result[1]
            if (self.DEP==None):
                self.DEP = 0.0
            self.TimeFrame = result[5]
            if (self.TimeFrame==None):
                self.TimeFrame = 0.0
            self.totalopcost = result[6]
            if (self.totalopcost==None):
                self.totalopcost = 0.0
            self.revenue     = 0.0 #will be read later
        else:
            #print "no result"
            self.tcaid     = None
            self.Inflation = 0.0
            self.NIR       = 0.0
            self.CSDR      = 0.0
            self.DEP       = 0.0
            self.TimeFrame = 20.0
            self.totalopcost = 0.0
            self.revenue     = 0.0   
        
        #FIX due to inconsitencies between questionair and tca
        self.Inflation = self.Inflation * 100.0
        self.NIR       = self.NIR * 100.0
        self.CSDR      = self.CSDR * 100.0
        self.DEP       = self.DEP * 100.0           
        
    def __getTCAGeneralData(self):
        #print "Get Data (General)"        
        query = """SELECT IDTca, InflationRate, NominalInterestRate, CompSpecificDiscountRate, FulePriceRate, AmotisationTime, TotalOperatingCost, TotalRevenue
                   FROM tcageneraldata 
                   WHERE ProjectID=%s AND AlternativeProposalNo=%s;""" 
        query = query % (self.pid,self.ano)
        #print query
        result = Status.DB.sql_query(query)        
        if (len(result)==0):
            return False
        else:
            self.tcaid     = result[0]
            self.Inflation = result[1]
            self.NIR       = result[2]
            self.CSDR      = result[3]
            self.DEP       = result[4]
            self.TimeFrame = result[5]
            self.totalopcost = result[6]
            self.revenue     = result[7]
		#self.PETFuels = result[8]
		#self.PETel = result[9]
            return True
        
    def __storeTCAGeneralDataEntry(self):
        #print "Store Data (General)"
        if (self.tcaid == None):            
#            query = """INSERT INTO tcageneraldata (ProjectID,AlternativeProposalNo, InflationRate, NominalInterestRate, CompSpecificDiscountRate, FulePriceRate, AmotisationTime, TotalOperatingCost, TotalRevenue)
#                       VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
#            query = query %(self.pid,self.ano,self.Inflation,self.NIR, self.CSDR,self.DEP,self.TimeFrame,self.totalopcost,self.revenue)
#            Status.DB.sql_query(query)
            Status.DB.tcageneraldata.insert({"ProjectID": self.pid,
                                             "AlternativeProposalNo": self.ano,
                                             "InflationRate": self.Inflation,
                                             "NominalInterestRate": self.NIR, 
                                             "CompSpecificDiscountRate": self.CSDR,
                                             "FulePriceRate": self.DEP,
                                             "AmotisationTime": self.TimeFrame,
                                             "TotalOperatingCost": self.totalopcost,
                                             "TotalRevenue": self.revenue})
            Status.SQL.commit()        

        else:
            #Update for all proposals
 #           query = """UPDATE tcageneraldata 
 #                      SET InflationRate = %s, NominalInterestRate = %s , CompSpecificDiscountRate  = %s , FulePriceRate  = %s, AmotisationTime  = %s
 #                      WHERE ProjectID = %s"""
 #           query = query %(self.Inflation,self.NIR, self.CSDR,self.DEP,self.TimeFrame,self.pid)
#           Status.DB.sql_query(query)

            for i in range(0,(Status.NoOfAlternatives+1)):
                table =  Status.DB.tcageneraldata.ProjectID[self.pid].AlternativeProposalNo[i]
                if len(table) > 0:
                    table[0].update({"InflationRate": self.Inflation,
                                     "NominalInterestRate": self.NIR, 
                                     "CompSpecificDiscountRate": self.CSDR,
                                     "FulePriceRate": self.DEP,
                                     "AmotisationTime": self.TimeFrame})
                    Status.SQL.commit()
                    
            #Set for current ano only - will be replaced after concrete calculation
            #e.g. storeDetailedOpCost
                    
#            query = """UPDATE tcageneraldata 
#                       SET TotalOperatingCost = %s, TotalRevenue = %s
#                       WHERE ProjectID = %s AND AlternativeProposalNo=%s"""
#            query = query %(self.totalopcost,self.revenue,self.pid,self.ano)
#            Status.DB.sql_query(query)                           

            table =  Status.DB.tcageneraldata.ProjectID[self.pid].AlternativeProposalNo[self.ano]
            if len(table) > 0:
                table[0].update({"TotalOperatingCost": self.totalopcost,
                                 "TotalRevenue": self.revenue})
                Status.SQL.commit()        
        
    def __deleteTCAGeneralDataEntry(self):
        query = """DELETE FROM tcageneraldata
                   WHERE ProjectID=%s AND AlternativeProposalNo=%s;""" 
        query = query % (self.pid,self.ano)
        result = Status.DB.sql_query(query)      
        
#--------------------------------------------------------------------------------------------
# Investment
#--------------------------------------------------------------------------------------------  

    def __setTCAInvestmentDataDefault(self):
        #print "Set Default Data (Investment)"
        # Structure [Descritpion, Investment, Fundig%, FundingFix]
        #try:
        self.investment = []
        if (self.ano > 0):
            self.__setDefaultEquipmentInvestment()
            self.__setDefaultHXInvestment()
            self.__setDefaultStorageInvestment()
    
    def __setDefaultHXInvestment(self):
        total_hx_investment = 0.0
        query = """SELECT TurnKeyPrice, OMFix, OMVar FROM qheatexchanger WHERE `ProjectID`=%s AND `AlternativeProposalNo`=%s"""
        query = query % (self.pid,self.ano)
        results = Status.DB.sql_query(query)  
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            
            for result in results:                
                Investment = result[0]
                if Investment == None:
                    Investment = 0
                total_hx_investment +=  Investment 
        self.investment.append(["HX Network",total_hx_investment,30,0])  
        
    def __setDefaultEquipmentInvestment(self):
        keys = []
        dict = {}
        query = """SELECT Equipment, EquipType, TurnKeyPrice, Price FROM `qgenerationhc` WHERE `Questionnaire_id`=%s AND `AlternativeProposalNo`=%s"""
        query = query % (self.pid,self.ano)
        results = Status.DB.sql_query(query)  
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            
            for result in results:
                EquipType = result[1]
                Investment = result[2]
                InvestmentBasedOnPrice = result[3]   
                                   
                if (EquipType != None):              
                    if not(EquipType in keys):
                        keys.append(EquipType)
                        dict[EquipType] = 0
                    if Investment == None:
                        if InvestmentBasedOnPrice != None:
                            Investment = InvestmentBasedOnPrice * 1.2
                        else:
                            Investment = 0
                    dict[EquipType] +=  Investment 
                
        for key in keys:
            self.investment.append([key,dict[key],30,0])                                         
        #except:        
        #    self.investment = []
        
    def __setDefaultStorageInvestment(self):
        query = """SELECT `NumStorageUnits`,`VUnitStorage` FROM `qdistributionhc` WHERE `Questionnaire_id`=%s AND `AlternativeProposalNo` = %s"""
        query = query % (self.pid,self.ano)
        results = Status.DB.sql_query(query)  
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            #XXX Constants should come from database! 
            #fixed cepci bad.... 
            CEPCI1976 = 192.1
            CEPCI2008 = 539.7
            EUR_USD_ratio = 1.55
            m3_ft3_ratio = 0.0283
            ratio = (CEPCI2008/CEPCI1976)/EUR_USD_ratio
            total_storage = 0.0
            for result in results:
                #print result
                NumStorageUnits = result[0]
                VUnitStorage = result[1]
                if not((NumStorageUnits == None) or (VUnitStorage==None) or (NumStorageUnits == 0) or (VUnitStorage==0)):                     
                    V=VUnitStorage/m3_ft3_ratio 
                    Storage_cost = (352*pow(V,0.515))*ratio
                    Storage_cost *= NumStorageUnits
                    total_storage+=Storage_cost
            self.investment.append(["H&C Storage",total_storage,30,0])
                
            
    def __storeTCAInvestmentDataEntry(self):
        #print "Store Data (Investment)"
        for investment in self.investment:
#            query = """INSERT INTO tcainvestments (TcaID, Description, Investment, FundingPerc, FundingFix)
#                       VALUES(%s,\"%r\",%s,%s,%s)"""
#            query = query %(self.tcaid,investment[0],investment[1],investment[2],investment[3])
#            Status.DB.sql_query(query)

# insert command subsituted by the following. -> has no problems with non-ascii characters in description !!!
            tmp = {"TcaID":self.tcaid,
                   "Description":check(investment[0]),
                   "Investment":investment[1],
                   "FundingPerc":investment[2],
                   "FundingFix":investment[3]}
            
            Status.DB.tcainvestments.insert(tmp)
            
    
    def __getTCAInvestmentData(self):
        #print "Get Data (Investment)"
        query = """SELECT Description, Investment, FundingPerc, FundingFix
                   FROM tcainvestments
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        results = Status.DB.sql_query(query)
        self.investment = []
        if (len(results)==0):        
            return False        
        else:
            if (type(results[0])!=type(())):
                results = [ results ]         #needed to have same behaviour if only one result
            for result in results:
                self.investment.append([unicode(result[0],"utf-8"),result[1],result[2],result[3]])            
            return True                                                   

    def __deleteTCAInvestmentDataEntry(self):
        #print "Delete Data (Investment)"
        query = """DELETE FROM tcainvestments
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        #print query
        result = Status.DB.sql_query(query)   

#--------------------------------------------------------------------------------------------
# Energy
#-------------------------------------------------------------------------------------------- 
    def __setTCAEnergyDataDefault(self):
        #print "Set Default Data (Energy)"
        self.energycosts = []
        self.__setElectricityDefault()
        self.__setOtherFuelsDefault()
    
    def __setElectricityDefault(self):
        query = """SELECT FECel FROM cgeneraldata WHERE `Questionnaire_id`=%s AND `AlternativeProposalNo`=%s"""
        query = query % (self.pid,self.ano)
        FECel = Status.DB.sql_query(query)
        if (FECel == None):
            FECel = 0.0
        
        query = """SELECT ElTariffCTot, ElTariffPowTot,PowerContrTot FROM qelectricity
                WHERE `Questionnaire_id`=%s AND `AlternativeProposalNo`=%s"""
        query = query % (self.pid,self.ano)
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ] 
            for result in results:
                ElTariffCTot = result[0]
                ElTariffPowTot = result[1]
                PowerContrTot = result[2]
                Tariff = 0.0
                if not(ElTariffCTot==None):
                    Tariff = ElTariffCTot 
                if not((ElTariffPowTot==None)or(PowerContrTot==None)):                    
                    if (FECel > 0):
                        Tariff+=(ElTariffPowTot*PowerContrTot*12)/FECel                      
                self.energycosts.append(["Electricity",FECel,Tariff,self.DEP]) 
            
                
    
    def __setOtherFuelsDefault(self):
        query = """SELECT FuelName, FETFuel, FuelTariff FROM qfuel, dbfuel 
                   WHERE dbfuel.DBFuel_ID=qfuel.DBFuel_ID
                   AND `Questionnaire_id`=%s AND `AlternativeProposalNo`=%s"""
        query = query % (self.pid,self.ano)
        results = Status.DB.sql_query(query)  
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]   
            for result in results:
                Name = unicode(result[0],"utf-8")
                FETFuel = result[1]
                if (FETFuel == None):
                    FETFuel = 0.0
                FuelTariff = result[2]
                if (FuelTariff == None):
                    FuelTariff = 0.0
                self.energycosts.append([Name,FETFuel,FuelTariff,self.DEP])                                                         
                
    def __storeTCAEnergyDataEntry(self):
        #print "Store Data (Energy)"
        for energycost in self.energycosts:
#            query = """INSERT INTO tcaenergy (TcaID, Description, EnergyDemand, EnergyPrice, DevelopmentOfEnergyPrice)
#                       VALUES(%s,\"%r\",%s,%s,%s)"""
#            query = query %(self.tcaid,energycost[0],energycost[1],energycost[2],energycost[3])
#            Status.DB.sql_query(query)

            tmp = {"TcaID": self.tcaid,
                   "Description": check(energycost[0]),
                   "EnergyDemand": energycost[1],
                   "EnergyPrice": energycost[2],
                   "DevelopmentOfEnergyPrice": energycost[3]}
            Status.DB.tcaenergy.insert(tmp)
            
    
    def getTotalEnergyCost(self):
        totalenergycost = 0.0
        for energycost in self.energycosts:
            totalenergycost+=energycost[1]*energycost[2]
        return totalenergycost

    def getTotalEnergyDemand(self):
        totalenergydemand = 0.0
        for energycost in self.energycosts:
            totalenergydemand+=energycost[1]
        return totalenergydemand
  
    def __getTCAEnergyData(self):
        #print "Get Data (Energy)"
        query = """SELECT Description, EnergyDemand, EnergyPrice, DevelopmentOfEnergyPrice
                   FROM tcaenergy
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        results = Status.DB.sql_query(query)
        self.energycosts = []
        if (len(results)==0):        
            return False        
        else:
            if (type(results[0])!=type(())):
                results = [ results ]         #needed to have same behaviour if only one result
            for result in results:
                self.energycosts.append([unicode(result[0],"utf-8"),result[1],result[2],result[3]])            
            return True                                                   

    def __deleteTCAEnergyDataEntry(self):
        #print "Delete Data (Energy)"
        query = """DELETE FROM tcaenergy
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        result = Status.DB.sql_query(query)   

#--------------------------------------------------------------------------------------------
# Non reocurring costs
#-------------------------------------------------------------------------------------------- 
    def __setTCANonDataDefault(self):
        #print "Set Default Data (Non reocurring costs)"
        self.nonreoccuringcosts = []
                
    def __storeTCANonDataEntry(self):
        #print "Store Data (Non reocurring costs)"
        for cost in self.nonreoccuringcosts:
#            query = u"""INSERT INTO tcanonreoccuringcosts (TcaID, Description, Value, Year, Type)
#                       VALUES(%s,\"%r\",%s,%s,\"%s\")"""
#            query = query %(self.tcaid,cost[0],cost[1],cost[2],cost[3])
#            Status.DB.sql_query(query)  

            tmp = {"TcaID": self.tcaid,
                   "Description": check(cost[0]),
                   "Value": cost[1],
                   "Year": cost[2],
                   "Type": cost[3]}
            Status.DB.tcanonreoccuringcosts.insert(tmp)
            Status.SQL.commit()
            
    
    def __getTCANonData(self):
        #print "Get Data (Non reocurring costs)"
        query = """SELECT Description, Value, Year, Type
                   FROM tcanonreoccuringCosts
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        results = Status.DB.sql_query(query)
        self.nonreoccuringcosts = []
        if (len(results)==0):        
            return False        
        else:
            if (type(results[0])!=type(())):
                results = [ results ]         #needed to have same behaviour if only one result
            for result in results:
                self.nonreoccuringcosts.append([unicode(result[0],"utf-8"),result[1],result[2],result[3]])            
            return True                                                   

    def __deleteTCANonDataEntry(self):
        #print "Delete Data (Non reocurring costs)"
        query = """DELETE FROM tcanonreoccuringcosts
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        result = Status.DB.sql_query(query)   

#--------------------------------------------------------------------------------------------
# Contingencies
#--------------------------------------------------------------------------------------------

    def __setTCAContingenciesDataDefault(self):
        #print "Set Default Data (Contingencies)"
        self.contingencies = []
                
    def __storeTCAContingenciesDataEntry(self):
        #print "Store Data (Contingencies)"
        for contingency in self.contingencies:
#            query = u"""INSERT INTO tcacontingencies (TcaID, Description, Value, TimeFrame)
#                       VALUES(%s,\"%r\",%s,%s)"""
#            query = query %(self.tcaid,contingency[0],contingency[1],contingency[2])
#            Status.DB.sql_query(query)                          

            tmp = {"TcaID": self.tcaid,
                   "Description": check(contingency[0]),
                   "Value": contingency[1],
                   "TimeFrame": contingency[2]}
            Status.DB.tcacontingencies.insert(tmp)
            Status.SQL.commit()
    
    def __getTCAContingenciesData(self):
        #print "Get Data (Contingencies)"
        query = """SELECT Description, Value, TimeFrame
                   FROM tcacontingencies
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        results = Status.DB.sql_query(query)
        self.contingencies = []
        if (len(results)==0):           
            return False        
        else:
            if (type(results[0])!=type(())):
                results = [ results ]         #needed to have same behaviour if only one result
            for result in results:                
                self.contingencies.append([unicode(result[0],"utf-8"),result[1],result[2]])            
            return True
                                                                

    def __deleteTCAContingenciesDataEntry(self):
        #print "Delete Data (Contingencies)"
        query = """DELETE FROM tcacontingencies
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        result = Status.DB.sql_query(query)   
          
#--------------------------------------------------------------------------------------------
# Detailed operating cost
#--------------------------------------------------------------------------------------------

    def __setTCADetailedOpCostDataDefault(self):
        if self.ano == 0:
            self.__setDefaultOPCostCurrent()
        else:
            self.__setDefaultOPCostProposal()
        
            cost = 0
            for category in self.detailedopcost:
                for entry in category:
                    cost+=entry[1]               
            self.totalopcost = cost
     
    def __setDefaultOPCostCurrent(self):
        self.detailedopcost = [[],[],[],[],[],[],[]]
        query = """SELECT OMTotalTot FROM questionnaire WHERE Questionnaire_id=%s"""
        query = query % (self.pid)
        result = Status.DB.sql_query(query)
        if (result !=None):
            #print "questionair opcost"
            #print result
            self.totalopcost = result
        else:                    
            #print "no opcost in db ("+str(self.ano)+")"
            self.totalopcost = 0.0
    
    def __setDefaultOPCostProposal(self):
        self.detailedopcost = [[],[],[],[],[],[],[]] 
        #self.totalopcost = 0.0
        self.__setDefaultEquipOpcost()
        self.__setDefaultHXOpcost()
    
    def __setDefaultHXOpcost(self):
        total_hx_opcost = 0.0
        query = """SELECT TurnKeyPrice, OMFix, OMVar FROM qheatexchanger WHERE `ProjectID`=%s AND `AlternativeProposalNo`=%s"""
        query = query % (self.pid,self.ano)
        results = Status.DB.sql_query(query)  
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            
            for result in results:                
                OMVar = result[2]
                OMFix = result[1]
                if OMVar == None:
                    OMVar = 0
                if OMFix == None:
                    OMFix = 0
                total_hx_opcost +=  (OMFix + OMVar)        
        self.detailedopcost[0].append(["HX network",total_hx_opcost])               
        self.totalopcost+= total_hx_opcost    
        
        
    def __setDefaultEquipOpcost(self):
        #print "Set Default Data (Detailed operting cost)"        
        #                   page1                page2             page7
        # Structure [[[Desc,Value],[Desc,Value]],[...],[],[],[],[],[]]
        #try:       
        keys = []
        dict = {}
        total = 0
        query = """SELECT Equipment, EquipType, TurnKeyPrice, OandMvar,OandMfix FROM `qgenerationhc` WHERE `Questionnaire_id`=%s AND `AlternativeProposalNo`=%s"""
        query = query % (self.pid,self.ano)
        results = Status.DB.sql_query(query)  
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            
            for result in results:
                EquipType = result[1]
                OMVar = result[3]
                OMFix = result[4]
                                   
                if (EquipType != None):              
                    if not(EquipType in keys):
                        keys.append(EquipType)
                        dict[EquipType] = 0
                    if OMVar == None:
                        OMVar = 0
                    if OMFix == None:
                        OMFix = 0
                    
                    dict[EquipType] +=  (OMVar + OMFix) 
                    total += (OMVar + OMFix) 
                
        for key in keys:
            self.detailedopcost[0].append([key,dict[key]])
               
        self.totalopcost+= total                                       
        #except:        
        #    self.detailedopcost = [[],[],[],[],[],[],[]] 

    def __gettotalopcost(self):
        if (self.ano<=0): #dont calculate opcost from detailed-opcost for current process
            return self.totalopcost
        
        cost = 0
        for category in self.detailedopcost:
            for entry in category:
                cost+=entry[1]
                
        return cost
                
    def __storeTCADetailedOpCostDataEntry(self):
        #print "Store Data (Detailed operting cost)"
        for i in range(0,7): #7 categorys in detailed opcost
            for opcost in self.detailedopcost[i]:
#                query = u"""INSERT INTO tcadetailedopcost (TcaID, Description, Value, Category)
#                           VALUES(%s,\"%r\",%s,%s)"""
#                query = query %(self.tcaid,opcost[0],opcost[1],i)
#                Status.DB.sql_query(query) 

                tmp = {"TcaID": self.tcaid,
                       "Description": check(opcost[0]),
                       "Value": opcost[1],
                       "Category": i}
                Status.DB.tcadetailedopcost.insert(tmp)
                Status.SQL.commit()
        
        query = """UPDATE tcageneraldata 
                SET TotalOperatingCost = %s
                WHERE IDTca=%s"""
        query = query %(self.totalopcost,self.tcaid)
        Status.DB.sql_query(query)                                       


    def __getTCADetailedOpCostData(self):
        #print "Get Data (Detailed operting cost)"
        self.detailedopcost = [[],[],[],[],[],[],[]] 
        for i in range(0,7):
            query = """SELECT Description, Value
                       FROM tcadetailedopcost
                       WHERE TcaID = %s AND Category = %s"""
            query = query % (self.tcaid,i)
            results = Status.DB.sql_query(query)            
            if (len(results)!=0):                           
                if (type(results[0])!=type(())):
                    results = [ results ]         #needed to have same behaviour if only one result
                for result in results:                
                    self.detailedopcost[i].append([unicode(result[0],"utf-8"),result[1]])                                
                return True
            return False
                                                                

    def __deleteTCADetailedOpCostDataEntry(self):
        #print "Delete Data (Detailed operting cost)"
        query = """DELETE FROM tcadetailedopcost
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        result = Status.DB.sql_query(query)

#--------------------------------------------------------------------------------------------
# Revenue
#--------------------------------------------------------------------------------------------

    def __setTCARevenueDataDefault(self):
        #print "Set Default Data (Revenue)"
        self.revenues = [] 
                
    def __storeTCARevenueDataEntry(self):
        #print "Store Data (Revenue)"
        for revenue in self.revenues:
#            query = u"""INSERT INTO tcadetailedrevenue (TcaID, Description, InitialInvestment, DeprecationPeriod, RemainingPeriod) 
#                       VALUES(%s,\"%r\",%s,%s,%s)"""
#            query = query %(self.tcaid,revenue[0],revenue[1],revenue[2],revenue[3])
#            Status.DB.sql_query(query)
            tmp = {"TcaID": self.tcaid,
                   "Description": revenue[0],
                   "InitialInvestment": revenue[1],
                   "DeprecationPeriod": revenue[2],
                   "RemainingPeriod": revenue[3]}
            Status.DB.tcadetailedrevenue.insert(tmp)
            Status.SQL.commit()
    
    def __getTCARevenueData(self):
        #print "Get Data (Revenue)"        
        query = """SELECT Description, InitialInvestment, DeprecationPeriod, RemainingPeriod
                   FROM tcadetailedrevenue
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        results = Status.DB.sql_query(query)
        self.revenues = []
        if (len(results)==0):        
            return False        
        else:
            if (type(results[0])!=type(())):
                results = [ results ]         #needed to have same behaviour if only one result
            for result in results:
                self.revenues.append([unicode(result[0],"utf-8"),result[1],result[2],result[3]])            
            return True          
                                                                

    def __deleteTCARevenueDataEntry(self):
        #print "Delete Data (Revenue)"
        query = """DELETE FROM tcadetailedrevenue
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        result = Status.DB.sql_query(query)   
         
