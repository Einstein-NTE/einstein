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
#	Version No.: 0.08
#	Created by: 	    Tom Sobota	April 2008
#       Revised by:         Hans Schweiger  12/04/2008
#                           Hans Schweiger  17/04/2008
#                           Tom Sobota      21/04/2008
#                           Tom Sobota      06/05/2008
#                           Stoyan Danov    18/06/2008
#                           Hans Schweiger  01/07/2008
#                           Hans Schweiger  16/09/2008
#
#       Changes to previous version:
#       12/04/08:       Link to functions in Project (open project)
#                       all searches in SQL passed to functions of class Project
#       17/04/08: HS    Adaptation to changes in module Project.
#       18/04/08: HS    Update of panelInfo included
#       21/04/08  TS    Separated NewProject from the button, so it can be called also from main.
#                       set 1st item from listbox as selected initially
#       06/05/08  TS    Put a Hide at the gui setup start, to avoid visual "effects"
#       18/06/2008 SD: change to translatable text _(...)
#       01/07/2008: HS  Change of lay-out; introduction of auto-run button and field
#                       for industry description
#       16/09/2008: HS  Call to panelinfo.update/showMainMenuAlternatives added in
#                       Delete and Copy 
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
import einstein.modules.control as control
from GUITools import *

def _U(text):
    return unicode(_(text),"utf-8")

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
        
#..............................................................................
# Description of selected industry

        self.box1 = wx.StaticBox(id=-1,
              label=_U('Projects in the database'),
              name='box1', parent=self, pos=wx.Point(10, 10),
              size=wx.Size(780, 380), style=0)
        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))


        self.listBoxProjects = wx.ListBox(id=-1,
					       choices=[],
					       name='listBoxProjects',
					       parent=self,
					       pos=wx.Point(20, 40),
					       size=wx.Size(400, 340),
					       style=wx.LB_SINGLE|wx.LB_SORT)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListBoxProjectsDclick, self.listBoxProjects)


        self.buttonOpenProject = wx.Button(id=-1,
						 label=_U('open project'),
						 name='buttonOpenProject',
						 parent=self,
						 pos=wx.Point(450, 40),
						 size=wx.Size(230, 32),
						 style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonOpenProject, self.buttonOpenProject)


        self.buttonCopyProject = wx.Button(id=-1,
						 label=_U('copy project'),
						 name='buttonCopyProject',
						 parent=self,
						 pos=wx.Point(450, 100),
						 size=wx.Size(230, 32),
						 style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonCopyProject, self.buttonCopyProject)


        self.buttonNewProject = wx.Button(id=-1,
						label=_U('new project'),
						name='buttonNewProject',
						parent=self,
						pos=wx.Point(450, 160),
						size=wx.Size(230, 32),
						style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonNewProject, self.buttonNewProject)


        self.buttonDeleteProject = wx.Button(id=-1,
						   label=_U('delete project'),
						   name='buttonDeleteProject',
						   parent=self,
						   pos=wx.Point(450, 220),
						   size=wx.Size(230, 32),
						   style=0)        
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteProject, self.buttonDeleteProject)

#..............................................................................
# Description of selected industry

        self.box2 = wx.StaticBox(id=-1,
              label=_U('Selected project'),
              name='box1', parent=self, pos=wx.Point(10, 410),
              size=wx.Size(780, 160), style=0)
        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.tc1 = wx.TextCtrl(id=-1, name='tc1',
              parent=self, pos=wx.Point(20, 440), size=wx.Size(400, 20), value="")

        self.tc2 = wx.TextCtrl(id=-1, name='tc2',
              parent=self, pos=wx.Point(20, 480), size=wx.Size(400, 80),
                               style=wx.TE_MULTILINE | wx.TE_LINEWRAP, value="")

        self.buttonAutoRun = wx.Button(id=-1,
						 label=_U('run EINSTEIN audit procedure'),
						 name='buttonOpenProject',
						 parent=self,
						 pos=wx.Point(450, 440),
						 size=wx.Size(230, 32),
						 style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAutoRun, self.buttonAutoRun)


        
#------------------------------------------------------------------------------
#--- Display function
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   double click also opens a new Project
#------------------------------------------------------------------------------		
        self.fillPage()

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
        self.NewProject()

#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
    def OnButtonCopyProject(self, event):
#------------------------------------------------------------------------------		
#   copies a project
#------------------------------------------------------------------------------		

        projectName = self.listBoxProjects.GetStringSelection()
        self.shortName = projectName+_U("(copy)")
        self.description = _U("new project copied from ")+projectName
        
        pu1 =  DialogP(self)
        if pu1.ShowModal() == wx.ID_OK:
            logTrack("PanelP - OK %r %r"%(self.shortName,self.description))

            Status.prj.createNewProject(-1,self.shortName,self.description,originalName=projectName)
            self.main.panelinfo.update()
            self.main.showMainMenuAlternatives()
            self.display()

#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
    def OnButtonOpenProject(self, event):
#------------------------------------------------------------------------------		
#   opens an existing Project
#------------------------------------------------------------------------------		
        projectName = self.listBoxProjects.GetStringSelection()
        Status.prj.setActiveProject(-1,name=projectName)
        #TS2008/05/17 two following lines interchanged
        #(after SelectItem is executed,this panel gets destroyed,
        # so the next line would bomb because self doesn't exist any more)
        self.main.panelinfo.update()
        self.main.showMainMenuAlternatives()
        self.fillPage()
        if Status.StatusCC <=0:
            pass
#            self.main.tree.SelectItem(self.main.qPage1, select=True)
        elif Status.ANo > 0:
            self.main.tree.SelectItem(self.main.qA,select=True)

#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
    def OnButtonDeleteProject(self, event):
#------------------------------------------------------------------------------		
        projectName = self.listBoxProjects.GetStringSelection()
        if self.main.askConfirmation(_U('Delete project %r ?') % (projectName,)) == wx.ID_YES:
            logTrack("PanelQ0 (ButtonDelete): deleting %r"%projectName)
            Status.prj.deleteProject(-1,name=projectName)
            self.main.panelinfo.update()
            self.main.showMainMenuAlternatives()
            self.display()
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
    def OnButtonAutoRun(self, event):
#------------------------------------------------------------------------------		
        self.main.showInfo("EINSTEIN - thermal energy audit at the speed of the light\n"+\
                           "fasten your seat belt. put your seats in upright position\n"
                           "ready for take off ?")
        control.autoRun(self)
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

    def NewProject(self):
        self.shortName = _U("New Project")
        self.description = _U("give here a short description of your project")
        
        pu1 =  DialogP(self)
        if pu1.ShowModal() == wx.ID_OK:
            logTrack("PanelP - OK %r %r"%(self.shortName,self.description))

            Status.prj.createNewProject(-1,self.shortName,self.description)
            self.fillPage()

    def SetProjectList(self,projectList):
        self.listBoxProjects.Clear()
        for n in projectList:
            self.listBoxProjects.Append(n)
        self.listBoxProjects.SetSelection(0)

    def clear(self):
        self.listBoxProjects.Clear()


    def fillPage(self):
	self.SetProjectList(Status.prj.getProjectList())
	try: self.listBoxProjects.SetStringSelection(Status.ActiveProjectName)
	except: pass
        self.main.panelinfo.update()
        self.tc1.SetValue(Status.ActiveProjectName)
        self.tc2.SetValue(Status.ActiveProjectDescription)

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
