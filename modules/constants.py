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
VERSION = "NOT_M2_DEMO" #M2_DEMO: deactivates pipes

#------------------------------------------------------------------------------		
INFINITE = 1.e99
YEAR = 8760.
KELVIN = 273.15
MAXTEMP = 999.9 #maximum allowed temperature in analysis 

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

#translatable dictionary
TRANSEQUIPTYPE = {"compression heat pump":_("compression heat pump"),
             "thermal heat pump":_("thermal heat pump"),
             "steam boiler":_("steam boiler"),
             "condensing boiler":_("condensing boiler"),
             "burner (direct heating)":_("burner (direct heating)"),
             "burner (indirect heating)":_("burner (indirect heating)"),
             "compression chiller":_("compression chiller"),
             "thermal chiller":_("thermal chiller"),
             "solar thermal (single-glazed selective)":_("solar thermal (single-glazed selective)"),
             "solar thermal (double-glazed selective)":_("solar thermal (double-glazed selective)"),
             "solar thermal (vacuum pump)":_("solar thermal (vacuum pump)"),
             "CHP engine":_("CHP engine"),
             "CHP steam turbine":_("CHP steam turbine"),
             "CHP gas turbine":_("CHP gas turbine"),
             "CHP fuel cell":_("CHP fuel cell")}


EQUIPMENTSUBTYPE = ["condensing",
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

BBTYPES = [EQUIPMENTSUBTYPE[0], EQUIPMENTSUBTYPE[1]]
HPTYPES = [EQUIPMENTSUBTYPE[4], EQUIPMENTSUBTYPE[5]]
TRANSHPTYPES = {"compression":_("compression"),
                "thermal":_("thermal")}

STTYPES = [ "flat plate",
            "evacuated tube",
            "parabolic trough",
            "linear fresnel concentrating"]
TRANSSTTYPES = {"flat plate":     _("flat plate"),
                "evacuated tube":           _("evacuated tube"),
                "parabolic trough":_("parabolic trough"),
                "linear fresnel concentrating":    _("linear fresnel concentrating")
                }

HXTYPES = [ "plate HX (liquid-liquid)",
            "plate HX (air-air)",
            "shell&tube HX (liquid-liquid)",
            "finned tubes (liquid-air)"]
TRANSHXTYPES = {"plate HX (liquid-liquid)":     _("plate HX (liquid-liquid)"),
                "plate HX (air-air)":           _("plate HX (air-air)"),
                "shell&tube HX (liquid-liquid)":_("shell&tube HX (liquid-liquid)"),
                "finned tubes (liquid-air)":    _("finned tubes (liquid-air)")
                }


EQUIPMENT = {"HP":                 # equipment class
             [(EQUIPTYPE[0],       # type of equipment, untranslated
               _(EQUIPTYPE[0]),    # type of equipment, translated
               EQUIPMENTSUBTYPE[4],     # type of process, untranslated
               _(EQUIPMENTSUBTYPE[4])), # type of process, translated

              (EQUIPTYPE[1],_(EQUIPTYPE[1]),EQUIPMENTSUBTYPE[5],_(EQUIPMENTSUBTYPE[5]))],

             "BB": [(EQUIPTYPE[2],_(EQUIPTYPE[2]),EQUIPMENTSUBTYPE[1],_(EQUIPMENTSUBTYPE[1])),
                    (EQUIPTYPE[3],_(EQUIPTYPE[3]),EQUIPMENTSUBTYPE[0],_(EQUIPMENTSUBTYPE[0])),
                    (EQUIPTYPE[4],_(EQUIPTYPE[4]),EQUIPMENTSUBTYPE[2],_(EQUIPMENTSUBTYPE[2])),
                    (EQUIPTYPE[5],_(EQUIPTYPE[5]),EQUIPMENTSUBTYPE[3],_(EQUIPMENTSUBTYPE[3]))],

             "CH": [(EQUIPTYPE[6],_(EQUIPTYPE[6]),EQUIPMENTSUBTYPE[4],_(EQUIPMENTSUBTYPE[4])),
                    (EQUIPTYPE[7],_(EQUIPTYPE[7]),EQUIPMENTSUBTYPE[5],_(EQUIPMENTSUBTYPE[5]))],

             "ST": [(EQUIPTYPE[8],_(EQUIPTYPE[8]),EQUIPMENTSUBTYPE[6],_(EQUIPMENTSUBTYPE[6])),
                    (EQUIPTYPE[9],_(EQUIPTYPE[9]),EQUIPMENTSUBTYPE[7],_(EQUIPMENTSUBTYPE[7])),
                    (EQUIPTYPE[10],_(EQUIPTYPE[10]),EQUIPMENTSUBTYPE[8],_(EQUIPMENTSUBTYPE[8]))],

             "CHP": [(EQUIPTYPE[11],_(EQUIPTYPE[11]),EQUIPMENTSUBTYPE[11],_(EQUIPMENTSUBTYPE[11])),
                    (EQUIPTYPE[12],_(EQUIPTYPE[12]),EQUIPMENTSUBTYPE[9],_(EQUIPMENTSUBTYPE[9])),
                    (EQUIPTYPE[13],_(EQUIPTYPE[13]),EQUIPMENTSUBTYPE[10],_(EQUIPMENTSUBTYPE[10])),
                    (EQUIPTYPE[14],_(EQUIPTYPE[14]),EQUIPMENTSUBTYPE[12],_(EQUIPMENTSUBTYPE[12]))]
             }


#....................................................................

PROCTYPES = ["continuous",
             "batch"]
#translatable dictionary
TRANSPROCTYPES = {"continuous":_("continuous"),
                  "batch":_("batch")}

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
TRANSWHEEWASTEHEATTYPES = {"CoolingWater":_("cooling water"),
                      "Intercooler":_("intercooler"),
                      "CoolingAir":_("cooling air")}

AMBIENTSOURCE = ["ambient air",
               "ground heat exchanger"]
#translatable dictionary
TRANSAMBIENTSOURCE = {"ambient air":_("ambient air"),
                    "ground heat exchanger":_("ground heat exchanger")}

AMBIENTSINK = ["cooling tower",
               "ground heat exchanger"]
#translatable dictionary
TRANSAMBIENTSINK = {"cooling tower":_("cooling tower"),
                    "ground heat exchanger":_("ground heat exchanger")}


#translatable dictionary
ORIENTATIONS = {"S":_("S"),
                "SE":_("SE"),
                "SW":_("SW"),
                "E":_("E"),
                "W":_("W"),
                "NE":_("NE"),
                "NW":_("NW"),
                "N":_("N")}

AZIMUTH = { "S":    0.0,
            "SE":   -45.0,
            "SW":   45.0,
            "E":    -90.0,
            "W":    90.0,
            "NE":   -135.0,
            "NW":   135.0,
            "N":    180.0}

SHADINGTYPES = {"No":_("No"), 
                "Yes,partially shaded":_("Yes,partially shaded"),
                "Yes,fully shaded":_("Yes,fully shaded")}

ROOFTYPES = {"Corrugated metal roof":_("Corrugated metal roof"), 
                "Composite sandwich panels":_("Composite sandwich panels"),
                "Concrete roof":_("Concrete roof"),
                "Tiled roof":_("Tiled roof"),
                "Other":_("Other")}

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
def getEquipmentSubClass(equipeType):
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
