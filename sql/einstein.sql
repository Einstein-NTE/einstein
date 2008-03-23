-- Dir: Created 12/02/2008
-- 
-- einsteinDB.txt - two heat pump tables added with respect to previous -> changed to einsteinDB_old.txt 26/02/2008
-- 
-- Note: I still use the previous database, 12/02/2008
-- 
-- 
-- einsteinDB.txt - created according to the "Heat Pump module technical description v0.5.odt", 26/02/2008
-- 
-- einsteintDB.txt - UHeatPump table added, 27/02/2008
-- 
-- einsteintDB.txt - Added Heat demand and availability curves: EnergyFlows, 27/02/2008
-- EnergyFlowsQDa, EnergyFlowsQAa, EnergyFlowsQDh, EnergyFlowsQAh - original curves from Joints
-- EnergyFlowsQDaRec, EnergyFlowsQAaRec, EnergyFlowsQDhRec, EnergyFlowsQAhRec - recalculated curves after HP application
-- 
-- 
-- einsteintDB.txt - Added two aditional tables to store HPM calculation data, change name to einstein_v8 28/02/2008
-- HPHourlyInternalData
-- HPAnnualInternalData
-- 
-- einsteintDB.txt - changes in UHeatPump - eliminate AUTO_INCREMENT statement, 28/02/2008
-- 
-- ========================================================================================================
-- 
-- einsteintDB.txt - 03/03/2008
-- changed database name: einstein_V8 --> einstein_001
-- according to Heiko (29/02/2008)-include "Index" column and AUTO_INCREMENT statement in QD,QA (EnergyFlows)
-- Its pending to add Alternative proposal ID in all the tables - 03/03/2008
-- 
-- ========================================================================================================
-- 
-- einsteintDB.txt - 03/03/2008
-- 
-- In order to store the Alternative Proposals, as each Alternative Proposal is the same set of data as the original -->
-- --> in each table where Questionnaire_id exists is created also a column AlternativeProposal_id
-- 
-- Because when composing the Alternative Proposal the equipment can be either introduced from Quest. or selected from DB,
-- four additional columns are created in the QGenerationHC table --> in order to store the equipment ID, equipment type, 
-- database table name and a check if the equipment is selected from DB or no:
-- 	- IsSelectedFromDB (yes/no)(1/0)
-- 	- DatabaseNameSelection - Database table name (from which equipment is selected)
-- 	- EquipTypeFromDB - (as predefined in equipment database)
-- 	- EquipIDFromDB - Equipment ID (as in DB table)
-- 
-- 	-IsAlternative parameter -> eliminated from QGenerationHC, -> now this is managed by AlternativeProposal_id
-- 
-- AlternativeProposal_id --> added in the PRIMARY KEY () list for non-repeating data??? -> no at the moment- consult with Heiko
-- 
-- ==========================================================================================================
-- 
-- einsteintDB.txt - 03/03/2008
-- 
-- Add the parameters from UHeatPump to PSetUpData. This is because in the automatic execution (Level 2, Level 3) some or all of this 
-- parameters will not be asked for, but will be searched in the PSetUpdata. In this table should be all the default values.
-- 
-- !!Note: Ask Heiko how PSetUpData_id will be charged in Questionnaire table:
-- options: 
-- -take the last ID from the PSetUpData as default. 
-- -indicate it from the settings: preview defaults and select ID
-- 
-- ===========================================================================================================
-- einsteinDB001.txt - 03/04/2008 -Heiko
-- 
-- Changed the AlternativeProposal_id to AlternativeProposalNo for all Tables and removed from the Questionnaire Table
-- changed QDistributionHC - HeatFromEquipNo to HeatFromQGenerationHC_id as relation to
-- the equipment id - QGenerationHC_ID
-- changed the period values of QBuildings to start and stop values 
-- changed datatype year to integer 
-- changed datatype date to varchar
-- renamed database to simply einstein




--CREATE DATABASE einstein;



USE einstein;


CREATE TABLE Questionnaire (
	Questionnaire_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	PSetUpData_id INTEGER UNSIGNED DEFAULT 0 COMMENT 'link the industry with the set-up data',
	Name VARCHAR(45) COMMENT 'name of the company',
	City VARCHAR(45) COMMENT 'city / country',
	DescripIndustry	VARCHAR(45) COMMENT 'description of the industry',
	Branch VARCHAR(45) COMMENT 'branch',
	SubBranch VARCHAR(45) COMMENT 'sub-branch',
	DBNaceCode_id INTEGER UNSIGNED COMMENT 'NACE code',
	Contact VARCHAR(45) COMMENT 'name of contact person',
	Role VARCHAR(45) COMMENT 'Role of contact person in the company',
	Address VARCHAR(45) COMMENT 'address',
	Phone VARCHAR(45) COMMENT 'Telephone  No',
	Fax VARCHAR(45)	COMMENT 'Fax No',
	Email VARCHAR(45) COMMENT 'E-mail',
	NEmployees INTEGER COMMENT 'number of employees',
	Turnover DOUBLE	COMMENT 'annual turnover',
	ProdCost DOUBLE COMMENT 'annual production cost',
	BaseYear INTEGER COMMENT 'base year for ec. Data',
	Growth DOUBLE COMMENT 'growth rate of the production volume foreseen for the next 5 years',
	Independent TINYINT COMMENT 'Is the company independent ?',
	OMThermal DOUBLE COMMENT 'Yearly O&M heat & cold',
	OMElectrical DOUBLE COMMENT 'Yearly O&M electrical', 
	HPerDayInd DOUBLE COMMENT 'total hours of operation per working day',
	NShifts DOUBLE COMMENT 'number of shifts',
	NDaysInd DOUBLE COMMENT 'days of production / operation per year',
	NoProdStart VARCHAR(6) COMMENT 'principal period of holidays or stops for maintenance - start date',
	NoProdStop VARCHAR(6) COMMENT 'principal period of holidays or stops for maintenance - end date',
	PercentElTotcost DOUBLE COMMENT 'Percentage of electricity cost  on overall production cost',
	PercentFuelTotcost DOUBLE COMMENT 'Percentage of fuel cost on overall production cost',
	EnclMonthlyElBills TINYINT COMMENT 'Enclosing monthly electricity bills?',
	EnclMonthlyFuelBills TINYINT COMMENT 'Enclosing monthly fuel bills?',
	InflationRate DOUBLE COMMENT 'General inflation rate',
	FuelPriceRate DOUBLE COMMENT 'Rate of increment of energy prices',
	InterestExtFinancing DOUBLE COMMENT 'Nominal rate of interest for external financing of installations', 
	PercentExtFinancing DOUBLE COMMENT 'Percentage of external financing for installations',
	AmortisationTime DOUBLE COMMENT 'Time for economic amortisation of installations',		
	PublicFundType VARCHAR(45) COMMENT 'Type (credit, subvention)',
	OMGenTot DOUBLE COMMENT 'General maintenance - total costs',
	OMGenOP DOUBLE COMMENT 'General maintenance - own personnel',
	OMGenEP DOUBLE COMMENT 'General maintenance - external personnel',
	OMGenFung DOUBLE COMMENT 'General maintenance - fungible assets',		
	OMBuildTot DOUBLE COMMENT 'Buildings - total costs',
	OMBuildOP DOUBLE COMMENT 'Buildings - own personnel',
	OMBuildEP DOUBLE COMMENT 'Buildings - external personnel',
	OMBiuildFung DOUBLE COMMENT 'Buildings - fungible assets',	
	OMMachEquipTot DOUBLE COMMENT 'Machines and equipment - total costs',
	OMMachEquipOP DOUBLE COMMENT 'Machines and equipment - own personnel',
	OMMachEquipEP DOUBLE COMMENT 'Machines and equipment  - external personnel',
	OMMachEquipFung DOUBLE COMMENT 'Machines and equipment  - fungible assets',	
	OMHCGenDistTot DOUBLE COMMENT 'Generation and distribution of heat and cold - total costs',
	OMHCGenDistOP DOUBLE COMMENT 'Generation and distribution of heat and cold - own personnel',
	OMHCGenDistEP DOUBLE COMMENT 'Generation and distribution of heat and cold  - external personnel',
	OMHCGenDistFung DOUBLE COMMENT 'Generation and Distribution of heat and cold  - fungible assets',		
	OMTotalTot DOUBLE COMMENT 'Total - total costs',
	OMTotalOP DOUBLE COMMENT 'Total - own personnel',
	OMTotalEP DOUBLE COMMENT 'Total - external personnel',
	OMTotalFung DOUBLE COMMENT 'Total - fungible assets',
	EnergyManagExisting TINYINT COMMENT 'Is there any energy menagement system implemented?',
	EnergyManagExternal TINYINT COMMENT 'Is the energy menagent externalized?',
	EnclChartHCDistribSys TINYINT COMMENT 'Enclosing flowchart of the heat supply and distribution system?',
	NPIPEDUCT INTEGER COMMENT 'Number of pipes or ducts',
	HDEffAvg DOUBLE COMMENT 'Average distribution efficiency',
	NBuild INTEGER COMMENT 'Number of buildings',
	PRIMARY KEY (Questionnaire_ID)
);



