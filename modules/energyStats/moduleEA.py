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
from GUITools import *  #for the check function

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
                logWarning("WARNING: present standard report is limited to 80 temperature intervals !!!")

        for iT in range(Status.NT+1,81):
                tableReport.append([" ",                             
                                    " ",                             
                                    " ",                             
                                    " "])                            



        Status.int.setGraphicsData("PROCHEATTEMP", array(tableReport))

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
            ElGen = 0.0
            FETFuel = 0.0
            FETHeat = 0.0
            FET = 0.0

            USH = 0.0
            QHX = 0.0
            QWH = 0.0

            for equipe in equipments:
                jc = equipe.CascadeIndex -  1
                dFETFuel = Status.int.FETFuel_j[jc]

                if dFETFuel is None:
                    logDebug("ModuleEA (cEEB): FETFuel of equipment %s (cascadeIndex = %s) is None"%\
                             (equipe.EqNo,equipe.CascadeIndex))
                    dFETFuel = 0.0
                    
                dFETel = Status.int.FETel_j[jc]

                if dFETel is None:
                    logDebug("ModuleEA (cEEB): FETel of equipment %s (cascadeIndex = %s) is None"%\
                             (equipe.EqNo,equipe.CascadeIndex))
                    dFETel = 0.0

                if equipe.HCGEEfficiency > 0:
                    dElGen = Status.int.ElGen_j[jc]
                else:
                    dElGen = 0.0
                if dElGen is None:
                    dElGen = 0.0
                
                dFETHeat = 0.0  #to be added once needed
                dUSH = Status.int.USHj[jc]
                dQHX = Status.int.QHXj[jc]
                dQWH = Status.int.QWHj[jc]

                equipe.FETFuel_j = dFETFuel
                equipe.FETel_j = dFETel
                
                if equipe.HCGEEfficiency > 0:
                    equipe.STAreaFactor = dElGen   #XXXXXXtemporarily STAreaFactor used as storage for ElGen
                    
                equipe.FETHeat_j = dFETHeat
                equipe.FETj = dFETel + dFETFuel + dFETHeat #simple sum of fuel + electricity. doesn't make very much sense, but ... 

                equipe.USHj = dUSH
                equipe.QHXj = dQHX       
                equipe.QHXEq = dQHX    #redundancy in nomenclature ... should be unified ... !!!
                equipe.QWHj = dQWH
                equipe.QWHEq = dQWH
                equipe.QExhaustGas = dQWH

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
                    logWarning("Fuel type for equipe %s is not known"%equipe.Equipment)

#..............................................................................
#..............................................................................

                
#..............................................................................
# calculate derived quantities and store in equipment table

            for equipe in equipments:
                jc = equipe.CascadeIndex -  1

# average thermal conversion efficiency
                if equipe.FETFuel_j > 0:
                    equipe.HCGTEffReal = Status.int.USHj[jc] / equipe.FETFuel_j
                elif equipe.FETHeat_j > 0:
                    equipe.HCGTEffReal = Status.int.USHj[jc] / equipe.FETHeat_j
                elif equipe.FETel_j > 0:
                    equipe.HCGTEffReal = Status.int.USHj[jc] / equipe.FETel_j
                else:
                    equipe.HCGTEffReal = 0.0

# real operating hours
                equipe.HPerYearEq = Status.int.HPerYearEq[jc]
                
# part load factor
                if equipe.HCGPnom is not None:
                    if equipe.HPerYearEq is not None:
                        USHmax = equipe.HPerYearEq*equipe.HCGPnom 
                        if USHmax > 0:
                            equipe.PartLoad = Status.int.USHj[jc]/USHmax
                        else:
                            equipe.PartLoad = 0.0
                    else:
                        equipe.PartLoad = 1.0
                        if equipe.HCGPnom > 0:
                            equipe.HPerYearEq = Status.int.USHj[jc]/equipe.HCGPnom
                        else:
                            equipe.HPerYearEq = 0.0
                else:
                    equipe.PartLoad = 0.0


# part load factor
            #HCGEEff -> only for CHP ??? or also for electrically driven chillers ???

    ##### TAKE CARE: here HCGTEfficiency is both an input and a result ... for equipments with
    ##### variable COP depending on temperature / ... this may lead to confusions.

