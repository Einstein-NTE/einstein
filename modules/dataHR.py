from einstein.GUI.status import *

#--------------------------------------------------------------------------------------------
#
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
    
    def loadFromDocument(self,doc):
        self.__storeNewHX(doc)
        self.__loadStreams(doc.streamdatabase)
        self.__loadCurves(doc.curvedatabase)
        self.__loadHEX()
    
    def __loadHEX(self):  
        try:      
            sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s'"%(self.pid,self.ano)
            self.hexers = Status.DB.qheatexchanger.sql_select(sqlQuery)
        except:
            self.hexers = []
    
                   
    def __storeNewHX(self,doc):                
        try:
            delquery = "DELETE FROM qheatexchanger  WHERE ProjectID=%s AND AlternativeProposalNo=%s" % (Status.PId,Status.ANo)
            Status.DB.sql_query(delquery)
            for hx in doc.hexdatabase:                
                query = hx.getInsertSQL(Status.PId,Status.ANo)
                Status.DB.sql_query(query)
        except:        
            print "error writing new HX"
    
    def __loadStreams(self,listofstreamdata):
        self.streams = []
        for streamdata in listofstreamdata:
            if (streamdata.IsValid):
                newstream = Stream()
                newstream.loadFromData(streamdata)
                self.streams.append(newstream)
    
    def __loadCurves(self,listofcurvedata):
        self.curves = []
        for curvedata in listofcurvedata:
            if (curvedata.IsValid):
                newcurve = Curve()
                newcurve.loadFromData(curvedata)
                self.curves.append(newcurve)
    
    def deleteHex(self,index):             
         try:
             hx = self.hexers[index]
             print "deleting hx "+ str(hx["QHeatExchanger_ID"])
             sqlQuery = "DELETE FROM qheatexchanger  WHERE ProjectID=%s AND AlternativeProposalNo=%s AND QHeatExchanger_ID=%s" % (self.pid,self.ano,hx["QHeatExchanger_ID"])
             Status.DB.sql_query(sqlQuery)
             self.__loadHEX()
         except w:
             print "deleting of hex failed."+w
    
    def deleteHexAndGenStreams(self,index):
        try:
            if (index < 0)or(index >= len(self.hexers)):
                return
            hx = self.hexers[index]
            print "generating new hot and cold stream from HEX"
            hot = Stream()
            hot.generateHotStreamFromHEX(hx)
            cold = Stream()
            cold.generateColdStreamFromHEX(hx)
            
            self.streams.append(hot)
            self.streams.append(cold)                                
            
            self.deleteHex(index)            
        except:
            print "generating new streams failed."
            
#--------------------------------------------------------------------------------------------
#
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
        
#--------------------------------------------------------------------------------------------
#
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
        
               