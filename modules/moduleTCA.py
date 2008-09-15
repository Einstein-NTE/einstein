# -*- coding: cp1252 -*-
#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#   
#           
#------------------------------------------------------------------------------
#           
#   
#
#==============================================================================
#
#------------------------------------------------------------------------------     
#   (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#   www.energyxperts.net / info@energyxperts.net
#
#   This program is free software: you can redistribute it or modify it under
#   the terms of the GNU general public license as published by the Free
#   Software Foundation (www.gnu.org).
#
#============================================================================== 
from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
from einstein.modules.constants import *
from einstein.modules.messageLogger import *


class ModuleTCA(object):

    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel
        self.setDefaultValues()
                       
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#------------------------------------------------------------------------------           
        self.updatePanel()
  
  
    def setDefaultValues(self):
        #Main Page-------------------------------------------------
        self.LIR = 0       #Loan interest rate
        self.CSDR = 0      #Company specific discount rate
        self.DEP  = 0      #development of energy price
        self.TimeFrame = 1 #timeframe
        #Contigenies-----------------------------------------------
        self.contingencies = []
        #Non-reocurring costs--------------------------------------
        self.nonreoccuringcosts = []
        #Investment -----------------------------------------------
        self.investment = []
        self.revenue = 0 
        #subpage - revenue
        self.revenues = [] 
        #Energy & op cost -----------------------------------------
        self.energycost = []
        self.totalopcost = 0
        #subpage - Detailed opcost
        self.detailedopcost = [[],[],[],[],[],[],[]]
        
        
        #query = "SELECT sum(`TurnKeyPrice`) FROM `qgenerationhc` WHERE`Questionnaire_id`=%s AND `AlternativeProposalNo`=%s" % (Status.PId,Status.ANo)
        #result = Status.DB.sql_query(query)        
        #if (result != None):
        #    pass #add to investment        
        #print result
        
    
    def calculateTotalOpCostFromDetailedOpcost(self):
        cost = 0
        for category in self.detailedopcost:
            for entry in category:
                cost+=entry[1]
        self.totalopcost = cost
            
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------
       pass


