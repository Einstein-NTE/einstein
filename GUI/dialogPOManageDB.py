#Boa:Dialog:DialogPOManageDB

import wx
from einstein.GUI.status import *
from dialogPOManageUO import DlgManageUO
from dialogPOManageTech import DlgManageTech
from dialogPOManageEM import DlgManageEM

def create(parent):
    return Dialog1(parent)

[wxID_DIALOGPOMANAGEDB, wxID_DIALOGPOMANAGEDBBTNADDEMLIST, 
 wxID_DIALOGPOMANAGEDBBTNADDSECTOR, wxID_DIALOGPOMANAGEDBBTNADDSUBSECTOR, 
 wxID_DIALOGPOMANAGEDBBTNADDTP, wxID_DIALOGPOMANAGEDBBTNADDUNITOPERATION, 
 wxID_DIALOGPOMANAGEDBBTNCHANGE, wxID_DIALOGPOMANAGEDBBTNCHANGESUBSECTOR, 
 wxID_DIALOGPOMANAGEDBBTNCHANGETP, wxID_DIALOGPOMANAGEDBBTNLINKMEASURE, 
 wxID_DIALOGPOMANAGEDBBTNMANAGEMEASURES, 
 wxID_DIALOGPOMANAGEDBBTNMANAGETECHNOLOGIES, 
 wxID_DIALOGPOMANAGEDBBTNMANAGEUNITOPERATION, wxID_DIALOGPOMANAGEDBBTNREMOVE, 
 wxID_DIALOGPOMANAGEDBBTNREMOVEEMLIST, 
 wxID_DIALOGPOMANAGEDBBTNREMOVESUBSECTOR, wxID_DIALOGPOMANAGEDBBTNREMOVETP, 
 wxID_DIALOGPOMANAGEDBBTNREMOVEUNITOPERATION, 
 wxID_DIALOGPOMANAGEDBBTNUNLINKMEASURE, wxID_DIALOGPOMANAGEDBCBMEASURE, 
 wxID_DIALOGPOMANAGEDBCBTECH, wxID_DIALOGPOMANAGEDBCBUO, 
 wxID_DIALOGPOMANAGEDBLBEMLIST, wxID_DIALOGPOMANAGEDBLBMEASURE, 
 wxID_DIALOGPOMANAGEDBLBSECTORS, wxID_DIALOGPOMANAGEDBLBSUBSECTORS, 
 wxID_DIALOGPOMANAGEDBLBTYPICALPROCESS, wxID_DIALOGPOMANAGEDBLBUNITOPERATION, 
 wxID_DIALOGPOMANAGEDBSTATICBOX1, wxID_DIALOGPOMANAGEDBSTATICBOX2, 
 wxID_DIALOGPOMANAGEDBSTATICBOX3, wxID_DIALOGPOMANAGEDBSTATICBOX4, 
 wxID_DIALOGPOMANAGEDBSTATICBOX5, wxID_DIALOGPOMANAGEDBSTATICBOX6, 
 wxID_DIALOGPOMANAGEDBSTATICTEXT1, wxID_DIALOGPOMANAGEDBSTATICTEXT2, 
 wxID_DIALOGPOMANAGEDBTCSECTORNAME, wxID_DIALOGPOMANAGEDBTCSHOWTP, 
 wxID_DIALOGPOMANAGEDBTCSUBSECTOR, wxID_DIALOGPOMANAGEDBTCTYPICALPROCESS, 
] = [wx.NewId() for _init_ctrls in range(40)]

