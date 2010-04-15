#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	displayClasses: Some useful classes for panel display
#
#==============================================================================
#
#	Version No.: 0.04
#	Created by: 	    Tom Sobota 06/06/2008
#       Changed by:         Hans Schweiger 10/10/2008
#
#       Changes to previous version:
#       TS20080530          Added several classes for data display and edition
#       06/06/2008: TS      Some changes for Stoyan's panel changes
#       14/06/2008: TS      Added multiple choices
#       27/06/2008: TS      Rewrote Float and Date entrys
#       10/10/2008: HS      conversion to unicode added in TextEntry(SetValue)
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
import sys
import re
import locale
import math
import wx
import wx.combo
#import wx.lib.masked.numctrl
import wx.lib.intctrl
import wx.lib.stattext
#import wx.lib.masked
import wx.calendar
from einstein.GUI.status import Status
from einstein.modules.messageLogger import *
import units
from fonts import FontProperties

CHOOSERBCGCOLOR    = (255,255,255)
FGCOLOR            = (0,0,0)
TEXTBKGCOLOR       = (255,255,255)
EMPTYBKGCOLOR      = (255,255,255)
INVALIDBKGCOLOR    = (255,255,0)
LOWERACCEPTEDDATE  = '01/01/1900'
UPPERACCEPTEDDATE  = '12/31/2050'

ENCODING = "latin-1"    #local encoding

def error(text):
    dlg = wx.MessageDialog(None,text,'Error',wx.OK | wx.ICON_ERROR)
    ret = dlg.ShowModal()
    dlg.Destroy()
    
        
class FieldSizes(object):
    # sizes of subwidgets
    labelWidth=100
    dataWidth=200
    unitsWidth=80
    totalWidth = labelWidth + dataWidth + unitsWidth
    Height=32
    
    def __init__(self, wHeight=None, wLabel=None,wData=None,wUnits=None):
        #
        # size properties
        #
        try:
            if wHeight is not None: FieldSizes.Height = int(wHeight)
            if wLabel is not None: FieldSizes.labelWidth = int(wLabel)
            if wData is not None: FieldSizes.dataWidth = int(wData)
            if wUnits is not None: FieldSizes.unitsWidth = int(wUnits)
            FieldSizes.totalWidth = int(FieldSizes.labelWidth+FieldSizes.dataWidth+FieldSizes.unitsWidth+6)
        except:
            error('Error in FieldSizes: wHeight=%s, wLabel=%s,wData=%s,wUnits=%s' % \
                                   (wHeight,wLabel,wData,wUnits))

        
class Generics(object):
    def makeColour(self, something):
        if isinstance(something,tuple):
            try:
                newcolor = wx.Colour(something[0],something[1],something[2])
                something = newcolor
            except:
                error(repr(something)+' is not a valid color, sorry')
                something = wx.Colour(100,100,100)
                
        return something

    def setTooltips(self,other,tip):
        if tip:
            t = tip.strip()
            if len(t) > 0:
                other.entry.SetToolTipString(t)
                try:
                    # the label can exist or not
                    other.label.SetToolTipString(t)
                except:
                    pass

    def setUnits(self,other,tip,unitdict):
        defaultDisplayUnit = None
        if unitdict is not None:
            other.units.Clear()
            try:
                #if unitdict.__class__.__name__ == 'str':
                if isinstance(unitdict,str):
                    try:
                        # find default display unit
                        defaultDisplayUnit = units.UNITSYSTEM[Status.Units][unitdict]
                        # find the whole list of possible units of this class
                        unitlist = units.UNITS[unitdict].keys()
                        # load the choice
                        for u in unitlist:
                            other.units.Append(u)
                        # set the choice to the default unit
                        other.units.SetStringSelection(defaultDisplayUnit)
                    except:
                        error(unitdict+' is not a defined measurement class')
                else:
                    error(repr(unitdict)+' is not a string')
            except:
                error(repr(unitdict)+' is not a string')

            other.units.SetToolTipString(tip)
        return defaultDisplayUnit

    def setSizes(self,wLabel,wData,hasunits,wUnits):
        h = FieldSizes.Height

        # sets label size
        if wLabel is None:
            lW = FieldSizes.labelWidth
        else:
            lW = wLabel
        lblSize = wx.Size(lW, h)

        # sets data size
        if hasunits:
            if wData is None:
                lD = FieldSizes.dataWidth
            else:
                lD = wData
        else:
            if wData is None:
                lD = FieldSizes.dataWidth + FieldSizes.unitsWidth + 1
            else:
                lD = wData
        datSize = wx.Size(lD, h)
        # sets units size
        if wUnits is None:
            lU = FieldSizes.unitsWidth
        else:
            lU = wUnits
        uniSize = wx.Size(lU, h)

        totSize = wx.Size(lW + lD + lU + 2, h+1)
        return (totSize,lblSize,datSize,uniSize)


    def getChoiceValues(self, other, multiple, text):
        if multiple:
            # multiple values can be selected
            if text:
                # return a list with the texts of the selections
                slist = other.GetSelection()
                return tuple(slist)
                    
            else:
                # we return a tuple with the indices of the selections
                return other.GetSelection()
        else:
            # single values can be selected
            if text:
                # return a tuple with the texts of the selections
                return other.GetStringSelection()
            else:
                # we return the index of the (single) selection
                return other.GetCurrentSelection()



