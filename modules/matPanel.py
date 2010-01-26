#!/usr/bin/env python
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	matPanel- Auxiliary GUI component for graphics
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Tom Sobota	16/03/2008
#
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

import new
import matplotlib
matplotlib.interactive(False)
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
import wx

WHITE=(255,255,255)

#############################################################
#
# Dynamically loaded methods.
# These methods are loaded as methods of the instance of
# the widget where the drawing will be done.
#
#############################################################
#
# 1. invariable methods. these are the same for all graphics
#
#############################################################

def setFigure(self, color = None, dpi = None):
    self.figure = Figure(None, dpi)
    self.canvas = FigureCanvasWxAgg(self, -1, self.figure)
    self.setColor(color)
    self.Bind(wx.EVT_IDLE, self.onIdle)
    self.Bind(wx.EVT_SIZE, self.onSize)
    self.resizeflag = True
    #self.setSize()
    self.params = {}
#    print 'setFigure'

def setColor(self, rgbtuple):
    """
    Set figure and canvas colours to be the same
    """
    if not rgbtuple:
        rgbtuple = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE).Get()
    col = [c/255.0 for c in rgbtuple]
    self.figure.set_facecolor(col)
    self.figure.set_edgecolor(col)
    self.canvas.SetBackgroundColour(wx.Colour(*rgbtuple))

def setParams(self, params):
    """
    Set params for the graphic
    """
    self.params = params
    
def setSize(self, pixels = None):
    """
    This method can be called to force the Plot to be a desired size, which defaults to
    the ClientSize of the panel
    """
    if not pixels:
        pixels = self.GetClientSize()
    self.canvas.SetSize(pixels)
#    self.figure.set_figsize_inches(pixels[0]/self.figure.get_dpi(), pixels[1]/self.figure.get_dpi())
    self.SetSize(pixels)

def onSize(self, event):
    """
    called after resizing. sets a flag for the next onIdle event
    """
    self.resizeflag = True

def onIdle(self, evt):
    """
    the actual repainting of the figure is done here
    """
#    if self.resizeflag:
#        self.resizeflag = False
#        self.setSize()
#        try:
#            self.draw()
#        except:
#            print "MatPanel (onIdle): error in function draw"
    pass

#############################################################
#
# 2. MatPanel class definition
#
#############################################################

class MatPanel(object):
    def __init__(self, widget_instance, widget_class, drawFunction, params=None):
        # dynamically adds methods to the panel instance
        # widget_instance: wx widget instance where the drawing is done
        # widget_class: wx widget class of 'widget_instance'
        # drawFunction: an external function to generate the drawing (using matplotlib)
        #
        widget_instance.draw = new.instancemethod(drawFunction, widget_instance, widget_class)
        widget_instance.setSize = new.instancemethod(setSize, widget_instance, widget_class)
        widget_instance.setColor = new.instancemethod(setColor, widget_instance, widget_class)
        widget_instance.onSize = new.instancemethod(onSize, widget_instance, widget_class)
        widget_instance.onIdle = new.instancemethod(onIdle, widget_instance, widget_class)
        widget_instance.setFigure = new.instancemethod(setFigure, widget_instance, widget_class)
        widget_instance.setParams = new.instancemethod(setParams, widget_instance, widget_class)

        # configure the panel
        widget_instance.setFigure(WHITE)
        
        widget_instance.setSize()

        if params is not None:
            widget_instance.setParams(params)

