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
#	Version No.: 0.07
#	Created by: 	    Hans Schweiger	05/07/2008
#                           Stoyan Danov        10/07/2008
#                           Stoyan Danov        12/07/2008
#                           Stoyan Danov        13/07/2008
#                           Stoyan Danov        14/07/2008
#                           Stoyan Danov        15/07/2008
#                           Hans Schweiger      08/10/2008
#
#       Changes to previous version:
#       09/07/2008ff SD: add modules for CS2, CS3,
#       12/07/2008   SD: algunas correcciones en la parte CS2 (Hans)
#                       -> parte CS3 re-worked: control StatusEnergy > 0 added,
#                       -> clean-up
#       13/07/2008   SD: CS4 added
#       14/07/2008   SD: CS5, queries: qelectricity, qfuel
#       15/07/2008   SD: CS6, CS7
#       08/10/2008   HS: Table generation for report added
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
import copy

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

        sqlQuery = "Questionnaire_id = '%s' ORDER BY AlternativeProposalNo ASC"%(Status.PId)
        qelectricity = Status.DB.qelectricity.sql_select(sqlQuery)


        PEC = []

        PECTable = []
        PECPlot = []
        
#Panel CS1: Primary energy
        if self.keys[0] == "CS1_Plot":
            
            PEC0 = 0.0
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

                    PECSaving = PEC0 - dPEC #SD corrected, was inverted
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

                if ANo != 0: #SD corrected, was ==
                    tableEntry = noneFilter([str(salternatives[i].ShortName),dPEC_Table,PECSaving,RelSaving*100])
                else:
                    tableEntry = noneFilter([str(salternatives[i].ShortName),dPEC_Table,"---","---"])
                plotEntry = noneFilter([str(salternatives[i].ShortName),dPEC])
                
                PECTable.append(tableEntry)
                PECPlot.append(plotEntry)
                            
#..............................................................................
# then send everything to the GUI

            data1 = array(PECTable)
                              
            Status.int.setGraphicsData("CS1_Table", data1)

            matrix2 = transpose(PECPlot)
            data2 = array(PECPlot)

            Status.int.setGraphicsData("CS1_Plot", data2)

#            print 'Table: data1\n',data1
#            print 'Plot: data2\n',data2

            PECReport = copy.deepcopy(PECTable)
            for i in range(len(PECTable),11):
                PECReport.append([" "," "," "," "])
            dataReport1 = array(PECReport)                  
            Status.int.setGraphicsData("CS1_REPORT", dataReport1)

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Panel CS2: Process & supply heat
        elif self.keys[0] == "CS2_Plot":

#............................................................................
# charge UPH and USH data from SQL
            UPH = []
            USH = []
            Alternative = []

            CS2Table = []
            CS2Plot = []

            USH0 = 0.0
            UPH0 = 0.0
            
            for ANo in range(len(generalData)-1):
                i = ANo+1

                if salternatives[i].ShortName is None:
                    Alternative.append('--')
                else:
                    Alternative.append(str(salternatives[i].ShortName))

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
                        dUPH_Table = dUPH #SD: gazapo aqui, era (= dUSH)!!!

                    if ANo == 0: #SD: here passes the first time only and calculates USH0, UPH0
                        USH0 = dUSH #can be assigned once, why check each time?
                        UPH0 = dUPH

                    USHSaving = USH0 - dUSH #SD: inverted-changed sign
                    if USH0 > 0:
                        RelSavingUSH = USHSaving/USH0
                        if dUSH_Table == "---":
                            RatioUSH = 0.0
                        else:
                            RatioUSH = dUSH*100.0/USH0 #SD in %
                    else:
                        RelSavingUSH = 0.0
                        RatioUSH = 0.0 #SD in %

                    UPHSaving = UPH0 - dUPH #SD: inverted-changed sign
                    if UPH0 > 0:
                        RelSavingUPH = UPHSaving/UPH0
                        if dUPH_Table == "---":
                            RatioUPH = 0.0
                        else:
                            RatioUPH = dUPH*100.0/UPH0 #SD in %
                    else:
                        RelSavingUPH = 0.0
                        RatioUPH = 0.0 #SD in %

                else:
                    dUSH = 0.0
                    dUPH = 0.0
                    dUSH_Table = "---"
                    dUPH_Table = "---"
                    USHSaving = "---"
                    UPHSaving = "---"
                    RelSavingUSH = 0.0 #SD: before "---" (could be plot data)
                    RelSavingUPH = 0.0 #SD: before "---" (could be plot data)
                    RatioUSH = 0.0
                    RatioUPH = 0.0
                        
                USH.append(dUSH) #SD: these are not used
                UPH.append(dUPH) #SD: these are not used


                if ANo == 0:
                    tableEntry = noneFilter([str(salternatives[i].ShortName),
                                             dUPH_Table,"---",
                                             dUSH_Table,"---"])
                else:
                    tableEntry = noneFilter([str(salternatives[i].ShortName),
                                             dUPH_Table,UPHSaving,
                                             dUSH_Table,USHSaving])
                plotEntry = noneFilter([str(salternatives[i].ShortName),RatioUSH,RatioUPH]) #SD: before: dUSH, dUPH

                CS2Table.append(tableEntry)
                CS2Plot.append(plotEntry)
