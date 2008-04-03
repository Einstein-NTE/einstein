#Boa:Dialog:APopUp1

import wx
from einstein.GUI.DBEditFrame import DBEditFrame

[wxID_APOPUP1, wxID_APOPUP1BTNACCEPT, wxID_APOPUP1BTNCANCEL, 
 wxID_APOPUP1COPYFROM, wxID_APOPUP1LISTBOX1, wxID_APOPUP1STATICTEXT1, 
 wxID_APOPUP1STATICTEXT2, wxID_APOPUP1STATICTEXT3, wxID_APOPUP1TEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(9)]

class APopUp1(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_APOPUP1, name=u'APopUp1', parent=prnt,
              pos=wx.Point(490, 158), size=wx.Size(537, 332),
              style=wx.DEFAULT_DIALOG_STYLE, title='New alternative')
        self.SetClientSize(wx.Size(529, 298))

        self.staticText1 = wx.StaticText(id=wxID_APOPUP1STATICTEXT1,
              label='Short name of new alternative', name='staticText1',
              parent=self, pos=wx.Point(24, 16), size=wx.Size(147, 13),
              style=0)

        self.listBox1 = wx.ListBox(choices=[], id=wxID_APOPUP1LISTBOX1,
              name='listBox1', parent=self, pos=wx.Point(24, 72),
              size=wx.Size(480, 112), style=0)

        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label=u'Cancel',
              name=u'btnCancel', parent=self, pos=wx.Point(318, 248),
              size=wx.Size(104, 32), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_APOPUP1BTNCANCEL)

        self.btnAccept = wx.Button(id=wx.ID_OK, label=u'Accept',
              name=u'btnAccept', parent=self, pos=wx.Point(200, 248),
              size=wx.Size(104, 32), style=0)
        self.btnAccept.Bind(wx.EVT_BUTTON, self.OnBtnAcceptButton,
              id=wxID_APOPUP1BTNACCEPT)

        self.staticText2 = wx.StaticText(id=wxID_APOPUP1STATICTEXT2,
              label='Copy from:', name='staticText2', parent=self,
              pos=wx.Point(24, 208), size=wx.Size(55, 13), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_APOPUP1TEXTCTRL1, name='textCtrl1',
              parent=self, pos=wx.Point(200, 16), size=wx.Size(304, 24),
              style=0, value='textCtrl1')

        self.CopyFrom = wx.Choice(choices=["Present state",
              "Build from scratch", "Alternative1"], id=wxID_APOPUP1COPYFROM,
              name='CopyFrom', parent=self, pos=wx.Point(200, 208),
              size=wx.Size(304, 21), style=0)

        self.staticText3 = wx.StaticText(id=wxID_APOPUP1STATICTEXT3,
              label='Description', name='staticText3', parent=self,
              pos=wx.Point(24, 48), size=wx.Size(54, 13), style=0)

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

    
