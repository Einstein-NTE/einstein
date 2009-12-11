# -*- coding: cp1252 -*-
#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#   ModulePO (Process Optimisation)
#           
#------------------------------------------------------------------------------
#           
#   
#
#==============================================================================
#
#   Version No.: 0.01
#   Created by:         Florian Joebstl 24/09/2008  
#
#
#
#
#   
#------------------------------------------------------------------------------

from einstein.GUI.status import *
from einstein.modules.messageLogger import *


class ModulePO(object):

    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel
        self.sectors = [ ]
        self.sectorSelection = None  
        self.subsectors = [] 
        self.subsectorSelection = None
        self.unitoperations = []
        self.unitoperationSelection = None
        self.typicalprocess = []
        self.typicalprocessSelection = None
        self.techs = []
        self.techSelection = []
        self.measures = []                
                       
    def initPanel(self):         
        self.updatePanel()
              
    def updatePanel(self):
        self.getSectors()    
        
        if (self.sectorSelection!=None):
            self.getSubsectors(self.sectorSelection)  
        else:
            self.subsectors = [ ]
             
        if (self.subsectorSelection!=None):
            self.getUnitoperation(self.subsectorSelection)
        else:
            self.unitoperations = [ ]
               
        if (self.unitoperationSelection!=None):
            self.getTypicalProcess(self.subsectorSelection,self.unitoperationSelection)
        else:
            self.typicalprocess = [ ] 
        
        if (self.typicalprocessSelection!=None):
            self.getTechnologies(self.subsectorSelection,self.unitoperationSelection,self.typicalprocessSelection)
        else: 
            self.techs = [ ]
        
        if (self.typicalprocessSelection!=None):
            self.getMeasures(self.subsectorSelection,self.unitoperationSelection,self.typicalprocessSelection)
        else:
            self.measures = []
    
          
    def runPOModule(self):
       pass 
   
    def getSectors(self):
        query = """SELECT IDSector,Name FROM posector"""
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.sectors = results 
        else:
            self.sectors = []
            
    def getSubsectors(self,index):
        query = """SELECT IDSubsector,Name FROM posubsector WHERE SectorID = %s"""
        sector = self.sectors[index]
        query = query % sector[0] 
        
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.subsectors = results 
        else:
            self.subsectors = [] 
            
    def getUnitoperation(self,ssindex):
        query = """SELECT IDUnitOperation, Name FROM pounitoperation as unit, poemlist as list 
                   WHERE unit.IDUnitOperation = list.UnitOperationID AND list.SubsectorID = %s
                   GROUP BY IDUnitOperation"""
        subsector = self.subsectors[ssindex]
        query = query % subsector[0]                 
        results = Status.DB.sql_query(query)  
        
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.unitoperations = results 
        else:
            self.unitoperations = []
    
    def getTypicalProcess(self,ssindex,uoindex):
        query = """SELECT IDTypicalProcess,Name FROM poemlist as list, potypicalprocess as p 
                   WHERE list.TypicalProcessID = p.IDTypicalProcess 
                   AND UnitOperationID = %s AND SubsectorID = %s
                   GROUP BY IDTypicalProcess"""
        uo = self.unitoperations[uoindex]
        subsector = self.subsectors[ssindex]
        query = query % (uo[0],subsector[0])        
        
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.typicalprocess = results 
        else:
            self.typicalprocess = []
                 
    def getTechnologies(self,ssindex,uoindex,tpindex):
        query = """SELECT tech.IDTechnology, tp.Name, tech.Name FROM poemlist as list, potypicalprocess as tp, potech as tech 
                   WHERE tp.IDTypicalProcess = list.TypicalProcessID AND tech.IDtechnology = list.TechnologyID 
                         AND list.TypicalProcessID = %s AND list.UnitOperationID=%s AND list.SubsectorID = %s"""
        tp   = self.typicalprocess[tpindex]
        subsector = self.subsectors[ssindex]
        uo = self.unitoperations[uoindex]
        query = query % (tp[0],uo[0],subsector[0]) 
        
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.techs = results 
        else:
            self.techs = []
    
    def getMeasures(self,ssindex,uoindex,tpindex):
        allresults = [ ]   
        for techindex in self.techSelection:
            query = """SELECT em.ShortDescription, em.Text FROM poefficiencymeasure as em, poemlistentry as entry, poemlist as list
                       WHERE  entry.EfficiencyMeasureID = em.IDEfficiencyMeasure
                       AND    entry.EMListID = list.IDEMList
                       AND    list.SubsectorID = %s
                       AND    list.UnitOperationID = %s
                       AND    list.TypicalProcessID = %s
                       AND    list.TechnologyID = %s"""
            subsector = self.subsectors[ssindex]
            uo = self.unitoperations[uoindex]
            tp = self.typicalprocess[tpindex]
            tech = self.techs[techindex]

            query = query % (subsector[0],uo[0],tp[0],tech[0]) 
            results = Status.DB.sql_query(query)
    
            if len(results)>0:
                if (type(results[0])!=type(())):
                    results = [ results ]
                for result in results:
                    allresults.append(result)
                    
        self.measures = allresults
        