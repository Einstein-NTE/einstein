import wx
import pSQL
import HelperClass
from status import Status


class PanelQ8(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Panel.__init__(self, id=-1, name='PanelQ8', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

        self.stInfo1 = wx.StaticText(id=-1,
              label=self.PList["X084"][1], name='stInfo1', parent=self,
              pos=wx.Point(24, 24), size=wx.Size(64, 13), style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo2 = wx.StaticText(id=-1,
              label=self.PList["X085"][1], name='stInfo2',
              parent=self, pos=wx.Point(272, 24), size=wx.Size(157, 13),
              style=0)
        self.stInfo2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        
        
        self.listBoxBuildingList = wx.ListBox(choices=[], id=-1,
              name='listBoxBuildingList', parent=self,
              pos=wx.Point(24, 40), size=wx.Size(200, 216), style=0)
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxBuildingListClick, self.listBoxBuildingList)


        self.buttonClear = wx.Button(id=-1,
              label=self.PList["X028"][1], name='buttonClear', parent=self,
              pos=wx.Point(272, 464), size=wx.Size(192, 32), style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClear, self.buttonClear)

        self.buttonDeleteBuilding = wx.Button(id=-1,
              label=self.PList["X086"][1], name='buttonDeleteBuilding',
              parent=self, pos=wx.Point(128, 264), size=wx.Size(192, 32),
              style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteBuilding, self.buttonDeleteBuilding)

        self.buttonAddBuilding = wx.Button(id=-1,
              label=self.PList["X087"][1], name='buttonAddBuilding',
              parent=self, pos=wx.Point(584, 464), size=wx.Size(192, 32),
              style=0)
	self.Bind(wx.EVT_BUTTON, self.OnButtonAddBuilding, self.buttonAddBuilding)


        

        self.st1 = wx.StaticText(id=-1, label=self.PList["0802"][1] + " " + self.PList["0802"][2], name='st1', parent=self, pos=wx.Point(272, 48), style=0)
        
        self.tc1 = wx.TextCtrl(id=-1, name='tc1',
              parent=self, pos=wx.Point(272, 64), size=wx.Size(200, 21),
              style=0, value='')



        self.st2 = wx.StaticText(id=-1, label=self.PList["0803"][1] + " " + self.PList["0803"][2], name='st2', parent=self, pos=wx.Point(272, 88), style=0)

        self.tc2 = wx.TextCtrl(id=-1, name='tc2',
              parent=self, pos=wx.Point(272, 104), size=wx.Size(200, 21),
              style=0, value='')



        self.st3 = wx.StaticText(id=-1, label=self.PList["0804"][1] + " " + self.PList["0804"][2], name='st3', parent=self, pos=wx.Point(272, 128), style=0)

        self.tc3 = wx.TextCtrl(id=-1, name='tc3',
              parent=self, pos=wx.Point(272, 144), size=wx.Size(200, 21),
              style=0, value='')



        self.st4 = wx.StaticText(id=-1, label=self.PList["0805"][1] + " " + self.PList["0805"][2], name='st4', parent=self, pos=wx.Point(272, 168), style=0)

        self.tc4 = wx.TextCtrl(id=-1, name='tc4',
              parent=self, pos=wx.Point(272, 184), size=wx.Size(200, 21),
              style=0, value='')        


        
        self.st5 = wx.StaticText(id=-1, label=self.PList["0807"][1] + " " + self.PList["0807"][2], name='st5', parent=self, pos=wx.Point(272, 208), style=0)

        self.tc5 = wx.TextCtrl(id=-1, name='tc5',
              parent=self, pos=wx.Point(272, 224), size=wx.Size(200, 21),
              style=0, value='')





        self.st6 = wx.StaticText(id=-1, label=self.PList["0808"][1] + " " + self.PList["0808"][2], name='st6', parent=self, pos=wx.Point(272, 248), style=0)

        self.tc6 = wx.TextCtrl(id=-1, name='tc6',
              parent=self, pos=wx.Point(272, 264), size=wx.Size(200, 21),
              style=0, value='')




        self.st7 = wx.StaticText(id=-1, label=self.PList["0809"][1] + " " + self.PList["0809"][2], name='st7', parent=self, pos=wx.Point(272, 288), style=0)

        self.tc7 = wx.TextCtrl(id=-1, name='tc7',
              parent=self, pos=wx.Point(272, 304), size=wx.Size(200, 21),
              style=0, value='')




        self.st8 = wx.StaticText(id=-1, label=self.PList["0810"][1] + " " + self.PList["0810"][2], name='st8', parent=self, pos=wx.Point(272, 328), style=0)

        self.tc8 = wx.TextCtrl(id=-1, name='tc8',
              parent=self, pos=wx.Point(272, 344), size=wx.Size(200, 21),
              style=0, value='')




        self.st9 = wx.StaticText(id=-1, label=self.PList["0811"][1] + " " + self.PList["0811"][2], name='st9', parent=self, pos=wx.Point(272, 368), style=0)

        self.tc9 = wx.TextCtrl(id=-1, name='tc9',
              parent=self, pos=wx.Point(272, 384), size=wx.Size(200, 21),
              style=0, value='')

        

        self.st10 = wx.StaticText(id=-1, label=self.PList["0812"][1] + " " + self.PList["0812"][2], name='st10', parent=self, pos=wx.Point(272, 408), style=0)

        self.tc10 = wx.TextCtrl(id=-1, name='tc10',
              parent=self, pos=wx.Point(272, 424), size=wx.Size(200, 21),
              style=0, value='')




        self.st11 = wx.StaticText(id=-1, label=self.PList["0813"][1] + " " + self.PList["0813"][2], name='st11', parent=self, pos=wx.Point(512, 48), style=0)

        self.tc11 = wx.TextCtrl(id=-1, name='tc11',
              parent=self, pos=wx.Point(512, 64), size=wx.Size(200, 21),
              style=0, value='')




        self.st12 = wx.StaticText(id=-1, label=self.PList["0814"][1] + " " + self.PList["0814"][2], name='st12', parent=self, pos=wx.Point(512, 88), style=0)

        self.tc12_1 = wx.TextCtrl(id=-1,
              name='tc12_1', parent=self, pos=wx.Point(512, 104),
              size=wx.Size(96, 21), style=0, value='')

        self.tc12_2 = wx.TextCtrl(id=-1,
              name='tc12_2', parent=self, pos=wx.Point(616, 104),
              size=wx.Size(96, 21), style=0, value='')



        
        self.st13 = wx.StaticText(id=-1, label=self.PList["0815"][1] + " " + self.PList["0815"][2], name='st13', parent=self, pos=wx.Point(512, 128), style=0)

        self.tc13_1 = wx.TextCtrl(id=-1,
              name='tc13_1', parent=self, pos=wx.Point(512, 144),
              size=wx.Size(96, 21), style=0, value='')      

        self.tc13_2 = wx.TextCtrl(id=-1,
              name='tc13_2', parent=self, pos=wx.Point(616, 144),
              size=wx.Size(96, 21), style=0, value='')




        self.st14 = wx.StaticText(id=-1, label=self.PList["0816"][1] + " " + self.PList["0816"][2], name='st14', parent=self, pos=wx.Point(512, 168), style=0)

        self.tc14_1 = wx.TextCtrl(id=-1,
              name='tc14_1', parent=self, pos=wx.Point(512, 184),
              size=wx.Size(96, 21), style=0, value='')        

        self.tc14_2 = wx.TextCtrl(id=-1,
              name='tc14_2', parent=self, pos=wx.Point(616, 184),
              size=wx.Size(96, 21), style=0, value='')


#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		


    def OnListBoxBuildingListClick(self, event):
        q = Status.DB.qbuildings.Questionnaire_id[self.main.activeQid].BuildName[str(self.listBoxBuildingList.GetStringSelection())][0]
        self.tc1.SetValue(str(q.BuildName))
        self.tc2.SetValue(str(q.BuildConstructSurface))
        self.tc3.SetValue(str(q.BuildUsefulSurface))
        self.tc4.SetValue(str(q.BuildUsage))
        self.tc5.SetValue(str(q.BuildMaxHP))
        self.tc6.SetValue(str(q.BuildMaxCP))
        self.tc7.SetValue(str(q.BuildAnnualHeating))
        self.tc8.SetValue(str(q.BuildAnnualAirCond))
        self.tc9.SetValue(str(q.BuildDailyDHW))
        self.tc10.SetValue(str(q.BuildHoursOccup))
        self.tc11.SetValue(str(q.BuildDaysInUse))
        self.tc12_1.SetValue(str(q.BuildHolidaysPeriodStart))
        self.tc12_2.SetValue(str(q.BuildHolidaysPeriodStop))
        self.tc13_1.SetValue(str(q.BuildHeatingPeriodStart))
        self.tc13_2.SetValue(str(q.BuildHeatingPeriodStop))
        self.tc14_1.SetValue(str(q.BuildAirCondPeriodStart))
        self.tc14_2.SetValue(str(q.BuildAirCondPeriodStop))
        #event.Skip()

    def OnButtonClear(self, event):
        self.clear()
        #event.Skip()

    def OnButtonDeleteBuilding(self, event):
        event.Skip()

    def OnButtonAddBuilding(self, event):
        if self.main.activeQid <> 0:
            if self.check(self.tc1.GetValue()) <> 'NULL' and len(Status.DB.qbuildings.BuildName[self.tc1.GetValue()].Questionnaire_id[self.main.activeQid]) == 0:

                tmp = {
                    "Questionnaire_id":self.main.activeQid,
                    "BuildName":self.check(self.tc1.GetValue()), 
                    "BuildConstructSurface":self.check(self.tc2.GetValue()), 
                    "BuildUsefulSurface":self.check(self.tc3.GetValue()), 
                    "BuildUsage":self.check(self.tc4.GetValue()),
                    "BuildMaxHP":self.check(self.tc5.GetValue()), 
                    "BuildMaxCP":self.check(self.tc6.GetValue()), 
                    "BuildAnnualHeating":self.check(self.tc7.GetValue()), 
                    "BuildAnnualAirCond":self.check(self.tc8.GetValue()), 
                    "BuildDailyDHW":self.check(self.tc9.GetValue()), 
                    "BuildHoursOccup":self.check(self.tc10.GetValue()), 
                    "BuildDaysInUse":self.check(self.tc11.GetValue()), 
                    "BuildHolidaysPeriodStart":self.check(self.tc12_1.GetValue()), 
                    "BuildHolidaysPeriodStop":self.check(self.tc12_2.GetValue()), 
                    "BuildHeatingPeriodStart":self.check(self.tc13_1.GetValue()), 
                    "BuildHeatingPeriodStop":self.check(self.tc13_2.GetValue()), 
                    "BuildAirCondPeriodStart":self.check(self.tc14_1.GetValue()), 
                    "BuildAirCondPeriodStop":self.check(self.tc14_2.GetValue())
                    }

                Status.DB.qbuildings.insert(tmp)               
                Status.SQL.commit()
                self.fillBuildingList()

            elif self.check(self.tc1.GetValue()) <> 'NULL' and len(Status.DB.qbuildings.BuildName[self.tc1.GetValue()].Questionnaire_id[self.main.activeQid]) == 1:

                tmp = {
                    "BuildName":self.check(self.tc1.GetValue()), 
                    "BuildConstructSurface":self.check(self.tc2.GetValue()), 
                    "BuildUsefulSurface":self.check(self.tc3.GetValue()), 
                    "BuildUsage":self.check(self.tc4.GetValue()),
                    "BuildMaxHP":self.check(self.tc5.GetValue()), 
                    "BuildMaxCP":self.check(self.tc6.GetValue()), 
                    "BuildAnnualHeating":self.check(self.tc7.GetValue()), 
                    "BuildAnnualAirCond":self.check(self.tc8.GetValue()), 
                    "BuildDailyDHW":self.check(self.tc9.GetValue()), 
                    "BuildHoursOccup":self.check(self.tc10.GetValue()), 
                    "BuildDaysInUse":self.check(self.tc11.GetValue()), 
                    "BuildHolidaysPeriodStart":self.check(self.tc12_1.GetValue()), 
                    "BuildHolidaysPeriodStop":self.check(self.tc12_2.GetValue()), 
                    "BuildHeatingPeriodStart":self.check(self.tc13_1.GetValue()), 
                    "BuildHeatingPeriodStop":self.check(self.tc13_2.GetValue()), 
                    "BuildAirCondPeriodStart":self.check(self.tc14_1.GetValue()), 
                    "BuildAirCondPeriodStop":self.check(self.tc14_2.GetValue())
                    }
                q = Status.DB.qbuildings.BuildName[self.tc1.GetValue()].Questionnaire_id[self.main.activeQid][0]
                q.update(tmp)               
                Status.SQL.commit()
                self.fillBuildingList()
                          
            else:
                self.showError("BuildingName have to be an uniqe value!")


#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

    def fillBuildingList(self):
        self.listBoxBuildingList.Clear()
        if len(Status.DB.qbuildings.Questionnaire_id[self.main.activeQid]) > 0:
            for n in Status.DB.qbuildings.Questionnaire_id[self.main.activeQid]:
                self.listBoxBuildingList.Append (str(n.BuildName))


    def fillPage(self):
	self.fillBuildingList()
            
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
        self.tc12_1.SetValue('')
        self.tc12_2.SetValue('')
        self.tc13_1.SetValue('')
        self.tc13_2.SetValue('')
        self.tc14_1.SetValue('')
        self.tc14_2.SetValue('')
