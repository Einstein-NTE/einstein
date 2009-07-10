#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#    XMLExportHRModule
#           
#------------------------------------------------------------------------------
#
#    Module to create customized export XML for the HRModule
#           
#==============================================================================
#
#   Version No.: 0.04
#   Created by:         Florian Joebstl  20/08/2008
#   Last revised by:
#                       Florian Joebstl  04/09/2008
#                       Hans Schweiger   06/07/2009
#
#   Changes to previous version:
#   01/09/2008: (FJ) Set all NULL values to 0 like expected by the external tool 
#   04/09/2008: (FJ) Fixed the QOpProc value problem
#   06/07/2009: HS   Export of TCond and LatentHeat in QWHProc data
#   
#------------------------------------------------------------------------------     
#   (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#   www.energyxperts.net / info@energyxperts.net
#
#   This program is free software: you can redistribute it or modify it under
#   the terms of the GNU general public license as published by the Free
#   Software Foundation (www.gnu.org).
#
#============================================================================== 
#  INFORMATION:
#
#  Usage:
#    XMLExportHRModule.export(path,qid,ano,export_exheatex = False)
#    e.g. XMLExportHRModule.export("hr.xml",74,1,False)
# 
#  Contains:
#    class XMLExportHRModule: Interface to use export functionality.
#                             Static class, suggested usage:
#                             XMLExportHRModule.export(path,qid,pid,...)  
#  
#   --------------------------------------------------------------------------    
#
#   class DBConnection: connects to einstein database. should be replaced by 
#                       einstein default db-connection class
#   class SQLViews    : holds all sql statements used 
#
#   class XMLDocHRModuleBase : Defines default behaviour for the xml writer.
#                              This class has no document structure defined and
#                              is only used as base class for concrete xml 
#                              export configurations.
#   class XMLDocHRModuleAll  : Defines the document structure of the HR export 
#                              xml (derives from XMLDocHRModuleBase)
#   class XMLDocHRModuleNoHX : Alters XMLDocHRModuleAll , existing heat ex. 
#                              will not be exported
#
#==============================================================================

import xml.dom
from einstein.modules.messageLogger import *
#Try to import the PYXML library to generate human readable (well formated) xml
#else the default print is used
TRY_PYXML = True
if (TRY_PYXML):
    try:
        import xml.dom.ext
        PyXMLavaliable = True
    except:
        PyXMLavaliable = False

import xml.dom.minidom
import MySQLdb
import string
import wx

from xml.dom.minidom import getDOMImplementation
from einstein.GUI.status import Status


#------------------------------------------------------------------------------               
# DBConnection
#------------------------------------------------------------------------------
class DBConnection:    
    connection = None
    
    def connect(self):
         frame = wx.GetApp().GetTopWindow()
         self.connection = frame.connectToDB()                                   
    
    def close(self):
        self.connection.close()              
    
    def sql(self,statement):    
        #print statement  
        cursor = self.connection.cursor()
        cursor.execute(statement)
        results = cursor.fetchall()   
        cursor.close() 
        return results