#..............................................................................
# then send everything to the GUI

            data1 = array(CS2Table)
                              
            Status.int.setGraphicsData("CS2_Table", data1)

##            matrix2 = transpose(CS2Plot)
            data2 = array(CS2Plot)

            Status.int.setGraphicsData("CS2_Plot", data2)
##            print 'CS2 table =', data1
##            print 'CS2 plot =', data2
##            print 'USH =', USH
##            print 'UPH =', UPH

            CS2Report = copy.deepcopy(CS2Table)
            for i in range(len(CS2Table),11):
                CS2Report.append([" "," "," "," "," "])
            dataReport2 = array(CS2Report)                  
            Status.int.setGraphicsData("CS2_REPORT", dataReport2)

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Panel CS3: Ambiental impact
        elif self.keys[0] == "CS3_Plot":

#............................................................................
# charge UPH and USH data from SQL
            CO2El = []
            CO2Fuel = []
            CO2Total = []
            NucWaste = []
            WaterConsum = []
            Alternative = []

            CS3Table = []
            CS3Plot = []

            CO2_0 = 0
            NucWaste0 = 0
            WatConsum0 = 0

            for ANo in range(len(generalData)-1):
                i = ANo+1

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

                CO2Total.append(CO2El[i-1]+CO2Fuel[i-1])#to i-1 (list from 0 to ANo)

                #nuclear waste from sql
                if generalData[i].ProdNoNukesEl is None:
                    NucWaste.append(0.0)
                else:
                    NucWaste.append(generalData[i].ProdNoNukesEl*1.e-6) #conversion mg-> kg

                WaterConsum.append(0.0)
                
                if salternatives[i].StatusEnergy > 0:
                    dCO2 = CO2Total[i-1]#to i-1 (list from 0 to ANo)
                    if dCO2 == 0.0:
                        dCO2_Table = "--"
                    else:
                        dCO2_Table = dCO2

                    dNucWaste = generalData[i].ProdNoNukesEl
                    if dNucWaste is None:
                        dNucWaste = 0.0
                        dNucWaste_Table = "---"
                    else:
                        dNucWaste = dNucWaste*1.e-6 #conversion mg-> kg
                        dNucWaste_Table = dNucWaste

                    dWatConsum = WaterConsum[i-1]#to i-1 (list from 0 to ANo)
                    dWatConsum_Table = dWatConsum
            
                    if ANo == 0:
                        CO2_0 = dCO2
                        NucWaste0 = dNucWaste
                        WatConsum0 = dWatConsum

                    CO2Saving = CO2_0 - dCO2
                    if CO2_0 > 0:
                        RelSavingCO2 = CO2Saving/CO2_0
                        RatioCO2 = dCO2*100.0/CO2_0 #in %
                    else:
                        RelSavingCO2 = 0.0
                        RatioCO2 = 0.0

                    NucWasteSaving = NucWaste0 - dNucWaste
                    if NucWaste0 > 0:
                        RelSavingNucWaste = NucWasteSaving/NucWaste0
                        RatioNucWaste = dNucWaste*100.0/NucWaste0 #in %
                    else:
                        RelSavingNucWaste = 0.0
                        RatioNucWaste = 0.0

                    WatConsumSaving = WatConsum0 - dWatConsum
                    if WatConsum0 > 0:
                        RelSavingWatConsum = WatConsumSaving/WatConsum0
                        RatioWatConsum = dWatConsum*100.0/WatConsum0 #in %
                    else:
                        RelSavingWatConsum = 0.0
                        RatioWatConsum = 0.0

                else:
                    dCO2 = 0.0
                    dNucWaste = 0.0
                    dWatConsum = 0.0
                    dCO2_Table = "---"
                    dNucWaste_Table = "---"
                    dWatConsum_Table = "---"
                    CO2Saving = "---"
                    NucWasteSaving = "---"
                    WatConsumSaving = "---"
                    RelSavingCO2 = 0.0
                    RelSavingNucWaste = 0.0
                    RelSavingWatConsum = 0.0
                    RatioCO2 = 0.0
                    RatioNucWaste = 0.0
                    RatioWatConsum = 0.0                    
                    

                tableEntry = noneFilter([str(salternatives[i].ShortName),
                                         dCO2_Table,dNucWaste_Table,dWatConsum_Table])

                plotEntry = noneFilter([str(salternatives[i].ShortName),RatioCO2,RatioNucWaste,RatioWatConsum])
               
                CS3Table.append(tableEntry)
                CS3Plot.append(plotEntry)
