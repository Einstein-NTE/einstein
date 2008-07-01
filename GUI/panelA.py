#Boa:FramePanel:PanelA
# -*- coding: cp1252 -*-
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	Panel Design of Alternative Proposals
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	
#
#==============================================================================
#
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	    03/04/2008
#	Revised by:    
#                           Tom Sobota              05/04/2008
#                           Hans Schweiger          15/04/2008
#                           Stoyan Danov            18/06/2008
#
#       Revised by:         Tom Sobota  28/04/2008
#
#       Changes to previous version:
#       05/04/08    changed call to popup1 in OnButtonpageHPAddButton
#                   slight change to OK and Cancel buttons, to show the right icons
#       15/04/08 HS copy and delete buttons added. event handler "Generate New" linked
#       28/04/2008  added 'draw' to method display
#       18/06/2008 SD: change to translatable text _(...)
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
import wx.grid
from einstein.GUI.status import Status

import einstein.modules.matPanel as Mp
from einstein.GUI.dialogA import *
from einstein.GUI.dialogOK import *


[wxID_PANELA, wxID_PANELABUTTONPAGEABACK, wxID_PANELABUTTONPAGEACANCEL, 
 wxID_PANELABUTTONPAGEAFWD, wxID_PANELABUTTONPAGEAOK, wxID_PANELACOPYPROPOSAL, 
 wxID_PANELADELETEPROPOSAL, wxID_PANELADESIGNHC, wxID_PANELADESIGNHX, 
 wxID_PANELADESIGNPA, wxID_PANELADESIGNPO, wxID_PANELAGENERATENEW, 
 wxID_PANELAGRID, wxID_PANELAPANELAFIG, wxID_PANELAST1PAGEA, 
 wxID_PANELAST3PAGEA, 
] = [wx.NewId() for _init_ctrls in range(16)]

# constants
#
ORANGE = '#FF6000'
LIGHTGREY = '#F8F8F8'
WHITE = '#FFFFFF'
DARKGREY = '#000060'

GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = DARKGREY     # specified as hex #RRGGA
GRID_LETTER_COLOR2 = WHITE     # specified as hex #RRGGA
GRID_BACKGROUND_COLOR = LIGHTGREY # idem
GRID_BACKGROUND_COLOR2 = ORANGE # idem
GRAPH_BACKGROUND_COLOR = WHITE # idem
TITLE_COLOR = ORANGE

COLNO = 6
MAXROWS = 20

#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		
    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)

    gdata = Status.int.GData["A Table"]

    try: (rows,cols) = gdata.shape
    except: (rows,cols) = (0,COLNO)
    NAlternatives = rows - 2

    if rows >= 2:
        N0 = _("present state")
        E0 = gdata[1][4]
        C0 = gdata[1][5]
        print "PanelA (drawFigure): present state data E= %s C= %s"%(E0,C0)

        self.subplot.plot([C0],
                      [E0],
                      'rs-', label=N0, linewidth=2)

        for i in range(NAlternatives):
            Ei = gdata[i+2][4]
            Ci = gdata[i+2][5]
            Ni = gdata[i+2][1]
            self.subplot.plot([Ci],
                              [Ei],
                              'go',  label=Ni)
#    self.subplot.axis(axis)


#XXXXXX To be checked how to bring x/y- labels to this plot ...
#    self.figure.xlabel('time (s)')
#    self.figure.ylabel('current (nA)')
#    self.figure.title('Gaussian colored noise')

    self.subplot.legend()

#==============================================================================
#==============================================================================
class PanelA(wx.Panel):
#==============================================================================
#==============================================================================

    def __init__(self, parent, main):
        self._init_ctrls(parent)
	keys = ['A Table','A Plot']
	self.keys = keys
	self.main = main
        self.mod = Status.mod.moduleA
        self.shortName = _("new alternative")
        self.description = _("describe shortly the main differential features of the new alternative")
        self.ANo = Status.ANo
