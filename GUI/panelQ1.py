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
#                           Tom Sobota      01/07/2008
#                           Hans Schwieger  03/07/2008
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
#        1/07/2008 TS   General fields arranging
#       02/07/2008: HS  Paint it orange
#                       Some bug-fixes (SetValue('') clears not only the selection
#                       but also the list of choices in ChoiceEntry
#                       -> commented out in tc19
#                       -> call of self.clear() BEFORE filling list of NACE codes
#       03/07/2008: HS  bug-fix in read/write of parameter "Independent" (tc19)
#       16/07/2008: HS  bug-fix: findKey in reading of Independent ? [yes/no] 
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
from fonts import *

# constants that control the default sizes
# 1. font sizes
TYPE_SIZE_LEFT    =   9
TYPE_SIZE_MIDDLE  =   9
TYPE_SIZE_RIGHT   =   9
TYPE_SIZE_TITLES  =  10

# 2. field sizes
HEIGHT               =  27
HEIGHT_MIDDLE        =  32
HEIGHT_RIGHT         =  32
LABEL_WIDTH_LEFT     = 300
LABEL_WIDTH_MIDDLE   = 500
LABEL_WIDTH_RIGHT    = 300
DATA_ENTRY_WIDTH     = 100
DATA_ENTRY_WIDTH_LEFT= 300
UNITS_WIDTH          =  90

# 3. vertical separation between fields
VSEP_LEFT            =   2
VSEP_MIDDLE          =   4
VSEP_RIGHT           =   4

ORANGE = '#FF6000'
TITLE_COLOR = ORANGE


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

        wx.Panel.__init__(self, id=-1, name='PanelQ1', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580), style=0)
        self.Hide()

        # access to font properties object
        fp = FontProperties()

        self.notebook = wx.Notebook(self, -1, style=0)
        self.notebook.SetFont(fp.getFont())

        self.page0 = wx.Panel(self.notebook) # left panel
        self.notebook.AddPage(self.page0, _('General information'))
        self.page0.SetForegroundColour(TITLE_COLOR)
        self.page0.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.page1 = wx.Panel(self.notebook) # middle left panel
        self.notebook.AddPage(self.page1, _('Statistical and economical data'))
        self.page1.SetForegroundColour(TITLE_COLOR)
        self.page1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.page2 = wx.Panel(self.notebook) # middle right panel
        self.notebook.AddPage(self.page2, _('Period of operation'))
        self.page2.SetForegroundColour(TITLE_COLOR)
        self.page2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.page3 = wx.Panel(self.notebook) # right panel
        self.notebook.AddPage(self.page3, _('Information on products'))
        self.page3.SetForegroundColour(TITLE_COLOR)
        self.page3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_general_information = wx.StaticBox(self.page0, -1, _("General information"))
        self.frame_general_information.SetForegroundColour(TITLE_COLOR)
        self.frame_general_information.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_statistical_data = wx.StaticBox(self.page1, -1, _("Statistical and economical data"))
        self.frame_statistical_data.SetForegroundColour(TITLE_COLOR)
        self.frame_statistical_data.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_period_operation = wx.StaticBox(self.page2, -1, _("Period of operation"))
        self.frame_period_operation.SetForegroundColour(TITLE_COLOR)
        self.frame_period_operation.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_information_products = wx.StaticBox(self.page3, -1, _("Information on products"))
        self.frame_information_products.SetForegroundColour(TITLE_COLOR)
        self.frame_information_products.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_energy_consumption = wx.StaticBox(self.page3, -1, _("Energy consumption by product"))
        self.frame_energy_consumption.SetForegroundColour(TITLE_COLOR)
        self.frame_energy_consumption.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.frame_product_list = wx.StaticBox(self.page3, -1, _("Product list"))
        self.frame_product_list.SetForegroundColour(TITLE_COLOR)
        self.frame_product_list.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.st27 = wx.StaticText(self.page2,-1,
                                  label=_('Principal periods of holidays or stops for maintenance'))

        # set font for titles
        # 1. save actual font parameters on the stack
        fp.pushFont()
        # 2. change size and weight
        fp.changeFont(size=TYPE_SIZE_TITLES, weight=wx.BOLD)
        self.frame_general_information.SetFont(fp.getFont())
        self.frame_statistical_data.SetFont(fp.getFont())
        self.frame_period_operation.SetFont(fp.getFont())
        self.frame_information_products.SetFont(fp.getFont())
        self.frame_energy_consumption.SetFont(fp.getFont())
        self.frame_product_list.SetFont(fp.getFont())
        self.st27.SetFont(fp.getFont())

        # 3. recover previous font state
        fp.popFont()


        fs = FieldSizes(wHeight=HEIGHT,wLabel=LABEL_WIDTH_LEFT,
                       wData=DATA_ENTRY_WIDTH_LEFT,wUnits=UNITS_WIDTH)

        #
        # left tab controls
        # tab 0 - General information
        #
        fp.pushFont()
        fp.changeFont(size=TYPE_SIZE_LEFT)

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

        self.tc11 = TextEntry(self.page0,maxchars=255,value='',
                             label=_("Sub-branch"),
                             tip=_(""))


