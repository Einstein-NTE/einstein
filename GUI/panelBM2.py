#Boa:FramePanel:PanelBM2
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
#	Panel BM2
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#       Benchmark module, part 2: specific energy consumption by product
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	    08/04/2008
#       Revised by:         Tom Sobota  28/04/2008
#                           Stoyan Danov            18/06/2008
#                           
#
#       Changes to previous version:
#       28/04/2008          created method display
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
from einstein.GUI.graphics import drawPiePlot
from einstein.modules.modules import Modules
from einstein.GUI.status import Status
from einstein.GUI.addEquipment_popup import AddEquipment #TS 20080405 changed


import einstein.modules.matPanel as Mp
from einstein.modules.interfaces import *


[wxID_PANELBM2, wxID_PANELBM2BUTTONPAGEBM2BACK, 
 wxID_PANELBM2BUTTONPAGEBM2CANCEL, wxID_PANELBM2BUTTONPAGEBM2FWD, 
 wxID_PANELBM2BUTTONPAGEBM2OK, wxID_PANELBM2COMBOPRODUCT, 
 wxID_PANELBM2COMBOSEARCHCRIT1, wxID_PANELBM2FINDBENCHMARKS, 
 wxID_PANELBM2GRIDPAGE, wxID_PANELBM2FIG, wxID_PANELBM2SEARCHCRIT2, 
 wxID_PANELBM2ST1, wxID_PANELBM2ST1PAGEBM2, wxID_PANELBM2ST2, 
 wxID_PANELBM2ST3PAGEBM2, wxID_PANELBM2STATICTEXT1, wxID_PANELBM2STATICTEXT2, 
 wxID_PANELBM2STPRODUCT, wxID_PANELBM2STSEARCHCRIT1, 
 wxID_PANELBM2STSEARCHCRIT2UNIT, wxID_PANELBM2STSEARCHCRIT3, 
 wxID_PANELBM2STTITLE, wxID_PANELBM2TCSEARCHCRIT2A, 
 wxID_PANELBM2TCSEARCHCRIT2B, wxID_PANELBM2TCSEARCHCRIT3A, 
 wxID_PANELBM2TCSEARCHCRIT3B, 
] = [wx.NewId() for _init_ctrls in range(26)]

# constants
#
GRID_LETTER_SIZE = 8 #points
GRID_LABEL_SIZE = 9  # points
GRID_LETTER_COLOR = '#000060'     # specified as hex #RRGGA
GRID_BACKGROUND_COLOR = '#F0FFFF' # idem
GRAPH_BACKGROUND_COLOR = '#FFFFFF' # idem


class PanelBM2(wx.Panel):

    def __init__(self, parent):
        self._init_ctrls(parent)
	keys = ['BM2 Table']
        self.mod = Status.mod.moduleBM
        
