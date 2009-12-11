#Boa:Dialog:DialogPOManageDB

import wx
from einstein.GUI.status import *
from dialogPOManageUO import DlgManageUO
from dialogPOManageTech import DlgManageTech
from dialogPOManageEM import DlgManageEM
from dialogPOManageTypical import DlgManageTP

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)


def create(parent):
    return Dialog1(parent)

[wxID_DIALOGPOMANAGEDB, wxID_DIALOGPOMANAGEDBBTNADDEMLIST, 
 wxID_DIALOGPOMANAGEDBBTNADDSECTOR, wxID_DIALOGPOMANAGEDBBTNADDSUBSECTOR, 
 wxID_DIALOGPOMANAGEDBBTNCHANGE, wxID_DIALOGPOMANAGEDBBTNCHANGESUBSECTOR, 
 wxID_DIALOGPOMANAGEDBBTNLINKMEASURE, wxID_DIALOGPOMANAGEDBBTNMANAGEMEASURES, 
 wxID_DIALOGPOMANAGEDBBTNMANAGETECHNOLOGIES, wxID_DIALOGPOMANAGEDBBTNMANAGETP, 
 wxID_DIALOGPOMANAGEDBBTNMANAGEUNITOPERATION, wxID_DIALOGPOMANAGEDBBTNREMOVE, 
 wxID_DIALOGPOMANAGEDBBTNREMOVEEMLIST, 
 wxID_DIALOGPOMANAGEDBBTNREMOVESUBSECTOR, 
 wxID_DIALOGPOMANAGEDBBTNUNLINKMEASURE, wxID_DIALOGPOMANAGEDBCBMEASURE, 
 wxID_DIALOGPOMANAGEDBCBSHOWALL, wxID_DIALOGPOMANAGEDBCBTECH, 
 wxID_DIALOGPOMANAGEDBCBTP, wxID_DIALOGPOMANAGEDBCBUO, 
 wxID_DIALOGPOMANAGEDBLBEMLIST, wxID_DIALOGPOMANAGEDBLBMEASURE, 
 wxID_DIALOGPOMANAGEDBLBSECTORS, wxID_DIALOGPOMANAGEDBLBSUBSECTORS, 
 wxID_DIALOGPOMANAGEDBSTATICBOX1, wxID_DIALOGPOMANAGEDBSTATICBOX2, 
 wxID_DIALOGPOMANAGEDBSTATICBOX5, wxID_DIALOGPOMANAGEDBSTATICBOX6, 
 wxID_DIALOGPOMANAGEDBSTATICTEXT1, wxID_DIALOGPOMANAGEDBSTATICTEXT2, 
 wxID_DIALOGPOMANAGEDBSTATICTEXT3, wxID_DIALOGPOMANAGEDBTCNACESECTOR, 
 wxID_DIALOGPOMANAGEDBTCNACESUBSECTOR, wxID_DIALOGPOMANAGEDBTCSECTORNAME, 
 wxID_DIALOGPOMANAGEDBTCSUBSECTOR, 
] = [wx.NewId() for _init_ctrls in range(35)]

