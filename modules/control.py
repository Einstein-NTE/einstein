# -*- coding: cp1252 -*-
#============================================================================== 				
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	CONTROL
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Auxiliary functions for the control of execution of the tool
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	    18/06/2008
#
#       Last modified by:   
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
from einstein.GUI.status import *

#------------------------------------------------------------------------------		
def prepareDataForReport():
#------------------------------------------------------------------------------		
#   calls the functions necessary for writing the report
#------------------------------------------------------------------------------		

    Status.mod.moduleEA.update()
    print "Control (prepareData): here I should do something more ..."

#============================================================================== 