#==============================================================================
#   graphic: Cumulative heat demand by hours
#==============================================================================
        labels_column = 0
        ignoredrows = []
        paramList={'labels'      : labels_column,          # labels column
                   'data'        : 3,                      # data column for this graph
                   'key'         : keys[0],                # key for Interface
                   'title'       : 'Some title',           # title of the graph
                   'backcolor'   : GRAPH_BACKGROUND_COLOR, # graph background color
                   'ignoredrows' : ignoredrows}            # rows that should not be plotted

        dummy = Mp.MatPanel(self.panelFig,
                            wx.Panel,
                            drawPiePlot,
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
        attr.SetFont(wx.Font(GRID_LETTER_SIZE, wx.SWISS, wx.NORMAL, wx.BOLD))

        key = keys[0]
        data = Interfaces.GData[key]
        (rows,cols) = data.shape
        self.gridPage.CreateGrid(max(rows,20), cols)

        self.gridPage.EnableGridLines(True)
        self.gridPage.SetDefaultRowSize(20)
        self.gridPage.SetRowLabelSize(30)
        self.gridPage.SetColSize(0,115)
        self.gridPage.EnableEditing(False)
        self.gridPage.SetLabelFont(wx.Font(9, wx.ROMAN, wx.ITALIC, wx.BOLD))
        self.gridPage.SetColLabelValue(0, _("Source"))
        self.gridPage.SetColLabelValue(1, _("Reference"))
        self.gridPage.SetColLabelValue(2, _("Validity"))
        self.gridPage.SetColLabelValue(3, _("Electricity (min)"))
        self.gridPage.SetColLabelValue(4, _("Electricity (target)"))
        self.gridPage.SetColLabelValue(5, _("Electricity (max)"))
        self.gridPage.SetColLabelValue(6, _("Fuels (min)"))
        self.gridPage.SetColLabelValue(7, _("Fuels (target)"))
        self.gridPage.SetColLabelValue(8, _("Fuels (max)"))
        self.gridPage.SetColLabelValue(9, _("Primary energy (min)"))
        self.gridPage.SetColLabelValue(10, _("Primary energy (target)"))
        self.gridPage.SetColLabelValue(11, _("Primary energy (max)"))
     #
        # copy values from dictionary to grid
        #
        for r in range(rows):
            self.gridPage.SetRowAttr(r, attr)
            for c in range(cols):
                self.gridPage.SetCellValue(r, c, data[r][c])
                if c == labels_column:
                    self.gridPage.SetCellAlignment(r, c, wx.ALIGN_LEFT, wx.ALIGN_CENTRE);
                else:
                    self.gridPage.SetCellAlignment(r, c, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE);

        self.gridPage.SetGridCursor(0, 0)

        self.stTitle.SetFont(wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD))
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELBM2, name='PanelBM2', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(808, 634), style=0)
        self.SetClientSize(wx.Size(800, 600))

        self.panelFig = wx.Panel(id=wxID_PANELBM2FIG, name='panelBM2Figure',
              parent=self, pos=wx.Point(26, 346), size=wx.Size(382, 220),
              style=wx.TAB_TRAVERSAL)

        self.gridPage = wx.grid.Grid(id=wxID_PANELBM2GRIDPAGE,
              name='gridpageBM2', parent=self, pos=wx.Point(24, 56),
              size=wx.Size(752, 216), style=0)
        self.gridPage.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,
              self.OnGridPageGridCellLeftDclick, id=wxID_PANELBM2GRIDPAGE)
        self.gridPage.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGridPageGridCellRightClick, id=wxID_PANELBM2GRIDPAGE)

        self.st1pageBM2 = wx.StaticText(id=-1, label=_('Search criteria'),
              name='st1pageBM2', parent=self, pos=wx.Point(448, 312), style=0)

        self.stTitle = wx.StaticText(id=wxID_PANELBM2STTITLE,
              label=_('Benchmarks 2: specific energy consumption by product'),
              name='stTitle', parent=self, pos=wx.Point(24, 16), style=0)
        self.stTitle.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.buttonpageBM2Ok = wx.Button(id=wx.ID_OK, label=_('OK'),
              name='buttonpageBM2Ok', parent=self, pos=wx.Point(528, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageBM2Ok.Bind(wx.EVT_BUTTON, self.OnButtonpageBM2OkButton,
              id=wx.ID_OK)

        self.buttonpageBM2Cancel = wx.Button(id=wx.ID_CANCEL, label=_('Cancel'),
              name='buttonpageBM2Cancel', parent=self, pos=wx.Point(616, 544),
              size=wx.Size(75, 23), style=0)
        self.buttonpageBM2Cancel.Bind(wx.EVT_BUTTON,
              self.OnButtonpageBM2CancelButton, id=wx.ID_CANCEL)

        self.buttonpageBM2Fwd = wx.Button(id=wxID_PANELBM2BUTTONPAGEBM2FWD,
              label='>>>', name='buttonpageBM2Fwd', parent=self,
              pos=wx.Point(704, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageBM2Fwd.Bind(wx.EVT_BUTTON, self.OnButtonpageBM2FwdButton,
              id=wxID_PANELBM2BUTTONPAGEBM2FWD)

        self.buttonpageBM2Back = wx.Button(id=wxID_PANELBM2BUTTONPAGEBM2BACK,
              label='<<<', name='buttonpageBM2Back', parent=self,
              pos=wx.Point(440, 544), size=wx.Size(75, 23), style=0)
        self.buttonpageBM2Back.Bind(wx.EVT_BUTTON,
              self.OnButtonpageBM2BackButton,
              id=wxID_PANELBM2BUTTONPAGEBM2BACK)

        self.FindBenchmarks = wx.Button(id=wxID_PANELBM2FINDBENCHMARKS,
              label=_('find benchmarks'), name='FindBenchmarks', parent=self,
              pos=wx.Point(592, 280), size=wx.Size(184, 24), style=0)
        self.FindBenchmarks.Bind(wx.EVT_BUTTON, self.OnGenerateNewButton,
              id=wxID_PANELBM2FINDBENCHMARKS)

        self.st3pageBM2 = wx.StaticText(id=wxID_PANELBM2ST3PAGEBM2,
              label=_('Comparison benchmark data'), name='st3pageBM2', parent=self,
              pos=wx.Point(24, 320), size=wx.Size(137, 13), style=0)

        self.staticText1 = wx.StaticText(id=wxID_PANELBM2STATICTEXT1,
              label=_('Benchmarks found:'), name='staticText1', parent=self,
              pos=wx.Point(24, 40), style=0)

        self.stSearchCrit1 = wx.StaticText(id=wxID_PANELBM2STSEARCHCRIT1,
              label=_('NACE Code range (digits)'), name='stSearchCrit1',
              parent=self, pos=wx.Point(448, 352), size=wx.Size(123, 13),
              style=0)

        self.SearchCrit2 = wx.StaticText(id=wxID_PANELBM2SEARCHCRIT2,
              label=_('Production volume'), name='SearchCrit2', parent=self,
              pos=wx.Point(448, 416), size=wx.Size(89, 13), style=0)

        self.stSearchCrit3 = wx.StaticText(id=wxID_PANELBM2STSEARCHCRIT3,
              label=_('Year of data'), name='stSearchCrit3', parent=self,
              pos=wx.Point(448, 440), size=wx.Size(61, 13), style=0)

        self.comboSearchCrit1 = wx.ComboBox(choices=["15500", "1550 _",
              "155 _ _", "15 _ _ _"], id=wxID_PANELBM2COMBOSEARCHCRIT1,
              name='comboSearchCrit1', parent=self, pos=wx.Point(640, 344),
              size=wx.Size(136, 21), style=0, value='1550 _')
        self.comboSearchCrit1.SetLabel('1550 _')

        self.tcSearchCrit2b = wx.TextCtrl(id=wxID_PANELBM2TCSEARCHCRIT2B,
              name='tcSearchCrit2b', parent=self, pos=wx.Point(712, 408),
              size=wx.Size(64, 24), style=1000, value='1000')

        self.tcSearchCrit2a = wx.TextCtrl(id=wxID_PANELBM2TCSEARCHCRIT2A,
              name='tcSearchCrit2a', parent=self, pos=wx.Point(640, 408),
              size=wx.Size(64, 24), style=0, value='0')

        self.st1 = wx.StaticText(id=wxID_PANELBM2ST1, label=_('max.'), name='st1',
              parent=self, pos=wx.Point(728, 384), size=wx.Size(25, 13),
              style=0)

        self.st2 = wx.StaticText(id=wxID_PANELBM2ST2, label=_('min.'), name='st2',
              parent=self, pos=wx.Point(664, 384), size=wx.Size(21, 13),
              style=0)

        self.tcSearchCrit3a = wx.TextCtrl(id=wxID_PANELBM2TCSEARCHCRIT3A,
              name='tcSearchCrit3a', parent=self, pos=wx.Point(640, 440),
              size=wx.Size(64, 24), style=0, value='2000')

        self.tcSearchCrit3b = wx.TextCtrl(id=wxID_PANELBM2TCSEARCHCRIT3B,
              name='tcSearchCrit3b', parent=self, pos=wx.Point(712, 440),
              size=wx.Size(64, 24), style=0, value='2008')

        self.stSearchCrit2Unit = wx.StaticText(id=wxID_PANELBM2STSEARCHCRIT2UNIT,
              label=_('t/year'), name='stSearchCrit2Unit', parent=self,
              pos=wx.Point(592, 416), size=wx.Size(30, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_PANELBM2STATICTEXT2,
              label=_('staticText2'), name='staticText2', parent=self.panelFig,
              pos=wx.Point(400, -320), size=wx.Size(55, 13), style=0)

        self.stProduct = wx.StaticText(id=wxID_PANELBM2STPRODUCT,
              label=_('Product:'), name='stProduct', parent=self, pos=wx.Point(512,
              16), size=wx.Size(42, 13), style=0)

        self.comboProduct = wx.ComboBox(choices=[_("milk"), _("cheese"), _("yoghourt")],
              id=wxID_PANELBM2COMBOPRODUCT, name='comboProduct', parent=self,
              pos=wx.Point(568, 8), size=wx.Size(210, 21), style=0,
              value='milk')
        self.comboProduct.SetLabel(_('milk'))


    def display(self):
        self.panelFig.draw()
        self.Show()

        
    def OnACalculateButton(self, event):
        ret = self.modA.designAssistant1()
        if (ret == "ManualFinalSelection"):
            print "here I should edit the data base"
        ret = self.modA.designAssistant2()
        if ret == "changed":
            modA.calculateCascade()
            #updatePlots
        
    def OnGenerateNewButton(self, event):
        #show pop-up menu for adding equipment
        #TS20080405 FIXME put dbheatpump table here just for testing! Should be replaced by the
	#right table when it is created
        pu1 =  AddEquipment(self, self.modHP, 'Add Heat Pump equipment','dbheatpump', 0, False)
        if pu1.ShowModal() == wx.ID_OK:
            print _('PanelBM2 AddEquipment accepted. Id=')+str(pu1.theId)
#            ret = self.modA.add(AId)
            #update plots
        else:
            print _('Cancelled')

    def OnGridPageGridCellLeftDclick(self, event):
        print "PanelBM2: Grid - left button Dclick"

    def OnGridPageGridCellRightClick(self, event):
        print "PanelBM2: Grid - right button click: scroll-up should appear"
        
    def OnButtonpageBM2OkButton(self, event):
        saveOption = "save"
        self.mod.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleOK: now I should go back to HC"

    def OnButtonpageBM2CancelButton(self, event):
        #warning: do you want to leave w/o saving ???
        saveOption = "save"
        self.mod.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleCancel: now I should go back to HC"

    def OnButtonpageBM2BackButton(self, event):
        #pop-up: to save or not to save ...
        saveOption = "save"
        self.modA.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleBack: now I should show another window"

    def OnButtonpageBM2FwdButton(self, event):
        #pop-up: to save or not to save ...
        saveOption = "save"
        self.mod.exitModule(saveOption)
        self.Hide()
        print "Button exitModuleFwd: now I should show another window"
