# -*- coding: cp1252 -*-
#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#   ModuleTCA (Total Cost Assessment)
#           
#------------------------------------------------------------------------------
#           
#   
#
#==============================================================================
#
#   Version No.: 0.01
#   Created by:         Florian Joebstl 15/09/2008  
#   Last revised by:    Florian Joebstl 17/09/2008  
#
#
#       Changes to previous version:
#            17/09/2008 FJ Moved all data handling to dataTCA.py
#   
#------------------------------------------------------------------------------
from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import Status
from einstein.modules.interfaces import *
from einstein.modules.constants import *
from einstein.modules.messageLogger import *
from einstein.modules.dataTCA import TCAData
from einstein.modules.calculationTCA import *

import sys
from pylab import *
import wx

class ModuleTCA(object):

    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel 
        self.data = None    
        self.result = None
                       

    def initPanel(self):         
        self.updatePanel()
              
#------------------------------------------------------------------------------
    def updatePanel(self):           
        #Create or Update data according to PID and ANo in Status    
        if (self.data == None):
            self.data = TCAData(Status.PId,Status.ANo)
            self.data.loadTCAData()        
        if (Status.PId != self.data.pid)or(Status.ANo != self.data.ano):
            self.data = TCAData(Status.PId,Status.ANo)
            self.data.loadTCAData()
    
    def resetTCA(self):
        query = """SELECT AlternativeProposalNo,ShortName FROM salternatives WHERE ProjectID = %s"""
        query = query % (self.data.pid)    
        results = Status.DB.sql_query(query)
        anos = []              
                  
        for result in results:
            if (result[0]>=0):
                anos.append([result[0],result[1]])              
        
        #print "reset:"
        #print anos
        for ano in anos: # ano = [ Number, Name ] !!!           
            data = TCAData(Status.PId,ano[0])  
            data.resetTCAData()   
        
        self.data = TCAData(Status.PId,Status.ANo)                 
        self.data.loadTCAData()               
    
    def runTCAModule(self):
        self.updatePanel()   
        self.result = []
                        
        #get cashflow for the current process
        data = TCAData(Status.PId,0)                
        data.loadTCAData()
        
        #set parameters
        InterestRate = data.NIR - data.Inflation
        DiscountRate = data.CSDR - data.Inflation
        ProjectLifetime = data.TimeFrame
          
        data = self.calculateCashFlow(data)
        old = data.cashflow
        
        #get all proposal numbers and names
        query = """SELECT AlternativeProposalNo,ShortName FROM salternatives WHERE ProjectID = %s"""
        query = query % (self.data.pid)    
        results = Status.DB.sql_query(query)
        self.anos = []              
                  
        for result in results:
            if (result[0]>0):
                self.anos.append([result[0],result[1]])              
        
        #calculate result for each proposal in project
        for ano in self.anos: # ano = [ Number, Name ] !!!
            try:
                name = ano[1]  
                #load data for alternative
                data = TCAData(Status.PId,ano[0])              
                data.loadTCAData() 
                #calculate cashflow for alternative
                data = self.calculateCashFlow(data)
                current = data.cashflow
                
                #set display option to 1 only for the current proposal
                display = 0
                
                #The currently selected proposal
                if (Status.ANo == ano[0]):
                    display = 1
                
                #calculate the results                  
                                
                npv = NPV(current.CF(), old.CF(), InterestRate)
                mirr = MIRR(current.CF(), old.CF(), InterestRate, DiscountRate)
                bcr = BCR(current.CF(), old.CF(), InterestRate)                    
                annuity = ANNUITY(current.TotalInvestmentCapital,InterestRate,ProjectLifetime)              
                pp = payback_period(npv)
                #set the results in data, store data in result list
                data.setResult(name,npv,mirr,bcr,annuity,pp,display)                                
                self.result.append(data)
                data.storeResultToCGeneralData()
            except Exception, inst:
                #print type(inst)
                #print inst.args
                #print inst
                data.setResultInvalid(name,display)
                self.result.append(data)
                logWarning((_("TCA: No result for %s") % ano[1]))
                logWarning(str(type(inst)))

        self.__setDataForReport()           
            
        
    def calculateCashFlow(self,data):                                     
        AmotisationTime        = data.TimeFrame + 1 #to fix calculation
        InterestRate           = data.NIR - data.Inflation
        EnergyPriceDevelopment = data.DEP  
              
        a = CashFlow(AmotisationTime, InterestRate, EnergyPriceDevelopment)
        
        a.TotalInvestmentCapital = 0
        a.EffectiveInvstmentCapital = 0
        a.TotalFundings = 0
        for investment in data.investment: 
            #Investment ------------------------------  
            value = investment[1]
            fp    = investment[2]
            ff    = investment[3]    
            a.TotalInvestmentCapital+= value   
            a.EffectiveInvstmentCapital+= value
            a.EffectiveInvstmentCapital-= value*(fp/100)+ff         
            a.Investment(0,-value)              
            #Funding ---------------------------------
            funding = value*(fp/100)+ff         
            a.TotalFundings+= funding
            a.Investment(0,funding)
             
        a.EffectiveInvstmentCapital-= data.revenue 
        a.Investment(0,data.revenue)       #Revenue
            
        for energy in data.energycosts:    #Energy
            demand = energy[1]
            price  = energy[2]
            a.Energy(-demand*price)     

        a.Operating(data.totalopcost)      #Operating
        
        for cont in data.contingencies:    #Contingencies
            Year  = cont[2]
            Value = cont[1]
            a.Contingency(Year,-Value)  
        
        for non in data.nonreoccuringcosts: #Non reocuring costs
            Value = non[1]
            Year  = non[2]
            Type  = non[3]
            if (Type == 'Cost'):
                a.Investment(Year,-Value)
            else:
                a.Investment(Year,Value)
        
        data.cashflow = a    
        return data 
    
    def __setDataForReport(self):
        FixedLineCount = 10
        self.__setReport47(self.keys[0], FixedLineCount)
        self.__setReport471(self.keys[1],FixedLineCount)
        bestAlternative = self.__setReport472(self.keys[2],FixedLineCount)
        self.__setReport52(self.keys[3], bestAlternative)
        
    def __setReport47(self,key,FixedLineCount):
        #Report Data 4.7
        #  1  Name OwnInvestment Npv PP MIRR BCR
        #...
        # 10
        data = []
        list = []  
        for result in self.result:                                 
            if result.ResultPresent:
                list.append([result.name, result.EIC, result.npv[len(result.npv)-1],result.PP,result.mirr[len(result.mirr)-1],result.bcr[len(result.bcr)-1]])     
        for i in range(0,min(len(list),FixedLineCount)):
            entry = list[i]
            data.append(entry)
        for i in range(len(list),FixedLineCount):
            data.append(["","","","","",""])                    
        Status.int.setGraphicsData(key,data)
        
    def __setReport471(self,key,FixedLineCount):
        #Report Data 4.7.1
        #  1  Name NPV MIRR PBP
        #...
        # 10
        data = []
        list = []  
        for result in self.result:                             
            if result.ResultPresent:
                if result.npv[len(result.npv)-1]<0:
                    list.append([result.name, result.npv[len(result.npv)-1],result.mirr[len(result.mirr)-1],result.PP])     
        for i in range(0,min(len(list),FixedLineCount)):
            entry = list[i]
            data.append(entry)
        for i in range(len(list),FixedLineCount):
            data.append(["","","",""])                    
        Status.int.setGraphicsData(key,data)
                
    def __setReport472(self,key,FixedLineCount):
        #Report Data 4.7.2
        #  1  Rating Name NPV
        #...
        # 10
        data = []
        list = []  
        for result in self.result:                  
            if result.ResultPresent:
                if result.npv[len(result.npv)-1]>0:
                    list.append([0, result.name, result.npv[len(result.npv)-1]])
        list.sort(lambda x, y: int(x[2])-int(y[2]))
        count = 1       
        for i in range(0,min(len(list),FixedLineCount)):
            entry = list[i]
            entry[0]=count
            count+=1
            data.append(entry)
        for i in range(len(list),FixedLineCount):
            data.append(["","",""])                    
        Status.int.setGraphicsData(key,data) 
        
        if (len(list)==0):
            return None
        else:
            name = list[0][1]
            for result in self.result:
                if (result.name == name):
                    return result         
        
    def __setReport52(self,key,bestAlternative):
        data = []
        
        if (bestAlternative==None):
            return

        data.append(bestAlternative.TIC)
        data.append(bestAlternative.totalfunding)   
        data.append(bestAlternative.revenue)  
        data.append(bestAlternative.annuity)
        data.append(bestAlternative.totalenergycost)
        data.append(bestAlternative.totalopcost)
        data.append(bestAlternative.contingencies)
        data.append(bestAlternative.nonreoccuringcosts)
        data.append(bestAlternative.npv[len(bestAlternative.npv)-1])
        data.append(bestAlternative.mirr[len(bestAlternative.mirr)-1])
        data.append(bestAlternative.PP)
        data.append(bestAlternative.bcr[len(bestAlternative.bcr)-1])
        
        Status.int.setGraphicsData(key,data) 

    
    def calculateTotalOpCostFromDetailedOpcost(self):
        cost = 0
        for category in self.data.detailedopcost:
            for entry in category:
                cost+=entry[1]
               
        self.data.totalopcost = cost
       
    def storeData(self):
        self.data.storeTCAData() 
    
    def resetData(self):
        self.data.resetTCAData()
        self.data.loadTCAData() 