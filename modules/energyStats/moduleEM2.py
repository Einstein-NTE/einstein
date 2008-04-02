#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEM2- Heat supply - Monthly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	28/03/2008
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
import wx

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP


class ModuleEM2(object):

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
        # In this grid the nr. of cols is variable, so we generate the
        # column headings dynamically here
        data = array([['Process heat\nsupply','Boiler 1\nMWh','Boiler 2\nMWh',
                       'CHP engine 1\nMWh','TOTAL\nKWh'],
                      ['January'  ,  10.0,  14.0,   30.0,   54.0],
                      ['February' ,  12.0,  16.0,   20.0,   48.0],
                      ['March'    ,  14.0,  18.0,   10.0,   42.0],
                      ['April'    ,  16.0,  20.0,    5.0,   41.0],
                      ['May'      ,  19.0,  23.0,    0.0,   42.0],
                      ['June'     ,   6.0,  10.0,    0.0,   16.0],
                      ['July'     ,   4.0,   8.0,    0.0,   12.0],
                      ['August'   ,   2.0,   6.0,    0.0,    8.0],
                      ['September',   7.0,  11.0,    0.0,   18.0],
                      ['October'  ,   9.0,  13.0,    10.0,  32.0],
                      ['November' ,  15.0,  19.0,    20.0,  54.0],
                      ['December' ,   4.0,   8.0,    30.0,  42.0],
                      ['Total'    ,  47.0,  75.0,    60.0, 182.0]])
                          
        self.interface.setGraphicsData(self.keys[0], data)

        #print "ModuleEM2 graphics data initialization"
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
