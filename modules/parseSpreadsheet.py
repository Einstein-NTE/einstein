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

class parseSpreadsheet():
    def __init__(self,path):
        self.path=path
        
    def parse(self):
        pass

    @staticmethod
    def parseError(errorname):
        return "Parsing failed because of: " + str(errorname)+ "! Please check your data and try again."
        

                
    def __writeToDB(self,Q1, Q2, QProduct, QFuel, Q3, QRenewables, QSurf, QProfiles, QIntervals, Q9Questionnaire):
        
        try:
            q2dict = SD.createQElectricityDictionary(Q2, self.__md)
            self.__md.qelectricity.insert(q2dict)
        except:
            return parseSpreadsheet.parseError(self.__sheetnames[1])

        try:
            for i in xrange(3):
                self.__md.profiles.insert(SD.createProfilesDictionary(QProfiles[i], self.__md))
    
            for i in xrange(len(QIntervals)/2):
                self.__md.intervals.insert(SD.createIntervalDictionary([QIntervals[i],QIntervals[len(QIntervals)/2+i]], self.__md))
        except:
            return parseSpreadsheet.parseError(self.__sheetnames[3])
        
        try:
            Q1dict = SD.createQuestionnaireDictionary(Q1, self.__md)
            Q9dict = SD.createQ9dictionary(Q9Questionnaire, self.__md)
            NaceDict = SD.createNACEDictionary(Q1, self.__md)
            strNace = "CodeNACE = '"+str(Q1[20])+"' AND CodeNACESub ='"+str(int(Q1[24]))+"'"
            dbnacecodeid = self.__md.dbnacecode.sql_select(strNace)
            
            Q1dict.update(Q9dict)
            Q1dict.update({'DBNaceCode_id':dbnacecodeid[0]['DBNaceCode_ID']})
            self.__md.questionnaire.insert(Q1dict)
        except:
            return parseSpreadsheet.parseError(self.__sheetnames[0])
        
        try:
            Questionnaire_ID = self.__md.questionnaire.sql_select("LAST_INSERT_ID()")
            Questionnaire_ID =  Questionnaire_ID[-1]['Questionnaire_ID']
        except: 
            return parseSpreadsheet.parseError("No Questionnare ID Found")
        quest_id = 'Questionnaire_id'
        Areas = ["Q4H_", "Q4C_", "Q5_", "Q6_", "Q8_"]

        for i in xrange(5):
            try:
                Q4Hdict = SD.createQ4HDictionary(self.__tupleToList(self.__xlWb.Worksheets(self.__sheetnames[4]).Range("Q4H_"+str(i+1))),self.__md)
                Q4Hdict[quest_id]=Questionnaire_ID
                self.__md.qgenerationhc.insert(Q4Hdict)
            except:
                return parseSpreadsheet.parseError(self.__sheetnames[4])
                
            try:    
                Q4Cdict = SD.createQ4CDictionary(self.__tupleToList(self.__xlWb.Worksheets(self.__sheetnames[5]).Range("Q4C_"+str(i+1))), self.__md)
                Q4Cdict[quest_id]=Questionnaire_ID
                self.__md.qgenerationhc.insert(Q4Cdict)
            except:
                return parseSpreadsheet.parseError(self.__sheetnames[5])
            
            try:
                self.__md.qdistributionhc.insert(SD.createQ5Dictionary(self.__tupleToList(self.__xlWb.Worksheets(self.__sheetnames[6]).Range("Q5_"+str(i+1))), self.__md))
            except:
                return parseSpreadsheet.parseError(self.__sheetnames[6])
            
            try:
                Q6 = self.__tupleToList(self.__xlWb.Worksheets(self.__sheetnames[7]).Range("Q6_"+str(i+1)))
                self.__md.qheatexchanger.insert(SD.createQ6Dictionary(Q6, self.__md))
                self.__md.qwasteheatelequip.insert(SD.createQ6EDictionary(Q6, self.__md))
            except:
                return parseSpreadsheet.parseError(self.__sheetnames[7])
                
            try:
                Q8dict = SD.createQ8Dictionary(self.__tupleToList(self.__xlWb.Worksheets(self.__sheetnames[9]).Range("Q8_"+str(i+1))), self.__md)
                Q8dict[quest_id]=Questionnaire_ID
                self.__md.qbuildings.insert(Q8dict)
            except:
                return parseSpreadsheet.parseError(self.__sheetnames[9])
                
        try:
            QRenewables = SD.createQ7Dictionary(QRenewables, self.__md)
            QRenewables[quest_id] = Questionnaire_ID
            self.__md.qrenewables.insert(QRenewables)
        except:
            return parseSpreadsheet.parseError(self.__sheetnames[8])
        
        try:
            self.__splitExcelColumns(3, 5, QProduct, {}, Questionnaire_ID ,SD.createQProductDictionary,self.__md.qproduct)
            self.__splitExcelColumns(6, 6, QFuel, {}, Questionnaire_ID ,SD.createQFuelDictionary,self.__md.qfuel)
            latitude = self.__xlWb.Worksheets(self.__sheetnames[8]).Range("Q7_Latitude")
            self.__splitExcelColumns(4, 4, QSurf, {'ST_IT':latitude[1]}, "", SD.createQSurfDictionary, self.__md.qsurfarea)
            
            # Code to skip a specific amount of columns
            index =0
            Q3n = []
            for i in range(0,len(Q3),3):
                Q3n.append(Q3[i]) 
                index+=1
                
            self.__splitExcelColumns(3, 3, Q3n, {}, Questionnaire_ID, SD.createQProcessDictionary,self.__md.qprocessdata)
        except:
            return parseSpreadsheet.parseError("QProduct, QFuel or QSurfarea")

        
        return "Parsing successful!"
