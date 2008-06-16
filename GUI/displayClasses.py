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
#	Version No.: 0.04
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
import locale
import wx
import wx.lib.masked.numctrl
import wx.lib.intctrl
import wx.lib.stattext
import wx.lib.masked

CHOOSERBCGCOLOR = (250,250,230)
TEXTBKGCOLOR    = (250,250,255)

class FieldSizes(object):
    # sizes of subwidgets
    labelWidth=100
    dataWidth=200
    unitsWidth=80
    totalWidth = labelWidth + dataWidth + unitsWidth
    Height=32
    # font parameters
    fontSize=10
    fontFamily=wx.FONTFAMILY_ROMAN
    fontStyle=wx.FONTSTYLE_NORMAL
    fontWeight=wx.FONTWEIGHT_NORMAL
    fontUnderline=False
    fontFacename='Verdana'
    #fontEncoding = wx.FONTENCODING_DEFAULT
    
    def __init__(self, wHeight=None, wLabel=None,wData=None,wUnits=None,
                 fSize=None, fFamily=None, fStyle=None, fWeight=None,
                 fUnderline=None, fFacename=None, fEncoding=None):
        #---------------------------------------------------------------
        # stores the default properties for font and field sizes
        #---------------------------------------------------------------
        # font properties
        # family constants:
        # wx.FONTFAMILY_DEFAULT, wx.FONTFAMILY_DECORATIVE, wx.FONTFAMILY_ROMAN,
        # wx.FONTFAMILY_SCRIPT, wx.FONTFAMILY_SWISS, wx.FONTFAMILY_MODERN,
        # wx.FONTFAMILY_TELETYPE
        #
        # style constants:
        # wx.FONTSTYLE_NORMAL, wx.FONTSTYLE_SLANT and wx.FONTSTYLE_ITALIC
        #
        # weight constants:
        # wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_LIGHT, wx.FONTWEIGHT_BOLD
        #
        if fSize is not None: FieldSizes.fontSize=fSize
        if fFamily is not None: FieldSizes.fontFamily=fFamily
        if fStyle is not None: FieldSizes.fontStyle=fStyle
        if fWeight is not None: FieldSizes.fontWeight=fWeight
        if fUnderline is not None: FieldSizes.fontUnderline=fUnderline
        if fFacename is not None: FieldSizes.fontFacename=fFacename
        #if fEncoding is not None: FieldSizes.fontEncoding=fEncoding
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
            dlg = wx.MessageDialog(None,'Error in FieldSizes: wHeight=%s, wLabel=%s,wData=%s,wUnits=%s' % \
                                   (wHeight,wLabel,wData,wUnits),'Error',wx.OK | wx.ICON_ERROR)
            ret = dlg.ShowModal()
            dlg.Destroy()

            