class DialogPOManageDB(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOGPOMANAGEDB, name='', parent=prnt,
              pos=wx.Point(4, 23), size=wx.Size(1279, 719),
              style=wx.DEFAULT_DIALOG_STYLE,
              title=_(u'Manage Process Optimisation Database'))
        self.SetClientSize(wx.Size(1271, 692))

        self.staticBox1 = wx.StaticBox(id=wxID_DIALOGPOMANAGEDBSTATICBOX1,
              label=u'Sectors', name='staticBox1', parent=self, pos=wx.Point(8,
              8), size=wx.Size(328, 296), style=0)

        self.lbSectors = wx.ListBox(choices=[],
              id=wxID_DIALOGPOMANAGEDBLBSECTORS, name=u'lbSectors', parent=self,
              pos=wx.Point(16, 24), size=wx.Size(312, 208), style=0)
        self.lbSectors.Bind(wx.EVT_LISTBOX, self.OnLbSectorsListbox,
              id=wxID_DIALOGPOMANAGEDBLBSECTORS)

        self.btnAddSector = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNADDSECTOR,
              label=u'Add', name=u'btnAddSector', parent=self, pos=wx.Point(144,
              272), size=wx.Size(56, 23), style=0)
        self.btnAddSector.Bind(wx.EVT_BUTTON, self.OnBtnAddSectorButton,
              id=wxID_DIALOGPOMANAGEDBBTNADDSECTOR)

        self.btnRemove = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNREMOVE,
              label=u'Remove', name=u'btnRemove', parent=self, pos=wx.Point(208,
              272), size=wx.Size(56, 23), style=0)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.OnBtnRemoveButton,
              id=wxID_DIALOGPOMANAGEDBBTNREMOVE)

        self.btnChange = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNCHANGE,
              label=u'Change', name=u'btnChange', parent=self, pos=wx.Point(272,
              272), size=wx.Size(56, 23), style=0)
        self.btnChange.Bind(wx.EVT_BUTTON, self.OnBtnChangeButton,
              id=wxID_DIALOGPOMANAGEDBBTNCHANGE)

        self.tcSectorName = wx.TextCtrl(id=wxID_DIALOGPOMANAGEDBTCSECTORNAME,
              name=u'tcSectorName', parent=self, pos=wx.Point(16, 240),
              size=wx.Size(312, 21), style=0, value=u'New Sector')

        self.staticBox2 = wx.StaticBox(id=wxID_DIALOGPOMANAGEDBSTATICBOX2,
              label=u'Subsectors', name='staticBox2', parent=self,
              pos=wx.Point(344, 8), size=wx.Size(328, 296), style=0)

        self.lbSubsectors = wx.ListBox(choices=[],
              id=wxID_DIALOGPOMANAGEDBLBSUBSECTORS, name=u'lbSubsectors',
              parent=self, pos=wx.Point(352, 24), size=wx.Size(312, 208),
              style=0)
        self.lbSubsectors.Bind(wx.EVT_LISTBOX, self.OnLbSubsectors,
              id=wxID_DIALOGPOMANAGEDBLBSUBSECTORS)

        self.tcSubsector = wx.TextCtrl(id=wxID_DIALOGPOMANAGEDBTCSUBSECTOR,
              name=u'tcSubsector', parent=self, pos=wx.Point(352, 240),
              size=wx.Size(312, 21), style=0, value=u'New Subsector')

        self.btnAddSubsector = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNADDSUBSECTOR,
              label=u'Add', name=u'btnAddSubsector', parent=self,
              pos=wx.Point(480, 272), size=wx.Size(56, 23), style=0)
        self.btnAddSubsector.Bind(wx.EVT_BUTTON, self.OnBtnAddSubsectorButton,
              id=wxID_DIALOGPOMANAGEDBBTNADDSUBSECTOR)

        self.btnRemoveSubsector = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNREMOVESUBSECTOR,
              label=u'Remove', name=u'btnRemoveSubsector', parent=self,
              pos=wx.Point(544, 272), size=wx.Size(56, 23), style=0)
        self.btnRemoveSubsector.Bind(wx.EVT_BUTTON,
              self.OnBtnRemoveSubsectorButton,
              id=wxID_DIALOGPOMANAGEDBBTNREMOVESUBSECTOR)

        self.btnChangeSubsector = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNCHANGESUBSECTOR,
              label=u'Change', name=u'btnChangeSubsector', parent=self,
              pos=wx.Point(608, 272), size=wx.Size(56, 23), style=0)
        self.btnChangeSubsector.Bind(wx.EVT_BUTTON,
              self.OnBtnChangeSubsectorButton,
              id=wxID_DIALOGPOMANAGEDBBTNCHANGESUBSECTOR)

        self.staticBox3 = wx.StaticBox(id=wxID_DIALOGPOMANAGEDBSTATICBOX3,
              label=u'Unit Operation', name='staticBox3', parent=self,
              pos=wx.Point(680, 8), size=wx.Size(328, 296), style=0)

        self.lbUnitOperation = wx.ListBox(choices=[],
              id=wxID_DIALOGPOMANAGEDBLBUNITOPERATION, name=u'lbUnitOperation',
              parent=self, pos=wx.Point(688, 24), size=wx.Size(312, 208),
              style=0)
        self.lbUnitOperation.Bind(wx.EVT_LISTBOX, self.OnLbUnitOperationListbox,
              id=wxID_DIALOGPOMANAGEDBLBUNITOPERATION)

        self.cbUO = wx.Choice(choices=[], id=wxID_DIALOGPOMANAGEDBCBUO,
              name='cbUO', parent=self, pos=wx.Point(688, 240),
              size=wx.Size(216, 21), style=0)

        self.btnAddUnitOperation = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNADDUNITOPERATION,
              label=u'Link', name=u'btnAddUnitOperation', parent=self,
              pos=wx.Point(912, 240), size=wx.Size(40, 23), style=0)
        self.btnAddUnitOperation.Bind(wx.EVT_BUTTON,
              self.OnBtnAddUnitOperationButton,
              id=wxID_DIALOGPOMANAGEDBBTNADDUNITOPERATION)

        self.btnRemoveUnitOperation = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNREMOVEUNITOPERATION,
              label=u'Unlink', name=u'btnRemoveUnitOperation', parent=self,
              pos=wx.Point(960, 240), size=wx.Size(40, 23), style=0)
        self.btnRemoveUnitOperation.Bind(wx.EVT_BUTTON,
              self.OnBtnRemoveUnitOperationButton,
              id=wxID_DIALOGPOMANAGEDBBTNREMOVEUNITOPERATION)

        self.btnManageUnitOperation = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNMANAGEUNITOPERATION,
              label=u'Manage Unit Operation', name=u'btnManageUnitOperation',
              parent=self, pos=wx.Point(688, 272), size=wx.Size(312, 23),
              style=0)
        self.btnManageUnitOperation.Bind(wx.EVT_BUTTON,
              self.OnBtnManageUnitOperationButton,
              id=wxID_DIALOGPOMANAGEDBBTNMANAGEUNITOPERATION)

        self.btnManageTechnologies = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNMANAGETECHNOLOGIES,
              label=u'Manage Technologies', name=u'btnManageTechnologies',
              parent=self, pos=wx.Point(32, 544), size=wx.Size(152, 23),
              style=0)
        self.btnManageTechnologies.Bind(wx.EVT_BUTTON,
              self.OnBtnManageTechnologiesButton,
              id=wxID_DIALOGPOMANAGEDBBTNMANAGETECHNOLOGIES)

        self.staticBox4 = wx.StaticBox(id=wxID_DIALOGPOMANAGEDBSTATICBOX4,
              label=u'Typical Process', name='staticBox4', parent=self,
              pos=wx.Point(1016, 8), size=wx.Size(248, 296), style=0)

        self.tcTypicalProcess = wx.TextCtrl(id=wxID_DIALOGPOMANAGEDBTCTYPICALPROCESS,
              name=u'tcTypicalProcess', parent=self, pos=wx.Point(1024, 240),
              size=wx.Size(232, 21), style=0, value=u'New Typical Process')

        self.btnChangeTP = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNCHANGETP,
              label=u'Change', name=u'btnChangeTP', parent=self,
              pos=wx.Point(1200, 272), size=wx.Size(56, 23), style=0)
        self.btnChangeTP.Bind(wx.EVT_BUTTON, self.OnBtnChangeTPButton,
              id=wxID_DIALOGPOMANAGEDBBTNCHANGETP)

        self.btnRemoveTP = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNREMOVETP,
              label=u'Remove', name=u'btnRemoveTP', parent=self,
              pos=wx.Point(1136, 272), size=wx.Size(59, 23), style=0)
        self.btnRemoveTP.Bind(wx.EVT_BUTTON, self.OnBtnRemoveTPButton,
              id=wxID_DIALOGPOMANAGEDBBTNREMOVETP)

        self.btnAddTP = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNADDTP,
              label=u'Add', name=u'btnAddTP', parent=self, pos=wx.Point(1072,
              272), size=wx.Size(59, 23), style=0)
        self.btnAddTP.Bind(wx.EVT_BUTTON, self.OnBtnAddTPButton,
              id=wxID_DIALOGPOMANAGEDBBTNADDTP)

        self.lbTypicalProcess = wx.ListBox(choices=[],
              id=wxID_DIALOGPOMANAGEDBLBTYPICALPROCESS,
              name=u'lbTypicalProcess', parent=self, pos=wx.Point(1024, 24),
              size=wx.Size(232, 208), style=0)
        self.lbTypicalProcess.Bind(wx.EVT_LISTBOX,
              self.OnLbTypicalProcessListbox,
              id=wxID_DIALOGPOMANAGEDBLBTYPICALPROCESS)

        self.staticBox6 = wx.StaticBox(id=wxID_DIALOGPOMANAGEDBSTATICBOX6,
              label=u'Linking', name='staticBox6', parent=self, pos=wx.Point(8,
              312), size=wx.Size(480, 368), style=0)

        self.tcShowTP = wx.TextCtrl(id=wxID_DIALOGPOMANAGEDBTCSHOWTP,
              name=u'tcShowTP', parent=self, pos=wx.Point(112, 336),
              size=wx.Size(360, 21), style=0, value=u'')
        self.tcShowTP.Enable(False)

        self.cbTech = wx.ComboBox(choices=[], id=wxID_DIALOGPOMANAGEDBCBTECH,
              name=u'cbTech', parent=self, pos=wx.Point(96, 512),
              size=wx.Size(376, 21), style=0, value=u'')
        self.cbTech.SetLabel(u'')

        self.staticText1 = wx.StaticText(id=wxID_DIALOGPOMANAGEDBSTATICTEXT1,
              label=u'Typical Process:', name='staticText1', parent=self,
              pos=wx.Point(32, 336), size=wx.Size(77, 13), style=0)

        self.lbEMList = wx.ListBox(choices=[], id=wxID_DIALOGPOMANAGEDBLBEMLIST,
              name=u'lbEMList', parent=self, pos=wx.Point(32, 360),
              size=wx.Size(440, 144), style=0)
        self.lbEMList.Bind(wx.EVT_LISTBOX, self.OnLbEMListListbox,
              id=wxID_DIALOGPOMANAGEDBLBEMLIST)

        self.staticText2 = wx.StaticText(id=wxID_DIALOGPOMANAGEDBSTATICTEXT2,
              label=u'Technology', name='staticText2', parent=self,
              pos=wx.Point(32, 512), size=wx.Size(55, 13), style=0)

        self.btnRemoveEMList = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNREMOVEEMLIST,
              label=u'Remove', name=u'btnRemoveEMList', parent=self,
              pos=wx.Point(408, 544), size=wx.Size(59, 23), style=0)
        self.btnRemoveEMList.Bind(wx.EVT_BUTTON, self.OnBtnRemoveEMListButton,
              id=wxID_DIALOGPOMANAGEDBBTNREMOVEEMLIST)

        self.btnAddEMList = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNADDEMLIST,
              label=u'Add', name=u'btnAddEMList', parent=self, pos=wx.Point(344,
              544), size=wx.Size(59, 23), style=0)
        self.btnAddEMList.Bind(wx.EVT_BUTTON, self.OnBtnAddEMListButton,
              id=wxID_DIALOGPOMANAGEDBBTNADDEMLIST)

        self.staticBox5 = wx.StaticBox(id=wxID_DIALOGPOMANAGEDBSTATICBOX5,
              label=u'Measures', name='staticBox5', parent=self,
              pos=wx.Point(496, 312), size=wx.Size(712, 368), style=0)

        self.lbMeasure = wx.ListBox(choices=[],
              id=wxID_DIALOGPOMANAGEDBLBMEASURE, name=u'lbMeasure', parent=self,
              pos=wx.Point(512, 336), size=wx.Size(680, 264), style=0)
        self.lbMeasure.Bind(wx.EVT_LISTBOX, self.OnLbMeasureListbox,
              id=wxID_DIALOGPOMANAGEDBLBMEASURE)

        self.cbMeasure = wx.Choice(choices=[],
              id=wxID_DIALOGPOMANAGEDBCBMEASURE, name=u'cbMeasure', parent=self,
              pos=wx.Point(512, 608), size=wx.Size(680, 21), style=0)

        self.btnUnlinkMeasure = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNUNLINKMEASURE,
              label=u'Unlink', name=u'btnUnlinkMeasure', parent=self,
              pos=wx.Point(1112, 640), size=wx.Size(75, 23), style=0)
        self.btnUnlinkMeasure.Bind(wx.EVT_BUTTON, self.OnBtnUnlinkMeasureButton,
              id=wxID_DIALOGPOMANAGEDBBTNUNLINKMEASURE)

        self.btnLinkMeasure = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNLINKMEASURE,
              label=u'Link', name=u'btnLinkMeasure', parent=self,
              pos=wx.Point(1024, 640), size=wx.Size(75, 23), style=0)
        self.btnLinkMeasure.Bind(wx.EVT_BUTTON, self.OnBtnLinkMeasureButton,
              id=wxID_DIALOGPOMANAGEDBBTNLINKMEASURE)

        self.btnManageMeasures = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNMANAGEMEASURES,
              label=u'Manage Measures', name=u'btnManageMeasures', parent=self,
              pos=wx.Point(512, 640), size=wx.Size(176, 23), style=0)
        self.btnManageMeasures.Bind(wx.EVT_BUTTON,
              self.OnBtnManageMeasuresButton,
              id=wxID_DIALOGPOMANAGEDBBTNMANAGEMEASURES)

    def __init__(self, parent):
        self._init_ctrls(parent)
        #sector------------------------------------------------------
        self.sectorSelection = None
        self.sectors = []
        self.onSectorSelected(False)
        self.updateSectors()
        #SUBsector---------------------------------------------------
        self.subsectorSelection = None
        self.subsectors = []  
        #Unit Operation
        self.selectedUO = None
        self.uos = []
        #Typical Process
        self.typicalProcessSelection = None
        self.tps = []
        #Techs
        self.techs = None
        #Lists
        self.lists = None
         
        
    def onSectorSelected(self,bool):
        self.btnChange.Enabled = bool
        self.btnRemove.Enabled = bool
        self.tcSubsector.Enabled = bool
        self.btnAddSubsector.Enabled = bool       
        self.onSubsectorSelected(False)
    
    def onSubsectorSelected(self,bool):
        self.btnChangeSubsector.Enabled = bool
        self.btnRemoveSubsector.Enabled = bool
        self.cbUO.Enabled = bool
        self.btnAddUnitOperation.Enabled = bool
        self.btnManageUnitOperation.Enabled = bool
        if (bool==True):
            self.updateUO()    
        else:
            self.lbUnitOperation.Clear()
                    
        self.onUOSelected(False)
    
    def onUOSelected(self,bool):        
        self.btnRemoveUnitOperation.Enabled = bool
        self.btnAddTP.Enabled = bool
        self.tcTypicalProcess.Enabled = bool
        self.onTPSelected(False)
        if (bool == True):
            self.updateTP()
        else:
            self.lbTypicalProcess.Clear()
    
    def onTPSelected(self,bool):
        self.btnRemoveTP.Enabled = bool
        self.btnChangeTP.Enabled = bool
        self.cbTech.Enabled = bool
        self.onListSelected(False)    
        self.btnAddEMList.Enabled = bool
        self.btnManageTechnologies.Enabled = bool    
        if (bool==True):
            self.updateTech()    
            self.updateEMList()        
        else:
            self.cbTech.Clear()
            self.lbEMList.Clear()
            
    def onListSelected(self,bool):
        self.cbMeasure.Enabled = bool
        self.btnLinkMeasure.Enabled = bool
        self.btnManageMeasures.Enabled = bool    
        self.btnRemoveEMList.Enabled = bool
        self.lbMeasure.Enabled = bool
        self.cbMeasure.Enabled = bool 
        if (bool==True):
            self.updateEMListEntries()                        
        else:
            self.lbMeasure.Clear()   
            
        self.onMeasureSelected(False)         
        
    def onMeasureSelected(self,bool):        
        self.btnUnlinkMeasure.Enabled = bool
        