CREATE TABLE QProduct (
	QProduct_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	Product VARCHAR(45) COMMENT 'type of product',
	ProductCode VARCHAR(45) COMMENT 'product code',
	QProdYear DOUBLE COMMENT 'quantity of product per year',
	ProdUnit VARCHAR(45) COMMENT 'measurement unit for product quantity',
	TurnoverProd DOUBLE COMMENT 'anual turnover per product',
	ElProd DOUBLE COMMENT 'Electricity consumption per product',
	FuelProd DOUBLE COMMENT 'Fuel consumption per product',
	PRIMARY KEY (QProduct_ID)
);




CREATE TABLE QFuel (
	QFuel_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	FuelUnit VARCHAR(45) COMMENT 'Unit',
	DBFuel_id INTEGER UNSIGNED COMMENT 'Selected Fueltype',
	MFuelYear DOUBLE COMMENT 'Annual consumption',
	FuelOwn DOUBLE COMMENT 'Total own fuel consumption (LCV)',
	FuelTariff DOUBLE COMMENT 'Fuel price',
	FuelCostYear DOUBLE COMMENT 'Annual energy cost',
	PRIMARY KEY (QFuel_ID)
);



CREATE TABLE QElectricity (
	QElectricity_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	PowerContrTot DOUBLE COMMENT 'Contracted power total',
	PowerContrStd DOUBLE COMMENT 'Contracted power standard',
	PowerContrPeak DOUBLE COMMENT 'Contracted power peak',
	PowerContrVall DOUBLE COMMENT 'Contracted power valley',
	ElectricityTotYear DOUBLE COMMENT 'Annual consumption',
	ElectricityPeakYear DOUBLE COMMENT 'Annual consumption peak',
	ElectricityStandYear DOUBLE COMMENT 'Annual consumption standard',
	ElectricityValleyYear DOUBLE COMMENT 'Annual consumption valley',
	ElGenera DOUBLE COMMENT 'Self-generation (co-generation)',
	ElSales DOUBLE COMMENT 'Sales to grid (co-generation)',		
	ElectricityRef DOUBLE COMMENT 'Electricity for refrigeration',
	ElectricityAC DOUBLE COMMENT 'Electricity for air conditioning',
	ElectricityThOther DOUBLE COMMENT 'Electricity for other thermal uses',
	ElectricityMotors DOUBLE COMMENT 'Electricity for motors',
	ElectricityChem DOUBLE COMMENT 'Electricity for electro-chemical processes',
	ElectricityLight DOUBLE COMMENT 'Electricity for lightning',		
	ElTariffClassTot VARCHAR(45) COMMENT 'Tariff type / class (total)',
	ElTariffClassStd VARCHAR(45) COMMENT 'Tariff type / class (standard)',
	ElTariffClassPeak VARCHAR(45) COMMENT 'Tariff type / class (peak)',
	ElTariffClassTotVall VARCHAR(45) COMMENT 'Tariff type / class (valley)',
	ElTariffClassCHP VARCHAR(45) COMMENT 'Tariff type / class (CHP)',
	ElTariffPowTot DOUBLE COMMENT 'Tariff on installed power (total)',
	ElTariffPowStd DOUBLE COMMENT 'Tariff on installed power (standard)',
	ElTariffPowPeak DOUBLE COMMENT 'Tariff on installed power (peak)',
	ElTariffPowVall DOUBLE COMMENT 'Tariff on installed power (valley)',
	ElTariffPowCHP DOUBLE COMMENT 'Tariff on installed power (CHP)',
	ElTariffCTot DOUBLE COMMENT 'Tariff on consumption (total)',
	ElTariffCStd DOUBLE COMMENT 'Tariff on consumption (standard)',
	ElTariffCPeak DOUBLE COMMENT 'Tariff on consumption (peak)',
	ElTariffCVall DOUBLE COMMENT 'Tariff on consumption (valley)',
	ETariffCHP DOUBLE COMMENT 'Tariff sales of CHP (without feedin-tariff)',
	ElCostYearTot DOUBLE COMMENT 'Annual electricity cost total',
	ElCostYearStd DOUBLE COMMENT 'Annual electricity cost standard',
	ElCostYearPeak DOUBLE COMMENT 'Annual electricity cost peak',
	ElCostYearVall DOUBLE COMMENT 'Annual electricity cost valley',
	ElSalesYearCHP DOUBLE COMMENT 'Annual electricity sales CHP',
	PRIMARY KEY (QElectricity_ID)
);




CREATE TABLE QProcessData (
	QProcessData_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	Process VARCHAR(45) COMMENT 'process short name',
	DBUnitOperation_id INTEGER UNSIGNED COMMENT '',
	ProcType VARCHAR(45) COMMENT 'process type',		
	ProcMedDBFluid_id INTEGER UNSIGNED COMMENT 'Product or process medium (water, oil, air, lye ...)',
	PT DOUBLE COMMENT 'typical(final) temperature of the process medium during operation',
	PTInFlow DOUBLE COMMENT 'inlet temperature of the process medium(before heat recovery)',
	PTStartUp DOUBLE COMMENT 'start-up temperature of process medium after breaks',
	VInFlowDay DOUBLE COMMENT 'Daily inflow of process medium',
	VolProcMed DOUBLE COMMENT 'Volume of the process medium within the equipment or storage',
	UAProc DOUBLE COMMENT 'Thermal heat loss coefficient of the process',
	HPerDayProc DOUBLE COMMENT 'hours of process operation per day',
	NBatch DOUBLE COMMENT 'Number of batches per day',
	HBatch DOUBLE COMMENT 'Duration of 1 batch',
	NDaysProc DOUBLE COMMENT 'days of operation per year',		
	PTOutFlow DOUBLE COMMENT 'outlet temperature of waste heat flows',
	PTFinal DOUBLE COMMENT 'final  temperature of waste heat flows',
	VOutFlow DOUBLE COMMENT 'Daily outflow of process medium',
	HeatRecOK TINYINT COMMENT 'can heat be recovered from the outflowing medium ?',
	HeatRecExist TINYINT COMMENT 'Exsists heat from heat  recovery for the process ?',
	SourceWasteHeat VARCHAR(45) COMMENT 'Source of waste heat',
	PTInFlowRec DOUBLE COMMENT 'inlet temperature of the process medium (after heat recovery)',
	EnclChartHCSupply TINYINT COMMENT 'Enclosing Flowchart of HC supply system',
	SupplyMedDBFluid_id INTEGER UNSIGNED COMMENT 'heat or cold supply medium (water, steam, air)',
	PipeDuctProc VARCHAR(45) COMMENT 'heat or cold supply to the process from distribution line / branch No.',
	TSupply DOUBLE COMMENT 'Temperature of the heat or cold supply',
	SupplyMedFlow DOUBLE COMMENT 'flow rate',
	UPHtotQ DOUBLE COMMENT 'UPH from questionnaire (annual)',
	PRIMARY KEY (QProcessData_ID)
);




