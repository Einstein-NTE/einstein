#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	INDUSTRY
#			
#------------------------------------------------------------------------------
#			
#	Definition of objects defining and handling a project (industry)
#
#==============================================================================
#
#	Version No.: 0.06
#
#       Created by:     Hans Schweiger      02/04/2008
#       Revised by:     Hans Schweiger      15/04/2008
#                       Hans Schweiger      18/04/2008
#                       Hans Schweiger      23/04/2008
#
#       15/04/08: HS    Functions Add-, Copy-, Delete-Alternative
#       18/04/08: HS    Functions Add-, Copy-, Delete-Project
#                       UserInteractionLevel
#       23/04/08: HS    Completed list of data tables to be created in
#                       createNewProject
#       02/05/08: HS    deleteProduct, deleteFuel, deleteProcess
#                       and addFuel/ProcessDummy added
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

from einstein.GUI.status import Status
from messageLogger import *
from constants import *

#------------------------------------------------------------------------------		
def copySQLRows(table,query,keyID,keyPar,valPar):
#------------------------------------------------------------------------------		
#       auxiliary function for copying full rows in SQL Tables
#------------------------------------------------------------------------------		
    rows = table.sql_select(query)

    newID = None
        
    for row in rows:
#..............................................................................
# translates the pSQL - object into a dictionary

        mydict = {}
        mydict.update(row)

#..............................................................................
# eliminates the main key of the table, that has to be unique

        mydict.pop(keyID)
        
#..............................................................................
# changes one parameter within the row (usually AlternativeNo or ProjectID

        if valPar is not None:
            mydict.update([(keyPar,valPar)])

#..............................................................................
# eliminates the None's from the dictionary (would otherwise be substituted by
# 0 in SQL

        noneKeys = []
        for key in mydict:
            if mydict[key] is None:
                noneKeys.append(key)
        for key in noneKeys:
            mydict.pop(key)
                
#..............................................................................
# now inserts the new row into the SQL Table

        newID = table.insert(mydict)
        print "copySQL rows. newID = ",newID

    return newID
#------------------------------------------------------------------------------		
def deleteSQLRows(table,query):
#------------------------------------------------------------------------------		
#       auxiliary function for copying full rows in SQL Tables
#------------------------------------------------------------------------------		
    rows = table.sql_select(query)

    for row in rows:
        print "deleting: ",row
        row.delete()

#------------------------------------------------------------------------------		
def shiftANoInSQLRows(table,query, shift):
#------------------------------------------------------------------------------		
#       auxiliary function for changing a value in rows
#------------------------------------------------------------------------------		
    rows = table.sql_select(query)

    for row in rows:
        newval = row.AlternativeProposalNo + shift
        row.AlternativeProposalNo = newval
        print "newval assigned",newval,row.AlternativeProposalNo
                
#==============================================================================
#       PROJECT CLASS
#==============================================================================

class Project(object):

#------------------------------------------------------------------------------		
    def __init__(self):
#------------------------------------------------------------------------------		
# initialisation. does the initialisation of basic parameters in Status
#------------------------------------------------------------------------------		

#..............................................................................
# get last tool settings from table STOOLS (last project opened, etc.)

        self.getLastToolSettings()

#..............................................................................
# set active project to the last one opened

        self.setActiveProject(Status.PId)

#------------------------------------------------------------------------------		
        
#------------------------------------------------------------------------------		
# HANDLING OF ALTERNATIVE PROPOSALS (= REPEATED PART OF A PROJECT)
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------
    def createNewAlternative(self,originalANo,shortName,description):
#------------------------------------------------------------------------------
#   creates a new alternative copying all entries for the original ANo
#------------------------------------------------------------------------------

        DB = Status.DB

        Status.NoOfAlternatives += 1
        ANo = Status.NoOfAlternatives

        sproject = Status.DB.sproject.ProjectID[Status.PId][0]
        sproject.NoOfAlternatives = Status.NoOfAlternatives

        print "Project (createNewAlternative) - project %s, copying from"%Status.PId,originalANo,ANo

#..............................................................................
# create a copy of present state ...

        if (originalANo == 0):

#XXX init project information with defaults where necessary
#            initAlternative()
             pass
            
#..............................................................................
# ... create a new alternative copying from an existing one
        else:
            pass

