# -*- coding: iso-8859-15 -*-
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
#	Version No.: 0.10
#	Created by: 	    Tom Sobota	April 2008
#       Revised by:         Hans Schweiger  13/04/2008
#                           Stoyan Danov    25/04/2008
#                           Hans Schweiger  25/04/2008
#                           Tom Sobota      04/05/2008
#                           Hans Schweiger  05/05/2008
#                           Tom Sobota      07/05/2008
#                           Hans Schweiger  07/05/2008
#                           Hans Schweiger  10/05/2008
#                           Stoyan Danov    06/06/2008
#                           Hans Schweiger  16/06/2008
#                           Stoyan Danov    17/06/2008
#
#       Changes to previous version:
#       13/04/08:       Additional inputs in init: selection
#       25/04/08:       line 50, change query, unnecessary large: there is a problem with eqId !!! (add HP manually)
#                   HS  Alternative proposal no. introduced ...
#       04/05/2008      Changed display logic
#       05/05/2008  HS  Event handlers changed.
#       07/05/2008  HS  Some security features added (Nones, ...)
#                       Function "display" was duplicated. one deleted
#       10/05/2008  HS  AddEquipmentDummy added
#       06/06/2008  SD  label/tooltip, new displayClasses
#       16/06/2008: HS  clean-up and adapt SQL-I/O to new label names/numbers
#       17/06/2008: SD  order the parameters as in paper Q4H, unitdict, OnButtonOK
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
from status import Status
from displayClasses import *
from GUITools import *  #HS2008-05-07 added
from units import *

### constants
##LABELWIDTH=150
TEXTENTRYWIDTH=160

# constants that control the default field sizes

HEIGHT         =  27
LABELWIDTH     = 180
DATAENTRYWIDTH = 100
UNITSWIDTH     =  90

class PanelQ4(wx.Panel):
    def __init__(self, parent, main, eqId,prefill=None):
        print "PanelQ4 (__init__)"
	self.parent = parent
	self.main = main
        self._init_ctrls(parent)
        self.__do_layout()
        self.equipeID = eqId

        print 'panelQ4 (__init__): eqId =', eqId, 'Status.PId =', Status.PId, 'Status.ANo =', Status.ANo
        if eqId is not None:
            equipe = Status.DB.qgenerationhc.QGenerationHC_ID[eqId][0]
            self.display(equipe)

        try:
            for key in prefill:
                if key=="EquipeType":
                    self.tc5.SetValue(prefill[key])
        except:
            pass


    def _init_ctrls(self, parent):
#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------

        wx.Panel.__init__(self, id=-1, name='PanelQ4', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(780, 580))
        self.Hide()

        # fillers for the gridsizer
        self.dummy1 = wx.StaticText(self,-1,'')
        self.dummy2 = wx.StaticText(self,-1,'')
        self.dummy3 = wx.StaticText(self,-1,'')

        self.sizer_4_staticbox = wx.StaticBox(self, -1, _("Equipment list"))
        self.sizer_4_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.sizer_5_staticbox = wx.StaticBox(self, -1,
                                              _("Descriptive data"))
        self.sizer_5_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_7_staticbox = wx.StaticBox(self, -1, _("Thechnical data"))
        self.sizer_7_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_8_staticbox = wx.StaticBox(self, -1, _("Schedule"))
        self.sizer_8_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.sizer_9_staticbox = wx.StaticBox(self, -1, _("Heat source / sink"))
        self.sizer_9_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

        self.listBoxEquipment = wx.ListBox(self,-1,choices=[])
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxEquipmentClick, self.listBoxEquipment)

        # izquierda
#In Descriptive data
        
        self.tc1 = TextEntry(self,maxchars=255,value='',
                             label=_("Short name of equipment"),
                             tip=_("Give some brief name of the equipments to identify them in the reports"))
        
        self.tc2 = TextEntry(self,maxchars=255,value='',
                             label=_("Manufacturer"),
                             tip=_("Attach the technical data if available"))
        
        self.tc3 = IntEntry(self,
                            minval=2000, maxval=2050, value=0,
                            label=_("Year of  manufacturing or/and installation?"),
                            tip=_("Year of manufacturing or installation"),
                            hasunits=False)

        self.tc4 = TextEntry(self,maxchars=255,value='',
                             label=_("Model"),
                             tip=_("Model according manufacturer nomenclature"))

        self.tc5 = ChoiceEntry(self,
                               values=TRANSEQUIPTYPE.values(),
                               label=_("Type of equipment"),
                               tip=_("e.g. boiler / burner / chiller / compressor / CHP motor"))

        self.tc6 = IntEntry(self,
                            minval=0, maxval=100, value=0,
                            label=_("Number of units of the same type"),
                            tip=_("Specify how many units of this type exist"),
                            hasunits=False)
