#import the mysqlconnector and the table script
import einstein.GUI.pSQL as pSQL, MySQLdb

from sys import *
from math import *
from einstein.auxiliary.auxiliary import *
from demand_curves import *

#=======================================================================
# EINSTEIN MAIN ROUTINE
#=======================================================================

#connect to the database
db = MySQLdb.connect(user="root", passwd="tom.tom", db="einstein")
einsteinDB = pSQL.pSQL(db, "einstein")

#Set-up menu. Filling of databases.
##"""Inserting data in the DBFuel table"""
DBFuel_id1=einsteinDB.dbfuel.insert({"FuelName":"Natural gas","DBFuelUnit":"m3","FuelCode":"NG","FuelLCV":9.94,"FuelHCV":0.0,"tCO2":0.25,"FuelDensity":0.0,"ConversPrimEnergy":1.1,"FuelDataSource":"Poship tool"})
DBFuel_id2=einsteinDB.dbfuel.insert({"FuelName":"Liquid petroleum gas","DBFuelUnit":"kg","FuelCode":"LPG","FuelLCV":12.56,"FuelHCV":0.0,"tCO2":0.25,"FuelDensity":0.0,"ConversPrimEnergy":1.1,"FuelDataSource":"Poship tool"})
DBFuel_id3=einsteinDB.dbfuel.insert({"FuelName":"Heavy fuel oil","DBFuelUnit":"kg","FuelCode":"HFO","FuelLCV":11.0,"FuelHCV":0.0,"tCO2":0.25,"FuelDensity":0.0,"ConversPrimEnergy":1.1,"FuelDataSource":"Poship tool"})
DBFuel_id4=einsteinDB.dbfuel.insert({"FuelName":"Butane","DBFuelUnit":"kg","FuelCode":"BUT","FuelLCV":12.5,"FuelHCV":0.0,"tCO2":0.25,"FuelDensity":0.0,"ConversPrimEnergy":1.1,"FuelDataSource":"Poship tool"})
DBFuel_id5=einsteinDB.dbfuel.insert({"FuelName":"Propane","DBFuelUnit":"kg","FuelCode":"PRO","FuelLCV":12.5,"FuelHCV":0.0,"tCO2":0.25,"FuelDensity":0.0,"ConversPrimEnergy":1.1,"FuelDataSource":"Poship tool"})
DBFuel_id6=einsteinDB.dbfuel.insert({"FuelName":"Gas oil","DBFuelUnit":"kg","FuelCode":"GO","FuelLCV":11.0,"FuelHCV":0.0,"tCO2":0.25,"FuelDensity":0.0,"ConversPrimEnergy":1.1,"FuelDataSource":"Poship tool"})
DBFuel_id7=einsteinDB.dbfuel.insert({"FuelName":"Electricity","DBFuelUnit":"MWh","FuelCode":"EL","FuelLCV":1000.0,"FuelHCV":1000.0,"tCO2":0.7,"FuelDensity":0.0,"ConversPrimEnergy":1.1,"FuelDataSource":"Poship tool"})
db.commit()

print DBFuel_id1, DBFuel_id2, DBFuel_id3, DBFuel_id4, DBFuel_id5, DBFuel_id6, DBFuel_id7,
print ''
dbfu=einsteinDB.dbfuel.DBFuel_ID[DBFuel_id1][0]
print dbfu.FuelName

#the result is a list of dictionaries(entries in the table)
dbfuNG=einsteinDB.dbfuel.FuelName["Natural gas"]
print 'Natural gas entries =', len(dbfuNG)

#prints the first dictionary (entry) in the list
dbfuNG=einsteinDB.dbfuel.FuelName["Natural gas"][0]
print dbfuNG

NoEntries = len(einsteinDB.dbfuel.sql_select("DBFuel_ID BETWEEN 0 AND 1000000"))
print 'NoEntries = ', NoEntries

##"""Inserting data in the Questionnaire table"""
Qid = einsteinDB.questionnaire.insert({"Name":"enerCHEESExperts","City":"Barcelona","Contact":"Hans Schweiger","Turnover":5.2})
db.commit()

print 'LastQid =', Qid

##"""Inserting data in the QProduct table"""
QProd_id1 = einsteinDB.qproduct.insert({"Questionnaire_id":Qid,"Product":"Milk","QProdYear":10000.0,"ProdUnit":"t","TurnoverProd":1.5,"ElProd":500.0,"FuelProd":1000.0})
QProd_id2 = einsteinDB.qproduct.insert({"Questionnaire_id":Qid,"Product":"Cheese","QProdYear":4000.0,"ProdUnit":"t","TurnoverProd":2.5,"ElProd":400.0,"FuelProd":600.0})
QProd_id3 = einsteinDB.qproduct.insert({"Questionnaire_id":Qid,"Product":"Yoghourt","QProdYear":2000.0,"ProdUnit":"t","TurnoverProd":1.2,"ElProd":100.0,"FuelProd":200.0})
db.commit()

