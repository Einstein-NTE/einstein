# -*- coding: cp1252 -*-
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	PanelQ0: Tool main page (page 0) -> project selection
#
#==============================================================================
#
#	Version No.: 0.12
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger 02/05/2008
#                           Tom Sobota 04/05/2008
#                           Hans Schweiger 05/05/2008
#                           Stoyan Danov    06/06/2008
#                           Hans Schweiger  10/06/2008
#                           Stoyan Danov    11/06/2008
#                           Hans Schweiger  12/06/2008
#                           Stoyan Danov    17/06/2008
#                           Stoyan Danov    18/06/2008
#                           Hans Schweiger  18/06/2008
#
#       Changes to previous version:
#       02/05/08:       AlternativeProposalNo added in queries for table qproduct
#       04/05/2008      Changed position of OK/Quit buttons
#       05/05/2008      Eventhandlers linked to OK/Cancel
#       06/06/2008      New label/tooltips according to new displayClasses defined;
#                       do_layout still not adapted
#       10/06/2008 HS   Minor bug corrections to get it running:
#                       SetValue for eliminated labels tc25_1/tc25_2 eliminated
#       17/06/2008 SD   adapt to new unitdict
#       18/06/2008 SD   create display()
#                   HS  some bug corrections; SetValue in date-entry cancelled
#                       temporarily due to problems ...
#                       NACE code list added
#
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	http://www.energyxperts.net/
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================

import wx
import pSQL
import HelperClass
from status import Status
from GUITools import *
from displayClasses import *
from units import *

# constants that control the default field sizes

HEIGHT          =  27 #SD
LABELWIDTHLEFT  = 260
LABELWIDTHRIGHT = 500
DATAENTRYWIDTH  = 100
UNITSWIDTH      =  90

class PanelQ1(wx.Panel):
    def __init__(self, parent, main):
        self.main = main
        self.parent = parent
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)
        self.__do_layout()
        self.branch = ""

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

