#Boa:Dialog:dlgChangeHX

from wx import *

def create(parent):
    return dlgChangeHX(parent)

[wxID_DLGCHANGEHX, wxID_DLGCHANGEHXBTNCANCEL, wxID_DLGCHANGEHXBTNOK, 
 wxID_DLGCHANGEHXCHGG, wxID_DLGCHANGEHXCHLG, wxID_DLGCHANGEHXCHLL, 
 wxID_DLGCHANGEHXCHMATTYPE, wxID_DLGCHANGEHXSTATICBOX1, 
 wxID_DLGCHANGEHXSTATICBOX2, wxID_DLGCHANGEHXSTATICBOX3, 
 wxID_DLGCHANGEHXSTATICBOX4, wxID_DLGCHANGEHXSTATICBOX5, 
 wxID_DLGCHANGEHXSTATICBOX6, wxID_DLGCHANGEHXSTATICBOX7, 
 wxID_DLGCHANGEHXSTATICBOX8, wxID_DLGCHANGEHXSTATICTEXT1, 
 wxID_DLGCHANGEHXSTATICTEXT10, wxID_DLGCHANGEHXSTATICTEXT11, 
 wxID_DLGCHANGEHXSTATICTEXT12, wxID_DLGCHANGEHXSTATICTEXT13, 
 wxID_DLGCHANGEHXSTATICTEXT14, wxID_DLGCHANGEHXSTATICTEXT15, 
 wxID_DLGCHANGEHXSTATICTEXT16, wxID_DLGCHANGEHXSTATICTEXT17, 
 wxID_DLGCHANGEHXSTATICTEXT18, wxID_DLGCHANGEHXSTATICTEXT19, 
 wxID_DLGCHANGEHXSTATICTEXT2, wxID_DLGCHANGEHXSTATICTEXT20, 
 wxID_DLGCHANGEHXSTATICTEXT21, wxID_DLGCHANGEHXSTATICTEXT22, 
 wxID_DLGCHANGEHXSTATICTEXT23, wxID_DLGCHANGEHXSTATICTEXT24, 
 wxID_DLGCHANGEHXSTATICTEXT3, wxID_DLGCHANGEHXSTATICTEXT4, 
 wxID_DLGCHANGEHXSTATICTEXT5, wxID_DLGCHANGEHXSTATICTEXT6, 
 wxID_DLGCHANGEHXSTATICTEXT7, wxID_DLGCHANGEHXSTATICTEXT8, 
 wxID_DLGCHANGEHXSTATICTEXT9, wxID_DLGCHANGEHXTBALPHAG, 
 wxID_DLGCHANGEHXTBALPHAL, wxID_DLGCHANGEHXTBALPHAPC, 
 wxID_DLGCHANGEHXTBPRESSURE, 
] = [wx.NewId() for _init_ctrls in range(43)]



class HXConsts:
    MAT_TYPE_SS = 'SS'
    MAT_TYPE_CS = 'CS'
    MAT_TYPE_CU = 'Cu'
    MAT_TYPE_NI = 'NI'
    
    
