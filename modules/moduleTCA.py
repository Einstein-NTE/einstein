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
from einstein.GUI.status import *
from einstein.modules.interfaces import *
from einstein.modules.constants import *
from einstein.modules.messageLogger import *
from einstein.modules.dataTCA import TCAData
from einstein.modules.calculationTCA import *
import sys
from pylab import *


class ModuleTCA(object):

    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel 
        self.data = None    
        self.result = None
                       
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#------------------------------------------------------------------------------           
        self.updatePanel()
  

    def calculateTotalOpCostFromDetailedOpcost(self):
        cost = 0
        for category in self.data.detailedopcost:
            for entry in category:
                cost+=entry[1]
               
        self.data.totalopcost = cost
       
    def storeData(self):
        self.data.storeTCAData() 
            
#------------------------------------------------------------------------------
    def updatePanel(self):
        if (Status.ANo == -1):
            wx.MessageBox("Could not display TCA for unchecked state!")
            self.Hide()
            self.main.tree.SelectItem(self.main.qA, select=True)
            
        if (self.data == None):
            self.data = TCAData(Status.PId,Status.ANo)
            self.data.loadTCAData()        
        if (Status.PId != self.data.pid)or(Status.ANo != self.data.ano):
            self.data = TCAData(Status.PId,Status.ANo)
            self.data.loadTCAData()
        else:
            print "ok"
     
    
    def calculate(self):
        InterestRate = self.data.NIR - self.data.Inflation
        DiscountRate = self.data.CSDR - self.data.Inflation
        self.result = []    
        
        old     = self.getCashFlow(0)
        query = """SELECT AlternativeProposalNo,ShortName FROM salternatives WHERE ProjectID = %s"""
        query = query % (self.data.pid)
    
        results = Status.DB.sql_query(query)
        self.anos = []        
        
        for result in results:
            if (result[0]>0):
                self.anos.append([result[0],result[1]])              
        
        for ano in self.anos:
            current = self.getCashFlow(ano[0])
            display = 0
            if (Status.ANo == ano[0]):
                display = 1
            npv = NPV(current.CF(), old.CF(), InterestRate)
            mirr = MIRR(current.CF(), old.CF(), InterestRate, DiscountRate)
            bcr = BCR(current.CF(), old.CF(), InterestRate)        
            
            result = CalculationResult(ano[0],ano[1],npv,mirr,bcr,current.TotalInvestmentCapital,current.EffectiveInvstmentCapital,display)                           
            self.result.append(result)
            
              

        
        
        
        
        #current = self.getCashFlow(1)       
        #print NPV(current.CF(), old.CF(), InterestRate)
    
        
        #bcr = BCR(current.CF(), old.CF(), InterestRate) # call with <InterestRate>?
        #print
        #print "BCR: ", bcr
        #figure(3)
        #plot(bcr)
        #xlabel('time / Y')
        #ylabel('BCR')
        #title('benefit cost ratio')
        #grid(True)
        #show()
    
        #print
        #raw_input('Press any key to continue.')
        #close('all')              
        
    def getCashFlow(self,ano):
        data = TCAData(Status.PId,ano)                
        data.loadTCAData()   
                            
        AmotisationTime        = data.TimeFrame + 1 #to fix calculation
        InterestRate           = data.NIR - data.Inflation
        EnergyPriceDevelopment = data.DEP  
              
        a = CashFlow(AmotisationTime, InterestRate, EnergyPriceDevelopment)
        
        a.TotalInvestmentCapital = 0
        a.EffectiveInvstmentCapital = 0
        for investment in data.investment:   
            value = investment[1]
            fp    = investment[2]
            ff    = investment[3]    
            a.TotalInvestmentCapital+= value   
            a.EffectiveInvstmentCapital+= value
            a.EffectiveInvstmentCapital-= value*(fp/100)+ff         
            a.Investment(0,-value)              #Investment
            a.Investment(0,value*(fp/100)+ff)   #Funding
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
        
        del data                
        return a 