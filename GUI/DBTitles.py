# -*- coding: iso-8859-15 -*-
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	DBTitles: dictionaries for text and units in the database editing window
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Stoyan Danov    19/06/2008
#
#       Revised by:         Tom Sobota      7/07/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes to previous version:
#        7/07/2008 TS  Syntax errors fixed.
#       13/10/2008: SD  change _U() to _U()
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

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

CHP = {
# 'Variable name':('Descriptive name text','Units')
    'DBCHP_ID':(_U('Identifier'),_U('-')),
    'ManData':(_U('Manufacturer data'),_U('-')),#SD: This is in the sense of "Sorce of information" ->change to Source??
    'Manufacturer':(_U('Manufacturer'),_U('-')),
    'Model':(_U('Model'),_U('-')),
    'DBFuel_id':(_U('Fuel type (identifier in fuel database)'),_U('-')),#foresee introduction from choice? (Tom)
    'FuelConsum':(_U('Fuel consumption'),_U('kW (LCV)')),#this should be given by user ??Hans
    'UnitsFuelConsum':(_U('Fuel units'),_U('-')),#foresee introduction from choice? (Tom),Hans
    'YearManufact':(_U('Year of manufacturing'),_U('-')),
    'Type':(_U('Type of equipment'),_U('-')),#foresee introduction from choice? (Tom)
    'SubType':(_U('Subtype of equipment'),_U('-')),#foresee introduction from choice? (Tom)
    'CHPPe':(_U('Electric power'),_U('kW')),
    'CHPPt':(_U('Thermal power'),_U('kW')),
##    'CHPFuelConsum':('Fuel consumption','[kW] (LCV)'),#SD These are redundant, eliminate them from DB draft
##    'UnitsFuelConsum': ('Units fuel consumption','-'),
    'Eta_e':(_U('Electric efficiency'),_U('-')),# 0-1 or % ??
    'Eta_t':(_U('Thermal efficiency'),_U('-')),# 0-1 or % ??
    'Thigh':(_U('High temperature at which energy can be delivered'),_('ºC')),
    'Tlow':(_U('Low temperature at which energy can be delivered'),_('ºC')),
    'PercentPowThigh':(_U('Percent of energy at high temperature'),_U('%')),
    'PercentPowTlow':(_U('Percent of energy at low temperature'),_U('%')),
    'EEEmin':(_U('Minimum electric efficiency by law'),_U('-')),
    'InvRate':(_U('Investment cost'),_U('€/kW_el')),
    'Price':(_U('Price'),_U('€')),
    'TurnKeyPrice':(_U('Turnkey price'),_U('€')),
    'OandMfix':(_U('Fixed Operation and Maintenance costs'),_U('€/kW_el year')),
    'OandMRvar':(_U('Variable Operation and Maintenance costs'),_U('€/kW_el')),
    'YearUpdate':(_U('Year of update'),_U('-'))
    }

