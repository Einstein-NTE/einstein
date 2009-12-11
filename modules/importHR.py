#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#    XMLImportHRModule
#           
#------------------------------------------------------------------------------
#
#    Module to load XML from the external PE tool
#    Part of the HRModule
#           
#==============================================================================
#
#   Version No.: 0.01
#   Created by:         Florian Joebstl  01/09/2008
#   Last revised by:
#                       Florian Joebstl  01/09/2008                       
#
#   Changes to previous version:
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

import xml.dom
import xml.dom.minidom
import MySQLdb
import string
from einstein.modules.messageLogger import *

import sys

class DataBaseClass:   
    IsValid = False 
    __values = []
    nodes = []
    
    def __init__(self,entry):
        try:            
            self.__values = []
            self.__parse(entry)
            self.IsValid = True
        except:
            self.IsValid = False
    
    def __parse(self,entry):
        for nodename in self.nodes:
            foundnodes = entry.getElementsByTagName(nodename)
            index = self.nodes.index(nodename)
            value = foundnodes[0].childNodes[0].nodeValue  
            self.__values.insert(index, value)
    
    def setValues(self,values):                
        if (len(values)!=len(self.nodes)):
            self.IsValid = False
            return
        self.__values = values
        self.IsValid = True
    
    def getValue(self,name):
        try:
            index = self.nodes.index(name)
            return self.__values[index]
        except:
            return null
    
    def printData(self): #debug
        print "DATA----------------------"
        if (self.IsValid == False):
            print "data not valid"
            return
        for name in self.nodes:
            index = self.nodes.index(name)
            value = self.__values[index]
            print " "+name+" "+str(value)


class HexData(DataBaseClass):
    nodes  = ['HXNo','HxName','HXType','QdotHX','HXLMTD','QHX','HXSource','HXTSourceInlet','HXTSourceOutlet','HXhSourceInlet','HXhSourceOutlet',
              'HXSink','HXTSinkInlet','HXTSinkOutlet','HXSource_FluidID','HXSink_FluidID','storage_size','HEX_area','HEX_turnkeyprice',
              'HX_OandMfix','HX_OandMvar','HperYear','StreamStatusSource','StreamStatusSink','StreamTypeSink','StreamTypeSource']
    
    def __getValuesInDBOrder(self):           
        values = []
        values.append(self.getValue("HXNo"))
        values.append(self.getValue("HxName"))     #HXname 
        values.append(self.getValue("HXType"))
        values.append(self.getValue("QdotHX"))
        values.append(self.getValue("HXLMTD"))
        values.append("NULL")                       #UA
        values.append(self.getValue("HEX_area"))
        values.append(self.getValue("QHX"))
        values.append("NULL")                       #HPerYearHX
        values.append(self.getValue("HXSource"))
        values.append(self.getValue("HXSource_FluidID"))                #FluidIDSource
        values.append("NULL")                       #FlowSource
        values.append(self.getValue("HXTSourceInlet"))
        values.append(self.getValue("HXhSourceInlet"))
        values.append(self.getValue("HXTSourceOutlet"))
        values.append(self.getValue("HXhSourceOutlet"))
        values.append(self.getValue("HXSink"))
        values.append(self.getValue("HXSink_FluidID"))
        values.append("NULL")                       #FlowSink
        values.append(self.getValue("HXTSinkInlet"))
        values.append(self.getValue("HXTSinkOutlet"))
        values.append(self.getValue("HEX_turnkeyprice")) 
        values.append(self.getValue("HX_OandMfix")) 
        values.append(self.getValue("HX_OandMvar")) 
        values.append(self.getValue("storage_size"))
        values.append(self.getValue("StreamStatusSource")) 
        values.append(self.getValue("StreamStatusSink")) 
        values.append(self.getValue("StreamTypeSink"))
        values.append(self.getValue("StreamTypeSource"))                        #StreamTypeSource
        return values
    
    def getInsertSQL(self,pid,ano):                
        str_values = "(NULL,'%s','%s'" % (pid,ano)
        values = self.__getValuesInDBOrder()
        for value in values:
            if (value == "NULL"):
                str_values = str_values + "," + value
            else:
                str_values = str_values + ",'" + value + "'"
        
        sqlQuery = "INSERT INTO qheatexchanger VALUES" + str_values + ");"
        return sqlQuery
    
