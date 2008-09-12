#Boa:Frame:PreferencesFrame
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	Preferences Frame
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger  12/09/2008
#       Revised by:         
#
#       Changes to previous version:
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
from GUITools import *
from displayClasses import *
from units import *
from fonts import *
from einstein.GUI.dialogOK import *

# constants that control the default sizes
# 1. font sizes
TYPE_SIZE_LEFT    =   9
TYPE_SIZE_RIGHT   =   9
TYPE_SIZE_TITLES  =  10

# 2. field sizes
HEIGHT_LEFT        =  29
LABEL_WIDTH_LEFT   = 300
HEIGHT_RIGHT       =  26
LABEL_WIDTH_RIGHT  = 300
DATA_ENTRY_WIDTH   = 100
UNITS_WIDTH        = 100

def create(parent):
    return PreferencesFrame(parent)

[wxID_FRAME1, wxID_FRAME1NOTEBOOK1, wxID_FRAME1STATICTEXT1, 
 wxID_FRAME1STATICTEXT2, 
] = [wx.NewId() for _init_ctrls in range(4)]

class PreferencesFrame(wx.Frame):
    def __init__(self, parent):
        self._init_ctrls(parent)
        self.__do_layout()
        self.fillPage()

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(300, 140), size=wx.Size(600, 400),
              style=wx.DEFAULT_FRAME_STYLE, title='EINSTEINs preferences')
        self.SetClientSize(wx.Size(600, 400))

        # access to font properties object
        fp = FontProperties()

        self.notebook = wx.Notebook(id=wxID_FRAME1NOTEBOOK1, name='notebook',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(600, 340), style=0)
        self.notebook.SetFont(fp.getFont())

        self.page1 = wx.Panel(self.notebook)
        self.page2 = wx.Panel(self.notebook)

        self.boxDebug = wx.StaticBox(self.page1, -1, _("Debugging options"))
        self.boxDebug.SetForegroundColour(TITLE_COLOR)
        self.boxDebug.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.boxHR = wx.StaticBox(self.page2, -1, _("Heat recovery calculation"))
        self.boxHR.SetForegroundColour(TITLE_COLOR)
        self.boxHR.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        fs = FieldSizes(wHeight=HEIGHT_LEFT,wLabel=LABEL_WIDTH_LEFT,
                       wData=DATA_ENTRY_WIDTH,wUnits=UNITS_WIDTH)

        self.par1_1 = ChoiceEntry(self.page1,
                               values=DEBUGMODES,
                               label=_("Debug mode for consistency check:"),
                               tip=_("This will create different volume of output for debugging:"))        

        self.par2_1 = ChoiceEntry(self.page2,
                               values=["estimate","PE2"],
                               label=_("Method for calculation of heat exchanger network"),
                               tip=_("estimate is based on HR potential and does not account for real HXs"))

        self.buttonCancel = wx.Button(self,wx.ID_CANCEL,_("Cancel"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.buttonCancel)
        self.buttonCancel.SetFont(fp.getFont())

        self.buttonOK = wx.Button(self,wx.ID_OK,_("OK"))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOK)
        self.buttonOK.SetDefault()
        self.buttonOK.SetFont(fp.getFont())

    def __do_layout(self):
        # generated method, don't edit
        sizer_frame = wx.BoxSizer(wx.VERTICAL)
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_HR = wx.StaticBoxSizer(self.boxHR, wx.VERTICAL)
        sizer_Debug = wx.StaticBoxSizer(self.boxDebug, wx.VERTICAL)

        flagLabel = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM
        flagText = wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.BOTTOM

        sizer_buttons.Add(self.buttonCancel, 0, flagText, 1)
        sizer_buttons.Add(self.buttonOK, 0, flagText, 1)
        
        # Left tab. Processes description
        sizer_Debug.Add(self.par1_1, 0, flagText, 1)

        sizer_1.Add(sizer_Debug, 0, flagText, 1)

        sizer_HR.Add(self.par2_1, 0, flagText, 1)

        sizer_2.Add(sizer_HR, 0, flagText, 1)

        self.page1.SetSizer(sizer_1)
        self.page2.SetSizer(sizer_2)
                
        self.notebook.AddPage(self.page1, _('debug options'))
        self.notebook.AddPage(self.page2, _('calculation tools'))

        sizer_frame.Add(self.notebook, 0, flagText, 1)
        sizer_frame.Add(sizer_buttons)

        self.SetSizer(sizer_frame)

        self.Layout()

    def OnButtonCancel(self, event):
        confirm =  DialogOK(self,_("exit settings"),_("do you want to exit without saving ?"))
        if confirm.ShowModal() == wx.ID_OK: self.Close()

    def OnButtonOK(self, event):
        Status.HRTool = self.par2_1.GetValue(text="True")
        print "Preferences (ButtonOK): HRTool = ",Status.HRTool
        self.Close()

    def fillPage(self):
        try:
            print "Preferences (fillPage): HRTool = ",Status.HRTool
        except:
            print "Preferences (fillPage): HRTool undefined"
            Status.HRTool = "PE2"
            
        self.par2_1.entry.SetStringSelection(Status.HRTool)


