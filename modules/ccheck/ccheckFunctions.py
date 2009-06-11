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
#   EINSTEIN Version No.: 1.0
#   Created by: 	Claudia Vannoni, Hans Schweiger
#                       08/03/2008 - 24/09/2008
#
#   Update No. 001
#
#   Since Version 1.0 revised by:
#
#                       Hans Schweiger  06/04/2008
#               
#   06/04/2008  HS  Clean-up: elimination of prints
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

from einstein.modules.messageLogger import *
from einstein.GUI.GUITools import *     #needed for function check

EPSILON = 1.e-10     # required accuracy for function "isequal"
INFINITE = 1.e99    # numerical value assigned to "infinite"
MINIMUM_VALUE = 1.e-10
DEFAULT_SQERR = 1.e-4 # default value for sqerr assigned to questionnaire values
NUMERIC_ERR = 1.e-10 # accuracy of numeric calculations
MAX_SQERR = 0.1     # critical square error for screening

CONFIDENCE = 4.0    #maximum relation between statistical error and abs.min/max
                    #!!!!!!!!!! at present deactivated (set to 999.) because gave adjustment problems

CHECKMODE = "BEST"  #MEAN or BEST. MEAN recommened as BEST doesn't give consistent results

def setCheckMode(mode):
    global CHECKMODE
    CHECKMODE = mode
    
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
        self.parType = parType
        self.val = None
        self.sqerr = INFINITE
        self.sqdev = INFINITE
        self.dev = pow(INFINITE,0.5)

        self.valMin = 0         #default: non-negative values !!!!

        if parType=="T" or parType=="DT":
            self.valMax = MAXTEMP
        elif parType =="X":
            self.valMax = 1.0
        elif parType =="S":
            self.valMin = -INFINITE
            self.valMax = INFINITE
        else:
            self.valMax = INFINITE

        self.track = [self.name]

#------------------------------------------------------------------------------
    def calcDev(self):
#------------------------------------------------------------------------------
#   calculates sqDev from sqErr and value
#------------------------------------------------------------------------------
        if (self.val > NUMERIC_ERR or self.val < - NUMERIC_ERR) and self.val is not None:
            if self.sqerr == INFINITE:
                self.sqdev = INFINITE
            else:
                self.sqdev = self.sqerr*pow(self.val,2.)
        elif self.sqerr ==0:
            self.sqdev = 0
        else:
            try:
                self.sqdev = pow((self.valMax - self.valMin,0),2.)
            except:
                self.sqdev = INFINITE
                
        self.dev = pow(self.sqdev,0.5)
        return self.sqdev

#------------------------------------------------------------------------------
    def calcErr(self):
#------------------------------------------------------------------------------
#   calculates sqErr from sqDev and value
#------------------------------------------------------------------------------
        if (self.val > NUMERIC_ERR or self.val < - NUMERIC_ERR) and self.val is not None:
            if self.sqdev >= 1.e-20*INFINITE:
                self.sqerr = INFINITE
            else:
                self.sqerr = self.sqdev/pow(self.val,2.)
        elif self.sqdev == 0:
            self.sqerr = 0
        else:
            self.sqerr = INFINITE
        return self.sqerr

#------------------------------------------------------------------------------
    def invSqErr(self):
#------------------------------------------------------------------------------
#   calculates the square error of 1/x
#   sqerr(1/x) = sqerr(x) for sqerr << 1
#------------------------------------------------------------------------------
        if self.sqerr >= pow(CONFIDENCE,-2.0): # value 0.0 can not be excluded
            return INFINITE
        else:
            err = pow(self.sqerr,0.5)
            return pow(err/(1-err),2.0)

#------------------------------------------------------------------------------
    def update(self,new):
#------------------------------------------------------------------------------
        self.val = new.val
            
        self.sqerr = new.sqerr
        self.sqdev = new.sqdev
        self.dev = new.dev
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
                if len(cleanTrack) < 10:
                    cleanTrack.append(entry)
                elif (len(cleanTrack)==10):
                    cleanTrack.append("etc.")
                    break                
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

# special case EXACT ZERO
        elif val == 0:
            self.sqerr = 0

# special case for fractions (values between 0 and 1): -> set to EXACT 1
# is required in checkPipe for setting feed-up flow to EXACTLY 0

        elif self.parType == "X" and self.val > 1.0 - NUMERIC_ERR:
            self.val = 1.0
            self.sqerr = 0
        elif self.parType == "T" and err==DEFAULT_SQERR:
            self.sqdev = 0.1
            self.calcErr()
        else:
            self.sqerr = err

        self.constrain()

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

        if self.parType <> "S": self.valMin = max(self.valMin,0)
        self.valMax = min(self.valMax,INFINITE)
            
        if self.val is not None:

            if (self.val > MINIMUM_VALUE):

