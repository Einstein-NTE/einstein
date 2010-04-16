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
    
    def parse(self):
        self.__xlApp = Dispatch("Excel.Application")
        self.__xlWb = self.__xlApp.Workbooks.Open(self.__filepath)
        self.__md = self.__connectToDB()
        self.handle = self.__readQ()    
        self.__xlWb.Close(SaveChanges=0)
        self.__xlApp.Quit()
        return self.handle    
        
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
        
        

    
    
    


