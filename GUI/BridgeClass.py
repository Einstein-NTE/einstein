#!/usr/bin/env python
# -*- coding: cp1252 -*-

"""
##########################################################################################

EINSTEIN
Expert system for an intelligent supply of thermal energy in industry
www.energyxperts.net

energyXperts.BCN

Ingeniería Termo-energética y Energías Renovables
Thermo-energetical Engineering and Renewable Energies

Dr. Ullés, 2, 3o
08224 Terrassa (Barcelona), Spain


GUI-Modul Version 0.5
2008 by imsai eSoft Heiko Henning
heiko.henning@imsai.de


##########################################################################################
"""


#-----  Imports
import HelperClass
#--- import all your modules here
#TS2008-03-23 Deleted references to ExampleOfYourFunctionsModule
#import ExampleOfYourFunctionsModule




class BridgeToModules():
    
    def __init__(self):
        #----- Initialise
        self.doLog = HelperClass.LogHelper()
        #----- init ExampleOfYourFunctionsModule
        #TS2008-03-23 Deleted references to ExampleOfYourFunctionsModule
        #self.exmod = ExampleOfYourFunctionsModule.ExampleMod()



    def StartPageHeatPump(self, MySql, DB, Qid):
        ret = 0

        return ret
        


    #----- function called from the GUI
    # p.e. the GUI will call this function to start the datacheck
    def FunctionOneDataCheck(self, MySql, DB, Qid):
        # MySql is passed from the GUI to use the MySql.commit() command to finaly store the values in the Database
        # DB is passed from the GUI to access the tables from the Database
        # Qid is passed from the GUI witch contains the active selected Questionnaire_ID
        # call the function from your modules here
        # and provide a result
        self.doLog.LogThis('Starting FunctionOneDataCheck')
        # Here some code to execute
        # call the first function from your module

        # i chose to pass here only "DB" and "Qid" without "MySql", because i think the check don´t
        # need to write to the database, but for the functions who writes to the database you need "MySql" to make a MySql.commit()
        returnvalue = self.exmod.dataCheckDistibutionHC(DB, Qid)
        if returnvalue <> 0:
            self.doLog.LogThis('exmod.dataCheckDistibutionHC returned %s' %(returnvalue))
            return returnvalue
        
        # call the second function from your module
#        returnvalue = self.exmod.dataCheckGenerationHC(DB, Qid)
#        if returnvalue <> 0:
#            self.doLog.LogThis('exmod.dataCheckGenerationHC returned %s' %(returnvalue))
#            return returnvalue
        
        # if no errors happend this function will end here an return a 0 to the GUI
        return 0









    

    def FunctionTwo(self, MySql, DB, Qid):
        # call the function from your modules here
        # and provide a return value
        

        return 0
        