class DialogPOManageDB(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOGPOMANAGEDB, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(1018, 719),
              style=wx.DEFAULT_DIALOG_STYLE,
              title=_U('Manage Process Optimisation Database'))
        self.SetClientSize(wx.Size(1010, 692))

        self.staticBox1 = wx.StaticBox(id=wxID_DIALOGPOMANAGEDBSTATICBOX1,
              label='1. Sectors', name='staticBox1', parent=self,
              pos=wx.Point(8, 8), size=wx.Size(504, 296), style=0)

        self.lbSectors = wx.ListBox(choices=[],
              id=wxID_DIALOGPOMANAGEDBLBSECTORS, name='lbSectors', parent=self,
              pos=wx.Point(16, 24), size=wx.Size(488, 208), style=0)
        self.lbSectors.Bind(wx.EVT_LISTBOX, self.OnLbSectorsListbox,
              id=wxID_DIALOGPOMANAGEDBLBSECTORS)

        self.btnAddSector = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNADDSECTOR,
              label='Add', name='btnAddSector', parent=self, pos=wx.Point(320,
              272), size=wx.Size(56, 23), style=0)
        self.btnAddSector.Bind(wx.EVT_BUTTON, self.OnBtnAddSectorButton,
              id=wxID_DIALOGPOMANAGEDBBTNADDSECTOR)

        self.btnRemove = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNREMOVE,
              label='Remove', name='btnRemove', parent=self, pos=wx.Point(384,
              272), size=wx.Size(56, 23), style=0)
        self.btnRemove.Bind(wx.EVT_BUTTON, self.OnBtnRemoveButton,
              id=wxID_DIALOGPOMANAGEDBBTNREMOVE)

        self.btnChange = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNCHANGE,
              label='Change', name='btnChange', parent=self, pos=wx.Point(448,
              272), size=wx.Size(56, 23), style=0)
        self.btnChange.Bind(wx.EVT_BUTTON, self.OnBtnChangeButton,
              id=wxID_DIALOGPOMANAGEDBBTNCHANGE)

        self.tcSectorName = wx.TextCtrl(id=wxID_DIALOGPOMANAGEDBTCSECTORNAME,
              name='tcSectorName', parent=self, pos=wx.Point(128, 240),
              size=wx.Size(376, 21), style=0, value='New Sector')

        self.staticBox2 = wx.StaticBox(id=wxID_DIALOGPOMANAGEDBSTATICBOX2,
              label='2. Subsectors', name='staticBox2', parent=self,
              pos=wx.Point(520, 8), size=wx.Size(480, 296), style=0)

        self.lbSubsectors = wx.ListBox(choices=[],
              id=wxID_DIALOGPOMANAGEDBLBSUBSECTORS, name='lbSubsectors',
              parent=self, pos=wx.Point(536, 24), size=wx.Size(456, 208),
              style=0)
        self.lbSubsectors.Bind(wx.EVT_LISTBOX, self.OnLbSubsectors,
              id=wxID_DIALOGPOMANAGEDBLBSUBSECTORS)

        self.tcSubsector = wx.TextCtrl(id=wxID_DIALOGPOMANAGEDBTCSUBSECTOR,
              name='tcSubsector', parent=self, pos=wx.Point(648, 240),
              size=wx.Size(344, 21), style=0, value='New Subsector')

        self.btnAddSubsector = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNADDSUBSECTOR,
              label='Add', name='btnAddSubsector', parent=self,
              pos=wx.Point(808, 272), size=wx.Size(56, 23), style=0)
        self.btnAddSubsector.Bind(wx.EVT_BUTTON, self.OnBtnAddSubsectorButton,
              id=wxID_DIALOGPOMANAGEDBBTNADDSUBSECTOR)

        self.btnRemoveSubsector = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNREMOVESUBSECTOR,
              label='Remove', name='btnRemoveSubsector', parent=self,
              pos=wx.Point(872, 272), size=wx.Size(56, 23), style=0)
        self.btnRemoveSubsector.Bind(wx.EVT_BUTTON,
              self.OnBtnRemoveSubsectorButton,
              id=wxID_DIALOGPOMANAGEDBBTNREMOVESUBSECTOR)

        self.btnChangeSubsector = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNCHANGESUBSECTOR,
              label='Change', name='btnChangeSubsector', parent=self,
              pos=wx.Point(936, 272), size=wx.Size(56, 23), style=0)
        self.btnChangeSubsector.Bind(wx.EVT_BUTTON,
              self.OnBtnChangeSubsectorButton,
              id=wxID_DIALOGPOMANAGEDBBTNCHANGESUBSECTOR)

        self.cbUO = wx.Choice(choices=[], id=wxID_DIALOGPOMANAGEDBCBUO,
              name='cbUO', parent=self, pos=wx.Point(112, 336),
              size=wx.Size(296, 21), style=0)
        self.cbUO.Bind(wx.EVT_CHOICE, self.OnCbUOChoice,
              id=wxID_DIALOGPOMANAGEDBCBUO)

        self.btnManageUnitOperation = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNMANAGEUNITOPERATION,
              label='Manage', name='btnManageUnitOperation', parent=self,
              pos=wx.Point(480, 336), size=wx.Size(60, 18), style=0)
        self.btnManageUnitOperation.Bind(wx.EVT_BUTTON,
              self.OnBtnManageUnitOperationButton,
              id=wxID_DIALOGPOMANAGEDBBTNMANAGEUNITOPERATION)

        self.btnManageTechnologies = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNMANAGETECHNOLOGIES,
              label='Manage', name='btnManageTechnologies', parent=self,
              pos=wx.Point(480, 600), size=wx.Size(60, 18), style=0)
        self.btnManageTechnologies.Bind(wx.EVT_BUTTON,
              self.OnBtnManageTechnologiesButton,
              id=wxID_DIALOGPOMANAGEDBBTNMANAGETECHNOLOGIES)

        self.staticBox6 = wx.StaticBox(id=wxID_DIALOGPOMANAGEDBSTATICBOX6,
              label='3. Linking', name='staticBox6', parent=self,
              pos=wx.Point(8, 312), size=wx.Size(552, 368), style=0)

        self.cbTech = wx.Choice(choices=[], id=wxID_DIALOGPOMANAGEDBCBTECH,
              name='cbTech', parent=self, pos=wx.Point(112, 600),
              size=wx.Size(360, 21), style=0)
        self.cbTech.Bind(wx.EVT_CHOICE, self.OnCbTechChoice,
              id=wxID_DIALOGPOMANAGEDBCBTECH)

        self.staticText1 = wx.StaticText(id=wxID_DIALOGPOMANAGEDBSTATICTEXT1,
              label='Typical Process', name='staticText1', parent=self,
              pos=wx.Point(32, 576), size=wx.Size(73, 13), style=0)

        self.lbEMList = wx.ListBox(choices=[], id=wxID_DIALOGPOMANAGEDBLBEMLIST,
              name='lbEMList', parent=self, pos=wx.Point(24, 360),
              size=wx.Size(520, 200), style=0)
        self.lbEMList.Bind(wx.EVT_LISTBOX, self.OnLbEMListListbox,
              id=wxID_DIALOGPOMANAGEDBLBEMLIST)

        self.staticText2 = wx.StaticText(id=wxID_DIALOGPOMANAGEDBSTATICTEXT2,
              label='Technology', name='staticText2', parent=self,
              pos=wx.Point(32, 600), size=wx.Size(55, 13), style=0)

        self.btnRemoveEMList = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNREMOVEEMLIST,
              label='Remove', name='btnRemoveEMList', parent=self,
              pos=wx.Point(480, 632), size=wx.Size(59, 23), style=0)
        self.btnRemoveEMList.Bind(wx.EVT_BUTTON, self.OnBtnRemoveEMListButton,
              id=wxID_DIALOGPOMANAGEDBBTNREMOVEEMLIST)

        self.btnAddEMList = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNADDEMLIST,
              label='Add', name='btnAddEMList', parent=self, pos=wx.Point(408,
              632), size=wx.Size(59, 23), style=0)
        self.btnAddEMList.Bind(wx.EVT_BUTTON, self.OnBtnAddEMListButton,
              id=wxID_DIALOGPOMANAGEDBBTNADDEMLIST)

        self.staticBox5 = wx.StaticBox(id=wxID_DIALOGPOMANAGEDBSTATICBOX5,
              label='4. Measures', name='staticBox5', parent=self,
              pos=wx.Point(568, 312), size=wx.Size(432, 368), style=0)

        self.lbMeasure = wx.ListBox(choices=[],
              id=wxID_DIALOGPOMANAGEDBLBMEASURE, name='lbMeasure', parent=self,
              pos=wx.Point(584, 336), size=wx.Size(400, 264), style=0)
        self.lbMeasure.Bind(wx.EVT_LISTBOX, self.OnLbMeasureListbox,
              id=wxID_DIALOGPOMANAGEDBLBMEASURE)

        self.cbMeasure = wx.Choice(choices=[],
              id=wxID_DIALOGPOMANAGEDBCBMEASURE, name='cbMeasure', parent=self,
              pos=wx.Point(584, 608), size=wx.Size(400, 21), style=0)

        self.btnUnlinkMeasure = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNUNLINKMEASURE,
              label='Unlink', name='btnUnlinkMeasure', parent=self,
              pos=wx.Point(912, 640), size=wx.Size(75, 23), style=0)
        self.btnUnlinkMeasure.Bind(wx.EVT_BUTTON, self.OnBtnUnlinkMeasureButton,
              id=wxID_DIALOGPOMANAGEDBBTNUNLINKMEASURE)

        self.btnLinkMeasure = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNLINKMEASURE,
              label='Link', name='btnLinkMeasure', parent=self,
              pos=wx.Point(832, 640), size=wx.Size(75, 23), style=0)
        self.btnLinkMeasure.Bind(wx.EVT_BUTTON, self.OnBtnLinkMeasureButton,
              id=wxID_DIALOGPOMANAGEDBBTNLINKMEASURE)

        self.btnManageMeasures = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNMANAGEMEASURES,
              label='Manage Measures', name='btnManageMeasures', parent=self,
              pos=wx.Point(584, 640), size=wx.Size(176, 23), style=0)
        self.btnManageMeasures.Bind(wx.EVT_BUTTON,
              self.OnBtnManageMeasuresButton,
              id=wxID_DIALOGPOMANAGEDBBTNMANAGEMEASURES)

        self.btnManageTP = wx.Button(id=wxID_DIALOGPOMANAGEDBBTNMANAGETP,
              label='Manage', name='btnManageTP', parent=self,
              pos=wx.Point(480, 576), size=wx.Size(60, 18), style=0)
        self.btnManageTP.Bind(wx.EVT_BUTTON, self.OnBtnManageTPButton,
              id=wxID_DIALOGPOMANAGEDBBTNMANAGETP)

        self.cbTP = wx.Choice(choices=[], id=wxID_DIALOGPOMANAGEDBCBTP,
              name='cbTP', parent=self, pos=wx.Point(112, 576),
              size=wx.Size(360, 21), style=0)
        self.cbTP.Bind(wx.EVT_CHOICE, self.OnCbTPChoice,
              id=wxID_DIALOGPOMANAGEDBCBTP)

        self.staticText3 = wx.StaticText(id=wxID_DIALOGPOMANAGEDBSTATICTEXT3,
              label='UnitOperation', name='staticText3', parent=self,
              pos=wx.Point(24, 336), size=wx.Size(67, 13), style=0)

        self.tcNACESector = wx.TextCtrl(id=wxID_DIALOGPOMANAGEDBTCNACESECTOR,
              name='tcNACESector', parent=self, pos=wx.Point(16, 240),
              size=wx.Size(108, 21), style=0, value='NACE')

        self.tcNACESubsector = wx.TextCtrl(id=wxID_DIALOGPOMANAGEDBTCNACESUBSECTOR,
              name='tcNACESubsector', parent=self, pos=wx.Point(536, 240),
              size=wx.Size(108, 21), style=0, value='NACE')

        self.cbShowAll = wx.CheckBox(id=wxID_DIALOGPOMANAGEDBCBSHOWALL,
              label='Show all', name='cbShowAll', parent=self,
              pos=wx.Point(416, 336), size=wx.Size(64, 18), style=0)
        self.cbShowAll.SetValue(True)
        self.cbShowAll.Bind(wx.EVT_CHECKBOX, self.OnCbShowAllCheckbox,
              id=wxID_DIALOGPOMANAGEDBCBSHOWALL)

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
        self.tcNACESubsector.Enabled = bool  
        self.onSubsectorSelected(False)
    
    def onSubsectorSelected(self,bool):
        self.btnChangeSubsector.Enabled = bool
        self.btnRemoveSubsector.Enabled = bool
        self.cbUO.Enabled = bool
        self.cbTech.Enabled = bool
        self.cbTP.Enabled = bool
        self.btnAddEMList.Enabled = bool
        self.btnRemoveEMList.Enabled = bool
        self.lbEMList.Enabled = bool
        self.cbShowAll.Enabled = bool
        
        if (bool):
            self.updateUO()  
            self.updateEMList()
            self.updateTP()  
            self.updateTech()          
 
            
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
            self.lbSectors.Append(sector[2]+"|"+sector[1])

    #DATABASE------------------------------------------------------------------------
    def loadSectors(self):         
        query = """SELECT IDSector,Name,NACE FROM posector"""
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.sectors = results 
        else:
            self.sectors = []
            
    def addSector(self,name,nace):
        query = """INSERT INTO posector (Name,NACE) VALUES (\"%s\",\"%s\")"""
        query = query % (name,nace)
        Status.DB.sql_query(query)
    
    def deleteSector(self,index):                
        sector = self.sectors[index]
        
        query = """SELECT * FROM posubsector WHERE SectorID = %s"""
        query = query % sector[0]
        result = Status.DB.sql_query(query)
        
        if (len(result)==0):
            query = """DELETE FROM posector WHERE IDSector = %s"""
            query = query % sector[0]
            Status.DB.sql_query(query)
        else:
            wx.MessageBox("Could not delete. Sector is in use.")
        
    def changeSector(self,index,name,nace):
        sector = self.sectors[index]
        query = """UPDATE posector SET Name = \"%s\" , NACE = \"%s\" WHERE IDSector = %s"""
        query = query % (name,nace,sector[0])
        Status.DB.sql_query(query)

    #BUTTONS-------------------------------------------------------------------------
    def OnLbSectorsListbox(self, event):
        self.sectorSelection = self.lbSectors.GetSelection()
        sector = self.sectors[self.sectorSelection]        
        self.tcSectorName.SetValue(sector[1])
        self.tcNACESector.SetValue(sector[2])
        self.onSectorSelected(True)
        self.updateSubsectors()
        event.Skip()

    def OnBtnAddSectorButton(self, event):
        self.addSector(self.tcSectorName.GetValue(),self.tcNACESector.GetValue())
        self.updateSectors()
        event.Skip()

    def OnBtnRemoveButton(self, event):
        self.onSectorSelected(False)
        self.deleteSector(self.sectorSelection)
        self.updateSectors()
        event.Skip()

    def OnBtnChangeButton(self, event):
        self.onSectorSelected(False)
        self.changeSector(self.sectorSelection,self.tcSectorName.GetValue(),self.tcNACESector.GetValue())
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
            self.lbSubsectors.Append(subsector[2]+"|"+subsector[1])

    #DATABASE------------------------------------------------------------------------
    def loadSubsectors(self):         
        query = """SELECT IDSubsector,Name,NACE FROM posubsector WHERE SectorID = %s"""
        sector = self.sectors[self.sectorSelection]
        query = query % sector[0] 
        
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.subsectors = results 
        else:
            self.subsectors = []
            
    def addSubsector(self,name,nace):
        sector = self.sectors[self.sectorSelection]
        query = """INSERT INTO posubsector (Name,NACE,SectorID) VALUES (\"%s\",\"%s\","%s")"""
        query = query % (name,nace,sector[0])
        Status.DB.sql_query(query)
    
    def deleteSubsector(self,subsector):            
        query = """DELETE FROM poemlist WHERE SubsectorID = %s"""
        query = query % subsector[0]
        Status.DB.sql_query(query)
        
        query = """DELETE FROM poSubsector WHERE IDSubsector = %s"""
        query = query % subsector[0]
        Status.DB.sql_query(query)
        
    def changeSubsector(self,subsector,name,nace):      
        query = """UPDATE posubsector SET Name = \"%s\", NACE = \"%s\" WHERE IDSubsector = %s"""
        query = query % (name,nace,subsector[0])
        Status.DB.sql_query(query)

    #BUTTONS-------------------------------------------------------------------------
    def OnLbSubsectors(self, event):
        self.subsectorSelection = self.subsectors[self.lbSubsectors.GetSelection()]      
        self.tcSubsector.SetValue(self.subsectorSelection[1])
        self.tcNACESubsector.SetValue(self.subsectorSelection[2])
        self.onSubsectorSelected(True)        
        event.Skip()

    def OnBtnAddSubsectorButton(self, event):
        self.addSubsector(self.tcSubsector.GetValue(),self.tcNACESubsector.GetValue())
        self.updateSubsectors()
        event.Skip()

    def OnBtnRemoveSubsectorButton(self, event):
        self.onSubsectorSelected(False)
        self.deleteSubsector(self.subsectorSelection)
        self.updateSubsectors()
        event.Skip()

    def OnBtnChangeSubsectorButton(self, event):
        self.onSubsectorSelected(False)
        self.changeSubsector(self.subsectorSelection,self.tcSubsector.GetValue(),self.tcNACESubsector.GetValue())
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
        if (self.cbShowAll.GetValue()):
            uo.loadUO()
        else:
            uo.loadUOExisting(self.subsectorSelection[0])
        self.cbUO.Clear()
        self.uos = uo.uos
        for unit in self.uos:
            self.cbUO.Append(unit[2]+"|"+unit[1])
        
        bool = False
        if len(self.uos)>0:
            bool = True
            self.cbUO.SetSelection(0)
            self.selectedUO = self.uos[0]
        
        self.cbUO.Enabled = bool     
        self.cbTech.Enabled = bool
        self.cbTP.Enabled = bool
        self.btnAddEMList.Enabled = bool
        self.btnRemoveEMList.Enabled = bool             

