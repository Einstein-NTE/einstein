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
#	Version No.: 0.06
#	Created by: 	    Hans Schweiger	    03/04/2008
#	Revised by:    
#                           Tom Sobota              05/04/2008
#                           Hans Schweiger          15/04/2008
#                           Tom Sobota              28/04/2008
#                           Stoyan Danov            18/06/2008
#                           Hans Schweiger          16/09/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes to previous version:
#       05/04/08    changed call to popup1 in OnButtonpageHPAddButton
#                   slight change to OK and Cancel buttons, to show the right icons
#       15/04/08 HS copy and delete buttons added. event handler "Generate New" linked
#       28/04/2008  added 'draw' to method display
#       18/06/2008 SD: change to translatable text _(...)
#       16/09/2008  HS  call to showMainMenuAlternatives added in display
#       13/10/2008: SD  change _() to _U()
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
from dialogA import *
from dialogOK import *
from GUITools import *
from numCtrl import *


[wxID_PANELA, wxID_PANELABUTTONPAGEABACK, wxID_PANELABUTTONPAGEACANCEL, 
 wxID_PANELABUTTONPAGEAFWD, wxID_PANELABUTTONPAGEAOK, wxID_PANELACOPYPROPOSAL, 
 wxID_PANELADELETEPROPOSAL, wxID_PANELADESIGNHC, wxID_PANELADESIGNHX, 
 wxID_PANELADESIGNPA, wxID_PANELADESIGNPO, wxID_PANELAGENERATENEW, 
 wxID_PANELAGRID, wxID_PANELAPANELAFIG, wxID_PANELAST1PAGEA, 
 wxID_PANELAST3PAGEA, 
] = [wx.NewId() for _init_ctrls in range(16)]

# constants
#

COLNO = 6
MAXROWS = 20

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

#------------------------------------------------------------------------------		
def drawFigure(self):
#------------------------------------------------------------------------------
#   defines the figures to be plotted
#------------------------------------------------------------------------------		
    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)

    gdata = Status.int.GData["A Plot"]

    try: (rows,cols) = gdata.shape
    except: (rows,cols) = (0,COLNO)
    NAlternatives = rows - 2

    if rows >= 2:
        N0 = _U("present state")
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
    self.subplot.legend()

    self.subplot.axes.set_ylabel(_U('Primary energy consumption [MWh]'))
    self.subplot.axes.set_xlabel(_U('Energy cost [€]'))
    
    for label in self.subplot.axes.get_yticklabels():
#        label.set_color(self.params['ytickscolor'])
        label.set_fontsize(8)
#        label.set_rotation(self.params['yticksangle'])
    #
    # properties of labels on the x axis
    #
    for label in self.subplot.axes.get_xticklabels():
#        label.set_color(self.params['xtickscolor'])
        label.set_fontsize(8)
#        label.set_rotation(self.params['xticksangle'])

    try:
        lg = self.subplot.get_legend()
        ltext  = lg.get_texts()             # all the text.Text instance in the legend
        for txt in ltext:
            txt.set_fontsize(10)  # the legend text fontsize
        # legend line thickness
        llines = lg.get_lines()             # all the lines.Line2D instance in the legend
        for lli in llines:
            lli.set_linewidth(1.5)          # the legend linewidth
        # color of the legend frame
        # this only works when the frame is painted (see below draw_frame)
        frame  = lg.get_frame()             # the patch.Rectangle instance surrounding the legend
        frame.set_facecolor('#F0F0F0')      # set the frame face color to light gray
        # should the legend frame be painted
        lg.draw_frame(False)
    except:
        # no legend
        pass

