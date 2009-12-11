#Boa:Dialog:DlgManageEM

import wx
from einstein.GUI.status import *

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)


def create(parent):
    return DlgManageEM(parent)

[wxID_DIALOGMANNAGEEM, wxID_DIALOGMANNAGEEMBTNADD, 
 wxID_DIALOGMANNAGEEMBTNCHANGE, wxID_DIALOGMANNAGEEMBTNDELETE, 
 wxID_DIALOGMANNAGEEMLBMEASURES, wxID_DIALOGMANNAGEEMSTATICTEXT1, 
 wxID_DIALOGMANNAGEEMSTATICTEXT2, wxID_DIALOGMANNAGEEMSTATICTEXT3, 
 wxID_DIALOGMANNAGEEMTCDESC, wxID_DIALOGMANNAGEEMTCTEXT, 
] = [wx.NewId() for _init_ctrls in range(10)]

class DlgManageEM(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOGMANNAGEEM, name='', parent=prnt,
              pos=wx.Point(91, 140), size=wx.Size(1046, 471),
              style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Manage Efficiency Measures')
        self.SetClientSize(wx.Size(1038, 444))

        self.tcDesc = wx.TextCtrl(id=wxID_DIALOGMANNAGEEMTCDESC, name=u'tcDesc',
              parent=self, pos=wx.Point(592, 24), size=wx.Size(432, 21),
              style=0, value=u'')

        self.staticText1 = wx.StaticText(id=wxID_DIALOGMANNAGEEMSTATICTEXT1,
              label=u'Short Description:', name='staticText1', parent=self,
              pos=wx.Point(496, 24), size=wx.Size(86, 13), style=0)

        self.lbMeasures = wx.ListBox(choices=[],
              id=wxID_DIALOGMANNAGEEMLBMEASURES, name=u'lbMeasures',
              parent=self, pos=wx.Point(8, 24), size=wx.Size(464, 384),
              style=0)
        self.lbMeasures.Bind(wx.EVT_LISTBOX, self.OnLbMeasuresListbox,
              id=wxID_DIALOGMANNAGEEMLBMEASURES)

        self.staticText2 = wx.StaticText(id=wxID_DIALOGMANNAGEEMSTATICTEXT2,
              label=u'Text:', name='staticText2', parent=self, pos=wx.Point(557,
              48), size=wx.Size(26, 13), style=0)

        self.btnChange = wx.Button(id=wxID_DIALOGMANNAGEEMBTNCHANGE,
              label=u'Change', name=u'btnChange', parent=self, pos=wx.Point(952,
              416), size=wx.Size(75, 23), style=0)
        self.btnChange.Bind(wx.EVT_BUTTON, self.OnBtnChangeButton,
              id=wxID_DIALOGMANNAGEEMBTNCHANGE)

        self.btnAdd = wx.Button(id=wxID_DIALOGMANNAGEEMBTNADD, label=u'Add',
              name=u'btnAdd', parent=self, pos=wx.Point(864, 416),
              size=wx.Size(75, 23), style=0)
        self.btnAdd.Bind(wx.EVT_BUTTON, self.OnBtnAddButton,
              id=wxID_DIALOGMANNAGEEMBTNADD)

        self.btnDelete = wx.Button(id=wxID_DIALOGMANNAGEEMBTNDELETE,
              label=u'Delete', name=u'btnDelete', parent=self, pos=wx.Point(392,
              416), size=wx.Size(75, 23), style=0)
        self.btnDelete.Bind(wx.EVT_BUTTON, self.OnBtnDeleteButton,
              id=wxID_DIALOGMANNAGEEMBTNDELETE)

        self.tcText = wx.TextCtrl(id=wxID_DIALOGMANNAGEEMTCTEXT, name=u'tcText',
              parent=self, pos=wx.Point(592, 48), size=wx.Size(432, 360),
              style=wx.TE_MULTILINE, value=u'')

        self.staticText3 = wx.StaticText(id=wxID_DIALOGMANNAGEEMSTATICTEXT3,
              label=u'Measures:', name='staticText3', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(50, 13), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.ems = []
        self.selectedEM = None
        self.updateEM()
        self.onEMSelected(False)
    
    def onEMSelected(self,bool):
        self.btnChange.Enabled = bool
        self.btnDelete.Enabled = bool

    def loadEM(self):
        query = """SELECT IDEfficiencyMeasure,ShortDescription,Text FROM poefficiencymeasure"""
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.ems = results 
        else:
            self.ems = []
           
    def addEM(self,desc,text):
        query = """INSERT INTO poefficiencymeasure (ShortDescription,Text) VALUES (\"%s\",\"%s\")"""
        query = query % (desc,text) 
        Status.DB.sql_query(query)        
        
    def deleteEM(self,index):
        em = self.ems[index]
        query = """SELECT * FROM poemlistentry WHERE EfficiencyMeasureID=%s"""
        query = query % (em[0])
        result = Status.DB.sql_query(query)
        if len(result) == 0:                
            query = """DELETE FROM poefficiencymeasure WHERE IDEfficiencyMeasure = %s"""
            query = query % (em[0])
            Status.DB.sql_query(query)
        else:
            wx.MessageBox("Could not delete. Efficiency Measure is in use.")
        
    def changeEM(self,index,name,text):
        em = self.ems[index]
        query = """UPDATE poefficiencymeasure SET ShortDescription=\'%s\', Text = \'%s\'   
                   WHERE IDEfficiencyMeasure = %s"""
        query = query % (name,text,em[0])
        Status.DB.sql_query(query)
     
    def updateEM(self):
        self.loadEM()
        self.lbMeasures.Clear()
        for em in self.ems:
            self.lbMeasures.Append(em[1])
    

    def OnLbMeasuresListbox(self, event):
        self.selectedEM = self.lbMeasures.GetSelection()
        em = self.ems[self.selectedEM]
        self.onEMSelected(True)
        self.tcDesc.SetValue(em[1])
        self.tcText.SetValue(em[2])
        event.Skip()

    def OnBtnChangeButton(self, event):
        self.onEMSelected(False)
        self.changeEM(self.selectedEM,self.tcDesc.GetValue(),self.tcText.GetValue())
        self.updateEM()
        self.onEMSelected(False)
        event.Skip()

    def OnBtnAddButton(self, event):
        self.addEM(self.tcDesc.GetValue(),self.tcText.GetValue()) 
        self.updateEM()
        self.onEMSelected(False)
        event.Skip()

    def OnBtnDeleteButton(self, event):
        self.deleteEM(self.selectedEM)
        self.onEMSelected(False)
        self.updateEM()
        event.Skip()
