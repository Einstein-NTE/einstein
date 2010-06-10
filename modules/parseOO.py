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
from spreadsheetUtils import Utils
import xml.dom.minidom, zipfile
from dialogGauge import DialogGauge

class parseOO(parseSpreadsheet):
    def __init__(self,filepath,mysql_username,mysql_password):
        parseSpreadsheet.__init__(self, filepath)
        self.__filepath=filepath
        self.__username = mysql_username
        self.__password = mysql_password
    
    def parse(self):
        
        __sheetnames = [u'Q1 GeneralData', 
              u'Q2 EnergyConsumption', 
              u'Q3_ Processes', 
              u'Q3A', 
              u'Q4H_HeatGeneration', 
              u'Q4C_ColdGeneration', 
              u'Q5_Distribution', 
              u'Q6_HeatRecovery', 
              u'Q7_ Renewables', 
              u'Q8 Buildings', 
              u'Q9 Economics']
        
        dlg = DialogGauge(None,"OpenOffice Calc Parsing","reading document")
        self.__md = self.__connectToDB()
        xmlString = self.readOOContent(self.__filepath)
        dlg.update(10)
        parsedDom = xml.dom.minidom.parseString(xmlString)
        dlg.update(53)
        
        __handle, lists = self.__getLists(parsedDom, dlg, __sheetnames)
        DButil = Utils(self.__md, __sheetnames)
        __handle = DButil.writeToDB(lists)
        dlg.update(100)
        dlg.Destroy()
        return __handle
        
    def __getLists(self,ooWb,dlg, sheetnames): 
        lists = []
        #if len(sheetnames)!=11:
        #    return self.__parseError("wrong number of Sheets"), []
        try:
            Q1 = self.parseOOxmlarea(ooWb,"Q1_GeneralData",sheetnames[0])      
            Q1+= self.parseOOxmlarea(ooWb, "Q1_StatisticalData", sheetnames[0])
            Q1+= self.parseOOxmlarea(ooWb, "Q1_Operation", sheetnames[0])
            QProduct = self.parseOOxmlarea(ooWb, "Q1_Products", sheetnames[0])
        except:
            return "parseError Sheet Q1", []
            #return self.__parseError(sheetnames[0]), []
        dlg.update(60)
        try:
            Q1+= self.parseOOxmlarea(ooWb, "Q1_Percent", sheetnames[1])
            QProduct += self.parseOOxmlarea(ooWb, "Q2_Products", sheetnames[1]) 
            Q2 = self.parseOOxmlarea(ooWb, "Q2_EnergyConsumption", sheetnames[1])    
            Q2+= self.parseOOxmlarea(ooWb, "Q2_ElectricityConsumption", sheetnames[1]) 
            Q2+= self.parseOOxmlarea(ooWb, "Q2_EnergyConsumptionProduct", sheetnames[1])  
            QFuel = self.parseOOxmlarea(ooWb, "Q2_EnergyConsumption", sheetnames[1])
        except:
            return "parseError Sheet Q2", []
            #return self.__parseError(sheetname), []
        dlg.update(68)
        try:
            Q3 = self.parseOOxmlarea(ooWb, "Q3_ProcessData", sheetnames[2])
            Q3+= self.parseOOxmlarea(ooWb, "Q3_WasteHeat", sheetnames[2])
            Q3+= self.parseOOxmlarea(ooWb, "Q3_Schedule", sheetnames[2])
            Q3+= self.parseOOxmlarea(ooWb, "Q3_DataOfExistingHCSupply", sheetnames[2])
     
            dlg.update(76)
        except:
            return "parseError Sheet Q3", []
            #return self.__parseError(sheetnames[2]), []
        #Q3A
        try:    

            Q3+= self.parseOOxmlarea(ooWb, "Q3_ScheduleTolerance", sheetnames[3])
            Q3+= self.parseOOxmlarea(ooWb, "Q3_OperationCycle", sheetnames[3])
            Q3+= self.parseOOxmlarea(ooWb, "Q3_ScheduleCorrelation", sheetnames[3])
        except:
            return self.__parseError(sheetnames[3]), []
            
        try:    
        
            QRenewables = []
            QRenewables.append(self.parseOOxmlarea(ooWb, "Q7_Interest", sheetnames[8]))
            QRenewables += self.parseOOxmlarea(ooWb, "Q7_REReason", sheetnames[8])
            QRenewables.append(self.parseOOxmlarea(ooWb, "Q7_Others", sheetnames[8]))
            QRenewables += self.parseOOxmlarea(ooWb, "Q7_Latitude", sheetnames[8])
            QRenewables += self.parseOOxmlarea(ooWb, "Q7_Biomass", sheetnames[8])
        
            QSurf = self.parseOOxmlarea(ooWb, "Q7_Area", sheetnames[8])
            QSurf += self.parseOOxmlarea(ooWb, "Q7_Roof", sheetnames[8])
        except:
            return self.__parseError(sheetnames[8]), []
        dlg.update(84)
        try:    
            sheetname = "Q3A"
            QProfiles = []
            QProcNames = self.parseOOxmlarea(ooWb, "Q3A_ProcessName", sheetnames[3])
            for i in xrange(3):
                QProfil = self.parseOOxmlarea(ooWb, "Q3A_Profiles_"+ str(i+1), sheetnames[3])
                QProfil.append(QProcNames[i*3])       
                QProfiles.append(QProfil)
    
            QIntervals  = self.parseOOxmlarea(ooWb, "Q3A_StartTime_1", sheetnames[3])
            QIntervals += self.parseOOxmlarea(ooWb, "Q3A_StartTime_2", sheetnames[3])
            QIntervals += self.parseOOxmlarea(ooWb, "Q3A_StartTime_3", sheetnames[3])
            QIntervals += self.parseOOxmlarea(ooWb, "Q3A_EndTime_1", sheetnames[3])
            QIntervals += self.parseOOxmlarea(ooWb, "Q3A_EndTime_2", sheetnames[3])
            QIntervals += self.parseOOxmlarea(ooWb, "Q3A_EndTime_3", sheetnames[3])
        except:
            return self.__parseError(sheetnames[3]), []
        dlg.update(92)
        try:
        
            Q9Questionnaire=[]
            for i in xrange(3):
                Q9Questionnaire+=self.parseOOxmlarea(ooWb, "Q9_"+str(i+1), sheetnames[10])

        except:
            return self.__parseError(sheetnames[10]), []
         
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
                    Q4_8.append(self.parseOOxmlarea(ooWb, startStructure[j]+str(i+1), structureNames[j]))
                except:
                    return structureNames[j] + " " + startStructure[j]+str(i+1),[]
                    
        
        try:
            latitude = self.parseOOxmlarea(ooWb, "Q7_Latitude", sheetnames[8])
        except:
            return self.parseError(sheetnames[8])
        
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
        appendData = []
        sumRepeatedCells=0
        # If only one cell is selected
        if len(cellrange)<4:
            sumRepeatedCells = 0
            tablecells = tablerows[int(cellrange[1])-1].childNodes
            for j in xrange(1,ord(str(cellrange[0]).upper())-64+1):
                if tablecells[j-1].hasAttribute("table:number-columns-repeated"):
                    repeatedCells= int(tablecells[j-1].getAttribute("table:number-columns-repeated"))
                    sumRepeatedCells += (repeatedCells-1)
                
            tabledata =  tablerows[int(cellrange[1])-1].childNodes[ord(cellrange[0])-64-1-sumRepeatedCells]
            while tabledata.hasChildNodes():
                tabledata = tabledata.firstChild
            try:    
                return tabledata.data
            except:
                return None
            
        repeatedcells = 0
        # Cell rows
        for i in xrange(int(cellrange[1]), int(cellrange[3])+1):
            tablecells = tablerows[i-1].childNodes

            sumRepeatedCells=0
            # Cell columns
            
            for j in xrange(1,ord(str(cellrange[2]).upper())-64+1):
                try:
                    tablecell = tablecells[j-1]
                    if(ord(str(cellrange[2]).upper())-64 +0<j+sumRepeatedCells):
                        continue
                    
                    if tablecell.hasAttribute("table:number-columns-repeated"):
                        repeatedCells= int(tablecell.getAttribute("table:number-columns-repeated"))
                        if repeatedCells > 50:
                            continue
                        sumRepeatedCells=sumRepeatedCells+(repeatedCells-1)
                        if j+sumRepeatedCells >= ord(str(cellrange[0]).upper())-64:
                            if ord(str(cellrange[2]).upper()) - ord(str(cellrange[0]).upper()) >0:
                                for k in xrange(repeatedCells):
                                    data.append(None)
                            else:
                                data.append(None)
                        continue
                        
                    if j+sumRepeatedCells >= ord(str(cellrange[0]).upper())-64:
                        tabletext = tablecell.getElementsByTagName("text:p")
                        if(len(tabletext)<1):
                            data.append(None)
                        elif len(tabletext) == 1:
                            
                            for elem in tabletext:
                                while elem.hasChildNodes():
                                    elem = elem.firstChild
                                try:
                                    if tablecell.hasAttribute("office:value-type"):
                                        celltype = tablecell.getAttribute("office:value-type")
                                        if celltype == "float":
                                            cell = tablecell.getAttribute("office:value")
                                            data.append(cell)
                                            #data.append(str(elem.data).replace('.', ''))
                                            continue
                                    data.append(elem.data)
                                except:
                                    data.append(None)
                        else:
                            for elem in tabletext:
                                while elem.hasChildNodes():
                                    elem = elem.firstChild
                                try:
                                    appendData.append(elem.data)
                                except:
                                    pass
                            dataelem = ""
                            for elem1 in appendData:
                                dataelem +=str(elem1)+"\n"
                            try:
                                data.append(SD._U(dataelem))
                            except:
                                data.append(None)
                except:
                    pass
            
            


           

        return data
        
        
    
    def __connectToDB(self):
        conn = MySQLdb.connect("localhost", self.__username, self.__password, db="einstein")
        md = pSQL.pSQL(conn, "einstein")
        return md