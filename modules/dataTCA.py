from einstein.GUI.status import *
from einstein.modules.constants import *
from einstein.modules.messageLogger import *

class TCAData(object):
        
    def __init__(self,pid,ano):
        print "Init TCA Data (%s,%s)" % (pid,ano)
        self.pid = pid
        self.ano = ano
        self.tcaid = None   #will be set after generaldata is loaded
            
#--------------------------------------------------------------------------------------------
# Public Methodes
#--------------------------------------------------------------------------------------------         
                        
    def loadTCAData(self):
        print "Load Data"
        #General Data
        if (self.__getTCAGeneralData()    == False):
            self.__setTCAGeneralDataDefault()
            self.__storeTCAGeneralDataEntry()
            self.__getTCAGeneralData()
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

    def storeTCAData(self):
        print "Store Data"
        self.resetTCAData()
        self.__storeTCAGeneralDataEntry()
        self.__storeTCAInvestmentDataEntry()  
        self.__storeTCAEnergyDataEntry()
        self.__storeTCANonDataEntry()
        self.__storeTCAContingenciesDataEntry()      
    
    def resetTCAData(self):
        print "Reset Data"
        self.__deleteTCAGeneralDataEntry() 
        self.__deleteTCAInvestmentDataEntry()  
        self.__deleteTCAEnergyDataEntry()
        self.__deleteTCANonDataEntry()
        self.__deleteTCAContingenciesDataEntry()
            
