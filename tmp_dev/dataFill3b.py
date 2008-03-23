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
db = MySQLdb.connect(user="root", passwd='tom.tom', db="einstein")
einsteinDB = pSQL.pSQL(db, "einstein")



print 'Step 1 .........................'

##"""Inserting data in the EnergyFlowsQDa table"""

#define the temperature range for the hot (QD) and cold (QA) curves 

(T, QDh, QAh, QDa, QAa) = createDemandAndAvailabCurves()

##print 'QDa', QDa
##print 'QAa', QAa
##
##print 'QDh[0]', QDh[0]
##print 'QDh[1]', QDh[1]
##print 'QDh[2]', QDh[2]
##
##print 'QAh[0]', QAh[0]
##print 'QAh[1]', QAh[1]
##print 'QAh[2]', QAh[2]

##print 'T', T


print 'Step 2 .........................'

Qid = 1
Aid = 1

QDa_id = []
for i in range(1):
    QDa_id.append(0)
QAa_id = []
for i in range(1):
    QAa_id.append(0)

KeyD = ['Questionnaire_id','AlternativeProposalNo','IndexNo']
KeyD.append('T0'); KeyD.append('T5'); KeyD.append('T10'); KeyD.append('T15'); KeyD.append('T20'); KeyD.append('T25');
KeyD.append('T30'); KeyD.append('T35'); KeyD.append('T40'); KeyD.append('T45'); KeyD.append('T50'); KeyD.append('T55');
KeyD.append('T60'); KeyD.append('T65'); KeyD.append('T70'); KeyD.append('T75'); KeyD.append('T80'); KeyD.append('T85');
KeyD.append('T90'); KeyD.append('T95'); KeyD.append('T100'); KeyD.append('T105'); KeyD.append('T110'); KeyD.append('T115');
KeyD.append('T120'); KeyD.append('T125'); KeyD.append('T130'); KeyD.append('T135'); KeyD.append('T140'); KeyD.append('T145');
KeyD.append('T150'); KeyD.append('T155'); KeyD.append('T160'); KeyD.append('T165'); KeyD.append('T170'); KeyD.append('T175');
KeyD.append('T180'); KeyD.append('T185'); KeyD.append('T190'); KeyD.append('T195'); KeyD.append('T200'); KeyD.append('T205');
KeyD.append('T210'); KeyD.append('T215'); KeyD.append('T220'); KeyD.append('T225'); KeyD.append('T230'); KeyD.append('T235');
KeyD.append('T240'); KeyD.append('T245'); KeyD.append('T250'); KeyD.append('T255'); KeyD.append('T260'); KeyD.append('T265');
KeyD.append('T270'); KeyD.append('T275'); KeyD.append('T280'); KeyD.append('T285'); KeyD.append('T290'); KeyD.append('T295');
KeyD.append('T300');KeyD.append('T305');
KeyD.append('T310'); KeyD.append('T315'); KeyD.append('T320'); KeyD.append('T325'); KeyD.append('T330'); KeyD.append('T335');
KeyD.append('T340'); KeyD.append('T345'); KeyD.append('T350'); KeyD.append('T355'); KeyD.append('T360'); KeyD.append('T365');
KeyD.append('T370'); KeyD.append('T375'); KeyD.append('T380'); KeyD.append('T385'); KeyD.append('T390'); KeyD.append('T395');
KeyD.append('T400');

TKeyD = tuple(KeyD)

KeyA = ['Questionnaire_id','AlternativeProposalNo','IndexNo']
KeyA.append('T0'); KeyA.append('T5'); KeyA.append('T10'); KeyA.append('T15'); KeyA.append('T20'); KeyA.append('T25');
KeyA.append('T30'); KeyA.append('T35'); KeyA.append('T40'); KeyA.append('T45'); KeyA.append('T50'); KeyA.append('T55');
KeyA.append('T60'); KeyA.append('T65'); KeyA.append('T70'); KeyA.append('T75'); KeyA.append('T80'); KeyA.append('T85');
KeyA.append('T90'); KeyA.append('T95'); KeyA.append('T100'); KeyA.append('T105'); KeyA.append('T110'); KeyA.append('T115');
KeyA.append('T120'); KeyA.append('T125'); KeyA.append('T130'); KeyA.append('T135'); KeyA.append('T140'); KeyA.append('T145');
KeyA.append('T150'); KeyA.append('T155'); KeyA.append('T160'); KeyA.append('T165'); KeyA.append('T170'); KeyA.append('T175');
KeyA.append('T180'); KeyA.append('T185'); KeyA.append('T190'); KeyA.append('T195'); KeyA.append('T200'); KeyA.append('T205');
KeyA.append('T210'); KeyA.append('T215'); KeyA.append('T220'); KeyA.append('T225'); KeyA.append('T230'); KeyA.append('T235');
KeyA.append('T240'); KeyA.append('T245'); KeyA.append('T250'); KeyA.append('T255'); KeyA.append('T260'); KeyA.append('T265');
KeyA.append('T270'); KeyA.append('T275'); KeyA.append('T280'); KeyA.append('T285'); KeyA.append('T290'); KeyA.append('T295');
KeyA.append('T300'); KeyA.append('T305');
KeyA.append('T310'); KeyA.append('T315'); KeyA.append('T320'); KeyA.append('T325'); KeyA.append('T330'); KeyA.append('T335');
KeyA.append('T340'); KeyA.append('T345'); KeyA.append('T350'); KeyA.append('T355'); KeyA.append('T360'); KeyA.append('T365');
KeyA.append('T370'); KeyA.append('T375'); KeyA.append('T380'); KeyA.append('T385'); KeyA.append('T390'); KeyA.append('T395');
KeyA.append('T400');