##        wx.Panel.__init__(self, id=-1, name='PanelQ1', parent=parent,
##              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=wx.BK_DEFAULT|wx.BK_TOP)
        wx.Panel.__init__(self, id=-1, name='PanelQ1', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.page0 = wx.Panel(self.notebook)
        self.page1 = wx.Panel(self.notebook)
        self.page2 = wx.Panel(self.notebook)

        self.notebook.AddPage(self.page0, _('General information')) #SD put this later in do_layout
        self.notebook.AddPage(self.page1, _('Statistical and economical data'))
        self.notebook.AddPage(self.page2, _('Information on products'))

        self.sizer_5_staticbox = wx.StaticBox(self.page0, -1, _("General information")) #SD added
        self.sizer_5_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_7_staticbox = wx.StaticBox(self.page1, -1, _("Statistical and economical data")) #SD added
        self.sizer_7_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_8_staticbox = wx.StaticBox(self.page1, -1, _("Period of operation")) #SD added
        self.sizer_8_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_9_staticbox = wx.StaticBox(self.page2, -1, _("Information on products")) #SD added
        self.sizer_9_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_10_staticbox = wx.StaticBox(self.page2, -1, _("Energy consumption by product")) #SD added
        self.sizer_10_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_11_staticbox = wx.StaticBox(self.page2, -1, _("Product list")) #SD added
        self.sizer_11_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        f = FieldSizes(wHeight=HEIGHT,wLabel=LABELWIDTHLEFT,wData=DATAENTRYWIDTH,wUnits=UNITSWIDTH)#SD

        # panel 0 - General information
        self.tc1 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Name of the company"),
                             tip=_("Legal name of the company"))


        self.tc2 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("City / Country"),
                             tip=_("City where production is located"))


        self.tc3 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Name of contact person"),
                             tip=_(" "))

        self.tc4 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Position of contact person in the company"),
                             tip=_(" "))

        self.tc5 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Address"),
                             tip=_(" "))

        self.tc6 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Telephone No"),
                             tip=_(" "))

        self.tc7 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Fax No"),
                             tip=_(" "))

        self.tc8 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("E-mail"),
                             tip=_(" "))

        self.tc9 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Description of the industry"),
                             tip=_(" "))

        self.tc10 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Branch"),
                             tip=_(" "))

        self.tc11 = ChoiceEntry(self.page0, 
                               values=['NACE code list','one source'],
                               label=_("NACE code branch"),
                               tip=_(" "))

        self.tc12 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Sub-branch"),
                             tip=_(""))


        self.tc13 = ChoiceEntry(self.page0, 
                               values=['NACE code sublist','one source'],
                               label=_("NACE code sub-branch"),
                               tip=_(" "))



        # panel 1 - Left. Statistical and economical data


        self.tc14 = IntEntry(self.page1,
                              minval=0, maxval=999999, value=0,
                              unitdict=None,
                              label=_("Number of employees"),
                              tip=_(" "))

        self.tc15 = FloatEntry(self.page1,
                              ipart=10, decimals=2, minval=0., maxval=1.0e+9, value=0.,
                              unitdict='PRICE',
                              label=_("Annual turnover"),
                              tip=_("Million of euro per year"))

        self.tc16 = FloatEntry(self.page1,
                              ipart=10, decimals=1, minval=0., maxval=1.0e+9, value=0.,
                              unitdict='PRICE',
                              label=_("Annual production cost"),
                              tip=_("Specify total factor inputs for production"))

        self.tc17 = IntEntry(self.page1,
                              minval=2000, maxval=2050, value=0,
                              unitdict=None,
                              label=_("Base year for economic data"),
                              tip=_("Specify the reference year for economic parameters"))

        self.tc18 = FloatEntry(self.page1,
                              ipart=3, decimals=1, minval=0., maxval=100, value=0.,
                              unitdict=None,
                              label=_("Growth rate of the production volume foreseen for the next 5 years [%/year]"),
                              tip=_(" "))

        self.tc19 = ChoiceEntry(self.page1, 
                               values=YESNO,
                               label=_("Is the company independent?"),
                               tip=_(" "))

        self.tc20 = FloatEntry(self.page1,
                              ipart=10, decimals=1, minval=0., maxval=1.0e+9, value=0.,
                              unitdict='PRICE',
                              label=_("Yearly O&M heat & cold"),
                              tip=_(" "))

        self.tc21 = FloatEntry(self.page1,
                              ipart=10, decimals=1, minval=0., maxval=1.0e+9, value=0.,
                              unitdict='PRICE',
                              label=_("Yearly O&M electrical"),
                              tip=_(" "))

#new fields added SD
        self.tc22 = FloatEntry(self.page1,
                              ipart=2, decimals=2, minval=0., maxval=99.9, value=0.,
                              unitdict=None,
                              label=_("Percentage of fuel cost on overall production cost"),
                              tip=_(" "))

        self.tc23 = FloatEntry(self.page1,
                              ipart=2, decimals=2, minval=0., maxval=99.9, value=0.,
                              unitdict=None,
                              label=_("Percentage of electricity cost on overall production cost"),
                              tip=_(" "))        

        # panel 1 - Right. Statistical and economical data

        self.tc24 = FloatEntry(self.page1,
                              ipart=2, decimals=2, minval=0., maxval=24, value=0.,
                              unitdict=None,
                              label=_("Total hours of operation per working day"),
                              tip=_(" "))

        self.tc25 = FloatEntry(self.page1,
                              ipart=2, decimals=0, minval=0., maxval=10, value=0.,
                              unitdict=None,
                              label=_("Number of shifts"),
                              tip=_(" "))

        self.tc26 = FloatEntry(self.page1,
                              ipart=3, decimals=0, minval=0, maxval=365, value=0.,
                              unitdict=None,
                              label=_("Days of production / operation per year"),
                              tip=_(" "))



        self.st27 = wx.StaticText(id=-1,
                                    label=_('Principal periods of holidays or stops for maintenance'),
                                    name='st25',
                                    parent=self.page1,
                                    pos=wx.Point(416, 178),
                                    style=0)

