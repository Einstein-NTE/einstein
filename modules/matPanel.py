#!/usr/bin/env python

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
    self.setSize()

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

def setSize(self, pixels = None):
    """
    This method can be called to force the Plot to be a desired size, which defaults to
    the ClientSize of the panel
    """
    if not pixels:
        pixels = self.GetClientSize()
    self.canvas.SetSize(pixels)
    self.figure.set_figsize_inches(pixels[0]/self.figure.get_dpi(), pixels[1]/self.figure.get_dpi())

def onSize(self, event):
    """
    called after resizing. sets a flag for the next onIdle event
    """
    self.resizeflag = True

def onIdle(self, evt):
    """
    the actual repainting of the figure is done here
    """
    if self.resizeflag:
        self.resizeflag = False
        self.setSize()
        self.draw()

#############################################################
#
# 2. MatPanel class definition
#
#############################################################

class MatPanel(object):
    def __init__(self, widget_instance, widget_class, drawFunction):
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

        # configure the panel
        widget_instance.setFigure(WHITE)
        widget_instance.setSize()


if __name__ == "__main__":
    # example for testing.
    # call: python matPanel.py
    #
    def draw(self):
        #
        # this function produces the drawing
        # on a wx widget usin matplotlib
        #
        from matplotlib.numerix import arange, sin, cos, pi
        if not hasattr(self, 'subplot'):
            self.subplot = self.figure.add_subplot(1,1,1)
        theta = arange(0, 45*2*pi, 0.02)
        rad = (0.8*theta/(2*pi)+1)
        r = rad*(8 + sin(theta*7+rad/1.8))
        x = r*cos(theta)
        y = r*sin(theta)
        # now draw it
        self.subplot.plot(x,y, '-r')
        # set some plot attributes
        self.subplot.set_title("Una estrella polar (%s puntos)"%len(x), fontsize = 12)
        self.subplot.set_xlabel("La flor es de  http://www.physics.emory.edu/~weeks/ideas/rose.html",
                                fontsize = 8)
        self.subplot.set_xlim([-400, 400])
        self.subplot.set_ylim([-400, 400])


    class TestMatPanel(object):
        #
        # class for testing MatPanel
        # instantiates a wx frame with a wx panel
        # and draws on the panel using the 'draw' function
        # declared above.
        #
        def __init__(self):
            # create a frame ...
            self.frame = wx.Frame(None, -1, 'WxPython and Matplotlib example')

            # Make a child plot panel...
            self.panel = wx.Panel(self.frame)

            dummy = MatPanel(self.panel,wx.Panel,draw)

            # show all
            self.frame.Show()
        
        
    app = wx.PySimpleApp(0)
    t = TestMatPanel()
    app.MainLoop()
