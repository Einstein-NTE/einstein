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
#	Version No.: 0.04
#	Created by: 	    Hans Schweiger	13/06/2008
#	Last revised by:
#                           Hans Schweiger      21/07/2008
#                           Hans Schweiger      01/10/2008
#                           Hans Schweiger      07/10/2008
#                    
#
#       Changes in last update:
#
#       21/07/2008: HS  Split-up of FETLink into FETFuelLink and FETelLink
#       01/10/2008: HS  Error messages when equipments or processes are not connected
#       07/10/2008: HS  FluidID of source and sink in HX's checked and stored
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
from einstein.modules.messageLogger import *
from einstein.GUI.GUITools import check

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
    NN = Status.NWHEE

#..............................................................................
# 1. FETi-FETj-Link: fuels used in equipment

    fuelIDs_i = Status.prj.getFuelList("DBFuel_id")
    
    fuelIDs_j = Status.prj.getEquipmentList("DBFuel_id")

#    print "Connect: fuelIDs_i",fuelIDs_i
#    print "Connect: fuelIDs_j",fuelIDs_j
   

    Status.FETFuelLink = arange((NI-1)*NJ).reshape(NJ,(NI-1))  # reshape(rows,cols)
    Status.FETelLink = arange(1*NJ).reshape(NJ,1)  # reshape(rows,cols)
    
    check_j = []
    check_i = []
    for i in range(NI-1):
        check_i.append(0)
        
    for j in range(NJ):
        check_j.append(0)
        
        for i in range(NI-1):
            if fuelIDs_i[i] == fuelIDs_j[j]:
                Status.FETFuelLink[j][i] = 1
                check_j[j] = 1
                check_i[i] = 1
            else:
                Status.FETFuelLink[j][i] = 0
        Status.FETelLink[j][0] = 1  #all equipments potentially consume something of (parasitic) electricity.

#    print "Connect: FETLink created"
#    print Status.FETFuelLink
#    print Status.FETelLink
    for j in range(NJ):
        if check_j[j] == 0 and fuelIDs_j[j] is not None:
            showError(_("Fuel used in equipment no. %s is not specified or is not in fuel list")%(j+1))
        
#..............................................................................
# 2. USHj-USHm-Link: conecction equipment to pipe

    pipes_j = Status.prj.getEqList("PipeDuctEquip")
        
    pipeID_m = Status.prj.getPipeList("QDistributionHC_ID")

#    print "Connect: pipes_j",pipes_j
#    print "Connect: pipeID_m",pipeID_m
       
    Status.USHLink = arange(NJ*NM).reshape(NM,NJ)  # reshape(rows,cols)

    check_j = []
    for j in range(NJ):
        check_j.append(0)

    for m in range(NM):        
        for j in range(NJ):
            pipeIDs_j = []
            if pipes_j[j] is not None:
                pipesSplit = pipes_j[j].split(';')
                for i in range(len(pipesSplit)):
                    try:
                        pipeIDs_j.append(long(pipesSplit[i]))
                    except:
                        logDebug("Connect: erroneous value in pipe-string [%s][%s]"%\
                                 (pipesSplit[i],pipes_j[j]))
#                print "Connect: pipeIDs_j[%s]"%j,pipeIDs_j
                
            if pipeID_m[m] in pipeIDs_j:
                Status.USHLink[m][j] = 1
                check_j[j] = 1
            else:
                Status.USHLink[m][j] = 0
        
#    print "Connect: USHLink created"
#    print Status.USHLink
    for j in range(NJ):
        if check_j[j] == 0:
            showError(_("Equipment no. %s is not connected to any pipe")%(j+1))

#..............................................................................
# 3. UPHm-UPHk Link: conecction pipe to process

    check_k = []

    pipeName_k = Status.prj.getProcessList("PipeDuctProc")    
    pipeName_m = Status.prj.getPipeList("Pipeduct")

#    print "Connect: pipeName_k",pipeName_k
#    print "Connect: pipeName_m",pipeName_m
       
    Status.UPHLink = arange(NM*NK).reshape(NK,NM)  # reshape(rows,cols)

    for k in range(NK):
        check_k.append(0)
        for m in range(NM):
            if pipeName_m[m] == pipeName_k[k]:
                Status.UPHLink[k][m] = 1
                check_k[k] = 1
            else:
                Status.UPHLink[k][m] = 0
        
#    print "Connect: UPHLink created"
#    print Status.UPHLink

#..............................................................................
# 4. QHX/QWH - Eq/Pipe/Proc Links

    sourceName_h = Status.prj.getHXList("HXSource")    
    sinkName_h = Status.prj.getHXList("HXSink")

    procName_k = Status.prj.getProcessList("Process")
    pipeName_m = Status.prj.getPipeList("Pipeduct")
    equipeName_j = Status.prj.getEquipmentList("Equipment")
    wheeName_n = Status.prj.getWHEEList("WHEEName")