#        fs = FieldSizes(wData=DATA_ENTRY_WIDTH_LEFT / 3)
#HS2008-07-02 shifted down, so that field size for choice entry remains large
        self.tc12 = ChoiceEntry(self.page0, 
                               values=['NACE code list','one source'],
                               label=_("NACE code branch"),
                               tip=_(" "))

        self.tc13 = ChoiceEntry(self.page0, 
                               values=['NACE code sublist','one source'],
                               label=_("NACE code sub-branch"),
                               tip=_(" "))

        fs = FieldSizes(wData=DATA_ENTRY_WIDTH_LEFT / 3)

        #
        # middle left tab controls
        #
        # tab 1 - Statistical and economical data
        #
        fp.changeFont(size=TYPE_SIZE_MIDDLE)
        f = FieldSizes(wHeight=HEIGHT_MIDDLE,wLabel=LABEL_WIDTH_MIDDLE)

        self.tc14 = IntEntry(self.page1,
                              minval=0, maxval=999999, value=0,
                              unitdict=None,
                              label=_("Number of employees"),
                              tip=_(" "))

        self.tc15 = FloatEntry(self.page1,
                              decimals=2, minval=0., maxval=1.0e+9, value=0.,
                              unitdict='PRICE',
                              label=_("Annual turnover"),
                              tip=_("Million of euro per year"))

        self.tc16 = FloatEntry(self.page1,
                              decimals=1, minval=0., maxval=1.0e+9, value=0.,
                              unitdict='PRICE',
                              label=_("Annual production cost"),
                              tip=_("Specify total factor inputs for production"))

        self.tc17 = IntEntry(self.page1,
                              minval=2000, maxval=2050, value=0,
                              unitdict=None,
                              label=_("Base year for economic data"),
                              tip=_("Specify the reference year for economic parameters"))

        self.tc18 = FloatEntry(self.page1,
                              decimals=1, minval=0., maxval=100, value=0.,
                              unitdict=None,
                              label=_("Growth rate of the production volume foreseen for the next 5 years [%/year]"),
                              tip=_(" "))

        self.tc19 = ChoiceEntry(self.page1,
                               values=TRANSYESNO.values(),
                               label=_("Is the company independent?"),
                               tip=_(" "))

        self.tc20 = FloatEntry(self.page1,
                              decimals=1, minval=0., maxval=1.0e+9, value=0.,
                              unitdict='PRICE',
                              label=_("Yearly O&M heat & cold"),
                              tip=_(" "))

        self.tc21 = FloatEntry(self.page1,
                              decimals=1, minval=0., maxval=1.0e+9, value=0.,
                              unitdict='PRICE',
                              label=_("Yearly O&M electrical"),
                              tip=_(" "))

        self.tc22 = FloatEntry(self.page1,
                              decimals=2, minval=0., maxval=99.9, value=0.,
                              unitdict=None,
                              label=_("Percentage of fuel cost on overall production cost"),
                              tip=_(" "))

        self.tc23 = FloatEntry(self.page1,
                              decimals=2, minval=0., maxval=99.9, value=0.,
                              unitdict=None,
                              label=_("Percentage of electricity cost on overall production cost"),
                              tip=_(" "))        

        #
        # middle right tab controls
        # tab 2. Period of operation
        #
        self.tc24 = FloatEntry(self.page2,
                              decimals=2, minval=0., maxval=24, value=0.,
                              unitdict=None,
                              label=_("Total hours of operation per working day"),
                              tip=_(" "))

        self.tc25 = FloatEntry(self.page2,
                               decimals=0, minval=0., maxval=10., value=0.,
                               unitdict=None,
                               label=_("Number of shifts"),
                               tip=_(" "))

        self.tc26 = FloatEntry(self.page2,
                               decimals=0, minval=0., maxval=365., value=0.,
                               unitdict=None,
                               label=_("Days of production / operation per year"),
                               tip=_(" "))

        self.tc27_10 = DateEntry(self.page2,
                              #value='',
                              label=_("Period of holidays No. 1 - start date"),
                              tip=_(" "))

        self.tc27_11 = DateEntry(self.page2,
                              #value='',
                              label=_("Period of holidays No. 1 - stop date"),
                              tip=_(" "))

        self.tc27_20 = DateEntry(self.page2,
                              #value='',
                              label=_("Period of holidays No. 2 - start date"),
                              tip=_(" "))

        self.tc27_21 = DateEntry(self.page2,
                              #value='',
                              label=_("Period of holidays No. 2 - stop date"),
                              tip=_(" "))

        self.tc27_30 = DateEntry(self.page2,
                              #value='',
                              label=_("Period of holidays No. 3 - start date"),
                              tip=_(" "))

        self.tc27_31 = DateEntry(self.page2,
                              #value='',
                              label=_("Period of holidays No. 3 - stop date"),
                              tip=_(" "))

        #
        # right tab controls
        #
        # panel 3.Left. Product list
        fp.changeFont(size=TYPE_SIZE_RIGHT)
        f = FieldSizes(wHeight=HEIGHT_RIGHT,wLabel=LABEL_WIDTH_RIGHT)

        self.listBoxProducts = wx.ListBox(self.page3,-1, choices=[])
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxProductsListboxClick, self.listBoxProducts)

        # panel 3.Right top. Information on products

        self.tc30 = TextEntry(self.page3,maxchars=255,value='',
                             label=_("Type of product"),
                             tip=_(" "))

        self.tc31 = ChoiceEntry(self.page3, 
                               values=PRODUCTCODES.values(),
                               label=_("Product's code"),
                               tip=_(" "))

        self.tc32 = FloatEntry(self.page3,
                              decimals=2, minval=0., maxval=1.e+9, value=0.,
                              unitdict=None,
                              label=_("Quantity of product(s) per year [product-units/year]"),
                              tip=_(" "))

        self.tc33 = TextEntry(self.page3,maxchars=255,value='',
                             label=_("Measurement unit for\nproduct quantity"),
                             tip=_(" "))

        self.tc34 = FloatEntry(self.page3,
                              decimals=2, minval=0., maxval=1e+9, value=0.,
                              unitdict='PRICE',
                              label=_("Annual turnover per product"),
                              tip=_(" "))

        # panel 3.Right bottom. Energy consumption by product

        self.tc35 = FloatEntry(self.page3,
                              decimals=2, minval=0., maxval=1.e+9, value=0.,
                              unitdict='ENERGY',
                              label=_("Electricity consumption per product"),
                              tip=_(" "))

        self.tc36 = FloatEntry(self.page3,
                              decimals=2, minval=0., maxval=1.e+9, value=0.,
                              unitdict='ENERGY',
                              label=_("Fuel consumption per product(LCV)"),
                              tip=_("Specify energy content of fuels in LCV "))

        #
        # buttons
        #
        self.buttonAddProduct = wx.Button(self.page3,-1,label=_('Add product'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddProduct, self.buttonAddProduct)
        self.buttonAddProduct.SetMinSize((136, 32))
        self.buttonAddProduct.SetFont(fp.getFont())

        self.buttonDeleteProduct = wx.Button(self.page3,-1,label=_('Delete product'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteProduct, self.buttonDeleteProduct)
        self.buttonDeleteProduct.SetMinSize((136, 32))
        self.buttonDeleteProduct.SetFont(fp.getFont())

        self.buttonOK = wx.Button(self, wx.ID_OK, '')
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()

        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, '')
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)

        # recover previous font parameters from the stack
        fp.popFont()


    def __do_layout(self):
        flagText = wx.ALIGN_CENTER_VERTICAL|wx.TOP

        # global sizer for panel. Contains notebook w/three tabs + buttons Cancel and Ok
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)
        # sizer for left tab
        # tab 0, general information
        sizerPage0 = wx.StaticBoxSizer(self.frame_general_information, wx.VERTICAL)
        sizerPage0.Add(self.tc1, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc2, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc3, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc4, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc5, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc6, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc7, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc8, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc9, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc10, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc11, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc12, 0, flagText, VSEP_LEFT)
        sizerPage0.Add(self.tc13, 0, flagText, VSEP_LEFT)
        self.page0.SetSizer(sizerPage0)

        # sizer for left middle tab
        # tab 1, general information
        sizerPage1 = wx.StaticBoxSizer(self.frame_statistical_data, wx.VERTICAL)
        sizerPage1.Add(self.tc14, 0, flagText, VSEP_MIDDLE)
        sizerPage1.Add(self.tc15, 0, flagText, VSEP_MIDDLE)
        sizerPage1.Add(self.tc16, 0, flagText, VSEP_MIDDLE)
        sizerPage1.Add(self.tc17, 0, flagText, VSEP_MIDDLE)
        sizerPage1.Add(self.tc18, 0, flagText, VSEP_MIDDLE)
        sizerPage1.Add(self.tc19, 0, flagText, VSEP_MIDDLE)
        sizerPage1.Add(self.tc20, 0, flagText, VSEP_MIDDLE)
        sizerPage1.Add(self.tc21, 0, flagText, VSEP_MIDDLE)
        sizerPage1.Add(self.tc22, 0, flagText, VSEP_MIDDLE)
        sizerPage1.Add(self.tc23, 0, flagText, VSEP_MIDDLE)
        self.page1.SetSizer(sizerPage1)
        
        # sizer for right middle tab
        # tab 2, period of operation
        sizerPage2 = wx.StaticBoxSizer(self.frame_period_operation, wx.VERTICAL)
        sizerPage2.Add(self.tc24, 0, flagText, VSEP_MIDDLE)
        sizerPage2.Add(self.tc25, 0, flagText, VSEP_MIDDLE)
        sizerPage2.Add(self.tc26, 0, flagText, VSEP_MIDDLE)
        sizerPage2.Add(self.st27, 0, wx.TOP|wx.BOTTOM, 12)
        sizerPage2.Add(self.tc27_10, 0, flagText, VSEP_MIDDLE)
        sizerPage2.Add(self.tc27_11, 0, flagText, VSEP_MIDDLE)
        sizerPage2.Add(self.tc27_20, 0, flagText, VSEP_MIDDLE)
        sizerPage2.Add(self.tc27_21, 0, flagText, VSEP_MIDDLE)
        sizerPage2.Add(self.tc27_30, 0, flagText, VSEP_MIDDLE)
        sizerPage2.Add(self.tc27_31, 0, flagText, VSEP_MIDDLE)
        self.page2.SetSizer(sizerPage2)

        # sizer for right tab
        # tab 3, products
        sizerPage3 = wx.BoxSizer(wx.HORIZONTAL)
        sizerP3Left = wx.StaticBoxSizer(self.frame_product_list, wx.VERTICAL)
        sizerP3Left.Add(self.listBoxProducts,1,wx.EXPAND,0)
        sizerP3Left.Add(self.buttonAddProduct, 0, wx.ALIGN_RIGHT, 0)
        sizerP3Left.Add(self.buttonDeleteProduct, 0, wx.ALIGN_RIGHT, 0)
        sizerPage3.Add(sizerP3Left,1,wx.EXPAND|wx.TOP,10)

        sizerP3Right = wx.BoxSizer(wx.VERTICAL)
        sizerP3RightUp = wx.StaticBoxSizer(self.frame_information_products, wx.VERTICAL)
        sizerP3RightUp.Add(self.tc30, 0, flagText, VSEP_RIGHT)
        sizerP3RightUp.Add(self.tc31, 0, flagText, VSEP_RIGHT)
        sizerP3RightUp.Add(self.tc32, 0, flagText, VSEP_RIGHT)
        sizerP3RightUp.Add(self.tc33, 0, flagText, VSEP_RIGHT)
        sizerP3RightUp.Add(self.tc34, 0, flagText, VSEP_RIGHT)
        sizerP3Right.Add(sizerP3RightUp,2,wx.EXPAND,0)
        
        sizerP3RightDown = wx.StaticBoxSizer(self.frame_energy_consumption, wx.VERTICAL)
        sizerP3RightDown.Add(self.tc35, 0, flagText, VSEP_RIGHT)
        sizerP3RightDown.Add(self.tc36, 0, flagText, VSEP_RIGHT)
        sizerP3Right.Add(sizerP3RightDown,1,wx.EXPAND,0)
        
        sizerPage3.Add(sizerP3Right,2,wx.EXPAND|wx.TOP,10)
        self.page3.SetSizer(sizerPage3)
        
        sizerGlobal.Add(self.notebook, 1, wx.EXPAND, 0)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)
        sizerGlobal.Add(sizerOKCancel, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizerGlobal)
        self.Layout()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------      
    def OnListBoxProductsListboxClick(self, event):
        self.productName = str(self.listBoxProducts.GetStringSelection())
        p = Status.DB.qproduct.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].Product[str(self.listBoxProducts.GetStringSelection())][0]
        self.tc30.SetValue(str(p.Product))
        print "PanelQ1 (ListBoxClick): tc31 set to %s"%p.ProductCode
        self.tc31.SetValue(str(p.ProductCode))
        self.tc32.SetValue(str(p.QProdYear))
        self.tc33.SetValue(str(p.ProdUnit))
        self.tc34.SetValue(str(p.TurnoverProd))
        self.tc35.SetValue(str(p.ElProd))
        self.tc36.SetValue(str(p.FuelProd))
        event.Skip()

    def OnSelectBranch(self, event):
        branch = self.tc12.GetValue(text=True).split(":")[1]
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
        if Status.PId <> 0 and self.notebook.GetSelection()<3:
            if check(self.tc1.GetValue()) <> 'NULL' and \
                Status.DB.questionnaire.Name[check(self.tc1.GetValue())][0].Questionnaire_ID == Status.PId:

                branchSplit = self.tc12.GetValue(text=True).split("|")
                if len(branchSplit) > 1:
                    branch = branchSplit[1]
                else:
                    branch = None
                self.branch = branch
                subBranchSplit = self.tc13.GetValue(text=True).split("|")
                if len(subBranchSplit) > 1:
                    subBranch = subBranchSplit[1]
                else:
                    subBranch = None
                    
                tmp = {
                    "Name":check(self.tc1.GetValue()),
                    "City":check(self.tc2.GetValue()),
                    "DescripIndustry":check(self.tc9.GetValue()),
                    "Branch":check(branch),
                    "SubBranch":check(subBranch),
                    "Contact":check(self.tc3.GetValue()),
                    "Role":check(self.tc4.GetValue()),
                    "Address":check(self.tc5.GetValue()),
                    "Phone":check(self.tc6.GetValue()),
                    "Fax":check(self.tc7.GetValue()),
                    "Email":check(self.tc8.GetValue()),
                    "NEmployees":check(self.tc14.GetValue()),
                    "Turnover":check(self.tc15.GetValue()),
                    "ProdCost":check(self.tc16.GetValue()),
                    "BaseYear":check(self.tc17.GetValue()),
                    "Growth":check(self.tc18.GetValue()),
                    "Independent":check(findKey(TRANSYESNO,check(self.tc19.GetValue(text=True)))),
                    "OMThermal":check(self.tc20.GetValue()),
                    "OMElectrical":check(self.tc21.GetValue()),
                    "PercentFuelTotcost":check(self.tc22.GetValue()),
                    "PercentElTotcost":check(self.tc23.GetValue()),
                    "HPerDayInd":check(self.tc24.GetValue()),
                    "NShifts":check(self.tc25.GetValue()),
                    "NDaysInd":check(self.tc26.GetValue()),
                    "NoProdStart_1":check(self.tc27_10.GetValue()),
                    "NoProdStop_1":check(self.tc27_11.GetValue()),
                    "NoProdStart_2":check(self.tc27_20.GetValue()),
                    "NoProdStop_2":check(self.tc27_21.GetValue()),
                    "NoProdStart_3":check(self.tc27_30.GetValue()),
                    "NoProdStop_3":check(self.tc27_31.GetValue())
                    }
                                
                q = Status.DB.questionnaire.Questionnaire_ID[Status.PId][0]
                q.update(tmp)
                    
                Status.SQL.commit()

                Status.prj.setStatus("Q")
                self.display()
                          
            else:
                self.main.showError(_("Name has to be an unique value!"))
            
