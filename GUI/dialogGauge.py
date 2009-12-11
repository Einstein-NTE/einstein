#Boa:Dialog:DialogGauge
#	Last revised by:    
#                           Stoyan Danov        19/06/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes in last update:
#       19/06/2008 SD: change to translatable text _(...)
#       13/10/2008: SD  change _() to _U()

import wx

[wxID_DIALOGGAUGE, wxID_STGAUGE, wxID_GAUGE,
] = [wx.NewId() for _init_ctrls in range(3)]

def _U(text):
    return unicode(_(text),"utf-8")

class DialogGauge(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOGGAUGE, name="dialogGauge", parent=None,
              pos=wx.Point(400, 300), size=wx.Size(400, 180),
              style=wx.DEFAULT_DIALOG_STYLE, title=self.title)
        self.SetClientSize(wx.Size(392, 137))

        self.stDialog = wx.StaticText(id=wxID_STGAUGE,
              label=self.message, name='stDialog', parent=self,
              pos=wx.Point(20, 20), size=wx.Size(344, 64), style=0)
        self.stDialog.Center(wx.HORIZONTAL)

        self.gauge1 = wx.Gauge(id=wxID_GAUGE, name='gauge1', parent=self,
              pos=wx.Point(20, 100), range=100, size=wx.Size(360, 20),
              style=wx.GA_HORIZONTAL)


    def __init__(self, parent, title, message):
        self.message = message
        self.title = title
        self._init_ctrls(parent)
        self.update(0)

    def update(self,f):
        if f >= 100:
            self.Destroy()
        else:
            self.stDialog.SetLabel(self.message+"\n(%6.2f percent completed)"%f)
            self.gauge1.SetValue(f)
            self.Show()
            wx.SafeYield()

