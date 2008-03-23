#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA4- Process heat- Yearly data
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

def draw_UPHbyProcess_Plot(self):
    try:
        theData = Interfaces.GData['EA4_UPH']
    except:
        print "draw_UPHbyProcess_Plot: values EA4_UPH missing"
        print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.set_title("UPH by process")
    self.subplot.pie(theData[0], explode=None, labels=theData[1],
                     autopct=None, pctdistance=0.6, labeldistance=1.2, shadow=True)

def draw_HDbyProcess_Plot(self):
    try:
        theData = Interfaces.GData['EA4_HD']
    except:
        print "draw_HDbyProcess_Plot: values EA4_HD missing"
        print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.set_title("Heat demand by process")
    self.subplot.pie(theData[0], explode=None, labels=theData[1],
                     autopct=None, pctdistance=0.6, labeldistance=1.2, shadow=True)

class ModuleEA4(object):

    def __init__(self):
        self.interface = Interfaces()
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------
        UPH_values = [33.01, 54.37, 12.62]
        UPH_labels = ['Process 1','Process 2','Process 3']
        self.interface.setGraphicsData('EA4_UPH', (UPH_values, UPH_labels))

        HD_values = [170, 280, 65]
        HD_labels = ['Process 1','Process 2','Process 3']
        self.interface.setGraphicsData('EA4_HD', (HD_values, HD_labels))

        #print "ModuleEA4 graphics data initialization"
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
    # called from panelEA4
    def getPlotMethod(self,item):
        global draw_UPHbyProcess_Plot, draw_HDbyProcess_Plot
        if item == 0:
            return draw_UPHbyProcess_Plot
        elif item == 1:
            return draw_HDbyProcess_Plot
        else:
            return None
#==============================================================================
