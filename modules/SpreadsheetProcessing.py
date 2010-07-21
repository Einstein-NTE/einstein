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
#    parseSpreadsheet.py
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
from parseExcel import ExcelSpreadsheetParser
from parseOO import OOSpreadsheetParser
from parseSpreadsheet import parseSpreadsheet
import MySQLdb
import pSQL
from spreadsheetUtils import SpreadsheetDict as SD
from spreadsheetUtils import Utils
import xml.dom.minidom, zipfile
from dialogGauge import DialogGauge
from einstein.GUI.status import *

class SpreadsheetProcessing():
    
    def __init__(self, inputfile, frame, fileending):
        self.__filepath=inputfile
        self.__fileending = fileending
        #self.__md = self.__connectToDB(frame.DBHost, frame.DBUser, frame.DBPass, frame.DBName)
        self.__md = Status.DB
        self.__error = 0
        if fileending == 'xls':
            try:
                self.spreadsheetparser = ExcelSpreadsheetParser(inputfile)
                self.__sheetnames = self.spreadsheetparser.sheetnames
                self.__dialog = ["Excel Parsing","reading document"]
            except:
                self.__error = 1
                
        elif fileending == 'ods':
            try:
                self.spreadsheetparser = OOSpreadsheetParser(inputfile)
                self.__sheetnames = self.spreadsheetparser.sheetnames
                self.__dialog = ["OpenOffice Calc Parsing","reading document"]
            except:
                self.__error = 1
            
    def parse(self):
        if self.__error == 0: 
            dlg = DialogGauge(None,self.__dialog[0],self.__dialog[1])
            self.spreadsheetparser.startProcessing()
            
            try:
                __handle, lists = self.__getLists(self.__sheetnames, dlg, self.spreadsheetparser)
            except:
                __handle, lists = "", []
            if len(lists)==0:
                self.spreadsheetparser.endProcessing()
                dlg.Destroy()
                return __handle
            dlg.update(80)
            DButil = Utils(self.__md, self.__sheetnames)
            try:
                __handle = DButil.writeToDB(lists)
            except:
                self.spreadsheetparser.endProcessing()
                dlg.Destroy()
                return "Error while writing to database"
            self.spreadsheetparser.endProcessing()
            dlg.Destroy()
        else:
            return "Parsing of Spreadsheet not possible. Check if all System Components exist. If Excel is opened, please close it!"
        
        Status.SQL.commit()
        return __handle
        
    def __getLists(self, sheetnames, dlg, spreadsheetparser):
        lists = []
        if len(sheetnames)!=11:
            return Utils.parseError("wrong number of Sheets"), []
        try:
            sht = sheetnames[0]
            Q1=spreadsheetparser.parseRange("Q1_GeneralData",sht)    
            Q1+=spreadsheetparser.parseRange("Q1_StatisticalData",sht)
            Q1+=spreadsheetparser.parseRange("Q1_Operation",sht)
            QProduct =spreadsheetparser.parseRange("Q1_Products",sht)
        except:
            return Utils.parseError(sheetnames[0]), []
        dlg.update(13)
        try:
            sht = sheetnames[1]
            Q1+=spreadsheetparser.parseRange("Q1_Percent",sht)
            QProduct+=spreadsheetparser.parseRange("Q2_Products",sht)
            Q2 = spreadsheetparser.parseRange("Q2_EnergyConsumption",sht)
            Q2 += spreadsheetparser.parseRange("Q2_ElectricityConsumption",sht)
            Q2 += spreadsheetparser.parseRange("Q2_EnergyConsumptionProduct",sht)
            QFuel = spreadsheetparser.parseRange("Q2_EnergyConsumption",sht)
        except:
            return Utils.parseError(sheetnames[1]), []
        dlg.update(22)
        try:
            sht = sheetnames[2]
            Q3 = spreadsheetparser.parseRange("Q3_ProcessData",sht)
            Q3 += spreadsheetparser.parseRange("Q3_WasteHeat",sht)
            Q3 += spreadsheetparser.parseRange("Q3_Schedule",sht) 
            Q3 += spreadsheetparser.parseRange("Q3_DataOfExistingHCSupply",sht) 
        except:
            return Utils.parseError(sheetnames[2]), []
        dlg.update(31)
        try:    
            sht= sheetnames[3]
            Q3+= spreadsheetparser.parseRange("Q3_ScheduleTolerance",sht)
            Q3+= spreadsheetparser.parseRange("Q3_OperationCycle",sht)
            Q3+= spreadsheetparser.parseRange("Q3_ScheduleCorrelation",sht)
        except:
            return Utils.parseError(sheetnames[3]), []
        dlg.update(40)    
        try: 
            sht = sheetnames[8]
            if(self.__fileending == 'xls'):
                QRenewables = []
                QRenewables += spreadsheetparser.parseRange("Q7_Interest",sht)
                QRenewables += spreadsheetparser.parseRange("Q7_REReason",sht)
                QRenewables += spreadsheetparser.parseRange("Q7_Others",sht)
                QRenewables += spreadsheetparser.parseRange("Q7_Latitude",sht)
                QRenewables += spreadsheetparser.parseRange("Q7_Biomass",sht)
            else:
                QRenewables = []
                QRenewables.append(spreadsheetparser.parseRange( "Q7_Interest", sht))
                QRenewables += spreadsheetparser.parseRange( "Q7_REReason", sht)
                QRenewables.append(spreadsheetparser.parseRange( "Q7_Others", sht))
                QRenewables += spreadsheetparser.parseRange( "Q7_Latitude", sht)
                QRenewables += spreadsheetparser.parseRange( "Q7_Biomass", sht)
            
            QSurf = spreadsheetparser.parseRange("Q7_Area",sht)
            QSurf += spreadsheetparser.parseRange("Q7_Roof",sht)
        except:
            return Utils.parseError(sheetnames[8]), []
        dlg.update(49)  
        try:    
            sht = sheetnames[3]
            QProfiles = []
            QProcNames = spreadsheetparser.parseRange("Q3A_ProcessName",sht)
            for i in xrange(3):
                QProfil = spreadsheetparser.parseRange("Q3A_Profiles_"+ str(i+1), sht)
                QProfil.append(QProcNames[i*3])
                QProfiles.append(QProfil)
        
            QIntervals  = spreadsheetparser.parseRange("Q3A_StartTime_1",sht)
            QIntervals += spreadsheetparser.parseRange("Q3A_StartTime_2",sht)
            QIntervals += spreadsheetparser.parseRange("Q3A_StartTime_3",sht)
            QIntervals += spreadsheetparser.parseRange("Q3A_EndTime_1",sht)
            QIntervals += spreadsheetparser.parseRange("Q3A_EndTime_2",sht)
            QIntervals += spreadsheetparser.parseRange("Q3A_EndTime_3",sht)
        except:
            return Utils.parseError(sheetnames[3]), []
        dlg.update(57)
        try:
            sht = sheetnames[10]
            Q9Questionnaire=[]
            for i in xrange(3):
                Q9Questionnaire+=spreadsheetparser.parseRange("Q9_"+str(i+1),sht)
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
                    Q4_8.append(spreadsheetparser.parseRange( startStructure[j]+str(i+1), structureNames[j]))
                except:
                    return structureNames[j] + " " + startStructure[j]+str(i+1),[]
                    
        
        try:
            sht = sheetnames[8]
            latitude = spreadsheetparser.parseRange("Q7_Latitude",sht)
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
        
        return "", lists
    
    def __connectToDB(self, hostname, username, password, dbname):
        __conn = MySQLdb.connect(hostname, username, password, db=dbname)
        __md = pSQL.pSQL(__conn, dbname)
        return __md
    
    
    
    
    
    
    
    
    
    