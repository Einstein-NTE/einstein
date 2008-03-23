# -*- coding: cp1252 -*-
#============================================================================== 				
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	CCheck (Consistency Check)
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Functions for consistency checking of data
#
#==============================================================================
#
#	Version No.: 0.02
#	Created by: 	    Hans Schweiger	08/03/2008
#	Last revised by:    Hans Schweiger      17/03/2008
#
#       Changes in last update:
#
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

EPSILON = 1.e-3     # required accuracy for function "isequal"
INFINITE = 1.e99    # numerical value assigned to "infinite"

from math import *

#------------------------------------------------------------------------------
class CCheck():
#------------------------------------------------------------------------------
#   Main class for carrying out consistency checking
#------------------------------------------------------------------------------

    def run(self):

        print "here should be the main module for consistency checking "

#------------------------------------------------------------------------------
class CCPar():
#------------------------------------------------------------------------------
#   Class for grouping value and attributes of a parameter
#------------------------------------------------------------------------------

    val = None
    sqerr = None
    sqdev = None
    name = "not defined"
    lowerLimit = None
    upperLimit = None

    def __init__(self,s):
        self.name = s

    def update(self,new):
        self.val = new.val
        self.sqerr = new.sqerr

    def show(self):
        print "%s = "%self.name,self.val,"(sqerr: %s)"%self.sqerr