#.............................................................................
# first set absolute constraint of the value to reasonable limits around its
# actual value - in function of the specified error margins

                if self.sqerr < INFINITE and self.parType <> "S":
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
# special parameters that allow negative values

            elif self.val < - MINIMUM_VALUE and self.parType == "S":
                pass

#.............................................................................
# special case: unallowed negative values

            else:
                self.val = 0.0
                self.sqerr = INFINITE

#.............................................................................
# and finally constrain the value itself within the allowed limits

            self.sqdev = self.calcDev() #maintain sqDev as determinant error margin
            self.val = min(self.val,self.valMax)
            self.val = max(self.val,self.valMin)
            self.calcErr()

#.............................................................................
# consider that the error can not be larger than [maxVal - minVal]

            if self.val <> 0:
                
                try:    #helps to avoid crash for very large errors
                    newErr = max(pow((self.valMax-self.val)/self.val,2.0),\
                                 pow((self.val-self.valMin)/self.val,2.0))
                    self.sqerr = min(self.sqerr,newErr)  #XXX Security feature !!!
                except:
                    pass

                self.sqerr = min(self.sqerr,INFINITE)
                
            elif self.val == 0 and self.valMax == 0:    #set to exact zero
                self.sqerr = 0

#.............................................................................
# check for all values larger than 0 !!!
# if constrain in between min/max works, and min> 0, the following should be unnecessary

            if self.val < 0 and self.parType <> "S":
                print "======================================================"
                print "======================================================"
                print "%s.CONSTRAIN: SEVERE ERROR - VALUE < 0 !!!! "%self.name
                self.show()
                print "======================================================"
                print "======================================================"

        elif self.valMax < 1.e-10*INFINITE:
            self.val = 0.5 * (self.valMin+self.valMax)
            self.dev = pow((self.valMax-self.valMin),2.0)
                
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

        if (self.val == None) or (self.sqerr > MAX_SQERR):
            CCScreen.screenList.append([self.name,self.val,self.sqerr,screen.dataGroup,self.priority])    
#        if (self.val == None):
#            CCScreen.screenList.append([self.name,"---","---",screen.dataGroup,self.priority])
#        elif (self.sqerr > MAX_SQERR):
#            if self.sqerr < 1.0:
#                err = pow(self.sqerr,0.5)
#                CCScreen.screenList.append([self.name,'%9.2f'%self.val,'%5.2f'%err,screen.dataGroup,self.priority])
#            CCScreen.screenList.append([self.name,self.val,err,screen.dataGroup,self.priority])
#            else:
#                CCScreen.screenList.append([self.name,'%9.2f'%self.val,'>100.00',screen.dataGroup,self.priority])
                
        if DEBUG in ["ALL","BASIC"]:
            print "CCPar (screen): screening parameter"
            self.show()
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    def setEstimate(self,val,newSqErr=MAX_SQERR,limits=None):
#------------------------------------------------------------------------------
#   creates a register entry if the parameter is None or with a high error
#------------------------------------------------------------------------------
        if (self.val == None) or (self.sqerr > MAX_SQERR):

            self.val = val
            if limits is not None:
                (newMin,newMax) = limits

# update limits only if not in conflict with old limits !!!!

                newMin = min(newMin,self.valMax)
                newMax = max(newMax,self.valMin)
                
                self.valMin = max(newMin,self.valMin)
                self.valMax = min(newMax,self.valMax)
                
#            if newSqErr is not None: self.sqerr = min(self.sqerr,newSqErr)
# HS 20090611 -> default error margin only applied if no limits are given !!!
            elif newSqErr is not None: self.sqerr = min(self.sqerr,newSqErr)
            self.constrain()

            logMessage("Parameter %s estimated to %s [%s,%s]"%
                       (self.name+"["+str(screen.dataGroup)+"]",
                        self.val,self.valMin,self.valMax))
            
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def CCRow(name,m):
#------------------------------------------------------------------------------
#   Builds up rows of CCPars
#------------------------------------------------------------------------------

    row = []
    for i in range(m):
        row.append(CCPar(name+"["+str(i+1)+"]"))
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
    one.dev = 0
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
#   class for convergence testing in check cycles
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def __init__(self,itMax,maxDifference,minImprovement,itMaxImprove):
#------------------------------------------------------------------------------
        self.itMax  = itMax                     #absolute maximum number of iterations
        self.maxDifference = maxDifference      #maximum difference in precision below which cycle stops
        self.minImprovement = minImprovement    #min. improvement required below which cycle stops
        self.itMaxImprove = itMaxImprove        #maximum number of iterations for trying if there's still
                                                #improvement possible

        self.balanceSum = 0
        self.balanceMax = 0
        self.nBalanceChecks = 0
        
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
    def checkBalance(self,values):
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
        minVal = INFINITE
        maxVal = 0
        for x in values:
            if x is not None:
                minVal = min(minVal,x)
                maxVal = max(maxVal,x)

        if maxVal > 0:
            balance = min((maxVal - minVal)/maxVal,1.0) #> 1 and Nones count the same ...
        elif minVal == 0:
            balance = 0.
        else:
            balance = 1.
            
        self.balanceSum += balance
        self.balanceMax = max(balance,self.balanceMax)
        self.nBalanceChecks += 1
        return balance
    
