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
from einstein.GUI.GUITools import check

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

        qq = Status.DB.questionnaire.Questionnaire_ID[Status.PId]
        if len(qq) > 0:
            questionnaire = qq[0]
        else:
            questionnaire = None

######XXX TEST TEST TEST TEST TEST ###########################################3
        Status.StatusECO = 1
        logDebug("ModuleCS: WARNING -- StatusECO always set to 1 !!!!")


        PEC = []

        PECTable = []
        PECPlot = []
        
#Panel CS1: Primary energy
        if self.keys[0] == "CS1_Plot":
            
            PEC0 = 0.0

            presentAlternative = Status.ANo
                    
            for ANo in range(len(generalData)-1):
                i = ANo+1

                if salternatives[i].StatusEnergy == 0:
                    Status.prj.setActiveAlternative(ANo)
                    Status.mod.moduleEA.update()

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
                    tableEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),dPEC_Table,PECSaving,RelSaving*100])
                else:
                    tableEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),dPEC_Table,"---","---"])
                plotEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),dPEC])
                
                PECTable.append(tableEntry)
                PECPlot.append(plotEntry)
                            
            if Status.ANo <> presentAlternative:
                Status.prj.setActiveAlternative(presentAlternative)
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
                    Alternative.append(unicode(salternatives[i].ShortName,"utf-8"))

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
                    tableEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),
                                             dUPH_Table,"---",
                                             dUSH_Table,"---"])
                else:
                    tableEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),
                                             dUPH_Table,UPHSaving,
                                             dUSH_Table,USHSaving])
                plotEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),RatioUSH,RatioUPH]) #SD: before: dUSH, dUPH

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
                    Alternative.append(unicode(salternatives[i].ShortName,"utf-8"))

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
                    

                tableEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),
                                         dCO2_Table,dNucWaste_Table,dWatConsum_Table])

                plotEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),RatioCO2,RatioNucWaste,RatioWatConsum])
               
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
                    Alternative.append(unicode(salternatives[i].ShortName,"utf-8"))

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

                
#                if salternatives[i].StatusECO > 0:
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


#            else:
#                dTotalCost = 0.0
#                dOwnCost = 0.0
#                dSubsidies = 0.0
#                dTotalCost_Table = "---"
#                dOwnCost_Table = "---"
#                dSubsidies_Table = "---"  
                

                tableEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),
                                         dTotalCost_Table,dOwnCost_Table,dSubsidies_Table])

#                plotEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),dOwnCost,dSubsidies])
                plotEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),dTotalCost,dOwnCost])
               
                CS4Table.append(tableEntry)
                CS4Plot.append(plotEntry)
#..............................................................................
# then send everything to the GUI

            data1 = array(CS4Table)
                              
            Status.int.setGraphicsData("CS4_Table", data1)

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

            print "CS5"
#............................................................................
# charge data from SQL

            Amortization = []
            ElCost = []

            FuelCost = [] # holds the fuels EnergyCost from ANo=0 to the ANo=last (all fuels)

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
                    Alternative.append(unicode(salternatives[i].ShortName,"utf-8"))

                if generalData[i].Amortization is None: #protection against None
                    Amortization.append(0.0)
                else:
                    Amortization.append(generalData[i].Amortization)

