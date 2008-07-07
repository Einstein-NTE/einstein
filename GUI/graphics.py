#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	graphics- GUI component for creating plot graphics
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Tom Sobota	28/03/2008
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

from numpy import *
from einstein.modules.interfaces import *


#
# some constants
#
COLORTABLE = ['#0000FF','#00FF00','#FF0000','#00FFFF','#FF00FF',
              '#FFFF00','#000000','#FFFFFF']
#
# title properties dictionary
#
TITLE_FONT_DICT = {'fontname'  : 'Roman',
                   'fontweight': 'bold',
                   'color'     : '#808080',
                   'fontsize'  : 12}

## TS 2008/03/17 #########################################################################
#
# the following is a kit of graphic routines.
# Caution: the routines have the form of class methods (using 'self') but they will NOT
# be executed in the context of any of the other classes in this file.
# They will be dynamically bound to the wx widget doing the actual drawing (in panel*.py)
# For the same reason, even if the routines draw their graphics using the 'matplotlib'
# package, the package does not have to be imported here.
#
##########################################################################################


##############################################################################
#
# generic pie drawing routine
#
##############################################################################

def drawPiePlot(self):
    #
    # some constants for the pie
    #
    PIE_LABEL_COLOR = '#808080'
    PIE_PERCENT_COLOR = '#000000'
    PIE_PERCENT_SIZE = 9

    # generic function for painting pies.
    # Takes its data from the dictionary Interfaces.GData.
    # The data is a numpy array. The first column has the labels, and another
    # column has the values
    #
    # the following params are mandatory
    #
    try:
        index_data = int(self.params['data'])      # index to the column of data
    except KeyError:
        print "drawPiePlot: missing index to data column."
        return

    try:
        key = self.params['key']                   # key for Interfaces.GData
    except KeyError:
        print "drawPiePlot: missing key to data."
        return

    # the following params are optative
    try:
        index_labels = int(self.params['labels'])  # index to the column of labels
    except KeyError:
        index_labels = 0

    try:
        title = self.params['title']               # title of the graphic
    except KeyError:
        title = ''

    try:
        backcolor = self.params['backcolor']       # background color of the graph
    except KeyError:
        backcolor = '#FFFFFF'

    try:
        tickfontsize = self.params['tickfontsize'] # fontsize of the tick mark labels
    except KeyError:
        tickfontsize = 9

    try:
        ignoredrows = self.params['ignoredrows']  # list of rows to be ignored (totals and such)
    except KeyError:
        ignoredrows = []


    try:
        (rows,cols) = Interfaces.GData[key].shape
        theValues = []
        theLabels = []
        for r in range(rows):
            if r not in ignoredrows: 
                row = Interfaces.GData[key][r]
                value = float(row[index_data])
                if value != 0.0:
                    # plot only values <> 0
                    theLabels.append(row[index_labels])
                    theValues.append(value)
    except:
        print "drawPiePlot: values %s missing or bad." % (key,)
        print "Interfaces.GData['%s'] contains:\n%s\n" % (key, repr(Interfaces.GData[key]))
        return

    if len(theValues) == 0:
        #oh oh ... no values -> no graphic
        return
    if hasattr(self, 'subplot'):
        del self.subplot
    self.subplot = self.figure.add_subplot(1,1,1)
    self.figure.set_facecolor(backcolor)

    self.subplot.set_title(title, TITLE_FONT_DICT)
    #
    # now we finally plot the pie
    #
    (patches, labels, texts) = self.subplot.pie(theValues, explode=None,
                                                labels=theLabels,
                                                autopct='%.4s%%', pctdistance=0.6,
                                                labeldistance=1.2, shadow=True)
    #
    # and then we set text attributes
    #
    for t in labels:
        t.set_fontsize(tickfontsize)
        t.set_color(PIE_LABEL_COLOR)

    for t in texts:
        t.set_fontsize(PIE_PERCENT_SIZE)
        t.set_color(PIE_PERCENT_COLOR)


