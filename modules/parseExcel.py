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
from spreadsheetUtils import Utils
from dialogGauge import DialogGauge
 
import wx
import time


class parseExcel(parseSpreadsheet):
    def __init__(self,filepath,mysql_username,mysql_password):
        parseSpreadsheet.__init__(self, filepath)
        self.__filepath=filepath
        self.__username = mysql_username
        self.__password = mysql_password

    
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
    

    
    def __getExcelLists(self, sheetnames, xlWb , dlg): 
        lists = []
        if len(sheetnames)!=11:
            return Utils.parseError("wrong number of Sheets"), []
        try:
            sht = xlWb.Worksheets(sheetnames[0])
            Q1=Utils.tupleToList(sht.Range("Q1_GeneralData"))    
            Q1+=Utils.tupleToList(sht.Range("Q1_StatisticalData"))
            Q1+=Utils.tupleToList(sht.Range("Q1_Operation"))
            QProduct =Utils.tupleToList(sht.Range("Q1_Products"))
        except:
            return Utils.parseError(sheetnames[0]), []
        dlg.update(13)
        try:
            sht = xlWb.Worksheets(sheetnames[1])
            Q1+=Utils.tupleToList(sht.Range("Q1_Percent"))
            QProduct+=Utils.tupleToList(sht.Range("Q2_Products"))
            
            Q2 = Utils.tupleToList(sht.Range("Q2_EnergyConsumption"))
            Q2 += Utils.tupleToList(sht.Range("Q2_ElectricityConsumption"))
            Q2 += Utils.tupleToList(sht.Range("Q2_EnergyConsumptionProduct"))
            QFuel = Utils.tupleToList(sht.Range("Q2_EnergyConsumption"))
        except:
            return Utils.parseError(sheetnames[1]), []
        dlg.update(22)
        try:
            sht = xlWb.Worksheets(sheetnames[2])
            Q3 = Utils.tupleToList(sht.Range("Q3_ProcessData"))
            Q3 += Utils.tupleToList(sht.Range("Q3_WasteHeat"))
            Q3 += Utils.tupleToList(sht.Range("Q3_Schedule")) 
            Q3 += Utils.tupleToList(sht.Range("Q3_DataOfExistingHCSupply")) 
        except:
            return Utils.parseError(sheetnames[2]), []
        dlg.update(31)
        try:    
            sht= xlWb.Worksheets(sheetnames[3])
            Q3+= Utils.tupleToList(sht.Range("Q3_ScheduleTolerance"))
            Q3+= Utils.tupleToList(sht.Range("Q3_OperationCycle"))
            Q3+= Utils.tupleToList(sht.Range("Q3_ScheduleCorrelation"))
        except:
            return Utils.parseError(sheetnames[3]), []
        dlg.update(40)    
        try:    
            sht = xlWb.Worksheets(sheetnames[8])
            QRenewables = Utils.tupleToList(sht.Range("Q7_Interest"))
            QRenewables += Utils.tupleToList(sht.Range("Q7_REReason"))
            QRenewables += Utils.tupleToList(sht.Range("Q7_Others"))
            QRenewables += Utils.tupleToList(sht.Range("Q7_Latitude"))
            QRenewables += Utils.tupleToList(sht.Range("Q7_Biomass"))
            
            QSurf = Utils.tupleToList(sht.Range("Q7_Area"))
            QSurf += Utils.tupleToList(sht.Range("Q7_Roof"))
        except:
            return Utils.parseError(sheetnames[8]), []
        dlg.update(49)  
        try:    
            sht = xlWb.Worksheets(sheetnames[3])
            QProfiles = []
            QProcNames = Utils.tupleToList(sht.Range("Q3A_ProcessName"))
            for i in xrange(3):
                QProfil = Utils.tupleToList(sht.Range("Q3A_Profiles_"+ str(i+1)))
                QProfil.append(QProcNames[i*3])
                QProfiles.append(QProfil)
        
            QIntervals  = Utils.tupleToList(sht.Range("Q3A_StartTime_1"))
            QIntervals += Utils.tupleToList(sht.Range("Q3A_StartTime_2"))
            QIntervals += Utils.tupleToList(sht.Range("Q3A_StartTime_3"))
            QIntervals += Utils.tupleToList(sht.Range("Q3A_EndTime_1"))
            QIntervals += Utils.tupleToList(sht.Range("Q3A_EndTime_2"))
            QIntervals += Utils.tupleToList(sht.Range("Q3A_EndTime_3"))
        except:
            return Utils.parseError(sheetnames[3]), []
        dlg.update(57)
        try:
            sht = xlWb.Worksheets(sheetnames[10])
            Q9Questionnaire=[]
            for i in xrange(3):
                Q9Questionnaire+=Utils.tupleToList(sht.Range("Q9_"+str(i+1)))
        except:
            return Utils.parseError(sheetnames[10]), []
            
        dlg.update(66)
        Q4_8 = []    
        for i in xrange(5):
            try:
                Q4_8.append(Utils.tupleToList(xlWb.Worksheets(sheetnames[4]).Range("Q4H_"+str(i+1))))
                
            except:
                return self.parseError(sheetnames[4])
                
            try:    
                Q4_8.append(Utils.tupleToList(xlWb.Worksheets(sheetnames[5]).Range("Q4C_"+str(i+1))))
            except:
                return self.parseError(sheetnames[5])
            
            try:
                Q4_8.append(Utils.tupleToList(xlWb.Worksheets(sheetnames[6]).Range("Q5_"+str(i+1))))
            except:
                return self.parseError(sheetnames[6])
            
            try:
                Q4_8.append(Utils.tupleToList(xlWb.Worksheets(sheetnames[7]).Range("Q6_"+str(i+1))))
                
            except:
                return self.parseError(sheetnames[7])
                
            try:
                Q4_8.append(Utils.tupleToList(xlWb.Worksheets(sheetnames[9]).Range("Q8_"+str(i+1))))
                
            except:
                return self.parseError(sheetnames[9])
        try:
            latitude = self.__xlWb.Worksheets(sheetnames[8]).Range("Q7_Latitude")
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

    
    def parse(self):
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
        

        
    def __connectToDB(self):
        conn = MySQLdb.connect("localhost", self.__username, self.__password, db="einstein")
        md = pSQL.pSQL(conn, "einstein")
        return md
    

    

        
        

    
    
    