#------------------------------------------------------------------------------               
# SQLViews
#------------------------------------------------------------------------------
class SQLViews(object):
    SQL_HeatGeneration = """SELECT q.`Equipment`, d.`FuelName`, q.`HCGPnom`, q.`FuelConsum`, q.`UnitsFuelConsum`, d.`FuelDensity`, 
                            q.`ExcessAirRatio`, q.`TExhaustGas`,q.QExhaustGas, q.FlowExhaustGas, q.`PartLoad`, q.`HPerDayEq`, q.`NDaysEq`, d.`Offgas`, d.`CombAir`, 
                            d.`Humidity`, d.`OffgasHeatCapacity`, d.`OffgasDensity` 
                            FROM qgenerationhc q, dbfuel d
                            WHERE q.`Questionnaire_id`=%s AND q.`AlternativeProposalNo`=%s AND q.`DBFuel_id` = d.`DBFuel_ID` 
                            ORDER BY q.`EqNo`;"""
                            
    SQL_ColdGeneration = """SELECT q.`Equipment`, q.`HCGPnom`, q.`PartLoad`, q.`HPerDayEq`, q.`NDaysEq`, d.`THighP`, d.`TCond`, 
                            d.`SpecificMassFlow`, d.`LatentHeat`, q.`TemperatureReCooling`, q.`ElectriConsum`, q.`ThermalConsum`, 
                            d.`DBFluid_ID`, d.`FluidDensity`, d.`FluidCp`, q. `THeatSourceHT` 
                            FROM qgenerationhc q, dbfluid d
                            WHERE q.`Questionnaire_id`=%s AND q.`AlternativeProposalNo`=%s AND q.`Refrigerant` =d.`FluidName`
                            ORDER BY q.`EqNo`;"""
                                                             
    SQL_ProcessData    = """SELECT q.`Process`, q.`ProcType`, q. HPerDayProc, q. VolProcMed
                            FROM qprocessdata q, dbfluid d
                            WHERE q.`QProcessData_ID`=%s AND q.`Questionnaire_id`=%s AND q.`AlternativeProposalNo`=%s AND q.`ProcMedDBFluid_id`=d.`DBFluid_ID`
                            ORDER BY q.`ProcNo`;""" 
                            
    SQL_ProcessData2   = """SELECT q.`NBatch`, q.`HBatch`, q.`NDaysProc`, q.`QOpProc`, q.`HPerDayProc`, q.`QEvapProc`  
                            FROM qprocessdata q
                            WHERE q.`QProcessData_ID`=%s AND q.`Questionnaire_id`=%s AND q.`AlternativeProposalNo`=%s
                            ORDER BY q.`ProcNo`;"""
                            
    SQL_QProcessMedium1 ="""SELECT d.`FluidName`, q.`PTStartUp`, q.`PTInFlow`, q.`VInFlowDay`, d.`DBFluid_ID`, 
                            d.`FluidDensity`, d.`FluidCp`, q.`HeatRecExist`, q.`PTInFlowRec`, q.`PT`, q.`PTInMax` 
                            FROM qprocessdata q, dbfluid d
                            WHERE q.`QProcessData_ID`=%s AND q.`Questionnaire_id`=%s AND q.`AlternativeProposalNo`=%s AND q.`ProcMedDBFluid_id`=d.`DBFluid_ID`
                            ORDER BY q.`ProcNo`;"""   
                            
    SQL_QWHProcessMed1=  """SELECT d.`FluidName`, q.`PTOutFlow`, q.`HOutFlow`, q.`PTFinal`, 
                            q.`VOutFlow`, q.`HeatRecOK`, d.`DBFluid_ID`, d.`FluidDensity`, d.`FluidCp`, d.`TCond`, d.`LatentHeat` 
                            FROM qprocessdata q, dbfluid d
                            WHERE q.`QProcessData_ID`=%s AND q.`Questionnaire_id`=%s AND q.`AlternativeProposalNo`=%s AND q.`ProcMedOut` =d.`DBFluid_ID`
                            ORDER BY q.`ProcNo`;""" 
    
    SQL_InputSupplyMed1= """SELECT d.`FluidName`, q.`TSupply`, q.`SupplyMedFlow`, d.`DBFluid_ID`, d.`FluidDensity`, d.`FluidCp` 
                            FROM qprocessdata q, dbfluid d
                            WHERE q.`QProcessData_ID`=%s AND q.`Questionnaire_id`=%s AND q.`AlternativeProposalNo`=%s AND q.`SupplyMedDBFluid_id`=d.`DBFluid_ID`
                            ORDER BY q.`ProcNo`;"""                   
                            
    SQL_WasteHeatElec   = """SELECT q.`WHEEName`, q.`QWHEE`, q.`WHEEMedium`, q.`WHEEFlow`, q.`WHEETOutlet`, q.`HPerDayWHEE`, q.`NDaysWHEE`,
                            d.`DBFluid_ID`, d.`FluidCp`, d.`FluidDensity` 
                            FROM qwasteheatelequip q, dbfluid d
                            WHERE q.`ProjectID`=%s AND q.`AlternativeProposalNo`=%s AND q.`WHEEMedium`=d.`DBFluid_ID` 
                            ORDER BY q.`WHEENo`;"""
    
    SQL_ExistingHeatEx = """SELECT q.`HXName`, q.`HXType`, q.`QdotHX` , q.`HXSource`, q.`HXTSourceInlet`, q.`HXhSourceInlet`, q.`HXTSourceOutlet`, q.`HXhSourceOutlet`,  
                            q.`HXSink`, q.`HXTSinkInlet`, q.`HXTSinkOutlet`, q.`HXLMTD`, q.`Area`,  q.`QHX`, q.`HPerYearHX`, q.`FluidIDSource`, q.`FlowSource`, 
                            d.`FluidCp` as 'FluidCPSource', d.`FluidDensity` as 'FluidDensitySource', q.`FluidIDSink`, q.`FlowSink`, d1.`FluidCp` as 'FluidCPSink', 
                            d1.`FluidDensity` as 'FluidDensitySink', q.`TurnKeyPrice`, q.`OMFix`, q.`OMVar`, q.`StorageSize`, q.`StreamStatusSource`, q.`StreamStatusSink`,
                            q.StreamTypeSink, q.StreamTypeSource 
                            FROM qheatexchanger q, dbfluid d, dbfluid d1
                            WHERE q.`ProjectID`=%s AND q.`AlternativeProposalNo`=%s AND q.`FluidIDSource`=d.`DBFluid_ID` AND q.`FluidIDSink`=d1.`DBFluid_ID`
                            ORDER BY q.`HXNo`;"""