##############################################################################
#
# generic stacked bars drawing routine
#
##############################################################################

def drawStackedBarPlot(self):
    #
    # generic function for stacked bars.
    # Takes its data from the dictionary Interfaces.GData.
    # The data is a numpy array. The first column has the labels, and another
    # column has the values
    #
    # the following params are mandatory
    #
    try:
        index_data = int(self.params['data'])      # index to the column of data
    except KeyError:
        print "drawPiePlot: missing index to data column."
        return

    try:
        key = self.params['key']                   # key for Interfaces.GData
    except KeyError:
        print "drawPiePlot: missing key to data."
        return

    # the following params are optative
    try:
        index_labels = int(self.params['labels'])  # index to the column of labels
    except KeyError:
        index_labels = 0

    try:
        title = self.params['title']               # title of the graphic
    except KeyError:
        title = ''

    try:
        legend = self.params['legend']             # legend list
    except KeyError:
        legend = []

    try:
        ylabel = self.params['ylabel']             # label on the y axis
    except KeyError:
        ylabel = ''

    try:
        backcolor = self.params['backcolor']       # background color of the graph
    except KeyError:
        backcolor = '#FFFFFF'

    try:
        tickfontsize = self.params['tickfontsize'] # fontsize of the tick mark labels
    except KeyError:
        tickfontsize = 8

    try:
        ignoredrows = self.params['ignoredrows']  # list of rows to be ignored (totals and such)
    except KeyError:
        ignoredrows = []

    try:
        # make a copy of the array without the ignored rows
        (rows,cols) = Interfaces.GData[key].shape
        rowList = []
        for r in range(rows):
            if r not in ignoredrows:
                rowList.append(Interfaces.GData[key][r])

        # simultaneously transpose the matrix so each row is a dataset
        data = array(rowList).transpose()
        # now, row 0 are the vert. labels
        (rows,cols) = data.shape
    except:
        print "drawStackedBarPlot: values %s missing or bad." % (key,)
        print "Interfaces.GData['%s'] contains:\n%s\n" % (key, repr(Interfaces.GData[key]))
        return

    # load the x tick labels
    xticklabels = data[0]
    # if the legend has been given as a parameter, use it
    # if not, take the texts from col 0
    legendlabels = []
    if len(legend)>0:
        legendlabels = legend
    legendptr = []
    vx = arange(cols) # intervals on x
    width = 0.9                          # the width of the bars
    if hasattr(self, 'subplot'):
        del self.subplot
    self.subplot = self.figure.add_subplot(1,1,1)
    self.figure.set_facecolor(backcolor)

    # for all rows except 0, which has the labels
    for r in range(1,rows):
        row = data[r]
        if len(legend) <= 0:
            legendlabels.append(row[0].replace("\n"," "))
        #floatdata = map(lambda a: float(a), row[0:cols])
        floatdata = map(lambda a: float(a), row)
        if r == 1:
            p = self.subplot.bar(vx, floatdata, width, color=COLORTABLE[r % 8])
        else:
            p = self.subplot.bar(vx, floatdata, width, color=COLORTABLE[r % 8], bottom=previous)
        legendptr.append(p[0])
        previous = floatdata[:]

    self.subplot.axes.set_ylabel(ylabel)
    self.subplot.set_title(title, TITLE_FONT_DICT)
    # create xticks
    self.subplot.axes.set_xticks(map(lambda x: x + width/2., vx))
    xlabels = self.subplot.axes.set_xticklabels(xticklabels)
    for xlabel in xlabels:
        xlabel.set_size(tickfontsize)
    
    # create yticks
    #self.subplot.axes.set_yticks(arange(0,61,10))

    # draw legend and set legend parameters
    self.subplot.legend(legendptr,legendlabels)
    # legend text size
    lg = self.subplot.get_legend()
    ltext  = lg.get_texts()             # all the text.Text instance in the legend
    for txt in ltext:
        txt.set_fontsize(tickfontsize)  # the legend text fontsize
    # legend line thickness
    llines = lg.get_lines()             # all the lines.Line2D instance in the legend
    for lli in llines:
        lli.set_linewidth(1.5)          # the legend linewidth
    # color of the legend frame
    frame  = lg.get_frame()             # the patch.Rectangle instance surrounding the legend
    frame.set_facecolor('#F0F0F0')      # set the frame face color to light gray
    # should the legend frame be painted
    lg.draw_frame(False)                # don't draw the legend frame

