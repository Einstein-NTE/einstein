# -*- coding: cp1252 -*-
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
#	Version No.: 0.12
#	Created by: 	    Hans Schweiger	10/03/2008
#	Revised by:         Hans Schweiger      13/03/2008
#	                    Tom Sobota          17/03/2008
#	                    Hans Schweiger      21/03/2008
#                           Stoyan Danov        27/03/2008
#                           Hans Schweiger      02/04/2008
#                           Stoyan Danov        09/04/2008
#                           Stoyan Danov        24/04/2008
#                           Stoyan Danov        30/04/2008
#                           Hans Schweiger      05/05/2008
#                           Hans Schweiger      14/05/2008
#                           Stoyan Danov        15/05/2008
#
#       Changes in last update:
#       - new arrays QDh_mod, USHj ...
#       - new function DefaultDemand
#       16/3/2008 Added methods for getting and setting values.
#       17/3/2008 Added support for getting and setting graphic values.
#       21/3/2008 Storage space for full heat supply cascade
#                   QDh/QAh renamed to QD_Tt, QA_Tt
#       27/03/2008 getEquipmentCascade(self): adaptation
#       02/04/2008 corrections in getEquipmentCascade
#       09/04/2008 getEquipmentCascade: add filling EquipTableDataList-data fields shown in Table panel
#       24/04/2008 getEquipmentCascade: add filling EquipTableDataList-changed
#       30/04/2008 eliminate references to C tables, function affected: getEquipmentCascade
#       05/05/2008  autocorrection of equipment cascade introduced
#       14/05/2008  auxiliary function "print cascade" added for testing purposes
#       15/05/2008 initCascadeArrays: parenthesis added in call calculateQ_Tt()...
#                   functions added: printCascade_mod, printUSH
#
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

QUERY = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY IndexNo ASC"

class Interfaces(object):

#..........................................................................
# DATA BLOCK 1: energy flows in the system
    T = []      #temperature steps

# total heat demand and availability in the system

    QD_T = []
    QA_T = []
    QD_Tt = []
    QA_Tt = []
    
# intermediate heat demand / availability within equipment cascade

    QD_T_mod = []    
    QA_T_mod = []
    QD_Tt_mod = []
    QA_Tt_mod = []

# heat supplied by each equipment
    USHj_Tt = []    
    USHj_T = []
    USHj_t = []
    USHj = []
    
# waste heat absorbed in each equipment
    QHXj_Tt = []    
    QHXj_T = []
    QHXj_t = []
    QHXj = []

# dictionary of the HC supply cascade. entries "equipeID" and "equipeNo"

    NEquipe = None
    cascade = []
    EquipTableDataList = []
    
#..........................................................................
# DATA BLOCK 2: graphics data dictionary for graphics on panels

    GData = {}

   
#------------------------------------------------------------------------------		
    def __init__(self):
#------------------------------------------------------------------------------		
#
# Instance initialization
#
        self.T = []
        for iT in range(Status.NT+1):
            self.T.append(iT*Status.TemperatureInterval)
        self.T.append(999.0)
        
        self.setDefaultDemand()
        
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    def createQ_Tt(self):
#------------------------------------------------------------------------------		
#   function for creating an empty matrix for temperature and time dependent
#   energy flows
#------------------------------------------------------------------------------		
        Q_Tt = []
        for iT in range(Status.NT+2):
            Q_Tt.append(self.createQ_t())

        return Q_Tt

#------------------------------------------------------------------------------		
    def createQ_t(self):
#------------------------------------------------------------------------------		
#   function for creating an empty vector for time dependent
#   energy flows
#------------------------------------------------------------------------------		
        Q_t = []
        for it in range(Status.Nt+1):
            Q_t.append(0.0)
        
        return Q_t

#------------------------------------------------------------------------------		
    def createQ_T(self):
#------------------------------------------------------------------------------		
#   function for creating an empty vector for time dependent
#   energy flows
#------------------------------------------------------------------------------		
        Q_T = []
        for iT in range(Status.NT+2):
            Q_T.append(0.0)
        
        return Q_T

#------------------------------------------------------------------------------		
    def initCascadeArrays(self,NEquipe):
