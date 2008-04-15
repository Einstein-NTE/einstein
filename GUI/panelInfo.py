import wx

assistantList = ['Interactive','Semi-automatic','Automatic']

class PanelInfo(wx.Panel):
    def __init__(self, parent, main, name='', project=''):
	self.main = main

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelInfo', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(800, 32), style=0)

        self.SetBackgroundColour ("#909090")

        self.s1 = wx.StaticText(id=-1, label='Project', parent=self, pos=wx.Point(10, 8))
        self.t1 = wx.TextCtrl(id=-1, parent=self,pos=wx.Point(60,4),size=wx.Size(250, 28),
			      value=name)

        self.s2 = wx.StaticText(id=-1, label='Alternative 3', parent=self, pos=wx.Point(320, 8))
        self.t2 = wx.TextCtrl(id=-1, parent=self,pos=wx.Point(420, 4),size=wx.Size(300, 28),
			      value=project)

        self.s3 = wx.StaticText(id=-1, label='Design\nassistant', parent=self, pos=wx.Point(730, 2))
        self.choiceAssistant = wx.Choice(choices=assistantList,
              id=-1, name='choiceAssistant', parent=self, pos=wx.Point(800, 4),size=wx.Size(200,28))

        self.Bind(wx.EVT_CHOICE, self.OnChoiceAssistant, self.choiceAssistant)


#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		

    def OnChoiceAssistant(self, event):
	i = self.choiceAssistant.GetCurrentSelection()
	self.main.logWarning('Design assistant changed to '+repr(assistantList[i]))
        event.Skip()


if __name__ == '__main__':

    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(800, 600), title="Einstein - panelInfo")
    main = Main(1)
    panel = PanelInfo(frame, main)

    frame.Show(True)
    app.MainLoop()
