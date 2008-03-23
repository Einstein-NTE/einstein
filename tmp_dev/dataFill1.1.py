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

Qid = 1

##"""Inserting data in the CGeneralData table""" #how add data to an entry in a table with repetitive data, Heiko?
CGenData_id = einsteinDB.cgeneraldata.insert({"Questionnaire_id":Qid,"PECFuels":14913.8,"PECElect":3000.0,"PETFuels":14913.8,"PETElect":510.0,"FECel":1000.0,"FETel":170.0})
activeCGD = einsteinDB.cgeneraldata.Questionnaire_id[Qid][0]
activeCGD.ProdCO2Elect = 700.0
activeCGD.PE_INT = 2.94
activeCGD.EL_INT = 0.15
activeCGD.FUEL_INT = 2.27
db.commit()

##"""Inserting data in the CProduct table"""
CProd_id1 = einsteinDB.cproduct.insert({"Questionnaire_id":Qid,"QProduct_id":1,"PE_SEC":271.18,"EL_SEC":51.36,"FUEL_SEC":102.73})
CProd_id2 = einsteinDB.cproduct.insert({"Questionnaire_id":Qid,"QProduct_id":2,"PE_SEC":500.97,"EL_SEC":105.68,"FUEL_SEC":161.36})
CProd_id3 = einsteinDB.cproduct.insert({"Questionnaire_id":Qid,"QProduct_id":3,"PE_SEC":292.78,"EL_SEC":55.45,"FUEL_SEC":110.91})
db.commit()

print 'Step 0 ..................'
