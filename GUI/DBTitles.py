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
#
#       Changes to previous version:
#        7/07/2008 TS  Syntax errors fixed.
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

CHP = {
# 'Variable name':('Descriptive name text','Units')
    'DBCHP_ID':(_('Identifier'),_('-')),
    'ManData':(_('Manufacturer data'),_('-')),#SD: This is in the sense of "Sorce of information" ->change to Source??
    'Manufacturer':(_('Manufacturer'),_('-')),
    'Model':(_('Model'),_('-')),
    'DBFuel_id':(_('Fuel type (identifier in fuel database)'),_('-')),#foresee introduction from choice? (Tom)
    'FuelConsum':(_('Fuel consumption'),_('kW (LCV)')),#this should be given by user ??Hans
    'UnitsFuelConsum':(_('Fuel units'),_('-')),#foresee introduction from choice? (Tom),Hans
    'YearManufact':(_('Year of manufacturing'),_('-')),
    'Type':(_('Type of equipment'),_('-')),#foresee introduction from choice? (Tom)
    'SubType':(_('Subtype of equipment'),_('-')),#foresee introduction from choice? (Tom)
    'CHPPe':(_('Electric power'),_('kW')),
    'CHPPt':(_('Thermal power'),_('kW')),
##    'CHPFuelConsum':('Fuel consumption','[kW] (LCV)'),#SD These are redundant, eliminate them from DB draft
##    'UnitsFuelConsum': ('Units fuel consumption','-'),
    'Eta_e':(_('Electric efficiency'),_('-')),# 0-1 or % ??
    'Eta_t':(_('Thermal efficiency'),_('-')),# 0-1 or % ??
    'Thigh':(_('High temperature at which energy can be delivered'),_('ºC')),
    'Tlow':(_('Low temperature at which energy can be delivered'),_('ºC')),
    'PercentPowThigh':(_('Percent of energy at high temperature'),_('%')),
    'PercentPowTlow':(_('Percent of energy at low temperature'),_('%')),
    'EEEmin':(_('Minimum electric efficiency by law'),_('-')),
    'InvRate':(_('Investment cost'),_('€/kW_el')),
    'Price':(_('Price'),_('€')),
    'TurnKeyPrice':(_('Turnkey price'),_('€')),
    'OandMfix':(_('Fixed Operation and Maintenance costs'),_('€/kW_el year')),
    'OandMRvar':(_('Variable Operation and Maintenance costs'),_('€/kW_el')),
    'YearUpdate':(_('Year of update'),_('-'))
    }

