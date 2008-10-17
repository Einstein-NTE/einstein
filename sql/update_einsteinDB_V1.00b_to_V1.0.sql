-- update einstein database for Release Version 1.0
-- includes updates no. 28 .. 42

USE einstein;

ALTER DATABASE einstein DEFAULT CHARACTER SET 'utf8';

ALTER TABLE cgeneraldata ADD COLUMN CompSpecificDiscountRate DOUBLE COMMENT 'Company Specific Discount rate' AFTER InterestExtFinancing;
ALTER TABLE cgeneraldata ADD COLUMN PayBack DOUBLE COMMENT '' AFTER BCR;
ALTER TABLE cgeneraldata ADD COLUMN EnergySystemCost DOUBLE COMMENT 'Energy cost including OM and annuity' AFTER EnergyCost;
ALTER TABLE cgeneraldata ADD COLUMN AddCost DOUBLE COMMENT 'Additional Cost' AFTER EnergySystemCost;
ALTER TABLE cgeneraldata ADD COLUMN AddCostperSavedPE DOUBLE COMMENT 'Additional Cost per saved primary energy' AFTER AddCost;
ALTER TABLE cgeneraldata ADD COLUMN RevenueSaleEquipment DOUBLE COMMENT '' AFTER Subsidies;

ALTER TABLE qgenerationhc CHANGE COLUMN HeatSourceLT HeatSourceLT VARCHAR(200);
ALTER TABLE qgenerationhc CHANGE COLUMN HeatSourceHT HeatSourceHT VARCHAR(200);
ALTER TABLE qgenerationhc ADD COLUMN OandM DOUBLE After TurnKeyPrice;
ALTER TABLE qgenerationhc CHANGE COLUMN HeatSourceLT HeatSourceLT VARCHAR(200) COMMENT '' AFTER ExcessAirRatio;
ALTER TABLE qgenerationhc CHANGE COLUMN HeatSourceHT HeatSourceHT VARCHAR(200) COMMENT '' AFTER HeatSourceLT;
ALTER TABLE qgenerationhc CHANGE COLUMN DestinationWasteHeat DestinationWasteHeat VARCHAR(200) COMMENT '' AFTER Refrigerant;
ALTER TABLE qgenerationhc CHANGE COLUMN Refrigerant Refrigerant INTEGER COMMENT '' AFTER THeatSourceHT;

ALTER TABLE qheatexchanger ADD COLUMN StreamStatusSource VARCHAR(200) AFTER StreamType;
ALTER TABLE qheatexchanger ADD COLUMN StreamTypeSource VARCHAR(200) AFTER StreamStatusSource;
ALTER TABLE qheatexchanger ADD COLUMN StreamStatusSink VARCHAR(200) AFTER StreamTypeSource;
ALTER TABLE qheatexchanger ADD COLUMN StreamTypeSink VARCHAR(200) AFTER StreamStatusSink;
ALTER TABLE qheatexchanger DROP COLUMN StreamStatus;
ALTER TABLE qheatexchanger DROP COLUMN StreamType;
ALTER TABLE qheatexchanger CHANGE COLUMN StreamStatusSource StreamStatusSource VARCHAR(200) AFTER StorageSize;
ALTER TABLE qheatexchanger CHANGE COLUMN StreamStatusSink StreamStatusSink VARCHAR(200) AFTER StreamStatusSource;
ALTER TABLE qheatexchanger CHANGE COLUMN StreamTypeSink StreamTypeSink VARCHAR(200) AFTER StreamStatusSink;
ALTER TABLE qheatexchanger CHANGE COLUMN StreamTypeSource StreamTypeSource VARCHAR(200) AFTER StreamTypeSink;



