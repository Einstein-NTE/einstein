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
#	Version No.: 0.06
#	Created by: 	    Tom Sobota	    21/03/2008
#       Revised by:         Hans Schweiger  28/03/2008
#                           Tom Sobota      28/03/2008
#                           Stoyan Danov    07/04/2008
#                           Stoyan Danov    11/04/2008
#                           Hans Schweiger  13/04/2008
#                           Stoyan Danov    02/05/2008
#
#       Changes to previous version:
#	28/03/08:   functions draw_ ... moved to panel
#	28/03/08:   TS changed functions draw... to use numpy arrays,
#       07/04/2008: SD Adapted to show data from sql, not checked
#       11/04/2008: SD: Dummy data added for displaying temporaly, to avoid problems with None.
#                       Return to original state later!
#       13/04/2008: HS: initialisation moved to function initPanel
#       02/05/2008: SD: C->Q tables, change FECi,FETi(old) to FECFuel,FEFFuel; self.interfaces -> Status.int #SD, check for None
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

#------------------------------------------------------------------------------
    def __init__(self, keys):
#------------------------------------------------------------------------------
#   instance of module is created at the beginning when GUI is built-up
#   only basic initialisation
#------------------------------------------------------------------------------
        self.keys = keys # keys for accessing the data in Interfaces
#        self.interface = Interfaces() #SD
#------------------------------------------------------------------------------
        dummydata = array([['Heavy fuel oil' ,  0.0,   0.00,   0.0,   0.00],#temporary solution of Nones, SD
                      ['Natural gas'    ,200.0,  30.77, 180.0,  32.73],
                      ['Gas oil'        ,100.0,  15.38,  50.0,   9.09],
                      ['LPG'            ,300.0,  46.15, 300.0,  54.55],
                      ['Other'          ,  0.0,   0.00,   0.0,   0.00],
                      ['Electricity'    , 50.0,   7.69,  20.0,   3.64],
                      ['Total'          ,650.0, 100.00, 550.0, 100.00]])

                          
        Status.int.setGraphicsData(self.keys[0], dummydata)#SD

        self.initPanel()

    def initPanel(self):
#------------------------------------------------------------------------------
#   initialisation of the Panel before displaying.
#   activated when EA1 is selected on the tree
#------------------------------------------------------------------------------
#..............................................................................
#   get access to the info in SQL

        PId = Status.PId
        ANo = Status.ANo

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(PId,ANo)
        self.equipements = Status.DB.qgenerationhc.sql_select(sqlQuery) 
        self.NEquipe = len(self.equipements)
        print "PanelEA1 (initPanel): %s equipes found" % self.NEquipe

        self.fuels = Status.DB.qfuel.sql_select(sqlQuery)

#        self.cfuel = Status.DB.cfuel.sql_select(sqlQuery) #SD 
        self.NFuels = len(self.fuels)#SD
        print "PanelEA1 (initPanel): %s fuels found" % self.NFuels

#..............................................................................
# Final energy consumption by fuels (data for panel EA1)

        TotalFEC = 0.0
        TotalFETi = 0.0
        FEC = []
        FETi = []
        FuelType = []
            
        for row in self.fuels:  #sum all FECFuel/FETFuel for fuels used #SD 
            Fuel_id = row.DBFuel_id #SD
            FuelName = Status.DB.dbfuel.DBFuel_ID[Fuel_id][0].FuelName
            FuelType.append(FuelName)
            TotalFEC += row.FECFuel #SD
            FEC.append(row.FECFuel)#SD
            TotalFETi += row.FETFuel#SD
            FETi.append(row.FETFuel)#SD

        FECel = Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FECel #SD: check for None follows
        FETel = Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FETel
        if FECel is not None:
            TotalFEC += FECel  #add FECel to TotalFEC
            FEC.append(FECel) #SD: check if OK here
        else:
            TotalFEC += 0.0
            FEC.append(-1) #SD: check if OK here

        if FETel is not None:
            TotalFETi += FETel
            FETi.append(FETel) #SD: check if OK here
        else:
            TotalFETi += 0.0
            FETi.append(-1) #SD: check if OK here
            
        FuelType.append("Electricity")
##        FEC.append(Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FECel)
##        FETi.append(Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FETel)

        #save TotalFEC in CGeneralData table in DB variable FEC (FEC total) #Necessary ?? SD
        Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FEC = TotalFEC
        Status.DB.cgeneraldata.Questionnaire_id[Status.PId][0].FET = TotalFETi
        Status.SQL.commit() 

        FECPercentage = []
        FETPercentage = []

        for i in range (self.NFuels + 1):
            if TotalFEC > 0.0: #SD avoid division by zero
                FECPercentage.append(FEC[i]*100.0/TotalFEC)
            else:
                FECPercentage.append(-1)
            if TotalFETi > 0.0: #SD avoid division by zero
                FETPercentage.append(FETi[i]*100.0/TotalFETi)
            else:
                FETPercentage.append(-1)

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

        Status.int.setGraphicsData(self.keys[0], data) #SD

#------------------------------------------------------------------------------

#==============================================================================
