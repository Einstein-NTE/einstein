import wx
import pSQL
import HelperClass
from status import Status


class PanelQ7(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Panel.__init__(self, id=-1, name='PanelQ7', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)


        self.buttonStoreData = wx.Button(id=-1,
					 label=self.PList["X019"][1],
					 name='buttonStoreData',
					 parent=self,
					 pos=wx.Point(640, 472),
					 size=wx.Size(192, 32),
					 style=0)
        self.Bind(wx.EVT_BUTTON, self.OnButtonStoreData, self.buttonStoreData)
        

        self.stInfo1 = wx.StaticText(id=-1,
				     label=self.PList["0901"][1],
				     name='stInfo1',
				     parent=self,
				     pos=wx.Point(16, 24),
				     style=0)
        self.stInfo1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo2 = wx.StaticText(id=-1,
				     label=self.PList["X066"][1],
				     name='stInfo2',
				     parent=self,
				     pos=wx.Point(16, 128),
				     style=0)
        self.stInfo2.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo3 = wx.StaticText(id=-1,
				     label=self.PList["X067"][1],
				     name='stInfo3',
				     parent=self,
				     pos=wx.Point(72, 152),
				     style=0)
        self.stInfo3.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo4 = wx.StaticText(id=-1,
				     label=self.PList["X068"][1],
				     name='stInfo4',
				     parent=self,
				     pos=wx.Point(192, 152),
				     style=0)
        self.stInfo4.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo5 = wx.StaticText(id=-1,
				     label=self.PList["X069"][1],
				     name='stInfo5',
				     parent=self,
				     pos=wx.Point(360, 128),
				     style=0)
        self.stInfo5.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo6 = wx.StaticText(id=-1,
				     label=self.PList["X070"][1],
				     name='stInfo6',
				     parent=self,
				     pos=wx.Point(360, 152),
				     size=wx.Size(128, 26),
				     style=0)
        self.stInfo6.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.stInfo7 = wx.StaticText(id=-1,
				     label=self.PList["X071"][1],
				     name='stInfo7',
				     parent=self,
				     pos=wx.Point(576, 152),
				     size=wx.Size(128, 26),
				     style=0)
        self.stInfo7.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))


        self.st1 = wx.StaticText(id=-1,
				 label=self.PList["X072"][1],
				 name='st1',
				 parent=self,
				 pos=wx.Point(24, 48),
				 style=0)        

        self.checkBox1 = wx.CheckBox(id=-1,
				     label='',
				     name='checkBox1',
				     parent=self,
				     pos=wx.Point(24, 64),
				     size=wx.Size(24, 16),
				     style=0)
        self.checkBox1.SetValue(False)
        self.checkBox1.SetAutoLayout(True)
        

        self.st2 = wx.StaticText(id=-1,
				 label=self.PList["X073"][1],
				 name='st2',
				 parent=self,
				 pos=wx.Point(24, 80),
				 style=0)

        self.checkBox2 = wx.CheckBox(id=-1,
				     label='',
				     name='checkBox2',
				     parent=self,
				     pos=wx.Point(24, 96),
				     size=wx.Size(24, 16),
				     style=0)
        self.checkBox2.SetValue(False)
        self.checkBox2.SetAutoLayout(True)
        

        self.st3 = wx.StaticText(id=-1,
				 label=self.PList["X074"][1],
				 name='st3',
				 parent=self,
				 pos=wx.Point(290, 48),
				 style=0)

        self.checkBox3 = wx.CheckBox(id=-1,
				     label='',
				     name='checkBox3',
				     parent=self,
				     pos=wx.Point(290, 64),
				     size=wx.Size(24, 16),
				     style=0)
        self.checkBox3.SetValue(False)
        self.checkBox3.SetAutoLayout(True)


        self.st4 = wx.StaticText(id=-1,
				 label=self.PList["X075"][1],
				 name='st4',
				 parent=self,
				 pos=wx.Point(290, 80),
				 style=0)
	
        self.checkBox4 = wx.CheckBox(id=-1,
				     label='',
				     name='checkBox4',
				     parent=self,
				     pos=wx.Point(290, 96),
				     size=wx.Size(24, 16),
				     style=0)
        self.checkBox4.SetValue(False)
        self.checkBox4.SetAutoLayout(True)

        
        self.st5 = wx.StaticText(id=-1,
				 label=self.PList["X076"][1],
				 name='st5',
				 parent=self,
				 pos=wx.Point(608, 48),
				 style=0)

        self.tc1 = wx.TextCtrl(id=-1,
			       name='tc1',
			       parent=self,
			       pos=wx.Point(608, 64),
			       size=wx.Size(168, 48),
			       style=wx.TE_MULTILINE,
			       value='')


        self.st6 = wx.StaticText(id=-1,
				 label=self.PList["X077"][1] + " " + self.PList["X077"][2],
				 name='st6',
				 parent=self,
				 pos=wx.Point(16, 168),
				 style=0)

        self.st7 = wx.StaticText(id=-1,
				 label=self.PList["X078"][1] + " " + self.PList["X078"][2],
				 name='st7',
				 parent=self,
				 pos=wx.Point(16, 208),
				 style=0)

        self.st8 = wx.StaticText(id=-1,
				 label=self.PList["X079"][1] + " " + self.PList["X079"][2],
				 name='st8',
				 parent=self,
				 pos=wx.Point(16, 248),
				 style=0)

        self.st9 = wx.StaticText(id=-1,
				 label=self.PList["X080"][1] + " " + self.PList["X080"][2],
				 name='st9',
				 parent=self,
				 pos=wx.Point(16, 288),
				 style=0)

        self.st10 = wx.StaticText(id=-1,
				  label=self.PList["X081"][1] + " " + self.PList["X081"][2],
				  name='st10',
				  parent=self,
				  pos=wx.Point(16, 328),
				  style=0)

        self.st11 = wx.StaticText(id=-1,
				  label=self.PList["0914"][1] + " " + self.PList["0914"][2],
				  name='st11',
				  parent=self,
				  pos=wx.Point(16, 368),
				  style=0)

        self.st12 = wx.StaticText(id=-1,
				  label=self.PList["0915"][1] + " " + self.PList["0915"][2],
				  name='st12',
				  parent=self,
				  pos=wx.Point(16, 408),
				  style=0)


        self.st13 = wx.StaticText(id=-1,
				  label=self.PList["0916"][1] + " " + self.PList["0916"][2],
				  name='st13',
				  parent=self,
				  pos=wx.Point(16, 456),
				  style=0)

        self.checkBox5 = wx.CheckBox(id=-1,
				     label='',
				     name='checkBox5',
				     parent=self,
				     pos=wx.Point(16, 472),
				     size=wx.Size(16, 13),
				     style=0)
        self.checkBox5.SetValue(False)

        
        self.st14 = wx.StaticText(id=-1,
				  label=self.PList["0921"][1] + " " + self.PList["0921"][2],
				  name='st14',
				  parent=self,
				  pos=wx.Point(360, 192),
				  style=0)

        self.st15 = wx.StaticText(id=-1,
				  label=self.PList["X082"][1] + " " + self.PList["X082"][2],
				  name='st15',
				  parent=self,
				  pos=wx.Point(360, 232),
				  style=0)

        self.st16 = wx.StaticText(id=-1,
				  label=self.PList["0924"][1] + " " + self.PList["0924"][2],
				  name='st16',
				  parent=self,
				  pos=wx.Point(360, 272),
				  style=0)

        self.st17 = wx.StaticText(id=-1,
				  label=self.PList["0925"][1] + " " + self.PList["0925"][2],
				  name='st17',
				  parent=self,
				  pos=wx.Point(360, 312),
				  style=0)

        self.st18 = wx.StaticText(id=-1,
				  label=self.PList["0926"][1] + " " + self.PList["0926"][2],
				  name='st18',
				  parent=self,
				  pos=wx.Point(360, 352),
				  style=0)

        self.st19 = wx.StaticText(id=-1,
				  label=self.PList["0927"][1] + " " + self.PList["0927"][2],
				  name='st19',
				  parent=self,
				  pos=wx.Point(360, 392),
				  style=0)

        self.st20 = wx.StaticText(id=-1,
				  label=self.PList["0928"][1] + " " + self.PList["0928"][2],
				  name='st20',
				  parent=self,
				  pos=wx.Point(360, 432),
				  style=0)

        self.st21 = wx.StaticText(id=-1,
				  label=self.PList["0929"][1] + " " + self.PList["0929"][2],
				  name='st21',
				  parent=self,
				  pos=wx.Point(576, 192),
				  style=0)

        self.st22 = wx.StaticText(id=-1,
				  label=self.PList["0930"][1] + " " + self.PList["0930"][2],
				  name='st22',
				  parent=self,
				  pos=wx.Point(576, 232),
				  style=0)
        
        self.st23 = wx.StaticText(id=-1,
				  label=self.PList["X083"][1] + " " + self.PList["X083"][2],
				  name='st23',
				  parent=self,
				  pos=wx.Point(576, 272),
				  style=0)

        self.st24 = wx.StaticText(id=-1,
				  label=self.PList["0933"][1] + " " + self.PList["0933"][2],
				  name='st24',
				  parent=self,
				  pos=wx.Point(576, 312),
				  style=0)


        self.tc6_1 = wx.TextCtrl(id=-1,
				 name='tc6_1',
				 parent=self,
				 pos=wx.Point(16, 184),
				 size=wx.Size(128, 21),
				 style=0,
				 value='')

        self.tc6_2 = wx.TextCtrl(id=-1,
				 name='tc6_2',
				 parent=self,
				 pos=wx.Point(152, 184),
				 size=wx.Size(128, 21),
				 style=0,
				 value='')

        self.tc7_1 = wx.TextCtrl(id=-1,
				 name='tc7_1',
				 parent=self,
				 pos=wx.Point(16, 224),
				 size=wx.Size(128, 21),
				 style=0,
				 value='')
        
        self.tc7_2 = wx.TextCtrl(id=-1,
				 name='tc7_2',
				 parent=self,
				 pos=wx.Point(152, 224),
				 size=wx.Size(128, 21),
				 style=0,
				 value='')

        self.tc8_1 = wx.TextCtrl(id=-1,
				 name='tc8_1',
				 parent=self,
				 pos=wx.Point(16, 264),
				 size=wx.Size(128, 21),
				 style=0,
				 value='')

        self.tc8_2 = wx.TextCtrl(id=-1,
				 name='tc8_2',
				 parent=self,
				 pos=wx.Point(152, 264),
				 size=wx.Size(128, 21),
				 style=0,
				 value='')

        self.tc9_1 = wx.TextCtrl(id=-1,
				 name='tc9_1',
				 parent=self,
				 pos=wx.Point(16, 304),
				 size=wx.Size(128, 21),
				 style=0,
				 value='')

        self.tc9_2 = wx.TextCtrl(id=-1,
				 name='tc9_2',
				 parent=self,
				 pos=wx.Point(152, 304),
				 size=wx.Size(128, 21),
				 style=0,
				 value='')

        self.tc10_1 = wx.TextCtrl(id=-1,
				  name='tc10_1',
				  parent=self,
				  pos=wx.Point(16, 344),
				  size=wx.Size(128, 21),
				  style=0,
				  value='')

        self.tc10_2 = wx.TextCtrl(id=-1,
				  name='tc10_2',
				  parent=self,
				  pos=wx.Point(152, 344),
				  size=wx.Size(128, 21),
				  style=0,
				  value='')
	
        self.tc11 = wx.TextCtrl(id=-1,
				name='tc11',
				parent=self,
				pos=wx.Point(16,384),
				size=wx.Size(128, 21),
				style=0,
				value='')

        self.tc12 = wx.TextCtrl(id=-1,
				name='tc12',
				parent=self,
				pos=wx.Point(16, 424),
				size=wx.Size(128, 21),
				style=0,
				value='')


        self.tc14 = wx.TextCtrl(id=-1,
				name='tc14',
				
				parent=self,
				pos=wx.Point(360, 208),
				size=wx.Size(150, 21),
				style=0,
				value='')


        self.tc15_1 = wx.TextCtrl(id=-1,
				  name='tc15_1',
				  parent=self,
				  pos=wx.Point(360, 248),
				  size=wx.Size(72, 21),
				  style=0,
				  value='')

        self.tc15_2 = wx.TextCtrl(id=-1,
				  name='tc15_2',
				  parent=self,
				  pos=wx.Point(438, 248),
				  size=wx.Size(72, 21),
				  style=0,
				  value='')


        self.tc16 = wx.TextCtrl(id=-1,
				name='tc16',
				parent=self,
				pos=wx.Point(360, 288),
				size=wx.Size(150, 21),
				style=0,
				value='')


        self.tc17 = wx.TextCtrl(id=-1,
				name='tc17',
				parent=self,
				pos=wx.Point(360, 328),
				size=wx.Size(150, 21),
				style=0,
				value='')


        self.tc18 = wx.TextCtrl(id=-1,
				name='tc18',
				parent=self,
				pos=wx.Point(360, 368),
				size=wx.Size(150, 21),
				style=0,
				value='')


        self.tc19 = wx.TextCtrl(id=-1,
				name='tc19',
				parent=self,
				pos=wx.Point(360, 408),
				size=wx.Size(150, 21),
				style=0,
				value='')


        self.tc20 = wx.TextCtrl(id=-1,
				name='tc20',
				parent=self,
				pos=wx.Point(360, 448),
				size=wx.Size(150, 21),
				style=0,
				value='')


        self.tc21 = wx.TextCtrl(id=-1,
				name='tc21',
				parent=self,
				pos=wx.Point(576, 208),
				size=wx.Size(150, 21),
				style=0,
				value='')


        self.tc22 = wx.TextCtrl(id=-1,
				name='tc22',
				parent=self,
				pos=wx.Point(576, 248),
				size=wx.Size(150, 21),
				style=0,
				value='')


        self.tc23_1 = wx.TextCtrl(id=-1,
				  name='tc23_1',
				  parent=self,
				  pos=wx.Point(576, 288),
				  size=wx.Size(72, 21),
				  style=0,
				  value='')

        self.tc23_2 = wx.TextCtrl(id=-1,
				  name='tc23_2',
				  parent=self,
				  pos=wx.Point(656, 288),
				  size=wx.Size(72, 21),
				  style=0,
				  value='')


        self.tc24 = wx.TextCtrl(id=-1,
				name='tc24',
				parent=self,
				pos=wx.Point(576, 328),
				size=wx.Size(150, 21),
				style=0,
				value='')