#..............................................................................
# copying Q- and corresponding C-Tables

        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,originalANo)

        #additional query necessary for old tables who still have Questionnaire_id instead of ProjectID
        sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,originalANo)

        copySQLRows(DB.salternatives,sqlQuery,"SAlternative_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.cgeneraldata,sqlQueryQ,"CGeneralData_ID","AlternativeProposalNo",ANo)

        copySQLRows(DB.qbuildings,sqlQueryQ,"QBuildings_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.qdistributionhc,sqlQueryQ,"QDistributionHC_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.qelectricity,sqlQueryQ,"QElectricity_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.qfuel,sqlQueryQ,"QFuel_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.qgenerationhc,sqlQueryQ,"QGenerationHC_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.qheatexchanger,sqlQuery,"QHeatExchanger_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.qprocessdata,sqlQueryQ,"QProcessData_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.qproduct,sqlQueryQ,"QProduct_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.qrenewables,sqlQueryQ,"QRenewables_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.qwasteheatelequip,sqlQuery,"QWasteHeatElEquip_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.uheatpump,sqlQueryQ,"UHeatPump_ID","AlternativeProposalNo",ANo)

#..............................................................................
# rename alternative

        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,ANo)
        a = DB.salternatives.sql_select(sqlQuery)[0]
        a.ShortName = shortName
        a.Description = description

        Status.SQL.commit()
        self.setActiveAlternative(ANo)

#------------------------------------------------------------------------------
        
#------------------------------------------------------------------------------
    def deleteAlternative(self,ANo):
#------------------------------------------------------------------------------
#   deletes all entries for the original ANo
#------------------------------------------------------------------------------

        if ANo > Status.NoOfAlternatives or ANo <= 0:
            print"Project (deleteAlternative) - project %s, cannot delete alternative "%Status.PId,ANo
            return -1
        
        print "Project (deleteAlternative) - project %s, deleting alternative "%Status.PId,ANo

#..............................................................................
# deleting Q- and corresponding C-Tables

        DB = Status.DB
        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,ANo)

        #additional query necessary for old tables who still have Questionnaire_id instead of ProjectID
        sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,ANo)

        deleteSQLRows(DB.salternatives,sqlQuery)
        deleteSQLRows(DB.cgeneraldata,sqlQueryQ)

        deleteSQLRows(DB.qbuildings,sqlQueryQ)
        deleteSQLRows(DB.qdistributionhc,sqlQueryQ)
        deleteSQLRows(DB.qelectricity,sqlQueryQ)
        deleteSQLRows(DB.qfuel,sqlQueryQ)
        deleteSQLRows(DB.qgenerationhc,sqlQueryQ)
        deleteSQLRows(DB.qheatexchanger,sqlQuery)
        deleteSQLRows(DB.qprocessdata,sqlQueryQ)
        deleteSQLRows(DB.qproduct,sqlQueryQ)
        deleteSQLRows(DB.qrenewables,sqlQueryQ)
        deleteSQLRows(DB.qwasteheatelequip,sqlQuery)
        deleteSQLRows(DB.uheatpump,sqlQueryQ)


#..............................................................................
# changing ANos in all rows with ANo higher than the deleted one

        for i in range(ANo+1,Status.NoOfAlternatives+1):
            sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,i)

        #additional query necessary for old tables who still have Questionnaire_id instead of ProjectID
            sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,i)

            print "Project (deleteAlternative): shifting row"
            
            shiftANoInSQLRows(DB.salternatives,sqlQuery,-1)
            shiftANoInSQLRows(DB.cgeneraldata,sqlQueryQ,-1)

            shiftANoInSQLRows(DB.qbuildings,sqlQueryQ,-1)
            shiftANoInSQLRows(DB.qdistributionhc,sqlQueryQ,-1)
            shiftANoInSQLRows(DB.qelectricity,sqlQueryQ,-1)
            shiftANoInSQLRows(DB.qfuel,sqlQueryQ,-1)
            shiftANoInSQLRows(DB.qgenerationhc,sqlQueryQ,-1)
            shiftANoInSQLRows(DB.qheatexchanger,sqlQuery,-1)
            shiftANoInSQLRows(DB.qprocessdata,sqlQueryQ,-1)
            shiftANoInSQLRows(DB.qproduct,sqlQueryQ,-1)
            shiftANoInSQLRows(DB.qrenewables,sqlQueryQ,-1)
            shiftANoInSQLRows(DB.qwasteheatelequip,sqlQuery,-1)
            shiftANoInSQLRows(DB.uheatpump,sqlQueryQ,-1)