##"""Inserting data in the QFuel table"""
QFuel_id1 = einsteinDB.qfuel.insert({"Questionnaire_id":Qid,"FuelUnit":"kg","DBFuel_id":DBFuel_id3,"MFuelYear":600000.0,"FuelOwn":6700.0,"FuelTariff":25.0,"FuelCostYear":120000.0})
QFuel_id2 = einsteinDB.qfuel.insert({"Questionnaire_id":Qid,"FuelUnit":"m3","DBFuel_id":DBFuel_id1,"MFuelYear":700000.0,"FuelOwn":7000.0,"FuelTariff":18.0,"FuelCostYear":150000.0})
db.commit()

##"""Inserting data in the QElectricity table"""
QElect_id = einsteinDB.qelectricity.insert({"Questionnaire_id":Qid,"ElCostYearTot":60000.0})
db.commit()

##"""Inserting data in the QProcessData table"""
QProc_id1 = einsteinDB.qprocessdata.insert({"Questionnaire_id":Qid,"Process":"Pasteurisation","PT":72.0,"TSupply":180.0})
QProc_id2 = einsteinDB.qprocessdata.insert({"Questionnaire_id":Qid,"Process":"Heating","PT":40.0,"TSupply":180.0})
QProc_id3 = einsteinDB.qprocessdata.insert({"Questionnaire_id":Qid,"Process":"Mozzarella production","PT":90.0,"TSupply":180.0})
QProc_id4 = einsteinDB.qprocessdata.insert({"Questionnaire_id":Qid,"Process":"Drying of milk","PT":180.0,"TSupply":500.0})
QProc_id5 = einsteinDB.qprocessdata.insert({"Questionnaire_id":Qid,"Process":"Hot water for washing","PT":80.0,"TSupply":80.0})
QProc_id6 = einsteinDB.qprocessdata.insert({"Questionnaire_id":Qid,"Process":"Cooling","PT":4.0,"TSupply":0.0})
db.commit()

##"""Inserting data in the QGenerationHC table"""
QEquip_id1 = einsteinDB.qgenerationhc.insert({"Questionnaire_id":Qid,"Equipment":"Boiler 1","DBFuel_id":DBFuel_id1})
QEquip_id2 = einsteinDB.qgenerationhc.insert({"Questionnaire_id":Qid,"Equipment":"Boiler 2","DBFuel_id":DBFuel_id1})
QEquip_id3 = einsteinDB.qgenerationhc.insert({"Questionnaire_id":Qid,"Equipment":"Burner","DBFuel_id":DBFuel_id3})
QEquip_id4 = einsteinDB.qgenerationhc.insert({"Questionnaire_id":Qid,"Equipment":"Boiler 3","DBFuel_id":DBFuel_id3})
QEquip_id5 = einsteinDB.qgenerationhc.insert({"Questionnaire_id":Qid,"Equipment":"Chiller","DBFuel_id":DBFuel_id7})
db.commit()

####"""Inserting data in the CGeneralData table""" #how add data to an entry in a table with repetitive data, Heiko?
##CGenData_id = einsteinDB.cgeneraldata.insert({"Questionnaire_id":Qid,"PECFuels":14913.8,"PECElect":3000.0,"PETFuels":14913.8,"PETElect":510.0,"FECel":1000.0,"FETel":170.0})
##activeCGD = einsteinDB.cgeneraldata.Questionnaire_id[Qid][0]
##activeCGD.ProdCO2Elect = 700.0
##activeCGD.PE_INT = 2.94
##activeCGD.EL_INT = 0.15
##activeCGD.FUEL_INT = 2.27
##db.commit()
##
####"""Inserting data in the CProduct table"""
##CProd_id1 = einsteinDB.cproduct.insert({"Questionnaire_id":Qid,"QProduct_id":QProd_id1,"PE_SEC":271.18,"EL_SEC":51.36,"FUEL_SEC":102.73})
##CProd_id2 = einsteinDB.cproduct.insert({"Questionnaire_id":Qid,"QProduct_id":QProd_id2,"PE_SEC":500.97,"EL_SEC":105.68,"FUEL_SEC":161.36})
##CProd_id3 = einsteinDB.cproduct.insert({"Questionnaire_id":Qid,"QProduct_id":QProd_id3,"PE_SEC":292.78,"EL_SEC":55.45,"FUEL_SEC":110.91})
##db.commit()
##
##print 'Step 0 ..................'
