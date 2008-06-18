#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA - module that calls the energyStatistics functions without
#       displaying the panels (used for report generation)
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger  18/06/2008
#       Revised by:         
#
#       Changes to previous version:
#       18/06/2008          
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

from sys import *
from math import *
from numpy import *


from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP


class ModuleEA(object):

    def __init__(self):
        
        pass

#------------------------------------------------------------------------------
    def update(self):
#------------------------------------------------------------------------------
#       updates all the energyStatistics needed for the report        
#------------------------------------------------------------------------------
        self.procHeatTemp()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def procHeatTemp(self):
#------------------------------------------------------------------------------
# report field PROCHEATTEMP: process heat demand by temperature levels

        tableReport = [["T","UPH","UPHnet","USH"]]
        for iT in range(Status.NT+1):
            if iT < 81:
                temp = Status.TemperatureInterval *iT
                tableReport.append([temp,                           
                                    Status.int.QD_T[iT],                            # cols E-K 
                                    Status.int.QA_T[iT],                                  # cols L-M are merged
                                    Status.int.QA_T[iT]])                                  # col P-Q
            elif k == 81:
                print "WARNING: present standard report is limited to 80 temperature intervals !!!"

        for iT in range(Status.NT+1,81):
                tableReport.append([" ",                             
                                    " ",                             
                                    " ",                             
                                    " "])                            



        Status.int.setGraphicsData("PROCHEATTEMP", array(tableReport))
        print "ModuleEA (procHeatTemp): resulting array"
        print array(tableReport)

#==============================================================================
