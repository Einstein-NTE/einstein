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

from moduleEA1 import ModuleEA1
from moduleEA2 import ModuleEA2
from moduleEA3 import ModuleEA3
from moduleEA4 import ModuleEA4
from moduleEA5 import ModuleEA5

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP

from einstein.modules.fluids import *
import wx


class ModuleEA(object):

    def __init__(self):
        print "ModuleEA (__init__)"
        pass

#------------------------------------------------------------------------------
    def update(self):
#------------------------------------------------------------------------------
#       updates all the energyStatistics needed for the energyStatisticsDisplay
#       - called from PanelCC 
#------------------------------------------------------------------------------

        logTrack("ModuleEA (update): StatusEnergy %s"%Status.StatusEnergy)
        if Status.StatusCC > 0:
            Status.processData.createYearlyDemand()
            
        if Status.StatusEnergy == 0:
            if Status.ANo > 0:
                logMessage(_("EINSTEIN running system simulation for updating energy balances"))
                logMessage(_("This may take a while. please be patient ..."))
                wx.SafeYield()
                Status.mod.moduleEnergy.runSimulation()
            logMessage(_("EINSTEIN now updating annual energy balances"))
            self.calculateEquipmentEnergyBalances()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updateForReport(self):
#------------------------------------------------------------------------------
#       updates all the energyStatistics needed for the report        
#------------------------------------------------------------------------------
        self.calculateAnnualResults()
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

#------------------------------------------------------------------------------
    def calculateAnnualResults(self):
#------------------------------------------------------------------------------
#   calculates the full statistics based on the results from the consistency
#   check
#------------------------------------------------------------------------------

        ea1 = ModuleEA1()
        ea2 = ModuleEA2()
        ea3 = ModuleEA3()
        ea4 = ModuleEA4()
        ea5 = ModuleEA5()


#------------------------------------------------------------------------------
    def calculateEquipmentEnergyBalances(self):
#------------------------------------------------------------------------------
#   calculates the annual fuel balances from the results of system simulations
#   and stores the within the SQL tables
#------------------------------------------------------------------------------
        
        logTrack("ModuleEA (calculateEquipmentEnergyBalances)")
        
        (projectData,generalData) = Status.prj.getProjectData()
        equipments = Status.prj.getEquipments() 
        fuels = Status.prj.getQFuels()
        fuelList = Status.prj.getQFuelList("DBFuel_id")
        
        electricities = Status.prj.getElectricity()
        if len(electricities) > 0:
            electricity = electricities[0]
        else:
            logDebug("Corrupt entry in electricity table -> no data found for PId %s ANo %s"%(Status.PId,Status.ANo))

#..............................................................................
# Update of FETi/FECi values based on equipment fuel consumption FETj
# Carried out only if ANo > 0. For ANo = 0 comes from consistency check

        if Status.ANo > 0:
        
            if Status.int.cascadeUpdateLevel < len(equipments):
                logTrack("ModuleEA (calcEq.En.Bal.): calling runSimulation before updating energy balances")
                Status.mod.moduleEnergy.runSimulation()
                
            FETi = []
            for fuel in fuels:
                FETi.append(0.0)
                
            FETiUnKnown = 0.0
            FETel = 0.0
            FETFuel = 0.0
            FETHeat = 0.0
            FET = 0.0

            USH = 0.0
            QHX = 0.0
            QWH = 0.0

            for equipe in equipments:
                jc = equipe.CascadeIndex -  1
                dFETFuel = Status.int.FETFuel_j[jc]
                dFETel = Status.int.FETel_j[jc]
                dFETHeat = 0.0  #to be added once needed
                dUSH = Status.int.USHj[jc]
                dQHX = Status.int.QHXj[jc]
                dQWH = Status.int.QWHj[jc]

                equipe.FETFuel_j = dFETFuel
                equipe.FETel_j = dFETel
                equipe.FETHeat_j = dFETHeat
                equipe.FETj = dFETel + dFETFuel + dFETHeat #simple sum of fuel + electricity. doesn't make very much sense, but ... 

                print "CalcEqEnBal: equipe = %s ci = %s FET = %s "%\
                      (equipe.Equipment,equipe.CascadeIndex,equipe.FETj)
                equipe.USHj = dUSH
                equipe.QHXj = dQHX       
                equipe.QWHj = dQWH

                FET += dFETFuel + dFETel
                FETFuel += dFETFuel
                FETel += dFETel
                FETHeat += dFETHeat

                USH += dUSH
                QHX += dQHX
                QWH += dQWH

                fuelID = equipe.DBFuel_id
                if fuelID in fuelList:
                    i = fuelList.index(fuelID)
                    FETi[i] += dFETFuel
                else:
                    FETiUnKnown += dFETFuel
                    print "WARNING: fuel type for equipe %s is not known"