#------------------------------------------------------------------------------               
# XMLDocHRModuleBase
#
# Defines default behaviour for the xml writer. This class has no document  
# structure defined and is only used as base class for concrete xml 
# export configurations.                           
#------------------------------------------------------------------------------
class XMLDocHRModuleBase:
    qid = 0
    ano = 0
    document = None
    
    documentname = ""
    xsi          = ""
    xsd          = ""
    
    LISTTAG      = 0
    ELEMENTTAG   = 1
    INNERTAGS    = 2
    SQL          = 3
    CHILDS       = 4
    HANDLE       = 5
    
    docStruct = []
    
    def __init__(self, qid, ano):
        self.qid = qid
        self.ano = ano
        
        impl = getDOMImplementation()
        self.document = impl.createDocument(None, self.documentname, None)        
        top = self.document.documentElement        
        #top.setAttributeNS(self.xsi,"xsi:xsd",self.xsd)
        
        for structentry in self.docStruct:                                  
            if (structentry[self.HANDLE]!=None):
               structentry[self.HANDLE](self,top)
            else:            
                entry = self.document.createElement(structentry[self.LISTTAG])        
                self.createEntrys(structentry[self.ELEMENTTAG], 
                                  structentry[self.INNERTAGS] , 
                                  structentry[self.SQL]       ,
                                  entry)                                                   
                top.appendChild(entry) 
            if (structentry[self.CHILDS]!=None):
                 assert "XMLDocumentHRModule: Found childs in "+str(structentry[self.ELEMENTTAG])+"Operation not implemented."                              
    
    
    def createEntrys(self,name,tags,sql,parent):                          
        db = DBConnection();
        db.connect()
        r = db.sql( sql % (self.qid,self.ano) )
        
        #if (sql == SQLViews.SQL_WasteHeatElec):
        #    print (sql % (self.qid,self.ano))
        
        for result in r:
            entry = self.document.createElement(name)
            count = 0
            for value in result:
                innerentry = self.document.createElement(tags[count])
                convertedvalue = self.handleSpecialCases(value,tags[count])                
                if (convertedvalue!=None):
                    innerentryvalue = self.document.createTextNode(convertedvalue) ##XX
                    innerentry.appendChild(innerentryvalue)
                entry.appendChild(innerentry)
                count+=1
            parent.appendChild(entry)            
        db.close()                        
        return None        
    
    
    def writeToFile(self,path):
        if (TRY_PYXML and PyXMLavaliable):
            xml.dom.ext.PrettyPrint(self.document, open(path, "w"))
        else:
            fd = open(path, 'w')
            #fd.write(self.document.toprettyxml("  "))
            fd.write(self.document.toxml())
            fd.close()        
        
    def handleSpecialCases(self,value,tag):
        #1) Convert UnitFuleConsum units
        if (tag=="UnitFuelConsum"):
            if (value==None):
                return "ufc_none"
            if (str(value)=="l_per_hour"):
                return "ufc_l_per_hour"
            if (str(value)=="m_3_per_hour,"):
                return "ufc_m_3_per_hour,"
            if (str(value)=="m_3_per_day"):
                return "m_3_per_day"
                    
        #2) interpret NBatch value as integer
        if (tag=="NBatch"):
            return str(int(value))
        
        #3) special cases for HXType
        if (tag=="HXType"):  
            s=str(value)                  
            if (string.find(s,"plate hx")!=-1):
                return"plate (PHE)"                        
            if (string.find(s,"shell&tube HX")!=-1):
                return "shell and tube (STHE)"                                             
        
        #2) treat null values in DB
        #realValueList = ["SupplyMedFlow","PTInMax","Area","Qhx","HPerYearHx","FlowSource","FlowSink","OmFix","OmVar","StorageSize",
        #                 "StreamStatusSource","StreamStatusSink","TurnKeyPrice","QdotHX","HXTSourceInlet","HXhSourceInlet","HXTSourceOutlet"
        #                 "HXhSourceOutlet","HxLmtd"] ## TODO: fill list
        #if (value==None):
        #    if tag in realValueList:
        #        return "0"
        #    else: return None
        if (value==None):
            return "0"
        
        #3) force bool value strings to true or false         
        if (type(value)==bool):
            if(value):
                return "true"
            else:
                return "false"
            
        #4) convert yes/no to true/false        
        if(type(value)==str):            
            if (value.lower()=="yes"):
                return "true"
            if (value.lower()=="no"):
                return "false"
        
        #5) StreamStatusConversion
        if (tag=="StreamStatusSink")or(tag=="StreamStatusSource"):
            s=str(value)
            if(s=='sst_none'):
                return "0"
            if(s=='sst_liquid'):
                return "1"
            if(s=='sst_gaseous'):
                return "2"
            if(s=='sst_condensation'):
                return "3"
                
        #6) default
        return str(value)
         
