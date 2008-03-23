#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEA5- Energy intensity- Yearly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	22/03/2008
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

def draw_EIbyType_Plot(self):
    try:
        theData = Interfaces.GData['EA5_EI']
    except:
        print "draw_EIbyType_Plot: values EA5_EI missing"
        print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.set_title("Energy intensity")
    self.subplot.pie(theData[0], explode=None, labels=theData[1],
                     autopct=None, pctdistance=0.6, labeldistance=1.2, shadow=True)

def draw_SECbyProduct_Plot(self):
    n_energies = 3               # values per set
    width = 0.3                  # the width of the bars
    theLabels = ('Energy by fuels', 'Energy by electricity', 'Primary energy')

    try:
        theData = Interfaces.GData['EA5_SEC']
        theValues = theData[0]
        theProducts = theData[1]
    except:
        print "draw_SECbyProduct_Plot: values EA5_SEC missing"
        print "Interfaces.GData contains:\n%s\n" % (repr(Interfaces.GData),)
        return

    n_products = len(theValues)
    ind = range(n_energies)     # the x locations for the groups
    fuels = []
    electricity = []
    primary = []
    for i in range(n_energies):
        product = theValues[i]
        fuels.append(product[0])
        electricity.append(product[1])
        primary.append(product[2])

    if not hasattr(self, 'subplot'):
        self.subplot = self.figure.add_subplot(1,1,1)
    self.subplot.set_title("SEC by product")
    # labels and ticks
    self.subplot.set_xlabel(theLabels)
    self.subplot.set_ylabel('Energy')
    self.subplot.set_title('SEC by product')
    self.subplot.set_xticks(map(lambda x: x+width,ind), theProducts)
    self.subplot.set_xlim(-width,len(ind))
    self.subplot.set_yticks(range(0,1000,100))
    #self.subplot.legend( (p1[0], p2[0], p3[0]), labels, shadow=True)
    # bars
    self.subplot.bar(ind, fuels, width, color='b')
    self.subplot.bar(map(lambda x: x+width,ind), electricity, width, color='r')
    self.subplot.bar(map(lambda x: x+(2*width),ind), primary, width, color='w')


class ModuleEA5(object):

    def __init__(self):
        self.interface = Interfaces()
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------
        EI_values = [1.91, 0.18, 2.65]
        EI_labels = ['Fuels','Electricity','Total primary energy']
        self.interface.setGraphicsData('EA5_EI', (EI_values, EI_labels))


        SEC_values = [[500,50,700], # values of En.by fuels, En.by electricity, Primary en. for Product 1
                      [400,80,680], # values of En.by fuels, En.by electricity, Primary en. for Product 2
                      [100,10,140]] # values of En.by fuels, En.by electricity, Primary en. for Product 3

        SEC_labels = ['Product 1','Product 2','Product 3']
        self.interface.setGraphicsData('EA5_SEC', (SEC_values, SEC_labels))

        #print "ModuleEA5 graphics data initialization"
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
        global draw_EIbyType_Plot, draw_SECbyProduct_Plot
        if item == 0:
            return draw_EIbyType_Plot
        elif item == 1:
            return draw_SECbyProduct_Plot
        else:
            return None
#==============================================================================