#..............................................................................
# calculate derived quantities and store in equipment table

            for equipe in equipments:
                jc = equipe.CascadeIndex -  1

                if equipe.FETFuel_j > 0:
                    equipe.HCGTEffReal = Status.int.USHj[jc] / equipe.FETFuel_j
                elif equipe.FETHeat_j > 0:
                    equipe.HCGTEffReal = Status.int.USHj[jc] / equipe.FETHeat_j
                elif equipe.FETel_j > 0:
                    equipe.HCGTEffReal = Status.int.USHj[jc] / equipe.FETel_j
                else:
                    equipe.HCGTEffReal = 0.0

                if equipe.HCGPnom > 0:
                    equipe.PartLoad = Status.int.USHj[jc]/equipe.HCGPnom
                else:
                    equipe.PartLoad = 0.0

            #HCGEEff -> only for CHP ??? or also for electrically driven chillers ???


            #TExhaustGas ????

    ##### TAKE CARE: here HCGTEfficiency is both an input and a result ... for equipments with
    ##### variable COP depending on temperature / ... this may lead to confusions.

#..............................................................................
# now store fuel and electricity consumption in the corresponding tables

            FETFuels = 0.0
            for fuel in fuels:
                i = fuel.FuelNo - 1
                fuel.FETFuel = FETi[i]
                FETFuels += FETi[i]
                if fuel.FEOFuel is not None:
                    fuel.FECFuel = FETi[i] + fuel.FEOFuel
                else:
                    fuel.FECFuel = FETi[i]
                    fuel.FEOFuel = 0.0
                    logDebug("ModuleEA (calculateEqEnergyBalances): no entry found for FEOFuel of fuel no. %s"%(i+1))

            generalData.FETel = FETel
            if generalData.FEOel is not None:
                generalData.FECel = FETel + generalData.FEOel
                electricity.ElectricityTotYear = generalData.FECel
            else:
                generalData.FECel = FETel
                generalData.FEOel = 0.0
                electricity.ElectricityTotYear = generalData.FECel
                logDebug("ModuleEA (cEEBalances): No entry found in FEOel. Set to zero !!!")

            generalData.FET = FET  #total FET as simple sum
            generalData.USH = USH  #total USH


#..............................................................................
#..............................................................................
#..............................................................................
# in case of present state:
# some global derived quantities that are not calculated in the CCheck module

        else:
            if generalData.USH > 0 and generalData.UPH is not None:
                UPH = generalData.UPH
                USH = generalData.USH
                generalData.HDEffAvg = UPH/USH
                if UPH/USH < 0.5:
                    logWarning(_("ModuleEA (calcEq.En.Bal): check your input data.\ncalculated distribution efficiency is less than 50 %"))
            else:
                logTrack("ModuleEA (calcEq.En.Bal): Error in UPH/USH data. cannot calculate distribution efficiency")
                generalData.HDEffAvg = 0.0

#..............................................................................
# from here on actions also for ANo = 0
#..............................................................................
#..............................................................................
#..............................................................................

#..............................................................................
# conversion to primary energy and environmental impact parameters

        if generalData.PEConvEl is None:
            generalData.PEConvEl = 3.0
            showWarning(_("No conversion factor electricity - primary energy was specified.\default value 3.0 assumed"))

        generalData.PETel = generalData.FETel * generalData.PEConvEl
        generalData.PECel = generalData.FECel * generalData.PEConvEl

        if generalData.CO2ConvEl is None:
            generalData.CO2ConvEl = 0.5
            showWarning(_("No conversion factor electricity - CO2 emission was specified.\default value 0.5 t/MWh assumed"))

        generalData.ProdCO2el = generalData.FECel * generalData.CO2ConvEl

        if generalData.NoNukesConvEl is None:
            generalData.NoNukesConvEl = 5.00
            showWarning(_("No conversion factor electricity - HR nuclear waste was specified.\default value 5.0 g/MWh assumed (15 % nuclear)"))

        generalData.ProdNoNukesEl = generalData.FECel * generalData.NoNukesConvEl

        PETFuels = 0.0
        PECFuels = 0.0
        ProdCO2Fuels = 0.0
        
        for fuel in fuels:
            i = fuel.FuelNo - 1
            f = Fuel(fuel.DBFuel_id)
            
            dPET = fuel.FETFuel * f.PEConv
            dPEC = fuel.FECFuel * f.PEConv
            dCO2 = fuel.FECFuel * f.CO2Conv

            fuel.PETFuel = dPET
            fuel.PECFuel = dPEC
            fuel.ProdCO2Fuel = dCO2

            PETFuels += dPET
            PECFuels += dPEC
            ProdCO2Fuels += dCO2

        generalData.PETFuels = PETFuels
        generalData.PECFuels = PECFuels
        generalData.ProdCO2Fuels = ProdCO2Fuels

        generalData.PEC = generalData.PECFuels + generalData.PECel
        generalData.PET = generalData.PETFuels + generalData.PETel

#..............................................................................
# set Status flag indicating that ANNUAL energy balances for the present alternative
# are up to date

        Status.prj.setStatus("Energy")
        Status.SQL.commit()
            
        
#==============================================================================
