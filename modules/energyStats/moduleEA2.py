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

class ModuleEA2(object):

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
        data = array([['Total Fuels'       ,660.0,  81.48, 583.0,  90.67],
                      ['Total Electricity' ,150.0,  18.52,  60.0,   9.33],
                      ['Total (F+E)'       ,810.0, 100.00, 643.0, 100.00]])

        self.interface.setGraphicsData(self.keys[0], data)

        #print "ModuleEA2 graphics data initialization"
        #print "Interfaces.GData[%s] contains:\n%s\n" % (self.keys[0],repr(Interfaces.GData[self.keys[0]))

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
