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
#	Version No.: 0.06
#	Created by: 	    Hans Schweiger	    22/03/2008
#
#       Last modified by:   Stoyan Danov            04/06/2008
#                           Hans Schweiger          10/06/2008
#                           Claudia Vannoni         02/07/2008
#                           Hans Schweiger          03/07/2008
#                           Hans Schweiger          02/08/2008
#
#       Changes to previous version:
#       04/06/2008  SD: traduceable lists creation
#       10/06/2008  HS: function findKey added
#       02/07/2008  CV: ST parameters
#       03/07/2008: HS  subtypes for boilers adapted to DB Boiler
#       02/08/2008: HS  constant "DEBUG" incorporated
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

#------------------------------------------------------------------------------		
VERSION = "V1.0 Revision No. 259" #Number of upload in sourceforge
#------------------------------------------------------------------------------		
DEBUG = "OFF"   #Set to:
DEBUGMODES = ["OFF","BASIC","MAIN","ALL"]
                #"OFF" (default): no debug

                #"BASIC": basic debugging
                #"ALL": highest level of debugging,
                #"CALC": only ccheck debug in CALC Functions
                #"ADJUST": only ccheck debug in ADJUST Functions
                #"MAIN": ccheck plots the show-alls in each block
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
# constants of general use in EINSTEIN
#------------------------------------------------------------------------------		

INFINITE = 1.e99
KELVIN = 273.15
MAXTEMP = 999.9 #maximum allowed temperature in analysis 

YEAR = 8760.0
DAY = 24.0
WEEK = DAY*7
MONTHSTARTDAY = [0,31,59,90,120,151,181,212,243,273,304,334,365]
    #note: time 0:00h of the first day of each month = MONTHSTARTDAY*DAY
MONTHS = [_('January'),
          _('February'),
          _('March'),
          _('April'),
          _('May'),
          _('June'),
          _('July'),
          _('August'),
          _('September'),
          _('October'),
          _('November'),
          _('December')]

#------------------------------------------------------------------------------		
#default values for status variables

EINSTEIN_OK = 1
EINSTEIN_NOTOK = 0

INTERACTIONLEVELS = ['interactive','semi-automatic','automatic']


#------------------------------------------------------------------------------		
#default entries for parameters

#equiptype is the full description of the type containing information on the equipement-class (BB,HP, ...)
# and on the equipment sub-class (STEAM boiler, CONDENSING boiler, etc.)

EQUIPTYPE = ["compression heat pump",
             "thermal heat pump",
             "steam boiler",
             "condensing boiler",
             "hot water boiler",
             "burner (direct heating)",
             "burner (indirect heating)",
             "compression chiller",
             "thermal chiller",
             "solar thermal (flat-plate)",
             "solar thermal (evacuated tubes)",
             "solar thermal (concentrating solar systems)",
             "CHP engine",
             "CHP steam turbine",
             "CHP gas turbine",
             "CHP fuel cell"]

HPIndex = 0
BBIndex = 2
CHIndex = 7
STIndex = 9
CHPIndex = 12

#translatable dictionary
TRANSEQUIPTYPE = {"compression heat pump":_("compression heat pump"),
             "thermal heat pump":_("thermal heat pump"),
             "steam boiler":_("steam boiler"),
             "condensing boiler":_("condensing boiler"),
             "hot water boiler":_("hot water boiler"),
             "burner (direct heating)":_("burner (direct heating)"),
             "burner (indirect heating)":_("burner (indirect heating)"),
             "compression chiller":_("compression chiller"),
             "thermal chiller":_("thermal chiller"),
             "solar thermal (flat-plate)":_("solar thermal (flat-plate)"),
             "solar thermal (evacuated tubes)":_("solar thermal (evacuated tubes)"),
             "solar thermal (concentrating solar systems)":_("solar thermal (concentrating solar systems)"),
             "CHP engine":_("CHP engine"),
             "CHP steam turbine":_("CHP steam turbine"),
             "CHP gas turbine":_("CHP gas turbine"),
             "CHP fuel cell":_("CHP fuel cell")}