CREATE TABLE QGenerationHC (                                                
	QGenerationHC_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	Equipment VARCHAR(45) COMMENT 'Short name of equipment',
	Manufact VARCHAR(45) COMMENT 'Manufacturer',
	YearManufact INTEGER COMMENT 'Year of  manufacturing or/and installation?',
	Model VARCHAR(45) COMMENT 'Model',
	EquipType VARCHAR(45) COMMENT 'Type of boiler / burner or chiller / compressor',
	NumEquipUnits INTEGER COMMENT 'Number of units of the same type',
	DBFuel_id INTEGER UNSIGNED COMMENT 'Fuel type',
	HCGPnom DOUBLE COMMENT 'Nominal Power (heat or cold, output)',
	FuelConsum DOUBLE COMMENT 'Fuel consumption (nominal)',
	UnitsFuelConsum VARCHAR(45) COMMENT 'Units for fuel consumption e.g. m3/h, l/h',
	ElectriConsum DOUBLE COMMENT 'Electricity consumption',
	HCGTEfficiency DOUBLE COMMENT 'Mean overall thermal conversion efficiency',
	HCGEEfficiency DOUBLE COMMENT 'CHP only: Electrical conversion efficiency',
	ElectriProduction DOUBLE COMMENT 'CHP only: Electricity production',
	TExhaustGas DOUBLE COMMENT 'Temperature of exhaust gas at standard operation conditions',
	PartLoad DOUBLE COMMENT 'Mean utilisation factor (full capacity = 100%)',
	HPerDayEq DOUBLE COMMENT 'hours of operation per day',
	NDaysEq DOUBLE COMMENT 'days of operation per year',
	PipeDuctEquip VARCHAR(45) COMMENT 'heat or cold supplyed to the distribution line / branch (piping or duct) no.',
	CoolTowerType VARCHAR(45) COMMENT 'Only for cooling: Type of cooling tower: dry / wet ?',
	IsSelectedFromDB TINYINT DEFAULT 0 COMMENT 'For Alternative Proposal: Is equipment selected from DB?',
	DatabaseNameSelection VARCHAR(45) COMMENT 'Database name from which equipment is selected',
	EquipTypeFromDB VARCHAR(45) COMMENT 'Equipment type (as in database)',
	EquipIDFromDB INTEGER UNSIGNED COMMENT 'Equipment ID from database',
	PRIMARY KEY (QGenerationHC_ID)
);



CREATE TABLE  QDistributionHC (                  
	QDistributionHC_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	Pipeduct VARCHAR(45) COMMENT 'Name of the branch / distribution system',
	HeatFromQGenerationHC_id INTEGER COMMENT 'Heat or cold supply comes from equipment(s) QGenerationHC_id:',
	HeatDistMedium VARCHAR(45) COMMENT 'heat or cold distribution medium',
	DistribCircFlow DOUBLE COMMENT 'nominal production or circulation rate (specify units)',
	ToutDistrib DOUBLE COMMENT 'outlet temperature (to distribution)',
	TreturnDistrib DOUBLE COMMENT 'return temperature (from distribution)',
	PercentRecirc DOUBLE COMMENT 'Percentage of recirculation',
	Tfeedup DOUBLE COMMENT 'feed-up in open circuit',
	PressDistMedium DOUBLE COMMENT 'pressure of the distribution medium',
	PercentCondRecovery DOUBLE COMMENT 'percentage of condensate recovery (steam boilers only)',
	TotLengthDistPipe DOUBLE COMMENT 'total length of distribution piping or ducts (one way)',
	UDistPipe DOUBLE COMMENT 'total coefficient of heat losses for piping or ducts',
	DDistPipe DOUBLE COMMENT 'mean pipe diameter',
	DeltaDistPipe DOUBLE COMMENT 'insulation thickness',		
	NumStorageUnits INTEGER COMMENT 'Number of the heat or cold storage units', 
	VtotStorage DOUBLE COMMENT 'Total volume of the storage',
	TypeStorage VARCHAR(45) COMMENT 'Type of storage / storage medium',
	PmaxStorage DOUBLE COMMENT 'maximum pressure',
	TmaxStorage DOUBLE COMMENT 'maximum temperature of the storage',
	IsAlternative TINYINT DEFAULT 0 COMMENT '',
	PRIMARY KEY (QDistributionHC_ID)
);




CREATE TABLE QRenewables (
	QRenewables_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	REMotivation VARCHAR(45) COMMENT 'Main motivation for renewable energy use',
	REInterest TINYINT COMMENT 'Are you interested in the use of renweable energy? (solar thermal/biomass)',
	REReason VARCHAR(45) COMMENT 'If affirmative, please specify the principal reasons:',
	SurfAreaRoof DOUBLE COMMENT 'Available roof area',
	SurfAreaGround DOUBLE COMMENT 'Available ground area',		
	InclinationRoof DOUBLE COMMENT 'Positioning of the roof area',
	InclinationGround DOUBLE COMMENT 'Positioning of the ground area',
	OrientationRoof VARCHAR(45) COMMENT 'Orientation of the roof area',
	OrientationGround VARCHAR(45) COMMENT 'Orientation of the ground area',
	ShadingRoof VARCHAR(45) COMMENT 'shading of roof',
	ShadingGround VARCHAR(45) COMMENT 'shading of ground',
	DistanceToRoof DOUBLE COMMENT 'Distance between roof and process',
	DistanceToGround DOUBLE COMMENT 'Distance between ground and process',
	RoofType VARCHAR(45) COMMENT 'Type of roof',
	RoofStaticLoadCap DOUBLE COMMENT 'static load capacity of the roof(s)',
	EnclBuildGroundSketch TINYINT COMMENT 'Enclosing of drawing or scheme of building?',		
	BiomassFromProc VARCHAR(45) COMMENT 'Type of biomass available from processes',
	PeriodBiomassProcStart VARCHAR(6) COMMENT 'Period of year the biomass is available - start',
	PeriodBiomassProcStop VARCHAR(6) COMMENT 'Period of year the biomass is available - stop',
	NDaysBiomassProc DOUBLE COMMENT 'Number of days biomass is produced',
	QBiomassProcDay DOUBLE COMMENT 'Daily quantity of biomass',
	SpaceBiomassProc DOUBLE COMMENT 'Space availability to stock biomass',
	LCVBiomassProc DOUBLE COMMENT 'LCV biomass',
	HumidBiomassProc DOUBLE COMMENT 'Humidity',		
	BiomassFromRegion VARCHAR(45) COMMENT 'Type of biomass available from the region',
	PriceBiomassRegion DOUBLE COMMENT 'Unit price of biomass',
	PeriodBiomassRegionStart VARCHAR(6) COMMENT 'Period of year the biomass is available - start',
	PeriodBiomassRegionStop VARCHAR(6) COMMENT 'Period of year the biomass is available - stop',
	NDaysBiomassRegion DOUBLE COMMENT 'Number of days the biomass is produced',
	PRIMARY KEY (QRenewables_ID)
);