HEATPUMP = {
    'DBHeatPump_ID':(_('Identifier'),_('-')),
    'HPManData':(_('Manufacturer data'),_('-')),
    'HPManufacturer':(_('Manufacturer'),_('-')),
    'HPModel':(_('Model'),_('-')),
    'DBFuel_id':(_('Fuel type (identifier in fuel database)'),_('-')),#foresee introduction from choice? (Tom)
    'HPFuelConsum':(_('Fuel consumption'),_('kW (LCV)')),#this should be given by user ??Hans
    'HPUnitsFuelConsum':(_('Fuel units'),_('-')),#foresee introduction from choice? (Tom),Hans
    'HPYearManufact':(_('Year of manufacturing'),_('year')),
    'HPType':(_('Type'),_('-')),
    'HPSubType':(_('Sub-type'),_('-')),
    'HPAbsEffects':(_('Effects (absorption)'),_('-')),
    'HPAbsHeatMed':(_('Heating medium (absorption)'),_('-')),
    'HPWorkFluid':(_('Working fluid'),_('-')),
    'HPCoolCap':(_('Cooling capacity'),_('kW')),
    'HPCoolCOP':(_('Nominal cooling COP'),_('-')),
    'HPExCoolCOP':(_('Exergetic cooling COP'),_('-')),
    'HPThCoolCOP':(_('Theoretical cooling COP'),_('-')),
    'HPConstExCoolCOP':(_('Temperature range of constant exergetic COP application, cooling'),_('ºC')),
    'HPAbsTinC':(_('Absorber inlet temperature, cooling mode'),_('ºC')),
    'HPCondTinC':(_('Condenser inlet temperature, cooling mode'),_('ºC')),
    'HPGenTinC':(_('Generator inlet temperature, cooling mode'),_('ºC')),
    'HPEvapTinC':(_('Evaporator inlet temperature, cooling mode'),_('ºC')),
    'HPHeatCap':(_('Heating capacity'),_('kW')),
    'HPHeatCOP':(_('Nominal heating COP'),_('-')),
    'HPExHeatCOP':(_('Exergetic heating COP'),_('-')),
    'HPThHeatCOP':(_('Theoretical heating COP'),_('-')),
    'HPConstExHeatCOP':(_('Temperature range of constant exergetic COP application, heating'),_('ºC')),
    'HPAbsTinH':(_('Absorber inlet temperature, heating mode'),_('ºC')),
    'HPCondTinH':(_('Condenser inlet temperature, heating mode'),_('ºC')),
    'HPGenTinH':(_('Generator inlet temperature, heating mode'),_('ºC')),
    'HPEvapTinH':(_('Evaporator inlet temperature, heating mode'),_('ºC')),
    'HPLimDT':(_('Limit temperature difference'),_('ºC')),
    'HPGenTmin':(_('Minimum generator temperature'),_('ºC')),
    'HPCondTmax':(_('Maximum condensing temperature'),_('ºC')),
    'HPEvapTmin':(_('Minimum evaporating  temperature'),_('ºC')),
    'HPElectConsum':(_('Electricity consumption'),_('kW')),
    'HPPrice':(_('Equipment factory price'),_('€')),
    'HPTurnKeyPrice':(_('Turn-key price'),_('€')),
    'HPOandMfix':(_('Ratio for O&M costs (fixed)'),_('€/kW year')),
    'HPOandMvar':(_('Ratio for O&M costs (variable)'),_('€/MWh year')),
    'HPYearUpdate':(_('Year of last data update'),_('year'))
    }


CHILLER = {
    'DBChiller_ID':(_('Identifier'),_('-')),
    'ManData':(_('Manufacturer data is provided only for Heating (H), Cooling (C), or both (HC)'),_('-')),
    'Manufacturer':(_('Manufacturer'),_('-')),
    'Model':(_('Model'),_('-')),
    'Type':(_('Type of HP: compression or absorption'),_('-')),
    'SubType':(_('Heat source - Heat sink, e.g. water-water'),_('-')),
    'AbsEffects':(_('Only abs. HP: effects: 1, 2, or 3'),_('-')),
    'AbsHeatMed':(_('Only abs HP: Heating medium in generator:hot water, vapour, exhaust gas, directfired'),_('-')),
    'WorkFluid':(_('Absorbent-refrigerant pair, e.g. LiBr-H2O'),_('-')),
    'CoolCap':(_('Nominal Cooling capacity'),_('kW')),
    'CoolCOP':(_('Nominal COP cooling'),_('-')),
    'ExCoolCOP':(_('Exergetic COP cooling'),_('-')),
    'ThCoolCOP':(_('Theoretical COP cooling'),_('-')),
    'ConstExCoolCOP':(_('Temperature interval COPex is assumed constant, cooling'),_('ºC')),
    'AbsTinC':(_('Absorber inlet temperature, cooling mode, catalogue (sec. fluid)'),_('ºC')),
    'CondTinC':(_('Condenser inlet temperature, cooling mode, catalogue (sec. fluid)'),_('ºC')),
    'GenTinC':(_('Generator inlet temperature, cooling mode, catalogue (sec. fluid)'),_('ºC')),
    'EvapTinC':(_('Evaporator inlet temperature, cooling mode, catalogue (sec. fluid)'),_('ºC')),
    'HeatCap':(_('Nominal Heating capacity'),_('kW')),
    'HeatCOP':(_('Nominal COP heating'),_('-')),
    'ExHeatCOP':(_('Exergetic COP heating'),_('-')),
    'ThHeatCOP':(_('Theoretical COP heating'),_('-')),
    'ConstExHeatCOP':(_('Temperature interval COPex is assumed constant, heating'),_('ºC')),
    'AbsTinH':(_('Absorber inlet temperature, heating mode, catalogue (sec. fluid)'),_('ºC')),
    'CondTinH':(_('Condenser inlet temperature, heating mode, catalogue (sec. fluid)'),_('ºC')),
    'GenTinH':(_('Generator inlet temperature, heating mode, catalogue (sec. fluid)'),_('ºC')),
    'EvapTinH':(_('Evaporator inlet temperature, heating mode, catalogue (sec. fluid)'),_('ºC')),
    'LimDT':(_('Working Limit temperature difference (lift)'),_('ºC')),
    'GenTmin':(_('Minimum generator temperature (primary)-work limit'),_('ºC')),
    'CondTmax':(_('Maximum condensing (and absorber) temperature (primary)-work limit'),_('ºC')),
    'EvapTmin':(_('Minimum evaporating temperature (primary)-work limit'),_('ºC')),
    'ElectConsum':(_('Electricity consumption'),_('kW')),
    'Price':(_('Equipment factory price incl. discount'),_('EUR')),
    'TurnKeyPrice':(_('Equipment turn-key price'),_('EUR')),
    'OandMfix':(_('Ratio O&M costs fixed'),_('EUR/kW(heating)')),
    'OandMvar':(_('Ratio O&M costs variable'),_('EUR/MWh year(heating)')),
    'YearUpdate':(_('Year of last data update'),_('year'))
    }


