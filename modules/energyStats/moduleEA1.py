#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA1- Primary energy - Yearly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	21/03/2008
#
#       Changes to previous version:
#	
#------------------------------------------------------------------------------		
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	www.energyxperts.net / info@energyxperts.net
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#============================================================================== 

from sys import *
from math import *
import wx


from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP

def draw_FECbyFuel_Plot(self):
    try:
        # This curve takes its data from the dictionary Interfaces.GData, with the key 'EA1_FEC'
        # As an example, the data for this curve are stored in Interfaces as two different entries:
        # Values and Labels.
        theValues = Interfaces.GData['EA1_FEC_VALUES']
        theLabels = Interfaces.GData['EA1_FEC_LABELS']
    except:
        print "draw_FECbyFuel_Plot: values EA1_FEC_VALUES or EA1_FEC_LABELS missing."
        print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return

    #print "draw_FECbyFuel_Plot: EA1_FEC_VALUES=%s, EA1_FEC_LABELS=%s\n" %(theValues, theLabels)

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.set_title("FEC by fuel")
    self.subplot.pie(theValues, explode=None, labels=theLabels, autopct=None,
                     pctdistance=0.6, labeldistance=1.2, shadow=True)

def draw_FETbyFuel_Plot(self):
    try:
        # This curve takes its data from the dictionary Interfaces.GData, with the key 'EA1_FET'
        # As an example, the data for this curve are stored in Interfaces as a single entry, a tuple.
        # So, the values are extracted as element 0 of the tuple, and the labels as element 1.
        theData = Interfaces.GData['EA1_FET']
    except:
        print "draw_FETbyFuel_Plot: values EA1_FET missing"
        print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.set_title("FET by fuel")
    self.subplot.pie(theData[0], explode=None,labels=theData[1],
                     autopct=None, pctdistance=0.6, labeldistance=1.2, shadow=True)


class ModuleEA1(object):

    def __init__(self):
        self.interface = Interfaces()
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------
        # Here, the data for the graphs are loaded in Interfaces, to be recovered later
        # by the graphing procedures.
        # There are two graphs in this page, and each graph needs two series of data:
        # 1. the values (in this case percentages)
        # 2. the labels (in this case fuel names)
        #
        # The storing of the data is completely flexible and up to the programmer. As an
        # example, the data for EA1_FET and EA1_FEC are stored differently. Naturally, the
        # graphing procedure needs to know how the data were stored.
        # In the case of EA1_FET, the Values and the Labels are stored as different entries
        # in the data dictionary in Interfaces.
        # The data for EA1_FEC are stored as a single entry in a tuple.
        #
        # Naturally, the real values will be eventually extracted from the database, so
        # the lists FET_values, FET_fuels, FEC_values, FEC_fuels will be dinamically
        # loaded with data.
        #
        FEC_values = [31, 15, 46, 8]
        FEC_labels = ['Natural gas','Gas oil','LPG','Electricity']
        self.interface.setGraphicsData('EA1_FEC_VALUES', FEC_values)
        self.interface.setGraphicsData('EA1_FEC_LABELS', FEC_labels)

        FET_values = [31, 15, 46, 8]
        FET_labels = ['Natural gas','Gas oil','LPG','Electricity']
        self.interface.setGraphicsData('EA1_FET',(FET_values, FET_labels))

        #print "ModuleEA1 graphics data initialization"
        #print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return "ok"

#------------------------------------------------------------------------------
    def exitModule(self,exit_option):
#------------------------------------------------------------------------------
        """
        carries out any calculations necessary previous to displaying the HP
        design assitant window
        """
#------------------------------------------------------------------------------
        if exit_option == "save":
            print "exitModule: here I should save the current configuration"
        elif exit_option == "cancel":
            print "exitModule: here I should retreive the previous configuration"
            

        print "exitModule: function not yet defined"

        return "ok"

#------------------------------------------------------------------------------

    # Method for copying the graphic methods.
    # this is called from panelEA1
    # the item argument (0:n) defines which graphics procedure
    # will be returned.
    #
    def getPlotMethod(self,item):
        global draw_FECbyFuel_Plot, draw_FETbyFuel_Plot
        if item == 0:
            return draw_FECbyFuel_Plot
        elif item == 1:
            return draw_FETbyFuel_Plot
        else:
            return None
#==============================================================================