ALTER TABLE questionnaire ADD COLUMN OMGenUtilities DOUBLE COMMENT 'General maintenance - Utilities and operating materials costs' AFTER OMGenTot;
ALTER TABLE questionnaire ADD COLUMN OMGenLabour DOUBLE COMMENT 'General maintenance - Labour costs' AFTER OMGenUtilities;
ALTER TABLE questionnaire ADD COLUMN OMGenExternal DOUBLE COMMENT 'General maintenance - External costs' AFTER OMGenLabour;
ALTER TABLE questionnaire ADD COLUMN OMGenRegulatory DOUBLE COMMENT 'General maintenance - Regulatory compliance, insurance and future liability costs' AFTER OMGenExternal;
ALTER TABLE questionnaire ADD COLUMN OMBuildUtilities DOUBLE COMMENT 'Buildings - Utilities and operating materials costs' AFTER OMBuildTot;
ALTER TABLE questionnaire ADD COLUMN OMBuildLabour DOUBLE COMMENT 'Buildings - Labour costs' AFTER OMBuildUtilities;
ALTER TABLE questionnaire ADD COLUMN OMBuildExternal DOUBLE COMMENT 'Buildings - External costs' AFTER OMBuildLabour;
ALTER TABLE questionnaire ADD COLUMN OMBuildRegulatory DOUBLE COMMENT 'Buildings - Regulatory compliance, insurance and future liability costs' AFTER OMBuildExternal;
ALTER TABLE questionnaire ADD COLUMN OMMachEquipUtilities DOUBLE COMMENT 'Machines and equipment - Utilities and operating materials costs' AFTER OMMachEquipTot;
ALTER TABLE questionnaire ADD COLUMN OMMachEquipLabour DOUBLE COMMENT 'Machines and equipment - Labour costs' AFTER OMMachEquipTot;
ALTER TABLE questionnaire ADD COLUMN OMMachEquipExternal DOUBLE COMMENT 'Machines and equipment  - External costs' AFTER OMMachEquipLabour;
ALTER TABLE questionnaire ADD COLUMN OMMachEquipRegulatory DOUBLE COMMENT 'Machines and equipment  - Regulatory compliance, insurance and future liability costs' AFTER OMMachEquipExternal;
ALTER TABLE questionnaire ADD COLUMN OMHCGenDistUtilities DOUBLE COMMENT 'Generation and distribution of heat and cold - Utilities and operating materials costs' AFTER OMHCGenDistTot;
ALTER TABLE questionnaire ADD COLUMN OMHCGenDistLabour DOUBLE COMMENT 'Generation and distribution of heat and cold - Labour costs' AFTER OMHCGenDistUtilities;
ALTER TABLE questionnaire ADD COLUMN OMHCGenDistExternal DOUBLE COMMENT 'Generation and distribution of heat and cold  - External costs' AFTER OMHCGenDistUtilities;
ALTER TABLE questionnaire ADD COLUMN OMHCGenDistRegulatory DOUBLE COMMENT 'Generation and Distribution of heat and cold  - Regulatory compliance, insurance and future liability costs' AFTER OMHCGenDistExternal;
ALTER TABLE questionnaire ADD COLUMN OMTotalUtilities DOUBLE COMMENT 'Total - Utilities and operating materials costs' AFTER OMTotalTot;
ALTER TABLE questionnaire ADD COLUMN OMTotalLabour DOUBLE COMMENT 'Total - Labour costs' AFTER OMTotalTot;
ALTER TABLE questionnaire ADD COLUMN OMTotalExternal DOUBLE COMMENT 'Total - External costs' AFTER OMTotalLabour;
ALTER TABLE questionnaire ADD COLUMN OMTotalRegulatory DOUBLE COMMENT 'Total - Regulatory compliance, insurance and future liability costs' AFTER OMTotalExternal;

ALTER TABLE questionnaire ADD COLUMN CompSpecificDiscountRate DOUBLE COMMENT 'Company Specific Discount Rate' AFTER InterestExtFinancing;

