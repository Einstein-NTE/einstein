# -*- coding: iso-8859-15 -*-
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	UNITS: dictionaries and functions for unit conversion
#
#==============================================================================
#
#	Version No.: 0.07
#	Created by: 	    Stoyan Danov    03/06/2008
#
#       Revised by:         Stoyan Danov    10/06/2008
#                           Stoyan Danov    11/06/2008
#                           Hans Schweiger  11/06/2008
#                           Stoyan Danov    12/06/2008
#                           Hans Schweiger  01/09/2008
#                           Hans Schweiger  14/10/2008
#
#       Changes to previous version:
#       SD: 10/06/2008: added FUELPRICELCV, PRICE
#       SD: 11/06/2008: mergeDict() added
#       HS: 11/06/2008: corrections of bugs: MJ/GJ, comma by dot, ...
#                       new structure of dictionaries
#       SD: 12/06/2008: completing the new structure: MASSFLOW,PRESSURE,SPECIFICENTHALPY,
#                       VOLUMEFLOW,TIME,
#       HS: 01/09/2008: bug-fix in SPECIFICENTHALPY and SPECIFICHEAT
#       HS: 14/10/2008: conversion from mass to volume brought to work
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

from einstein.modules.fluids import Fluid
from einstein.modules.fluids import Fuel
from einstein.modules.messageLogger import *

CURRENCY = 'EUR'

UNITSDENSITY = 1000.0

def setUnitsFluidDensity(fluidID):
    global UNITSDENSITY

    fluid = Fluid(fluidID)
    UNITSDENSITY = fluid.rho
    changeMassOrVolumeUnits()

def setUnitsFuelDensity(fuelID):
    global UNITSDENSITY

    fuel = Fuel(fuelID)
    UNITSDENSITY = fuel.rho
    changeMassOrVolumeUnits()


def changeMassOrVolumeUnits():
    global UNITSDENSITY

    if UNITSDENSITY <= 0 or UNITSDENSITY == None:   #security feature
        logDebug("Units: UNITSDENSITY undefined or zero [%s]"%UNITSDENSITY)
        UNITSDENSITY = 1000.0   
    
    UNITS["MASSORVOLUME"] = {
        'kg' : (1.0,0.0),
        'lb' : (0.45359,0.0),
        't' : (1000.0,0.0),
        'm3' : (1.0*UNITSDENSITY,0.0),
        'l' : (1.0e-3*UNITSDENSITY,0.0),
        'ft3' : (0.028317*UNITSDENSITY,0.0),
        'U.S. gal' : (0.003785*UNITSDENSITY,0.0),
        'Brit. gal' : (0.004546*UNITSDENSITY,0.0),
        'barrel (U.S. pet.)' : (0.15898*UNITSDENSITY,0.0)
        }

    UNITS['MASSORVOLUMEFLOW'] = {
        'kg/h' : (1.0,0.0),
        'kg/s' : (3600.0,0.0),
        'lb/h' : (0.45359,0.0),
        'lb/s' : (1632.924,0.0),
        'm3/h' : (1.0*UNITSDENSITY,0.0),
        'm3/s' : (3600.0*UNITSDENSITY,0.0)
        }

    UNITS['VOLUMEORMASS'] = {
        'kg' : (1.0/UNITSDENSITY,0.0),
        'lb' : (0.45359/UNITSDENSITY,0.0),
        't' : (1000.0/UNITSDENSITY,0.0),
        'm3' : (1.0,0.0),
        'l' : (1.0e-3,0.0),
        'ft3' : (0.028317,0.0),
        'U.S. gal' : (0.003785,0.0),
        'Brit. gal' : (0.004546,0.0),
        'barrel (U.S. pet.)' : (0.15898,0.0)
        }