#..............................................................................
# book-keeping: reduce number of alernatives in the system

        Status.NoOfAlternatives -= 1
        ANo = Status.NoOfAlternatives
        self.setActiveAlternative(ANo)

        sproject = Status.DB.sproject.ProjectID[Status.PId][0]
        sproject.NoOfAlternatives = Status.NoOfAlternatives


        Status.SQL.commit()

#------------------------------------------------------------------------------
    def getAlternativeList(self):
#------------------------------------------------------------------------------

        defaultList = [[-1, "Present State (original)",
                            "original data as delivered in questionnaire",
                            "---","---","---"],
                            [0,"Present State (checked)",
                            "complete data set for present state after cross-checking and data estimation",
                            "---","---","---"]]

        alternativeList = []
        
        for ANo in range(-1,Status.NoOfAlternatives+1):
            try:
                a = Status.DB.salternatives.ProjectID[Status.PId].AlternativeProposalNo[ANo][0]
                alternativeList.append([a.AlternativeProposalNo, a.ShortName, a.Description,a.StatusA,"par5","par6"])
            except:
                if ANo in [-1,0]:
                    alternativeList.append(defaultList[ANo+1])
                pass
        return alternativeList
            
#------------------------------------------------------------------------------
    def setActiveAlternative(self,n):
#------------------------------------------------------------------------------

        if (n>=-1) and n <= Status.NoOfAlternatives:
            try:
                Status.DB.sproject.ProjectID[Status.PId][0].ActiveAlternative = n
                Status.SQL.commit()
                Status.ANo = n
                Status.ActiveAlternativeName = Status.DB.salternatives.ProjectID[Status.PId].AlternativeProposalNo[n][0].ShortName
                print "Project (setActiveAlternative): set alternative to",n

            except:
                print "Project (setActiveAlternative): error trying to set alternative to ",n
                pass
        else:
            print "Project (setActiveAlternative): alternative number out of range"
            
#------------------------------------------------------------------------------
    def initAlternative(copyFrom = None):
#------------------------------------------------------------------------------
        # copy all demand parameters describing the industry (processes)
        # set status variables for the given alternative
        # ...
        pass
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
# HANDLING OF PROJECTS (CREATE,COPY,DELETE,INIT ...)
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------
    def getProjectList(self):
#------------------------------------------------------------------------------
#   returns a list with the names of the projects. used in panelQ0
#------------------------------------------------------------------------------
        projectList = []
        for n in Status.DB.questionnaire.Name["%"]:
            projectList.append(n.Name)
        return projectList


#------------------------------------------------------------------------------
    def getProjectID(self,name):
#------------------------------------------------------------------------------
#   returns a list with the names of the projects
#------------------------------------------------------------------------------

        return Status.DB.questionnaire.Name[name][0].Questionnaire_ID

#------------------------------------------------------------------------------
    def setActiveProject(self,PId,name=None):
#------------------------------------------------------------------------------
#   sets the presently active project no.
#   If PId <= 0 and no name is given, then all projects are deselected
#------------------------------------------------------------------------------
        
        try:
            print "trying to adjust the name"
            if name is not None:    #if a name is given, overwrite ID
                PId = self.getProjectID(name)
                print "Project (setActiveProject): project id updated to ",PId

            print "now checking for none or <= 0"                
            if (PId <= 0 or (PId is None)):
                Status.PId = -1
                Status.ActiveProjectName = "---"
                
#                Status.DB.stool.STool_ID[1][0].ActiveProject = PId
                print "Project (setActiveProject): active project set to ",PId

#                logTrack("Project (setActiveProject): no project selected")

            else:
                print "now looking for project parameters in sproject"                

                Status.ActiveProjectName = Status.DB.questionnaire.Questionnaire_ID[PId][0].Name
                sproject = Status.DB.sproject.ProjectID[PId][0]
                
                Status.NoOfAlternatives = sproject.NoOfAlternatives
#                logTrack("Project (setActiveProject): number of alternatives in the project %s"%Status.NoOfAlternatives)
                
                Status.PId = PId
                Status.DB.stool.STool_ID[1][0].ActiveProject = PId
                print "Project (setActiveProject): active project set to ",PId

                self.setActiveAlternative(sproject.ActiveAlternative)
#                logTrack("Project (setActiveProject): active alternative %s"&Status.ANo)

            Status.SQL.commit()

