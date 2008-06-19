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
#	Version No.: 0.02
#
#       Created by:     Hans Schweiger      17/04/2008
#
#       Last modified by:   Hans Schweiger  19/06/2008
#
#       Changes:
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

DEBUG = "LOGFILE"    #SCREEN: prints debug information on the screen
                    #LOGFILE: writes debug information to the log-File
                    #OFF: no debug information written

from einstein.GUI.status import Status
import einstein.GUI.HelperClass as HelperClass

#------------------------------------------------------------------------------		
def setDebugMode(mode):

    global DEBUG

    if mode in ["SCREEN","LOGFILE","OFF"]:
        DEBUG = mode
    else:
        DEBUG = "OFF"
        logWARNING("messageLogger (setDebugMode): error in debug mode [%s]"%mode)
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
def logTrack(message):
#------------------------------------------------------------------------------		
    try:
        Status.doLog.LogThis(message)
    except:
        Status.doLog = HelperClass.LogHelper()
        Status.doLog.LogThis(message)

    if DEBUG == "SCREEN":
        print(message)

#------------------------------------------------------------------------------		
def logMessage(message):
#------------------------------------------------------------------------------		
    Status.main.logMessage(message)

#------------------------------------------------------------------------------		
def logError(message):
#------------------------------------------------------------------------------		
    Status.main.logMessage(message)

#------------------------------------------------------------------------------		
def logWarning(message):
#------------------------------------------------------------------------------		
    Status.main.logMessage(message)

#------------------------------------------------------------------------------		
def logDebug(message):
    if DEBUG == "SCREEN":
        print message
    elif DEBUG == "LOGFILE":
        logTrack("DEBUG: "+message)
    
#------------------------------------------------------------------------------		
def showWarning(text):
    Status.main.showWarning(text)

#------------------------------------------------------------------------------		
def showInfo(text):
    Status.main.showInfo(text)
        
#------------------------------------------------------------------------------		
def askConfirmation(self, text):
    return Status.main.askConfirmation(text)
#------------------------------------------------------------------------------		