##############################################################################
#
# generic simple bar histogram drawing routine
#
##############################################################################

def drawSimpleBarPlot(self):
    # Takes its data from the dictionary Interfaces.GData.
    # The data is a numpy array. The first column has the labels, and another
    # column has the values
    #
    # the following params are mandatory
    #
    try:
        index_data = int(self.params['data'])      # index to the column of data
    except KeyError:
        print "drawSimpleBarPlot: missing index to data column."
        return

    try:
        key = self.params['key']                   # key for Interfaces.GData
    except KeyError:
        print "drawSimpleBarPlot: missing key to data."
        return

    # the following params are optative

    try:
        index_labels = int(self.params['labels'])  # index to the column of labels
    except KeyError:
        index_labels = 0

    try:
        title = self.params['title']               # title of the graphic
    except KeyError:
        title = ''

    try:
        ylabel = self.params['ylabel']             # label on the y axis
    except KeyError:
        ylabel = ''

    try:
        legend = self.params['legend']             # legend list
    except KeyError:
        legend = []

    try:
        backcolor = self.params['backcolor']       # background color of the graph
    except KeyError:
        backcolor = '#FFFFFF'

    try:
        tickfontsize = self.params['tickfontsize'] # fontsize of the tick mark labels
    except KeyError:
        tickfontsize = 8

    try:
        ignoredrows = self.params['ignoredrows']  # list of rows to be ignored (totals and such)
    except KeyError:
        ignoredrows = []


    try:
        # make a copy of the array without the ignored rows
        (rows,cols) = Interfaces.GData[key].shape
        rowList = []
        for r in range(rows):
            if r not in ignoredrows:
                rowList.append(Interfaces.GData[key][r])

        # simultaneously transpose the matrix so each row is a dataset
        data = array(rowList).transpose()
        # now, row 0 are the vert. labels
        (rows,cols) = data.shape
    except:
        print "drawSimpleBarPlot: values %s missing or bad." % (key,)
        print "Interfaces.GData['%s'] contains:\n%s\n" % (key, repr(Interfaces.GData[key]))
        return

    # load the x tick labels (1st. row of the transposed matrix)
    xticklabels = data[0]
    # load the data
    vx = arange(cols)         # intervals on x
    width = 0.8               # the width of the bars
    if hasattr(self, 'subplot'):
        del self.subplot
    self.subplot = self.figure.add_subplot(1,1,1)
    self.figure.set_facecolor(backcolor)
    # extract data from second row on
    legendlabels = legend
    legendptr = []
    for r in range(1,rows):
        row = data[r]
        floatdata = map(lambda a: float(a), row)
        p = self.subplot.bar(vx, floatdata, width, color=COLORTABLE[r % 8])
        legendptr.append(p[0])

    self.subplot.axes.set_ylabel(ylabel)
    self.subplot.set_title(title, TITLE_FONT_DICT)
    # create xticks
    self.subplot.axes.set_xticks(map(lambda x: x + width/2., vx))
    xlabels = self.subplot.axes.set_xticklabels(xticklabels)
    for xlabel in xlabels:
        xlabel.set_size(tickfontsize)

    # draw legend and set legend parameters
    self.subplot.legend(legendptr,legendlabels)
    # legend text size
    lg = self.subplot.get_legend()
    ltext  = lg.get_texts()
    for txt in ltext:
        txt.set_fontsize(tickfontsize)
    # legend line thickness
    llines = lg.get_lines()
    for lli in llines:
        lli.set_linewidth(1.5)
    # color of the legend frame
    frame  = lg.get_frame()
    frame.set_facecolor('#F0F0F0')
    # should the legend frame be painted
    lg.draw_frame(False)

    return