HEATPUMP = {
    'DBHeatPump_ID':(_U('Identifier'),_U('-')),
    'HPManData':(_U('Manufacturer data'),_U('-')),
    'HPManufacturer':(_U('Manufacturer'),_U('-')),
    'HPModel':(_U('Model'),_U('-')),
    'DBFuel_id':(_U('Fuel type (identifier in fuel database)'),_U('-')),#foresee introduction from choice? (Tom)
    'HPFuelConsum':(_U('Fuel consumption'),_U('kW (LCV)')),#this should be given by user ??Hans
    'HPUnitsFuelConsum':(_U('Fuel units'),_U('-')),#foresee introduction from choice? (Tom),Hans
    'HPYearManufact':(_U('Year of manufacturing'),_U('year')),
    'HPType':(_U('Type'),_U('-')),
    'HPSubType':(_U('Sub-type'),_U('-')),
    'HPAbsEffects':(_U('Effects (absorption)'),_U('-')),
    'HPAbsHeatMed':(_U('Heating medium (absorption)'),_U('-')),
    'HPWorkFluid':(_U('Working fluid'),_U('-')),
    'HPCoolCap':(_U('Cooling capacity'),_U('kW')),
    'HPCoolCOP':(_U('Nominal cooling COP'),_U('-')),
    'HPExCoolCOP':(_U('Exergetic cooling COP'),_U('-')),
    'HPThCoolCOP':(_U('Theoretical cooling COP'),_U('-')),
    'HPConstExCoolCOP':(_U('Temperature range of constant exergetic COP application, cooling'),_('ºC')),
    'HPAbsTinC':(_U('Absorber inlet temperature, cooling mode'),_('ºC')),
    'HPCondTinC':(_U('Condenser inlet temperature, cooling mode'),_('ºC')),
    'HPGenTinC':(_U('Generator inlet temperature, cooling mode'),_('ºC')),
    'HPEvapTinC':(_U('Evaporator inlet temperature, cooling mode'),_('ºC')),
    'HPHeatCap':(_U('Heating capacity'),_U('kW')),
    'HPHeatCOP':(_U('Nominal heating COP'),_U('-')),
    'HPExHeatCOP':(_U('Exergetic heating COP'),_U('-')),
    'HPThHeatCOP':(_U('Theoretical heating COP'),_U('-')),
    'HPConstExHeatCOP':(_U('Temperature range of constant exergetic COP application, heating'),_('ºC')),
    'HPAbsTinH':(_U('Absorber inlet temperature, heating mode'),_('ºC')),
    'HPCondTinH':(_U('Condenser inlet temperature, heating mode'),_('ºC')),
    'HPGenTinH':(_U('Generator inlet temperature, heating mode'),_('ºC')),
    'HPEvapTinH':(_U('Evaporator inlet temperature, heating mode'),_('ºC')),
    'HPLimDT':(_U('Limit temperature difference'),_('ºC')),
    'HPGenTmin':(_U('Minimum generator temperature'),_('ºC')),
    'HPCondTmax':(_U('Maximum condensing temperature'),_('ºC')),
    'HPEvapTmin':(_U('Minimum evaporating  temperature'),_('ºC')),
    'HPElectConsum':(_U('Electricity consumption'),_U('kW')),
    'HPPrice':(_U('Equipment factory price'),_U('€')),
    'HPTurnKeyPrice':(_U('Turn-key price'),_U('€')),
    'HPOandMfix':(_U('Ratio for O&M costs (fixed)'),_U('€/kW year')),
    'HPOandMvar':(_U('Ratio for O&M costs (variable)'),_U('€/MWh year')),
    'HPYearUpdate':(_U('Year of last data update'),_U('year'))
    }


