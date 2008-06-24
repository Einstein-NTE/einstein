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
#	MONDAY
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Example how to apply the solar calculation in
#       CalculateEnergyFlows
#
#       Copy the functions into the ModuleST
#
#       ***GETTING_STARTED***: -> comments for getting started.
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	   Hans Schweiger 	17/06/2008
#	Last revised by:   
#            
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
from sunday import *

NtStart = 4800
Nt = 24
TIMESTEP = 1.0
HOUR = 3600.

sunOnH = Intensity()
sunOnT = Intensity()
sunAnglesOnSurface = Angles()
dirSunOnT = [0.0,0.0,0.0]

#------------------------------------------------------------------------------		
def getDailyRadiation(I,day):
#------------------------------------------------------------------------------		
#   Calculates some (more or less) "reasonable" distribution of yearly solar
#   radiation
#   very very basic and only reasonable for European latitudes !!!
#------------------------------------------------------------------------------		

#       ***GETTING_STARTED***:
#   The SUNDAY functions are written radically in SI-units, this is J, W, s; no
#   hours, no kilos, no Megas ... !!!! => unit conversion from EINSTEIN-units
#   to Sunday (SI-) units is necessary

    kWh_to_J = 3.6e+6
    Hmean = I/365*kWh_to_J
    H = Hmean * (1 - 0.5*cos(2.0*math.pi*(day+10)/365))
    print "daily radiation = ",H
    return H
                 
#------------------------------------------------------------------------------		
def collectorEfficiency(GT,dT):
#------------------------------------------------------------------------------		
#   Calculates the collector efficiency at a given working point
#   GT: Solar radiation on tilted surface (SI - units: W/m2)
#   c1/c2 are in W/m2K, W/m2K2 !!!
#------------------------------------------------------------------------------		

#       ***GETTING_STARTED***:
#   Later on the incidence angle modifier and decomposition into direct
#   and diffuse radiation could be added
#   The necessary input values GbT, GdT and cos(theta) are already available
#   from the function SUN_HOURLY 

    if GT <= 0:
        return 0.0
    else:
        c0 = 0.80 # Collector parameters from the DB: As default STARTING value choose always:LowTempCollType=FPEinstein
        c1 = 3.50
        c2 = 0.010
        return c0 + (c1 + c2*dT)*dT/(GT)
                 
#------------------------------------------------------------------------------		
def calculateEnergyFlows():
#------------------------------------------------------------------------------		
#   Basic example of how the calculateEnergyFlows-function in ModuleST
#   could look like
#------------------------------------------------------------------------------		

#       ***GETTING_STARTED***:
#   Nt and TIMESTEP in ModuleST should be imported from Status !!!

    global Nt
    global TIMESTEP

#       ***GETTING_STARTED***:
#   This are the required input data for the calculation of the radiation
#   on tilted surface. are used as input values in the function prep_sun

    Latitude = 41.4
    Inclination = 30
    Azimuth = 15.0
    I = 1750.0    #yearly radiation in kWh/m2a

#       ***GETTING_STARTED***:
#   The area should be imported from the QGenerationHC equipment parameters
#   A solar system should be entered like any other heat supply equipment
#   into the QGenerationHC - Table. We should think about how to match the
#   parameters there with characteristic solar parameters
#   e.g. PNom for solar systems = the nominal solar system power
#   -> SurfaceAreaSol = PNom / 0.7

    SurfAreaSol = 100.0
    
    systemEfficiency = 0.90         #accounting for all the thermal losses in the solar system
                                    #including pipe and tank losses
    
#       ***GETTING_STARTED***:
#   These are the parameters for storage modelling:

    TStorage = 20.0                 #initial temperature of the storage at 1st of January 0:00
    TStorageMax = 250.0             #maximum allowed temperature in the storage
    storageVolume = 0.05*area       #in m3. for the moment fixed to 50 l/m2. can be an equipment parameter
    CStorage = 1.16*storageVolume   #heat capacity of the storage in kW/K
    QStorage = CStorage*TStorage    #total heat stored in the tank (reference temperature = 0ºC)
    QStorageMax = CStorage*TStorageMax #maximum amount of heat that can be stored in the tank (ref. = 0ºC)
                 

    QavColl = 0    #these two values only for calculating the weighted mean of the average collector
    QTavColl = 0    #temperature during the year

    oldDay = 0
    for it in range(NtStart,NtStart+Nt):
        time_in_h = it * TIMESTEP
        time_in_s = time_in_h * HOUR
        nday = int(ceil(time_in_h/24.0))

        print "DAY: %s Hour: %s Sec: %s"%(nday,time_in_h,time_in_s)

