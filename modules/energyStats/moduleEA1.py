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
#	Version No.: 0.02
#	Created by: 	    Tom Sobota	   21/03/2008
#       Revised by:         Hans Schweiger 28/03/2008
#       Revised by:         Tom Sobota     28/03/2008
#
#       Changes to previous version:
#	28/03/08:   functions draw_ ... moved to panel
#	28/03/08:   TS changed functions draw... to use numpy arrays,
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
        data = array([['Heavy fuel oil' ,  0.0,   0.00,   0.0,   0.00],
                      ['Natural gas'    ,200.0,  30.77, 180.0,  32.73],
                      ['Gas oil'        ,100.0,  15.38,  50.0,   9.09],
                      ['LPG'            ,300.0,  46.15, 300.0,  54.55],
                      ['Other'          ,  0.0,   0.00,   0.0,   0.00],
                      ['Electricity'    , 50.0,   7.69,  20.0,   3.64],
                      ['Total'          ,650.0, 100.00, 550.0, 100.00]])
                          
        self.interface.setGraphicsData(self.keys[0], data)

        #print "ModuleEA1 graphics data initialization"
        #print "Interfaces.GData[%s] contains:\n%s\n" % (self.keys[0],repr(Interfaces.GData[self.keys[0]]))
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
