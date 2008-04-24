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
#	Version No.: 0.08
#	Created by: 	    Hans Schweiger	08/03/2008
#	Last revised by:    Claudia Vannoni     9/04/2008
#                           Hans Schweiger      09/04/2008
#                           Claudia Vannoni     16/04/2008
#                           Claudia Vannoni     17/04/2008
#                           Hans Schweiger      18/04/2008
#                           Hans Schweiger      23/04/2008
#                           Hans Schweiger      24/04/2008
#
#       Changes in last update:
#       09/04/08    Change in adjustProd ..
#                   def init
#       09/04/08 HS Functions meanValueOf added;
#                   ccheck - functions adapted
#                   adjustProd - simulataneous adjustment of both variables
#	16/04/08 CV adjustSum3 modified, calcFlow and adjustFlow
#       17/04/08 CV calcK and adjustcalcK
#       18/04/08 HS valMin and valMax included in most functions
#                   constraints actually applied (function "constrain" in CCPar)
#                   general testing and correction of several bugs
#       23/04/08 HS method setValue added in CCPar
#       24/04/08 HS added method "screen" in CCPar
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

EPSILON = 1.e-10     # required accuracy for function "isequal"
INFINITE = 1.e99    # numerical value assigned to "infinite"
DEFAULT_SQERR = 1.e-4 # default value for sqerr assigned to questionnaire values
NUMERIC_ERR = 1.e-10 # accuracy of numeric calculations
MAX_SQERR = 1       # critical square error for screening

CONFIDENCE = 2      #maximum relation between statistical square error and abs.min/max

DEBUG = "BASIC" #Set to:
                #"ALL": highest level,
                #"CALC": only debug in CALC Functions
                #"ADJUST": only debug in ADJUST Functions
                #"BASIC": basic debugging (not yet implemented)
                #"OFF" or any other value ...: doesn't print anything

TEST = True
TESTCASE = 3
                
from math import *

#------------------------------------------------------------------------------
class CCPar():
#------------------------------------------------------------------------------
#   Class for grouping value and attributes of a parameter
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def __init__(self,s):
#------------------------------------------------------------------------------
        self.name = s
        self.val = None
        self.sqerr = INFINITE
        self.sqdev = INFINITE

        self.valMin = 0         #default: non-negative values !!!!
        self.valMax = INFINITE

#------------------------------------------------------------------------------
    def update(self,new):
#------------------------------------------------------------------------------
        self.val = new.val
        self.sqerr = new.sqerr
        self.valMin = new.valMin
        self.valMax = new.valMax

#------------------------------------------------------------------------------
    def setValue(self,val,err=DEFAULT_SQERR):
#------------------------------------------------------------------------------
#   function to be used for setting values from data questionnaire
#   sets default values to errors
#------------------------------------------------------------------------------
        self.val = val
        if val is None:
            self.sqerr = INFINITE
        elif val == 0:
            self.sqerr = 0
        else:
            self.sqerr = err
        self.constrain

#------------------------------------------------------------------------------
    def constrain(self):
#------------------------------------------------------------------------------

        if (self.valMin > self.valMax + NUMERIC_ERR):

            print "======================================================"
            print "======================================================"
            print "%s.CONSTRAIN: SEVERE ERROR - MIN > MAX VALUE !!!! "%self.name
            self.show()
            print "======================================================"
            print "======================================================"

            newMax = self.valMin
            newMin = self.valMax
            self.valMin = newMin
            self.valMax = newMax

#.............................................................................
# general control: min/max values between [0,INFINITE] and min < max

        self.valMin = max(self.valMin,0)
        self.valMax = min(self.valMax,INFINITE)
            
        if self.val is not None:

            if (self.val > 0):

#.............................................................................
# first set absolute constraint of the value to reasonable limits around its
# actual value - in function of the specified error margins

                errMax = CONFIDENCE*pow(self.sqerr,0.5)
                self.valMin = max(self.valMin,self.val*max(1-errMax,0))
                self.valMin = min(self.valMin,self.valMax) #new min can not be higher as max
                
                self.valMax = min(self.valMax,self.val*(1+errMax))
                self.valMax = max(self.valMin,self.valMax) #new max can not be lower than min

#.............................................................................
# consider that the error can not be larger than [maxVal - minVal]

                try:    #helps to avoid crash for very large errors
                    self.sqerr = min(self.sqerr,pow((self.valMax-self.valMin)/self.val,2))
                except:
                    pass

                self.sqerr = min(self.sqerr,INFINITE)

#.............................................................................
# special case: exact zero

            elif self.val==0 and self.sqerr==0:
                self.valMin = 0.0
                self.valMax = 0.0

#.............................................................................
# and finally constrain the value itself within the allowed limits

            self.val = min(self.val,self.valMax)
            self.val = max(self.val,self.valMin)

#.............................................................................
# check for all values larger than 0 !!!
# if constrain in between min/max works, and min> 0, the following should be unnecessary

            if self.val < 0:
                print "======================================================"
                print "======================================================"
                print "%s.CONSTRAIN: SEVERE ERROR - VALUE < 0 !!!! "%self.name
                self.show()
                print "======================================================"
                print "======================================================"
                
#------------------------------------------------------------------------------
    def show(self):
#------------------------------------------------------------------------------
        print "%s = "%self.name,self.val,"(sqerr: %s)"%self.sqerr,"[%s"%self.valMin,",%s"%self.valMax,"]"
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def screen(self):
#------------------------------------------------------------------------------
#   creates a register entry if the parameter is None or with a high error
#------------------------------------------------------------------------------
        CCScreen.nScreened += 1
        
        if (self.val == None):
            CCScreen.screenList.append([self.name,self.val,"-"])
        elif (self.sqerr > MAX_SQERR):
            err = pow(self.sqerr,0.5)*100
            CCScreen.screenList.append([self.name,self.val, str(err)+"%"])
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def CCRow(name,m):
#------------------------------------------------------------------------------
#   Builds up rows of CCPars
#------------------------------------------------------------------------------

    row = []
    for i in range(m):
        row.append(CCPar(name+"["+str(i)+"]"))
    return row

