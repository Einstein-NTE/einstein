#Boa:Dialog:dlgChangeHX
#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#    DlgChangeHX
#           
#------------------------------------------------------------------------------
#
#    Dialog for changing a heatexchanger in the HRModule
#           
#==============================================================================
#
#   Version No.: 0.02
#   Created by:         Florian Joebstl  01/09/2008
#   Last revised by:
#                       Florian Joebstl  03/09/2008                       
#
#   Changes to previous version:
#   03/09/2008: (FJ) Disable all not used fields based on hot and cold type index 
#   
#   
#------------------------------------------------------------------------------     
#   (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#   www.energyxperts.net / info@energyxperts.net
#
#   This program is free software: you can redistribute it or modify it under
#   the terms of the GNU general public license as published by the Free
#   Software Foundation (www.gnu.org).
#
#============================================================================== 


from wx import *
from einstein.modules.messageLogger import *

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

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
 wxID_DLGCHANGEHXSTATICTEXT16, wxID_PANEL1TBADDITIONAL, 
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
    MAT_TYPE_CU = 'C'
    MAT_TYPE_NI = 'NI'
        
    HX_TYPE_P = 'plate (PHE)'
    HX_TYPE_S = 'shell and tube (STHE)' #XXX
    
    
class DlgChangeHX(wx.Dialog):
    def _init_ctrls(self, prnt):
        self.recalc = False
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGCHANGEHX, name='dlgChangeHX',
              parent=prnt, pos=wx.Point(373, 250), size=wx.Size(493, 409),
              style=wx.DIALOG_MODAL | wx.DIALOG_NO_PARENT | wx.DEFAULT_DIALOG_STYLE,
              title=_U('Change Heatexchanger - Parameters for calculation of HEX'))
        self.SetClientSize(wx.Size(485, 382))

        self.staticBox1 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX1,
              label=_U('4. Type of HEX'), name='staticBox1', parent=self,
              pos=wx.Point(8, 240), size=wx.Size(200, 104), style=0)

        self.btnOK = wx.Button(id=wxID_DLGCHANGEHXBTNOK,
              label=_U('Recalcualte HEX'), name='btnOK', parent=self,
              pos=wx.Point(288, 352), size=wx.Size(91, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_DLGCHANGEHXBTNOK)

        self.btnCancel = wx.Button(id=wxID_DLGCHANGEHXBTNCANCEL, label=_U('Cancel'),
              name='btnCancel', parent=self, pos=wx.Point(392, 352),
              size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGCHANGEHXBTNCANCEL)

        self.staticText1 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT1,
              label=_U('liquid-liquid'), name='staticText1', parent=self,
              pos=wx.Point(16, 264), size=wx.Size(52, 13), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX2,
              label=_U('1. dTmin values'), name='staticBox2', parent=self,
              pos=wx.Point(8, 16), size=wx.Size(200, 88), style=0)

        self.staticBox3 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX3,
              label=_U('2. material'), name='staticBox3', parent=self,
              pos=wx.Point(8, 112), size=wx.Size(200, 56), style=0)

        self.staticBox4 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX4,
              label=_U('3. wall thickness of tubes or plates'),
              name='staticBox4', parent=self, pos=wx.Point(8, 176),
              size=wx.Size(200, 56), style=0)

        self.staticBox5 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX5,
              label=_U('5. alpha values'), name='staticBox5', parent=self,
              pos=wx.Point(216, 16), size=wx.Size(256, 96), style=0)

        self.staticBox6 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX6,
              label=_U('6. cost factor for materials required for installation'),
              name='staticBox6', parent=self, pos=wx.Point(216, 120),
              size=wx.Size(256, 64), style=0)

        self.staticBox7 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX7,
              label=_U('7. pressure [bar]'), name='staticBox7', parent=self,
              pos=wx.Point(216, 192), size=wx.Size(256, 56), style=0)

        self.staticBox8 = wx.StaticBox(id=wxID_DLGCHANGEHXSTATICBOX8,
              label=_U('8. standart storage'), name='staticBox8', parent=self,
              pos=wx.Point(216, 256), size=wx.Size(256, 88), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT2,
              label=_U('liquids [K]'), name='staticText2', parent=self,
              pos=wx.Point(24, 40), size=wx.Size(46, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT3,
              label=_U('gases [K]'), name='staticText3', parent=self,
              pos=wx.Point(24, 56), size=wx.Size(45, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT4,
              label=_U('phase change [K]'), name='staticText4', parent=self,
              pos=wx.Point(24, 72), size=wx.Size(84, 13), style=0)

        self.staticText5 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT5,
              label=_U('material type'), name='staticText5', parent=self,
              pos=wx.Point(24, 136), size=wx.Size(63, 13), style=0)

        self.staticText6 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT6,
              label=_U('s [mm]'), name='staticText6', parent=self,
              pos=wx.Point(24, 200), size=wx.Size(32, 13), style=0)

        self.staticText7 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT7,
              label=_U('liquid-gaseus'), name='staticText7', parent=self,
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

        self.chLL = wx.Choice(choices=[HXConsts.HX_TYPE_P, HXConsts.HX_TYPE_S], id=wxID_DLGCHANGEHXCHLL, name='chLL',
              parent=self, pos=wx.Point(96, 264), size=wx.Size(104, 21),
              style=0)
        self.chLL.SetSelection(0)

        self.staticText12 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT12,
              label=_U('gaseous-gaseus'), name='staticText12', parent=self,
              pos=wx.Point(16, 312), size=wx.Size(78, 13), style=0)

        self.chLG = wx.Choice(choices=[HXConsts.HX_TYPE_P, HXConsts.HX_TYPE_S], id=wxID_DLGCHANGEHXCHLG, name='chLG',
              parent=self, pos=wx.Point(96, 288), size=wx.Size(104, 21),
              style=0)
        self.chLG.SetSelection(1)

        self.chGG = wx.Choice(choices=[HXConsts.HX_TYPE_P, HXConsts.HX_TYPE_S], id=wxID_DLGCHANGEHXCHGG, name='chGG',
              parent=self, pos=wx.Point(96, 312), size=wx.Size(104, 21),
              style=0)
        self.chGG.SetSelection(1)

        self.chMatType = wx.Choice(choices=[HXConsts.MAT_TYPE_SS,HXConsts.MAT_TYPE_CS,HXConsts.MAT_TYPE_NI,HXConsts.MAT_TYPE_CU], id=wxID_DLGCHANGEHXCHMATTYPE,
              name='chMatType', parent=self, pos=wx.Point(96, 136),
              size=wx.Size(104, 21), style=0)
        self.chMatType.SetSelection(0)

        self.staticText13 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT13,
              label=_U('liquides [W/m\xb2K]'), name='staticText13', parent=self,
              pos=wx.Point(232, 40), size=wx.Size(79, 13), style=0)

        self.staticText14 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT14,
              label=_U('gases [W/m\xb2K]'), name='staticText14', parent=self,
              pos=wx.Point(232, 64), size=wx.Size(72, 13), style=0)

        self.staticText15 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT15,
              label=_U('phase change [W/m\xb2K]'), name='staticText15',
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
              label=_U('additional % based on \ntotal equipment costs'),
              name='staticText16', parent=self, pos=wx.Point(232, 144),
              size=wx.Size(110, 26), style=0)
        
        self.tbAdditional = wx.TextCtrl(id=wxID_PANEL1TBADDITIONAL,
              name='tbAdditional', parent=self, pos=wx.Point(352,
              152),size=wx.Size(100, 21), style=0, value='0')

        self.staticText18 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT18,
              label=_U('pressure [bar]'), name='staticText18', parent=self,
              pos=wx.Point(232, 216), size=wx.Size(69, 13), style=0)

        self.tbPressure = wx.TextCtrl(id=wxID_DLGCHANGEHXTBPRESSURE,
              name='tbPressure', parent=self, pos=wx.Point(352, 216),
              size=wx.Size(100, 21), style=0, value='2')

        self.staticText19 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT19,
              label=_U('insulation [mm]'), name='staticText19', parent=self,
              pos=wx.Point(232, 280), size=wx.Size(72, 13), style=0)

        self.staticText20 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT20,
              label=_U('material'), name='staticText20', parent=self,
              pos=wx.Point(232, 296), size=wx.Size(38, 13), style=0)

        self.staticText21 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT21,
              label=_U('connections'), name='staticText21', parent=self,
              pos=wx.Point(232, 312), size=wx.Size(57, 13), style=0)

        self.staticText22 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT22,
              label='10', name='staticText22', parent=self, pos=wx.Point(416,
              280), size=wx.Size(12, 13), style=0)

        self.staticText23 = wx.StaticText(id=wxID_DLGCHANGEHXSTATICTEXT23,
              label=_U('stainless steel'), name='staticText23', parent=self,
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
        return self.chMatType.GetStringSelection()
    
    def AlphaLiquid(self):
        return float(self.tbAlphaL.GetValue())
    
    def AlphaGas(self):
        return float(self.tbAlphaG.GetValue())
    
    def AlphaPC(self):
        return float(self.tbAlphaPC.GetValue())
    
    def PressureValue(self):
        return float(self.tbPressure.GetValue())
    
    def AdditionalCostPercent(self):
        return float(self.tbAdditional.GetValue())
    
    def HXType(self,hoti,coldi):
        # 0=liquid 1=gas 2=condensation
        if (hoti==2): #condensation --> gas            
            hoti=1
        if (coldi==2):#condensation --> liquid
            coldi=0
        
        if (hoti==0) and (coldi==0):
            return self.chLL.GetStringSelection()
        if (hoti==1) and (coldi==1):
            return self.chGG.GetStringSelection()
                           
        return self.chLG.GetStringSelection()
    
    def LockChoices(self,hoti,coldi):
        self.tbAlphaPC.Enabled = False
        self.tbAlphaL.Enabled  = False
        self.tbAlphaG.Enabled  = False
        
        if (hoti==2): #condensation --> gas
            self.tbAlphaPC.Enabled = True
            hoti=1
        if (coldi==2):#condensation --> liquid
            self.tbAlphaPC.Enabled = True
            coldi=0
            
        #enable AlphaGas and AlphaLiquid if one of both is Gas/Liquid
        if (hoti==1) or (coldi==1):
             self.tbAlphaG.Enabled = True            
        if (hoti==0) and (coldi==0):
            self.tbAlphaL.Enabled = True
        
        #enable plate / shell&tube choice
        if (hoti==0) and (coldi==0):
            self.chGG.Enabled = False
            self.chLG.Enabled = False
            return
        if (hoti==1) and (coldi==1):
            self.chLL.Enabled = False
            self.chLG.Enabled = False
            return        
                        
        self.chGG.Enabled = False
        self.chLL.Enabled = False               
    
    def LockInput(self):        
        self.btnOK.Enabled =False
        self.chGG.Enabled = False
        self.chLG.Enabled = False
        self.chLL.Enabled = False
        self.chMatType.Enabled =False
        self.tbAlphaG.Enabled =False
        self.tbAlphaL.Enabled = False
        self.tbAlphaPC.Enabled = False
        self.tbPressure.Enabled = False
        self.tbAdditional.Enabled = False
