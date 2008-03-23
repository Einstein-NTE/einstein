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
#	Dummy module for simulating the GUI running the HP module
#       using the structure of the BridgeClass.py
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	07/03/2008
#	Last revised by:    ---      ---
#
#       Changes to previous version:
#       ----
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

import einstein.GUI.pSQL as pSQL, MySQLdb
sql = MySQLdb.connect(user="root", db="einstein")
DB = pSQL.pSQL(sql, "einstein")

import einstein.GUI.HelperClass as HelperClass
import einstein.modules.heatPump.ModuleHP as HP


class BridgeToModules():
    
    def __init__(self):
        #----- Initialise
        self.doLog = HelperClass.LogHelper()
        #----- init Modules
        self.modHP = HP.ModuleHP()

    def RunSelectHeatPump(self,sql,DB):
        self.modHP.selectHeatPump(sql,DB,Qid,Aid,PSid,LEVEL)
        return 0
        
Qid = 1
Aid = 1
PSid = 1
LEVEL = 2

ModBridge = BridgeToModules()
ModBridge.RunSelectHeatPump(sql,DB)

