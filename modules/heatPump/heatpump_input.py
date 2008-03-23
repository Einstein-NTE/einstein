#V0.02 HS. changed import paths; AlternativeProposalNo instead of Id

#######################################################################################################
#INPUT FOR THE HEAT PUMP MODULE
#######################################################################################################

import einstein.GUI.pSQL as pSQL, MySQLdb
sql = MySQLdb.connect(user="root", passwd="tom.tom", db="einstein")
DB = pSQL.pSQL(sql, "einstein")

#In the future this data will be given from the GUI and the database 

##def inputData():
##    """Input data for the Heat Pump Module:
##    Represents the user defined data and the database data"""
##    global DB_Qh, DB_COPh, DB_COPex, Tmax, Tmin, DTlim, HPumpType, Hop, DTmax, Tge
##
##    #Data from HeatPumpDB - still missing, example values here
##    #Range of heat capacities [kW] from DB:
##    #10, 15, 20, 30, 50, 80, 100, 150, 200, 300, 500, 800, 1000, 1500, 2000, 3000, 5000, 8000, 10000, 15000, 20000,...
##    DB_Qh = [10., 15., 20., 30., 50., 80., 100., 150., 200., 300., 500., 800., 1000., 1500., 2000., 3000., 5000., 8000., 10000., 15000., 20000.]
##    #COPh from DB
##    #4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, ...
##    DB_COPh = [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0]
##    DB_COPex = [0.30,0.32,0.34,0.36,0.38,0.40,0.42,0.44,0.46,0.48,0.50,0.52,0.54,0.56,0.58,0.60,0.61,0.62,0.63,0.64,0.65]
##
##    #DB_ID = [3,4,5,8,9,...,..] #list of the HeatPump_IDs corresponding to the capacities in the DB_Qh
##    #(needed to identify the selection in the database)
##
##    #Maximum and minimum temperature (limit) for heat pump, from DB
##    Tmax = 100.0
##    Tmin = 5.0
##    DTlim = 50.0
##
##    #User defined values
##    HPumpType = 'COMP' #Type of Heat Pump: COMP or ABS (vapor-compression or thermal)
##    Hop = 2.0 #minimum desired annual operation hours, user defined. Note: Should be less than year hours!
##    DTmax = 40.0 #maximum temperature diffrence between heat source and sink (inlets temp.), user defined
##    Tge =90.0 #generator inlet temperature (steam, hot water)(thermal HP only), user defined
##
        
def inputData(sql,DB,Qid,Aid,PSid,HPTypeUD):

    global qhListDB, cophListDB, copexListDB, idListDB, dtlimListDB, maxTcondListDB, minTevapListDB, minTgeListDB
    
    sqlQuery = "HPType LIKE '%s' ORDER BY HPHeatCap ASC"%(HPTypeUD)
    databaseList = DB.dbheatpump.sql_select(sqlQuery) #this is a list of rows (dictionaries) in DBHeatPump

    qhListDB = [] #list of heating capacities of HP in DBHeatPump (in ascending order)
    cophListDB = [] #list of nominal heating COPs
    copexListDB = [] #list of exergetic heating COPs
    idListDB = [] #list of heat pump IDs in the DBHeatPump
    dtlimListDB = [] #list of working limit temperature lift for HP
    maxTcondListDB = [] #list of maximum condensing T for HP (working limit)
    minTevapListDB = [] #list of minimum evaporating T for HP (working limit)
    minTgeListDB = [] #list of minimum Tge for HP (working limit)

    #filling the lists
    for i in range(len(databaseList)):
        qhListDB.append(databaseList[i].HPHeatCap) 
        cophListDB.append(databaseList[i].HPHeatCOP)
        copexListDB.append(databaseList[i].HPExHeatCOP)
        idListDB.append(databaseList[i].DBHeatPump_ID)
        dtlimListDB.append(databaseList[i].HPLimDT)
        maxTcondListDB.append(databaseList[i].HPCondTmax)
        minTevapListDB.append(databaseList[i].HPEvapTmin)
        minTgeListDB.append(databaseList[i].HPGenTmin)
        


def chargeCurvesQDQA(sql,DB,Qid,Aid):
    global QDa, QAa, QDh, QAh, T

    #define the temperature range for the hot (QD) and cold (QA) cureves 
    T = range(0.0,405.0,5.0)

    sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY IndexNo ASC"%(Qid,Aid)

    tableQDa = DB.energyflowsqda.sql_select(sqlQuery)
    QDa = tableQDa[0].values()
    QDa.pop() #Delete the last element of the list (empty)
    QDa.pop(0) #Delete the first 4 elements in the QD, QA lists
    QDa.pop(0)
    QDa.pop(0)
    QDa.pop(0)
    

    tableQAa = DB.energyflowsqaa.sql_select(sqlQuery)
    QAa = tableQAa[0].values()
    QAa.pop() #Delete the last element of the list (empty)
    QAa.pop(0) #Delete the first 4 elements in the QD, QA lists
    QAa.pop(0)
    QAa.pop(0)
    QAa.pop(0)
    
        
    tableQDh = DB.energyflowsqdh.sql_select(sqlQuery)
    QDh = []
    for i in range(len(tableQDh)):
        QDh.append(tableQDh[i].values())
        QDh[i].pop() #Delete the last element of the list (empty)
        QDh[i].pop(0) #Delete the first 4 elements in the QD, QA lists
        QDh[i].pop(0)
        QDh[i].pop(0)
        QDh[i].pop(0)

    tableQAh = DB.energyflowsqah.sql_select(sqlQuery)
    QAh = []
    for i in range(len(tableQAh)):
        QAh.append(tableQAh[i].values())
        QAh[i].pop() #Delete the last element of the list (empty)
        QAh[i].pop(0) #Delete the first 4 elements in the QD, QA lists
        QAh[i].pop(0)
        QAh[i].pop(0)
        QAh[i].pop(0)

########################################################################################

Qid = 1
Aid = 1
PSid = 1
HPTypeUD = 'COMP'
    
inputData(sql,DB,Qid,Aid,PSid,HPTypeUD)

chargeCurvesQDQA(sql,DB,Qid,Aid)
