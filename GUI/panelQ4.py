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
#	Version No.: 0.05
#	Created by: 	    Tom Sobota	April 2008
#       Revised by:         Hans Schweiger  13/04/2008
#                           Stoyan Danov    25/04/2008
#                           Hans Schweiger  25/04/2008
#                           Tom Sobota      04/05/2008
#                           Hans Schweiger  05/05/2008
#
#       Changes to previous version:
#       13/04/08:       Additional inputs in init: selection
#       25/04/08:       line 50, change query, unnecessary large: there is a problem with eqId !!! (add HP manually)
#                   HS  Alternative proposal no. introduced ...
#       04/05/2008      Changed display logic
#       05/05/2008  HS  Event handlers changed.
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
from wx.lib.stattext import *
import pSQL
import HelperClass
from status import Status

# constants
LABELWIDTH=150
TEXTENTRYWIDTH=160


class Label(wx.lib.stattext.GenStaticText):
    # auxiliary class for labels (static text)
    # will show a short descriptive string and
    # generate a longer tooltip.
    # the tooltip is also associated to the text control
    #
    w0 = None
    w1 = None
    def __init__(self,parent,txtctrl,text,tip,width0=None,width1=None):
        wx.lib.stattext.GenStaticText.__init__(self,ID=-1,parent=parent,label='',
                                              style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
        self.SetLabel(text)
        h = self.GetMinHeight()
        if width0 is None:
            if Label.w0 is not None:
                self.SetMinSize((Label.w0, h))
        else:
            Label.w0 = width0
            self.SetMinSize((Label.w0, h))
        if width1 is None:
            if Label.w1 is not None:
                txtctrl.SetMinSize((Label.w1, h))
        else:
            txtctrl.SetMinSize((width1, h))
            Label.w1 = width1

        self.SetToolTipString(tip)
        self.SetHelpText(u'esto es un help')
        txtctrl.SetToolTipString(tip)


class PanelQ4(wx.Panel):
    def __init__(self, parent, main, eqId,prefill=None):
        print "PanelQ4 (__init__)"
	self.parent = parent
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
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

        # fillers for the gridsizer
        self.dummy1 = wx.StaticText(self,-1,'')
        self.dummy2 = wx.StaticText(self,-1,'')
        self.dummy3 = wx.StaticText(self,-1,'')

        self.sizer_4_staticbox = wx.StaticBox(self, -1, _("Equipment list"))
        self.sizer_4_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        self.sizer_5_staticbox = wx.StaticBox(self, -1,
                                              _("Description of equipment for heat and cold generation"))
        self.sizer_5_staticbox.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))
        

        self.listBoxEquipment = wx.ListBox(self,-1,choices=[])
        self.Bind(wx.EVT_LISTBOX, self.OnListBoxEquipmentClick, self.listBoxEquipment)

        # izquierda
        self.tc1 = wx.TextCtrl(self,-1,'')
        self.st1 = Label(self,self.tc1,_("Name"),_("Short name of equipment"),LABELWIDTH, TEXTENTRYWIDTH)


        self.tc2 = wx.TextCtrl(self,-1,'')
        self.st2 = Label(self,self.tc2,_("Manufacturer"),_("Who made this equipment"))

        self.tc3 = wx.TextCtrl(self,-1,'')
        self.st3 = Label(self,self.tc3,_("Year"),_("Year of manufacturing or/and installation"))

        self.tc4 = wx.TextCtrl(self,-1,'')
        self.st4 = Label(self,self.tc4,_("Model"),_("Model of the equipment"))

        self.tc5 = wx.TextCtrl(self,-1,'')
        self.st5 = Label(self,self.tc5,_("Type"),_("Type of equipment"))

        self.tc6 = wx.TextCtrl(self,-1,'')
        self.st6 = Label(self,self.tc6,_("Nº units"),_("Number of units of the same type"))

        self.choiceOfDBFuel = wx.Choice(self,-1,choices=[])
        self.st7 = Label(self,self.choiceOfDBFuel,_("Fuel type"),_("Fuel type"))

        self.tc8 = wx.TextCtrl(self,-1,'')
        self.st8 = Label(self,self.tc8,_("Cooling tower"),_("Only for cooling: Type of cooling tower: dry/wet ?"))

        self.tc9 = wx.TextCtrl(self,-1,'')
        self.st9 = Label(self,self.tc9,_("Nominal power"),_("Nominal Power (heat or cold,output) (kW)"))

        self.tc10 = wx.TextCtrl(self,-1,'')
        self.st10 = Label(self,self.tc10,_("Fuel consumption"),_("Fuel consumption (nominal)"))

        # derecha
        self.tc11 = wx.TextCtrl(self,-1,'')
        self.st11 = Label(self,self.tc11,_("Units fuel"),_("Units (fuel consumption)"))

        self.tc12 = wx.TextCtrl(self,-1,'')
        self.st12 = Label(self,self.tc12,_("Elect. consumption"),_("Electricity consumption (kW)"))

        self.tc13 = wx.TextCtrl(self,-1,'')
        self.st13 = Label(self,self.tc13,_("Conversion efficiency"),_("Mean overall thermal conversion efficiency (%)"))

        self.tc14 = wx.TextCtrl(self,-1,'')
        self.st14 = Label(self,self.tc14,_("Elect. production"),_("CHP only: Electricity production (kW)"))

        self.tc15 = wx.TextCtrl(self,-1,'')
        self.st15 = Label(self,self.tc15,_("Conversion efficiency"),_("CHP only: Electrical conversion efficiency (%)"))

        self.tc16 = wx.TextCtrl(self,-1,'')
        self.st16 = Label(self,self.tc16,_("Temperature Exhaust"),_("Temperature of exhaust gas at standard operation conditions"))

        self.tc17 = wx.TextCtrl(self,-1,'')
        self.st17 = Label(self,self.tc17,_("Utiliz. factor"),_("Mean utilisation factor (full capacity = 100%) (%)"))

        self.tc18 = wx.TextCtrl(self,-1,'')
        self.st18 = Label(self,self.tc18,_("Hours of operation"),_("Hours of operation per day (hrs/day)"))

        self.tc19 = wx.TextCtrl(self,-1,'')
        self.st19 = Label(self,self.tc19,_("Days of operation"),_("Days of operation per year (days/year)"))

        self.tc20 = wx.TextCtrl(self,-1,'')
        self.st20 = Label(self,self.tc20,_("Heat or cold supplied"),_("Heat or cold supplied to the distribution line / branch (piping or duct) no."))

        self.buttonDeleteEquipment = wx.Button(self,-1,label=_("Delete equipment"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonDeleteEquipment, self.buttonDeleteEquipment)

        self.buttonAddEquipment = wx.Button(self,-1,label=_("Add equipment"))
        self.Bind(wx.EVT_BUTTON,self.OnButtonAddEquipment, self.buttonAddEquipment)

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL, label='Cancel')
        self.buttonCancel.SetMinSize((125, 32))
        self.buttonCancel.SetMaxSize((125, 32))
        self.Bind(wx.EVT_BUTTON,self.OnButtonCancel, self.buttonCancel)

        self.buttonOK = wx.Button(self,wx.ID_OK, label='OK')
        self.buttonOK.SetMinSize((125, 32))
        self.buttonOK.SetMaxSize((125, 32))
        self.Bind(wx.EVT_BUTTON,self.OnButtonOK, self.buttonOK)

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        #grid_sizer_1 = wx.FlexGridSizer(10, 4, 10, 10) #r,c,vsep,hsep
        grid_sizer_1 = wx.FlexGridSizer(10, 4, 10, 2) #r,c,vsep,hsep
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.VERTICAL)
        sizer_4.Add(self.listBoxEquipment, 1, wx.EXPAND, 0)
        sizer_4.Add(self.buttonDeleteEquipment, 0, wx.EXPAND, 0)
        sizer_4.Add(self.buttonAddEquipment, 0, wx.EXPAND, 2)
        sizer_3.Add(sizer_4, 1, wx.EXPAND, 0)

        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)
        sizer_5.Add(grid_sizer_1, 1, wx.EXPAND, 0)


        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL
        flagText = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL
        grid_sizer_1.Add(self.st1, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc1, 0, flagText, 0)
        grid_sizer_1.Add(self.st11, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc11, 0, flagText, 0)
        grid_sizer_1.Add(self.st2, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc2, 0, flagText, 0)
        grid_sizer_1.Add(self.st12, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc12, 0, flagText, 0)
        grid_sizer_1.Add(self.st3, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc3, 0, flagText, 0)
        grid_sizer_1.Add(self.st13, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc13, 0, flagText, 0)
        grid_sizer_1.Add(self.st4, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc4, 0, flagText, 0)
        grid_sizer_1.Add(self.st14, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc14, 0, flagText, 0)
        grid_sizer_1.Add(self.st5, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc5, 0, flagText, 0)
        grid_sizer_1.Add(self.st15, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc15, 0, flagText, 0)
        grid_sizer_1.Add(self.st6, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc6, 0, flagText, 0)
        grid_sizer_1.Add(self.st16, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc16, 0, flagText, 0)
        grid_sizer_1.Add(self.st7, 0, flagLabel, 0)
        grid_sizer_1.Add(self.choiceOfDBFuel, 0, flagText, 0)
        grid_sizer_1.Add(self.st17, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc17, 0, flagText, 0)
        grid_sizer_1.Add(self.st8, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc8, 0, flagText, 0)
        grid_sizer_1.Add(self.st18, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc18, 0, flagText, 0)
        grid_sizer_1.Add(self.st9, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc9, 0, flagText, 0)
        grid_sizer_1.Add(self.st19, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc19, 0, flagText, 0)
        grid_sizer_1.Add(self.st10, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc10, 0, flagText, 0)
        grid_sizer_1.Add(self.st20, 0, flagLabel, 0)
        grid_sizer_1.Add(self.tc20, 0, flagText, 0)
        grid_sizer_1.Add(self.dummy1, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.dummy2, 0, wx.EXPAND, 0)
            
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
        if Status.PId <> 0:
