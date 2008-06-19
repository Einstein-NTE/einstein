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
#	displayClasses: Some useful classes for panel display
#
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Tom Sobota 06/06/2008
#
#       Changes to previous version:
#       TS20080530          Added several classes for data display and edition
#       06/06/2008: TS      Some changes for Stoyan's panel changes
#       14/06/2008: TS      Added multiple choices,
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
import wx
import wx.lib.masked.numctrl
import wx.lib.intctrl
import wx.lib.stattext
import wx.lib.masked
from status import Status
import units
from fonts import FontProperties

CHOOSERBCGCOLOR = (255,255,255)
TEXTBKGCOLOR    = (255,255,255)
LOWERACCEPTEDDATE = '01/02/1970'
UPPERACCEPTEDDATE = '12/31/2050'

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
                if unitdict.__class__.__name__ == 'str':
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
                # return the text of the selections
                # first get the indices
                ituple = other.GetSelections()
                slist = []
                # then look for the text of each index
                for i in ituple:
                    slist.append(other.GetString(i))
                return tuple(slist)
                    
            else:
                # we return a tuple with the indices of the selections
                return other.GetSelections()
        else:
            # single values can be selected
            if text:
                # return a tuple with the texts of the selections
                return other.GetStringSelection()
            else:
                # we return the index of the (single) selection
                return other.GetCurrentSelection()



        
class MskFC(wx.lib.masked.numctrl.NumCtrl):
    def __init__(self, prnt,
                 id=-1,
                 pos=wx.DefaultPosition,
                 size=(100,32),
                 min= None,
                 max= None,
                 foregroundColour=(0,0,0),
                 signedForegroundColour=(0,0,0),
                 emptyBackgroundColour=TEXTBKGCOLOR,
                 validBackgroundColour=TEXTBKGCOLOR,
                 invalidBackgroundColour=(255,250,250),
                 style=0,
                 value=0.0,
                 allowNegative=True,
                 allowNone=True,
                 integerWidth=10,
                 fractionWidth=2):
        u = Generics()
        foregroundColour = u.makeColour(foregroundColour)
        signedForegroundColour = u.makeColour(signedForegroundColour)
        emptyBackgroundColour = u.makeColour(emptyBackgroundColour)
        validBackgroundColour = u.makeColour(validBackgroundColour)
        invalidBackgroundColour = u.makeColour(invalidBackgroundColour)
        
        wx.lib.masked.numctrl.NumCtrl.__init__(self,id=id,parent=prnt,
                                               pos=pos,
                                               size=size,style=style,
                                               value=value,
                                               selectOnEntry=False,
                                               allowNegative=allowNegative,
                                               allowNone=allowNone,
                                               min=min,max=max,
                                               integerWidth=integerWidth,
                                               fractionWidth=fractionWidth,
                                               foregroundColour=foregroundColour,
                                               signedForegroundColour=signedForegroundColour,
                                               emptyBackgroundColour=emptyBackgroundColour,
                                               validBackgroundColour=validBackgroundColour,
                                               invalidBackgroundColour=invalidBackgroundColour,
                                               autoSize=False)
        #self.SetAutoSize(False)
        self.SetLimited(False)
        #self.SetAllowNone(True)
        self.SetMaxSize(size)
        # get a dictionary of local parameters
        loc = locale.localeconv()
        #for key in loc.keys():
        #    print 'LOC[%s] = [%s]' % (key,loc[key])
        #self.SetDefaultValue('')
        # extract decimal and thousands separator from
        # locale and use them to setup this control
        #
        # a hack, necessary to avoid the error that is produced when
        # groupchar and decimalchar are the same
        self.SetDecimalChar(';')
        try:
            tsep = loc['thousands_sep']
            if tsep:
                self.SetGroupChar(tsep)
                self.SetGroupDigits(True)
            else:
                self.SetGroupChar(' ') # dummy
                self.SetGroupDigits(False)

            # now set the 'real' decimal char
            self.SetDecimalChar(loc['decimal_point'])
        except:
            # some error. use European notation
            self.SetGroupChar('.')
            self.SetDecimalChar(',')

