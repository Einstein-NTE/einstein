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
#	CONNECT
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Builds the connection matrices between the different subsystems:
#       Fuels - Equipes - Pipes/Ducts - Processes
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Hans Schweiger	13/06/2008
#	Last revised by:    
#                    
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

from einstein.GUI.status import *
from einstein.modules.project import *
from numpy import *

#------------------------------------------------------------------------------
def getConnections():
#------------------------------------------------------------------------------
#   Gets the connections from the entries in the SQL
#------------------------------------------------------------------------------
        
#..............................................................................
# get list of sub-systems

    fuels = Status.prj.getFuels()
    Status.NFuels = len(fuels)
    Status.NFET = Status.NFuels+1
    NI = Status.NFET
    
    equipments = Status.prj.getEquipments()
    Status.NEquipe = len(equipments)
    NJ = Status.NEquipe
    
    pipes = Status.prj.getPipes()
    Status.NPipeDuct = len(pipes)
    NM = Status.NPipeDuct

    processes = Status.prj.getProcesses()
    Status.NThProc = len(processes)
    NK = Status.NThProc
    
    hxes = Status.prj.getHXes()
    Status.NHX = len(hxes)
    NH = Status.NHX
    
    whees = Status.prj.getWHEEs()
    Status.NWHEE = len(whees)
    NWHEE = Status.NWHEE

#..............................................................................
# 1. FETi-FETj-Link: fuels used in equipment

    fuelIDs_i = Status.prj.getFuelList("DBFuel_id")
    fuelIDs_i.insert(0,99) #first fuel is electricity (default_ID = 99)
    
    fuelIDs_j = Status.prj.getEquipmentList("DBFuel_id")

    print "Connect: fuelIDs_i",fuelIDs_i
    print "Connect: fuelIDs_j",fuelIDs_j
   

    Status.FETLink = arange(NI*NJ).reshape(NJ,NI)  # reshape(rows,cols)
    
    for j in range(NJ):
        for i in range(NI):
            if fuelIDs_i[i] == fuelIDs_j[j]:
                Status.FETLink[j][i] = 1
            else:
                Status.FETLink[j][i] = 0

    print "Connect: FETLink created"
    print Status.FETLink
        
#..............................................................................
# 2. USHj-USHm-Link: conecction equipment to pipe

    pipes_j = Status.prj.getEqList("PipeDuctEquip")
        
    pipeID_m = Status.prj.getPipeList("QDistributionHC_ID")

    print "Connect: pipes_j",pipes_j
    print "Connect: pipeID_m",pipeID_m
       
    Status.USHLink = arange(NJ*NM).reshape(NM,NJ)  # reshape(rows,cols)

    for m in range(NM):
        for j in range(NJ):
            pipeIDs_j = []
            if pipes_j[j] is not None:
                pipesSplit = pipes_j[j].split(';')
                for i in range(len(pipesSplit)):
                    pipeIDs_j.append(long(pipesSplit[i]))
                print "Connect: pipeIDs_j[%s]"%j,pipeIDs_j
                
            if pipeID_m[m] in pipeIDs_j:
                Status.USHLink[m][j] = 1
            else:
                Status.USHLink[m][j] = 0
        
    print "Connect: USHLink created"
    print Status.USHLink

#..............................................................................
# 3. UPHm-UPHk Link: conecction pipe to process

    pipeName_k = Status.prj.getProcessList("PipeDuctProc")    
    pipeName_m = Status.prj.getPipeList("Pipeduct")

    print "Connect: pipeName_k",pipeName_k
    print "Connect: pipeName_m",pipeName_m
       
    Status.UPHLink = arange(NM*NK).reshape(NK,NM)  # reshape(rows,cols)

    for k in range(NK):
        for m in range(NM):
            if pipeName_m[m] == pipeName_k[k]:
                Status.UPHLink[k][m] = 1
            else:
                Status.UPHLink[k][m] = 0
        
    print "Connect: UPHLink created"
    print Status.UPHLink

#..............................................................................
# 4. QHX/QWH - Eq/Pipe/Proc Links

    sourceName_h = Status.prj.getHXList("HXSource")    
    sinkName_h = Status.prj.getHXList("HXSink")

    procName_k = Status.prj.getProcessList("Process")
    pipeName_m = Status.prj.getPipeList("Pipeduct")
    equipeName_j = Status.prj.getEquipmentList("Equipment")

    print "Connect: sourceName_h",sourceName_h
    print "Connect: sinkName_h",sinkName_h
    print "Connect: procName_k",procName_k
    print "Connect: pipeName_m",pipeName_m
    print "Connect: equipeName_j",equipeName_j
       
    Status.QWHEqLink = arange(NJ*NH).reshape(NJ,NH)  
    Status.QWHPipeLink = arange(NM*NH).reshape(NM,NH)
    Status.QWHProcLink = arange(NK*NH).reshape(NK,NH)

    Status.QHXEqLink = arange(NJ*NH).reshape(NJ,NH)
    Status.QHXPipeLink = arange(NM*NH).reshape(NM,NH)
    Status.QHXProcLink = arange(NK*NH).reshape(NK,NH)
    
    for h in range(NH):
        for j in range(NJ):
            if sourceName_h[h] == equipeName_j[j]:
                Status.QWHEqLink[j][h] = 1
            else:
                Status.QWHEqLink[j][h] = 0
                
            if sinkName_h[h] == equipeName_j[j]:
                Status.QHXEqLink[j][h] = 1
            else:
                Status.QHXEqLink[j][h] = 0
        
        for m in range(NM):
            if sourceName_h[h] == pipeName_m[m]:
                Status.QWHPipeLink[m][h] = 1
            else:
                Status.QWHPipeLink[m][h] = 0
                
            if sinkName_h[h] == pipeName_m[m]:
                Status.QHXPipeLink[m][h] = 1
            else:
                Status.QHXPipeLink[m][h] = 0
        
        for k in range(NK):
            if sourceName_h[h] == procName_k[k]:
                Status.QWHProcLink[k][h] = 1
            else:
                Status.QWHProcLink[k][h] = 0
                
            if sinkName_h[h] == procName_k[k]:
                Status.QHXProcLink[k][h] = 1
            else:
                Status.QHXProcLink[k][h] = 0
        
    print "Connect: QWHEqLink created"
    print Status.QWHEqLink
    print "Connect: QHXEqLink created"
    print Status.QHXEqLink
    print "Connect: QWHPipeLink created"
    print Status.QWHPipeLink
    print "Connect: QHXPipeLink created"
    print Status.QHXPipeLink
    print "Connect: QWHProcLink created"
    print Status.QWHProcLink
    print "Connect: QHXProcLink created"
    print Status.QHXProcLink


#==============================================================================
if __name__ == "__main__":
    
    pass

#==============================================================================