#####################################################################################
# Sector
#####################################################################################

    #GUI-----------------------------------------------------------------------------
    def updateSectors(self):
        self.loadSectors()
        self.lbSectors.Clear()
        for sector in self.sectors:
            self.lbSectors.Append(sector[1])

    #DATABASE------------------------------------------------------------------------
    def loadSectors(self):         
        query = """SELECT IDSector,Name FROM poSector"""
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.sectors = results 
        else:
            self.sectors = []
            
    def addSector(self,name):
        query = """INSERT INTO poSector (Name) VALUES (\"%s\")"""
        query = query % name
        Status.DB.sql_query(query)
    
    def deleteSector(self,index):                
        sector = self.sectors[index]
        
        query = """SELECT * FROM poSubsector WHERE SectorID = %s"""
        query = query % sector[0]
        result = Status.DB.sql_query(query)
        
        if (len(result)==0):
            query = """DELETE FROM poSector WHERE IDSector = %s"""
            query = query % sector[0]
            Status.DB.sql_query(query)
        else:
            wx.MessageBox("Could not delete. Sector is in use.")
        
    def changeSector(self,index,name):
        sector = self.sectors[index]
        query = """UPDATE poSector SET Name = \"%s\" WHERE IDSector = %s"""
        query = query % (name,sector[0])
        Status.DB.sql_query(query)

    #BUTTONS-------------------------------------------------------------------------
    def OnLbSectorsListbox(self, event):
        self.sectorSelection = self.lbSectors.GetSelection()
        sector = self.sectors[self.sectorSelection]        
        self.tcSectorName.SetValue(sector[1])
        self.onSectorSelected(True)
        self.updateSubsectors()
        event.Skip()

    def OnBtnAddSectorButton(self, event):
        self.addSector(self.tcSectorName.GetValue())
        self.updateSectors()
        event.Skip()

    def OnBtnRemoveButton(self, event):
        self.onSectorSelected(False)
        self.deleteSector(self.sectorSelection)
        self.updateSectors()
        event.Skip()

    def OnBtnChangeButton(self, event):
        self.onSectorSelected(False)
        self.changeSector(self.sectorSelection,self.tcSectorName.GetValue())
        self.updateSectors()
        event.Skip()

