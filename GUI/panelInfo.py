import wx

ASSISTANTLIST = ['Interactive','Semi-automatic','Automatic']

class PanelInfo(wx.StatusBar):
    def __init__(self, parent, main, name='', project=''):
	self.main = main
	self.parent = parent
	self.main = main

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.StatusBar.__init__(self, id=-1, name='PanelInfo', parent=parent, style=wx.SUNKEN_BORDER)
	self.SetFieldsCount(3)
        self.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD, False, 'Times Roman'))

	self.SetStatusText('Project',0)
        self.t0 = wx.TextCtrl(id=-1, parent=self,pos=wx.Point(60,0),size=wx.Size(270, 21),
			      value=name, style=wx.TE_READONLY)
        self.t0.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD, False, 'Times Roman'))
	self.t0.Center(direction=wx.VERTICAL)

	self.SetStatusText('Alternative',1)
        self.t1 = wx.TextCtrl(id=-1, parent=self,pos=wx.Point(416, 0),size=wx.Size(260, 21),
			      value=project, style=wx.TE_READONLY)
        self.t1.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD, False, 'Times Roman'))
	self.t1.Center(direction=wx.VERTICAL)

	self.SetStatusText('Design assistant',2)
        self.choiceAssistant = wx.Choice(choices=ASSISTANTLIST,
              id=-1, name='choiceAssistant', parent=self, pos=wx.Point(800, 0),size=wx.Size(200,21))
        self.choiceAssistant.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.BOLD, False, 'Times Roman'))
	self.choiceAssistant.Center(direction=wx.VERTICAL)

        self.Bind(wx.EVT_SIZE, self.OnSize, self)
        self.Bind(wx.EVT_CHOICE, self.OnChoiceAssistant, self.choiceAssistant)


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
	self.main.logWarning('Design assistant changed to '+repr(ASSISTANTLIST[i]))
        event.Skip()

    def OnSize(self, event):
	self._szpos(0,self.t0,60)
	self._szpos(1,self.t1,80)
	self._szpos(2,self.choiceAssistant,140)
	#print 'SIZE 0 x=%s y=%s w=%s' % (r.x,r.y,r.width)

if __name__ == '__main__':

    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(800, 600), title="Einstein - panelInfo")
    main = Main(1)
    panel = PanelInfo(frame, main)

    frame.Show(True)
    app.MainLoop()
