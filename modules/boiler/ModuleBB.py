#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleBB (Boilers and Burners)
#			
#------------------------------------------------------------------------------
#			
#	Module for calculation of boilers
#
#==============================================================================
#
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	11/03/2008
#	Last revised by:    Tom Sobota          15/03/2008
#
#       Changes to previous version:
#       2008-3-15 Added graphics functionality
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

def drawHeatDemandPlot(self):
    #
    # this function draws the Heat Demand Plot
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
    self.subplot.set_title("A Polar star(%s points)"%len(x), fontsize = 12)
    self.subplot.set_xlabel("Example adapted from  http://www.physics.emory.edu/~weeks/ideas/rose.html",
                            fontsize = 8)
    self.subplot.set_xlim([-400, 400])
    self.subplot.set_ylim([-400, 400])

class ModulePars():
    topMin = None  #minimum annual operation hours
    par2 = None #other parameter of the module
    par3 = None #...

    def __init__(self):
#       initialise with some default parameters
        pass
    

class ModuleBB():

    BBList = []
    # please use status.DB, status.PId ...
    #DB = None
    #sql = None
    #PId = None #Project identity
    #ANo = None #Alternative number
    Pars = ModulePars()
    
    def __init__(self, parent):
        self.parent = parent
        self.initModule()

#------------------------------------------------------------------------------
    def initModule(self):
        """
        carries out any calculations necessary previous to displaying the BB
        design assistant window
        """
        #interfaces.chargeCurvesQDQA() #gets the updated heat demand from the SQL
        
        #self.DB = status.DB
        #self.sql = status.SQL
        #self.PId = status.PId
        #self.ANo = status.ANo
#       self.BBList = detectBB() # detects the boilers & burners in the list of existing equipment
        self.updateHeatDemandPlot()

        return "ok"
#------------------------------------------------------------------------------

    def exitModule(self,exit_option):
        """
        carries out any calculations necessary previous to displaying the HP
        design assitant window
        """
        if exit_option == "save":
            print "exitModule: here I should save the current configuration"
        elif exit_option == "cancel":
            print "exitModule: here I should retreive the previous configuration"
            

        print "exitModule: function not yet defined"

        return "ok"

#------------------------------------------------------------------------------

    def storeModulePars(self):
        """
        store Module parameters in the SQL or some other save space
        """
        print "storeModulePars: not yet defined"

        return "ok"


#------------------------------------------------------------------------------
    def add(self,BBId):
        """
        adds a new heat pump 
        """
        #--> add HP to the equipment list under current alternative
        print "add (BB): function not yet defined"

        self.calculateEnergyFlows(BBId)

        return "ok"

#------------------------------------------------------------------------------

    def delete(self,BBid):
        """
        deletes the selected boiler / burner in the current alternative
        """
        print "delete (BB): function not yet defined"

        return "ok"

        #--> delete HP from the equipment list under current alternative
        
#------------------------------------------------------------------------------
    def retrieveDeleted(self):
        """
        returns a list of previously deleted equipment that can be retrieved
        """
        print "deleteHP: function not yet defined"

        return "ok"

        #--> delete HP from the equipment list under current alternative
        
#------------------------------------------------------------------------------

    def designAssistant1(self):
        """
        step 1 of the design assistant (from activation to 1st user interaction)
        """
        try:
            print "designAssistant1: function not yet implemented"
            return "ManualFinalAdjustment"
#..............................................................................
        except Exception, designAssistant1: #in case of an error
            print 'designAssistant1', designAssistant1
            return designAssistant1

#..............................................................................
        else:       #everything is fine
            return 0

#------------------------------------------------------------------------------

    def designAssistant2(self):
        """
        step 2 of the design assistant (after 1st user interaction)
        """
        try:
            print "designAssistant2: function not yet implemented"
            return "ok"
#..............................................................................
        except Exception, designAssistant2: #in case of an error
            print 'designAssistant2', designAssistant2
            return designAssistant2

#..............................................................................
        else:       #everything is fine
            return 0

#------------------------------------------------------------------------------

    def calculateEnergyFlows(self,BBid):
        """
        updates the energy flows in the newly added equipment 
        """
        print "calculateEnergyFlows: function not yet defined"
        return "ok"

#------------------------------------------------------------------------------

    def calculateCascade(self):
        """
        updates the energy flows for ALL boilers, following the cascade
        hierarchy
        """
        for BBid in self.BBList:
            calculateEnergyFlows(BBid)

        return "ok"
#------------------------------------------------------------------------------

    def updateHeatDemandPlot(self):
        try:
            self.parent.panelHeatDemandPlot.draw()
        except:
            # First call. Drawing widget not yet initialized.
            dummy = mP.MatPanel(self.parent.panelHeatDemandPlot,wx.Panel,drawHeatDemandPlot)
            del dummy
            self.parent.panelHeatDemandPlot.draw()
    

#==============================================================================
