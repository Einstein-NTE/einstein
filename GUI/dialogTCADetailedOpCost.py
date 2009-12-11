#Boa:Dialog:dlgOpcost
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    dlgOpcost: Dialog that displays the "detailed operating cost"-Tabpages
#               (part of the TCA module)
#
#
#==============================================================================
#
#    Version No.: 0.01
#       Created by:          Florian Joebstl 15/09/2008  
#       Revised by:       
#
#       Changes to previous version:
#
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
from panelTCAOpTabpage import panelTCAOpTabpage
from einstein.GUI.status import Status

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)

def create(parent):
    return dlgOpcost(parent)

[wxID_DLGOPCOST, wxID_DLGOPCOSTBTNCANCEL, wxID_DLGOPCOSTBTNOK, 
 wxID_DLGOPCOSTTCNOTEBOOK, 
] = [wx.NewId() for _init_ctrls in range(4)]

class dlgOpcost(wx.Dialog):
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGOPCOST, name='', parent=prnt,
              pos=wx.Point(0, 0), size=wx.Size(617, 540),
              style=wx.DEFAULT_DIALOG_STYLE,
              title=_U('Detailed operating costs calculation'))
        self.SetClientSize(wx.Size(609, 513))

        self.tcNotebook = wx.Notebook(id=wxID_DLGOPCOSTTCNOTEBOOK,
              name='tcNotebook', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(595, 464), style=0)

        self.btnCancel = wx.Button(id=wxID_DLGOPCOSTBTNCANCEL, label=_U('Cancel'),
              name='btnCancel', parent=self, pos=wx.Point(528, 480),
              size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGOPCOSTBTNCANCEL)

        self.btnOk = wx.Button(id=wxID_DLGOPCOSTBTNOK, label=_U('Ok'),
              name='btnOk', parent=self, pos=wx.Point(440, 480),
              size=wx.Size(75, 23), style=0)
        self.btnOk.Bind(wx.EVT_BUTTON, self.OnBtnOkButton,
              id=wxID_DLGOPCOSTBTNOK)

    def __init_custom_ctrls(self, prnt):
        self.utilities = panelTCAOpTabpage(id=wx.NewId(), name='Utilities',
              parent=self.tcNotebook, pos=wx.Point(0, 0), size=wx.Size(504,
              438), style=wx.TAB_TRAVERSAL)  
        self.utilities.tHelp.SetLabel(_U("Cost for water, plant air, inert gas, refrigerant, sewerage, ..."))      
        self.tcNotebook.AddPage(imageId=-1, page=self.utilities, select=True, text='Utilities')
        
        self.opmaterials = panelTCAOpTabpage(id=wx.NewId(), name='Operating materials',
              parent=self.tcNotebook, pos=wx.Point(0, 0), size=wx.Size(504,
              438), style=wx.TAB_TRAVERSAL)
        self.opmaterials.tHelp.SetLabel(_U("chemicals e.g. for conditioning of boiler feed water, lubricants, \ncleaning materials, materials for maintenance and service)"))
        self.tcNotebook.AddPage(imageId=-1, page=self.opmaterials, select=False, text='Operating materials')
        
        self.labour = panelTCAOpTabpage(id=wx.NewId(), name='Labour',
              parent=self.tcNotebook, pos=wx.Point(0, 0), size=wx.Size(504,
              438), style=wx.TAB_TRAVERSAL)
        self.labour.tHelp.SetLabel(_U("labor for operating, on-site handling and storage, onsite pretreatment, hauling, supervision; \npersonnel, management personnel, maintenance personnel, energy agent, internal costs for \nanalyses and measurements, internal costs for inspection, supervision and control"))
        self.tcNotebook.AddPage(imageId=-1, page=self.labour, select=False, text='Labour')
        
        self.extcost = panelTCAOpTabpage(id=wx.NewId(), name='External costs',
              parent=self.tcNotebook, pos=wx.Point(0, 0), size=wx.Size(504,
              438), style=wx.TAB_TRAVERSAL)
        self.extcost.tHelp.SetLabel(_U("external maintenance personnel costs, external costs for analyses and measurements, \nOff-site Treatment, Off-site Disposal"))
        self.tcNotebook.AddPage(imageId=-1, page=self.extcost, select=False, text='External costs')
        
        self.compliance = panelTCAOpTabpage(id=wx.NewId(), name='Regulatory compliance costs',
              parent=self.tcNotebook, pos=wx.Point(0, 0), size=wx.Size(504,
              438), style=wx.TAB_TRAVERSAL)
        self.compliance.tHelp.SetLabel(_U("permits (if not in labour costs), mandatory trainings  (if not in labour costs), costs for mandatory \nmonitoring and inspection (if not in labour costs), fees/taxes, reporting (if not in labour costs)"))
        self.tcNotebook.AddPage(imageId=-1, page=self.compliance, select=False, text='Regulatory compliance costs')
        
        self.insurance = panelTCAOpTabpage(id=wx.NewId(), name='Insurance cost',
              parent=self.tcNotebook, pos=wx.Point(0, 0), size=wx.Size(504,
              438), style=wx.TAB_TRAVERSAL)
        self.insurance.tHelp.SetLabel('')
        self.tcNotebook.AddPage(imageId=-1, page=self.insurance, select=False, text='Insurance cost')
        
        self.liability = panelTCAOpTabpage(id=wx.NewId(), name='Future liability',
              parent=self.tcNotebook, pos=wx.Point(0, 0), size=wx.Size(504,
              438), style=wx.TAB_TRAVERSAL)
        self.liability.tHelp.SetLabel(_U("fines/penalties, legal costs, personal injury, property/natural resource damage, \nremediationcosts, (provisions for) clean up costs, (provisions for) treatment costs "))
        self.tcNotebook.AddPage(imageId=-1, page=self.liability, select=False, text='Future liability')
        
    def __init_data(self):
        self.utilities.items    = Status.mod.moduleTCA.data.detailedopcost[0][:]
        self.utilities.display()
        self.opmaterials.items  = Status.mod.moduleTCA.data.detailedopcost[1][:]
        self.opmaterials.display()
        self.labour.items       = Status.mod.moduleTCA.data.detailedopcost[2][:]
        self.labour.display()
        self.extcost.items      = Status.mod.moduleTCA.data.detailedopcost[3][:]
        self.extcost.display()
        self.compliance.items   = Status.mod.moduleTCA.data.detailedopcost[4][:]
        self.compliance.display()
        self.insurance.items    = Status.mod.moduleTCA.data.detailedopcost[5][:]
        self.insurance.display()
        self.liability.items    = Status.mod.moduleTCA.data.detailedopcost[6][:]
        self.liability.display()
    
    def store_data(self):
        Status.mod.moduleTCA.data.detailedopcost[0] = self.utilities.items
        Status.mod.moduleTCA.data.detailedopcost[1] = self.opmaterials.items
        Status.mod.moduleTCA.data.detailedopcost[2] = self.labour.items     
        Status.mod.moduleTCA.data.detailedopcost[3] = self.extcost.items  
        Status.mod.moduleTCA.data.detailedopcost[4] = self.compliance.items
        Status.mod.moduleTCA.data.detailedopcost[5] = self.insurance.items
        Status.mod.moduleTCA.data.detailedopcost[6] = self.liability.items
        

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.__init_custom_ctrls(parent)
        self.__init_data()

    def OnBtnCancelButton(self, event):
        self.save = False
        self.Destroy()
        event.Skip()

    def OnBtnOkButton(self, event):
        self.save = True
        self.Destroy()
        event.Skip()
        
        
