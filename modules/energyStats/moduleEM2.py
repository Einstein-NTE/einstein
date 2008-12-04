#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	ModuleEM2- Heat supply - Monthly data
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	28/03/2008
#                       Stoyan Danov    04/07/2008
#                       Stoyan Danov    07/07/2008
#                       Stoyan Danov    09/07/2008
#
#       Changes to previous version:
#       04/07/08:   SD changes
#       07/07/08:   SD data1 added for plot
#       09/07/08:   SD calculation of monthly from hourly data
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
from numpy import *
import wx

from einstein.auxiliary.auxiliary import *
from einstein.GUI.status import *
from einstein.modules.interfaces import *
import einstein.modules.matPanel as mP
import copy

def _U(text):
    return unicode(_(text),"utf-8")

class ModuleEM2(object):

    def __init__(self, keys):
        self.keys = keys
        self.interface = Interfaces()
        self.initModule()

    def initModule(self):
#------------------------------------------------------------------------------
        
        """
        module initialization
        """
#------------------------------------------------------------------------------
        # In this grid the nr. of cols is variable, so we generate the
        # column headings dynamically here
##        data = array([['Process heat\nsupply','Boiler 1\n[MWh]','Boiler 2\n[MWh]',
##                       'CHP engine 1\n[MWh]','TOTAL\n[MWh]'],
##                      ['Total'    ,  47.0,  75.0,    60.0, 182.0],
##                      ['January'  ,  10.0,  14.0,   30.0,   54.0],
##                      ['February' ,  12.0,  16.0,   20.0,   48.0],
##                      ['March'    ,  14.0,  18.0,   10.0,   42.0],
##                      ['April'    ,  16.0,  20.0,    5.0,   41.0],
##                      ['May'      ,  19.0,  23.0,    0.0,   42.0],
##                      ['June'     ,   6.0,  10.0,    0.0,   16.0],
##                      ['July'     ,   4.0,   8.0,    0.0,   12.0],
##                      ['August'   ,   2.0,   6.0,    0.0,    8.0],
##                      ['September',   7.0,  11.0,    0.0,   18.0],
##                      ['October'  ,   9.0,  13.0,    10.0,  32.0],
##                      ['November' ,  15.0,  19.0,    20.0,  54.0],
##                      ['December' ,   4.0,   8.0,    30.0,  42.0]])
##
##
##        data1 = array([['Process heat\ndemand','Process 1\n[MWh]','Process 2\n[MWh]',
##                       'Office heating\n[MWh]'],
##                       ['Total'    , 118.0,  75.0,    60.0],
##                      ['January'  ,  10.0,  14.0,   30.0],
##                      ['February' ,  12.0,  16.0,   20.0],
##                      ['March'    ,  14.0,  18.0,   10.0],
##                      ['April'    ,  16.0,  20.0,    5.0],
##                      ['May'      ,  19.0,  23.0,    0.0],
##                      ['June'     ,   6.0,  10.0,    0.0],
##                      ['July'     ,   4.0,   8.0,    0.0],
##                      ['August'   ,   2.0,   6.0,    0.0],
##                      ['September',   7.0,  11.0,    0.0],
##                      ['October'  ,   9.0,  13.0,    10.0],
##                      ['November' ,  15.0,  19.0,    20.0],
##                      ['December' ,   4.0,   8.0,    30.0]])
##                          
##        self.interface.setGraphicsData(self.keys[0], data)
##        self.interface.setGraphicsData(self.keys[1], data1)
##
##        #print "ModuleEM2 graphics data initialization"
##        #print "Interfaces.GData[%s] contains:\n%s\n" % (self.keys[0],repr(Interfaces.GData[self.keys[0]]))


#------------------------------------------------------------------------------
#SQL data search

        PId = Status.PId
        ANo = Status.ANo


        self.qgenerationhc = Status.prj.getEquipments()   #sqlqueries centralised in project-functions
        equipments = self.qgenerationhc

        print 'No of equipments: ',len(equipments)
        for equip in equipments:
            print 'Equipment name: ',equip.Equipment
            
#........................................................................
# filling the label row
        #for the graphic data array
        LabelRow1 =['Process heat\nsupply']
        for equip in equipments:
            LabelRow1.append(unicode(equip.Equipment,"utf-8") +'\n[MWh]')

        #for the table data array
        LabelRow = copy.deepcopy(LabelRow1)
        LabelRow.append(_U('TOTAL\n[MWh]'))

        print 'LabelRow =', LabelRow

#........................................................................
# taking the USH values from interfaces

        USH_T = Status.int.USHTotal_T
        USHTotal_Tt = Status.int.USHTotal_Tt
        USH_Tt = Status.int.USHj_Tt


        print 'len(USH_Tt): =', len(USH_Tt)
        print 'len(USH_Tt[0]): =', len(USH_Tt[0])
        print 'len(USH_Tt[0][0]) =', len(USH_Tt[0][0])