class MskIC(wx.lib.intctrl.IntCtrl):
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
                 ipart=6,                                      # max digits in the integer part
                 decimals=2,                                   # digits in the fraction
                 minval=None,                                  # min value
                 maxval=None,                                  # max value
                 value=0.,                                     # initial value
                 unitdict=None,                                # unit dict for the unit selector
                 wLabel=None,                                  # width of the label
                 wData=None,                                   # width of the data entry
                 wUnits=None,                                  # width of the unit selector
                 label='',                                     # text of the label
                 tip='',                                       # text of the tip
                 fontsize=None):                                # fontsize for subwidgets

        self.unitdict = unitdict
        self.lastInternalValue = None
        self.defaultDisplayUnit = None
        self.lastTypedString = ''

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
        self.entry = MskFC(self,pos=(lblSize[0]+1,0),
                size=datSize,                        # size of control
                min=minval,                          # minimum value admitted
                max=maxval,                          # maximum value admitted
                foregroundColour=(0,0,100),          # dark blue
                signedForegroundColour=(0,255,0),    # green
                emptyBackgroundColour=TEXTBKGCOLOR,  # white
                validBackgroundColour=TEXTBKGCOLOR,  # very light blue
                invalidBackgroundColour=(255,255,0), # yellow
                allowNegative=True,                  # negative values allowed?
                allowNone=True,                      # empty value allowed?
                integerWidth=ipart,                  # size of integer part
                fractionWidth=decimals,              # number of decimals
                style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
        self.f.setFont(self.entry,size=fontsize)
        self.entry.Center(wx.VERTICAL)
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
            
    def OnEntry(self, event):
        s = event.GetString()
        self.lastTypedString = s
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
        # trick for detecting a Null value
        if self.lastTypedString.strip() == u',00' or self.lastTypedString.strip() == u'.00':
            return None
        if self.defaultDisplayUnit is None:
            return dValue
        try:
            iValue = units.internalValue(dValue,self.defaultDisplayUnit,self.unitdict)
            return iValue
        except:
            print 'FloatEntry: error in conversion disp->int ' \
                  'disp=%s class=%s default=%s' % (dValue,self.unitdict,
                                                   repr(self.defaultDisplayUnit))

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
                f = float(iValue)
            except:
                print 'FloatEntry: bad value for SetValue ' % (repr(iValue),)
                self.entry.SetValue(0.0)
                return
            
            if self.defaultDisplayUnit is None:
                dValue = f
            else:
                try:
                    dValue = units.displayValue(f,self.defaultDisplayUnit,self.unitdict)
                except:
                    print 'FloatEntry: error in conversion int->disp ' \
                          'int=%s class=%s default=%s' % (f, self.unitdict,
                                                          repr(self.defaultDisplayUnit))

                self.entry.SetValue(dValue)

    def GetUnit(self,text=False):
        if self.unitdict:
            return self.g.getChoiceValues(self.units, False, text)
        else:
            return None

    def setUnit(self,n):
        if self.unitdict:
            # n is the 0-based index to the contents
            self.units.SetSelection(n)



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
        self.entry = MskIC(self,pos=(lblSize[0]+1,0),
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
        if self.defaultDisplayUnit is None:
            return dValue
        try:
            iValue = units.internalValue(float(dValue),self.defaultDisplayUnit,self.unitdict)
            return int(iValue)
        except:
            print 'IntEntry: error in conversion disp->int '\
                  'disp=%s class=%s default=%s' % (dValue,self.unitdict,
                                                   repr(self.defaultDisplayUnit))


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
                f = int(iValue)
            except:
                print 'IntEntry: bad value for SetValue ' % (repr(iValue),)
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

        foregroundColour=(0,0,100)
        foregroundColour = self.g.makeColour(foregroundColour)
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
        return self.entry.GetValue()

    def SetValue(self, value):
        self.entry.SetValue(value)
    
    def getUnit(self):
        # this method is just for compatibility
        return None

    def setUnit(self,value):
        # this method is just for compatibility
        pass



class DateEntry(wx.Panel):
    def __init__(self, parent=None,
                 value='',       # initial value
                 wLabel=None,    # width of the label
                 wData=None,     # width of the data entry
                 wUnits=None,    # width of the unit selector (not used)
                 label='',       # text of the label
                 tip='',         # text of the tip
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


        self.entry = wx.DatePickerCtrl(self, id=-1, pos=(lblSize[0]+1,0), size=datSize,
                                style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.entry.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

        # sets range of accepted values
        lowerLimit = wx.DateTime()
        lowerLimit.ParseDate(LOWERACCEPTEDDATE)
        upperLimit = wx.DateTime()
        upperLimit.ParseDate(UPPERACCEPTEDDATE)
        self.entry.SetRange(lowerLimit, upperLimit)

        self.SetValue(value)

        self.f.setFont(self.entry,size=fontsize)

        foregroundColour=(0,0,100)
        foregroundColour = self.g.makeColour(foregroundColour)
        validBackgroundColour = self.g.makeColour(TEXTBKGCOLOR)
        self.entry.SetForegroundColour(foregroundColour)
        self.entry.SetBackgroundColour(validBackgroundColour)

        # set tooltips
        self.g.setTooltips(self,tip)

        # create popup menu for easy clearing/setting to zero
        self.popupmenu = wx.Menu()
        for text in "Today|Unknown (sets date to 1/1/1970)".split('|'):
            item = self.popupmenu.Append(-1, text)
            self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)

    def OnShowPopup(self, event):
        pos = event.GetPosition()
        pos = self.ScreenToClient(pos)
        self.PopupMenu(self.popupmenu, pos)

    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        if text.startswith('Unknown'):
            self.SetValue('1/1/1970')
        elif text == 'Today':
            theDate = wx.DateTime().Today()
            y = theDate.GetYear()
            m = theDate.GetMonth()
            d = theDate.GetDay()
            self.SetValue('%02d/%02d/%4d' % (m+1,d,y))

    def setUnits(self,tip,unitdict):
        # this method is just for compatibility
        pass

    def GetValue(self):
        theDate = self.entry.GetValue()
        y = theDate.GetYear()
        m = theDate.GetMonth()
        d = theDate.GetDay()
        if y == 1970 and m == 0 and d == 1:
            # campo vacío
            return None
        # campo con fecha
        return '%4d/%02d/%02d' % (y,m+1,d)

    def SetValue(self, value):
        if not value:
            value = '1/1/1970'

        theDate = wx.DateTime()
        theDate.ParseDate(value)
        self.entry.SetValue(theDate)
    
    def getUnit(self):
        # this method is just for compatibility
        return None

    def setUnit(self,value):
        # this method is just for compatibility
        pass



class ChoiceEntry(wx.Panel):
    def __init__(self, parent=None,
                 multiple=False,  # admits choosing multiple elements?
                 values=[],       # initial values list
                 wLabel=None,     # width of the label
                 wData=None,      # width of the data entry
                 wUnits=None,     # width of the unit selector (not used)
                 label='',        # text of the label
                 tip='',          # text of the tip
                 fontsize=None):

        self.multiple = multiple
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

        if multiple:
            # if multiple choice, create a listbox
            self.entry = wx.ListBox(self, -1, pos=(lblSize[0]+1,0),
                                    choices=values, size=datSize,
                                    style=wx.LB_MULTIPLE|wx.LB_ALWAYS_SB)
        else:
            #create a choice control
            self.entry = wx.Choice(self, -1, pos=(lblSize[0]+1,0),
                                   choices=values, size=datSize)
        backgroundcolour = self.g.makeColour(CHOOSERBCGCOLOR)
        self.entry.SetBackgroundColour(backgroundcolour)
        self.f.setFont(self.entry,size=fontsize)

        # set tooltips
        self.g.setTooltips(self,tip)


    def setUnits(self,tip,unitdict):
        # this method is just for compatibility
        pass

    def GetValue(self,text=False):
        return self.g.getChoiceValues(self.entry, self.multiple, text)

    def SetValue(self, thing=0):
        # this method has triple functionality:
        # if 'thing' is an integer n, the choice will show the nth element. 
        # if 'thing' is a string, the choice will show the element that contains the string
        # if 'thing' is a list, the elements of the list will be loaded in the choice.
        try:
            t = thing.__class__.__name__
            if t == 'int':
                try:
                    self.entry.SetSelection(thing)
                except:
                    self.entry.SetSelection(0)
            elif t == 'str':
                if thing.strip() == '':
                    # clear the choice
                    self.entry.Clear()
                    return
                try:
                    self.entry.SetSelection(self.entry.FindString(thing))
                except:
                    try:
                        self.entry.SetSelection(self.entry.FindString("None"))
                    except:
                        self.entry.SetSelection(0)

            elif t == 'list':
                # thing is a list of values for the choice control
                self.entry.Clear()
                self.entry.Append("None")
                for item in thing:
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



class Label(wx.lib.stattext.GenStaticText):
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


