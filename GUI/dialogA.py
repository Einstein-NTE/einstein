#Boa:Dialog:DialogA
#	Last revised by:    
#                           Stoyan Danov        19/06/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes in last update:
#       19/06/2008 SD: change to translatable text _(...)
#       13/10/2008: SD  change _() to _U()

import wx

def _U(text):
    return unicode(_(text),"utf-8")

def create(parent):
    return DialogA(parent)

[wxID_DIALOGA, wxID_DIALOGABUTTONCANCEL, wxID_DIALOGABUTTONOK, 
 wxID_DIALOGASTDESCRIPTION, wxID_DIALOGASTDIALOG1, wxID_DIALOGATCDESCRIPTION, 
 wxID_DIALOGATCSHORTNAME, 
] = [wx.NewId() for _init_ctrls in range(7)]

class DialogA(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOGA, name='DialogA', parent=prnt,
              pos=wx.Point(433, 283), size=wx.Size(400, 188),
              style=wx.DEFAULT_DIALOG_STYLE, title=_U('New alternative proposal'))
        self.SetClientSize(wx.Size(392, 154))

        self.stDialog1 = wx.StaticText(id=wxID_DIALOGASTDIALOG1,
              label=_U('shortname:'), name='stDialog1', parent=self,
              pos=wx.Point(24, 16), size=wx.Size(56, 13), style=0)
        self.stDialog1.Center(wx.HORIZONTAL)

        self.buttonOK = wx.Button(id=wxID_DIALOGABUTTONOK, label=_U('OK'),
              name='buttonOK', parent=self, pos=wx.Point(176, 112),
              size=wx.Size(91, 23), style=0)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOKButton,
              id=wxID_DIALOGABUTTONOK)

        self.buttonCancel = wx.Button(id=wxID_DIALOGABUTTONCANCEL,
              label=_U('cancel'), name='buttonCancel', parent=self,
              pos=wx.Point(280, 112), size=wx.Size(91, 23), style=0)
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.OnButtonCancelButton,
              id=wxID_DIALOGABUTTONCANCEL)

        self.stDescription = wx.StaticText(id=wxID_DIALOGASTDESCRIPTION,
              label=_U('description:'), name='stDescription', parent=self,
              pos=wx.Point(24, 40), size=wx.Size(57, 13), style=0)
        self.stDescription.Center(wx.HORIZONTAL)

        self.tcShortName = wx.TextCtrl(id=wxID_DIALOGATCSHORTNAME,
              name='tcShortName', parent=self, pos=wx.Point(96, 16),
              size=wx.Size(280, 16), style=0, value=_U('new alternative'))

        self.tcDescription = wx.TextCtrl(id=wxID_DIALOGATCDESCRIPTION,
              name='tcDescription', parent=self, pos=wx.Point(96, 40),
              size=wx.Size(280, 56), style=0,
              value=_U('describe briefly the new alternative'))

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
        self.EndModal(wx.ID_CANCEL)
