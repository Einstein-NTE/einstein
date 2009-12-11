#Boa:Dialog:DialogOK
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
    return DialogOK(parent)

[wxID_DIALOGOK, wxID_DIALOGOKBUTTONCANCEL, wxID_DIALOGOKBUTTONOK, 
 wxID_DIALOGOKSTDIALOG, 
] = [wx.NewId() for _init_ctrls in range(4)]

class DialogOK(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOGOK, name="dialogA", parent=prnt,
              pos=wx.Point(433, 286), size=wx.Size(400, 171),
              style=wx.DEFAULT_DIALOG_STYLE, title=self.title)
        self.SetClientSize(wx.Size(392, 137))

        self.stDialog = wx.StaticText(id=wxID_DIALOGOKSTDIALOG,
              label=self.message, name='stDialog', parent=self,
              pos=wx.Point(24, 16), size=wx.Size(344, 64), style=0)
        self.stDialog.Center(wx.HORIZONTAL)

        self.buttonOK = wx.Button(id=wxID_DIALOGOKBUTTONOK, label=_U('OK'),
              name='buttonOK', parent=self, pos=wx.Point(176, 96),
              size=wx.Size(91, 23), style=0)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOKButton,
              id=wxID_DIALOGOKBUTTONOK)

        self.buttonCancel = wx.Button(id=wxID_DIALOGOKBUTTONCANCEL,
              label=_U('cancel'), name='buttonCancel', parent=self,
              pos=wx.Point(280, 96), size=wx.Size(91, 23), style=0)
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.OnButtonCancelButton,
              id=wxID_DIALOGOKBUTTONCANCEL)

    def __init__(self, parent, title, message):
        self.message = message
        self.title = title
        self._init_ctrls(parent)

    def OnButtonOKButton(self, event):
        self.EndModal(wx.ID_OK)

    def OnButtonCancelButton(self, event):
        self.EndModal(wx.ID_CANCEL)