#------------------------------------------------------------------------------
def calcProd(yname,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------

    y = CCPar(yname)

    if (x1.val ==None or x2.val==None):
        y.val = None
        y.sqerr = None
    else:
        y.val = x1.val * x2.val
        y.sqerr = x1.sqerr + x2.sqerr
    return y
    
#------------------------------------------------------------------------------
def calcSum(yname,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------
    y = CCPar(yname)
    if (x1.val ==None or x2.val==None):
        y.val = None
        y.sqerr = None
    else:
        y.val = x1.val + x2.val
        if (y <> 0):
            y.sqerr = (x1.sqerr*pow(x1.val,2) + x2.sqerr*pow(x2.val,2))/pow(y.val,2)
        else:
            y.sqerr = INFINITE
    return y
    

#------------------------------------------------------------------------------
def adjustProd(y,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------


##### missing 1: the "none" - check.
##### missing 2: what if sqerr of 1 and 2 are different, but very similar ???
    
    if not (y.val == None):
        if not (x1.val == None) and ((x1.sqerr < x2.sqerr) or (x2.val == None)):
            if (x1.val ==0):
                x2.val = INFINITE
                x2.sqerr = INFINITE
            else:
                x2.val = y.val / x1.val
                x2.sqerr = y.sqerr + x1.sqerr
        elif not (x2.val == None):
            if (x2.val ==0):
                x1.val = INFINITE
                x1.sqerr = INFINITE
            else:
                x1.val = y.val / x2.val
                x1.sqerr = y.sqerr + x2.sqerr
            
    
#------------------------------------------------------------------------------
def adjustSum(y,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------

##### missing 1: the "none" - check.
##### missing 2: what if sqerr of 1 and 2 are different, but very similar ???

    if not (y.val == None):
        y.sqdev = y.sqerr*pow(y.val,2)
        if not (x1.val==None) and ((x1.sqdev < x2.sqdev) or x2.val ==None):
            x1.sqdev = x1.sqerr*pow(x1.val,2)
        
            x2.val = y.val - x1.val
            x2.sqdev = y.sqdev + x1.sqdev
            if (x2.val == 0):
                x2.sqerr = INFINITE
            else:
                x2.sqerr = x2.sqdev/pow(x2.val,2)
        elif not (x2.val == None):
            x2.sqdev = x2.sqerr*pow(x2.val,2)

            x1.val = y.val - x2.val
            x1.sqdev = y.sqdev + x2.sqdev
            if (x2.val ==0):
                x1.sqerr = INFINITE
            else:
                x1.sqerr = x1.sqdev/pow(x1.val,2)
       
    
#------------------------------------------------------------------------------
def ccheck1(y0,y1):
#------------------------------------------------------------------------------
#   Carries out consistency checking of the actual value with one external
#   calculated input.
#------------------------------------------------------------------------------

    ccheckMsg = []
    
    if (y0.val == None and y1.val == None): #Case 1: Nothing to do
        print "CCHECK(%s) - Case1: all parameters are unknown. Calculation of Pnom not possible"%y0.name
        ccheckMsg.append("All parameters are unknown: calculation not possible")
        
    elif y1.val == None: #Case 2: Pnom1 = ok, Pnom2 = None
        print "Case 2: Pnom1 = ok, Pnom2 = None then Pnom2 adjusted"
        y1.update(y0)
                
    elif y0 == None: #case 3: Pnom1 = None, Pnom2 = ok
        print "case 3: Pnom1 = None, Pnom2 = ok then Pnom1 adjusted" 
        y0.update(y1)
               
    else: #case 4 Pnom1 = ok, Pnom2 = ok
        if y0.sqerr <= y1.sqerr:   #case 4
            print "Case4: Pnom1 and Pnom2 redundant and consistent"
            y1.update(y0)
        else:
            print "Case4: Pnom1 and Pnom2 redundant but not consistent"
            y0.update(y1)

#------------------------------------------------------------------------------
def ccheck2(y0,y1,y2):
#------------------------------------------------------------------------------
#   Carries out consistency checking of the actual value with two externally
#   calculated inputs.
#------------------------------------------------------------------------------
#..............................................................................

#XXX from ccheckUSH
    HUGE = 1.e99
    ccheckMsg = []

    y = CCPar("CCheck2")

    if y1.val == None: 
        if y2.val == None:
            if y0.val == None:
#..............................................................................
#Case 1: Nothing to do
                
                print "Case 1: all parameters are unknown. Calculation not possible"
                ccheckMsg.append("Case 1: all parameters are unknown. Calculation not possible")
                y.val = None
                y.sqerr = None

            else:               
#..............................................................................
#Case 2: USH3 known, USH1 unknown,USH2 unknown,
                y.update(y0)
                print "Case 2: USH3 known. USH1 and USH2 adjusted"
             
        else:
            if y0.val == None:
#..............................................................................
#Case 3: USH3 unknown, USH1 unknown,USH2 known

                y.update(y2)
                print "Case 3: USH2 known. USH1 and USH3 adjusted"
                
            else:
#..............................................................................
#Case 4: USH3 known, USH1 unknown,USH2 known
                if isequal(y2.val, y0.val):
                    print "Case4: USH1 unknown. USH2 and USH3 redundant and consistent"
                else:
                    print "Case4: USH1 unknown. USH2 and USH3 redundant and not consistent"

                y = bestOf(y0,y2)
                    
    else:
        if y2.val == None:
            if y0.val == None:
#..............................................................................
#Case 5: USH3 unknown, USH1 known,USH2 unknown,
                y.update(y1)
                print "Case 5: USH1 known. USH2 and USH3 adjusted"
                
            else:
#..............................................................................
#Case 6: USH3 known, USH1 known,USH2 unknown,
                if isequal(y1.val, y0.val):
                    print "Case6: USH2 unknown. USH1 and USH3 redundant and consistent"
                else:
                    print "Case6: USH2 unknown. USH1 and USH3 redundant and not consistent"

                y = bestOf(y0,y1)
                    
        else:
            if y0.val == None:
#..............................................................................
#Case 7: USH3 unknown, USH1 known,USH2 known,
                if isequal(y1.val, v2.val):
                    print "Case7: USH3 unknown. USH2 and USH1 redundant and consistent"
                else:
                    print "Case7: USH3 unknown. USH2 and USH1 redundant and not consistent"

                y = bestOf(y1,y2)
                                        
            else:
    
#..............................................................................
# Case 8:USH3 known, USH1 known,USH2 known,

                    y = bestOf3(y0,y1,y2)
                                                        
                    if not isequal(y.val,y1.val):
                        print " Case8: USH1, USH2, USH3 known and USH1 to be adjusted"
             
                    if not isequal(y.val,y2.val):
                        print "Case8: USH1, USH2, USH3 known and USH2 to be adjusted"
             
                    if not isequal(y.val,y0.val):
                        print "Case8: USH1, USH2, USH3 known and USH3 to be adjusted"
             
#..............................................................................
# Updating values

    y0.update(y)
    y1.update(y)
    y2.update(y)



#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def bestOf(y1,y2):
#------------------------------------------------------------------------------
#   Selects the best of three values (the one with lowest errors)
#   Does not carry out None-check !!!!
#------------------------------------------------------------------------------

    if (y1.sqerr < y2.sqerr):
            best = y1
    else:
            best = y2
    return best   

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def bestOf3(y1,y2,y3):
#------------------------------------------------------------------------------
#   Selects the best of three values (the one with lowest errors)
#   Does not carry out None-check !!!!
#------------------------------------------------------------------------------

    best = bestOf(y1,y2)
    best = bestOf(best,y3)
    return best   

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def isequal(a,b):
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------

    try:
        if (fabs(a-b) < EPSILON):
            return True
        else:
            return False

    except Exception:
        return False

    else:
        pass
        


#==============================================================================

if __name__ == "__main__":


    def showAll():

        global PNom,TOpNom,FETj,HCGEfficiency,USH,USH1,USHBoiler1,USHBoiler2
        
        print "====================="
        PNom.show()
        PNom1.show()
        FuelConsum.show()
        TOpNom.show()
        TOpNom1.show()
        TOp.show()
        TOp1.show()
        HPerDay.show()
        NDaysEq.show()
        PartLoad.show()
        FETj.show()
        HCGEfficiency.show()
        USH.show()
        USH1.show()
        USHBoiler1.show()
        USHBoiler2.show()
        USHBoiler.show()
        print "====================="
        
# Step 0: Assign all a priori known values to variables.
#   -> here manually. in tool values substituted by import from SQL

    PNom = CCPar("PNom")
    PNom.val = 1000
    PNom.sqerr = 0.0   #example: nominal power is exactly given (manufacturer parameter !)€
    
    FuelConsum = CCPar("FuelConsum")
    PNom.val = 1300
    PNom.sqerr = 0.1   #
    
    NDaysEq = CCPar("NDaysEq")
    NDaysEq.val = 260 # 5 days/week
    NDaysEq.sqerr = 0.0  #example: big uncertainty in operating hours

    HPerDay = CCPar("HPerDay")
    HPerDay.val = 10
    HPerDay.sqerr = 0.3  #example: uncertainty in operating hours

    TOp = CCPar("TOp")
    TOp.val = 6000
    TOp.sqerr = 0.5  #example: big uncertainty in operating hours

    PartLoad = CCPar("PartLoad")
    PartLoad.val = 0.5
    PartLoad.sqerr = 0.5  #example: big uncertainty in operating hours

    TOpNom = CCPar("TOpNom")
    TOpNom.val = 4000
    TOpNom.sqerr = 0.5  #example: big uncertainty in operating hours
    
    USH = CCPar("USH")
    USH.val = 5e+6
    USH.sqerr = 0.05    #example: quantity of heat produced is well known

    FETj = CCPar("FETj")
    FETj.val = None
    FETj.sqerr = None    #example: fuel consumption can approximately estimated from fuel balances

    HCGEfficiency = CCPar("HCGEfficiency")
    HCGEfficiency.val = 0.8
    HCGEfficiency.sqerr = 0.03    #efficiency rather well known ...

    QHX = CCPar("QHX")
    QHX.val = 1.e+6
    QHX.sqerr = 0

# assign a variable to all intermediate values needed

    USH1 = CCPar("USH1")

    USHBoiler1 = CCPar("USHBoiler1")
    USHBoiler2 = CCPar("USHBoiler2")
    USHBoiler = CCPar("USHBoiler")

    PNom1 = CCPar("PNom1")
    TOpNom1 = CCPar("TOpNom1")
    TOp1 = CCPar("TOp1")

    showAll()

    for n in range(4):

        print "-------------------------------------------------"
        print "Ciclo %s"%n
        print "-------------------------------------------------"
        
# Step 1: Call all calculation routines in a given sequence

        print "Step 1: calculating from left to right (CALC)"
        TOp1 = calcProd("TOp1",HPerDay,NDaysEq)
        TOpNom1 = calcProd("TOpNom1",TOp,PartLoad)
        PNom1 = calcProd("PNom1",FuelConsum,HCGEfficiency)
        USHBoiler1 = calcProd("USH1",PNom,TOpNom)
        USHBoiler2 = calcProd("USH2",FETj,HCGEfficiency)
        USH1 = calcSum("USH1",USHBoiler,QHX)

        showAll()

# Step 2: Cross check the variables

        print "Step 2: cross checking"

        ccheck1(TOp,TOp1)
        ccheck1(TOpNom,TOpNom1)
        ccheck1(PNom,PNom1)
        ccheck2(USHBoiler,USHBoiler1,USHBoiler2)
        ccheck1(USH,USH1)

        showAll()

# Step 3: Adjust the variables (inverse of calculation routines)

        print "Step 3: calculating from right to left (ADJUST)"
        
        adjustSum(USH1,USHBoiler,QHX)
        adjustProd(USHBoiler1,PNom,TOpNom)
        adjustProd(USHBoiler2,FETj,HCGEfficiency)
        adjustProd(PNom1,FuelConsum,HCGEfficiency)
        adjustProd(TOpNom1,TOp,PartLoad)
        adjustProd(TOp1,HPerDay,NDaysEq)

        showAll
    

    
    
#==============================================================================