#==============================================================================
#   graphic: Cumulative heat demand by hours
#==============================================================================
        labels_column = 2
        ignoredrows = []
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : 'Some title',           # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelAFig,
                            wx.Panel,
                            drawFigure,
                            paramList)

        #
        # additional widgets setup
        # here, we modify some widgets attributes that cannot be changed
        # directly by Boa. This cannot be done in _init_ctrls, since that
        # method is rewritten by Boa each time.
        #
        # data cell attributes
        attr = wx.grid.GridCellAttr()
        attr.SetTextColour(GRID_LETTER_COLOR)
        attr.SetBackgroundColour(GRID_BACKGROUND_COLOR)
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL))

        # data cell attributes for present state 
        attr2 = wx.grid.GridCellAttr()
        attr2.SetTextColour(GRID_LETTER_COLOR2)
        attr2.SetBackgroundColour(GRID_BACKGROUND_COLOR2)
        attr2.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.grid.CreateGrid(MAXROWS, COLNO)

        self.grid.EnableGridLines(True)
        self.grid.SetDefaultRowSize(30)
        self.grid.SetRowLabelSize(0)
        self.grid.SetColLabelSize(60)
        self.grid.SetDefaultColSize(80)
        self.grid.SetColSize(0,40)
        self.grid.SetColSize(1,160)
        self.grid.SetColSize(2,330)
        self.grid.SetColSize(3,40)
        
        self.grid.EnableEditing(False)
        self.grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.grid.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.grid.SetColLabelValue(0, _("No."))
        self.grid.SetColLabelValue(1, _("Name"))
        self.grid.SetColLabelValue(2, _("Description"))
        self.grid.SetColLabelValue(3, _("State"))
        self.grid.SetColLabelValue(4, _("Primary energy\nconsumption\n[MWh/a]"))
        self.grid.SetColLabelValue(5, _("Total annual\nenergy cost\n[€/a]"))
        #
        # copy values from dictionary to grid
        #
        for r in range(MAXROWS):
            if r ==1:
                self.grid.SetRowAttr(r,attr2)
            else:
                self.grid.SetRowAttr(r, attr)
            for c in range(COLNO):
#                self.grid.SetCellValue(r, c, "")
                if c <= labels_column:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.grid.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.grid.SetGridCursor(0, 0)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELA, name='PanelA', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(808, 634), style=0)
        self.SetClientSize(wx.Size(800, 600))

#..............................................................................
# grid for displaying alternatives

        self.box1 = wx.StaticBox(self, -1, _("design of alternative prooposals"),
                                 pos = (10,10),size=(780,260))
        
#        self.box1.SetForegroundColour(wx.Colour(255, 128, 0))
        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.grid = wx.grid.Grid(id=wxID_PANELAGRID, name='gridpageA',
              parent=self, pos=wx.Point(20, 40), size=wx.Size(760, 220),
              style=0)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageAGridCellLeftDclick, id=wxID_PANELAGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageAGridCellRightClick, id=wxID_PANELAGRID)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK,
              self.OnGridPageAGridCellLeftClick)

#..............................................................................
# action buttons for management of alternatives

        self.GenerateNew = wx.Button(id=wxID_PANELAGENERATENEW,
              label=_('generate new proposal'), name='GenerateNew', parent=self,
              pos=wx.Point(10, 280), size=wx.Size(120, 20), style=0)
        self.GenerateNew.Bind(wx.EVT_BUTTON, self.OnGenerateNewButton,
              id=wxID_PANELAGENERATENEW)

        self.copyProposal = wx.Button(id=wxID_PANELACOPYPROPOSAL,
              label=_('copy proposal'), name='copyProposal', parent=self,
              pos=wx.Point(150, 280), size=wx.Size(120, 20), style=0)
        self.copyProposal.Bind(wx.EVT_BUTTON, self.OnCopyProposalButton,
              id=wxID_PANELACOPYPROPOSAL)

        self.deleteProposal = wx.Button(id=wxID_PANELADELETEPROPOSAL,
              label=_('delete proposal'), name='deleteProposal', parent=self,
              pos=wx.Point(290, 280), size=wx.Size(120, 20), style=0)
        self.deleteProposal.Bind(wx.EVT_BUTTON, self.OnDeleteProposalButton,
              id=wxID_PANELADELETEPROPOSAL)

        self.selectProposal = wx.Button(id=-1,
              label=_('select proposal'), name='selectProposal', parent=self,
              pos=wx.Point(430, 280), size=wx.Size(120, 20), style=0)
        self.selectProposal.Bind(wx.EVT_BUTTON, self.OnSelectProposalButton,
              id=-1)


#..............................................................................
# comparative graphics

        self.box2 = wx.StaticBox(self, -1, _("comparison of primary energy consumption and effective annual cost"),
                                 pos = (10,310),size=(400,270))
        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelAFig = wx.Panel(id=wxID_PANELAPANELAFIG, name='panelAFigure',
              parent=self, pos=wx.Point(20, 340), size=wx.Size(380, 230),
              style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)