UNITS = {
# conversion to internal unit: [ºC]
    'TEMPERATURE' : {
        'ºC':   (1.0,   0.0),
        'ºF':   (5.0/9, -32.0*5/9),
        'K':    (1.0,   -273.15)
        },

# conversion to internal unit: [K]
    'TEMPERATUREDIFF' : {
        'K':    (1.0,   0.0),
        'ºF':   (5.0/9, 0.0),
        },

# conversion to internal unit: [h]
    'TIME' : {
        'h' : (1.0,0.0),
        'min' : (1.0/60,0.0),
        's' : (1.0/3600,0.0)
        },

# conversion to internal unit: [a]
    'LONGTIME' : {
        'a' : (1.0,0.0),
        },

# conversion to internal unit: [m]
    'LENGTH' : {
        'm' :       (1.0,       0.0),
        'km' :      (1000.0,    0.0),
        'mm' :      (1.0e-3,    0.0),
        'yards':    (0.9144,    0.0),
        'ft'   :    (0.3048,    0.0),
        'in'   :    (0.0254,    0.0)
        },
    

#### to be continued ...

# conversion to internal unit: [bar]
    'PRESSURE' : {
        'bar' : (1.0,0.0),
        'atm' : (1.01325,0.0),
        'mm Hg' : (0.001333224,0.0),
        'Pa' : (1.0e-5,0.0),
        'kPa' : (1.0e-2,0.0),
        'MPa' : (10.0,0.0)
        },
    
# conversion to internal unit: [m2]
    'AREA': {
        'm2' : (1.0,0.0),
        'ft2' : (0.3048*0.3048,0.0),
        'ha' : (1.0e4,0.0),
        },

# conversion to internal unit: [m3]
    'VOLUME': {
        'm3' : (1.0,0.0),
        'l' : (1.0e-3,0.0),
        'ft3' : (0.028317,0.0),
        'U.S. gal' : (0.003785,0.0),
        'Brit. gal' : (0.004546,0.0),
        'barrel (U.S. pet.)' : (0.15898,0.0)
        },

# conversion to internal unit: [m3/h]
    'VOLUMEFLOW' : {
        'm3/h' : (1.0,0.0),
        'm3/s' : (3600.0,0.0)
        },

# conversion to internal unit: [kg]
    'MASS': {
        'kg' : (1.0,0.0),
        'lb' : (0.45359,0.0),
        't' : (1000.0,0.0)
        },

# conversion to internal unit: [kg/h]
    'MASSFLOW': {
        'kg/h' : (1.0,0.0),
        'kg/s' : (3600.0,0.0),
        'lb/h' : (0.45359,0.0),
        'lb/s' : (1632.924,0.0)
        },

# conversion to internal unit: [kg or m3]
    'MASSORVOLUME': {
        'kg' : (1.0,0.0),
        'lb' : (0.45359,0.0),
        't' : (1000.0,0.0),
        'm3' : (1.0*UNITSDENSITY,0.0),
        'l' : (1.0e-3*UNITSDENSITY,0.0),
        'ft3' : (0.028317*UNITSDENSITY,0.0),
        'U.S. gal' : (0.003785*UNITSDENSITY,0.0),
        'Brit. gal' : (0.004546*UNITSDENSITY,0.0),
        'barrel (U.S. pet.)' : (0.15898*UNITSDENSITY,0.0)
        },

# conversion to internal unit: [kg/h]
    'MASSORVOLUMEFLOW': {
        'kg/h' : (1.0,0.0),
        'kg/s' : (3600.0,0.0),
        'lb/h' : (0.45359,0.0),
        'lb/s' : (1632.924,0.0),
        'm3/h' : (1.0*UNITSDENSITY,0.0),
        'm3/s' : (3600.0*UNITSDENSITY,0.0)
        },

# conversion to internal unit: [kg or m3]
    'VOLUMEORMASS': {
        'kg' : (1.0/UNITSDENSITY,0.0),
        'lb' : (0.45359/UNITSDENSITY,0.0),
        't' : (1000.0/UNITSDENSITY,0.0),
        'm3' : (1.0,0.0),
        'l' : (1.0e-3,0.0),
        'ft3' : (0.028317,0.0),
        'U.S. gal' : (0.003785,0.0),
        'Brit. gal' : (0.004546,0.0),
        'barrel (U.S. pet.)' : (0.15898,0.0)
        },

# conversion to internal unit: [kWh]
    'ENERGY': {
        'kWh' : (1.0,0.0),
        'MWh' : (1.0e+3,0.0),
        'GWh' : (1.0e+6,0.0),
        'kJ': (1.0/3600,0.0),
        'MJ': (1.0/3.6,0.0),
        'GJ': (1.0e6/3600,0.0),
        'kcal': (1.163/1000,0.0),
        'btu': (0.0002930711,0.0)
        },

# conversion to internal unit: [kWh]
    'ENERGYFLOW': {
        'kWh/m2a' : (1.0,0.0),
        'MJ/m2a': (1.0/3.6,0.0),
        'btu/h.ft2a': (0.0002930711/(0.3048*0.3048),0.0)
        },

# conversion to internal unit: [kW]
    'POWER' : {
        'kW' : (1.0,0.0),
        'MW' : (1.0e3,0.0),
        'GW' : (1.0e6,0.0),
        'W' : (1.0e-3,0.0),
        'kcal/h' : (1.163e-3,0.0),
        'btu/h' : (0.0002930711,0.0)
        },

# conversion to internal unit: [kWh/kg]
    'SPECIFICENTHALPY' : {
        'kWh/kg' : (1.0,0.0),
        'kJ/kg' : (1.0/3600,0.0),
        'kcal/kg' : (1.163e-3,0.0),
        'btu/lb' : (0.0002930711/0.45359,0.0)
        },

# conversion to internal unit: [kWh/kgK]
    'SPECIFICHEAT' : {
        'kWh/kgK' : (1.0,0.0),
        'kJ/kgK' : (1.0/3600.0,0.0),
        'kcal/kgK' : (1.163e-3,0.0),
        'btu/lbºF' : (((0.0002930711*9)/(0.45359*5)),0.0)
        },

# conversion to internal unit: [kW/K]
    'HEATTRANSFERCOEF' : {
        'kW/K' : (1.0,0.0),
        'W/K' : (1.0e-3,0.0),
        'btu/hºF' : ((0.0002930711*9)/5,0.0)
        },

# conversion to internal unit: [-]
    'ANGLE' : {
        'º' : (1.0,0.0),
        'rad' : (0.017453,0.0),
        },

# conversion to internal unit: [-]
    'FRACTION' : {
        '-' : (1.0,0.0),
        '%' : (0.01,0.0),
        },

# conversion to internal unit: [1/a]
    'GROWTHRATE' : {
        '1/a' : (1.0,0.0),
        '%/a' : (0.01,0.0),
        },

# conversion to internal unit: [€/kWh]
    'ENERGYTARIFF': {
        '%s/kWh'%CURRENCY : (1.0,0.0),
        '%s/MWh'%CURRENCY : (0.001,0.0),
        '%s/kJ'%CURRENCY: (3600.0,0),
        '%s/MJ'%CURRENCY: (3.6,0.0),
        '%s/GJ'%CURRENCY: (3.6e-3,0.0),
        '%s/btu'%CURRENCY: (1.0/0.0002930711,0.0)
        },

# conversion to internal unit: [€]
    'PRICE': {
        '%s'%CURRENCY : (1.0,0.0),
        'k%s'%CURRENCY: (1000.0,0.0),
        'M%s'%CURRENCY: (1.e+6,0.0),
        }
    }



