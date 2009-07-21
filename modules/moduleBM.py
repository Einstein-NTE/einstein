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
from einstein.GUI.units import *

class ModuleBM(object):
    
#------------------------------------------------------------------------------
    def __init__(self, keys):
#------------------------------------------------------------------------------
#       the init function is called quite at the beginning of the session
#       no project information available yet !!!
#------------------------------------------------------------------------------
        self.keys = keys # the key to the data is sent by the panel
        self.process = None
        self.product = None
        self.procNo = 0
        self.prodNo = 0
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self, keys):
#------------------------------------------------------------------------------
#       function called from the panel once the user enters the panel
#------------------------------------------------------------------------------

        self.keys = keys # the key to the data is sent by the panel

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
        self.productCodes = Status.prj.getProductList("ProductCode")
        self.productUnits = Status.prj.getProductList("ProdUnit")
        
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

        bmList = self.findBenchmarks()[0]
        data = array(noneFilter(bmList))
#        print "ModuleBM (updatePanel): key %s data %s"%(self.keys[0],data)

        Status.int.setGraphicsData(self.keys[0], data)

        Status.int.setGraphicsData("%s Figure"%self.keys[0], self.createBMgraphs())

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

        bmListReport = [["","","","","",""]]
        for i in range(10):
            if i < len(bmList): #bmList
                bmListReport.append(bmList[i])
            else:
                bmListReport.append([" "," "," "," "," "," "])

        dataReport = array(noneFilter(bmListReport))
        Status.int.setGraphicsData("%s_REPORT"%self.keys[0], dataReport)

        if self.keys[0] == "BM1":
            ext = ""
        elif self.keys[0] == "BM2":
            ext = "%02d_"%self.prodNo
        elif self.keys[0] == "BM3":
            ext = "%02d_"%self.procNo

#        print "ModuleBM (updatePanel): extenstion = %s"%ext
                        
        if Status.ANo == 0:
            Status.int.setGraphicsData("%s_%sREPORT"%(self.keys[0],ext),dataReport)
        elif Status.ANo == Status.FinalAlternative:
            Status.int.setGraphicsData("%s_%sREPORT_F"%(self.keys[0],ext),dataReport)

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

#        print "ModuleBM (updateSearch): new search criteria",searchCriteria

        self.updatePanel()
        
#------------------------------------------------------------------------------
    def createBMgraphs(self):
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
            tar_fuel = self.bmTable[i][6]
            if tar_fuel is not None:
                bmtar_fuel.append([tar_fuel])
            else:
                bmtar_fuel.append([0.0])

            tar_el = self.bmTable[i][9]
            if tar_el is not None:
                bmtar_el.append([tar_el])
            else:
                bmtar_el.append([0.0])

            e0 = self.bmTable[i][10]
            e1 = self.bmTable[i][11]
            f0 = self.bmTable[i][7]
            f1 = self.bmTable[i][8]

            if e0 is not None: elmin = min(e0,elmin)
            if e1 is not None: elmax = max(e1,elmax)

            if f0 is not None: fuelmin = min(f0,fuelmin)
            if f1 is not None: fuelmax = max(f1,fuelmax)
            
            bm_el.append(   [e0,e0,e1,e1,e0])
            bm_fuel.append( [f0,f1,f1,f0,f0])

        for i in range(Status.NoOfAlternatives+1):

            if self.keys[0] == "BM1":
                generalDataTable = Status.DB.cgeneraldata.Questionnaire_id[Status.PId].AlternativeProposalNo[i]
                if len(generalDataTable) > 0:
                    generalData = generalDataTable[0]

                    SECel = generalData.EL_INT
                    SECfuel = generalData.FUEL_INT
                else:
                    SECel = 0.0
                    SECfuel = 0.0
                    logDebug("ModuleBM (createBMgraphs): no generalData entry found for ANo = %s"%i)
                
            elif self.keys[0] == "BM2":
                productTable = Status.DB.qproduct.Questionnaire_id[Status.PId].AlternativeProposalNo[i].Product[self.product]
                if len(productTable) > 0:
                    product = productTable[0]

                    SECel = product.EL_SEC
                    SECfuel = product.FUEL_SEC
                else:
                    SECel = 0.0
                    SECfuel = 0.0
                    logDebug("ModuleBM (createBMgraphs): no product data entry found for ANo = %s"%i)

            elif self.keys[0] == "BM3":
                processTable = Status.DB.qprocessdata.Questionnaire_id[Status.PId].AlternativeProposalNo[i].Process[self.process]
                if len(processTable) > 0:
                    process = processTable[0]

                    SECel = process.EL_SEC
                    SECfuel = process.UPH_SEC
                else:
                    SECel = 0.0
                    SECfuel = 0.0
                    logDebug("ModuleBM (createBMgraphs): no process data entry found for ANo = %s"%i)

            else:
                logDebug("ModuleBM (createBMgraphs): called with erroneous key: %s "%self.keys[0])

            if SECel is not None:
                elmin = min(SECel,elmin)
                elmax = max(SECel,elmax)
                
            if SECfuel is not None:
                fuelmin = min(SECfuel,fuelmin)
                fuelmax = max(SECfuel,fuelmax)
            
            ps_el.append([SECel])
            ps_fuel.append([SECfuel])

        config = [0.9*elmin,elmax*1.1,0.9*fuelmin,fuelmax*1.1]

