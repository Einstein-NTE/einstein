#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA5- Energy intensity- Yearly data
#			
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Tom Sobota	22/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#       Last revised by:    Stoyan Danov 07/04/2008
#       Revised by:         Stoyan Danov     11/04/2008
#       Revised by:         Stoyan Danov     02/05/2008
#
#       Changes to previous version:
#	28/03/08:   TS changed functions draw... to use numpy arrays,
#       07/04/08:   SD, adapted to use data from sql, not checked
#       11/04/2008: SD: Dummy data added for displaying temporaly, to avoid problems with None.
#                       Return to original state later!
#       02/05/2008: SD: sqlQuery -> to initModule; sejf.interfaces -> Status.int
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

class ModuleEA5(object):

    def __init__(self, keys):
        print "ModuleEA5(__init__)"
        self.keys = keys

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

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(PId,ANo)
        self.cgeneraldata = Status.DB.cgeneraldata.sql_select(sqlQuery)[0]
        self.questionnaire = Status.DB.questionnaire.Questionnaire_ID[PId][0]
        self.qproduct = Status.DB.qproduct.sql_select(sqlQuery)

#Part 1: Energy Intensity

#        TotalFEC = self.cgeneraldata.FEC   #FEC in [MWh]
#        ElectFEC = self.cgeneraldata.FECel
#        FuelsFEC = TotalFEC - ElectFEC
#        PE_FEC = self.cgeneraldata.PEC #substitute later the conv. coef. from SetUp #pending put conv. coef. in status.py
            
#        Turnover = self.questionnaire.Turnover #in [million euros]

#        if (Turnover > 0) and not (Turnover==None):    
#            self.cgeneraldata.FUEL_INT = (FuelsFEC)/(Turnover) #converted to [kWh/euro]
#            self.cgeneraldata.EL_INT = (ElectFEC)/(Turnover) #converted to [kWh/euro]
#            self.cgeneraldata.PE_INT = (PE_FEC)/(Turnover) #converted to [kWh/euro]
#        else:
#            self.cgeneraldata.FUEL_INT = None
#            self.cgeneraldata.EL_INT = None
#            self.cgeneraldata.PE_INT = None

# back-up in SQL                                      
#        Status.SQL.commit() #SD, to be checked


        EI_values = []
        EI_values.append(self.cgeneraldata.FUEL_INT)
        EI_values.append(self.cgeneraldata.EL_INT)
        EI_values.append(self.cgeneraldata.PE_INT)

        EI_labels = [_U('Fuels'),_U('Electricity'),_U('Total primary energy')]


#.........................................................................
#Part 2: SEC by product

        for row in self.qproduct:

            #calculate SEC for each product
            if (row.QProdYear > 0) and row.QProdYear is not None:    
                if row.FuelProd is not None: row.FUEL_SEC = (row.FuelProd)/row.QProdYear #converted to [kWh/pu]
                else: row.FUEL_SEC = 0
                if row.ElProd is not None: row.EL_SEC = (row.ElProd)/row.QProdYear #converted to [kWh/pu]
                else: row.EL_SEC = 0.
                if row.FuelProd is not None and row.ElProd is not None: row.PE_SEC = (1.1*row.FuelProd + 3.0*row.ElProd)/row.QProdYear #converted to [kWh/pu], fixed energy conv. coef. ->change this later
                else: row.PE_SEC = 0.

                Status.SQL.commit() #SD, check this

        SEC_values = []
        ProductNames = []
        for row in self.qproduct:#SD
            SECPerProduct = [unicode(row.Product,"utf-8")]
            SECPerProduct.append(row.FUEL_SEC)
            SECPerProduct.append(row.EL_SEC)
            SECPerProduct.append(row.PE_SEC)

            SEC_values.append(noneFilter(SECPerProduct))

#...............................................................................
#Part 3: SEC by unit operation
#XXX Still missing...

#...............................................................................

        #
        # upper grid: Energy intensity by type
        #

        TableColumnList1 = [EI_labels,noneFilter(EI_values)]

        matrix1 = transpose(TableColumnList1)
        data1 = array(matrix1)
                          
        Status.int.setGraphicsData(self.keys[0], data1)

        #
        # lower grid: Energy consumption by product
        #

        data2 = array(SEC_values)
                          
        Status.int.setGraphicsData(self.keys[1], data2)

#------------------------------------------------------------------------------

#==============================================================================