#------------------------------------------------------------------------------
def CCOne():
#------------------------------------------------------------------------------
#   Builds up matrix
#------------------------------------------------------------------------------

    one = CCPar("1")
    one.val = 1.0
    one.sqerr = 0
    one.sqdev = 0
    one.valMin = 1.0
    one.valMax = 1.0
    
    return one
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class CCScreen():
#------------------------------------------------------------------------------
#   module for screening of errors and missing data
#------------------------------------------------------------------------------

    screenList = []
    nScreened = 0
    
    def __init__(self):
        self.reset()

    def reset(self):
        CCScreen.screenList = []
        CCScreen.nScreened = 0

    def show(self):
        print "CCScreen: %s parameters screened"%len(CCScreen.screenList)
        for i in range(len(CCScreen.screenList)):
            print i+1, CCScreen.screenList[i]

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class Cycle():
#------------------------------------------------------------------------------
#   Class for grouping value and attributes of a parameter
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def __init__(self,itMax,maxDifference,minImprovement,itMaxImprove):
#------------------------------------------------------------------------------
        self.itMax  = itMax                     #absolute maximum number of iterations
        self.maxDifference = maxDifference      #maximum difference in precision below which cycle stops
        self.minImprovement = minImprovement    #min. improvement required below which cycle stops
        self.itMaxImprove = itMaxImprove        #maximum number of iterations for trying if there's still
                                                #improvement possible

#------------------------------------------------------------------------------
    def initCycle(self):
#------------------------------------------------------------------------------
        self.itCtr = 0
        self.itImproveCtr = 0
        self.lastDiff = INFINITE
        self.diff = 0.5*INFINITE
        self.nChecks = 0

#------------------------------------------------------------------------------
    def count(self,diff):
#------------------------------------------------------------------------------
        self.diff += abs(diff)
        self.nChecks += 1
        
#------------------------------------------------------------------------------
    def converged(self):
#------------------------------------------------------------------------------

        if (self.nChecks > 0):
            self.diff /= self.nChecks

        self.improvement = self.lastDiff - self.diff
        if self.diff < self.maxDifference or self.improvement <= 0:
            self.itImproveCtr +=1
        else:
            self.itImproveCtr = 0
        self.lastDiff = self.Diff

        if self.itImproveCtr >= self.itMaxImprove:
            return True
        else:
            return False
        

#============================================================================== 				
# Global CCheck auxiliary functions
#============================================================================== 				

#------------------------------------------------------------------------------
def calcK(yname,a,x1):
#------------------------------------------------------------------------------
#   Default function for calculating the product among a value and a constant
#------------------------------------------------------------------------------
    y = CCPar(yname)

    if (x1.val ==None):
        y.val = None
        y.sqerr = INFINITE
    else:
        y.val = a * x1.val
        y.sqerr = x1.sqerr

    y.valMin = a*x1.valMin
    y.valMax = min(INFINITE,a*x1.valMax)
    y.constrain()

    return y

