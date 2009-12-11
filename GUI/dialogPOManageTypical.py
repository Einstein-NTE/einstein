#Boa:Dialog:DlgManageTP

import wx
from einstein.GUI.status import *

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)


def create(parent):
    return Dialog1(parent)

[wxID_DLGMANAGETP, wxID_DLGMANAGETPBTNADD, wxID_DLGMANAGETPBTNCHANGE, 
 wxID_DLGMANAGETPBTNREMOVE, wxID_DLGMANAGETPLBLIST, wxID_DLGMANAGETPTCCODE, 
 wxID_DLGMANAGETPTCNAME, 
] = [wx.NewId() for _init_ctrls in range(7)]

class DlgManageTP(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGMANAGETP, name='', parent=prnt,
              pos=wx.Point(414, 71), size=wx.Size(490, 441),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'Manage Typical Process')
        self.SetClientSize(wx.Size(482, 414))

        self.lbList = wx.ListBox(choices=[], id=wxID_DLGMANAGETPLBLIST,
              name=u'lbList', parent=self, pos=wx.Point(8, 8), size=wx.Size(376,
              368), style=0)
        self.lbList.Bind(wx.EVT_LISTBOX, self.OnLbListListbox,
              id=wxID_DLGMANAGETPLBLIST)

        self.tcName = wx.TextCtrl(id=wxID_DLGMANAGETPTCNAME, name=u'tcName',
              parent=self, pos=wx.Point(96, 384), size=wx.Size(288, 21),
              style=0, value=u'')

        self.btnAdd = wx.Button(id=wxID_DLGMANAGETPBTNADD, label=u'Add',
              name=u'btnAdd', parent=self, pos=wx.Point(392, 384),
              size=wx.Size(75, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_DLGMANAGETPBTNADD)

        self.btnRemove = wx.Button(id=wxID_DLGMANAGETPBTNREMOVE,
              label=u'Remove', name=u'btnRemove', parent=self, pos=wx.Point(392,
              320), size=wx.Size(75, 23), style=0)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.OnBtnRemoveButton,
              id=wxID_DLGMANAGETPBTNREMOVE)

        self.btnChange = wx.Button(id=wxID_DLGMANAGETPBTNCHANGE,
              label=u'Change', name=u'btnChange', parent=self, pos=wx.Point(392,
              352), size=wx.Size(75, 23), style=0)
        self.btnChange.Bind(wx.EVT_BUTTON, self.OnBtnChangeButton,
              id=wxID_DLGMANAGETPBTNCHANGE)

        self.tcCode = wx.TextCtrl(id=wxID_DLGMANAGETPTCCODE, name=u'tcCode',
              parent=self, pos=wx.Point(8, 384), size=wx.Size(88, 21), style=0,
              value=u'')

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.onTPSelected(False)
        self.updateTP()
    
    def updateTP(self):
        self.loadTP()
        self.lbList.Clear()
        for tech in self.techs:
            self.lbList.Append(tech[2]+"|"+tech[1])
    
    def onTPSelected(self,bool):
        self.btnChange.Enabled = bool
        self.btnRemove.Enabled = bool
        
    def loadTP(self):
        query = """SELECT IDTypicalProcess,Name,Code FROM potypicalprocess"""
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.techs = results 
        else:
            self.techs = []
    
    def addTP(self,name,code):
        query = """INSERT INTO potypicalprocess (Name,Code) VALUES (\"%s\",\"%s\")"""
        query = query % (name,code)
        Status.DB.sql_query(query)
    
    def deleteTP(self,index):
        tech = self.techs[index]
        
        query = """SELECT * FROM poemlist WHERE TypicalProcessID = %s"""
        query = query % tech[0]
        result = Status.DB.sql_query(query)
        
        if (len(result)==0):                
            query = """DELETE FROM potypicalprocess WHERE IDTypicalProcess = %s"""                        
            query = query % tech[0]
            Status.DB.sql_query(query)
        else:
            wx.MessageBox("Could not delete. Typical Process is in use.")
        
    def changeTP(self,index,name,code):
        uo = self.techs[index]
        query = """UPDATE potypicalprocess SET Name = \"%s\",Code = \"%s\" WHERE IDTypicalProcess = %s"""
        query = query % (name,code,uo[0])
        Status.DB.sql_query(query)

    def OnLbListListbox(self, event):
        self.techselection = self.lbList.GetSelection()
        tech = self.techs[self.techselection]
        self.tcCode.SetValue(tech[2])
        self.tcName.SetValue(tech[1])
        self.onTPSelected(True)
        event.Skip()

    def OnBtnAddButton(self, event):
        self.addTP(self.tcName.GetValue(),self.tcCode.GetValue())
        self.updateTP()
        event.Skip()

    def OnBtnRemoveButton(self, event):
        self.onTPSelected(False)
        self.deleteTP(self.techselection)
        self.updateTP()
        event.Skip()

    def OnBtnChangeButton(self, event):
        self.onTPSelected(False)
        self.changeTP(self.techselection,self.tcName.GetValue(),self.tcCode.GetValue())
        self.updateTP()
        event.Skip()