#------------------------------------------------------------------------------
    def initCheckBalance(self):
#------------------------------------------------------------------------------
        self.balanceSum = 0
        self.balanceMax = 0
        self.nBalanceChecks = 0

#------------------------------------------------------------------------------
    def getMeanBalance(self):
#------------------------------------------------------------------------------
        if self.nBalanceChecks > 0:
            return self.balanceSum/self.nBalanceChecks
        else:
            return 0

#------------------------------------------------------------------------------
    def getMaxBalance(self):
#------------------------------------------------------------------------------
        return self.balanceMax

        
#------------------------------------------------------------------------------
    def checkTotalBalance(self):
#------------------------------------------------------------------------------
        self.totalBalanceSum += self.getMeanBalance()
        self.totalBalanceMax = max(self.totalBalanceMax,self.getMaxBalance())
        self.nTotalBalanceChecks += 1

#------------------------------------------------------------------------------
    def initTotalBalance(self):
#------------------------------------------------------------------------------
        self.totalBalanceSum = 0
        self.totalBalanceMax = 0
        self.nTotalBalanceChecks = 0

#------------------------------------------------------------------------------
    def getMeanTotalBalance(self):
#------------------------------------------------------------------------------
        if self.nTotalBalanceChecks > 0:
            return self.totalBalanceSum/self.nTotalBalanceChecks
        else:
            return 0

#------------------------------------------------------------------------------
    def getMaxTotalBalance(self):
#------------------------------------------------------------------------------
        return self.totalBalanceMax

        
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
def calcSum(yname,x1,x2,parType=None):
#------------------------------------------------------------------------------
#   Default function for calculating the product of two values
#------------------------------------------------------------------------------
    y = CCPar(yname,parType=parType)
    if (x1.val ==None or x2.val==None):
        y.val = None
        y.sqerr = INFINITE
    else:
        y.val = x1.val + x2.val
        x1.calcDev()
        x2.calcDev()
        y.dev = x1.dev + x2.dev
        y.sqdev = pow(y.dev,2.0)
        y.calcErr()

    y.valMin = min(INFINITE,x1.valMin + x2.valMin)
    y.valMax = min(INFINITE,x1.valMax + x2.valMax)

    if DEBUG in ["ALL","CALC"]:
        print "CalcSum(x1,x2)_(before constrain)__________________"
        print "x1+x2 = "
        y.show()
        print "parType = ",y.parType
        print "___________________________________________________"

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
        x1.calcDev()
        x2.calcDev()
        x3.calcDev()
        y.val = x1.val + x2.val + x3.val
        y.dev = x1.dev+x2.dev+x3.dev
        y.sqdev = pow(y.dev,2.0)
        y.calcErr()

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
        y.dev = 0
        y.valMin = 0
        y.valMax = 0
        y.val = 0
        for i in range(len(row)):
            y.val += row[i].val
            row[i].calcDev()
            y.dev += row[i].dev
            y.valMin += row[i].valMin
            y.valMax += row[i].valMax
            y.valMax = min(y.valMax,INFINITE)

        y.sqdev = pow(y.sqdev,2.0)
        y.calcErr()
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
def calcDiff(yname,x1,x2,parType=None):
#------------------------------------------------------------------------------
#   Default function for calculating the difference of two values
#------------------------------------------------------------------------------

    y = CCPar(yname,parType=parType)
    if (x1.val is None or x2.val is None):
        y.val = None
        y.sqerr = INFINITE
    else:
        y.val = x1.val - x2.val
            
        if (y.val <> 0):
            x1.calcDev()
            x2.calcDev()
            y.dev = x1.dev + x2.dev
            y.sqdev = pow(y.dev,2.0)
            y.calcErr()
        elif iszero(x1) and iszero(x2):   # all the two are exactly zero
            y.sqerr = 0
        else:
            y.sqerr = INFINITE

    y.valMin = x1.valMin - x2.valMax
    y.valMax = x1.valMax - x2.valMin

    if y.parType <> "S":
        y.valMin = max(y.valMin,0)
        y.valMax = max(y.valMax,0)