#--------------------------------------------------------------------------------------------
# General Data
#--------------------------------------------------------------------------------------------     
    def __setTCAGeneralDataDefault(self):
        print "Set Default Data (General)"
        self.tcaid     = None
        self.LIR       = 0.0
        self.CSDR      = 0.0
        self.DEP       = 0.0
        self.TimeFrame = 0.0
        self.totalopcost = 0.0
        self.revenue = 0.0
        
    def __getTCAGeneralData(self):
        print "Get Data (General)"
        query = """SELECT IDTca, LoanInterestRate, CompSpecificDiscountRate, FulePriceRate, AmotisationTime, TotalOperatingCost, TotalRevenue 
                   FROM tcaData 
                   WHERE ProjectID=%s AND AlternativeProposalNo=%s;""" 
        query = query % (Status.PId,Status.ANo)
        result = Status.DB.sql_query(query)        
        if (len(result)==0):
            return False
        else:
            self.tcaid     = result[0]
            self.LIR       = result[1]
            self.CSDR      = result[2]
            self.DEP       = result[3]
            self.TimeFrame = result[4]
            self.totalopcost = result[5]
            self.revenue   = result[6]
            return True
        
    def __storeTCAGeneralDataEntry(self):
        print "Store Data (General)"
        query = """INSERT INTO tcaData (ProjectID,AlternativeProposalNo,LoanInterestRate, CompSpecificDiscountRate, FulePriceRate, AmotisationTime)
                   VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
        query = query %(self.pid,self.ano,self.LIR,self.CSDR,self.DEP,self.TimeFrame,self.totalopcost,self.revenue)
        Status.DB.sql_query(query)
       
        
    def __deleteTCAGeneralDataEntry(self):
        print "Delete Data (General)"
        query = """DELETE FROM tcaData
                   WHERE ProjectID=%s AND AlternativeProposalNo=%s;""" 
        query = query % (Status.PId,Status.ANo)
        result = Status.DB.sql_query(query)      
        
#--------------------------------------------------------------------------------------------
# Investment
#--------------------------------------------------------------------------------------------  

    def __setTCAInvestmentDataDefault(self):
        print "Set Default Data (Investment)"
        self.investment = []
                
    def __storeTCAInvestmentDataEntry(self):
        print "Store Data (Investment)"
        for investment in self.investment:
            query = """INSERT INTO tcaInvestments (TcaID, Description, Investment, FundingPerc, FundingFix)
                       VALUES(%s,%s,%s,%s,%s)"""
            query = query %(self.tcaid,investment[0],investment[1],investment[2],investment[3])
            Status.DB.sql_query(query)  
            
    
    def __getTCAInvestmentData(self):
        print "Get Data (Investment)"
        query = """SELECT Description, Investment, FundingPerc, FundingFix
                   FROM tcaInvestments
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        results = Status.DB.sql_query(query)
        self.investment = []
        if (len(results)==0):
            return False
        else:
            for result in results:
                self.investment.append([result[0],result[1],result[2],result[3]])            
            return True                                                   

    def __deleteTCAInvestmentDataEntry(self):
        print "Delete Data (Investment)"
        query = """DELETE FROM tcaInvestments
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        result = Status.DB.sql_query(query)   

#--------------------------------------------------------------------------------------------
# Energy
#-------------------------------------------------------------------------------------------- 
    def __setTCAEnergyDataDefault(self):
        print "Set Default Data (Energy)"
        self.energycosts = []
                
    def __storeTCAEnergyDataEntry(self):
        print "Store Data (Energy)"
        for energycost in self.energycosts:
            query = """INSERT INTO tcaEnergy (TcaID, Description, EnergyDemand, EnergyPrice, DevelopmentOfEnergyPrice)
                       VALUES(%s,%s,%s,%s,%s)"""
            query = query %(self.tcaid,energycost[0],energycost[1],energycost[2],energycost[3])
            Status.DB.sql_query(query)  
            
    
    def __getTCAEnergyData(self):
        print "Get Data (Energy)"
        query = """SELECT Description, EnergyDemand, EnergyPrice, DevelopmentOfEnergyPrice
                   FROM tcaEnergy
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        results = Status.DB.sql_query(query)
        self.energycosts = []
        if (len(results)==0):
            return False
        else:
            for result in results:
                self.energycosts.append([result[0],result[1],result[2],result[3]])            
            return True                                                   

    def __deleteTCAEnergyDataEntry(self):
        print "Delete Data (Energy)"
        query = """DELETE FROM tcaEnergy
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        result = Status.DB.sql_query(query)   

#--------------------------------------------------------------------------------------------
# Non reocurring costs
#-------------------------------------------------------------------------------------------- 

    def __setTCANonDataDefault(self):
        print "Set Default Data (Non reocurring costs)"
        self.nonreoccuringcosts = []
                
    def __storeTCANonDataEntry(self):
        print "Store Data (Non reocurring costs)"
        for cost in self.nonreoccuringcosts:
            query = """INSERT INTO tcaNonReoccuringCosts (TcaID, Description, Value, Year, Type)
                       VALUES(%s,%s,%s,%s,%s)"""
            query = query %(self.tcaid,cost[0],cost[1],cost[2],cost[3])
            Status.DB.sql_query(query)  
            
    
    def __getTCANonData(self):
        print "Get Data (Non reocurring costs)"
        query = """SELECT Description, Value, Year, Type
                   FROM tcaNonReoccuringCosts
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        results = Status.DB.sql_query(query)
        self.nonreoccuringcosts = []
        if (len(results)==0):
            return False
        else:
            for result in results:
                self.nonreoccuringcosts.append([result[0],result[1],result[2],result[3]])            
            return True                                                   

    def __deleteTCANonDataEntry(self):
        print "Delete Data (Non reocurring costs)"
        query = """DELETE FROM tcanonreoccuringcosts
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        result = Status.DB.sql_query(query)   

#--------------------------------------------------------------------------------------------
# Contingencies
#--------------------------------------------------------------------------------------------

    def __setTCAContingenciesDataDefault(self):
        print "Set Default Data (Contingencies)"
        self.contingencies = []
                
    def __storeTCAContingenciesDataEntry(self):
        print "Store Data (Contingencies)"
        for contingency in self.contingencies:
            query = """INSERT INTO tcaContingencies (TcaID, Description, Contingecy, TimeFrame)
                       VALUES(%s,%s,%s,%s)"""
            query = query %(self.tcaid,contingency[0],contingency[1],contingency[2])
            Status.DB.sql_query(query)  
            
    
    def __getTCAContingenciesData(self):
        print "Get Data (Contingencies)"
        query = """SELECT Description, Value, Contingecy, TimeFrame
                   FROM tcaContingencies
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        results = Status.DB.sql_query(query)
        self.contingencies = []
        if (len(results)==0):
            return False
        else:
            for result in results:
                self.contingencies.append([result[0],result[1],result[2]])            
            return True                                                   

    def __deleteTCAContingenciesDataEntry(self):
        print "Delete Data (Contingencies)"
        query = """DELETE FROM tcaContingencies
                   WHERE TcaID = %s"""
        query = query % (self.tcaid)
        result = Status.DB.sql_query(query)         