#..............................................................................
# 1. equipment with this name not yet existing

            if self.check(self.tc1.GetValue()) <> 'NULL' and \
		    len(Status.DB.qgenerationhc.Equipment[self.tc1.GetValue()].Questionnaire_id[\
		    Status.PId].AlternativeProposalNo[Status.ANo]) == 0:

                if len(Status.DB.dbfuel.FuelName[\
		    str(self.choiceOfDBFuel.GetStringSelection())])>0:
                    dbfid = Status.DB.dbfuel.FuelName[\
                        str(self.choiceOfDBFuel.GetStringSelection())][0].DBFuel_ID
                else:
                    dbfid = None

                tmp = {
                    "Questionnaire_id":Status.PId,
                    "AlternativeProposalNo":Status.ANo,
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
                    "CoolTowerType":self.check(self.tc8.GetValue())
#                    "IsAlternative":0
                    }

                Status.DB.qgenerationhc.insert(tmp)
                Status.SQL.commit()
                self.fillEquipmentList()

#..............................................................................
# 2. overwrite data of existing equipment

            elif self.check(self.tc1.GetValue()) <> 'NULL' and \
		    len(Status.DB.qgenerationhc.Equipment[self.tc1.GetValue()].Questionnaire_id[\
		    Status.PId].AlternativeProposalNo[Status.ANo]) == 1:

                if len(Status.DB.dbfuel.FuelName[\
		    str(self.choiceOfDBFuel.GetStringSelection())])>0:
                    dbfid = Status.DB.dbfuel.FuelName[\
                        str(self.choiceOfDBFuel.GetStringSelection())][0].DBFuel_ID
                else:
                    dbfid = None

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
                    "CoolTowerType":self.check(self.tc8.GetValue())
#                    "IsAlternative":0
                    }

                q = Status.DB.qgenerationhc.Equipment[\
		    self.tc1.GetValue()].Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo][0]
                q.update(tmp)
                Status.SQL.commit()
                self.fillEquipmentList()

            else:
                self.main.showError("Equipment has to be an unique value!")

            print "PanelQ4 (add button): equipment type = ",self.tc5.GetValue()
            self.parent.equipeType = self.check(self.tc5.GetValue())


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

    def fillEquipmentList(self):
        self.listBoxEquipment.Clear()
        if len(Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]) > 0:
            for n in Status.DB.qgenerationhc.Questionnaire_id[Status.PId].AlternativeProposalNo[Status.ANo]:
                self.listBoxEquipment.Append (str(n.Equipment))


    def fillChoiceOfDBFuel(self):
        self.choiceOfDBFuel.Clear()
        self.choiceOfDBFuel.Append ("None")
        for n in Status.DB.dbfuel.FuelName["%"]:
            self.choiceOfDBFuel.Append (n.FuelName)
        self.choiceOfDBFuel.SetSelection(0)


    def fillPage(self):
	if Status.PId != 0:
	    self.fillEquipmentList()

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
