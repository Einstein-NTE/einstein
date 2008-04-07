#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA2- Final energy by fuels- Yearly data
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
#       07/04/2008           Adapted to use data from sql, not checked     
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

class ModuleEA2(object):

    def __init__(self, keys):
        self.keys = keys
        self.interface = Interfaces()
#...............................................................
        PId = Status.PId
        ANo = Status.ANo

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(PId,ANo)
        self.cgeneraldata = Status.DB.cgeneraldata.sql_select(sqlQuery)[0]
#................................................................
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------

        PEC = [self.cgeneraldata.PECFuels, self.cgeneraldata.PECElect]
        PECTotal = self.cgeneraldata.PECFuels + self.cgeneraldata.PECElect
        PECPercentage = [PEC[0]*100.0/PECTotal, PEC[1]*100.0/PECTotal]

        PET = [self.cgeneraldata.PETFuels, self.cgeneraldata.PETElect]
        PETTotal = self.cgeneraldata.PETFuels + self.cgeneraldata.PETElect
        PETPercentage = [PET[0]*100.0/PETTotal, PET[1]*100.0/PETTotal]

#..............................................................
        #finish the table columns, add total, percentage
        Labels = ['Total fuels','Total electricity','Total (fuels + electricity)']
        PEC.append(PECTotal)
        PET.append(PETTotal)

        suma = 0
        for i in PECPercentage:
            suma += i
        PECPercentage.append(suma)

        suma = 0
        for i in PETPercentage:
            suma += i
        PETPercentage.append(suma)
      
#.................................................................

        TableColumnList = [Labels,PEC,PECPercentage,PET,PETPercentage]

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
