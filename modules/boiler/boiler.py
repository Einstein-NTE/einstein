#============================================================================== 				
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	BOILER - Module for boiler dimensioning and calculation
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Module for boiler dimensioning and calculation
#       Draft version
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	31/01/2008
#	Last revised by:    Hans Schweiger      31/01/2008
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

from einstein.auxiliary.auxiliary import *

#------------------------------------------------------------------------------
#   default parameters of the boiler module:
def setBoilerDefaultPars():
#------------------------------------------------------------------------------

    SecurityMargin = 0.2
    BoilerModel = "Detailed"
    minOpTime = 1300
    return 1

#------------------------------------------------------------------------------
#def boiler(sql, DB, Qid):
def boiler(CHD):
#------------------------------------------------------------------------------
#   short description of the function or class(especially if several functions
#   are defined in one file
#------------------------------------------------------------------------------

    SecurityMargin = 0.2
    BoilerModel = "Detailed"
    minOpTime = 1300

    print "within boiler module ", SecurityMargin, BoilerModel,minOpTime
    
    try:

#..............................................................................
#1. Look for maximum power in demand
        Qmax = maxInList(CHD)
        print 'Maximum heat demand = ', Qmax

#..............................................................................
#2. Apply Security margin / redundancy 
        QBoiler = Qmax*(1+SecurityMargin)
        print 'Total boiler power', QBoiler


#..............................................................................
#3. Subdivision of total boiler power
        Boilers = []

        if BoilerModel == "Simplified":
            NBoilers = 2

            power = QBoiler/2
            Boilers.append(power)   #add first boiler to the list

            power = QBoiler/2
            Boilers.append(power)   #add second boiler to the list
    
        elif BoilerModel == "Detailed":

            NBoilers = 3
            power = CHD[minOpTime]

            Boilers.append(power)

            power = CHD[minOpTime/2] - Boilers[0]
            Boilers.append(power)

            power = QBoiler - Boilers[0] - Boilers[1]
            Boilers.append(power)
        
    
        else:
            print 'dont know this boiler model'

        print 'total number of boilers: ',NBoilers
        for i in range(len(Boilers)):
            print 'Boiler power, boiler [', i+1, ']', Boilers[i]
        
#..............................................................................
    except Exception, boiler: #in case of an error

        print 'exception', boiler
        return boiler

#..............................................................................
    else:		#everything is fine
        return 1
#------------------------------------------------------------------------------