##### 2B CHECKED ... AT THE MOMENT OMTHERMAL FOR ANo = 0 IS IN QUESTIONNAIRE !!!
                if ANo == 0:
                    qq = Status.DB.questionnaire.Questionnaire_ID[Status.PId]
                    if len(qq) > 0:
                        generalData[i].OMThermal = check(qq[0].OMThermal)
                    
                if generalData[i].OMThermal is None: #here O&M costs for heat/cold generation and dist. considered
                    if ANo == 0:
                        logWarning(_("No OandM cost specified for present state"))
                    OMCost.append(0.0)
                else:
                    OMCost.append(generalData[i].OMThermal)

                if qelectricity[i].ElCostYearTot is None:
                    if ANo == 0:
                        logWarning(_("No electricity cost specified for present state"))
                        
                    ElCost.append(0.0)
                else:
                    ElCost.append(qelectricity[i].ElCostYearTot)

                sumcost = 0.0
                sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%\
                           (Status.PId,ANo)
                fuelsByANo = Status.DB.qfuel.sql_select(sqlQuery)
                for fuel in fuelsByANo:
                    fuelcost = fuel['FuelCostYear']
                    if fuelcost is not None:
                        sumcost += fuelcost
                    else:
                        if ANo == 0:
                            logWarning(_("No fuel cost specified for  for present state for fuel no. %s ")%fuel.FuelNo)
                FuelCost.append(sumcost)

                if ANo == 0:
                    EnergyCost.append(ElCost[i-1]
                                      +FuelCost[i-1])

                else:
                    if generalData[i].EnergyCost is None:
                        EnergyCost.append(0.0)
                    else:
                        EnergyCost.append(generalData[i].EnergyCost)
                
#                if salternatives[i].StatusECO > 0: #SD: changed control 13/07/2008
                dAmortization = generalData[i].Amortization
                if dAmortization is None:
                    dAmortization = 0.0
                    dAmortization_Table = "---"
                else:
                    dAmortization_Table = dAmortization

                dOMCost = OMCost[ANo]
                if dOMCost is None or dOMCost == 'NULL':
                    dOMCost = 0.0
                    dOMCost_Table = "---"
                else:
                    dOMCost_Table = dOMCost
                print "dOMCost = ",dOMCost,dOMCost_Table

                dEnergyCost = EnergyCost[ANo]#to i-1 (list from 0 to ANo)
                if dEnergyCost == 0.0:
                    dEnergyCost_Table = "--"
                else:
                    dEnergyCost_Table = dEnergyCost

                if ANo == 0:
                    Amortization0 = dAmortization
                    OMCost0 = dOMCost
                    EnergyCost0 = dEnergyCost


#            else:
#                dAmortization = 0.0
#                dOMCost = 0.0
#                dEnergyCost = 0.0
#                dAmortization_Table = "---"
#                dOMCost_Table = "---"
#                dEnergyCost_Table = "---"  
                

            
                tableEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),
                                         dAmortization_Table,dEnergyCost_Table,dOMCost_Table])

                plotEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),\
                                        dAmortization+dEnergyCost+dOMCost,\
                                        dEnergyCost+dOMCost,\
                                        dOMCost])
               
                CS5Table.append(tableEntry)
                CS5Plot.append(plotEntry)

# economic parameters used in the analysis (for the report)

            if questionnaire is not None:
                if questionnaire.InterestExtFinancing is not None:
                    i = questionnaire.InterestExtFinancing
                else:
                    i = 0.06
                    
                if questionnaire.AmortisationTime is not None:
                    N = int(questionnaire.AmortisationTime)
                else:
                    N = 15
            else:
                i = 0.06
                N = 15

            sum = 0
            for n in range(1,N+1):
                sum += 1/pow(1.0+i,n)

            if sum > 0:
                annuity = 1./sum
            else:
                annuity = 1.0
                
            ecopars = [i*100.0,
                       N,
                       annuity*100.0]
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

            Status.int.setGraphicsData("CS5_REPORT_PARS", array(ecopars))

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Panel CS6: Annual cost
        elif self.keys[0] == "CS6_Plot":

#............................................................................
# charge data from SQL

            EnergySystemCost = []
            PEC = []
            AddedCost = []
            AddedCost_Table = []
            AddedCostSavedPEC = []#SD check
            AddedCostSavedPEC_Table = []#SD check
            SavedPEC = []
            Alternative = []

            CS6Table = []
            CS6Plot = []


            PEC0 = 0.0
            EnergySystemCost0 = 0.0

            for ANo in range(len(generalData)-1):
                i = ANo+1

                if salternatives[i].ShortName is None:
                    Alternative.append('--')
                else:
                    Alternative.append(unicode(salternatives[i].ShortName,"utf-8"))

                if generalData[i].EnergySystemCost is None: #protection against None
                    EnergySystemCost.append(0.0)
                else:
                    EnergySystemCost.append(generalData[i].EnergySystemCost)