#HS2008-04-21: here just for TESTING. should later be assigned to real value.
            Status.ConsistencyCheckOK = True
            
            
        except:
            logTrack("Project (setActiveProject): Error opening project %s"%PId)

#------------------------------------------------------------------------------
    def createNewProject(self,originalPId,shortName,description,originalName=None):
#------------------------------------------------------------------------------

        DB = Status.DB
        questionnaires = Status.DB.questionnaire
        sprojects = Status.DB.sproject
        salternatives = Status.DB.salternatives
        
        if (originalPId <= 0) and (originalName is None):
#..............................................................................
# start a new project from scratch (creates basic project tables)

            newProject = {"Name": shortName,"DescripIndustry":description}
            newID = questionnaires.insert(newProject)
            print "new project inserted: ",newID

            newSProject = {"ProjectID":newID,
                           "NoOfAlternatives":0,
                           "ActiveAlternative":0,
                           "WriteProtected":0,
                           "StatusQ":EINSTEIN_NOTOK,
                           "LanguageReport":Status.LanguageTool,
                           "UnitsReport":Status.UnitsTool}
            sprojects.insert(newSProject)

            newAlternative = {"ProjectID":newID,
                              "AlternativeProposalNo":-1,
                              "ShortName":"present state (original)",
                              "Description":"original data as submitted by industry"}
            salternatives.insert(newAlternative)
            
            newAlternative = {"ProjectID":newID,
                              "AlternativeProposalNo":0,
                              "ShortName":"present state (checked)",
                              "Description":"present state after consistency checking"}
            salternatives.insert(newAlternative)
            
        else:  

            if originalName is not None:    #if a name is given, overwrite ID
                originalPId = self.getProjectID(originalName)

            print "Project (createNewProject): copying from ",originalPId,originalName

#..............................................................................
# copy a project
# 1. create a copy of the entry in the main table (questionnaire) with different ID and get the new ID

            sqlQuery = "ProjectID = '%s'"%originalPId
            #additional query necessary for old tables who still have Questionnaire_id instead of ProjectID
            sqlQueryQ = "Questionnaire_id = '%s'"%originalPId
            sqlQueryQ_ID = "Questionnaire_ID = '%s'"%originalPId
            print "Project (createNewProject: trying to insert copy of project %s: "%originalPId

            Status.SQL.commit()
            
            newID = copySQLRows(DB.questionnaire,sqlQueryQ_ID,"Questionnaire_ID",None,None)
            print "Project (createNewProject: copy of project %s inserted: "%originalPId,newID

#..............................................................................
# copying project data tables

            copySQLRows(DB.sproject,sqlQuery,"SProject_ID","ProjectID",newID)
            copySQLRows(DB.salternatives,sqlQuery,"SAlternative_ID","ProjectID",newID)
            
            copySQLRows(DB.cgeneraldata,sqlQueryQ,"CGeneralData_ID","Questionnaire_id",newID)
            copySQLRows(DB.qelectricity,sqlQueryQ,"QElectricity_ID","Questionnaire_id",newID)

            copySQLRows(DB.qbuildings,sqlQueryQ,"QBuildings_ID","Questionnaire_id",newID)
            copySQLRows(DB.qdistributionhc,sqlQueryQ,"QDistributionHC_ID","Questionnaire_id",newID)
            copySQLRows(DB.qelectricity,sqlQueryQ,"QElectricity_ID","Questionnaire_id",newID)
            copySQLRows(DB.qfuel,sqlQueryQ,"QFuel_ID","Questionnaire_id",newID)
            copySQLRows(DB.qgenerationhc,sqlQueryQ,"QGenerationHC_ID","Questionnaire_id",newID)
            copySQLRows(DB.qheatexchanger,sqlQuery,"QHeatExchanger_ID","Questionnaire_id",newID)
            copySQLRows(DB.qprocessdata,sqlQueryQ,"QProcessData_ID","Questionnaire_id",newID)
            copySQLRows(DB.qproduct,sqlQueryQ,"QProduct_ID","Questionnaire_id",newID)
            copySQLRows(DB.qrenewables,sqlQueryQ,"QRenewables_ID","Questionnaire_id",newID)
            copySQLRows(DB.qwasteheatelequip,sqlQuery,"QWasteHeatElEquip_ID","Questionnaire_id",newID)
            copySQLRows(DB.uheatpump,sqlQueryQ,"UHeatPump_ID","Questionnaire_id",newID)

