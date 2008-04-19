# v0.02
#   Revised by:     Hans Schweiger      19/04/2008
#
#   Changes:
#   19/04/2008: HS  activeQid substituted by Status.PId; only positive values of PId allowed
#                   PId = -1 or PId = None means "no project open"


import wx
import pSQL
import HelperClass
from status import Status


class PanelQ1(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Panel.__init__(self, id=-1, name='PanelQ1', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

        self.stInfo3 = wx.StaticText(id=-1,
				     label=self.PList["X020"][1],
				     name='stInfo3',
				     parent=self,
				     pos=wx.Point(248, 384),
				     style=0)
        self.stInfo3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo1 = wx.StaticText(id=-1,
				     label=self.PList["X021"][1],
				     name='stInfo1',
				     parent=self,
				     pos=wx.Point(16, 24),
				     style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS,wx.NORMAL,wx.BOLD, False, 'Tahoma'))

        self.stInfo2 = wx.StaticText(id=-1,
				     label=self.PList["X022"][1],
				     name='stInfo2',
				     parent=self,
				     pos=wx.Point(248,24),
				     style=0)
        self.stInfo2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        
        self.st1 = wx.StaticText(id=-1,
				 label=self.PList["0101"][1],
				 name='st1',
				 parent=self,
				 pos=wx.Point(16,48),
				 style=0)

        self.tc1 = wx.TextCtrl(id=-1,
			       name='tc1',
			       parent=self,
			       pos=wx.Point(16, 64),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st2 = wx.StaticText(id=-1,
				 label=self.PList["0102"][1],
				 name='st2',
				 parent=self,
				 pos=wx.Point(16,88),
				 style=0)

        self.tc2 = wx.TextCtrl(id=-1,
			       name='tc2',
			       parent=self,
			       pos=wx.Point(16,104),
			       size=wx.Size(200,21),
			       style=0,
			       value='')

        self.st3 = wx.StaticText(id=-1,
				 label=self.PList["0108"][1],
				 name='st3',
				 parent=self,
				 pos=wx.Point(16,128),
				 style=0)

        self.tc3 = wx.TextCtrl(id=-1,
			       name='tc3',
			       parent=self,
			       pos=wx.Point(16,144),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st4 = wx.StaticText(id=-1,
				 label=self.PList["0109"][1],
				 name='st4',
				 parent=self,
				 pos=wx.Point(16, 168),
				 style=0)

        self.tc4 = wx.TextCtrl(id=-1,
			       name='tc4',
			       parent=self,
			       pos=wx.Point(16,184),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st5 = wx.StaticText(id=-1,
				 label=self.PList["0110"][1],
				 name='st5',
				 parent=self,
				 pos=wx.Point(16, 208),
				 style=0)

        self.tc5 = wx.TextCtrl(id=-1,
			       name='tc5',
			       parent=self,
			       pos=wx.Point(16, 224),
			       size=wx.Size(200, 56),
			       style=wx.TE_MULTILINE,
			       value='')

        self.st6 = wx.StaticText(id=-1,
				 label=self.PList["0111"][1],
				 name='st6',
				 parent=self,
				 pos=wx.Point(16, 286),
				 style=0)

        self.tc6 = wx.TextCtrl(id=-1,
			       name='tc6',
			       parent=self,
			       pos=wx.Point(16, 304),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st7 = wx.StaticText(id=-1,
				 label=self.PList["0112"][1],
				 name='st7',
				 parent=self,
				 pos=wx.Point(16, 328),
				 style=0)

        self.tc7 = wx.TextCtrl(id=-1,
			       name='tc7',
			       parent=self,
			       pos=wx.Point(16, 344),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st8 = wx.StaticText(id=-1,
				 label=self.PList["0113"][1],
				 name='st8',
				 parent=self,
				 pos=wx.Point(16, 368),
				 style=0)

        self.tc8 = wx.TextCtrl(id=-1,
			       name='tc8',
			       parent=self,
			       pos=wx.Point(16, 384),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st9 = wx.StaticText(id=-1,
				 label=self.PList["0103"][1],
				 name='st9',
				 parent=self,
				 pos=wx.Point(16, 408),
				 style=0)

        self.tc9 = wx.TextCtrl(id=-1,
			       name='tc9',
			       parent=self,
			       pos=wx.Point(16, 424),
			       size=wx.Size(200,56),
			       style=wx.TE_MULTILINE,
			       value='')

        self.st10 = wx.StaticText(id=-1,
				  label=self.PList["0104"][1],
				  name='st10',
				  parent=self,
				  pos=wx.Point(16, 488),
				  style=0)

        self.tc10 = wx.TextCtrl(id=-1,
				name='tc10',
				parent=self,
				pos=wx.Point(16, 504),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st11 = wx.StaticText(id=-1,
				  label=self.PList["0106"][1],
				  name='st11',
				  parent=self,
				  pos=wx.Point(16, 528),
				  style=0)

        self.st14 = wx.StaticText(id=-1,
				  label=self.PList["0201"][1],
				  name='st14',
				  parent=self,
				  pos=wx.Point(248, 48),
				  style=0)

        self.tc14 = wx.TextCtrl(id=-1,
				name='tc14',
				parent=self,
				pos=wx.Point(248, 64),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st15 = wx.StaticText(id=-1,
				  label=self.PList["0202"][1] + ' ' + self.PList["0202"][2],
				  name='st15',
				  parent=self,
				  pos=wx.Point(248, 88),
				  style=0)

        self.tc15 = wx.TextCtrl(id=-1,
				name='tc15',
				parent=self,
				pos=wx.Point(248, 104),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st16 = wx.StaticText(id=-1,
				  label=self.PList["0203"][1] + ' ' + self.PList["0203"][2],
				  name='st16',
				  parent=self,
				  pos=wx.Point(248, 128),
				  style=0)

        self.tc16 = wx.TextCtrl(id=-1,
				name='tc16',
				parent=self,
				pos=wx.Point(248, 144),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st17 = wx.StaticText(id=-1,
				  label=self.PList["0204"][1],
				  name='st17',
				  parent=self,
				  pos=wx.Point(248, 168),
				  style=0)

        self.tc17 = wx.TextCtrl(id=-1,
				name='tc17',
				parent=self,
				pos=wx.Point(248, 184),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st18 = wx.StaticText(id=-1,
				  label=self.PList["0205"][1] + ' ' + self.PList["0205"][2],
				  name='st18',
				  parent=self,
				  pos=wx.Point(248, 208),
				  style=0)

        self.tc18 = wx.TextCtrl(id=-1,
				name='tc18',
				parent=self,
				pos=wx.Point(248, 224),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st19 = wx.StaticText(id=-1,
				  label=self.PList["0206"][1] + ' ' + self.PList["0206"][2],
				  name='st19',
				  parent=self,
				  pos=wx.Point(248, 248),
				  style=0)

        self.tc19 = wx.TextCtrl(id=-1,
				name='tc19',
				parent=self,
				pos=wx.Point(248, 264),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st20 = wx.StaticText(id=-1,
				  label=self.PList["0207"][1] + ' ' + self.PList["0207"][2],
				  name='st20',
				  parent=self,
				  pos=wx.Point(248, 288),
				  style=0)

        self.tc20 = wx.TextCtrl(id=-1,
				name='tc20',
				parent=self,
				pos=wx.Point(248, 304),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st21 = wx.StaticText(id=-1,
				  label=self.PList["0208"][1] + ' ' + self.PList["0208"][2],
				  name='st21',
				  parent=self,
				  pos=wx.Point(248, 328),
				  style=0)

        self.tc21 = wx.TextCtrl(id=-1,
				name='tc21',
				parent=self,
				pos=wx.Point(248, 344),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st22 = wx.StaticText(id=-1,
				  label=self.PList["0210"][1] + ' ' + self.PList["0210"][2],
				  name='st22',
				  parent=self,
				  pos=wx.Point(248, 408),
				  style=0)

        self.tc22 = wx.TextCtrl(id=-1,
				name='tc22',
				parent=self,
				pos=wx.Point(248, 424),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st23 = wx.StaticText(id=-1,
				  label=self.PList["0211"][1],
				  name='st23',
				  parent=self,
				  pos=wx.Point(248, 448),
				  style=0)

        self.tc23 = wx.TextCtrl(id=-1,
				name='tc23',
				parent=self,
				pos=wx.Point(248, 464),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st24 = wx.StaticText(id=-1,
				  label=self.PList["0212"][1] + ' ' + self.PList["0212"][2],
				  name='st24',
				  parent=self,
				  pos=wx.Point(248, 488),
				  style=0)

        self.tc24 = wx.TextCtrl(id=-1,
				name='tc24',
				parent=self,
				pos=wx.Point(248, 504),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st25_1 = wx.StaticText(id=-1,
				    label=self.PList["0213"][1],
				    name='st25',
				    parent=self,
				    pos=wx.Point(248, 528),
				    style=0)

        self.tc25_1 = wx.TextCtrl(id=-1,
				  name='tc25_1',
				  parent=self,
				  pos=wx.Point(248, 544),
				  size=wx.Size(96, 21),
				  style=0,
				  value='')

        self.tc25_2 = wx.TextCtrl(id=-1,
				  name='tc25_2',
				  parent=self,
				  pos=wx.Point(352, 544),
				  size=wx.Size(96, 21),
				  style=0,
				  value='')

        self.choiceOfNaceCode = wx.Choice(id=-1,
					  choices=[],
					  name='choiceOfNaceCode',
					  parent=self,
					  pos=wx.Point(16,544),
					  size=wx.Size(200, 21),
					  style=0)

        self.buttonStoreData = wx.Button(id=-1,
					 label=self.PList["X019"][1],
					 name='buttonStoreData',
					 parent=self,
					 pos=wx.Point(592, 552),
					 size=wx.Size(192, 32),
					 style=0)
	self.Bind(wx.EVT_BUTTON, self.OnButtonStoreData, self.buttonStoreData)
	
        self.listBoxProducts = wx.ListBox(id=-1,
					  choices=[],
					  name='listBoxProducts',
					  parent=self,
					  pos=wx.Point(496,416),
					  size=wx.Size(200, 96),
					  style=0)
	self.Bind(wx.EVT_LISTBOX, self.OnListBoxProductsListboxClick, self.listBoxProducts)

        self.stInfo6 = wx.StaticText(id=-1,
				     label=self.PList["X023"][1],
				     name='stInfo6',
				     parent=self,
				     pos=wx.Point(496, 400),
				     style=0)
        self.stInfo6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.st27 = wx.StaticText(id=-1,
				  label=self.PList["0217"][1],
				  name='st27',
				  parent=self,
				  pos=wx.Point(496, 88),
				  style=0)

        self.tc27 = wx.TextCtrl(id=-1,
				name='tc27',
				parent=self,
				pos=wx.Point(496, 104),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st28 = wx.StaticText(id=-1,
				  label=self.PList["0218"][1] + ' ' + self.PList["0218"][2],
				  name='st28',
				  parent=self,
				  pos=wx.Point(496, 128),
				  style=0)

        self.tc28 = wx.TextCtrl(id=-1,
				name='tc28',
				parent=self,
				pos=wx.Point(496, 144),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st29 = wx.StaticText(id=-1,
				  label=self.PList["0219"][1],
				  name='st29',
				  parent=self,
				  pos=wx.Point(496, 168),
				  style=0)

        self.tc29 = wx.TextCtrl(id=-1,
				name='tc29',
				parent=self,
				pos=wx.Point(496, 184),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st32 = wx.StaticText(id=-1,
				  label=self.PList["0443"][1],
				  name='st32',
				  parent=self,
				  pos=wx.Point(496, 320),
				  style=0)

        self.tc31 = wx.TextCtrl(id=-1,
				name='tc31',
				parent=self,
				pos=wx.Point(496, 296),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st26 = wx.StaticText(id=-1,
				  label=self.PList["0216"][1],
				  name='st26',
				  parent=self,
				  pos=wx.Point(496, 48),
				  style=0)

        self.tc26 = wx.TextCtrl(id=-1,
				name='tc26',
				parent=self,
				pos=wx.Point(496, 64),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.stInfo4 = wx.StaticText(id=-1,
				     label=self.PList["X024"][1],
				     name='stInfo4',
				     parent=self,
				     pos=wx.Point(496, 24),
				     style=0)
        self.stInfo4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.buttonAddProduct = wx.Button(id=-1,
					  label=self.PList["X025"][1],
					  name='buttonAddProduct',
					  parent=self,
					  pos=wx.Point(608, 368),
					  size=wx.Size(192, 32),
					  style=0)
	self.Bind(wx.EVT_BUTTON, self.OnButtonAddProduct, self.buttonAddProduct)


        self.st31 = wx.StaticText(id=-1,
				  label=self.PList["0444"][1],
				  name='st31',
				  parent=self,
				  pos=wx.Point(496, 280),
				  style=0)

        self.tc32 = wx.TextCtrl(id=-1,
				name='tc32',
				parent=self,
				pos=wx.Point(496, 336),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st30 = wx.StaticText(id=-1,
				  label=self.PList["0220"][1] + ' ' + self.PList["0220"][2],
				  name='st30',
				  parent=self,
				  pos=wx.Point(496, 208),
				  style=0)

        self.tc30 = wx.TextCtrl(id=-1,
				name='tc30',
				parent=self,
				pos=wx.Point(496, 224),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.stInfo5 = wx.StaticText(id=-1,
				     label=self.PList["X026"][1],
				     name='stInfo5',
				     parent=self,
				     pos=wx.Point(496, 256),
				     style=0)
        self.stInfo5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.buttonDeleteProduct = wx.Button(id=-1,
					     label=self.PList["X027"][1],
					     name='buttonDeleteProduct',
					     parent=self,
					     pos=wx.Point(608, 520),
					     size=wx.Size(192, 32),
					     style=0)
	self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteProduct, self.buttonDeleteProduct)


        self.buttonClear = wx.Button(id=-1,
				     label=self.PList["X028"][1],
				     name='buttonClear',
				     parent=self,
				     pos=wx.Point(496, 368),
				     size=wx.Size(192, 32),
				     style=0)
	self.Bind(wx.EVT_BUTTON, self.OnButtonClear, self.buttonClear)


#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		

    def OnButtonStoreData(self, event):
        if Status.PId == 0:
            if self.check(self.tc1.GetValue()) <> 'NULL' and \
		    len(Status.DB.questionnaire.Name[self.check(self.tc1.GetValue())]) == 0:
                newID = Status.DB.questionnaire.insert({"Name":self.check(self.tc1.GetValue())})
                print "PANELQ1: HERE SOMETHING SHOULD BE CHANGED. CREATION OF NEW PROJECT ONLY IN Q0 ???!!!"
                Status.SQL.commit()
                
                tmp = {
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
                    tmp["DBNaceCode_id"] = Status.DB.dbnacecode.CodeNACE[\
			str(self.choiceOfNaceCode.GetStringSelection())][0].DBNaceCode_ID
                
                q = Status.DB.questionnaire.Questionnaire_ID[Status.PId][0]
                q.update(tmp)
                Status.SQL.commit()
                          
            else:
                self.showError("Name have to be an uniqe value!")
                
        elif Status.PId > 0:       #project already existing. positive PId required !!!
            
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
                          
            else:
                self.showError("Name have to be an uniqe value!")
            


    def OnButtonAddProduct(self, event):
        if Status.PId > 0:
            if self.check(self.tc26.GetValue()) <> 'NULL' and len(Status.DB.qproduct.Product[self.tc26.GetValue()].Questionnaire_id[Status.PId]) == 0:
                tmp = {
                    "Questionnaire_id":Status.PId,
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

            elif self.check(self.tc26.GetValue()) <> 'NULL' and len(Status.DB.qproduct.Product[self.tc26.GetValue()].Questionnaire_id[Status.PId]) == 1:
                tmp = {
                    "Product":self.check(self.tc26.GetValue()),
                    "ProductCode":self.check(self.tc27.GetValue()),
                    "QProdYear":self.check(self.tc28.GetValue()),
                    "ProdUnit":self.check(self.tc29.GetValue()),
                    "TurnoverProd":self.check(self.tc30.GetValue()),
                    "ElProd":self.check(self.tc32.GetValue()),
                    "FuelProd":self.check(self.tc31.GetValue())
                    }
                q = Status.DB.qproduct.Product[\
		    self.tc26.GetValue()].Questionnaire_id[Status.PId][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillProductList()
                          
            else:
                self.showError("Product have to be an uniqe value!")

    def OnListBoxProductsListboxClick(self, event):
        p = Status.DB.qproduct.Questionnaire_id[\
	    status.PId].Product[str(self.listBoxProducts.GetStringSelection())][0]
        self.tc26.SetValue(str(p.Product))
        self.tc27.SetValue(str(p.ProductCode))
        self.tc28.SetValue(str(p.QProdYear))
        self.tc29.SetValue(str(p.ProdUnit))
        self.tc30.SetValue(str(p.TurnoverProd))
        self.tc32.SetValue(str(p.ElProd))
        self.tc31.SetValue(str(p.FuelProd))
        event.Skip()

    def OnButtonDeleteProduct(self, event):
        event.Skip()

    def OnButtonClear(self, event):
        self.clear()
        event.Skip()


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
	    self.choiceOfNaceCode.SetSelection(\
		self.choiceOfNaceCode.FindString(\
		    str(Status.DB.dbnacecode.DBNaceCode_ID[q.DBNaceCode_id][0].CodeNACE)))
            self.fillProductList()



    def fillProductList(self):
        self.listBoxProducts.Clear()
        if len(Status.DB.qproduct.Questionnaire_id[Status.PId]) > 0:
            for n in Status.DB.qproduct.Questionnaire_id[Status.PId]:
                self.listBoxProducts.Append(n.Product)

#XXX This functions should be substituted by the general message-logger functions !!!!
    def showError(self, message):
        dlg = wx.MessageDialog(None, message, 'Error', wx.OK)
        ret = dlg.ShowModal()
        dlg.Destroy()

    def showInfo(self, message):
        dlg = wx.MessageDialog(None, message, 'Info', wx.OK)
        ret = dlg.ShowModal()
        dlg.Destroy()

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

if __name__ == '__main__':
    import pSQL
    import MySQLdb

    class Main(object):
	def __init__(self,qid):
	    Status.PId = qid

    DBName = 'einstein'
    Status.SQL = MySQLdb.connect(host='localhost', user='root', passwd='tom.tom', db=DBName)
    Status.DB =  pSQL.pSQL(Status.SQL, DBName)

    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(800, 600), title="Einstein - panelQ1")
    main = Main(1)
    panel = PanelQ1(frame, main)

    frame.Show(True)
    app.MainLoop()