class ListCombo(wx.ListCtrl, wx.combo.ComboPopup):
    def __init__(self):
        # Since we are using multiple inheritance, and don't know yet
        # which window is to be the parent, we'll do 2-phase create of
        # the ListCtrl instead, and call its Create method later in
        # our Create method.  (See Create below.)
        self.PostCreate(wx.PreListCtrl())
        # Init the ComboPopup base class.
        wx.combo.ComboPopup.__init__(self)

    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.value = -1
        self.curitem = -1


    def AddItem(self, txt):
        self.InsertStringItem(self.GetItemCount(), txt)

    def OnMotion(self, evt):
        item, flags = self.HitTest(evt.GetPosition())
        if item >= 0:
            #self.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        pass
        #self.value = self.curitem
        #self.Dismiss()

    def OnLeftDClick(self, evt):
        # close the listbox
        self.Dismiss()

    # The following methods are those that are overridable from the
    # ComboPopup base class.

    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        wx.ListCtrl.Create(self, parent,style=wx.LC_LIST|wx.SIMPLE_BORDER)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        #self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        return True


    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        idx = self.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.value >= 0:
            return self.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.combo.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        s = ';'.join(self.GetSelection())
        combo = self.GetCombo()
        combo.SetText(s)
        wx.combo.ComboPopup.OnDismiss(self)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped.
    def OnComboKeyEvent(self, event):
        wx.combo.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        wx.combo.ComboPopup.OnComboDoubleClick(self)

    def Clear(self):
        self.ClearAll()

    # utility functions for implementing a GetSelection method
    def GetFirstSelected(self):
        """return first selected item, or -1 when none"""
        return self.GetNextSelected(-1)

    def GetNextSelected(self, item):
        """return subsequent selected items, or -1 when no more"""
        return self.GetNextItem(item, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

    def GetSelection(self):
        sel = []
        i = self.GetFirstSelected()
        while i >= 0:
            s = self.GetItemText(i)
            sel.append(s)
            i = self.GetNextSelected(i)
        return sel
        

class CFloat(wx.TextCtrl):
    def __init__(self, prnt,
                 id=-1,
                 pos=wx.DefaultPosition,
                 size=(100,32),
                 min= -1e38,
                 max= +1e38,
                 foregroundColour=FGCOLOR,
                 emptyBackgroundColour=EMPTYBKGCOLOR,
                 validBackgroundColour=TEXTBKGCOLOR,
                 invalidBackgroundColour=INVALIDBKGCOLOR,
                 style=0,
                 value=0.0,
                 decimals=2,
                 nosep=False):
        self.prnt = prnt
        self.min = min
        self.max = max
        self.decimals = decimals

        u = Generics()
        self.foregroundColour = u.makeColour(foregroundColour)
        self.emptyBackgroundColour = u.makeColour(emptyBackgroundColour)
        self.validBackgroundColour = u.makeColour(validBackgroundColour)
        self.invalidBackgroundColour = u.makeColour(invalidBackgroundColour)
        self.validFloat = re.compile(r'-?\d*\.?\d*')

        wx.TextCtrl.__init__(self,id=id,parent=prnt,
                             pos=pos,
                             size=size,
                             style=style)
        # bind some events
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_TEXT, self.OnEntry)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

        # get a dictionary of local parameters
        loc = locale.localeconv()
        self.dc = loc['decimal_point']
        if nosep:
            self.tsep = ''
        else:
            self.tsep = loc['thousands_sep']
        self.tsep = ' ' # just for testing
        self.dc = '.'   # testing

        if self.tsep == self.dc:
            # if decimal dot is the same as thousands separator,
            # default to something sensible
            self.tsep = ','
            self.dc = '.'

    def OnChar(self, event):
        # filter all characters except deletes, positioning,
        # digits, minus sign, decimal point
        c = event.GetKeyCode()
        if c == wx.WXK_BACK or c == wx.WXK_DELETE or c == wx.WXK_RIGHT or c == wx.WXK_LEFT:
            event.Skip()
        elif (c >= ord('0') and c <= ord('9')) or c == ord('-') or c == ord(self.dc):
            event.Skip()
        else:
            # ignore invalid keys
            event.Skip(False)


    def OnEntry(self, event):
        s = event.GetString()
        # sets value in parent (FloatEntry instance)
        self.prnt.lastInternalValue = s 
        if s.strip() == '':
            # don't touch null value
            self.SetBackgroundColour(self.emptyBackgroundColour)
        else:
            t =self.__clean_dot(s)
            if self.__isValidFloat(t):
                f = float(t)
                ignore = self.verifyLimits(f)
            else:
                self.SetBackgroundColour(self.invalidBackgroundColour)
                
        event.Skip()

    def OnFocus(self,event):
        # clean thousands separators for editing
        s = self.GetValue()
        if s.strip() == '':
            # don't touch null value
            return
        s1 = self.__clean_tsep(s)
        self.ChangeValue(s1)
        event.Skip()

    
    def OnKillFocus(self,event):
        value = self.GetValue()
        if value.strip() == '':
            self.SetBackgroundColour(self.emptyBackgroundColour)
        else:
            f = self.toFloat(value)
            if f is not None:
                value = self.verifyLimits(f)
        self.showFormatted(str(value))
        event.Skip()

    def toFloat(self,value):
        s1 = self.__clean_tsep(value) 
        s2 = self.__clean_dot(s1)
        try:
            f = float(s2)
            return f
        except:
            return None
        
    def verifyLimits(self,value):
        if value > self.max:
            self.SetBackgroundColour(self.invalidBackgroundColour)
            return self.max
        elif value < self.min:
            self.SetBackgroundColour(self.invalidBackgroundColour)
            return self.min
        else:
            self.SetBackgroundColour(self.validBackgroundColour)
        return value
        
    def SetValue(self,value):
        # several empty field conditions
        if value is None or (isinstance(value,str) and value == ''):
            value = ''
            self.ChangeValue(value)
            self.SetBackgroundColour(self.emptyBackgroundColour)
        elif isinstance(value,str) and value != '':
            # value is a string. must convert to float
            f = self.toFloat(value)
            if f is not None:
                value = f
            else:
                value = None
                self.SetBackgroundColour(self.invalidBackgroundColour)

        if isinstance(value,float):
            # verify limits
            ignore = self.verifyLimits(value)
            self.showFormatted(str(value))

        return value

    
    def showFormatted(self,s):
        if s.strip() == '':
            # don't touch null value
            return
        f = self.toFloat(s)
        sign = ''
        if f<0.0:
            sign='-'
            f = abs(f)
        snum = "%.*f" % (self.decimals,f)
        try:
            (integ,frac) = snum.split(".")
        except ValueError:
            integ = snum
            frac = ''
        # set thousands separator
        sn = ''
        r0 = integ[::-1] # reverse
        for i,c in enumerate(r0):
            if (i % 3) == 0 and len(sn)>1:
                sn += self.tsep
            sn += c
        s3 = sign + sn[::-1] + self.dc + frac
        self.ChangeValue(s3)

    def __isValidFloat(self, s):
        if not isinstance(s,str):
            s = str(s)
        m = self.validFloat.match(s)
        if m:
            ss = m.group(0)
            if len(s) == len(ss):
                return True
        return False

    def __clean_tsep(self,s):
        if not isinstance(s,str):
            s = str(s)
        if not self.__isValidFloat(s):
            return s.replace(self.tsep,'')
        return s
    
    def __clean_dot(self,s):
        if not isinstance(s,str):
            s = str(s)
        if not self.__isValidFloat(s):
            return s.replace(self.dc,'.')
        return s