#..............................................................................
# now store fuel and electricity consumption in the corresponding tables

            FETFuels = 0.0
            FECFuels = 0.0
            
            for fuel in fuels:
                i = fuel.FuelNo - 1
                fuel.FETFuel = FETi[i]
                FETFuels += FETi[i]
                FECFuels += FETi[i]
                if fuel.FEOFuel is not None:
                    fuel.FECFuel = FETi[i] + fuel.FEOFuel
                    FECFuels += fuel.FEOFuel
                else:
                    fuel.FECFuel = FETi[i]
                    fuel.FEOFuel = 0.0
                    logDebug("ModuleEA (calculateEqEnergyBalances): no entry found for FEOFuel of fuel no. %s"%(i+1))

                if fuel.FECFuel is not None and fuel.QFuel_ID in fuelList:
                    fuelData = Fuel(fuel.QFuel_ID)
                    if fuelData.LCV is not None and fuelData.LCV > 0:
                        fuel.MFuelYear = fuel.FECFuel/fuelData.LCV
                        
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

            Status.int.USHTotal = USH
            Status.int.QWHEqTotal = QWH

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
            logWarning(_("No conversion factor electricity - primary energy was specified.\default value 3.0 assumed"))

        if generalData.FETel is None:
            logWarning(_("WARNING: No data available for electricity consumption for thermal uses. Set to 0 !!!"))
            generalData.FETel = 0.0

        generalData.PETel = generalData.FETel * generalData.PEConvEl

        if generalData.FECel is None and generalData.FEOel is None:
            logWarning(_("WARNING: No data available for electricity consumption for non-thermal uses. Set to 0 !!!"))
            generalData.FECel = generalData.FETel
            generalData.FEOel = 0.0
            
        generalData.PECel = generalData.FECel * generalData.PEConvEl

        if generalData.CO2ConvEl is None:
            generalData.CO2ConvEl = 0.5
            logWarning(_("No conversion factor electricity - CO2 emission was specified.\default value 0.5 t/MWh assumed"))

        generalData.ProdCO2el = generalData.FECel * generalData.CO2ConvEl

        if generalData.NoNukesConvEl is None:
            generalData.NoNukesConvEl = 5.00
            logWarning(_("No conversion factor electricity - HR nuclear waste was specified.\default value 5.0 g/MWh assumed (15 % nuclear)"))

        generalData.ProdNoNukesEl = generalData.FECel * generalData.NoNukesConvEl

        PETFuels = 0.0
        PECFuels = 0.0
        ProdCO2Fuels = 0.0
        FECFuels = 0.0  # direct sum of fuel FECs -> used for SEC values only !!
        
        for fuel in fuels:
            i = fuel.FuelNo - 1
            f = Fuel(fuel.DBFuel_id)
            
            if fuel.FETFuel is None:
                logWarning(_("WARNING: No data available for fuel consumption for thermal uses (fuel no. %s). Set to 0 !!!")
                           %(i+1))
                fuel.FETFuel = 0.0

            if fuel.FECFuel is None:
                logWarning(_("WARNING: No data available for total fuel consumption (fuel no. %s). Set to 0 !!!")
                           %(i+1))
                fuel.FECFuel = 0.0

            dPET = fuel.FETFuel * f.PEConv
            dFEC = fuel.FECFuel
            dPEC = fuel.FECFuel * f.PEConv
            dCO2 = fuel.FECFuel * f.CO2Conv

            fuel.PETFuel = dPET
            fuel.PECFuel = dPEC
            fuel.ProdCO2Fuel = dCO2

            PETFuels += dPET
            PECFuels += dPEC
            ProdCO2Fuels += dCO2
            FECFuels += dFEC

        generalData.PETFuels = PETFuels
        generalData.PECFuels = PECFuels
        generalData.ProdCO2Fuels = ProdCO2Fuels

        generalData.PEC = generalData.PECFuels + generalData.PECel
        generalData.PET = generalData.PETFuels + generalData.PETel

#..............................................................................
# energy intensity and specific energy consumption

#Part 1: Energy Intensity

        Turnover = projectData.Turnover #in euros

        if (Turnover > 0) and Turnover is not None:    
            generalData.FUEL_INT = check(FECFuels/Turnover) 
            generalData.EL_INT = check(generalData.FECel/Turnover) 
            generalData.PE_INT = check(generalData.PEC/Turnover) 
        else:
            generalData.FUEL_INT = check(None)
            generalData.EL_INT = check(None)
            generalData.PE_INT = check(None)

#Part 2: SEC by products

        products = Status.prj.getProducts()

        if Status.ANo > 0: # distribution of energy consumption to products by proportion in turnover.
                    # could later on be improved taking into account the original distribution ...
                    
            sumTurnoverProd = 0.0
            for product in products:
                if product.TurnoverProd is not None: sumTurnoverProd += product.TurnoverProd

            for product in products:
                if sumTurnoverProd > 0:
                    if product.TurnoverProd is not None:
                        fTurnover = product.TurnoverProd / sumTurnoverProd
                    else:
                        fTurnover = 0.0
                else:
                    fTurnover = 1./len(products)

                quantity = product.QProdYear

                PEC = generalData.PEC
                if PEC is not None and quantity > 0 and quantity is not None:
                    product.PE_SEC = fTurnover*PEC/quantity
                else:
                    product.PE_SEC = 0.0

                FECel = generalData.FECel
                if FECel is not None and quantity > 0 and quantity is not None:
                    product.EL_SEC = fTurnover*FECel/quantity
                else:
                    product.EL_SEC = 0.0

                if FECFuels is not None and quantity > 0 and quantity is not None:
                    product.FUEL_SEC = fTurnover*FECFuels/quantity
                else:
                    product.FUEL_SEC = 0.0

#Part 3: SEC by unit operations

        processes = Status.prj.getProcesses()

        for process in processes:
            UPH = process.UPH
            try:
                quantity = process.VInFlowDay*process.NDaysProc
            except:
                quantity = 1.0
                
            if quantity > 0 and quantity is not None and UPH is not None: process.UPH_SEC = UPH/quantity
            else: process.UPH_SEC = 0.0
            process.PE_SEC = 0.0
            process.EL_SEC = 0.0

# back-up in SQL                                      
        Status.SQL.commit() #SD, to be checked


#..............................................................................
# set Status flag indicating that ANNUAL energy balances for the present alternative
# are up to date

        Status.prj.setStatus("Energy")
        Status.SQL.commit()
            
        
#==============================================================================
