# -*- coding: cp1252 -*-
#==============================================================================#
#   E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#   ModulePO (Process Optimisation)
#           
#------------------------------------------------------------------------------
#           
#   
#
#==============================================================================
#
#   Version No.: 0.01
#   Created by:         Florian Joebstl 24/09/2008  
#
#
#
#
#   
#------------------------------------------------------------------------------

from einstein.GUI.status import *
from einstein.modules.messageLogger import *


class ModulePO(object):

    def __init__(self, keys):
        self.keys = keys # the key to the data is sent by the panel       
                       

    def initPanel(self):         
        self.updatePanel()
              
    def updatePanel(self):
        pass        
          
    def runPOModule(self):
       pass 
            
        
  