#..............................................................................
# rename project

            print "renaming project [%s]"%newID,shortName,description
            
            q = DB.questionnaire.Questionnaire_ID[newID][0]
            print "query carried out"
            print q.Name,q.DescripIndustry
            q.Name = shortName
            q.DescripIndustry = description


        Status.SQL.commit()

        print "setting new project as active project"

        self.setActiveProject(newID)

        print "finished my work - uff"
        
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def deleteProject(self,PId,name=None):
#------------------------------------------------------------------------------
#   deletes all entries for a given project
#------------------------------------------------------------------------------

        if name is not None:    #if a name is given, overwrite ID
            PId = self.getProjectID(name)

        print "Project (deleteProject): deleting ",PId,name
            
        if PId <= 3:    #XXX security for testing -> not deleting projects with Pid < 3
            logError("Project (deleteProject) - project %s, cannot delete alternative "%PId)
            return -1
        
        logMessage("Project (deleteProject) -deleting project %s"%PId)

#..............................................................................
# deleting Q- and corresponding C-Tables

        DB = Status.DB
        sqlQuery = "ProjectID = '%s'"%PId

        #additional query necessary for old tables who still have Questionnaire_id instead of ProjectID
        sqlQueryQ = "Questionnaire_id = '%s'"%PId

        deleteSQLRows(DB.questionnaire,sqlQueryQ)
        deleteSQLRows(DB.sproject,sqlQuery)
        deleteSQLRows(DB.salternatives,sqlQuery)
                   
        deleteSQLRows(DB.cgeneraldata,sqlQueryQ)

        deleteSQLRows(DB.qbuildings,sqlQueryQ)
        deleteSQLRows(DB.qdistributionhc,sqlQueryQ)
        deleteSQLRows(DB.qelectricity,sqlQueryQ)
        deleteSQLRows(DB.qfuel,sqlQueryQ)
        deleteSQLRows(DB.qgenerationhc,sqlQueryQ)
        deleteSQLRows(DB.qheatexchanger,sqlQuery)
        deleteSQLRows(DB.qprocessdata,sqlQueryQ)
        deleteSQLRows(DB.qproduct,sqlQueryQ)
        deleteSQLRows(DB.qrenewables,sqlQueryQ)
        deleteSQLRows(DB.qwasteheatelequip,sqlQuery)
        deleteSQLRows(DB.uheatpump,sqlQueryQ)

#..............................................................................
# book-keeping: reduce number of alernatives in the system

        self.setActiveProject(-1)

        Status.SQL.commit()


#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
# OTHER SET-UP FUNCTIONS
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------
    def getLastToolSettings(self):
#------------------------------------------------------------------------------

        stool = Status.DB.stool.STool_ID[1][0]
        Status.PId = stool.ActiveProject
        logTrack("New session of tool starting with ProjectID %s"%Status.PId)

        Status.UserType = stool.UserType
        Status.Auditor_ID = stool.Auditor_ID
        Status.UserInteractionLevel = stool.UserInteractionLevel
        Status.LanguageTool = stool.LanguageTool
        Status.UnitsTool = stool.UnitsTool
        
#------------------------------------------------------------------------------
    def setUserInteractionLevel(self,level):
#------------------------------------------------------------------------------
        
        if level in INTERACTIONLEVELS:
            Status.UserInteractionLevel = level
            Status.DB.stool.STool_ID[1][0].UserInteractionLevel = level
            print "Project (setUserInteractionLevel): ",level
        else:
            print "Project (setUserInteractionLevel): ERROR in level ",level

#------------------------------------------------------------------------------
    def deleteProduct(self,productName):
#------------------------------------------------------------------------------
#   deletes all entries for the original ANo
#------------------------------------------------------------------------------

        print "Project (deleteProduct) - project %s, alternative %s, deleting product %s "%(Status.PId,Status.ANo,productName)

#..............................................................................
# deleting Q- and corresponding C-Tables

        DB = Status.DB
        sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' AND Product = '%s'"\
                    %(Status.PId,Status.ANo,productName)

        deleteSQLRows(DB.qproduct,sqlQueryQ)

#------------------------------------------------------------------------------
    def addFuelDummy(self):
