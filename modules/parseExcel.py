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
#    ExcelSpreadsheetParser.py : provides functionality to parse Excel Questionnaires
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

from parseSpreadsheet import parseSpreadsheet
import MySQLdb
import pSQL
try:
    from win32com.client import Dispatch
except ImportError:
    pass

from spreadsheetUtils import Utils
from dialogGauge import DialogGauge
 
import wx
import time


class ExcelSpreadsheetParser(parseSpreadsheet):
    def __init__(self,filepath):
        parseSpreadsheet.__init__(self, filepath)
        self.__filepath=filepath
        self.__xlApp, self.__xlWb = self.__openExcelDispatch(self.__filepath)
        __sheets = self.__xlWb.Sheets
        self.sheetnames = []
        for i in xrange(0,__sheets.count):
            if __sheets[i].Name[0] == 'Q':
                self.sheetnames.append(__sheets[i].Name)
    
    
    def __tupleToList(self,tuple):
        data = []
        for elem in tuple:
            data.append(elem.GetValue())
        return data
    
    def __openExcelDispatch(self,filepath):
        xlApp = Dispatch("Excel.Application")
        xlWb = xlApp.Workbooks.Open(filepath)
        return xlApp, xlWb
    
    def __closeExcelDispatch(self,xlWb,xlApp):
        xlWb.Close(SaveChanges=0)
        xlApp.Quit()
    
    def parseRange(self, range, sht):
        return Utils.tupleToList(self.__xlWb.Worksheets(sht).Range(range)) 
    
    def __getExcelLists(self, sheetnames, xlWb , dlg): 
        lists = []
        if len(sheetnames)!=11:
            return Utils.parseError("wrong number of Sheets"), []
        try:
            sht = sheetnames[0]
            Q1=self.parseRange("Q1_GeneralData",sht)    
            Q1+=self.parseRange("Q1_StatisticalData",sht)
            Q1+=self.parseRange("Q1_Operation",sht)
            QProduct =self.parseRange("Q1_Products",sht)
        except:
            return Utils.parseError(sheetnames[0]), []
        dlg.update(13)
        try:
            sht = sheetnames[1]
            Q1+=self.parseRange("Q1_Percent",sht)
            QProduct+=self.parseRange("Q2_Products",sht)
            Q2 = self.parseRange("Q2_EnergyConsumption",sht)
            Q2 += self.parseRange("Q2_ElectricityConsumption",sht)
            Q2 += self.parseRange("Q2_EnergyConsumptionProduct",sht)
            QFuel = self.parseRange("Q2_EnergyConsumption",sht)
        except:
            return Utils.parseError(sheetnames[1]), []
        dlg.update(22)
        try:
            sht = sheetnames[2]
            Q3 = self.parseRange("Q3_ProcessData",sht)
            Q3 += self.parseRange("Q3_WasteHeat",sht)
            Q3 += self.parseRange("Q3_Schedule",sht) 
            Q3 += self.parseRange("Q3_DataOfExistingHCSupply",sht) 
        except:
            return Utils.parseError(sheetnames[2]), []
        dlg.update(31)
        try:    
            sht= sheetnames[3]
            Q3+= self.parseRange("Q3_ScheduleTolerance",sht)
            Q3+= self.parseRange("Q3_OperationCycle",sht)
            Q3+= self.parseRange("Q3_ScheduleCorrelation",sht)
        except:
            return Utils.parseError(sheetnames[3]), []
        dlg.update(40)    
        try:    
            sht = sheetnames[8]
            QRenewables = []
            QRenewables += self.parseRange("Q7_Interest",sht)
            QRenewables += self.parseRange("Q7_REReason",sht)
            QRenewables += self.parseRange("Q7_Others",sht)
            QRenewables += self.parseRange("Q7_Latitude",sht)
            QRenewables += self.parseRange("Q7_Biomass",sht)
            
            QSurf = self.parseRange("Q7_Area",sht)
            QSurf += self.parseRange("Q7_Roof",sht)
        except:
            return Utils.parseError(sheetnames[8]), []
        dlg.update(49)  
        try:    
            sht = sheetnames[3]
            QProfiles = []
            QProcNames = self.parseRange("Q3A_ProcessName",sht)
            for i in xrange(3):
                QProfil = self.parseRange("Q3A_Profiles_"+ str(i+1), sht)
                QProfil.append(QProcNames[i*3])
                QProfiles.append(QProfil)
        
            QIntervals  = self.parseRange("Q3A_StartTime_1",sht)
            QIntervals += self.parseRange("Q3A_StartTime_2",sht)
            QIntervals += self.parseRange("Q3A_StartTime_3",sht)
            QIntervals += self.parseRange("Q3A_EndTime_1",sht)
            QIntervals += self.parseRange("Q3A_EndTime_2",sht)
            QIntervals += self.parseRange("Q3A_EndTime_3",sht)
        except:
            return Utils.parseError(sheetnames[3]), []
        dlg.update(57)
        try:
            sht = sheetnames[10]
            Q9Questionnaire=[]
            for i in xrange(3):
                Q9Questionnaire+=self.parseRange("Q9_"+str(i+1),sht)
        except:
            return Utils.parseError(sheetnames[10]), []
            
        dlg.update(66)
        
         
        Q4_8=[]
        # sheets with the same structure
        structureNames = ["Q4H_HeatGeneration",
                          "Q4C_ColdGeneration",
                          "Q5_Distribution",
                          "Q6_HeatRecovery",
                          "Q8 Buildings"]
        
        startStructure = ["Q4H_", "Q4C_", "Q5_", "Q6_", "Q8_"]
        
        
        # Change to xrange(5) to get all sheets --> Q4C_5
        for i in xrange(5):
            for j in xrange(len(structureNames)):
                try:
                    Q4_8.append(self.parseRange( startStructure[j]+str(i+1), structureNames[j]))
                except:
                    return structureNames[j] + " " + startStructure[j]+str(i+1),[]
                    
        
        
        try:
            sht = sheetnames[8]
            latitude = self.parseRange("Q7_Latitude",sht)
        except:
            return self.parseError(sheetnames[8])
        dlg.update(72)

        lists.append(Q1)
        lists.append(Q2)
        lists.append(QProduct)
        lists.append(QFuel)
        lists.append(Q3)
        lists.append(QRenewables)
        lists.append(QSurf)
        lists.append(QProfiles)
        lists.append(QIntervals)
        lists.append(Q9Questionnaire)
        lists.append(Q4_8)
        lists.append(latitude)
        
        
        """
        biglist = []
        for listelem in lists:
            QList = []
            for elem in listelem:
                try:
                    QList.append(float(elem))
                except:
                    try:
                        QList.append(float(str(elem).replace(',', '.')))
                    except:
                        if type(elem) == type(QList):
                           list = []
                           for el in elem:
                               try:
                                   list.append(float(el))
                               except:
                                   try:
                                       list.append(float(str(el).replace(',', '.')))
                                   except:
                                       list.append(el)
                           QList.append(list)
                        else:
                            QList.append(elem)
            biglist.append(QList)
        print biglist
        """
       
        return "", lists

    @DeprecationWarning
    def parseold(self):
        dlg = DialogGauge(None,"Excel Parsing","reading document")
        Q1 = Q2 = QProduct = QFuel = Q3 = QRenewables = QSurf = QProfiles = QIntervals = Q9Questionnaire = []
        try:
            self.__xlApp, self.__xlWb = self.__openExcelDispatch(self.__filepath)
            __sheets = self.__xlWb.Sheets
            self.__sheetnames = []
            for i in xrange(0,__sheets.count):
                if __sheets[i].Name[0] == 'Q':
                    self.__sheetnames.append(__sheets[i].Name)
            self.__md = self.__connectToDB()
            
        except:
            self.__closeExcelDispatch(self.__xlWb, self.__xlApp)
            return Utils.parseError("Consistency")
        dlg.update(5)
        try:
            __handle, lists = self.__getExcelLists(self.__sheetnames, self.__xlWb,dlg)
        except:
            try:
                time.sleep(3)
                self.__xlApp, self.__xlWb = openExcelDispatch()
                __handle, lists = self.__getExcelLists(self.__sheetnames, self.__xlWb,dlg)
            except:
                try:
                    time.sleep(3)
                    self.__xlApp, self.__xlWb = openExcelDispatch()
                    __handle, lists = self.__getExcelLists(self.__sheetnames, self.__xlWb, dlg)
                except:
                    self.__closeExcelDispatch(self.__xlWb, self.__xlApp)
                    return Utils.parseError("Consistency")
                
        
        DButil = Utils(self.__md, self.__sheetnames)
        dlg.update(75)
        __handle = DButil.writeToDB(lists)
        dlg.update(100)
        dlg.Destroy()
        self.__closeExcelDispatch(self.__xlWb, self.__xlApp)
        return __handle
        
    def startProcessing(self):
        pass

    def setLists(self, lists):
        self.__lists = lists
        
    def endProcessing(self):
        self.__closeExcelDispatch(self.__xlWb, self.__xlApp)
        


    

        
        

    
    
    


