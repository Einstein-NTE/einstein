# -*- coding: utf_8 -*-
#   18/04/2008  HS  function "update added" and import of Status added.
#                           Stoyan Danov            18/06/2008
#                           Stoyan Danov    13/10/2008
#       Changes to previous version:
#       18/06/2008 SD: change to translatable text _(...)
#       13/10/2008: SD  change _() to _U()

import wx

from einstein.GUI.status import Status
from einstein.modules.constants import *
ASSISTANTLIST = INTERACTIONLEVELS

def _U(text):
    return unicode(_(text),"utf-8")

class PanelInfo(wx.StatusBar):
    def __init__(self, parent, main):
	self.main = main
	self.parent = parent
	self.main = main
	
	project = Status.ActiveProjectName
	alternative = Status.ActiveAlternativeName
	level = Status.UserInteractionLevel

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.StatusBar.__init__(self, id=-1, name='PanelInfo', parent=parent, style=wx.SUNKEN_BORDER)
	self.SetFieldsCount(3)
        self.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD, False, 'Times Roman'))

	self.SetStatusText(_U('Project'),0)
        self.t0 = wx.TextCtrl(id=-1, parent=self,pos=wx.Point(60,0),size=wx.Size(270, 21),
			      value=project, style=wx.TE_READONLY)
        self.t0.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD, False, 'Times Roman'))
	self.t0.Center(direction=wx.VERTICAL)

	self.SetStatusText(_U('Alternative'),1)
        self.t1 = wx.TextCtrl(id=-1, parent=self,pos=wx.Point(416, 0),size=wx.Size(260, 21),
			      value=alternative, style=wx.TE_READONLY)
        self.t1.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD, False, 'Times Roman'))
	self.t1.Center(direction=wx.VERTICAL)

	self.SetStatusText(_U('Design assistant'),2)
        self.choiceAssistant = wx.Choice(choices=ASSISTANTLIST,
              id=-1, name='choiceAssistant', parent=self, pos=wx.Point(800, 0),size=wx.Size(200,21))
        self.choiceAssistant.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD, False, 'Times Roman'))
	self.choiceAssistant.Center(direction=wx.VERTICAL)

        self.Bind(wx.EVT_SIZE, self.OnSize, self)
        self.Bind(wx.EVT_CHOICE, self.OnChoiceAssistant, self.choiceAssistant)

        self.update()


#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		
    def _szpos(self,index,control,labelwidth):
	rect=self.GetFieldRect(index)
	end = rect.x + rect.width
	p = control.GetPosition()
	sz = control.GetSize()
	sz.width = rect.width-labelwidth
	npos = wx.Point(end-sz.width,p.y)
	control.SetPosition(npos)
	control.SetSize(sz)

    def OnChoiceAssistant(self, event):
	i = self.choiceAssistant.GetCurrentSelection()
	self.main.logWarning(_U('Design assistant changed to ')+repr(ASSISTANTLIST[i]))	
        Status.prj.setUserInteractionLevel(ASSISTANTLIST[i])
        self.main.changeAssistantMainMenu(i)
        if event is not None:
            event.Skip()

    def OnSize(self, event):
	self._szpos(0,self.t0,60)
	self._szpos(1,self.t1,80)
	self._szpos(2,self.choiceAssistant,140)

#------------------------------------------------------------------------------
# public methods
#------------------------------------------------------------------------------
    def update(self):
        self.t0.SetValue(Status.ActiveProjectName)
        self.t1.SetValue(Status.ActiveAlternativeName)
        self.choiceAssistant.SetSelection(ASSISTANTLIST.index(Status.UserInteractionLevel))
       
    def changeAssistant(self,level):
        self.choiceAssistant.SetSelection(level)
        self.OnChoiceAssistant(None)

        
if __name__ == '__main__':

    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(800, 600), title="Einstein - panelInfo")
    main = Main(1)
    panel = PanelInfo(frame, main)

    frame.Show(True)
    app.MainLoop()
