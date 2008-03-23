#Boa:FramePanel:PanelEnergy

import wx
import wx.grid
#from einstein.modules.energy.moduleEnergy import ModuleEnergy
from status import Status
from einstein.modules.energy.moduleEnergy import *
import einstein.modules.matPanel as Mp


[wxID_PANELENERGY, wxID_PANELENERGYANNUAL, wxID_PANELENERGYBUTTONBACK, 
 wxID_PANELENERGYBUTTONCANCEL, wxID_PANELENERGYBUTTONFWD, 
 wxID_PANELENERGYBUTTONOK, wxID_PANELENERGYBUTTONRUNSIMULATION, 
 wxID_PANELENERGYCHOICESIMULATIONTOOL, wxID_PANELENERGYGRID, 
 wxID_PANELENERGYHOURLY, wxID_PANELENERGYMONTHLY, wxID_PANELENERGYST1, 
 wxID_PANELENERGYST2, wxID_PANELENERGYST3, wxID_PANELENERGYSTATICBOX1, 
 wxID_PANELENERGYSTATICBOX2,
 wxID_PANELENERGYPICTURE1, wxID_PANELENERGYPICTURE2,
] = [wx.NewId() for _init_ctrls in range(18)]

class PanelEnergy(wx.Panel):

    def __init__(self, parent, id, pos, size, style, name):

        self._init_ctrls(parent)
        self.mod = ModuleEnergy()

        #TS2008-03-17 modified graphics generation structure
        # remaps drawing methods to the wx widgets.
        # gets the drawing methods from moduleEnergy.
        dummy = Mp.MatPanel(self.panelEnergyDemand, wx.Panel, self.mod.getDrawEnergyDemand())
        dummy = Mp.MatPanel(self.panelComPerformance, wx.Panel, self.mod.getDrawComPerformance())
        del dummy

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELENERGY, name='PanelEnergy',
              parent=prnt, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)
        self.SetClientSize(wx.Size(792, 566))

        self.monthly = wx.Button(id=wxID_PANELENERGYMONTHLY,
              label='monthly data', name='monthly', parent=self,
              pos=wx.Point(592, 144), size=wx.Size(184, 23), style=0)
        self.monthly.Bind(wx.EVT_BUTTON, self.OnMonthlyButton,
              id=wxID_PANELENERGYMONTHLY)

        self.grid = wx.grid.Grid(id=wxID_PANELENERGYGRID, name='grid',
              parent=self, pos=wx.Point(16, 104), size=wx.Size(504, 168),
              style=0)
        self.grid.SetDefaultRowSize(12)
        self.grid.EnableEditing(False)

        self.st2 = wx.StaticText(id=wxID_PANELENERGYST2,
              label='simulation results', name='st2', parent=self,
              pos=wx.Point(632, 72), style=0)
        self.st2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.choiceSimulationTool = wx.Choice(choices=["einstein",
              "transEnergy"], id=wxID_PANELENERGYCHOICESIMULATIONTOOL,
              name='choiceSimulationTool', parent=self, pos=wx.Point(392, 16),
              size=wx.Size(130, 21), style=0)
        self.choiceSimulationTool.Bind(wx.EVT_CHOICE,
              self.OnChoiceSimulationToolChoice,
              id=wxID_PANELENERGYCHOICESIMULATIONTOOL)

        self.staticBox1 = wx.StaticBox(id=wxID_PANELENERGYSTATICBOX1,
              label='energy demand', name='staticBox1', parent=self,
              pos=wx.Point(16, 288), size=wx.Size(360, 224), style=0)
        self.panelEnergyDemand = wx.Panel(id=wxID_PANELENERGYPICTURE1, name='panelEnergyDemand', parent=self,
              pos=wx.Point(24, 312), size=wx.Size(344, 192),
              style=wx.TAB_TRAVERSAL)

        self.buttonOK = wx.Button(id=wxID_PANELENERGYBUTTONOK, label='ok',
              name='buttonOK', parent=self, pos=wx.Point(528, 528),
              size=wx.Size(75, 23), style=0)
        self.buttonOK.Bind(wx.EVT_BUTTON, self.OnButtonOKButton,
              id=wxID_PANELENERGYBUTTONOK)

        self.buttonCancel = wx.Button(id=wxID_PANELENERGYBUTTONCANCEL,
              label='cancel', name='buttonCancel', parent=self,
              pos=wx.Point(616, 528), size=wx.Size(75, 23), style=0)
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.OnButtonCancelButton,
              id=wxID_PANELENERGYBUTTONCANCEL)

        self.buttonRunSimulation = wx.Button(id=wxID_PANELENERGYBUTTONRUNSIMULATION,
              label='run simulation', name='buttonRunSimulation', parent=self,
              pos=wx.Point(16, 16), size=wx.Size(184, 23), style=0)
        self.buttonRunSimulation.Bind(wx.EVT_BUTTON,
              self.OnButtonRunSimulationButton,
              id=wxID_PANELENERGYBUTTONRUNSIMULATION)

        self.buttonFwd = wx.Button(id=wxID_PANELENERGYBUTTONFWD, label='>>>',
              name='buttonFwd', parent=self, pos=wx.Point(704, 528),
              size=wx.Size(75, 23), style=0)
        self.buttonFwd.Bind(wx.EVT_BUTTON, self.OnButtonFwdButton,
              id=wxID_PANELENERGYBUTTONFWD)

        self.buttonBack = wx.Button(id=wxID_PANELENERGYBUTTONBACK, label='<<<',
              name='buttonBack', parent=self, pos=wx.Point(440, 528),
              size=wx.Size(75, 23), style=0)
        self.buttonBack.Bind(wx.EVT_BUTTON, self.OnButtonBackButton,
              id=wxID_PANELENERGYBUTTONBACK)

        self.hourly = wx.Button(id=wxID_PANELENERGYHOURLY,
              label='hourly performance', name='hourly', parent=self,
              pos=wx.Point(592, 184), size=wx.Size(184, 23), style=0)
        self.hourly.Bind(wx.EVT_BUTTON, self.OnHourlyButton,
              id=wxID_PANELENERGYHOURLY)

        self.annual = wx.Button(id=wxID_PANELENERGYANNUAL, label='annual data',
              name='annual', parent=self, pos=wx.Point(592, 104),
              size=wx.Size(184, 23), style=0)
        self.annual.Bind(wx.EVT_BUTTON, self.OnAnnualButton,
              id=wxID_PANELENERGYANNUAL)

        self.st3 = wx.StaticText(id=wxID_PANELENERGYST3,
              label='simulation setup: ', name='st3', parent=self,
              pos=wx.Point(280, 20), style=0)
        self.st3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.st1 = wx.StaticText(id=wxID_PANELENERGYST1,
              label='energetic performance', name='st1', parent=self,
              pos=wx.Point(16, 82), style=0)
        self.st1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'Tahoma'))

        self.staticBox2 = wx.StaticBox(id=wxID_PANELENERGYSTATICBOX2,
              label='comparative performance', name='staticBox2', parent=self,
              pos=wx.Point(416, 288), size=wx.Size(360, 224), style=0)
        
        self.panelComPerformance = wx.Panel(id=wxID_PANELENERGYPICTURE2,
                                            name='panelComPerformance', parent=self,
              pos=wx.Point(424, 312), size=wx.Size(344, 192),
              style=wx.TAB_TRAVERSAL)
        
    def OnButtonRunSimulationButton(self, event):
        self.mod.runSimulation()

    def OnButton1Button(self, event):
        event.Skip()

    def OnButtonpageHeatPumpBackButton(self, event):
        event.Skip()

    def OnButtonpageHeatPumpFwdButton(self, event):
        event.Skip()

    def OnMonthlyButton(self, event):
        event.Skip()

    def OnChoiceSimulationToolChoice(self, event):
        event.Skip()

    def OnButtonOKButton(self, event):
        event.Skip()

    def OnButtonCancelButton(self, event):
        event.Skip()

    def OnButtonFwdButton(self, event):
        event.Skip()

    def OnButtonBackButton(self, event):
        event.Skip()

    def OnHourlyButton(self, event):
        event.Skip()

    def OnAnnualButton(self, event):
        event.Skip()