#..............................................................................
# action buttons for design of subsystems

        self.box3 = wx.StaticBox(self, -1, _("design of subsystems"),
                                 pos = (430,310),size=(360,240))
        self.box3.SetForegroundColour(TITLE_COLOR)
        self.box3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.DesignPO = wx.Button(id=wxID_PANELADESIGNPO,
              label=_('process optimisation'), name='DesignPO', parent=self,
              pos=wx.Point(590, 360), size=wx.Size(180, 24), style=0)
        self.DesignPO.Bind(wx.EVT_BUTTON, self.OnDesignPOButton,
              id=wxID_PANELADESIGNPO)

        self.DesignPA = wx.Button(id=wxID_PANELADESIGNPA,
              label=_('pinch analysis'), name='DesignPA', parent=self,
              pos=wx.Point(590, 400), size=wx.Size(180, 24), style=0)
        self.DesignPA.Bind(wx.EVT_BUTTON, self.OnDesignPAButton,
              id=wxID_PANELADESIGNPA)

        self.DesignHX = wx.Button(id=wxID_PANELADESIGNHX,
              label=_('HX network design'), name='DesignHX', parent=self,
              pos=wx.Point(590, 440), size=wx.Size(180, 24), style=0)
        self.DesignHX.Bind(wx.EVT_BUTTON, self.OnDesignHXButton,
              id=wxID_PANELADESIGNHX)

        self.DesignHC = wx.Button(id=wxID_PANELADESIGNHC,
              label=_('Heat and cold supply'), name='DesignHC', parent=self,
              pos=wx.Point(590, 480), size=wx.Size(180, 24), style=0)
        self.DesignHC.Bind(wx.EVT_BUTTON, self.OnDesignHCButton,
              id=wxID_PANELADESIGNHC)

#..............................................................................
# default action buttons for design of subsystems
        self.buttonpageAOk = wx.Button(id=wx.ID_OK, label=_('OK'),
              name='buttonpageAOk', parent=self, pos=wx.Point(528, 560),
              size=wx.Size(75, 20), style=0)
        self.buttonpageAOk.Bind(wx.EVT_BUTTON, self.OnButtonpageAOkButton,
              id=wx.ID_OK)

        self.buttonpageACancel = wx.Button(id=wx.ID_CANCEL, label=_('Cancel'),
              name='buttonpageACancel', parent=self, pos=wx.Point(616, 560),
              size=wx.Size(75, 0), style=0)
        self.buttonpageACancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpageACancelButton, id=wx.ID_CANCEL)

        self.buttonpageAFwd = wx.Button(id=wxID_PANELABUTTONPAGEAFWD,
              label='>>>', name='buttonpageAFwd', parent=self, pos=wx.Point(704,
              560), size=wx.Size(75, 20), style=0)
        self.buttonpageAFwd.Bind(wx.EVT_BUTTON, self.OnButtonpageAFwdButton,
              id=wxID_PANELABUTTONPAGEAFWD)

        self.buttonpageABack = wx.Button(id=wxID_PANELABUTTONPAGEABACK,
              label='<<<', name='buttonpageABack', parent=self,
              pos=wx.Point(440, 560), size=wx.Size(75, 20), style=0)
        self.buttonpageABack.Bind(wx.EVT_BUTTON, self.OnButtonpageABackButton,
              id=wxID_PANELABUTTONPAGEABACK)


#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   function activated on each entry into the panel from the tree
#------------------------------------------------------------------------------		
        self.mod.updatePanel()        # prepares data for plotting

#..............................................................................
# update of alternatives table

        data = Status.int.GData[self.keys[0]]
        print "data = ",data
        (rows,cols) = data.shape
        print rows,cols
        for r in range(rows):
            for c in range(cols):
                try:
                    self.grid.SetCellValue(r, c, data[r][c])
                except:
                    pass

#XXX Here better would be updating the grid and showing less rows ... ????
        for r in range(rows,MAXROWS):
            for c in range(cols):
                self.grid.SetCellValue(r, c, "")

        self.panelAFig.draw()
        self.Show()
        self.main.panelinfo.update()
       
#------------------------------------------------------------------------------		

#==============================================================================
#   EVENT HANDLERS
#==============================================================================

#------------------------------------------------------------------------------		
    def OnGenerateNewButton(self, event):
