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
#	Version No.: 0.10
#	Created by: 	    Hans Schweiger	08/03/2008
#	Last revised by:    Claudia Vannoni     9/04/2008
#                           Hans Schweiger      09/04/2008
#                           Claudia Vannoni     16/04/2008
#                           Claudia Vannoni     17/04/2008
#                           Hans Schweiger      18/04/2008
#                           Hans Schweiger      23/04/2008
#                           Hans Schweiger      24/04/2008
#                           Hans Schweiger      25/04/2008
#                           Claudia Vannoni     02/05/2008
#                           Hans Schweiger      07/05/2008
#                           Hans Schweiger      19/06/2008
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
#       25/04/08 HS tracking of conflicts in ccheck-functions 
#       02/05/08 CV calcH,adjustH provisional: TO BE IMPROVED
#       07/05/08 HS entry for process/equipe/pipe no added in conflict list
#                   adjustProd/ProdC -> changed
#       19/06/08 HS constraints added
#                   introduction of "setEstimate" in function CCPar
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
DEFAULT_SQERR = 1.e-10 # default value for sqerr assigned to questionnaire values
NUMERIC_ERR = 1.e-10 # accuracy of numeric calculations
MAX_SQERR = 0.25     # critical square error for screening

CONFIDENCE = 2      #maximum relation between statistical square error and abs.min/max
CHECKMODE = "MEAN"  #MEAN or BEST. MEAN recommened as BEST doesn't give consistent results

DEBUG = "BASIC" #Set to:
                #"ALL": highest level,
                #"CALC": only debug in CALC Functions
                #"ADJUST": only debug in ADJUST Functions
                #"MAIN": plots the show-alls in each block
                #"BASIC": basic debugging (not yet implemented)
                #"OFF" or any other value ...: doesn't print anything

TEST = False
TESTCASE = 3

from einstein.modules.constants import *                
from math import *

#------------------------------------------------------------------------------
class CCPar():
#------------------------------------------------------------------------------
#   Class for grouping value and attributes of a parameter
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def __init__(self,s,parType=None,priority=3):
#------------------------------------------------------------------------------
        self.name = s
        self.priority = priority
        self.val = None
        self.sqerr = INFINITE
        self.sqdev = INFINITE

        self.valMin = 0         #default: non-negative values !!!!

        if parType=="T" or parType=="DT":
            self.valMax = MAXTEMP
        elif parType =="X":
            self.valMax = 1.0
        else:
            self.valMax = INFINITE

        self.track = [self.name]

#------------------------------------------------------------------------------
    def calcDev(self):
#------------------------------------------------------------------------------
#   calculates sqDev from sqErr and value
#------------------------------------------------------------------------------
        if self.val > NUMERIC_ERR:
            self.sqdev = self.sqerr*pow(self.val,2.)
        elif self.sqerr ==0:
            self.sqdev = 0
        else:
            try:
                self.sqdev = (self.valMax - self.valMin,0)^2
            except:
                self.sqdev = INFINITE
        return self.sqdev

#------------------------------------------------------------------------------
    def calcErr(self):
#------------------------------------------------------------------------------
#   calculates sqErr from sqDev and value
#------------------------------------------------------------------------------
        if self.val > NUMERIC_ERR:
            self.sqerr = self.sqdev/pow(self.val,2.)
        elif self.sqdev == 0:
            self.sqerr = 0
        else:
            self.sqerr = INFINITE
        return self.sqerr

#------------------------------------------------------------------------------
    def update(self,new):
#------------------------------------------------------------------------------
        self.val = new.val
        self.sqerr = new.sqerr
        self.sqdev = new.sqdev
        self.valMin = new.valMin
        self.valMax = new.valMax

        newtrack = new.track
        self.track = []
        self.track.extend(newtrack)

#------------------------------------------------------------------------------
    def cleanUp(self):
#------------------------------------------------------------------------------
#   cleans the track from double entries
#------------------------------------------------------------------------------

        cleanTrack = []
        for entry in self.track:            
            if entry not in cleanTrack:
                cleanTrack.append(entry)
        self.track = cleanTrack

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
# special case: exact zero

            elif self.val==0 and self.sqerr==0:
                self.valMin = 0.0
                self.valMax = 0.0