#------------------------------------------------------------------------------
#   deletes all entries for the original ANo
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        fuels = Status.DB.qfuel.sql_select(sqlQuery)
        NFuels = len(fuels)
        tmp = {
            "Questionnaire_id":Status.PId,
            "AlternativeProposalNo":Status.ANo,
            "FuelNo": NFuels+1
            }          
        newID = Status.DB.qfuel.insert(tmp)

        NFuels += 1

        generaldata = Status.DB.cgeneraldata.sql_select(sqlQuery)
        generaldata[0].Nfuels = NFuels

        Status.SQL.commit()

        return newID

#------------------------------------------------------------------------------
    def deleteFuel(self,DBFuel_id):
#------------------------------------------------------------------------------
#   deletes all entries for a given fuel type
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        DB = Status.DB
        sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' AND DBFuel_id = '%s'"\
                    %(Status.PId,Status.ANo,DBFuel_id)

        deleteSQLRows(DB.qfuel,sqlQueryQ)

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY FuelNo ASC"%(Status.PId,Status.ANo)
        fuels = Status.DB.qfuel.sql_select(sqlQuery)

        for i in range(len(fuels)): #assign new EqNo in QGenerationHC table
            fuels[i].FuelNo = i+1

        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        generaldata = Status.DB.cgeneraldata.sql_select(sqlQuery)
        generaldata[0].Nfuels = len(fuels)

        Status.SQL.commit()

#------------------------------------------------------------------------------
    def addProcessDummy(self):
#------------------------------------------------------------------------------
#   deletes all entries for the original ANo
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)

        processes = Status.DB.qprocessdata.sql_select(sqlQuery)
        NThProc = len(processes)
        tmp = {
            "Questionnaire_id":Status.PId,
            "AlternativeProposalNo":Status.ANo,
            "ProcNo": NThProc+1
            }          
        newID = Status.DB.qprocessdata.insert(tmp)

        NThProc += 1

        generaldata = Status.DB.cgeneraldata.sql_select(sqlQuery)
        generaldata[0].NThProc = NThProc

        Status.SQL.commit()

        return newID

#------------------------------------------------------------------------------
    def deleteProcess(self,processID):
#------------------------------------------------------------------------------
#   deletes all entries for a given fuel type
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        DB = Status.DB
        sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' AND QProcessData_ID = '%s'"\
                    %(Status.PId,Status.ANo,processID)  #query is redundant, but maintained as is for security

        deleteSQLRows(DB.qprocessdata,sqlQueryQ)

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY ProcNo ASC"%(Status.PId,Status.ANo)
        processes = Status.DB.qprocessdata.sql_select(sqlQuery)

        for i in range(len(processes)): #assign new EqNo in QGenerationHC table
            processes[i].ProcNo = i+1

        
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        generaldata = Status.DB.cgeneraldata.sql_select(sqlQuery)
        generaldata[0].NThProc = len(processes)

        Status.SQL.commit()

#------------------------------------------------------------------------------
    def addPipeDummy(self):
#------------------------------------------------------------------------------
#   adds a new empty pipe field in table qdistributionhc
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)

        pipes = Status.DB.qdistributionhc.sql_select(sqlQuery)
        NPipes = len(pipes)
        tmp = {
            "Questionnaire_id":Status.PId,
            "AlternativeProposalNo":Status.ANo,
            "PipeDuctNo": NPipes+1
            }          
        newID = Status.DB.qdistributionhc.insert(tmp)

        NPipes += 1

        cgeneraldata = Status.DB.cgeneraldata.sql_select(sqlQuery)
        cgeneraldata[0].NPipeDuct = NPipes

        Status.SQL.commit()

        return newID

#------------------------------------------------------------------------------
    def deletePipe(self,pipeID):
#------------------------------------------------------------------------------
#   deletes all entries for a given fuel type
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        DB = Status.DB
        sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' AND QDistributionHC_ID = '%s'"\
                    %(Status.PId,Status.ANo,pipeID)  #query is redundant, but maintained as is for security

        deleteSQLRows(DB.qdistributionhc,sqlQueryQ)

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY PipeDuctNo ASC"%(Status.PId,Status.ANo)
        pipes = Status.DB.qdistributionhc.sql_select(sqlQuery)

        for i in range(len(pipes)): #assign new EqNo in QGenerationHC table
            pipes[i].PipeDuctNo = i+1
            pass

        
        sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)  
        cgeneraldata = Status.DB.cgeneraldata.sql_select(sqlQueryQ)
        cgeneraldata[0].NPipeDuct = len(pipes)

        Status.SQL.commit()

#==============================================================================
#------------------------------------------------------------------------------
    def addBuildingDummy(self):
