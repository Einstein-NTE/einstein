#Boa:Dialog:HPPopUp1

#   Last modified by:       Hans Schweiger      02-04-2008
#
#   02/04/2008:     

import wx
from einstein.GUI.DBEditFrame import DBEditFrame

[wxID_HPPOPUP1, wxID_HPPOPUP1BTNACCEPT, wxID_HPPOPUP1BTNCANCEL, 
 wxID_HPPOPUP1BTNENTERMANUALLY, wxID_HPPOPUP1BTNSELECTFROMDATABASE, 
 wxID_HPPOPUP1LISTBOX1, wxID_HPPOPUP1STATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(7)]

class HPPopUp1(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_HPPOPUP1, name=u'HPPopUp1',
              parent=prnt, pos=wx.Point(609, 199), size=wx.Size(529, 447),
              style=wx.DEFAULT_DIALOG_STYLE, title='Add equipment')
        self.SetClientSize(wx.Size(529, 447))

        self.btnSelectFromDatabase = wx.Button(id=wxID_HPPOPUP1BTNSELECTFROMDATABASE,
              label=u'Select from database', name=u'btnSelectFromDatabase',
              parent=self, pos=wx.Point(160, 24), size=wx.Size(192, 32),
              style=0)
        self.btnSelectFromDatabase.Bind(wx.EVT_BUTTON,
              self.OnBtnSelectFromDatabaseButton,
              id=wxID_HPPOPUP1BTNSELECTFROMDATABASE)

        self.btnEnterManually = wx.Button(id=wxID_HPPOPUP1BTNENTERMANUALLY,
              label=u'Enter manually', name=u'btnEnterManually', parent=self,
              pos=wx.Point(160, 64), size=wx.Size(192, 32), style=0)
        self.btnEnterManually.Bind(wx.EVT_BUTTON, self.OnBtnEnterManuallyButton,
              id=wxID_HPPOPUP1BTNENTERMANUALLY)

        self.staticText1 = wx.StaticText(id=wxID_HPPOPUP1STATICTEXT1,
              label=u'Retrieve from previously deleted equipment',
              name='staticText1', parent=self, pos=wx.Point(120, 128),
              size=wx.Size(302, 17), style=0)

        self.listBox1 = wx.ListBox(choices=[], id=wxID_HPPOPUP1LISTBOX1,
              name='listBox1', parent=self, pos=wx.Point(128, 160),
              size=wx.Size(288, 232), style=0)

        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label=u'Cancel',
              name=u'btnCancel', parent=self, pos=wx.Point(206, 408),
              size=wx.Size(104, 32), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_HPPOPUP1BTNCANCEL)

        self.btnAccept = wx.Button(id=wx.ID_OK, label=u'Accept',
              name=u'btnAccept', parent=self, pos=wx.Point(312, 408),
              size=wx.Size(104, 32), style=0)
        self.btnAccept.Bind(wx.EVT_BUTTON, self.OnBtnAcceptButton,
              id=wxID_HPPOPUP1BTNACCEPT)

    def __init__(self, parent):
        self._init_ctrls(parent)

#HS2008-04-02: storing parent for event handlers ...
        
        self.prnt = parent
        # create a list of previously deleted equipment for display
        self.RetrieveDeleted()

    def OnBtnSelectFromDatabaseButton(self, event):
        self.dbe = DBEditFrame(self, 'Title of the frame', 'uheatpump')
        self.dbe.Show()

#   Here the identity of the selected equipment should be delivered, in order
#   to give it back to the panelHP.
        self.DBId = 11
        print "PanelHP PopUp1 (Database button): ",self.DBId
        self.prnt.modHP.setEquipmentFromDB(self.prnt.equipe,self.DBId)
        print "PanelHP PopUp1 (Database button): equipment added to Q/C"
        self.prnt.mode = "DB"
        event.Skip()

    def OnBtnEnterManuallyButton(self, event):

#XXX Tom: here page 4 from the questionnaire should be opened with a pointer
#       to the row for the new equipment.
#       Options of Q4:
#       Equipment type: constrained to heat pumps
#       OpenQ4(self.prnt.equipe)

        self.prnt.mode = "Manual"
        event.Skip()

    def OnBtnCancelButton(self, event):
        print "PanelHP PopUp1 (Accept button) "

        event.Skip()

    def OnBtnAcceptButton(self, event):

        self.prnt.DBId = self.DBId
        print "PanelHP PopUp1 (Accept button) "
        
        event.Skip()

    def RetrieveDeleted(self):
        print 'PanelHP PopUp1 (RetrieveDeleted): not yet implemented'

    
