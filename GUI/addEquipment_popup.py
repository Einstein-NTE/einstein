#Boa:Dialog:AddEquipment_popup

import wx
from einstein.GUI.DBEditFrame import DBEditFrame
from einstein.GUI.panelQ4 import PanelQ4
from einstein.modules.interfaces import Interfaces

[wxID_AEPOPUP1, #wxID_AEPOPUP1BTNACCEPT, wxID_AEPOPUP1BTNCANCEL, 
 wxID_AEPOPUP1BTNENTERMANUALLY, wxID_AEPOPUP1BTNSELECTFROMDATABASE, 
 wxID_AEPOPUP1LISTBOX1, wxID_AEPOPUP1STATICTEXT1, 
] = [wx.NewId() for _init_ctrls in range(5)]

class ManualAddDialog(wx.Dialog):
    def __init__(self, prnt, eqId):
	self.prnt = prnt
        wx.Dialog.__init__(self, id=-1, name=u'ManualAddDialog',
              parent=prnt, pos=wx.Point(0, 0), size=wx.Size(800, 600),
              style=wx.DEFAULT_DIALOG_STYLE, title='Manual equipment add')
	# load the Q4 panel, extracted from main.

#HS2004-04-13 call to p4 changed
	self.p4 = PanelQ4(self, prnt, eqId)
	self.eqId = eqId


class AddEquipment(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_AEPOPUP1, name=u'AEPopUp',
              parent=prnt, pos=wx.Point(609, 199), size=wx.Size(529, 447),
              style=wx.DEFAULT_DIALOG_STYLE, title=self.title)
        self.SetClientSize(wx.Size(529, 447))

        self.btnSelectFromDatabase = wx.Button(id=wxID_AEPOPUP1BTNSELECTFROMDATABASE,
              label=u'Select from database', name=u'btnSelectFromDatabase',
              parent=self, pos=wx.Point(160, 24), size=wx.Size(192, 32),
              style=0)
        self.btnSelectFromDatabase.Bind(wx.EVT_BUTTON,
              self.OnBtnSelectFromDatabaseButton,
              id=wxID_AEPOPUP1BTNSELECTFROMDATABASE)

        self.btnEnterManually = wx.Button(id=wxID_AEPOPUP1BTNENTERMANUALLY,
              label=u'Enter manually', name=u'btnEnterManually', parent=self,
              pos=wx.Point(160, 64), size=wx.Size(192, 32), style=0)
        self.btnEnterManually.Bind(wx.EVT_BUTTON, self.OnBtnEnterManuallyButton,
              id=wxID_AEPOPUP1BTNENTERMANUALLY)

        self.staticText1 = wx.StaticText(id=wxID_AEPOPUP1STATICTEXT1,
              label=u'Retrieve from previously deleted equipment',
              name='staticText1', parent=self, pos=wx.Point(120, 128),
              size=wx.Size(302, 17), style=0)

        self.listBox1 = wx.ListBox(choices=[], id=wxID_AEPOPUP1LISTBOX1,
              name='listBox1', parent=self, pos=wx.Point(128, 160),
              size=wx.Size(288, 232), style=0)

        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label=u'Cancel',
              name=u'btnCancel', parent=self, pos=wx.Point(206, 408),
              size=wx.Size(104, 32), style=0)

        self.btnAccept = wx.Button(id=wx.ID_OK, label=u'OK',
              name=u'btnAccept', parent=self, pos=wx.Point(312, 408),
              size=wx.Size(104, 32), style=0)

    def __init__(self, parent, module, title, tablename, col_returned, can_edit):
	self.module = module
	self.title = title
	self.tablename = tablename
	# the column that would be returned by DBEditFrame
	self.col_returned = col_returned
	self.can_edit = can_edit
#HS2008-04-02: storing parent for event handlers ...
        self.prnt = parent
	self.theId = -1
        self._init_ctrls(parent)

        # create a list of previously deleted equipment for display
        self.RetrieveDeleted()

    def OnBtnSelectFromDatabaseButton(self, event):
        self.dbe = DBEditFrame(self, self.title, self.tablename, self.col_returned, self.can_edit)
        if self.dbe.ShowModal() == wx.ID_OK:
	    # the user has accepted a selection from the database dialog
	    # so we exit also from this dialog
	    #
	    #   Here the identity of the selected equipment should be delivered, in order
	    #   to give it back to the calling panel
	    # this should be cleaned somewhat
	    self.theId = self.dbe.theId
	    print "addEquipment popup (Database button): ", self.theId
	    print "addEquipment popup (Database button): equipe = ",self.prnt.equipe.Equipment

	    try:
                print "trying to set equipment row in DB "
		self.module.setEquipmentFromDB(self.prnt.equipe, self.prnt.equipeC, self.theId)
		self.prnt.mode = "DB"
		print "addEquipment popup (Database button): equipment added to Q/C"
	    except:
		print 'setEquipmentFromDB from module did not execute'

	    # close this dialog
	    self.EndModal(wx.ID_OK)

    def OnBtnEnterManuallyButton(self, event):
	#XXX Tom: here page 4 from the questionnaire should be opened with a pointer
	#       to the row for the new equipment.
	#       Options of Q4:
	#       Equipment type: constrained to heat pumps
	#       OpenQ4(self.prnt.equipe)
        self.prnt.mode = "Manual"
	activeQid = 1 # Hans, is this the pointer to the new equipment?
	self.dMan = ManualAddDialog(self, activeQid)
        if self.dMan.ShowModal() == wx.ID_OK:
	    pass

        event.Skip()

    def RetrieveDeleted(self):
        print 'RetrieveDeleted() not yet implemented'

    
