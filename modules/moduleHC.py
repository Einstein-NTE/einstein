# -*- coding: cp1252 -*-
#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#   ModuleHC (Heat and Cold Supply)
#           
#------------------------------------------------------------------------------
#           
#   Module for design of HC Supply cascade
#
#==============================================================================
#
#   Version No.: 0.03
#   Created by:         Hans Schweiger  03/04/2008
#   Last revised by:    Stoyan Danov    29/04/2008
#                       Stoyan Danov    30/04/2008
#                       Stoyan Danov    05/05/2008
#
#       Changes to previous version:
#   29/04/2008 SD: added: cascadeMoveUp, cascadeMoveDown, cascadeMoveToTop, ...
#   30/04/2008 SD: reference to cgenerationhc commented -> line 60
#   05/05/2008 SD: move query PId,ANo from __init__ to initPanel
#   
#------------------------------------------------------------------------------     
#   (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#   www.energyxperts.net / info@energyxperts.net
#
#   This program is free software: you can redistribute it or modify it under
#   the terms of the GNU general public license as published by the Free
#   Software Foundation (www.gnu.org).
#
#============================================================================== 

from sys import *
from math import *
from numpy import *


from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP
from einstein.modules.constants import *

class ModuleHC(object):

    HCList = []
    
    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def initPanel(self):
#------------------------------------------------------------------------------
#       screens existing equipment, whether there are already heat pumps
#       XXX to be implemented
#------------------------------------------------------------------------------

        self.DB = Status.DB
        self.sql = Status.SQL
        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        self.equipments = self.DB.qgenerationhc.sql_select(sqlQuery)
        self.NEquipe = len(self.equipments)

        Status.int.getEquipmentCascade()
        self.cascadeIndex = 0
        
#............................................................................................
#XXX FOR TESTING PURPOSES ONLY: load default demand
# here it should be assured that heat demand and availability for position in cascade
# of presently existing heat pumps is already defined

        Status.int.initCascadeArrays(self.NEquipe)
       
#............................................................................................
#returns HPList to the GUI for displaying in window

        self.updatePanel()
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def updatePanel(self):
#------------------------------------------------------------------------------
#       Here all the information should be prepared so that it can be plotted on the panel
#------------------------------------------------------------------------------

        dataList = []
        for i in range(self.NEquipe):
            row = Status.int.cascade[i]
            equipmentName=Status.DB.qgenerationhc.QGenerationHC_ID[row["equipeID"]][0].Equipment
            dataList.append(noneFilter([i+1,row["equipeNo"],equipmentName,row["equipeType"],row["equipePnom"],"???"]))
        data = array(dataList)

        Status.int.setGraphicsData(self.keys[0], data)

        try:
            Status.int.setGraphicsData('HC Info',{"noseque":55})
        except:
            pass

#------------------------------------------------------------------------------
    def cascadeMoveUp(self,actualCascadeIndex):
#------------------------------------------------------------------------------
#        moves equipment up in the cascade sequence
#------------------------------------------------------------------------------

        idx = 0
        for i in range(self.NEquipe):
            if self.equipments[i]['CascadeIndex'] == actualCascadeIndex:
                idx = self.equipments[i]['CascadeIndex']

        if idx == 0:
            print 'moduleHC: cascadeMoveUp: there is no equipe with CascadeIndex =', actualCascadeIndex
            return 0

        elif idx == 1:
            print 'moduleHC: cascadeMoveUp: equipe cannot be moved up, actualCascadeIndex =', actualCascadeIndex
            return 1            

        else:
            try:
                actualEquip = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].CascadeIndex[actualCascadeIndex][0]
                upEquip = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].CascadeIndex[actualCascadeIndex - 1][0]

                actualEquip.CascadeIndex = actualCascadeIndex - 1
                upEquip.CascadeIndex = actualCascadeIndex          
                Status.SQL.commit()
            except:
                print "ModuleHC (cascadeMoveUp): severe error - couldn't find equipe"
                
            Status.int.getEquipmentCascade()

            return actualEquip.CascadeIndex


#------------------------------------------------------------------------------
    def cascadeMoveDown(self,actualCascadeIndex):
#------------------------------------------------------------------------------
#        moves equipment down in the cascade sequence
#------------------------------------------------------------------------------

        idx = 0
        for i in range(self.NEquipe):
            if self.equipments[i]['CascadeIndex'] == actualCascadeIndex:
                idx = self.equipments[i]['CascadeIndex']

        if idx == 0:
            return 0

        elif idx == self.NEquipe:
            return self.NEquipe

        else:
            try:
                actualEquip = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].CascadeIndex[actualCascadeIndex][0]
                downEquip = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].CascadeIndex[actualCascadeIndex + 1][0]

                actualEquip.CascadeIndex = actualCascadeIndex + 1
                downEquip.CascadeIndex = actualCascadeIndex          
                Status.SQL.commit()
            except:
                print "ModuleHC (cascadeMoveDown): severe error - couldn't find equipe"

            Status.int.getEquipmentCascade()

            return actualEquip.CascadeIndex

#------------------------------------------------------------------------------
    def cascadeMoveToTop(self,actualCascadeIndex):
#------------------------------------------------------------------------------
#   moves equipment to top in cascade sequence
#------------------------------------------------------------------------------

        for i in range(actualCascadeIndex,1,-1):
            newIndex = self.cascadeMoveUp(i)

        return newIndex

#------------------------------------------------------------------------------
    def cascadeMoveToBottom(self,actualCascadeIndex):
#------------------------------------------------------------------------------
#   moves equipment to bottom in cascade sequence
#------------------------------------------------------------------------------

        for i in range(actualCascadeIndex,self.NEquipe):
            newIndex = self.cascadeMoveDown(i)

        return newIndex

#------------------------------------------------------------------------------
    def cascadeMoveTo(self,actualIndex,finalIndex):
#------------------------------------------------------------------------------
#   moves equipment to a userdefined finalIndex position in cascade sequence
#------------------------------------------------------------------------------

        if (finalIndex > actualIndex and finalIndex <= self.NEquipe):
            for i in range (actualIndex,finalIndex):
                newIndex = self.cascadeMoveDown(i)

        elif (finalIndex < actualIndex and finalIndex > 0):
            for i in range (actualIndex,finalIndex,-1):
                newIndex = self.cascadeMoveUp(i)

        else: newIndex = actualIndex

        return newIndex

#------------------------------------------------------------------------------

if __name__ == "__main__":
    print "Testing ModuleHC"
    import einstein.GUI.pSQL as pSQL, MySQLdb
    from einstein.modules.interfaces import *
    from einstein.modules.energy.moduleEnergy import *
    stat = Status("testModuleHC")

    Status.SQL = MySQLdb.connect(user="root", db="einstein")
    Status.DB = pSQL.pSQL(Status.SQL, "einstein")
    
    Status.PId = 99
    Status.ANo = 0
    Status.SetUpId = 1 #this is PSetUpData_ID
    
    Status.int = Interfaces()
    keys = ["HP Table","HP Plot","HP UserDef"]

    mod = ModuleHC(keys)
    