#    else:
#        print "CalcDiff: parameter with parType S"
#        y.show()

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
    
    DT1.update(diff)    #calcFlow modifies DT1 <-> adjustflow modifies DT !!!
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
def enthalpy(cL,cV,h,T0,T,x):
#------------------------------------------------------------------------------
#   enthalpy calculation
#------------------------------------------------------------------------------

    if (T ==None):
        return(None)
    
    elif h is None or T0 is None:
        return (cL * T)
    
    elif isequal(T,T0):
        if x is None:
            return (cL * T0 + 0.5*h)
        else:
            return(cL * T0 + x*h)
    
    elif T < T0:
        return(cL * T)
    
    elif T > T0:
        return(cL * T0 + h + cV * (T - T0))

#------------------------------------------------------------------------------
def invEnthalpy(cL,cV,h,T0,y):
#------------------------------------------------------------------------------
#   enthalpy calculation
#------------------------------------------------------------------------------

    h0 = cL*T0
    h1 = h0 + h
    
    if (y ==None):
        return(None,None)
    
    elif y < h0:     #liquid phase
        return (y/cL,0.0)
    
    elif y < h1:
        if h > 0:   #avoid zero division
            x = (y - h0)/h
        else:
            x = 1.0
        return(T0,x)
    
    elif y >= h1:
        return(T0 + (y - h1)/cV,1.0)
    
#------------------------------------------------------------------------------
def calcH(yname,cL,cV,h,T0,x1,x2):
#------------------------------------------------------------------------------
#   Default function for calculating the entalpy h
#------------------------------------------------------------------------------
    y = CCPar(yname)

    y.val = enthalpy(cL,cV,h,T0,x1.val,x2.val)
    y.valMin = enthalpy(cL,cV,h,T0,x1.valMin,x2.valMin)
    y.valMax = enthalpy(cL,cV,h,T0,x1.valMax,x2.valMax)

    if x1.val is None:
        y.sqerr = INFINITE
    else:
        devT = pow(x1.calcDev(),0.5)
        devh = pow(x2.calcDev(),0.5)
        TL = max(0.0,x1.val - devT)

        if x2.val is None:
            xL = 0
        else:
            xL = max(0.0,x2.val - devh)
        hL = enthalpy(cL,cV,h,T0,TL,xL)
        
        TH = x1.val + devT
        if x2.val is None:
            xH = 1
        else:
            xH = x2.val + devh
        hH = enthalpy(cL,cV,h,T0,TH,xH)

        y.sqdev = pow(max(hH - y.val,y.val-hL),2.0)
        y.calcErr()
        
    y.constrain()

    if y.val is not None:
        y.track = []
        y.track.extend(x1.track)
        y.track.extend(x2.track)
        y.cleanUp()

    if DEBUG in ["ALL","CALC"]:
        print "CalcH(x1,x2)____________________________________"
        x1.show()
        x2.show()
        print "h(%s,x1,x2) = "%cL
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
                x2.sqerr = y.sqerr + x1.invSqErr()
                x2.calcDev()
#                x2.sqerr = min(y.sqerr + x1.sqerr,x2.sqerr)
        elif (x2.val is not None):
            if (x2.val ==0):
                if y.val > 0:
                    x1.val = INFINITE
                    x1.sqerr = INFINITE
            else:
                x1.val = y.val / x2.val
                x1.sqerr = y.sqerr + x2.invSqErr()
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

    if DEBUG in ["ALL","ADJUST"]:
        print "adjustProd_before constrain________________________"
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
                x2.sqerr = y.sqerr + x1.invSqErr()
                x2.calcDev()
                                    