#------------------------------------------------------------------------------
#   deletes all entries for the original ANo
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)

        buildings = Status.DB.qbuildings.sql_select(sqlQuery)
        NBuildings = len(buildings)
        tmp = {
            "Questionnaire_id":Status.PId,
            "AlternativeProposalNo":Status.ANo,
#            "BuildingNo": NBuildings+1
            }          
        newID = Status.DB.qbuildings.insert(tmp)

        NBuildings += 1

        sqlQuery = "Questionnaire_id = '%s'"%(Status.PId)
        questionnaire = Status.DB.questionnaire.sql_select(sqlQuery)
        questionnaire[0].NBuild = NBuildings

        Status.SQL.commit()

        return newID

#------------------------------------------------------------------------------
    def deleteBuilding(self,buildingID):
#------------------------------------------------------------------------------
#   deletes all entries for a given fuel type
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        DB = Status.DB
        sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' AND QBuildings_ID = '%s'"\
                    %(Status.PId,Status.ANo,buildingID)  #query is redundant, but maintained as is for security

        print "Project (deleteBuilding): query"
        print sqlQueryQ
        
        deleteSQLRows(DB.qbuildings,sqlQueryQ)

#        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY BuildingNo ASC"%(Status.PId,Status.ANo)
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)
        buildings = Status.DB.qbuildings.sql_select(sqlQuery)

        for i in range(len(buildings)): #assign new EqNo in QGenerationHC table
#            buildings[i].BuildingNo = i+1
            pass

        
        sqlQuery = "Questionnaire_id = '%s'"%(Status.PId)
        questionnaire = Status.DB.questionnaire.sql_select(sqlQuery)
        questionnaire[0].NBuild = len(buildings)

        Status.SQL.commit()

#------------------------------------------------------------------------------
    def addHXDummy(self):
#------------------------------------------------------------------------------
#   adds a new empty HX field in table qgenerationhc
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)

        hxes = Status.DB.qheatexchanger.sql_select(sqlQuery)
        NHX = len(hxes)
        tmp = {
            "ProjectID":Status.PId,
            "AlternativeProposalNo":Status.ANo,
            "HXNo": NHX+1
            }          
        newID = Status.DB.qheatexchanger.insert(tmp)
        newhx = Status.DB.qheatexchanger.QHeatExchanger_ID[newID]

        NHX += 1

        cgeneraldata = Status.DB.cgeneraldata.sql_select(sqlQuery)
        cgeneraldata[0].NHX = NHX

        Status.SQL.commit()

        return newhx

#------------------------------------------------------------------------------
    def deleteHX(self,HXID):
#------------------------------------------------------------------------------
#   deletes all entries for a given heat exchanger
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        DB = Status.DB
        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s' AND QHeatExchanger_ID = '%s'"\
                    %(Status.PId,Status.ANo,HXID)  #query is redundant, but maintained as is for security

        deleteSQLRows(DB.qheatexchanger,sqlQuery)

        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s' ORDER BY HXNo ASC"%(Status.PId,Status.ANo)
        hxes = Status.DB.qheatexchanger.sql_select(sqlQuery)

        for i in range(len(hxes)): #assign new EqNo in QGenerationHC table
            hxes[i].HXNo = i+1
            pass

        
        sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)  
        cgeneraldata = Status.DB.cgeneraldata.sql_select(sqlQueryQ)
        cgeneraldata[0].NHX = len(hxes)

        Status.SQL.commit()

#------------------------------------------------------------------------------
    def getHXList(self,key):
#------------------------------------------------------------------------------
#   returns a list of existing heat exchangers
#------------------------------------------------------------------------------

        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s' ORDER BY HXNo ASC"%(Status.PId,Status.ANo)
        hxes = Status.DB.qheatexchanger.sql_select(sqlQuery)
        
        HXList = []
        for hx in hxes:
            HXList.append(hx[key])

        return HXList

#------------------------------------------------------------------------------
    def addWHEEDummy(self):
#------------------------------------------------------------------------------
#   adds a new empty WHEE field in table qwasteheatelequip
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)

        whees = Status.DB.qwasteheatelequip.sql_select(sqlQuery)
        NWHEE = len(whees)
        tmp = {
            "ProjectID":Status.PId,
            "AlternativeProposalNo":Status.ANo,
            "WHEENo": NWHEE+1
            }          
        newID = Status.DB.qwasteheatelequip.insert(tmp)
        newwhee = Status.DB.qwasteheatelequip.QWasteHeatElEquip_ID[newID]

        NWHEE += 1

        cgeneraldata = Status.DB.cgeneraldata.sql_select(sqlQuery)
        cgeneraldata[0].NWHEE = NWHEE

        Status.SQL.commit()

        return newwhee