#==============================================================================
#==============================================================================
class PanelA(wx.Panel):
#==============================================================================
#==============================================================================

    def __init__(self, parent, main):
	keys = ['A Table','A Plot']
	self.keys = keys
	self.main = main
        self.mod = Status.mod.moduleA
        self.shortName = _U("new alternative")
        self.description = _U("describe shortly the main differential features of the new alternative")
        self.ANo = Status.ANo
        self.selectedProposalName = "---"
        self._init_ctrls(parent)
        
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
        attr2.SetTextColour(GRID_LETTER_COLOR_HIGHLIGHT)
        attr2.SetBackgroundColour(GRID_BACKGROUND_COLOR_HIGHLIGHT)
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
        self.grid.SetColLabelValue(0, _U("No."))
        self.grid.SetColLabelValue(1, _U("Name"))
        self.grid.SetColLabelValue(2, _U("Description"))
        self.grid.SetColLabelValue(3, _U("State"))
        self.grid.SetColLabelValue(4, _U("Primary energy\nconsumption\n[MWh/a]"))
        self.grid.SetColLabelValue(5, _U("Total annual\nenergy cost\n[€/a]"))
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

        self.box1 = wx.StaticBox(self, -1, _U("design of alternative prooposals"),
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
              label=_U('generate new proposal'), name='GenerateNew', parent=self,
              pos=wx.Point(10, 280), size=wx.Size(120, 20), style=0)
        self.GenerateNew.Bind(wx.EVT_BUTTON, self.OnGenerateNewButton,
              id=wxID_PANELAGENERATENEW)

        self.copyProposal = wx.Button(id=wxID_PANELACOPYPROPOSAL,
              label=_U('copy proposal'), name='copyProposal', parent=self,
              pos=wx.Point(150, 280), size=wx.Size(120, 20), style=0)
        self.copyProposal.Bind(wx.EVT_BUTTON, self.OnCopyProposalButton,
              id=wxID_PANELACOPYPROPOSAL)

        self.deleteProposal = wx.Button(id=wxID_PANELADELETEPROPOSAL,
              label=_U('delete proposal'), name='deleteProposal', parent=self,
              pos=wx.Point(290, 280), size=wx.Size(120, 20), style=0)
        self.deleteProposal.Bind(wx.EVT_BUTTON, self.OnDeleteProposalButton,
              id=wxID_PANELADELETEPROPOSAL)

        self.selectProposal = wx.Button(id=-1,
              label=_U('select proposal'), name='selectProposal', parent=self,
              pos=wx.Point(430, 280), size=wx.Size(120, 20), style=0)
        self.selectProposal.Bind(wx.EVT_BUTTON, self.OnSelectProposalButton,
              id=-1)

        self.stSelected = wx.StaticText(id=-1,
              label=_U("selected proposal: "),
              name='stSelected', parent=self, pos=wx.Point(440, 310),
              style=0)
        self.stSelected.SetForegroundColour(TITLE_COLOR)
        self.stSelected.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
        
        self.selectedProposal = wx.StaticText(id=-1,
              label=self.selectedProposalName,
              name='selectedProposal', parent=self, pos=wx.Point(580, 310),
              style=0)


#..............................................................................
# comparative graphics

        self.box2 = wx.StaticBox(self, -1, _U("comparison of primary energy consumption and effective annual cost"),
                                 pos = (10,310),size=(400,270))
        self.box2.SetForegroundColour(TITLE_COLOR)
        self.box2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.panelAFig = wx.Panel(id=wxID_PANELAPANELAFIG, name='panelAFigure',
              parent=self, pos=wx.Point(20, 340), size=wx.Size(380, 230),
              style=wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)

#..............................................................................
# action buttons for design of subsystems

        self.box3 = wx.StaticBox(self, -1, _U("design of subsystems"),
                                 pos = (430,350),size=(360,200))
        self.box3.SetForegroundColour(TITLE_COLOR)
        self.box3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.DesignPO = wx.Button(id=wxID_PANELADESIGNPO,
              label=_U('process optimisation'), name='DesignPO', parent=self,
              pos=wx.Point(590, 400), size=wx.Size(180, 24), style=0)
        self.DesignPO.Bind(wx.EVT_BUTTON, self.OnDesignPOButton,
              id=wxID_PANELADESIGNPO)

        self.DesignHX = wx.Button(id=wxID_PANELADESIGNHX,
              label=_U('HX network design'), name='DesignHX', parent=self,
              pos=wx.Point(590, 440), size=wx.Size(180, 24), style=0)
        self.DesignHX.Bind(wx.EVT_BUTTON, self.OnDesignHXButton,
              id=wxID_PANELADESIGNHX)

        self.DesignHC = wx.Button(id=wxID_PANELADESIGNHC,
              label=_U('Heat and cold supply'), name='DesignHC', parent=self,
              pos=wx.Point(590, 480), size=wx.Size(180, 24), style=0)
        self.DesignHC.Bind(wx.EVT_BUTTON, self.OnDesignHCButton,
              id=wxID_PANELADESIGNHC)