class StreamData(DataBaseClass):
    nodes = ['OperatingHours','HeatLoad','StartTemp','EndTemp','HotColdType','HeatType']   
   
    
class CurveData:
    Name = "None"
    IsValid = False
    __points = []
    
    def __init__(self,name,curveentry):
        try:
            self.Name = name
            self.__points = []
            self.__parse(curveentry)
            self.IsValid = True                                                
        except:
            self.IsValid = False
    
    def __parse(self,curveentry):
        foundnodes = curveentry.getElementsByTagName('PairOfDouble')
        for node in foundnodes:            
            self.__parsePairOfDouble(node)
            
    def __parsePairOfDouble(self,node):
        n1 = node.getElementsByTagName('getSetFirst')[0]
        n2 = node.getElementsByTagName('getSetSecond')[0]
        value1 = float(n1.childNodes[0].nodeValue)
        value2 = float(n2.childNodes[0].nodeValue)
        self.__points.append((value1,value2))
        
    def printData(self):#debug
        print " "+self.Name + "   points:"+str(len(self.__points))
        print self.__points
        
    def getPoints(self):
        return __points
    
    def getXValues(self):
        X = []
        for p in self.__points:
            X.append(p[0])
        return X
    
    def getYValues(self):
        Y = []
        for p in self.__points:
            Y.append(p[1])
        return Y


class XMLDocHRModuleImport:
    hexdatabase = []
    curvedatabase = []
    streamdatabase = []
    
    def __init__(self, doc):
        self.hexdatabase = []
        self.curvedatabase = []
        self.streamdatabase = []
        self.__HandleHexes(doc)
        self.__HandleCurves(doc)
        self.__HandleStreams(doc)
    
    def __HandleHexes(self,doc):
        hexes = doc.getElementsByTagName('ExportXMLDataForEachHexDatabaseSpecific')
        for hex in hexes:
            hexdata = HexData(hex)            
            if (hexdata.IsValid):
                self.hexdatabase.append(hexdata)
            else:
                logDebug("Invalid HX data.")
                
    def __HandleCurves(self,doc):
        coldcurve  = doc.getElementsByTagName('ColdCompositeCurveValues')[0]
        hotcurve   = doc.getElementsByTagName('HotCompositeCurveValues')[0]
        grandcurve = doc.getElementsByTagName('GrandCompositeCurveValues')[0]
        
        curves = [CurveData("CCC",coldcurve),CurveData("HCC",hotcurve),CurveData("GCC",grandcurve)] 
        
        for curve in curves:
            if (curve.IsValid):
                self.curvedatabase.append(curve)
            else:
                logDebug("Invalid curve data ("+curve.Name+")")
        
    def __HandleStreams(self,doc):
        streams = doc.getElementsByTagName('ExportStreamInformation')
        for stream in streams:
            streamdata = StreamData(stream)            
            if (streamdata.IsValid):
                self.streamdatabase.append(streamdata)
            else:
                logDebug("Invalid stream data.")
            
    def debug(self): #debug            
        for hexdata in self.hexdatabase:
            hexdata.printData()
        print "Curves-----------------------" 
        for curve in self.curvedatabase:
            curve.printData()
        print "Streams-----------------------" 
        for stream in self.streamdatabase:
            stream.printData()
    

class XMLImportHRModule:
    def importXML(path):
        logDebug("Importing data from "+str(path))
        try:
            dom = xml.dom.minidom.parse(path)
            document = XMLDocHRModuleImport(dom);            
            #document.debug()
            dom.unlink()
            return document
        except:
            logError(_("Importing failed."))
            return None

    importXML = staticmethod(importXML)

#XMLImportHRModule.importXML("export.xml")