#####################################################################################
# SUB-SECTORS
#####################################################################################
    #GUI-----------------------------------------------------------------------------
    def updateSubsectors(self):
        self.loadSubsectors()
        self.lbSubsectors.Clear()
        for subsector in self.subsectors:
            self.lbSubsectors.Append(subsector[1])

    #DATABASE------------------------------------------------------------------------
    def loadSubsectors(self):         
        query = """SELECT IDSubsector,Name FROM poSubsector WHERE SectorID = %s"""
        sector = self.sectors[self.sectorSelection]
        query = query % sector[0] 
        
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.subsectors = results 
        else:
            self.subsectors = []
            
    def addSubsector(self,name):
        sector = self.sectors[self.sectorSelection]
        query = """INSERT INTO poSubsector (Name,SectorID) VALUES (\"%s\","%s")"""
        query = query % (name,sector[0])
        Status.DB.sql_query(query)
    
    def deleteSubection(self,index):
        subsector = self.subsectors[index]
        
        query = """DELETE FROM poSubsector_to_UO WHERE SubsectorID = %s"""
        query = query % subsector[0]
        Status.DB.sql_query(query)
        
        query = """DELETE FROM poSubsector WHERE IDSubsector = %s"""
        query = query % subsector[0]
        Status.DB.sql_query(query)
        
    def changeSubsector(self,index,name):
        subsector = self.subsectors[index]
        query = """UPDATE poSubsector SET Name = \"%s\" WHERE IDSubsector = %s"""
        query = query % (name,subsector[0])
        Status.DB.sql_query(query)

    #BUTTONS-------------------------------------------------------------------------
    def OnLbSubsectors(self, event):
        self.subsectorSelection = self.lbSubsectors.GetSelection()
        subsector = self.subsectors[self.subsectorSelection]        
        self.tcSubsector.SetValue(subsector[1])
        self.onSubsectorSelected(True)        
        event.Skip()

    def OnBtnAddSubsectorButton(self, event):
        self.addSubsector(self.tcSubsector.GetValue())
        self.updateSubsectors()
        event.Skip()

    def OnBtnRemoveSubsectorButton(self, event):
        self.onSubsectorSelected(False)
        self.deleteSubsector(self.subsectorSelection)
        self.updateSubsectors()
        event.Skip()

    def OnBtnChangeSubsectorButton(self, event):
        self.onSubsectorSelected(False)
        self.changeSubsector(self.subsectorSelection,self.tcSubsector.GetValue())
        self.updateSubsectors()
        event.Skip()

    def OnBtnManageUnitOperationButton(self, event):
        dlg = DlgManageUO(self)
        dlg.ShowModal()
        self.updateUO()
        event.Skip()
        