#..............................................................................
# default action buttons for design of subsystems
        self.buttonpageAOk = wx.Button(id=wx.ID_OK, label=_U('OK'),
              name='buttonpageAOk', parent=self, pos=wx.Point(528, 560),
              size=wx.Size(75, 20), style=0)
        self.buttonpageAOk.Bind(wx.EVT_BUTTON, self.OnButtonpageAOkButton,
              id=wx.ID_OK)

        self.buttonpageACancel = wx.Button(id=wx.ID_CANCEL, label=_U('Cancel'),
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
        (rows,cols) = data.shape

        decimals = [-1,-1,-1,-1,2,2]
        for r in range(rows):                
            for c in range(cols):
                try:
                    if decimals[c] >= 0: # -1 indicates text
                        self.grid.SetCellValue(r, c, \
                            convertDoubleToString((data[r][c]),nDecimals = decimals[c]))
                    else:
                        self.grid.SetCellValue(r, c, data[r][c])
                except:
                    logDebug("PanelEA4a: error writing data[%r][%r]: "%(r,c))

#XXX Here better would be updating the grid and showing less rows ... ????
        for r in range(rows,MAXROWS):
            for c in range(cols):
                self.grid.SetCellValue(r, c, "")

        self.grid.SelectRow(Status.ANo+1)
        self.ANo = Status.ANo

        self.selectedProposal.SetLabel(check(Status.FinalAlternativeName))

        self.Hide()
        self.panelAFig.draw()
        self.Show()
        self.main.panelinfo.update()
        self.main.showMainMenuAlternatives()
       
#------------------------------------------------------------------------------		

#==============================================================================
#   EVENT HANDLERS
#==============================================================================

#------------------------------------------------------------------------------		
    def OnGenerateNewButton(self, event):
#------------------------------------------------------------------------------		
#   Generate new alterantive proposal
#------------------------------------------------------------------------------		

        self.shortName = _U("New Proposal %s")%(Status.NoOfAlternatives+1)
        self.description = _U("based on present state")
        
        pu1 =  DialogA(self)
        if pu1.ShowModal() == wx.ID_OK:

            Status.prj.createNewAlternative(0,self.shortName,self.description)
            self.display()

        elif pu1.ShowModal() == wx.ID_Cancel:
            print "PanelA - Cancel"
        else:
            print "PanelA ???"

        self.display()
        
#------------------------------------------------------------------------------		
    def OnCopyProposalButton(self, event):
#------------------------------------------------------------------------------		
#   Generate new porposal copying from existing alternative
#------------------------------------------------------------------------------		
        self.shortName = self.grid.GetCellValue(self.selectedRow,1)+_U('(mod.)')
        self.description = self.grid.GetCellValue(self.selectedRow,2)+ \
                           _U('(modified alternative based on ')+ \
                           self.grid.GetCellValue(self.selectedRow,1)+ u')'

        pu1 =  DialogA(self)
        if pu1.ShowModal() == wx.ID_OK:

            Status.prj.createNewAlternative(self.ANo,self.shortName,self.description)
            self.display()

        elif pu1.ShowModal() == wx.ID_Cancel:
            print "PanelA - Cancel"
        else:
            print "PanelA - ???"

#------------------------------------------------------------------------------		
    def OnDeleteProposalButton(self, event):
#------------------------------------------------------------------------------		
#   Delete alternative proposal
#------------------------------------------------------------------------------		

        pu2 =  DialogOK(self,_U("delete alternative"),_U("do you really want to delete this alternative ?"))
        if pu2.ShowModal() == wx.ID_OK:
            if self.ANo > 0:
                Status.prj.deleteAlternative(self.ANo)
                self.display()
            elif self.ANo in [-1,0]:
                print "PanelA (DeleteButton): cannot delete alternative ",self.ANo
            else:
                print "PanelA (DeleteButton): erroneous alternative number ",self.ANo

#------------------------------------------------------------------------------		
    def OnSelectProposalButton(self, event):
#------------------------------------------------------------------------------		
#   Select alternative proposal
#------------------------------------------------------------------------------		

        showMessage(_U("Alternative %s selected as final proposal")%self.ANo)
        Status.prj.setFinalAlternative(self.ANo)
        self.selectedProposalName = Status.FinalAlternativeName
        logMessage("Final alternative selected = %r"%self.selectedProposalName)
        self.selectedProposal.SetLabel(self.selectedProposalName)
        self.display()
        
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

    def OnDesignHXButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHX, select=True)

    def OnDesignHCButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qHC, select=True)

    def OnDesignPOButton(self, event):
        self.Hide()
        self.main.tree.SelectItem(self.main.qPO, select=True)

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


