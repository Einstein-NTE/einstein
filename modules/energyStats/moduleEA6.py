#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA6- Production of CO2- Yearly data
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

def draw_CO2byFuel_Plot(self):
    try:
        theData = Interfaces.GData['EA6_CO2']
    except:
        print "draw_CO2byFuel_Plot: values EA6_CO2 missing"
        print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.set_title("Production of\nCO2 by fuel")
    self.subplot.pie(theData[0], explode=None, labels=theData[1],
                     autopct=None, pctdistance=0.6, labeldistance=1.2, shadow=True)

class ModuleEA6(object):

    def __init__(self):
        self.interface = Interfaces()
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------
        # generate data for graphics
        CO2_values = [28, 14, 42, 15]
        CO2_labels = ['Natural gas','Gasoil','LPG', 'Electricity']
        self.interface.setGraphicsData('EA6_CO2', (CO2_values, CO2_labels))

        #print "ModuleEA6 graphics data initialization"
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
    # called from panelEA5
    def getPlotMethod(self,item):
        global draw_CO2byFuel_Plot
        if item == 0:
            return draw_CO2byFuel_Plot
        elif item == 1:
            return None
        else:
            return None
#==============================================================================