#..............................................................................
# then send everything to the GUI

            data1 = array(CS3Table)
                              
            Status.int.setGraphicsData("CS3_Table", data1)

##            matrix2 = transpose(CS3Plot)
            data2 = array(CS3Plot)

            Status.int.setGraphicsData("CS3_Plot", data2)

            CS3Report = copy.deepcopy(CS3Table)
            for i in range(len(CS3Table),11):
                CS3Report.append([" "," "," "," "])
            dataReport3 = array(CS3Report)                  
            Status.int.setGraphicsData("CS3_REPORT", dataReport3)

#------------------------------------------------------------------------------

##########################################################################
#------------------------------------------------------------------------------
# Panel CS4: Investment cost
        elif self.keys[0] == "CS4_Plot":

#............................................................................
# charge data from SQL
            TotalCost = []
            OwnCost = []
            Subsidies = []
            Alternative = []

            CS4Table = []
            CS4Plot = []

            TotalCost0 = 0
            OwnCost0 = 0
            Subsidies0 = 0

            for ANo in range(len(generalData)-1):
                i = ANo+1

                if salternatives[i].ShortName is None:
                    Alternative.append('--')
                else:
                    Alternative.append(str(salternatives[i].ShortName))

                if generalData[i].TotalInvCost is None: #protection against None
                    TotalCost.append(0.0)
                else:
                    TotalCost.append(generalData[i].TotalInvCost)

                if generalData[i].OwnInvCost is None:
                    OwnCost.append(0.0)
                else:
                    OwnCost.append(generalData[i].OwnInvCost)

                if generalData[i].Subsidies is None:
                    Subsidies.append(0.0)
                else:
                    Subsidies.append(generalData[i].Subsidies)

                
                if salternatives[i].StatusECO > 0:
                    dTotalCost = generalData[i].TotalInvCost
                    if dTotalCost is None:
                        dTotalCost = 0.0
                        dTotalCost_Table = "---"
                    else:
                        dTotalCost_Table = dTotalCost

                    dOwnCost = generalData[i].OwnInvCost
                    if dOwnCost is None:
                        dOwnCost = 0.0
                        dOwnCost_Table = "---"
                    else:
                        dOwnCost_Table = dOwnCost

                    dSubsidies = generalData[i].Subsidies
                    if dSubsidies is None:
                        dSubsidies = 0.0
                        dSubsidies_Table = "---"
                    else:
                        dSubsidies_Table = dSubsidies
            
                    if ANo == 0:
                        TotalCost0 = dTotalCost
                        OwnCost0 = dOwnCost
                        Subsidies0 = dSubsidies


                else:
                    dTotalCost = 0.0
                    dOwnCost = 0.0
                    dSubsidies = 0.0
                    dTotalCost_Table = "---"
                    dOwnCost_Table = "---"
                    dSubsidies_Table = "---"  
                    

                tableEntry = noneFilter([str(salternatives[i].ShortName),
                                         dTotalCost_Table,dOwnCost_Table,dSubsidies_Table])

                plotEntry = noneFilter([str(salternatives[i].ShortName),dOwnCost,dSubsidies])
               
                CS4Table.append(tableEntry)
                CS4Plot.append(plotEntry)
