#Boa:Dialog:DialogP

import wx

def create(parent):
    return DialogP(parent)

[wxID_DIALOGP, wxID_DIALOGPBUTTONCANCEL, wxID_DIALOGPBUTTONOK, 
 wxID_DIALOGPSTDESCRIPTION, wxID_DIALOGPSTDIALOG1, wxID_DIALOGPTCDESCRIPTION, 
 wxID_DIALOGPTCSHORTNAME, 
] = [wx.NewId() for _init_ctrls in range(7)]

class DialogP(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOGP, name='DialogP', parent=prnt,
              pos=wx.Point(433, 283), size=wx.Size(400, 188),
              style=wx.DEFAULT_DIALOG_STYLE, title='New project')
        self.SetClientSize(wx.Size(392, 154))

        self.stDialog1 = wx.StaticText(id=wxID_DIALOGPSTDIALOG1,
              label='shortname:', name='stDialog1', parent=self,
              pos=wx.Point(24, 16), size=wx.Size(56, 13), style=0)
        self.stDialog1.Center(wx.HORIZONTAL)

        self.buttonOK = wx.Button(id=wxID_DIALOGPBUTTONOK, label='OK',
              name='buttonOK', parent=self, pos=wx.Point(176, 112),
              size=wx.Size(91, 23), style=0)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOKButton,
              id=wxID_DIALOGPBUTTONOK)

        self.buttonCancel = wx.Button(id=wxID_DIALOGPBUTTONCANCEL,
              label='cancel', name='buttonCancel', parent=self,
              pos=wx.Point(280, 112), size=wx.Size(91, 23), style=0)
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.OnButtonCancelButton,
              id=wxID_DIALOGPBUTTONCANCEL)

        self.stDescription = wx.StaticText(id=wxID_DIALOGPSTDESCRIPTION,
              label='description:', name='stDescription', parent=self,
              pos=wx.Point(24, 40), size=wx.Size(57, 13), style=0)
        self.stDescription.Center(wx.HORIZONTAL)

        self.tcShortName = wx.TextCtrl(id=wxID_DIALOGPTCSHORTNAME,
              name='tcShortName', parent=self, pos=wx.Point(96, 16),
              size=wx.Size(280, 16), style=0, value='new alternative')

        self.tcDescription = wx.TextCtrl(id=wxID_DIALOGPTCDESCRIPTION,
              name='tcDescription', parent=self, pos=wx.Point(96, 40),
              size=wx.Size(280, 56), style=0,
              value='describe briefly the new alternative')

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.prnt = parent
        self.tcShortName.SetValue(parent.shortName)
        self.tcDescription.SetValue(parent.description)

    def OnButtonOKButton(self, event):
        self.prnt.shortName = self.tcShortName.GetValue()
        self.prnt.description = self.tcDescription.GetValue()
        self.EndModal(wx.ID_OK)

    def OnButtonCancelButton(self, event):
        self.EndModal(wx.Cancel)
