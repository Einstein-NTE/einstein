#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#    HRData
#           
#------------------------------------------------------------------------------
#
#    Part of the HRModule. Provides classes to store/load needed data
#           
#==============================================================================
#
#   Version No.: 0.03
#   Created by:         Florian Joebstl  02/09/2008
#   Last revised by:
#                       Florian Joebstl  25/09/2008
#                       Hans Schweiger   06/07/2009
#
#   Changes to previous version:
#       25/09/08   FJ   getStreamsFromHiddenHX added
#       06/07/09   HS   change of __storeNewHX, so that UTF names are supported
#
#
#   
#------------------------------------------------------------------------------     
#   (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008,2009
#   www.energyxperts.net / info@energyxperts.net
#
#   This program is free software: you can redistribute it or modify it under
#   the terms of the GNU general public license as published by the Free
#   Software Foundation (www.gnu.org).
#
#============================================================================== 


from einstein.GUI.status import *
from einstein.GUI.GUITools import check
from einstein.modules.messageLogger import *
#--------------------------------------------------------------------------------------------
# stores all data needed in the HRModule
# default state is loaded from db
# expects a XMLDocHRModuleImport to load data from XML
#--------------------------------------------------------------------------------------------
class HRData:
    pid     = None
    ano     = None
    hexers  = []
    streams = []
    curves  = []   
    
    def __init__(self,pid,ano):        
        self.pid = pid
        self.ano = ano
        print "NEW HR DATA "+str(self.pid)+ " " +str(self.ano)
        hexers  = []
        streams = []
        curves  = []   
        
    def loadDatabaseData(self):
        self.__loadHEX()
    
    def loadCurves(self,doc):
        self.__loadCurves(doc.curvedatabase)
        
    def loadFromDocument(self,doc,overrideHX = False):
    # doc is a XMLDocHRModuleImport Document (importHR.py)
        
        #stores HEXers from document to database
        if (overrideHX):
            self.__storeNewHX(doc.hexdatabase)
        #loads Streams, Curves from document to HRData
        self.__loadStreams(doc.streamdatabase)
        self.__loadCurves(doc.curvedatabase)
        #loads HEXers from database to HRData
        self.__loadHEX()
    
    def __loadHEX(self):  
    #loads HEX from Database
        try:      
            sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s'"%(self.pid,self.ano)
            self.hexers = Status.DB.qheatexchanger.sql_select(sqlQuery)
        except:
            self.hexers = []
    
                   
    def __storeNewHX(self,listofhexdata):   
    #stores HEXers found in XML document
    #deletes old HEX             
#        try:
        delquery = "DELETE FROM qheatexchanger  WHERE ProjectID=%s AND AlternativeProposalNo=%s" % (self.pid,self.ano)
        Status.DB.sql_query(delquery)

        qhxTable = Status.DB.qheatexchanger
        for hx in listofhexdata:                