#..............................................................................
# then send everything to the GUI

            data1 = array(CS4Table)
                              
            Status.int.setGraphicsData("CS4_Table", data1)

            matrix2 = transpose(CS4Plot)
            data2 = array(CS4Plot)

            Status.int.setGraphicsData("CS4_Plot", data2)

            CS4Report = copy.deepcopy(CS4Table)
            for i in range(len(CS4Table),11):
                CS4Report.append([" "," "," "," "])
            dataReport4 = array(CS4Report)                  
            Status.int.setGraphicsData("CS4_REPORT", dataReport4)


#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Panel CS5: Annual cost
        elif self.keys[0] == "CS5_Plot":

#............................................................................
# charge data from SQL

            Amortization = []
            ElCost = []

            FuelCost = [] # holds the fuels EnergyCost from ANo=0 to the ANo=last (all fuels)
            for i in range(1,len(generalData)):
                sumcost = 0.0
                sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%\
                           (Status.PId,generalData[i].AlternativeProposalNo)
                fuelsByANo = Status.DB.qfuel.sql_select(sqlQuery)
                for fuel in fuelsByANo:
                    fuelcost = fuel['FuelCostYear']
                    if fuelcost is None:
                        fuelcost = 0.0
                    else:
                        pass                       
                    sumcost += fuelcost
                FuelCost.append(sumcost)
#            print 'FuelCost =', FuelCost 

            EnergyCost = []
            OMCost = []
            Alternative = []

            CS5Table = []
            CS5Plot = []

            Amortization0 = 0
            OMCost0 = 0
            EnergyCost0 = 0

            for ANo in range(len(generalData)-1):
                i = ANo+1

                if salternatives[i].ShortName is None:
                    Alternative.append('--')
                else:
                    Alternative.append(str(salternatives[i].ShortName))

                if generalData[i].Amortization is None: #protection against None
                    Amortization.append(0.0)
                else:
                    Amortization.append(generalData[i].Amortization)

                if generalData[i].OMThermal is None: #here O&M costs for heat/cold generation and dist. considered
                    OMCost.append(0.0)
                else:
                    OMCost.append(generalData[i].OMThermal)

                if qelectricity[i].ElCostYearTot is None:
                    ElCost.append(0.0)
                else:
                    ElCost.append(qelectricity[i].ElCostYearTot)

##                if qfuel[i].FuelCostYear is None:
##                    FuelCost.append(0.0)
##                else:
##                    FuelCost.append(qfuel[i].FuelCostYear)


#                EnergyCost.append(ElCost[i-1]+FuelCost[i-1])#to i-1 (list from 0 to ANo)
        
                if generalData[i].EnergySystemCost is None:
                    EnergyCost.append(0.0)
                else:
                    EnergyCost.append(generalData[i].EnergySystemCost)
                
                if salternatives[i].StatusECO > 0: #SD: changed control 13/07/2008
                    dAmortization = generalData[i].Amortization
                    if dAmortization is None:
                        dAmortization = 0.0
                        dAmortization_Table = "---"
                    else:
                        dAmortization_Table = dAmortization

                    dOMCost = generalData[i].OMThermal
                    if dOMCost is None:
                        dOMCost = 0.0
                        dOMCost_Table = "---"
                    else:
                        dOMCost_Table = dOMCost

                    dEnergyCost = EnergyCost[i-1]#to i-1 (list from 0 to ANo)
                    if dEnergyCost == 0.0:
                        dEnergyCost_Table = "--"
                    else:
                        dEnergyCost_Table = dEnergyCost
  
                    if ANo == 0:
                        Amortization0 = dAmortization
                        OMCost0 = dOMCost
                        EnergyCost0 = dEnergyCost


                else:
                    dAmortization = 0.0
                    dOMCost = 0.0
                    dEnergyCost = 0.0
                    dAmortization_Table = "---"
                    dOMCost_Table = "---"
                    dEnergyCost_Table = "---"  
                    

                tableEntry = noneFilter([str(salternatives[i].ShortName),
                                         dAmortization_Table,dEnergyCost_Table,dOMCost_Table])

                plotEntry = noneFilter([str(salternatives[i].ShortName),dAmortization,dEnergyCost,dOMCost])
               
                CS5Table.append(tableEntry)
                CS5Plot.append(plotEntry)
