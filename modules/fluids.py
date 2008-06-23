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
#	FLUIDS
#			
#------------------------------------------------------------------------------
#			
#	Access to fluid and fuel properties in the database
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	22/06/2008
#	Revised by:         
#
#       Changes in last update:
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

from einstein.modules.messageLogger import *

#------------------------------------------------------------------------------		
class Fluid():
#------------------------------------------------------------------------------		

    def __init__(self,fluidID):
        fluids = Status.DB.dbfluid.DBFluid_ID[fluidID]
        if len(fluids) > 0:
            self.rho = fluids[0].FluidDensity
            self.cp = fluids[0].FluidCp/3600.   #data in DB are in kJ/kgK ->
                                                #conversion to kWh/kgK
        else:
            self.rho = 1000.0                   #kg/m3
            self.cp  = 1.16/1000.0              #water properties in kWh/kgK
            logError(_("Fluid (init): cannot find fluid with ID = %s")%fluidID)
           
           
#------------------------------------------------------------------------------		
