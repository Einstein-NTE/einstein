# -*- coding: cp1252 -*-
#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#	GUI Tools
#
#------------------------------------------------------------------------------
#
#       Common functions used in sevaral GUI panels
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger      03/05/2008
#
#       Changes to previous versions:
#
#------------------------------------------------------------------------------
#	(C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#	http://www.energyxperts.net/
#
#	This program is free software: you can redistribute it or modify it under
#	the terms of the GNU general public license as published by the Free
#	Software Foundation (www.gnu.org).
#
#==============================================================================

import wx
import pSQL
import HelperClass
from status import Status
from einstein.modules.constants import *

#------------------------------------------------------------------------------
def fillChoice(choice,choiceList,nonePossible=True):
#------------------------------------------------------------------------------
#   fills the list of possible choices from a list of strings
#------------------------------------------------------------------------------
    choice.Clear()
    if nonePossible==True:choice.Append("None")
    for c in choiceList:choice.Append(str(c))
    choice.SetSelection(0)
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
def setChoice(choice,strChoice):
#------------------------------------------------------------------------------		
#   sets a choice to the string
#------------------------------------------------------------------------------		
    try:choice.SetSelection(choice.FindString(strChoice))
    except:choice.SetSelection(choice.FindString("None"))
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------
def check(value):
#------------------------------------------------------------------------------
#   auxiliary function. substitutes ""'s and None's by 'NULL'
#   (should be moved some day to a separate file with sql-tools ...)
#------------------------------------------------------------------------------
    if value <> "" and value <> "None":
        return value
    else:
        return 'NULL'
#==============================================================================

        
