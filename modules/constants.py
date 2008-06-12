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
#	Version No.: 0.03
#	Created by: 	    Hans Schweiger	    22/03/2008
#
#       Last modified by:   Stoyan Danov            04/06/2008
#                           Hans Schweiger          10/06/2008
#
#       Changes to previous version:
#       04/06/2008  SD: traduceable lists creation
#       10/06/2008  HS: function findKey added
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
def _(text):
    return text

#------------------------------------------------------------------------------		
VERSION = "M2_DEMO"

#------------------------------------------------------------------------------		
INFINITE = 1.e99
YEAR = 8760.
KELVIN = 273.15
MAXTEMP = 999.9 #maximum allowed temperature in analyisis 

#------------------------------------------------------------------------------		
#default values for status variables

EINSTEIN_OK = 1
EINSTEIN_NOTOK = 0

INTERACTIONLEVELS = ['interactive','semi-automatic','automatic']


#------------------------------------------------------------------------------		
#default entries for parameters

EQUIPTYPE = ["compression heat pump",
             "thermal heat pump",
             "steam boiler",
             "condensing boiler",
             "burner (direct heating)",
             "burner (indirect heating)",
             "compression chiller",
             "thermal chiller",
             "solar thermal (single-glazed selective)",
             "solar thermal (double-glazed selective)",
             "solar thermal (vacuum pump)",
             "CHP engine",
             "CHP steam turbine",
             "CHP gas turbine",
             "CHP fuel cell"]

PROCESSTYPE = ["condensing",
               "steam",
               "direct heating",
               "indirect heating",
               "compression",
               "thermal",
               "single-glazed selective",
               "double-glazed selective",
               "vacuum tube",
               "steam turbine",
               "gas turbine",
               "engine",
               "fuel cell",
               "plate HX (liquid-liquid)",
               "plate HX (air-air)",
               "shell&tube HX (liquid-liquid)",
               "finned tubes (liquid-air)"]

BBTYPES = [PROCESSTYPE[0], PROCESSTYPE[1]]
HPTYPES = [PROCESSTYPE[4], PROCESSTYPE[5]]
HXTYPES = [PROCESSTYPE[13], PROCESSTYPE[14], PROCESSTYPE[15], PROCESSTYPE[16]]

EQUIPMENT = {"HP":                 # equipment class
             [(EQUIPTYPE[0],       # type of equipment, untranslated
               _(EQUIPTYPE[0]),    # type of equipment, translated
               PROCESSTYPE[4],     # type of process, untranslated
               _(PROCESSTYPE[4])), # type of process, translated

              (EQUIPTYPE[1],_(EQUIPTYPE[1]),PROCESSTYPE[5],_(PROCESSTYPE[5]))],

             "BB": [(EQUIPTYPE[2],_(EQUIPTYPE[2]),PROCESSTYPE[1],_(PROCESSTYPE[1])),
                    (EQUIPTYPE[3],_(EQUIPTYPE[3]),PROCESSTYPE[0],_(PROCESSTYPE[0])),
                    (EQUIPTYPE[4],_(EQUIPTYPE[4]),PROCESSTYPE[2],_(PROCESSTYPE[2])),
                    (EQUIPTYPE[5],_(EQUIPTYPE[5]),PROCESSTYPE[3],_(PROCESSTYPE[3]))],

             "CH": [(EQUIPTYPE[6],_(EQUIPTYPE[6]),PROCESSTYPE[4],_(PROCESSTYPE[4])),
                    (EQUIPTYPE[7],_(EQUIPTYPE[7]),PROCESSTYPE[5],_(PROCESSTYPE[5]))],

             "ST": [(EQUIPTYPE[8],_(EQUIPTYPE[8]),PROCESSTYPE[6],_(PROCESSTYPE[6])),
                    (EQUIPTYPE[9],_(EQUIPTYPE[9]),PROCESSTYPE[7],_(PROCESSTYPE[7])),
                    (EQUIPTYPE[10],_(EQUIPTYPE[10]),PROCESSTYPE[8],_(PROCESSTYPE[8]))],

             "CHP": [(EQUIPTYPE[11],_(EQUIPTYPE[11]),PROCESSTYPE[11],_(PROCESSTYPE[11])),
                    (EQUIPTYPE[12],_(EQUIPTYPE[12]),PROCESSTYPE[9],_(PROCESSTYPE[9])),
                    (EQUIPTYPE[13],_(EQUIPTYPE[13]),PROCESSTYPE[10],_(PROCESSTYPE[10])),
                    (EQUIPTYPE[14],_(EQUIPTYPE[14]),PROCESSTYPE[12],_(PROCESSTYPE[12]))]
             }