# BBTYPES, STTYPES etc. are the short classifications of the equipment sub-class (usually used within the specific
# equipment modules

BBTYPES = ["steam boiler",
           "condensing boiler",
           "hot water boiler",
           "burner (direct heating)",
           "burner (indirect heating)"]

TRANSBBTYPES = {"steam boiler":_("steam boiler"),
                "condensing boiler":_("condensing boiler"),
                "hot water boiler":_("hot water boiler"),
                "burner (direct heating)":_("burner (direct heating)"),
                "burner (indirect heating)":_("burner (indirect heating)")}

CHTYPES = [ "compression chiller",
            "thermal chiller"]

TRANSCHTYPES = { "compression chiller":_("compression chiller"),
                 "thermal chiller":_("thermal chiller")}


HPTYPES = ["compression",
           "thermal"]

TRANSHPTYPES = {"compression":_("compression"),
                "thermal":_("thermal")}

STTYPES = [ "Flat-plate collector",
            "Evacuated tube collector",
            "Concentrating collector"]

TRANSSTTYPES = {"Flat-plate collector":     _("Flat-plate collector"),
                "Evacuated tube collector": _("Evacuated tube collector"),
                "Concentrating collector":  _("Concentrating collector")
                }

HXTYPES = [ "plate HX (liquid-liquid)",
            "plate HX (air-air)",
            "shell and tube HX (liquid-liquid)",
            "finned tubes (liquid-air)"]
TRANSHXTYPES = {"plate HX (liquid-liquid)":     _("plate HX (liquid-liquid)"),
                "plate HX (air-air)":           _("plate HX (air-air)"),
                "shell and tube HX (liquid-liquid)":_("shell and tube HX (liquid-liquid)"),
                "finned tubes (liquid-air)":    _("finned tubes (liquid-air)")
                }

CHPTYPES = [ "CHP engine",
             "CHP steam turbine",
             "CHP gas turbine",
             "CHP fuel cell"]

TRANSCHPTYPES = {
             "CHP engine":_("CHP engine"),
             "CHP steam turbine":_("CHP steam turbine"),
             "CHP gas turbine":_("CHP gas turbine"),
             "CHP fuel cell":_("CHP fuel cell")}


# EQUIPMENTSUBTYPE collects all the sub-types in ONE list, in the same order as the corresponding
# EQUIPTYPE

EQUIPMENTSUBTYPE = [HPTYPES[0],
                    HPTYPES[1],
                    BBTYPES[0],
                    BBTYPES[1],
                    BBTYPES[2],
                    BBTYPES[3],
                    BBTYPES[4],
               "flat-plate",
               "evacuated tubes",
               "concentrating solar systems",
               "steam turbine",
               "gas turbine",
               "engine",
               "fuel cell",
               "plate HX (liquid-liquid)",
               "plate HX (air-air)",
               "shell and tube HX (liquid-liquid)",
               "finned tubes (liquid-air)"]

# EQUIPMENT associates equipment class and sub-class

