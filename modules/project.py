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
#	Version No.: 0.03
#
#       Created by:     Hans Schweiger      02/04/2008
#       Revised by:     Hans Schweiger      15/04/2008
#
#       15/04/08: HS    Functions Add-, Copy-, Delete-Alternative
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
# changes one parameter within the row (usually AlternativeNo or ProjectID)

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

    def __init__(self):

        Status.PId = 2 #XXX For testing: start with project No. 2
        print "Project (__init__): set PId to ",Status.PId

        sproject = Status.DB.sproject.ProjectID[Status.PId][0]
        Status.NoOfAlternatives = sproject.NoOfAlternatives
        print "Project (__init__): number of alternatives in the project",Status.NoOfAlternatives
        
        Status.ANo = sproject.ActiveAlternative
        self.setActiveAlternative(0)    #XXX For testing: start with ANo = 0!!!!
        print "Project (__init__): active alternative",Status.ANo

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
        copySQLRows(DB.qgenerationhc,sqlQueryQ,"QGenerationHC_ID","AlternativeProposalNo",ANo)
        copySQLRows(DB.cgenerationhc,sqlQueryQ,"CGenerationHC_ID","AlternativeProposalNo",ANo)

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
        deleteSQLRows(DB.qgenerationhc,sqlQueryQ)
        deleteSQLRows(DB.cgenerationhc,sqlQueryQ)

#..............................................................................
# changing ANos in all rows with ANo higher than the deleted one

        for i in range(ANo+1,Status.NoOfAlternatives+1):
                sqlQuery = "ProjectID = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,i)

        #additional query necessary for old tables who still have Questionnaire_id instead of ProjectID
                sqlQueryQ = "Questionnaire_id = '%s' AND AlternativeProposalNo = '%s'"%(Status.PId,i)

                print "Project (deleteAlternative): shifting row"
                
                shiftANoInSQLRows(DB.salternatives,sqlQuery,-1)
                shiftANoInSQLRows(DB.cgeneraldata,sqlQueryQ,-1)
                shiftANoInSQLRows(DB.qgenerationhc,sqlQueryQ,-1)
                shiftANoInSQLRows(DB.cgenerationhc,sqlQueryQ,-1)


#..............................................................................
# book-keeping: reduce number of alernatives in the system

        Status.NoOfAlternatives -= 1
        ANo = Status.NoOfAlternatives
        self.setActiveAlternative(ANo)

        sproject = Status.DB.sproject.ProjectID[Status.PId][0]
        sproject.NoOfAlternatives = Status.NoOfAlternatives


        Status.SQL.commit()

#------------------------------------------------------------------------------
    def getActiveAlternatives():
#------------------------------------------------------------------------------

        listOfAlternatives = ["present state"]
        for i in range(1,Status.NoOfALternatives+1):
        #XXX get here name of all existing alternatives
            listOfAlternatives.append("???")
        return listOfAlternatives
            
#------------------------------------------------------------------------------
    def setActiveAlternative(self,n):
#------------------------------------------------------------------------------

        if (n>=-1) and n <= Status.NoOfAlternatives:
                Status.ANo = n
                Status.DB.sproject.ProjectID[Status.PId][0].ActiveAlternative = n
                Status.SQL.commit()
                print "Project (setActiveAlternative): ",n
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
    def getProjectList(self):
#------------------------------------------------------------------------------
        projectList = []
        for n in Status.DB.questionnaire.Name["%"]:
            projectList.append(n.Name)
        return projectList


#------------------------------------------------------------------------------
    def setActiveProject(self,name):
#------------------------------------------------------------------------------
        
        Status.PId = Status.DB.questionnaire.Name[name][0].Questionnaire_ID
        Status.ANo = 0

        print "Project (setActiveProject): name = ",name, " PId = ",Status.PId

#------------------------------------------------------------------------------
    def createNewProject(self,copyFrom = None):
#------------------------------------------------------------------------------

        self.newPId = Status.DB.questionnaire.insert({"Name":"new project"})

        if (copyFrom == None):
#XXX init project information with defaults where necessary
#            initProject()
            pass
        else:
            pass
#XXX here all relevant project information should be copied in SQL
#       from PId = copyFrom to newPId
#       all tables Q and C, tables U, ...

        Status.SQL.commit()
        Status.PId = self.newPId

#------------------------------------------------------------------------------
    def deleteProject():
#------------------------------------------------------------------------------
        pass


#------------------------------------------------------------------------------
    def setUserInteractionLevel(self,level):
#------------------------------------------------------------------------------
        levels = ["interactive","semi-automatic","automatic"]
        if level in range(1,4):
            Status.UserInteractionLevel = level
            print "Project (setUserInteractionLevel): ",levels[level-1]
        else:
            print "Project (setUserInteractionLevel): ERROR in level ",level


        
           


    
    