#.........................................................................
# calculating the monthly data start

        USHMonthly = [] #USH all equipments (matrix)
        LabelColumn = [_U('Total'),
                       _U('January'),
                       _U('February'),
                       _U('March'),
                       _U('April'),
                       _U('May'),
                       _U('June'),
                       _U('July'),
                       _U('August'),
                       _U('September'),
                       _U('October'),
                       _U('November'),
                       _U('December')]
        USHMonthly.append(LabelColumn)

#.........................................................................
# start of calculation loop

        for k in range(len(equipments)):
            print 'ProcNo:',k

            USHMonthlyEquip = [] #USH single equipment
            for i in range(13):
                USHMonthlyEquip.append(0.0)

            print 'Status.Nt =',Status.Nt

            #Annual simulation. Hours month assumed = 730 (8760/12)
            if Status.Nt == 8760:
            
                for NT in range(1,len(USH_Tt[0])):
                    for Nt in range(1,len(USH_Tt[0][0])):

                        if Nt <= 730: #January
                            USHMonthlyEquip[1] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        elif Nt > 730 and Nt <= 1460: #February
                            USHMonthlyEquip[2] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]
                    
                        elif Nt > 1460 and Nt <= 2190: #March
                            USHMonthlyEquip[3] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        elif Nt > 2190 and Nt <= 2920: #April
                            USHMonthlyEquip[4] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        elif Nt > 2920 and Nt <= 3650: #May
                            USHMonthlyEquip[5] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        elif Nt > 3650 and Nt <= 4380: #June
                            USHMonthlyEquip[6] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        elif Nt > 4380 and Nt <= 5110: #July
                            USHMonthlyEquip[7] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        elif Nt > 5115 and Nt <= 5840: #August
                            USHMonthlyEquip[8] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        elif Nt > 5840 and Nt <= 6570: #Setember
                            USHMonthlyEquip[9] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        elif Nt > 6570 and Nt <= 7300: #Octuber
                            USHMonthlyEquip[10] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        elif Nt > 7300 and Nt <= 8030: #November
                            USHMonthlyEquip[11] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        elif Nt > 8030 and Nt <= 8760: #December
                            USHMonthlyEquip[12] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        else:
                            pass

                #calculating the total for process: USHMonthlyEquip[0]
                for i in range(1,13):
                    USHMonthlyEquip[0] += USHMonthlyEquip[i]
                
                #print '1: USHMonthlyEquip =', USHMonthlyEquip

                USHMonthly.append(USHMonthlyEquip)

            #Monthly simulation
            elif Status.Nt == 168: 
            
                for NT in range(1,81):
                    for Nt in range(1,Status.Nt):

                        #January
                        USHMonthlyEquip[1] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        #February
                        USHMonthlyEquip[2] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]
                    
                        #March
                        USHMonthlyEquip[3] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        #April
                        USHMonthlyEquip[4] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        #May
                        USHMonthlyEquip[5] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        #June
                        USHMonthlyEquip[6] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        #July
                        USHMonthlyEquip[7] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        #August
                        USHMonthlyEquip[8] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        #September
                        USHMonthlyEquip[9] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        #Octuber
                        USHMonthlyEquip[10] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        #November
                        USHMonthlyEquip[11] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]

                        #December
                        USHMonthlyEquip[12] += USH_Tt[0][NT][Nt]/1000 #converted to [MWh]
            

                for i in range(len(USHMonthlyEquip)):
                    USHMonthlyEquip[i] = USHMonthlyEquip[i]*4.345 #multiplied by the ratio 730/168 (hours month/hours week)

                #calculating the total for process: USHMonthlyEquip[0]
                for i in range(1,13):
                    USHMonthlyEquip[0] += USHMonthlyEquip[i]

                #print '2: USHMonthlyEquip =', USHMonthlyEquip

                USHMonthly.append(USHMonthlyEquip)        

        else:
            pass #Status.Nt different from 8760 and 168
#................................................................................
# end of the calculatin loop

        print 'USHMonthly=',USHMonthly

        # transposing the matrix: order as shown in table
        USHMonthly = transpose(USHMonthly)
        print 'USHMonthly=',USHMonthly


        for row in USHMonthly:
            print row

# creating the data array for the graph
        GraphUSHMonthly = copy.deepcopy(USHMonthly)
        GraphUSHMonthly.insert(0,LabelRow1)
        graphdata = GraphUSHMonthly
        data1 = array(graphdata)

# calculating monthly totals
        for i in range(len(USHMonthly)):
            USHMonthlyTotal = 0.0
            for j in range(1,len(USHMonthly[i])):
                USHMonthlyTotal += USHMonthly[i][j]
            USHMonthly[i].append(USHMonthlyTotal)

# creating the data array for the table
        TableUSHMonthly = copy.deepcopy(USHMonthly)
        TableUSHMonthly.insert(0,LabelRow)
        tabledata = TableUSHMonthly
        data = array(tabledata)

# writing the arrays in interfaces
        self.interface.setGraphicsData(self.keys[0], data)
        self.interface.setGraphicsData(self.keys[1], data1)



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

#==============================================================================
