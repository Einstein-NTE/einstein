#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	INTERFACES
#			
#------------------------------------------------------------------------------
#			
#	Definition of interfaces in between modules
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Stoyan Danov	---
#	Last revised by:    Hans Schweiger      18/03/2008
#
#       Changes in last update:
#       - adaptation to new structure of GUI / Tool
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

from einstein.modules.interfaces import *
from einstein.GUI.status import *

class ModuleEnergyStatistics():
    
    def __init__(self):
#..............................................................................
# getting list of equipment in SQL
        self.interface = Interfaces(80,8760)

        PId = 2
        ANo = 0

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(PId,ANo)
        self.equipements = Status.DB.qgenerationhc.sql_select(sqlQuery)
        NEquipe = len(self.equipements)
        print "%s equipes found" % NEquipe

        self.fuels = Status.DB.qfuel.sql_select(sqlQuery)
        NFuels = len(self.equipements)
        print "%s fuels found" % NFuels
        
        self.initModule()

#------------------------------------------------------------------------------
    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        carries out any calculations necessary previous to displaying the BB
        design assitant window
        """
#------------------------------------------------------------------------------
        self.update()
        return "ok"

    def update(self):

        try:
#..............................................................................
# Final energy consumption by fuels (data for panel EA1)

            TotalFEC = 0.0
            TotalFETi = 0.0
            FEC = []
            FETi = []
            FuelType = []
            
            for row in self.fuels:  #sum all FECi/FETi for fuels used
                FuelType.append("buscar en DB !!!")
                TotalFEC += row.FECi
                FEC.append row.FECi
                TotalFETi += row.FETi
                FET.append row.FETi
                print 'FECi = ', row.FECi, 'DBFuel_id: ', row.DBFuel_id, DB.dbfuel.DBFuel_ID[row.DBFuel_id][0].FuelName

            TotalFEC += DB.cgeneraldata.Questionnaire_id[PId][0].FECel  #add FECel to TotalFEC
            TotalFETi += DB.cgeneraldata.Questionnaire_id[PId][0].FETel
            FuelType.append("Electricity")
            FEC.append(DB.cgeneraldata.Questionnaire_id[PId][0].FECel)
            FET.append(DB.cgeneraldata.Questionnaire_id[PId][0].FETel)

            print 'FECel = ', DB.cgeneraldata.Questionnaire_id[PId][0].FECel
            print 'Total FEC = ', TotalFEC
            print 'Electricity: ', 'FETel = ', FETel
            print 'TotalFET (calculated from CFuel and CGeneralData) = ', TotalFETi


            #save TotalFEC in CGeneralData table in DB variable FEC (FEC total)
            DB.cgeneraldata.Questionnaire_id[PId][0].FEC = TotalFEC
            DB.cgeneraldata.Questionnaire_id[PId][0].FETi = TotalFETi
            sql.commit()

# generating data tables for plots
# TOM -> por favor revisa esto ...
            FECPercentage = []
            FETPercentage = []

            for i in range (NFuels+ 1):
                FECPercentage.append(FEC[i]/TotalFEC)
                FETPercentage.append(FET[i]/TotalFET)
                
            self.interface.setGraphicsData('EA1-FEC',(FuelType, FEC, FECPercentage, TotalFEC)
            self.interface.setGraphicsData('EA1-FET',(FuelType, FET, FETPercentage, TotalFET)
               
#..............................................................................
# Primary energy consumption by fuels (data for panel EA2)

#xxx missing xxx

#..............................................................................
# Final energy consumption by equipments (data for panel EA3 - part 1)

            TotalFETj = 0.0
            for row in DB.cgenerationhc.Questionnaire_id[PId]:  #sum all FETj for equipment used
                TotalFETj += row.FETj
                #get the name of the equipment from QGenerationHC table using the QGenerationHC_id
                EquipName = DB.qgenerationhc.QGenerationHC_ID[row.QGenerationHC_id][0].Equipment
                print 'Equipment name: ', EquipName, ';' , 'FETj = ', row.FETj

            print 'TotalFET (calculated from CGenerationHC) = ', TotalFETj


#..............................................................................
# Final energy consumption by equipments (data for panel EA3 - part 1)

#xxx missing xxx

#..............................................................................
# Useful process heat demand by processes

#xxx missing xxx


#..............................................................................
# Energy intensity - Fuel, Electricity, PE (data for panel EA5 - part 1)

            CGD = DB.cgeneraldata.Questionnaire_id[PId][0]

            TotalFEC = CGD.FEC   #FEC in [MWh]
            ElectFEC = CGD.FECel
            FuelsFEC = TotalFEC - ElectFEC
            PE_FEC = 1.1*FuelsFEC + 3.0*ElectFEC #substitute later the conv. coef. from SetUp
            
            Turnover = DB.questionnaire.Questionnaire_ID[Qid][0].Turnover #in [million euros]

            if (Turnover > 0) and not (Turnover==None):    
                CGD.FUEL_INT = (FuelsFEC)/(Turnover*1000) #converted to [kWh/euro]
                CGD.EL_INT = (ElectFEC)/(Turnover*1000) #converted to [kWh/euro]
                CGD.PE_INT = (PE_FEC)/(Turnover*1000) #converted to [kWh/euro]
            else:
                CGD.FUEL_INT = None
                CGD.EL_INT = None
                CGD.PE_INT = None

# back-up in SQL                                      
            sql.commit()
                
#..............................................................................
# SEC by product (data for panel EA5 - part 2)

            for row in DB.qproduct.Questionnaire_id[PId]:

                #calculate SEC for each product
                FUEL_SEC = (row.FuelProd)*1000/row.QProdYear #converted to [kWh/pu]
                EL_SEC = (row.ElProd)*1000/row.QProdYear #converted to [kWh/pu]
                PE_SEC = (1.1*row.FuelProd + 3.0*row.ElProd)*1000/row.QProdYear #converted to [kWh/pu], fixed energy conv. coef. ->change this later

                #this selects the corresponding row in CProduct in a shorter variable name
                rowCProd = DB.cproduct.QProduct_id[row.QProduct_ID][0]
                #now write the SEC values in the CProduct table
                rowCProd.FUEL_SEC = FUEL_SEC
                rowCProd.EL_SEC = EL_SEC
                rowCProd.PE_SEC = PE_SEC
                sql.commit()
                print 'Product name: ', row.Product, ';','Annual quantity[pu]', row.QProdYear, ';', 'Consumed energy[MWh]: fuel, el, pe: ',row.FuelProd,row.ElProd,(1.1*row.FuelProd + 3.0*row.ElProd)
                print 'SEC(per product)[kWh/pu]: fuel, el, pe ', rowCProd.FUEL_SEC, rowCProd.EL_SEC, rowCProd.PE_SEC


#..............................................................................
# SEC by unit operation (data for panel EA5 - part 3)

#xxx missing xxx

        except Exception, energyStatistics: #in case of an error 
            return energyStatistics


        else:		#everything is fine
            return 1


#------------------------------------------------------------------------------		
#==============================================================================
