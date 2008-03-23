#============================================================================== 				
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	HEAT PUMP - Module for heat pump selection and calculation
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Module for heat pump selection and calculation
#       Draft version
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Stoyan Danov	31/01/2008
#	Last revised by:    Hans Schweiger      07/03/2008
#
#       Changes to previous version:
#       - change into module structure (class) as proposed by Heiko
#       - changes in path for SQL, according to folder structure
#       - function heatPump renamed to selectHeatPump
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
from einstein.auxiliary.auxiliary import *
from userdefined import *
from heatpump_input import *

class ModuleHP():

    #def __init__(self):
        #--- initialise something

#------------------------------------------------------------------------------
    def initFrame():
#------------------------------------------------------------------------------
        """
        carries out any calculations necessary previous to displaying the HP
        design assitant window
        """
#------------------------------------------------------------------------------
        print "initFrame: function not yet defined"

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def exitFrame(exit_option):
#------------------------------------------------------------------------------
        """
        carries out any calculations necessary previous to displaying the HP
        design assitant window
        """
#------------------------------------------------------------------------------
        #if exit_option == "save":
            # save current HP configuration
        #elif exit_option == "nosave":
            # restore HP configuration before entering the window from back-up

        print "exitFrame: function not yet defined"

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def addHP(HPid):
#------------------------------------------------------------------------------
        """
        adds a new heat pump 
        """
#------------------------------------------------------------------------------

        #--> add HP to the equipment list under current alternative
        self.calculateEnergyFlows(HPid)

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def deleteHP(HPid):
#------------------------------------------------------------------------------
        """
        deletes the selected heat pump in the current alternative
        """
#------------------------------------------------------------------------------
        print "deleteHP: function not yet defined"

        #--> delete HP from the equipment list under current alternative
        
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def selectHeatPump(self,sql,DB,Qid,Aid,PSid,LEVEL):
#------------------------------------------------------------------------------
        """
        Function for selection of heat pump and calculation of the heat flows in it (annual, hourly) on base of
        temperature and time dependent heat demand and availability curves. 
        Arguments:
        sql - MySQL database connector; DB - database einstein;
        Qid - Questionnaire_id; Aid - AlternativeProposalNo; PSid - PSetUpData_ID
        LEVEL - user interaction level (selected from setup menu)
        OPTION - mode of selection 1)OPTI-optimal to match demand-involves search in the HP DB 2)DB-manual from DB or part of DB
        """
#------------------------------------------------------------------------------
        try:
            #Charge the QD and QA curves from the database (previously passed from Joints)  
            chargeCurvesQDQA(sql,DB,Qid,Aid) #????????????????????????????????????????????????  03.03.2008, add errNo.
            #Charge the user-defined data. Three different functions charge the data for the 3 Levels of user interaction
            if LEVEL == 1: #user interaction level 1
                userDefinedLevel1(sql,DB,Qid,Aid) #all data from UHeatPump
            elif LEVEL == 2: #user interaction level 2
                userDefinedLevel2(sql,DB,Qid,Aid,PSid) #some data from UHeatPump, other from PSetUpData
            elif LEVEL == 3:           #user interaction level 3
                userDefinedLevel3(sql,DB,PSid) #all data from PSetUpData
            else:
                pass
                #warning: errNo ????????????????????????????????????????????????????????????????

            DTmax = DTmaxUD
            
            HoursYear = len(QDh) #check later if len(QDh)=len(QAh)

            #check of user input
            if Hop > HoursYear:    #?????????????????????from UHeatPump, err001: "Display warning: Required working hours are greater than the hours of the year!"
                print 'Hop is greater than the hours of the year!'
                print 'The program will be terminated. Exit'        
                exit()

#Calculation Algorithm

####################################################################################
#Previous checks and considerations

#-if the difference between the "minimum demand temperature" (Tmind) (from QDa, Q=0) and the
#"maximum availability temperature" (Tmaxa) (from QAa, Q=0) is greater then the dTmax (limit):
#if so, heat pump should not be considered at all.

            i_Tmind = first_filled(QDa) 
            Tmind = T[i_Tmind]
            print 'Tmind = ', Tmind

            i_Tmaxa = last_filled(QAa)
            Tmaxa = T[i_Tmaxa]
            print 'Tmaxa = ', Tmaxa
                        #DTlim in this case should be the minimum or maximum from the DTlimListDB ????????????????????????
            if Tmind - Tmaxa > maxInList(dtlimListDB): #????? err002: "Display warning: Heat pump application impossible. Temperature lift from QD-QA greater than limit value."
                print 'Heat pump application impossible !!!'
                exit()
        
            else:  #in the case heat pump application is possible: calculate all this...
            
#TODO Note:-store the temperature level at which the heat is delivered and consumed - Th, Tc for each hour
#calculate the modified demand and availability curves after heat pump application.
####################################################################################