#------------------------------------------------------------------------------               
# XMLDocHRModuleAll
#
# Defines the document structure of the HR export xml. Provides handles to
# change the processing of more complex xml elements                          
#------------------------------------------------------------------------------      
class XMLDocHRModuleAll(XMLDocHRModuleBase):
    
    #Overrides the default behavior of XMLDocumentHRModule to model the 
    #nesting needed in ProcessData.    
    def HandleProcessData(self,parent):    
        listentry = self.document.createElement(self.procedata[self.LISTTAG])
        db = DBConnection();
        db.connect()
        pids = db.sql("""SELECT QProcessData_ID FROM `qprocessdata`;""")
        for pid in pids:
            processes = db.sql( self.procedata[self.SQL] % (pid[0],self.qid,self.ano) )
            for process in processes:
                entry = self.document.createElement(self.procedata[self.ELEMENTTAG])              
                count = 0
                for value in process:               
                    innerentry = self.document.createElement((self.procedata[self.INNERTAGS])[count])
                    convertedvalue = self.handleSpecialCases(value,self.procedata[self.INNERTAGS])                    
                    if (convertedvalue!=None):
                        innerentryvalue = self.document.createTextNode(convertedvalue) ##XX
                        innerentry.appendChild(innerentryvalue)
                    entry.appendChild(innerentry)
                    count+=1
                childs = self.procedata[self.CHILDS]
                for child in childs:
                    if (child[self.HANDLE]!=None):
                        child[self.HANDLE](self,entry,pid[0])
                    else:
                        self.createEntrysPD(child[self.ELEMENTTAG],child[self.INNERTAGS],child[self.SQL],entry,pid[0])
                listentry.appendChild(entry)           
        parent.appendChild(listentry)
        db.close()            
        
    def createEntrysPD(self,name,tags,sql,parent,pid):                          
        db = DBConnection();
        db.connect()
        if (sql==None):
             entry = self.document.createElement(name)
             parent.appendChild(entry)  
             return None
         
        r = db.sql( sql % (pid,self.qid,self.ano) )
        for result in r:
            entry = self.document.createElement(name)
            count = 0
            for value in result:
                innerentry = self.document.createElement(tags[count])
                convertedvalue = self.handleSpecialCases(value,tags[count])                
                if (convertedvalue!=None):
                    innerentryvalue = self.document.createTextNode(convertedvalue) ##XX
                    innerentry.appendChild(innerentryvalue)
                entry.appendChild(innerentry)
                count+=1
            parent.appendChild(entry)            
        db.close()                        
        return None        
     
    #Overrides the default behavior of XMLDocumentHRModule to model the 
    #batch data in Process data. 
    #MinStartBatch = 30.0
    #MinStartCont = 30.0   
    def HandleBatchData(self,parent,pid):
        db = DBConnection();
        db.connect()
        sql = self.procdatabatch[self.SQL]
        tags= self.procdatabatch[self.INNERTAGS]   
                             
        r = db.sql( sql % (pid,self.qid,self.ano) )
        valuecount = 0
        
        hbatch = 0        
        for tag in tags:                        
            value = r[0][valuecount]
                    
            override = 0                       
            innerentry = self.document.createElement(tag)
            innerentryvalue = None
            convertedvalue = self.handleSpecialCases(value,tag)
            
            if (tag=="MinStartBatch"):
                override = 1      
                valuecount-=1          
                convertedvalue = str(30.0)
                                          
            if (tag=="MinStartCont"):
                override = 1     
                valuecount-=1             
                convertedvalue = str(30.0)
                
            innerentryvalue = self.document.createTextNode(convertedvalue) 
                
            if (convertedvalue!=None):
                innerentry.appendChild(innerentryvalue)
                
            parent.appendChild(innerentry)
            valuecount+=1                     
        db.close()                        
        return None   

    #Overrides the default behavior of XMLDocumentHRModule to model the 
    #batch data in Process data exceptions for the ExHeatEx data
    def HandleExHeatEx(self,parent):
        entry = self.document.createElement(self.exheatex[self.LISTTAG])        
        self.createEntrysExHeatEx(self.exheatex[self.ELEMENTTAG], 
                                  self.exheatex[self.INNERTAGS] , 
                                  self.exheatex[self.SQL]       ,
                                  entry)                                                   
        parent.appendChild(entry) 
    
            
    def createEntrysExHeatEx(self,name,tags,sql,parent):                            
        db = DBConnection();
        db.connect()
        r = db.sql( sql % (self.qid,self.ano) )
        #print sql % (self.qid,self.ano)
        #print r
        for result in r:
            entry = self.document.createElement(name)
            count = 0
            ignore_entry = 0
            for value in result:
                innerentry = self.document.createElement(tags[count])
                convertedvalue = self.handleSpecialCases(value,tags[count])                
                
                if (string.find(tags[count],"HXType")!=-1):                               
                    if (string.find(convertedvalue,"finned tubes (liquid-air)")!=-1):
                        ignore_entry = 1               
                                           
                if (convertedvalue!=None):
                    innerentryvalue = self.document.createTextNode(convertedvalue) ##XX                  
                    innerentry.appendChild(innerentryvalue)
                entry.appendChild(innerentry)
                count+=1
            if (ignore_entry==0):
                parent.appendChild(entry)            
        db.close()                        

    #Overrides the default behavior of XMLDocumentHRModule to model the 
    #schedule data 
    def HandleSchedules(self,parent):
        entry = self.document.createElement(self.schedules[self.LISTTAG])
        for scheduleList in [Status.schedules.procOpSchedules,
                             Status.schedules.procStartUpSchedules,
                             Status.schedules.procInFlowSchedules,
                             Status.schedules.procOutFlowSchedules,
                             Status.schedules.equipmentSchedules,
                             Status.schedules.WHEESchedules]:
            for schedule in scheduleList:
               self.createProcessEntry(schedule,entry)
        parent.appendChild(entry)  
    
    def createProcessEntry(self,schedule,parent):
        process = self.document.createElement(self.schedules[self.ELEMENTTAG])                
        name = self.document.createElement("Name")
        name.appendChild(self.document.createTextNode(str(schedule.name)))
        type = self.document.createElement("Type")
        type.appendChild(self.document.createTextNode(str(schedule.ScheduleType)))
        holidays = self.document.createElement("Holidays")
        holidays.appendChild(self.document.createTextNode(str(len(schedule.holidays))))
        
        weekly = self.document.createElement("ListOfTimePeriods")  
        for w in schedule.weekly:
            timeperiod = self.document.createElement("TimePeriod")
            start =  self.document.createElement("Start")
            end   =  self.document.createElement("End")
            start.appendChild(self.document.createTextNode(str(w[0])))
            end.appendChild(self.document.createTextNode(str(w[1])))
            timeperiod.appendChild(start)
            timeperiod.appendChild(end)
            weekly.appendChild(timeperiod)
          
        monthly = self.document.createElement("MonthlyVariation")  
        month  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        monthc = 0   
        for m in schedule.monthly:
            i = self.document.createElement(month[monthc])
            i.appendChild(self.document.createTextNode(str(m)))
            monthly.appendChild(i)
            monthc+=1                    
                 
        process.appendChild(name)
        process.appendChild(type)
        process.appendChild(holidays)    
        process.appendChild(weekly)    
        process.appendChild(monthly)           
        parent.appendChild(process)
              
                
    #DOCUMENT STRUCTURE DEFINITION
    #a document item format in docStruct:
    #item = [ LISTNAME , ELEMENTNAME, TAGS, SQL-STATEMENT, CHILDS, PROCESS-HANDLE* ]
    #* Process-Handle is a function pointer to override default behavior
    
    documentname = "InputXMLDataController"
    xsi          = "http://www.w3.org/2001/XMLSchema-instance"
    xsd          = "http://www.w3.org/2001/XMLSchema"
    
    #ListOfHeatGenerationData struture
    heatgentags     = ["EquipmentName","FuelType","HCGPNom","FuelConsum","UnitFuelConsum","FuelDensity",
                       "EcessAirRatio","TExhaustGas","QExhaustGas", "FlowExhaustGas","PartLoad","HPerDayEq","NDaysEq","OffGas","CombAir",
                       "FuelHumidityFactor","FuelOffGasCp","FuelOffGasDensity"]    
    heatgen         =  ["ListOfHeatGenerationData","InputXMLHeatGeneration",heatgentags,SQLViews.SQL_HeatGeneration,None,None]
    
    coldgentags     = ["EquipmentName","HCGPNom","PartLoad","HPerDayEq","NDaysEq","THighP","TCond","SpecificMassFlow",
                       "SensibleHeat","LatentHeat","TemperatureRecooling","ElectricConsumption","ThermalConsumption",
                       "FluidId","FluidDensity","FluidCp","THeatSourceHT"]
    coldgen         = ["ListOfColdGenerationData","InputXMLColdGeneration",coldgentags,SQLViews.SQL_ColdGeneration,None,None]    
    
    #QProcessMedium1 structure
    qprocmed1tags   = ["ProcMed","PTStartUp","PTInFlow","VInFlowDay","FluidId","FluidDensity","FluidCp","HeatRecExists",
                       "PTInFlowRec","PT","PTInMax"]
    qprocmed1       = [None,"QProcessMedium1",qprocmed1tags,SQLViews.SQL_QProcessMedium1,None,None]
    
    #QProcessMedium1 structure
    qprocmed2       = [None,"QProcessMedium2",None,None,None,None]
    
    #QWasteHeatProcessMedium1 structure
    qwhprocmed1tags = ["ProcMedOut","PTOutFlow","HOutFlow","PTFinal","VOutFlow","HeatRecOK","FluidId","FluidDensity",
                       "FluidCp","TCond","LatentHeat"]
    qwhprocmed1     = [None,"QWasteHeatProcessMedium1",qwhprocmed1tags,SQLViews.SQL_QWHProcessMed1,None,None]
    
    #InputSupplyMedium1 structure    
    insupplymedtags = ["SupplyMed","TSupply","SupplyMedFlow","FluidId","FluidDensity","FluidCp"]
    insupplymed     = [None,"InputSupplyMedium1",insupplymedtags,SQLViews.SQL_InputSupplyMed1,None,None]      
    
    #InputXMLQProcessDataBatch structure                              
    procdatabatchtags = ["NBatch","HBatch","NDaysProc","MinStartBatch","MinStartCont","QOpProc","HPerDayProc","QEvapProc"]
    procdatabatch     = [None,None,procdatabatchtags,SQLViews.SQL_ProcessData2, None, HandleBatchData]       
    
    #InputXMLQProcessData structure    
    procdatatags    = ["Process","ProcType","HPerDayProc","VolProcMed"]
    procedata       = ["ListOfQProcessData", "InputXMLQProcessData", procdatatags, SQLViews.SQL_ProcessData ,[qprocmed1,qwhprocmed1,insupplymed,qprocmed2,procdatabatch], HandleProcessData]
    
    #ListOfWasteHeatElectrical structure    
    wasteheattags   = ["WHEEName","QWHEE","WHEEMedium","WHEEFlow","WHEETOutlet","HPerDayWHEE","NDaysWHEE","FluidId","FluidCp","FluidDensity"]
    wasteheat       = ["ListOfWasteHeatElectrical","InputXMLWasteHeatElectrical",wasteheattags,SQLViews.SQL_WasteHeatElec,None,None]
    
        
    #ListOfExistingHeatExchangers structure 
    exheatextags    = ["HXName","HXType","QdotHX","HXSource","HXTSourceInlet","HXhSourceInlet","HXTSourceOutlet","HXhSourceOutlet","HXSink","HXTSinkInlet",
                       "HXTSinkOutlet","HxLmtd","Area","Qhx","HPerYearHx","FluidIdSource","FlowSource","FluidCpSource","FluidDensitySource","FluidIdSink",
                       "FlowSink","FluidCpSink","FluidDensitySink","TurnKeyPrice","OmFix","OmVar","StorageSize","StreamStatusSource","StreamStatusSink",
                       "StreamTypeSink","StreamTypeSource"]
    exheatex        = ["ListOfExistingHeatExchangers","InputXMLExistingHeatExchanger",exheatextags,SQLViews.SQL_ExistingHeatEx,None,HandleExHeatEx]
        
    schedules       = ["Schedule","Process",[],None,None,HandleSchedules]
                                  
    #MAIN DOCUMENT STRUCTURE                                  
    docStruct    = [heatgen,coldgen,procedata,wasteheat,exheatex,schedules]     

