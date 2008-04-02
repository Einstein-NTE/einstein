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
#
#       Changes to previous version:
#	28/03/08:   functions draw_ ... moved to panel
#	28/03/08:   changed functions draw... to use numpy arrays,
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
        self.keys = keys
        self.interface = Interfaces()
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------
        # generate data for graphics

        data = array([['Heavy fuel oil',   0.0,    0.00],
                      ['Natural gas'   ,  50.0,   28.17],
                      ['Gas oil'       ,  25.0,   14.08],
                      ['LPG'           ,  75.0,   42.25],
                      ['Other'         ,   0.0,    0.00],
                      ['Electricity'   ,  27.5,   15.49],
                      ['Total'         , 177.5,  100.00]])

        self.interface.setGraphicsData(self.keys[0], data)

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
