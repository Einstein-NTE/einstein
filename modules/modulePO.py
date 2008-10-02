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
            self.getTypicalProcess(self.unitoperationSelection)
        else:
            self.typicalprocess = [ ] 
        
        if (self.typicalprocessSelection!=None):
            self.getTechnologies(self.typicalprocessSelection)
        else: 
            self.techs = [ ]
        
        if (self.typicalprocessSelection!=None):
            self.getMeasures()
        else:
            self.measures = []
    
          
    def runPOModule(self):
       pass 
   
    def getSectors(self):
        query = """SELECT IDSector,Name FROM poSector"""
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.sectors = results 
        else:
            self.sectors = []
            
    def getSubsectors(self,index):
        query = """SELECT IDSubsector,Name FROM poSubsector WHERE SectorID = %s"""
        sector = self.sectors[index]
        query = query % sector[0] 
        
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.subsectors = results 
        else:
            self.subsectors = [] 
            
    def getUnitoperation(self,index):
        query = """SELECT IDUnitOperation, Name FROM pounitoperation as unit, posubsector_to_uo as link 
                   WHERE unit.IDUnitOperation = link.UnitOperationID AND link.SubsectorID = %s"""
        subsector = self.subsectors[index]
        query = query % subsector[0]  
        results = Status.DB.sql_query(query)  
        
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
                self.unitoperations = results 
        else:
            self.unitoperations = []
    
    def getTypicalProcess(self,index):
        query = """SELECT IDTypicalProcess,Name FROM poTypicalProcess WHERE UnitOperationID = %s"""
        uo = self.unitoperations[index]
        query = query % uo[0]        
        
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.typicalprocess = results 
        else:
            self.typicalprocess = []
                 
    def getTechnologies(self,index):
        query = """SELECT tech.IDTechnology, tp.Name, tech.Name FROM poEMList as list, poTypicalProcess as tp, poTech as tech 
                   WHERE tp.IDTypicalProcess = list.TypicalProcessID AND tech.IDtechnology = list.TechnologyID 
                         AND list.TypicalProcessID = %s"""
        #tech = self.techs[self.cbTech.GetSelection()]
        tp   = self.typicalprocess[index]
        query = query % (tp[0]) 
        
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.techs = results 
        else:
            self.techs = []
    
    def getMeasures(self):
        allresults = [ ]   
        for techindex in self.techSelection:
            query = """SELECT em.ShortDescription, em.Text FROM poEfficiencyMeasure as em, poEmListEntry as entry, poEMList as list
                       WHERE  entry.EfficiencyMeasureID = em.IDEfficiencyMeasure
                       AND    entry.EMListID = list.IDEMList
                       AND    list.TypicalProcessID = %s
                       AND    list.TechnologyID = %s"""
            tp = self.typicalprocess[self.typicalprocessSelection]
            tech = self.techs[techindex]

            query = query % (tp[0],tech[0]) 
            results = Status.DB.sql_query(query)
    
            if len(results)>0:
                if (type(results[0])!=type(())):
                    results = [ results ]
                for result in results:
                    allresults.append(result)
                    
        self.measures = allresults
        