#three start-stop dates entered
        self.tc27_10 = DateEntry(self.page1,
                              value='',
                              label=_("Period of holidays No. 1 - start date"),
                              tip=_(" "))

        self.tc27_11 = DateEntry(self.page1,
                              value='',
                              label=_("Period of holidays No. 1 - stop date"),
                              tip=_(" "))

        self.tc27_20 = DateEntry(self.page1,
                              value='',
                              label=_("Period of holidays No. 2 - start date"),
                              tip=_(" "))

        self.tc27_21 = DateEntry(self.page1,
                              value='',
                              label=_("Period of holidays No. 2 - stop date"),
                              tip=_(" "))

        self.tc27_30 = DateEntry(self.page1,
                              value='',
                              label=_("Period of holidays No. 3 - start date"),
                              tip=_(" "))

        self.tc27_31 = DateEntry(self.page1,
                              value='',
                              label=_("Period of holidays No. 3 - stop date"),
                              tip=_(" "))


        # panel 2 - Left. Products

        self.stInfo6 = wx.StaticText(id=-1,
                                     label=_('Information on products'),
                                     name='stInfo6',
                                     parent=self.page2,
                                     pos=wx.Point(100, 10),
                                     style=0)
        self.stInfo6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))


        self.tc30 = TextEntry(self.page2,maxchars=255,value='',
                             label=_("Type of product"),
                             tip=_(" "))

        self.tc31 = ChoiceEntry(self.page2, 
                               values=['Product code list to be defined'],
                               label=_("Product's code"),
                               tip=_(" "))

        self.tc32 = FloatEntry(self.page2,
                              ipart=10, decimals=2, minval=0., maxval=1.e+9, value=0.,
                              unitdict=None,
                              label=_("Quantity of product(s) per year [product-units/year]"),
                              tip=_(" "))

        self.tc33 = TextEntry(self.page2,maxchars=255,value='',
                             label=_("Measurement unit for\nproduct quantity"),
                             tip=_(" "))

        self.tc34 = FloatEntry(self.page2,
                              ipart=10, decimals=2, minval=0., maxval=1e+9, value=0.,
                              unitdict='PRICE',
                              label=_("Annual turnover per product"),
                              tip=_(" "))

#substitute by StaticBox
        self.stInfo5 = wx.StaticText(id=-1,
                                     label=_('Energy consumption by product'),
                                     name='stInfo5',
                                     parent=self.page2,
                                     pos=wx.Point(100, 256),
                                     style=0)
        self.stInfo5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.tc35 = FloatEntry(self.page2,
                              ipart=10, decimals=2, minval=0., maxval=1.e+9, value=0.,
                              unitdict='ENERGY',
                              label=_("Electricity consumption per product"),
                              tip=_(" "))

        self.tc36 = FloatEntry(self.page2,
                              ipart=10, decimals=2, minval=0., maxval=1.e+9, value=0.,
                              unitdict='ENERGY',
                              label=_("Fuel consumption per product(LCV)"),
                              tip=_("Specify energy content of fuels in LCV "))

        # panel 2 - Right. Product list