#####################################################################################
# Unit Operation
#####################################################################################
    def updateUO(self):
        uo = DlgManageUO(self)
        uo.loadUO()
        self.cbUO.Clear()
        self.uos = uo.uos
        for unit in self.uos:
            self.cbUO.Append(unit[1])
        
        if len(self.uos)>0:
            self.cbUO.SetSelection(0)
        else:
            self.cbUO.Enabled = False
            
        query = """SELECT IDUnitOperation, Name FROM pounitoperation as unit, posubsector_to_uo as link 
                   WHERE unit.IDUnitOperation = link.UnitOperationID AND link.SubsectorID = %s"""
        subsector = self.subsectors[self.subsectorSelection]
        query = query % subsector[0]  
        results = Status.DB.sql_query(query)  
        
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.uoslinked = results 
        else:
            self.uoslinked = []
            
        self.lbUnitOperation.Clear()
        for uo in self.uoslinked:
            self.lbUnitOperation.Append(uo[1])

    def addUOLink(self,uo,subsector):
        query = """INSERT INTO posubsector_to_uo VALUES (%s,%s)"""
        query = query % (subsector[0],uo[0])
        Status.DB.sql_query(query)
    
    def deleteUOLink(self,uo,subsector):
        query = """DELETE FROM posubsector_to_uo WHERE SubsectorID = %s AND UnitOperationID = %s"""
        query = query % (subsector[0],uo[0])
        Status.DB.sql_query(query)

    def OnBtnAddUnitOperationButton(self, event):
        uo        = self.uos[self.cbUO.GetSelection()]
        subsector = self.subsectors[self.subsectorSelection]
        self.addUOLink(uo, subsector)
        self.updateUO()
        event.Skip()

    def OnBtnRemoveUnitOperationButton(self, event):
        uo        = self.uos[self.selectedUO]
        subsector = self.subsectors[self.subsectorSelection]
        self.deleteUOLink(uo, subsector)
        self.onUOSelected(False)
        self.updateUO()
        event.Skip()

    def OnLbUnitOperationListbox(self, event):
        self.selectedUO = self.lbUnitOperation.GetSelection()
        self.onUOSelected(True)
        event.Skip()

