#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	MESSAGE LOGGER
#			
#------------------------------------------------------------------------------
#			
#	Auxiliary module for using the main-fucntions
#       logMessage, logError and logWarning also from other modules
#
#       logMessage, logWarnings, logError: display on the GUI interface
#       logTrack: tracks messages in data file for further analysis
#
#==============================================================================
#	Version No.: 0.01
#
#       Created by:     Hans Schweiger      17/04/2008
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

DEBUG = True

from einstein.GUI.status import Status
import einstein.GUI.HelperClass as HelperClass

#------------------------------------------------------------------------------		
def logTrack(message):
#------------------------------------------------------------------------------		
    try:
        Status.doLog.LogThis(message)
    except:
        Status.doLog = HelperClass.LogHelper()
        Status.doLog.LogThis(message)

    if DEBUG:
        print(message)

#------------------------------------------------------------------------------		
def logMessage(message):
#------------------------------------------------------------------------------		
    Status.main.logMessage(message)
    logTrack("#MESSAGE: "+message)

#------------------------------------------------------------------------------		
def logError(message):
#------------------------------------------------------------------------------		
    Status.main.logMessage(message)
    logTrack("#ERROR: "+message)

#------------------------------------------------------------------------------		
def logWarning(message):
#------------------------------------------------------------------------------		
    Status.main.logMessage(message)
    logTrack("#WARNING: "+message)

#------------------------------------------------------------------------------		
def logDebug(message):
    if DEBUG:
        logTrack("DEBUG: "+message)
#------------------------------------------------------------------------------		

        
