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
#	Version No.: 0.01
#
#       Created by:     Hans Schweiger      02/04/2008
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

class Project(object):

    def __init__(self):
        pass
#        NoAlternatives = ???

#------------------------------------------------------------------------------
    def createNewAlternative(copyFrom = None):
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
 
        if (copyFrom == None):
#XXX init project information with defaults where necessary
#            initAlternative()
             pass
            
        else:
            pass
#XXX here all relevant project information should be copied in SQL
#       from ANo = copyFrom to newANo
#       all tables Q and C, tables U, ...


#------------------------------------------------------------------------------
    def getActiveAlternatives():
#------------------------------------------------------------------------------

        listOfAlternatives = ["present state"]
        for i in range(1,Status.NoOfALternatives+1):
        #XXX get here name of all existing alternatives
            listOfAlternatives.append("???")
        return listOfAlternatives
            
#------------------------------------------------------------------------------
    def setActiveAlternative(n):
#------------------------------------------------------------------------------

        Status.ANo = n
        print "Project (setActiveAlternative): ",n
        #XXX do here any inicialisation necessary if active alternative is changed
#       Status.ActivePanel.updateDisplay            
            
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
    def deleteAlternative():
#------------------------------------------------------------------------------
        pass
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


        
           


    
    

