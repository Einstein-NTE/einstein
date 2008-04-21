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
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	08/03/2008
#	Last revised by:    claudia Vannoni      9/04/2008
#                           claudia Vannoni      16/04/2008
#
#       Changes in last update:
#                           moved functions to ccheckfunctions
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

MAXBALANCEERROR = 1.e-3
NMAXITERATIONS = 5
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
class CheckMatrix():
#------------------------------------------------------------------------------
#   Carries out consistency checking for equipe j
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    def __init__(self,name,colTotals,rowTotals,linkMatrix):     #function that is called at the beginning when object is created
#------------------------------------------------------------------------------
#   init function is only called once at the beginning (every time that base
#   actions that should be carried out in each iteration -> initCheck()
#------------------------------------------------------------------------------

# assign a variable to all intermediate values needed
        ncol = len(colTotals)
        nrow = len(rowTotals)
        self.ncol = ncol
        self.nrow = nrow

        self.colTotals = colTotals
        self.rowTotals = rowTotals
        
        self.M = CCMatrix(name+"(M)",ncol,nrow)
        self.FCol = CCMatrix(name+"(FCol)",ncol,nrow)
        self.FRow = CCMatrix(name+"(FRow)",ncol,nrow)
        self.initF(linkMatrix)

        
#------------------------------------------------------------------------------
    def initF(self,linkMatrix):
#------------------------------------------------------------------------------
#   Initialises the FRow and FCol matrix with the basic link matrix:
#   0: no connection between source n and sink m
#   1: connection between source n and sink m
#------------------------------------------------------------------------------

#..............................................................................
# avoid singularities if one row or one column is completely zero

        rowSum = []
        for n in range(self.nrow):
            rowSum.append(0.0)
            for m in range(self.ncol):
                rowSum[n] += linkMatrix[n][m]

        colSum = []
        for m in range(self.ncol):
            colSum.append(0.0)
            for n in range(self.nrow):
                colSum[m] += linkMatrix[n][m]

#..............................................................................
# now assign zeros where the linkMatrix is zero

        for m in range(self.ncol):
            for n in range(self.nrow):
                if linkMatrix[n][m] == 0 and rowSum[n]>0:
                    self.FRow[n][m].val = 0
                    self.FRow[n][m].valMin = 0
                    self.FRow[n][m].valMax = 0
                    self.FRow[n][m].sqerr = 0
                else:
                    self.FRow[n][m].val = None
                    self.FRow[n][m].valMin = 0
                    self.FRow[n][m].valMax = 1
                    self.FRow[n][m].sqerr = INFINITE

                if linkMatrix[n][m] == 0 and colSum[m]>0:
                    self.FCol[n][m].val = 0
                    self.FCol[n][m].valMin = 0
                    self.FCol[n][m].valMax = 0
                    self.FCol[n][m].sqerr = 0
                else:
                    self.FCol[n][m].val = None
                    self.FCol[n][m].valMin = 0
                    self.FCol[n][m].valMax = 1
                    self.FCol[n][m].sqerr = INFINITE

                if linkMatrix[n][m] == 0:
                    self.M[n][m].val = 0
                    self.M[n][m].valMin = 0
                    self.M[n][m].valMax = 0
                    self.M[n][m].sqerr = 0
                else:
                    self.M[n][m].val = None
                    self.M[n][m].valMin = 0
                    self.M[n][m].valMax = INFINITE
                    self.M[n][m].sqerr = INFINITE
        
#------------------------------------------------------------------------------        
    def checkFRow(self):  #later on should import data from SQL. now simply sets to some value
#------------------------------------------------------------------------------
#   checks the row sums of the distribution matrix FRow (SUM = 1)
#------------------------------------------------------------------------------
        
        diff = 0
        for n in range(self.nrow):
            diff += adjRowSum("FRow",CCOne(),self.FRow[n],self.ncol)
        return diff

#------------------------------------------------------------------------------
    def checkFCol(self):
#------------------------------------------------------------------------------
#   checks the column sums of the distribution matrix FCol (SUM = 1)
#------------------------------------------------------------------------------
        diff = 0
        for m in range(self.ncol):
            col = CCRow("FCol",self.nrow) #???
            for n in range(self.nrow):
                col[n] = self.FCol[n][m]
                
            diff += adjRowSum("FCol",CCOne(),col,self.nrow)

            for n in range(self.nrow):
                self.FCol[n][m].update(col[n])
        return diff

#------------------------------------------------------------------------------
    def checkMRow(self):  #later on should import data from SQL. now simply sets to some value
#------------------------------------------------------------------------------
#   calculates energy balances in rows of the distribution matrix
#------------------------------------------------------------------------------
        Sum = CCPar("checkMRow")
        
        diff = 0
        for n in range(self.nrow):
            Sum = calcRowSum("calcMRow",self.M[n],self.ncol)
            ccheck1(Sum,self.rowTotals[n])
            if not (Sum.val == None):              
                diff += adjRowSum("adjMRow",Sum,self.M[n],self.ncol)
        return diff

#------------------------------------------------------------------------------
    def checkMCol(self):