CREATE TABLE QBuildings (
	QBuildings_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	BuildName VARCHAR(45) COMMENT 'Building short name',
	BuildConstructSurface DOUBLE COMMENT 'Constructed surface', 
	BuildUsefulSurface DOUBLE COMMENT 'Useful surface', 
	BuildUsage VARCHAR(45) COMMENT 'Use of the building',
	BuildEnergyDemand VARCHAR(45) COMMENT 'Global data on energy demand',
	BuildMaxHP DOUBLE COMMENT 'Maximum heating power',
	BuildMaxCP DOUBLE COMMENT 'Maximum cooling power',
	BuildAnnualHeating DOUBLE COMMENT 'Annual heating demand',
	BuildAnnualAirCond DOUBLE COMMENT 'Annual demand of air conditioning',
	BuildDailyDHW DOUBLE COMMENT 'Daily consumption of  DHW',
	BuildHoursOccup DOUBLE COMMENT 'Hours of occupation', 
	BuildDaysInUse DOUBLE COMMENT 'Days of use per year',
  	BuildHolidaysPeriodStart varchar(45) default NULL COMMENT 'Holidays period start',
  	BuildHolidaysPeriodStop varchar(45) default NULL COMMENT 'Holidays period stop',
  	BuildHeatingPeriodStart varchar(45) default NULL COMMENT 'Heating period start',
  	BuildHeatingPeriodStop varchar(45) default NULL COMMENT 'Heating period stop',
  	BuildAirCondPeriodStart varchar(45) default NULL COMMENT 'Air conditioning period start',
  	BuildAirCondPeriodStop varchar(45) default NULL COMMENT 'Air conditioning period stop',
	EnclBuildDraw TINYINT COMMENT 'Enclosing building drawing or sketch?',
	PRIMARY KEY (QBuildings_ID)
);




CREATE TABLE CGeneralData (
	CGeneralData_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	NProducts INTEGER COMMENT 'Number of products',
	HoursInd DOUBLE COMMENT 'Total yearly working hours in industry',
	PETOTAL DOUBLE COMMENT 'Total primary energy consumption',
	PECFuels DOUBLE COMMENT 'Total Primary Energy per all fuels used in industry',
	PECElect DOUBLE COMMENT 'Total Primary Energy per all electricity used in industry',
	PETFuels DOUBLE COMMENT 'Total Primary Energy per all fuels thermal use',
	PETElect DOUBLE COMMENT 'Total Primary Energy per all electricity thermal use',
	FECel DOUBLE COMMENT 'Total electricity consumed by the factory',
	FETel DOUBLE COMMENT 'Total electricity consumed by the factory for thermal uses',
	ProdCO2FuelMix DOUBLE COMMENT 'Produced CO2 with the fuel mix',
	ProdCO2Elect DOUBLE COMMENT 'Production of CO2 per electricity',
	PETOTAL_EXT DOUBLE COMMENT 'Total primary energy consumption extrapolated to growth of production volume',
	PE_INT DOUBLE COMMENT 'Primary energy intensity (turnover)',
	EL_OWN DOUBLE COMMENT 'Total own electricity consumption',
	EL_OWN_EXT DOUBLE COMMENT 'Total own electricity consumption extrapolated to growth of production volume',
	EL_INT DOUBLE COMMENT 'Intensity of electricity consumption on turnover',
	FUEL_OWN_EXT DOUBLE COMMENT 'Total own fuel consumption extrapolated to growth of production volume',
	FUEL_INT DOUBLE COMMENT 'Intensity of fuel consumption (LCV) on turnover',
	FEC DOUBLE COMMENT 'Final energy consumption total (for the analysed industry)',
	Nfuels INTEGER COMMENT 'Number of fuels',
	ElecticityThermUse DOUBLE COMMENT 'Electricity for thermal use (total industry)',
	ElectricityNonThermUse DOUBLE COMMENT 'Electricity for non thermal use (total industry)',
	PEConvFuelMix DOUBLE COMMENT 'Conversion to primary energy of fuel mix',
	CO2ConvFuelMix DOUBLE COMMENT 'Specific CO2 emission of fuel mix',
	PEConvFuelCHP DOUBLE COMMENT 'Conversion to primary energy of fuel mix',
	CO2ConvFuelCHP DOUBLE COMMENT 'Specific CO2 emission of fuel mix',
	FuelTariffMix DOUBLE COMMENT 'Mean tariff of the fuel mix',
	FuelTariffCHP DOUBLE COMMENT 'Fuel tariff for CHP',
	NThProc INTEGER COMMENT 'Number of thermal processes',
	USH DOUBLE COMMENT 'Useful Supply Heat for industry (total)',
	FET DOUBLE COMMENT 'Final Energy consumption for Thermal use for industry (total)',
	PRIMARY KEY (CGeneralData_ID)
);



CREATE TABLE CProduct (
	CProduct_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	QProduct_id INTEGER UNSIGNED COMMENT '', 
	PE_SEC DOUBLE COMMENT 'Specific energy consumption (primary energy)',
	EL_SEC DOUBLE COMMENT 'Specific energy consumption (electricity)',
	FUEL_SEC DOUBLE COMMENT 'Specific energy consumption (fuel)',
	PRIMARY KEY (CProduct_ID)
);



CREATE TABLE CFuel (
	CFuel_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',                   
	QFuel_id INTEGER UNSIGNED COMMENT '',    
	FECi DOUBLE COMMENT 'Final energy consumption per fuels (No. 7 = electricity for thermal uses)',
	FETi DOUBLE COMMENT 'total FET per fuel type (for energyStatistics)',
	ProdCO2Fuel DOUBLE COMMENT 'Production of CO2 per fuel type',
	DBFuel_id INTEGER UNSIGNED COMMENT 'Fuel code',
	PRIMARY KEY (CFuel_ID)
);




CREATE TABLE CElectricity (
	CElectricity_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	ELECTRICITY_Type DOUBLE COMMENT 'Electricity by type of use',
	PRIMARY KEY (CElectricity_ID)
);



CREATE TABLE CProcessData (
	CProcessData_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	QProcessData_id INTEGER UNSIGNED COMMENT '',
	UPH DOUBLE COMMENT 'TOTAL- Useful process heat (per process - UPHk)',
	UPHc DOUBLE COMMENT 'circulation / renovation',
	UPHm DOUBLE COMMENT 'maintenance',
	UPHs DOUBLE COMMENT 'preheating at start-up',
	UPHw DOUBLE COMMENT 'available waste heat from processes',
	UPHp DOUBLE COMMENT 'preheating from waste heat',
	UPHmin DOUBLE COMMENT 'minimum required heat demand with heat recovery',
	ProcHC INTEGER COMMENT 'Heating (1) or Cooling (-1)',
	UPCtot DOUBLE COMMENT 'total process cooling demand',
	UPCnet DOUBLE COMMENT 'total process cooling demand after heat recovery',
	PMU VARCHAR(45) COMMENT 'measurement unit for process medium (pmu)',
	MProcMed DOUBLE COMMENT 'yearly quantity of medimum processed',		
	PE_SEC DOUBLE COMMENT 'Specific energy consumption (primary energy)',
	EL_SEC DOUBLE COMMENT 'Specific energy consumption (electricity)',		
	UPH_SEC DOUBLE COMMENT 'Specific energy consumption (UPH)',
	TEnvProc DOUBLE COMMENT 'Temperature of the process environment for calculation of heat losses under operation',
	QdotProc_c DOUBLE COMMENT 'power demand of process while operating circulation / renovation',
	QdotProc_m DOUBLE COMMENT 'power demand of process while operating maintenance',
	QdotProc_s DOUBLE COMMENT 'power demand of process while operating preheating at start-up',
	QdotProc_w DOUBLE COMMENT 'power demand of process while operating waste heat recovery',
	PRIMARY KEY (CProcessData_ID)
);



CREATE TABLE CGenerationHC (
	CGenerationHC_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',         	
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',                                     
	QGenerationHC_id INTEGER UNSIGNED COMMENT '',
	Nequip INTEGER COMMENT 'Number of supply equipments of each type(boilers, …) / No. of units',
	USHj DOUBLE COMMENT 'Useful Supply Heat by equipment',
	FETj DOUBLE COMMENT 'Final energy for thermal use (consumed by each equipment)',
	HGEffAvg DOUBLE COMMENT 'Average conversion efficiency from final energy to useful supply heat', 
	PRIMARY KEY (CGenerationHC_ID)
);



