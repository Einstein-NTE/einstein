#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA3- Final energy by equipment- Yearly data
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

def draw_FETbyEquipment_Plot(self):
    try:
        theData = Interfaces.GData['EA3_FET']
    except:
        print "draw_FETbyProcess_Plot: values EA3_FET missing"
        print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.set_title("FET by equipment")
    self.subplot.pie(theData[0], explode=None, labels=theData[1],
                     autopct=None, pctdistance=0.6, labeldistance=1.2, shadow=True)

def draw_USHbyEquipment_Plot(self):
    try:
        theData = Interfaces.GData['EA3_USH']
    except:
        print "draw_USHbyProcess_Plot: values EA3_USH missing"
        print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.set_title("USH by equipment")
    self.subplot.pie(theData[0], explode=None, labels=theData[1],
                     autopct=None, pctdistance=0.6, labeldistance=1.2, shadow=True)

class ModuleEA3(object):

    def __init__(self):
        self.interface = Interfaces()
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------
        self.interface.setGraphicsData('EA3_FET',([16.36, 16.36, 9.09, 27.27, 27.27, 3.64],
                                       ['Equipment 1','Equipment 2','Equipment 3','Equipment 4',
                                        'Equipment 5','Equipment 6']))

        self.interface.setGraphicsData('EA3_USH',([16.29, 16.29, 9.05, 27.16, 27.16, 4.05],
                                       ['Equipment 1','Equipment 2','Equipment 3','Equipment 4',
                                        'Equipment 5','Equipment 6']))
        #print "ModuleEA3 graphics data initialization"
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
    # called from panelEA3
    def getPlotMethod(self,item):
        global draw_FETbyEquipment_Plot, draw_USHbyEquipment_Plot
        if item == 0:
            return draw_FETbyEquipment_Plot
        elif item == 1:
            return draw_USHbyEquipment_Plot
        else:
            return None
#==============================================================================
