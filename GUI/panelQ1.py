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
#	Version No.: 0.04
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger 02/05/2008
#                           Tom Sobota 04/05/2008
#                           Hans Schweiger 05/05/2008
#
#       Changes to previous version:
#       02/05/08:       AlternativeProposalNo added in queries for table qproduct
#       04/05/2008      Changed position of OK/Quit buttons
#       05/05/2008      Eventhandlers linked to OK/Cancel
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

class PanelQ1(wx.Panel):
    def __init__(self, parent, main):
        self.main = main
        self.parent = parent
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)
        self.__do_layout()
        self.fillPage()

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ1', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=wx.BK_DEFAULT|wx.BK_TOP)

        self.notebook = wx.Notebook(self, -1, style=0)
        self.page0 = wx.Panel(self.notebook)
        self.page1 = wx.Panel(self.notebook)
        self.page2 = wx.Panel(self.notebook)

        self.notebook.AddPage(self.page0, _('General information'))
        self.notebook.AddPage(self.page1, _('Statistical and economical data'))
        self.notebook.AddPage(self.page2, _('Information on products'))

        # panel 0 - General information
        self.stInfo1 = wx.StaticText(id=-1,
                                     label=_('General information'),
                                     name='stInfo1',
                                     parent=self.page0,
                                     pos=wx.Point(100, 10),
                                     style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS,wx.NORMAL,wx.BOLD, False, 'Tahoma'))

        self.st1 = wx.StaticText(id=-1,
                                 label=_('Name of the company'),
                                 name='st1',
                                 parent=self.page0,
                                 pos=wx.Point(16,48),
                                 style=0)

        self.tc1 = wx.TextCtrl(id=-1,
                               name='tc1',
                               parent=self.page0,
                               pos=wx.Point(200, 48),
                               size=wx.Size(400, 21),
                               style=0,
                               value='')

        self.st2 = wx.StaticText(id=-1,
                                 label=_('City / Country'),
                                 name='st2',
                                 parent=self.page0,
                                 pos=wx.Point(16,88),
                                 style=0)

        self.tc2 = wx.TextCtrl(id=-1,
                               name='tc2',
                               parent=self.page0,
                               pos=wx.Point(200,88),
                               size=wx.Size(400,21),
                               style=0,
                               value='')

        self.st3 = wx.StaticText(id=-1,
                                 label=_('Name of contact person'),
                                 name='st3',
                                 parent=self.page0,
                                 pos=wx.Point(16,128),
                                 style=0)

        self.tc3 = wx.TextCtrl(id=-1,
                               name='tc3',
                               parent=self.page0,
                               pos=wx.Point(200,128),
                               size=wx.Size(400, 21),
                               style=0,
                               value='')

        self.st4 = wx.StaticText(id=-1,
                                 label=_('Role of contact person\nin the company'),
                                 name='st4',
                                 parent=self.page0,
                                 pos=wx.Point(16, 168),
                                 style=0)

        self.tc4 = wx.TextCtrl(id=-1,
                               name='tc4',
                               parent=self.page0,
                               pos=wx.Point(200,168),
                               size=wx.Size(400, 21),
                               style=0,
                               value='')

        self.st5 = wx.StaticText(id=-1,
                                 label=_('Address'),
                                 name='st5',
                                 parent=self.page0,
                                 pos=wx.Point(16, 208),
                                 style=0)

        self.tc5 = wx.TextCtrl(id=-1,
                               name='tc5',
                               parent=self.page0,
                               pos=wx.Point(200, 208),
                               size=wx.Size(400, 56),
                               style=wx.TE_MULTILINE,
                               value='')

        self.st6 = wx.StaticText(id=-1,
                                 label=_('Telephone No'),
                                 name='st6',
                                 parent=self.page0,
                                 pos=wx.Point(16, 286),
                                 style=0)

        self.tc6 = wx.TextCtrl(id=-1,
                               name='tc6',
                               parent=self.page0,
                               pos=wx.Point(200, 286),
                               size=wx.Size(400, 21),
                               style=0,
                               value='')


        self.st7 = wx.StaticText(id=-1,
                                 label=_('Fax No'),
                                 name='st7',
                                 parent=self.page0,
                                 pos=wx.Point(16, 328),
                                 style=0)

        self.tc7 = wx.TextCtrl(id=-1,
                               name='tc7',
                               parent=self.page0,
                               pos=wx.Point(200, 328),
                               size=wx.Size(400, 21),
                               style=0,
                               value='')

        self.st8 = wx.StaticText(id=-1,
                                 label=_('E-mail'),
                                 name='st8',
                                 parent=self.page0,
                                 pos=wx.Point(16, 368),
                                 style=0)

        self.tc8 = wx.TextCtrl(id=-1,
                               name='tc8',
                               parent=self.page0,
                               pos=wx.Point(200, 368),
                               size=wx.Size(400, 21),
                               style=0,
                               value='')

        self.st9 = wx.StaticText(id=-1,
                                 label=_('Description of the industry'),
                                 name='st9',
                                 parent=self.page0,
                                 pos=wx.Point(16, 408),
                                 style=0)

        self.tc9 = wx.TextCtrl(id=-1,
                               name='tc9',
                               parent=self.page0,
                               pos=wx.Point(200, 408),
                               size=wx.Size(400,56),
                               style=wx.TE_MULTILINE,
                               value='')

        self.st10 = wx.StaticText(id=-1,
                                  label=_('Branch'),
                                  name='st10',
                                  parent=self.page0,
                                  pos=wx.Point(16, 468),
                                  style=0)

        self.tc10 = wx.TextCtrl(id=-1,
                                name='tc10',
                                parent=self.page0,
                                pos=wx.Point(200, 468),
                                size=wx.Size(400, 21),
                                style=0,
                                value='')

        self.st11 = wx.StaticText(id=-1,
                                  label=_('NACE code'),
                                  name='st11',
                                  parent=self.page0,
                                  pos=wx.Point(16, 498),
                                  style=0)

        self.choiceOfNaceCode = wx.Choice(id=-1,
                                          choices=[],
                                          name='choiceOfNaceCode',
                                          parent=self.page0,
                                          pos=wx.Point(200,498),
                                          size=wx.Size(200, 21),
                                          style=0)

        # panel 1 - Left. Statistical and economical data


        self.stInfo2 = wx.StaticText(id=-1,
                                     label=_('Statistical and economical data'),
                                     name='stInfo2',
                                     parent=self.page1,
                                     pos=wx.Point(100,10),
                                     style=0)
        self.stInfo2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        
        self.st14 = wx.StaticText(id=-1,
                                  label=_('Number of employees'),
                                  name='st14',
                                  parent=self.page1,
                                  pos=wx.Point(16, 48),
                                  style=0)

        self.tc14 = wx.TextCtrl(id=-1,
                                name='tc14',
                                parent=self.page1,
                                pos=wx.Point(220, 48),
                                size=wx.Size(100, 21),
                                style=0,
                                value='')

        self.st15 = wx.StaticText(id=-1,
                                  label=_('Annual turnover (M?/year)'),
                                  name='st15',
                                  parent=self.page1,
                                  pos=wx.Point(16, 88),
                                  style=0)

        self.tc15 = wx.TextCtrl(id=-1,
                                name='tc15',
                                parent=self.page1,
                                pos=wx.Point(220, 88),
                                size=wx.Size(100, 21),
                                style=0,
                                value='')

        self.st16 = wx.StaticText(id=-1,
                                  label=_('Annual production cost\n(M?/year)'),
                                  name='st16',
                                  parent=self.page1,
                                  pos=wx.Point(16, 128),
                                  style=0)

        self.tc16 = wx.TextCtrl(id=-1,
                                name='tc16',
                                parent=self.page1,
                                pos=wx.Point(220, 128),
                                size=wx.Size(150, 21),
                                style=0,
                                value='')

        self.st17 = wx.StaticText(id=-1,
                                  label=_('Base year for ec. Data'),
                                  name='st17',
                                  parent=self.page1,
                                  pos=wx.Point(16, 168),
                                  style=0)

        self.tc17 = wx.TextCtrl(id=-1,
                                name='tc17',
                                parent=self.page1,
                                pos=wx.Point(220, 168),
                                size=wx.Size(100, 21),
                                style=0,
                                value='')

        self.st18 = wx.StaticText(id=-1,
                                  label=_('Growth rate of the production volume\nforeseen for the next 5 years (%/year)'),
                                  name='st18',
                                  parent=self.page1,
                                  pos=wx.Point(16, 210),
                                  style=0)

        self.tc18 = wx.TextCtrl(id=-1,
                                name='tc18',
                                parent=self.page1,
                                pos=wx.Point(220, 208),
                                size=wx.Size(150, 21),
                                style=0,
                                value='')

        self.st19 = wx.StaticText(id=-1,
                                  label=_('Is the company independent?\n(yes/no)'),
                                  name='st19',
                                  parent=self.page1,
                                  pos=wx.Point(16, 248),
                                  style=0)

        self.tc19 = wx.TextCtrl(id=-1,
                                name='tc19',
                                parent=self.page1,
                                pos=wx.Point(220, 248),
                                size=wx.Size(50, 21),
                                style=0,
                                value='')

        self.st20 = wx.StaticText(id=-1,
                                  label=_('Yearly O&M heat & cold (?/year)'),
                                  name='st20',
                                  parent=self.page1,
                                  pos=wx.Point(16, 288),
                                  style=0)

        self.tc20 = wx.TextCtrl(id=-1,
                                name='tc20',
                                parent=self.page1,
                                pos=wx.Point(220, 288),
                                size=wx.Size(150, 21),
                                style=0,
                                value='')

        self.st21 = wx.StaticText(id=-1,
                                  label=_('Yearly O&M electrical (?/year)'),
                                  name='st21',
                                  parent=self.page1,
                                  pos=wx.Point(16, 328),
                                  style=0)

        self.tc21 = wx.TextCtrl(id=-1,
                                name='tc21',
                                parent=self.page1,
                                pos=wx.Point(220, 328),
                                size=wx.Size(150, 21),
                                style=0,
                                value='')

        # panel 1 - Right. Statistical and economical data

        self.stInfo3 = wx.StaticText(id=-1,
                                     label=_('Period of operation'),
                                     name='stInfo3',
                                     parent=self.page1,
                                     pos=wx.Point(550, 10),
                                     style=0)
        self.stInfo3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.st22 = wx.StaticText(id=-1,
                                  label=_('Total hours of operation\nper working day (h/day)'),
                                  name='st22',
                                  parent=self.page1,
                                  pos=wx.Point(416, 48),
                                  style=0)

        self.tc22 = wx.TextCtrl(id=-1,
                                name='tc22',
                                parent=self.page1,
                                pos=wx.Point(620, 48),
                                size=wx.Size(50, 21),
                                style=0,
                                value='')

        self.st23 = wx.StaticText(id=-1,
                                  label=_('Number of shifts'),
                                  name='st23',
                                  parent=self.page1,
                                  pos=wx.Point(416, 88),
                                  style=0)

        self.tc23 = wx.TextCtrl(id=-1,
                                name='tc23',
                                parent=self.page1,
                                pos=wx.Point(620, 88),
                                size=wx.Size(50, 21),
                                style=0,
                                value='')

        self.st24 = wx.StaticText(id=-1,
                                  label=_('Days of production /\nOperation per year (days)'),
                                  name='st24',
                                  parent=self.page1,
                                  pos=wx.Point(416, 128),
                                  style=0)

        self.tc24 = wx.TextCtrl(id=-1,
                                name='tc24',
                                parent=self.page1,
                                pos=wx.Point(620, 128),
                                size=wx.Size(50, 21),
                                style=0,
                                value='')

        self.st25_1 = wx.StaticText(id=-1,
                                    label=_('Principal period of holidays or stops for maintenance'),
                                    name='st25',
                                    parent=self.page1,
                                    pos=wx.Point(416, 178),
                                    style=0)
        self.st25_1a = wx.StaticText(id=-1,
                                     label=_('Start date'),
                                     parent=self.page1,
                                     pos=wx.Point(416, 208),
                                     style=0)
        self.st25_1b = wx.StaticText(id=-1,
                                     label=_('End date'),
                                     parent=self.page1,
                                     pos=wx.Point(580, 208),
                                     style=0)

        self.tc25_1 = wx.TextCtrl(id=-1,
                                  name='tc25_1',
                                  parent=self.page1,
                                  pos=wx.Point(486, 208),
                                  size=wx.Size(90, 21),
                                  style=0,
                                  value='')

        self.tc25_2 = wx.TextCtrl(id=-1,
                                  name='tc25_2',
                                  parent=self.page1,
                                  pos=wx.Point(650, 208),
                                  size=wx.Size(90, 21),
                                  style=0,
                                  value='')


        # panel 2 - Left. Products

        self.stInfo6 = wx.StaticText(id=-1,
                                     label=_('Information on products'),
                                     name='stInfo6',
                                     parent=self.page2,
                                     pos=wx.Point(100, 10),
                                     style=0)
        self.stInfo6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))


        self.st26 = wx.StaticText(id=-1,
                                  label=_('Type of product'),
                                  name='st26',
                                  parent=self.page2,
                                  pos=wx.Point(16, 48),
                                  style=0)

        self.tc26 = wx.TextCtrl(id=-1,
                                name='tc26',
                                parent=self.page2,
                                pos=wx.Point(220, 48),
                                size=wx.Size(200, 21),
                                style=0,
                                value='')

        self.st27 = wx.StaticText(id=-1,
                                  label=_('Product code'),
                                  name='st27',
                                  parent=self.page2,
                                  pos=wx.Point(16, 88),
                                  style=0)

        self.tc27 = wx.TextCtrl(id=-1,
                                name='tc27',
                                parent=self.page2,
                                pos=wx.Point(220, 88),
                                size=wx.Size(200, 21),
                                style=0,
                                value='')

        self.st28 = wx.StaticText(id=-1,
                                  label=_('Quantity of product(s) per\nyear (product-units/year)'),
                                  name='st28',
                                  parent=self.page2,
                                  pos=wx.Point(16, 128),
                                  style=0)

        self.tc28 = wx.TextCtrl(id=-1,
                                name='tc28',
                                parent=self.page2,
                                pos=wx.Point(220, 128),
                                size=wx.Size(200, 21),
                                style=0,
                                value='')

        self.st29 = wx.StaticText(id=-1,
                                  label=_('Measurement unit for\nproduct quantity'),
                                  name='st29',
                                  parent=self.page2,
                                  pos=wx.Point(16, 168),
                                  style=0)

        self.tc29 = wx.TextCtrl(id=-1,
                                name='tc29',
                                parent=self.page2,
                                pos=wx.Point(220, 168),
                                size=wx.Size(50, 21),
                                style=0,
                                value='')

        self.st32 = wx.StaticText(id=-1,
                                  label=_('Electricity consumption per\nproduct (MWh / year)'),
                                  name='st32',
                                  parent=self.page2,
                                  pos=wx.Point(16, 210),
                                  style=0)

        self.tc31 = wx.TextCtrl(id=-1,
                                name='tc31',
                                parent=self.page2,
                                pos=wx.Point(220, 210),
                                size=wx.Size(100, 21),
                                style=0,
                                value='')


        self.stInfo5 = wx.StaticText(id=-1,
                                     label=_('Energy consumption by product'),
                                     name='stInfo5',
                                     parent=self.page2,
                                     pos=wx.Point(100, 256),
                                     style=0)
        self.stInfo5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.st31 = wx.StaticText(id=-1,
                                  label=_('Fuel consumption per\nproduct (MWh/year) (LCV)'),
                                  name='st31',
                                  parent=self.page2,
                                  pos=wx.Point(16, 280),
                                  style=0)

        self.tc32 = wx.TextCtrl(id=-1,
                                name='tc32',
                                parent=self.page2,
                                pos=wx.Point(220, 280),
                                size=wx.Size(200, 21),
                                style=0,
                                value='')

        self.st30 = wx.StaticText(id=-1,
                                  label=_('Anual turnover per\nproduct (M?/year)'),
                                  name='st30',
                                  parent=self.page2,
                                  pos=wx.Point(16, 328),
                                  style=0)

        self.tc30 = wx.TextCtrl(id=-1,
                                name='tc30',
                                parent=self.page2,
                                pos=wx.Point(220, 328),
                                size=wx.Size(200, 21),
                                style=0,
                                value='')


        # panel 2 - Right. Product list

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
        self.tc26.SetValue(str(p.Product))
        self.tc27.SetValue(str(p.ProductCode))
        self.tc28.SetValue(str(p.QProdYear))
        self.tc29.SetValue(str(p.ProdUnit))
        self.tc30.SetValue(str(p.TurnoverProd))
        self.tc32.SetValue(str(p.ElProd))
        self.tc31.SetValue(str(p.FuelProd))
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
                tmp = {
                    "Name":self.check(self.tc1.GetValue()),
                    "City":self.check(self.tc2.GetValue()),
                    "DescripIndustry":self.check(self.tc9.GetValue()),
                    "Branch":self.check(self.tc10.GetValue()),                                      
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
                    "HPerDayInd":self.check(self.tc22.GetValue()),
                    "NShifts":self.check(self.tc23.GetValue()),
                    "NDaysInd":self.check(self.tc24.GetValue()),
                    "NoProdStart":self.check(self.tc25_1.GetValue()),
                    "NoProdStop":self.check(self.tc25_2.GetValue())
                    }
                
                if str(self.choiceOfNaceCode.GetStringSelection()) <> 'None':
                    tmp["DBNaceCode_id"] = Status.DB.dbnacecode.CodeNACE[str(self.choiceOfNaceCode.GetStringSelection())][0].DBNaceCode_ID
                
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
            
            if self.check(self.tc26.GetValue()) <> 'NULL' and len(Status.DB.qproduct.Product[self.tc26.GetValue()].\
                                                                  Questionnaire_id[Status.PId].\
                                                                  AlternativeProposalNo[Status.ANo]) == 0:
                tmp = {
                    "Questionnaire_id":Status.PId,
                    "AlternativeProposalNo":Status.ANo,
                    "Product":self.check(self.tc26.GetValue()),
                    "ProductCode":self.check(self.tc27.GetValue()),
                    "QProdYear":self.check(self.tc28.GetValue()),
                    "ProdUnit":self.check(self.tc29.GetValue()),
                    "TurnoverProd":self.check(self.tc30.GetValue()),
                    "ElProd":self.check(self.tc32.GetValue()),
                    "FuelProd":self.check(self.tc31.GetValue())
                    }

                Status.DB.qproduct.insert(tmp)               
                Status.SQL.commit()
                self.fillProductList()

            elif self.check(self.tc26.GetValue()) <> 'NULL' and len(Status.DB.qproduct.Product[self.tc26.GetValue()].\
                                                                    Questionnaire_id[Status.PId].\
                                                                    AlternativeProposalNo[Status.ANo]) == 1:
                tmp = {
                    "Product":self.check(self.tc26.GetValue()),
                    "ProductCode":self.check(self.tc27.GetValue()),
                    "QProdYear":self.check(self.tc28.GetValue()),
                    "ProdUnit":self.check(self.tc29.GetValue()),
                    "TurnoverProd":self.check(self.tc30.GetValue()),
                    "ElProd":self.check(self.tc32.GetValue()),
                    "FuelProd":self.check(self.tc31.GetValue())
                    }
                q = Status.DB.qproduct.Product[self.tc26.GetValue()].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillProductList()
                self.productName = self.tc26.GetValue()
                          
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

    def fillChoiceOfNaceCode(self):
        self.choiceOfNaceCode.Clear()
        self.choiceOfNaceCode.Append ("None")
        for n in Status.DB.dbnacecode.CodeNACE["%"]:
            self.choiceOfNaceCode.Append(n.CodeNACE)
        self.choiceOfNaceCode.SetSelection(0)



    def fillPage(self):
        if Status.PId == 0:
            return
        q = Status.DB.questionnaire.Questionnaire_ID[Status.PId][0]
        self.tc1.SetValue(str(q.Name))
        self.tc2.SetValue(str(q.City))
        self.tc9.SetValue(str(q.DescripIndustry))
        self.tc10.SetValue(str(q.Branch))
        self.tc3.SetValue(str(q.Contact))
        self.tc4.SetValue(str(q.Role))
        self.tc5.SetValue(str(q.Address))
        self.tc6.SetValue(str(q.Phone))
        self.tc7.SetValue(str(q.Fax))
        self.tc8.SetValue(str(q.Email))
        self.tc14.SetValue(str(q.NEmployees))
        self.tc15.SetValue(str(q.Turnover))
        self.tc16.SetValue(str(q.ProdCost))
        self.tc17.SetValue(str(q.BaseYear))
        self.tc18.SetValue(str(q.Growth))
        self.tc19.SetValue(str(q.Independent))
        self.tc20.SetValue(str(q.OMThermal))
        self.tc21.SetValue(str(q.OMElectrical))
        self.tc22.SetValue(str(q.HPerDayInd))
        self.tc23.SetValue(str(q.NShifts))
        self.tc24.SetValue(str(q.NDaysInd))
        self.tc25_1.SetValue(str(q.NoProdStart))
        self.tc25_2.SetValue(str(q.NoProdStop))
        if q.DBNaceCode_id <> None:
            self.choiceOfNaceCode.SetSelection(self.choiceOfNaceCode.FindString(str(Status.DB.dbnacecode.DBNaceCode_ID[q.DBNaceCode_id][0].CodeNACE)))
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
        self.tc9.SetValue('')
        self.tc10.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
        self.tc6.SetValue('')
        self.tc7.SetValue('')
        self.tc8.SetValue('')
        self.tc14.SetValue('')
        self.tc15.SetValue('')
        self.tc16.SetValue('')
        self.tc17.SetValue('')
        self.tc18.SetValue('')
        self.tc19.SetValue('')
        self.tc20.SetValue('')
        self.tc21.SetValue('')
        self.tc22.SetValue('')
        self.tc23.SetValue('')
        self.tc24.SetValue('')
        self.tc25_1.SetValue('')
        self.tc25_2.SetValue('')
        self.tc26.SetValue('')
        self.tc27.SetValue('')
        self.tc28.SetValue('')
        self.tc29.SetValue('')
        self.tc30.SetValue('')
        self.tc32.SetValue('')
        self.tc31.SetValue('')

    def clearProduct(self):
        self.tc26.SetValue('')
        self.tc27.SetValue('')
        self.tc28.SetValue('')
        self.tc29.SetValue('')
        self.tc30.SetValue('')
        self.tc31.SetValue('')
        self.tc32.SetValue('')

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

