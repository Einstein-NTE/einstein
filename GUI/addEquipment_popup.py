#Boa:Dialog:AddEquipment_popup
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	DBEditFrame
#			
#------------------------------------------------------------------------------
#			
#	Data base editing window
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Tom Sobota	    April 2008
#	Last revised by:    Hans Schweiger      25/04/2008
#                           Stoyan Danov        19/06/2008
#
#       Changes in last update:
#       25/04/08:       preselection added as input
#       19/06/2008 SD: change to translatable text _(...)
#
#------------------------------------------------------------------------------		
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	www.energyxperts.net / info@energyxperts.net
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================

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
              style=wx.DEFAULT_DIALOG_STYLE, title=_('Manual equipment add'))

        print "AddEquipment_popup (ManualAddDialog): eqId = ",eqId
        self.equipeType = None
        
	self.p4 = PanelQ4(self, prnt, eqId)
	self.eqId = eqId
	print _("AddEquipment_popup (ManualAddDialog): new type = "),self.equipeType


class AddEquipment(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_AEPOPUP1, name=u'AEPopUp',
              parent=prnt, pos=wx.Point(609, 199), size=wx.Size(529, 447),
              style=wx.DEFAULT_DIALOG_STYLE, title=self.title)
        self.SetClientSize(wx.Size(529, 447))

        self.btnSelectFromDatabase = wx.Button(id=wxID_AEPOPUP1BTNSELECTFROMDATABASE,
              label=_('Select from database'), name=u'btnSelectFromDatabase',
              parent=self, pos=wx.Point(160, 24), size=wx.Size(192, 32),
              style=0)
        self.btnSelectFromDatabase.Bind(wx.EVT_BUTTON,
              self.OnBtnSelectFromDatabaseButton,
              id=wxID_AEPOPUP1BTNSELECTFROMDATABASE)

        self.btnEnterManually = wx.Button(id=wxID_AEPOPUP1BTNENTERMANUALLY,
              label=_('Enter manually'), name=u'btnEnterManually', parent=self,
              pos=wx.Point(160, 64), size=wx.Size(192, 32), style=0)
        self.btnEnterManually.Bind(wx.EVT_BUTTON, self.OnBtnEnterManuallyButton,
              id=wxID_AEPOPUP1BTNENTERMANUALLY)

        self.staticText1 = wx.StaticText(id=wxID_AEPOPUP1STATICTEXT1,
              label=_('Retrieve from previously deleted equipment'),
              name='staticText1', parent=self, pos=wx.Point(120, 128),
              size=wx.Size(302, 17), style=0)

        self.listBox1 = wx.ListBox(choices=[], id=wxID_AEPOPUP1LISTBOX1,
              name='listBox1', parent=self, pos=wx.Point(128, 160),
              size=wx.Size(288, 232), style=0)

        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label=_('Cancel'),
              name=u'btnCancel', parent=self, pos=wx.Point(206, 408),
              size=wx.Size(104, 32), style=0)

        self.btnAccept = wx.Button(id=wx.ID_OK, label=_('OK'),
              name=u'btnAccept', parent=self, pos=wx.Point(312, 408),
              size=wx.Size(104, 32), style=0)

#------------------------------------------------------------------------------		
    def __init__(self, parent, module, title, tablename, col_returned, can_edit):
#------------------------------------------------------------------------------		
	self.module = module
	self.title = title
	self.tablename = tablename

	# the column that would be returned by DBEditFrame
	self.col_returned = col_returned
	self.can_edit = can_edit

        self.prnt = parent
	self.theId = -1
        self._init_ctrls(parent)

        # create a list of previously deleted equipment for display
#        self.RetrieveDeleted()

#------------------------------------------------------------------------------		
    def OnBtnSelectFromDatabaseButton(self, event):
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
        self.dbe = DBEditFrame(self, self.title, self.tablename, self.col_returned, self.can_edit)
        if self.dbe.ShowModal() == wx.ID_OK:
	    # the user has accepted a selection from the database dialog
	    # so we exit also from this dialog
	    #
	    #   Here the identity of the selected equipment should be delivered, in order
	    #   to give it back to the calling panel
	    # this should be cleaned somewhat
	    self.theId = self.dbe.theId
#	    print "addEquipment popup (Database button): ", self.theId
#	    print "addEquipment popup (Database button): equipe = ",self.prnt.equipe.Equipment

	    try:
#            print "trying to set equipment row in DB "
                self.module.setEquipmentFromDB(self.prnt.equipe, self.theId)
                self.prnt.mode = "DB"
#            print _("addEquipment popup (Database button): equipment added to Q/C")
	    except:
		logTrack('addEquipment popup (Database button): setEquipmentFromDB from module did not execute')

	    # close this dialog
	    self.EndModal(wx.ID_OK)
        else:
            self.EndModal(wx.ID_CANCEL)

#------------------------------------------------------------------------------		
    def OnBtnEnterManuallyButton(self, event):
#------------------------------------------------------------------------------		
#   Manual entry selected
#------------------------------------------------------------------------------		
        self.prnt.mode = "Manual"
        logTrack("AddEquipment_popup (Manual Button): adding equipe ID %s"%(self.prnt.equipe.QGenerationHC_ID))
	self.dMan = ManualAddDialog(self, self.prnt.equipe.QGenerationHC_ID)
        if self.dMan.ShowModal() == wx.ID_OK:
	    self.EndModal(wx.ID_OK)
	else:
            print _("AddEquipment_popup (Manual Button): Cancelled")
            self.EndModal(wx.ID_CANCEL)

#------------------------------------------------------------------------------		
    def RetrieveDeleted(self):
#------------------------------------------------------------------------------		
        print _('RetrieveDeleted() not yet implemented')
#------------------------------------------------------------------------------		

    
