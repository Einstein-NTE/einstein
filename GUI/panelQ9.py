import wx
import pSQL
import HelperClass
from status import Status


class PanelQ9(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Panel.__init__(self, id=-1, name='PanelQ9', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)

        self.buttonStoreData = wx.Button(id=-1,
              label=self.PList["X019"][1], name='buttonStoreData',
              parent=self, pos=wx.Point(664, 544), size=wx.Size(192, 32),
              style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonStoreData, self.buttonStoreData)

        
        self.stInfo1 = wx.StaticText(id=-1, label=self.PList["1000"][1], name='stInfo1', parent=self, pos=wx.Point(8, 24), style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        #self.stInfo2 = wx.StaticText(id=-1, label=self.PList["X088"][1], name='stInfo2', parent=self, pos=wx.Point(264, 64), style=0)

        #self.stInfo3 = wx.StaticText(id=-1, label=self.PList["X089"][1], name='stInfo3', parent=self, pos=wx.Point(264, 120), style=0)

        self.stInfo4_1 = wx.StaticText(id=-1, label=self.PList["X090"][1], name='stInfo4_1', parent=self, pos=wx.Point(392, 56), style=0)
        
        self.stInfo4_2 = wx.StaticText(id=-1, label=self.PList["X091"][1], name='stInfo4_2', parent=self, pos=wx.Point(600, 56), style=0)


        self.stInfo5 = wx.StaticText(id=-1, label=self.PList["X092"][1], name='stInfo5', parent=self, pos=wx.Point(8, 272), style=0)
        self.stInfo5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo6 = wx.StaticText(id=-1, label=self.PList["X093"][1], name='stInfo6', parent=self, pos=wx.Point(16, 328), style=0)

        self.stInfo7 = wx.StaticText(id=-1, label=self.PList["X094"][1], name='stInfo7', parent=self, pos=wx.Point(16, 352), style=0)

        self.stInfo8 = wx.StaticText(id=-1, label=self.PList["X095"][1], name='stInfo8', parent=self, pos=wx.Point(16, 376), style=0)

        self.stInfo9 = wx.StaticText(id=-1, label=self.PList["X096"][1], name='stInfo9', parent=self, pos=wx.Point(16, 400), style=0)

        self.stInfo10 = wx.StaticText(id=-1, label=self.PList["X097"][1], name='stInfo10', parent=self, pos=wx.Point(16, 424), style=0)

        self.stInfo11 = wx.StaticText(id=-1, label=self.PList["X098"][1], name='stInfo11', parent=self, pos=wx.Point(264, 288), style=0)
        self.stInfo11.SetMaxSize(wx.Size(88, 40))

        self.stInfo12 = wx.StaticText(id=-1, label=self.PList["X099"][1], name='stInfo12', parent=self, pos=wx.Point(368, 288), style=0)
        self.stInfo12.SetMaxSize(wx.Size(88, 40))

        self.stInfo13 = wx.StaticText(id=-1, label=self.PList["X100"][1], name='stInfo13', parent=self, pos=wx.Point(464, 288), style=0)
        self.stInfo13.SetMaxSize(wx.Size(88, 40))

        self.stInfo14 = wx.StaticText(id=-1, label=self.PList["X101"][1], name='stInfo14', parent=self, pos=wx.Point(560, 288), style=0)
        self.stInfo14.SetMaxSize(wx.Size(88, 40))

        self.stInfo15 = wx.StaticText(id=-1, label=self.PList["X102"][1], name='stInfo15', parent=self, pos=wx.Point(8, 472), style=0)
        self.stInfo15.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.st1 = wx.StaticText(id=-1, label=self.PList["1001"][1] + ' ' + self.PList["1001"][2], name='st1', parent=self, pos=wx.Point(16, 48), style=0)

        self.tc1 = wx.TextCtrl(id=-1, name='tc1',
              parent=self, pos=wx.Point(16, 64), size=wx.Size(100, 21),
              style=0, value='')


        self.st2 = wx.StaticText(id=-1, label=self.PList["1002"][1] + ' ' + self.PList["1002"][2], name='st2', parent=self, pos=wx.Point(16, 88), style=0)

        self.tc2 = wx.TextCtrl(id=-1, name='tc2',
              parent=self, pos=wx.Point(16, 104), size=wx.Size(100, 21),
              style=0, value='')


        self.st3 = wx.StaticText(id=-1, label=self.PList["1003"][1] + ' ' + self.PList["1003"][2], name='st3', parent=self, pos=wx.Point(16, 128), style=0)

        self.tc3 = wx.TextCtrl(id=-1, name='tc3',
              parent=self, pos=wx.Point(16, 144), size=wx.Size(100, 21),
              style=0, value='')



        self.st4 = wx.StaticText(id=-1, label=self.PList["1004"][1] + ' ' + self.PList["1004"][2], name='st4', parent=self, pos=wx.Point(16, 168), style=0)

        self.tc4 = wx.TextCtrl(id=-1, name='tc4',
              parent=self, pos=wx.Point(16, 184), size=wx.Size(100, 21),
              style=0, value='')



        self.st5 = wx.StaticText(id=-1, label=self.PList["1005"][1] + ' ' + self.PList["1005"][2], name='st5', parent=self, pos=wx.Point(16, 208), style=0)

        self.tc5 = wx.TextCtrl(id=-1, name='tc5',
              parent=self, pos=wx.Point(16, 224), size=wx.Size(100, 21),
              style=0, value='')


        self.tc6_1 = wx.TextCtrl(id=-1,
              name='tc6_1', parent=self, pos=wx.Point(392, 72),
              size=wx.Size(200, 21), style=0, value='')

        self.tc6_2 = wx.TextCtrl(id=-1,
              name='tc6_2', parent=self, pos=wx.Point(600, 72),
              size=wx.Size(150, 21), style=0, value='')


        self.tc7_1 = wx.TextCtrl(id=-1,
              name='tc7_1', parent=self, pos=wx.Point(392, 96),
              size=wx.Size(200, 21), style=0, value='')

        self.tc7_2 = wx.TextCtrl(id=-1,
              name='tc7_2', parent=self, pos=wx.Point(600, 96),
              size=wx.Size(150, 21), style=0, value='')
        

        self.tc8_1 = wx.TextCtrl(id=-1,
              name='tc8_1', parent=self, pos=wx.Point(392, 120),
              size=wx.Size(200, 21), style=0, value='')

        self.tc8_2 = wx.TextCtrl(id=-1,
              name='tc8_2', parent=self, pos=wx.Point(600, 120),
              size=wx.Size(150, 21), style=0, value='')
        

        self.tc9_1 = wx.TextCtrl(id=-1,
              name='tc9_1', parent=self, pos=wx.Point(392, 144),
              size=wx.Size(200, 21), style=0, value='')
        
        self.tc9_2 = wx.TextCtrl(id=-1,
              name='tc9_2', parent=self, pos=wx.Point(600, 144),
              size=wx.Size(150, 21), style=0, value='')


        self.tc10_1 = wx.TextCtrl(id=-1,
              name='tc10_1', parent=self, pos=wx.Point(248, 328),
              size=wx.Size(100, 21), style=0, value='')        

        self.tc10_2 = wx.TextCtrl(id=-1,
              name='tc10_2', parent=self, pos=wx.Point(352, 328),
              size=wx.Size(100, 21), style=0, value='')

        self.tc10_3 = wx.TextCtrl(id=-1,
              name='tc10_3', parent=self, pos=wx.Point(456, 328),
              size=wx.Size(100, 21), style=0, value='')

        self.tc10_4 = wx.TextCtrl(id=-1,
              name='tc10_4', parent=self, pos=wx.Point(560, 328),
              size=wx.Size(100, 21), style=0, value='')




        self.tc11_1 = wx.TextCtrl(id=-1,
              name='tc11_1', parent=self, pos=wx.Point(248, 352),
              size=wx.Size(100, 21), style=0, value='')

        self.tc11_2 = wx.TextCtrl(id=-1,
              name='tc11_2', parent=self, pos=wx.Point(352, 352),
              size=wx.Size(100, 21), style=0, value='')        

        self.tc11_3 = wx.TextCtrl(id=-1,
              name='tc11_3', parent=self, pos=wx.Point(456, 352),
              size=wx.Size(100, 21), style=0, value='')
        
        self.tc11_4 = wx.TextCtrl(id=-1,
              name='tc11_4', parent=self, pos=wx.Point(560, 352),
              size=wx.Size(100, 21), style=0, value='')




        self.tc12_1 = wx.TextCtrl(id=-1,
              name='tc12_1', parent=self, pos=wx.Point(248, 376),
              size=wx.Size(100, 21), style=0, value='')

        self.tc12_2 = wx.TextCtrl(id=-1,
              name='tc12_2', parent=self, pos=wx.Point(352, 376),
              size=wx.Size(100, 21), style=0, value='')

        self.tc12_3 = wx.TextCtrl(id=-1,
              name='tc12_3', parent=self, pos=wx.Point(456, 376),
              size=wx.Size(100, 21), style=0, value='')

        self.tc12_4 = wx.TextCtrl(id=-1,
              name='tc12_4', parent=self, pos=wx.Point(560, 376),
              size=wx.Size(100, 21), style=0, value='')





        self.tc13_1 = wx.TextCtrl(id=-1,
              name='tc13_1', parent=self, pos=wx.Point(248, 400),
              size=wx.Size(100, 21), style=0, value='')

        self.tc13_2 = wx.TextCtrl(id=-1,
              name='tc13_2', parent=self, pos=wx.Point(352, 400),
              size=wx.Size(100, 21), style=0, value='')

        self.tc13_3 = wx.TextCtrl(id=-1,
              name='tc13_3', parent=self, pos=wx.Point(456, 400),
              size=wx.Size(100, 21), style=0, value='')

        self.tc13_4 = wx.TextCtrl(id=-1,
              name='tc13_4', parent=self, pos=wx.Point(560, 400),
              size=wx.Size(100, 21), style=0, value='')




        self.tc14_1 = wx.TextCtrl(id=-1,
              name='tc14_1', parent=self, pos=wx.Point(248, 424),
              size=wx.Size(100, 21), style=0, value='')

        self.tc14_2 = wx.TextCtrl(id=-1,
              name='tc14_2', parent=self, pos=wx.Point(352, 424),
              size=wx.Size(100, 21), style=0, value='')

        self.tc14_3 = wx.TextCtrl(id=-1,
              name='tc14_3', parent=self, pos=wx.Point(456, 424),
              size=wx.Size(100, 21), style=0, value='')        

        self.tc14_4 = wx.TextCtrl(id=-1,
              name='tc14_4', parent=self, pos=wx.Point(560, 424),
              size=wx.Size(100, 21), style=0, value='')



        self.st6 = wx.StaticText(id=-1, label=self.PList["1028"][1] + ' ' + self.PList["1028"][2], name='st6', parent=self, pos=wx.Point(16, 496), style=0)

        self.checkBox6 = wx.CheckBox(id=-1,
              label='', name='checkBox6', parent=self,
              pos=wx.Point(24, 512), size=wx.Size(16, 13), style=0)
        self.checkBox6.SetValue(False)

        self.st7 = wx.StaticText(id=-1, label=self.PList["1029"][1] + ' ' + self.PList["1029"][2], name='st7', parent=self, pos=wx.Point(16, 536), style=0)

        self.checkBox7 = wx.CheckBox(id=-1,
              label='', name='checkBox7', parent=self,
              pos=wx.Point(24, 552), size=wx.Size(16, 13), style=0)
        self.checkBox7.SetValue(False)



#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		

    def OnButtonStoreData(self, event):
        if self.main.activeQid <> 0 and \
		len(Status.DB.questionnaire.Questionnaire_ID[self.main.activeQid]) == 1:            
            tmp = {
                "InflationRate":self.check(self.tc1.GetValue()),
                "FuelPriceRate":self.check(self.tc2.GetValue()),
                "InterestExtFinancing":self.check(self.tc3.GetValue()),
                "PercentExtFinancing":self.check(self.tc4.GetValue()),
                "AmortisationTime":self.check(self.tc5.GetValue()),
                "OMGenTot":self.check(self.tc10_1.GetValue()),
                "OMGenOP":self.check(self.tc10_2.GetValue()),
                "OMGenEP":self.check(self.tc10_3.GetValue()),
                "OMGenFung":self.check(self.tc10_4.GetValue()),
                "OMBuildTot":self.check(self.tc11_1.GetValue()),
                "OMBuildOP":self.check(self.tc11_2.GetValue()),
                "OMBuildEP":self.check(self.tc11_3.GetValue()),
                "OMBiuildFung":self.check(self.tc11_4.GetValue()),
                "OMMachEquipTot":self.check(self.tc12_1.GetValue()),
                "OMMachEquipOP":self.check(self.tc12_2.GetValue()),
                "OMMachEquipEP":self.check(self.tc12_3.GetValue()),
                "OMMachEquipFung":self.check(self.tc12_4.GetValue()),
                "OMHCGenDistTot":self.check(self.tc13_1.GetValue()),
                "OMHCGenDistOP":self.check(self.tc13_2.GetValue()),
                "OMHCGenDistEP":self.check(self.tc13_3.GetValue()),
                "OMHCGenDistFung":self.check(self.tc13_4.GetValue()),
                "OMTotalTot":self.check(self.tc14_1.GetValue()),
                "OMTotalOP":self.check(self.tc14_2.GetValue()),
                "OMTotalEP":self.check(self.tc14_3.GetValue()),
                "OMTotalFung":self.check(self.tc14_4.GetValue())               
                  }                
              
            q = Status.DB.questionnaire.Questionnaire_ID[self.main.activeQid][0]
            q.update(tmp)
            Status.SQL.commit()


#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		

    def clear(self):
        self.checkBox6.SetValue(False)
        self.checkBox7.SetValue(False)
        self.tc1.SetValue('')
        self.tc2.SetValue('')
        self.tc3.SetValue('')
        self.tc4.SetValue('')
        self.tc5.SetValue('')
        self.tc10_1.SetValue('')
        self.tc10_2.SetValue('')
        self.tc10_3.SetValue('')
        self.tc10_4.SetValue('')
        self.tc11_1.SetValue('')
        self.tc11_2.SetValue('')
        self.tc11_3.SetValue('')
        self.tc11_4.SetValue('')
        self.tc12_1.SetValue('')
        self.tc12_2.SetValue('')
        self.tc12_3.SetValue('')
        self.tc12_4.SetValue('')
        self.tc13_1.SetValue('')
        self.tc13_2.SetValue('')
        self.tc13_3.SetValue('')
        self.tc13_4.SetValue('')
        self.tc14_1.SetValue('')
        self.tc14_2.SetValue('')
        self.tc14_3.SetValue('')
        self.tc14_4.SetValue('')
        

    def fillPage(self):
	if self.main.activeQid == 0:
	    return

	q = Status.DB.questionnaire.Questionnaire_ID[self.main.activeQid][0]
	self.tc1.SetValue(str(q.InflationRate))
	self.tc2.SetValue(str(q.FuelPriceRate))
	self.tc3.SetValue(str(q.InterestExtFinancing))
	self.tc4.SetValue(str(q.PercentExtFinancing))
	self.tc5.SetValue(str(q.AmortisationTime))
	self.tc10_1.SetValue(str(q.OMGenTot))
	self.tc10_2.SetValue(str(q.OMGenOP))
	self.tc10_3.SetValue(str(q.OMGenEP))
	self.tc10_4.SetValue(str(q.OMGenFung))
	self.tc11_1.SetValue(str(q.OMBuildTot))
	self.tc11_2.SetValue(str(q.OMBuildOP))
	self.tc11_3.SetValue(str(q.OMBuildEP))
	self.tc11_4.SetValue(str(q.OMBiuildFung))
	self.tc12_1.SetValue(str(q.OMMachEquipTot))
	self.tc12_2.SetValue(str(q.OMMachEquipOP))
	self.tc12_3.SetValue(str(q.OMMachEquipEP))
	self.tc12_4.SetValue(str(q.OMMachEquipFung))
	self.tc13_1.SetValue(str(q.OMHCGenDistTot))
	self.tc13_2.SetValue(str(q.OMHCGenDistOP))
	self.tc13_3.SetValue(str(q.OMHCGenDistEP))
	self.tc13_4.SetValue(str(q.OMHCGenDistFung))
	self.tc14_1.SetValue(str(q.OMTotalTot))
	self.tc14_2.SetValue(str(q.OMTotalOP))
	self.tc14_3.SetValue(str(q.OMTotalEP))
	self.tc14_4.SetValue(str(q.OMTotalFung))
            
	if q.EnergyManagExisting is None:
	    self.checkBox6.SetValue(False)
	else:
	    self.checkBox6.SetValue(bool(q.EnergyManagExisting))

	if q.EnergyManagExternal is None:
	    self.checkBox7.SetValue(False)
	else:
	    self.checkBox7.SetValue(bool(q.EnergyManagExternal))