#..............................................................................
#Case 3: x2 known, x1 = None
        elif (x1.val == None and not (x2.val == None)):
            if (x2.val ==0 and y.val > 0):
                x1.val = INFINITE
                x1.sqerr = INFINITE
            elif (x2.val > 0):
                x1.val = y.val / x2.val
                x1.sqerr = y.sqerr + x2.invSqErr()
                x1.calcDev()

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
                    x1.sqerr = y.sqerr + x2.invSqErr()
                    x1.calcDev()
                    
                elif (x2.val == 0 and x1.val <> 0):
                    x2.val = y.val / x1.val
                    x2.sqerr = y.sqerr + x1.invSqErr()
                    x2.calcDev()

            else:
                sqerr_invx1 = x1.invSqErr()
                sqerr_invx2 = x2.invSqErr()
                
                if (sqerr_invx1 + sqerr_invx2)==0:
                    f1 = 0.5
                    f2 = 0.5
                else:
                    f1 = sqerr_invx1/(sqerr_invx1 + sqerr_invx2)
                    f2 = sqerr_invx2/(sqerr_invx1 + sqerr_invx2)

                x1.val *= pow(y.val/yold,f1)
                x2.val *= pow(y.val/yold,f2)

                x2.sqerr = y.sqerr + sqerr_invx1    
                x1.sqerr = y.sqerr + sqerr_invx2


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
                x2.sqerr = y.sqerr + x1.invSqErr()
                x2.calcDev()

        elif not (x2.val == None):
            if (x2.val ==0):
                if y.val > 0:
                    x1.val = INFINITE
                    x1.sqerr = INFINITE
            else:
                x1.val = y.val / (a*x2.val)
                x1.sqerr = y.sqerr + x2.invSqErr()
                x1.calcDev()

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
        y.calcDev()
        x1.calcDev()
        x2.calcDev()
        if not (x1.val==None) and ((x1.sqdev < x2.sqdev) or x2.val ==None):
        
            x2.val = y.val - x1.val
            x2.dev = y.dev + x1.dev
            x2.sqdev = pow(x2.dev,2.0)

            if (x2.val <> 0):
                x2.calcErr()
            else:
                x2.sqerr = INFINITE

        elif not (x2.val == None):
            x2.calcDev()

            x1.val = y.val - x2.val
            x1.dev = y.dev + x2.dev
            x1.sqdev = pow(x1.dev,2.0)

            if (x1.val <> 0):
                x1.calcErr()
            else:
                x1.sqerr = INFINITE
    
    newMin = y.valMin-x2.valMax
    newMax = y.valMax-x2.valMin

    x2.valMin = y.valMin-x1.valMax
    x2.valMax = y.valMax-x1.valMin

    x1.valMin = newMin
    x1.valMax = newMax

    if x2.parType <> "S":
        x2.valMin = max(x2.valMin,0.0)
        x2.valMax = max(x2.valMax,0.0)

    if x1.parType <> "S":
        x1.valMin = max(x1.valMin,0.0)
        x1.valMax = max(x1.valMax,0.0)
        

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
        print "adjRowSum: Sum of not Nones =", Sum, "SumErr=", SumErr, "SumSqDev=", SumSqDev, "NNones = ",nNones
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

# first adjustment
        for i in range(m):
            if SumErr <> 0:
                
                newValMin = y.valMin
                newValMax = y.valMax
                for j in range(m):
                    if not j==i:
                        newValMin -= row[j].valMax
                        newValMax -= row[j].valMin
              
                newValMin = max(newValMin,row[i].valMin)
                newValMax = min(newValMax,row[i].valMax)

                row[i].valMax = newValMax
                row[i].valMin = newValMin

                if y.val is not None:
                    newval = row[i].val + ((row[i].sqdev/SumSqDev)*(y.val-Sum))
                    newval = max(newval,row[i].valMin)
                    newval = min(newval,row[i].valMax)
                    newval = min(newval,y.val)  #no value can be bigger than the sum.
                    if DEBUG in ["ALL","ADJUST"]:
                        print "In adjRowSum newval = ",newval," substitutes "
                        row[i].show()
                        
                    shift = newval - row[i].val
                    row[i].val = newval

                    maxSqDev = y.sqdev
                    maxDev = pow(y.sqdev,0.5)
                    for j in range(m):
                        if not j==i:
                            maxSqDev += row[j].sqdev
                            maxDev += row[j].dev

                    newDev = row[i].dev + abs(shift)
                    row[i].dev = min(newDev,maxDev)
                    row[i].sqdev = pow(row[i].dev,2.0)
                    row[i].calcErr()

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
                                
        if y.val is not None:
            diff = abs(Sum - y.val)
        else:
            diff = 1.0

# second pass -> try to adjust the balance

        Sum=0.0
        for i in range(m):
            if row[i].val is None:
                nNones += 1
            else:
                Sum += row[i].val