class CDate(wx.TextCtrl):
    def __init__(self, prnt, prnt2,
                 id=-1,
                 pos=wx.DefaultPosition,
                 size=(100,32),
                 min= LOWERACCEPTEDDATE,
                 max= UPPERACCEPTEDDATE,
                 foregroundColour=FGCOLOR,
                 emptyBackgroundColour=EMPTYBKGCOLOR,
                 validBackgroundColour=TEXTBKGCOLOR,
                 invalidBackgroundColour=INVALIDBKGCOLOR,
                 style=0,
                 value=wx.DateTime_Now()):

        self.prnt = prnt
        self.prnt2 = prnt2
        self.cal = None
        self.min = wx.DateTime()
        self.min.ParseDate(min)
        self.max = wx.DateTime()
        self.max.ParseDate(max)
        if isinstance(value,wx.DateTime):
            self.initialdate = value
        else:
            self.initialdate = wx.DateTime()
            self.initialdate.ParseDate(value)
            
        u = Generics()
        self.foregroundColour = u.makeColour(foregroundColour)
        self.emptyBackgroundColour = u.makeColour(emptyBackgroundColour)
        self.validBackgroundColour = u.makeColour(validBackgroundColour)
        self.invalidBackgroundColour = u.makeColour(invalidBackgroundColour)

        wx.TextCtrl.__init__(self,id=id,parent=prnt,
                             pos=pos,
                             size=size,
                             style=style)
        # bind some events
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_TEXT, self.OnEntry)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

    def OnCalSelected(self, event):
        newdate = event.GetDate()
        self.showFormatted(newdate)
        #cal = event.GetEventObject()
        self.calpanel.Destroy()
        self.cal = None
        self.prnt2.SetFocus()
        
    def OnCalSelChanged(self, event):
        cal = event.GetEventObject()
        date = cal.GetDate()
        event.Skip()


    def OnCharCal(self,event):
        # any keypress on the calendar closes the window
        # this works in Windows but not in FreeBSD
        self.calpanel.Destroy()
        self.cal = None
        event.Skip()

    def OnChar(self, event):
        # if the calendar is displayed, delete it
        if self.cal is not None:
            self.calpanel.Destroy()
            self.cal = None
        
        # filter all characters except digits, '-', '/'
        c = event.GetKeyCode()
        if c == wx.WXK_BACK or c == wx.WXK_DELETE or c == wx.WXK_RIGHT or c == wx.WXK_LEFT:
            event.Skip()
        elif (c >= ord('0') and c <= ord('9')) or c == ord('-') or c == ord('/'):
            event.Skip()
        else:
            # ignore invalid keys
            event.Skip(False)


    def OnEntry(self, event):
        s = event.GetString()
        if s.strip() == '':
            # don't touch null value
            self.SetBackgroundColour(self.emptyBackgroundColour)
        else:
            self.verifyLimits(s)
                
        event.Skip()

    def OnFocus(self,event):
        if self.cal is None:
            # show calendar control
            (x,y) = self.GetPositionTuple()
            (xp,yp) = self.prnt.GetPositionTuple()
            (w,h) = self.prnt.GetSizeTuple()
            # frame for the calendar
            self.calpanel = wx.Frame(self.prnt2, id=-1,
                                     style=wx.STAY_ON_TOP)
            self.cal = wx.calendar.CalendarCtrl(self.calpanel, -1,
                                                self.initialdate, pos=(0,0))
            (wc,hc) = self.cal.GetSizeTuple()
            self.calpanel.SetDimensions(x+xp,yp+h,wc,hc)
            self.calpanel.Show()
            self.cal.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED,self.OnCalSelChanged)
            self.cal.Bind(wx.calendar.EVT_CALENDAR, self.OnCalSelected)
            self.cal.Bind(wx.EVT_CHAR, self.OnCharCal)

        event.Skip()


    
    def OnKillFocus(self,event):
        # if there is input from the calendar control
        value = self.GetValue()
        if value.strip() == '':
            self.SetBackgroundColour(self.emptyBackgroundColour)
        else:
            self.verifyLimits(value)
        self.showFormatted(value)
        event.Skip()

    def verifyLimits(self,value):
        if isinstance(value,wx.DateTime):
            d = value
        else:
            # value is a string
            d = wx.DateTime()
            rsp = d.ParseDate(value)
            if rsp == -1:
                self.SetBackgroundColour(self.invalidBackgroundColour)
                return

        if d.IsLaterThan(self.max):
            self.SetBackgroundColour(self.invalidBackgroundColour)
        elif d.IsEarlierThan(self.min):
            self.SetBackgroundColour(self.invalidBackgroundColour)
        else:
            self.SetBackgroundColour(self.validBackgroundColour)
        
    def SetValue(self,value):
        # several empty field conditions
        if value is None:
            value = ''
            self.ChangeValue(value)
            self.SetBackgroundColour(self.emptyBackgroundColour)
        elif isinstance(value,wx.DateTime):
            s = value.FormatISODate()
            value = s
            self.verifyLimits(value)
            self.ChangeValue(value)
        elif isinstance(value,str):
            if value.strip() == '' or value.strip() == 'None':
                self.ChangeValue('')
                self.SetBackgroundColour(self.emptyBackgroundColour)
            else:
                # verify limits
                self.verifyLimits(value)
                self.showFormatted(value)

        return value

    
    def showFormatted(self,s):
        if isinstance(s,wx.DateTime):
            s1 = s.FormatISODate()
        elif s.strip() == '':
            # don't touch null value
            s1 = ''
        else:
            d = wx.DateTime()
            d.ParseDate(s)
            s1 = d.FormatISODate()
        self.ChangeValue(s1)


