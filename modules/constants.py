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
#	CONSTANTS
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Constants for general use in the tool
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	    22/03/2008
#
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

INFINITE = 1.e99
YEAR = 8760.
KELVIN = 273.15

#------------------------------------------------------------------------------		
#default values for status variables

EINSTEIN_OK = 1
EINSTEIN_NOTOK = 0

INTERACTIONLEVELS = ['interactive','semi-automatic','automatic']


#------------------------------------------------------------------------------		
#default entries for parameters

EQUIPETYPESDICT = [{"Type":"compression heat pump", "Class":"HP",   "SubClass":"compression"},
                   {"Type":"thermal heat pump",  "Class":"HP",   "SubClass":"thermal"},
                   {"Type":"steam boiler",          "Class":"BB",   "SubClass":"steam"},
                   {"Type":"condensing boiler",     "Class":"BB",   "SubClass":"condensing"}]

EQUIPETYPES = ["compression heat pump",
              "thermal heat pump"
              "steam boiler",
              "condensing boiler"]

EQUIPECLASSES = ["HP","BB"]

HPTYPES = ["compression",
           "thermal"]

#==============================================================================
#   auxiliary functions for lookup in default tables and dictionaries
#==============================================================================
#------------------------------------------------------------------------------
def getEquipmentClass(equipeType):
#------------------------------------------------------------------------------
#       returns the class of the equipment as a function of the equipment type
#------------------------------------------------------------------------------

    for eq in EQUIPETYPESDICT:
        if eq["Type"] == equipeType:
            return eq["Class"]
    return "class undefined (equipeType = %s)"%equipeType
            
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def getEquipmentSubClass(equipeType):
#------------------------------------------------------------------------------
#       returns the class of the equipment as a function of the equipment type
#------------------------------------------------------------------------------

    for eq in EQUIPETYPESDICT:
        if eq["Type"] == equipeType:
            return eq["SubClass"]
    return "subClass undefined (equipeType = %s)"%equipeType

#------------------------------------------------------------------------------
def getEquipmentType(equipeClass,equipeSubClass):
#------------------------------------------------------------------------------
#       returns the class of the equipment as a function of the equipment type
#------------------------------------------------------------------------------

    print "getEquipmentType: starting"
    print "getEquipmentType: ",equipeClass,equipeSubClass
    for eq in EQUIPETYPESDICT:
        if eq["Class"] == equipeClass and eq["SubClass"]==equipeSubClass:
            print "getEquipmentType: selected type = ",eq["Type"]
            return eq["Type"]
    return "type undefined (equipeSubClass = %s)"%equipeSubClass
            
#------------------------------------------------------------------------------
            