#        dummy = None                
#        if dummy is not None:
        if y.val is not None:
            newdiff = Sum - y.val
            if newdiff <> 0:
                for i in range(m):
                    newval = row[i].val - newdiff
                    newval = max(newval,row[i].valMin)
                    newval = min(newval,row[i].valMax)
                    shift = row[i].val - newval
                    newdiff -= shift
                    row[i].val = newval
                    row[i].dev += abs(shift)
                    row[i].sqdev = pow(row[i].dev,2.0)
                    row[i].calcErr()

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
def adjustDiff(y,x1,x2,GTZero=False):
#------------------------------------------------------------------------------
#   Default function for calculating and adjusting the components of a difference of two values
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","ADJUST"]:
        print "___________________________________________________"
        print "adjustDiff starting",x1.name,x2.name
        y.show()
        x1.show()
        x2.show()
    
    if y.val is not None:

        y.calcDev()
        x1.calcDev()
        x2.calcDev()

        if iszero(y):   #special case SUM = 0
                    # in this case holds x1 = x2                    
            if GTZero == False:
                ccheck1(x1,x2)

        elif (x1.val is not None) and ((x1.sqdev < x2.sqdev) or x2.val ==None):
          
            x2.val = x1.val - y.val

            x2.dev = y.dev + x1.dev
            x2.sqdev = pow(x2.dev,2.0)
            x2.calcErr()
                
        elif x2.val is not None:
            
            x1.val = y.val + x2.val
            x1.dev = y.dev + x2.dev
            x1.sqdev = pow(x1.dev,2.0)
            x1.calcErr()

    if DEBUG in ["ALL","ADJUST"]:
        print "results before constrain and min/max adjust:___________________________________________"
        y.show()
        x1.show()
        x2.show()
        print "___________________________________________________"

    newMin = min(y.valMin+x2.valMin,INFINITE)
    newMax = min(y.valMax+x2.valMax,INFINITE)

    x2.valMin = x1.valMin-y.valMax
    x2.valMax = x1.valMax-y.valMin

    if x2.parType <> "S":
        x2.valMin = max(x2.valMin,0)
        x2.valMax = max(x2.valMax,0)

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
def adjustH(y,cL,cV,h,T0,x1,x2):
#------------------------------------------------------------------------------
#   Default function for adjusting the entalpy h
#------------------------------------------------------------------------------

    if DEBUG in ["ALL","ADJUST"]:
        print "___________________________________________________"
        print "adjustProd starting",x1.name,x2.name
        y.show()
        print "CL= ",cL
        x1.show()
        x2.show()

    h0 = enthalpy(cL,cV,h,T0,T0,0.0)
    h1 = enthalpy(cL,cV,h,T0,T0,1.0)
    
    if not (y.val == None):

        dev = pow(y.calcDev(),0.5)
        yL = max(y.val - dev,0.0)
        yH = y.val + dev
        
        (T,x) = invEnthalpy(cL,cV,h,T0,y.val)            
        (TL,xL) = invEnthalpy(cL,cV,h,T0,yL)            
        (TH,xH) = invEnthalpy(cL,cV,h,T0,yH)

        devT = max(T-TL,TH-T)
        devx = max(x-xL,xH-x)

        x1.val = T
        x1.sqdev = pow(devT,2.0)
        x1.calcErr()

        x2.val = x
        x2.sqdev = pow(devx,2.0)
        x2.calcErr()

    (Tmin,xmin) = invEnthalpy(cL,cV,h,T0,y.valMin)
    (Tmax,xmax) = invEnthalpy(cL,cV,h,T0,y.valMax)

    x1.valMin = max(min(Tmin,INFINITE),0.0)
    x1.valMax = min(Tmax,INFINITE)

    x1.constrain()

    x2.valMin = max(min(xmin,INFINITE),0.0)
    x2.valMax = min(xmax,1.0)

    x2.constrain()

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

    cycle.checkBalance([y0.val,y1.val])
    
    if DEBUG in ["ALL","CHECK"]:
        print "CCheck1_(before...)________________________________"
        y0.show()
        y1.show()
        print "________________________________Mode = ",CHECKMODE

    y = CCPar("CCheck1",parType=y0.parType)
    
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
   
    if DEBUG in ["ALL","CHECK"]:
        print "CCheck1_(... before constrain ...)_________________"
        y.show()
        print "___________________________________________________"

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

    bal = cycle.checkBalance([y0.val,y1.val,y2.val])
    
    if DEBUG in ["ALL","CHECK"]:
        print "CCheck1_(before...)________________________________"
        y0.show()
        y1.show()
        y2.show()
        print "________________________________Mode = ",CHECKMODE

    row = CCRow("ccheck2-row",3)
    y = CCPar("ccheck2-y",parType=y0.parType)
    
    row[0] = y0
    row[1] = y1
    row[2] = y2
                
    if CHECKMODE == "BEST":
        y = bestOfRow(row,3)
    else:
        y = meanOfRow(row,3)

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
def ccheck2old(y0,y1,y2):
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
        print "_____________________________________Mode = ",CHECKMODE


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

    cycle.checkBalance([y0.val,y1.val,y2.val,y3.val])
    
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
def ccheck4(y0,y1,y2,y3,y4):
#------------------------------------------------------------------------------
#   Carries out consistency checking of the actual value with three externally
#   calculated inputs.
#------------------------------------------------------------------------------
#..............................................................................

    cycle.checkBalance([y0.val,y1.val,y2.val,y3.val,y4.val])

    row = CCRow("ccheck4-row",5)
    y = CCPar("ccheck4-y",parType=y0.parType)
    
    row[0] = y0
    row[1] = y1
    row[2] = y2
    row[3] = y3
    row[4] = y4
                
    if CHECKMODE == "BEST":
        y = bestOfRow(row,5)
    else:
        y = meanOfRow(row,5)

    y0.update(y)
    y1.update(y)
    y2.update(y)
    y3.update(y)
    y4.update(y)

    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def ccheck5(y0,y1,y2,y3,y4,y5):
