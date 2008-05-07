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
#	Version No.: 0.01
#	Created by: 	    Tom Sobota 06/05/2008
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
from wx.lib.stattext import *

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

