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
#	Version No.: 0.03
#	Created by: 	    Hans Schweiger	03/04/2008
#	Last revised by:    Hans Schweiger      18/04/2008
#                           Hans Schweiger      01/07/2008
#
#       Changes to previous version:
#       18/04/2008 HS   Reference to Status.int
#       01/07/2008: HS  Clean-up; call to updatePanel eliminated in init and
#                       initPanel
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

from numpy import *
from einstein.GUI.status import *

class ModuleA(object):

#------------------------------------------------------------------------------
    def __init__(self, keys):
#------------------------------------------------------------------------------
        self.keys = keys # the key to the data is sent by the panel        

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       functions that have to be called when panel is created
#------------------------------------------------------------------------------

        pass
    
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
#==============================================================================

if __name__ == "__main__":
    pass