#substitute by StaticBox
        self.stInfo4 = wx.StaticText(id=-1,
                                     label=_('Product list'),
                                     name='stInfo4',
                                     parent=self.page2,
                                     pos=wx.Point(550, 10),
                                     style=0)
        self.stInfo4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))


        self.listBoxProducts = wx.ListBox(id=-1,
                                          choices=[],
                                          name='listBoxProducts',
                                          parent=self.page2,
                                          pos=wx.Point(516,48),
                                          size=wx.Size(192, 300),
                                          style=0)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxProductsListboxClick, self.listBoxProducts)

        self.buttonAddProduct = wx.Button(id=-1,
                                          label=_('Add product'),
                                          name='buttonAddProduct',
                                          parent=self.page2,
                                          pos=wx.Point(516, 400),
                                          size=wx.Size(192, 32),
                                          style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddProduct, self.buttonAddProduct)

        self.buttonDeleteProduct = wx.Button(id=-1,
                                             label=_('Delete product'),
                                             name='buttonDeleteProduct',
                                             parent=self.page2,
                                             pos=wx.Point(516, 433),
                                             size=wx.Size(192, 32),
                                             style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteProduct, self.buttonDeleteProduct)

        self.buttonOK = wx.Button(self, wx.ID_OK, 'OK')
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)

        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)#SD added
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.notebook, 3, wx.EXPAND, 0)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)
        sizer_1.Add(sizerOKCancel, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer_1)
        self.Layout()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------      
    def OnListBoxProductsListboxClick(self, event):
        self.productName = str(self.listBoxProducts.GetStringSelection())
        p = Status.DB.qproduct.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].Product[str(self.listBoxProducts.GetStringSelection())][0]
        self.tc30.SetValue(str(p.Product))
        self.tc31.SetValue(str(p.ProductCode))
        self.tc32.SetValue(str(p.QProdYear))
        self.tc33.SetValue(str(p.ProdUnit))
        self.tc34.SetValue(str(p.TurnoverProd))
        self.tc35.SetValue(str(p.ElProd))
        self.tc36.SetValue(str(p.FuelProd))
        event.Skip()

    def OnSelectBranch(self, event):
        branch = self.tc11.GetValue(text=True).split(":")[1]
        self.branch = branch
        self.fillChoiceOfNaceCode
        event.Skip()

    def OnButtonAddProduct(self, event):
        self.clearProduct()
        self.fillPage()

    def OnButtonDeleteProduct(self, event):
        Status.prj.deleteProduct(self.productName)
        self.clearProduct()
        self.fillPage()

    def OnButtonCancel(self, event):
        self.clear()
        self.fillPage()

    def OnButtonOK(self, event):
        if Status.PId <> 0 and self.notebook.GetSelection()<2:
            if self.check(self.tc1.GetValue()) <> 'NULL' and \
                Status.DB.questionnaire.Name[self.check(self.tc1.GetValue())][0].Questionnaire_ID == Status.PId:

                branch = self.tc11.GetValue(text=True).split(":")[1]
                self.branch = branch
                subBranch = self.tc13.GetValue(text=True).split(":")[1]
                tmp = {
                    "Name":self.check(self.tc1.GetValue()),
                    "City":self.check(self.tc2.GetValue()),
                    "DescripIndustry":self.check(self.tc9.GetValue()),
                    "Branch":self.check(branch),
                    "SubBranch":self.check(subBranch),
                    "Contact":self.check(self.tc3.GetValue()),
                    "Role":self.check(self.tc4.GetValue()),
                    "Address":self.check(self.tc5.GetValue()),
                    "Phone":self.check(self.tc6.GetValue()),
                    "Fax":self.check(self.tc7.GetValue()),
                    "Email":self.check(self.tc8.GetValue()),
                    "NEmployees":self.check(self.tc14.GetValue()),
                    "Turnover":self.check(self.tc15.GetValue()),
                    "ProdCost":self.check(self.tc16.GetValue()),
                    "BaseYear":self.check(self.tc17.GetValue()),
                    "Growth":self.check(self.tc18.GetValue()),
                    "Independent":self.check(self.tc19.GetValue()),
                    "OMThermal":self.check(self.tc20.GetValue()),
                    "OMElectrical":self.check(self.tc21.GetValue()),
                    "PercentFuelTotcost":self.check(self.tc22.GetValue()),
                    "PercentElTotcost":self.check(self.tc23.GetValue()),
                    "HPerDayInd":self.check(self.tc24.GetValue()),
                    "NShifts":self.check(self.tc25.GetValue()),
                    "NDaysInd":self.check(self.tc26.GetValue()),
                    "NoProdStart_1":self.check(self.tc27_10.GetValue()),
                    "NoProdStop_1":self.check(self.tc27_11.GetValue()),
                    "NoProdStart_2":self.check(self.tc27_20.GetValue()),
                    "NoProdStop_2":self.check(self.tc27_21.GetValue()),
                    "NoProdStart_3":self.check(self.tc27_30.GetValue()),
                    "NoProdStop_3":self.check(self.tc27_31.GetValue())
                    }
                                
                q = Status.DB.questionnaire.Questionnaire_ID[Status.PId][0]
                q.update(tmp)
                Status.SQL.commit()

                Status.prj.setStatus("Q")
                          
            else:
                self.main.showError(_("Name has to be an unique value!"))
            
