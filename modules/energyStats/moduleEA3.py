#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA3- Final energy by equipment- Yearly data
#			
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Tom Sobota	21/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#       Revised by:         Stoyan Danov  07/04/2008
#       Revised by:         Stoyan Danov     11/04/2008
#       Revised by:         Stoyan Danov     02/05/2008
#
#       Changes to previous version:
#       29/3/2008          Adapted to numpy arrays
#       07/4/2008          Adapted to use data from sql, not checked
#       11/04/2008: SD: Dummy data added for displaying temporaly, to avoid problems with None.
#                       Return to original state later!
#                       Control for DBFluid_id = None, to be checked.
#       02/05/2008: SD: sqlQuery -> to initModule; sejf.interfaces -> Status.int; None resistance control, avoid ZeroDivision
#       05/05/2008: HS  check of Fuel-id eliminated. not necessary here
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
import wx

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP

def _U(text):
    return unicode(_(text),"utf-8")

class ModuleEA3(object):

    def __init__(self, keys):
        self.keys = keys # two grids, so a list of (2) keys

        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------

        Status.mod.moduleEA.update()

        PId = Status.PId
        ANo = Status.ANo

        self.equipments = Status.prj.getEquipments()
        self.NEquipe = len(self.equipments)

        dbfuel = Status.DB.dbfuel
        NDBFuel = len(dbfuel)

# Final energy consumption by equipments 

        TotalFETj = 0.0
        TotalUSHj = 0.0
        EquipName = []
        FETj = []
        USHj = []
        FuelType = []

        for equipe in self.equipments:
            Equipment = unicode(equipe.Equipment,"utf-8")
            EquipName.append(Equipment)


#................................................................................
            if equipe.FETj is None:#SD: None control added
                TotalFETj += 0.0
                FETj.append(0.0)
            else:
                TotalFETj += equipe.FETj/1000.0
                FETj.append(equipe.FETj/1000.0)

            if equipe.USHj is None:
                TotalUSHj += 0.0
                USHj.append(0.0)
            else:
                TotalUSHj += equipe.USHj/1000.0
                USHj.append(equipe.USHj/1000.0)


            DBFuel_id = equipe.DBFuel_id
            if DBFuel_id is None or NDBFuel==0: 
                FuelName = _U('Electricity')
            else:
                try:
                    FuelName = unicode(dbfuel.DBFuel_ID[DBFuel_id][0].FuelName,"utf-8")
                except:
                    FuelName = 'not available'

            equipmentClass = getEquipmentClass(equipe.EquipType)
            if equipmentClass == "CHP":
                FuelName += "(- gen.elect.)"
                
            FuelType.append(FuelName)

#.................................................................................           

#        print 'TotalFET (calculated from CGenerationHC) = ', TotalFETj

        FETjPercentage = []
        USHjPercentage = []

        for i in range (self.NEquipe):
            if TotalFETj > 0.0: #SD avoid division by zero
                FETjPercentage.append(FETj[i]*100.0/TotalFETj)
            else:
                FETjPercentage.append(0.0)

            if TotalUSHj > 0.0:
                USHjPercentage.append(USHj[i]*100.0/TotalUSHj)
            else:
                USHjPercentage.append(0.0)


#.............................................................................
        #finish the table columns, add total, percentage total
        EquipName.append('Total')
        FuelType.append('')
        FETj.append(TotalFETj)
        USHj.append(TotalUSHj)

        sum = 0
        for i in FETjPercentage:
            sum += i
        FETjPercentage.append(sum)

        sum = 0
        for i in USHjPercentage:
            sum += i
        USHjPercentage.append(sum)
#.........................................................
            

        #
        # upper grid FET by equipment
        #
        TableColumnList1 = [EquipName,FuelType,FETj,FETjPercentage]

        #screen list and substitute None with "not available"
        for i in range(len(TableColumnList1)):
            for j in range(len(TableColumnList1[i])):
                if TableColumnList1[i][j] == None:
                    TableColumnList1[i][j] = 0           
        
        matrix1 = transpose(TableColumnList1)
        data1 = array(matrix1)     
                          
        Status.int.setGraphicsData(self.keys[0], data1)
        #
        # lower grid USH by equipment
        #
        TableColumnList2 = [EquipName,USHj,USHjPercentage]

        #screen list and substitute None with "not available"
        for i in range(len(TableColumnList2)):
            for j in range(len(TableColumnList2[i])):
                if TableColumnList2[i][j] == None:
                    TableColumnList2[i][j] = 0
                    
        matrix2 = transpose(TableColumnList2)
        data2 = array(matrix2)

        Status.int.setGraphicsData(self.keys[1], data2)

#------------------------------------------------------------------------------
        reportMatrix1 = []
        for i in range(len(matrix1)-1):
            if i < 10:
                reportMatrix1.append(matrix1[i])
        for i in range(len(matrix1)-1,10):
            reportMatrix1.append([" "," "," "," "])
        reportMatrix1.append(matrix1[len(matrix1)-1])

        reportData1 = array(reportMatrix1)
        print reportData1

        if Status.ANo == 0:
            Status.int.setGraphicsData("EA3_FET_REPORT", reportData1)
        elif Status.ANo == Status.FinalAlternative:
            Status.int.setGraphicsData("EA3_FET_REPORT_F", reportData1)

        reportMatrix2 = []
        for i in range(len(matrix2)-1):
            if i < 10:
                reportMatrix2.append(matrix2[i])
        for i in range(len(matrix2)-1,10):
            reportMatrix2.append([" "," "," "])
        reportMatrix2.append(matrix2[len(matrix2)-1])

        reportData2 = array(reportMatrix2)
        print reportData2

        if Status.ANo == 0:
            Status.int.setGraphicsData("EA3_USH_REPORT", reportData2)
        elif Status.ANo == Status.FinalAlternative:
            Status.int.setGraphicsData("EA3_USH_REPORT_F", reportData2)
#------------------------------------------------------------------------------

#==============================================================================
