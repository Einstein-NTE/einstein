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
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	22/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#
#       Changes to previous version:
#	28/03/08:   TS changed functions draw... to use numpy arrays,
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
        self.keys = keys
        self.interface = Interfaces()
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------
        #
        # upper grid: Energy intensity by type
        #
        data = array([['Fuels',                1.91],
                      ['Electricity',          0.18],
                      ['Total primary energy', 2.65]])
                          
        self.interface.setGraphicsData(self.keys[0], data)

        #
        # lower grid: Energy consumption by product
        #
        data = array([['Product 1', 500.0, 50.0, 700.0],
                      ['Product 2', 400.0, 80.0, 680.0],
                      ['Product 3', 100.0, 10.0, 140.0]])
                          
        self.interface.setGraphicsData(self.keys[1], data)

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
