#######################################################################################################
#INPUT FOR THE HEAT PUMP MODULE
#######################################################################################################

import einstein.GUI.pSQL as pSQL, MySQLdb
sql = MySQLdb.connect(user="root", passwd="tom.tom", db="einstein")
DB = pSQL.pSQL(sql, "einstein")

################################################################       
def userDefinedLevel1(sql,DB,Qid,Aid):
    """Takes user-defined data for Level1 (interactive) - from UHeatPump table
    Arguments: sql - MySQL database connector; DB - database einstein;
    Qid - Questionnaire_id; Aid - AlternativeProposalNo"""
    global TmaxUD, TminUD, HPTypeUD, Hop, DTmaxUD, TgeUD

    row = DB.uheatpump.Questionnaire_id[Qid].AlternativeProposalNo[Aid][0]

    HPTypeUD = row.UHPType
    Hop = row.UHPMinHop
    DTmaxUD = row.UHPDTMax
    TgeUD = row.UHPTgenIn
    TmaxUD = row.UHPmaxT
    TminUD = row.UHPminT

##    print 'HPTypeUD', HPTypeUD
##    print 'Hop', Hop
##    print 'DTmaxUD', DTmaxUD
##    print 'TgeUD', TgeUD
##    print 'TmaxUD', TmaxUD
##    print 'TminUD', TminUD

###############################################################3

def userDefinedLevel2(sql,DB,Qid,Aid,PSid):
    """Takes user-defined data for Level2 (semi-automatic) - from UHeatPump and PSetUpData tables
    Arguments: sql - MySQL database connector; DB - database einstein;
    Qid - Questionnaire_id; Aid - AlternativeProposalNo; PSid - PSetUpData_ID"""
    global TmaxUD, TminUD, HPTypeUD, Hop, DTmaxUD, TgeUD

    rowUHP = DB.uheatpump.Questionnaire_id[Qid].AlternativeProposalNo[Aid][0]

    rowPS = DB.psetupdata.PSetUpData_ID[PSid][0]
    
    HPTypeUD = rowUHP.UHPType
    Hop = rowPS.UHPMinHop
    DTmaxUD = rowPS.UHPDTMax
    TgeUD = rowPS.UHPTgenIn
    TmaxUD = rowPS.UHPmaxT
    TminUD = rowPS.UHPminT

##    print 'HPTypeUD', HPTypeUD
##    print 'Hop', Hop
##    print 'DTmaxUD', DTmaxUD
##    print 'TgeUD', TgeUD
##    print 'TmaxUD', TmaxUD
##    print 'TminUD', TminUD
    
    
###############################################################

def userDefinedLevel3(sql,DB,PSid):
    """Takes user-defined data for Level3 (automatic) - from PSetUpData table
    Arguments: sql - MySQL database connector; DB - database einstein;
    PSid - PSetUpData_ID"""
    global TmaxUD, TminUD, HPTypeUD, Hop, DTmaxUD, TgeUD

    rowPS = DB.psetupdata.PSetUpData_ID[PSid][0]
    
    HPTypeUD = rowPS.UHPType
    Hop = rowPS.UHPMinHop
    DTmaxUD = rowPS.UHPDTMax
    TgeUD = rowPS.UHPTgenIn
    TmaxUD = rowPS.UHPmaxT
    TminUD = rowPS.UHPminT

##    print 'HPTypeUD', HPTypeUD
##    print 'Hop', Hop
##    print 'DTmaxUD', DTmaxUD
##    print 'TgeUD', TgeUD
##    print 'TmaxUD', TmaxUD
##    print 'TminUD', TminUD
    

###############################################################
##Qid = 1
##Aid = 1
##PSid = 1
##
##print 'userDefinedLevel1'
##userDefinedLevel1(sql,DB,Qid,Aid)
##
####print 'Globals - outside'
####print 'HPTypeUD', HPTypeUD
####print 'Hop', Hop
####print 'DTmaxUD', DTmaxUD
####print 'TgeUD', TgeUD
####print 'TmaxUD', TmaxUD
####print 'TminUD', TminUD
##
##print ''
##print 'userDefinedLevel2'
##userDefinedLevel2(sql,DB,Qid,Aid,PSid)
##
##print ''
##print 'userDefinedLevel3'
##userDefinedLevel3(sql,DB,PSid)
##