class CInt(wx.lib.intctrl.IntCtrl):
    def __init__(self,
                 prnt,
                 id=-1,
                 pos=wx.DefaultPosition,
                 allowLong=True,
                 allowNone=True,
                 size=(100,32),
                 min= None,
                 max= None,
                 foregroundcolour=(0,0,100),
                 backgroundcolour=TEXTBKGCOLOR,
                 invalidBackgroundColour=(255,250,250),
                 style=0,
                 value=0):

        u = Generics()
        foregroundcolour = u.makeColour(foregroundcolour)
        backgroundcolour = u.makeColour(backgroundcolour)
        invalidBackgroundColour = u.makeColour(invalidBackgroundColour)
        
        wx.lib.intctrl.IntCtrl.__init__(self,id=id,
                                        parent=prnt,oob_color=invalidBackgroundColour,
                                        pos=pos,
                                        allow_long=allowLong,allow_none=allowNone,
                                        size=size,style=style,value=value)
        self.SetMaxSize(size)
        # allowable range of number
        self.SetMax(max)
        self.SetMin(min)
        # background color
        self.SetBackgroundColour(backgroundcolour)
        # foreground (letters) color
        self.SetForegroundColour(foregroundcolour)
        #self.SetValue(initialvalue)



class FloatEntry(wx.Panel):
    def __init__(self, parent=None,
                 decimals=2,                                   # digits in the fraction
                 ipart=None,                                   # deprecated (and ignored)
                 nosep=False,                                  # ignore thousands separator
                 minval=-1e38,                                 # min value
                 maxval=+1e38,                                 # max value
                 value=0.,                                     # initial value
                 unitdict=None,                                # unit dict for the unit selector
                 wLabel=None,                                  # width of the label
                 wData=None,                                   # width of the data entry
                 wUnits=None,                                  # width of the unit selector
                 label='',                                     # text of the label
                 tip='',                                       # text of the tip
                 fontsize=None):                               # fontsize for subwidgets

        self.unitdict = unitdict
        self.lastInternalValue = None
        self.defaultDisplayUnit = None

        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.g = Generics()
        self.f = FontProperties()

        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,True,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            sty = wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT|wx.BORDER_NONE
            self.label = wx.StaticText(self,id=-1,label=label,size=lblSize,pos=(0,0),style = sty)
            self.f.setFont(self.label,size=fontsize)
            self.label.Wrap(lblSize.GetWidth())
            self.label.Center(wx.VERTICAL)

        # create a masked float-point control
        self.entry = CFloat(self,pos=(lblSize[0]+1,0),
                           size=datSize,                        # size of control
                           min=minval,                          # minimum value admitted
                           max=maxval,                          # maximum value admitted
                           decimals=decimals,                   # number of decimals
                           nosep=nosep,
                           style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)

        self.f.setFont(self.entry,size=fontsize)
        self.entry.Center(wx.VERTICAL)
        self.entry.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

        # load and show a unit selector
        # also sets the default display unit
        if self.unitdict is not None:
            self.units = wx.Choice(self, -1, pos=(lblSize[0]+datSize[0]+2,0),
                                     choices=[], size=uniSize)
            self.setUnits('Select a measurement unit', unitdict)
            backgroundcolour = self.g.makeColour(CHOOSERBCGCOLOR)
            self.units.SetBackgroundColour(backgroundcolour)
            self.f.setFont(self.units,size=fontsize)
            self.units.Center(wx.VERTICAL)
            self.units.Bind(wx.EVT_CHOICE, self.OnUnits)
        

        # set initial value (must be after loading the selector)
        self.SetValue(value)

        # set tooltips
        self.g.setTooltips(self,tip)

        # create popup menu for easy clearing/setting to zero
        self.popupmenu = wx.Menu()
        for text in "Clear Zero".split():
            item = self.popupmenu.Append(-1, text)
            self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)

    def OnShowPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)

    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        if text == 'Clear':
            self.entry.SetValue(None)
        elif text == 'Zero':
            self.entry.SetValue(0.0)
            
    def OnUnits(self, event):
        # read new measurement unit and convert to internal encoding
        self.defaultDisplayUnit = event.GetString().encode('iso-8859-15')
        # recalculate to display units
        self.SetValue(self.lastInternalValue)

    def setUnits(self,tip,unitdict):
        # only allows change in units when units were initially declared
        # and the units choice control was created
        if self.unitdict:
            self.defaultDisplayUnit = self.g.setUnits(self,tip, unitdict)

    def GetValue(self):
        dValue = self.entry.GetValue().encode('iso-8859-15')
        if dValue is None:
            return None
        elif isinstance(dValue,str):
            if dValue.strip() == '':
                return None
            f = self.entry.toFloat(dValue)
        elif isinstance(dValue,float) or isinstance(dValue,int):
            f = dValue
            
        if self.defaultDisplayUnit is None:
            return f
        try:
            iValue = units.internalValue(f,
                                         self.defaultDisplayUnit,
                                         self.unitdict)
            return self.entry.toFloat(iValue)
        except:
            print 'FloatEntry: error in conversion display->internal ' \
                  'display=%s class=%s default=%s' % (dValue,
                                                      self.unitdict,
                                                      self.defaultDisplayUnit)
            
    def Clear(self):
        self.SetValue(None)
        
    def SetValue(self, iValue):
        #
        # saves internal value for an eventual unit change by user
        #
        self.lastInternalValue = iValue
        #
        # find display value
        #
        if iValue is None or iValue == '' or iValue == 'None':
            self.entry.SetValue(None)
        elif self.defaultDisplayUnit is None:
            # no unit conversion necessary
            f = self.entry.SetValue(iValue)
            if f is None:
                print 'FloatEntry: bad value for SetValue %s' % repr(iValue)
                self.entry.SetValue(None)
                self.lastInternalValue = None
        else:
            # convert to user units
            try:
                f = self.entry.toFloat(iValue)
                if f is not None:
                    dValue = units.displayValue(f,self.defaultDisplayUnit,self.unitdict)
                    self.entry.SetValue(dValue)
                else:
                    print 'FloatEntry: bad value for SetValue %s' % repr(iValue)
                    self.entry.SetValue(None)
                    self.lastInternalValue = None
            except:
                print 'FloatEntry: error in conversion internal->display ' \
                      'internal=%s class=%s default=%s' % (iValue, self.unitdict,self.defaultDisplayUnit)


    def GetUnit(self,text=False):
        if self.unitdict:
            return self.g.getChoiceValues(self.units, False, text)
        else:
            return None

    def setUnit(self,n):
        if self.unitdict:
            # n is the 0-based index to the contents
            self.units.SetSelection(n)

    def setColor(self, bgColor=(255,255,255), fgColor=(0,0,0)):
        self.entry.SetBackgroundColour(self.g.makeColour(bgColor))
        self.entry.SetForegroundColour(self.g.makeColour(fgColor))
 

        