#..............................................................................
# aqui parte que guarda la información del producto
                
        print "PanelQ1 (OK): selected page ",self.notebook.GetSelection()
        print "condition = ",(self.notebook.GetSelection() == 3)
        if (Status.PId <> 0) and (self.notebook.GetSelection() == 3):

            print "Now saving product entries"
            
            product = self.tc30.GetValue()

            print "PanelQ1 (OK): saving product entries for product %s"%product
            
            if check(product) <> 'NULL' and len(Status.DB.qproduct.Product[product].\
                                                                  Questionnaire_id[Status.PId].\
                                                                  AlternativeProposalNo[Status.ANo]) == 0:
                print "PanelQ1 (OK): saving data for new product"
                tmp = {
                    "Questionnaire_id":Status.PId,
                    "AlternativeProposalNo":Status.ANo,
                    "Product":check(self.tc30.GetValue()),
                    "ProductCode":check(self.tc31.GetValue(text=True)),
                    "QProdYear":check(self.tc32.GetValue()),
                    "ProdUnit":check(self.tc33.GetValue()),
                    "TurnoverProd":check(self.tc34.GetValue()),
                    "ElProd":check(self.tc35.GetValue()),
                    "FuelProd":check(self.tc36.GetValue())
                    }

                print "PanelQ1: product code = %s saved to SQL"%self.tc31.GetValue(text=True)
                Status.DB.qproduct.insert(tmp)               
                Status.SQL.commit()
                self.fillProductList()

            elif check(product) <> 'NULL' and len(Status.DB.qproduct.Product[product].\
                                                                    Questionnaire_id[Status.PId].\
                                                                    AlternativeProposalNo[Status.ANo]) == 1:
                print "PanelQ1 (OK): saving data for existing product"
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
#   Some problem here with the GetValues
#   Doesn't arrive to the following print
#   Doesn't give an error message
#   => EINSTEIN's magic mysteries ... ????
#
                tmp = {
                    "Product":check(self.tc30.GetValue()),
                    "ProductCode":check(self.tc31.GetValue(text=True)),
                    "QProdYear":check(self.tc32.GetValue()),
                    "ProdUnit":check(self.tc33.GetValue()),
                    "TurnoverProd":check(self.tc34.GetValue()),
                    "ElProd":check(self.tc35.GetValue()),
                    "FuelProd":check(self.tc36.GetValue())
                    }
                print "PanelQ1 (OK): temporary dictionary created"
                print "tmp = ",tmp

                print "PanelQ1: product code = %s saved to SQL"%self.tc31.GetValue(text=True)

                q = Status.DB.qproduct.Product[self.tc30.GetValue()].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillProductList()
                self.productName = self.tc30.GetValue()
                          
            else:
                print "PanelQ1 (OK): some error saving product info"
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
        self.clear()
        self.fillPage()
        self.Show()

    def fillChoiceOfNaceCode(self):
        naceDict,naceSubDict = Status.prj.getNACEDict(self.branch)

        self.tc12.entry.Clear()
        self.tc13.entry.Clear()
        naceList = []
        naceSubList = []
        for code in naceDict.keys():
            naceList.append("%s|%s"%(code,naceDict[code]))
        naceList.sort()
        
        for code in naceSubDict.keys():
            naceSubList.append("%s|%s"%(code,naceSubDict[code]))
        naceSubList.sort()

        for entry in naceList:
            self.tc12.entry.Append(entry)
        for entry in naceSubList:
            self.tc13.entry.Append(entry)

        return naceDict,naceSubDict

    def fillPage(self):
        if Status.PId == 0:
            return

        q = Status.DB.questionnaire.Questionnaire_ID[Status.PId][0]

        self.branch = q.Branch
        naceDict,naceSubDict = self.fillChoiceOfNaceCode()
        
        self.tc1.SetValue(str(q.Name))
        self.tc2.SetValue(str(q.City))
        self.tc3.SetValue(str(q.Contact))
        self.tc4.SetValue(str(q.Role))
        self.tc5.SetValue(str(q.Address))
        self.tc6.SetValue(str(q.Phone))
        self.tc7.SetValue(str(q.Fax))
        self.tc8.SetValue(str(q.Email))
        self.tc9.SetValue(str(q.DescripIndustry))

        print "PanelQ1 (fillPage): branch = ",q.Branch
        self.tc10.SetValue(str(q.Branch))
        if str(q.Branch) in naceDict.values():
            string = "%s|%s"%(findKey(naceDict,str(q.Branch)),q.Branch)
            self.tc12.SetValue(string)
            print "tc12 set to value %s"%string
        else:
            print "branch %s not in naceDict"%q.Branch
            print naceDict.values()
            
        print "PanelQ1 (fillPage): sub-branch = ",q.SubBranch
        self.tc11.SetValue(str(q.SubBranch))
        if str(q.SubBranch) in naceSubDict.values():
            string = "%s|%s"%(findKey(naceSubDict,str(q.SubBranch)),q.SubBranch)
            self.tc13.SetValue(string)
            print "tc13 set to value %s"%string
        else:
            print "subbranch %s not in naceDict"%q.SubBranch
            print naceSubDict.values()
            
        self.tc14.SetValue(str(q.NEmployees))
        self.tc15.SetValue(str(q.Turnover))
        self.tc16.SetValue(str(q.ProdCost))
        self.tc17.SetValue(str(q.BaseYear))
        self.tc18.SetValue(str(q.Growth))
        if q.Independent in TRANSYESNO.keys(): self.tc19.SetValue(TRANSYESNO[str(q.Independent)])
        self.tc20.SetValue(str(q.OMThermal))
        self.tc21.SetValue(str(q.OMElectrical))
        self.tc22.SetValue(str(q.PercentFuelTotcost))
        self.tc23.SetValue(str(q.PercentElTotcost))
        self.tc24.SetValue(str(q.HPerDayInd))
        self.tc25.SetValue(str(q.NShifts))
        self.tc26.SetValue(str(q.NDaysInd))
