#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEM1- Energy performance - Monthly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	21/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#                       Stoyan Danov    04/07/2008
#                       Stoyan Danov    07/07/2008
#                       Stoyan Danov    09/07/2008
#                       Hans Schweiger  16/07/2008
#
#       Changes to previous version:
#	29/03/08:   TS changed functions draw... to use numpy arrays,
#       04/07/08:   SD changes
#       07/07/08:   SD data1 added for plot
#       09/07/08:   SD calculation of monthly from hourly data
#       16/07/08:   HS bug-fixing and complete rearrangement
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
import wx

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.constants import *
import einstein.modules.matPanel as mP
import copy

def _U(text):
    return unicode(_(text),"utf-8")


class ModuleEM1(object):

    def __init__(self, keys):
        self.keys = keys
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        # In this grid the nr. of cols is variable, so we generate the
        # column headings dynamically here
#------------------------------------------------------------------------------

        if Status.int.cascadeUpdateLevel < 0:
            Status.int.initCascadeArrays(0)     #creates the demand profiles
#SQL data search

        self.qprocessdata = Status.prj.getProcesses()   #sqlqueries centralised in project-functions
        processes = self.qprocessdata
            
#........................................................................
# filling the label row (row with 1 + NThProc + 1 entries)
        #for the graphic data array
        LabelRow1 =[_U('Process heat\ndemand')]
        for process in processes:
            LabelRow1.append(unicode(process.Process,"utf-8") +'\n[MWh]')

        #for the table data array
        LabelRow = copy.deepcopy(LabelRow1)
        LabelRow.append(_U('TOTAL\n[MWh]'))


#........................................................................
# taking the UPH values from interfaces

        UPH_Tt = Status.int.UPH_Tt

#.........................................................................
# calculating the monthly data start

        UPHMonthly = [] #UPH all processes (matrix)
        LabelColumn = [_U('Total')]
        LabelColumn.extend(MONTHS)
        UPHMonthly.append(LabelColumn)

#.........................................................................
# start of calculation loop

        UPHMonthlyTotal = []    #Monthly total of ALL PROCESSES
        for i in range(13):
            UPHMonthlyTotal.append(0.0)
            
        for k in range(len(processes)):

            UPHMonthlyProc = [] #UPH single process
            for i in range(13):
                UPHMonthlyProc.append(0.0)

            month = 1
            for it in range(Status.Nt):
                time = Status.TimeStep*it*Status.EXTRAPOLATE_TO_YEAR
                if time >= 24.0*MONTHSTARTDAY[month]:
                    month += 1

                UPHMonthlyProc[month] += UPH_Tt[k][Status.NT+1][it]/1000 #converted to [MWh]

                #calculating the total for process: UPHMonthlyProc[0]

            for month in range(1,13):
                UPHMonthlyProc[0] += UPHMonthlyProc[month]  #Yearly total of the process !!!
                UPHMonthlyTotal[month] += UPHMonthlyProc[month] #Monthly total of all processes
                
            UPHMonthly.append(UPHMonthlyProc)

            

# calculating monthly totals

        GraphUPHMonthly = transpose(copy.deepcopy(UPHMonthly))
        GraphUPHMonthly.insert(0,LabelRow1)

        for month in range(1,13):
            UPHMonthlyTotal[0] += UPHMonthlyTotal[month]
        UPHMonthly.append(UPHMonthlyTotal)       #Add as last column the total of all processes

        TableUPHMonthly = transpose(UPHMonthly)
        TableUPHMonthly.insert(0,LabelRow)

#................................................................................
# end of the calculatin loop

        data1 = array(GraphUPHMonthly)

# creating the data array for the table
        data = array(TableUPHMonthly)

# writing the arrays in interfaces
        Status.int.setGraphicsData(self.keys[0], data)
        Status.int.setGraphicsData(self.keys[1], data1)

   

#------------------------------------------------------------------------------

#==============================================================================