#------------------------------------------------------------------------------
#   Carries out consistency checking of the actual value with three externally
#   calculated inputs.
#------------------------------------------------------------------------------
#..............................................................................

    cycle.checkBalance([y0.val,y1.val,y2.val,y3.val,y4.val,y5.val])

    row = CCRow("ccheck5-row",6)
    y = CCPar("ccheck5-y",parType=y0.parType)
    
    row[0] = y0
    row[1] = y1
    row[2] = y2
    row[3] = y3
    row[4] = y4
    row[5] = y5
                
    if CHECKMODE == "BEST":
        y = bestOfRow(row,6)
    else:
        y = meanOfRow(row,6)

    y0.update(y)
    y1.update(y)
    y2.update(y)
    y3.update(y)
    y4.update(y)
    y5.update(y)

    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def checkIfConflict(y1,y2):
#------------------------------------------------------------------------------
#   Checks if there is a conflict between values and error ranges of y1 and y2
#------------------------------------------------------------------------------
#..............................................................................

    if y1.val is not None and y2.val is not None:
        dif=abs(y1.val-y2.val)
        maxDif = max(abs(y1.val),abs(y2.val))* \
                 max(pow(y1.sqerr+y2.sqerr,0.5)*CONFIDENCE,NUMERIC_ERR)
        
        if dif > maxDif + NUMERIC_ERR:
            print "======================================================"
            print "WARNING !!!! "
            print "CCheckFunctions (checkIfConflict): contradiction found"
            print "-> stochastic error !!!"
            y1.show()
            y2.show()
            print "dif = ",dif," maxDif = ",maxDif
            print "======================================================"
            conflict.screen(y1,y2,dif,maxDif)

    difLimits = max(y2.valMin - y1.valMax,y1.valMin - y2.valMax)
    if difLimits > NUMERIC_ERR*max(y1.valMin,y2.valMin):
        print "======================================================"
        print "WARNING !!!! "
        print "CCheckFunctions (checkIfConflict): contradiction found"
        print "-> absolute limits error !!!"
        y1.show()
        y2.show()
        print "difLimits = ",difLimits
        print "======================================================"
        conflict.screen(y1,y2,difLimits,0.0)
        

    
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

#    print "BestOf: starting"
#    y1.show()
#    y2.show()

    checkIfConflict(y1,y2)

    if (y1.sqerr < y2.sqerr):
            best = y1
    else:
            best = y2

# adding too much tracks gave problems ... -> back to the roots
# just following the track of the best
#    best.track = []
#    best.track.extend(y1.track)
#    best.track.extend(y2.track)
        
    best.valMin = max(y1.valMin,y2.valMin)
    best.valMax = min(y1.valMax,y2.valMax)

#    print "BestOf: before constrain"
#    best.show()
    best.constrain()
#    print "BestOf: after constrain"
#    best.show()

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

    for i in range(m):
        if row[i].val is not None:
            for j in range(i+1,m):
                if row[j].val is not None:
                    checkIfConflict(row[i],row[j])

    best = CCPar("",parType=row[0].parType)
    best.val = 1.0
    
    for i in range(m):
        best = bestOf(best,row[i])
    
    return best   

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def meanValueOf(y1,y2):
#------------------------------------------------------------------------------
#   Selects the best of three values (the one with lowest errors)
#   Does not carry out None-check !!!!
#------------------------------------------------------------------------------

    mean = CCPar("meanValueOf",parType=y1.parType)
    mean.update(bestOf(y1,y2))

#    mean.track = trackBestOf(y1,y2)
# adding too much tracks gave problems ... -> back to the roots
# just following the track of the best
    mean.track = trackBestOf(y1,y2) #assure that the best comes first
    mean.track.extend(y1.track)
    mean.track.extend(y2.track)
    mean.cleanUp()

