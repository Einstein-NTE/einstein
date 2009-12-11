#Boa:FramePanel:PanelPO
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    panelPO: Process opti.
#
#
#==============================================================================
#
#    Version No.: 0.01
#       Created by:          Florian Joebstl 25/09/2008  
#                 
#------------------------------------------------------------------------------
#    (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#    http://www.energyxperts.net/
#
#    This program is free software: you can redistribute it or modify it under
#    the terms of the GNU general public license as published by the Free
#    Software Foundation (www.gnu.org).
#
#==============================================================================
import wx
import wx.html
import webbrowser
from einstein.GUI.status import Status

from GUITools import *
from dialogPOManageDB import DialogPOManageDB

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)


[wxID_PANELPO, wxID_PANELPOBTNMANAGEDB, wxID_PANELPOBTNNEXT, 
 wxID_PANELPOBTNPREV, wxID_PANELPOCBSECTOR, wxID_PANELPOCBSUBSECTOR, 
 wxID_PANELPOCBTYPICALPROCESS, wxID_PANELPOCBUNIT, wxID_PANELPOHTMLWND, 
 wxID_PANELPOLBTECH, wxID_PANELPOSTATICBOX1, wxID_PANELPOSTATICTEXT1, 
 wxID_PANELPOSTATICTEXT3, wxID_PANELPOSTATICTEXT4, wxID_PANELPOSTATICTEXT5, 
 wxID_PANELPOSTATICTEXT6, 
] = [wx.NewId() for _init_ctrls in range(16)]



class wxHTML(wx.html.HtmlWindow):
    def OnLinkClicked(self,link):
        webbrowser.open(link.GetHref())