#------------------------------------------------------------------------------		
#..............................................................................
# initialising storage space for energy flows in cascade
# assigning total heat demand and availability to the first row in cascade

        self.NEquipe = NEquipe
        
        Interfaces.QD_Tt_mod = []      
        Interfaces.QD_T_mod = []
        Interfaces.QA_Tt_mod = []       
        Interfaces.QA_T_mod = []

        Interfaces.USHj_Tt = []
        Interfaces.USHj_T = []
        Interfaces.QHXj_Tt = []
        Interfaces.QHXj_T = []

        Interfaces.QD_Tt_mod.append(self.QD_Tt)       
        Interfaces.QD_T_mod.append(self.QD_T)
        Interfaces.QA_Tt_mod.append(self.QA_Tt)      
        Interfaces.QA_T_mod.append(self.QA_T)

        for j in range(NEquipe):
            Interfaces.QD_Tt_mod.append(self.QD_Tt)       
            Interfaces.QD_T_mod.append(self.QD_T)
            Interfaces.QA_Tt_mod.append(self.QA_Tt)      
            Interfaces.QA_T_mod.append(self.QA_T)

            Interfaces.USHj_Tt.append(self.createQ_Tt())
            Interfaces.USHj_T.append(self.createQ_T())
            Interfaces.QHXj_Tt.append(self.createQ_Tt())
            Interfaces.QHXj_T.append(self.createQ_T())

        self.printCascade()
                        
#------------------------------------------------------------------------------		
    def addCascadeArrays(self):
#------------------------------------------------------------------------------		

        Interfaces.QD_Tt_mod.append(self.QD_Tt)       
        Interfaces.QD_T_mod.append(self.QD_T)
        Interfaces.QA_Tt_mod.append(self.QA_Tt)      
        Interfaces.QA_T_mod.append(self.QA_T)

        Interfaces.USHj_Tt.append(self.createQ_Tt())
        Interfaces.USHj_T.append(self.createQ_T())
        Interfaces.QHXj_Tt.append(self.createQ_Tt())
        Interfaces.QHXj_T.append(self.createQ_T())

        self.NEquipe += 1

#------------------------------------------------------------------------------		
    def deleteCascadeArrays(self,NEquipe):
#------------------------------------------------------------------------------		

        Interfaces.QD_Tt_mod.pop(NEquipe-1)       
        Interfaces.QD_T_mod.pop(NEquipe-1)
        Interfaces.QA_Tt_mod.pop(NEquipe-1)      
        Interfaces.QA_T_mod.pop(NEquipe-1)

        Interfaces.USHj_Tt.pop(NEquipe-1)
        Interfaces.USHj_T.pop(NEquipe-1)
        Interfaces.QHXj_Tt.pop(NEquipe-1)
        Interfaces.QHXj_T.pop(NEquipe-1)

        self.NEquipe -= 1


        
#------------------------------------------------------------------------------		
    def printCascade(self,):
#------------------------------------------------------------------------------		

        NT = Status.NT
        print "Heat Demand"
        print "CascadeIndex - QD_total - QD_Tt(first day)"
        for i in range(self.NEquipe+1):
            print i,\
            "%10.4f"%Interfaces.QD_T_mod[i][NT+1],\
            Interfaces.QD_Tt_mod[i][NT+1][0:23]
        print "Heat Availability"
        print "CascadeIndex - QA_total - QA_Tt(first day)"
        for i in range(self.NEquipe+1):
            print i,\
            "%10.4f"%Interfaces.QA_T_mod[i][NT+1],\
            Interfaces.QA_Tt_mod[i][0][0:23]
        
#------------------------------------------------------------------------------		
    def printUSH(self):
#------------------------------------------------------------------------------		

        NT = Status.NT
        print "USH"
        print "CascadeIndex - USHj_total - USHj_Tt(first day)"
        for i in range(self.NEquipe+1):
            print i,\
            "%10.4f"%Interfaces.USHj_T[i][NT],\
            Interfaces.USHj_Tt[i][NT][0:23]
        
#------------------------------------------------------------------------------		
    def printCascade_mod(self,cascade):