CREATE TABLE CDistributionHC (
	CDistributionHC_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '', 
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	QDistributionHC_id INTEGER UNSIGNED COMMENT '',
	NPIPEDUCT INTEGER COMMENT 'Number of pipes or ducts',
	HDEffAvg DOUBLE COMMENT 'Average distribution efficiency',
	PRIMARY KEY (CDistributionHC_ID)
);



CREATE TABLE CRenewables (
	CRenewables_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '', 
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	QRenewables_id INTEGER UNSIGNED COMMENT '',
	PRIMARY KEY (CRenewables_ID)
);




CREATE TABLE CBuildings (
	CBuildings_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '', 
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	QBuildings_id INTEGER UNSIGNED COMMENT '',
	PRIMARY KEY (CBuildings_ID)
);



CREATE TABLE PSetUpData (
	PSetUpData_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	PEConvEl DOUBLE COMMENT 'Conversion to primary energy of electricity',
	PEConvFuels DOUBLE COMMENT 'Conversion to primary energy of fuels', 
	CO2ConvEl DOUBLE COMMENT 'Specific CO2 emission of electricity',		
	HRInvRate DOUBLE COMMENT 'Specific investment cost for heat recovery system',
	HROMRate DOUBLE COMMENT 'Specific annual O&M cost for heat recovery system',
	FeedInCHP DOUBLE COMMENT 'Feedin Tariff for CHP Electricity',
	SolarInvRateL DOUBLE COMMENT 'Specific turn-key installation cost large systems ( > 1 MW)',
	SolarInvRateS DOUBLE COMMENT 'Specific turn-key installation cost small systems (< 10 kW)',
	SolarOMRate DOUBLE COMMENT 'specific yearly O&M costs',
	SolarFunding DOUBLE COMMENT 'Percentage of public funding',
	QuSolar DOUBLE COMMENT 'Specifc solar useful heat production',
	Inflation DOUBLE COMMENT 'Inflació general',
	InflationFuels DOUBLE COMMENT 'Increment previst preu de combustible (nominal)',
	InterestRate DOUBLE COMMENT 'Interest rate for external financing',
	ExternalFinance DOUBLE COMMENT 'Percentage of external financing',
	Amortisation DOUBLE COMMENT 'Amortisation period',
	Annuity DOUBLE COMMENT 'Annuity of investment',
	EEFunding DOUBLE COMMENT 'Public funding for energy saving measures',
	UHPType VARCHAR(45) COMMENT 'User defined heat pump type - default value',
	UHPMinHop DOUBLE COMMENT 'Minimum desired annual operation hours - default value',
	UHPDTMax DOUBLE COMMENT 'Maximum desired temperature lift - default value',
	UHPTgenIn DOUBLE COMMENT 'Only for abs. HP: Inlet temperature of heating fluid in generator- default value',
	UHPmaxT DOUBLE COMMENT 'Maximum desired condensing temperature - default value',
	UHPminT DOUBLE COMMENT 'Minimum desired evaporating temperature - default value',
	PRIMARY KEY (PSetUpData_ID)
);



CREATE TABLE EBenchmarkGeneralData (
	EBenchmarkGeneralData_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	PE_INT_BML DOUBLE COMMENT 'Primary energy intensity (turnover), benchmark (lower limit)',
	PE_INT_BMH DOUBLE COMMENT 'Primary energy intensity (turnover), benchmark (upper limit)',
	PE_INT_TAR DOUBLE COMMENT 'Primary energy intensity (turnover), target',
	PE_INT_REF VARCHAR(45) COMMENT 'Primary energy intensity (turnover), reference code selected benchmark and target',
	EL_INT_BML DOUBLE COMMENT 'electricity intensity on turnover, benchmark (lower limit)',
	EL_INT_BMH DOUBLE COMMENT 'electricity intensity on turnover, benchmark (upper limit)',
	EL_INT_TAR DOUBLE COMMENT 'electricity intensity on turnover, target',
	EL_INT_REF VARCHAR(45) COMMENT 'electricity intensity on turnover, reference code selected benchmark and target',
	FUEL_INT_BML DOUBLE COMMENT 'Fuel consumption - intensity on turnover, benchmark (lower limit)',
	FUEL_INT_BMH DOUBLE COMMENT 'Fuel consumption - intensity on turnover, benchmark (upper limit)',
	FUEL_INT_TAR DOUBLE COMMENT 'Fuel consumption - intensity on turnover, target',
	FUEL_INT_REF VARCHAR(45) COMMENT 'Fuel consumption - intensity on turnover, reference code selected benchmark and target',
	ENE_INT_CHK DOUBLE COMMENT 'State of evaluation, evaluation of energy intensity',
	ENE_INT_COM DOUBLE COMMENT 'State of evaluation, comment on evaluation of energy intensity',
	PRIMARY KEY (EBenchmarkGeneralData_ID)
);



CREATE TABLE EBenchmarkProductData (
	EBenchmarkProductData_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	QProduct_id INTEGER UNSIGNED COMMENT '',
	PE_SEC_BML DOUBLE COMMENT 'Specific energy consumption (primary energy), benchmark (lower limit)',
	PE_SEC_BMH DOUBLE COMMENT 'Specific energy consumption (primary energy), benchmark (upper limit)',
	PE_SEC_TAR DOUBLE COMMENT 'Specific energy consumption (primary energy), target',
	PE_SEC_REF VARCHAR(45) COMMENT 'Specific energy consumption (primary energy), reference code selected benchmark and target',
	EL_SEC_BML DOUBLE COMMENT 'specific electricity consumption, benchmark (lower limit)',
	EL_SEC_BMH DOUBLE COMMENT 'specific electricity consumption, benchmark (upper limit)',
	EL_SEC_TAR DOUBLE COMMENT 'specific electricity consumption, target',
	EL_SEC_REF VARCHAR(45) COMMENT 'specific electricity consumption, reference code selected benchmark and target',
	FUEL_SEC_BML DOUBLE COMMENT 'Specific fuel consumption, benchmark (lower limit)',
	FUEL_SEC_BMH DOUBLE COMMENT 'Specific fuel consumption, benchmark (upper limit)',
	FUEL_SEC_TAR DOUBLE COMMENT 'Specific fuel consumption, target',
	FUEL_SEC_REF VARCHAR(45) COMMENT 'Specific fuel consumption, reference code selected benchmark and target',
	ENE_SEC_CHK DOUBLE COMMENT 'State of evaluation, evaluation of energy intensity',
	ENE_SEC_COM VARCHAR(45) COMMENT 'comment on evaluation of energy intensity',
	PRIMARY KEY (EBenchmarkProductData_ID)
);




CREATE TABLE EBenchmarkProcessData (
	EBenchmarkProcessData_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	QProcessData_id INTEGER UNSIGNED COMMENT '',
	PE_UOS_BML DOUBLE COMMENT 'Specific energy consumption (primary energy), benchmark (lower limit)',
	PE_UOS_BMH DOUBLE COMMENT 'Specific energy consumption (primary energy), benchmark (upper limit)',
	PE_UOS_TAR DOUBLE COMMENT 'Specific energy consumption (primary energy), target',
	PE_UOS_REF VARCHAR(45) COMMENT 'Specific energy consumption (primary energy), reference code selected benchmark and target',
	EL_UOS_BML DOUBLE COMMENT 'specific electricity consumption, benchmark (lower limit)',
	EL_UOS_BMH DOUBLE COMMENT 'specific electricity consumption, benchmark (upper limit)',
	EL_UOS_TAR DOUBLE COMMENT 'specific electricity consumption, target',
	EL_UOS_REF VARCHAR(45) COMMENT 'specific electricity consumption, reference code selected benchmark and target',
	UPHS_BML DOUBLE COMMENT 'Specific fuel consumption, benchmark (lower limit)',
	UPHS_BMH DOUBLE COMMENT 'Specific fuel consumption, benchmark (upper limit)',
	UPHS_TAR DOUBLE COMMENT 'Specific fuel consumption, target',
	UPHS_REF VARCHAR(45) COMMENT 'Specific fuel consumption, reference code selected benchmark and target',
	ENE_UOS_CHK VARCHAR(45) COMMENT 'evaluation of energy intensity',
	ENE_UOS_COM TEXT COMMENT 'comment on evaluation of energy intensity',
	PRIMARY KEY (EBenchmarkProcessData_ID)
);