#In Technical data

        self.tc7 = FloatEntry(self,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict='POWER',
                              label=_("Nominal power (heat or cold, output)"),
                              tip=_("Power at manufacturer nominal conditions"))

        self.tc8 = ChoiceEntry(self,
                               values=[],
                               label=_("Fuel type"),
                               tip=_("Select fuel type from predefined list"))

        self.tc9 = FloatEntry(self,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict='MASSORVOLUME',
                              label=_("Fuel consumption (nominal)"),
                              tip=_("Specify the units below"))

        self.tc12 = FloatEntry(self,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict='POWER',
                              label=_("Electrical power input"),
                              tip=_("Electrical power, incl. auxiliary components, such as water pumps, control,..."))

        self.tc13 = FloatEntry(self,
                              ipart=1, decimals=3, minval=0., maxval=1., value=0.,
                              label=_("Mean overall thermal conversion efficiency"),
                              tip=_("Specify the efficiency of boiler or EER(COP) for cold generation"))

        self.tc17 = FloatEntry(self,
                              ipart=1, decimals=3, minval=0., maxval=1., value=0.,
                              label=_("Mean utilisation factor (full capacity = 100%)"),
                              tip=_("Specify the mean supplied power of the boiler/cooler/etc. with respect to its nominal power"))


        self.tc16 = FloatEntry(self,
                              ipart=4, decimals=1, minval=0., maxval=9999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_("Temperature of exhaust gas at standard operation conditions (boilers only)"),
                              tip=_("Only for boilers and CHP"))

        self.tc16_2 = FloatEntry(self,
                              ipart=2, decimals=2, minval=0., maxval=99.99, value=0.,
                              label=_("Excess air ratio (boilers only)"),
                              tip=_("Only for boilers and CHP"))

        self.tc15 = FloatEntry(self,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict='POWER',
                              label=_("Electricity production (CHP only)"),
                              tip=_("Only for CHP"))

        self.tc14 = FloatEntry(self,
                              ipart=1, decimals=3, minval=0., maxval=1., value=0.,
                              label=_("Electrical conversion efficiency (CHP only)"),
                              tip=_("Only for CHP"))
#next from Q4C
        self.tc102 = ChoiceEntry(self,
                               values=[],
                               label=_("Refrigerant (HP or Chiller only)"),
                               tip=_("Refrigerant or working fluid (HP or Chiller only)"))

        # derecha
#In Heat source / sink
        self.tc20 = ChoiceEntry(self,
                             values = [],
                             multiple = True,
                             label=_("Heat or cold supplyed to the distribution line / branch (piping or duct) no."),
                             tip=_("Specify the tube for supply to the equipment, using the nomenclature of the block ''distribution system''"))
        #
        self.tc30 = ChoiceEntry(self,
                               values=[],
                               label=_("Low temperature heat source"),
                               tip=_("If waste heat is used, indicate the process or equipment from which waste heat originates"))


        self.tc31 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_("Temperature of low temp. heat source"),
                              tip=_("Temperature of the medium entering the evaporator"))


        self.tc34 = FloatEntry(self,
                              ipart=6, decimals=1, minval=0., maxval=999999., value=0.,
                              unitdict='POWER',
                              label=_("Thermal power input high temp. (thermal HP and chillers only)"),
                              tip=_("Power applied to the generator of a thermal heat pump or chiller"))


        self.tc33 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_("Driving temperature (thermal HP and chillers only)"),
                              tip=_("Temperature of heat supply fluid entering the generator"))


        self.tc32 = ChoiceEntry(self,
                               values=[],
                               label=_("High temperature heat source (thermal HP and chillers only)"),
                               tip=_("Indicate if the circuit of the heat supply to generator is closed or opened (waste heat released to ambient)"))

#next 2 from Q4C
        self.tc35 = ChoiceEntry(self,
                               values=[],
                               label=_("Destination of waste heat (chillers only)"),
                               tip=_("If applies, specify heat exchanger where waste heat is used"))

        self.tc36 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=999., value=0.,
                              unitdict='TEMPERATURE',
                              label=_("Temperature of re-cooling (chillers only)"),
                              tip=_("Outlet temperature of cooling water or hot air stream"))