UNITSYSTEM = {
    'SI' :      {
                'TEMPERATURE':'ºC',
                'TEMPERATUREDIFF':'K',
                'TIME':'s',
                'LONGTIME':'a',
                'LENGTH': 'm',
                'PRESSURE':'bar',
                'AREA':'m2',
                'VOLUME':'m3',
                'VOLUMEFLOW':'m3/s',
                'MASS':'kg',
                'MASSFLOW':'kg/s',
                'MASSORVOLUME':'kg',
                'MASSORVOLUMEFLOW':'kg/h',
                'VOLUMEORMASS':'m3',
                'ENERGY':'GJ',
                'ENERGYFLOW':'MJ/m2a',
                'POWER':'kW',
                'SPECIFICENTHALPY':'kWh/kg',
                'SPECIFICHEAT':'kWh/kgK',
                'HEATTRANSFERCOEF':'kW/K',
                'ANGLE':'º',
                'FRACTION':'-',
                'GROWTHRATE':'%/a',
                'ENERGYTARIFF':'%s/GJ'%CURRENCY,
                'PRICE':'%s'%CURRENCY
                },
    
    'SI-kWh' :  {
                'TEMPERATURE':'ºC',
                'TEMPERATUREDIFF':'K',
                'TIME':'h',
                'LONGTIME':'a',
                'LENGTH': 'm',
                'PRESSURE':'bar',
                'AREA':'m2',
                'VOLUME':'m3',
                'VOLUMEFLOW':'m3/h',
                'MASS':'kg',
                'MASSFLOW':'kg/h',
                'MASSORVOLUME':'kg',
                'MASSORVOLUMEFLOW':'kg/h',
                'VOLUMEORMASS':'m3',
                'ENERGY':'MWh',
                'ENERGYFLOW':'kWh/m2a',
                'POWER':'kW',
                'SPECIFICENTHALPY':'kWh/kg',
                'SPECIFICHEAT':'kWh/kgK',
                'HEATTRANSFERCOEF':'kW/K',
                'ANGLE':'º',
                'FRACTION':'-',
                'GROWTHRATE':'%/a',
                'ENERGYTARIFF':'%s/MWh'%CURRENCY,
                'PRICE':'%s'%CURRENCY
                },

    'BTU' :     {
                'TEMPERATURE':'ºF',
                'TEMPERATUREDIFF':'ºF',
                'TIME':'h',
                'LONGTIME':'a',
                'LENGTH': 'ft',
                'PRESSURE':'lb/ft2',
                'AREA':'ft2',
                'VOLUME':'US gal',
                'VOLUMEFLOW':'US gal/h',
                'MASS':'lb',
                'MASSFLOW':'lb/h',
                'MASSORVOLUME':'kg',
                'MASSORVOLUMEFLOW':'kg/h',
                'VOLUMEORMASS':'m3',
                'ENERGY':'btu',
                'ENERGYFLOW':'btu/h.ft2.a',
                'POWER':'btu/h',
                'SPECIFICENTHALPY':'btu/lb',
                'SPECIFICHEAT':'btu/lbºF',
                'HEATTRANSFERCOEF':'btu/hºF',
                'ANGLE':'º',
                'FRACTION':'-',
                'GROWTHRATE':'%/a',
                'ENERGYTARIFF':'%s/btu'%CURRENCY,
                'PRICE':'%s'%CURRENCY
                }
}