#..............................................................................
# aqui parte que guarda la información del producto
                
        print "PanelQ1 (OK): selected page",self.notebook.GetSelection()
        if Status.PId <> 0 and self.notebook.GetSelection()==2:
            
            if self.check(self.tc30.GetValue()) <> 'NULL' and len(Status.DB.qproduct.Product[self.tc30.GetValue()].\
                                                                  Questionnaire_id[Status.PId].\
                                                                  AlternativeProposalNo[Status.ANo]) == 0:
                tmp = {
                    "Questionnaire_id":Status.PId,
                    "AlternativeProposalNo":Status.ANo,
                    "Product":self.check(self.tc30.GetValue()),
                    "ProductCode":self.check(self.tc31.entry.GetStringSelection()),
                    "QProdYear":self.check(self.tc32.GetValue()),
                    "ProdUnit":self.check(self.tc33.GetValue()),
                    "TurnoverProd":self.check(self.tc34.GetValue()),
                    "ElProd":self.check(self.tc35.GetValue()),
                    "FuelProd":self.check(self.tc36.GetValue())
                    }

                Status.DB.qproduct.insert(tmp)               
                Status.SQL.commit()
                self.fillProductList()

            elif self.check(self.tc30.GetValue()) <> 'NULL' and len(Status.DB.qproduct.Product[self.tc30.GetValue()].\
                                                                    Questionnaire_id[Status.PId].\
                                                                    AlternativeProposalNo[Status.ANo]) == 1:
                tmp = {
                    "Product":self.check(self.tc30.GetValue()),
                    "ProductCode":self.check(self.tc31.GetValue()),
                    "QProdYear":self.check(self.tc32.GetValue()),
                    "ProdUnit":self.check(self.tc33.GetValue()),
                    "TurnoverProd":self.check(self.tc34.GetValue()),
                    "ElProd":self.check(self.tc35.GetValue()),
                    "FuelProd":self.check(self.tc36.GetValue())
                    }
                q = Status.DB.qproduct.Product[self.tc30.GetValue()].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillProductList()
                self.productName = self.tc30.GetValue()
                          
            else:
                self.main.showError(_("Product must be an unique value!"))

#------------------------------------------------------------------------------
#--- Private methods
#------------------------------------------------------------------------------      

    def __makeColorPanel(self, color):
        p = wx.Panel(self, -1)
        win = ColorPanel.ColoredPanel(p, color)
        p.win = win
        def OnCPSize(evt, win=win):
            win.SetPosition((0,0))
            win.SetSize(evt.GetSize())
        p.Bind(wx.EVT_SIZE, OnCPSize)
        return p
#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------      

    def display(self):
        self.fillChoiceOfNaceCode()
        self.clear()
        self.fillPage()
        self.Show()

    def fillChoiceOfNaceCode(self):
        naceDict,naceSubDict = Status.prj.getNACEDict(self.branch)
        self.tc11.entry.Clear()
        self.tc13.entry.Clear()
        for code in naceDict.keys():
            self.tc11.entry.Append("%s:%s"%(code,naceDict[code]))
        for code in naceSubDict.keys():
            self.tc13.entry.Append("%s:%s"%(code,naceSubDict[code]))

        return naceDict,naceSubDict

    def fillPage(self):
        if Status.PId == 0:
            return

        naceDict,naceSubDict = self.fillChoiceOfNaceCode()

        q = Status.DB.questionnaire.Questionnaire_ID[Status.PId][0]
        
        self.tc1.SetValue(str(q.Name))
        self.tc2.SetValue(str(q.City))
        self.tc3.SetValue(str(q.Contact))
        self.tc4.SetValue(str(q.Role))
        self.tc5.SetValue(str(q.Address))
        self.tc6.SetValue(str(q.Phone))
        self.tc7.SetValue(str(q.Fax))
        self.tc8.SetValue(str(q.Email))
        self.tc9.SetValue(str(q.DescripIndustry))
        self.tc10.SetValue(str(q.Branch))
        if str(q.Branch) in naceDict.values(): self.tc11.SetValue(findKey(naceDict,str(q.Branch)))
        self.tc12.SetValue(str(q.SubBranch))
        if str(q.SubBranch) in naceSubDict.values(): self.tc13.SetValue(findKey(naceSubDict,str(q.SubBranch)))
        self.tc14.SetValue(str(q.NEmployees))
        self.tc15.SetValue(str(q.Turnover))
        self.tc16.SetValue(str(q.ProdCost))
        self.tc17.SetValue(str(q.BaseYear))
        self.tc18.SetValue(str(q.Growth))
        self.tc19.SetValue(str(q.Independent))
        self.tc20.SetValue(str(q.OMThermal))
        self.tc21.SetValue(str(q.OMElectrical))
        self.tc22.SetValue(str(q.PercentFuelTotcost))
        self.tc23.SetValue(str(q.PercentElTotcost))
        self.tc24.SetValue(str(q.HPerDayInd))
        self.tc25.SetValue(str(q.NShifts))
        self.tc26.SetValue(str(q.NDaysInd))
