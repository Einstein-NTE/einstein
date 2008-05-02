#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	PanelQ5: Pipes and ducts
#
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Heiko Henning February2008
#       Revised by:         Tom Sobota March/April 2008
#                           Hans Schweiger 02/05/2008
#
#       Changes to previous version:
#       02/05/08:       AlternativeProposalNo added in queries for table qdistributionhc
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


class PanelQ5(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)

        self.pipeID = None

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Panel.__init__(self,
			  id=-1,
			  name='PanelQ5',
			  parent=parent,
			  pos=wx.Point(0, 0),
			  size=wx.Size(800, 600),
			  style=0)

        self.listBoxDistributionList = wx.ListBox(choices=[],
						       id=-1,
						       name='listBoxDistributionList',
						       parent=self,
						       pos=wx.Point(24, 40),
						       size=wx.Size(200, 216),
						       style=0)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxDistributionListListboxClick, self.listBoxDistributionList)


        self.stInfo1 = wx.StaticText(id=-1,
					  label=self.PList["X063"][1],
					  name='stInfo1',
					  parent=self,
					  pos=wx.Point(24, 24),
					  style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo2 = wx.StaticText(id=-1,
					  label=self.PList["0600"][1],
					  name='stInfo2',
					  parent=self,
					  pos=wx.Point(272, 24),
					  style=0)
        self.stInfo2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo3 = wx.StaticText(id=-1,
					  label=self.PList["0615"][1],
					  name='stInfo3',
					  parent=self,
					  pos=wx.Point(512, 224),
					  style=0)
        self.stInfo3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))


        self.buttonClear = wx.Button(id=-1,
					  label=self.PList["X028"][1],
					  name='buttonClear',
					  parent=self,
					  pos=wx.Point(272, 464),
					  size=wx.Size(192, 32),
					  style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClear, self.buttonClear)

        self.buttonDeleteDistribution = wx.Button(id=-1,
						       label=self.PList["X064"][1],
						       name='buttonDeleteDistribution',
						       parent=self,
						       pos=wx.Point(136, 264),
						       size=wx.Size(192, 32),
						       style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteDistribution, self.buttonDeleteDistribution)

        self.buttonAddDistribution = wx.Button(id=-1,
						    label=self.PList["X065"][1],
						    name='buttonAddDistribution',
						    parent=self,
						    pos=wx.Point(584, 464),
						    size=wx.Size(192, 32),
						    style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonAddDistribution, self.buttonAddDistribution)

	
        self.st1 = wx.StaticText(id=-1,
				      label=self.PList["0601"][1] + ' ' + self.PList["0601"][2],
				      name='st1',
				      parent=self,
				      pos=wx.Point(272, 48),
				      style=0)        

        self.tc1 = wx.TextCtrl(id=-1,
				    name='tc1',
				    parent=self,
				    pos=wx.Point(272, 64),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')        

	
        self.st2 = wx.StaticText(id=-1,
				      label=self.PList["0602"][1] + ' ' + self.PList["0602"][2],
				      name='st2',
				      parent=self,
				      pos=wx.Point(272, 88),
				      style=0)

        #self.tc2 = wx.TextCtrl(id=-1, name='tc2',
        #      parent=self, pos=wx.Point(272, 104), size=wx.Size(200, 21),
        #      style=0, value='')
        self.choiceOfEquipment = wx.Choice(choices=[],
						id=-1,
						name='choiceOfEquipment',
						parent=self,
						pos=wx.Point(272, 104),
						size=wx.Size(200, 21),
						style=0)

        self.st3 = wx.StaticText(id=-1,
				      label=self.PList["0603"][1] + ' ' + self.PList["0603"][2],
				      name='st3',
				      parent=self,
				      pos=wx.Point(272, 128),
				      style=0)

	self.tc3 = wx.TextCtrl(id=-1,
				    name='tc3',
				    parent=self,
				    pos=wx.Point(272, 144),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st4 = wx.StaticText(id=-1,
				      label=self.PList["0604"][1] + ' ' + self.PList["0604"][2],
				      name='st4',
				      parent=self,
				      pos=wx.Point(272, 168),
				      style=0)

        self.tc4 = wx.TextCtrl(id=-1,
				    name='tc4',
				    parent=self,
				    pos=wx.Point(272, 184),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st5 = wx.StaticText(id=-1,
				      label=self.PList["0605"][1] + ' ' + self.PList["0605"][2],
				      name='st5',
				      parent=self,
				      pos=wx.Point(272, 208),
				      style=0)

        self.tc5 = wx.TextCtrl(id=-1,
				    name='tc5',
				    parent=self,
				    pos=wx.Point(272, 224),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')
        

        self.st6 = wx.StaticText(id=-1,
				      label=self.PList["0606"][1] + ' ' + self.PList["0606"][2],
				      name='st6',
				      parent=self,
				      pos=wx.Point(272, 248),
				      style=0)

        self.tc6 = wx.TextCtrl(id=-1,
				    name='tc6',
				    parent=self,
				    pos=wx.Point(272, 264),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')
        

        self.st7 = wx.StaticText(id=-1,
				      label=self.PList["0607"][1] + ' ' + self.PList["0607"][2],
				      name='st7',
				      parent=self,
				      pos=wx.Point(272, 288),
				      style=0)

        self.tc7 = wx.TextCtrl(id=-1,
				    name='tc7',
				    parent=self,
				    pos=wx.Point(272, 304),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st8 = wx.StaticText(id=-1,
				      label=self.PList["0608"][1] + ' ' + self.PList["0608"][2],
				      name='st8',
				      parent=self,
				      pos=wx.Point(272, 328),
				      style=0)

        self.tc8 = wx.TextCtrl(id=-1,
				    name='tc8',
				    parent=self,
				    pos=wx.Point(272, 344),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st9 = wx.StaticText(id=-1,
				      label=self.PList["0609"][1] + ' ' + self.PList["0609"][2],
				      name='st9',
				      parent=self,
				      pos=wx.Point(272, 368),
				      style=0)

        self.tc9 = wx.TextCtrl(id=-1,
				    name='tc9',
				    parent=self,
				    pos=wx.Point(272, 384),
				    size=wx.Size(200, 21),
				    style=0,
				    value='')


        self.st10 = wx.StaticText(id=-1,
				       label=self.PList["0610"][1] + ' ' + self.PList["0610"][2],
				       name='st10',
				       parent=self,
				       pos=wx.Point(272, 408),
				       style=0)

        self.tc10 = wx.TextCtrl(id=-1,
				     name='tc10',
				     parent=self,
				     pos=wx.Point(272, 424),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st11 = wx.StaticText(id=-1,
				       label=self.PList["0611"][1] + ' ' + self.PList["0611"][2],
				       name='st11',
				       parent=self,
				       pos=wx.Point(512, 48),
				       style=0)

        self.tc11 = wx.TextCtrl(id=-1,
				     name='tc11',
				     parent=self,
				     pos=wx.Point(512, 64),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')        


        self.st12 = wx.StaticText(id=-1,
				       label=self.PList["0612"][1] + ' ' + self.PList["0612"][2],
				       name='st12',
				       parent=self,
				       pos=wx.Point(512, 88),
				       style=0)
        
        self.tc12 = wx.TextCtrl(id=-1,
				     name='tc12',
				     parent=self,
				     pos=wx.Point(512, 104),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st13 = wx.StaticText(id=-1,
				       label=self.PList["0613"][1] + ' ' + self.PList["0613"][2],
				       name='st13',
				       parent=self,
				       pos=wx.Point(512, 128),
				       style=0)

        self.tc13 = wx.TextCtrl(id=-1,
				     name='tc13',
				     parent=self,
				     pos=wx.Point(512, 144),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')

        
        self.st14 = wx.StaticText(id=-1,
				       label=self.PList["0614"][1] + ' ' + self.PList["0614"][2],
				       name='st14',
				       parent=self,
				       pos=wx.Point(512, 168),
				       style=0)

        self.tc14 = wx.TextCtrl(id=-1,
				     name='tc14',
				     parent=self,
				     pos=wx.Point(512, 184),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st15 = wx.StaticText(id=-1,
				       label=self.PList["0616"][1] + ' ' + self.PList["0616"][2],
				       name='st15',
				       parent=self,
				       pos=wx.Point(512, 248),
				       style=0)

        self.tc15 = wx.TextCtrl(id=-1,
				     name='tc15',
				     parent=self,
				     pos=wx.Point(512, 264),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st16 = wx.StaticText(id=-1,
				       label=self.PList["0617"][1] + ' ' + self.PList["0617"][2],
				       name='st16',
				       parent=self,
				       pos=wx.Point(512, 288),
				       style=0)

        self.tc16 = wx.TextCtrl(id=-1,
				     name='tc16',
				     parent=self,
				     pos=wx.Point(512, 304),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st17 = wx.StaticText(id=-1,
				       label=self.PList["0618"][1] + ' ' + self.PList["0618"][2],
				       name='st17',
				       parent=self,
				       pos=wx.Point(512, 328),
				       style=0)

        self.tc17 = wx.TextCtrl(id=-1,
				     name='tc17',
				     parent=self,
				     pos=wx.Point(512, 344),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


        self.st18 = wx.StaticText(id=-1,
				       label=self.PList["0619"][1] + ' ' + self.PList["0619"][2],
				       name='st18',
				       parent=self,
				       pos=wx.Point(512, 368),
				       style=0)
	
        self.tc18 = wx.TextCtrl(id=-1,
				     name='tc18',
				     parent=self,
				     pos=wx.Point(512, 384),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')        
	
	
        self.st19 = wx.StaticText(id=-1,
				       label=self.PList["0620"][1] + ' ' + self.PList["0620"][2],
				       name='st19',
				       parent=self,
				       pos=wx.Point(512, 408),
				       style=0)
        
        self.tc19 = wx.TextCtrl(id=-1,
				     name='tc19',
				     parent=self,
				     pos=wx.Point(512, 424),
				     size=wx.Size(200, 21),
				     style=0,
				     value='')


#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		


    def OnListBoxDistributionListListboxClick(self, event):
        self.pipeName = str(self.listBoxDistributionList.GetStringSelection())
        pipes = Status.DB.qdistributionhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].Pipeduct[self.pipeName]

        p = pipes[0]
        self.pipeNo = p.PipeDuctNo
        self.pipeID = p.QDistributionHC_ID
        
        self.tc1.SetValue(str(p.Pipeduct))
        #self.tc2.SetValue(str(p.HeatFromQGenerationHC_id))
        if len(Status.DB.qgenerationhc.QGenerationHC_ID[p.HeatFromQGenerationHC_id]) <> 0:
            self.choiceOfEquipment.SetSelection(\
		self.choiceOfEquipment.FindString(\
		    str(Status.DB.qgenerationhc.QGenerationHC_ID[p.HeatFromQGenerationHC_id][0].Equipment)))
            
        self.tc3.SetValue(str(p.HeatDistMedium))
        self.tc4.SetValue(str(p.DistribCircFlow))
        self.tc5.SetValue(str(p.ToutDistrib))
        self.tc6.SetValue(str(p.TreturnDistrib))
        self.tc7.SetValue(str(p.PercentRecirc))
        self.tc8.SetValue(str(p.Tfeedup))
        self.tc9.SetValue(str(p.PressDistMedium))
        self.tc10.SetValue(str(p.PercentCondRecovery))
        self.tc11.SetValue(str(p.TotLengthDistPipe))
        self.tc12.SetValue(str(p.UDistPipe))
        self.tc13.SetValue(str(p.DDistPipe))
        self.tc14.SetValue(str(p.DeltaDistPipe))		
        self.tc15.SetValue(str(p.NumStorageUnits)) 
        self.tc16.SetValue(str(p.VtotStorage))
        self.tc17.SetValue(str(p.TypeStorage))
        self.tc18.SetValue(str(p.PmaxStorage))
        self.tc19.SetValue(str(p.TmaxStorage))
        #event.Skip()

    def OnButtonClear(self, event):
        self.clear()
        #event.Skip()

    def OnButtonDeleteDistribution(self, event):
        Status.prj.deletePipe(self.pipeID)
        self.clear()
        self.fillPage()
        event.Skip()

    def OnButtonAddDistribution(self, event):
        if Status.PId == 0:
	    return

        pipeName = self.check(self.tc1.GetValue())
        pipes = Status.DB.qdistributionhc.Pipeduct[pipeName].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
	if pipeName <> 'NULL' and len(pipes) == 0:

            newID = Status.prj.addPipeDummy()
            
            eqTable = Status.DB.qgenerationhc.Equipment[str(self.choiceOfEquipment.GetStringSelection())].\
                      Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
            if len(eqTable) >0: qgid = eqTable[0].QGenerationHC_ID
            else: qgid = None
        
	    tmp = {
		"Questionnaire_id":Status.PId,
		"Pipeduct":self.check(self.tc1.GetValue()),
		"HeatFromQGenerationHC_id":qgid,
		"HeatDistMedium":self.check(self.tc3.GetValue()), 
		"DistribCircFlow":self.check(self.tc4.GetValue()), 
		"ToutDistrib":self.check(self.tc5.GetValue()), 
		"TreturnDistrib":self.check(self.tc6.GetValue()), 
		"PercentRecirc":self.check(self.tc7.GetValue()), 
		"Tfeedup":self.check(self.tc8.GetValue()), 
		"PressDistMedium":self.check(self.tc9.GetValue()), 
		"PercentCondRecovery":self.check(self.tc10.GetValue()), 
		"TotLengthDistPipe":self.check(self.tc11.GetValue()), 
		"UDistPipe":self.check(self.tc12.GetValue()), 
		"DDistPipe":self.check(self.tc13.GetValue()), 
		"DeltaDistPipe":self.check(self.tc14.GetValue()), 		
		"NumStorageUnits":self.check(self.tc15.GetValue()),  
		"VtotStorage":self.check(self.tc16.GetValue()), 
		"TypeStorage":self.check(self.tc17.GetValue()), 
		"PmaxStorage":self.check(self.tc18.GetValue()), 
		"TmaxStorage":self.check(self.tc19.GetValue()),
		"IsAlternative":0
		}

            q = Status.DB.qdistributionhc.QDistributionHC_ID[newID][0]
	    q.update(tmp)               
	    Status.SQL.commit()
	    self.fillPage()

	elif pipeName <> 'NULL' and len(pipes) == 1:

            eqTable = Status.DB.qgenerationhc.Equipment[\
		str(self.choiceOfEquipment.GetStringSelection())].\
		Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]

            if len(eqTable) >0: qgid = eqTable[0].QGenerationHC_ID                       
            else: qgid = None
        
	    tmp = {
		"Pipeduct":self.check(self.tc1.GetValue()),
		"HeatFromQGenerationHC_id":qgid,
		"HeatDistMedium":self.check(self.tc3.GetValue()), 
		"DistribCircFlow":self.check(self.tc4.GetValue()), 
		"ToutDistrib":self.check(self.tc5.GetValue()), 
		"TreturnDistrib":self.check(self.tc6.GetValue()), 
		"PercentRecirc":self.check(self.tc7.GetValue()), 
		"Tfeedup":self.check(self.tc8.GetValue()), 
		"PressDistMedium":self.check(self.tc9.GetValue()), 
		"PercentCondRecovery":self.check(self.tc10.GetValue()), 
		"TotLengthDistPipe":self.check(self.tc11.GetValue()), 
		"UDistPipe":self.check(self.tc12.GetValue()), 
		"DDistPipe":self.check(self.tc13.GetValue()), 
		"DeltaDistPipe":self.check(self.tc14.GetValue()), 		
		"NumStorageUnits":self.check(self.tc15.GetValue()),  
		"VtotStorage":self.check(self.tc16.GetValue()), 
		"TypeStorage":self.check(self.tc17.GetValue()), 
		"PmaxStorage":self.check(self.tc18.GetValue()), 
		"TmaxStorage":self.check(self.tc19.GetValue()),
		"IsAlternative":0
		}
	    
	    q = pipes[0]
	    q.update(tmp)               
	    Status.SQL.commit()
	    self.fillPage()
                          
	else:
	    self.showError("Pipeduct have to be an uniqe value!")

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

    def fillchoiceOfEquipment(self):
        self.choiceOfEquipment.Clear()
        self.choiceOfEquipment.Append("None")
        if Status.PId <> 0:
            equipments = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
            if len(equipments) <> 0:
                for equipe in equipments:
                    self.choiceOfEquipment.Append(equipe.Equipment)
        self.choiceOfEquipment.SetSelection(0)


    def fillPage(self):
        self.listBoxDistributionList.Clear()
        pipes = Status.DB.qdistributionhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]
        if len(pipes) > 0:
            for pipe in pipes:
                self.listBoxDistributionList.Append (str(pipe.Pipeduct))


    def check(self, value):
        if value <> "" and value <> "None":
            return value
        else:
            return 'NULL'

    def clear(self):
        self.tc1.SetValue('')
        #self.tc2.SetValue('')
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
        self.tc19.SetValue('')
        
        