CHILLER = {
    'DBChiller_ID':(_U('Identifier'),_U('-')),
    'ManData':(_U('Manufacturer data is provided only for Heating (H), Cooling (C), or both (HC)'),_U('-')),
    'Manufacturer':(_U('Manufacturer'),_U('-')),
    'Model':(_U('Model'),_U('-')),
    'Type':(_U('Type of HP: compression or absorption'),_U('-')),
    'SubType':(_U('Heat source - Heat sink, e.g. water-water'),_U('-')),
    'AbsEffects':(_U('Only abs. HP: effects: 1, 2, or 3'),_U('-')),
    'AbsHeatMed':(_U('Only abs HP: Heating medium in generator:hot water, vapour, exhaust gas, directfired'),_U('-')),
    'WorkFluid':(_U('Absorbent-refrigerant pair, e.g. LiBr-H2O'),_U('-')),
    'CoolCap':(_U('Nominal Cooling capacity'),_U('kW')),
    'CoolCOP':(_U('Nominal COP cooling'),_U('-')),
    'ExCoolCOP':(_U('Exergetic COP cooling'),_U('-')),
    'ThCoolCOP':(_U('Theoretical COP cooling'),_U('-')),
    'ConstExCoolCOP':(_U('Temperature interval COPex is assumed constant, cooling'),_('ºC')),
    'AbsTinC':(_U('Absorber inlet temperature, cooling mode, catalogue (sec. fluid)'),_('ºC')),
    'CondTinC':(_U('Condenser inlet temperature, cooling mode, catalogue (sec. fluid)'),_('ºC')),
    'GenTinC':(_U('Generator inlet temperature, cooling mode, catalogue (sec. fluid)'),_('ºC')),
    'EvapTinC':(_U('Evaporator inlet temperature, cooling mode, catalogue (sec. fluid)'),_('ºC')),
    'HeatCap':(_U('Nominal Heating capacity'),_U('kW')),
    'HeatCOP':(_U('Nominal COP heating'),_U('-')),
    'ExHeatCOP':(_U('Exergetic COP heating'),_U('-')),
    'ThHeatCOP':(_U('Theoretical COP heating'),_U('-')),
    'ConstExHeatCOP':(_U('Temperature interval COPex is assumed constant, heating'),_('ºC')),
    'AbsTinH':(_U('Absorber inlet temperature, heating mode, catalogue (sec. fluid)'),_('ºC')),
    'CondTinH':(_U('Condenser inlet temperature, heating mode, catalogue (sec. fluid)'),_('ºC')),
    'GenTinH':(_U('Generator inlet temperature, heating mode, catalogue (sec. fluid)'),_('ºC')),
    'EvapTinH':(_U('Evaporator inlet temperature, heating mode, catalogue (sec. fluid)'),_('ºC')),
    'LimDT':(_U('Working Limit temperature difference (lift)'),_('ºC')),
    'GenTmin':(_U('Minimum generator temperature (primary)-work limit'),_('ºC')),
    'CondTmax':(_U('Maximum condensing (and absorber) temperature (primary)-work limit'),_('ºC')),
    'EvapTmin':(_U('Minimum evaporating temperature (primary)-work limit'),_('ºC')),
    'ElectConsum':(_U('Electricity consumption'),_U('kW')),
    'Price':(_U('Equipment factory price incl. discount'),_U('€')),
    'TurnKeyPrice':(_U('Equipment turn-key price'),_U('€')),
    'OandMfix':(_U('Ratio O&M costs fixed'),_U('€/kW(heating)')),
    'OandMvar':(_U('Ratio O&M costs variable'),_U('€/MWh year(heating)')),
    'YearUpdate':(_U('Year of last data update'),_U('year'))
    }


BOILER = {
    'DBBoiler_ID':(_U('Identifier'),_U('-')),
    'BoilerManufacturer':(_U('Manufacturer'),_U('-')),
    'BoilerModel':(_U('Model'),_U('-')),
    'BoilerType':(_U('Type of Boiler'),_U('-')),	
    'BBPnom':(_U('Nominal power'),_U('kW')),
    'Economiser':(_U('Does the equip. include an economiser (water preheater)?'),_U('Yes/No')),
    'Preheater':(_U('Does the equip. include an air pre-heater?'),_U('Yes/No')),
    'BBEfficiency':(_U('Boiler efficiency'),_U('-')),
    'BoilerTemp':(_U('Maximum operating temperature'),_('ºC')),
    'BBA1':(_U('Linear dependence of the efficiency on the load'),_U('-')),
    'BBA2':(_U('Quadratic dependence of the efficiency on the load'),_U('-')),
    'BBK1':(_U('Linear dependence of the efficiency on temperature'),_U('-')),
    'BBK2':(_U('Quadratic dependence of the efficiency on temperature'),_U('-')),
    'BoilerPrice':(_U('Equipment price at factory applied installers discount'),_U('€')),
    'BoilerTurnKeyPrice':(_U('Price of installed equipment (including work, additional accessories)'),_U('€')),
    'BoilerOandMfix':(_U('Ratio O&M costs fixed'),_U('€/kW(heating)')),
    'BoilerOandMvar':(_U('Ratio O&M costs variable'),_U('€/MWh year(heating)'))
    }


