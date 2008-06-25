# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleBM (Benchmarks)
#			
#------------------------------------------------------------------------------
#			
#	
#
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Hans Schweiger	08/04/2008
#	Last revised by:    Hans Schweiger      18/04/2008
#                           Hans Schweiger      25/06/2008
#
#       Changes to previous version:
#       18/04/2008 HS   Reference to Status.int
#       25/06/2008 HS   First real module functions activated:
#                       - query in benchmark DB
#	
#------------------------------------------------------------------------------		
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	www.energyxperts.net / info@energyxperts.net
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#============================================================================== 

from sys import *
from math import *
from numpy import *


from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
from einstein.modules.messageLogger import *
import einstein.modules.matPanel as mP

class ModuleBM(object):
    
#------------------------------------------------------------------------------
    def __init__(self, keys):
#------------------------------------------------------------------------------
#       the init function is called quite at the beginning of the session
#       no project information available yet !!!
#------------------------------------------------------------------------------
        self.keys = keys # the key to the data is sent by the panel

        self.DB = Status.DB
        self.sql = Status.SQL
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       function called from the panel once the user enters the panel
#------------------------------------------------------------------------------

#..............................................................................
# first get NACE code of current industry

        qTable = Status.DB.questionnaire.Questionnaire_ID[Status.PId]
        if len(qTable) > 0:
            subBranch = qTable[0].SubBranch
            
        naceTable = Status.DB.dbnacecode.NameNACEsub[str(subBranch)]
        if len(naceTable) > 0:
            naceCode = str(naceTable[0].CodeNACE)
            naceCodeSub = str(naceTable[0].CodeNACEsub)
        else:
            naceCode = "XY99"
            naceCodeSub = "99"

        self.naceSelector = []
        self.naceSelector.append(naceCode+"."+naceCodeSub)
        self.naceSelector.append(naceCode+"."+naceCodeSub[0:1]+"0")
        self.naceSelector.append(naceCode+".00")

        self.naceFilter = naceCode
        self.naceSubFilter = [naceCodeSub,naceCodeSub[0:1]+"0","00"]
        self.naceCodeSub = naceCodeSub

        self.naceSearch = 0

#..............................................................................
# get list of products and processes for BM2 and BM3

        self.products = Status.prj.getProductList("Product")
        self.processes = Status.prj.getProcessList("Process")
        self.unitOpIDs = Status.prj.getProcessList("DBUnitOperation_id")

        self.unitOps = []
        for unitOpID in self.unitOpIDs:
            unitOpTable = Status.DB.dbunitoperation.DBUnitOperation_ID[unitOpID]
            if len(unitOpTable) > 0:
                self.unitOps.append(unitOpTable[0].UnitOperation)
            else:
                self.unitOps.append("---")

        self.selector = 0

#..............................................................................
# sets default values for the search function

        self.naceSearch = 0 #searches for the specific subsector

        self.turnover0 = 0
        self.turnover1 = 1000.0
        
        self.year0 = 1990
        self.year1 = 2050

#..............................................................................
# call the updatePanel function to bring everything to the GUI
        self.updatePanel()
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       function called always when some of the information to be displayed on
#       GUI has changed
#------------------------------------------------------------------------------

#..............................................................................
# benchmarks on energy intensity

        data = array(noneFilter(self.findBenchmarks()[0]))

        Status.int.setGraphicsData("BM1 Table", data)
        Status.int.setGraphicsData("BM2 Table", data)
        Status.int.setGraphicsData("BM3 Table", data)

        Status.int.setGraphicsData("BM1 Figure", self.createBMgraphs("EINT"))
        Status.int.setGraphicsData("BM2 Figure", self.createBMgraphs("SECP"))
        Status.int.setGraphicsData("BM3 Figure", self.createBMgraphs("SECU"))

        Status.int.setGraphicsData('BM Info',[self.naceSearch,\
                                              self.naceSelector,\
                                              self.turnover0,\
                                              self.turnover1,\
                                              self.year0,\
                                              self.year1,\
                                              self.products,\
                                              self.processes,\
                                              self.unitOps,\
                                              self.selector])

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def updateSearch(self):
#------------------------------------------------------------------------------
#       takes the search criteria from the GUI and calls updatePanel
#------------------------------------------------------------------------------

        searchCriteria = Status.int.GData["BM Info"]
        
        self.naceSearch = searchCriteria[0]
        self.turnover0 = searchCriteria[2]
        self.turnover1 = searchCriteria[3]
        self.year0 = searchCriteria[4]
        self.year1 = searchCriteria[5]
        self.product = searchCriteria[6]
        self.process = searchCriteria[7]

        self.selector = searchCriteria[9]

        print "ModuleBM (updateSearch): new search criteria",searchCriteria

        self.updatePanel()
        
#------------------------------------------------------------------------------
    def createBMgraphs(self,bmType):
