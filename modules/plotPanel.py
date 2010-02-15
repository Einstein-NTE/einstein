#import matplotlib
#matplotlib.interactive( True )
#matplotlib.use( 'WXAgg' )
#
#import numpy as num
#import wx
#
#class PlotPanel (wx.Panel):
#    """The PlotPanel has a Figure and a Canvas. OnSize events simply set a 
#flag, and the actual resizing of the figure is triggered by an Idle event."""
#    def __init__( self, parent, color=None, dpi=None, **kwargs ):
#        from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
#        from matplotlib.figure import Figure
#
#        # initialize Panel
#        if 'id' not in kwargs.keys():
#            kwargs['id'] = wx.ID_ANY
#        if 'style' not in kwargs.keys():
#            kwargs['style'] = wx.NO_FULL_REPAINT_ON_RESIZE
#        wx.Panel.__init__( self, parent, **kwargs )
#
#        # initialize matplotlib stuff
#        self.figure = Figure( None, dpi )
#        self.canvas = FigureCanvasWxAgg( self, -1, self.figure )
#        self.SetColor( color )
#
#        self._SetSize()
#        self.draw()
#
#        self._resizeflag = False
#
#        self.Bind(wx.EVT_IDLE, self._onIdle)
#        self.Bind(wx.EVT_SIZE, self._onSize)
#
#    def SetColor( self, rgbtuple=None ):
#        """Set figure and canvas colours to be the same."""
#        if rgbtuple is None:
#            rgbtuple = wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ).Get()
#        clr = [c/255. for c in rgbtuple]
#        self.figure.set_facecolor( clr )
#        self.figure.set_edgecolor( clr )
#        self.canvas.SetBackgroundColour( wx.Colour( *rgbtuple ) )
#
#    def _onSize( self, event ):
#        self._resizeflag = True
#
#    def _onIdle( self, evt ):
#        if self._resizeflag:
#            self._resizeflag = False
#            self._SetSize()
#
#    def _SetSize( self ):
#        pixels = tuple( self.parent.GetClientSize() )
#        self.SetSize( pixels )
#        self.canvas.SetSize( pixels )
#        self.figure.set_size_inches( float( pixels[0] )/self.figure.get_dpi(),
#                                     float( pixels[1] )/self.figure.get_dpi() )
#
#    def draw(self): pass # abstract, to be overridden by child classes