BOILER = {
    'DBBoiler_ID':(_('Identifier'),_('-')),
    'BoilerManufacturer':(_('Manufacturer'),_('-')),
    'BoilerModel':(_('Model'),_('-')),
    'BoilerType':(_('Type of Boiler'),_('-')),	
    'BBPnom':(_('Nominal power'),_('kW')),
    'Economiser':(_('Does the equip. include an economiser (water preheater)?'),_('Yes/No')),
    'Preheater':(_('Does the equip. include an air pre-heater?'),_('Yes/No')),
    'BBEfficiency':(_('Boiler efficiency'),_('-')),
    'BoilerTemp':(_('Maximum operating temperature'),_('ºC')),
    'BBA1':(_('Linear dependence of the efficiency on the load'),_('-')),
    'BBA2':(_('Quadratic dependence of the efficiency on the load'),_('-')),
    'BBK1':(_('Linear dependence of the efficiency on temperature'),_('-')),
    'BBK2':(_('Quadratic dependence of the efficiency on temperature'),_('-')),
    'BoilerPrice':(_('Equipment price at factory applied installers discount'),_('EUR')),
    'BoilerTurnKeyPrice':(_('Price of installed equipment (including work, additional accessories)'),_('EUR')),
    'BoilerOandMfix':(_('Ratio O&M costs fixed'),_('EUR/kW(heating)')),
    'BoilerOandMvar':(_('Ratio O&M costs variable'),_('EUR/MWh year(heating)'))
    }


STORAGE = {
    'DBStorage_ID':(_('Identifier'),_('-')),
    'ManData':(_('Manufacturer data is provided only for Heating (H), Cooling (C), or both (HC)'),_('-')),
    'Manufacturer':(_('Manufacturer'),_('-')),
    'Model':(_('Model'),_('-')),
    'Type':(_('Type of HP: compression or absorption'),_('-')),
    'SubType':(_('Heat source - Heat sink, e.g. water-water'),_('-')),
    'MaxHeatCap':(_('Maximum heat capacity'),_('kWh')),
    'Tmax':(_('Maximum temperature of storage'),_('ºC')),
    'UA':(_('Heat loss coefficient'),_('kW/K')),
    'Volume':(_('Volume'),_('m3')),
    'Height':(_('Height'),_('m')),
    'Mass':(_('Mass'),_('kg')),
    'Price':(_('Equipment factory price incl. discount'),_('EUR')),
    'TurnKeyPrice':(_('Equipment turn-key price'),_('EUR')),
    'OandMfix':(_('Ratio O&M costs fixed'),_('EUR/kW(heating)')),
    'OandMvar':(_('Ratio O&M costs variable'),_('EUR/MWh year(heating)')),
    'YearUpdate':(_('Year of last data update'),_('year'))
    }