EQUIPMENT = {"HP":                 # equipment class
             [(EQUIPTYPE[HPIndex+0],TRANSEQUIPTYPE[EQUIPTYPE[HPIndex+0]],    # type of equipment, translated
               HPTYPES[0], TRANSHPTYPES[HPTYPES[0]]), # type of process, translated
              (EQUIPTYPE[HPIndex+1],TRANSEQUIPTYPE[EQUIPTYPE[HPIndex+1]],
               HPTYPES[1],TRANSHPTYPES[HPTYPES[1]])],

             "BB": [(EQUIPTYPE[BBIndex+0],TRANSEQUIPTYPE[EQUIPTYPE[BBIndex+0]],
                     BBTYPES[0],TRANSBBTYPES[BBTYPES[0]]),
                    (EQUIPTYPE[BBIndex+1],TRANSEQUIPTYPE[EQUIPTYPE[BBIndex+1]],
                     BBTYPES[1],TRANSBBTYPES[BBTYPES[1]]),
                    (EQUIPTYPE[BBIndex+2],TRANSEQUIPTYPE[EQUIPTYPE[BBIndex+2]],
                     BBTYPES[2],TRANSBBTYPES[BBTYPES[2]]),
                    (EQUIPTYPE[BBIndex+3],TRANSEQUIPTYPE[EQUIPTYPE[BBIndex+3]],
                     BBTYPES[3],TRANSBBTYPES[BBTYPES[3]]),
                    (EQUIPTYPE[BBIndex+4],TRANSEQUIPTYPE[EQUIPTYPE[BBIndex+4]],
                     BBTYPES[4],TRANSBBTYPES[BBTYPES[4]])],

             "CH": [(EQUIPTYPE[CHIndex+0],TRANSEQUIPTYPE[EQUIPTYPE[CHIndex+0]],
                     CHTYPES[0],TRANSCHTYPES[CHTYPES[0]]),
                    (EQUIPTYPE[CHIndex+1],TRANSEQUIPTYPE[EQUIPTYPE[CHIndex+1]],
                     CHTYPES[1],TRANSCHTYPES[CHTYPES[1]])],

             "ST": [(EQUIPTYPE[STIndex+0],TRANSEQUIPTYPE[EQUIPTYPE[STIndex+0]],
                     STTYPES[0],TRANSSTTYPES[STTYPES[0]]),
                    (EQUIPTYPE[STIndex+1],TRANSEQUIPTYPE[EQUIPTYPE[STIndex+1]],
                     STTYPES[1],TRANSSTTYPES[STTYPES[1]]),
                    (EQUIPTYPE[STIndex+2],TRANSEQUIPTYPE[EQUIPTYPE[STIndex+2]],
                     STTYPES[2],TRANSSTTYPES[STTYPES[2]])],

             "CHP": [(EQUIPTYPE[CHPIndex+0],TRANSEQUIPTYPE[EQUIPTYPE[CHPIndex+0]],
                      CHPTYPES[0],TRANSCHPTYPES[CHPTYPES[0]]),
                    (EQUIPTYPE[CHPIndex+1],TRANSEQUIPTYPE[EQUIPTYPE[CHPIndex+1]],
                      CHPTYPES[1],TRANSCHPTYPES[CHPTYPES[1]]),
                    (EQUIPTYPE[CHPIndex+2],TRANSEQUIPTYPE[EQUIPTYPE[CHPIndex+2]],
                      CHPTYPES[2],TRANSCHPTYPES[CHPTYPES[2]]),
                    (EQUIPTYPE[CHPIndex+3],TRANSEQUIPTYPE[EQUIPTYPE[CHPIndex+3]],
                      CHPTYPES[3],TRANSCHPTYPES[CHPTYPES[3]])]
             }


#....................................................................

PROCTYPES = ["continuous",
             "batch"]
#translatable dictionary
TRANSPROCTYPES = {"continuous":_("continuous"),
                  "batch":_("batch")}

YESNO = ["yes","no"]
#translatable dictionary
TRANSYESNO = {"yes":_("yes"),"no":_("no")}

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

PRODUCTCODES = {"ZZ000":_("ZZ000: other products"),
                "DA010":_("DA010: milk products"),
                "DA020":_("DA020: fruits/vegetables/herbs"),
                "DA030":_("DA030: sugar"),
                "DA040":_("DA040: beer"),
                "DA050":_("DA050: fats/oils"),
                "DA060":_("DA060: chocolate/cacao/coffee"),
                "DA070":_("DA070: starch/potatoes/grain mill products"),
                "DA080":_("DA080: wine/beverage"),
                "DA090":_("DA090: meat"),
                "DA100":_("DA100: fish"),
                "DA110":_("DA110: aroma")}

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
def setDebugMode(value):
#------------------------------------------------------------------------------
#   sets the DEBUG variable
#------------------------------------------------------------------------------
    global DEBUG
    if value in DEBUGMODES:
        DEBUG = value
#------------------------------------------------------------------------------

if __name__ == '__main__':

    print 'Class   = '+getEquipmentClassUntrans("steam boiler")
    print 'SubClass= '+getEquipmentSubClassUntrans("steam boiler")
    print 'Type    = '+getEquipmentType("BB","direct heating")
