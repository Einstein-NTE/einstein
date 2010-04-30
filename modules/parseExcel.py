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
#    parseExcel.py : provides functionality to parse Excel Questionnaires
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
from win32com.client import Dispatch
from SpreadsheetDictionary import SpreadsheetDict as SD
import wx


class parseExcel(parseSpreadsheet):
    def __init__(self,filepath,mysql_username,mysql_password):
        parseSpreadsheet.__init__(self, filepath)
        self.__filepath=filepath
        self.__username = mysql_username
        self.__password = mysql_password
    
    def __tupleToSimpleList(self,tuple):
        data = []
        for elem in tuple:
            data.append(elem.GetValue())
        return data
    
    def openExcelDispatch(self,filepath):
        xlApp = Dispatch("Excel.Application")
        xlWb = xlApp.Workbooks.Open(filepath)
        return xlApp, xlWb
    
    def splitExcelColumns(self,nr_of_elements, columns, parsed_list,dict,Questionnaire_id,createDictionary,db_table):
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
            Dict = createDictionary(list)
            if Questionnaire_id != "":
                Dict['Questionnaire_id']= Questionnaire_id
            Dict.update(dict)
            db_table.insert(Dict)
            list = []
    
    def getExcelLists(self, sheetnames, xlWb): 
        sht = xlWb.Worksheets(sheetnames[0])
        
        Q1=tupleToList(sht.Range("Q1_GeneralData"))    
        Q1+=tupleToList(sht.Range("Q1_StatisticalData"))
        Q1+=tupleToList(sht.Range("Q1_Operation"))
        
        QProduct =tupleToList(sht.Range("Q1_Products"))
        
        sht = xlWb.Worksheets(sheetnames[1])
        
        Q1+=tupleToList(sht.Range("Q1_Percent"))
        QProduct+=tupleToList(sht.Range("Q2_Products"))
        
        Q2 = tupleToList(sht.Range("Q2_EnergyConsumption"))
        Q2 += tupleToList(sht.Range("Q2_ElectricityConsumption"))
        Q2 += tupleToList(sht.Range("Q2_EnergyConsumptionProduct"))
        QFuel = tupleToList(sht.Range("Q2_EnergyConsumption"))
        
        sht = xlWb.Worksheets(sheetnames[2])
        Q3 = tupleToList(sht.Range("Q3_ProcessData"))
        Q3 += tupleToList(sht.Range("Q3_WasteHeat"))
        Q3 += tupleToList(sht.Range("Q3_Schedule")) 
        Q3 += tupleToList(sht.Range("Q3_DataOfExistingHCSupply")) 
        
        sht= xlWb.Worksheets(sheetnames[3])
        Q3+= tupleToList(sht.Range("Q3_ScheduleTolerance"))
        Q3+= tupleToList(sht.Range("Q3_OperationCycle"))
        
        sht = xlWb.Worksheets(sheetnames[8])
        QRenewables = tupleToList(sht.Range("Q7_Interest"))
        QRenewables += tupleToList(sht.Range("Q7_REReason"))
        QRenewables += tupleToList(sht.Range("Q7_Others"))
        QRenewables += tupleToList(sht.Range("Q7_Latitude"))
        QRenewables += tupleToList(sht.Range("Q7_Biomass"))
        
        QSurf = tupleToList(sht.Range("Q7_Area"))
        QSurf += tupleToList(sht.Range("Q7_Roof"))
        
        sht = xlWb.Worksheets(sheetnames[3])
    
        QProfiles = []
        QProcNames = tupleToList(sht.Range("Q3A_ProcessName"))
        
        for i in xrange(3):
            QProfil = tupleToList(sht.Range("Q3A_Profiles_"+ str(i+1)))
            QProfil.append(QProcNames[i*3])
            QProfiles.append(QProfil)
    
            
        QIntervals  = tupleToList(sht.Range("Q3A_StartTime_1"))
        QIntervals += tupleToList(sht.Range("Q3A_StartTime_2"))
        QIntervals += tupleToList(sht.Range("Q3A_StartTime_3"))
        QIntervals += tupleToList(sht.Range("Q3A_EndTime_1"))
        QIntervals += tupleToList(sht.Range("Q3A_EndTime_2"))
        QIntervals += tupleToList(sht.Range("Q3A_EndTime_3"))
        
        
        return Q1, Q2, QProduct, QFuel, Q3 , QRenewables, QSurf, QProfiles, QIntervals

    
    def parse(self):
        self.__xlApp, self.__xlWb = self.openExcelDispatch(self.__filepath)
        __md = self.__connectToDB()
        __handle = self.__readQ()    
        self.__xlWb.Close(SaveChanges=0)
        self.__xlApp.Quit()
        return __handle    
        
    def __connectToDB(self):
        conn = MySQLdb.connect("localhost", self.__username, self.__password, db="einstein")
        md = pSQL.pSQL(conn, "einstein")
        return md
    
    def __readQ(self):

        sheets = self.__xlWb.Sheets
        sheetnames = []
        
        for i in xrange(0,sheets.count):
            if sheets[i].Name[0] == 'Q':
                sheetnames.append(sheets[i].Name)
        
        """
        for i in xrange(0,len(sheetnames)):
            try:
                sht.append(self.__xlWb.Worksheets(sheetnames[i]))
            except:
                return 'Failed to import ' + self.__filepath + ' at table: ' + sheetnames[i] + "!"
        """
        
        try:
            sht = self.__xlWb.Worksheets(sheetnames[0])
            self.__Q1GD=self.__tupleToSimpleList(sht.Range("GeneralData"))
            self.__Q1GD+=self.__tupleToSimpleList(sht.Range("StatisticalData"))
            self.__Q1GD+=self.__tupleToSimpleList(sht.Range("PeriodOfOperation"))
            self.__Q1GD+=self.__tupleToSimpleList(sht.Range("InformationOnProducts"))
            self.__md.questionnaire.insert(SD.createQuestionnaireDictionary(self,self.__Q1GD))
            #return 'Import completed!'
        except:
            return 'Failed to parse ' + self.__filepath + ' at table: ' + sheetnames[0] + "!"
        
        try:
            sht = self.__xlWb.Worksheets(sheetnames[1])
            self.__Qelectricity= self.__tupleToSimpleList(sht.Range("EnergyConsumption"))
            self.__Qelectricity+=self.__tupleToSimpleList(sht.Range("ElectricityConsumption"))
            self.__Qelectricity+=self.__tupleToSimpleList(sht.Range("EnergyConsumptionProduct"))
            self.__md.qelectricity.insert(SD.createQElectricityDictionary(self,self.__Qelectricity))
        except:
            return 'Failed to parse ' + self.__filepath + ' at table: ' + sheetnames[1] + "!"
        
        return 'Import completed!'
    
    def printQ1(self):
        md = self.__connectToDB() 
        quest = md.questionnaire
        quest = quest.sql_select("")
        for elem in quest:
            print elem
        
        

    
    
    