TKeyA = tuple(KeyA)

modQDa = tuple([Qid, Aid, 1] + QDa)
modQAa = tuple([Qid, Aid, 1] + QAa)


DictQDa = dict(zip(TKeyD,modQDa))
DictQAa = dict(zip(TKeyA,modQAa))

print ''

##print 'DictQDa', DictQDa
##print 'DictQAa', DictQAa

##result = einsteinDB.energyflowsqda.sql_select("EnergyFlowsQDa_ID LIKE 1")
##
##print 'result',result

QDa_id[0] = einsteinDB.energyflowsqda.insert(DictQDa)
QAa_id[0] = einsteinDB.energyflowsqaa.insert(DictQAa)


########################################################################

KeyDh = KeyD

KeyAh = KeyA

TKeyDh =tuple(KeyDh)
TKeyAh =tuple(KeyAh)

##print 'KeyDh', KeyDh
##print 'KeyAh', KeyAh

modQDh1 = tuple([Qid, Aid, 1] + QDh[0])
modQDh2 = tuple([Qid, Aid, 2] + QDh[1])
modQDh3 = tuple([Qid, Aid, 3] + QDh[2])

modQAh1 = tuple([Qid, Aid, 1] + QAh[0])
modQAh2 = tuple([Qid, Aid, 2] + QAh[1])
modQAh3 = tuple([Qid, Aid, 3] + QAh[2])

DictQDh1 = dict(zip(TKeyDh,modQDh1))
DictQDh2 = dict(zip(TKeyDh,modQDh2))
DictQDh3 = dict(zip(TKeyDh,modQDh3))

DictQAh1 = dict(zip(TKeyAh,modQAh1))
DictQAh2 = dict(zip(TKeyAh,modQAh2))
DictQAh3 = dict(zip(TKeyAh,modQAh3))

print 'DictQDh1', DictQDh1
print 'DictQDh2', DictQDh2
print 'DictQDh3', DictQDh3
print 'DictQAh1', DictQAh1
print 'DictQAh2', DictQAh2
print 'DictQAh3', DictQAh3

QDh_id = []
for i in range(8760):
    QDh_id.append(0)
QAh_id = []
for i in range(8760):
    QAh_id.append(0)

QDh_id[0] = einsteinDB.energyflowsqdh.insert(DictQDh1)
QDh_id[1] = einsteinDB.energyflowsqdh.insert(DictQDh2)
QDh_id[2] = einsteinDB.energyflowsqdh.insert(DictQDh3)

QAh_id[0] = einsteinDB.energyflowsqah.insert(DictQAh1)
QAh_id[1] = einsteinDB.energyflowsqah.insert(DictQAh2)
QAh_id[2] = einsteinDB.energyflowsqah.insert(DictQAh3)

################################################################


db.commit()
                                              
print 'ha ha ha!'


#Fill in database the user-defined parameters: table UHeatPump

UHP_id = einsteinDB.uheatpump.insert({'UHeatPump_ID':1,'Questionnaire_id':Qid,'AlternativeProposalNo':1,'UHPType':'COMP','UHPMinHop':1.8,'UHPDTMax':40.0,'UHPTgenIn':90.0,'UHPmaxT':100.0,'UHPminT':5.0})
db.commit()

PSid = einsteinDB.psetupdata.insert({'UHPType':'COMP','UHPMinHop':1.8,'UHPDTMax':40.0,'UHPTgenIn':90.0,'UHPmaxT':65.0,'UHPminT':5.0})
db.commit()

#Fill Heat Pump Database