ALTER TABLE questionnaire DROP COLUMN OMGenOP;
ALTER TABLE questionnaire DROP COLUMN OMGenEP;
ALTER TABLE questionnaire DROP COLUMN OMGenFung;
ALTER TABLE questionnaire DROP COLUMN OMBuildOP;
ALTER TABLE questionnaire DROP COLUMN OMBuildEP;
ALTER TABLE questionnaire DROP COLUMN OMBuildFung;
ALTER TABLE questionnaire DROP COLUMN OMMachEquipOP;
ALTER TABLE questionnaire DROP COLUMN OMMachEquipEP;
ALTER TABLE questionnaire DROP COLUMN OMMachEquipFung;
ALTER TABLE questionnaire DROP COLUMN OMHCGenDistOP;
ALTER TABLE questionnaire DROP COLUMN OMHCGenDistEP;
ALTER TABLE questionnaire DROP COLUMN OMHCGenDistFung;
ALTER TABLE questionnaire DROP COLUMN OMTotalOP;
ALTER TABLE questionnaire DROP COLUMN OMTotalEP;
ALTER TABLE questionnaire DROP COLUMN OMTotalFung;

ALTER TABLE questionnaire DROP COLUMN OMGenExtenal;
ALTER TABLE questionnaire DROP COLUMN OMBuildExtenal;
ALTER TABLE questionnaire DROP COLUMN OMMachEquipExtenal;
ALTER TABLE questionnaire DROP COLUMN OMHCGenDistExtenal;
ALTER TABLE questionnaire DROP COLUMN OMTotalExtenal;

ALTER TABLE sproject ADD COLUMN Summary TEXT COMMENT 'Audit summary' AFTER UnitsReport;
ALTER TABLE sproject ADD COLUMN HRTool VarChar(45) COMMENT 'Heat recovery calculation tool' AFTER Summary;

ALTER TABLE uheatpump ADD COLUMN CHPEff DOUBLE AFTER AlternativeProposalNo;
ALTER TABLE uheatpump ADD COLUMN CHPHOp DOUBLE AFTER AlternativeProposalNo;
ALTER TABLE uheatpump ADD COLUMN CHPFuelType VARCHAR(45) AFTER AlternativeProposalNo;
ALTER TABLE uheatpump ADD COLUMN CHPType VARCHAR(45) AFTER AlternativeProposalNo;
ALTER TABLE uheatpump ADD COLUMN CHPMaintain TINYINT AFTER AlternativeProposalNo;


-- update 031
-- TCA

CREATE TABLE IF NOT EXISTS `tcacontingencies` (
  `TcaID` int(11) NOT NULL,
  `Description` varchar(200) NOT NULL,
  `Value` float NOT NULL,
  `TimeFrame` int(11) NOT NULL
) TYPE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `tcadetailedopcost`
--

CREATE TABLE IF NOT EXISTS `tcadetailedopcost` (
  `TcaID` int(11) NOT NULL,
  `Description` varchar(200) NOT NULL,
  `Value` float NOT NULL,
  `Category` int(11) NOT NULL COMMENT '0-6 for the 7 subcategories'
) TYPE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `tcadetailedrevenue`
--

CREATE TABLE IF NOT EXISTS `tcadetailedrevenue` (
  `TcaID` int(11) NOT NULL,
  `Description` varchar(200) NOT NULL,
  `InitialInvestment` float NOT NULL,
  `DeprecationPeriod` int(11) NOT NULL,
  `RemainingPeriod` int(11) NOT NULL
) TYPE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `tcaenergy`
--

CREATE TABLE IF NOT EXISTS `tcaenergy` (
  `TcaID` int(11) NOT NULL,
  `Description` varchar(200) NOT NULL,
  `EnergyDemand` float NOT NULL,
  `EnergyPrice` float NOT NULL,
  `DevelopmentOfEnergyPrice` float NOT NULL
) TYPE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `tcageneraldata`
--

CREATE TABLE IF NOT EXISTS `tcageneraldata` (
  `IDTca` int(11) NOT NULL auto_increment,
  `ProjectID` int(11) NOT NULL,
  `AlternativeProposalNo` int(11) NOT NULL,
  `InflationRate` float NOT NULL,
  `NominalInterestRate` float NOT NULL COMMENT 'Nominal interrest rate of external financing',
  `CompSpecificDiscountRate` float NOT NULL,
  `FulePriceRate` float NOT NULL,
  `AmotisationTime` int(11) NOT NULL,
  `TotalOperatingCost` float NOT NULL,
  `TotalRevenue` float NOT NULL,
  PRIMARY KEY  (`IDTca`)
) TYPE=MyISAM AUTO_INCREMENT=32 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `tcainvestments`
--