class IntEntry(wx.Panel):
    def __init__(self, parent=None,
                 minval=None,                                  # min value
                 maxval=None,                                  # max value
                 value=0,                                      # initial value
                 unitdict=None,                                # unit dict for the unit selector
                 wLabel=None,                                  # width of the label
                 wData=None,                                   # width of the data entry
                 wUnits=None,                                  # width of the unit selector
                 label='',                                     # text of the label
                 tip='',                                       # text of the tip
                 fontsize=None):

        self.unitdict = unitdict
        self.lastInternalValue = None
        self.defaultDisplayUnit = None

        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.g = Generics()
        self.f = FontProperties()
        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,True,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            self.label = wx.lib.stattext.GenStaticText(self,ID=-1,label=label,size=lblSize,pos=(0,0),
                                                       style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
            self.f.setFont(self.label,size=fontsize)

        # create a masked fixed-point control
        self.entry = CInt(self,pos=(lblSize[0]+1,0),
                           size=datSize,                     # size of control
                           min=minval,                       # minimum value admitted
                           max=maxval,                       # maximum value admitted
                           style=wx.ALIGN_RIGHT)
        self.f.setFont(self.entry,size=fontsize)
        self.entry.Bind(wx.EVT_TEXT, self.OnEntry)
        self.entry.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

        # load and show a unit selector
        # also sets the default display unit
        if self.unitdict is not None:
            self.units = wx.Choice(self, -1, pos=(lblSize[0]+datSize[0]+2,0),
                                     choices=[], size=uniSize)
            self.setUnits('Select a measurement unit', unitdict)
            backgroundcolour = self.g.makeColour(CHOOSERBCGCOLOR)
            self.units.SetBackgroundColour(backgroundcolour)
            self.f.setFont(self.units,size=fontsize)
            self.units.Bind(wx.EVT_CHOICE, self.OnUnits)

        # set initial value (must be after loading the selector
        self.SetValue(value)

        # set tooltips
        self.g.setTooltips(self,tip)

        # create popup menu for easy clearing/setting to zero
        self.popupmenu = wx.Menu()
        for text in "Clear Zero".split():
            item = self.popupmenu.Append(-1, text)
            self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)

    def OnShowPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)

    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        if text == 'Clear':
            self.entry.SetValue(None)
        elif text == 'Zero':
            self.entry.SetValue(0)

    def OnEntry(self, event):
        s = event.GetString()
        self.lastInternalValue = self.GetValue()

    def OnUnits(self, event):
        # read new measurement unit and convert to internal encoding
        self.defaultDisplayUnit = event.GetString().encode('iso-8859-15')
        # recalculate to display units
        self.SetValue(self.lastInternalValue)

    def setUnits(self,tip,unitdict):
        if self.unitdict:
            self.defaultDisplayUnit = self.g.setUnits(self,tip, unitdict)

    def GetValue(self):
        dValue = self.entry.GetValue()
        if dValue is None:
            return None
        elif isinstance(dValue,str):
            if dValue.strip() == '':
                return None
            f = self.entry.toFloat(dValue)
        elif isinstance(dValue,float) or isinstance(dValue,int):
            f = dValue

        if self.defaultDisplayUnit is None:
            return int(f)
        try:
            iValue = units.internalValue(f,self.defaultDisplayUnit,self.unitdict)
            return int(iValue)
        except:
            print 'IntEntry: error in conversion disp->int '\
                  'disp=%s class=%s default=%s' % (dValue,
                                                   self.unitdict,
                                                   repr(self.defaultDisplayUnit))

    def Clear(self):
        self.SetValue(None)

    def SetValue(self, iValue):
        #
        # saves internal value for an eventual unit change by user
        #
        self.lastInternalValue = iValue
        #
        # find display value
        #
        if iValue is None or iValue == '' or iValue == 'None':
            self.entry.SetValue(None)
        else:
            try:
                f = int(float(iValue))
            except:
                print 'IntEntry: bad value for SetValue %s' % (repr(iValue),)
                self.entry.SetValue(0)
                return
            
            if self.defaultDisplayUnit is None:
                dValue = f
            else:
                try:
                    dValue = units.displayValue(float(f),self.defaultDisplayUnit,self.unitdict)
                except:
                    print 'IntEntry: error in conversion int->disp ' \
                          'int=%s class=%s default=%s' % (f, self.unitdict,
                                                          repr(self.defaultDisplayUnit))

                self.entry.SetValue(int(dValue))



    def GetUnit(self,text=False):
        if self.unitdict:
            return self.g.getChoiceValues(self.units, False, text)
        else:
            return None

    def setUnit(self,n):
        if self.unitdict:
            # n is the 0-based index to the contents
            self.units.SetSelection(n)

    def setColor(self, bgColor=(255,255,255), fgColor=(0,0,0)):
        self.entry.SetBackgroundColour(self.g.makeColour(bgColor))
        self.entry.SetForegroundColour(self.g.makeColour(fgColor))
 


