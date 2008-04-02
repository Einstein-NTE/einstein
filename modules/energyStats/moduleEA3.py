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
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	21/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#
#       Changes to previous version:
#       29/3/2008          Adapted to numpy arrays
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
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------
        #
        # upper grid FET by equipment
        #
        data = array([['Equipname 1', 'Natural gas',  90.0,   16.36],
                      ['Equipname 2', 'Natural gas',  90.0,   16.36],
                      ['Equipname 3', 'Gas oil'    ,  50.0,  9.09],
                      ['Equipname 4', 'LPG'        , 150.0, 27.27],
                      ['Equipname 5', 'LPG'        , 150.0, 27.27],
                      ['Equipname 6', 'Electricity',  20.0,  3.64],
                      ['Total'      , ''           , 550.0, 100.00]])
                          
        self.interface.setGraphicsData(self.keys[0], data)
        #
        # lower grid USH by equipment
        #
        data = array([['Equipname 1',  76.5,  16.29],
                      ['Equipname 2',  76.5,  16.29],
                      ['Equipname 3',  42.5,   9.05],
                      ['Equipname 4', 127.5,  27.16],
                      ['Equipname 5', 127.5,  27.16],
                      ['Equipname 6',  19.0 ,  4.05],
                      ['Total'      , 469.5, 100.00]])

        self.interface.setGraphicsData(self.keys[1], data)

        #print "ModuleEA3 graphics data initialization"
        #print "Interfaces.GData[%s] contains:\n%s\n" % (self.keys[0], repr(Interfaces.GData[self.keys[0]]),)
        #print "Interfaces.GData[%s] contains:\n%s\n" % (self.keys[1], repr(Interfaces.GData[self.keys[1]]),)

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