#------------------------------------------------------------------------------
#       creates benchmark graphs for plots in panel and report
#------------------------------------------------------------------------------

        bmtar_fuel = []
        bmtar_el = []
        bm_el = []
        bm_fuel = []
        ps_el = []
        ps_fuel = []

        elmin = 1.e+99
        elmax = 0
        fuelmin = 1.e+99
        fuelmax = 0
        
        for i in range(len(self.bmTable)):
            bmtar_fuel.append([self.bmTable[i][6]])
            bmtar_el.append([self.bmTable[i][9]])

            e0 = self.bmTable[i][10]
            e1 = self.bmTable[i][11]
            f0 = self.bmTable[i][7]
            f1 = self.bmTable[i][8]

            elmin = min(e0,elmin)
            elmax = max(e1,elmax)

            fuelmin = min(f0,fuelmin)
            fuelmax = max(f1,fuelmax)
            
            bm_el.append(   [e0,e0,e1,e1,e0])
            bm_fuel.append( [f0,f1,f1,f0,f0])

        for i in range(Status.NoOfAlternatives+1):

            SECel = 55.0
            SECfuel = 55.0

            elmin = min(SECel,elmin)
            elmax = max(SECel,elmax)
            fuelmin = min(SECfuel,fuelmin)
            fuelmax = max(SECfuel,fuelmax)
            
            ps_el.append([SECel])
            ps_fuel.append([SECfuel])

        config = [0.9*elmin,elmax*1.1,0.9*fuelmin,fuelmax*1.1]

        print "createBMgraphs: bmtar_el  ",bmtar_el
        print "createBMgraphs: bmtar_fuel",bmtar_fuel
        print "createBMgraphs: ps_el  ",ps_el
        print "createBMgraphs: ps_fuel  ",ps_fuel
        
        
        return [config,bmtar_el,bmtar_fuel,bm_el,bm_fuel,ps_el,ps_fuel]

#------------------------------------------------------------------------------
    def findBenchmarks(self):
#------------------------------------------------------------------------------
#       looks up for benchmarks within the database
#------------------------------------------------------------------------------

        print "ModuleBM (findBenchmarks): creating panel data"
        
        if self.year0 > 0:
            sqlQuery = "YearReference > %s AND YearReference < %s ORDER BY YearReference DESC"%(self.year0,self.year1)

        else:
            sqlQuery = "YearReference < %s ORDER BY YearReference DESC"%(self.year1)
            
        benchmarks = Status.DB.dbbenchmark.sql_select(sqlQuery)

        self.bmIDs = []
        self.bmTable = []
        plus = 0.1
        for benchmark in benchmarks:

            naceCodeID = benchmark.NaceCode_id
            naces = Status.DB.dbnacecode.DBNaceCode_ID[naceCodeID]

            selected = False
            
            if len(naces) > 0:
                nace = naces[0]
                naceCode = nace.CodeNACE
                naceCodeSub = nace.CodeNACEsub

                print "naceCode of benchmark entry: ",naceCode,naceCodeSub

                if str(naceCode) == self.naceFilter:

                    level = self.naceSearch #from 0 to 2

                    print "now comparing with level %s: "%level,self.naceSearch,naceCodeSub,self.naceCodeSub

                    subOK = 2
                    if ((str(naceCodeSub)[0:1] == self.naceCodeSub[0:1]) or (self.naceCodeSub == "0")):
                           subOK = 1
                           if ((str(naceCodeSub)[1:2] == self.naceCodeSub[1:2]) or (self.naceCodeSub[1:2] == "0")):
                               subOK = 0

                    if level >= subOK:
                               
                        FECel = [benchmark.E_EnergyInt_TARG_T,\
                                 benchmark.E_EnergyInt_MIN_T,\
                                 benchmark.E_EnergyInt_MAX_T]

                        hasFECelData = ((FECel[0] is not None) or (FECel[1]is not None) or (FECel[2] is not None))
                        
                        FECfuel = [benchmark.H_EnergyInt_TARG_T,\
                                 benchmark.H_EnergyInt_MIN_T,\
                                 benchmark.H_EnergyInt_MAX_T]

                        hasFECfuelData = ((FECfuel[0] is not None) or (FECfuel[1]is not None) or (FECfuel[2] is not None))

                        PEC =   [benchmark.T_EnergyInt_TARG_T,\
                                 benchmark.T_EnergyInt_MIN_T,\
                                 benchmark.T_EnergyInt_MAX_T]
  
                        hasPECData = ((PEC[0] is not None) or (PEC[1]is not None) or (PEC[2] is not None))

                        hasData = hasFECelData or hasFECfuelData or hasPECData

                        print "hasData el %s fuel %s PEC %s "%(hasFECelData,hasFECfuelData,hasPECData)
                        if hasData:
                            selected = True
            else:
                logWarning(_("Error in benchmark database has been detected: ID %s not found. Update your database")%naceCodeID)

                
            if selected == True:

                source = benchmark.Literature
                reference = benchmark.Reference
                validity = benchmark.DataRelevance
                
                self.bmIDs.append(int(benchmark.DBBenchmark_ID))
                
                tableEntry = [source,reference,validity]
                tableEntry.extend(PEC)
                tableEntry.extend(FECfuel)
                tableEntry.extend(FECel)

                print "selected benchmark: ",tableEntry
                self.bmTable.append(tableEntry)

        return self.bmTable,self.bmIDs
            
#------------------------------------------------------------------------------

#==============================================================================

if __name__ == "__main__":
    pass