#.............................................................................
# recalculate solar data for a new day

#       ***GETTING_STARTED***:
#   The function PREP_SUN prepares the radiation calculations for a given day
#   in the year

        if nday > oldDay:
            oldDay = nday
            sunOnH.t = getDailyRadiation(I,nday)
            prep_sun(latitud,inclinacion,azimuth,nday,sunAnglesOnSurface,sunOnH)

#.............................................................................
# now get instantaneous radiation (in W/m2)

        sun_hourly(sunAnglesOnSurface,sunOnH,time_in_s,sunOnT,dirSunOnT)
        GbT = sunOnT.b / 1000.    #conversion to kW/m2
        GdT = sunOnT.d / 1000.
        GT = sunOnT.t / 1000.

#.............................................................................
# calculate maximum solar system output, heat demand and storage capacity

#       ***GETTING_STARTED***:
#   The working temperature of the solar system is the temperature
#   of the storage tank at the beginning of the time-step plus a Delta_T
#   accounting for the heat exchanger in the primary loop

        deltaT_primary = 7.0
        TStorage = QStorage/CStorage
        TavCollector = TStorage + deltaT_primary    #=working temperature of the collector in the present time step
        TEnv = 20.0
        DeltaT = TavCollector - TEnv
                 
        dotQuSolarMax = collectorEfficiency(sunOnT.t,DeltaT)*systemEfficiency*SurfAreaSol*GT #if shaded then add shading factor.ADD an IF!
                                #maximum instantaneous power the solar system may deliver

#       ***GETTING_STARTED***:
#   general Note: I used the "dot" to distinguish between power and energy.
#   we could adapt the calculations using the energy-fraction in time interval: dQ = dotQ*TIMESTEP
#   as is used in the EINSTEIN - arrays ...
#   dotQDemand should be set to the heat demand below TStorage (dotQDemand * TIMESTEP = QD_Tt[TStorage])

        dotQDemand = 9999.

#       ***GETTING_STARTED***:
#   the minimum temperature of demand indicates to what temperature the storage can be cooled down.
#   if we have heat demand only above e.g. 60ºC, we cannot cool down the storage lower than this,
#   as heat can not be transferred from cold to hot (at least not yet, maybe EINSTEIN succeeds to do it)
        
        TMinDemand = 50.0

        QStorageCapacity = QStorageMax - QStorage   #maximum amount of heat that still can be fed into the storage
        dotQuSolar = min(dotQDemand+QStorageCapacity/TIMESTEP,dotQuSolarMax)
                                                    #solar production constrained by demand + remaining storage capacity

        QStorageMin = CStorage*TMinDemand           #minimum heat that has to remain within the storage, as it can't be cooled down further
        dotQuSupply = min(dotQDemand,dotQuSolar + max((QStorage - QStorageMin)/TIMESTEP,0))
                                                    #supply constrained by solar production + available heat stored at T > TMinDemand

        USHj = dotQuSupply*TIMESTEP

#       ***GETTING_STARTED***:
#   note: the remaining problem is to decide at WHAT temperature the solar system does supply heat (from USHj_t to USHj_Tt)
#   -> let's use the simplest possible solution (although it's not the most efficient one ...):
#   fill up the demand from below (-> see heat pump example, I think there the same strategy
#   is applied. you can copy ...

        for iT in range(NT+2):
            USHj_Tt[iT][it] = min(USHj,QD_Tt[iT][it])

# now update heat stored in tank
        QStorage += (dotQuSolar - dotQuSupply)*TIMESTEP

        print "----------------------------------------------"
        print "GT %10.4f dotQuSolar %10.4f"%(GT,dotQuSolar)

        QavColl += dotQuSolar
        QTavColl += dotQuSolar*TavCollector

#.............................................................................
# end of the year reached. now some final calculations

    TavCollMean = QTavColl/max(QavColl,0.000000001)


    
    
#*======================================================================*/

if __name__ == "__main__":

    calculateEnergyFlows()