SOLAR = {
    'DBSolar_ID':(_('Identifier'),_('-')),
    'ManData':(_('Manufacturer data is provided only for Heating (H), Cooling (C), or both (HC)'),_('-')),
    'Manufacturer':(_('Manufacturer'),_('-')),
    'Model':(_('Model'),_('-')),
    'Type':(_('Type of HP: compression or absorption'),_('-')),
    'SubType':(_('Heat source - Heat sink, e.g. water-water'),_('-')),
    'Tmax':(_('Maximum temperature'),_('ºC')),
    'UA':(_('Heat loss coefficient'),_('kW/K')),
    'Absorbtivity':(_('Absorbtivity'),_('-')),
    'Transmittance':(_('Transmittance'),_('-')),
    'Reflectivity':(_('Reflectivity'),_('-')),
    'Price':(_('Equipment factory price incl. discount'),_('EUR')),
    'TurnKeyPrice':(_('Equipment turn-key price'),_('EUR')),
    'OandMfix':(_('Ratio O&M costs fixed'),_('EUR/kW(heating)')),
    'OandMvar':(_('Ratio O&M costs variable'),_('EUR/MWh year(heating)')),
    'YearUpdate':(_('Year of last data update'),_('year'))
    }


FUEL = {
    'DBFuel_ID':(_('Identifier'),_('-')),#actual DB
    'FuelName':(_('Fuel name'),_('-')),
    'DBFuelUnit':(_('Unit'),_('-')),
    'FuelCode':(_('Fuel code'),_('-')),
    'FuelLCV':(_('Lower calorific value'),_('kWh/Unit')),
    'FuelHCV':(_('Higher calorific value'),_('kWh/Unit')),
    'tCO2':(_('Production of CO2'),_('tCO2/MWh(LCV)')),
    'FuelDensity':(_('Density'),_('kg/m3')),
    'ConversPrimEnergy':(_('Conversion to primary energy'),_('-')),
    'FuelDataSource':(_('Data source'),_('-')),
    'FuelComment':(_('Comment'),_('-'))
    }


FLUID = {
    'DBFluid_ID':(_('Identifier'),_('-')),#Actual DB
    'FluidName':(_('Fluid name'),_('-')),
    'FluidCp':(_('Specific heat capacity'),_('kJ/kgK')),
    'FluidDensity':(_('Density'),_('kg/m3')),
    'FluidComment':(_('Comment'),_('-'))
    }