#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		

    def OnButtonStoreData(self, event):
        
        if Status.PId == 0:
	    return


	tmp = {
	    "SurfAreaRoof":self.check(self.tc6_1.GetValue()), 
	    "SurfAreaGround":self.check(self.tc6_2.GetValue()), 	
	    "InclinationRoof":self.check(self.tc7_1.GetValue()), 
	    "InclinationGround":self.check(self.tc7_2.GetValue()), 
	    "OrientationRoof":self.check(self.tc8_1.GetValue()), 
	    "OrientationGround":self.check(self.tc8_2.GetValue()), 
	    "ShadingRoof":self.check(self.tc9_1.GetValue()), 
	    "ShadingGround":self.check(self.tc9_2.GetValue()), 
	    "DistanceToRoof":self.check(self.tc10_1.GetValue()), 
	    "DistanceToGround":self.check(self.tc10_2.GetValue()), 
	    "RoofType":self.check(self.tc11.GetValue()), 
	    "RoofStaticLoadCap":self.check(self.tc12.GetValue()),	
	    "BiomassFromProc":self.check(self.tc14.GetValue()), 
	    "PeriodBiomassProcStart":self.check(self.tc15_1.GetValue()), 
	    "PeriodBiomassProcStop":self.check(self.tc15_2.GetValue()), 
	    "NDaysBiomassProc":self.check(self.tc16.GetValue()), 
	    "QBiomassProcDay":self.check(self.tc17.GetValue()), 
	    "SpaceBiomassProc":self.check(self.tc18.GetValue()), 
	    "LCVBiomassProc":self.check(self.tc19.GetValue()), 
	    "HumidBiomassProc":self.check(self.tc20.GetValue()), 	
	    "BiomassFromRegion":self.check(self.tc21.GetValue()), 
	    "PriceBiomassRegion":self.check(self.tc22.GetValue()), 
	    "PeriodBiomassRegionStart":self.check(self.tc23_1.GetValue()), 
	    "PeriodBiomassRegionStop":self.check(self.tc23_2.GetValue()), 
	    "NDaysBiomassRegion":self.check(self.tc24.GetValue())
	    }                

	if len(Status.DB.qrenewables.Questionnaire_id[Status.PId]) == 0:
	    # register does not exist, so store also id
	    tmp["Questionnaire_id"] = Status.PId
           
	    Status.DB.qrenewables.insert(tmp)
	    Status.SQL.commit()
       
	else:
	    # register does exist              
	    q = Status.DB.qrenewables.Questionnaire_id[Status.PId][0]
	    q.update(tmp)
	    Status.SQL.commit()
                          

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		


    def clear(self):
        self.checkBox1.SetValue(False)
        self.checkBox2.SetValue(False)
        self.checkBox3.SetValue(False)
        self.checkBox4.SetValue(False)
        self.checkBox5.SetValue(False)
        self.tc6_1.SetValue('')
        self.tc6_2.SetValue('')
        self.tc7_1.SetValue('')
        self.tc7_2.SetValue('')
        self.tc8_1.SetValue('')
        self.tc8_2.SetValue('')
        self.tc9_1.SetValue('')
        self.tc9_2.SetValue('')
        self.tc10_1.SetValue('')
        self.tc10_2.SetValue('')
        self.tc11.SetValue('')
        self.tc12.SetValue('')
        self.tc14.SetValue('')
        self.tc15_1.SetValue('')
        self.tc15_2.SetValue('')
        self.tc16.SetValue('')
        self.tc17.SetValue('')
        self.tc18.SetValue('')
        self.tc19.SetValue('')
        self.tc20.SetValue('')
        self.tc21.SetValue('')
        self.tc22.SetValue('')
        self.tc23_1.SetValue('')
        self.tc23_2.SetValue('')
        self.tc24.SetValue('')



    def fillPage(self):
	if Status.PId == 0:
	    return

	if len(Status.DB.qrenewables.Questionnaire_id[Status.PId]) > 0:
	    p = Status.DB.qrenewables.Questionnaire_id[Status.PId][0]
	    if p.REInterest is None:
		self.checkBox1.SetValue(False)
	    else:
		self.checkBox1.SetValue(bool(p.REInterest))

	    if p.EnclBuildGroundSketch is None:
		self.checkBox5.SetValue(False)
	    else:
		self.checkBox5.SetValue(bool(p.EnclBuildGroundSketch))
                
	    self.tc6_1.SetValue(str(p.SurfAreaRoof))
	    self.tc6_2.SetValue(str(p.SurfAreaGround))
	    self.tc7_1.SetValue(str(p.InclinationRoof))
	    self.tc7_2.SetValue(str(p.InclinationGround))
	    self.tc8_1.SetValue(str(p.OrientationRoof))
	    self.tc8_2.SetValue(str(p.OrientationGround))
	    self.tc9_1.SetValue(str(p.ShadingRoof))
	    self.tc9_2.SetValue(str(p.ShadingGround))
	    self.tc10_1.SetValue(str(p.DistanceToRoof))
	    self.tc10_2.SetValue(str(p.DistanceToGround))
	    self.tc11.SetValue(str(p.RoofType))
	    self.tc12.SetValue(str(p.RoofStaticLoadCap))                
	    self.tc14.SetValue(str(p.BiomassFromProc))
	    self.tc15_1.SetValue(str(p.PeriodBiomassProcStart))
	    self.tc15_2.SetValue(str(p.PeriodBiomassProcStop))
	    self.tc16.SetValue(str(p.NDaysBiomassProc))
	    self.tc17.SetValue(str(p.QBiomassProcDay))
	    self.tc18.SetValue(str(p.SpaceBiomassProc))
	    self.tc19.SetValue(str(p.LCVBiomassProc))
	    self.tc20.SetValue(str(p.HumidBiomassProc))
	    self.tc21.SetValue(str(p.BiomassFromRegion))
	    self.tc22.SetValue(str(p.PriceBiomassRegion))
	    self.tc23_1.SetValue(str(p.PeriodBiomassRegionStart))
	    self.tc23_2.SetValue(str(p.PeriodBiomassRegionStop))
	    self.tc24.SetValue(str(p.NDaysBiomassRegion))                


