#   Hans Schweiger      28/11/2008
#   Changes:
#
#   28/11/2008: HS  function str() in result.name eliminated -> is unicode !!!

#Boa:FramePanel:panelResult1

import wx
import wx.grid
from GUITools import *
from einstein.modules.calculationTCA import *

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

[wxID_PANELRESULT1, wxID_PANELRESULT1BTNADDPROPOSAL, 
 wxID_PANELRESULT1BTNREMOVEPROPOSAL, wxID_PANELRESULT1CBPROPOSALS, 
 wxID_PANELRESULT1GRID, wxID_PANELRESULT1STATICBOX1, 
] = [wx.NewId() for _init_ctrls in range(6)]

class panelResult1(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELRESULT1, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(730, 350),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(722, 323))
        
        self.grid = wx.grid.Grid(id=wxID_PANELRESULT1GRID, name='grid',
              parent=self, pos=wx.Point(8, 8), size=wx.Size(704, 170), style=0)
        self.grid.EnableEditing(False)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGridGridCellLeftClick)

        self.cbProposals = wx.Choice(choices=[],
              id=wxID_PANELRESULT1CBPROPOSALS, name='cbProposals', parent=self,
              pos=wx.Point(24, 264), size=wx.Size(160, 21), style=0)
        self.cbProposals.Bind(wx.EVT_CHOICE, self.OnCbProposalsChoice,
              id=wxID_PANELRESULT1CBPROPOSALS)

        self.staticBox1 = wx.StaticBox(id=wxID_PANELRESULT1STATICBOX1,
              label='Choose the proposal(s) to be additionaly displayed:',
              name='staticBox1', parent=self, pos=wx.Point(8, 240),
              size=wx.Size(704, 64), style=0)

        self.btnAddProposal = wx.Button(id=wxID_PANELRESULT1BTNADDPROPOSAL,
              label='Add', name='btnAddProposal', parent=self,
              pos=wx.Point(192, 264), size=wx.Size(75, 23), style=0)
        self.btnAddProposal.Bind(wx.EVT_BUTTON, self.OnBtnAddProposalButton,
              id=wxID_PANELRESULT1BTNADDPROPOSAL)

        self.btnRemoveProposal = wx.Button(id=wxID_PANELRESULT1BTNREMOVEPROPOSAL,
              label='Remove', name='btnRemoveProposal', parent=self,
              pos=wx.Point(272, 264), size=wx.Size(75, 23), style=0)
        self.btnRemoveProposal.Bind(wx.EVT_BUTTON,
              self.OnBtnRemoveProposalButton,
              id=wxID_PANELRESULT1BTNREMOVEPROPOSAL)

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)
        self.selectedRow = None

        self.display()

    def __init_custom_ctrls(self, prnt):
#Grid-------------------------------------------------------------------------
        self.rows = 5
        self.cols = 1
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid.CreateGrid(self.rows,self.cols)

        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(25)
        self.grid.SetRowLabelSize(250)
        self.grid.SetDefaultColSize(100)
        self.grid.SetColSize(0,150)
        
        self.grid.EnableEditing(False)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _U("Proposal 1"))
        
        self.grid.SetRowLabelValue(0, _U("Total investment capital (EUR)"))
        self.grid.SetRowLabelValue(1, _U("Effective investment capital (EUR)"))
        self.grid.SetRowLabelValue(2, _U("Benefit cost ratio"))
        self.grid.SetRowLabelValue(3, _U("Payback period (years)"))
        self.grid.SetRowLabelValue(4, _U("MIRR at final year (%)"))
        
        self.grid.SetBackgroundColour(wx.Colour(255, 0, 0))
        #choices--------------------------------------------------------------------------------
    
    def display(self):   
        if (Status.mod.moduleTCA.result!=None):
            self.cbProposals.Clear()
            for result in Status.mod.moduleTCA.result:            
                self.cbProposals.Append(result.name)
            self.cbProposals.SetSelection(0)
        self.updateButtons()  
        self.updateGrid()    

    def updateGrid(self):
        if (Status.mod.moduleTCA.result!=None):
            
            cols = self.grid.GetNumberCols()
            if (cols>0):
                self.grid.DeleteCols(0,cols)
            
            num = 0
            for result in Status.mod.moduleTCA.result:
                if (result.display == 1):
                    num+=1
                             
            self.cols = num  
            if (num>0):
                self.grid.AppendCols(num)
            self.updateGridAttributes()
            
            count = 0
            for result in Status.mod.moduleTCA.result:
                if (result.display == 1):    
                    try:                
                        if (result.ResultPresent == True):
                            self.grid.SetColLabelValue(count,  result.name)
                            str_pp = "%.2f" % result.PP
                            str_mirr = "%.2f" % (result.mirr[len(result.mirr)-1]*100)
                            str_TIC = "%.0f" % result.TIC
                            str_EIC = "%.0f" % result.EIC
                            str_BCR = "%.2f" % (result.bcr[len(result.bcr)-1])
                                       
                            self.grid.SetCellValue(0, count, str_TIC)
                            self.grid.SetCellValue(1, count, str_EIC)
                            self.grid.SetCellValue(2, count, str_BCR)
                            self.grid.SetCellValue(3, count, str_pp)
                            self.grid.SetCellValue(4, count, str_mirr)
                        else:
                            self.grid.SetColLabelValue(count,  str(result.name))
                            self.grid.SetCellValue(0, count, _U("No Result"))
                            self.grid.SetCellValue(1, count, _U("No Result"))
                            self.grid.SetCellValue(2, count, _U("No Result"))
                            self.grid.SetCellValue(3, count, _U("No Result"))
                            self.grid.SetCellValue(4, count, _U("No Result"))
                    except:
                            self.grid.SetColLabelValue(count,  "Invalid Proposal")
                            self.grid.SetCellValue(0, count, _U("ERROR"))
                            self.grid.SetCellValue(1, count, _U("ERROR"))
                            self.grid.SetCellValue(2, count, _U("ERROR"))
                            self.grid.SetCellValue(3, count, _U("ERROR"))
                            self.grid.SetCellValue(4, count, _U("ERROR"))
                    count +=1  
                       
        
    def updateGridAttributes(self):
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))
        for r in range(self.rows):
            self.grid.SetRowSize(r,25)
            self.grid.SetRowAttr(r, attr)                    
           
        
        
            
    def OnGridGridCellLeftClick(self, event):
        event.Skip()

    def OnBtnAddProposalButton(self, event):
        try:
            index = self.cbProposals.GetSelection()
            Status.mod.moduleTCA.result[index].display = 1
        except:
            pass
        self.display()
        event.Skip()     
    
    def updateButtons(self):
        try:            
            index = self.cbProposals.GetSelection()
            if (Status.mod.moduleTCA.result[index].display == 0):
                self.btnAddProposal.Enabled = True
                self.btnRemoveProposal.Enabled  = False
            else:
                self.btnAddProposal.Enabled = False
                self.btnRemoveProposal.Enabled  = True
        except:
            pass
        
    def OnBtnRemoveProposalButton(self, event):
        try:
            index = self.cbProposals.GetSelection()
            Status.mod.moduleTCA.result[index].display = 0
        except:
            pass
        self.display()
        event.Skip()   

    def OnCbProposalsChoice(self, event):       
        self.updateButtons()
        event.Skip()
        

