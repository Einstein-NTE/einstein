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
#    SpreadsheetDictionary.py : Dictionarys for Database Translation
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

class SpreadsheetDict():
        def createQ1Dictionary(self,Q1):
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
            Q1dict['NEmployees']= Q1[26]
            Q1dict['Turnover']= Q1[27]
            Q1dict['ProdCost']= Q1[28]
            Q1dict['BaseYear']= Q1[29]
            Q1dict['Growth']= Q1[30]
    
            if Q1[31]=="no":
                Q1dict['Independent']= 0
            else: Q1dict['Independent']= 1
                
            Q1dict['OMThermal']= Q1[32]
            Q1dict['OMElectrical']= Q1[33]
            Q1dict['HPerDayInd']= Q1[34]
            Q1dict['NShifts']= Q1[38]
            Q1dict['NDaysInd']= Q1[42]
            #Q1dict['']= Q1[44]#principal period of holidays or stops for maintenance
            #Q1dict['']= Q1[45]
            #Q1dict['']= Q1[]
            return Q1dict
        
        def createQ2Dictionary(self,Q2):
            pass

        def createQ3Dictionary(self,Q3):
            pass
        
        def createQ4Dictionary(self,Q4):
            pass
        
        def createQ5Dictionary(self,Q5):
            pass
        
        def createQ6Dictionary(self,Q6):
            pass    
    
        createQ1Dictionary=staticmethod(createQ1Dictionary)
        createQ2Dictionary=staticmethod(createQ2Dictionary)
        createQ3Dictionary=staticmethod(createQ3Dictionary)
        createQ4Dictionary=staticmethod(createQ4Dictionary)
        createQ5Dictionary=staticmethod(createQ5Dictionary)
        createQ6Dictionary=staticmethod(createQ6Dictionary)
        
        
        
        