#####################################################################################
# Typical Process
#####################################################################################

    #GUI-----------------------------------------------------------------------------
    def updateTP(self):
        self.loadTP()
        self.lbTypicalProcess.Clear()
        for tp in self.tps:
            self.lbTypicalProcess.Append(tp[1])

    #DATABASE------------------------------------------------------------------------
    def loadTP(self):         
        query = """SELECT IDTypicalProcess,Name FROM poTypicalProcess WHERE UnitOperationID = %s"""
        uo = self.uos[self.selectedUO]
        query = query % uo[0] 
        
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.tps = results 
        else:
            self.tps = []
            
    def addTP(self,name):
        uo = self.uos[self.selectedUO]
        query = """INSERT INTO poTypicalProcess (Name,UnitOperationID) VALUES (\"%s\","%s")"""
        query = query % (name,uo[0])
        Status.DB.sql_query(query)
    
    def deleteTP(self,index):
        tp = self.tps[index]
        
        query = """SELECT * FROM poEMList WHERE TypicalProcessID = %s"""
        query = query % tp[0]
        result = Status.DB.sql_query(query)
        
        if len(result)==0:
            query = """DELETE FROM poTypicalProcess WHERE IDTypicalProcess = %s"""
            query = query % tp[0]
            Status.DB.sql_query(query)
        else:
            wx.MessageBox("Could not delete. Typical Process is in use. Unlink technology first.")
    
    def changeTP(self,index,name):
        tp = self.tps[index]
        query = """UPDATE poTypicalProcess SET Name = \"%s\" WHERE IDTypicalProcess = %s"""
        query = query % (name,tp[0])
        Status.DB.sql_query(query)


    #Buttons-------------------------------------------------------------------------------------
    def OnBtnChangeTPButton(self, event):
        self.onTPSelected(False)
        self.changeTP(self.typicalProcessSelection,self.tcTypicalProcess.GetValue())
        self.updateTP()
        
    def OnBtnRemoveTPButton(self, event):
        self.onTPSelected(False)
        self.deleteTP(self.typicalProcessSelection)
        self.updateTP()
        event.Skip()

    def OnBtnAddTPButton(self, event):
        self.addTP(self.tcTypicalProcess.GetValue())
        self.updateTP()
        event.Skip()
         
    def OnLbTypicalProcessListbox(self, event):
        self.typicalProcessSelection = self.lbTypicalProcess.GetSelection()
        tp = self.tps[self.typicalProcessSelection]        
        self.tcTypicalProcess.SetValue(tp[1])
        self.onTPSelected(True)        
        event.Skip()