#------------------------------------------------------------------------------
    def deleteWHEE(self,WHEEID):
#------------------------------------------------------------------------------
#   deletes all entries for a given heat exchanger
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        DB = Status.DB
        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s' AND QWasteHeatElEquip_ID = '%s'"\
                    %(Status.PId,Status.ANo,WHEEID)  #query is redundant, but maintained as is for security

        deleteSQLRows(DB.qwasteheatelequip,sqlQuery)

        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s' ORDER BY WHEENo ASC"%(Status.PId,Status.ANo)
        whees = Status.DB.qwasteheatelequip.sql_select(sqlQuery)

        for i in range(len(whees)): #assign new EqNo in QGenerationHC table
            whees[i].WHEENo = i+1
            pass

        
        sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)  
        cgeneraldata = Status.DB.cgeneraldata.sql_select(sqlQueryQ)
        cgeneraldata[0].NWHEE = len(whees)

        Status.SQL.commit()

#------------------------------------------------------------------------------
    def getWHEEList(self,key):
#------------------------------------------------------------------------------
#   returns a list of existing heat exchangers
#------------------------------------------------------------------------------

        sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s' ORDER BY WHEENo ASC"%(Status.PId,Status.ANo)
        whees = Status.DB.qwasteheatelequip.sql_select(sqlQuery)
        
        WHEEList = []
        for whee in whees:
            WHEEList.append(whee[key])

        return WHEEList

#------------------------------------------------------------------------------
    def deleteEquipment(self,eqID):
#------------------------------------------------------------------------------
#   deletes all entries for a given equipment
#------------------------------------------------------------------------------

#..............................................................................
# deleting Q- and corresponding C-Tables

        DB = Status.DB
        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' AND QGenerationHC_ID = '%s'"\
                    %(Status.PId,Status.ANo,eqID)  #query is redundant, but maintained as is for security

        deleteSQLRows(DB.qgenerationhc,sqlQuery)

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY EqNo ASC"%(Status.PId,Status.ANo)
        equipes = Status.DB.qgenerationhc.sql_select(sqlQuery)

        for i in range(len(equipes)): #assign new EqNo in QGenerationHC table
            equipes[i].EqNo = i+1
            pass

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY CascadeIndex ASC"%(Status.PId,Status.ANo)
        equipes = Status.DB.qgenerationhc.sql_select(sqlQuery)

        for i in range(len(equipes)): #assign new EqNo in QGenerationHC table
            equipes[i].CascadeIndex = i+1
            pass
        
        sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,Status.ANo)  
        cgeneraldata = Status.DB.cgeneraldata.sql_select(sqlQueryQ)
        cgeneraldata[0].NEquipe = len(equipes)

        Status.SQL.commit()

#------------------------------------------------------------------------------
    def getEqList(self,key):
#------------------------------------------------------------------------------
#   returns a list of existing heat exchangers
#------------------------------------------------------------------------------

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY EqNo ASC"%(Status.PId,Status.ANo)
        eqs = Status.DB.qgenerationhc.sql_select(sqlQuery)
        
        eqList = []
        for eq in eqs:
            eqList.append(eq[key])

        return eqList

#------------------------------------------------------------------------------
    def getProcessList(self,key):
#------------------------------------------------------------------------------
#   returns a list of existing heat exchangers
#------------------------------------------------------------------------------

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY ProcNo ASC"%(Status.PId,Status.ANo)
        processes = Status.DB.qprocessdata.sql_select(sqlQuery)
        
        processList = []
        for process in processes:
            processList.append(process[key])

        return processList

#------------------------------------------------------------------------------
    def getPipeList(self,key):
#------------------------------------------------------------------------------
#   returns a list of existing heat exchangers
#------------------------------------------------------------------------------

        sqlQuery = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s' ORDER BY PipeDuctNo ASC"%(Status.PId,Status.ANo)
        pipes = Status.DB.qdistributionhc.sql_select(sqlQuery)
        
        pipeList = []
        for pipe in pipes:
            pipeList.append(pipe[key])

        return pipeList

#==============================================================================

