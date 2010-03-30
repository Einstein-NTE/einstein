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
        self.__sheets = ["Q1 GeneralData",
                  "Q2 EnergyConsumption",
                  "Q3_ Processes",
                  "Q3A",
                  "Q4H_HeatGeneration",
                  "Q4C_ColdGeneration",
                  "Q5_Distribution",
                  "Q6_HeatRecovery",
                  "Q7_ Renewables",
                  "Q8 Buildings",
                  "Q9 Economics"]
        sht=[]
        for i in xrange(0,len(self.__sheets)):
            try:
                sht.append(self.__xlWb.Worksheets(self.__sheets[i]))
            except:
                return 'Failed to import ' + self.__filepath + ' at table: ' + self.__sheets[i] + "!"
        
        try:
            self.__Q1GD=self.__tupleToSimpleList(sht[0].Range("GenInfo"))
            self.__Q1GD+=self.__tupleToSimpleList(sht[0].Range("StatData"))
            self.__Q1GD+=self.__tupleToSimpleList(sht[0].Range("operations"))
            self.__Q1GD+=self.__tupleToSimpleList(sht[0].Range("products"))
            self.__md.questionnaire.insert(SD.createQ1Dictionary(self, self.__Q1GD))
            #return 'Import completed!'
        except:
            return 'Failed to parse ' + self.__filepath + ' at table: ' + self.__sheets[0] + "!"
        

                                            
            
        """ 
        try:
            sht = self.__xlWb.Worksheets(sheets[1])
            
        except:
            return 'Failed to import ' + self.__filepath + ' at table: ' + sheets[1] + "!"

        try:
            sht = self.__xlWb.Worksheets(sheets[2])
        except:
            return 'Failed to import ' + self.__filepath + ' at table: ' + sheets[2] + "!"
        
        try:
            sht = self.__xlWb.Worksheets(sheets[3])
        except:
            return 'Failed to import ' + self.__filepath + ' at table: ' + sheets[3] + "!"
        
        try:
            sht = self.__xlWb.Worksheets(sheets[4])
        except:
            return 'Failed to import ' + self.__filepath + ' at table: ' + sheets[4] + "!"
        """
        
        return 'Import completed!'
    
    def printQ1(self):
        md = self.__connectToDB() 
        quest = md.questionnaire
        quest = quest.sql_select("")
        for elem in quest:
            print elem
        
        

    
    
    


