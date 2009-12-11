#Boa:Dialog:DialogP
# v0.02
#
# 21/04/2008 Tom
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
              style=wx.DEFAULT_DIALOG_STYLE, title=_U('New project'))
        self.SetClientSize(wx.Size(392, 154))

        self.stDialog1 = wx.StaticText(id=wxID_DIALOGPSTDIALOG1,
              label=_U('shortname:'), name='stDialog1', parent=self,
              pos=wx.Point(24, 16), size=wx.Size(56, 13), style=0)
        self.stDialog1.Center(wx.HORIZONTAL)

        #TS20080421 changed ID
        self.buttonOK = wx.Button(id=wx.ID_OK, label=_U('OK'),
              name='buttonOK', parent=self, pos=wx.Point(176, 112),
              size=wx.Size(91, 23), style=0)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOKButton,
              id=wx.ID_OK)

        #TS20080421 changed ID. Deleted innecessary bind
        self.buttonCancel = wx.Button(id=wx.ID_CANCEL,
              label=_U('Cancel'), name='buttonCancel', parent=self,
              pos=wx.Point(280, 112), size=wx.Size(91, 23), style=0)

        self.stDescription = wx.StaticText(id=wxID_DIALOGPSTDESCRIPTION,
              label=_U('description:'), name='stDescription', parent=self,
              pos=wx.Point(24, 40), size=wx.Size(57, 13), style=0)
        self.stDescription.Center(wx.HORIZONTAL)

        self.tcShortName = wx.TextCtrl(id=wxID_DIALOGPTCSHORTNAME,
              name='tcShortName', parent=self, pos=wx.Point(96, 16),
              size=wx.Size(280, 21), style=0, value=_U('New alternative'))

        self.tcDescription = wx.TextCtrl(id=wxID_DIALOGPTCDESCRIPTION,
              name='tcDescription', parent=self, pos=wx.Point(96, 40),
              size=wx.Size(280, 64), style=wx.TE_MULTILINE,
              value=_U('Describe briefly the new alternative'))

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.prnt = parent
        self.tcShortName.SetValue(parent.shortName)
        self.tcDescription.SetValue(parent.description)

    def OnButtonOKButton(self, event):
        self.prnt.shortName = self.tcShortName.GetValue()
        self.prnt.description = self.tcDescription.GetValue()
        self.EndModal(wx.ID_OK)