#.............................................................................
# and finally constrain the value itself within the allowed limits

            self.val = min(self.val,self.valMax)
            self.val = max(self.val,self.valMin)


#.............................................................................
# consider that the error can not be larger than [maxVal - minVal]

            if self.val > 0:
                
                try:    #helps to avoid crash for very large errors
                    self.sqerr = min(self.sqerr,pow((self.valMax-self.valMin)/self.val,2))
                except:
                    pass

                self.sqerr = min(self.sqerr,INFINITE)

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

        elif self.valMax < 1.e-10*INFINITE:
            self.val = 0.5 * (self.valMin+self.valMax)
            self.sqdev = pow((self.valMax-self.valMin),2)
                
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
            CCScreen.screenList.append([self.name,"---","---",screen.dataGroup,self.priority])
        elif (self.sqerr > MAX_SQERR):
            err = pow(self.sqerr,0.5)*100
            CCScreen.screenList.append([self.name,'%9.2f'%self.val,'+/-%5.2f'%err,screen.dataGroup,self.priority])

        if DEBUG in ["ALL","BASIC"]:
            print "CCPar (screen): screening parameter"
            self.show()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def setEstimate(self,val,newSqErr=None,limits=None):
#------------------------------------------------------------------------------
#   creates a register entry if the parameter is None or with a high error
#------------------------------------------------------------------------------
        if (self.val == None) or (self.sqerr > MAX_SQERR):
            self.val = val
            if limits is not None:
                (newMin,newMax) = limits
                self.valMin = max(newMin,self.valMin)
                self.valMax = min(newMax,self.valMax)
            if newSqErr is not None: self.sqerr = min(self.sqerr,newSqErr)
            self.constrain()
            
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

    def setDataGroup(self,name,no):
        self.dataGroup = str(no)

    def reset(self):
        CCScreen.screenList = []
        CCScreen.nScreened = 0

    def show(self):
        print "CCScreen: %s parameters screened"%len(CCScreen.screenList)
        for i in range(len(CCScreen.screenList)):
            print i+1, CCScreen.screenList[i]

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
class CCConflict():
#------------------------------------------------------------------------------
#   module for screening of conflicts between data
#------------------------------------------------------------------------------

    conflictList = []
    nConflictChecked = 0
    nConflicts = 0
    
    def __init__(self):
        self.reset()

    def reset(self):
        CCConflict.conflictList = []
        CCConflict.nConflictChecked = 0
        CCConflict.nConflicts = 0

    def setDataGroup(self,name,no):
        self.dataGroup = name + "["+str(no)+"]"

    def show(self):
        print "CCConflict: %s parameters screened for possible conflicts"%len(CCConflict.conflictList)
        for i in range(len(CCConflict.conflictList)):
            print i+1, CCConflict.conflictList[i]

    def screen(self,y1,y2,dif,maxDif):

        y1err = pow(y1.sqerr,0.5)
        y2err = pow(y2.sqerr,0.5)
        
        row = [dif,maxDif,y1.name,y1.track,y1.val,y1err,y2.name,y2.track,y2.val,y2err,self.dataGroup]
        CCConflict.conflictList.append(row)
        CCConflict.nConflicts += 1

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

    if y.val is not None:
        y.track = []
        y.track.extend(x1.track)
        y.cleanUp()

    if DEBUG in ["ALL","CALC"]:
        print "CalcK(%s*x1)_______________________"%a
        x1.show()
        print "a*x1 = "
        y.show()
        print "___________________________________________________"

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

    if y.val is not None:
        y.track = []
        y.track.extend(x1.track)
        y.track.extend(x2.track)
        y.cleanUp()

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

    if y.val is not None:
        y.track = []
        y.track.extend(x1.track)
        y.track.extend(x2.track)
        y.cleanUp()

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

    if y.val is not None:
        y.track = []
        y.track.extend(x1.track)
        y.track.extend(x2.track)
        y.cleanUp()

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

    if y.val is not None:
        y.track = []
        y.track.extend(x1.track)
        y.track.extend(x2.track)
        y.track.extend(x3.track)
        y.cleanUp()

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

    if y.val is not None:
        y.track = []
        for i in range(len(row)):
            y.track.extend(row[i].track)

        y.cleanUp()

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
    
    if y.val is not None:
        y.track = []
        y.track.extend(x1.track)
        y.track.extend(x2.track)

        y.cleanUp()

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
def calcH(yname,a,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the entalpy h
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

    if y.val is not None:
        y.track = []
        y.track.extend(x1.track)
        y.cleanUp()

    if DEBUG in ["ALL","CALC"]:
        print "CalcH(x1,x2)____________________________________"
        x1.show()
        x2.show()
        print "h(%s,x1,x2) = "%a
        y.show()
        print "___________________________________________________"

    return y


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

    if y.val is not None:
        x1.track = []
        x1.track.extend(y.track)

        x1.cleanUp()
        
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

    if (y.val is not None):
        if (x1.val is not None) and ((x1.sqerr < x2.sqerr) or (x2.val is None)):
            if (x1.val ==0):
                if y.val > 0:
                    x2.val = INFINITE
                    x2.sqerr = INFINITE
            else:
                x2.val = y.val / x1.val
                x2.sqerr = y.sqerr + x1.sqerr
                x2.calcDev()
#                x2.sqerr = min(y.sqerr + x1.sqerr,x2.sqerr)
        elif (x2.val is not None):
            if (x2.val ==0):
                if y.val > 0:
                    x1.val = INFINITE
                    x1.sqerr = INFINITE
            else:
                x1.val = y.val / x2.val
#HS2008-05-07 minimum eliminated. gave problems                x1.sqerr = min(y.sqerr + x2.sqerr,x1.sqerr)
                x1.sqerr = y.sqerr + x2.sqerr
                x1.calcDev()

    if (x2.valMax > 0):
        newMin = min(y.valMin/x2.valMax,INFINITE)
    elif (y.valMin > 0):
        newMin = INFINITE
    else:
        newMin = x1.valMin

    if (x2.valMin > 0):
        newMax = min(y.valMax/x2.valMin,INFINITE)
    elif (y.valMax > 0):
        newMax = INFINITE
    else:
        newMax = x1.valMax

    if (x1.valMax > 0):
        x2.valMin = min(y.valMin/x1.valMax,INFINITE)
    elif (y.valMin > 0):
        x2.valMin = INFINITE

    if (x1.valMin > 0):
        x2.valMax = min(y.valMax/x1.valMin,INFINITE)
    elif (y.valMax > 0):
        x2.valMax = INFINITE

    x1.valMin = newMin
    x1.valMax = newMax

    x1.constrain()
    x2.constrain()

    if y.val is not None:

        newtrackx1 = []
        newtrackx1.extend(y.track)
        if x2.val is not None:
            newtrackx1.extend(x2.track)

        newtrackx2 = []
        newtrackx2.extend(y.track)
        if x1.val is not None:
            newtrackx2.extend(x1.track)

        x1.track = newtrackx1
        x2.track = newtrackx2

        x1.cleanUp()
        x2.cleanUp()

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
    
    if y.val is not None:
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
        newMin = min(y.valMin/x2.valMax,INFINITE)
    elif (y.valMin > 0):
        newMin = INFINITE
    else:
        newMin = x1.valMin

    if (x2.valMin > 0):
        newMax = min(y.valMax/x2.valMin,INFINITE)
    elif (y.valMax > 0):
        newMax = INFINITE
    else:
        newMax = x2.valMin

    if (x1.valMax > 0):
        x2.valMin = min(y.valMin/x1.valMax,INFINITE)
    elif (y.valMin > 0):
        x2.valMin = INFINITE

    if (x1.valMin > 0):
        x2.valMax = min(y.valMax/x1.valMin,INFINITE)
    elif (y.valMax > 0):
        x2.valMax = INFINITE

    x1.valMin = newMin
    x1.valMax = newMax

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustProdS before constraint......................"
        y.show()
        x1.show()
        x2.show()


    x1.constrain()
    x2.constrain()

    if y.val is not None:
        newtrackx1 = []
        newtrackx1.extend(y.track)
        if x2.val is not None:
            newtrackx1.extend(x2.track)

        newtrackx2 = []
        newtrackx2.extend(y.track)
        if x1.val is not None:
            newtrackx2.extend(x1.track)

        x1.track = newtrackx1
        x2.track = newtrackx2

        x1.cleanUp()
        x2.cleanUp()

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
    
    if y.val is not None:
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
        newMin = min(y.valMin/(a*x2.valMax),INFINITE)
    elif (y.valMin > 0):
        newMin = INFINITE
    else:
        newMin = x1.valMin

    if (a*x2.valMin > 0):
        newMax = min(y.valMax/(a*x2.valMin),INFINITE)
    elif (y.valMax > 0):
        newMax = INFINITE
    else:
        newMax = x1.valMax

    if (a*x1.valMax > 0):
        x2.valMin = min(y.valMin/(a*x1.valMax),INFINITE)
    elif (y.valMin > 0):
        x2.valMin = INFINITE

    if (a*x1.valMin > 0):
        x2.valMax = min(y.valMax/(a*x1.valMin),INFINITE)
    elif (y.valMax > 0):
        x2.valMax = INFINITE

    x1.valMin = newMin
    x1.valMax = newMax

    x1.constrain()
    x2.constrain()

    if y.val is not None:
        newtrackx1 = []
        newtrackx1.extend(y.track)
        if x2.val is not None:
            newtrackx1.extend(x2.track)

        newtrackx2 = []
        newtrackx2.extend(y.track)
        if x1.val is not None:
            newtrackx2.extend(x1.track)

        x1.track = newtrackx1
        x2.track = newtrackx2

        x1.cleanUp()
        x2.cleanUp()

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
    
    newMin = max(y.valMin-x2.valMax,0)
    newMax = max(y.valMax-x2.valMin,0)

    x2.valMin = max(y.valMin-x1.valMax,0)
    x2.valMax = max(y.valMax-x1.valMin,0)

    x1.valMin = newMin
    x1.valMax = newMax

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustSum before constraints",x1.name,x2.name
        y.show()
        x1.show()
        x2.show()
        print "___________________________________________________"

    x1.constrain()
    x2.constrain()

    if y.val is not None:
        newtrackx1 = []
        newtrackx1.extend(y.track)
        if x2.val is not None:
            newtrackx1.extend(x2.track)

        newtrackx2 = []
        newtrackx2.extend(y.track)
        if x1.val is not None:
            newtrackx2.extend(x1.track)

        x1.track = newtrackx1
        x2.track = newtrackx2

        x1.cleanUp()
        x2.cleanUp()

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

    if y.val is not None:
        newtrackx1 = []
        newtrackx1.extend(y.track)
        if x2.val is not None:
            newtrackx1.extend(x2.track)

        newtrackx2 = []
        newtrackx2.extend(y.track)
        if x1.val is not None:
            newtrackx2.extend(x1.track)

        x1.track = newtrackx1
        x2.track = newtrackx2

        x1.cleanUp()
        x2.cleanUp()

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

    y.calcDev()
    
    for i in range(m):
        if row[i].val is None:
            nNones += 1
        else:
            Sum += row[i].val
            SumMin += row[i].valMin
            SumMax += row[i].valMax
            SumErr += row[i].sqerr
            SumSqDev += row[i].calcDev()
            
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
            row[i].sqdev = 0

        diff = abs(Sum - y.val)

    elif (nNones > 0):

        newSqDev = y.sqdev + pow(sMax,2)
        if (y.val is not None):
            sEst = float (y.val - Sum)/nNones
            if DEBUG in ["ALL","ADJUST"]:
                print "adjustRowSum: (nNones=%s) sEst = "%nNones,sEst
                
            if (sEst > 0):
                newSqerr = newSqDev/pow(sEst,2)
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

                row[i].sqdev = newSqDev
                row[i].calcErr()
                        
        diff = nNones

    else:
        
        for i in range(m):
            if SumErr <> 0:
                
                newValMin = max(y.valMin - SumMax + row[i].valMax,row[i].valMin)
                newValMax = min(y.valMax - SumMin + row[i].valMin,row[i].valMax)

                if y.val is not None:
                    maxSqDev = SumSqDev - row[i].calcDev() + y.sqdev

                    newval = row[i].val + ((row[i].sqdev/SumSqDev)*(y.val-Sum))
                    newval = max(newval,row[i].valMin)
                    newval = min(newval,row[i].valMax)
                    if DEBUG in ["ALL","ADJUST"]:
                        print "In adjRowSum newval = ",newval," substitutes "
                        row[i].show()  

                    row[i].val = newval

                    if DEBUG in ["ALL","ADJUST"]:
                        print "... to new value:"
                        row[i].show()  

                    row[i].sqdev = min(row[i].sqdev,maxSqDev)
                    row[i].calcErr()


                row[i].valMax = newValMax
                row[i].valMin = newValMin

            elif not isequal(Sum,y.val):

                print "====================================================="
                print "WARNING"
                print "In adjRowSum sumErr=0 and Sum <> 1. Check consistency"
                print "SumErr = ",SumErr," Sum=",Sum," y = ",y.val
                y.show()
                for i in range(m):
                    row[i].show()  
                print "====================================================="
                                
        if y.val is not None:
            diff = abs(Sum - y.val)
        else:
            diff = 1.0

    for i in range(m):        
        row[i].constrain()

    if y.val is not None:
        newtrack = []
        for i in range(m):
            newtrack.append([])
            newtrack[i].extend(y.track)
            for j in range(m):
                if not (i==j) and row[i].val is not None:
                    newtrack[i].extend(row[i].track)
        for i in range(m):
            row[i].track = []
            row[i].track.extend(newtrack[i])
            row[i].cleanUp()

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

    if y.val is not None:

        y.calcDev()

        if iszero(y):   #special case SUM = 0
                    # in this case holds x1 = x2                    
            ccheck1(x1,x2)

        elif (x1.val is not None) and ((x1.sqdev < x2.sqdev) or x2.val ==None):
          
            x2.val = x1.val - y.val
            x2.sqdev = y.sqdev + x1.calcDev()
            x2.calcErr()
                
        elif x2.val is not None:
            
            x1.val = y.val + x2.val
            x1.sqdev = y.sqdev + x2.calcDev()
            x1.calcErr()

    newMin = min(y.valMin+x2.valMin,INFINITE)
    newMax = min(y.valMax+x2.valMax,INFINITE)

    x2.valMin = max(x1.valMin-y.valMax,0)
    x2.valMax = max(x1.valMax-y.valMin,0)

    x1.valMin = newMin
    x1.valMax = newMax

    x1.constrain()
    x2.constrain()

    if y.val is not None:
        newtrackx1 = []
        newtrackx1.extend(y.track)
        if x2.val is not None:
            newtrackx1.extend(x2.track)

        newtrackx2 = []
        newtrackx2.extend(y.track)
        if x1.val is not None:
            newtrackx2.extend(x1.track)

        x1.track = newtrackx1
        x2.track = newtrackx2

        x1.cleanUp()
        x2.cleanUp()

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
def adjustH(y,a,x1,x2):
#------------------------------------------------------------------------------
#   Default function for adjusting the entalpy h
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","ADJUST"]:
        print "___________________________________________________"
        print "adjustProd starting",x1.name,x2.name
        y.show()
        print "a= ",a
        x1.show()
        x2.show()

    if not (y.val == None):
        
        x1.val = y.val /a
        x1.sqerr = y.sqerr

    x1.valMin = min(y.valMin/a,INFINITE)
    x1.valMax = min(y.valMax/a,INFINITE)

    x1.constrain()

    if y.val is not None:
        x1.track = []
        x1.track.extend(y.track)

        x1.cleanUp()

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustH________________________________________"
        y.show()
        x1.show()
        x2.show()
        print "___________________________________________________"


#------------------------------------------------------------------------------
def ccheck1(y0,y1):
#------------------------------------------------------------------------------
#   Carries out consistency checking of the actual value with one external
#   calculated input.
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","CHECK"]:
        print "CCheck1_(before...)________________________________"
        y0.show()
        y1.show()
        print "___________________________________________________"

    y = CCPar("CCheck1")
    
    if (y0.val == None and y1.val == None): #Case 1: Nothing to do
        y.update(y0)
        y.valMin = max(y0.valMin,y1.valMin)
        y.valMax = min(y0.valMax,y1.valMax)
        
    elif y1.val == None: #Case 2: Pnom1 = ok, Pnom2 = None
        y.update(y0)
        y.valMin = max(y0.valMin,y1.valMin)
        y.valMax = min(y0.valMax,y1.valMax)
                
    elif y0.val == None: #case 3: Pnom1 = None, Pnom2 = ok
        y.update(y1)
        y.valMin = max(y0.valMin,y1.valMin)
        y.valMax = min(y0.valMax,y1.valMax)
               
    else: #case 4 Pnom1 = ok, Pnom2 = ok
        if CHECKMODE == "BEST":
            y = bestOf(y0,y1)
        else:
            y = meanValueOf(y0,y1)
                     
#..............................................................................
# Updating values
   
    y.constrain()
    
    y0.update(y)
    y1.update(y)

    if DEBUG in ["ALL","CHECK"]:
        print "CCheck1_(... and after adjustment)_________________"
        y0.show()
        y1.show()
        print "___________________________________________________"


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
                y.valMin = max(y0.valMin,y1.valMin,y2.valMin)
                y.valMax = min(y0.valMax,y1.valMax,y2.valMax)

            else:               
#..............................................................................
#Case 2: USH3 known, USH1 unknown,USH2 unknown,
                y.update(y0)
                y.valMin = max(y0.valMin,y1.valMin,y2.valMin)
                y.valMax = min(y0.valMax,y1.valMax,y2.valMax)
#                print "Case 2: USH3 known. USH1 and USH2 adjusted"
             
        else:
            if y0.val == None:
#..............................................................................
#Case 3: USH3 unknown, USH1 unknown,USH2 known

                y.update(y2)
                y.valMin = max(y0.valMin,y1.valMin,y2.valMin)
                y.valMax = min(y0.valMax,y1.valMax,y2.valMax)
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

                if CHECKMODE == "BEST":
                    y = bestOf(y0,y2)
                else:
                    y = meanValueOf(y0,y2)
                y.valMin = max(y.valMin,y1.valMin)
                y.valMax = min(y.valMax,y1.valMax)
                    
    else:
        if y2.val == None:
            if y0.val == None:
#..............................................................................
#Case 5: USH3 unknown, USH1 known,USH2 unknown,
                y.update(y1)
                y.valMin = max(y0.valMin,y1.valMin,y2.valMin)
                y.valMax = min(y0.valMax,y1.valMax,y2.valMax)
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

                if CHECKMODE == "BEST":
                    y = bestOf(y0,y1)
                else:
                    y = meanValueOf(y0,y1)
                y.valMin = max(y.valMin,y2.valMin)
                y.valMax = min(y.valMax,y2.valMax)
                    
        else:
            if y0.val == None:
#..............................................................................
#Case 7: USH3 unknown, USH1 known,USH2 known,

#                if isequal(y1.val, y2.val):
#                    print "Case7: USH3 unknown. USH2 and USH1 redundant and consistent"
#                else:
#                    print "Case7: USH3 unknown. USH2 and USH1 redundant and not consistent"

                if CHECKMODE == "BEST":
                    y = bestOf(y1,y2)
                else:
                    y = meanValueOf(y1,y2)
                y.valMin = max(y.valMin,y0.valMin)
                y.valMax = min(y.valMax,y0.valMax)
                                        
            else:
    
#..............................................................................
# Case 8:USH3 known, USH1 known,USH2 known,

                    if CHECKMODE == "BEST":
                        y = bestOf3(y0,y1,y2)
                    else:
                        y = meanValueOf3(y0,y1,y2)
                                                                            
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
    
    row[0] = y0
    row[1] = y1
    row[2] = y2
    row[3] = y3
                
    if CHECKMODE == "BEST":
        y = bestOfRow(row,4)
    else:
        y = meanOfRow(row,4)

    y0.update(y)
    y1.update(y)
    y2.update(y)
    y3.update(y)

    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def checkIfConflict(y1,y2):
#------------------------------------------------------------------------------
#   Checks if there is a conflict between values and error ranges of y1 and y2
#------------------------------------------------------------------------------
#..............................................................................

    dif=abs(y1.val-y2.val)
    maxDif = max(y1.val,y2.val)*pow(y1.sqerr+y2.sqerr,0.5)*CONFIDENCE
    
    if dif > maxDif + NUMERIC_ERR:
        print "======================================================"
        print "WARNING !!!! "
        print "CCheckFunctions (checkIfConflict): contradiction found"
        y1.show()
        y2.show()
        print "dif = ",dif," maxDif = ",maxDif
        print "======================================================"
        conflict.screen(y1,y2,dif,maxDif)
        

    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def trackBestOf(y1,y2):
#------------------------------------------------------------------------------
#   takes the track of the best
#------------------------------------------------------------------------------

    if (y1.sqerr < y2.sqerr):
            return y1.track
    else:
            return y2.track

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def trackBestOf3(y1,y2,y3):
#------------------------------------------------------------------------------
#   takes the track of the best
#------------------------------------------------------------------------------

    if (y1.sqerr < y2.sqerr and y1.sqerr < y3.sqerr):
            return y1.track
    elif (y2.sqerr < y3.sqerr):
            return y2.track
    else:
            return y3.track

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def trackBestOfRow(row,m):
#------------------------------------------------------------------------------
#   takes the track of the best
#------------------------------------------------------------------------------

    best = INFINITE
    track = []
    for i in range(m):
        if row[i].sqerr <= best:
            best = row[i].sqerr
            track = row[i].track
    return track            

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

    checkIfConflict(y1,y2)
    
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
def bestOfRow(row,m):
#------------------------------------------------------------------------------
#   Selects the best of three values (the one with lowest errors)
#   Does not carry out None-check !!!!
#------------------------------------------------------------------------------

    best = CCPar("bestOfRow")
    best.val = INFINITE
    for i in range(m):
        if row[i].val is not None:
            best = bestOf(best,row[i])
    
    return best   

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def meanValueOf(y1,y2):
#------------------------------------------------------------------------------
#   Selects the best of three values (the one with lowest errors)
#   Does not carry out None-check !!!!
#------------------------------------------------------------------------------

    mean = CCPar("meanValueOf")
    mean.track = trackBestOf(y1,y2)

#    sumSqErr = pow(y1.sqerr,2) + pow(y2.sqerr,2)
    sumSqDev = y1.calcDev() + y2.calcDev()
    
#    if sumSqErr > 0:
#        mean.val = (pow(y1.sqerr,2)*y2.val + pow(y2.sqerr,2)*y1.val)/sumSqErr

    if sumSqDev > 0:
        mean.val = (y1.sqdev*y2.val + y2.sqdev*y1.val)/sumSqDev
        
    else:
        mean.val=0.5*(y1.val+y2.val)

    
    dif=abs(y1.val-y2.val)
    maxDif = pow(sumSqDev,0.5)*CONFIDENCE
    
    if dif > maxDif + NUMERIC_ERR:
        print "======================================================"
        print "WARNING !!!! "
        print "CCheckFunctions (meanValueOf): contradiction found"
        y1.show()
        y2.show()
        print "======================================================"


    mean.sqdev = min(y1.sqdev,y2.sqdev)
    
    mean.valMin = max(y1.valMin,y2.valMin)
    mean.valMax = min(y1.valMax,y2.valMax)
    mean.calcErr()

    mean.constrain()
    
    checkIfConflict(y1,y2)
    
    return mean   

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def meanValueOf3(y1,y2,y3):
#------------------------------------------------------------------------------
#   Selects the best of three values (the one with lowest errors)
#   Does not carry out None-check !!!!
#------------------------------------------------------------------------------

    mean = CCPar("meanValueOf3")
    mean.track = trackBestOf3(y1,y2,y3)

    sumSqDev = y1.calcDev() + y2.calcDev() + y3.calcDev()
    
    if (y1.sqdev == 0):
        mean = y1
        if (y2.sqdev == 0) and not isequal(y1.val,y2.val):
            mean = meanValueOf(mean,y1)

            if DEBUG=="ALL":
                print "======================================================"
                print "WARNING !!!! "
                print "CCheckFunctions (meanValueOf3): contradiction found",y1.name,y1.val,y2.name,y2.val
                y1.show()
                y2.show()
                print "======================================================"

        if (y3.sqdev == 0) and not isequal(y1.val,y3.val):
            mean = meanValueOf(mean,y3)

            if DEBUG=="ALL":
                print "======================================================"
                print "WARNING !!!! "
                print "CCheckFunctions (meanValueOf3): contradiction found",y1.name,y1.val,y3.name,y3.val
                y1.show()
                y2.show()
                print "======================================================"

    elif (y2.sqdev ==0 and y1.sqdev <> 0):
        mean = y2
        if (y3.sqerr == 0) and not isequal(y2.val,y3.val):
            mean = meanValueOf(mean,y3)

            if DEBUG=="ALL":           
                print "======================================================"
                print "WARNING !!!! "
                print "CCheckFunctions (meanValueOf3): contradiction found",y2.name,y2.val,y3.name,y3.val
                y1.show()
                y2.show()
                print "======================================================"

    elif (y3.sqdev == 0 and y2.sqdev <> 0 and y1.sqdev <> 0):
        mean = y3
    else:
        p1 = 1/y1.sqdev
        p2 = 1/y2.sqdev
        p3 = 1/y3.sqdev
        mean.val = (y1.val*p1 + y2.val*p2 + y3.val*p3)/(p1+p2+p3)

    mean.sqdev = min(y1.sqdev,y2.sqdev,y3.sqdev)
    mean.valMin = max(y1.valMin,y2.valMin,y3.valMin)
    mean.valMax = min(y1.valMax,y2.valMax,y3.valMax)
    mean.calcErr()
            
    mean.constrain()

    checkIfConflict(y1,y2)
    checkIfConflict(y1,y3)
    checkIfConflict(y2,y3)

    return mean   

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def meanOfRow(row,m):
#------------------------------------------------------------------------------
#   Calculates the mean value of a row of CCPar values
#------------------------------------------------------------------------------

    mean = CCPar("meanOfRow")
    mean.track = trackBestOfRow(row,m)

    if DEBUG in ["ALL","ADJUST"]:
        print "meanOfRow__________________________________________"
        for i in range(m):
            row[i].show()  
        print "___________________________________________________"

    
    sumVal = 0
    sumWeight = 0

    for i in range(m):
        if not (row[i].val == None):
            if row[i].calcDev() == 0:
                weight = INFINITE
            else:
                weight = 1./row[i].sqdev
                
            sumWeight += weight
            sumVal += row[i].val*weight

        mean.sqdev = min(mean.sqdev,row[i].sqdev)

        mean.valMin = max(mean.valMin,row[i].valMin)
        mean.valMax = min(mean.valMax,row[i].valMax)
    
    if sumWeight > 0:
        mean.val = sumVal/sumWeight
        mean.calcErr()

    mean.constrain()

    for i in range(m):
        if row[i].val is not None:
            for j in range(i+1,m):
                if row[j].val is not None:
                    checkIfConflict(row[i],row[j])
    
    if DEBUG in ["ALL","ADJUST"]:
        mean.show()
        print "___________________________________________________"
            
    return mean              
#------------------------------------------------------------------------------
def calcConstraintLT(y,xlim):
#------------------------------------------------------------------------------
#   Changes y so that y <= xlim
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","CALC"]:
        print "constrainLT(x1,x2)_________________________________"
        y.show()

    y.valMin = min(y.valMin,ylim.valMax)
    y.valMax = min(y.valMax,ylim.valMax)
    y.val = min(y.val,xlim.val)
    y.constrain()

    if DEBUG in ["ALL","CALC"]:
        xlim.show()
        print "y (constrained) = "
        y.show()
        print "___________________________________________________"

    return y

#------------------------------------------------------------------------------
def adjConstraintLT(y,xlim):
#------------------------------------------------------------------------------
#   Changes y so that y <= xlim
#------------------------------------------------------------------------------

    calcConstraintGT(xlim,y)

#------------------------------------------------------------------------------
def calcConstraintGT(y,xlim):
#------------------------------------------------------------------------------
#   Changes y so that y >= xlim
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","CALC"]:
        print "constrainLT(x1,x2)_________________________________"
        y.show()

    y.valMin = max(y.valMin,ylim.valMin)
    y.valMax = max(y.valMax,ylim.valMin)
    y.val = max(y.val,xlim.val)
    y.constrain()

    if DEBUG in ["ALL","CALC"]:
        xlim.show()
        print "y (constrained) = "
        y.show()
        print "___________________________________________________"

    return y

#------------------------------------------------------------------------------
def adjConstraintGT(y,xlim):
#------------------------------------------------------------------------------
#   Changes y so that y <= xlim
#------------------------------------------------------------------------------

    calcConstraintLT(xlim,y)

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
conflict = CCConflict()     #instance for access to CCConflict functions
screen = CCScreen()