CREATE TABLE DBBenchmark (
	DBBenchmark_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	NaceCode_id INTEGER UNSIGNED COMMENT '',
	UnitOperation_id INTEGER UNSIGNED COMMENT '',
	E_EnergyInt_MIN_PC DOUBLE COMMENT 'Energy intensity (production cost) MIN [kWh/€]',
	E_EnergyInt_MAX_PC DOUBLE COMMENT 'Energy intensity (production cost) MAX [kWh/€]',
	E_EnergyInt_TARG_PC DOUBLE COMMENT 'Energy intensity (production cost) TARGET [kWh/€]',
	E_EnergyInt_MIN_T DOUBLE COMMENT 'Energy intensity (turnover) MIN [kWh/€]',
	E_EnergyInt_MAX_T DOUBLE COMMENT 'Energy intensity (turnover) MAX [kWh/€]',
	E_EnergyInt_TARG_T DOUBLE COMMENT 'Electricity: Energy intensity TARGET (turnover) [kWh/€]',
	E_SEC DOUBLE COMMENT 'Specific Energy Consumption (SEC)',
	E_SEC_TARG DOUBLE COMMENT 'Specific Energy Consumption (SEC) TARGET',
	E_SEC_AVG DOUBLE COMMENT 'Electricity: Specific Energy Consumption (SEC) AVERAGE',
	E_Unit VARCHAR(45) COMMENT 'Unit of measurement',
	H_EnergyInt_MIN_PC DOUBLE COMMENT 'Energy intensity (production cost) MIN [kWh/€]',
	H_EnergyInt_MAX_PC DOUBLE COMMENT 'Heat: Energy intensity (production cost) MAX [kWh/€]',
	H_EnergyInt_TARG_PC DOUBLE COMMENT 'Energy intensity (production cost) TARGET [kWh/€]',
	H_EnergyInt_MIN_T DOUBLE COMMENT 'Heat: Energy intensity (turnover) MIN  [kWh/€]',
	H_EnergyInt_MAX_T DOUBLE COMMENT 'Energy intensity (turnover) MAX [kWh/€]',
	H_EnergyInt_TARG_T DOUBLE COMMENT 'Heat: Energy intensity (turnover) TARGET [kWh/€]',
	H_SEC DOUBLE COMMENT 'Specific Energy Consumption (SEC)',
	H_SEC_TARG DOUBLE COMMENT 'Specific Energy Consumption (SEC) TARGET',
	H_SEC_AVG DOUBLE COMMENT 'Specific Energy Consumption (SEC) AVERAGE',
	H_Unit VARCHAR(45) COMMENT 'Unit of measurement',
	T_EnergyInt_MIN_PC DOUBLE COMMENT 'Energy intensity (production cost) MIN [kWh/€]',
	T_EnergyInt_MAX_PC DOUBLE COMMENT 'Energy intensity (production cost) MAX [kWh/€]',
	T_EnergyInt_TARG_PC DOUBLE COMMENT 'Energy intensity (production cost) TARGET [kWh/€]',
	T_EnergyInt_MIN_T DOUBLE COMMENT 'Energy intensity (turnover) MIN [kWh/€]',
	T_EnergyInt_MAX_T DOUBLE COMMENT 'Energy intensity (turnover) MAX [kWh/€]',
	T_EnergyInt_TARG_T DOUBLE COMMENT 'Energy intensity (turnover) TARGET [kWh/€]',
	T_SEC DOUBLE COMMENT 'Specific Energy Consumption (SEC)',
	T_SEC_TARG DOUBLE COMMENT 'Specific Energy Consumption (SEC) TARGET',
	T_SEC_AVG DOUBLE COMMENT 'Specific Energy Consumption (SEC) AVERAGE',
	T_Unit VARCHAR(45) COMMENT 'Unit of measurement',
	Comments TEXT COMMENT 'Comments',
	YearReference INTEGER UNSIGNED COMMENT 'Year (reference for economic data)',
	Reference TEXT COMMENT 'References',
	Literature TEXT COMMENT 'Literature',
	DataRelevance VARCHAR(45) COMMENT 'Data relevance/reliability',
	PRIMARY KEY (DBBenchmark_ID)
);




CREATE TABLE DBNaceCode (
	DBNaceCode_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	CodeNACE VARCHAR(45) COMMENT 'Industrial sector_NACE Code',
	CodeNACEsub VARCHAR(45) COMMENT 'Industrial subsector_NACE Code',
	NameNACE VARCHAR(200) COMMENT 'Industrial sector_NACE Name',
	NameNACEsub VARCHAR(200) COMMENT 'Industrial subsector_NACE Name',
	ProductName VARCHAR(200) COMMENT 'Product',
	NationalCode VARCHAR(45) COMMENT 'Industrial sector National Code',
	NationalSubCode VARCHAR(45) COMMENT 'Industrial subsector National Code',
	NameNationalCode VARCHAR(200) COMMENT 'Industrial sector National Name',
	NameNationalSubCode VARCHAR(200) COMMENT 'Industrial subsector National Name',
	PRIMARY KEY (DBNaceCode_ID)
);




CREATE TABLE DBUnitOperation (
	DBUnitOperation_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	UnitOperation VARCHAR(45) COMMENT 'Unit Operation',
	UnitOperationCode VARCHAR(45) COMMENT 'Unit Operation code',
	UnitOperationDescrip VARCHAR(200) COMMENT 'Unit Operation description',
	PRIMARY KEY (DBUnitOperation_ID)
);



CREATE TABLE DBCHP (
	DBCHP_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	CHPequip VARCHAR(45) COMMENT 'Type of equipment',
	CHPPe DOUBLE COMMENT 'Electric power [kW]',
	CHPPt DOUBLE COMMENT 'Thermal power [kW]',
	FuelConsum DOUBLE COMMENT 'Fuel consumption [kW] (LCV)',
	Eta_e DOUBLE COMMENT 'Electric efficiency',
	Eta_t DOUBLE COMMENT 'Thermal efficiency',
	InvRate DOUBLE COMMENT 'Investment cost [€/kW_el]',
	OMRateFix DOUBLE COMMENT 'Fixed Operation and Maintenance costs [€/kW_el year]',
	OMRateVar DOUBLE COMMENT 'Variable Operation and Maintenance costs [€/kW_el]',
	PRIMARY KEY (DBCHP_ID)
);