#..............................................................................
# then send everything to the GUI

            data1 = array(CS5Table)
                              
            Status.int.setGraphicsData("CS5_Table", data1)

            data2 = array(CS5Plot)

            Status.int.setGraphicsData("CS5_Plot", data2)

            CS5Report = copy.deepcopy(CS5Table)
            for i in range(len(CS5Table),11):
                CS5Report.append([" "," "," "," "])
            dataReport5 = array(CS5Report)                  
            Status.int.setGraphicsData("CS5_REPORT", dataReport5)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Panel CS6: Annual cost
        elif self.keys[0] == "CS6_Plot":

#............................................................................
# charge data from SQL

            EnergyCost = []
            PEC = []
            AdditCost = []
            AdditCost_Table = []
            AdditCostSavedPEC = []#SD check
            AdditCostSavedPEC_Table = []#SD check
            SavedPEC = []
            Alternative = []

            CS6Table = []
            CS6Plot = []


            PEC0 = 0.0
            EnergyCost0 = 0.0

            for ANo in range(len(generalData)-1):
                i = ANo+1

                if salternatives[i].ShortName is None:
                    Alternative.append('--')
                else:
                    Alternative.append(str(salternatives[i].ShortName))

                if generalData[i].EnergyCost is None: #protection against None
                    EnergyCost.append(0.0)
                else:
                    EnergyCost.append(generalData[i].EnergyCost)

                if salternatives[i].StatusEnergy > 0 and salternatives[i].StatusECO > 0:
                    print 'ANo = "%s"  PEC = "%s"',(generalData[i].AlternativeProposalNo,generalData[i].PEC)
                    dPEC = generalData[i].PEC                
                    if dPEC is None:
                        dPEC = 0.0
                    else:
                        dPEC /= 1000.0  #conversion kWh -> MWh

                    dEnergyCost = generalData[i].EnergyCost
                    if dEnergyCost is None:
                        dEnergyCost = 0.0
                        dEnergyCost_Table = "---"
                    else:
                        dEnergyCost_Table = dEnergyCost
                    
                    if ANo == 0:
                        PEC0 = dPEC
                        EnergyCost0 = dEnergyCost


                    PECSaving = PEC0 - dPEC

       
                    AddCost = dEnergyCost - EnergyCost0
                    if dEnergyCost_Table == "---":
                        AddCost_Table = "---"
                    else:
                        AddCost_Table = AddCost


                    if PECSaving == 0.0:
                        AddCostSavedPEC = 0.0
                        AddCostSavedPEC_Table = "---"
                    else:
                        AddCostSavedPEC = AddCost/PECSaving
                        AddCostSavedPEC_Table = AddCostSavedPEC
   

                else:
                    dPEC = 0.0
                    PECSaving = 0.0
                    dEnergyCost = 0.0
                    AddCost = 0.0
                    AddCostSavedPEC = 0.0
                    dEnergyCost_Table = "---"
                    AddCost_Table = "---"
                    AddCostSavedPEC_Table = "---"
                        
                PEC.append(dPEC)
                SavedPEC.append(PECSaving)
                AdditCost.append(AddCost)
                AdditCost_Table.append(AddCost_Table)#SD check

                AdditCostSavedPEC.append(AddCostSavedPEC)#SD check


                tableEntry = noneFilter([str(salternatives[i].ShortName),
                                         dEnergyCost_Table,AddCost_Table,AddCostSavedPEC_Table])

                plotEntry = noneFilter([str(salternatives[i].ShortName),AddCostSavedPEC])
               
                CS6Table.append(tableEntry)
                CS6Plot.append(plotEntry)
