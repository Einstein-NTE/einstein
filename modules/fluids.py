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
from einstein.auxiliary.auxiliary import *

#------------------------------------------------------------------------------		
class Fluid():
#------------------------------------------------------------------------------		

    def __init__(self,fluidID):
        fluids = Status.DB.dbfluid.DBFluid_ID[fluidID]
        if len(fluids) > 0:
            self.cp = fluids[0].FluidCp
            self.rho = fluids[0].FluidDensity
            self.hL = fluids[0].LatentHeat
            self.TCond = fluids[0].TCond
            
            if self.cp is not None and self.cp > 0: self.cp = self.cp/3600.0
            else:
                logError(_("Severe error in your fluid data for fluid %s: cp  %s")%\
                           (fluids[0].FluidName,self.cp))
                self.cp = 1.16/1000.0
                
            
            if self.hL is not None: self.hL = self.hL/3600.0
                                                #data in DB are in kJ/kgK ->
                                                #conversion to kWh/kgK
            else: self.hL = 0.0 #if nothing is specified, 0 latent heat supposed

            if self.TCond is None:
                self.TCond = 1e+99 #if no condensing temperature is given, no phase change
                
            if self.rho is None or self.rho < 0 or self.rho > 1e+5:
                logError(_("Severe error in your fluid data for fluid %s: density %s")%\
                           (fluids[0].FluidName,self.rho))
                self.rho = 1000.0
            

            if self.cp is None or self.cp < 0 or self.cp > 5.0:
                logError(_("Severe error in your fluid data for fluid %s: cp %s")%\
                           (fluids[0].FluidName,self.cp))
                self.cp = 1.16/1000.0

            self.name = unicode(fluids[0].FluidName,"utf-8")

        else:
            self.rho = 1000.0                   #kg/m3
            self.cp  = 1.16/1000.0              #water properties in kWh/kgK
            self.hL  = 0.7
            self.TCond = 115.0 #
            self.name = "dummy fluid"
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
            self.HCV = fuel.FuelHCV
            self.PEConv = fuel.PEConvFuel
            self.CO2Conv = fuel.CO2ConvFuel
            self.rho = fuel.FuelDensity
            self.CombAir = fuel.CombAir
            self.OffgasHeatCapacity = fuel.OffgasHeatCapacity
            self.Offgas = fuel.Offgas
            self.OffgasDensity = fuel.OffgasDensity
            self.Humidity = fuel.Humidity
            
            self.name = unicode(fuel.FuelName,"utf-8")
            
            if self.LCV is None or \
               self.HCV is None or \
               self.PEConv is None or \
               self.CO2Conv is None or \
               self.CombAir is None or \
               self.OffgasHeatCapacity is None:

                logError(_("Severe error in your fuel data for fuel %s: some parameters are missing")%\
                           (fuels[0].FuelName))
                                                #conversion to kWh/kgK
            self.OffgasHeatCapacity = noneFilterNumber(self.OffgasHeatCapacity)/3600.

            if self.rho is None or self.rho <= 0.0:
                logError(_("Severe error in your fuel data for fuel %s: erroneous value for density = %s")%\
                           (fuels[0].FuelName,self.rho))
                self.rho = 1.0

            if self.Offgas is None:
                logDebug("Missing fuel parameter OffGas in fuel %s. Default assumed"%self.name)
                self.Offgas = 17.6
            if self.CombAir is None:
                logDebug("Missing fuel parameter CombAir in fuel %s. Default assumed"%self.name)
                self.CombAir = 16.6
            if self.Humidity is None:
                logDebug("Missing fuel parameter Humidity in fuel %s. Default assumed"%self.name)
                self.Humidity = 0.12
            if self.OffgasDensity is None:
                logDebug("Missing fuel parameter OffgasDensity in fuel %s. Default assumed"%self.name)
                self.OffgasDensity = 1.23
            
        else:
            self.LCV = 10.0
            self.HCV = 11.0
            self.PEConv = 1.1
            self.CO2Conv = 0.20
            self.rho = 10.0
            self.CombAir = 16.6     #approximate values of natural gas as default
            self.OffgasHeatCapacity = 1.13/3600.0
            self.Offgas = 17.6
            self.CombAir = 16.6
            self.OffgasDensity = 1.23
            self.Humidity = 0.12
            self.name = u"dummy fuel"
            logError(_("Fluid (init): cannot find fuel with ID = %s")%fuelID)
           
           
#------------------------------------------------------------------------------		