#    print "Connect: sourceName_h",sourceName_h
#    print "Connect: sinkName_h",sinkName_h
#    print "Connect: procName_k",procName_k
#    print "Connect: pipeName_m",pipeName_m
#    print "Connect: equipeName_j",equipeName_j
#    print "Connect: wheeName_n",wheeName_n
       
    Status.QWHEqLink = arange(NJ*NH).reshape(NJ,NH)  
    Status.QWHPipeLink = arange(NM*NH).reshape(NM,NH)
    Status.QWHProcLink = arange(NK*NH).reshape(NK,NH)
    Status.QWHEELink = arange(NN*NH).reshape(NN,NH)

    Status.QHXEqLink = arange(NJ*NH).reshape(NJ,NH)
    Status.QHXPipeLink = arange(NM*NH).reshape(NM,NH)
    Status.QHXProcLink = arange(NK*NH).reshape(NK,NH)
    
    for h in range(NH):
        sourceFluidID = None
        sinkFluidID = None
        
        for j in range(NJ):
            if sourceName_h[h] == equipeName_j[j]:
                Status.QWHEqLink[j][h] = 1
                sourceFluidID = None
            else:
                Status.QWHEqLink[j][h] = 0
                
            if sinkName_h[h] == equipeName_j[j]:
                Status.QHXEqLink[j][h] = 1
                sinkFluidID = None
            else:
                Status.QHXEqLink[j][h] = 0
        
        for m in range(NM):
            if sourceName_h[h] == pipeName_m[m]:
                Status.QWHPipeLink[m][h] = 1

                pipes = Status.DB.qdistributionhc.\
                        Questionnaire_id[Status.PId].\
                        AlternativeProposalNo[Status.ANo].\
                        Pipeduct[sourceName_h[h]]
                if len(pipes) > 0:
                    sourceFluidID = pipes[0].HeatDistMedium

            else:
                Status.QWHPipeLink[m][h] = 0
                
            if sinkName_h[h] == pipeName_m[m]:
                Status.QHXPipeLink[m][h] = 1

                pipes = Status.DB.qdistributionhc.\
                        Questionnaire_id[Status.PId].\
                        AlternativeProposalNo[Status.ANo].\
                        Pipeduct[sinkName_h[h]]
                if len(pipes) > 0:
                    sinkFluidID = pipes[0].HeatDistMedium

            else:
                Status.QHXPipeLink[m][h] = 0
        
        for k in range(NK):
            if sourceName_h[h] == procName_k[k]:
                Status.QWHProcLink[k][h] = 1

                processes = Status.DB.qprocessdata.\
                        Questionnaire_id[Status.PId].\
                        AlternativeProposalNo[Status.ANo].\
                        Process[sourceName_h[h]]
                if len(processes) > 0:
                    sourceFluidID = processes[0].ProcMedOut

            else:
                Status.QWHProcLink[k][h] = 0
                
            if sinkName_h[h] == procName_k[k]:
                Status.QHXProcLink[k][h] = 1
                check_k[k] = 1

                processes = Status.DB.qprocessdata.\
                        Questionnaire_id[Status.PId].\
                        AlternativeProposalNo[Status.ANo].\
                        Process[sinkName_h[h]]
                if len(processes) > 0:
                    sinkFluidID = processes[0].SupplyMedDBFluid_id
            else:
                Status.QHXProcLink[k][h] = 0
        
        for n in range(NN):                         #WHEE can only be source, not sink !!!
            if sourceName_h[h] == wheeName_n[n]:
                Status.QWHEELink[n][h] = 1

                whees = Status.DB.qwasteheatelequip.\
                        ProjectID[Status.PId].\
                        AlternativeProposalNo[Status.ANo].\
                        WHEEName[sourceName_h[h]]
                if len(whees) > 0:
                    sourceFluidID = whees[0].WHEEMedium
            else:
                Status.QWHEELink[n][h] = 0


        hxes = Status.DB.qheatexchanger.\
                        ProjectID[Status.PId].\
                        AlternativeProposalNo[Status.ANo].\
                        HXNo[h+1]
        if len(hxes) > 0:
            hxes[0].FluidIDSource = check(sourceFluidID)
            hxes[0].FluidIDSink = check(sinkFluidID)

    Status.SQL.commit()
    
#    print "Connect: QWHEqLink created"
#    print Status.QWHEqLink
#    print "Connect: QHXEqLink created"
#    print Status.QHXEqLink
#    print "Connect: QWHPipeLink created"
#    print Status.QWHPipeLink
#    print "Connect: QHXPipeLink created"
#    print Status.QHXPipeLink
#    print "Connect: QWHProcLink created"
#    print Status.QWHProcLink
#    print "Connect: QHXProcLink created"
#    print Status.QHXProcLink
#    print "Connect: QWHEELink created"
#    print Status.QWHEELink

    for k in range(NK):
        if check_k[k] == 0:
            showError(_("No heat supply (pipe or heat exchanger) connected to process no. %s")%(k+1))


#==============================================================================
if __name__ == "__main__":
    
    pass

#==============================================================================
