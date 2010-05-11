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
#    parseOO.py : provides functionality to parse Open Office Questionnaires
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
from SpreadsheetDictionary import SpreadsheetDict as SD
import xml.dom.minidom, zipfile

class parseOO(parseSpreadsheet):
    def __init__(self,filepath,mysql_username,mysql_password):
        parseSpreadsheet.__init__(self, filepath)
        self.__filepath=filepath
        self.__username = mysql_username
        self.__password = mysql_password
    
    def parse(self):
        self.__md = self.__connectToDB()
        ooWb = readOOContent(self.__filepath)
        __handle, lists = self.__getLists(ooWb)
        
        return "not implemented"
        
    def __getLists(self,ooWb): 
        lists = []
        #if len(sheetnames)!=11:
        #    return self.__parseError("wrong number of Sheets"), []
        try:
            sheetname = "Q1_GeneralData"
            
            Q1 = self.parseOOxmlarea(ooWb,"Q1_GeneralData",sheetname)
            Q1+= self.parseOOxmlarea(ooWb, "Q1_StatisticalData", sheetname)
            Q1+= self.parseOOxmlarea(ooWb, "Q1_Operation", sheetname)
            QProduct = self.parseOOxmlarea(ooWb, "Q1_Products", sheetname)
            
        except:
            pass
            #return self.__parseError(sheetnames[0]), []
        
        try:
            sheetname = "Q2 EnergyConsumption"
            Q1+= self.parseOOxmlarea(ooWb, "Q1_Percent", sheetname)
            QProduct += self.parseOOxmlarea(ooWb, "Q2_Products", sheetname) 
            Q2 = self.parseOOxmlarea(ooWb, "Q2_EnergyConsumption", sheetname)    
            Q2+= self.parseOOxmlarea(ooWb, "Q2_ElectricityConsumption", sheetname) 
            Q2+= self.parseOOxmlarea(ooWb, "Q2_EnergyConsumptionProduct", sheetname)  
            QFuel = self.parseOOxmlarea(ooWb, "Q2_EnergyConsumption", sheetname)
        except:
            pass
            #return self.__parseError(sheetname), []
        
        try:
            sheetname = "Q3_ Processes"
            Q2 = self.parseOOxmlarea(ooWb, "Q3_ProcessData", sheetname)
            Q2+= self.parseOOxmlarea(ooWb, "Q3_WasteHeat", sheetname)
            Q2+= self.parseOOxmlarea(ooWb, "Q3_Schedule", sheetname)
            Q2+= self.parseOOxmlarea(ooWb, "Q3_DataOfExistingHCSupply", sheetname)
 
        except:
            pass
            #return self.__parseError(sheetnames[2]), []
        """    
        try:    
            sht= xlWb.Worksheets(sheetnames[3])
            Q3+= self.__tupleToList(sht.Range("Q3_ScheduleTolerance"))
            Q3+= self.__tupleToList(sht.Range("Q3_OperationCycle"))
        except:
            return self.__parseError(sheetnames[3]), []
            
        try:    
            sht = xlWb.Worksheets(sheetnames[8])
            QRenewables = self.__tupleToList(sht.Range("Q7_Interest"))
            QRenewables += self.__tupleToList(sht.Range("Q7_REReason"))
            QRenewables += self.__tupleToList(sht.Range("Q7_Others"))
            QRenewables += self.__tupleToList(sht.Range("Q7_Latitude"))
            QRenewables += self.__tupleToList(sht.Range("Q7_Biomass"))
            
            QSurf = self.__tupleToList(sht.Range("Q7_Area"))
            QSurf += self.__tupleToList(sht.Range("Q7_Roof"))
        except:
            return self.__parseError(sheetnames[8]), []
          
        try:    
            sht = xlWb.Worksheets(sheetnames[3])
            QProfiles = []
            QProcNames = self.__tupleToList(sht.Range("Q3A_ProcessName"))
            
            for i in xrange(3):
                QProfil = self.__tupleToList(sht.Range("Q3A_Profiles_"+ str(i+1)))
                QProfil.append(QProcNames[i*3])
                QProfiles.append(QProfil)
        
            QIntervals  = self.__tupleToList(sht.Range("Q3A_StartTime_1"))
            QIntervals += self.__tupleToList(sht.Range("Q3A_StartTime_2"))
            QIntervals += self.__tupleToList(sht.Range("Q3A_StartTime_3"))
            QIntervals += self.__tupleToList(sht.Range("Q3A_EndTime_1"))
            QIntervals += self.__tupleToList(sht.Range("Q3A_EndTime_2"))
            QIntervals += self.__tupleToList(sht.Range("Q3A_EndTime_3"))
        except:
            return self.__parseError(sheetnames[3]), []
        
        try:
            sht = xlWb.Worksheets(sheetnames[10])
            Q9Questionnaire=[]
            for i in xrange(3):
                Q9Questionnaire+=self.__tupleToList(sht.Range("Q9_"+str(i+1)))
        except:
            return self.__parseError(sheetnames[10]), []
        """    
        lists.append(Q1)
        lists.append(Q2)
        lists.append(QProduct)
        lists.append(QFuel)
        """
        lists.append(Q3)
        lists.append(QRenewables)
        lists.append(QSurf)
        lists.append(QProfiles)
        lists.append(QIntervals)
        lists.append(Q9Questionnaire)
        """
        return "", lists
    
    def readOOContent(filename):
        """
        reads the input file (.ods) and opens the content.xml
        """
        # TODO Add Exception if File doesnt exist
        if zipfile.is_zipfile(filename):
            ziparchive = zipfile.ZipFile(filename, "r")
            archivedata = ziparchive.read("content.xml")
            return archivedata
    
    def parseOOxmlarea(xmlString,area,worksheet):
        """
        parses the given string into a domstructure, and extracts a list of the given area.
        area: the assigned range in the .ods document
        Example usage: parseOOxmlarea(readOOContent("File.ods"),"PersonalInfo")
        
        returns a list with the data read from the ods file
        """
        parsedDom = xml.dom.minidom.parseString(xmlString)
        
        #Get all named expressions and resolve the areas
        namedrange = parsedDom.getElementsByTagName("table:named-range")
        
        table = None
        cellrange = None
        for elem in namedrange:
            if elem.getAttribute("table:name")==area:
                cellrange = elem.getAttribute("table:cell-range-address")
                break    
        if cellrange == None:
            print "Area not found"
            return
        cellrange = cellrange.split('$')
        cellr = []
    
        for elem in xrange(2,len(cellrange)):
            cellr.append(cellrange[elem].strip(".:"))
        cellrange = cellr
        #Test cellrange for correct values and length(ascii signs, numbers)
        #On OO only rectangular areas can be selected -> length should be ok
        domtable = parsedDom.getElementsByTagName("table:table")
        for elem in domtable:
            if elem.getAttribute("table:name")==worksheet:
                table = elem
        if table == None:
            print "Area not found"
            return
        tablerows = table.getElementsByTagName("table:table-row")
        data = []
        repeatedcells=0
        sumRepeatedCells=0
        for i in xrange(int(cellrange[1]), int(cellrange[3])+1):
            for j in xrange(ord(cellrange[0])-64, ord(cellrange[2])-64+1):
                tabledata = tablerows[i-1].childNodes[j-1]
                if tabledata.hasAttribute("table:number-columns-repeated"):
                    repeatedcells= int(tabledata.getAttribute("table:number-columns-repeated"))
                    if repeatedcells ==1014:
                        break
                    [data.append(None) for k in xrange(0,repeatedcells)]
                    sumRepeatedCells+=repeatedcells
                    repeatedcells=0
                    continue
                if sumRepeatedCells+j > ord(cellrange[2])-64+1:
                    break
                while tabledata.hasChildNodes():
                    tabledata = tabledata.firstChild
                try:
                    data.append(tabledata.data)
                except:
                    data.append(None)
        return data
        
        
    
    def __connectToDB(self):
        conn = MySQLdb.connect("localhost", self.__username, self.__password, db="einstein")
        md = pSQL.pSQL(conn, "einstein")
        return md