STORAGE = {
    'DBStorage_ID':(_U('Identifier'),_U('-')),
    'ManData':(_U('Manufacturer data is provided only for Heating (H), Cooling (C), or both (HC)'),_U('-')),
    'Manufacturer':(_U('Manufacturer'),_U('-')),
    'Model':(_U('Model'),_U('-')),
    'Type':(_U('Type of HP: compression or absorption'),_U('-')),
    'SubType':(_U('Heat source - Heat sink, e.g. water-water'),_U('-')),
    'MaxHeatCap':(_U('Maximum heat capacity'),_U('kWh')),
    'Tmax':(_U('Maximum temperature of storage'),_('ºC')),
    'UA':(_U('Heat loss coefficient'),_U('kW/K')),
    'Volume':(_U('Volume'),_U('m3')),
    'Height':(_U('Height'),_U('m')),
    'Mass':(_U('Mass'),_U('kg')),
    'Price':(_U('Equipment factory price incl. discount'),_U('€')),
    'TurnKeyPrice':(_U('Equipment turn-key price'),_U('€')),
    'OandMfix':(_U('Ratio O&M costs fixed'),_U('€/kW(heating)')),
    'OandMvar':(_U('Ratio O&M costs variable'),_U('€/MWh year(heating)')),
    'YearUpdate':(_U('Year of last data update'),_U('year'))
    }


SOLAR = {
    'DBSolar_ID':(_U('Identifier'),_U('-')),
    'ManData':(_U('Manufacturer data is provided only for Heating (H), Cooling (C), or both (HC)'),_U('-')),
    'Manufacturer':(_U('Manufacturer'),_U('-')),
    'Model':(_U('Model'),_U('-')),
    'Type':(_U('Type of HP: compression or absorption'),_U('-')),
    'SubType':(_U('Heat source - Heat sink, e.g. water-water'),_U('-')),
    'Tmax':(_U('Maximum temperature'),_('ºC')),
    'UA':(_U('Heat loss coefficient'),_U('kW/K')),
    'Absorbtivity':(_U('Absorbtivity'),_U('-')),
    'Transmittance':(_U('Transmittance'),_U('-')),
    'Reflectivity':(_U('Reflectivity'),_U('-')),
    'Price':(_U('Equipment factory price incl. discount'),_U('€')),
    'TurnKeyPrice':(_U('Equipment turn-key price'),_U('€')),
    'OandMfix':(_U('Ratio O&M costs fixed'),_U('€/kW(heating)')),
    'OandMvar':(_U('Ratio O&M costs variable'),_U('€/MWh year(heating)')),
    'YearUpdate':(_U('Year of last data update'),_U('year'))
    }


FUEL = {
    'DBFuel_ID':(_U('Identifier'),_U('-')),#actual DB
    'FuelName':(_U('Fuel name'),_U('-')),
    'DBFuelUnit':(_U('Unit'),_U('-')),
    'FuelCode':(_U('Fuel code'),_U('-')),
    'FuelLCV':(_U('Lower calorific value'),_U('kWh/Unit')),
    'FuelHCV':(_U('Higher calorific value'),_U('kWh/Unit')),
    'tCO2':(_U('Production of CO2'),_U('tCO2/MWh(LCV)')),
    'FuelDensity':(_U('Density'),_U('kg/m3')),
    'ConversPrimEnergy':(_U('Conversion to primary energy'),_U('-')),
    'FuelDataSource':(_U('Data source'),_U('-')),
    'FuelComment':(_U('Comment'),_U('-'))
    }


FLUID = {
    'DBFluid_ID':(_U('Identifier'),_U('-')),#Actual DB
    'FluidName':(_U('Fluid name'),_U('-')),
    'FluidCp':(_U('Specific heat capacity'),_U('kJ/kgK')),
    'FluidDensity':(_U('Density'),_U('kg/m3')),
    'FluidComment':(_U('Comment'),_U('-'))
    }

