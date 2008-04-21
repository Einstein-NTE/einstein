import wx
import pSQL
import HelperClass
from status import Status


class PanelQ3(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Panel.__init__(self, id=-1, name='PanelQ3', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

        self.tc1 = wx.TextCtrl(id=-1,
			       name='tc1',
			       parent=self,
			       pos=wx.Point(16, 352),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st1 = wx.StaticText(id=-1,
				 label=self.PList["0301"][1] + ' ' + self.PList["0301"][2],
				 name='st1',
				 parent=self,
				 pos=wx.Point(16, 336),
				 style=0)

        self.st2 = wx.StaticText(id=-1,
				 label=self.PList["0303"][1] + ' ' + self.PList["0303"][2],
				 name='st2',
				 parent=self,
				 pos=wx.Point(16, 376),
				 style=0)

        self.tc2 = wx.TextCtrl(id=-1,
			       name='tc2',
			       parent=self,
			       pos=wx.Point(16, 392),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')


        self.st3 = wx.StaticText(id=-1,
				 label=self.PList["0302"][1] + ' ' + self.PList["0302"][2],
				 name='st3',
				 parent=self,
				 pos=wx.Point(16, 416),
				 style=0)

        #self.tc3 = wx.TextCtrl(id=-1, name='tc3',
        #      parent=self, pos=wx.Point(16, 432), size=wx.Size(200, 21),
        #      style=0, value='')

        self.choiceOfDBUnitOperation = wx.Choice(choices=[],
						 id=-1,
						 name='choiceOfDBUnitOperation',
						 parent=self,
						 pos=wx.Point(16, 432),
						 size=wx.Size(200, 21),
						 style=0)

        self.st4 = wx.StaticText(id=-1,
				 label=self.PList["0304"][1] + ' ' + self.PList["0304"][2],
				 name='st4',
				 parent=self,
				 pos=wx.Point(16, 456),
				 style=0)

        #self.tc4 = wx.TextCtrl(id=-1, name='tc4',
        #      parent=self, pos=wx.Point(16, 472), size=wx.Size(200, 21),
        #      style=0, value='')

        self.choiceOfPMDBFluid = wx.Choice(choices=[],
					   id=-1,
					   name='choiceOfPMDBFluid',
					   parent=self,
					   pos=wx.Point(16, 472),
					   size=wx.Size(200, 21),
					   style=0)        

        self.st5 = wx.StaticText(id=-1,
				 label=self.PList["0305"][1] + ' ' + self.PList["0305"][2],
				 name='st5',
				 parent=self,
				 pos=wx.Point(16, 496),
				 style=0)

        self.tc5 = wx.TextCtrl(id=-1,
			       name='tc5',
			       parent=self,
			       pos=wx.Point(16, 512),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st6 = wx.StaticText(id=-1,
				 label=self.PList["0306"][1] + ' ' + self.PList["0306"][2],
				 name='st6',
				 parent=self,
				 pos=wx.Point(16, 536),
				 style=0)

        self.tc6 = wx.TextCtrl(id=-1,
			       name='tc6',
			       parent=self,
			       pos=wx.Point(16, 552),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st7 = wx.StaticText(id=-1,
				 label=self.PList["0307"][1] + ' ' + self.PList["0307"][2],
				 name='st7',
				 parent=self,
				 pos=wx.Point(240, 40),
				 style=0)

        self.tc7 = wx.TextCtrl(id=-1,
			       name='tc7',
			       parent=self,
			       pos=wx.Point(240, 56),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st8 = wx.StaticText(id=-1,
				 label=self.PList["0308"][1] + ' ' + self.PList["0308"][2],
				 name='st8',
				 parent=self,
				 pos=wx.Point(240, 80),
				 style=0)

        self.tc8 = wx.TextCtrl(id=-1,
			       name='tc8',
			       parent=self,
			       pos=wx.Point(240, 96),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st9 = wx.StaticText(id=-1,
				 label=self.PList["0309"][1] + ' ' + self.PList["0309"][2],
				 name='st9',
				 parent=self,
				 pos=wx.Point(240, 120),
				 style=0)

        self.tc9 = wx.TextCtrl(id=-1,
			       name='tc9',
			       parent=self,
			       pos=wx.Point(240, 136),
			       size=wx.Size(200, 21),
			       style=0,
			       value='')

        self.st10 = wx.StaticText(id=-1,
				  label=self.PList["0310"][1] + ' ' + self.PList["0310"][2],
				  name='st10',
				  parent=self,
				  pos=wx.Point(240, 160),
				  style=0)

        self.tc10 = wx.TextCtrl(id=-1,
				name='tc10',
				parent=self,
				pos=wx.Point(240, 176),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st11 = wx.StaticText(id=-1,
				  label=self.PList["0312"][1] + ' ' + self.PList["0312"][2],
				  name='st11',
				  parent=self,
				  pos=wx.Point(240, 232),
				  style=0)

        self.tc11 = wx.TextCtrl(id=-1,
				name='tc11',
				parent=self,
				pos=wx.Point(240, 248),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st12 = wx.StaticText(id=-1,
				  label=self.PList["0313"][1] + ' ' + self.PList["0313"][2],
				  name='st12',
				  parent=self,
				  pos=wx.Point(240, 272),
				  style=0)

        self.tc12 = wx.TextCtrl(id=-1,
				name='tc12',
				parent=self,
				pos=wx.Point(240, 288),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st13 = wx.StaticText(id=-1,
				  label=self.PList["0314"][1] + ' ' + self.PList["0314"][2],
				  name='st13',
				  parent=self,
				  pos=wx.Point(240, 312),
				  style=0)

        self.tc13 = wx.TextCtrl(id=-1,
				name='tc13',
				parent=self,
				pos=wx.Point(240, 328),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st14 = wx.StaticText(id=-1,
				  label=self.PList["0315"][1] + ' ' + self.PList["0315"][2],
				  name='st14',
				  parent=self,
				  pos=wx.Point(240, 352),
				  style=0)

        self.tc14 = wx.TextCtrl(id=-1,
				name='tc14',
				parent=self,
				pos=wx.Point(240, 368),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st15 = wx.StaticText(id=-1,
				  label=self.PList["0317"][1] + ' ' + self.PList["0317"][2],
				  name='st15',
				  parent=self,
				  pos=wx.Point(240, 432),
				  style=0)

        self.tc15 = wx.TextCtrl(id=-1,
				name='tc15',
				parent=self,
				pos=wx.Point(240, 448),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st16 = wx.StaticText(id=-1,
				  label=self.PList["0318"][1] + ' ' + self.PList["0318"][2],
				  name='st16',
				  parent=self,
				  pos=wx.Point(240, 472),
				  style=0)

        self.tc16 = wx.TextCtrl(id=-1,
				name='tc16',
				parent=self,
				pos=wx.Point(240, 488),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st17 = wx.StaticText(id=-1,
				  label=self.PList["0319"][1] + ' ' + self.PList["0319"][2],
				  name='st17',
				  parent=self,
				  pos=wx.Point(240, 512),
				  style=0)

        self.tc17 = wx.TextCtrl(id=-1,
				name='tc17',
				parent=self,
				pos=wx.Point(240, 528),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st18 = wx.StaticText(id=-1,
				  label=self.PList["0320"][1] + ' ' + self.PList["0320"][2],
				  name='st18',
				  parent=self,
				  pos=wx.Point(240, 552),
				  style=0)

        self.tc18 = wx.TextCtrl(id=-1,
				name='tc18',
				parent=self,
				pos=wx.Point(240, 568),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st19 = wx.StaticText(id=-1,
				  label=self.PList["0322"][1] + ' ' + self.PList["0322"][2],
				  name='st19',
				  parent=self,
				  pos=wx.Point(488, 40),
				  style=0)
	
        self.tc19 = wx.TextCtrl(id=-1,
				name='tc19',
				parent=self,
				pos=wx.Point(488, 56),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st20 = wx.StaticText(id=-1,
				  label=self.PList["0323"][1] + ' ' + self.PList["0323"][2],
				  name='st20',
				  parent=self,
				  pos=wx.Point(488, 80),
				  style=0)

        self.tc20 = wx.TextCtrl(id=-1,
				name='tc20',
				parent=self,
				pos=wx.Point(488, 96),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st21 = wx.StaticText(id=-1,
				  label=self.PList["0324"][1] + ' ' + self.PList["0324"][2],
				  name='st21',
				  parent=self,
				  pos=wx.Point(488, 120),
				  style=0)

        self.tc21 = wx.TextCtrl(id=-1,
				name='tc21',
				parent=self,
				pos=wx.Point(488, 136),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st22 = wx.StaticText(id=-1,
				  label=self.PList["0327"][1] + ' ' + self.PList["0327"][2],
				  name='st22',
				  parent=self,
				  pos=wx.Point(488, 216),
				  style=0)

        #self.tc22 = wx.TextCtrl(id=-1, name='tc22',
        #      parent=self, pos=wx.Point(488, 232), size=wx.Size(200, 21),
        #      style=0, value='')

        self.choiceOfSMDBFluid = wx.Choice(choices=[],
					   id=-1,
					   name='choiceOfSMDBFluid',
					   parent=self,
					   pos=wx.Point(488, 232),
					   size=wx.Size(200, 21),
					   style=0)

        self.st23 = wx.StaticText(id=-1,
				  label=self.PList["0328"][1] + ' ' + self.PList["0328"][2],
				  name='st23',
				  parent=self,
				  pos=wx.Point(488, 256),
				  style=0)

        self.tc23 = wx.TextCtrl(id=-1,
				name='tc23',
				parent=self,
				pos=wx.Point(488, 272),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st24 = wx.StaticText(id=-1,
				  label=self.PList["0329"][1] + ' ' + self.PList["0329"][2],
				  name='st24',
				  parent=self,
				  pos=wx.Point(488, 296),
				  style=0)

        self.tc24 = wx.TextCtrl(id=-1,
				name='tc24',
				parent=self,
				pos=wx.Point(488, 312),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st25 = wx.StaticText(id=-1,
				  label=self.PList["0330"][1] + ' ' + self.PList["0330"][2],
				  name='st25',
				  parent=self,
				  pos=wx.Point(488, 336),
				  style=0)
	
        self.tc25 = wx.TextCtrl(id=-1,
				name='tc25',
				parent=self,
				pos=wx.Point(488, 352),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.st26 = wx.StaticText(id=-1,
				  label=self.PList["0331"][1] + ' ' + self.PList["0331"][2],
				  name='st26',
				  parent=self,
				  pos=wx.Point(488, 376),
				  style=0)

        self.tc26 = wx.TextCtrl(id=-1,
				name='tc26',
				parent=self,
				pos=wx.Point(488, 392),
				size=wx.Size(200, 21),
				style=0,
				value='')

        self.stInfo2 = wx.StaticText(id=-1,
				     label=self.PList["0300"][1],
				     name='stInfo2',
				     parent=self,
				     pos=wx.Point(16, 312),
				     style=0)
        self.stInfo2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo3 = wx.StaticText(id=-1,
				     label=self.PList["0311"][1],
				     name='stInfo3',
				     parent=self,
				     pos=wx.Point(240, 208),
				     style=0)
        self.stInfo3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo4 = wx.StaticText(id=-1,
				     label=self.PList["0316"][1],
				     name='stInfo4',
				     parent=self,
				     pos=wx.Point(240, 408),
				     style=0)
        self.stInfo4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo5 = wx.StaticText(id=-1,
				     label=self.PList["0321"][1],
				     name='stInfo5',
				     parent=self,
				     pos=wx.Point(488, 16),
				     style=0)
        self.stInfo5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        
        self.stInfo6 = wx.StaticText(id=-1,
				     label=self.PList["0326"][1],
				     name='stInfo6',
				     parent=self,
				     pos=wx.Point(488, 192),
				     style=0)
        self.stInfo6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.buttonAddProcess = wx.Button(id=-1,
					  label=self.PList["X057"][1],
					  name='buttonAddProcess',
					  parent=self,
					  pos=wx.Point(600, 568),
					  size=wx.Size(192, 32),
					  style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddProcess, self.buttonAddProcess)


        self.listBoxProcesses = wx.ListBox(choices=[],
					   id=-1,
					   name='listBoxProcesses',
					   parent=self,
					   pos=wx.Point(16, 40),
					   size=wx.Size(200, 216),
					   style=0)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxProcessesClick, self.listBoxProcesses)

        self.stInfo1 = wx.StaticText(id=-1,
				     label=self.PList["X059"][1],
				     name='stInfo1',
				     parent=self,
				     pos=wx.Point(16, 24),
				     size=wx.Size(64, 13),
				     style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.buttonDeleteProcess = wx.Button(id=-1,
					     label=self.PList["X058"][1],
					     name='buttonDeleteProcess',
					     parent=self,
					     pos=wx.Point(136, 264),
					     size=wx.Size(192, 32),
					     style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteProcess, self.buttonDeleteProcess)


        self.buttonClear = wx.Button(id=-1,
				     label=self.PList["X028"][1],
				     name='buttonClear',
				     parent=self,
				     pos=wx.Point(488, 568),
				     size=wx.Size(192, 32),
				     style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClear, self.buttonClear)


#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		


    def OnButtonAddProcess(self, event):
        if Status.PId == 0:
	    return

	if self.check(self.tc1.GetValue()) != 'NULL' and \
		len(Status.DB.qprocessdata.Process[\
		self.tc1.GetValue()].Questionnaire_id[Status.PId]) == 0:
	    dbuid = Status.DB.dbunitoperation.UnitOperation[\
		str(self.choiceOfDBUnitOperation.GetStringSelection())][0].DBUnitOperation_ID
	    dbpmfid = Status.DB.dbfluid.FluidName[\
		str(self.choiceOfPMDBFluid.GetStringSelection())][0].DBFluid_ID
	    dbsmfid = Status.DB.dbfluid.FluidName[\
		str(self.choiceOfSMDBFluid.GetStringSelection())][0].DBFluid_ID                       
        
	    tmp = {
		"Questionnaire_id":Status.PId,
		"Process":self.check(self.tc1.GetValue()),
		"DBUnitOperation_id":dbuid,
		"ProcType":self.check(self.tc2.GetValue()),	
		"ProcMedDBFluid_id":dbpmfid,
		"PT":self.check(self.tc5.GetValue()), 
		"PTInFlow":self.check(self.tc6.GetValue()), 
		"PTStartUp":self.check(self.tc7.GetValue()), 
		"VInFlowDay":self.check(self.tc8.GetValue()), 
		"VolProcMed":self.check(self.tc9.GetValue()), 
		"UAProc":self.check(self.tc10.GetValue()), 
		"HPerDayProc":self.check(self.tc11.GetValue()), 
		"NBatch":self.check(self.tc12.GetValue()), 
		"HBatch":self.check(self.tc13.GetValue()), 
		"NDaysProc":self.check(self.tc14.GetValue()), 	
		"PTOutFlow":self.check(self.tc15.GetValue()), 
		"PTFinal":self.check(self.tc16.GetValue()), 
		"VOutFlow":self.check(self.tc17.GetValue()), 
		"HeatRecOK":self.check(self.tc18.GetValue()), 
		"HeatRecExist":self.check(self.tc19.GetValue()), 
		"SourceWasteHeat":self.check(self.tc20.GetValue()), 	
		"PTInFlowRec":self.check(self.tc21.GetValue()), 
		"SupplyMedDBFluid_id":dbsmfid,
		"PipeDuctProc":self.check(self.tc23.GetValue()), 
		"TSupply":self.check(self.tc24.GetValue()), 
		"SupplyMedFlow":self.check(self.tc25.GetValue()), 
		"UPHtotQ":self.check(self.tc26.GetValue()) 
		}

	    Status.DB.qprocessdata.insert(tmp)               
	    Status.SQL.commit()
	    self.fillPage()

	elif self.check(self.tc1.GetValue()) <> 'NULL' and \
		len(Status.DB.qprocessdata.Process[\
		self.tc1.GetValue()].Questionnaire_id[Status.PId]) == 1:
	    dbuid = Status.DB.dbunitoperation.UnitOperation[\
		str(self.choiceOfDBUnitOperation.GetStringSelection())][0].DBUnitOperation_ID
	    dbpmfid = Status.DB.dbfluid.FluidName[\
		str(self.choiceOfPMDBFluid.GetStringSelection())][0].DBFluid_ID
	    dbsmfid = Status.DB.dbfluid.FluidName[\
		str(self.choiceOfSMDBFluid.GetStringSelection())][0].DBFluid_ID                       
        
	    tmp = {
		"Process":self.check(self.tc1.GetValue()),
		"DBUnitOperation_id":dbuid,
		"ProcType":self.check(self.tc2.GetValue()),	
		"ProcMedDBFluid_id":dbpmfid,
		"PT":self.check(self.tc5.GetValue()), 
		"PTInFlow":self.check(self.tc6.GetValue()), 
		"PTStartUp":self.check(self.tc7.GetValue()), 
		"VInFlowDay":self.check(self.tc8.GetValue()), 
		"VolProcMed":self.check(self.tc9.GetValue()), 
		"UAProc":self.check(self.tc10.GetValue()), 
		"HPerDayProc":self.check(self.tc11.GetValue()), 
		"NBatch":self.check(self.tc12.GetValue()), 
		"HBatch":self.check(self.tc13.GetValue()), 
		"NDaysProc":self.check(self.tc14.GetValue()), 	
		"PTOutFlow":self.check(self.tc15.GetValue()), 
		"PTFinal":self.check(self.tc16.GetValue()), 
		"VOutFlow":self.check(self.tc17.GetValue()), 
		"HeatRecOK":self.check(self.tc18.GetValue()), 
		"HeatRecExist":self.check(self.tc19.GetValue()), 
		"SourceWasteHeat":self.check(self.tc20.GetValue()), 	
		"PTInFlowRec":self.check(self.tc21.GetValue()), 
		"SupplyMedDBFluid_id":dbsmfid,
		"PipeDuctProc":self.check(self.tc23.GetValue()), 
		"TSupply":self.check(self.tc24.GetValue()), 
		"SupplyMedFlow":self.check(self.tc25.GetValue()), 
		"UPHtotQ":self.check(self.tc26.GetValue()) 
		}
	    q = Status.DB.qprocessdata.Process[self.tc1.GetValue()].Questionnaire_id[Status.PId][0]
	    q.update(tmp)               
	    Status.SQL.commit()
	    self.fillPage()
                          
	else:
	    self.showError("Process have to be an uniqe value!")



    def OnButtonDeleteProcess(self, event):
        event.Skip()

    def OnListBoxProcessesClick(self, event):
        q = Status.DB.qprocessdata.Questionnaire_id[\
	    Status.PId].Process[str(self.listBoxProcesses.GetStringSelection())][0]
        self.tc1.SetValue(str(q.Process))
        self.tc2.SetValue(str(q.ProcType))
        self.tc5.SetValue(str(q.PT))
        self.tc6.SetValue(str(q.PTInFlow))
        self.tc7.SetValue(str(q.PTStartUp))
        self.tc8.SetValue(str(q.VInFlowDay))
        self.tc9.SetValue(str(q.VolProcMed))
        self.tc10.SetValue(str(q.UAProc))
        self.tc11.SetValue(str(q.HPerDayProc))
        self.tc12.SetValue(str(q.NBatch))
        self.tc13.SetValue(str(q.HBatch))
        self.tc14.SetValue(str(q.NDaysProc))		
        self.tc15.SetValue(str(q.PTOutFlow))
        self.tc16.SetValue(str(q.PTFinal))
        self.tc17.SetValue(str(q.VOutFlow))
        self.tc18.SetValue(str(q.HeatRecOK))
        self.tc19.SetValue(str(q.HeatRecExist))
        self.tc20.SetValue(str(q.SourceWasteHeat))	
        self.tc21.SetValue(str(q.PTInFlowRec))
        self.tc23.SetValue(str(q.PipeDuctProc))
        self.tc24.SetValue(str(q.TSupply))
        self.tc25.SetValue(str(q.SupplyMedFlow))
        self.tc26.SetValue(str(q.UPHtotQ))
        if q.DBUnitOperation_id is not None:
            self.choiceOfDBUnitOperation.SetSelection(\
		self.choiceOfDBUnitOperation.FindString(\
		    str(Status.DB.dbunitoperation.DBUnitOperation_ID[q.DBUnitOperation_id][0].UnitOperation)))
        if q.ProcMedDBFluid_id is not None:
            self.choiceOfPMDBFluid.SetSelection(\
		self.choiceOfPMDBFluid.FindString(\
		    str(Status.DB.dbfluid.DBFluid_ID[q.ProcMedDBFluid_id][0].FluidName)))
        if q.SupplyMedDBFluid_id is not None:
            self.choiceOfSMDBFluid.SetSelection(\
		self.choiceOfSMDBFluid.FindString(\
		    str(Status.DB.dbfluid.DBFluid_ID[q.SupplyMedDBFluid_id][0].FluidName)))
        event.Skip()

    def OnButtonClear(self, event):
        self.clear()
        event.Skip()



#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		


    def fillChoiceOfDBUnitOperation(self):
        self.choiceOfDBUnitOperation.Clear()
        self.choiceOfDBUnitOperation.Append ("None")
        for n in Status.DB.dbunitoperation.UnitOperation["%"]:
            self.choiceOfDBUnitOperation.Append (n.UnitOperation)
        self.choiceOfDBUnitOperation.SetSelection(0)

    def fillChoiceOfPMDBFluid(self):
        self.choiceOfPMDBFluid.Clear()
        self.choiceOfPMDBFluid.Append ("None")
        for n in Status.DB.dbfluid.FluidName["%"]:
            self.choiceOfPMDBFluid.Append (n.FluidName)
        self.choiceOfPMDBFluid.SetSelection(0)

    def fillChoiceOfSMDBFluid(self):
        self.choiceOfSMDBFluid.Clear()
        self.choiceOfSMDBFluid.Append ("None")
        for n in Status.DB.dbfluid.FluidName["%"]:
            self.choiceOfSMDBFluid.Append (n.FluidName)
        self.choiceOfSMDBFluid.SetSelection(0)

    def fillPage(self):
        self.listBoxProcesses.Clear()
        if len(Status.DB.qprocessdata.Questionnaire_id[Status.PId]) > 0:
            for n in Status.DB.qprocessdata.Questionnaire_id[Status.PId]:
                self.listBoxProcesses.Append (str(n.Process))


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
        self.tc19.SetValue('')
        self.tc20.SetValue('')
        self.tc21.SetValue('')
        self.tc23.SetValue('')
        self.tc24.SetValue('')
        self.tc25.SetValue('')
        self.tc26.SetValue('')
        


if __name__ == '__main__':
    import pSQL
    import MySQLdb
    class Main(object):
	def __init__(self,qid):
	    self.activeQid = qid

    DBName = 'einstein'
    Status.SQL = MySQLdb.connect(host='localhost', user='root', passwd='tom.tom', db=DBName)
    Status.DB =  pSQL.pSQL(Status.SQL, DBName)

    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(800, 600), title="Einstein - panelQ3")
    main = Main(1)
    panel = PanelQ3(frame, main)

    frame.Show(True)
    app.MainLoop()
        