CREATE TABLE IF NOT EXISTS `tcainvestments` (
  `TcaID` int(11) NOT NULL,
  `Description` varchar(200) NOT NULL,
  `Investment` float NOT NULL,
  `FundingPerc` float NOT NULL,
  `FundingFix` float NOT NULL
) TYPE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `tcanonreoccuringcosts`
--

CREATE TABLE IF NOT EXISTS `tcanonreoccuringcosts` (
  `TcaID` int(11) NOT NULL,
  `Description` varchar(200) NOT NULL,
  `Value` float NOT NULL,
  `Year` int(11) NOT NULL,
  `Type` varchar(200) NOT NULL COMMENT 'Cost or Revenue'
) TYPE=MyISAM;


-- update 032

ALTER TABLE qprocessdata DROP COLUMN UPHtotQ;
ALTER TABLE cgeneraldata DROP COLUMN OMBiuildFung;

ALTER TABLE qdistributionhc CHANGE COLUMN UDistPipe UAPipe DOUBLE COMMENT 'Total pipe heat loss coefficient';
ALTER TABLE questionnaire CHANGE COLUMN Address Address VARCHAR(200) COMMENT 'Address of industry';


-- update 033

ALTER TABLE dbbenchmark CHANGE COLUMN DataRelevance DataRelevance VARCHAR(200);

ALTER TABLE qheatexchanger CHANGE HXSource HXSource VARCHAR( 300 );  
ALTER TABLE qheatexchanger CHANGE HXSink HXSink VARCHAR( 300 );  
ALTER TABLE qheatexchanger CHANGE HXName HXName VARCHAR( 300 );  
ALTER TABLE qheatexchanger CHANGE HXType HXType VARCHAR( 300 );


-- update 034


DROP TABLE IF EXISTS `poefficiencymeasure`;
CREATE TABLE IF NOT EXISTS `poefficiencymeasure` (
  `IDEfficiencyMeasure` int(11) NOT NULL auto_increment,
  `ShortDescription` varchar(300) NOT NULL,
  `Text` text NOT NULL,
  PRIMARY KEY  (`IDEfficiencyMeasure`)
) ENGINE=MyISAM AUTO_INCREMENT=7 ;

--
-- Daten für Tabelle `poefficiencymeasure`
--

INSERT INTO `poefficiencymeasure` (`IDEfficiencyMeasure`, `ShortDescription`, `Text`) VALUES
(1, 'EM0001 (Freecooling)', 'Freecooling: Condensation of the cooling agent via outside air (at colder air temperatures), no need for cooling machine operation at low outside temperatures'),
(2, 'EM0002 (Blabla)', 'blabla!'),
(6, 'EM0003 (Juhu!)', 'Beim Absturz der Aktienkurse in den USA am Montag sind etwa 1,2 Billionen Dollar (834 Milliarden Euro) Boersenwert vernichtet worden. Dies ergibt sich aus dem Dow-Jones-Wilshire-5000-Index, dem groessten Messwert fuer Boersenbewegungen in den USA. Damit sind die Verluste fast doppelt so hoch wie das von der US-Regierung geplante Rettungspaket fuer den US-Finanzsektor. \n<a href="http://www.kleinezeitung.at">Link zu weiteren Informationen</a>');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `poemlist`
--

DROP TABLE IF EXISTS `poemlist`;
CREATE TABLE IF NOT EXISTS `poemlist` (
  `IDEMList` int(11) NOT NULL auto_increment,
  `TechnologyID` int(11) NOT NULL,
  `TypicalProcessID` int(11) NOT NULL,
  PRIMARY KEY  (`IDEMList`)
) ENGINE=MyISAM AUTO_INCREMENT=13 ;

--
-- Daten für Tabelle `poemlist`
--