#------------------------------------------------------------------------------		

        NT = Status.NT
        print "Heat Demand"
        print "CascadeIndex - QD_total - QD_Tt(first day)"
        for i in range(self.NEquipe+1):
            if i == cascade:
                print i,\
                "%10.4f"%Interfaces.QD_T_mod[i][NT+1],\
                Interfaces.QD_Tt_mod[i][NT+1][0:23]
            else:
                pass
        print "Heat Availability"
        print "CascadeIndex - QA_total - QA_Tt(first day)"
        for i in range(self.NEquipe+1):
            if i == cascade:
                print i,\
                "%10.4f"%Interfaces.QA_T_mod[i][0],\
                Interfaces.QA_Tt_mod[i][0][0:23]
            else:
                pass
#------------------------------------------------------------------------------
    def getEquipmentCascade(self):
#------------------------------------------------------------------------------
#   gets the equipment list
#------------------------------------------------------------------------------


        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY CascadeIndex ASC"%(Status.PId,Status.ANo)
        self.equipments = Status.DB.qgenerationhc.sql_select(sqlQuery) #SD change 30/04.2008
        self.NEquipe = len(self.equipments) #SD change 30/04.2008

        self.cascade = []
        for j in range(self.NEquipe):
            self.cascade.append({"equipeID":self.equipments[j].QGenerationHC_ID,"equipeNo":self.equipments[j].EqNo,\
                            "equipeType":self.equipments[j].EquipType,\
                            "equipePnom":self.equipments[j].HCGPnom})
            if (self.equipments[j].CascadeIndex != j+1):
                print "Interfaces (getEquipmentCascade): error in SQL data - cascade index %s corrected to new index %s"%\
                      (self.equipments[j].CascadeIndex,j+1)
                self.equipments[j].CascadeIndex = j+1
                Status.SQL.commit()


        self.EquipTableDataList = []
        for j in range(self.NEquipe):
            self.EquipTableDataList.append([self.equipments[j].Equipment, self.equipments[j].HCGPnom, self.equipments[j].HCGTEfficiency, \
                                            self.equipments[j].EquipType, self.equipments[j].HPerYearEq, self.equipments[j].YearManufact]) #SD change 30/04.2008
                                                

#------------------------------------------------------------------------------		
    def setGraphicsData(self,key, data):
#------------------------------------------------------------------------------		
# method for storing graphics data
# the data are stored in the dictionary GData under the key 'key'
#------------------------------------------------------------------------------		
        Interfaces.GData[key] = data


#------------------------------------------------------------------------------		
    def setDefaultDemand(self):
#------------------------------------------------------------------------------		
# dummy fucntion for bringing in some data into the demand matrix
#------------------------------------------------------------------------------		
        NT = Status.NT
        Nt = Status.Nt

        hourlyProfile = [0,0,0,0,0,0,0,1,5,2,3.3,10,4,9,2,8,7,1,0,0,0,0,0,0] 
        Tpinch = 40.0
        for iT in range(NT+2): #NT + 1 + 1 -> additional value for T > Tmax
            fscaleD = max(self.T[iT]-Tpinch,0)*1e+2
            fscaleA = max(Tpinch-self.T[iT],0)*1e+2

            load = []
            waste = []
            hour = 0
            for it in range(Nt+1):
                 load.append(hourlyProfile[hour]*fscaleD)
                 waste.append(hourlyProfile[hour]*fscaleA)
                 
                 hour = (hour+1) % 24
                    
            self.QD_Tt.append(load)
            self.QA_Tt.append(waste)
             
        self.QD_T = self.calcQ_T(self.QD_Tt)    #annual values
        self.QA_T = self.calcQ_T(self.QA_Tt)
        print "Interfaces (set default demand): ",self.QD_T
        print "Interfaces (set default availability): ",self.QA_T

#------------------------------------------------------------------------------		
    def calcQ_T(self,Q_Tt):
#------------------------------------------------------------------------------		
#   Function that calculates the annual integral
#------------------------------------------------------------------------------		

        Q_T = []
        for iT in range(Status.NT + 2):
            Q_T.append([])
            Q_T[iT] = 0
            for it in range(Status.Nt):
                Q_T[iT] += Q_Tt[iT][it]
        return Q_T

