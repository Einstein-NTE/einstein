#Boa:FramePanel:PanelBO

import wx
#import einstein.modules.Boiler.ModuleBO as BO
import einstein.modules.boiler.boiler as BO


[wxID_PANELBO, wxID_PANELBOCHECKBOX1, wxID_PANELBOCHECKBOX2, 
 wxID_PANELBOCHOICE1, wxID_PANELBOBOCALCULATE, 
 wxID_PANELBOTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(6)]

class PanelBO(wx.Panel):

    def __init__(self, parent, id, pos, size, style, name, sql, db):

        self.sql = sql
        self.db = db
        
        self._init_ctrls(parent)

#        self.modBO = BO.ModuleBO()
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANELBO, name='PanelBO',
              parent=prnt, pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

        self.BOCalculate = wx.Button(id=wxID_PANELBOBOCALCULATE,
              label='Calculate', name='BO_Calculate', parent=self,
              pos=wx.Point(288, 222), size=wx.Size(128, 21), style=0)

        self.gridpageBoiler = wx.grid.Grid(id=-1,
              name='gridpageBoiler', parent=self,
              pos=wx.Point(40, 48), size=wx.Size(376, 168), style=0)

        self.st1pageBoiler = wx.StaticText(id=-1,
              label='Existing Boilers in the HC system',
              name='st1pageBoiler', parent=self, pos=wx.Point(40,
              32), style=0)

        self.st2pageBoiler = wx.StaticText(id=-1,
              label='Design assistant options:', name='st2pageBoiler',
              parent=self, pos=wx.Point(40, 272), style=0)
        self.st2pageBoiler.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.st3pageBoiler = wx.StaticText(id=-1,
              label='Maintain existing equipment ?', name='st3pageBoiler',
              parent=self, pos=wx.Point(40, 304), style=0)

        self.cb1pageBoiler = wx.CheckBox(id=-1,
              label='', name='cb1pageBoiler', parent=self,
              pos=wx.Point(288, 308), size=wx.Size(24, 13), style=0)
        self.cb1pageBoiler.SetValue(False)

        self.st4pageBoiler = wx.StaticText(id=-1,
              label='Type of boiler', name='st4pageBoiler',
              parent=self, pos=wx.Point(40, 344), style=0)

        self.choicepageBoiler = wx.Choice(choices=["steam boiler",
              "hot water (condensing)","hot water (standard)"], id=-1,
              name='choicepageBoiler', parent=self,
              pos=wx.Point(288, 336), size=wx.Size(130, 21), style=0)

        self.st5pageBoiler = wx.StaticText(id=-1,
              label='Minimum desired annual operation hours, h',
              name='st5pageBoiler', parent=self, pos=wx.Point(40,
              384), style=0)

        self.st6pageBoiler = wx.StaticText(id=-1,
              label='Maximum desired temperature lift, \xbaC',
              name='st6pageBoiler', parent=self, pos=wx.Point(40,
              424), style=0)

        self.st7pageBoiler = wx.StaticText(id=-1,
              label='Maximum desired condensing temperature, \xbaC',
              name='st7pageBoiler', parent=self, pos=wx.Point(40,
              464), style=0)

        self.st8pageBoiler = wx.StaticText(id=-1,
              label='Minimum desired evaporating temperature, \xbaC',
              name='st8pageBoiler', parent=self, pos=wx.Point(40,
              504), style=0)

        self.st9pageBoiler = wx.StaticText(id=-1,
              label='Only for absorption type:', name='st9pageBoiler',
              parent=self, pos=wx.Point(40, 536), style=0)

        self.st10pageBoiler = wx.StaticText(id=-1,
              label='Inlet temperature of heating fluid in generator, \xbaC',
              name='st10pageBoiler', parent=self,
              pos=wx.Point(40, 552), style=0)

        self.tc2pageBoiler = wx.TextCtrl(id=-1,
              name='tc2pageBoiler', parent=self,
              pos=wx.Point(288, 416), size=wx.Size(128, 21), style=0, value='')

        self.tc3pageBoiler = wx.TextCtrl(id=-1,
              name='tc3pageBoiler', parent=self,
              pos=wx.Point(288, 456), size=wx.Size(128, 21), style=0, value='')

        self.tc4pageBoiler = wx.TextCtrl(id=-1,
              name='tc4pageBoiler', parent=self,
              pos=wx.Point(288, 496), size=wx.Size(128, 21), style=0, value='')

        self.tc6pageBoiler = wx.TextCtrl(id=-1,
              name='tc6pageBoiler', parent=self,
              pos=wx.Point(640, 416), size=wx.Size(128, 21), style=0, value='')

        self.tc1pageBoiler = wx.TextCtrl(id=-1,
              name='tc1pageBoiler', parent=self,
              pos=wx.Point(288, 376), size=wx.Size(128, 21), style=0, value='')

        self.staticBox1 = wx.StaticBox(id=-1,
              label='Heat demand and availability with and without BO',
              name='staticBox1', parent=self, pos=wx.Point(440,
              40), size=wx.Size(336, 256), style=0)

        self.tc7pageBoiler = wx.TextCtrl(id=-1,
              name='tc7pageBoiler', parent=self,
              pos=wx.Point(640, 456), size=wx.Size(128, 21), style=0, value='')

        self.tc5pageBoiler = wx.TextCtrl(id=-1,
              name='tc5pageBoiler', parent=self,
              pos=wx.Point(288, 544), size=wx.Size(128, 21), style=0, value='')

        self.st11pageBoiler = wx.StaticText(id=-1,
              label='Pinch temperature \xb0C', name='st11pageBoiler',
              parent=self, pos=wx.Point(440, 424), style=0)

        self.st12pageBoiler = wx.StaticText(id=-1,
              label='Temperature gap \xb0K', name='st12pageBoiler',
              parent=self, pos=wx.Point(440, 464), style=0)

        self.buttonpageBoilerOk = wx.Button(id=-1,
              label='ok', name='buttonpageBoilerOk', parent=self,
              pos=wx.Point(576, 552), size=wx.Size(75, 23), style=0)

        self.buttonpageBoilerCancel = wx.Button(id=-1,
              label='cancel', name='buttonpageBoilerCancel',
              parent=self, pos=wx.Point(664, 552), size=wx.Size(75,
              23), style=0)

        self.buttonpageBoilerAdd = wx.Button(id=-1,
              label='add boiler', name='buttonpageBoilerAdd',
              parent=self, pos=wx.Point(40, 224), size=wx.Size(96,
              23), style=0)

        self.BOCalculate.Bind(wx.EVT_BUTTON, self.OnBOCalculateButton,
              id=wxID_PANELBOBOCALCULATE)

    def OnBOCalculateButton(self, event):

        global DB
        global MySql

        self.tc1pageBoiler.ChangeValue("1000")
#        ret = self.ModBridge.FunctionOneDataCheck(self.sql, DB, self.activeQid)
#        ret = self.modBO.selectBoiler(self.sql,self.db,1,1,1,2)
        BO.boiler()