class PanelPO(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELPO, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(800, 616),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(792, 589))

        self.staticBox1 = wx.StaticBox(id=wxID_PANELPOSTATICBOX1,
              label='Process Optimisation', name='staticBox1', parent=self,
              pos=wx.Point(8, 6), size=wx.Size(760, 546), style=0)

        self.btnNext = wx.Button(id=wxID_PANELPOBTNNEXT, label='>>>',
              name='btnNext', parent=self, pos=wx.Point(696, 560),
              size=wx.Size(75, 23), style=0)
        self.btnNext.Bind(wx.EVT_BUTTON, self.OnBtnNextButton,
              id=wxID_PANELPOBTNNEXT)

        self.btnPrev = wx.Button(id=wxID_PANELPOBTNPREV, label='<<<',
              name='btnPrev', parent=self, pos=wx.Point(8, 560),
              size=wx.Size(75, 23), style=0)
        self.btnPrev.Bind(wx.EVT_BUTTON, self.OnBtnPrevButton,
              id=wxID_PANELPOBTNPREV)

        self.staticText1 = wx.StaticText(id=wxID_PANELPOSTATICTEXT1,
              label=_U('Technologies:'), name='staticText1', parent=self,
              pos=wx.Point(496, 184), size=wx.Size(66, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID_PANELPOSTATICTEXT3,
              label='Sector:', name='staticText3', parent=self,
              pos=wx.Point(496, 24), size=wx.Size(35, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_PANELPOSTATICTEXT4,
              label='Subsector:', name='staticText4', parent=self,
              pos=wx.Point(496, 64), size=wx.Size(52, 13), style=0)

        self.staticText5 = wx.StaticText(id=wxID_PANELPOSTATICTEXT5,
              label='Unit Operation:', name='staticText5', parent=self,
              pos=wx.Point(496, 104), size=wx.Size(74, 13), style=0)

        self.staticText6 = wx.StaticText(id=wxID_PANELPOSTATICTEXT6,
              label='Typical Process:', name='staticText6', parent=self,
              pos=wx.Point(496, 144), size=wx.Size(77, 13), style=0)

        self.cbSector = wx.Choice(choices=[], id=wxID_PANELPOCBSECTOR,
              name='cbSector', parent=self, pos=wx.Point(496, 40),
              size=wx.Size(264, 19), style=0)
        self.cbSector.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))
        self.cbSector.Bind(wx.EVT_CHOICE, self.OnCbSectorChoice,
              id=wxID_PANELPOCBSECTOR)

        self.cbSubsector = wx.Choice(choices=[], id=wxID_PANELPOCBSUBSECTOR,
              name='cbSubsector', parent=self, pos=wx.Point(496, 80),
              size=wx.Size(264, 19), style=0)
        self.cbSubsector.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))
        self.cbSubsector.Bind(wx.EVT_CHOICE, self.OnCbSubsectorChoice,
              id=wxID_PANELPOCBSUBSECTOR)

        self.cbUnit = wx.Choice(choices=[], id=wxID_PANELPOCBUNIT,
              name='cbUnit', parent=self, pos=wx.Point(496, 120),
              size=wx.Size(264, 19), style=0)
        self.cbUnit.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))
        self.cbUnit.Bind(wx.EVT_CHOICE, self.OnCbUnitChoice,
              id=wxID_PANELPOCBUNIT)

        self.cbTypicalProcess = wx.Choice(choices=[],
              id=wxID_PANELPOCBTYPICALPROCESS, name='cbTypicalProcess',
              parent=self, pos=wx.Point(496, 160), size=wx.Size(264, 19),
              style=0)
        self.cbTypicalProcess.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))
        self.cbTypicalProcess.Bind(wx.EVT_CHOICE, self.OnCbTypicalProcessChoice,
              id=wxID_PANELPOCBTYPICALPROCESS)

        self.btnManageDB = wx.Button(id=wxID_PANELPOBTNMANAGEDB,
              label=_U('Manage Database'), name='btnManageDB', parent=self,
              pos=wx.Point(568, 560), size=wx.Size(120, 23), style=0)
        self.btnManageDB.Bind(wx.EVT_BUTTON, self.OnBtnManageDBButton,
              id=wxID_PANELPOBTNMANAGEDB)

        self.htmlWnd = wx.html.HtmlWindow(id=wxID_PANELPOHTMLWND,
              name='htmlWnd', parent=self, pos=wx.Point(16, 32),
              size=wx.Size(472, 512), style=wx.html.HW_SCROLLBAR_AUTO)

        self.lbTech = wx.CheckListBox(choices=[], id=wxID_PANELPOLBTECH,
              name='lbTech', parent=self, pos=wx.Point(496, 200),
              size=wx.Size(256, 344), style=0)
        self.lbTech.Bind(wx.EVT_CHECKLISTBOX, self.OnLbTechChecklistbox,
              id=wxID_PANELPOLBTECH)
        self.lbTech.Bind(wx.EVT_LISTBOX, self.OnLbTechListbox,
              id=wxID_PANELPOLBTECH)

    def __init_custom_ctrls(self,prnt):
        self.staticBox1.SetForegroundColour(TITLE_COLOR)
        self.staticBox1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False,'Tahoma'))

    def __init__(self, parent, main, id, pos, size, style, name):
        self.main = main
        self.mod = Status.mod.modulePO
        self.shortName = _U("PO")
        self.description = _U("")               
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)

    def display(self):
        self.mod.updatePanel()
        self.__updateCBSector()
        self.__updateCBSubsector()     
        self.__updateCBUnitoperation()  
        self.__updateCBTypicalprocess()    
        self.__updateCBTech()  
        self.__updateMeasures()                         
                                   
    def __updateCBSector(self):
        self.cbSector.Clear()
        for sector in self.mod.sectors:
            self.cbSector.Append(sector[1])
        if (self.mod.sectorSelection!=None):
            self.cbSector.SetSelection(self.mod.sectorSelection)
             
    def __updateCBSubsector(self):
        self.cbSubsector.Clear()
        if (len(self.mod.subsectors)==0):
            self.cbSubsector.Enabled = False
        else:
            self.cbSubsector.Enabled = True            
            for subsector in self.mod.subsectors:
                self.cbSubsector.Append(subsector[1])
            if (self.mod.subsectorSelection!=None):
                self.cbSubsector.SetSelection(self.mod.subsectorSelection)
                   
    def __updateCBUnitoperation(self):
        self.cbUnit.Clear()
        if (len(self.mod.unitoperations)==0):
            self.cbUnit.Enabled = False
        else:
            self.cbUnit.Enabled= True            
            for unit in self.mod.unitoperations:
                self.cbUnit.Append(unit[1])
            if (self.mod.unitoperationSelection!=None):
                self.cbUnit.SetSelection(self.mod.unitoperationSelection)
                  
    def __updateCBTypicalprocess(self):
        self.cbTypicalProcess.Clear()    
        if (len(self.mod.typicalprocess)==0):
            self.cbTypicalProcess.Enabled = False
        else:
            self.cbTypicalProcess.Enabled = True           
            for tp in self.mod.typicalprocess:
                self.cbTypicalProcess.Append(tp[1])
            if (self.mod.typicalprocessSelection!=None):
                self.cbTypicalProcess.SetSelection(self.mod.typicalprocessSelection)
                  
    def __updateCBTech(self):
        self.lbTech.Clear()
        if (len(self.mod.techs)==0):
            self.lbTech.Enabled = False
        else:
            self.lbTech.Enabled = True
            for tech in self.mod.techs:
                self.lbTech.Append(tech[2])
            for index in self.mod.techSelection:                
                self.lbTech.Check(index,True)
                
    def __updateMeasures(self):
        TEXT = "<center> <img src = \"img/einstein_em.png\"><br>"
        TEXT +=self.cbSector.GetStringSelection()+"<br>"
        TEXT +=self.cbSubsector.GetStringSelection()+"</center>"
        TEXT +="<hr><b>Unit Operation: </b>"+self.cbUnit.GetStringSelection()+"<br>"
        TEXT +="<br><b>Typical process: </b>"+self.cbTypicalProcess.GetStringSelection()
                
        TEXT +="<br><br><b>Listing measures for technology:</b>"
        TEXT +="<ul>"
        
        for techindex in self.mod.techSelection:
            tech = self.mod.techs[techindex]  
            TEXT+="<li>"+tech[2]+"</li>"
  
        TEXT +="</ul>"
                        
        TEXT +="<hr>"
        for measure in self.mod.measures:
            try:      
                print "bla"          
                TEXT+='<h3>'+str(measure[0])+'</h3>'         
                TEXT+='<p>'+str(measure[1])+'</p>'
            except:
                TEXT+='<h3>'+str("ERROR")+'</h3>'         
                TEXT+='<p>'+str("Could not read measure. Please check character encoding.")+'</p>'
                
        self.htmlWnd.SetPage(TEXT)
          
                        
    def OnBtnManageDBButton(self, event):
        dlg = DialogPOManageDB(self)
        dlg.ShowModal()
        event.Skip()

    def OnBtnReportButton(self, event):
        event.Skip()

    def OnLbTechListbox(self, event):
        self.mod.techSelection = self.lbTech.GetSelection()
        self.display()
        event.Skip()

    def OnCbSectorChoice(self, event):        
        self.mod.sectorSelection = self.cbSector.GetSelection()
        self.mod.subsectorSelection = None
        self.mod.unitoperationSelection = None
        self.mod.typicalprocessSelection = None
        self.mod.techSelection = []
        self.display()
        event.Skip()

    def OnCbSubsectorChoice(self, event):
        self.mod.subsectorSelection = self.cbSubsector.GetSelection()
        self.mod.unitoperationSelection = None
        self.mod.typicalprocessSelection = None
        self.mod.techSelection = []
        self.display()
        event.Skip()

    def OnCbUnitChoice(self, event):
        self.mod.unitoperationSelection = self.cbUnit.GetSelection()
        self.mod.typicalprocessSelection = None
        self.mod.techSelection = []
        self.display()
        event.Skip()

    def OnCbTypicalProcessChoice(self, event):
        self.mod.typicalprocessSelection = self.cbTypicalProcess.GetSelection()
        self.mod.techSelection = []      
        self.display()
        event.Skip()

    def OnLbTechChecklistbox(self, event):
        self.mod.techSelection = []
        for i in range(0,len(self.mod.techs)):
            if (self.lbTech.IsChecked(i)):
                self.mod.techSelection.append(i)        
        self.display()
        event.Skip()

    def OnBtnNextButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHX, select=True)
        event.Skip()

    def OnBtnPrevButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qA, select=True)
        event.Skip()
