#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	PanelQ0: Questionnaire page 4
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Tom Sobota	April 2008
#       Revised by:         Hans Schweiger 13/04/2008
#
#       Changes to previous version:
#       13/04/08:       Additional inputs in init: selection
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


class PanelQ4(wx.Panel):
    def __init__(self, parent, main, eqId):
        print "PanelQ4 (__init__)"
	self.parent = parent
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)

#HS2004-04-13 added
        if eqId is not None:
            equipe = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].QGenerationHC_ID[eqId][0]
            self.display(equipe)


    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Panel.__init__(self, id=-1, name='PanelQ4', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

        self.stInfo1 = wx.StaticText(id=-1,
					  label=self.PList["X060"][1],
					  name='stInfo1',
					  parent=self,
					  pos=wx.Point(24, 24),
					  style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
	
        self.stInfo2 = wx.StaticText(id=-1,
					  label=self.PList["0500"][1],
					  name='stInfo2',
					  parent=self,
					  pos=wx.Point(272, 24),
					  style=0)
        self.stInfo2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))


        self.listBoxEquipment = wx.ListBox(choices=[],
						    id=-1,
						    name='listBoxEquipment',
						    parent=self,
						    pos=wx.Point(24, 40),
						    size=wx.Size(200, 216),
						    style=0)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxEquipmentClick, self.listBoxEquipment)


        self.buttonDeleteEquipment = wx.Button(id=-1,
						    label=self.PList["X061"][1],
						    name='buttonDeleteEquipment',
						    parent=self,
						    pos=wx.Point(32, 264),
						    size=wx.Size(192, 32),
						    style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteEquipment, self.buttonDeleteEquipment)

        self.buttonAddEquipment = wx.Button(id=-1,
						 label=self.PList["X062"][1],
						 name='buttonAddEquipment',
						 parent=self,
						 pos=wx.Point(520, 464),
						 size=wx.Size(192, 32),
						 style=0)
        self.Bind(wx.EVT_BUTTON,self.OnButtonAddEquipment, self.buttonAddEquipment)

        self.buttonClear = wx.Button(id=-1,
					  label=self.PList["X028"][1],
					  name='buttonClear',
					  parent=self,
					  pos=wx.Point(280, 464),
					  size=wx.Size(192, 32),
					  style=0)
        self.Bind(wx.EVT_BUTTON,self.OnButtonClear, self.buttonClear)
        

        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label=u'Cancel',
              name=u'btnCancel', parent=self, pos=wx.Point(520, 500),
              size=wx.Size(96, 32), style=0)

        self.btnAccept = wx.Button(id=wx.ID_OK, label=u'OK',
              name=u'btnAccept', parent=self, pos=wx.Point(616, 500),
              size=wx.Size(96, 32), style=0)

        self.st1 = wx.StaticText(id=-1,
				      label=self.PList["0501"][1] + ' ' +self.PList["0501"][2],
				      name='st1',
				      parent=self,
				      pos=wx.Point(272, 48),
				      style=0)

        self.tc1 = wx.TextCtrl(id=-1,
				    name='tc1',
				    parent=self,
				    pos=wx.Point(272, 64),
				    size=wx.Size(200, 21),
				    style=0,value='')


        self.st2 = wx.StaticText(id=-1,
				      label=self.PList["0502"][1] + ' ' +self.PList["0502"][2],
				      name='st2',
				      parent=self,
				      pos=wx.Point(272, 88),
				      style=0)

        self.tc2 = wx.TextCtrl(id=-1,
				    name='tc2',
				    parent=self,
				    pos=wx.Point(272, 104),
				    size=wx.Size(200, 21),
				    style=0,value='')


        self.st3 = wx.StaticText(id=-1,
				      label=self.PList["0503"][1] + ' ' +self.PList["0503"][2],
				      name='st3',
				      parent=self,
				      pos=wx.Point(272, 128),
				      style=0)

        self.tc3 = wx.TextCtrl(id=-1,
				    name='tc3',
				    parent=self, pos=wx.Point(272, 144), size=wx.Size(200, 21),
				    style=0, value='')


        self.st4 = wx.StaticText(id=-1,
				      label=self.PList["0504"][1] + ' ' +self.PList["0504"][2],
				      name='st4',
				      parent=self,
				      pos=wx.Point(272, 168),
				      style=0)

        self.tc4 = wx.TextCtrl(id=-1,
				    name='tc4',
				    parent=self,
				    pos=wx.Point(272, 184),
				    size=wx.Size(200, 21),
				    style=0, value='')


        self.st5 = wx.StaticText(id=-1,
				      label=self.PList["0505"][1] + ' ' +self.PList["0505"][2],
				      name='st5',
				      parent=self,
				      pos=wx.Point(272, 208),
				      style=0)

        self.tc5 = wx.TextCtrl(id=-1,
				    name='tc5',
				    parent=self,
				    pos=wx.Point(272, 224),
				    size=wx.Size(200, 21),
				    style=0, value='')


        self.st6 = wx.StaticText(id=-1,
				      label=self.PList["0506"][1] + ' ' +self.PList["0506"][2],
				      name='st6',
				      parent=self,
				      pos=wx.Point(272, 248),
				      style=0)

        self.tc6 = wx.TextCtrl(id=-1, name='tc6',
				    parent=self,
				    pos=wx.Point(272, 264),
				    size=wx.Size(200, 21),
				    style=0,value='')


        self.st7 = wx.StaticText(id=-1,
				      label=self.PList["0507"][1] + ' ' +self.PList["0507"][2],
				      name='st7',
				      parent=self,
				      pos=wx.Point(272, 288),
				      style=0)

        #self.tc7 = wx.TextCtrl(id=-1, name='tc7',
        #      parent=self, pos=wx.Point(272, 304), size=wx.Size(200, 21),
        #      style=0, value='')

        self.choiceOfDBFuel = wx.Choice(choices=[],
					     id=-1,
					     name='choiceOfDBFuel',
					     parent=self,
					     pos=wx.Point(272, 304),
					     size=wx.Size(200, 21),
					     style=0)


        self.st8 = wx.StaticText(id=-1,
				      label=self.PList["0521"][1] + ' ' +self.PList["0521"][2],
				      name='st8',
				      parent=self,
				      pos=wx.Point(272, 328),
				      style=0)

        self.tc8 = wx.TextCtrl(id=-1,
				    name='tc8',
				    parent=self,
				    pos=wx.Point(272, 344),
				    size=wx.Size(200, 21),
				    style=0,value='')


        self.st9 = wx.StaticText(id=-1,
				      label=self.PList["0508"][1] + ' ' +self.PList["0508"][2],
				      name='st9',
				      parent=self,
				      pos=wx.Point(272, 368),
				      style=0)

        self.tc9 = wx.TextCtrl(id=-1,
				    name='tc9',
				    parent=self,
				    pos=wx.Point(272, 384),
				    size=wx.Size(200, 21),
				    style=0,value='')


        self.st10 = wx.StaticText(id=-1,
				       label=self.PList["0509"][1] + ' ' +self.PList["0509"][2],
				       name='st10',
				       parent=self,
				       pos=wx.Point(272, 408),
				       style=0)

        self.tc10 = wx.TextCtrl(id=-1,
				     name='tc10',
				     parent=self,
				     pos=wx.Point(272, 424),
				     size=wx.Size(200, 21),
				     style=0, value='')


        self.st11 = wx.StaticText(id=-1,
				       label=self.PList["0510"][1] + ' ' +self.PList["0510"][2],
				       name='st11',
				       parent=self,
				       pos=wx.Point(512, 48),
				       style=0)

        self.tc11 = wx.TextCtrl(id=-1,
				     name='tc11',
				     parent=self,
				     pos=wx.Point(512, 64),
				     size=wx.Size(200, 21),
				     style=0, value='')


        self.st12 = wx.StaticText(id=-1,
				       label=self.PList["0511"][1] + ' ' +self.PList["0511"][2],
				       name='st12',
				       parent=self,
				       pos=wx.Point(512, 88),
				       style=0)

        self.tc12 = wx.TextCtrl(id=-1,
				     name='tc12',
				     parent=self,
				     pos=wx.Point(512, 104),
				     size=wx.Size(200, 21),
				     style=0, value='')


        self.st13 = wx.StaticText(id=-1,
				       label=self.PList["0512"][1] + ' ' +self.PList["0512"][2],
				       name='st13',
				       parent=self,
				       pos=wx.Point(512, 128),
				       style=0)

        self.tc13 = wx.TextCtrl(id=-1,
				     name='tc13',
				     parent=self,
				     pos=wx.Point(512, 144),
				     size=wx.Size(200, 21),
				     style=0, value='')


        self.st14 = wx.StaticText(id=-1,
				       label=self.PList["0514"][1] + ' ' + self.PList["0514"][2],
				       name='st14',
				       parent=self,
				       pos=wx.Point(512, 168),
				       style=0)

        self.tc14 = wx.TextCtrl(id=-1,
				     name='tc14',
				     parent=self,
				     pos=wx.Point(512, 184),
				     size=wx.Size(200, 21),
				     style=0, value='')


        self.st15 = wx.StaticText(id=-1,
				       label=self.PList["0513"][1] + ' ' + self.PList["0513"][2],
				       name='st15',
				       parent=self,
				       pos=wx.Point(512, 208),
				       style=0)

        self.tc15 = wx.TextCtrl(id=-1,
				     name='tc15',
				     parent=self,
				     pos=wx.Point(512, 224),
				     size=wx.Size(200, 21),
				     style=0, value='')


        self.st16 = wx.StaticText(id=-1,
				       label=self.PList["0515"][1] + ' ' + self.PList["0515"][2],
				       name='st16',
				       parent=self,
				       pos=wx.Point(512, 248),
				       style=0)

        self.tc16 = wx.TextCtrl(id=-1,
				     name='tc16',
				     parent=self,
				     pos=wx.Point(512, 264),
				     size=wx.Size(200, 21),
				     style=0, value='')


        self.st17 = wx.StaticText(id=-1,
				       label=self.PList["0516"][1] + ' ' + self.PList["0516"][2],
				       name='st17',
				       parent=self,
				       pos=wx.Point(512, 288),
				       style=0)

        self.tc17 = wx.TextCtrl(id=-1,
				     name='tc17',
				     parent=self,
				     pos=wx.Point(512, 304),
				     size=wx.Size(200, 21),
				     style=0, value='')


        self.st18 = wx.StaticText(id=-1, 
				       label=self.PList["0517"][1] + ' ' + self.PList["0517"][2],
				       name='st18',
				       parent=self,
				       pos=wx.Point(512, 328),
				       style=0)

        self.tc18 = wx.TextCtrl(id=-1,
				     name='tc18',
				     parent=self,
				     pos=wx.Point(512, 344),
				     size=wx.Size(200, 21),
				     style=0, value='')


        self.st19 = wx.StaticText(id=-1,
				       label=self.PList["0518"][1] + ' ' + self.PList["0518"][2],
				       name='st19',
				       parent=self,
				       pos=wx.Point(512, 368),
				       style=0)

        self.tc19 = wx.TextCtrl(id=-1,
				     name='tc19',
				     parent=self,
				     pos=wx.Point(512, 384),
				     size=wx.Size(200, 21),
				     style=0, value='')


        self.st20 = wx.StaticText(id=-1,
				       label=self.PList["0520"][1] + ' ' + self.PList["0520"][2],
				       name='st20',
				       parent=self,
				       pos=wx.Point(512, 408),
				       style=0)

        self.tc20 = wx.TextCtrl(id=-1,
				     name='tc20',
				     parent=self,
				     pos=wx.Point(512, 424),
				     size=wx.Size(200, 21),
				     style=0, value='')