ELECTRICITYMIX = {
    'id':('ID',_('-')),#Actual DB
    'Year':(_('Year of the data'),_('-')),
    'Country':(_('Country of the data'),_('kJ/kgK')),
    'Reference':(_('Reference (data source)'),_('kg/m3')),
    'AuditorID':(_('ID of auditor'),_('-'))
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
    'DBBenchmark_ID':(_('Identifier'),_('-')),#Actual DB
    'NaceCode_id':(_('Nace code identifier'),_('-')),
    'UnitOperation_id':(_('Unit operation code'),_('-')),
    'E_EnergyInt_MIN_PC':(_('Energy intensity (production cost) MIN'),_('kWh/€')),
    'E_EnergyInt_MAX_PC':(_('Energy intensity (production cost) MAX'),_('kWh/€')),
    'E_EnergyInt_TARG_PC':(_('Energy intensity (production cost) TARGET'),_('kWh/€')),
    'E_EnergyInt_MIN_T':(_('Energy intensity (turnover) MIN'),_('kWh/€')),
    'E_EnergyInt_MAX_T':(_('Energy intensity (turnover) MAX'),_('kWh/€')),
    'E_EnergyInt_TARG_T':(_('Electricity: Energy intensity TARGET (turnover)'),_('kWh/€')),
    'E_SEC':(_('Specific electricity Consumption Min(SEC)'),_('-')),
    'E_SEC_TARG':(_('Specific Electricity Consumption TARGET(SEC)'),_('-')),
    'E_SEC_AVG':(_('Specific Electricity Consumption (SEC) AVERAGE'),_('-')),
    'E_Unit':(_('Unit of SEC electricity'),_('-')),
    'H_EnergyInt_MIN_PC':(_('Energy intensity (production cost) MIN'),_('kWh/€')),
    'H_EnergyInt_MAX_PC':(_('Heat: Energy intensity (production cost) MAX'),_('kWh/€')),
    'H_EnergyInt_TARG_PC':(_('Energy intensity (production cost) TARGET'),_('kWh/€')),
    'H_EnergyInt_MIN_T':(_('Heat: Energy intensity (turnover) MIN'),_('kWh/€')),
    'H_EnergyInt_MAX_T':(_('Energy intensity (turnover) MAX'),_('kWh/€')),
    'H_EnergyInt_TARG_T':(_('Heat: Energy intensity (turnover) TARGET'),_('kWh/€')),
    'H_SEC':(_('Specific Heat Consumption Min(SEC)'),_('-')),
    'H_SEC_TARG':(_('Specific Heat Consumption TARGET(SEC)'),_('-')),
    'H_SEC_AVG':(_('Specific Heat Consumption (SEC) AVERAGE'),_('-')),
    'H_Unit':(_('Unit of SEC heat'),_('-')),
    'T_EnergyInt_MIN_PC':(_('Energy intensity (production cost) MIN'),_('kWh/€')),
    'T_EnergyInt_MAX_PC':(_('Energy intensity (production cost) MAX'),_('kWh/€')),
    'T_EnergyInt_TARG_PC':(_('Energy intensity (production cost) TARGET'),_('kWh/€')),
    'T_EnergyInt_MIN_T':(_('Energy intensity (turnover) MIN'),_('kWh/€')),
    'T_EnergyInt_MAX_T':(_('Energy intensity (turnover) MAX'),_('kWh/€')),
    'T_EnergyInt_TARG_T':(_('Energy intensity (turnover) TARGET'),_('kWh/€')),
    'T_SEC':(_('Specific Energy Consumption Min(SEC)'),_('-')),
    'T_SEC_TARG':(_('Specific Energy Consumption TARGET(SEC)'),_('-')),
    'T_SEC_AVG':(_('Specific Energy Consumption (SEC) AVERAGE'),_('-')),
    'T_Unit':(_('Unit SEC'),_('-')),
    'Comments':(_('Comments'),_('-')),
    'YearReference':(_('Year (reference for economic data)'),_('-')),
    'Reference':(_('Reference'),_('-')),
    'Literature':(_('Literature'),_('-')),
    'DataRelevance':(_('Data relevance/reliability'),_('-'))
    }


UNITOP = {
    'DBUnitOperation_ID':(_('Identifier'),_('-')),
    'UnitOperation':(_('Unit operation'),_('-')),
    'UnitOperationCode':(_('Code'),_('-')),
    'UnitOperationDescrip':(_('Description'),_('-'))
    }


NACE = {
    'DBNaceCode_ID':(_('Identifier'),_('-')),
    'CodeNACE':(_('NACE code'),_('-')),
    'CodeNACEsub':(_('NACE subcode'),_('-')),
    'NameNACE':(_('NACE Name'),_('-')),
    'NameNACEsub':(_('NACE Subname'),_('-')),
    'ProductName':(_('Product name'),_('-')),
    'NationalCode':(_('National code'),_('-')),
    'NationalSubCode':(_('National subcode'),_('-')),
    'NameNationalCode':(_('National code name'),_('-')),
    'NameNationalSubCode':(_('National subcode name'),_('-'))
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
    
    