##############################################################################
#
# generic compared bar histogram drawing routine
# draws several bars for each x interval, corresponding to
# several series to be compared.
#
##############################################################################

def drawComparedBarPlot(self):
    #
    # Takes its data from the dictionary Interfaces.GData.
    # The data is a numpy array. The first column has the labels, and another
    # column has the values

    #
    # the following params are mandatory
    #
    try:
        index_data = int(self.params['data'])      # index to the column of data
    except KeyError:
        print "drawComparedBarPlot: missing index to data column."
        return

    try:
        key = self.params['key']                   # key for Interfaces.GData
    except KeyError:
        print "drawComparedBarPlot: missing key to data."
        return

    # the following params are optative

    try:
        index_labels = int(self.params['labels'])  # index to the column of labels
    except KeyError:
        index_labels = 0

    try:
        title = self.params['title']               # title of the graphic
    except KeyError:
        title = ''

    try:
        ylabel = self.params['ylabel']             # label on the y axis
    except KeyError:
        ylabel = ''

    try:
        legend = self.params['legend']             # legend list
    except KeyError:
        legend = []

    try:
        backcolor = self.params['backcolor']       # background color of the graph
    except KeyError:
        backcolor = '#FFFFFF'

    try:
        tickfontsize = self.params['tickfontsize'] # fontsize of the tick mark labels
    except KeyError:
        tickfontsize = 8

    try:
        ignoredrows = self.params['ignoredrows']  # list of rows to be ignored (totals and such)
    except KeyError:
        ignoredrows = []


    width = 0.3                  # the width of the bars

    try:
        # make a copy of the array without the ignored rows
        (rows,cols) = Interfaces.GData[key].shape
        rowList = []
        for r in range(rows):
            if r not in ignoredrows:
                rowList.append(Interfaces.GData[key][r])

        # simultaneously transpose the matrix so each row is a dataset
        data = array(rowList).transpose()
        # now, row 0 are the vert. labels
        (rows,cols) = data.shape
    except:
        print "drawComparedBarPlot: values %s missing or bad." % (key,)
        print "Interfaces.GData['%s'] contains:\n%s\n" % (key, repr(Interfaces.GData[key]))
        return

    # load the x tick labels
    xticklabels = data[0]

    legendlabels = legend
    legendptr = []
    vx = range(cols)     # the x locations for the groups

    if hasattr(self, 'subplot'):
        del self.subplot

    self.subplot = self.figure.add_subplot(1,1,1)
    self.figure.set_facecolor(backcolor)

    # extract the transposed data from second row on
    for r in range(1,rows):
        row = data[r]
        floatdata = map(lambda a: float(a), row)
        p = self.subplot.bar(map(lambda x: x+((r-1)*width),vx),
                             floatdata, width, color=COLORTABLE[r % 8])
        legendptr.append(p[0])

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)

    self.subplot.axes.set_ylabel(ylabel)
    self.subplot.set_title(title, TITLE_FONT_DICT)
    # create xticks
    self.subplot.axes.set_xticks(map(lambda x: x + width/2., vx))
    xlabels = self.subplot.axes.set_xticklabels(xticklabels)
    for xlabel in xlabels:
        xlabel.set_size(tickfontsize)

    # draw legend and set legend parameters
    self.subplot.legend(legendptr,legendlabels)
    # legend text size
    lg = self.subplot.get_legend()
    ltext  = lg.get_texts()
    for txt in ltext:
        txt.set_fontsize(tickfontsize)
    # legend line thickness
    llines = lg.get_lines()
    for lli in llines:
        lli.set_linewidth(1.5)
    # color of the legend frame
    frame  = lg.get_frame()
    frame.set_facecolor('#F0F0F0')
    # should the legend frame be painted
    lg.draw_frame(False)
