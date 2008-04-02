#Boa:Dialog:BBPopUp1

import wx
from einstein.GUI.DBEditFrame import DBEditFrame

[wxID_BBPOPUP1, wxID_BBPOPUP1BTNACCEPT, wxID_BBPOPUP1BTNCANCEL, 
 wxID_BBPOPUP1BTNENTERMANUALLY, wxID_BBPOPUP1BTNSELECTFROMDATABASE, 
 wxID_BBPOPUP1LISTBOX1, wxID_BBPOPUP1STATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(7)]

class BBPopUp1(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_BBPOPUP1, name=u'BBPopUp1',
              parent=prnt, pos=wx.Point(609, 199), size=wx.Size(529, 447),
              style=wx.DEFAULT_DIALOG_STYLE, title='Add equipment')
        self.SetClientSize(wx.Size(529, 447))

        self.btnSelectFromDatabase = wx.Button(id=wxID_BBPOPUP1BTNSELECTFROMDATABASE,
              label=u'Select from database', name=u'btnSelectFromDatabase',
              parent=self, pos=wx.Point(160, 24), size=wx.Size(192, 32),
              style=0)
        self.btnSelectFromDatabase.Bind(wx.EVT_BUTTON,
              self.OnBtnSelectFromDatabaseButton,
              id=wxID_BBPOPUP1BTNSELECTFROMDATABASE)

        self.btnEnterManually = wx.Button(id=wxID_BBPOPUP1BTNENTERMANUALLY,
              label=u'Enter manually', name=u'btnEnterManually', parent=self,
              pos=wx.Point(160, 64), size=wx.Size(192, 32), style=0)
        self.btnEnterManually.Bind(wx.EVT_BUTTON, self.OnBtnEnterManuallyButton,
              id=wxID_BBPOPUP1BTNENTERMANUALLY)

        self.staticText1 = wx.StaticText(id=wxID_BBPOPUP1STATICTEXT1,
              label=u'Retrieve from previously deleted equipment',
              name='staticText1', parent=self, pos=wx.Point(120, 128),
              size=wx.Size(302, 17), style=0)

        self.listBox1 = wx.ListBox(choices=[], id=wxID_BBPOPUP1LISTBOX1,
              name='listBox1', parent=self, pos=wx.Point(128, 160),
              size=wx.Size(288, 232), style=0)

        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label=u'Cancel',
              name=u'btnCancel', parent=self, pos=wx.Point(206, 408),
              size=wx.Size(104, 32), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_BBPOPUP1BTNCANCEL)

        self.btnAccept = wx.Button(id=wx.ID_OK, label=u'Accept',
              name=u'btnAccept', parent=self, pos=wx.Point(312, 408),
              size=wx.Size(104, 32), style=0)
        self.btnAccept.Bind(wx.EVT_BUTTON, self.OnBtnAcceptButton,
              id=wxID_BBPOPUP1BTNACCEPT)

    def __init__(self, parent):
        self._init_ctrls(parent)
        # create a list of previously deleted equipment for display
        self.RetrieveDeleted()

    def OnBtnSelectFromDatabaseButton(self, event):
        self.dbe = DBEditFrame(self, 'Title of the frame', 'uheatpump')
        self.dbe.Show()
        event.Skip()

    def OnBtnEnterManuallyButton(self, event):
        event.Skip()

    def OnBtnCancelButton(self, event):
        event.Skip()

    def OnBtnAcceptButton(self, event):
        event.Skip()

    def RetrieveDeleted(self):
        print 'RetrieveDeleted() not yet implemented'

    
