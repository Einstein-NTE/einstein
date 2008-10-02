#Boa:Dialog:DlgManageUO

import wx
from einstein.GUI.status import *

def create(parent):
    return Dialog1(parent)

[wxID_DLGMANAGEUO, wxID_DLGMANAGEUOBTNADD, wxID_DLGMANAGEUOBTNCHANGE, 
 wxID_DLGMANAGEUOBTNREMOVE, wxID_DLGMANAGEUOLBLIST, wxID_DLGMANAGEUOTCNAME, 
] = [wx.NewId() for _init_ctrls in range(6)]

class DlgManageUO(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGMANAGEUO, name='', parent=prnt,
              pos=wx.Point(414, 71), size=wx.Size(490, 441),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'Manage Unit Operation')
        self.SetClientSize(wx.Size(482, 414))

        self.lbList = wx.ListBox(choices=[], id=wxID_DLGMANAGEUOLBLIST,
              name=u'lbList', parent=self, pos=wx.Point(8, 8), size=wx.Size(376,
              368), style=0)
        self.lbList.Bind(wx.EVT_LISTBOX, self.OnLbListListbox,
              id=wxID_DLGMANAGEUOLBLIST)

        self.tcName = wx.TextCtrl(id=wxID_DLGMANAGEUOTCNAME, name=u'tcName',
              parent=self, pos=wx.Point(8, 384), size=wx.Size(376, 21), style=0,
              value=u'')

        self.btnAdd = wx.Button(id=wxID_DLGMANAGEUOBTNADD, label=u'Add',
              name=u'btnAdd', parent=self, pos=wx.Point(392, 384),
              size=wx.Size(75, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_DLGMANAGEUOBTNADD)

        self.btnRemove = wx.Button(id=wxID_DLGMANAGEUOBTNREMOVE,
              label=u'Remove', name=u'btnRemove', parent=self, pos=wx.Point(392,
              320), size=wx.Size(75, 23), style=0)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.OnBtnRemoveButton,
              id=wxID_DLGMANAGEUOBTNREMOVE)

        self.btnChange = wx.Button(id=wxID_DLGMANAGEUOBTNCHANGE,
              label=u'Change', name=u'btnChange', parent=self, pos=wx.Point(392,
              352), size=wx.Size(75, 23), style=0)
        self.btnChange.Bind(wx.EVT_BUTTON, self.OnBtnChangeButton,
              id=wxID_DLGMANAGEUOBTNCHANGE)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.onUOSelected(False)
        self.updateUos()
    
    def updateUos(self):
        self.loadUO()
        self.lbList.Clear()
        for uo in self.uos:
            self.lbList.Append(uo[1])
    
    def onUOSelected(self,bool):
        self.btnChange.Enabled = bool
        self.btnRemove.Enabled = bool
        
    def loadUO(self):
        query = """SELECT IDUnitOperation,Name FROM poUnitOperation"""
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.uos = results 
        else:
            self.uos = []
    
    def addUO(self,name):
        query = """INSERT INTO poUnitOperation (Name) VALUES (\"%s\")"""
        query = query % name
        Status.DB.sql_query(query)
    
    def deleteUO(self,index):
        uo = self.uos[index]
        
        query = """SEleCT * FROM poSubsector_to_UO WHERE UnitOperationID = %s"""
        query = query % uo[0]
        result = Status.DB.sql_query(query)
                
        if (len(result) == 0):
            query = """DELETE FROM poUnitOperation WHERE IDUnitOperation = %s"""
            query = query % uo[0]
            Status.DB.sql_query(query)
        else:
            wx.MessageBox("Could not delete. Unit Operation in use.")
        
    def changeUO(self,index,name):
        uo = self.uos[index]
        query = """UPDATE poUnitOperation SET Name = \"%s\" WHERE IDUnitOperation = %s"""
        query = query % (name,uo[0])
        Status.DB.sql_query(query)

    def OnLbListListbox(self, event):
        self.uoSelection = self.lbList.GetSelection()
        self.onUOSelected(True)
        event.Skip()

    def OnBtnAddButton(self, event):
        self.addUO(self.tcName.GetValue())
        self.updateUos()
        event.Skip()

    def OnBtnRemoveButton(self, event):
        self.onUOSelected(False)
        self.deleteUO(self.uoSelection)
        self.updateUos()
        event.Skip()

    def OnBtnChangeButton(self, event):
        self.onUOSelected(False)
        self.changeUO(self.uoSelection,self.tcName.GetValue())
        self.updateUos()
        event.Skip()