#------------------------------------------------------------------------------		
#   Generate new alterantive proposal
#------------------------------------------------------------------------------		

        self.shortName = "New Proposal %s"%(Status.NoOfAlternatives+1)
        self.description = "based on present state"
        
        pu1 =  DialogA(self)
        if pu1.ShowModal() == wx.ID_OK:
            print _("PanelA - OK"),self.shortName,self.description
            print "PanelA (GenerateNew-Button): calling function createNewAlternative"

            Status.prj.createNewAlternative(0,self.shortName,self.description)
            self.display()

        elif pu1.ShowModal() == wx.ID_Cancel:
            print _("PanelA - Cancel")
        else:
            print _("PanelA ???")

        self.display()
        
#------------------------------------------------------------------------------		
    def OnCopyProposalButton(self, event):
#------------------------------------------------------------------------------		
#   Generate new porposal copying from existing alternative
#------------------------------------------------------------------------------		
        self.shortName = self.grid.GetCellValue(self.selectedRow,1)+"(mod.)"
        self.description = self.grid.GetCellValue(self.selectedRow,2)+"(modified alternative based on "+self.grid.GetCellValue(self.selectedRow,1)+")"

        pu1 =  DialogA(self)
        if pu1.ShowModal() == wx.ID_OK:
            print _("PanelA - OK"),self.shortName,self.description
            print "PanelA (GenerateNew-Button): calling function createNewAlternative"

            Status.prj.createNewAlternative(self.ANo,self.shortName,self.description)
            self.display()

        elif pu1.ShowModal() == wx.ID_Cancel:
            print _("PanelA - Cancel")
        else:
            print _("PanelA - ???")

#------------------------------------------------------------------------------		
    def OnDeleteProposalButton(self, event):
#------------------------------------------------------------------------------		
#   Delete alternative proposal
#------------------------------------------------------------------------------		

        pu2 =  DialogOK(self,_("delete alternative"),_("do you really want to delete this alternative ?"))
        if pu2.ShowModal() == wx.ID_OK:
            if self.ANo > 0:
                Status.prj.deleteAlternative(self.ANo)
                self.display()
            elif self.ANo in [-1,0]:
                print _("PanelA (DeleteButton): cannot delete alternative "),self.ANo
            else:
                print _("PanelA (DeleteButton): erroneous alternative number "),self.ANo

#------------------------------------------------------------------------------		
    def OnSelectProposalButton(self, event):
#------------------------------------------------------------------------------		
#   Select alternative proposal
#------------------------------------------------------------------------------		

#        Status.prj.setFinalAlternative(self.ANo)
        event.skip()
        
#------------------------------------------------------------------------------		
    def OnGridPageAGridCellLeftClick(self, event):
#------------------------------------------------------------------------------		
#   Detects selected row
#------------------------------------------------------------------------------		
	self.selectedRow = event.GetRow()
	self.ANo = self.selectedRow - 1
        Status.prj.setActiveAlternative(self.ANo)

        print "PanelA - updating panelinfo"
        self.main.panelinfo.update()

        print "PanelA (GridCellLeftClick): row, ANo = ",self.selectedRow,self.ANo	    
        event.Skip()

#------------------------------------------------------------------------------		
    def OnGridPageAGridCellLeftDclick(self, event):
#------------------------------------------------------------------------------		
        self.OnGridPageAGridCellLeftClick(event)
        event.Skip()

    def OnGridPageAGridCellRightClick(self, event):
        event.Skip()        

#==============================================================================
#   EVENT HANDLERS BUTTONS TO DESIGN ASSISTANTS
#==============================================================================
    def OnDesignPAButton(self, event):
        event.Skip()

    def OnDesignHXButton(self, event):
        event.Skip()

    def OnDesignHCButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)

    def OnDesignPOButton(self, event):
        event.Skip()

#------------------------------------------------------------------------------		
#   <<< OK Cancel >>>
#------------------------------------------------------------------------------		
    def OnButtonpageAOkButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)
        print "Button exitModuleOK: now I should go back to HC"

    def OnButtonpageACancelButton(self, event):
        #warning: do you want to leave w/o saving ???
        print "Button exitModuleCancel: now I should go back to HC"

    def OnButtonpageABackButton(self, event):
        self.Hide()
        print "Button exitModuleBack: now I should show another window"

    def OnButtonpageAFwdButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)
        print "Button exitModuleFwd: now I should show another window"


