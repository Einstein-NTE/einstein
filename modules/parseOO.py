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
from spreadsheetUtils import SpreadsheetDict as SD
import xml.dom.minidom, zipfile

class parseOO(parseSpreadsheet):
    def __init__(self,filepath,mysql_username,mysql_password):
        parseSpreadsheet.__init__(self, filepath)
        self.__filepath=filepath
        self.__username = mysql_username
        self.__password = mysql_password
    
    def parse(self):
        self.__md = self.__connectToDB()
        xmlString = self.readOOContent(self.__filepath)
        parsedDom = xml.dom.minidom.parseString(xmlString)
        __handle, lists = self.__getLists(parsedDom)
        
        
        return __handle
        
    def __getLists(self,ooWb): 
        lists = []
        #if len(sheetnames)!=11:
        #    return self.__parseError("wrong number of Sheets"), []
        #try:
        sheetname = "Q1 GeneralData"
            
        Q1 = self.parseOOxmlarea(ooWb,"Q1_GeneralData",sheetname)      
        Q1+= self.parseOOxmlarea(ooWb, "Q1_StatisticalData", sheetname)
        Q1+= self.parseOOxmlarea(ooWb, "Q1_Operation", sheetname)
        QProduct = self.parseOOxmlarea(ooWb, "Q1_Products", sheetname)
        #except:
        #    return "parseError Sheet Q1", []
            #return self.__parseError(sheetnames[0]), []
        
        #try:
        sheetname = "Q2 EnergyConsumption"
        Q1+= self.parseOOxmlarea(ooWb, "Q1_Percent", sheetname)
        QProduct += self.parseOOxmlarea(ooWb, "Q2_Products", sheetname) 
        Q2 = self.parseOOxmlarea(ooWb, "Q2_EnergyConsumption", sheetname)    
        Q2+= self.parseOOxmlarea(ooWb, "Q2_ElectricityConsumption", sheetname) 
        Q2+= self.parseOOxmlarea(ooWb, "Q2_EnergyConsumptionProduct", sheetname)  
        QFuel = self.parseOOxmlarea(ooWb, "Q2_EnergyConsumption", sheetname)
        #except:
            #return "parseError Sheet Q2", []
            #return self.__parseError(sheetname), []
        
        #try:
        sheetname = "Q3_ Processes"
        Q3 = self.parseOOxmlarea(ooWb, "Q3_ProcessData", sheetname)
        Q3+= self.parseOOxmlarea(ooWb, "Q3_WasteHeat", sheetname)
        Q3+= self.parseOOxmlarea(ooWb, "Q3_Schedule", sheetname)
        Q3+= self.parseOOxmlarea(ooWb, "Q3_DataOfExistingHCSupply", sheetname)
 
        #except:
            #return "parseError Sheet Q3", []
            #return self.__parseError(sheetnames[2]), []
        #Q3A
        #try:    
        sheetname = "Q3A"
        
        Q3+= self.parseOOxmlarea(ooWb, "Q3_ScheduleTolerance", sheetname)
        Q3+= self.parseOOxmlarea(ooWb, "Q3_OperationCycle", sheetname)
        #except:
            #return self.__parseError(sheetnames[3]), []
            
        #try:    
        
        sheetname = "Q7_ Renewables"
        QRenewables = []
        QRenewables.append(self.parseOOxmlarea(ooWb, "Q7_Interest", sheetname))
        QRenewables += self.parseOOxmlarea(ooWb, "Q7_REReason", sheetname)
        QRenewables.append(self.parseOOxmlarea(ooWb, "Q7_Others", sheetname))
        QRenewables += self.parseOOxmlarea(ooWb, "Q7_Latitude", sheetname)
        QRenewables += self.parseOOxmlarea(ooWb, "Q7_Biomass", sheetname)
        
        QSurf = self.parseOOxmlarea(ooWb, "Q7_Area", sheetname)
        QSurf += self.parseOOxmlarea(ooWb, "Q7_Roof", sheetname)
        #except:
            #return self.__parseError(sheetnames[8]), []
        
        #try:    
        sheetname = "Q3A"
        QProfiles = []
        QProcNames = self.parseOOxmlarea(ooWb, "Q3A_ProcessName", sheetname)
        
        for i in xrange(3):
            QProfil = self.parseOOxmlarea(ooWb, "Q3A_Profiles_"+ str(i+1), sheetname)
            QProfil.append(QProcNames[i*3])
            QProfiles.append(QProfil)

        QIntervals  = self.parseOOxmlarea(ooWb, "Q3A_StartTime_1", sheetname)
        QIntervals += self.parseOOxmlarea(ooWb, "Q3A_StartTime_2", sheetname)
        QIntervals += self.parseOOxmlarea(ooWb, "Q3A_StartTime_3", sheetname)
        QIntervals += self.parseOOxmlarea(ooWb, "Q3A_EndTime_1", sheetname)
        QIntervals += self.parseOOxmlarea(ooWb, "Q3A_EndTime_2", sheetname)
        QIntervals += self.parseOOxmlarea(ooWb, "Q3A_EndTime_3", sheetname)
        #except:
            #return self.__parseError(sheetnames[3]), []
        
        #try:
        
        sheetname = "Q9 Economics"
        Q9Questionnaire=[]
        for i in xrange(3):
            Q9Questionnaire+=self.parseOOxmlarea(ooWb, "Q9_"+str(i+1), sheetname)

        #except:
            #return self.__parseError(sheetnames[10]), []
         
        
        Q4_8=[]
        # sheets with the same structure
        structureNames = ["Q4H_HeatGeneration",
                          "Q4C_ColdGeneration",
                          "Q5_Distribution",
                          "Q6_HeatRecovery",
                          "Q8 Buildings"]
        
        startStructure = ["Q4H_", "Q4C_", "Q5_", "Q6_", "Q8_"]
        
        for i in xrange(5):
            for j in xrange(len(structureNames)):
                try:
                    Q4_8.append(self.parseOOxmlarea(ooWb, startStructure[j]+str(i+1), structureNames[j]))
                except:
                    return structureNames[j],[]
         
        """
        Q4_8=[]
        for i in xrange(5):
            try:
                sheetname = "Q4H_HeatGeneration"
                Q4_8.append(self.parseOOxmlarea(ooWb, "Q4H_"+str(i+1), sheetname))
            except:
                return "Parsing failed at "+sheetname, []
                
           # try:
            sheetname = "Q4C_ColdGeneration"
            Q4_8.append(self.parseOOxmlarea(ooWb, "Q4C_"+str(i+1), sheetname))
            #except:
             #   return "Parsing failed at "+sheetname, []
            
            try:
                sheetname = "Q5_Distribution"
                Q4_8.append(self.parseOOxmlarea(ooWb, "Q5_"+str(i+1), sheetname))
            except:
                return "Parsing failed at "+sheetname, []
            
            try:
                sheetname = "Q6_HeatRecovery"
                Q4_8.append(self.parseOOxmlarea(ooWb, "Q6_"+str(i+1), sheetname))
                
            except:
                return "Parsing failed at "+sheetname, []
                
            try:
                sheetname = "Q8 Buildings"
                Q4_8.append(self.parseOOxmlarea(ooWb, "Q8_"+str(i+1), sheetname))
                
            except:
                return "Parsing failed at "+sheetname, []
        """
        
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
        return "Parsing successful!", lists
    
    def readOOContent(self, filename):
        """
        reads the input file (.ods) and opens the content.xml
        """
        # TODO Add Exception if File doesnt exist
        if zipfile.is_zipfile(filename):
            ziparchive = zipfile.ZipFile(filename, "r")
            archivedata = ziparchive.read("content.xml")
            return archivedata
    
    def parseOOxmlarea(self, parsedDom, area, worksheet):
        """
        parses the given string into a domstructure, and extracts a list of the given area.
        area: the assigned range in the .ods document
        Example usage: parseOOxmlarea(readOOContent("File.ods"),Areaname, Sheetname)
        
        returns a list with the data read from the ods file
        """
        
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
        # If only one cell is selected
        if len(cellrange)<4:
            tabledata =  tablerows[int(cellrange[1])-1].childNodes[ord(cellrange[0])-64-1]
            while tabledata.hasChildNodes():
                tabledata = tabledata.firstChild
            try:    
                return tabledata.data
            except:
                return None
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