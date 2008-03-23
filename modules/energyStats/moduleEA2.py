#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA2- Final energy by fuels- Yearly data
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

def draw_PECbyFuel_Plot(self):
    try:
        theData = Interfaces.GData['EA2_PEC']
    except:
        print "draw_PECbyFuel_Plot: values EA2_PEC missing"
        print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.set_title("PEC by fuel")
    self.subplot.pie(theData[0], explode=None, labels=theData[1], autopct=None,
                     pctdistance=0.6, labeldistance=1.2, shadow=True)

def draw_PETbyFuel_Plot(self):
    try:
        theData = Interfaces.GData['EA2_PET']
    except:
        print "draw_PETbyFuel_Plot: values EA2_PET missing"
        print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.set_title("PET by fuel")
    self.subplot.pie(theData[0], explode=None, labels=theData[1], autopct=None,
                     pctdistance=0.6, labeldistance=1.2, shadow=True)


class ModuleEA2(object):

    def __init__(self):
        self.interface = Interfaces()
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------
        PEC_values = [81, 19]
        PEC_labels = ['Total fuels','Total electricity']
        self.interface.setGraphicsData('EA2_PEC',(PEC_values, PEC_labels))

        PET_values = [91, 9]
        PET_labels = ['Total fuels','Total electricity']
        self.interface.setGraphicsData('EA2_PET',(PET_values, PET_labels))

        #print "ModuleEA2 graphics data initialization"
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
    # called from panelEA2
    def getPlotMethod(self,item):
        global draw_PECbyFuel_Plot, draw_PETbyFuel_Plot
        if item == 0:
            return draw_PECbyFuel_Plot
        elif item == 1:
            return draw_PETbyFuel_Plot
        else:
            return None
#==============================================================================