ELECTRICITYMIX = {
    'id':('ID',_U('-')),#Actual DB
    'Year':(_U('Year of the data'),_U('-')),
    'Country':(_U('Country of the data'),_U('kJ/kgK')),
    'Reference':(_U('Reference (data source)'),_U('kg/m3')),
    'AuditorID':(_U('ID of auditor'),_U('-'))
    }


##BENCH = {#DB Maribor draft (excel)
##Benchcode	
##CodeNACE_id	
##UnitOperationCode	
##E_EnergyInt_MIN-PC	
##E_EnergyInt_MAX-PC	
##E_EnergyInt_TARG-PC	
##E_EnergyInt_MIN-T	
##E_EnergyInt_MAX-T	
##E_EnergyInt_TARG-T	
##E_SEC min	
##E_SEC max	
##E_SEC_TARG	
##E_Unit	
##H_EnergyInt_MIN-PC	
##H_EnergyInt_MAX-PC	
##H_EnergyInt_TARG-PC	
##H_EnergyInt_MIN-T	
##H_EnergyInt_MAX-T	
##H_EnergyInt_TARG-T	
##H_SEC min	
##H_SEC max	
##H_SEC_TARG	
##H_Unit	
##T_EnergyInt_MIN-PC	
##T_EnergyInt_MAX-PC	
##T_EnergyInt_TARG-PC	
##T_EnergyInt_MIN-T	
##T_EnergyInt_MAX-T	
##T_EnergyInt_TARG-T	
##E_SEC min	Specific electricity Consumption Min(SEC)
##E_SEC max	Specific Electricity Consumption Max(SEC)
##E_SEC_TARG	Specific Electricity Consumption (SEC) TARGET
##H_SEC min	Specific Heat Consumption Min(SEC)
##H_SEC max	Specific Heat Consumption Max(SEC)
##H_SEC_TARG	Specific Heat Consumption (SEC) TARGET
##T_SEC min	
##T_SEC max	
##T_SEC_TARG	
##T_SEC_AVG	Specific Energy Consumption (SEC) AVERAGE
##T_Unit	
##Comments	
##YearReference	
##References	References
##Literature	Literature
##DataRelevance	