#    sumSqErr = pow(y1.sqerr,2) + pow(y2.sqerr,2)
    sumSqDev = y1.calcDev() + y2.calcDev()
    
    dif=abs(y1.val-y2.val)
    maxDif = pow(sumSqDev,0.5)*CONFIDENCE
    
    if dif > maxDif + NUMERIC_ERR:
        print "======================================================"
        print "WARNING !!!! "
        print "CCheckFunctions (meanValueOf): contradiction found"
        y1.show()
        y2.show()
        print "======================================================"

    if y1.sqdev > 10.0*y2.sqdev or y2.sqdev > 10.0*y1.sqdev:
        pass
    
    elif sumSqDev > 0:
        mean.val = (y1.sqdev*y2.val + y2.sqdev*y1.val)/sumSqDev
        
    else:
        mean.val=0.5*(y1.val+y2.val)
        
    shift = min(abs(mean.val-y1.val),abs(mean.val-y2.val))
    y1.calcDev()
    y2.calcDev()
    mean.dev = min(y1.dev,y2.dev) + shift
    mean.sqdev = pow(mean.dev,2.0)
    
    mean.valMin = max(y1.valMin,y2.valMin)
    mean.valMax = min(y1.valMax,y2.valMax)
    mean.calcErr()

    mean.constrain()
        
    return mean   

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def meanValueOf3(y1,y2,y3):
#------------------------------------------------------------------------------
#   Selects the best of three values (the one with lowest errors)
#   Does not carry out None-check !!!!
#------------------------------------------------------------------------------

    checkIfConflict(y1,y2)
    checkIfConflict(y1,y3)
    checkIfConflict(y2,y3)

    mean = CCPar("meanValueOf3",parType=y1.parType)
    mean.track = trackBestOf3(y1,y2,y3) #assure that best comes first
    mean.track.extend(y1.track)
    mean.track.extend(y2.track)
    mean.track.extend(y3.track)
    mean.cleanUp()

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
        p1 = 1.0/y1.sqdev
        p2 = 1.0/y2.sqdev
        p3 = 1.0/y3.sqdev
        mean.val = (y1.val*p1 + y2.val*p2 + y3.val*p3)/(p1+p2+p3)

    shift = min(abs(mean.val-y1.val),abs(mean.val-y2.val),abs(mean.val-y3.val))
                
    y1.calcDev()
    y2.calcDev()
    y3.calcDev()
                
    mean.dev = min(y1.dev,y2.dev,y3.dev) + shift
                
    mean.sqdev = pow(mean.dev,2.0)

    mean.valMin = max(y1.valMin,y2.valMin,y3.valMin)
    mean.valMax = min(y1.valMax,y2.valMax,y3.valMax)
    mean.calcErr()
            
    mean.constrain()

    return mean   

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def meanOfRow(row,m):
#------------------------------------------------------------------------------
#   Calculates the mean value of a row of CCPar values
#------------------------------------------------------------------------------

    for i in range(m):
        if row[i].val is not None:
            for j in range(i+1,m):
                if row[j].val is not None:
                    checkIfConflict(row[i],row[j])

    mean = CCPar("meanOfRow",parType=row[0].parType)
    mean.track = trackBestOfRow(row,m)  #assure that best comes first
    for i in range(m):
        mean.track.extend(row[i].track)
    mean.cleanUp()

    if DEBUG in ["ALL","ADJUST"]:
        print "meanOfRow__________________________________________"
        for i in range(m):
            row[i].show()  
        print "___________________________________________________"

    
    minDev = INFINITE
    for i in range(m):
        minDev = min(minDev,row[i].calcDev())
        
    if minDev == 0:
        minWeight = INFINITE
    else:
        minWeight = 0.1/minDev
    
    sumVal = 0
    sumWeight = 0

    for i in range(m):
        if not (row[i].val == None):
            if row[i].sqdev == 0:
                weight = INFINITE
            else:
                weight = 1./row[i].sqdev

            if weight < minWeight:
                weight = 0            # skip very bad estimates
                
            sumWeight += weight
            sumVal += row[i].val*weight

        mean.valMin = max(mean.valMin,row[i].valMin)
        mean.valMax = min(mean.valMax,row[i].valMax)
    
    if sumWeight > 0:
        mean.val = sumVal/sumWeight

        mean.sqdev = INFINITE
        for i in range(m):
            if row[i].val is not None:
                shift = mean.val - row[i].val
                newDev = pow(row[i].sqdev,0.5) + abs(shift)
                mean.sqdev = min(mean.sqdev,pow(newDev,2.0))

        mean.calcErr()

    mean.constrain()
    
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
