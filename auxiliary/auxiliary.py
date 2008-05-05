#==============================================================================
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	AUXILIARY - Auxiliary functions (general)
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Module for calculation of energy statistics
#
#==============================================================================
#
#	Version No.: 0.05
#	Created by: 	    Hans Schweiger	30/01/2008
#	Revised by:         Tom Sobota          12/03/2008
#                           Hans Schweiger      21/03/2008
#                           Stoyan Danov        28/03/2008
#                           Hans Schweiger      24/04/2008
#                           Stoyan Danov        05/05/2008
#
#       Changes:
#       - introduction of function frange
#	20/03/08: HP specific functions eliminated. abstract nomenclature of
#                   list and table interpolation functions
#       28/03/2008 added: transpose(), firstHigher()
#       24/04/2008  function "noneFilter" added
#       05/05/2008 bug corrected in interpolateList (yList was used instead of ylist)
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

from math import *

#------------------------------------------------------------------------------		
#   1. Minimum and maximum values
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
def min(a,b):
#------------------------------------------------------------------------------		
    if a >= b: return b
    else: return a

#------------------------------------------------------------------------------		
def max(a,b):
#------------------------------------------------------------------------------		
    if a >= b: return a
    else: return b

#------------------------------------------------------------------------------		
def maxInList(ylist):
#------------------------------------------------------------------------------		
    m = 0
    for i in range(len(ylist)):
        m = max(m,ylist[i])
    return m

#------------------------------------------------------------------------------		
#   2. Table look-up and interpolation routines
#       - lists: lists of values ylist[i]
#       - tables: pairs of values y-x in lists ylist[i],xlist[i]
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------
def lastNonZero(ylist):
#------------------------------------------------------------------------------
#finds the last filled position of the list (different from zero)
#------------------------------------------------------------------------------
    n = len(ylist)
    i = n - 1
    while ylist[i] == 0.0:
        if i < 1: break
        i = i - 1
    return i
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def firstNonZero(ylist):
#------------------------------------------------------------------------------
#finds the first filled position of the list (different from zero)
#------------------------------------------------------------------------------
    n = len(ylist)
    i = 0
    while ylist[i] == 0.0:
        if i > n -1: break
        i = i + 1
    return i
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def findInListASC(y,ylist):
#------------------------------------------------------------------------------
#   selects the table entry with a value closest, but lower to val.
#   returns the index
#------------------------------------------------------------------------------
    for i in range(len(ylist)):
        if y < ylist[i]:
            return int(i-1)
    return(len(ylist)-1)        
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def interpolateList(xi,ylist):
#------------------------------------------------------------------------------
#   interpolates the y-values in a table y(x) for non-integer values of x0
#------------------------------------------------------------------------------
    #finds the temperature interval values (floor and ceil)
    i1 = int(floor(xi)) # math.floor and math.ceil return DOUBLEs -> int() should be applied then
    i0 = int(ceil(xi))
    if i0 == i1: #avoid division to zero
        y = ylist[i1]# SD: error yList en vez de ylist, 05/05/2008
        #print 'interp...1'
    else:
        #print 'interp...2'
        y1 = ylist[i1]
        y0 = ylist[i0]
        #interpolates to find the Q corresponding to T
        y = (y0 * (i1 - xi) + y1 * (xi - i0))/(i1-i0)
    return y   

#------------------------------------------------------------------------------
def interpolateTable(x,xlist,ylist):
#------------------------------------------------------------------------------
#   interpolates the table values ylist(xlist) for values of x not in xlist
#   only works for montonous curves (both ascending and descending)
#------------------------------------------------------------------------------

    n = len(xlist)
    for i in range(n-1):
        if ((x >= xlist[i]) and (x < xlist[i+1])) or ((x <= xlist[i]) and (x > xlist[i+1])):
            y = (ylist[i]*(xlist[i+1]-x) + ylist[i+1]*(x-xlist[i]))/(xlist[i+1]-xlist[i])
            break   

#...............................................................................
# check of special cases when x is out of the limits of xlist
# in this case, the corresponding limit value of y is assigned
    
    if xlist[0] < xlist[n-1]:  #ascending list

        if x < xlist[0]:
            y = ylist[0]
            
        elif x >= xlist[n-1]:
            y = ylist[n-1]
            
    else:   # descending list

        if x > xlist[0]:
            y = ylist[0]
            
        elif x <= xlist[n-1]:
            y = ylist[n-1]

    return y

#---------------------------------------------------------------------------
def transpose(T):
    """ Transposes a matrix (list of lists) interchanging rows with columns
    """
    invT = []

    for j in range(len(T[0])):
        row = []
        for i in range(len(T)):
            row.append(T[i][j])
        invT.append(row)

    return invT

#-----------------------------------------------------------------------------
def firstHigher(val, ASClist):
    """Returns the index of the first higher value than val in the
    ascending values list ASClist"""

    for i in range(len(ASClist)):
        if val <= ASClist[i]:
            return i
        else:
            continue
    
    print 'In auxiliary.py - firstHigher() not found: error!'
    return 0


#------------------------------------------------------------------------------		
#   3. Others
#------------------------------------------------------------------------------		

#------------------------------------------------------------------------------		
def frange(start, end, inc=None):   
#------------------------------------------------------------------------------
#   A range function with float arguments
#------------------------------------------------------------------------------		

    if inc == None:
        inc = 1.0

    L = []
    while True:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L

#------------------------------------------------------------------------------		
def noneFilter(datalist,substitute=" "):   
#------------------------------------------------------------------------------
#   A range function with float arguments
#------------------------------------------------------------------------------		

    for i in range(len(datalist)):
        if datalist[i] is None:
            datalist[i] = substitute
    return datalist

#==============================================================================