#------------------------------------------------------------------------------               
# XMLDocHRModuleNoHX
#
# Alters XMLDocHRModuleAll , existing heat ex. will not be exported                                                   
#------------------------------------------------------------------------------  
class XMLDocHRModuleNoHX(XMLDocHRModuleAll):   
    docStruct    = [XMLDocHRModuleAll.heatgen,
                    XMLDocHRModuleAll.coldgen,
                    XMLDocHRModuleAll.procedata,
                    XMLDocHRModuleAll.wasteheat,
                    XMLDocHRModuleAll.schedules]          

#------------------------------------------------------------------------------               
# XMLExportHRModule
#
# Interface to use export functionality. 
# Static class, suggested usage:  XMLExportHRModule.export(...)                                                  
#------------------------------------------------------------------------------ 
class XMLExportHRModule:
    def export(path,qid,ano,export_exheatex = False):
        print "Exporting data to "+str(path) + "  UseExistingHX:"+str(export_exheatex)
                
        if (export_exheatex):
            doc = XMLDocHRModuleAll(qid,ano)
            print len(doc.docStruct)
        else:
            doc = XMLDocHRModuleNoHX(qid,ano)
        doc.writeToFile(path)

    export = staticmethod(export)

#XMLExportHRModule.export("hr.xml",74,1,False)
    
