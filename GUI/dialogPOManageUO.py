#Boa:Dialog:DlgManageUO

import wx
from einstein.GUI.status import *

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)


def create(parent):
    return Dialog1(parent)

[wxID_DLGMANAGEUO, wxID_DLGMANAGEUOBTNADD, wxID_DLGMANAGEUOBTNCHANGE, 
 wxID_DLGMANAGEUOBTNREMOVE, wxID_DLGMANAGEUOLBLIST, wxID_DLGMANAGEUOTCCODE, 
 wxID_DLGMANAGEUOTCNAME, 
] = [wx.NewId() for _init_ctrls in range(7)]

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
              parent=self, pos=wx.Point(104, 384), size=wx.Size(280, 21),
              style=0, value=u'')

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

        self.tcCode = wx.TextCtrl(id=wxID_DLGMANAGEUOTCCODE, name=u'tcCode',
              parent=self, pos=wx.Point(8, 384), size=wx.Size(88, 21), style=0,
              value=u'')

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.onUOSelected(False)
        self.updateUos()
    
    def updateUos(self):
        self.loadUO()
        self.lbList.Clear()
        for uo in self.uos:
            self.lbList.Append(uo[2]+"|"+uo[1])
    
    def onUOSelected(self,bool):
        self.btnChange.Enabled = bool
        self.btnRemove.Enabled = bool
        
    def loadUO(self):
        query = """SELECT IDUnitOperation,Name,Code FROM pounitoperation"""
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.uos = results 
        else:
            self.uos = []
            
    def loadUOExisting(self,SSID):
        query = """SELECT IDUnitOperation,Name,Code FROM pounitoperation as uo, poemlist as list
                    WHERE list.UnitOperationID = uo.IDUnitOperation AND SubsectorID=%s 
                    GROUP BY IDUnitOperation"""
        query = query % SSID
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.uos = results 
        else:
            self.uos = []
    
    def addUO(self,name,code):
        query = """INSERT INTO pounitoperation (Name,Code) VALUES (\"%s\",\"%s\")"""
        query = query % (name,code)
        Status.DB.sql_query(query)
    
    def deleteUO(self,index):
        uo = self.uos[index]
        
        query = """SELECT * FROM poemlist WHERE UnitOperationID = %s"""
        query = query % uo[0]
        result = Status.DB.sql_query(query)
                
        if (len(result) == 0):
            query = """DELETE FROM pounitoperation WHERE IDUnitOperation = %s"""
            query = query % uo[0]
            Status.DB.sql_query(query)
        else:
            wx.MessageBox("Could not delete. Unit Operation in use.")
        
    def changeUO(self,index,name,code):
        uo = self.uos[index]
        query = """UPDATE pounitoperation SET Name = \"%s\", Code = \"%s\" WHERE IDUnitOperation = %s"""
        query = query % (name,code,uo[0])
        Status.DB.sql_query(query)

    def OnLbListListbox(self, event):
        self.uoSelection = self.lbList.GetSelection()
        uo = self.uos[self.uoSelection]
        self.onUOSelected(True)
        self.tcName.SetValue(uo[1])
        self.tcCode.SetValue(uo[2])
        event.Skip()

    def OnBtnAddButton(self, event):
        self.addUO(self.tcName.GetValue(),self.tcCode.GetValue())
        self.updateUos()
        event.Skip()

    def OnBtnRemoveButton(self, event):
        self.onUOSelected(False)
        self.deleteUO(self.uoSelection)
        self.updateUos()
        event.Skip()

    def OnBtnChangeButton(self, event):
        self.onUOSelected(False)
        self.changeUO(self.uoSelection,self.tcName.GetValue(),self.tcCode.GetValue())
        self.updateUos()
        event.Skip()