#In Schedule

        self.tc18 = FloatEntry(self,
                              ipart=2, decimals=1, minval=0., maxval=24., value=0.,
                              label=_("Hours of operation per day"),
                              tip=_("Specify representative mean values"))

        self.tc19 = FloatEntry(self,
                              ipart=3, decimals=1, minval=0., maxval=365., value=0.,
                              label=_("Days of operation per year"),
                              tip=_("Specify representative mean values"))


        self.buttonDeleteEquipment = wx.Button(self,-1,label=_("Delete equipment"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteEquipment, self.buttonDeleteEquipment)

        self.buttonAddEquipment = wx.Button(self,-1,label=_("Add equipment"))
        self.Bind(wx.EVT_BUTTON,self.OnButtonAddEquipment, self.buttonAddEquipment)

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL, label='Cancel')
        #self.buttonCancel.SetMinSize((125, 32))
        #self.buttonCancel.SetMaxSize((125, 32))
        self.Bind(wx.EVT_BUTTON,self.OnButtonCancel, self.buttonCancel)

        self.buttonOK = wx.Button(self,wx.ID_OK, label='OK')
        #self.buttonOK.SetMinSize((125, 32))
        #self.buttonOK.SetMaxSize((125, 32))
        self.Bind(wx.EVT_BUTTON,self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()


    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.FlexGridSizer(14, 2, 10, 10) #r,c,vsep,hsep
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.VERTICAL)
        sizer_4.Add(self.listBoxEquipment, 1, wx.EXPAND, 0)
        sizer_4.Add(self.buttonDeleteEquipment, 0, wx.EXPAND, 0)
        sizer_4.Add(self.buttonAddEquipment, 0, wx.EXPAND, 2)
        sizer_3.Add(sizer_4, 1, wx.EXPAND, 0)

        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)
        sizer_5.Add(grid_sizer_1, 1, wx.EXPAND, 0)


        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL
        flagText = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL
        grid_sizer_1.Add(self.tc1, 0, flagText, 0)
        grid_sizer_1.Add(self.dummy1, 0, wx.EXPAND, 0)
#        grid_sizer_1.Add(self.tc11, 0, flagText, 0)
        grid_sizer_1.Add(self.tc2, 0, flagText, 0)
        grid_sizer_1.Add(self.tc12, 0, flagText, 0)
        grid_sizer_1.Add(self.tc3, 0, flagText, 0)
        grid_sizer_1.Add(self.tc13, 0, flagText, 0)
        grid_sizer_1.Add(self.tc4, 0, flagText, 0)
        grid_sizer_1.Add(self.tc14, 0, flagText, 0)
        grid_sizer_1.Add(self.tc5, 0, flagText, 0)
        grid_sizer_1.Add(self.tc15, 0, flagText, 0)
        grid_sizer_1.Add(self.tc6, 0, flagText, 0)
        grid_sizer_1.Add(self.tc16, 0, flagText, 0)
        grid_sizer_1.Add(self.tc7, 0, flagText, 0)
        grid_sizer_1.Add(self.tc17, 0, flagText, 0)
        grid_sizer_1.Add(self.tc8, 0, flagText, 0)
        grid_sizer_1.Add(self.tc18, 0, flagText, 0)
        grid_sizer_1.Add(self.tc9, 0, flagText, 0)
        grid_sizer_1.Add(self.tc19, 0, flagText, 0)
#        grid_sizer_1.Add(self.tc10, 0, flagText, 0)
        grid_sizer_1.Add(self.tc20, 0, flagText, 0)
        grid_sizer_1.Add(self.dummy2, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.tc30, 0, flagText, 0)
        grid_sizer_1.Add(self.tc31, 0, flagText, 0)
        grid_sizer_1.Add(self.tc32, 0, flagText, 0)
        grid_sizer_1.Add(self.tc33, 0, flagText, 0)
        grid_sizer_1.Add(self.tc34, 0, flagText, 0)
        grid_sizer_1.Add(self.tc35, 0, flagText, 0)
        grid_sizer_1.Add(self.tc36, 0, flagText, 0)
            
        sizerOKCancel.Add(self.buttonCancel, 0, wx.ALL|wx.EXPAND, 2)
        sizerOKCancel.Add(self.buttonOK, 0, wx.ALL|wx.EXPAND, 2)
        sizer_3.Add(sizer_5, 4, wx.LEFT|wx.RIGHT|wx.EXPAND, 0)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_1.Add(sizerOKCancel, 0, wx.TOP|wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer_1)
        self.Layout()

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------

    def OnListBoxEquipmentClick(self, event):
        equipe = Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo].Equipment[\
	    str(self.listBoxEquipment.GetStringSelection())][0]
        self.equipeID = equipe.QGenerationHC_ID
        self.display(equipe)
        event.Skip()

    def OnButtonDeleteEquipment(self, event):
        Status.prj.deleteEquipment(self.equipeID)
        self.clear()
        self.fillPage()

