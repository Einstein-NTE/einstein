#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA1- Final energy by fuels- Yearly data
#			
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Tom Sobota	21/03/2008
#       Revised by:         Tom Sobota  29/03/2008
#       Revised by:         Stoyan Danov  07/04/2008
#       Revised by:         Stoyan Danov     11/04/2008
#                           Stoyan Danov    02/05/2008
#                           Hans Schweiger  02/07/2008
#                           Hans Schweiger  08/07/2008
#
#       Changes to previous version:
#       29/3/2008          Adapted to numpy arrays
#       07/04/2008           Adapted to use data from sql, not checked
#       11/04/2008: SD: Dummy data added for displaying temporaly, to avoid problems with None.
#                       Return to original state later!
#       02/05/2008: SD: sqlQuery -> to initModule; sejf.interfaces -> Status.int,
#                                   protection zeroDivision and missing data(PId,ANo)->probably not necessary??
#       02/07/2008: HS  Adaptation to changes in nomeclature (update_einsteinDB_019)
#                       Some compacting and clean-up
#       08/07/2008: HS  Conversion kWh -> MWh
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
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP

def _U(text):
    return unicode(_(text),"utf-8")

class ModuleEA1(object):

    def __init__(self, keys):
        self.keys = keys
        self.initModule()

#------------------------------------------------------------------------------
    def initModule(self):
#------------------------------------------------------------------------------

        PId = Status.PId
        ANo = Status.ANo

        Status.mod.moduleEA.update()    #checks if data in SQL are uptodate
                                        #and otherwise carries out necessary
                                        #calculations

#..............................................................................
#Check: Protection for missing data(Pid and ANo)in cgeneraldata
        
        (projectData,generalData) = Status.prj.getProjectData()

        if generalData is None:
        
            PEC = [0.0, 0.0]
            PECTotal = 0.0
            PECPercentage = [0.0,0.0]

            PET = [0.0, 0.0]
            PETTotal = 0.0
            PETPercentage = [0.0,0.0]

        else:
            PEC = [generalData.PECFuels, generalData.PECel]

            for i in range(len(PEC)):
                if PEC[i] is not None:
                    PEC[i] /= 1000.0        #convert to MWh
                else:
                    PEC[i] = 0.0

            PECTotal = PEC[0] + PEC[1]
            
            if PECTotal > 0.0 and PECTotal is not None: #SD: zeroDivision and None check
                PECPercentage = [PEC[0]*100.0/PECTotal, PEC[1]*100.0/PECTotal]
            else:
                PECPercentage = [0.0,0.0]

            PET = [generalData.PETFuels, generalData.PETel]
            
            for i in range(len(PET)):
                if PET[i] is not None:
                    PET[i] /= 1000.0        #convert to MWh
                else:
                    PET[i] = 0.0

            PETTotal = PET[0]+PET[1]
            
            if PETTotal > 0.0 and PETTotal is not None: #SD: zeroDivision and None check
                PETPercentage = [PET[0]*100.0/PETTotal, PET[1]*100.0/PETTotal]
            else:
                PETPercentage = [0.0,0.0]

#..............................................................
        #finish the table columns, add total, percentage
        Labels = [_U('Total fuels'),_U('Total electricity'),_U('Total (fuels + electricity)')]
        PEC.append(PECTotal)
        PET.append(PETTotal)

        suma = 0
        for i in PECPercentage:
            suma += i
        PECPercentage.append(suma)

        suma = 0
        for i in PETPercentage:
            suma += i
        PETPercentage.append(suma)
      
#.................................................................

        TableColumnList = [Labels,PEC,PECPercentage,PET,PETPercentage]

        matrix = transpose(TableColumnList)
        data = array(matrix)
        
        Status.int.setGraphicsData(self.keys[0], data)

        if Status.ANo == 0:
            Status.int.setGraphicsData("EA1_REPORT", data)
        elif Status.ANo == Status.FinalAlternative:
            Status.int.setGraphicsData("EA1_REPORT_F", data)
            

        print data

#------------------------------------------------------------------------------

#==============================================================================
