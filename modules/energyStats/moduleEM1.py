#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEM1- Energy performance - Monthly data
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

def draw_MPHD_Plot(self):
    #
    # this function draws the Monthly process heat demand Plot
    #
    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    # this is just an example curve
    # the curve takes it's data from the dictionary Interfaces.GData, with the key 'EM1'
    self.subplot.plot(Interfaces.GData['EM1_MPHD'][0],
                      Interfaces.GData['EM1_MPHD'][1],
                      'go-', label='line 1', linewidth=2)
    self.subplot.plot(Interfaces.GData['EM1_MPHD'][2],
                      Interfaces.GData['EM1_MPHD'][3],
                      'rs',  label='line 2')
    self.subplot.axis([0, 4, 0, 10])
    self.subplot.legend()


class ModuleEM1(object):

    def __init__(self):
        self.interface = Interfaces()
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------
        self.interface.setGraphicsData('EM1_MPHD',([1,2,3], [1,2,3], [1,2,3], [1,4,9]))
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
    # called from panelEM1
    def getPlotMethod(self, item):
        global draw_MPHD_Plot
        if item == 0:
            return draw_MPHD_Plot
        elif item == 1:
            return None
        else:
            return None
#==============================================================================
