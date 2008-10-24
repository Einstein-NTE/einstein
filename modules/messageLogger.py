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

DEBUG_TO = "LOGFILE"    #SCREEN: prints debug information on the screen
                    #LOGFILE: writes debug information to the log-File
                    #OFF: no debug information written

from einstein.GUI.status import Status
import einstein.GUI.HelperClass as HelperClass

#------------------------------------------------------------------------------		
def setDebugMode(mode):
#------------------------------------------------------------------------------		
#   function that can be called from somewhere for setting the mode of debugging
#------------------------------------------------------------------------------		

    global DEBUG_TO

    if mode in ["SCREEN","LOGFILE","OFF"]:
        DEBUG_TO = mode
    else:
        DEBUG_TO = "OFF"
        logWARNING("messageLogger (setDebugMode): error in debug mode [%s]"%mode)
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
def logTrack(message):
#------------------------------------------------------------------------------		
#   keeps track of what the user does within the EINSTEIN log-file
#   this information can be very useful for debuggig
#   e.g. each user interaction on the GUI should be logged
#------------------------------------------------------------------------------		
    try:
        Status.doLog.LogThis(message)
    except:
        Status.doLog = HelperClass.LogHelper()
        Status.doLog.LogThis(message)

    if DEBUG_TO == "SCREEN":
        print(message)

#------------------------------------------------------------------------------		
def logMessage(message):
#------------------------------------------------------------------------------		
#   writes a message to the EINSTEIN GUI and parallely to the log-file
#------------------------------------------------------------------------------		
    Status.main.logMessage(message)

#------------------------------------------------------------------------------		
def logError(message):
#------------------------------------------------------------------------------		
#   writes a message to the EINSTEIN GUI and parallely to the log-file
#   highlights as ERROR
#------------------------------------------------------------------------------		
    Status.main.logError(message)

#------------------------------------------------------------------------------		
def logWarning(message):
#------------------------------------------------------------------------------		
#   writes a message to the EINSTEIN GUI and parallely to the log-file
#   highlights as WARNING
#------------------------------------------------------------------------------		
    Status.main.logWarning(message)

#------------------------------------------------------------------------------		
def logDebug(message):
#------------------------------------------------------------------------------		
#   writes a message to the log-file or to the screen (depending on DEBUG mode)
#   doesn't do anything if DEBUG = "OFF"
#------------------------------------------------------------------------------		
    if DEBUG_TO == "SCREEN":
        print message
    elif DEBUG_TO == "LOGFILE":
        logTrack("DEBUG: "+message)
    
#------------------------------------------------------------------------------		
def showError(text):
#------------------------------------------------------------------------------		
#   like logError, but opens a pop-up for confirmation
#------------------------------------------------------------------------------		
    Status.main.showError(text)
#------------------------------------------------------------------------------		
def showWarning(text):
#------------------------------------------------------------------------------		
#   like logWarning, but opens a pop-up for confirmation
#------------------------------------------------------------------------------		
    Status.main.showWarning(text)

#------------------------------------------------------------------------------		
def showMessage(text):
#------------------------------------------------------------------------------		
#   like logMessage, but opens a pop-up for confirmation
#------------------------------------------------------------------------------		
    Status.main.showInfo(text)
        
#------------------------------------------------------------------------------		
def askConfirmation(text):
#------------------------------------------------------------------------------		
#   like showMessage, but returns the answer of the user (wx.YES_NO)
#------------------------------------------------------------------------------		
    return Status.main.askConfirmation(text)
#------------------------------------------------------------------------------		

