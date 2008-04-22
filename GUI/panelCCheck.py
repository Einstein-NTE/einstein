#Boa:FramePanel:PanelCC

import wx
import wx.grid
#import einstein.modules.ccheck.ccheck as CC


[wxID_PANELCC, wxID_PANELCCBUTTONPAGECCHECKBACK, 
 wxID_PANELCCBUTTONPAGECCHECKCANCEL, wxID_PANELCCBUTTONPAGECCHECKFWD, 
 wxID_PANELCCBUTTONPAGECCHECKOK, wxID_PANELCCCALCULATE, 
 wxID_PANELCCCB1PAGECCHECK, wxID_PANELCCCHOICEPAGECCHECK, 
 wxID_PANELCCGRIDPAGECCHECK, wxID_PANELCCST1PAGECCHECK, 
 wxID_PANELCCST2PAGECCHECK,wxID_PANELCCPIC1 
] = [wx.NewId() for _init_ctrls in range(12)]

class PanelCC(wx.Panel):

    def __init__(self, parent, id, pos, size, style, name, sql, db):

        self.sql = sql
        self.db = db
        
        self._init_ctrls(parent)

#        self.CCheck = CC.CCheck()
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELCC, name='PanelCC', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

        self.Calculate = wx.Button(id=wxID_PANELCCCALCULATE,
              label='Run consistency check', name='Calculate', parent=self,
              pos=wx.Point(72, 392), size=wx.Size(552, 64), style=0)
        self.Calculate.Bind(wx.EVT_BUTTON, self.OnCalculateButton,
              id=wxID_PANELCCCALCULATE)

        self.gridpageCCheck = wx.grid.Grid(id=-1, name='gridpageCCheck',
              parent=self, pos=wx.Point(40, 48), size=wx.Size(376, 168),
              style=0)
        self.gridpageCCheck.SetDefaultRowSize(12)
        self.gridpageCCheck.EnableEditing(False)

        self.st1pageCCheck = wx.StaticText(id=-1,
              label='Existing Heat pumps in the HC system',
              name='st1pageCCheck', parent=self, pos=wx.Point(40, 32), style=0)

        self.st2pageCCheck = wx.StaticText(id=-1,
              label='Design assistant options:', name='st2pageCCheck',
              parent=self, pos=wx.Point(40, 272), style=0)
        self.st2pageCCheck.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.cb1pageCCheck = wx.CheckBox(id=-1, label='', name='cb1pageCCheck',
              parent=self, pos=wx.Point(288, 308), size=wx.Size(24, 13),
              style=0)
        self.cb1pageCCheck.SetValue(False)

        self.choicepageCCheck = wx.Choice(choices=["compression", "absorption"],
              id=-1, name='choicepageCCheck', parent=self, pos=wx.Point(288,
              336), size=wx.Size(130, 21), style=0)

        self.buttonpageCCheckOk = wx.Button(id=-1, label='ok',
              name='buttonpageCCheckOk', parent=self, pos=wx.Point(528, 528),
              size=wx.Size(75, 23), style=0)

        self.buttonpageCCheckCancel = wx.Button(id=-1, label='cancel',
              name='buttonpageCCheckCancel', parent=self, pos=wx.Point(616,
              528), size=wx.Size(75, 23), style=0)

        self.buttonpageCCheckFwd = wx.Button(id=wxID_PANELCCBUTTONPAGECCHECKFWD,
              label='>>>', name='buttonpageCCheckFwd', parent=self,
              pos=wx.Point(704, 528), size=wx.Size(75, 23), style=0)
        self.buttonpageCCheckFwd.Bind(wx.EVT_BUTTON,
              self.OnButtonpageCCheckFwdButton,
              id=wxID_PANELCCBUTTONPAGECCHECKFWD)

        self.buttonpageCCheckBack = wx.Button(id=wxID_PANELCCBUTTONPAGECCHECKBACK,
              label='<<<', name='buttonpageCCheckBack', parent=self,
              pos=wx.Point(440, 528), size=wx.Size(75, 23), style=0)
        self.buttonpageCCheckBack.Bind(wx.EVT_BUTTON,
              self.OnButtonpageCCheckBackButton,
              id=wxID_PANELCCBUTTONPAGECCHECKBACK)


#        self.CCheck = CC.CCheck()


    def OnCalculateButton(self, event):

        global DB
        global MySql

        print "running consistency check"
        self.st1pageCCheck.Label = "estoy haciendo maravillas ..."
        ret = self.CCheck.init_industry(self.sql,self.db,1,1)
        ret = self.CCheck.run()
        print "... satisfaction ..."
        
    def OnButtonpageCCheckBackButton(self, event):
        event.Skip()

    def OnButtonpageCCheckFwdButton(self, event):
        event.Skip()