#------------------------------------------------------------------------------
def calcProd(yname,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------

    y = CCPar(yname)

    if (x1.val == 0 and x1.sqerr == 0) or (x2.val == 0 and x2.sqerr == 0):
        y.val = 0
        y.sqerr = 0
    elif (x1.val ==None or x2.val==None):
        y.val = None
        y.sqerr = INFINITE
    else:
        y.val = x1.val * x2.val
        y.sqerr = x1.sqerr + x2.sqerr

    y.valMin = x1.valMin * x2.valMin
    y.valMax = min(INFINITE,x1.valMax*x2.valMax)
    y.constrain()

    if DEBUG in ["ALL","CALC"]:
        print "CalcProd(x1,x2)____________________________________"
        x1.show()
        x2.show()
        print "x1*x2 = "
        y.show()
        print "___________________________________________________"

    return y

#------------------------------------------------------------------------------
def calcProdC(yname,a,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the product among two values and a constant
#------------------------------------------------------------------------------
    y = CCPar(yname)
    
    if (x1.val == 0 and x1.sqerr == 0) or (x2.val == 0 and x2.sqerr == 0):
        y.val = 0
        y.sqerr = 0
    elif (x1.val ==None or x2.val==None):
        y.val = None
        y.sqerr = INFINITE
    else:
        y.val = a * x1.val * x2.val
        y.sqerr = x1.sqerr + x2.sqerr

    y.valMin = a*x1.valMin * x2.valMin
    y.valMax = min(INFINITE,a*x1.valMax*x2.valMax)
    y.constrain()

    if DEBUG in ["ALL","CALC"]:
        print "CalcProdC(x1,x2)___________________________________"
        x1.show()
        x2.show()
        print "x1*x2 = "
        y.show()
        print "___________________________________________________"
    
    return y  

#------------------------------------------------------------------------------
def calcSum(yname,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------
    y = CCPar(yname)
    if (x1.val ==None or x2.val==None):
        y.val = None
        y.sqerr = INFINITE
    else:
        y.val = x1.val + x2.val
        if (y.val <> 0.0):
            y.sqerr = (x1.sqerr*pow(x1.val,2) + x2.sqerr*pow(x2.val,2))/pow(y.val,2)
        elif iszero(x1) and iszero(x2):
            y.sqerr = 0.0
        else:
            y.sqerr = INFINITE

    y.valMin = min(INFINITE,x1.valMin + x2.valMin)
    y.valMax = min(INFINITE,x1.valMax + x2.valMax)
    y.constrain()

    if DEBUG in ["ALL","CALC"]:
        print "CalcSum(x1,x2)_____________________________________"
        x1.show()
        x2.show()
        print "x1*x2 = "
        y.show()
        print "___________________________________________________"

    return y
    
#------------------------------------------------------------------------------
def calcSum3(yname,x1,x2,x3): # To be replaced by the matrixsumcalc
#------------------------------------------------------------------------------
#   Default function for calculating the sum of 3 values
#------------------------------------------------------------------------------

    y = CCPar(yname)
    if (x1.val ==None or x2.val==None or x3.val==None ):
        y.val = None
        y.sqerr = INFINITE
    else:
        y.val = x1.val + x2.val + x3.val
        if (y.val <> 0):
            y.sqerr = (x1.sqerr*pow(x1.val,2)+ x2.sqerr*pow(x2.val,2)+ x3.sqerr*pow(x3.val,2))/pow(y.val,2)
        elif iszero(x1) and iszero(x2) and iszero(x3):   # all the three are exactly zero
            y.sqerr = 0
        else:                                           #if one is not excactly zero
            y.sqerr = INFINITE

    y.valMin = x1.valMin + x2.valMin + x3.valMin
    y.valMax = min(INFINITE,x1.valMax+x2.valMax+x3.valMax)

    y.constrain()

    if DEBUG in ["ALL","CALC"]:
        print "CalcSum3(x1,x2,x3)_________________________________"
        x1.show()
        x2.show()
        x3.show()
        print "x1+x2+x3 = "
        y.show()
        print "___________________________________________________"
    
    return y

#------------------------------------------------------------------------------
def calcRowSum(name,row,m):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------
    y = CCPar(name)
    (nones,isnone) = countNones(row)

#..............................................................................
#   Case 1: all values are defined 

    if nones == 0:
        y.sqerr = 0
        y.valMin = 0
        y.valMax = 0
        y.val = 0
        for i in range(len(row)):
            y.val += row[i].val
            y.sqerr += row[i].sqerr*pow(row[i].val,2)
            y.valMin += row[i].valMin
            y.valMax += row[i].valMax
            y.valMax = min(y.valMax,INFINITE)

        if (y.val <> 0):
            y.sqerr /= pow(y.val,2)
        elif y.sqerr <> 0:              # implicitely treats special case: all zeroes
            y.sqerr = INFINITE  

#..............................................................................
#   Case 2: any of the values is None 

    else:
        y.val = None
        y.sqerr = INFINITE

        for i in range(len(row)):
            y.valMin += row[i].valMin
            y.valMax += row[i].valMax
            y.valMax = min(y.valMax,INFINITE)

    y.constrain()

    if DEBUG in ["ALL","CALC"]:
        print "CalcRowSum(y,row)__________________________________"
        for i in range(len(row)):
            row[i].show()
        print "y = SUM x[i] = "
        y.show()
        print "___________________________________________________"

    return y
    

#------------------------------------------------------------------------------
def calcDiff(yname,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the difference of two values
#------------------------------------------------------------------------------

    y = CCPar(yname)
    if (x1.val is None or x2.val is None):
        y.val = None
        y.sqerr = INFINITE
    else:
        y.val = x1.val - x2.val
        if (y.val <> 0):
            y.sqerr = (x1.sqerr*pow(x1.val,2) + x2.sqerr*pow(x2.val,2))/pow(y.val,2)
        elif iszero(x1) and iszero(x2):   # all the two are exactly zero
            y.sqerr = 0
        else:
            y.sqerr = INFINITE

    y.valMin = max(x1.valMin - x2.valMax,0)
    y.valMax = max(x1.valMax - x2.valMin,0)

    y.constrain()
    
    if DEBUG in ["ALL","CALC"]:
        print "CalcDiff(x1,x2)____________________________________"
        x1.show()
        x2.show()
        print "x1-x2 = "
        y.show()
        print "___________________________________________________"

    return y

#------------------------------------------------------------------------------
def calcFlow(Qdotname,cp,m,T1,T0,DT,DT1):
#------------------------------------------------------------------------------
#   Default function for calculating the power required to increase the temperature of a mass flow m at a starting temperature T0 up to the final temperature T1
#------------------------------------------------------------------------------
    Qdot = CCPar (Qdotname)
    diff = CCPar

    diff = calcDiff(DT.name,T1,T0)
    
    DT.update(diff)
    ccheck1(DT,DT1)
    
    if DEBUG in ["ALL","CALC"]:
        print "CalcFlow-DT________________________________________"
        T1.show()
        T0.show()
        print "DT = T1 - T0 = "
        DT.show()
        DT1.show()
        print "___________________________________________________"

    
    Qdot = calcProdC(Qdotname,cp,m,DT1)

    if DEBUG in ["ALL","CALC"]:
        print "CalcFlow-Qdot______________________________________"
        m.show()
        print "cp = ",cp
        print "Qdot = m*cp*DT = "
        Qdot.show()
        print "___________________________________________________"
    
    return Qdot

#------------------------------------------------------------------------------
def adjustcalcK(y,a,x1):
#------------------------------------------------------------------------------
#   Default function for calculating and adjusting the product between a value and a constant
#------------------------------------------------------------------------------

    if not (y.val == None):
        
        x1.val = y.val /a
        x1.sqerr = y.sqerr

    x1.valMin = min(y.valMin/a,INFINITE)
    x1.valMax = min(y.valMax/a,INFINITE)

    x1.constrain()
        
#------------------------------------------------------------------------------
def adjustProd(y,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","ADJUST"]:
        print "___________________________________________________"
        print "adjustProd starting",x1.name,x2.name
        y.show()
        x1.show()
        x2.show()

    if not (y.val == None):
        if not (x1.val == None) and ((x1.sqerr < x2.sqerr) or (x2.val == None)):
            if (x1.val ==0):
                if y.val > 0:
                    x2.val = INFINITE
                    x2.sqerr = INFINITE
            else:
                x2.val = y.val / x1.val
                x2.sqerr = min(y.sqerr + x1.sqerr,x2.sqerr)
        elif not (x2.val == None):
            if (x2.val ==0):
                if y.val > 0:
                    x1.val = INFINITE
                    x1.sqerr = INFINITE
            else:
                x1.val = y.val / x2.val
                x1.sqerr = min(y.sqerr + x2.sqerr,x1.sqerr)

    if (x2.valMax > 0):
        x1.valMin = min(y.valMin/x2.valMax,INFINITE)
    elif (y.valMin > 0):
        x1.valMin = INFINITE

    if (x2.valMin > 0):
        x1.valMax = min(y.valMax/x2.valMin,INFINITE)
    elif (y.valMax > 0):
        x1.valMax = INFINITE

    if (x1.valMax > 0):
        x2.valMin = min(y.valMin/x1.valMax,INFINITE)
    elif (y.valMin > 0):
        x2.valMin = INFINITE

    if (x1.valMin > 0):
        x2.valMax = min(y.valMax/x1.valMin,INFINITE)
    elif (y.valMax > 0):
        x2.valMax = INFINITE

    x1.constrain()
    x2.constrain()

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustProd_________________________________________"
        y.show()
        x1.show()
        x2.show()
        print "___________________________________________________"

            
#------------------------------------------------------------------------------
def adjustProdS(y,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","ADJUST"]:
        print "___________________________________________________"
        print "adjustProdS starting",x1.name,x2.name
        y.show()
        x1.show()
        x2.show()
    
    if not (y.val == None):
#..............................................................................
#Case 1: both x1 and x2 unknown
        
        if (x1.val == None and x2.val == None):
            pass

#..............................................................................
#Case 2: x1 known, x2 = None
        
        elif (not (x1.val == None) and x2.val == None):
            if (x1.val ==0) and (y.val > 0):
                x2.val = INFINITE
                x2.sqerr = INFINITE
            elif (x1.val > 0):
                x2.val = y.val / x1.val
                x2.sqerr = y.sqerr + x1.sqerr
                                    
#..............................................................................
#Case 3: x2 known, x1 = None
        elif (x1.val == None and not (x2.val == None)):
            if (x2.val ==0 and y.val > 0):
                x1.val = INFINITE
                x1.sqerr = INFINITE
            elif (x2.val > 0):
                x1.val = y.val / x2.val
                x1.sqerr = y.sqerr + x2.sqerr

#..............................................................................
#Case 4: x1 and x2 known. simultaneous adjustment of both
        else:
            yold = x1.val*x2.val

            if (yold ==0):
                if (x1.val == 0 and x2.val ==0):
                    if (y.val <> 0):
                        x1.val = pow(y.val,0.5)
                        x2.val = pow(y.val,0.5)
                        x1.sqerr = INFINITE
                        x2.sqerr = INFINITE
                elif (x1.val == 0 and x2.val <> 0):
                    x1.val = y.val/x2.val
                    x1.sqerr = min(y.sqerr + x2.sqerr,x1.sqerr)
                    
                elif (x2.val == 0 and x1.val <> 0):
                    x2.val = y.val/x1.val
                    x2.sqerr = min(y.sqerr + x1.sqerr,x2.sqerr)

            else:
                if (x1.sqerr + x2.sqerr)==0:
                    f1 = 0.5
                    f2 = 0.5
                else:
                    f1 = x1.sqerr/(x1.sqerr + x2.sqerr)
                    f2 = x2.sqerr/(x1.sqerr + x2.sqerr)

                x1.val *= pow(y.val/yold,f1)
                x2.val *= pow(y.val/yold,f2)
                x2.sqerr = min(y.sqerr + x1.sqerr,x2.sqerr)
                x1.sqerr = min(y.sqerr + x2.sqerr,x1.sqerr)


#..............................................................................
# adjustment of minimum and maximum values (XXX Take care: only valid for non-negative data)
                      
    if (x2.valMax > 0):
        x1.valMin = min(y.valMin/x2.valMax,INFINITE)
    elif (y.valMin > 0):
        x1.valMin = INFINITE

    if (x2.valMin > 0):
        x1.valMax = min(y.valMax/x2.valMin,INFINITE)
    elif (y.valMax > 0):
        x1.valMax = INFINITE

    if (x1.valMax > 0):
        x2.valMin = min(y.valMin/x1.valMax,INFINITE)
    elif (y.valMin > 0):
        x2.valMin = INFINITE

    if (x1.valMin > 0):
        x2.valMax = min(y.valMax/x1.valMin,INFINITE)
    elif (y.valMax > 0):
        x2.valMax = INFINITE

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustProdS before constraint......................"
        y.show()
        x1.show()
        x2.show()


    x1.constrain()
    x2.constrain()

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustProdS final result..........................."
        y.show()
        x1.show()
        x2.show()
        print "___________________________________________________"
    
#------------------------------------------------------------------------------
def adjustProdC(y,a,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating and adjusting the multipliying factors of a product amomg two values and a constant
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","ADJUST"]:
        print "___________________________________________________"
        print "adjustProdC starting",x1.name,x2.name
        y.show()
        x1.show()
        x2.show()
    
    if not (y.val == None):
        if not (x1.val == None) and ((x1.sqerr < x2.sqerr) or (x2.val == None)):
            if (x1.val ==0):
                if y.val > 0:
                    x2.val = INFINITE
                    x2.sqerr = INFINITE
            else:
                x2.val = y.val / (a*x1.val)
                x2.sqerr = y.sqerr + x1.sqerr
        elif not (x2.val == None):
            if (x2.val ==0):
                if y.val > 0:
                    x1.val = INFINITE
                    x1.sqerr = INFINITE
            else:
                x1.val = y.val / (a*x2.val)
                x1.sqerr = y.sqerr + x2.sqerr

    if (a*x2.valMax > 0):
        x1.valMin = min(y.valMin/(a*x2.valMax),INFINITE)
    elif (y.valMin > 0):
        x1.valMin = INFINITE

    if (a*x2.valMin > 0):
        x1.valMax = min(y.valMax/(a*x2.valMin),INFINITE)
    elif (y.valMax > 0):
        x1.valMax = INFINITE

    if (a*x1.valMax > 0):
        x2.valMin = min(y.valMin/(a*x1.valMax),INFINITE)
    elif (y.valMin > 0):
        x2.valMin = INFINITE

    if (a*x1.valMin > 0):
        x2.valMax = min(y.valMax/(a*x1.valMin),INFINITE)
    elif (y.valMax > 0):
        x2.valMax = INFINITE

    x1.constrain()
    x2.constrain()

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustProdC________________________________________"
        y.show()
        x1.show()
        x2.show()
        print "___________________________________________________"
    
#------------------------------------------------------------------------------
def adjustSum(y,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","ADJUST"]:
        print "___________________________________________________"
        print "adjustSum starting",x1.name,x2.name
        y.show()
        x1.show()
        x2.show()

    if iszero(y):   #special case SUM = 0, valid if all numbers are positive
        x1.val = 0.0
        x1.sqerr = 0.0
        x2.val = 0.0
        x2.sqerr = 0.0
    elif not (y.val == None):
        y.sqdev = y.sqerr*pow(y.val,2)
        if not (x1.val==None) and ((x1.sqdev < x2.sqdev) or x2.val ==None):
            x1.sqdev = x1.sqerr*pow(x1.val,2)
        
            x2.val = y.val - x1.val
            x2.sqdev = y.sqdev + x1.sqdev

            if (x2.val > 0):
                x2.sqerr = x2.sqdev/pow(x2.val,2)
            else:
                x2.sqerr = INFINITE

        elif not (x2.val == None):
            x2.sqdev = x2.sqerr*pow(x2.val,2)

            x1.val = y.val - x2.val
            x1.sqdev = y.sqdev + x2.sqdev

            if (x1.val > 0):
                x1.sqerr = x1.sqdev/pow(x1.val,2)
            else:
                x1.sqerr = INFINITE

    x1.valMin = max(y.valMin-x2.valMax,0)
    x1.valMax = max(y.valMax-x2.valMin,0)

    x2.valMin = max(y.valMin-x1.valMax,0)
    x2.valMax = max(y.valMax-x1.valMin,0)

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustSum before constraints",x1.name,x2.name
        y.show()
        x1.show()
        x2.show()
        print "___________________________________________________"

    x1.constrain()
    x2.constrain()

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustSum after adjustment",x1.name,x2.name
        y.show()
        x1.show()
        x2.show()
        print "___________________________________________________"
       
#------------------------------------------------------------------------------
def adjustSumS (y,x1,x2): #Adjusting simultaneously both values, not only the worst
#------------------------------------------------------------------------------
#   Default function for calculating and adjusting the components of a sum of 2 values
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","ADJUST"]:
        print "___________________________________________________"
        print "adjustSumS starting",x1.name,x2.name
        y.show()
        x1.show()
        x2.show()
    
    row = [x1,x2]
        
    adjRowSum("adjustSumS",y,row,2)
    
    x1.update(row[0])
    x2.update(row[1])

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustSumS after adjustment",x1.name,x2.name
        y.show()
        x1.show()
        x2.show()
        print "___________________________________________________"

#------------------------------------------------------------------------------
def adjustSum3(y,x1,x2,x3): #Adjusting any value not only the worst
#------------------------------------------------------------------------------
#   Default function for calculating and adjusting the components of a sum of 3 values
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","ADJUST"]:
        print "___________________________________________________"
        print "adjustSum3 starting",x1.name,x2.name,x3.name
        y.show()
        x1.show()
        x2.show()
        x3.show()
    
    row = [x1,x2,x3]
        
    adjRowSum("adjustSum3",y,row,3)
    
    x1.update(row[0])
    x2.update(row[1])
    x3.update(row[2])

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustSum3 after adjustment",x1.name,x2.name,x3.name
        y.show()
        x1.show()
        x2.show()
        x3.show()
        print "___________________________________________________"

#------------------------------------------------------------------------------
def adjRowSum(name,y,row,m):
#------------------------------------------------------------------------------
#   Adjusts rows and estimates Nones
#------------------------------------------------------------------------------

    nNones = 0
    Sum=0.0
    SumMin=0.0
    SumMax=0.0
    SumErr=0.0
    SumSqDev=0.0
    for i in range(m):
        if row[i].val is None:
            nNones += 1
        else:
            Sum += row[i].val
            SumMin += row[i].valMin
            SumMax += row[i].valMax
            SumErr += row[i].sqerr
            SumSqDev += row[i].sqerr*pow(row[i].val,2)
            
    sMin = max(y.valMin - SumMax,0) #positive values considered
    sMax = max(y.valMax - SumMin,0)

    if DEBUG in ["ALL","ADJUST"]:
        print "AdjustRowSum(y,row)________________________________"
        y.show()
        for i in range(m):
            row[i].show()  
        print "___________________________________________________"
        print "adjRowSum: Sum of not Nones =", Sum, "SumErr=", SumErr, "NNones = ",nNones
        print "adjRowSum: sMin=", sMin, "sMax=", sMax

    if iszero(y):   #special case SUM = 0, valid if all numbers are positive
        for i in range(m):
            row[i].val = 0
            row[i].sqerr = 0

        diff = abs(Sum - y.val)

    elif (nNones > 0):

        if (y.val is not None):
            sEst = float (y.val - Sum)/nNones
            if DEBUG in ["ALL","ADJUST"]:
                print "adjustRowSum: (nNones=%s) sEst = "%nNones,sEst
                
            if (sEst > 0):
                newSqerr = (y.sqerr*pow(y.val,2)+pow(sMax,2))/pow(sEst,2)
            else:
                sEst = 0.0
                newSqerr = INFINITE
        else:
            sEst = None
            newSqerr = INFINITE

        
        for i in range(m):
            if row[i].val is None:

                if (sEst is not None):
                    row[i].val = min(sEst,row[i].valMax)
                    row[i].val = max(row[i].val,row[i].valMin)
                
                row[i].valMax=min(row[i].valMax,sMax)

                if nNones>=2:
                    row[i].valMin=max(row[i].valMin,0)
                else:
                    row[i].valMin=max(row[i].valMin,sMin)

                row[i].sqerr = min(newSqerr,row[i].sqerr)
                        
        diff = nNones

    else:
        for i in range(m):
            if SumErr <> 0:
                newval = row[i].val + ((row[i].sqerr/SumErr)*(y.val-Sum))
                newval = max(newval,row[i].valMin)
                newval = min(newval,row[i].valMax)
                
                if DEBUG in ["ALL","ADJUST"]:
                    print "In adjRowSum newval = ",newval," substitutes "
                    row[i].show()  

                newValMin = max(y.valMin - SumMax + row[i].valMax,row[i].valMin)
                newValMax = min(y.valMax - SumMin + row[i].valMin,row[i].valMax)

                maxSqDev = SumSqDev - row[i].sqerr*pow(row[i].val,2) + y.sqerr*pow(y.val,2)

                row[i].val = newval

                if (newval == 0):
                    maxSqerr = INFINITE
                else:
                    maxSqerr1 = pow((newValMax - newValMin)/newval,2)
                    maxSqerr2 = maxSqDev/pow(newval,2)
                    maxSqerr = min(maxSqerr1,maxSqerr2)


                row[i].valMax = newValMax
                row[i].valMin = newValMin

                row[i].sqerr = min(row[i].sqerr,maxSqerr)

                if DEBUG in ["ALL","ADJUST"]:
                    print "... to new value:"
                    row[i].show()  

            elif not isequal(Sum,y.val):

                print "====================================================="
                print "WARNING"
                print "In adjRowSum sumErr=0 and Sum <> 1. Check consistency"
                print "SumErr = ",SumErr," Sum=",Sum," y = ",y.val
                y.show()
                for i in range(m):
                    row[i].show()  
                print "====================================================="
                                
        diff = abs(Sum - y.val)

    if DEBUG in ["ALL","ADJUST"]:
        print "results before constraint:_________________________"
        y.show()
        for i in range(m):
            row[i].show()  
        print "___________________________________________________"
        
    for i in range(m):
        row[i].constrain()

    if DEBUG in ["ALL","ADJUST"]:
        print "results:___________________________________________"
        y.show()
        for i in range(m):
            row[i].show()  
        print "___________________________________________________"
        
    return diff     #returns the value of the adjustment difference for iteration control

#------------------------------------------------------------------------------
def adjustDiff(y,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating and adjusting the components of a difference of two values
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","ADJUST"]:
        print "___________________________________________________"
        print "adjustDiff starting",x1.name,x2.name
        y.show()
        x1.show()
        x2.show()
    
    if iszero(y):   #special case SUM = 0
                    # in this case holds x1 = x2                    
        ccheck1(x1,x2)

    if not (y.val == None):

        y.sqdev = y.sqerr*pow(y.val,2)

        if iszero(y):   #special case SUM = 0
                    # in this case holds x1 = x2                    
            ccheck1(x1,x2)

        elif not (x1.val==None) and ((x1.sqdev < x2.sqdev) or x2.val ==None):
          
            x1.sqdev = x1.sqerr*pow(x1.val,2)
        
            x2.val = x1.val - y.val
            x2.sqdev = y.sqdev + x1.sqdev
            if (x2.val == 0):
                x2.sqerr = INFINITE
            else:
                x2.sqerr = x2.sqdev/pow(x2.val,2)
        elif not (x2.val == None):
            
            x2.sqdev = x2.sqerr*pow(x2.val,2)

            x1.val = y.val + x2.val
            x1.sqdev = y.sqdev + x2.sqdev
            if (x1.val ==0):
                x1.sqerr = INFINITE
            else:
                x1.sqerr = x1.sqdev/pow(x1.val,2)              

        x1.valMin = min(y.valMin+x2.valMin,INFINITE)
        x1.valMax = min(y.valMax+x2.valMax,INFINITE)

        x2.valMin = max(x1.valMin-y.valMax,0)
        x2.valMax = max(x1.valMax-y.valMin,0)

        x1.constrain()
        x2.constrain()

    if DEBUG in ["ALL","ADJUST"]:
        print "results:___________________________________________"
        y.show()
        x1.show()
        x2.show()
        print "___________________________________________________"

#------------------------------------------------------------------------------
def adjustFlow(Qdot,cp,m,T1,T0,DT,DT1):
#------------------------------------------------------------------------------
#   Default function for calculating and adjusting the parameters m,cp,T1,T0
#------------------------------------------------------------------------------
    
    adjustProdC(Qdot,cp,m,DT)

    if DEBUG in ["ALL","CALC"]:
        print "CalcFlow-Qdot______________________________________"
        m.show()
        print "cp = ",cp
        print "Qdot = m*cp*DT = "
        Qdot.show()
        print "___________________________________________________"

    ccheck1(DT,DT1)

    adjustDiff(DT1,T1,T0)
   
    if DEBUG in ["ALL","CALC"]:
        print "adjustFlow-T1 y T0_________________________________"
        T1.show()
        T0.show()
        print "DT = T1 - T0 = "
        DT.show()
        DT1.show()
        print "___________________________________________________"

#------------------------------------------------------------------------------
def ccheck1(y0,y1):
#------------------------------------------------------------------------------
#   Carries out consistency checking of the actual value with one external
#   calculated input.
#------------------------------------------------------------------------------

    y = CCPar("CCheck1")
    
    if (y0.val == None and y1.val == None): #Case 1: Nothing to do
        y.update(y0)
        
    elif y1.val == None: #Case 2: Pnom1 = ok, Pnom2 = None
        y.update(y0)
                
    elif y0.val == None: #case 3: Pnom1 = None, Pnom2 = ok
        y.update(y1)
               
    else: #case 4 Pnom1 = ok, Pnom2 = ok
        y = meanValueOf(y0,y1)
        
        if not isequal(y.val,y1.val):
            pass
 
        if not isequal(y.val,y0.val):
            pass
             
#..............................................................................
# Updating values

    y.constrain()
    
    y0.update(y)
    y1.update(y)

#------------------------------------------------------------------------------
def ccheck2(y0,y1,y2):
#------------------------------------------------------------------------------
#   Carries out consistency checking of the actual value with two externally
#   calculated inputs.
#------------------------------------------------------------------------------
#..............................................................................

    if DEBUG in ["ALL","CHECK"]:
        print "CCheck2_(before...)________________________________"
        y0.show()
        y1.show()
        y2.show()
        print "___________________________________________________"


    ccheckMsg = []

    y = CCPar("CCheck2")

    if y1.val == None: 
        if y2.val == None:
            if y0.val == None:
#..............................................................................
#Case 1: Nothing to do
                
#                print "Case 1: all parameters are unknown. Calculation not possible"
#                ccheckMsg.append("Case 1: all parameters are unknown. Calculation not possible")
                y.val = None
                y.sqerr = INFINITE

            else:               
#..............................................................................
#Case 2: USH3 known, USH1 unknown,USH2 unknown,
                y.update(y0)
#                print "Case 2: USH3 known. USH1 and USH2 adjusted"
             
        else:
            if y0.val == None:
#..............................................................................
#Case 3: USH3 unknown, USH1 unknown,USH2 known

                y.update(y2)
#                print "Case 3: USH2 known. USH1 and USH3 adjusted"
                
            else:
#..............................................................................
#Case 4: USH3 known, USH1 unknown,USH2 known
                if isequal(y2.val, y0.val):
#                    print "Case4: USH1 unknown. USH2 and USH3 redundant and consistent"
                    pass
                else:
#                    print "Case4: USH1 unknown. USH2 and USH3 redundant and not consistent"
                    pass

                y = meanValueOf(y0,y2)
                    
    else:
        if y2.val == None:
            if y0.val == None:
#..............................................................................
#Case 5: USH3 unknown, USH1 known,USH2 unknown,
                y.update(y1)
#                print "Case 5: USH1 known. USH2 and USH3 adjusted"
                
            else:
#..............................................................................
#Case 6: USH3 known, USH1 known,USH2 unknown,
                if isequal(y1.val, y0.val):
#                    print "Case6: USH2 unknown. USH1 and USH3 redundant and consistent"
                    pass
                else:
#                    print "Case6: USH2 unknown. USH1 and USH3 redundant and not consistent"
                    pass

                y = meanValueOf(y0,y1)
                    
        else:
            if y0.val == None:
#..............................................................................
#Case 7: USH3 unknown, USH1 known,USH2 known,

#                if isequal(y1.val, y2.val):
#                    print "Case7: USH3 unknown. USH2 and USH1 redundant and consistent"
#                else:
#                    print "Case7: USH3 unknown. USH2 and USH1 redundant and not consistent"

                y = meanValueOf(y1,y2)
                                        
            else:
    
#..............................................................................
# Case 8:USH3 known, USH1 known,USH2 known,

                    y = meanValueOf3(y0,y1,y2)
                                                        
                    if not isequal(y.val,y1.val):
#                        print " Case8: USH1, USH2, USH3 known and USH1 to be adjusted"
                        pass
             
                    if not isequal(y.val,y2.val):
#                        print "Case8: USH1, USH2, USH3 known and USH2 to be adjusted"
                        pass
                    
                    if not isequal(y.val,y0.val):
#                        print "Case8: USH1, USH2, USH3 known and USH3 to be adjusted"
                        pass
                    
#..............................................................................
# Updating values

    y.constrain()
    
    y0.update(y)
    y1.update(y)
    y2.update(y)

    if DEBUG in ["ALL","CHECK"]:
        print "CCheck2_(... and after adjustment)_________________"
        y0.show()
        y1.show()
        y2.show()
        print "___________________________________________________"


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def ccheck3(y0,y1,y2,y3):
#------------------------------------------------------------------------------
#   Carries out consistency checking of the actual value with three externally
#   calculated inputs.
#------------------------------------------------------------------------------
#..............................................................................

    row = CCRow("ccheck3-row",4)
    y = CCPar("ccheck3-y")
    
    row[0].update(y0)
    row[1].update(y1)
    row[2].update(y2)
    row[3].update(y3)

    y = meanOfRow(row,4)

    y0.update(y)
    y1.update(y)
    y2.update(y)
    y3.update(y)

    
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

    best.valMin = max(y1.valMin,y2.valMin)
    best.valMax = min(y1.valMax,y2.valMax)

    best.constrain()
    
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
def meanValueOf(y1,y2):
#------------------------------------------------------------------------------
#   Selects the best of three values (the one with lowest errors)
#   Does not carry out None-check !!!!
#------------------------------------------------------------------------------

    mean = CCPar("meanValueOf")

    if DEBUG=="ALL":
        print "meanValueOf", y1.val, y1.sqerr, y2.val, y2.sqerr
        print "meanValueOf", y1.valMin, y1.valMax, y2.valMin, y2.valMax

    sumSqErr = pow(y1.sqerr,2) + pow(y2.sqerr,2)
    
    if sumSqErr > 0:
        mean.val = (pow(y1.sqerr,2)*y2.val + pow(y2.sqerr,2)*y1.val)/sumSqErr

    else:
        mean.val=0.5*(y1.val+y2.val)
    
    dif=abs(y1.val-y2.val)
    maxDif = max(y1.val,y2.val)*pow(y1.sqerr+y2.sqerr,0.5)*CONFIDENCE
    
    if dif > maxDif:
        print "======================================================"
        print "WARNING !!!! "
        print "CCheckFunctions (meanValueOf): contradiction found"
        y1.show()
        y2.show()
        print "======================================================"

            
    mean.sqerr = min(y1.sqerr,y2.sqerr)
    mean.valMin = max(y1.valMin,y2.valMin)
    mean.valMax = min(y1.valMax,y2.valMax)
    
    mean.constrain()
    
    return mean   

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def meanValueOf3(y1,y2,y3):
#------------------------------------------------------------------------------
#   Selects the best of three values (the one with lowest errors)
#   Does not carry out None-check !!!!
#------------------------------------------------------------------------------

    mean = CCPar("meanValueOf3")
    if DEBUG=="ALL":
        print "meanValueOf", y1.val, y1.sqerr, y2.val, y2.sqerr, y3.val, y3.sqerr

    if (y1.sqerr == 0):
        mean = y1
        if (y2.sqerr == 0) and not isequal(y1.val,y2.val) and DEBUG=="ALL":
            print "======================================================"
            print "WARNING !!!! "
            print "CCheckFunctions (meanValueOf3): contradiction found",y1.name,y1.val,y2.name,y2.val
            y1.show()
            y2.show()
            print "======================================================"
        if (y3.sqerr == 0) and not isequal(y1.val,y3.val) and DEBUG=="ALL":
            print "======================================================"
            print "WARNING !!!! "
            print "CCheckFunctions (meanValueOf3): contradiction found",y1.name,y1.val,y3.name,y3.val
            y1.show()
            y2.show()
            print "======================================================"
    elif (y2.sqerr ==0 and y1.sqerr <> 0):
        mean = y2
        if (y3.sqerr == 0) and not isequal(y2.val,y3.val) and DEBUG=="ALL":
            print "======================================================"
            print "WARNING !!!! "
            print "CCheckFunctions (meanValueOf3): contradiction found",y2.name,y2.val,y3.name,y3.val
            y1.show()
            y2.show()
            print "======================================================"
    elif (y3.sqerr == 0 and y2.sqerr <> 0 and y1.sqerr <> 0):
        mean = y3
    else:
        p1 = 1/pow(y1.sqerr,2)
        p2 = 1/pow(y2.sqerr,2)
        p3 = 1/pow(y3.sqerr,2)
        mean.val = (y1.val*p1 + y2.val*p2 + y3.val*p3)/(p1+p2+p3)

    mean.sqerr = min(y1.sqerr,y2.sqerr,y3.sqerr)
    mean.valMin = max(y1.valMin,y2.valMin,y3.valMin)
    mean.valMax = min(y1.valMax,y2.valMax,y3.valMax)
            
    mean.constrain()

    return mean   

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def meanOfRow(row,m):
#------------------------------------------------------------------------------
#   Calculates the mean value of a row of CCPar values
#------------------------------------------------------------------------------

    mean = CCPar("meanOfRow")
    if DEBUG in ["ALL","ADJUST"]:
        print "meanOfRow__________________________________________"
        for i in range(m):
            row[i].show()  
        print "___________________________________________________"

    
    sumVal = 0
    sumWeight = 0

    for i in range(m):
        if not (row[i].val == None):
            if row[i].sqerr == 0:
                weight = INFINITE
            else:
                weight = 1./row[i].sqerr
            sumWeight += weight
            sumVal += row[i].val*weight
            
            mean.valMin = max(mean.valMin,row[i].valMin)
            mean.valMax = min(mean.valMax,row[i].valMax)
            mean.sqerr = min(mean.sqerr,row[i].sqerr)

    if sumWeight > 0:
        mean.val = sumVal/sumWeight

    mean.constrain()
    if DEBUG in ["ALL","ADJUST"]:
        mean.show()
        print "___________________________________________________"
            
    return mean              
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
        
#------------------------------------------------------------------------------
def iszero(x):
#------------------------------------------------------------------------------
#   checks if a value is exactly zero
#------------------------------------------------------------------------------

    try:
        if x.val == 0 and x.sqerr == 0:
            return True
        else:
            return False

    except Exception:
        return False
        
#------------------------------------------------------------------------------
def countNones(row):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------
    isnone = []
    noneCounter = 0
    for i in range(len(row)):
        if (row[i].val == None):
            isnone.append(True)
            noneCounter += 1
        else:
            isnone.append(False)
            
    return (noneCounter,isnone)
          


#==============================================================================

#creates a Cycle-instance for being used in cycle checking

cycle = Cycle(10,1.e-3,1.e-5,3)     #basic cycle set-up for cycle class

#==============================================================================