#..............................................................................
# then send everything to the GUI
            print 'AdditCost_Table =', AdditCost_Table
            print 'PEC =', PEC
            print 'AdditCostSavedPEC_Table =', AdditCostSavedPEC_Table
            print '\n'
            print 'AdditCost =', AdditCost
            print 'SavedPEC =', SavedPEC
            print 'PEC =', PEC
            print 'AdditCostSavedPEC =', AdditCostSavedPEC          

            data1 = array(CS6Table)
                              
            Status.int.setGraphicsData("CS6_Table", data1)

            data2 = array(CS6Plot)

            Status.int.setGraphicsData("CS6_Plot", data2)

            CS6Report = copy.deepcopy(CS6Table)
            for i in range(len(CS6Table),11):
                CS6Report.append([" "," "," "," "])
            dataReport6 = array(CS6Report)                  
            Status.int.setGraphicsData("CS6_REPORT", dataReport6)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Panel CS7: Annual cost
        elif self.keys[0] == "CS7_Plot":

#............................................................................
# charge data from SQL

            IRR = []
            IRR_Table = []
            Alternative = []

            CS7Table = []
            CS7Plot = []


            for ANo in range(len(generalData)-1):
                i = ANo+1

                if salternatives[i].ShortName is None:
                    Alternative.append('--')
                else:
                    Alternative.append(str(salternatives[i].ShortName))

                if salternatives[i].StatusECO > 0:
                    dIRR = generalData[i].IRR                
                    if dIRR is None:
                        dIRR = 0.0
                        dIRR_Table = "---"
                    else:
                        dIRR_Table = dIRR

                else:
                    dIRR = 0.0
                    dIRR_Table = "---"
                        
                IRR.append(dIRR)
                IRR_Table.append(dIRR_Table)

                tableEntry = noneFilter([str(salternatives[i].ShortName),dIRR_Table])

                plotEntry = noneFilter([str(salternatives[i].ShortName),dIRR])
               
                CS7Table.append(tableEntry)
                CS7Plot.append(plotEntry)
#..............................................................................
# then send everything to the GUI

            data1 = array(CS7Table)
                              
            Status.int.setGraphicsData("CS7_Table", data1)

            data2 = array(CS7Plot)

            Status.int.setGraphicsData("CS7_Plot", data2)

            CS7Report = copy.deepcopy(CS7Table)
            for i in range(len(CS7Table),10):
                CS7Report.append([" "," "])
            dataReport7 = array(CS7Report)                  
            Status.int.setGraphicsData("CS7_REPORT", dataReport7)

#------------------------------------------------------------------------------
# Summary for report
        elif self.keys[0] == "Summary":
            qq = Status.DB.sproject.ProjectID[Status.PId]
            if len(qq) > 0:
                summary = qq[0].Summary
            else:
                summary = _(" ")

            Status.int.setGraphicsData("SUMMARY",array([[summary]]))

# build summary table

            if Status.FinalAlternative is not None:
                ANoList = [0,int(Status.FinalAlternative),None]
            else:
                ANoList = [0,-1,None]
            for ANo in range(1,len(generalData)-1):
                if ANo <> Status.FinalAlternative:
                    ANoList.append(ANo)
            
            summaryTable = []
                             
            for ANo in ANoList:

                if ANo is None:
                    row = [_("Other possible alternatives studied:"),
                           " "," "," "]
                elif ANo == -1:
                    row = [_("No alternative selected"),
                           " "," "," "]
                else:
                    row = []
                    i = ANo + 1

                    if salternatives[i].ShortName is None:
                        row.append('---')
                    else:
                        row.append(salternatives[i].ShortName)

                    if generalData[i].TotalInvCost is None: #protection against None
                        row.append('---')
                    else:
                        row.append(generalData[i].TotalInvCost)

                    if generalData[i].EnergyCost is None: #protection against None
                        row.append('---')
                    else:
                        row.append(generalData[i].EnergyCost)
            
                    if generalData[i].PEC is None: #protection against None
                        row.append('---')
                    else:
                        row.append(generalData[i].PEC/1000.0)

                summaryTable.append(row)

            Status.int.setGraphicsData("SUMMARY_TABLE", array(summaryTable))

                

#==============================================================================            
