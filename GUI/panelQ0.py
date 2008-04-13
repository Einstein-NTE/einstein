#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	PanelQ0: Questionnaire page 0
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Tom Sobota	April 2008
#       Revised by:         Hans Schweiger 12/04/2008
#
#       Changes to previous version:
#       12/04/08:       Link to functions in Project (open project)
#                       all searches in SQL passed to functions of class Project
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

        self.listBoxQuestionnaires = wx.ListBox(id=-1,
					       choices=[],
					       name='listBoxQuestionnaires',
					       parent=self,
					       pos=wx.Point(32, 64),
					       size=wx.Size(131, 312),
					       style=0)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListBoxQuestionnairesDclick, self.listBoxQuestionnaires)

        self.buttonNewQuestionnaire = wx.Button(id=-1,
						label='new questionnaire',
						name='buttonNewQuestionnaire',
						parent=self,
						pos=wx.Point(224, 72),
						size=wx.Size(192, 32),
						style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonNewQuestionnaire, self.buttonNewQuestionnaire)


        self.buttonOpenQuestionnaire = wx.Button(id=-1,
						 label='open questionnaire',
						 name='buttonOpenQuestionnaire',
						 parent=self,
						 pos=wx.Point(224, 112),
						 size=wx.Size(192, 32),
						 style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonOpenQuestionnaire, self.buttonOpenQuestionnaire)


        self.buttonDeleteQuestionnaire = wx.Button(id=-1,
						   label='delete questionnaire',
						   name='buttonDeleteQuestionnaire',
						   parent=self,
						   pos=wx.Point(224, 152),
						   size=wx.Size(192, 32),
						   style=0)        
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteQuestionnaire, self.buttonDeleteQuestionnaire)


        self.stInfo1 = wx.StaticText(id=-1,
				     label='Questionnaire list',
				     name='stInfo1',
				     parent=self,
				     pos=wx.Point(32, 48),
				     style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))



#------------------------------------------------------------------------------
#--- Eventhandlers
#------------------------------------------------------------------------------		

    def OnListBoxQuestionnairesDclick(self, event):
        projectName = self.listBoxQuestionnaires.GetStringSelection()
        Status.prj.setActiveProject(projectName)
        self.main.tree.SelectItem(self.main.qPage1, select=True)
        event.Skip()

    def OnButtonNewQuestionnaire(self, event):
        event.Skip()

    def OnButtonOpenQuestionnaire(self, event):
        projectName = self.listBoxQuestionnaires.GetStringSelection()
        Status.prj.setActiveProject(projectName)
        self.main.tree.SelectItem(self.main.qPage1, select=True)
#        self.selectQuestionnaire()

    def OnButtonDeleteQuestionnaire(self, event):
        event.Skip()



#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

    def SetProjectList(self,projectList):
        self.listBoxQuestionnaires.Clear()
        for n in projectList:
            self.listBoxQuestionnaires.Append(n)

#HS eliminated, no longer used.
#    def GetID(self):
#	return Status.DB.questionnaire.Name[self.listBoxQuestionnaires.GetStringSelection()][0].Questionnaire_ID


    def clear(self):
	pass

    def fillPage(self):
	self.SetProjectList(Status.prj.getProjectList())


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
