# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleHC (Heat and Cold Supply)
#			
#------------------------------------------------------------------------------
#			
#	Module for design of HC Supply cascade
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	03/04/2008
#	Last revised by:    
#
#       Changes to previous version:
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
import einstein.modules.matPanel as mP

class ModuleHC(object):

    HCList = []
    
    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel
        self.interface = Interfaces()

        self.DB = Status.DB
        self.sql = Status.SQL
        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        self.equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
        self.equipmentsC = self.DB.cgenerationhc.sql_select(sqlQuery)
        self.NEquipe = len(self.equipments)
        print "ModuleHC (__init__): %s equipes found"%self.NEquipe


#............................................................................................
#XXXHS2008-03-22: here for testing purposes.
#   -> initPanel should be activated by event handler on entry into panel

        self.initPanel()
        self.updatePanel()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

        HCList = self.screenEquipments()
        
#............................................................................................
#XXX FOR TESTING PURPOSES ONLY: load default demand
# here it should be assured that heat demand and availability for position in cascade
# of presently existing heat pumps is already defined

        self.interface.initCascadeArrays(self.NEquipe)
       
#............................................................................................
#returns HPList to the GUI for displaying in window
        
        return (HCList)
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def screenEquipments(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

        self.interface.getEquipmentCascade()
        self.cascadeIndex = 0
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------

        print "ModuleHC (updatePanel): data for panel are copied to interface"
        
        # plot to be displayed
	# this is how the data should be set up
	# (this data are just an example!)
        data = array([['HC 1', 2004, 'Type 1', 3000, 100, 120],
		      ['HC 2', 2006, 'Type 1', 4500, 120, 140],
                      ['HC 3', 2007, 'Type 2', 5000,  80, 130]])


        self.interface.setGraphicsData(self.keys[0], data)

        try:
	    #    self.interface.setGraphicsData('BB Plot',[self.interface.T,
	    #                                              self.interface.QD_T_mod[self.cascadeIndex],
	    #                                              self.interface.QA_T_mod[self.cascadeIndex],
	    #                                              self.interface.QD_T_mod[self.cascadeIndex+1],
	    #                                              self.interface.QA_T_mod[self.cascadeIndex+1]])
	    # info for text boxes in right side of panel
	    self.interface.setGraphicsData('HC Info',{"noseque":55})

            # list of equipments in cascade for Table
            self.interface.setGraphicsData('HC List',self.interface.cascade)
        except:
            pass

#------------------------------------------------------------------------------

    def exitModule(self,exit_option):
        """
        carries out any calculations necessary previous to displaying the HP
        design assitant window
        """
        if exit_option == "save":
            print "exitModule: here I should save the current configuration"
        elif exit_option == "cancel":
            print "exitModule: here I should retreive the previous configuration"
            

        print "exitModule: function not yet defined"

        return "ok"

#==============================================================================

if __name__ == "__main__":
    pass
