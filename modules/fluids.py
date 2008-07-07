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
            self.cp = fluids[0].FluidCp
            if self.cp is not None: self.cp = self.cp/3600.0
                                                #data in DB are in kJ/kgK ->
                                                #conversion to kWh/kgK

            if self.rho is None or self.rho < 0 or self.rho > 1e+5:
                logError(_("Severe error in your fluid data for fluid %s: density %s")%\
                           (fluids[0].FluidName,self.rho))
                self.rho = 1000.0
            

            if self.cp is None or self.cp < 0 or self.cp > 5.0:
                logError(_("Severe error in your fluid data for fluid %s: cp %s")%\
                           (fluids[0].FluidName,self.cp))
                self.cp = 1.16/1000.0
        else:
            self.rho = 1000.0                   #kg/m3
            self.cp  = 1.16/1000.0              #water properties in kWh/kgK
            logError(_("Fluid (init): cannot find fluid with ID = %s")%fluidID)
           
           
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
class Fuel():
#------------------------------------------------------------------------------		

    def __init__(self,fuelID):
        fuels = Status.DB.dbfuel.DBFuel_ID[fuelID]
        if len(fuels) > 0:
            fuel = fuels[0]
            self.LCV = fuel.FuelLCV
            self.HCV = fuel.FuelHCV  #data in DB are in kJ/kgK ->
            self.PEConv = fuel.PEConvFuel
            self.CO2Conv = fuel.CO2ConvFuel
            self.rho = fuel.FuelDensity
                                                #conversion to kWh/kgK
        else:
            self.LCV = 10.0
            self.HCV = 11.0
            self.PEConv = 1.1
            self.CO2Conv = 0.20
            self.rho = 10.0
            logError(_("Fluid (init): cannot find fuel with ID = %s")%fuelID)
           
           
#------------------------------------------------------------------------------		
