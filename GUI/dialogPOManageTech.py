#Boa:Dialog:DlgManageTech

import wx
from einstein.GUI.status import *

def create(parent):
    return Dialog1(parent)

[wxID_DLGMANAGETECH, wxID_DLGMANAGETECHBTNADD, wxID_DLGMANAGETECHBTNCHANGE, 
 wxID_DLGMANAGETECHBTNREMOVE, wxID_DLGMANAGETECHLBLIST, 
 wxID_DLGMANAGETECHTCNAME, 
] = [wx.NewId() for _init_ctrls in range(6)]

class DlgManageTech(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGMANAGETECH, name='', parent=prnt,
              pos=wx.Point(414, 71), size=wx.Size(490, 441),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'Manage Technology')
        self.SetClientSize(wx.Size(482, 414))

        self.lbList = wx.ListBox(choices=[], id=wxID_DLGMANAGETECHLBLIST,
              name=u'lbList', parent=self, pos=wx.Point(8, 8), size=wx.Size(376,
              368), style=0)
        self.lbList.Bind(wx.EVT_LISTBOX, self.OnLbListListbox,
              id=wxID_DLGMANAGETECHLBLIST)

        self.tcName = wx.TextCtrl(id=wxID_DLGMANAGETECHTCNAME, name=u'tcName',
              parent=self, pos=wx.Point(8, 384), size=wx.Size(376, 21), style=0,
              value=u'')

        self.btnAdd = wx.Button(id=wxID_DLGMANAGETECHBTNADD, label=u'Add',
              name=u'btnAdd', parent=self, pos=wx.Point(392, 384),
              size=wx.Size(75, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_DLGMANAGETECHBTNADD)

        self.btnRemove = wx.Button(id=wxID_DLGMANAGETECHBTNREMOVE,
              label=u'Remove', name=u'btnRemove', parent=self, pos=wx.Point(392,
              320), size=wx.Size(75, 23), style=0)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.OnBtnRemoveButton,
              id=wxID_DLGMANAGETECHBTNREMOVE)

        self.btnChange = wx.Button(id=wxID_DLGMANAGETECHBTNCHANGE,
              label=u'Change', name=u'btnChange', parent=self, pos=wx.Point(392,
              352), size=wx.Size(75, 23), style=0)
        self.btnChange.Bind(wx.EVT_BUTTON, self.OnBtnChangeButton,
              id=wxID_DLGMANAGETECHBTNCHANGE)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.onTechSelected(False)
        self.updateTech()
    
    def updateTech(self):
        self.loadTech()
        self.lbList.Clear()
        for tech in self.techs:
            self.lbList.Append(tech[1])
    
    def onTechSelected(self,bool):
        self.btnChange.Enabled = bool
        self.btnRemove.Enabled = bool
        
    def loadTech(self):
        query = """SELECT IDTechnology,Name FROM poTech"""
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.techs = results 
        else:
            self.techs = []
    
    def addTech(self,name):
        query = """INSERT INTO poTech (Name) VALUES (\"%s\")"""
        query = query % name
        Status.DB.sql_query(query)
    
    def deleteTech(self,index):
        tech = self.techs[index]
        
        query = """SELECT * FROM poEMList WHERE TechnologyID = %s"""
        query = query % tech[0]
        result = Status.DB.sql_query(query)
        
        if (len(result)==0):                
            query = """DELETE FROM poTech WHERE IDTechnology = %s"""                        
            query = query % tech[0]
            Status.DB.sql_query(query)
        else:
            wx.MessageBox("Could not delete. Technology is in use.")
        
    def changeTech(self,index,name):
        uo = self.techs[index]
        query = """UPDATE poTech SET Name = \"%s\" WHERE IDTechnology = %s"""
        query = query % (name,uo[0])
        Status.DB.sql_query(query)

    def OnLbListListbox(self, event):
        self.techselection = self.lbList.GetSelection()
        self.onTechSelected(True)
        event.Skip()

    def OnBtnAddButton(self, event):
        self.addTech(self.tcName.GetValue())
        self.updateTech()
        event.Skip()

    def OnBtnRemoveButton(self, event):
        self.onTechSelected(False)
        self.deleteTech(self.techselection)
        self.updateTech()
        event.Skip()

    def OnBtnChangeButton(self, event):
        self.onTechSelected(False)
        self.changeTech(self.techselection,self.tcName.GetValue())
        self.updateTech()
        event.Skip()