class TextEntry(wx.Panel):
    def __init__(self, parent=None,
                 maxchars=None,    # max characters accepted
                 value='',         # initial value
                 wLabel=None,      # width of the label
                 wData=None,       # width of the data entry
                 wUnits=None,      # width of the unit selector (not used)
                 label='',         # text of the label
                 tip='',           # text of the tip
                 fontsize=None):

        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.g = Generics()
        self.f = FontProperties()

        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,False,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            self.label = wx.lib.stattext.GenStaticText(self,ID=-1,label=label,size=lblSize,pos=(0,0),
                                                       style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
            self.f.setFont(self.label,size=fontsize)

        # create a text control
        self.entry = wx.TextCtrl(self,-1,pos=(lblSize[0]+1,0),
                                 value=value,size=datSize,style=wx.ALIGN_RIGHT)
        self.f.setFont(self.entry,size=fontsize)
        self.entry.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

        foregroundColour = self.g.makeColour(FGCOLOR)
        validBackgroundColour = self.g.makeColour(TEXTBKGCOLOR)
        self.entry.SetForegroundColour(foregroundColour)
        self.entry.SetBackgroundColour(validBackgroundColour)
        if maxchars is not None:
            self.entry.SetMaxLength(maxchars)

        # set tooltips
        self.g.setTooltips(self,tip)

        # create popup menu for easy clearing
        self.popupmenu = wx.Menu()
        for text in "Clear Unknown".split():
            item = self.popupmenu.Append(-1, text)
            self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)

    def OnShowPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)

    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        if text == 'Clear':
            self.entry.SetValue('')
        if text == 'Unknown':
            self.entry.SetValue('None')


    def setUnits(self,tip,unitdict):
        # this method is just for compatibility
        pass

    def GetValue(self):
#        return self.entry.GetValue().encode(ENCODING)
        return self.entry.GetValue()

    def Clear(self):
        self.SetValue('')

    def SetValue(self, value):
        if value == None:
            self.entry.SetValue('')
            return
        
#        print "DisplayClasses (TextEntry - SetValue): value = %r"%value
        try:
            self.entry.SetValue(unicode(value,"utf-8"))
        except:
            try:
                self.entry.SetValue(unicode(value,ENCODING))
            except:
                self.entry.SetValue(value)
        
    def getUnit(self):
        # this method is just for compatibility
        return None

    def setUnit(self,value):
        # this method is just for compatibility
        pass

    def setColor(self, bgColor=(255,255,255), fgColor=(0,0,0)):
        self.entry.SetBackgroundColour(self.g.makeColour(bgColor))
        self.entry.SetForegroundColour(self.g.makeColour(fgColor))


class StaticTextEntry(wx.Panel):
    def __init__(self, parent=None,
                 maxchars=None,    # max characters accepted
                 value='',         # initial value
                 wLabel=None,      # width of the label
                 wData=None,       # width of the data entry
                 wUnits=None,      # width of the unit selector (not used)
                 label='',         # text of the label
                 tip='',           # text of the tip
                 fontsize=None):

        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.g = Generics()
        self.f = FontProperties()

        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,False,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            self.label = wx.lib.stattext.GenStaticText(self,ID=-1,label=label,size=lblSize,pos=(0,0),
                                                       style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
            self.f.setFont(self.label,size=fontsize)

        # create a text control
        self.entry = wx.TextCtrl(self,-1,pos=(lblSize[0]+1,0),
                                 value=value,size=datSize,style=wx.ALIGN_RIGHT|wx.TE_READONLY)
        self.f.setFont(self.entry,size=fontsize)
        self.entry.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

        foregroundColour = self.g.makeColour(FGCOLOR)
        validBackgroundColour = self.g.makeColour(TEXTBKGCOLOR)
        self.entry.SetForegroundColour(foregroundColour)
        self.entry.SetBackgroundColour(validBackgroundColour)
        if maxchars is not None:
            self.entry.SetMaxLength(maxchars)

        # set tooltips
        self.g.setTooltips(self,tip)

        # create popup menu for easy clearing
        self.popupmenu = wx.Menu()
        for text in "Clear Unknown".split():
            item = self.popupmenu.Append(-1, text)
            self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)

    def OnShowPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)

    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        if text == 'Clear':
            self.entry.SetValue('')
        if text == 'Unknown':
            self.entry.SetValue('None')


    def setUnits(self,tip,unitdict):
        # this method is just for compatibility
        pass

    def GetValue(self):