CREATE TABLE DBHeatPump (
	DBHeatPump_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	HPManData VARCHAR(45) COMMENT 'Manufacturer data is provided only for Heating (H), Cooling (C), or both (HC)',
	HPManufacturer VARCHAR(45) COMMENT 'Manufacturer',
	HPModel VARCHAR(45) COMMENT 'Model',
	HPType VARCHAR(45) COMMENT 'Type of HP: compression or absorption',
	HPSubType VARCHAR(45) COMMENT 'Heat source - Heat sink, e.g. water-water',
	HPAbsEffects VARCHAR(45) COMMENT 'Only abs. HP: effects: 1, 2, or 3',
	HPAbsHeatMed VARCHAR(45) COMMENT 'Onlo abs HP: Heating medium in generator:hot water, vapour, exhaust gas, directfired',
	HPWorkFluid VARCHAR(45) COMMENT 'Absorbent-refrigerant pair, e.g. LiBr-H2O',
	HPCoolCap DOUBLE COMMENT 'Nominal Cooling capacity [kW]',
	HPCoolCOP DOUBLE COMMENT 'Nominal COP cooling',
	HPExCoolCOP DOUBLE COMMENT 'Exergetic COP cooling',
	HPThCoolCOP DOUBLE COMMENT 'Theoretical COP cooling',
	HPConstExCoolCOP DOUBLE COMMENT 'Temperature interval COPex is assumed constant, cooling',
	HPAbsTinC DOUBLE COMMENT 'Absorber inlet temperature, cooling mode, catalogue (sec. fluid)',
	HPCondTinC DOUBLE COMMENT 'Condenser inlet temperature, cooling mode, catalogue (sec. fluid)',
	HPGenTinC DOUBLE COMMENT 'Generator inlet temperature, cooling mode, catalogue (sec. fluid)',
	HPEvapTinC DOUBLE COMMENT 'Evaporator inlet temperature, cooling mode, catalogue (sec. fluid)',
	HPHeatCap DOUBLE COMMENT 'Nominal Heating capacity [kW]',
	HPHeatCOP DOUBLE COMMENT 'Nominal COP heating',
	HPExHeatCOP DOUBLE COMMENT 'Exergetic COP heating',
	HPThHeatCOP DOUBLE COMMENT 'Theoretical COP heating',
	HPConstExHeatCOP DOUBLE COMMENT 'Temperature interval COPex is assumed constant, heating',
	HPAbsTinH DOUBLE COMMENT 'Absorber inlet temperature, heating mode, catalogue (sec. fluid)',
	HPCondTinH DOUBLE COMMENT 'Condenser inlet temperature, heating mode, catalogue (sec. fluid)',
	HPGenTinH DOUBLE COMMENT 'Generator inlet temperature, heating mode, catalogue (sec. fluid)',
	HPEvapTinH DOUBLE COMMENT 'Evaporator inlet temperature, heating mode, catalogue (sec. fluid)',
	HPLimDT DOUBLE COMMENT 'Working Limit temperature difference (lift)',
	HPGenTmin DOUBLE COMMENT 'Minimum generator temperature (primary)-work limit',
	HPCondTmax  DOUBLE COMMENT 'Maximum condensing (and absorber) temperature (primary)-work limit',
	HPEvapTmin DOUBLE COMMENT 'Minimum evaporating temperature (primary)-work limit',
	HPElectConsum DOUBLE COMMENT 'Electricity consumption [kW]',
	HPPrice DOUBLE COMMENT 'Equipment factory price incl. discount [euro]',
	HPTurnKeyPrice DOUBLE COMMENT 'Equipment turn-key price [euro]',
	HPOandMfix DOUBLE COMMENT 'Ratio O&M costs fixed [euro/kW year, heating]',
	HPOandMvar DOUBLE COMMENT 'Ratio O&M costs variable [euro/MWh year, heating]',
	HPYearUpdate INTEGER COMMENT 'Year of last data update',
	PRIMARY KEY (DBHeatPump_ID)
);


CREATE TABLE UHeatPump (
	UHeatPump_ID INTEGER UNSIGNED NOT NULL COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	UHPType VARCHAR(45) COMMENT 'User defined heat pump type',
	UHPMinHop DOUBLE COMMENT 'Minimum desired annual operation hours',
	UHPDTMax DOUBLE COMMENT 'Maximum desired temperature lift',
	UHPTgenIn DOUBLE COMMENT 'Only for abs. HP: Inlet temperature of heating fluid in generator',
	UHPmaxT DOUBLE COMMENT 'Maximum desired condensing temperature',
	UHPminT DOUBLE COMMENT 'Minimum desired evaporating temperature',
	PRIMARY KEY (UHeatPump_ID)
);


CREATE TABLE HPHourlyInternalData (
	HPHourlyInternalData_ID INTEGER UNSIGNED NOT NULL COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	Thi DOUBLE COMMENT 'Hot, condensing =(absorbtion) temperature, ºC',
	Tci DOUBLE COMMENT 'Cold, evaporating temperature, ºC',
	COPhi DOUBLE COMMENT 'Calculated hourly real COP',
	COPhti DOUBLE COMMENT 'Calculated hourly theoretical COP',
	dotQhi DOUBLE COMMENT 'Hourly calculated heating capacity, kW',
	dotQci DOUBLE COMMENT 'Hourly calculated cooling capacity, kW',
	dotQwi DOUBLE COMMENT 'Hourly calculated consumed power, kW',
	Fpli DOUBLE COMMENT 'Hourly part load factor',
	PRIMARY KEY (HPHourlyInternalData_ID)
);


CREATE TABLE HPAnnualInternalData (
	HPAnnualInternalData_ID INTEGER UNSIGNED NOT NULL COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	HPid INTEGER COMMENT 'ID of the HP selected from database',
	dotQhDB DOUBLE COMMENT 'Nominal Heating capacity of the HP selected from DB',
	Fpla DOUBLE COMMENT 'Annual part load factor = Annually operating hours',
	PRIMARY KEY (HPAnnualInternalData_ID)
);


CREATE TABLE DBFluid (
	DBFluid_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	FluidName VARCHAR(45) COMMENT 'Fluid name',
	FluidCp DOUBLE COMMENT 'Fluid specific heat capacity [J/kgK]',
	FluidDensity DOUBLE COMMENT 'Fluid density [kg/m3]',
	FluidComment VARCHAR(200) COMMENT 'Comments',
	PRIMARY KEY (DBFluid_ID)
);



CREATE TABLE DBFuel (
	DBFuel_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	FuelName VARCHAR(45) COMMENT 'Name of fuel',
	DBFuelUnit VARCHAR(45) COMMENT 'Unit (kg, l, m3,….)',
	FuelCode VARCHAR(45) COMMENT '', 
	FuelLCV DOUBLE COMMENT 'Fuel low calorific value [kWh/unit]',
	FuelHCV DOUBLE COMMENT 'Fuel high calorific value [kWh/unit]',
	tCO2 DOUBLE COMMENT 'Tons of CO2 per MWh_lcv',
	FuelDensity DOUBLE COMMENT 'Density of fuel [kg/m3]',
	ConversPrimEnergy DOUBLE COMMENT 'Conversion factor to primary energy',
	FuelDataSource VARCHAR(200) COMMENT 'Source for fuel data',
	FuelComment VARCHAR(200) COMMENT 'Comments',
	PRIMARY KEY (DBFuel_ID)
);


CREATE TABLE EnergyFlowsQDa (
	EnergyFlowsQDa_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT'',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	IndexNo INTEGER COMMENT 'Index of the row, only one in this table',
	T0 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T5 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T10 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T15 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T20 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T25 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T30 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T35 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T40 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T45 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T50 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T55 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T60 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T65 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T70 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T75 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T80 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T85 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T90 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T95 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T100 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T105 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T110 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T115 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T120 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T125 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T130 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T135 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T140 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T145 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T150 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T155 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T160 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T165 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T170 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T175 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T180 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T185 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T190 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T195 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T200 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T205 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T210 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T215 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T220 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T225 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T230 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T235 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T240 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T245 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T250 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T255 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T260 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T265 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T270 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T275 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T280 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T285 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T290 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T295 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T300 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T305 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T310 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T315 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T320 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T325 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T330 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T335 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T340 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T345 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T350 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T355 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T360 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T365 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T370 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T375 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T380 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T385 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T390 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T395 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T400 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	PRIMARY KEY (EnergyFlowsQDa_ID)
);


