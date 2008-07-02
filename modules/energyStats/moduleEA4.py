# -*- coding: cp1252 -*-
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA4- Process heat- Yearly data
#			
#==============================================================================
#
#	Version No.: 0.06
#	Created by: 	    Tom Sobota	    21/03/2008
#       Revised by:         Tom Sobota      29/03/2008
#                           Stoyan Danov    07/04/2008
#                           Stoyan Danov    11/04/2008
#                           Stoyan Danov    02/05/2008
#                           Hans Schweiger  08/05/2008
#                           Stoyan Danov    02/07/2008
#
#       Changes to previous version:
#       29/3/2008          Adapted to numpy arrays
#       07/04/2008          Adapted to use data from sql, not checked
#       11/04/2008: SD: Dummy data added for displaying temporaly, to avoid problems with None.
#                       Return to original state later!
#       02/05/2008: SD: sqlQuery -> to initModule; sejf.interfaces -> Status.int,None resistance,avoid ZeroDivision
#       08/05/2008: HS  Generation of GDATA table PROCESS for report
#       02/05/2008: SD: add total row in data
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


class ModuleEA4(object):

    def __init__(self, keys):
        print "ModuleEA4"
        
        self.keys = keys


#############################################
        Status.int.setGraphicsData(self.keys[2],[Status.int.T[0:Status.NT],
                                                      Status.int.QD_T[0:Status.NT],
                                                      Status.int.QA_T[0:Status.NT]])
##        Interfaces.setDefaultDemand()
##        Interfaces.setGraphicsData(self.keys[2],[Interfaces.T,
##                                                      Interfaces.QD_T_mod[0],
##                                                      Interfaces.QA_T_mod[0]])
##############################################


##        dummydata1 = array([['Process name 1', 170.0,   33.01],
##                      ['Process name 2', 280.0,   54.37],
##                      ['Process name 3',  65.0,   12.62],
##                      ['Total'         , 515.0,  100.00]])
        
        dummydata1 = array([['Process name 1', 6.0, 60.0, 5.0, 0.5, 0.5, 90.0, 180.0],
                            ['Process name 2', 4.0, 40.0, 2.0, 1.0, 1.0, 110.0, 180.0],
                            ['Total'         , 10.0, 100.0, 7.0, 1.5, 1.5, 0, 0]])

        Status.int.setGraphicsData(self.keys[0], dummydata1)

##        dummydata2 = array([['Process name 1',  40.0, 180.0, 170.0],
##                            ['Process name 2',  75.0, 180.0, 280.0],
##                            ['Process name 3',  90.0, 180.0,  65.0],
##                            ['Total'         , 205.0, 540.0, 515.00]])

        dummydata2 = array([['< 60 C', 2, 8.51, 8.51, 2, 8.51, 8.51],
                            ['60 – 80 C', 1, 7.75, 7.75, 1, 7.75, 7.75],
                            ['80 – 100 C', 1, 7.75, 7.75, 1, 7.75, 7.75],
                            ['100 – 120 C', 1, 7.75, 7.75, 1, 7.75, 7.75],
                            ['120 – 140 C', 1, 7.75, 7.75, 1, 7.75, 7.75],
                            ['140 – 180 C',0, 7.75, 7.75, 0, 7.75, 7.75],
                            ['180 – 220 C', 0, 7.75, 7.75, 0, 7.75, 7.75],
                            ['220 – 300 C', 0, 7.75, 7.75, 0, 7.75, 7.75],
                            ['300 – 400 C',  0, 7.75, 7.75, 0, 7.75, 7.75],
                            ['> 400 C', 0, 8.75, 8.75, 0, 8.75, 8.75],
                            ['Total', 16, 100.0, 100.0, 16, 100.0, 100.0]])	

        Status.int.setGraphicsData(self.keys[1], dummydata2)

#        self.initModule()


    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------

        PId = Status.PId
        ANo = Status.ANo

        self.qprocessdata = Status.prj.getProcesses()   #sqlqueries centralised in project-functions
        processes = self.qprocessdata

        Process = []
        PT = []
        TSupply = []
        UPHk = 0.0
        UPH = []
        
        TotalUPH = 0.0
        for row in self.qprocessdata:
            Process.append(row.Process)
            PT.append(row.PT)
            TSupply.append(row.TSupply)
            UPHk = row.UPH
            if row.UPH is None:
                TotalUPH += 0.0
                UPH.append(0.0)
            else:
                TotalUPH += UPHk
                UPH.append(UPHk)

            print 'Process=',row.Process,'UPHk=',UPHk,'PT=',row.PT,'TSupply=',row.TSupply

        UPHPercentage = []
        for row in self.qprocessdata:
            UPHk = row.UPH
            if TotalUPH > 0.0: #SD avoid division by zero
                UPHPercentage.append(UPHk*100.0/TotalUPH)
            else:
                UPHPercentage.append(0.0)

        print 'UPHPercentage=',UPHPercentage

#.........................................................        
        #finish the table columns, add total, percentage total
        Process.append('Total')
        UPH.append(TotalUPH)

        suma = 0
        for i in UPHPercentage:
            suma += i
        UPHPercentage.append(suma)


#................................................................
# here data are prepared for the GUI and the report
        

# upper grid: UPH by process
        TableColumnList1 = [Process, UPH, UPHPercentage]

        matrix1 = transpose(TableColumnList1)
        print 'moduleEA4: matrix1 =', matrix1
        data1 = array(matrix1)

        Status.int.setGraphicsData(self.keys[0], data1)

# lower grid: Process heat by temperature
        
        Process.pop() #delete 'Total' and TotalUPH
        UPH.pop()

        TableColumnList2 = [Process, PT, TSupply, UPH]

        matrix2 = transpose(TableColumnList2)
        print 'moduleEA4: matrix2 =', matrix2
        data2 = array(matrix2)

        Status.int.setGraphicsData(self.keys[1], data2)

# report field PROCESS: process info

        tableReport = []
        for process in processes:
            k = process.ProcNo - 1
            if k < 10:   #present master limited to 10 processes !!!

                tableReport.append([process.Process,                              # col C-D
                                    process.Description,                            # cols E-K 
                                    process.UPH,                                  # cols L-M are merged
                                    UPHPercentage[k],                             # cols N-O are merged
                                    process.PT])                                  # col P-Q
            elif k == 10:
                print "WARNING: present standard report is limited to a maximum of 10 processes !!!"

        for k in range(len(processes),10):
                tableReport.append([" ",                             # col C-D
                                    " ",                             # cols E-K 
                                    " ",                             # cols L-M are merged
                                    " ",                             # cols N-O are merged
                                    " "])                             # col P-Q


        tableReport.append([_("Total"),                                           # col C-D
                            " ",                                                 # cols E-K 
                            TotalUPH,                                           # cols L-M are merged
                            100,                                                # cols N-O are merged
                            " "])                                                 # col P-Q

        Status.int.setGraphicsData("PROCESSES", array(tableReport))
        print "ModuleEA4 -> data table for processes",array(tableReport)

        return "ok"

#==============================================================================
