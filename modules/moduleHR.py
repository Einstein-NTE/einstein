# -*- coding: cp1252 -*-
#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#   ModuleHC (Heat and Cold Supply)
#           
#------------------------------------------------------------------------------
#           
#   Module for design of HC Supply cascade
#
#==============================================================================
#
#   Version No.: 0.01
#   Created by:         Hans Schweiger  10/06/2008
#   Last revised by:
#                       Hans Schweiger  23/06/2008
#
#   Changes to previous version:
#
#   23/06/2008: HS  Query of fluids and fuels used in export XML
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

from sys import *
from math import *
from numpy import *


from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP
from einstein.modules.constants import *
from einstein.modules.exportdata import *

class ModuleHR(object):

    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

        self.DB = Status.DB
        self.sql = Status.SQL
        
        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        self.hx = Status.DB.qheatexchanger.sql_select(sqlQuery)
        self.NHX = len(self.hx)

        Status.int.getEquipmentCascade()
        self.cascadeIndex = 0

        self.updatePanel()
            
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------

        dataList = []
        for i in range(self.NHX):
            row = {"equipeNo":1,"equipeType":"hx","equipePnom":1000}
            dataList.append(noneFilter([i+1,row["equipeNo"],"myname",row["equipeType"],row["equipePnom"],"???"]))
        data = array(dataList)

        Status.int.setGraphicsData(self.keys[0], data)

        try:
            Status.int.setGraphicsData('HR Info',{"noseque":55})
        except:
            pass

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def runHRModule(self):
#------------------------------------------------------------------------------
#       runs the calculations on the external HR module
#------------------------------------------------------------------------------

        Status.schedules.create()   #creates the process and equipment schedules

        fuelList = Status.prj.getQFuelList("DBFuel_id")
        fuelIDs = []
        for fuelID in fuelList:
            fuelIDs.append(int(fuelID))

        fluidList = []
        fluidList.extend(Status.prj.getEquipmentList("Refrigerant"))
        fluidList.extend(Status.prj.getPipeList("HeatDistMedium"))
        fluidList.extend(Status.prj.getProcessList("ProcMedDBFluid_id"))
        fluidList.extend(Status.prj.getProcessList("ProcMedOut"))
        fluidList.extend(Status.prj.getProcessList("SupplyMedDBFluid_id"))
        fluidList.extend(Status.prj.getWHEEList("WHEEMedium"))
        
        fluidIDs = []
        for fluidID in fluidList:
            if fluidID is not None:
                newID = int(fluidID)
                if newID not in fluidIDs:    #avoid double counting !!!
                    fluidIDs.append(newID)
                         
        ex = ExportDataHR(pid=Status.PId, ano=Status.ANo,fuels=fuelIDs, fluids=fluidIDs)

#        self.runHR()
#        self.importDataFromHR()

        pass
#------------------------------------------------------------------------------

if __name__ == "__main__":
    print "Testing ModuleHR"
    import einstein.GUI.pSQL as pSQL, MySQLdb
    from einstein.modules.interfaces import *
    from einstein.modules.energy.moduleEnergy import *
    stat = Status("testModuleHC")

    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    
    Status.PId = 99
    Status.ANo = 0
    Status.SetUpId = 1 #this is PSetUpData_ID
    
    Status.int = Interfaces()
    keys = ["HP Table","HP Plot","HP UserDef"]

    mod = ModuleHC(keys)
    