#XXXXXXX CHECK XXXXXXXXX: SetValue of date entry gave problems ...
#        self.tc27_10.SetValue(str(q.NoProdStart_1))
#        self.tc27_11.SetValue(str(q.NoProdStop_1))
#        self.tc27_20.SetValue(str(q.NoProdStart_2))
#        self.tc27_21.SetValue(str(q.NoProdStop_2))
#        self.tc27_30.SetValue(str(q.NoProdStart_3))
#        self.tc27_31.SetValue(str(q.NoProdStop_3))
        self.fillProductList()



    def fillProductList(self):
        self.listBoxProducts.Clear()
        if len(Status.DB.qproduct.Questionnaire_id[Status.PId]) > 0:
            for n in Status.DB.qproduct.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]:
                self.listBoxProducts.Append(n.Product)

    def check(self, value):
        if value <> "" and value <> "None":
            return value
        else:
            return 'NULL'


    def clear(self):
        self.tc1.SetValue('')
        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
        self.tc6.SetValue('')
        self.tc7.SetValue('')
        self.tc8.SetValue('')
        self.tc9.SetValue('')
        self.tc10.SetValue('')
        self.tc12.SetValue('')
        self.tc14.SetValue('')
        self.tc15.SetValue('')
        self.tc16.SetValue('')
        self.tc17.SetValue('')
        self.tc18.SetValue('')
        self.tc19.SetValue('')
        self.tc20.SetValue('')
        self.tc21.SetValue('')
        self.tc22.SetValue('')#SD
        self.tc23.SetValue('')#SD
        self.tc24.SetValue('')
        self.tc25.SetValue('')
        self.tc26.SetValue('')

#XXXXXXX CHECK XXXXXXXXX: SetValue of date entry gave problems ...
#        self.tc27_10.SetValue('')
#        self.tc27_11.SetValue('')
#        self.tc27_20.SetValue('')
#        self.tc27_21.SetValue('')
#        self.tc27_30.SetValue('')
#        self.tc27_31.SetValue('')
                           
        self.tc30.SetValue('')
        self.tc31.SetValue('')
        self.tc32.SetValue('')
        self.tc33.SetValue('')
        self.tc34.SetValue('')
        self.tc35.SetValue('')
        self.tc36.SetValue('')

    def clearProduct(self):
        self.tc30.SetValue('')
        self.tc31.SetValue('')
        self.tc32.SetValue('')
        self.tc33.SetValue('')
        self.tc34.SetValue('')
        self.tc35.SetValue('')
        self.tc36.SetValue('')

if __name__ == '__main__':
    import pSQL
    import MySQLdb
    import gettext

    gettext.install("einstein", "locale", unicode=False)
    language = gettext.translation("einstein", "locale", languages=['en'])
    language.install()

    DBName = 'einstein'
    Status.SQL = MySQLdb.connect(host='localhost', user='root', passwd='tom.tom', db=DBName)
    Status.DB =  pSQL.pSQL(Status.SQL, DBName)

    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(800, 600), title="Einstein - panelQ1")
    panel = PanelQ1(frame, None)

    frame.Show(True)
    app.MainLoop()

