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
        def createQuestionnaireDictionary(self,Q1):
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
        
        def createQElectricityDictionary(self,Q2):
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
            return Q2dict

        def createQ3Dictionary(self,Q3):
            pass
        
        def createQ4Dictionary(self,Q4):
            pass
        
        def createQ5Dictionary(self,Q5):
            pass
        
        def createQ6Dictionary(self,Q6):
            pass    
    
        createQuestionnaireDictionary=staticmethod(createQuestionnaireDictionary)
        createQElectricityDictionary=staticmethod(createQElectricityDictionary)
        createQ3Dictionary=staticmethod(createQ3Dictionary)
        createQ4Dictionary=staticmethod(createQ4Dictionary)
        createQ5Dictionary=staticmethod(createQ5Dictionary)
        createQ6Dictionary=staticmethod(createQ6Dictionary)
        
        
        
        