INSERT INTO `poemlist` (`IDEMList`, `TechnologyID`, `TypicalProcessID`) VALUES
(1, 1, 1),
(12, 3, 5),
(10, 2, 1),
(9, 2, 5);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `poemlistentry`
--

DROP TABLE IF EXISTS `poemlistentry`;
CREATE TABLE IF NOT EXISTS `poemlistentry` (
  `EMListID` int(11) NOT NULL,
  `EfficiencyMeasureID` int(11) NOT NULL
) ENGINE=MyISAM;

--
-- Daten für Tabelle `poemlistentry`
--

INSERT INTO `poemlistentry` (`EMListID`, `EfficiencyMeasureID`) VALUES
(10, 6),
(1, 2),
(1, 1),
(5, 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `posector`
--

DROP TABLE IF EXISTS `posector`;
CREATE TABLE IF NOT EXISTS `posector` (
  `IDsector` int(11) NOT NULL auto_increment,
  `Name` varchar(300) NOT NULL,
  PRIMARY KEY  (`IDsector`)
) ENGINE=MyISAM AUTO_INCREMENT=15 ;

--
-- Daten für Tabelle `posector`
--

INSERT INTO `posector` (`IDsector`, `Name`) VALUES
(13, 'Manufacture of food product, beverages and tabacco'),
(14, 'Manufacture of basic metals and fabricated metal products');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `posubsector`
--

DROP TABLE IF EXISTS `posubsector`;
CREATE TABLE IF NOT EXISTS `posubsector` (
  `IDSubsector` int(11) NOT NULL auto_increment,
  `SectorID` int(11) NOT NULL,
  `Name` varchar(300) NOT NULL,
  PRIMARY KEY  (`IDSubsector`)
) ENGINE=MyISAM AUTO_INCREMENT=18 ;

--
-- Daten für Tabelle `posubsector`
--

INSERT INTO `posubsector` (`IDSubsector`, `SectorID`, `Name`) VALUES
(2, 13, 'Meat'),
(5, 13, 'Fish'),
(3, 14, 'Iron'),
(4, 14, 'Steel'),
(6, 13, 'fruits/vegetables/herbs'),
(7, 13, 'fats/oils'),
(8, 13, 'milk products'),
(9, 13, 'starch/potatos/grain/mill products'),
(10, 13, 'other food products'),
(11, 13, 'Beverage'),
(12, 14, 'Copper'),
(13, 14, 'Brass'),
(14, 14, 'Alloys'),
(15, 14, 'Other metals'),
(16, 14, 'Plastic'),
(17, 14, 'Printed circuit board');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `posubsector_to_uo`
--

DROP TABLE IF EXISTS `posubsector_to_uo`;
CREATE TABLE IF NOT EXISTS `posubsector_to_uo` (
  `SubsectorID` int(11) NOT NULL,
  `UnitOperationID` int(11) NOT NULL
) ENGINE=MyISAM;

--
-- Daten für Tabelle `posubsector_to_uo`
--

INSERT INTO `posubsector_to_uo` (`SubsectorID`, `UnitOperationID`) VALUES
(4, 2),
(4, 1),
(2, 1);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `potech`
--

DROP TABLE IF EXISTS `potech`;
CREATE TABLE IF NOT EXISTS `potech` (
  `IDTechnology` int(11) NOT NULL auto_increment,
  `Name` varchar(300) NOT NULL,
  PRIMARY KEY  (`IDTechnology`)
) ENGINE=MyISAM AUTO_INCREMENT=6 ;

--
-- Daten für Tabelle `potech`
--

INSERT INTO `potech` (`IDTechnology`, `Name`) VALUES
(1, 'Technology 1'),
(2, 'Technology 2'),
(3, 'Technology 3');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `potypicalprocess`
--

DROP TABLE IF EXISTS `potypicalprocess`;
CREATE TABLE IF NOT EXISTS `potypicalprocess` (
  `IDTypicalProcess` int(11) NOT NULL auto_increment,
  `UnitOperationID` int(11) NOT NULL,
  `Name` varchar(300) NOT NULL,
  PRIMARY KEY  (`IDTypicalProcess`)
) ENGINE=MyISAM AUTO_INCREMENT=6 ;

--
-- Daten für Tabelle `potypicalprocess`
--

INSERT INTO `potypicalprocess` (`IDTypicalProcess`, `UnitOperationID`, `Name`) VALUES
(1, 1, 'TP1'),
(5, 1, 'TP2');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pounitoperation`
--

DROP TABLE IF EXISTS `pounitoperation`;
CREATE TABLE IF NOT EXISTS `pounitoperation` (
  `IDUnitOperation` int(11) NOT NULL auto_increment,
  `Name` varchar(300) NOT NULL,
  PRIMARY KEY  (`IDUnitOperation`)
) ENGINE=MyISAM AUTO_INCREMENT=4 ;

--
-- Daten für Tabelle `pounitoperation`
--

INSERT INTO `pounitoperation` (`IDUnitOperation`, `Name`) VALUES
(1, 'UnitOperation2'),
(2, 'UnitOperation1'),
(3, 'UnitOperation3');

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

-- Delete Table:
DROP TABLE IF EXISTS `posubsector_to_uo`;


--
-- Datenbank: `einstein`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `poefficiencymeasure`
--

DROP TABLE IF EXISTS `poefficiencymeasure`;
CREATE TABLE IF NOT EXISTS `poefficiencymeasure` (
  `IDEfficiencyMeasure` int(11) NOT NULL auto_increment,
  `ShortDescription` varchar(300) NOT NULL,
  `Text` text NOT NULL,
  PRIMARY KEY  (`IDEfficiencyMeasure`)
) ENGINE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `poemlist`
--

DROP TABLE IF EXISTS `poemlist`;
CREATE TABLE IF NOT EXISTS `poemlist` (
  `IDEMList` int(11) NOT NULL auto_increment,
  `SubsectorID` int(11) NOT NULL,
  `UnitOperationID` int(11) NOT NULL,
  `TechnologyID` int(11) NOT NULL,
  `TypicalProcessID` int(11) NOT NULL,
  PRIMARY KEY  (`IDEMList`)
) ENGINE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `poemlistentry`
--

DROP TABLE IF EXISTS `poemlistentry`;
CREATE TABLE IF NOT EXISTS `poemlistentry` (
  `EMListID` int(11) NOT NULL,
  `EfficiencyMeasureID` int(11) NOT NULL
) ENGINE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `posector`
--

DROP TABLE IF EXISTS `posector`;
CREATE TABLE IF NOT EXISTS `posector` (
  `IDsector` int(11) NOT NULL auto_increment,
  `Name` varchar(300) NOT NULL,
  `NACE` varchar(20) NOT NULL,
  PRIMARY KEY  (`IDsector`)
) ENGINE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `posubsector`
--

DROP TABLE IF EXISTS `posubsector`;
CREATE TABLE IF NOT EXISTS `posubsector` (
  `IDSubsector` int(11) NOT NULL auto_increment,
  `SectorID` int(11) NOT NULL,
  `Name` varchar(300) NOT NULL,
  `NACE` varchar(20) NOT NULL,
  PRIMARY KEY  (`IDSubsector`)
) ENGINE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `potech`
--

DROP TABLE IF EXISTS `potech`;
CREATE TABLE IF NOT EXISTS `potech` (
  `IDTechnology` int(11) NOT NULL auto_increment,
  `Name` varchar(300) NOT NULL,
  `Code` varchar(20) NOT NULL,
  PRIMARY KEY  (`IDTechnology`)
) ENGINE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `potypicalprocess`
--

DROP TABLE IF EXISTS `potypicalprocess`;
CREATE TABLE IF NOT EXISTS `potypicalprocess` (
  `IDTypicalProcess` int(11) NOT NULL auto_increment,
  `Name` varchar(300) NOT NULL,
  `Code` varchar(20) NOT NULL,
  PRIMARY KEY  (`IDTypicalProcess`)
) ENGINE=MyISAM;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pounitoperation`
--

DROP TABLE IF EXISTS `pounitoperation`;
CREATE TABLE IF NOT EXISTS `pounitoperation` (
  `IDUnitOperation` int(11) NOT NULL auto_increment,
  `Name` varchar(300) NOT NULL,
  `Code` varchar(20) NOT NULL,
  PRIMARY KEY  (`IDUnitOperation`)
) ENGINE=MyISAM;


-- Delete Table:
DROP TABLE IF EXISTS `posubsector_to_uo`;


--
-- Datenbank: `einstein`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `poefficiencymeasure`
--

DROP TABLE IF EXISTS `poefficiencymeasure`;
CREATE TABLE IF NOT EXISTS `poefficiencymeasure` (
  `IDEfficiencyMeasure` int(11) NOT NULL auto_increment,
  `ShortDescription` varchar(300) NOT NULL,
  `Text` text NOT NULL,
  PRIMARY KEY  (`IDEfficiencyMeasure`)
) ENGINE=MyISAM  AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `poemlist`
--

DROP TABLE IF EXISTS `poemlist`;
CREATE TABLE IF NOT EXISTS `poemlist` (
  `IDEMList` int(11) NOT NULL auto_increment,
  `SubsectorID` int(11) NOT NULL,
  `UnitOperationID` int(11) NOT NULL,
  `TechnologyID` int(11) NOT NULL,
  `TypicalProcessID` int(11) NOT NULL,
  PRIMARY KEY  (`IDEMList`)
) ENGINE=MyISAM  AUTO_INCREMENT=22 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `poemlistentry`
--

DROP TABLE IF EXISTS `poemlistentry`;
CREATE TABLE IF NOT EXISTS `poemlistentry` (
  `EMListID` int(11) NOT NULL,
  `EfficiencyMeasureID` int(11) NOT NULL
) ENGINE=MyISAM ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `posector`
--

DROP TABLE IF EXISTS `posector`;
CREATE TABLE IF NOT EXISTS `posector` (
  `IDsector` int(11) NOT NULL auto_increment,
  `Name` varchar(300) NOT NULL,
  `NACE` varchar(20) NOT NULL,
  PRIMARY KEY  (`IDsector`)
) ENGINE=MyISAM AUTO_INCREMENT=15 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `posubsector`
--

DROP TABLE IF EXISTS `posubsector`;
CREATE TABLE IF NOT EXISTS `posubsector` (
  `IDSubsector` int(11) NOT NULL auto_increment,
  `SectorID` int(11) NOT NULL,
  `Name` varchar(300) NOT NULL,
  `NACE` varchar(20) NOT NULL,
  PRIMARY KEY  (`IDSubsector`)
) ENGINE=MyISAM AUTO_INCREMENT=19 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `potech`
--

DROP TABLE IF EXISTS `potech`;
CREATE TABLE IF NOT EXISTS `potech` (
  `IDTechnology` int(11) NOT NULL auto_increment,
  `Name` varchar(300) NOT NULL,
  `Code` varchar(20) NOT NULL,
  PRIMARY KEY  (`IDTechnology`)
) ENGINE=MyISAM  AUTO_INCREMENT=6 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `potypicalprocess`
--

DROP TABLE IF EXISTS `potypicalprocess`;
CREATE TABLE IF NOT EXISTS `potypicalprocess` (
  `IDTypicalProcess` int(11) NOT NULL auto_increment,
  `Name` varchar(300) NOT NULL,
  `Code` varchar(20) NOT NULL,
  PRIMARY KEY  (`IDTypicalProcess`)
) ENGINE=MyISAM AUTO_INCREMENT=9 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pounitoperation`
--

DROP TABLE IF EXISTS `pounitoperation`;
CREATE TABLE IF NOT EXISTS `pounitoperation` (
  `IDUnitOperation` int(11) NOT NULL auto_increment,
  `Name` varchar(300) NOT NULL,
  `Code` varchar(20) NOT NULL,
  PRIMARY KEY  (`IDUnitOperation`)
) ENGINE=MyISAM AUTO_INCREMENT=4 ;