#==============================================================================
# from here on residuals that probably can be deleted in the future       
    def chargeCurvesQDQA(self):
        self.setQDa()
        self.setQAa()
        self.setQDh()
        self.setQAh()

    def getQDa(self):
        return Interfaces.QDa
    
    def getQAa(self):
        return Interfaces.QAa

    def getQDh(self):
        return Interfaces.QDh

    def getQAh(self):
        return Interfaces.QAh
        

    def setQDa(self):
        global QUERY
        sqlQuery = QUERY % (Status.PId, Status.ANo)
        tableQDa = Status.DB.energyflowsqda.sql_select(sqlQuery)
        Interfaces.QDa = tableQDa[0].values()
        Interfaces.QDa.pop() #Delete the last element of the list (empty)
        Interfaces.QDa.pop(0) #Delete the first 4 elements in the QD, QA lists
        Interfaces.QDa.pop(0)
        Interfaces.QDa.pop(0)
        Interfaces.QDa.pop(0)

    def setQAa(self):
        global QUERY
        sqlQuery = QUERY % (Status.PId, Status.ANo)
        tableQAa = Status.DB.energyflowsqaa.sql_select(sqlQuery)
        Interfaces.QAa = tableQAa[0].values()
        Interfaces.QAa.pop() #Delete the last element of the list (empty)
        Interfaces.QAa.pop(0) #Delete the first 4 elements in the QD, QA lists
        Interfaces.QAa.pop(0)
        Interfaces.QAa.pop(0)
        Interfaces.QAa.pop(0)

    def setQDh(self):
        global QUERY
        sqlQuery = QUERY % (Status.PId, Status.ANo)
        tableQDh = Status.DB.energyflowsqdh.sql_select(sqlQuery)
        for i in range(len(tableQDh)):
            Interfaces.QDh.append(tableQDh[i].values())
            Interfaces.QDh[i].pop() #Delete the last element of the list (empty)
            Interfaces.QDh[i].pop(0) #Delete the first 4 elements in the QD, QA lists
            Interfaces.QDh[i].pop(0)
            Interfaces.QDh[i].pop(0)
            Interfaces.QDh[i].pop(0)

    def setQAh(self):
        global QUERY
        sqlQuery = QUERY % (Status.PId, Status.ANo)
        tableQAh = Status.DB.energyflowsqah.sql_select(sqlQuery)
        for i in range(len(tableQAh)):
            Interfaces.QAh.append(tableQAh[i].values())
            Interfaces.QAh[i].pop() #Delete the last element of the list (empty)
            Interfaces.QAh[i].pop(0) #Delete the first 4 elements in the QD, QA lists
            Interfaces.QAh[i].pop(0)
            Interfaces.QAh[i].pop(0)
            Interfaces.QAh[i].pop(0)               

if __name__ == "__main__":
    # for testing purposes only
    # should be invoked: python interfaces.py
    #
    from einstein.modules.interfaces import Interfaces
    def connectToDB():
        #----- Connect to the Database
        MySql = MySQLdb.connect(host='localhost', user='root', passwd='tom.tom', db='einstein')
        Status.SQL = MySql
        Status.DB =  pSQL.pSQL(MySql, 'einstein')
        print "data base connected ",Status.SQL,Status.DB


    # values for testing purposes
    NT = 5
    Nt = 6
    Status.PId=1
    Status.ANo=1
    # Connect to database
    #
    connectToDB()
    #
    # create an instance of the Interfaces class. This will invoke the __init__ method
    # where the initialization work is done and the class variables are loaded.
    # Afterwards, it is not necessary to instantiate the class, just a reference
    # of type Interfaces.variable will allow access to the class variables.
    intf = Interfaces(NT, Nt) # initialization.
    intf.chargeCurvesQDQA()

    print 'T='+repr(Interfaces.T)
    print 'QDa=' + repr(intf.getQDa())
    print 'QAa=' + repr(intf.getQAa())
    print 'QDh=' + repr(intf.getQDh())
    print 'QAh=' + repr(intf.getQAh())
