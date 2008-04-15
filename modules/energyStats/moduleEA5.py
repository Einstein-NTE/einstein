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
#
#       Changes to previous version:
#	28/03/08:   TS changed functions draw... to use numpy arrays,
#       07/04/08:   SD, adapted to use data from sql, not checked
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

class ModuleEA5(object):

    def __init__(self, keys):
        print "ModuleEA5(__init__)"
        self.keys = keys
        self.interface = Interfaces()
#...................................................................
        PId = Status.PId
        ANo = Status.ANo

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(PId,ANo)
        self.cgeneraldata = Status.DB.cgeneraldata.sql_select(sqlQuery)[0]
        self.questionnaire = Status.DB.questionnaire.Questionnaire_ID[PId][0]
        self.cproduct = Status.DB.cproduct.sql_select(sqlQuery)
        self.qproduct = Status.DB.qproduct.sql_select(sqlQuery)
#....................................................................
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------

#Part 1: Energy Intensity

        TotalFEC = self.cgeneraldata.FEC   #FEC in [MWh]
        ElectFEC = self.cgeneraldata.FECel
        FuelsFEC = TotalFEC - ElectFEC
        PE_FEC = 1.1*FuelsFEC + 3.0*ElectFEC #substitute later the conv. coef. from SetUp #pending put conv. coef. in status.py
            
        Turnover = self.questionnaire.Turnover #in [million euros]

        if (Turnover > 0) and not (Turnover==None):    
            self.cgeneraldata.FUEL_INT = (FuelsFEC)/(Turnover*1000) #converted to [kWh/euro]
            self.cgeneraldata.EL_INT = (ElectFEC)/(Turnover*1000) #converted to [kWh/euro]
            self.cgeneraldata.PE_INT = (PE_FEC)/(Turnover*1000) #converted to [kWh/euro]
        else:
            self.cgeneraldata.FUEL_INT = None
            self.cgeneraldata.EL_INT = None
            self.cgeneraldata.PE_INT = None

# back-up in SQL                                      
        Status.SQL.commit() #SD, to be checked


        EI_values = []
        EI_values.append(self.cgeneraldata.FUEL_INT)
        EI_values.append(self.cgeneraldata.EL_INT)
        EI_values.append(self.cgeneraldata.PE_INT)

        EI_labels = ['Fuels','Electricity','Total primary energy']


#.........................................................................
#Part 2: SEC by product

        for row in self.qproduct:

            #calculate SEC for each product
            FUEL_SEC = (row.FuelProd)*1000/row.QProdYear #converted to [kWh/pu]
            EL_SEC = (row.ElProd)*1000/row.QProdYear #converted to [kWh/pu]
            PE_SEC = (1.1*row.FuelProd + 3.0*row.ElProd)*1000/row.QProdYear #converted to [kWh/pu], fixed energy conv. coef. ->change this later

            #this selects the corresponding row in CProduct in a shorter variable name
            rowCProd = Status.DB.cproduct.QProduct_id[row.QProduct_ID][0]
            #now write the SEC values in the CProduct table
            rowCProd.FUEL_SEC = FUEL_SEC
            rowCProd.EL_SEC = EL_SEC
            rowCProd.PE_SEC = PE_SEC
            Status.SQL.commit() #SD, check this

        SEC_values = []
        ProductNames = []
        for row in self.cproduct:
            SECPerProduct = []
            SECPerProduct.append(row.FUEL_SEC)
            SECPerProduct.append(row.EL_SEC)
            SECPerProduct.append(row.PE_SEC)
            SEC_values.append(SECPerProduct)
            Product = Status.DB.qproduct.QProduct_ID[row.QProduct_id][0].Product
            ProductNames.append(Product)

##        print 'SEC_values=',SEC_values
##        print 'ProductNames =', ProductNames


#...............................................................................
#Part 3: SEC by unit operation
#XXX Still missing...

#...............................................................................

        #
        # upper grid: Energy intensity by type
        #

        TableColumnList1 = [EI_labels,EI_values]

        matrix1 = transpose(TableColumnList1)

        data1 = array(matrix1)

        dummydata1 = array([['Fuels',                1.91],
                      ['Electricity',          0.18],
                      ['Total primary energy', 2.65]])
                          
        self.interface.setGraphicsData(self.keys[0], dummydata1)

        #
        # lower grid: Energy consumption by product
        #

        SEC_values.insert(0,ProductNames) #add ProductNames as a first in the list
        
        TableColumnList2 = SEC_values

        matrix2 = transpose(TableColumnList2)

        data2 = array(matrix2)            

        dummydata2 = array([['Product 1', 500.0, 50.0, 700.0],
                      ['Product 2', 400.0, 80.0, 680.0],
                      ['Product 3', 100.0, 10.0, 140.0]])
                          
        self.interface.setGraphicsData(self.keys[1], dummydata2)

        #print "ModuleEA5 graphics data initialization"
        #print "Interfaces.GData[%s] contains:\n%s\n" % (self.keys[0], repr(Interfaces.GData[self.keys[0]]))
        #print "Interfaces.GData[%s] contains:\n%s\n" % (self.keys[1], repr(Interfaces.GData[self.keys[1]]))

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
