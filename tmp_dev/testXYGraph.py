# -*- coding: iso-8859-15 -*-
import random
from numpy import *
import wx
from einstein.modules.interfaces import *
import einstein.modules.matPanel as Mp
from einstein.GUI.graphics import drawStackedBarPlot

def drawFigure(self):
    #
    # title properties dictionary
    #
    TITLE_FONT_DICT = {'fontname'  : 'Roman',
                       'fontweight': 'bold',
                       'color'     : '#808080',
                       'fontsize'  : 14}
    
    key = self.params['key']
    data = Interfaces.GData[key]
    (rows,cols) = data.shape
    linecolors = self.params['linecolors']
    labeltexts = self.params['labeltexts']

    x = data[0]
    xmax = max(x)
    ymax = -1e32

    if hasattr(self, 'subplot'):
        del self.subplot

    self.subplot = self.figure.add_subplot(1,1,1)

    for i in range(1,rows):
        self.subplot.plot(x, data[i], linecolors[i-1], label=labeltexts[i-1], linewidth=2)
        ymax = max(ymax,max(data[i]))

    self.subplot.axis([0, xmax, 0, ymax])

    # title
    self.subplot.set_title(self.params['title'], TITLE_FONT_DICT)
    # labels on the y axis
    self.subplot.axes.set_ylabel(self.params['ylabel'])
    # set legend parameters
    self.subplot.legend(labeltexts)
    # legend text size
    try:
        lg = self.subplot.get_legend()
        ltext  = lg.get_texts()             # all the text.Text instance in the legend
        for txt in ltext:
            txt.set_fontsize(self.params['tickfontsize'])  # the legend text fontsize
        # legend line thickness
        llines = lg.get_lines()             # all the lines.Line2D instance in the legend
        for lli in llines:
            lli.set_linewidth(1.5)          # the legend linewidth
        # color of the legend frame
        # this only works when the frame is painted (see below draw_frame)
        frame  = lg.get_frame()             # the patch.Rectangle instance surrounding the legend
        frame.set_facecolor('#F0F0F0')      # set the frame face color to light gray
        # should the legend frame be painted
        lg.draw_frame(False)
    except:
        # no legend
        pass


class TheFrame(wx.Frame):
    def __init__(self,parent,id,size,title):
        wx.Frame.__init__(self, parent, id, title=title, size=size)

class TestApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        self.frame = TheFrame(None,-1,wx.Size(520, 600),"XY graph test")
        self.SetTopWindow(self.frame)

        self.fig = wx.Panel(self.frame,-1,size=wx.Size(500, 280))
        self.fig2 = wx.Panel(self.frame,-1,size=wx.Size(500, 280))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.fig, 1, wx.ALL|wx.EXPAND, 1)
        sizer_1.Add(self.fig2, 1, wx.ALL|wx.EXPAND, 1)

        self.frame.SetSizer(sizer_1)
        self.frame.Layout()

        self.doXYGraph()
        self.doGraphStacked()
        self.frame.Show(True)
        return True

    def doXYGraph(self):
        key = 'UPH Plot'
        data = array([[0.0, 0.0, 0.0, 0.0],
                      [5.0, 2.24,  1.79, 1.43],
                      [10.0,  3.16, 2.53, 2.02],
                      [25.0, 3.87, 3.1, 2.48]])
        Interfaces.GData[key] = transpose(data)

        # array with the line colors. It can be larger (but not shorter!)
        # than the number of lines
        # 
        linecolors= ['#FF0000','green','#0000AA','0','0']

        # array with the labels
        labeltexts =['UPH','UPH net', 'USH']

        paramList={'labels'      : 0,              # labels column
                   'data'        : 3,              # data column for this graph
                   'key'         : key,            # key for Interface
                   'title'       : 'Test',         # title of the graph
                   'ylabel'      : 'label y axis', # text for y label
                   'labeltexts'  : labeltexts,     # list of texts for the labels
                   'backcolor'   : '#FFFFFF',      # graph background color
                   'linecolors'  : linecolors,     # list with line colors
                   'tickfontsize': 8,              # size of the tickmarks and legend font
                   'ignoredrows' : []}             # rows that should not be plotted

        dummy = Mp.MatPanel(self.fig,wx.Panel,drawFigure,paramList)
        self.fig.draw()

    def doGraphStacked(self):
        key = 'TEST'
        data = array([['Process heat\ndemand','Process 1\n[MWh]','Process 2\n[MWh]',
                       'Office heating\n[MWh]','TOTAL\n[MWh]'],
                      ['Total'    , 118.0,  75.0,    60.0, 182.0],
                      ['January'  ,  10.0,  14.0,   30.0,   54.0],
                      ['February' ,  12.0,  16.0,   20.0,   48.0],
                      ['March'    ,  14.0,  18.0,   10.0,   42.0],
                      ['April'    ,  16.0,  20.0,    5.0,   41.0],
                      ['May'      ,  19.0,  23.0,    0.0,   42.0],
                      ['June'     ,   6.0,  10.0,    0.0,   16.0],
                      ['July'     ,   4.0,   8.0,    0.0,   12.0],
                      ['August'   ,   2.0,   6.0,    0.0,    8.0],
                      ['September',   7.0,  11.0,    0.0,   18.0],
                      ['October'  ,   9.0,  13.0,    10.0,  32.0],
                      ['November' ,  15.0,  19.0,    20.0,  54.0],
                      ['December' ,   4.0,   8.0,    30.0,  42.0]])
        Interfaces.GData[key] = data
        
        paramList={'labels'      : 0,                               # labels column
                   'data'        : 4,                               # data column for this graph
                   'key'         : key,                             # key for Interface
                   'title'       :'Monthly process heat demand',    # title of the graph
                   'ylabel'      :'UPH (MWh)',                      # y axis label
                   'backcolor'   :'#FFFFFF',                        # graph background color
                   'tickfontsize': 8,                               # tick label fontsize
                   'ignoredrows' :[0,1]                             # rows that should not be plotted
                   }
        dummy = Mp.MatPanel(self.fig2,wx.Panel,drawStackedBarPlot, paramList)
        self.fig.draw()

#------------------------------------------------------------------------------
#   Application start
#------------------------------------------------------------------------------

if __name__ == '__main__':

    app = TestApp()
    app.MainLoop()

