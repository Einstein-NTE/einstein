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
#                           Stoyan Danov        10/07/2008
#
#       Changes to previous version:
#       09/07/2008ff SD: add modules for CS2, CS3,
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
        if self.keys[0] == "CS1 Plot":
            for ANo in range(len(generalData)-1):
                i = ANo+1

                if salternatives[i].StatusEnergy > 0:
                    dPEC = generalData[i].PEC                
                
                    if dPEC is None:
                        dPEC = 0.0
                        dPEC_Table = "---"
                    else:
                        dPEC /= 1000.0  #conversion kWh -> MWh
                        dPEC_Table = dPEC

                    if ANo == 0:
                        PEC0 = dPEC

                    PECSaving = dPEC - PEC0
                    if PEC0 > 0:
                        RelSaving = PECSaving/PEC0
                    else:
                        RelSaving = 0.0

                else:
                    dPEC = 0.0
                    dPEC_Table = "---"
                    PECSaving = "---"
                    RelSaving = "---"
                        
                PEC.append(dPEC)

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
#------------------------------------------------------------------------------
# Panel CS2: Process & supply heat
        elif self.keys[0] == "CS2 Plot":

#............................................................................
# charge UPH and USH data from SQL
            UPH = []
            USH = []
            Alternative = []

            CS2Table = []
            CS2Plot = []
            
            for ANo in range(len(generalData)-1):
                i = ANo+1

                if salternatives[i].ShortName is None:
                    Alternative.append('--')
                else:
                    Alternative.append(str(salternatives[i].ShortName))

                if generalData[i].UPH is None: #protection against None
                    UPH.append(0.0)
                else:
                    UPH.append(generalData[i].UPH)

                if generalData[i].USH is None:
                    USH.append(0.0)
                else:
                    USH.append(generalData[i].USH)           

                if salternatives[i].StatusEnergy > 0:
                    dUSH = generalData[i].USH
                    dUPH = generalData[i].UPH
                    if dUSH is None:
                        dUSH = 0.0
                        dUSH_Table = "---"
                    else:
                        dUSH /= 1000.0  #conversion kWh -> MWh
                        dUSH_Table = dUSH

                    if dUPH is None:
                        dUPH = 0.0
                        dUPH_Table = "---"
                    else:
                        dUPH /= 1000.0  #conversion kWh -> MWh
                        dUPH_Table = dUSH

                    if ANo == 0:
                        USH0 = dUSH
                        UPH0 = dUPH

                    USHSaving = dUSH - USH0
                    if USH0 > 0:
                        RelSavingUSH = USHSaving/USH0
                    else:
                        RelSavingUSH = 0.0

                    UPHSaving = dUPH - UPH0
                    if UPH0 > 0:
                        RelSavingUPH = UPHSaving/UPH0
                    else:
                        RelSavingUPH = 0.0

                else:
                    dUSH = 0.0
                    dUPH = 0.0
                    dUSH_Table = "---"
                    dUPH_Table = "---"
                    USHSaving = "---"
                    UPHSaving = "---"
                    RelSavingUSH = "---"
                    RelSavingUPH = "---"
                        
                USH.append(dUSH)
                UPH.append(dUPH)


                if ANo == 0:
                    tableEntry = noneFilter([str(salternatives[i].ShortName),
                                             dUPH_Table,"---",
                                             dUSH_Table,"---"])
                else:
                    tableEntry = noneFilter([str(salternatives[i].ShortName),
                                             dUPH_Table,UPHSaving,
                                             dUSH_Table,USHSaving])
                plotEntry = noneFilter([str(salternatives[i].ShortName),dUSH,dUPH])
                
                CS2Table.append(tableEntry)
                CS2Plot.append(plotEntry)
#..............................................................................
# then send everything to the GUI

            data1 = array(CS2Table)
                              
            Status.int.setGraphicsData("CS2 Table", data1)

            matrix2 = transpose(CS2Plot)
            data2 = array(CS2Plot)

            Status.int.setGraphicsData("CS2 Plot", data2)

#------------------------------------------------------------------------------
# Panel CS3: Ambiental impact
        elif self.keys[0] == "CS3 Plot":

#............................................................................
# charge data from SQL
            Alternative = []
            CO2El = []
            CO2Fuel = []
            CO2Total = []
            NucWaste = []
            WaterConsum = []
            for i in range(len(generalData)):
                if salternatives[i].ShortName is None:
                    Alternative.append('--')
                else:
                    Alternative.append(str(salternatives[i].ShortName))

                if generalData[i].ProdCO2el is None: #protection against None
                    CO2El.append(0.0)
                else:
                    CO2El.append(generalData[i].ProdCO2el/1000.0)   #kg -> tons

                if generalData[i].ProdCO2Fuels is None:
                    CO2Fuel.append(0.0)
                else:
                    CO2Fuel.append(generalData[i].ProdCO2Fuels/1000.0)  #kg -> tons

                CO2Total.append(CO2El[i]+CO2Fuel[i])

                # charge data from SQL for Nuclear waste and Water consumption
                #..... now dummydata added ...

                if generalData[i].ProdNoNukesEl is None:
                    NucWaste.append(0.0)
                else:
                    NucWaste.append(generalData[i].ProdNoNukesEl*1.e-6) #conversion mg-> kg

#                if generalData[i].WaterConsum is None:
                WaterConsum.append(0.0)
#                else:
#                    NucWaste.append(generalData[i].WaterConsum)
            
#.............................................................................
# calculate savings
            ComparCO2 = [100.0,100.0]
            ComparNW = [100.0,100.0]
            ComparWater = [100.0,100.0]
            SavingCO2 = [0.0,0.0]
            SavingNW = [0.0,0.0]
            SavingWater = [0.0,0.0]
            for i in range(2,len(generalData)):
                saveCO2 = CO2Total[1] - CO2Total[i]
                SavingCO2.append(saveCO2)

                saveNW = NucWaste[1] - NucWaste[i]
                SavingNW.append(saveNW)

                saveWater = WaterConsum[1] - WaterConsum[i]
                SavingWater.append(saveWater)
                
                if CO2Total[1] != 0.0: #protection division by zero
                    ComparCO2.append(100.0*CO2Total[i]/CO2Total[1])
                else:
                    ComparUPH.append(100.0)

                if NucWaste[1] != 0.0: #protection division by zero
                    ComparNW.append(100.0*NucWaste[i]/NucWaste[1])
                else:
                    ComparNW.append(100.0)

                if WaterConsum[1] != 0.0: #protection division by zero
                    ComparWater.append(100.0*WaterConsum[i]/WaterConsum[1])
                else:
                    ComparWater.append(100.0)

#.............................................................................
# set data to interfaces

# eliminate the original data (unchecked) entry from lists
            Alternative.pop(0)
            CO2El.pop(0)
            CO2Fuel.pop(0)
            CO2Total.pop(0)
            NucWaste.pop(0)
            WaterConsum.pop(0)
            SavingCO2.pop(0)
            SavingNW.pop(0)
            SavingWater.pop(0)
            ComparCO2.pop(0)
            ComparNW.pop(0)
            ComparWater.pop(0)   

            data1 = array(transpose([Alternative,CO2Total,NucWaste,WaterConsum]))
            data2 = array(transpose([Alternative,ComparCO2,ComparNW,ComparWater]))

##            print 'Plot: data2 =',data2
##            print 'Table: data1 =',data1

            Status.int.setGraphicsData("CS3 Table", data1)
            Status.int.setGraphicsData("CS3 Plot", data2)

#==============================================================================