#####################################################################################
# Technology
#####################################################################################  

    def updateTech(self):
        tp = self.tps[self.typicalProcessSelection]
        self.tcShowTP.SetValue(tp[1])
        
        tech = DlgManageTech(self)
        tech.loadTech()
        self.cbTech.Clear()
        self.techs = tech.techs
        for tech in self.techs:
            self.cbTech.Append(tech[1])
        
        if len(self.techs)>0:
            self.cbTech.SetSelection(0)
        else:
            self.cbtech.Enabled = False

    def OnBtnManageTechnologiesButton(self, event):
        dlg = DlgManageTech(self)
        dlg.ShowModal()
        self.updateTech()
        event.Skip()

#####################################################################################
# EmList - Linking
#####################################################################################  
    def updateEMList(self):
        self.loadEMList()
        self.lbEMList.Clear()
        for list in self.lists:
            self.lbEMList.Append(list[2]+" ("+list[1]+")")        
    
    def loadEMList(self):         
        query = """SELECT list.IDEMList, tp.Name, tech.Name FROM poEMList as list, poTypicalProcess as tp, poTech as tech 
                   WHERE tp.IDTypicalProcess = list.TypicalProcessID AND tech.IDtechnology = list.TechnologyID 
                         AND list.TypicalProcessID = %s"""
        #tech = self.techs[self.cbTech.GetSelection()]
        tp   = self.tps[self.typicalProcessSelection]
        query = query % (tp[0]) 
        
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.lists = results 
        else:
            self.lists = []

    def addEMList(self,tech,tp):
        query = """INSERT INTO poEMList (TechnologyID,TypicalProcessID) VALUES (%s,%s)"""
        query = query % (tech[0],tp[0]) 
        Status.DB.sql_query(query)    
    
    def deleteEMList(self,list):
        query = """DELETE FROM poEMList WHERE IDEMList = %s"""
        query = query % (list[0]) 
        Status.DB.sql_query(query)
        query = """DELETE FROM poEMListEntry WHERE EMListID = %s"""
        query = query % (list[0]) 
        Status.DB.sql_query(query)         


    def OnLbEMListListbox(self, event):
        self.ListSelection = self.lbEMList.GetSelection()
        self.onListSelected(True)        
        event.Skip()

    def OnBtnAddEMListButton(self, event):
        tech = self.techs[self.cbTech.GetSelection()]
        tp   = self.tps[self.typicalProcessSelection]
        self.addEMList(tech, tp)
        self.updateEMList()
        self.onListSelected(False)
        event.Skip()

    def OnBtnRemoveEMListButton(self, event):
        list = self.lists[self.ListSelection]
        self.deleteEMList(list)
        self.updateEMList()
        self.onListSelected(False) 
        event.Skip()