#....................................................................

PROCTYPES = ["continuous",
             "batch"]
#translatable dictionary
TRANSPROCTYPES = {"Continuous":_("continuous"),
                  "Batch":_("batch")}

YESNO = ["yes","no"]
#translatable dictionary
TRANSYESNO = {"Yes":_("yes"),"No":_("no")}

STORAGETYPES = ["sensible",
                "latent"]
#translatable dictionary
TRANSSTORAGETYPES = {"Sensible":_("sensible"),
                     "Latent":_("latent")}

WHEEEQTYPES = ["electric motor",
               "compressor","other"]
#translatable dictionary
TRANSWHEEEQTYPES = {"ElectricMotor":_("electric motor"),
                    "Compressor":_("compressor"),
                    "Other":_("other")}

WHEEWASTEHEATTYPES = ["cooling water",
                      "intercooler",
                      "cooling air"]
#translatable dictionary
WHEEWASTEHEATTYPES = {"CoolingWater":_("cooling water"),
                      "Intercooler":_("intercooler"),
                      "CoolingAir":_("cooling air")}


#==============================================================================
#   auxiliary functions for lookup in default tables and dictionaries
#==============================================================================
#------------------------------------------------------------------------------
def getEquipmentItem(item,equipeType):
#------------------------------------------------------------------------------
#       returns the class of the equipment as a function of the equipment type
#------------------------------------------------------------------------------

    for cls in EQUIPMENT.keys():
        theList = EQUIPMENT[cls]
        for elem in theList:
            if elem[item] == equipeType:
                return (cls,elem[1],elem[2],elem[3])

    return "cannot find element %s)" % equipeType


def getEquipmentClass(equipeType):
#------------------------------------------------------------------------------
#       returns the class of the untranslated equipment as a function of the equipment type
#------------------------------------------------------------------------------
    return getEquipmentItem(0,equipeType)[0]

def getEquipmentClassTrans(equipeType):
#------------------------------------------------------------------------------
#       returns the class of the translated equipment as a function of the equipment type
#------------------------------------------------------------------------------
    return getEquipmentItem(1,equipeType)[0]
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def getEquipmentSubClassUntrans(equipeType):
#------------------------------------------------------------------------------
#       returns the untranslated subclass of the untranslated equipment as a function of the equipment type
#------------------------------------------------------------------------------
    return getEquipmentItem(0,equipeType)[2]

#------------------------------------------------------------------------------
def getEquipmentType(equipeClass,equipeSubClass):
#------------------------------------------------------------------------------
#       returns the type of the equipment as a function of the untranslated equipment class and subclass
#------------------------------------------------------------------------------
    theList = EQUIPMENT[equipeClass]
    for eq in theList:
        if eq[2] == equipeSubClass:
            return eq[0]

    return "type undefined (equipeSubClass = %s)"%equipeSubClass
#------------------------------------------------------------------------------
def findKey(dictionary,value):
#------------------------------------------------------------------------------
#       returns the class of the equipment as a function of the equipment type
#------------------------------------------------------------------------------

    for key in dictionary.keys():
        if dictionary[key] == value:
            return key

    return None
            
#------------------------------------------------------------------------------
            


if __name__ == '__main__':

    print 'Class   = '+getEquipmentClassUntrans("steam boiler")
    print 'SubClass= '+getEquipmentSubClassUntrans("steam boiler")
    print 'Type    = '+getEquipmentType("BB","direct heating")