#        return self.entry.GetValue().encode(ENCODING)
        return self.entry.GetValue()

    def Clear(self):
        self.SetValue('')

    def SetValue(self, value):
        if value == None:
            self.entry.SetValue('')
            return

#        print "DisplayClasses (TextEntry - SetValue): value = %r"%value
        try:
            self.entry.SetValue(unicode(value,"utf-8"))
        except:
            try:
                self.entry.SetValue(unicode(value,ENCODING))
            except:
                self.entry.SetValue(value)

    def getUnit(self):
        # this method is just for compatibility
        return None

    def setUnit(self,value):
        # this method is just for compatibility
        pass

    def setColor(self, bgColor=(255,255,255), fgColor=(0,0,0)):
        self.entry.SetBackgroundColour(self.g.makeColour(bgColor))
        self.entry.SetForegroundColour(self.g.makeColour(fgColor))
 

class DateEntry(wx.Panel):
    def __init__(self, parent=None,
                 value=wx.DateTime_Now(), # initial value
                 min= LOWERACCEPTEDDATE,  # lower accepted date
                 max= UPPERACCEPTEDDATE,  # upper    "      "
                 wLabel=None,             # width of the label
                 wData=None,              # width of the data entry
                 wUnits=None,             # width of the unit selector (not used)
                 label='',                # text of the label
                 tip='',                  # text of the tip
                 fontsize=None):

        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.g = Generics()
        self.f = FontProperties()

        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,True,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            self.label = wx.lib.stattext.GenStaticText(self,ID=-1,label=label,size=lblSize,pos=(0,0),
                                                       style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
            self.f.setFont(self.label,size=fontsize)


        self.entry = CDate(self, parent, id=-1, pos=(lblSize[0]+1,0), size=datSize)

        self.SetValue(value)

        self.f.setFont(self.entry,size=fontsize)

        # set tooltips
        self.g.setTooltips(self,tip)

    def setUnits(self,tip,unitdict):
        # this method is just for compatibility
        pass

    def GetValue(self):
        value = self.entry.GetValue()
        if not value:
            return None
        date = wx.DateTime()
        date.ParseDate(value)
        return date.FormatISODate()

    def Clear(self):
        self.SetValue(None)

    def SetValue(self, value):
        self.entry.SetValue(value)
    
    def getUnit(self):
        # this method is just for compatibility
        return None

    def setUnit(self,value):
        # this method is just for compatibility
        pass

    def setColor(self, bgColor=(255,255,255), fgColor=(0,0,0)):
        self.entry.SetBackgroundColour(self.g.makeColour(bgColor))
        self.entry.SetForegroundColour(self.g.makeColour(fgColor))
 


class ChoiceEntry(wx.Panel):
    def __init__(self, parent=None,
                 values=[],       # initial values list
                 wLabel=None,     # width of the label
                 wData=None,      # width of the data entry
                 wUnits=None,     # width of the unit selector (not used)
                 label='',        # text of the label
                 tip='',          # text of the tip
                 fontsize=None):

        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.g = Generics()
        self.f = FontProperties()

        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,False,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            self.label = wx.lib.stattext.GenStaticText(self,ID=-1,pos=(0,0),
                                                       label=label,size=lblSize,
                                                       style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
            self.f.setFont(self.label,size=fontsize)

        #create a choice control
        self.entry = wx.Choice(self, -1, pos=(lblSize[0]+1,0),choices=values, size=datSize)
        backgroundcolour = self.g.makeColour(CHOOSERBCGCOLOR)
        self.entry.SetBackgroundColour(backgroundcolour)
        self.f.setFont(self.entry,size=fontsize)

        # set tooltips
        self.g.setTooltips(self,tip)

    def setUnits(self,tip,unitdict):
        # this method is just for compatibility
        pass

    def GetValue(self,text=False):
        return self.g.getChoiceValues(self.entry, False, text)

    def Clear(self):
        self.entry.Clear()

    def SetValue(self, thing=0):
        # this method has triple functionality:
        # if 'thing' is an integer n, the choice will show the nth element. 
        # if 'thing' is a string, the choice will show the element that contains the string
        # if 'thing' is a list, the elements of the list will be loaded in the choice.

#        print "DisplayClasses (SetValue): %r"%thing

        try:
            if isinstance(thing,int):
                try:
                    self.entry.SetSelection(thing)
                except:
                    self.entry.SetSelection(0)
            elif isinstance(thing,str) or isinstance(thing,unicode):
                if thing.strip() == '':
                    # clear the choice
                    self.entry.Clear()
                    return
                
#                print "DisplayClasses (ChoiceEntry - SetValue): value = %r"%thing
                try:
                    thing = unicode(thing,"utf-8")
                except:
                    try:
                        thing = unicode(thing,ENCODING)
                    except:
                        pass
                    
                try:
                    self.entry.SetSelection(self.entry.FindString(thing))
                except:
                    try:
                        self.entry.SetSelection(self.entry.FindString("None"))
                    except:
                        self.entry.SetSelection(0)

            elif isinstance(thing,list):
                # thing is a list of values for the choice control
                self.entry.Clear()
                for item in thing:
                    if item is None:
                        self.entry.Append(' ')
                    else:
                        self.entry.Append(item)
                self.entry.SetSelection(0)
        except:
            # possibly a numeric constant
            try:
                nn = int(thing)
                try:
                    self.entry.SetSelection(nn)
                except:
                    self.entry.SetSelection(0)
            except:
                self.entry.SetSelection(0)
    
    def getUnit(self):
        # this method is just for compatibility
        return None

    def setUnit(self,value):
        # this method is just for compatibility
        pass

    def setColor(self, bgColor=(255,255,255), fgColor=(0,0,0)):
        self.entry.SetBackgroundColour(self.g.makeColour(bgColor))
        self.entry.SetForegroundColour(self.g.makeColour(fgColor))
 


class MultipleChoiceEntry(wx.Panel):
    def __init__(self, parent=None,
                 values=None,       # initial values list
                 selected=None,     # initial selected values (list of strings)
                 wLabel=None,     # width of the label
                 wData=None,      # width of the data entry
                 wUnits=None,     # width of the unit selector (not used)
                 label='',        # text of the label
                 tip='',          # text of the tip
                 fontsize=None):

        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.g = Generics()
        self.f = FontProperties()

        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,False,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            self.label = wx.lib.stattext.GenStaticText(self,ID=-1,pos=(0,0),
                                                       label=label,size=lblSize,
                                                       style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
            self.f.setFont(self.label,size=fontsize)

        #create a ListCombo control
        # 1. Create a ComboCtrl
        self.cc = wx.combo.ComboCtrl(self, pos=(lblSize[0]+1,0),size=datSize)        
        # 2. Create a Popup
        self.entry = ListCombo()
        # 3. Associate them with each other.  This also triggers the
        #    creation of the ListCtrl.
        self.cc.SetPopupControl(self.entry)

        backgroundcolour = self.g.makeColour(CHOOSERBCGCOLOR)
        self.cc.SetBackgroundColour(backgroundcolour)
        self.entry.SetBackgroundColour(backgroundcolour)
        self.f.setFont(self.cc,size=fontsize)
        self.f.setFont(self.entry,size=fontsize)

        # set tooltips
        self.g.setTooltips(self,tip)

        # set values
        if values is not None:
            self.SetValue(values)

        # set initially selected
        if selected is not None:
            self.SetSelection(selected)
        
    def setUnits(self,tip,unitdict):
        # this method is just for compatibility
        pass

    def GetValue(self,text=False):
        #print self.entry.GetSelectedItemCount()
        return self.g.getChoiceValues(self.entry, True, text)

    def Clear(self):
        self.entry.Clear()

    def SetSelection(self,selection):
        combo = self.entry.GetCombo()
        if isinstance(selection,list):
            for val in selection:
                self.entry.SetStringValue(val)
            combo.SetText(';'.join(selection))
        else:
            self.entry.SetStringValue(selection)
            combo.SetText(selection)
        
    def SetValue(self, thing=0):
        try:
            if thing is None:
                self.entry.Append(' ')
            elif isinstance(thing,str) or isinstance(thing,unicode):
                try:
                    thing = unicode(thing,"utf-8")
                except:
                    try:
                        thing = unicode(thing,ENCODING)
                    except:
                        pass
                self.entry.Append(thing)
            elif isinstance(thing,list):
                # thing is a list of values for the control
                self.entry.Clear()
                for item in thing:
                    if item is None:
                        self.entry.AddItem(' ')
                    else:
                        self.entry.AddItem(item)
                self.SetSelection(thing[0])
        except:
            print 'DisplayClasses (MultipleChoiceEntry): Bad SetValue %s' % thing

    
    def getUnit(self):
        # this method is just for compatibility
        return None

    def setUnit(self,value):
        # this method is just for compatibility
        pass

    def setColor(self, bgColor=(255,255,255), fgColor=(0,0,0)):
        #combo = self.entry.GetCombo()
        self.cc.SetBackgroundColour(self.g.makeColour(bgColor))
        self.cc.SetForegroundColour(self.g.makeColour(fgColor))
 


class Label(wx.lib.stattext.GenStaticText):
    # ***** deprecated *****
    # this class is set to disappear soon!
    #
    # auxiliary class for labels (static text)
    # will show a short descriptive string and
    # generate a longer tooltip.
    # the tooltip is also associated to the text control(s)
    # 'txtlist' can be a scalar (just one control) or a list
    # of controls. 'tiplist' is expected to be the same type
    # and length as 'txtlist'
    # a default length is also managed.
    w0 = None
    w1 = None
    def __init__(self,parent,txtlist,text,tiplist,width0=None,width1=None,style=0):
        wx.lib.stattext.GenStaticText.__init__(self,ID=-1,parent=parent,label='',
                                              style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
        self.SetLabel(text)
        # sets sizes
        h = self.GetMinHeight()
        if width0 is None:
            if Label.w0 is not None:
                self.SetMinSize((Label.w0, h))
        else:
            Label.w0 = width0
            self.SetMinSize((Label.w0, h))
        if width1 is None:
            if Label.w1 is not None:
                if 'list' in str(type(txtlist)):
                    # list of controls
                    for tc  in txtlist:
                        tc.SetMinSize((Label.w1, h))
                else:
                    # just one control
                    txtlist.SetMinSize((Label.w1, h))
        else:
            Label.w1 = width1
            if 'list' in str(type(txtlist)):
                for tc  in txtlist:
                    tc.SetMinSize((width1, h))
            else:
                txtlist.SetMinSize((width1, h))
        # sets tooltips
        if 'list' in str(type(txtlist)):
            self.SetToolTipString(tiplist[0])
            for i in range(len(txtlist)):
                if len(tiplist[i].strip()) > 0:
                    txtlist[i].SetToolTipString(tiplist[i])
        else:
            if len(tiplist.strip()) > 0:
                self.SetToolTipString(tiplist)
                txtlist.SetToolTipString(tiplist)