#####################################################################################
# Typical Process
#####################################################################################

    #GUI-----------------------------------------------------------------------------
    def updateTP(self):
        self.loadTP()
        self.cbTP.Clear()
        for tp in self.tps:
            self.cbTP.Append(tp[2]+"|"+tp[1])
            
        if len(self.tps)>0:
            self.cbTP.SetSelection(0)
            self.selectedTP = self.tps[0]
        else:
            self.cbTP.Enabled = False        

    #DATABASE------------------------------------------------------------------------
    def loadTP(self):         
        query = """SELECT IDTypicalProcess,Name,Code FROM potypicalprocess"""
               
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.tps = results 
        else:
            self.tps = []               

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
        tech = DlgManageTech(self)
        tech.loadTech()
        self.cbTech.Clear()
        self.techs = tech.techs
        for tech in self.techs:
            self.cbTech.Append(tech[2]+"|"+tech[1])
        
        if len(self.techs)>0:
            self.cbTech.SetSelection(0)
            self.selectedTech = self.techs[0]
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
        query = """SELECT list.IDEMList, tp.Name, tech.Name FROM poemlist as list, potypicalprocess as tp, potech as tech 
                   WHERE tp.IDTypicalProcess = list.TypicalProcessID AND tech.IDtechnology = list.TechnologyID 
                         AND list.UnitOperationID = %s AND list.SubsectorID = %s"""
       
        query = query % (self.selectedUO[0],self.subsectorSelection[0])     
        results = Status.DB.sql_query(query)
        if len(results)>0:
            if (type(results[0])!=type(())):
                results = [ results ]
            self.lists = results 
        else:
            self.lists = []

    def addEMList(self):
        query = """INSERT INTO poemlist (SubsectorID,UnitOperationID,TechnologyID,TypicalProcessID) VALUES (%s,%s,%s,%s)"""
        query = query % (self.subsectorSelection[0],self.selectedUO[0],self.selectedTech[0],self.selectedTP[0]) 
        Status.DB.sql_query(query)    
    
    def deleteEMList(self,list):
        query = """DELETE FROM poemlist WHERE IDEMList = %s"""
        query = query % (list[0]) 
        Status.DB.sql_query(query)
        query = """DELETE FROM poemlistEntry WHERE EMListID = %s"""
        query = query % (list[0]) 
        Status.DB.sql_query(query)         


    def OnLbEMListListbox(self, event):
        self.ListSelection = self.lbEMList.GetSelection()
        self.onListSelected(True)        
        event.Skip()

    def OnBtnAddEMListButton(self, event):
        self.addEMList()
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
                   FROM poefficiencymeasure as em, poemlistentry as entry 
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
        query = """INSERT INTO poemlistentry (EMListID,EfficiencyMeasureID) VALUES (%s,%s)"""
        query = query % (list[0],measure[0])
        Status.DB.sql_query(query)  
    
    def deleteEMListEntry(self,list,measure):
        query = """DELETE FROM poemlistentry WHERE EMListID = %s AND EfficiencyMeasureID = %s"""
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

    def OnBtnManageTPButton(self, event):
        dlg = DlgManageTP(self)
        dlg.ShowModal()
        event.Skip()

    def OnCbUOChoice(self, event):
        self.selectedUO = self.uos[self.cbUO.GetSelection()]
        self.updateEMList()
        event.Skip()

    def OnCbTechChoice(self, event):
        self.selectedTech = self.techs[self.cbTech.GetSelection()]
        event.Skip()

    def OnCbTPChoice(self, event):
        self.selectedTP = self.tps[self.cbTP.GetSelection()]
        event.Skip()

    def OnCbShowAllCheckbox(self, event):
        self.updateUO()
        event.Skip()
        