#------------------------------------------------------------------------------
    def OnButtonAddEquipment(self, event):
#------------------------------------------------------------------------------
#   Adds an equipment depending on the equipment name given
#------------------------------------------------------------------------------

        self.clear()

    def OnButtonCancel(self, event):
        self.clear()


    def OnButtonOK(self, event):

        if Status.PId == 0:
	    return
        equipeName = check(self.tc1.GetValue())
        equipments = Status.DB.qgenerationhc.Equipment[equipeName].\
                     Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]

	if equipeName != 'NULL' and len(equipments) == 0:
            equipe = Status.prj.addEquipmentDummy()
        elif equipeName != 'NULL' and len(equipments) == 1:
            equipe = equipments[0]
        else:
	    print "PanelQ4 (ButtonOK) Equipment name has to be a unique value!"
	    return

        fuelDict = Status.prj.getFuelDict()
        fluidDict = Status.prj.getFluidDict()
        pipeDict = Status.prj.getPipeDict()

        tmp = {
            "Equipment":check(self.tc1.GetValue()),
            "Manufact":check(self.tc2.GetValue()),
            "YearManufact":check(self.tc3.GetValue()),
            "Model":check(self.tc4.GetValue()),
            "EquipType":check(findKey(TRANSEQUIPTYPES,self.tc5.GetValue(text=True))), 
            "NumEquipUnits":check(self.tc6.GetValue()),
            "HCGPnom":check(self.tc7.GetValue()),
            "DBFuel_id":check(findKey(fuelDict,self.tc8.GetValue(text=True))),
            "FuelConsum":check(self.tc9.GetValue()),
            "ElectriConsum":check(self.tc12.GetValue()),
            "HCGTEfficiency":check(self.tc13.GetValue()),
            "PartLoad":check(self.tc17.GetValue()),            
            "TExhaustGas":check(self.tc16.GetValue()),
            "ExcessAirRatio":check(self.tc16_2.GetValue()),
            "ElectriProduction":check(self.tc15.GetValue()),
            "HCGEEfficiency":check(self.tc14.GetValue()),
            "PipeDuctEquip":self.getPipeIDString(self.tc20.GetValue()),
            "HeatSourceLT":check(self.tc30.GetValue(text=True)),
            "THeatSourceLT":check(self.tc31.GetValue()),
            "ThermalConsum":check(self.tc34.GetValue()),
            "THeatSourceHT":check(self.tc33.GetValue()),
            "HeatSourceHT":check(findKey(pipeDict,self.tc32.GetValue(text=True))),
            "Refrigerant":self.getPipeIDString(),
            "DestinationWasteHeat":check(self.tc35.GetValue(text=True)),
            "TemperatureReCooling":check(self.tc36.GetValue()),
            "HPerDayEq":check(self.tc18.GetValue()),
            "NDaysEq":check(self.tc19.GetValue()),  
            }

        equipe.update(tmp)
        Status.SQL.commit()
        self.fillEquipmentList()

        print "PanelQ4 (add button): equipment type = ",self.tc5.GetValue()
        self.parent.equipeType = check(self.tc5.GetValue())

#HS2008-05-07: event.Skip() added. needed for leaving the dialog
        event.Skip()



#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------