BENCH = {
    'DBBenchmark_ID':(_U('Identifier'),_U('-')),#Actual DB
    'NaceCode_id':(_U('Nace code identifier'),_U('-')),
    'UnitOperation_id':(_U('Unit operation code'),_U('-')),
    'E_EnergyInt_MIN_PC':(_U('Energy intensity (production cost) MIN'),_U('kWh/€')),
    'E_EnergyInt_MAX_PC':(_U('Energy intensity (production cost) MAX'),_U('kWh/€')),
    'E_EnergyInt_TARG_PC':(_U('Energy intensity (production cost) TARGET'),_U('kWh/€')),
    'E_EnergyInt_MIN_T':(_U('Energy intensity (turnover) MIN'),_U('kWh/€')),
    'E_EnergyInt_MAX_T':(_U('Energy intensity (turnover) MAX'),_U('kWh/€')),
    'E_EnergyInt_TARG_T':(_U('Electricity: Energy intensity TARGET (turnover)'),_U('kWh/€')),
    'E_SEC':(_U('Specific electricity Consumption Min(SEC)'),_U('-')),
    'E_SEC_TARG':(_U('Specific Electricity Consumption TARGET(SEC)'),_U('-')),
    'E_SEC_AVG':(_U('Specific Electricity Consumption (SEC) AVERAGE'),_U('-')),
    'E_Unit':(_U('Unit of SEC electricity'),_U('-')),
    'H_EnergyInt_MIN_PC':(_U('Energy intensity (production cost) MIN'),_U('kWh/€')),
    'H_EnergyInt_MAX_PC':(_U('Heat: Energy intensity (production cost) MAX'),_U('kWh/€')),
    'H_EnergyInt_TARG_PC':(_U('Energy intensity (production cost) TARGET'),_U('kWh/€')),
    'H_EnergyInt_MIN_T':(_U('Heat: Energy intensity (turnover) MIN'),_U('kWh/€')),
    'H_EnergyInt_MAX_T':(_U('Energy intensity (turnover) MAX'),_U('kWh/€')),
    'H_EnergyInt_TARG_T':(_U('Heat: Energy intensity (turnover) TARGET'),_U('kWh/€')),
    'H_SEC':(_U('Specific Heat Consumption Min(SEC)'),_U('-')),
    'H_SEC_TARG':(_U('Specific Heat Consumption TARGET(SEC)'),_U('-')),
    'H_SEC_AVG':(_U('Specific Heat Consumption (SEC) AVERAGE'),_U('-')),
    'H_Unit':(_U('Unit of SEC heat'),_U('-')),
    'T_EnergyInt_MIN_PC':(_U('Energy intensity (production cost) MIN'),_U('kWh/€')),
    'T_EnergyInt_MAX_PC':(_U('Energy intensity (production cost) MAX'),_U('kWh/€')),
    'T_EnergyInt_TARG_PC':(_U('Energy intensity (production cost) TARGET'),_U('kWh/€')),
    'T_EnergyInt_MIN_T':(_U('Energy intensity (turnover) MIN'),_U('kWh/€')),
    'T_EnergyInt_MAX_T':(_U('Energy intensity (turnover) MAX'),_U('kWh/€')),
    'T_EnergyInt_TARG_T':(_U('Energy intensity (turnover) TARGET'),_U('kWh/€')),
    'T_SEC':(_U('Specific Energy Consumption Min(SEC)'),_U('-')),
    'T_SEC_TARG':(_U('Specific Energy Consumption TARGET(SEC)'),_U('-')),
    'T_SEC_AVG':(_U('Specific Energy Consumption (SEC) AVERAGE'),_U('-')),
    'T_Unit':(_U('Unit SEC'),_U('-')),
    'Comments':(_U('Comments'),_U('-')),
    'YearReference':(_U('Year (reference for economic data)'),_U('-')),
    'Reference':(_U('Reference'),_U('-')),
    'Literature':(_U('Literature'),_U('-')),
    'DataRelevance':(_U('Data relevance/reliability'),_U('-'))
    }


UNITOP = {
    'DBUnitOperation_ID':(_U('Identifier'),_U('-')),
    'UnitOperation':(_U('Unit operation'),_U('-')),
    'UnitOperationCode':(_U('Code'),_U('-')),
    'UnitOperationDescrip':(_U('Description'),_U('-'))
    }


NACE = {
    'DBNaceCode_ID':(_U('Identifier'),_U('-')),
    'CodeNACE':(_U('NACE code'),_U('-')),
    'CodeNACEsub':(_U('NACE subcode'),_U('-')),
    'NameNACE':(_U('NACE Name'),_U('-')),
    'NameNACEsub':(_U('NACE Subname'),_U('-')),
    'ProductName':(_U('Product name'),_U('-')),
    'NationalCode':(_U('National code'),_U('-')),
    'NationalSubCode':(_U('National subcode'),_U('-')),
    'NameNationalCode':(_U('National code name'),_U('-')),
    'NameNationalSubCode':(_U('National subcode name'),_U('-'))
    }
                    
DBTITLES = {
    'dbchp':CHP,
    'dbheatpump':HEATPUMP,
    'dbchiller':CHILLER,
    'dbboiler':BOILER,
    'dbstorage':STORAGE,
    'dbsolarthermal':SOLAR,
    'dbfuel':FUEL,
    'dbfluid':FLUID,
    'dbelectricitymix':ELECTRICITYMIX,
    'dbbenchmark':BENCH,
    'dbunitoperation':UNITOP,
    'dbnacecode':NACE
    }
    
    
