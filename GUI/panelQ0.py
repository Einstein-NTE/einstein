#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	PanelQ0: Tool main page (page 0) -> project selection
#
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Tom Sobota	April 2008
#       Revised by:         Hans Schweiger 12/04/2008
#                           Hans Schweiger 17/04/2008
#
#       Changes to previous version:
#       12/04/08:       Link to functions in Project (open project)
#                       all searches in SQL passed to functions of class Project
#       17/04/08: HS    Adaptation to changes in module Project. 
#
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	http://www.energyxperts.net/
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================

import wx
import pSQL
from status import Status
from dialogP import DialogP

class PanelQ0(wx.Panel):
    def __init__(self, parent, main):
	self.parent = parent
	self.main = main

        self._init_ctrls(parent)

    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Panel.__init__(self, id=-1, name='PanelQ0', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

        self.listBoxProjects = wx.ListBox(id=-1,
					       choices=[],
					       name='listBoxProjects',
					       parent=self,
					       pos=wx.Point(32, 64),
					       size=wx.Size(131, 312),
					       style=0)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListBoxProjectsDclick, self.listBoxProjects)

        self.buttonCopyProject = wx.Button(id=-1,
						 label='copy project',
						 name='buttonCopyProject',
						 parent=self,
						 pos=wx.Point(224,152),
						 size=wx.Size(192, 32),
						 style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonCopyProject, self.buttonCopyProject)


        self.buttonNewProject = wx.Button(id=-1,
						label='new project',
						name='buttonNewProject',
						parent=self,
						pos=wx.Point(224, 192),
						size=wx.Size(192, 32),
						style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonNewProject, self.buttonNewProject)


        self.buttonOpenProject = wx.Button(id=-1,
						 label='open project',
						 name='buttonOpenProject',
						 parent=self,
						 pos=wx.Point(224, 72),
						 size=wx.Size(192, 32),
						 style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonOpenProject, self.buttonOpenProject)


        self.buttonDeleteProject = wx.Button(id=-1,
						   label='delete project',
						   name='buttonDeleteProject',
						   parent=self,
						   pos=wx.Point(224, 272),
						   size=wx.Size(192, 32),
						   style=0)        
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteProject, self.buttonDeleteProject)


        self.stInfo1 = wx.StaticText(id=-1,
				     label='Project list',
				     name='stInfo1',
				     parent=self,
				     pos=wx.Point(32, 48),
				     style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))



#------------------------------------------------------------------------------
#--- Eventhandlers
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
    def OnListBoxProjectsDclick(self, event):
#------------------------------------------------------------------------------		
#   double click also opens a new Project
#------------------------------------------------------------------------------		
        self.OnButtonOpenProject(event)
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
    def OnButtonNewProject(self, event):
#------------------------------------------------------------------------------		
#   define a new project
#------------------------------------------------------------------------------		
        self.shortName = "New Project"
        self.description = "give here a short description of your project"
        
        pu1 =  DialogP(self)
        if pu1.ShowModal() == wx.ID_OK:
            print "PanelP - OK",self.shortName,self.description
            print "PanelP (GenerateNew-Button): calling function createNewProject"

            Status.prj.createNewProject(-1,self.shortName,self.description)
            self.fillPage()

        elif pu1.ShowModal() == wx.ID_Cancel:
            print "PanelP - Cancel"
        else:
            print "PanelP ???"

#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
    def OnButtonCopyProject(self, event):
#------------------------------------------------------------------------------		
#   copies a project
#------------------------------------------------------------------------------		

        projectName = self.listBoxProjects.GetStringSelection()
        self.shortName = projectName+"(copy)"
        self.description = "new project copied from "+projectName
        
        pu1 =  DialogP(self)
        if pu1.ShowModal() == wx.ID_OK:
            print "PanelP - OK",self.shortName,self.description
            print "PanelP (GenerateNew-Button): calling function createNewProject"

            Status.prj.createNewProject(-1,self.shortName,self.description,originalName=projectName)
            self.fillPage()

        elif pu1.ShowModal() == wx.ID_Cancel:
            print "PanelP - Cancel"
        else:
            print "PanelP ???"

#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
    def OnButtonOpenProject(self, event):
#------------------------------------------------------------------------------		
#   opens an existing Project
#------------------------------------------------------------------------------		
        projectName = self.listBoxProjects.GetStringSelection()
        Status.prj.setActiveProject(-1,name=projectName)
        self.main.tree.SelectItem(self.main.qPage1, select=True)
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
    def OnButtonDeleteProject(self, event):
#------------------------------------------------------------------------------		
        projectName = self.listBoxProjects.GetStringSelection()
        print "PanelQ0 (ButtonDelete): deleting ",projectName
        Status.prj.deleteProject(-1,name=projectName)
        self.fillPage()
#------------------------------------------------------------------------------		


#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

    def SetProjectList(self,projectList):
        self.listBoxProjects.Clear()
        for n in projectList:
            self.listBoxProjects.Append(n)

    def clear(self):
	pass

    def fillPage(self):
	self.SetProjectList(Status.prj.getProjectList())

#==============================================================================

if __name__ == '__main__':
    import pSQL
    import MySQLdb

    DBName = 'einstein'
    Status.SQL = MySQLdb.connect(host='localhost', user='root', passwd='tom.tom', db=DBName)
    Status.DB =  pSQL.pSQL(Status.SQL, DBName)

    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(800, 600), title="Einstein - panelQ0")
    panel = PanelQ0(frame, None)

    frame.Show(True)
    app.MainLoop()