class Generics(object):
    def makeColour(self, something):
        if isinstance(something,tuple):
            try:
                newcolor = wx.Colour(something[0],something[1],something[2])
                something = newcolor
            except:
                dlg = wx.MessageDialog(None,
                                       repr(something)+' is not a valid color, sorry', 'Error',
                                       wx.OK | wx.ICON_ERROR)
                ret = dlg.ShowModal()
                dlg.Destroy()
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
        if other.hasunits:
            other.units.Clear()
            try:
                if unitdict.__class__.__name__ == 'dict':
                    for u in unitdict.keys():
                        other.units.Append(u)
                elif unitdict.__class__.__name__ == 'list':
                    for u in unitdict:
                        other.units.Append(u)
                else:
                    dlg = wx.MessageDialog(None,
                                           repr(unitdict)+' is not a dictionary or a list', 'Error',
                                           wx.OK | wx.ICON_ERROR)
                    ret = dlg.ShowModal()
                    dlg.Destroy()
            except:
                pass
            other.units.SetToolTipString(tip)
            other.units.SetSelection(0)


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


    def fillChoice(self,other,choice,choiceList,preselected=0,nonePossible=True):
        #
        #   fills the list of possible choices from a list of strings
        #
        other.choice.Clear()
        if nonePossible==True:
            other.choice.Append("None")
        for c in choiceList:
            other.choice.Append(str(c))
        try:
            other.choice.SetSelection(preselected)
        except:
            other.choice.SetSelection(0)

    def setChoice(self, other, choice, strChoice):
        #
        #   sets a choice to the string
        #
        try:
            other.choice.SetSelection(other.choice.FindString(strChoice))
        except:
            try:
                other.choice.SetSelection(other.choice.FindString("None"))
            except:
                other.choice.SetSelection(0)

    def __sz(self,alist):
        for a in alist:
            if a is not None:
                return a
    
    def setFont(self, other, size=None, family=None, style=None, weight=None,
                underline=None, facename=None, encoding=None, font=None):
        self.resetFont(other)
        if font is not None:
            # a full wx.Font specification.
            # in this case the rest of args are ignored
            try:
                if font.__class__.__name__ == 'Font':
                    other.SetFont(font)
                    return
            except:
                pass
        try:
            si = self.__sz([size,FieldSizes.fontSize,10])
            fa = self.__sz([family,FieldSizes.fontFamily,wx.FONTFAMILY_DEFAULT])
            st = self.__sz([style,FieldSizes.fontStyle,wx.FONTSTYLE_NORMAL])
            we = self.__sz([weight,FieldSizes.fontWeight,wx.FONTWEIGHT_NORMAL])
            fn = self.__sz([facename,FieldSizes.fontFacename,'Roman'])
            un = self.__sz([underline,FieldSizes.fontUnderline,False])
            #en = self.__sz([encoding,FieldSizes.fontEncoding,wx.FONTENCODING_SYSTEM])
            fnt = wx.Font(si,fa,st,we)
            #fnt.SetFaceName(fn)
            fnt.SetUnderlined(un)
            #fnt.SetDefaultEncoding(en)
            other.SetFont(fnt)
        except:
            # some error in font specification. notify
            dlg = wx.MessageDialog(None,
                                   'Error in font specification, sorry', 'Error',
                                   wx.OK | wx.ICON_ERROR)
            ret = dlg.ShowModal()
            dlg.Destroy()

    def resetFont(self, other):
        # reset font to initial values
        si=FieldSizes.fontSize
        fa=FieldSizes.fontFamily
        st=FieldSizes.fontStyle
        we=FieldSizes.fontWeight
        un=FieldSizes.fontUnderline
        fn=FieldSizes.fontFacename
        #en=FieldSizes.fontEncoding
        font = wx.Font(si,fa,st,we)
        #font.SetFaceName(fn)
        font.SetUnderlined(un)
        #font.SetDefaultEncoding(en)
        other.SetFont(font)

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
                                               value=value,allowNone=True,
                                               selectOnEntry=True,
                                               allowNegative=allowNegative,
                                               min=min,max=max,
                                               integerWidth=integerWidth,
                                               fractionWidth=fractionWidth,
                                               foregroundColour=foregroundColour,
                                               signedForegroundColour=signedForegroundColour,
                                               emptyBackgroundColour=emptyBackgroundColour,
                                               validBackgroundColour=validBackgroundColour,
                                               invalidBackgroundColour=invalidBackgroundColour,
                                               autoSize=False)
        self.SetAutoSize(False)
        self.SetMaxSize(size)
        # get a dictionary of local parameters
        loc = locale.localeconv()
        #for key in loc.keys():
        #    print 'LOC[%s] = [%s]' % (key,loc[key])
        self.SetDefaultValue('')
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
                 allow_long=True,
                 allow_none=True,
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
                                        allow_long=allow_long,allow_none=allow_none,
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
                 unitdict={},                                  # unit dict for the unit selector
                 wLabel=None,                                  # width of the label
                 wData=None,                                   # width of the data entry
                 wUnits=None,                                  # width of the unit selector
                 label='',                                     # text of the label
                 tip='',                                       # text of the tip
                 hasunits=True,                                # unit selector shown?
                 fontsize=None,                                # fontsize for subwidgets
                 font=None):                                   # full wx.Font specification
        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.hasunits = hasunits
        self.g = Generics()

        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,True,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            sty = wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT|wx.BORDER_NONE
            #self.label = wx.lib.stattext.GenStaticText(self,ID=-1,label=label,size=lblSize,pos=(0,0),style = sty)
            self.label = wx.StaticText(self,id=-1,label=label,size=lblSize,pos=(0,0),style = sty)
            self.g.setFont(self.label,size=fontsize,font=font)
            self.label.Wrap(lblSize.GetWidth())

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
                integerWidth=ipart,                  # size of integer part
                fractionWidth=decimals,              # number of decimals
                value=value,                         # initial value
                style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
        self.g.setFont(self.entry,size=fontsize,font=font)


        # load and show a unit selector
        if self.hasunits:
            self.units = wx.Choice(self, -1, pos=(lblSize[0]+datSize[0]+2,0),
                                     choices=[], size=uniSize)
            self.setUnits('Select a measurement unit', unitdict)
            backgroundcolour = self.g.makeColour(CHOOSERBCGCOLOR)
            self.units.SetBackgroundColour(backgroundcolour)
            self.g.setFont(self.units,size=fontsize,font=font)

        # set tooltips
        self.g.setTooltips(self,tip)


    def setUnits(self,tip,unitdict):
        self.g.setUnits(self,tip, unitdict)

    def GetValue(self):
        return str(self.entry.GetValue())

    def SetValue(self, value):
        try:
            f = float(value)
            self.entry.SetValue(f)
        except:
            self.entry.SetValue(0.0)

    def GetUnit(self,text=False):
        return self.g.getChoiceValues(self.units, False, text)

    def setUnit(self,n):
        # n is the 0-based index to the contents
        self.units.SetSelection(n)
    