#####################################################################################
# EmList - Entries
##################################################################################### 
    def updateEMListEntries(self):
        self.loadEMListEntries()
        self.loadMeasures()
        
        self.cbMeasure.Clear()
        for em in self.ems:
            self.cbMeasure.Append(em[1])     
        self.cbMeasure.SetSelection(0) 
        
        self.lbMeasure.Clear()  
        for em in self.emslinked:
            self.lbMeasure.Append(em[1])
            
    
    def loadEMListEntries(self):
        query = """SELECT em.IDEfficiencyMeasure, em.ShortDescription 
                   FROM poEfficiencyMeasure as em, poemlistentry as entry 
                   WHERE entry.EfficiencyMeasureID = em.IDEfficiencyMeasure
                        AND entry.EMListID = %s"""
        list = self.lists[self.ListSelection]
        query = query % list[0]
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.emslinked = results 
        else:
            self.emslinked = []
    
    def loadMeasures(self):        
        dlg = DlgManageEM(self)
        dlg.loadEM()
        self.ems = dlg.ems   
    
    def addEMListEntry(self,list,measure):
        query = """INSERT INTO poEMListEntry (EMListID,EfficiencyMeasureID) VALUES (%s,%s)"""
        query = query % (list[0],measure[0])
        Status.DB.sql_query(query)  
    
    def deleteEMListEntry(self,list,measure):
        query = """DELETE FROM poEMListEntry WHERE EMListID = %s AND EfficiencyMeasureID = %s"""
        query = query % (list[0],measure[0])
        Status.DB.sql_query(query)

    def OnBtnUnlinkMeasureButton(self, event):
        list = self.lists[self.ListSelection]
        measure = self.emslinked[self.selectedMeasure]
        self.deleteEMListEntry(list, measure)
        self.updateEMListEntries()
        self.onMeasureSelected(False)        
        event.Skip()

    def OnBtnLinkMeasureButton(self, event):
        list = self.lists[self.ListSelection]
        measure = self.ems[self.cbMeasure.GetSelection()]
        self.addEMListEntry(list, measure)
        self.updateEMListEntries()
        self.onMeasureSelected(False) 
        event.Skip()

    def OnBtnManageMeasuresButton(self, event):
        dlg = DlgManageEM(self)
        dlg.ShowModal()
        self.updateEMListEntries()
        event.Skip()

    def OnLbMeasureListbox(self, event):
        self.selectedMeasure = self.lbMeasure.GetSelection()
        self.onMeasureSelected(True)
        event.Skip()
        