#HS2004-04-13 function display extracted from event handler

    def display(self,q=None):
        self.fillChoiceOfDBFuel()
        self.fillChoiceOfFluid()
        self.fillChoiceOfPipe()
        self.fillChoiceOfLTSource()
        self.fillChoiceOfLTSink()
        self.fillChoiceOfHTSource()
        self.clear()
        self.fillPage()

        pipeDict = Status.prj.getPipeDict()
        fuelDict = Status.prj.getFuelDict()
        
        if q is not None:
            self.tc1.SetValue(str(q.Equipment))
            self.tc2.SetValue(str(q.Manufact))
            self.tc3.SetValue(str(q.YearManufact))
            self.tc4.SetValue(str(q.Model))
            self.tc5.SetValue(str(q.EquipType))
            self.tc6.SetValue(str(q.NumEquipUnits))
            self.tc7.SetValue(str(q.HCGPnom))

            if q.DBFuel_id in fuelDict.keys():
                self.tc8.SetValue(fuelDict[q.DBFuel_id])

            self.tc9.SetValue(str(q.FuelConsum))

            self.tc12.SetValue(str(q.ElectriConsum))
            self.tc13.SetValue(str(q.HCGTEfficiency))
            self.tc14.SetValue(str(q.HCGEEfficiency))
            self.tc15.SetValue(str(q.ElectriProduction))
            self.tc16.SetValue(str(q.TExhaustGas))
            self.tc16_2.SetValue(str(q.ExcessAirRatio))
            self.tc17.SetValue(str(q.PartLoad))
            self.tc18.SetValue(str(q.HPerDayEq))
            self.tc19.SetValue(str(q.NDaysEq))
            self.tc20.SetValue(self.getPipeNames(q.PipeDuctEquip))
            self.tc30.SetValue(str(q.HeatSourceLT))
            self.tc31.SetValue(str(q.THeatSourceLT))
            
            if q.HeatSourceHT in pipeDict.keys():
                self.tc32.SetValue(pipeDict[q.HeatSourceHT])
                
            self.tc33.SetValue(str(q.THeatSourceHT))
            self.tc34.SetValue(str(q.ThermalConsum))
    #        self.tc35.SetValue(str(q.))
    #        self.tc36.SetValue(str(q.))

        self.Show()

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

        self.tc12.SetValue('')
        self.tc13.SetValue('')
        self.tc14.SetValue('')
        self.tc15.SetValue('')
        self.tc16.SetValue('')
        self.tc17.SetValue('')
        self.tc18.SetValue('')
        self.tc19.SetValue('')
        self.tc20.SetValue('')
        
        self.tc30.SetValue('')
        self.tc31.SetValue('')
        self.tc32.SetValue('')
        self.tc33.SetValue('')
        self.tc34.SetValue('')
        self.tc35.SetValue('')
        self.tc36.SetValue('')

    def fillEquipmentList(self):
        self.listBoxEquipment.Clear()
        if len(Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]) > 0:
            for n in Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]:
                self.listBoxEquipment.Append (str(n.Equipment))

    def fillChoiceOfDBFuel(self):
        self.tc8.entry.Clear()
        for n in Status.DB.dbfuel.FuelName["%"]:
            self.tc8.entry.Append (n.FuelName)

    def fillChoiceOfFluid(self):
        fluidDict = Status.prj.getFluidDict()
        fluidNames = fluidDict.values()
        self.tc102.entry.Clear()
        for name in fluidNames:
            self.tc102.entry.Append(name)

    def fillChoiceOfPipe(self):
        pipeList = Status.prj.getPipeList("Pipeduct")
        self.tc20.entry.Clear()
        for pipe in pipeList:
            self.tc20.entry.Append(pipe)

    def fillChoiceOfLTSource(self):
        hxList = Status.prj.getHXList("HXName")
        self.tc30.entry.Clear()
        for src in TRANSAMBIENTSOURCE.values():
            self.tc30.entry.Append(src)
        for hx in hxList:
            self.tc30.entry.Append(hx)

    def fillChoiceOfHTSource(self):
        pipeList = Status.prj.getPipeList("Pipeduct")
        self.tc32.entry.Clear()
        for pipe in pipeList:
            self.tc32.entry.Append(pipe)

    def fillChoiceOfLTSink(self):
        hxList = Status.prj.getHXList("HXName")
        self.tc35.entry.Clear()
        for src in TRANSAMBIENTSINK.values():
            self.tc35.entry.Append(src)
        for hx in hxList:
            self.tc35.entry.Append(hx)

    def fillPage(self):
	if Status.PId != 0:
	    self.fillEquipmentList()

    def getPipeNames(self,IDString):
        print "PanelQ4 (getPipeNames): Getting pipenames from :",IDString
        pipeDict = Status.prj.getPipeDict()
        pipeIDsSQL = IDString.split(';')
        pipes = []
        for i in pipeIDsSQL:
            pipeID = int(i)
            if pipeID in pipeDict.keys():
                pipes.append(pipeDict[pipeID])
        print "PanelQ4: Names of pipes stored in SQL :",pipes
        return pipes
            
    def getPipeIDString(self,nameList):
        print "PanelQ4 (getPipeIDString): Getting pipeIDs from :",nameList
        pipeDict = Status.prj.getPipeDict()
        pipeIDs = []
        for name in nameList:
            pipeID = findKey(pipeDict,name)
            pipeIDs.append("%10d"%pipeID)
            
        IDString = ";".join(pipeIDs)
        print "PanelQ4: ID's of pipes stored in SQL :",IDString
        return IDString
            

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