#------------------------------------------------------------------------------
#   calculates energy balances in colmns of the distribution matrix
#------------------------------------------------------------------------------
        Sum = CCPar("checkMRow")

        diff = 0
        for m in range(self.ncol):
            col = CCRow("colMCol",self.nrow) #???
            for n in range(self.nrow):
                col[n] = self.M[n][m]
            Sum = calcRowSum("calcMCol",col,self.nrow)
            ccheck1(Sum,self.colTotals[m])

            if not (self.colTotals[m] == None):
                diff += adjRowSum("adjMCol",Sum,col,self.nrow)

            for n in range(self.nrow):
                self.M[n][m].update(col[n])
        return diff

#------------------------------------------------------------------------------
    def checkM3(self):
#------------------------------------------------------------------------------
# Carries out the check of equations:
# (1) Mij = FRowij * xi
# (2) Mij = FColij * yj
#------------------------------------------------------------------------------
        MColTotals = CCMatrix("CheckM3-MCT",self.ncol,self.nrow)
        MRowTotals = CCMatrix("CheckM3-MRT",self.ncol,self.nrow)
        Mean = CCPar("CheckM3-Mean")
        col = CCRow("CheckM3-col",self.nrow)
        
        for n in range(self.nrow):
            for m in range(self.ncol):                
                MCol = calcProd("MCol",self.FCol[n][m],self.colTotals[m])
                MRow = calcProd("MRow",self.FRow[n][m],self.rowTotals[n])

                ccheck2(self.M[n][m],MCol,MRow)

                MColTotals[n][m].update(self.colTotals[m])
                MRowTotals[n][m].update(self.rowTotals[n])

                adjustProdS(MRow,self.FRow[n][m],MRowTotals[n][m])
                adjustProdS(MCol,self.FCol[n][m],MColTotals[n][m])

# get mean values of MRowTotals

        for n in range(self.nrow):
            Mean = meanOfRow(MRowTotals[n],self.ncol)
            ccheck1(Mean,self.rowTotals[n])

        for m in range(self.ncol):
            for n in range(self.nrow):
                col[n].update(MColTotals[n][m])
            Mean = meanOfRow(col,self.nrow)
            ccheck1(Mean,self.colTotals[m])
        

#------------------------------------------------------------------------------
    def check(self):
#------------------------------------------------------------------------------
#   Main function of matrix checking procedure
#------------------------------------------------------------------------------
#..............................................................................
# Step 0: initialise the vectors and arrays with (external) intial values
        
        improvement = INFINITE
        improvementCtr = 0

        if DEBUG in ["ALL","BASIC"]:
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

            diff += self.checkMCol()    #checks energy balances by columns

            if DEBUG in ["ALL"]:
                print "======================================================"
                print "check MCol============================================"
                print "======================================================"
                self.printM()

#..............................................................................
# Block B: adjustment of row/column-sums in FCol and FRow

            diff += self.checkFRow()

            if DEBUG in ["ALL"]:
                print "======================================================"
                print "check FRow============================================"
                print "======================================================"
                self.printM()

            diff += self.checkFCol()

            if DEBUG in ["ALL"]:
                print "======================================================"
                print "check FCol============================================"
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

            if DEBUG in ["ALL"]:
                print "======================================================"
                print "CheckMatrix (check): diff[%s] = "%i,diff
                print "======================================================"
                print "improvement [%s]: "%improvementCtr,improvement," diff: ",diff

            if (diff < MAXBALANCEERROR or improvement < 0.1*MAXBALANCEERROR):
                improvementCtr += 1
            else:
                improvementCtr = 0
            improvement = diff

            if improvementCtr == 10:
                break

        if DEBUG in ["ALL","BASIC"]:
            print "======================================================"
            print "CheckMatrix concluded ================================"
            print "======================================================"
            print "last adjustment difference: ",diff
            print "======================================================"
            self.printM()
            
#------------------------------------------------------------------------------
    def printM(self):
        print "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
        for i in range(self.nrow):
            for j in range(self.ncol):
                print i,j,self.M[i][j].val,self.M[i][j].sqerr,self.FCol[i][j].val,self.FRow[i][j].val
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

    NI = 2
    NJ = 3
    
    FECi = CCRow("FECi",NI)
    FECi[0].val = 2
    FECi[0].sqerr = 0.
    FECi[0].valMin = 1.9
    FECi[0].valMax = 2.1
    
    FECi[1].val = 4
    FECi[1].sqerr = 0.
    FECi[1].valMin = 3.9
    FECi[1].valMax = 4.1

    FECj = CCRow("FECj",NJ)
    FECj[0].val = 3
    FECj[0].valMin = 2.9
    FECj[0].valMax = 3.1
    FECj[0].sqerr = 0.001
    FECj[1].val = 2.5
    FECj[1].sqerr = 0.001
    FECj[1].valMin = 2.4
    FECj[1].valMax = 2.6
    FECj[2].val = None
    FECj[2].sqerr = INFINITE
    FECj[2].valMin = 0
    FECj[2].valMax = INFINITE

    FECLink = arange(NI*NJ).reshape(NJ,NI)
    FECLink[0][0] = 1
    FECLink[1][0] = 0
    FECLink[2][0] = 0
    FECLink[0][1] = 1
    FECLink[1][1] = 1
    FECLink[2][1] = 1
    print FECLink

    CM = CheckMatrix("FECi-FECj",FECi,FECj,FECLink)
    
    CM.check()