#1.Find the start temperature Th0: as maximum T (heat pump upper working limit)(or the user-defined temperature)
            #check if Tmax>Tmax_limit ????????????????????????????errNo.
                Th0 = TmaxUD

                print 'Start temperature (from annual demand curve)'
                print 'Th0, TmaxUD =', Th0, TmaxUD
                print 'TminUD =', TminUD

#2.From the annual Heat demand curve (QDa): calculate the necesary heating capacity (starting value)
                Qh0 = findQfromT(Th0,QDa) #calculates the annual energy demand for the Th_o from QDa
                dotQh0 = Qh0/HoursYear #the initial heat capacity of the heat pump is obtained dividing by the hours of year

##            print 'Initial Annual energy demand Qh0 =', Qh0
##            print 'Assumed hours in year: 3'
##            print 'Estimated initially heat capacity (from QDa) dotQh0 =', dotQh0


#3.Select from HeatPump database the nearest smaller heat capacity (starting value)
# function: selectHeatPumpFromDB()

# j is the index of the selected heat pump in the list DB_Qh (copacities in ascending order)
                j = selectHeatPumpFromDB(dotQh0, qhListDB)  
            #????????????????????????????????????????????? add check-if j<0? errNo : "Warning: There is no heat pump available in DB for this application"
##print 'Selected first smaller heat capacity from database DB_Qh[j] =', DB_Qh[j], 'j =', j

#4.Outest loop: check if the annual operating hours are less than the Hop (user defined minimum)

                Fpla = 0.0 #annual part load factor (initialized) == annual working hours

                while Fpla < Hop and j >= 0: #Outest loop (first while)
                    print 'while-loop 1...'   ############################################from here
                    Tc=[]; Th=[]; COPh=[]; COPht=[]; dotQh=[]; dotQw=[]; dotQc=[] #define lists to store hourly data
                    #resets the lists when passes again
                    Fpli = [] #list to store the part load factor for each hour
                    Fpla = 0.0 #annual part load factor (reset to zero) == annual working hours

#5.Start the hour loop (calculate hourly part-load factor)

                    print 'Start the hour-loop'
                    for i in range(HoursYear): # i is the index for the hours, normally should be from 0 to 8760
                        print 'For-loop, Now is hour i = ', i

                        Th_i = TmaxUD #initialize here
                        Tc_i = TminUD #Cold temperature (related to the heat availability curve)  #initiallized here

        #Find the start Th temperature as the minimum of the corresp. to the DB_Qh[j] from the QDh[i] intersection
        #and TmaxUD
                        Th_i = min(TmaxUD,findTfromDemandCurve(qhListDB[j],QDh[i],T))
        #check here: if Th_i=0 ->assign Fpl_i=0, continue (jump to next loop), Fpl_i.append(Flp_i),all...
                        if Th_i == 0.0:
                            Tc_i=0.0; COPh_i=0.0; COPht_i=0.0;
                            dotQh_i=0.0; dotQw_i=0.0; dotQc_i=0.0
                            Fpl_i=0.0
                            Fpla = Fpla + Fpl_i    #annual part-load factor [hours], does nothing, summs 0
                            Tc.append(Tc_i); Th.append(Th_i); COPh.append(COPh_i); COPht.append(COPht_i);
                            dotQh.append(dotQh_i); dotQw.append(dotQw_i); dotQc.append(dotQc_i);
                            Fpli.append(Fpl_i)
                            continue #continues with the next iteration of the for-loop / skips the rest 
        

                        print 'Starting temperature in the hour calc Th_i =', Th_i, 'qhListDB[j]=', qhListDB[j], 'j=',j

                    #############################################################################################
                        if fabs(Th_i-Tc_i) <= DTmaxUD:
                            DTmax = Th_i - Tc_i - 1.0


                    #############################################################################################

                        COPh_i = cophListDB[j] #assumes initially the COP is = to the nominal DB COP
                    #####################????????????????????????????????????? Add calc. dotQh_i,dotQc_i,dotQw_i
                    #dotQh_i = 

                        print 'Initial hourly COPh_i = ', COPh_i

                        COPh0_i = COPh_i - 1; Th0_i = Th_i - 1; Tc0_i = Tc_i - 1 #assignes start-up values

                        while fabs(Th_i - Tc_i) > DTmax: #while-loop 2 start