#==================================================================================
#   Conversion functions
#==================================================================================
#------------------------------------------------------------------------------
def internalValue(displayValue,unit,unitType):
#------------------------------------------------------------------------------
#   calculates the internal value from the value entered on GUI
#------------------------------------------------------------------------------
    (a,b) = UNITS[unitType][unit]    
    internalValue = a*displayValue + b

#    print "internalValue d: %s i: %s unit: %s unitType: %s a: %s"%(displayValue,
#                                                     internalValue,
#                                                     unit,
#                                                     unitType,
#                                                     a)

    return internalValue
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def displayValue(internalValue,unit,unitType):
#------------------------------------------------------------------------------
#   calculates the value to be displayed from the internally stored value
#------------------------------------------------------------------------------
    (a,b) = UNITS[unitType][unit]
    displayValue = (internalValue - b)/a

#    print "displayValue d: %s i: %s unit: %s unitType: %s a: %s"%(displayValue,
#                                                     internalValue,
#                                                     unit,
#                                                     unitType,
#                                                     a)
    return displayValue
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def conversionFactor(unit):
#------------------------------------------------------------------------------
#   returns the conversion factor: X (internal units) = X (user units) * cF
#------------------------------------------------------------------------------

    for unitType in UNITS.keys():
        if unit in UNITS[unitType].keys():
            (a,b) = UNITS[unitType][unit]
            return a

    logWarning(_("Units (conversionFactor): unknown unit <%s>")%unit)
        
    return 1.0
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def getUnitTypes(unit):
#------------------------------------------------------------------------------
#   gets the unit type (TEMPERATURE, MASSFLOW, ...) from the unit (ºC, kg/h, ...)
#   used for distinction of mass flow and volume flow, mass and volume, ...
#------------------------------------------------------------------------------
    unitTypes = []
    for key in UNITS.keys():
        if unit in UNITS[key].values():
            unitTypes.append(key)

    return unitTypes
    
#------------------------------------------------------------------------------
#==================================================================================



#Function for merging of two dictionaries
def mergeDict(DICT1,DICT2):
    keyvallist = []
    for k, v in DICT1.iteritems():
        keyvallist.append((k,v))

    for k, v in DICT2.iteritems():
        keyvallist.append((k,v))    

    mergedDict = dict(keyvallist)
    return mergedDict