class DlgChangeHX(wx.Dialog):
    def _init_ctrls(self, prnt):
        self.recalc = False
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGCHANGEHX, name='dlgChangeHX',
              parent=prnt, pos=wx.Point(373, 250), size=wx.Size(493, 409),
              style=wx.DIALOG_MODAL | wx.DIALOG_NO_PARENT | wx.DEFAULT_DIALOG_STYLE,
              title='Change Heatexchanger - Parameters for calculation of HEX')
        self.SetClientSize(wx.Size(485, 382))

        self.staticBox1 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX1,
              label=_('4. Type of HEX'), name='staticBox1', parent=self,
              pos=wx.Point(8, 240), size=wx.Size(200, 104), style=0)

        self.btnOK = wx.Button(id=wxID_DLGCHANGEHXBTNOK,
              label=_('Recalcualte HEX'), name='btnOK', parent=self,
              pos=wx.Point(288, 352), size=wx.Size(91, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGCHANGEHXBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGCHANGEHXBTNCANCEL, label='Cancel',
              name='btnCancel', parent=self, pos=wx.Point(392, 352),
              size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGCHANGEHXBTNCANCEL)

        self.staticText1 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT1,
              label='liquid-liquid', name='staticText1', parent=self,
              pos=wx.Point(16, 264), size=wx.Size(52, 13), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX2,
              label=_('1. dTmin values'), name='staticBox2', parent=self,
              pos=wx.Point(8, 16), size=wx.Size(200, 88), style=0)

        self.staticBox3 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX3,
              label=_('2. material'), name='staticBox3', parent=self,
              pos=wx.Point(8, 112), size=wx.Size(200, 56), style=0)

        self.staticBox4 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX4,
              label=_('3. wall thickness of tubes or plates'),
              name='staticBox4', parent=self, pos=wx.Point(8, 176),
              size=wx.Size(200, 56), style=0)

        self.staticBox5 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX5,
              label=_('5. alpha values'), name='staticBox5', parent=self,
              pos=wx.Point(216, 16), size=wx.Size(256, 96), style=0)

        self.staticBox6 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX6,
              label=_('6. cost factor for materials required for installation'),
              name='staticBox6', parent=self, pos=wx.Point(216, 120),
              size=wx.Size(256, 64), style=0)

        self.staticBox7 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX7,
              label=_('7. pressure [bar]'), name='staticBox7', parent=self,
              pos=wx.Point(216, 192), size=wx.Size(256, 56), style=0)

        self.staticBox8 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX8,
              label=_('8. standart storage'), name='staticBox8', parent=self,
              pos=wx.Point(216, 256), size=wx.Size(256, 88), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT2,
              label=_('liquids [K]'), name='staticText2', parent=self,
              pos=wx.Point(24, 40), size=wx.Size(46, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT3,
              label=_('gases [K]'), name='staticText3', parent=self,
              pos=wx.Point(24, 56), size=wx.Size(45, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT4,
              label=_('phase change [K]'), name='staticText4', parent=self,
              pos=wx.Point(24, 72), size=wx.Size(84, 13), style=0)

        self.staticText5 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT5,
              label=_('material type'), name='staticText5', parent=self,
              pos=wx.Point(24, 136), size=wx.Size(63, 13), style=0)

        self.staticText6 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT6,
              label=_('s [mm]'), name='staticText6', parent=self,
              pos=wx.Point(24, 200), size=wx.Size(32, 13), style=0)

        self.staticText7 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT7,
              label=_('liquid-gaseus'), name='staticText7', parent=self,
              pos=wx.Point(16, 288), size=wx.Size(62, 13), style=0)

        self.staticText8 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT8,
              label='5', name='staticText8', parent=self, pos=wx.Point(152, 40),
              size=wx.Size(14, 13), style=0)

        self.staticText9 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT9,
              label='10', name='staticText9', parent=self, pos=wx.Point(152,
              56), size=wx.Size(12, 13), style=0)

        self.staticText10 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT10,
              label='2,5', name='staticText10', parent=self, pos=wx.Point(152,
              72), size=wx.Size(16, 13), style=0)

        self.staticText11 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT11,
              label='1', name='staticText11', parent=self, pos=wx.Point(152,
              200), size=wx.Size(32, 13), style=0)

        self.chLL = wx.Choice(choices=['plate','shell&tube'], id=wxID_DLGCHANGEHXCHLL, name='chLL',
              parent=self, pos=wx.Point(96, 264), size=wx.Size(104, 21),
              style=0)
        self.chLL.SetSelection(0)

        self.staticText12 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT12,
              label=_('gaseous-gaseus'), name='staticText12', parent=self,
              pos=wx.Point(16, 312), size=wx.Size(78, 13), style=0)

        self.chLG = wx.Choice(choices=['plate','shell&tube'], id=wxID_DLGCHANGEHXCHLG, name='chLG',
              parent=self, pos=wx.Point(96, 288), size=wx.Size(104, 21),
              style=0)
        self.chLG.SetSelection(0)

        self.chGG = wx.Choice(choices=['plate','shell&tube'], id=wxID_DLGCHANGEHXCHGG, name='chGG',
              parent=self, pos=wx.Point(96, 312), size=wx.Size(104, 21),
              style=0)
        self.chGG.SetSelection(0)

        self.chMatType = wx.Choice(choices=[HXConsts.MAT_TYPE_CU,HXConsts.MAT_TYPE_CS,HXConsts.MAT_TYPE_NI,HXConsts.MAT_TYPE_NI], id=wxID_DLGCHANGEHXCHMATTYPE,
              name='chMatType', parent=self, pos=wx.Point(96, 136),
              size=wx.Size(104, 21), style=0)
        self.chMatType.SetSelection(0)

        self.staticText13 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT13,
              label='liquides [W/m\xb2K]', name='staticText13', parent=self,
              pos=wx.Point(232, 40), size=wx.Size(79, 13), style=0)

        self.staticText14 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT14,
              label=_('gases [W/m\xb2K]'), name='staticText14', parent=self,
              pos=wx.Point(232, 64), size=wx.Size(72, 13), style=0)

        self.staticText15 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT15,
              label=_('phase change [W/m\xb2K]'), name='staticText15',
              parent=self, pos=wx.Point(232, 88), size=wx.Size(111, 13),
              style=0)

        self.tbAlphaL = wx.TextCtrl(id=wxID_DLGCHANGEHXTBALPHAL,
              name='tbAlphaL', parent=self, pos=wx.Point(352, 32),
              size=wx.Size(100, 21), style=0, value='5000')

        self.tbAlphaG = wx.TextCtrl(id=wxID_DLGCHANGEHXTBALPHAG,
              name='tbAlphaG', parent=self, pos=wx.Point(352, 56),
              size=wx.Size(100, 21), style=0, value='100')

        self.tbAlphaPC = wx.TextCtrl(id=wxID_DLGCHANGEHXTBALPHAPC,
              name='tbAlphaPC', parent=self, pos=wx.Point(352, 80),
              size=wx.Size(100, 21), style=0, value='10000')

        self.staticText16 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT16,
              label=_('additional % based on \ntotal equipment costs'),
              name='staticText16', parent=self, pos=wx.Point(232, 144),
              size=wx.Size(110, 26), style=0)

        self.staticText17 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT17,
              label='5', name='staticText17', parent=self, pos=wx.Point(424,
              152), size=wx.Size(24, 13), style=0)

        self.staticText18 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT18,
              label=_('pressure [bar]'), name='staticText18', parent=self,
              pos=wx.Point(232, 216), size=wx.Size(69, 13), style=0)

        self.tbPressure = wx.TextCtrl(id=wxID_DLGCHANGEHXTBPRESSURE,
              name='tbPressure', parent=self, pos=wx.Point(352, 216),
              size=wx.Size(100, 21), style=0, value='2')

        self.staticText19 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT19,
              label=_('insulation [mm]'), name='staticText19', parent=self,
              pos=wx.Point(232, 280), size=wx.Size(72, 13), style=0)

        self.staticText20 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT20,
              label=_('material'), name='staticText20', parent=self,
              pos=wx.Point(232, 296), size=wx.Size(38, 13), style=0)

        self.staticText21 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT21,
              label=_('connections'), name='staticText21', parent=self,
              pos=wx.Point(232, 312), size=wx.Size(57, 13), style=0)

        self.staticText22 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT22,
              label='10', name='staticText22', parent=self, pos=wx.Point(416,
              280), size=wx.Size(12, 13), style=0)

        self.staticText23 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT23,
              label=_('stainless steel'), name='staticText23', parent=self,
              pos=wx.Point(360, 296), size=wx.Size(67, 13), style=0)

        self.staticText24 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT24,
              label='4', name='staticText24', parent=self, pos=wx.Point(424,
              312), size=wx.Size(16, 13), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnBtnCancelButton(self, event):
        self.recalc = False
        self.Destroy()
        event.Skip()

    def OnBtnOKButton(self, event):
        self.recalc = True
        self.Destroy()
        event.Skip()
        
    def MaterialType(self):
        return  self.chMatType.GetStringSelection()
    
    def AlphaLiquid(self):
        return float(self.tbAlphaL.GetValue())
    
    def AlphaGas(self):
        return float(self.tbAlphaG.GetValue())
    
    def AlphaPC(self):
        return float(self.tbAlphaPC.GetValue())