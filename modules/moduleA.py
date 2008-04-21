# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleA (Design of alternatives)
#			
#------------------------------------------------------------------------------
#			
#	
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Hans Schweiger	03/04/2008
#	Last revised by:    Hans Schweiger      18/04/2008  
#
#       Changes to previous version:
#       18/04/2008 HS   Reference to Status.int
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

class ModuleA(object):

    AList = []
    
    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel
        self.DB = Status.DB
        self.sql = Status.SQL
        
        self.updatePanel()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

        self.updatePanel()
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------

        alternativeList = Status.prj.getAlternativeList()            
        data = array(alternativeList)
        Status.int.setGraphicsData(self.keys[0], data)

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