CREATE TABLE EnergyFlowsQAa (
	EnergyFlowsQAa_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	IndexNo INTEGER COMMENT 'Index of the row, only one in this table',
	T0 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T5 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T10 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T15 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T20 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T25 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T30 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T35 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T40 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T45 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T50 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T55 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T60 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T65 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T70 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T75 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T80 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T85 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T90 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T95 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T100 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T105 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T110 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T115 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T120 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T125 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T130 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T135 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T140 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T145 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T150 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T155 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T160 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T165 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T170 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T175 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T180 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T185 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T190 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T195 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T200 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T205 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T210 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T215 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T220 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T225 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T230 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T235 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T240 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T245 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T250 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T255 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T260 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T265 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T270 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T275 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T280 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T285 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T290 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T295 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T300 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T305 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T310 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T315 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T320 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T325 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T330 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T335 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T340 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T345 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T350 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T355 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T360 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T365 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T370 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T375 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T380 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T385 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T390 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T395 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T400 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	PRIMARY KEY (EnergyFlowsQAa_ID)
);


CREATE TABLE EnergyFlowsQDh (
	EnergyFlowsQDh_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	IndexNo INTEGER COMMENT 'Index of the row, 8760 in this table',
	T0 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T5 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T10 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T15 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T20 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T25 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T30 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T35 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T40 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T45 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T50 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T55 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T60 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T65 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T70 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T75 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T80 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T85 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T90 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T95 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T100 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T105 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T110 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T115 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T120 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T125 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T130 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T135 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T140 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T145 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T150 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T155 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T160 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T165 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T170 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T175 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T180 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T185 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T190 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T195 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T200 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T205 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T210 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T215 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T220 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T225 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T230 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T235 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T240 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T245 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T250 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T255 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T260 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T265 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T270 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T275 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T280 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T285 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T290 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T295 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T300 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T305 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T310 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T315 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T320 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T325 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T330 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T335 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T340 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T345 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T350 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T355 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T360 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T365 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T370 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T375 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T380 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T385 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T390 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T395 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T400 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	PRIMARY KEY (EnergyFlowsQDh_ID)
);


CREATE TABLE EnergyFlowsQAh (
	EnergyFlowsQAh_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	IndexNo INTEGER COMMENT 'Index of the row, 8760 in this table',
	T0 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T5 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T10 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T15 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T20 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T25 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T30 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T35 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T40 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T45 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T50 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T55 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T60 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T65 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T70 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T75 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T80 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T85 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T90 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T95 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T100 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T105 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T110 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T115 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T120 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T125 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T130 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T135 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T140 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T145 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T150 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T155 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T160 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T165 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T170 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T175 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T180 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T185 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T190 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T195 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T200 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T205 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T210 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T215 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T220 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T225 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T230 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T235 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T240 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T245 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T250 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T255 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T260 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T265 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T270 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T275 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T280 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T285 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T290 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T295 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T300 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T305 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T310 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T315 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T320 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T325 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T330 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T335 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T340 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T345 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T350 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T355 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T360 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T365 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T370 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T375 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T380 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T385 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T390 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T395 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T400 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	PRIMARY KEY (EnergyFlowsQAh_ID)
);




CREATE TABLE EnergyFlowsQDaRec (
	EnergyFlowsQDaRec_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	IndexNo INTEGER COMMENT 'Index of the row, only one in this table',
	T0 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T5 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T10 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T15 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T20 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T25 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T30 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T35 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T40 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T45 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T50 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T55 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T60 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T65 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T70 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T75 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T80 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T85 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T90 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T95 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T100 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T105 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T110 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T115 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T120 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T125 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T130 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T135 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T140 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T145 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T150 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T155 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T160 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T165 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T170 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T175 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T180 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T185 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T190 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T195 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T200 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T205 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T210 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T215 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T220 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T225 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T230 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T235 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T240 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T245 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T250 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T255 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T260 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T265 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T270 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T275 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T280 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T285 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T290 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T295 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T300 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T305 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T310 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T315 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T320 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T325 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T330 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T335 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T340 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T345 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T350 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T355 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T360 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T365 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T370 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T375 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T380 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T385 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T390 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T395 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	T400 DOUBLE COMMENT 'Annual Heat demand at this temperature level in [MWh]',
	PRIMARY KEY (EnergyFlowsQDaRec_ID)
);


CREATE TABLE EnergyFlowsQAaRec (
	EnergyFlowsQAaRec_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	IndexNo INTEGER COMMENT 'Index of the row, only one in this table',
	T0 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T5 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T10 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T15 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T20 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T25 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T30 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T35 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T40 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T45 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T50 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T55 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T60 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T65 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T70 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T75 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T80 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T85 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T90 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T95 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T100 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T105 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T110 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T115 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T120 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T125 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T130 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T135 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T140 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T145 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T150 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T155 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T160 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T165 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T170 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T175 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T180 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T185 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T190 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T195 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T200 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T205 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T210 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T215 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T220 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T225 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T230 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T235 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T240 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T245 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T250 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T255 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T260 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T265 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T270 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T275 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T280 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T285 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T290 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T295 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T300 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T305 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T310 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T315 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T320 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T325 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T330 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T335 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T340 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T345 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T350 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T355 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T360 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T365 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T370 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T375 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T380 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T385 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T390 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T395 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	T400 DOUBLE COMMENT 'Annual Heat availability at this temperature level in [MWh]',
	PRIMARY KEY (EnergyFlowsQAaRec_ID)
);


CREATE TABLE EnergyFlowsQDhRec (
	EnergyFlowsQDhRec_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	IndexNo INTEGER COMMENT 'Index of the row, 8760 in this table',
	T0 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T5 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T10 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T15 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T20 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T25 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T30 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T35 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T40 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T45 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T50 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T55 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T60 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T65 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T70 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T75 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T80 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T85 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T90 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T95 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T100 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T105 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T110 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T115 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T120 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T125 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T130 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T135 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T140 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T145 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T150 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T155 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T160 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T165 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T170 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T175 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T180 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T185 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T190 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T195 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T200 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T205 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T210 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T215 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T220 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T225 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T230 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T235 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T240 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T245 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T250 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T255 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T260 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T265 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T270 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T275 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T280 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T285 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T290 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T295 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T300 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T305 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T310 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T315 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T320 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T325 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T330 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T335 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T340 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T345 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T350 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T355 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T360 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T365 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T370 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T375 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T380 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T385 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T390 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T395 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	T400 DOUBLE COMMENT 'Hourly Heat demand at this temperature level in [MWh]',
	PRIMARY KEY (EnergyFlowsQDhRec_ID)
);


CREATE TABLE EnergyFlowsQAhRec (
	EnergyFlowsQAhRec_ID INTEGER UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '',
	Questionnaire_id INTEGER UNSIGNED COMMENT '',
	AlternativeProposalNo INTEGER UNSIGNED DEFAULT 0 COMMENT '',
	IndexNo INTEGER COMMENT 'Index of the row, 8760 in this table',
	T0 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T5 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T10 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T15 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T20 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T25 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T30 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T35 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T40 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T45 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T50 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T55 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T60 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T65 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T70 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T75 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T80 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T85 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T90 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T95 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T100 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T105 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T110 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T115 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T120 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T125 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T130 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T135 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T140 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T145 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T150 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T155 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T160 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T165 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T170 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T175 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T180 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T185 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T190 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T195 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T200 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T205 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T210 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T215 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T220 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T225 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T230 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T235 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T240 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T245 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T250 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T255 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T260 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T265 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T270 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T275 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T280 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T285 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T290 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T295 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T300 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T305 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T310 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T315 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T320 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T325 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T330 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T335 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T340 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T345 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T350 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T355 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T360 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T365 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T370 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T375 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T380 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T385 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T390 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T395 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	T400 DOUBLE COMMENT 'Hourly Heat availability at this temperature level in [MWh]',
	PRIMARY KEY (EnergyFlowsQAhRec_ID)
);