##                      print 'while-loop 2...'

                            while fabs(COPh_i - COPh0_i) > 1e-4 or fabs(Th_i - Th0_i) > 1e-4 or fabs(Tc_i - Tc0_i) > 1e-4: #while-loop 3 start

                                print 'while-loop 3...'
                                print 'COPh_i=',COPh_i
                                COPh0_i = COPh_i; Th0_i = Th_i; Tc0_i = Tc_i #assign previous iteration values equal to present values
                                print 'Th_i =', Th_i
                                dotQh_i = findQfromT(Th_i,QDh[i]) #foresee here later unit conversion MWh(QD,QA)->KW(heat pump)

                                print 'Calculated dotQh_i = ', dotQh_i, 'i = ', i

                                dotQw_i = (dotQh_i/COPh_i) #heat pump input power (mechanical or thermal)

                                print 'Calculated dotQw_i = ', dotQw_i, 'i = ', i

                                dotQc_i = dotQh_i - dotQw_i #heat pump cooling power

                                print 'Calculated dotQc_i = ', dotQc_i, 'i = ', i

                                Tc_i = findTfromAvailabCurve(dotQc_i,QAh[i],T) #calc. the temp. corresp. to dotQc_i in QAh[i] curve
                                print 'Calculated Tc_i = ', Tc_i, 'i = ', i, 'Th_i = ', Th_i

                                #check here: if Tc_i=0 -> no heat availability -> assign Fpl_i=0
                                if Tc_i == 0.0:
                                    print '##### dotQc_i, dotQw_i, dotQh_i:', dotQc_i, dotQw_i, dotQh_i
                                    break #goes out of the while-loop 3/ continues in the while-loop 2

#Note: It is better at the moment to assume thet Th,Tc are respectively Tcond,Tevap, later introduce Tsec_fluids instead     
                            #calculate theoretical and real COPs
                                COPht_i = calculateCOPth(HPTypeUD,Th_i,Tc_i, TgeUD)
                                COPh_i = calculateCOP(HPTypeUD,COPht_i,copexListDB,j)
                                
                            #this is the end of while-loop 3

                        #checking if Th_i=0 and Tc_i=0, if yes skips -> Th_i = Th_i - 1.0
                            if Tc_i == 0.0:
                                break #goes out of while-loop 2 / continues in for-loop

                        #if the condition of while-loop 2 (DT>DTmax) remains -> Th_i is decreased with 1K
                            Th_i = Th_i - 1.0

                        #this is the end of the while-loop 2
            
            
          
                        print 'The selected HeatPump has dotQnominal = ', qhListDB[j], 'position in DB: j =', j, 'and...'
                        print '... Calculated hourly heating capacity dotQh_i = ', dotQh_i, 'i = ', i #???????????????????????????????????

                        Fpl_i = dotQh_i/qhListDB[j] #hourly part-load factor

                        Tc.append(Tc_i); Th.append(Th_i); COPh.append(COPh_i); COPht.append(COPht_i);
                        dotQh.append(dotQh_i); dotQw.append(dotQw_i); dotQc.append(dotQc_i);
                        Fpli.append(Fpl_i)
        
                        Fpla = Fpla + Fpl_i    #annual part-load factor [hours] / accumulates working hours
                        print 'Fpl_i, Fpla: ', Fpl_i, Fpla
                        print 'Th_i, Tc_i: ', Th_i, Tc_i
                        print 'ends hour iteration ...................................................'
                    #this is the end of the for-loop

#5.Check if real work hours are less than pre-defined (Fpl<Hop)
#if yes: select smaller heat pump from database - calculate again from point 4
#if not: selection is correct - print results: Fpl, dotQh (from DB), calculate average Tc and Th 

                    j = j - 1 #select the next smaller Heat Pump from the database
                    print 'check operating hours and selects smaller heat pump, now j=',j, '==============================='
                    print 'Fpla = ', Fpla, 'Hop = ', Hop
                    #the outest while-loop finishes, we have the heat pump selected

                #check if j<0: errNo - warning ?????????????????????????????????????????????????????????????????????????????????
                #check if Fpla<Hop : errNo - warning ???????????????????????????????????????????????????????????????????????????
                #compensate the last j=j-1 (when jumped from the while-loop 1)
                j = j + 1
                
                print 'End of search process.'
                print ''
                print 'Heat Pump selected from database: dotQ = ', qhListDB[j], 'j=',j
                print 'Annual working hours: ', Fpla
                print 'User defined minimum working hours: ',Hop
                print ''
                print 'Fpli', Fpli
                print 'Th', Th
                print 'Tc', Tc
                print 'dotQh', dotQh
                print 'dotQw', dotQw
                print 'dotQc', dotQc
                print 'COPh', COPh

#............................................................................................
        except Exception, heatPump: #in case of an error
            print 'exception heatPump', heatPump
            return heatPump

#............................................................................................
        else:       #everything is fine
            return 0
        print 'The program will be terminated. Exit'        

#------------------------------------------------------------------------------
    def calculateEnergyFlows(HPid):
#------------------------------------------------------------------------------
        """
        updates the energy flows in the newly added heat pump 
        """
#------------------------------------------------------------------------------
        print "calculateEnergyFlows: function not yet defined"

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def calculateCascade():
#------------------------------------------------------------------------------
        """
        updates the energy flows for ALL heat pumps, following the cascade
        hierarchy
        """
#------------------------------------------------------------------------------
        for HPid in HPList:
            calculateEnergyFlows(HPid)
#------------------------------------------------------------------------------


#============================================================================== 				