#entry 1
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':8.6,'HPCoolCOP':2.24,'HPExCoolCOP':0.258,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':10.0,'HPHeatCOP':2.8,'HPExHeatCOP':0.411,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':1670.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 2
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':12.9,'HPCoolCOP':2.28,'HPExCoolCOP':0.262,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':15.0,'HPHeatCOP':2.85,'HPExHeatCOP':0.419,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':2390.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 3
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':17.2,'HPCoolCOP':2.32,'HPExCoolCOP':0.267,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':20.0,'HPHeatCOP':2.9,'HPExHeatCOP':0.426,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':3100.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 4
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':25.8,'HPCoolCOP':2.36,'HPExCoolCOP':0.272,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':30.0,'HPHeatCOP':2.95,'HPExHeatCOP':0.433,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':4415.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 5
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':43.0,'HPCoolCOP':2.4,'HPExCoolCOP':0.276,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':50.0,'HPHeatCOP':3.0,'HPExHeatCOP':0.441,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':6940.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 6
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':86.,'HPCoolCOP':2.42,'HPExCoolCOP':0.279,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':100.0,'HPHeatCOP':3.03,'HPExHeatCOP':0.445,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':12824.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 7
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':129.0,'HPCoolCOP':2.45,'HPExCoolCOP':0.282,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':150.0,'HPHeatCOP':3.06,'HPExHeatCOP':0.449,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':18366.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 8
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':172.0,'HPCoolCOP':2.48,'HPExCoolCOP':0.285,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':200.0,'HPHeatCOP':3.10,'HPExHeatCOP':0.455,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':23700.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 9
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':258.0,'HPCoolCOP':2.5,'HPExCoolCOP':0.288,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':300.0,'HPHeatCOP':3.13,'HPExHeatCOP':0.46,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':33950.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 10
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':430.0,'HPCoolCOP':2.53,'HPExCoolCOP':0.291,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':500.0,'HPHeatCOP':3.16,'HPExHeatCOP':0.464,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':53370.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 11
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':688.0,'HPCoolCOP':2.55,'HPExCoolCOP':0.294,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':800.0,'HPHeatCOP':3.19,'HPExHeatCOP':0.469,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':80940.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 12
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':860,'HPCoolCOP':2.58,'HPExCoolCOP':0.297,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':1000.0,'HPHeatCOP':3.22,'HPExHeatCOP':0.473,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':98630.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 13
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':1290.0,'HPCoolCOP':2.60,'HPExCoolCOP':0.299,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':1500.0,'HPHeatCOP':3.25,'HPExHeatCOP':0.477,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':141264.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 14
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':1720.0,'HPCoolCOP':2.62,'HPExCoolCOP':0.302,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':2000.0,'HPHeatCOP':3.28,'HPExHeatCOP':0.482,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':182274.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 15
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':2580.0,'HPCoolCOP':2.64,'HPExCoolCOP':0.304,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':3000.0,'HPHeatCOP':3.30,'HPExHeatCOP':0.485,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':261063.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 16
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':4300.0,'HPCoolCOP':2.66,'HPExCoolCOP':0.307,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':5000.0,'HPHeatCOP':3.33,'HPExHeatCOP':0.489,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':410490.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 17
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':6880.0,'HPCoolCOP':2.69,'HPExCoolCOP':0.309,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':8000.0,'HPHeatCOP':3.36,'HPExHeatCOP':0.494,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':622518.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 18
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':8600.0,'HPCoolCOP':2.72,'HPExCoolCOP':0.313,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':10000.0,'HPHeatCOP':3.40,'HPExHeatCOP':0.499,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':758602.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 19
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':10320.0,'HPCoolCOP':2.76,'HPExCoolCOP':0.318,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':12000.0,'HPHeatCOP':3.45,'HPExHeatCOP':0.507,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':899083.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})

#entry 20
einsteinDB.dbheatpump.insert({'HPManData':'HC','HPManufacturer':'EINSTEIN','HPModel':'EINSTEIN','HPType':'COMP','HPSubType':'water-water',
##'HPAbsEffects': ,
##'HPAbsHeatMed': ,
'HPWorkFluid':'R407C','HPCoolCap':12900.0,'HPCoolCOP':2.80,'HPExCoolCOP':0.322,'HPThCoolCOP':8.69,'HPConstExCoolCOP':20.0,
##'HPAbsTinC': ,
'HPCondTinC':30.0,
##'HPGenTinC': ,
'HPEvapTinC':12.0,'HPHeatCap':15000.0,'HPHeatCOP':3.5,'HPExHeatCOP':0.514,'HPThHeatCOP':6.81,'HPConstExHeatCOP':20.0,
##'HPAbsTinH': ,
'HPCondTinH':40.0,
##'HPGenTinH': ,
'HPEvapTinH':7.0,'HPLimDT':65.0,
##'HPGenTmin': ,
'HPCondTmax':52.0,'HPEvapTmin':-18.0,
##'HPElectConsum': ,
'HPPrice':1086504.0,
##'HPTurnKeyPrice': ,
##'HPOandMfix': ,
##'HPOandMvar': ,
'HPYearUpdate':2008})


db.commit()

print 'ha ha ha ha ha!'


