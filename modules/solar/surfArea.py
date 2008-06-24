# -*- coding: cp1252 -*-
    Roof, Ground, Wall
    NetSurfAreaFactor 
    NetSurfAreaFactorSloped=1.2
    NetSurfAreaFactor=f(latitude)
    MININCLINATION = 20
    MaxInclination = 90
    DistanceFactor
    DistanceConstraint= 1500
    MaxDistance
    MaxDistance
    Latitude 
    SurfArea
    Inclination
    Azimuth
    Shading
    Distance
    RoofType
    RoofStaticLoadCap
    MINSTATICROOF= 25 kg/m2
    EnclBuildGroundSketch
    ShadingLossesFactor = K (10%?)
    TotSurfaceArea
    NetSurfaceArea
    TotNetSurfaceArea
    MinNetSurfArea = 20
    MinTotNetSurfArea = 40

    # NOTES: G(T) should be modified according the shading 

    #Read from the DB the NetSurfAreaFactorGround for the Country/Region
    # Assign constants

#Check latitude: if>70 and >20°data entering error
    #add check and warning

#Check inclination: if>90° data entering error
        
    if InclinationRoof>MaxInclination:
        append warning "Check surface inclination: out of range." 

#Calculate the net area and check if too small
    if Inclination>=MinInclination:
        NetSurfAreaFactor = NetSurfAreaFactorSloped
    else NetSurfAreaFactor = NetSurfAreaFactor[]# depending on the latitude

        NetSurfArea = SurfArea*NetSurfAreaFactor
        if NetSurfArea <MinNetSurfArea:
            delete SurfArea
            append warning "The surface available for the collectors mounting is too small."
        else add SurfArea

#Check the azimuth
    if Azimuth = N or NE or NW:
        if Inclination<MININCLINATION:
            add SurfArea
        else delete SurfArea:
            append warning "Area available oriented to North:not suitable." 
    else add SurfArea


#Check the shading
    if Shading = Yes,full shaded:
        delete SurfArea
        append warning "Area shaded: not suitable for collectors mounting."
    elif not Shading = Yes,partially:
        reduce G(T) by ShadingLossesFactor
        append warnings "Check how much of the available surface is shadowed. It might affect the solar yeld considerably"

#Check distance to technical room or process
    
    if Distance>MaxDistance:
        append warning "Check distance between the solar field and the technical room or process: out of range." 

#Calculate DistanceFactor
    DistanceFactor=(-2*0,0000001*SurfArea^2)+(0,0022*SurfArea)+0,3938
    MaxDistance=SurfAreaRoof/(DistanceFactor*NetSurfAreaFactor)#before assign NetSurfAreaFactor based on the inclination!
    if Distance>DistanceConstraint or Distance>MaxDistance:
        delete SurfArea
        append warning "Distance between the solar field and the technical room or process is too long"
    else add SurfArea

#ROOF (ONLY)
    if RoofStaticLoadCap<MINSTATICROOF:
        delete SurfArea
    elif RoofStaticLoadCap=None and RoofType = Corrugated metal roof or Composite sandwich panels:
        append warning "Check the static load capacity of the roof and the collectors mounting feasibility."
    elif RoofType = Glass roof:
         delete SurfAreaRoof
         append warning "Surface not suitable for collectors mounting."

#Calculate TotSurfaceArea
      #  see algorithm below

#Calculate TotNetSurfaceArea
    for i in range(NSurfaces): 
        NetSurfArea = SurfArea*NetSurfAreaFactor
        TotNetSurfaceArea += NetSurfArea
    if TotNetSurfArea<MinTotNetSurfArea:
        delete TotNetSurfArea
        append warning "The surface available for the collectors mounting is too small."
    
    
#ALGORITHM *********************************************************************

#check of appropriateness of surfaces

def checkStaticRoofCapacity:
    if (staticRoofCapacity > MINSTATICROOF):
        return "SURFACE_OK"
    else:
        return "SURFACE_NOTOK"

def checkSurfaceOrientation:
    if Azimuth in ["N","NE","NW"]:
        if Inclination > MININCLINATION:
            return "SURFACE_OK"
        else:
            return "SURFACE_NOTOK"



def algoritm:

    totalArea = 0
    totalAppropriateArea = 0
    surfaceCheck = []
    for i in range(NSurfaces):

        
        totalArea += surfaceArea
        if checkStaticRoofCapacity() = "SURFACE_OK" and \
            checkSurfaceOrientation() = "SURFACE_OK":
            totalAppropriateArea += surfaceArea
            surfaceCheck[i] = 1
        else:
            surfaceCheck[i] = 0

    print "total roof surface",totalArea
    print "roof surface possible for solar installation",totalAppropriateArea
            


        
   
