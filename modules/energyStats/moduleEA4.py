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
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	21/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#       Last revised by:    Stoyan Danov 07/04/2008
#       Revised by:         Stoyan Danov     11/04/2008
#
#       Changes to previous version:
#       29/3/2008          Adapted to numpy arrays
#       07/04/2008          Adapted to use data from sql, not checked
#       11/04/2008: SD: Dummy data added for displaying temporaly, to avoid problems with None.
#                       Return to original state later!
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
        self.interface = Interfaces()
#.........................................................................
        PId = Status.PId
        ANo = Status.ANo

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(PId,ANo)
        self.qprocessdata = Status.DB.qprocessdata.sql_select(sqlQuery)
#.........................................................................

        try:
            self.initModule()
        except:
            pass

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------

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
            UPHk = Status.DB.cprocessdata.QProcessData_id[row.QProcessData_ID][0].UPH
            TotalUPH += UPHk
            UPH.append(UPHk)

            print 'Process=',row.Process,'UPHk=',UPHk,'PT=',row.PT,'TSupply=',row.TSupply

        UPHPercentage = []
        for row in self.qprocessdata:
            UPHk = Status.DB.cprocessdata.QProcessData_id[row.QProcessData_ID][0].UPH
            UPHPercentage.append(UPHk*100.0/TotalUPH)

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
        #
        # upper grid: UPH by process
        #

        TableColumnList1 = [Process, UPH, UPHPercentage]

        matrix1 = transpose(TableColumnList1)

        data1 = array(matrix1)

        
        dummydata1 = array([['Process name 1', 170.0,   33.01],
                      ['Process name 2', 280.0,   54.37],
                      ['Process name 3',  65.0,   12.62],
                      ['Total'         , 515.0,  100.00]])

        self.interface.setGraphicsData(self.keys[0], dummydata1)

        #
        # lower grid: Process heat by temperature
        #

        Process.pop() #delete 'Total' and TotalUPH
        UPH.pop()

        TableColumnList2 = [Process, PT, TSupply, UPH]

        matrix2 = transpose(TableColumnList2)

        data2 = array(matrix2)

        dummydata2 = array([['Process name 1',  40.0, 180.0, 170.0],
                      ['Process name 2',  75.0, 180.0, 280.0],
                      ['Process name 3',  90.0, 180.0,  65.0]])


        self.interface.setGraphicsData(self.keys[1], dummydata2)

        #print "ModuleEA4 graphics data initialization"
        #print "Interfaces.GData[%s] contains:\n%s\n" % (self.keys[0],repr(Interfaces.GData[self.keys[0]]))
        #print "Interfaces.GData[%s] contains:\n%s\n" % (self.keys[1],repr(Interfaces.GData[self.keys[1]]))
        return "ok"

#------------------------------------------------------------------------------
    def exitModule(self,exit_option):
#------------------------------------------------------------------------------
        """
        carries out any calculations necessary previous to displaying the HP
        design assitant window
        """
#------------------------------------------------------------------------------
        if exit_option == "save":
            print "exitModule: here I should save the current configuration"
        elif exit_option == "cancel":
            print "exitModule: here I should retreive the previous configuration"
            

        print "exitModule: function not yet defined"

        return "ok"

#------------------------------------------------------------------------------

#==============================================================================
