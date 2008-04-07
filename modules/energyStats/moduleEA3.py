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
#
#       Changes to previous version:
#       29/3/2008          Adapted to numpy arrays
#       07/4/2008          Adapted to use data from sql, not checked
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

class ModuleEA3(object):

    def __init__(self, keys):
        self.keys = keys # two grids, so a list of (2) keys
        self.interface = Interfaces()
#...............................................................
        PId = Status.PId
        ANo = Status.ANo

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(PId,ANo)
        self.equipements = Status.DB.qgenerationhc.sql_select(sqlQuery)
        self.NEquipe = len(self.equipements)
        print "%s equipes found" % self.NEquipe

        self.fuels = Status.DB.qfuel.sql_select(sqlQuery)
        self.NFuels = len(self.fuels)
        print "%s fuels found" % self.NFuels

        self.cfuel = Status.DB.cfuel.sql_select(sqlQuery)

        self.cgenerationhc = Status.DB.cgenerationhc.sql_select(sqlQuery)
#................................................................
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------

# Final energy consumption by equipments 

        TotalFETj = 0.0
        TotalUSHj = 0.0
        EquipName = []
        FETj = []
        USHj = []
        FuelType = []
        
        for row in self.cgenerationhc:
            Equipment = Status.DB.qgenerationhc.QGenerationHC_ID[row.QGenerationHC_id][0].Equipment
            EquipName.append(Equipment)

            Fuel_id = Status.DB.qgenerationhc.QGenerationHC_ID[row.QGenerationHC_id][0].DBFuel_id
            print "EA3: Fuel_id = ",Fuel_id
            FuelName = Status.DB.dbfuel.DBFuel_ID[Fuel_id][0].FuelName
            FuelType.append(FuelName)
            
            TotalFETj += row.FETj
            FETj.append(row.FETj)

            TotalUSHj += row.USHj
            USHj.append(row.USHj)
            

#        print 'TotalFET (calculated from CGenerationHC) = ', TotalFETj

        FETjPercentage = []
        USHjPercentage = []


        for i in range (self.NEquipe):
            FETjPercentage.append(FETj[i]*100.0/TotalFETj)
            USHjPercentage.append(USHj[i]*100.0/TotalUSHj)


#.............................................................................
        #finish the table columns, add total, percentage total
        EquipName.append('Total')
        FuelType.append('')
        FETj.append(TotalFETj)
        USHj.append(TotalUSHj)

        suma = 0
        for i in FETjPercentage:
            suma += i
        FETjPercentage.append(suma)

        suma = 0
        for i in USHjPercentage:
            suma += i
        USHjPercentage.append(suma)
#.........................................................
            

        #
        # upper grid FET by equipment
        #
        TableColumnList1 = [EquipName,FuelType,FETj,FETjPercentage]
        matrix1 = transpose(TableColumnList1)
        data1 = array(matrix1)
                          
        self.interface.setGraphicsData(self.keys[0], data1)
        #
        # lower grid USH by equipment
        #
        TableColumnList2 = [EquipName,USHj,USHjPercentage]
        matrix2 = transpose(TableColumnList2)
        data2 = array(matrix2)

        self.interface.setGraphicsData(self.keys[1], data2)

#------------------------------------------------------------------------------
    def exitModule(self,exit_option):
#------------------------------------------------------------------------------
        """
        carries out any calculations necessary previous to displaying the HP
        design assitant window
        """
#------------------------------------------------------------------------------
        if exit_option == "save":
            print "exitModule: here I should save the current configuration"
        elif exit_option == "cancel":
            print "exitModule: here I should retreive the previous configuration"
            

        print "exitModule: function not yet defined"

        return "ok"

#------------------------------------------------------------------------------

#==============================================================================
