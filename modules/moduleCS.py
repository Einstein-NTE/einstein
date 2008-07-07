#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleCS - Comparative study
#
#       Preparation of comparative tables for GUI and report
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	05/07/2008
#       Revised by:         
#
#       Changes to previous version:
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

from math import *
from numpy import *

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *

class ModuleCS(object):

    def __init__(self, keys):
        self.keys = keys

#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#   data that have to be provided at the init of panel creation
#------------------------------------------------------------------------------

        pass
    
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#   send information to the GUI necessary for updating the panel
#------------------------------------------------------------------------------

#..............................................................................
# first collect the information for all the alternatives in the project

        sqlQuery = "Questionnaire_id = '%s' ORDER BY AlternativeProposalNo ASC"%(Status.PId)
        generalData = Status.DB.cgeneraldata.sql_select(sqlQuery)

        sqlQuery = "ProjectID = '%s' ORDER BY AlternativeProposalNo ASC"%(Status.PId)
        salternatives = Status.DB.salternatives.sql_select(sqlQuery)

        PEC = []

        PECTable = []
        PECPlot = [[10,11],[20,21]]  #dummies en dos primeras filas para test de labels + ignoredrows
                   
#Panel CS1: Primary energy
        for ANo in range(len(generalData)-1):
            i = ANo+1
            dPEC = generalData[i].PEC                
            
            if dPEC is None:
                dPEC = 0.0
                dPEC_Table = "---"
            else:
                dPEC /= 1000.0  #conversion kWh -> MWh
                dPEC_Table = dPEC

            if ANo == 0.0:
                PEC0 = dPEC

            PECSaving = dPEC - PEC0
            if PEC0 > 0:
                RelSaving = PECSaving/PEC0
            else:
                RelSaving = 0.0
                
                
            PEC.append(generalData[i].PEC)

            if ANo == 0:
                tableEntry = noneFilter([str(salternatives[i].ShortName),dPEC_Table,PECSaving,RelSaving*100])
            else:
                tableEntry = noneFilter([str(salternatives[i].ShortName),dPEC_Table,"---","---"])
            plotEntry = noneFilter([str(salternatives[i].ShortName),dPEC])
            
            PECTable.append(tableEntry)
            PECPlot.append(plotEntry)
                        
#..............................................................................
# then send everything to the GUI

        data1 = array(PECTable)
                          
        Status.int.setGraphicsData("CS1 Table", data1)

        matrix2 = transpose(PECPlot)
        data2 = array(PECPlot)

        Status.int.setGraphicsData("CS1 Plot", data2)

#------------------------------------------------------------------------------

#==============================================================================