#                if salternatives[i].StatusEnergy > 0 and salternatives[i].StatusECO > 0:
                if salternatives[i].StatusEnergy > 0:
                    dPEC = generalData[i].PEC                
                    if dPEC is None:
                        dPEC = 0.0
                    else:
                        dPEC /= 1000.0  #conversion kWh -> MWh

                    dEnergySystemCost = generalData[i].EnergySystemCost
                    if dEnergySystemCost is None:
                        dEnergySystemCost = 0.0
                        dEnergySystemCost_Table = "---"
                    else:
                        dEnergySystemCost_Table = dEnergySystemCost
                    
                    if ANo == 0:
                        PEC0 = dPEC
                        EnergySystemCost0 = dEnergySystemCost


                    PECSaving = PEC0 - dPEC

       
                    AddCost = dEnergySystemCost - EnergySystemCost0
                    if dEnergySystemCost_Table == "---":
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
                    dEnergySystemCost = 0.0
                    AddCost = 0.0
                    AddCostSavedPEC = 0.0
                    dEnergySystemCost_Table = "---"
                    AddCost_Table = "---"
                    AddCostSavedPEC_Table = "---"
                        
                PEC.append(dPEC)
                SavedPEC.append(PECSaving)
                AddedCost.append(AddCost)
                AddedCost_Table.append(AddCost_Table)#SD check

                AddedCostSavedPEC.append(AddCostSavedPEC)#SD check


                tableEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),
                                         dEnergySystemCost_Table,AddCost_Table,AddCostSavedPEC_Table])

                plotEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"),AddCostSavedPEC])
               
                CS6Table.append(tableEntry)
                CS6Plot.append(plotEntry)
#..............................................................................
# then send everything to the GUI
#            print 'AddedCost_Table =', AddedCost_Table
#            print 'PEC =', PEC
#            print 'AddedCostSavedPEC_Table =', AddedCostSavedPEC_Table
#            print '\n'
#            print 'AddedCost =', AddedCost
#            print 'SavedPEC =', SavedPEC
#            print 'PEC =', PEC
#            print 'AddedCostSavedPEC =', AddedCostSavedPEC          

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
            PayBack = []
            PayBack_Table = []
            BCR = []
            BCR_Table = []
            
            Alternative = []

            CS7Table = []
            CS7Plot = []


            for ANo in range(len(generalData)-1):
                i = ANo+1

                if salternatives[i].ShortName is None:
                    Alternative.append('--')
                else:
                    Alternative.append(unicode(salternatives[i].ShortName,"utf-8"))

#### TEST TEST TEST TEST ###################
                salternatives[i].StatusECO = 1
                if salternatives[i].StatusECO > 0:
                    dIRR = generalData[i].IRR
                    dBCR = generalData[i].BCR
                    dPayBack = generalData[i].PayBack
                    if dIRR is None:
                        dIRR = 0.0
                        dIRR_Table = "---"
                    else:
                        dIRR *= 100
                        dIRR_Table = dIRR

                    if dPayBack is None:
                        dPayBack = 0.0
                        dPayBack_Table = "---"
                    else:
                        dPayBack_Table = dPayBack

                    if dBCR is None:
                        dBCR = 0.0
                        dBCR_Table = "---"
                    else:
                        dBCR_Table = dBCR


                else:
                    dIRR = 0.0
                    dIRR_Table = "---"
                    dPayBack = 0.0
                    dPayBack_Table = "---"
                    dBCR = 0.0
                    dBCR_Table = "---"
                        
                IRR.append(dIRR)
                IRR_Table.append(dIRR_Table)

                PayBack.append(dPayBack)
                PayBack_Table.append(dPayBack_Table)

                BCR.append(dBCR)
                BCR_Table.append(dBCR_Table)

                tableEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"), \
                                         dIRR_Table,dPayBack_Table,dBCR_Table])

                plotEntry = noneFilter([unicode(salternatives[i].ShortName,"utf-8"), \
                                        dIRR])
               
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
                CS7Report.append([" "," "," "," "])
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
