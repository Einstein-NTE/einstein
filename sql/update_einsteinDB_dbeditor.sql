-- update einstein database
USE einstein;

-- update dbheatpump
ALTER TABLE dbheatpump ADD COLUMN Reference VARCHAR(200) DEFAULT NULL AFTER HPSubType;
ALTER TABLE dbheatpump DROP HPFuelConsum;
ALTER TABLE dbheatpump DROP DBFuel_id;
ALTER TABLE dbheatpump ADD COLUMN FuelType VARCHAR(45) DEFAULT NULL AFTER HPCoolCOP;
ALTER TABLE dbheatpump CHANGE HPAbsEffects HPSourceSink VARCHAR(45) DEFAULT NULL;
ALTER TABLE dbheatpump DROP HPYearManufact;
ALTER TABLE dbheatpump DROP HPUnitsFuelConsum;
ALTER TABLE dbheatpump DROP HPManData;
