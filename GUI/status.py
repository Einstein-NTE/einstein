#!/usr/bin/env python
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
#	STATUS
#			
#------------------------------------------------------------------------------
#			
#	Class defining the processing status in the module
#
#==============================================================================
#
#	Version No.: 0.05
#	Created by: 	    Hans Schweiger	10/03/2008
#	Last revised by:    Hans Schweiger      20/03/2008
#                           Hans Schweiger      05/04/2008
#                           Stoyan Danov        14/04/2008
#
#       Changes in last update:
#       - NT and Nt added
#       20/03/08: 
#       05/04/08:     some renaming (see ParameterList v0.31);
#                     identification of data blocks that should
#                     be included in SQL in future versions
#       14/04/08:     InteractionLevel changed to UserInteractionLevel
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

class Status(object):
  PId = None #Active project identity [==> SQL: ActiveProject]
  ANo = None #Active alternative under processing [==> SQL: ActiveAlternative]
  ActiveAlternativeName = ""
  ActiveProjectName = ""
  SetUpId = 0 #Active configuration
  DB = None
  SQL = None
  #------------------------------------------------------------------------------		
  # Statistical data of project [==> SQL Table STATUS]
  
  ProjectCreationDate = None
  ProjectFinalisationDate = None
  LastModificationDate = None
  AuditorId = None
  ConfidentialityLevel = "Public"

  #------------------------------------------------------------------------------		
  # Tool interface configuration [==> SQL Table STATUS]

  UserInteractionLevel = "interactive" # Selected level of user interaction
  LanguageTool = "en"         # Selected language for tool interface
  Units = "SI-kWh"                 # System of units (default: SI-kWh)
  Country = "Spain"                # Configuration for country specific aids ... NOT USED AT PRESENT
  UserType = "Expert"              # type of user: expert, student, end-user ... ???

  #------------------------------------------------------------------------------		
  # Status of processing [==> SQL Table STATUS]

  DataImportOK = False        #no longer used -> CHECK before eliminating !!!
  ConsistencyCheckOK = False  #no longer used -> CHECK before eliminating !!!
  NoOfAlternatives = 0 
  AlternativesOK =[]          #no longer used -> CHECK before eliminating !!!
  ComparativeAnalysisOK = False #no longer used -> CHECK before eliminating !!!
  ReportOK = False            #no longer used -> CHECK before eliminating !!!
  LanguageReport = "english"       # Selected language for report

  #------------------------------------------------------------------------------		
  # Tool configuration
  TimeStep = 1.0
  TemperatureInterval = 5.0
  MaximumTemperature = 400.0
  
  NT = (int) (MaximumTemperature / TemperatureInterval + 0.1)
  Nt = 168*12 #12 weeks instead of 52 for speed-up
  SIMULATED_YEAR = Nt*TimeStep
  EXTRAPOLATE_TO_YEAR = 8760.0 / SIMULATED_YEAR

  HRTool = "PE2"

#------------------------------------------------------------------------------		
# Instance variables

  def __init__(self, name):
    self.myname = name

#==============================================================================


if __name__ == "__main__":
    # for testing purposes only
    # should be invoked: python status.py
    #
    # example of class variables
    s1 = Status("first instance")  # one instance of Status is created 
    s2 = Status("second instance") # another instance is created
    # now class variable is changed. This change is propagated to
    # all instances of the class
    Status.Country = "Mongolia"
    # let's verify:
    print 's1.myname=%s s1.Country=%s' % (s1.myname, s1.Country) 
    print 's2.myname=%s s2.Country=%s' % (s2.myname, s2.Country) 

