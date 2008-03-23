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
#	Version No.: 0.06
#	Created by: 	    Hans Schweiger	10/03/2008
#	Last revised by:    Stoyan Danov      17/03/2008
#
#       Changes in last update:
#       - setDefaultDemand - adding QD, QA filling, USHj_Tt filling zero
#       - userDefinedLevel1,2,3 - adding
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

import MySQLdb
from einstein.GUI.status import Status
import einstein.GUI.pSQL as pSQL
import einstein.GUI.HelperClass as HelperClass
from einstein.auxiliary.auxiliary import *

class Interfaces(object):
    #
    # class variables
    #
    QDa = []
    QAa = []
    QDh = []
    QAh = []
    TEMP = []
#..........................................................................
# temporary arrays for calculation of equipment cascade

    QDa_mod = []    
    QAa_mod = []
    QDh_mod = []
    QAh_mod = []

    QD_Tt = []
    QD_Tt_mod = []

    QA_Tt = []
    QA_Tt_mod = []

    USHj_Tt = []    
    USHj_T = []
    USHj_t = []
    USH = None
    
    T = []
#..........................................................................
# temporary User Defined parameters for HP module
    userDefined1 = ()
    userDefined2 = ()
    userDefined3 = ()
    ANo = Status.ANo
    PId = Status.PId
    DB = Status.DB
    LEVEL = Status.LEVEL
    SetUpId = Status.SetUpId


    #
    # instance methods
    #
    def __init__(self, NT, Nt):
        #
        # Instance initialization
        #
        # Calculate and store QD, QA curves in class variables
        #
        row = []
        for it in range(Nt+1):
            row.append(None)
        
        Interfaces.T = []
        for iT in range(NT+1): #SD ->NT + 2 before, 15/03/2008
            Interfaces.T.append(row)
        
        # Connect to database
        #
#        self.connectToDB() #SD - lo he quitado 14/03/2008
        #
        # Calculate and store time and temperature dependent energy flows
        #
        #self.chargeCurvesQDQA()
        
    def connectToDB(self):
        #----- Connect to the Database
        conf = HelperClass.ConfigHelper()
        DBHost = conf.get('DB', 'DBHost')
        DBUser = conf.get('DB', 'DBUser')
        DBPass = conf.get('DB', 'DBPass')
        DBName = conf.get('DB', 'DBName')

        MySql = MySQLdb.connect(host=DBHost, user=DBUser, passwd=DBPass, db=DBName)
        Status.SQL = MySql
        Status.DB =  pSQL.pSQL(MySql, DBName)
        print "data base connected ",Status.SQL,Status.DB

    def chargeCurvesQDQA(self):
        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY IndexNo ASC" %\
                   (Status.PId, Status.ANo)

        tableQDa = Status.DB.energyflowsqda.sql_select(sqlQuery)
        Interfaces.QDa = tableQDa[0].values()
        Interfaces.QDa.pop() #Delete the last element of the list (empty)
        Interfaces.QDa.pop(0) #Delete the first 4 elements in the QD, QA lists
        Interfaces.QDa.pop(0)
        Interfaces.QDa.pop(0)
        Interfaces.QDa.pop(0)
    
        tableQAa = Status.DB.energyflowsqaa.sql_select(sqlQuery)
        Interfaces.QAa = tableQAa[0].values()
        Interfaces.QAa.pop() #Delete the last element of the list (empty)
        Interfaces.QAa.pop(0) #Delete the first 4 elements in the QD, QA lists
        Interfaces.QAa.pop(0)
        Interfaces.QAa.pop(0)
        Interfaces.QAa.pop(0)
        
        tableQDh = Status.DB.energyflowsqdh.sql_select(sqlQuery)
        for i in range(len(tableQDh)):
            Interfaces.QDh.append(tableQDh[i].values())
            Interfaces.QDh[i].pop() #Delete the last element of the list (empty)
            Interfaces.QDh[i].pop(0) #Delete the first 4 elements in the QD, QA lists
            Interfaces.QDh[i].pop(0)
            Interfaces.QDh[i].pop(0)
            Interfaces.QDh[i].pop(0)

        tableQAh = Status.DB.energyflowsqah.sql_select(sqlQuery)
        for i in range(len(tableQAh)):
            Interfaces.QAh.append(tableQAh[i].values())
            Interfaces.QAh[i].pop() #Delete the last element of the list (empty)
            Interfaces.QAh[i].pop(0) #Delete the first 4 elements in the QD, QA lists
            Interfaces.QAh[i].pop(0)
            Interfaces.QAh[i].pop(0)
            Interfaces.QAh[i].pop(0)
#-------------------------------------------------------------------------------------

    def setDefaultDemand(self):

        NT = Status.NT
        Nt = Status.Nt
        DT = Status.TemperatureInterval
        MaxT = Status.MaximumTemperature

        #......................................................
        #set temperature range

        Interfaces.T = frange(0.0,MaxT+5.0,DT)
        print 'setDefaultDemand: T = ', Interfaces.T
        
        #......................................................
        #set heat demand curves

        hourlyProfileD = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,5.0,2.0,3.3,10.0,4.0,9.0,2.0,8.0,7.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0] 

        for iT in range(NT+1): #NT + 1 + 1 -> additional value for T > Tmax #SD ->NT + 1, 15/03/2008

            fscale = iT*100.0

            hour = 0
            load = []
            ushload = [] #SD, 15/03/2008
        
            for it in range(Nt+1): 
                load.append(hourlyProfileD[hour]*fscale)
                ushload.append(0.0) #SD - create zero filled list, 15/03/2008
                if hour < 23:
                    hour += 1
                else:
                    hour = 0
                    
            self.QD_Tt.append(load)
            self.USHj_Tt.append(ushload) #SD - create zero filled matrix, 15/03/2008
             
        self.QD_Tt_mod = self.QD_Tt