#XXXXXXX CHECK XXXXXXXXX: SetValue of date entry gave problems ...
        self.tc27_10.SetValue(str(q.NoProdStart_1))
        self.tc27_11.SetValue(str(q.NoProdStop_1))
        self.tc27_20.SetValue(str(q.NoProdStart_2))
        self.tc27_21.SetValue(str(q.NoProdStop_2))
        self.tc27_30.SetValue(str(q.NoProdStart_3))
        self.tc27_31.SetValue(str(q.NoProdStop_3))
        self.fillProductList()



    def fillProductList(self):
        self.listBoxProducts.Clear()
        if len(Status.DB.qproduct.Questionnaire_id[Status.PId]) > 0:
            for n in Status.DB.qproduct.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]:
                self.listBoxProducts.Append(n.Product)

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
        self.tc11.SetValue('')
        self.tc12.SetValue('')
        self.tc13.SetValue('')
        self.tc14.SetValue('')
        self.tc15.SetValue('')
        self.tc16.SetValue('')
        self.tc17.SetValue('')
        self.tc18.SetValue('')
#        self.tc19.SetValue('')
        self.tc20.SetValue('')
        self.tc21.SetValue('')
        self.tc22.SetValue('')#SD
        self.tc23.SetValue('')#SD
        self.tc24.SetValue('')
        self.tc25.SetValue('')
        self.tc26.SetValue('')

#XXXXXXX CHECK XXXXXXXXX: SetValue of date entry gave problems ...
        self.tc27_10.SetValue('')
        self.tc27_11.SetValue('')
        self.tc27_20.SetValue('')
        self.tc27_21.SetValue('')
        self.tc27_30.SetValue('')
        self.tc27_31.SetValue('')
                           
        self.tc30.SetValue('')
##        self.tc31.SetValue('')
        self.tc32.SetValue('')
        self.tc33.SetValue('')
        self.tc34.SetValue('')
        self.tc35.SetValue('')
        self.tc36.SetValue('')

    def clearProduct(self):
        self.tc30.SetValue('')
#        self.tc31.SetValue('')
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

