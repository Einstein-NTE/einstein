#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (http://www.iee-einstein.org/)
#
#------------------------------------------------------------------------------
#
#	ModuleEA1- Primary energy - Yearly data
#
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Tom Sobota	   21/03/2008
#       Revised by:         Hans Schweiger 28/03/2008
#       Revised by:         Tom Sobota     28/03/2008
#       Revised by:         Stoyan Danov     07/04/2008
#
#       Changes to previous version:
#	28/03/08:   functions draw_ ... moved to panel
#	28/03/08:   TS changed functions draw... to use numpy arrays,
#       07/04/2008: SD Adapted to show data from sql, not checked
#                   
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	http://www.energyxperts.net/
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

class ModuleEA1(object):

    def __init__(self, keys):
        self.keys = keys # keys for accessing the data in Interfaces
        self.interface = Interfaces()
#..............................................................................

        PId = Status.PId
        ANo = Status.ANo

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(PId,ANo)
        self.equipements = Status.DB.qgenerationhc.sql_select(sqlQuery) 
        self.NEquipe = len(self.equipements)
        print "%s equipes found" % self.NEquipe

        self.fuels = Status.DB.qfuel.sql_select(sqlQuery)

        self.cfuel = Status.DB.cfuel.sql_select(sqlQuery) 
        self.NFuels = len(self.cfuel)
        print "%s fuels found" % self.NFuels
        
#..............................................................................

        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------

        """
        module initialization
        """
#------------------------------------------------------------------------------
        # Here, the data for the tables and graphs are loaded in Interfaces,
        # to be recovered later in the gui panel. 
        # There is one table and two graphs in this page, which will work with the same set
        # of data
        #
        # The storing of the data is done row by row using a numpy array, in the same
        # order as it will be presented in the table
        # The numeric values will be stored by 'array' as strings, but here it is not
        # necessary to enclose them in quotes.
        #
        # This data is only an example, the actual data will come from the database
        #


#..............................................................................
# Final energy consumption by fuels (data for panel EA1)

        TotalFEC = 0.0
        TotalFETi = 0.0
        FEC = []
        FETi = []
        FuelType = []
            
        for row in self.cfuel:  #sum all FECi/FETi for fuels used
            Fuel_id = Status.DB.qfuel.QFuel_ID[row.QFuel_id][0].DBFuel_id
            FuelName = Status.DB.dbfuel.DBFuel_ID[Fuel_id][0].FuelName
            FuelType.append(FuelName)
            TotalFEC += row.FECi
            FEC.append(row.FECi)
            TotalFETi += row.FETi
            FETi.append(row.FETi)

        TotalFEC += Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FECel  #add FECel to TotalFEC
        TotalFETi += Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FETel
        FuelType.append("Electricity")
        FEC.append(Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FECel)
        FETi.append(Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FETel)

        #save TotalFEC in CGeneralData table in DB variable FEC (FEC total) #Necessary ?? SD
        Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FEC = TotalFEC
        Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FET = TotalFETi
        Status.SQL.commit() 

        FECPercentage = []
        FETPercentage = []

        for i in range (self.NFuels + 1):
            FECPercentage.append(FEC[i]*100.0/TotalFEC)
            FETPercentage.append(FETi[i]*100.0/TotalFETi)

#.........................................................        
        #finish the table columns, add total, sum percentage
        FuelType.append('Total')
        FEC.append(TotalFEC)
        FETi.append(TotalFETi)

        suma = 0
        for i in FECPercentage:
            suma += i
        FECPercentage.append(suma)

        suma = 0
        for i in FETPercentage:
            suma += i
        FETPercentage.append(suma)

#.........................................................

        TableColumnList = [FuelType,FEC,FECPercentage,FETi,FETPercentage]
        matrix = transpose(TableColumnList)
        data = array(matrix)
                          
        self.interface.setGraphicsData(self.keys[0], data)

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