##        print "Default demand profile", self.QD_Tt
##        print "Default USHj_Tt", self.USHj_Tt

##        print 'My loop start'       
##        for it in range(Nt+1):
##            print ''
##            for iT in range(NT+1):
##                print self.QD_Tt[iT][it],
##        print 'My loop end'

#Transformation from QD_Tt to QDh
        #self.QDh = []
        for it in range(Nt+1):
            qdhrow = []
            for iT in range(NT+1):
                qdhrow.append(self.QD_Tt[iT][it])
            self.QDh.append(qdhrow)
##        print 'QDh', self.QDh

        #......................................................
        #set heat avallability curves

        hourlyProfileA = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,5.0,2.0,3.3,10.0,4.0,9.0,2.0,8.0,7.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0]

        for iT in range(NT+1): #NT + 1 + 1 -> additional value for T > Tmax #SD -> NT + 1, 15/03/2008

            if iT == 0:
                fscale = 100.0
            else:
                fscale = 100.0/iT

            if fscale < 25.0:
                fscale = 0.0
            
            hour = 0
            load = []
        
            for it in range(Nt+1):
                load.append(hourlyProfileA[hour]*fscale)

                if hour < 23:
                    hour += 1
                else:
                    hour = 0
                    
            self.QA_Tt.append(load)
             
        self.QA_Tt_mod = self.QA_Tt
##        print "Default availability profile", self.QD_Tt

##        print 'My loop start - availability'       
##        for it in range(Nt+1):
##            print ''
##            for iT in range(NT+1):
##                print self.QA_Tt[iT][it],
##        print 'My loop end - availability'

#Transformation from QA_Tt to QAh
        #self.QAh = []
        for it in range(Nt+1):
            qahrow = []
            for iT in range(NT+1):
                qahrow.append(self.QA_Tt[iT][it])
            self.QAh.append(qahrow)
##        print 'QAh', self.QAh
        
#...............................................
#Obtain the annual curves QDa and QAa
        Interfaces.QDa = []
        for j in range(len(self.QDh[0])):
            sum = 0.0
            for i in range(len(self.QDh)):
                sum = sum + self.QDh[i][j]
            Interfaces.QDa.append(sum)
##        print 'In interface: QDa:'
##        print self.QDa
##
##        for each in self.QDh:
##            print each
#..........................
        Interfaces.QAa = []
        for j in range(len(self.QAh[0])):
            sum = 0.0
            for i in range(len(self.QAh)):
                sum = sum + self.QAh[i][j]
            Interfaces.QAa.append(sum)
##        print 'In interface: QAa:'
##        print self.QAa
##
##        for each in self.QAh:
##            print each
           

#------------------------------------------------------------------------
    def userDefinedLevel1(self):

        row = Status.DB.uheatpump.Questionnaire_id[self.PId].AlternativeProposalNo[self.ANo][0]

        HPTypeUD = row.UHPType
        Hop = row.UHPMinHop
        DTmaxUD = row.UHPDTMax
        TgeUD = row.UHPTgenIn
        TmaxUD = row.UHPmaxT
        TminUD = row.UHPminT

        self.userDefined1 = (TmaxUD, TminUD, HPTypeUD, Hop, DTmaxUD, TgeUD)
        return self.userDefined1
#------------------------------------------------------------------------
    
    def userDefinedLevel2(self):
 
        rowUHP = Status.DB.uheatpump.Questionnaire_id[self.PId].AlternativeProposalNo[self.ANo][0]

        rowPS = Status.DB.psetupdata.PSetUpData_ID[self.SetUpId][0]
    
        HPTypeUD = rowUHP.UHPType
        Hop = rowPS.UHPMinHop
        DTmaxUD = rowPS.UHPDTMax
        TgeUD = rowPS.UHPTgenIn
        TmaxUD = rowPS.UHPmaxT
        TminUD = rowPS.UHPminT

        self.userDefined2 = (TmaxUD, TminUD, HPTypeUD, Hop, DTmaxUD, TgeUD)
        return self.userDefined2  
    
#------------------------------------------------------------------------

    def userDefinedLevel3(self):

        rowPS = Status.DB.psetupdata.PSetUpData_ID[self.SetUpId][0]
    
        HPTypeUD = rowPS.UHPType
        Hop = rowPS.UHPMinHop
        DTmaxUD = rowPS.UHPDTMax
        TgeUD = rowPS.UHPTgenIn
        TmaxUD = rowPS.UHPmaxT
        TminUD = rowPS.UHPminT

        self.userDefined3 = (TmaxUD, TminUD, HPTypeUD, Hop, DTmaxUD, TgeUD)
        return self.userDefined3  

#------------------------------------------------------------------------
            
#=================================================================================

if __name__ == "__main__":
    # for testing purposes only
    # should be invoked: python interfaces.py
    #
    from einstein.modules.interfaces import Interfaces
    # values for testing purposes
    NT = 5
    Nt = 6
    Status.PId=1
    Status.ANo=0
    # create an instance of the Interfaces class. This will invoke the __init__ method
    # where the initialization work is done and the class variables are loaded.
    # Afterwards, it is not necessary to instantiate the class, just a reference
    # of type Interfaces.variable will allow access to the class variables.
    int = Interfaces(NT, Nt) # initialization. this is necessary only once
    int = None               # this instance is not longer useful

    print 'T='+repr(Interfaces.T)
    print 'QDa=' + repr(Interfaces.QDa)
    print 'QAa=' + repr(Interfaces.QAa)
    print 'QDh=' + repr(Interfaces.QDh)
    print 'QAh=' + repr(Interfaces.QAh)