class IntEntry(wx.Panel):
    def __init__(self, parent=None,
                 minval=None,                                  # min value
                 maxval=None,                                  # max value
                 value=0,                                      # initial value
                 unitdict={},                                  # unit dict for the unit selector
                 wLabel=None,                                  # width of the label
                 wData=None,                                   # width of the data entry
                 wUnits=None,                                  # width of the unit selector
                 label='',                                     # text of the label
                 tip='',                                       # text of the tip
                 hasunits=True,                                # unit selector shown?
                 fontsize=None,
                 font=None):                                   # full wx.Font specification
        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.hasunits = hasunits
        self.g = Generics()

        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,True,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            self.label = wx.lib.stattext.GenStaticText(self,ID=-1,label=label,size=lblSize,pos=(0,0),
                                                       style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
            self.g.setFont(self.label,size=fontsize,font=font)

        # create a masked fixed-point control
        self.entry = MskIC(self,pos=(lblSize[0]+1,0),
                           size=datSize,                       # size of control
                           min=minval,                       # minimum value admitted
                           max=maxval,                       # maximum value admitted
                           value=value,                      # initial value
                           style=wx.ALIGN_RIGHT)
        self.g.setFont(self.entry,size=fontsize,font=font)

        # load and show a unit selector
        if self.hasunits:
            self.units = wx.Choice(self, -1, pos=(lblSize[0]+datSize[0]+2,0),
                                     choices=[], size=uniSize)
            self.setUnits('Select a measurement unit', unitdict)
            backgroundcolour = self.g.makeColour(CHOOSERBCGCOLOR)
            self.units.SetBackgroundColour(backgroundcolour)
            self.g.setFont(self.units,size=fontsize,font=font)

        # set tooltips
        self.g.setTooltips(self,tip)


    def setUnits(self,tip,unitdict):
        self.g.setUnits(self,tip, unitdict)

    def GetValue(self):
        return str(self.entry.GetValue())

    def SetValue(self, value):
        try:
            j = int(value)
            self.entry.SetValue(j)
        except:
            self.entry.SetValue(0)

    def GetUnit(self,text=False):
        return self.g.getChoiceValues(self.units, False, text)

    def setUnit(self,n):
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
                 fontsize=None,
                 font=None):                                   # full wx.Font specification

        self.hasunits = False
        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.g = Generics()

        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,False,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            self.label = wx.lib.stattext.GenStaticText(self,ID=-1,label=label,size=lblSize,pos=(0,0),
                                                       style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
            self.g.setFont(self.label,size=fontsize,font=font)

        # create a text control
        self.entry = wx.TextCtrl(self,-1,pos=(lblSize[0]+1,0),
                                 value=value,size=datSize,style=wx.ALIGN_RIGHT)
        self.g.setFont(self.entry,size=fontsize,font=font)

        foregroundColour=(0,0,100)
        foregroundColour = self.g.makeColour(foregroundColour)
        validBackgroundColour = self.g.makeColour(TEXTBKGCOLOR)
        self.entry.SetForegroundColour(foregroundColour)
        self.entry.SetBackgroundColour(validBackgroundColour)
        if maxchars is not None:
            self.entry.SetMaxLength(maxchars)

        # set tooltips
        self.g.setTooltips(self,tip)


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
                 fontsize=None,
                 font=None):     # full wx.Font specification

        self.hasunits = False
        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.g = Generics()
        locale.setlocale(locale.LC_ALL, '')

        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,True,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            self.label = wx.lib.stattext.GenStaticText(self,ID=-1,label=label,size=lblSize,pos=(0,0),
                                                       style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
            self.g.setFont(self.label,size=fontsize,font=font)

        # create a masked control
        self.entry  = wx.lib.masked.TextCtrl(self, -1, "", pos=(lblSize[0]+1,0),
                                             mask         = "##/##/####",
                                             excludeChars = "",
                                             formatcodes  = "DF>",
                                             includeChars = "",
                                             validRegex   = "",
                                             validRange   = "",
                                             choices      = "",
                                             choiceRequired = False,
                                             defaultValue = wx.DateTime_Now().Format("%d/%m/%Y"),
                                             size         = datSize,
                                             style        = wx.ALIGN_RIGHT)
        self.g.setFont(self.entry,size=fontsize,font=font)

        foregroundColour=(0,0,100)
        foregroundColour = self.g.makeColour(foregroundColour)
        validBackgroundColour = self.g.makeColour(TEXTBKGCOLOR)
        self.entry.SetForegroundColour(foregroundColour)
        self.entry.SetBackgroundColour(validBackgroundColour)

        # set tooltips
        self.g.setTooltips(self,tip)


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



class ChoiceEntry(wx.Panel):
    def __init__(self, parent=None,
                 multiple=False,  # admits choosing multiple elements?
                 values=[],       # initial values list
                 wLabel=None,     # width of the label
                 wData=None,      # width of the data entry
                 wUnits=None,     # width of the unit selector (not used)
                 label='',        # text of the label
                 tip='',          # text of the tip
                 fontsize=None,
                 font=None):      # full wx.Font specification

        self.hasunits = False
        self.multiple = multiple
        style = wx.NO_BORDER|wx.TAB_TRAVERSAL
        self.g = Generics()

        (size,lblSize,datSize,uniSize) = self.g.setSizes(wLabel,wData,False,wUnits)

        wx.Panel.__init__(self, parent, id=-1, size=size, style=style)

        if label.strip():
            # creates label
            self.label = wx.lib.stattext.GenStaticText(self,ID=-1,pos=(0,0),
                                                       label=label,size=lblSize,
                                                       style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT)
            self.g.setFont(self.label,size=fontsize,font=font)

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
        self.g.setFont(self.entry,size=fontsize,font=font)

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



if __name__ == '__main__':
    global ce
    def OnButtonOK(event):
        global ce
        print repr(ce.GetValue(text=True))

    app = wx.PySimpleApp()
    frame = wx.Frame(parent=None, id=-1, size=wx.Size(500, 80), title="Einstein - displayClasses test")

    ce = ChoiceEntry(parent=frame,
                     multiple=False,
                     values=['one','two','three'],
                     wLabel=200,
                     wData=200,
                     label='This is the label',
                     tip='This is a tip')

    buttonOK = wx.Button(frame,wx.ID_OK, 'OK')
    frame.Bind(wx.EVT_BUTTON, OnButtonOK, buttonOK)

    sizer_1 = wx.BoxSizer(wx.VERTICAL)
    sizer_1.Add(ce, 1, wx.ALL|wx.EXPAND, 5)
    sizer_1.Add(buttonOK, 0, 0, 1)
    frame.SetSizer(sizer_1)
    frame.Layout()

    frame.Show(True)
    app.MainLoop()


