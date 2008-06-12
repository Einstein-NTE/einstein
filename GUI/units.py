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
#	Version No.: 0.06
#	Created by: 	    Stoyan Danov    03/06/2008
#
#       Revised by:         Stoyan Danov    10/06/2008
#                           Stoyan Danov    11/06/2008
#                           Hans Schweiger  11/06/2008
#
#       Changes to previous version:
#       SD: 10/06/2008: added FUELPRICELCV, PRICE
#       SD: 11/06/2008: mergeDict() added
#       HS: 11/06/2008: corrections of bugs: MJ/GJ, comma by dot, ...
#                       new structure of dictionaries
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

UNITS = {
# conversion to internal unit: [ºC]
    'TEMPERATURE' : {
        'ºC':(1.0,0.0),
        'ºF':(5.0/9,-32.0*5/9),
        'K':(1.0,-273.15)
        }

# conversion to internal unit: [K]
    'TEMPERATUREDIFF' : {
        'K': (1.0,0.0),
        'ºF':(5.0/9,0.0),
        }

# conversion to internal unit: [m]
    'LENGTH' : {
        'm' : (1.0,0.0),
        'km' : (1000.0,0.0),
        'mm' : (1.0e-3,0.0),
        'yards': (0.9144,0.0),
        'ft'   : (0,3048,0.0),
        'in'   : (0.0254,0.0)
        }
    
    }


#### to be continued ...
    
###all converted to [bar]
##PRESSURE = {'bar' : 'v',
##            'atm' : 'v*1.01325',
##            'mm Hg' : 'v*0.001333224',
##            'kPa' : 'v/100',
##            'MPa' : 'v*10'}
##
###all converted to [m3]
##VOLUME = {'m3' : 'v',
##          'l' : 'v/1000',
##          'ft3' : 'v*0.028317',
##          'U.S. gal' : 'v*0.003785',
##          'Brit. gal' : 'v*0.004546',
##          'barrel (U.S. pet.)' : 'v*0.15898'}
##
###all converted to [kg]
##MASS = {'kg' : 'v',
##        'lb' : 'v*0.45359',
##        'ton' : 'v*1000'}
##
##
###all converted to [kg/h]
##MASSFLOW = {'kg/h' : 'v',
##            'kg/s': 'v*3600',
##            'lb/h'  : 'v*0.45359'}
##
###all converted to [kWh]
##ENERGY = {'kWh' : 'v',
##          'kJ': 'v/3600',
##          'MJ': 'v*1e3/3600',
##          'GJ': 'v*1e6/3600',
##          'kcal': 'v*1.163/1000',
##          'btu': 'v*0.0002930711'}
##
###all converted to [kW]
##POWER = {'kW' : 'v',
##         'kcal/h': 'v*1.163/1000',
##         'btu/h': 'v*0.0002930711'}
##
###all converted to [kWh/kg]
##ENTHALPY = {'kWh/kg' : 'v',
##            'kJ/kg': 'v/3600',
##            'kcal/kg': 'v*1.163/1000'}
##
###all converted to [kWh/kgK]
##SPECIFICHEAT = {'kWh/kgK' : 'v',
##                'kJ/kgK': 'v/3600',
##                'kcal/kgK': 'v*1.163/1000'}
##
###all converted to [kW/K]
##HEATTRANSFERCOEF = {'kW/K' : 'v',
##                    'W/K': 'v/1000'}


UNITSYSTEM = {'SI' : {'TEMPERATURE':'ºC',
                 'TEMPERATUREDIFF':'K',
                 'LENGTH': 'm',
                 'PRESSURE':'bar',
                 'VOLUME':'m3',
                 'MASS':'kg',
                 'MASSFLOW':'kg/s',
                 'ENERGY':'kJ',
                 'POWER':'kW'},
                 'SPECIFICENTHALPY':'kWh/kg',
                 'SPECIFICHEAT':'kWh/kgK',
                 'HEATTRANSFERCOEF':'kW/K',
                 'FUELPRICELCV':'€/kJ (LCV)',
                 'PRICE':'€'},
         'SI-kWh' : {'TEMPERATURE':'ºC',
                 'TEMPERATUREDIFF':'K',
                 'LENGTH': 'm',
                 'PRESSURE':'bar',
                 'VOLUME':'m3',
                 'MASS':'kg',
                 'MASSFLOW':'kg/h',
                 'ENERGY':'kWh',
                 'POWER':'kW'},
                 'SPECIFICENTHALPY':'kWh/kg',
                 'SPECIFICHEAT':'kWh/kgK',
                 'HEATTRANSFERCOEF':'kW/K',
                 'FUELPRICELCV':'€/kWh (LCV)',
                 'PRICE':'€'},
          'BTU' :{'TEMPERATURE':'ºF',
                 'TEMPERATUREDIFF':'ºF',
                 'LENGTH': 'ft',
                 'PRESSURE':'lbs/ft2',
                 'VOLUME':'US gal',
                 'MASS':'lb',
                 'MASSFLOW':'lb/h',
                 'ENERGY':'btu',
                 'POWER': 'btu/h',
                 'SPECIFICENTHALPY':'btu/lb???',
                 'SPECIFICHEAT':'btu/lbºF???',
                 'HEATTRANSFERCOEF':'btu/hºF'},
                 'FUELPRICELCV':'US-$/btu (LCV)',
                 'PRICE':'US-$'}
         }

#==================================================================================
#   Conversion functions
#==================================================================================
#------------------------------------------------------------------------------
def value(displayValue,unit,unitType):
#------------------------------------------------------------------------------
#   calculates the internal value from the value entered on GUI
#------------------------------------------------------------------------------
    (a,b) = UNITS[unitType][unit]
    
    value = a*value + b
    return value
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def displayValue(value,unit,unitType):
#------------------------------------------------------------------------------
#   calculates the value to be displayed from the internally stored value
#------------------------------------------------------------------------------
    (a,b) = UNITS[unitType][unit]
    
    displayValue = (value - b)/a
    return displayValue
    
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
