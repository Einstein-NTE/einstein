#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (http://www.iee-einstein.org/)
#
#------------------------------------------------------------------------------
#
#	ModuleEA2- Final energy (FEC/FET) - Yearly data
#
#==============================================================================
#
#	Version No.: 0.06
#	Created by: 	    Tom Sobota	    21/03/2008
#       Revised by:         Hans Schweiger  28/03/2008
#                           Tom Sobota      28/03/2008
#                           Stoyan Danov    07/04/2008
#                           Stoyan Danov    11/04/2008
#                           Hans Schweiger  13/04/2008
#                           Stoyan Danov    02/05/2008
#                           Hans Schweiger  07/07/2008
#
#       Changes to previous version:
#	28/03/08:   functions draw_ ... moved to panel
#	28/03/08:   TS changed functions draw... to use numpy arrays,
#       07/04/2008: SD Adapted to show data from sql, not checked
#       11/04/2008: SD: Dummy data added for displaying temporaly, to avoid problems with None.
#                       Return to original state later!
#       13/04/2008: HS: initialisation moved to function initPanel
#       02/05/2008: SD: C->Q tables, change FECi,FETi(old) to FECFuel,FEFFuel; self.interfaces -> Status.int #SD, check for None
#       07/07/2008: HS: Clean-up, conversion to MWh
#                   
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	http://www.energyxperts.net/
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
from einstein.modules.fluids import *
from einstein.modules.messageLogger import *

def _U(text):
    return unicode(_(text),"utf-8")

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class ModuleEA2(object):
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def __init__(self, keys):
#------------------------------------------------------------------------------
#   instance of module is created at the beginning when GUI is built-up
#   only basic initialisation
#------------------------------------------------------------------------------
        self.keys = keys # keys for accessing the data in Interfaces
        logTrack("ModuleEA2 (init): starting")

    def initPanel(self):
#------------------------------------------------------------------------------
#   initialisation of the Panel before displaying.
#   activated when EA2 is selected on the tree
#------------------------------------------------------------------------------

        Status.mod.moduleEA.update()
        
#..............................................................................
#   get access to the info in SQL

        PId = Status.PId
        ANo = Status.ANo

        fuels = Status.prj.getQFuels()
        (projectData,generalData) = Status.prj.getProjectData()
        
        self.NFuels = len(fuels)

#..............................................................................
# Final energy consumption by fuels (data for panel EA2)

        TotalFEC = 0.0
        TotalFETi = 0.0
        FEC = []
        FETi = []
        fuelNames = []
            
        for fuel in fuels:  #sum all FECFuel/FETFuel for fuels used #SD 
            fuelID = fuel.DBFuel_id #SD

            f = Fuel(fuelID)   
            fuelName = f.name
            
            fuelNames.append(fuelName)
            
            try: dFEC = fuel.FECFuel/1000.0
            except: dFEC = 0.0
            
            TotalFEC += dFEC 
            FEC.append(dFEC)
            
            try: dFET = fuel.FETFuel/1000.0
            except: dFET = 0.0
            
            TotalFETi += dFET
            FETi.append(dFET)

        try: FECel = generalData.FECel / 1000.0
        except: FECel = 0.0
        
        try: FETel = generalData.FETel / 1000.0
        except: FETel = 0.0
        
        if FECel is not None:
            TotalFEC += FECel  #add FECel to TotalFEC
            FEC.append(FECel) #SD: check if OK here
        else:
            TotalFEC += 0.0
            FEC.append(0.0) #SD: check if OK here

        if FETel is not None:
            TotalFETi += FETel
            FETi.append(FETel) #SD: check if OK here
        else:
            TotalFETi += 0.0
            FETi.append(0.0) #SD: check if OK here
            
        fuelNames.append(_U("Electricity"))

        FECPercentage = []
        FETPercentage = []

        for i in range (self.NFuels + 1):
            if TotalFEC > 0.0: #SD avoid division by zero
                FECPercentage.append(FEC[i]*100.0/TotalFEC)
            else:
                FECPercentage.append(0.0)
                
            if TotalFETi > 0.0: #SD avoid division by zero
                FETPercentage.append(FETi[i]*100.0/TotalFETi)
            else:
                FETPercentage.append(0.0)

#.........................................................        
        #finish the table columns, add total, sum percentage
        fuelNames.append(_U('Total'))
        FEC.append(TotalFEC)
        FETi.append(TotalFETi)

        suma = 0
        for i in FECPercentage:
            suma += i
        FECPercentage.append(suma)

        suma = 0
        for i in FETPercentage:
            suma += i
        FETPercentage.append(suma)

#.........................................................

        TableColumnList = [fuelNames,FEC,FECPercentage,FETi,FETPercentage]
        matrix = transpose(TableColumnList)

        data = array(matrix)

        Status.int.setGraphicsData(self.keys[0], data)

        reportMatrix = []
        for i in range(len(matrix)-1):
            if i < 10:
                reportMatrix.append(matrix[i])
        for i in range(len(matrix)-1,10):
            reportMatrix.append([" "," "," "," "," "])
        reportMatrix.append(matrix[len(matrix)-1])

        reportData = array(reportMatrix)
        if Status.ANo == 0:
            Status.int.setGraphicsData("EA2_REPORT", reportData)
        elif Status.ANo == Status.FinalAlternative:
            Status.int.setGraphicsData("EA2_REPORT_F", reportData)
        
#------------------------------------------------------------------------------

#==============================================================================