#        print "createBMgraphs: bmtar_el  ",bmtar_el
#        print "createBMgraphs: bmtar_fuel",bmtar_fuel
#        print "createBMgraphs: ps_el  ",ps_el
#        print "createBMgraphs: ps_fuel  ",ps_fuel
        
        
        return [config,bmtar_el,bmtar_fuel,bm_el,bm_fuel,ps_el,ps_fuel]

#------------------------------------------------------------------------------
    def findBenchmarks(self):
#------------------------------------------------------------------------------
#       looks up for benchmarks within the database
#------------------------------------------------------------------------------

#        print "ModuleBM (findBenchmarks): creating panel data"
        
        if self.year0 > 0:
            sqlQuery = "YearReference > %s AND YearReference < %s ORDER BY YearReference DESC"%(self.year0,self.year1)

        else:
            sqlQuery = "YearReference < %s ORDER BY YearReference DESC"%(self.year1)
            
        benchmarks = Status.DB.dbbenchmark.sql_select(sqlQuery)

#        print "ModuleBM (findBenchmarks): screening year of reference -> %s benchmarks found"%len(benchmarks)
        
        self.bmIDs = []
        self.bmTable = []
        plus = 0.1

#..............................................................................
#energy intensity benchmarks
        
        for benchmark in benchmarks:
            selected = False

            if self.keys[0] == "BM1":
#                naceCodeID = benchmark.NaceCode_id

#                print "ModuleBM (findBenchmarks): screening by NACE Code ID %s"%naceCodeID
#                naces = Status.DB.dbnacecode.DBNaceCode_ID[naceCodeID]

#                if len(naces) > 0:
#                    nace = naces[0]
#                    naceCode = nace.CodeNACE
#                    naceCodeSub = nace.CodeNACEsub

                naceBM = benchmark.NACECode
                if naceBM is not None:
                    naceBMsplit = naceBM.split('.')
                else:
                    naceBMsplit = []
                    
                if len(naceBMsplit) > 0:
                    naceCode = str(naceBMsplit[0])
                    if len(naceBMsplit) >= 2:
                        naceCodeSub = str(naceBMsplit[1])
                    else:
                        naceCodeSub = "00"                

#                    print "naceCode of benchmark entry: ",naceCode,naceCodeSub

                    if str(naceCode) == self.naceFilter:

                        level = self.naceSearch #from 0 to 2

#                        print "now comparing with level %s: "%level,self.naceSearch,naceCodeSub,self.naceCodeSub

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

#                            print "hasData el %s fuel %s PEC %s "%(hasFECelData,hasFECfuelData,hasPECData)
                            if hasData:
                                selected = True
                else:
#                    logWarning(_("Error in benchmark database has been detected: ID %s not found. Update your database")%naceCodeID)
                    logWarning(_("Error in benchmark database has been detected (id %s): NACE Code %s not found. Update your database")%\
                               (naceBM,benchmark.DBBenchmark_ID))
                    
#..............................................................................
#specific energy consumption by products benchmarks
                    
            elif self.keys[0] == "BM2":       #energy intensity benchmarks

                productCode = benchmark.ProductCode

                if self.product in self.products:
                    idx = self.products.index(self.product)
                    self.prodNo = idx+1
                    self.productCode = self.productCodes[idx]
                    pu = self.productUnits[idx]
                    
                else:
                    self.productCode = None
                    self.prodNo = 0
                    pu = "t"
                    