#                query = hx.getInsertSQL(self.pid,self.ano)
#                Status.DB.sql_query(query)

            tmp = {"ProjectID":self.pid,
                   "AlternativeProposalNo":self.ano,
                   "HXNo":check(hx.getValue("HXNo")),
                   "HXName":check(hx.getValue("HxName")),
                   "HXType":check(hx.getValue("HXType")),
                   "QdotHX":check(hx.getValue("QdotHX")),
                   "HXLMTD":check(hx.getValue("HXLMTD")),
                   "Area":check(hx.getValue("HEX_area")),
                   "QHX":check(hx.getValue("QHX")),
                   "HXSource":check(hx.getValue("HXSource")),
                   "FluidIDSource":check(hx.getValue("HXSource_FluidID")),
                   "HXTSourceInlet":check(hx.getValue("HXTSourceInlet")),
                   "HXhSourceInlet":check(hx.getValue("HXhSourceInlet")),
                   "HXTSourceOutlet":check(hx.getValue("HXTSourceOutlet")),
                   "HXhSourceOutlet":check(hx.getValue("HXhSourceOutlet")),
                   "HXSink":check(hx.getValue("HXSink")),
                   "FluidIDSink":check(hx.getValue("HXSink_FluidID")),
                   "HXTSinkInlet":check(hx.getValue("HXTSinkInlet")),
                   "HXTSinkOutlet":check(hx.getValue("HXTSinkOutlet")),
                   "TurnKeyPrice":check(hx.getValue("HEX_turnkeyprice")),
                   "OMFix":check(hx.getValue("HX_OandMfix")),
                   "OMVar":check(hx.getValue("HX_OandMvar")),
                   "StorageSize":check(hx.getValue("storage_size")),
                   "StreamStatusSource":check(hx.getValue("StreamStatusSource")),
                   "StreamStatusSink":check(hx.getValue("StreamStatusSink")),
                   "StreamTypeSink":check(hx.getValue("StreamTypeSink")),
                   "StreamTypeSource":check(hx.getValue("StreamTypeSource"))}

            try:
                qhxTable.insert(tmp)
            except:            
                logError(_("Error writing new HX into database.")+" [%s]"%tmp[HXName]) 
    
    def __loadStreams(self,listofstreamdata):
    #loads streams from document
        self.streams = []
        for streamdata in listofstreamdata:
            if (streamdata.IsValid):
                newstream = Stream()
                newstream.loadFromData(streamdata)
                self.streams.append(newstream)
    
    def __loadCurves(self,listofcurvedata):
    #loads curves from document
        self.curves = []
        for curvedata in listofcurvedata:
            if (curvedata.IsValid):
                newcurve = Curve()
                newcurve.loadFromData(curvedata)
                self.curves.append(newcurve)
    
    def deleteHex(self,index):   
    #deletes a specific HEX in db and reloads list of hx          
         try:
             hx = self.hexers[index]
             print "deleting hx "+ str(hx["QHeatExchanger_ID"])
             sqlQuery = "DELETE FROM qheatexchanger  WHERE ProjectID=%s AND AlternativeProposalNo=%s AND QHeatExchanger_ID=%s" % (self.pid,self.ano,hx["QHeatExchanger_ID"])
             Status.DB.sql_query(sqlQuery)
             self.__loadHEX()
         except:
             logError(_("Deleting HX from database failed")) 
    
    def deleteHexAndGenStreams(self,index):
    #delets a HEX and add a hot and cold stream into the stream list
    #
    # NOT USED ANYMORE - hx should not be deleted but temporarily hidden
    # see: getStreamsFromHiddenHX(hidden)
    #
        try:
            if (index < 0)or(index >= len(self.hexers)):
                return
            hx = self.hexers[index]
            
            hot = Stream()
            hot.generateHotStreamFromHEX(hx)
            cold = Stream()
            cold.generateColdStreamFromHEX(hx)
            
            self.streams.append(hot)
            self.streams.append(cold)                                
            
            self.deleteHex(index)            
        except:
            logError(_("Generating new streams failed."))
            
    def getStreamsFromHiddenHX(self,indizesOfHiddenHX):
        try:
            streamsFromHiddenHX = [ ]
            for index in indizesOfHiddenHX:
                if not((index < 0)or(index >= len(self.hexers))):
                    hx = self.hexers[index]
                    hot = Stream()
                    hot.generateHotStreamFromHEX(hx)
                    cold = Stream()
                    cold.generateColdStreamFromHEX(hx)
            
                    streamsFromHiddenHX.append(hot)
                    streamsFromHiddenHX.append(cold)   
            return streamsFromHiddenHX
        except:
            logError(_("Generating streams for hidden HX failed"))
            return []
#--------------------------------------------------------------------------------------------
# class representing a Stream
#--------------------------------------------------------------------------------------------
class Stream:
    OperatingHours = None
    HeatLoad       = None
    StartTemp      = None
    EndTemp        = None
    HotColdType    = None
    HeatType       = None
    
    def loadFromData(self,streamdata):
        if (streamdata.IsValid):
            self.OperatingHours = float(streamdata.getValue("OperatingHours"))
            self.HeatLoad       = float(streamdata.getValue("HeatLoad"))
            self.StartTemp      = float(streamdata.getValue("StartTemp"))
            self.EndTemp        = float(streamdata.getValue("EndTemp"))
            self.HotColdType    = str(streamdata.getValue("HotColdType"))
            self.HeatType       = streamdata.getValue("HeatType")                #wrong in db

    def __getOperatingHours(self,hx):    
        ophours     = hx["HPerYearHX"]
        storagesize = hx["StorageSize"]
        QdotHX      = hx["QdotHX"]
        QHX         = hx["QHX"]  
        if ((storagesize == "NULL")or(float(storagesize)==0)):
            ophours = float(QHX)/float(QdotHX)            
        return ophours
        
    def generateColdStreamFromHEX(self,hx):
        try:
            self.OperatingHours = self.__getOperatingHours(hx)
            self.HeatLoad  = float(hx["QdotHX"])
            self.StartTemp = float(hx["HXTSinkInlet"])
            self.EndTemp   = float(hx["HXTSinkOutlet"])
            self.HotColdType = "cold"
            self.HeatType    = hx["StreamTypeSink"]
            return True
        except:
            return False
    
    def generateHotStreamFromHEX(self,hx):
        try:
            self.OperatingHours = self.__getOperatingHours(hx)
            self.HeatLoad  = float(hx["QdotHX"])
            self.StartTemp = float(hx["HXTSourceInlet"])
            self.EndTemp   = float(hx["HXTSourceOutlet"])
            self.HotColdType = "hot"
            self.HeatType    = hx["StreamTypeSource"] 
            return True
        except:
            return False  
        
    def printStream(self):      
        print "Stream: " + str(self.HotColdType) + " / " + str(self.HeatType)
        print "  Load: " + str(self.HeatLoad)
        print "  Temp: " + str(self.StartTemp) + " - " + str(self.EndTemp)
        print " OpHrs: " + str(self.OperatingHours)
            
#--------------------------------------------------------------------------------------------
# class representing a curve
#--------------------------------------------------------------------------------------------
class Curve:
    X = []
    Y = []
    Name = "None"
    
    def loadFromData(self,curvedata):
        if (curvedata.IsValid):        
            self.Name = curvedata.Name
            self.X = curvedata.getXValues()
            self.Y = curvedata.getYValues()
        
               
