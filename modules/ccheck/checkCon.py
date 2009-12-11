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
#	CheckCon
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Simplified version of CheckMatrix for the connection of heat exchangers
#       to equipments, pipes etc.
#
#       Simplification: 1 HX has only one connection -> distribution matrix
#       consists of 0's and 1's
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	08/03/2008
#                           (based on CheckMatrix v0.04)
#
#	Last revised by:    
#
#       Changes in last update:
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

MAXBALANCEERROR = 1.e-3
NMAXITERATIONS = 1
INFINITE = 1.e99    # numerical value assigned to "infinite"

from math import *
from ccheckFunctions import *
from numpy import *

#------------------------------------------------------------------------------
def CCMatrix(name,ncol,nrow):
#------------------------------------------------------------------------------
#   Builds up matrix
#------------------------------------------------------------------------------

    matrix = []
    for j in range(nrow):
        matrix.append(CCRow(name+"["+str(j)+"]",ncol))
    return matrix


#------------------------------------------------------------------------------
class CheckCon():
#------------------------------------------------------------------------------
#   Carries out consistency checking for equipe j
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def __init__(self,name,colTotals,rowTotals,linkMatrix,ambient=False):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   init function is only called once at the beginning (every time that base
#   actions that should be carried out in each iteration -> initCheck()
#------------------------------------------------------------------------------

        self.ambient = ambient #ambient = True: -> dissipation to ambient is allowed
# assign a variable to all intermediate values needed
        ncol = len(colTotals)
        nrow = len(rowTotals)
        self.ncol = ncol
        self.nrow = nrow

        self.colTotals = colTotals
        self.rowTotals = rowTotals
        
        self.M = CCMatrix(name+"(M)",ncol,nrow)
        self.FCol = linkMatrix

        self.MAmb = CCRow(name+"(MAmb)",nrow)   #Energy dissipated to ambient
        self.MAmb1 = CCRow(name+"(MAmb1)",nrow)

        self.MRec = CCRow(name+"(MRec)",nrow)   #Energy used (recovered)
        self.MRec1 = CCRow(name+"(MRec1)",nrow)

#..............................................................................
#   Initialises the distribution matrix:
#   0: no connection between sub-system n and HX m
#   1: connection between sub-system n and HX m
#------------------------------------------------------------------------------

#..............................................................................
# avoid singularities if one row or one column is completely zero

        for m in range(self.ncol):
            colSum = 0
            for n in range(self.nrow):
                colSum += linkMatrix[n][m]

            if colSum > 1:
                print "CheckCon (__init__): ERROR in linkMatrix, column %s"%m

#..............................................................................
# now assign zeros where the linkMatrix is zero

        for m in range(self.ncol):
            for n in range(self.nrow):

                if linkMatrix[n][m] == 0:
                    self.M[n][m].val = 0
                    self.M[n][m].valMin = 0
                    self.M[n][m].valMax = 0
                    self.M[n][m].sqerr = 0
                else:
                    self.M[n][m].update(self.colTotals[m])
                    
#------------------------------------------------------------------------------
    def checkMRow(self):  #later on should import data from SQL. now simply sets to some value
#------------------------------------------------------------------------------
#   calculates energy balances in rows of the distribution matrix
#   if ambient = True: SUM(M[n]) = rowTotals[n] + MAmb[n]
#   else:              SUM(M[n]) = rowTotals[n], MAmb[n] = 0
#------------------------------------------------------------------------------
        Sum = CCPar("checkMRow-Sum")
        
        diff = 0
        for n in range(self.nrow):

            if self.ambient == False:
                self.MAmb[n].setValue(0.0)

            self.MRec1[n] = calcRowSum("calcMRow",self.M[n],self.ncol)
            Sum = calcSum("MRowAmb",self.MRec[n],self.MAmb[n])

            ccheck1(self.MRec[n],self.MRec1[n])
            ccheck1(Sum,self.rowTotals[n])

            adjustSum(Sum,self.MRec1[n],self.MAmb[n])

            ccheck1(self.MAmb[n],self.MAmb1[n])
            ccheck1(self.MRec[n],self.MRec1[n])
                
            if not (self.MRec[n].val == None):              
                diff += adjRowSum("adjMRow",self.MRec[n],self.M[n],self.ncol)
        return diff

#------------------------------------------------------------------------------
    def checkM3(self):
#------------------------------------------------------------------------------
# Carries out the check of the columns
# (2) Mij = yj if LinkMatrix(i,j) = 1
#------------------------------------------------------------------------------
        for m in range(self.ncol):                
            for n in range(self.nrow):
                if self.FCol[n][m] == 1:
                    ccheck1(self.M[n][m],self.colTotals[m])                

#------------------------------------------------------------------------------
    def check(self):
#------------------------------------------------------------------------------
#   Main function of matrix checking procedure
#------------------------------------------------------------------------------
#..............................................................................
# Step 0: initialise the vectors and arrays with (external) intial values
        
        improvement = INFINITE
        improvementCtr = 0

        if DEBUG in ["ALL","MAIN","BASIC"]:
            print "======================================================"
            print " starting values of connection matrix M"
            print "======================================================"
            self.printM()

        for i in range(NMAXITERATIONS):

            diff = 0

#..............................................................................
# Block A: adjustment of energy balances in M

            diff += self.checkMRow()    #checks energy balances by rows

            if DEBUG in ["ALL"]:
                print "======================================================"
                print "check MRow============================================"
                print "======================================================"
                self.printM()

#..............................................................................
# Block C: adjustment of matrix

            self.checkM3()

            if DEBUG in ["ALL"]:
                print "======================================================"
                print "check M3=============================================="
                print "======================================================"
                self.printM()
            
#..............................................................................
# Check for iterative improvement of balance errors

            improvement -= diff

            if DEBUG in ["ALL","MAIN"]:
                print "======================================================"
                print "CheckCon (check): diff[%s] = "%i,diff
                print "======================================================"
                print "improvement [%s]: "%improvementCtr,improvement," diff: ",diff

            if (diff < MAXBALANCEERROR or improvement < 0.1*MAXBALANCEERROR):
                improvementCtr += 1
            else:
                improvementCtr = 0
            improvement = diff

            if improvementCtr == 10:
                break

        if DEBUG in ["ALL","MAIN","BASIC"]:
            print "======================================================"
            print "CheckCon concluded ==================================="
            print "======================================================"
            print "last adjustment difference: ",diff
            print "======================================================"
            self.printM()
            
#------------------------------------------------------------------------------
    def printM(self):
        print "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
        for i in range(self.nrow):
            for j in range(self.ncol):
                print i,j,self.M[i][j].val,self.M[i][j].sqerr
        print "colTotals"
        for j in range(self.ncol):
            print j,self.colTotals[j].val,self.colTotals[j].sqerr
        print "rowTotals"
        for i in range(self.nrow):
            print i,self.rowTotals[i].val,self.rowTotals[i].sqerr
        print "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
        
#------------------------------------------------------------------------------
                
        
#==============================================================================

if __name__ == "__main__":

    pass
    