#                print "ModuleBM (findBMs): productCode BM: %s - product %s [%s]"%\
#                      (productCode,self.product,self.productCode)

                
                if self.productCode == productCode and productCode is not None:
                                   
                    FECel = [benchmark.E_SEC_TARG,\
                             benchmark.E_SEC_MIN,\
                             benchmark.E_SEC_MAX]

                    pu_BM = benchmark.E_Unit
                    fc = conversionFactor(pu)/conversionFactor(pu_BM)
                    for i in range(len(FECel)):
                        if FECel[i] is not None:
                            FECel[i] *= fc

                    hasFECelData = ((FECel[0] is not None) or (FECel[1]is not None) or (FECel[2] is not None))
                    
                    FECfuel = [benchmark.H_SEC_TARG,\
                             benchmark.H_SEC_MIN,\
                             benchmark.H_SEC_MAX]

                    pu_BM = benchmark.H_Unit
                    fc = conversionFactor(pu)/conversionFactor(pu_BM)

#                    print "pu %s [%s] pu_BM %s [%s] fc %s"%\
#                          (pu,conversionFactor(pu),pu_BM,conversionFactor(pu_BM),fc)
                    
                    for i in range(len(FECfuel)):
                        if FECfuel[i] is not None:
                            FECfuel[i] *= fc

                    hasFECfuelData = ((FECfuel[0] is not None) or (FECfuel[1]is not None) or (FECfuel[2] is not None))

                    PEC =   [benchmark.T_SEC_TARG,\
                             benchmark.T_SEC_MIN,\
                             benchmark.T_SEC_MAX]

                    pu_BM = benchmark.T_Unit
                    fc = conversionFactor(pu)/conversionFactor(pu_BM)
                    for i in range(len(PEC)):
                        if PEC[i] is not None:
                            PEC[i] *= fc

                    hasPECData = ((PEC[0] is not None) or (PEC[1]is not None) or (PEC[2] is not None))

                    hasData = hasFECelData or hasFECfuelData or hasPECData

#                    print "hasData el %s fuel %s PEC %s "%(hasFECelData,hasFECfuelData,hasPECData)
                    if hasData:
                        selected = True

#..............................................................................
#specific energy consumption by unit operation - benchmarks
                    
            elif self.keys[0] == "BM3":       #energy intensity benchmarks

                unitOpCode = benchmark.UnitOp
                if self.process in self.processes:
                    idx = self.processes.index(self.process)
                    self.unitOp = self.unitOps[idx]
                    self.procNo = idx+1
                    unitOpTable = Status.DB.dbunitoperation.UnitOperation[self.unitOp]
                    if len(unitOpTable) > 0:
                        self.unitOpCode = unitOpTable[0].UnitOperationCode
                    else:
                        self.unitOpCode = None
                        self.procNo = 0
                else:
                    self.unitOp = None
                    self.unitOpCode = None
                    self.procNo = 0
#                print "ModuleBM (findBMs): looking for unitOp %s [BM: %s]"%(self.unitOpCode,unitOpCode)
                    
                if self.unitOpCode == unitOpCode:
                                   
                    FECel = [benchmark.E_SEC_TARG,\
                             benchmark.E_SEC_MIN,\
                             benchmark.E_SEC_MAX]

                    hasFECelData = ((FECel[0] is not None) or (FECel[1]is not None) or (FECel[2] is not None))
                    
                    FECfuel = [benchmark.H_SEC_TARG,\
                             benchmark.H_SEC_MIN,\
                             benchmark.H_SEC_MAX]

                    hasFECfuelData = ((FECfuel[0] is not None) or (FECfuel[1]is not None) or (FECfuel[2] is not None))

                    PEC =   [benchmark.T_SEC_TARG,\
                             benchmark.T_SEC_MIN,\
                             benchmark.T_SEC_MAX]

                    hasPECData = ((PEC[0] is not None) or (PEC[1]is not None) or (PEC[2] is not None))

                    hasData = hasFECelData or hasFECfuelData or hasPECData

#                    print "hasData el %s fuel %s PEC %s "%(hasFECelData,hasFECfuelData,hasPECData)
                    if hasData:
                        selected = True
                
#..............................................................................
# common block for all types of benchmarks

            if selected == True:

                source = benchmark.Literature
                reference = benchmark.Reference
                validity = benchmark.DataRelevance
                
                self.bmIDs.append(int(benchmark.DBBenchmark_ID))
                
                tableEntry = [source,reference,validity]
                tableEntry.extend(PEC)
                tableEntry.extend(FECfuel)
                tableEntry.extend(FECel)

#                print "selected benchmark: ",tableEntry
                self.bmTable.append(tableEntry)

        return self.bmTable,self.bmIDs
            
#------------------------------------------------------------------------------

#==============================================================================

if __name__ == "__main__":
    pass
