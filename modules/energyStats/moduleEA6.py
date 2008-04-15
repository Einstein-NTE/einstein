#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA6- Production of CO2- Yearly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	21/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#       Last revised by:    Stoyan Danov 07/04/2008
#       Revised by:         Stoyan Danov     11/04/2008
#
#       Changes to previous version:
#	28/03/08:   functions draw_ ... moved to panel
#	28/03/08:   changed functions draw... to use numpy arrays,
#       07/04/08:   adapted to use data from sql, not checked
#       11/04/2008: SD: Dummy data added for displaying temporaly, to avoid problems with None.
#                       Return to original state later!
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

class ModuleEA6(object):

    def __init__(self, keys):
        print "ModuleEA6 (__init__)"
        self.keys = keys
        self.interface = Interfaces()
#.....................................................................
        PId = Status.PId
        ANo = Status.ANo

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(PId,ANo)
        self.cgeneraldata = Status.DB.cgeneraldata.sql_select(sqlQuery)[0]

        self.fuels = Status.DB.qfuel.sql_select(sqlQuery)
        self.NFuels = len(self.fuels)
        print "%s fuels found" % self.NFuels

        self.cfuel = Status.DB.cfuel.sql_select(sqlQuery) 
#......................................................................
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------

        FuelType = []
        ProdCO2 = []
        TotalProdCO2 = 0.0
        for row in self.cfuel:
            Fuel_id = Status.DB.qfuel.QFuel_ID[row.QFuel_id][0].DBFuel_id
            FuelName = Status.DB.dbfuel.DBFuel_ID[Fuel_id][0].FuelName
            FuelType.append(FuelName)
            TotalProdCO2 += row.ProdCO2Fuel
            ProdCO2.append(row.ProdCO2Fuel)

        FuelType.append('Electricity')
        
        ProdCO2Elect = self.cgeneraldata.ProdCO2Elect
        ProdCO2.append(ProdCO2Elect)

        TotalProdCO2 += ProdCO2Elect

        PercentageProdCO2 = []
        for i in range(len(self.cfuel)):
            Percent = ProdCO2[i]*100.0/TotalProdCO2
            PercentageProdCO2.append(Percent)

        Percent = ProdCO2Elect*100.0/TotalProdCO2
        PercentageProdCO2.append(Percent)

#.........................................................        
        #finish the table columns, add total, total percentage
        FuelType.append('Total')
        ProdCO2.append(TotalProdCO2)

        suma = 0
        for i in PercentageProdCO2:
            suma += i
        PercentageProdCO2.append(suma)

#.........................................................
        # generate data for graphics

        TableColumnList = [FuelType, ProdCO2, PercentageProdCO2]
        matrix = transpose(TableColumnList)
        data = array(matrix)

        dummydata = array([['Heavy fuel oil',   0.0,    0.00],
                      ['Natural gas'   ,  50.0,   28.17],
                      ['Gas oil'       ,  25.0,   14.08],
                      ['LPG'           ,  75.0,   42.25],
                      ['Other'         ,   0.0,    0.00],
                      ['Electricity'   ,  27.5,   15.49],
                      ['Total'         , 177.5,  100.00]])

        self.interface.setGraphicsData(self.keys[0], dummydata)

        #print "ModuleEA6 graphics data initialization"
        #print "Interfaces.GData[%s] contains:\n%s\n" % (self.keys[0], repr(Interfaces.GData[self.keys[0]))

        return "ok"

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