#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		
    
    def OnListBoxEquipmentClick(self, event):
        equipe = Status.DB.qgenerationhc.Questionnaire_id[self.main.activeQid].Equipment[\
	    str(self.listBoxEquipment.GetStringSelection())][0]
        self.display(equipe)
        event.Skip()

#HS2004-04-13 function display added
        
    def display(self,q):
        self.tc1.SetValue(str(q.Equipment))
        self.tc2.SetValue(str(q.Manufact))
        self.tc3.SetValue(str(q.YearManufact))
        self.tc4.SetValue(str(q.Model))
        self.tc5.SetValue(str(q.EquipType))
        self.tc6.SetValue(str(q.NumEquipUnits))
        self.tc9.SetValue(str(q.HCGPnom))
        self.tc10.SetValue(str(q.FuelConsum))
        self.tc11.SetValue(str(q.UnitsFuelConsum))
        self.tc12.SetValue(str(q.ElectriConsum))
        self.tc13.SetValue(str(q.HCGTEfficiency))
        self.tc14.SetValue(str(q.HCGEEfficiency))
        self.tc15.SetValue(str(q.ElectriProduction))
        self.tc16.SetValue(str(q.TExhaustGas))
        self.tc17.SetValue(str(q.PartLoad))
        self.tc18.SetValue(str(q.HPerDayEq))
        self.tc19.SetValue(str(q.NDaysEq))
        self.tc20.SetValue(str(q.PipeDuctEquip))
        self.tc8.SetValue(str(q.CoolTowerType))
        if q.DBFuel_id <> None:
            self.choiceOfDBFuel.SetSelection(self.choiceOfDBFuel.FindString(\
		    str(Status.DB.dbfuel.DBFuel_ID[q.DBFuel_id][0].FuelName)))

    def OnButtonDeleteEquipment(self, event):
        event.Skip()



    def OnButtonAddEquipment(self, event):        
        if self.main.activeQid <> 0:
            if self.check(self.tc1.GetValue()) <> 'NULL' and \
		    len(Status.DB.qgenerationhc.Equipment[self.tc1.GetValue()].Questionnaire_id[\
		    self.main.activeQid]) == 0:
                dbfid = Status.DB.dbfuel.FuelName[\
		    str(self.choiceOfDBFuel.GetStringSelection())][0].DBFuel_ID                      
        
                tmp = {
                    "Questionnaire_id":self.main.activeQid,
                    "Equipment":self.check(self.tc1.GetValue()), 
                    "Manufact":self.check(self.tc2.GetValue()), 
                    "YearManufact":self.check(self.tc3.GetValue()), 
                    "Model":self.check(self.tc4.GetValue()), 
                    "EquipType":self.check(self.tc5.GetValue()), 
                    "NumEquipUnits":self.check(self.tc6.GetValue()),
                    "DBFuel_id":dbfid,
                    "HCGPnom":self.check(self.tc9.GetValue()), 
                    "FuelConsum":self.check(self.tc10.GetValue()), 
                    "UnitsFuelConsum":self.check(self.tc11.GetValue()), 
                    "ElectriConsum":self.check(self.tc12.GetValue()), 
                    "HCGTEfficiency":self.check(self.tc13.GetValue()), 
                    "HCGEEfficiency":self.check(self.tc14.GetValue()), 
                    "ElectriProduction":self.check(self.tc15.GetValue()), 
                    "TExhaustGas":self.check(self.tc16.GetValue()), 
                    "PartLoad":self.check(self.tc17.GetValue()), 
                    "HPerDayEq":self.check(self.tc18.GetValue()), 
                    "NDaysEq":self.check(self.tc19.GetValue()), 
                    "PipeDuctEquip":self.check(self.tc20.GetValue()), 
                    "CoolTowerType":self.check(self.tc8.GetValue()),
                    "IsAlternative":0
                    }

                Status.DB.qgenerationhc.insert(tmp)               
                Status.SQL.commit()
                self.fillEquipmentList()

            elif self.check(self.tc1.GetValue()) <> 'NULL' and \
		    len(Status.DB.qgenerationhc.Equipment[self.tc1.GetValue()].Questionnaire_id[\
		    self.main.activeQid]) == 1:
                dbfid = Status.DB.dbfuel.FuelName[\
		    str(self.choiceOfDBFuel.GetStringSelection())][0].DBFuel_ID                       
        
                tmp = {
                    "Equipment":self.check(self.tc1.GetValue()), 
                    "Manufact":self.check(self.tc2.GetValue()), 
                    "YearManufact":self.check(self.tc3.GetValue()), 
                    "Model":self.check(self.tc4.GetValue()), 
                    "EquipType":self.check(self.tc5.GetValue()), 
                    "NumEquipUnits":self.check(self.tc6.GetValue()),
                    "DBFuel_id":dbfid,
                    "HCGPnom":self.check(self.tc9.GetValue()), 
                    "FuelConsum":self.check(self.tc10.GetValue()), 
                    "UnitsFuelConsum":self.check(self.tc11.GetValue()), 
                    "ElectriConsum":self.check(self.tc12.GetValue()), 
                    "HCGTEfficiency":self.check(self.tc13.GetValue()), 
                    "HCGEEfficiency":self.check(self.tc14.GetValue()), 
                    "ElectriProduction":self.check(self.tc15.GetValue()), 
                    "TExhaustGas":self.check(self.tc16.GetValue()), 
                    "PartLoad":self.check(self.tc17.GetValue()), 
                    "HPerDayEq":self.check(self.tc18.GetValue()), 
                    "NDaysEq":self.check(self.tc19.GetValue()), 
                    "PipeDuctEquip":self.check(self.tc20.GetValue()), 
                    "CoolTowerType":self.check(self.tc8.GetValue()),
                    "IsAlternative":0
                    }
                q = Status.DB.qgenerationhc.Equipment[\
		    self.tc1.GetValue()].Questionnaire_id[self.main.activeQid][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillEquipmentList()
                          
            else:
                self.showError("Equipment has to be an unique value!")
        
        

    def OnButtonClear(self, event):
        self.clear()
        event.Skip()


#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

#HS2004-04-13 function display extracted from event handler
        
    def display(self,q):
        self.tc1.SetValue(str(q.Equipment))
        self.tc2.SetValue(str(q.Manufact))
        self.tc3.SetValue(str(q.YearManufact))
        self.tc4.SetValue(str(q.Model))
        self.tc5.SetValue(str(q.EquipType))
        self.tc6.SetValue(str(q.NumEquipUnits))
        self.tc9.SetValue(str(q.HCGPnom))
        self.tc10.SetValue(str(q.FuelConsum))
        self.tc11.SetValue(str(q.UnitsFuelConsum))
        self.tc12.SetValue(str(q.ElectriConsum))
        self.tc13.SetValue(str(q.HCGTEfficiency))
        self.tc14.SetValue(str(q.HCGEEfficiency))
        self.tc15.SetValue(str(q.ElectriProduction))
        self.tc16.SetValue(str(q.TExhaustGas))
        self.tc17.SetValue(str(q.PartLoad))
        self.tc18.SetValue(str(q.HPerDayEq))
        self.tc19.SetValue(str(q.NDaysEq))
        self.tc20.SetValue(str(q.PipeDuctEquip))
        self.tc8.SetValue(str(q.CoolTowerType))
        if q.DBFuel_id <> None:
            self.choiceOfDBFuel.SetSelection(self.choiceOfDBFuel.FindString(\
		    str(Status.DB.dbfuel.DBFuel_ID[q.DBFuel_id][0].FuelName)))

    def clear(self):
        self.tc1.SetValue('')
        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
        self.tc6.SetValue('')
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
        self.tc8.SetValue('')
        
    def fillEquipmentList(self):
        self.listBoxEquipment.Clear()
        if len(Status.DB.qgenerationhc.Questionnaire_id[self.main.activeQid]) > 0:
            for n in Status.DB.qgenerationhc.Questionnaire_id[self.main.activeQid]:
                self.listBoxEquipment.Append (str(n.Equipment))


    def fillChoiceOfDBFuel(self):
        self.choiceOfDBFuel.Clear()
        self.choiceOfDBFuel.Append ("None")
        for n in Status.DB.dbfuel.FuelName["%"]:
            self.choiceOfDBFuel.Append (n.FuelName)
        self.choiceOfDBFuel.SetSelection(0)


    def fillPage(self):
	if self.main.activeQid != 0:
	    self.fillEquipmentList()

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
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(800, 600), title="Einstein - panelQ4")
    main = Main(1)
    panel = PanelQ4(frame, main)

    frame.Show(True)
    app.MainLoop()
