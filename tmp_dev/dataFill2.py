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


print 'Step 0 ..................'

Qid =1
##"""Inserting data in the CFuel table"""
CFuel_id1 = einsteinDB.cfuel.insert({"Questionnaire_id":Qid,"QFuel_id":1,"FECi":6600.0,"FETi":6600.0,"ProdCO2Fuel":1650.0,"DBFuel_id":2})
CFuel_id2 = einsteinDB.cfuel.insert({"Questionnaire_id":Qid,"QFuel_id":2,"FECi":6958.0,"FETi":6958.0,"ProdCO2Fuel":1739.5,"DBFuel_id":1})
db.commit()

print 'Step 0.1 ..................'

Qid =1
##"""Inserting data in the CProcessData table"""
CProcData_id1 = einsteinDB.cprocessdata.insert({"Questionnaire_id":Qid,"QProcessData_id":1,"UPH":2222.46})
CProcData_id2 = einsteinDB.cprocessdata.insert({"Questionnaire_id":Qid,"QProcessData_id":2,"UPH":950.0})
CProcData_id3 = einsteinDB.cprocessdata.insert({"Questionnaire_id":Qid,"QProcessData_id":3,"UPH":2495.19})
CProcData_id4 = einsteinDB.cprocessdata.insert({"Questionnaire_id":Qid,"QProcessData_id":4,"UPH":2647.56})
CProcData_id5 = einsteinDB.cprocessdata.insert({"Questionnaire_id":Qid,"QProcessData_id":5,"UPH":300.0})
CProcData_id6 = einsteinDB.cprocessdata.insert({"Questionnaire_id":Qid,"QProcessData_id":6,"UPH":750.0})
db.commit()

##"""Inserting data in the CGenerationHC table"""
CEquip_id1 = einsteinDB.cgenerationhc.insert({"Questionnaire_id":Qid,"QGenerationHC_id":1,"Nequip":1,"USHj":375.0,"FETj":513.7})
CEquip_id2 = einsteinDB.cgenerationhc.insert({"Questionnaire_id":Qid,"QGenerationHC_id":2,"Nequip":1,"USHj":3965.57,"FETj":5287.43})
CEquip_id3 = einsteinDB.cgenerationhc.insert({"Questionnaire_id":Qid,"QGenerationHC_id":3,"Nequip":1,"USHj":2800.0,"FETj":3500.0})
CEquip_id4 = einsteinDB.cgenerationhc.insert({"Questionnaire_id":Qid,"QGenerationHC_id":4,"Nequip":1,"USHj":2626.52,"FETj":3164.48})
CEquip_id5 = einsteinDB.cgenerationhc.insert({"Questionnaire_id":Qid,"QGenerationHC_id":5,"Nequip":1,"USHj":800.0,"FETj":266.67})
db.commit()

print 'Step 1 .........................'
