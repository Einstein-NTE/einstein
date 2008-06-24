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
#	SUNDAY
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Calculation of solar radiation based on daily mean values
#
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	   Hans Schweiger 	17/06/2008
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
#*  INDICE:
#
#   HDH_KT  Diffuse fraction of daily radiation as a funtion of KT
#
#   HOURS_OF_SUNSHINE
#           Convierte el numero de horas del sol en la radiacion
#           promedia diaria, y regresa adicionalmente KT
#
#   PREP_SUN    Preparacion de los parametros constantes (angulos,sin y
#           cos,...). Calculo de la fraccion difusa
#           H -> Hb,Hd
#
#   SUN_DAILY   = Integral diario de SUN_HOURLY
#           Hb,Hd -> GbT,GdT -|INT|-> HbT,HdT
#
#   SUN_HOURLY  Calculo de datos instantaneos sobre inclinada a partir
#           de promedios diarios sobre horizontal
#           Hb,Hd -|rb,rt|-> Gd,Gb,s -(sun_proj)-> GbT,GdT,sT 
#
#   SUN_INST    Calculo de datos instantaneos sobre la horizontal y 
#           sobre inclinada a partir de GT
#           GT -|SF,Erbs|-> Gd,Gb,s -(sun_proj)-> GbT,GdT,sT
#
#   SUN_PROJ    Projeccion del sol a una superficie inclinada
#           (Gb,Gd,s -|SF|-> GbT,GdT,sT)
#
#   SUN_BOX Projeccion del sol a las 6 caras de una caja rectan-
#           gular
#                                               */
#======================================================================*/
from math import *
from numpy import *
import copy

#* Solar constant, Duffie/Beckman 1981 (DB) p.6 */
Gsc = 1353.0

class Angles():
    lat=0
    coph=0
    siph=0
    decl=0
    cod=0
    sid=0
    azi=0
    cog=0
    sig=0
    incl=0
    cob=0
    sib=0
    hour=0
    cow=0
    siw=0
    sunset=0
    coss=0
    siss=0
    a=0
    b=0

class Intensity():
    t=0
    g=0
    d=0

gonh = Intensity()
#INTENSITY sunbox[3][2];
sunonh = [0.0,0.0,0.0]

#* la direccion Z en Sunday corresponde a DIR/OR en el sistema del usuario */
#int user_coord_dir,user_coord_or;

#double groundref;
#int backshading;


#/* Modelo para el calculo de fraccion difusa a partir de KT */
COLLARES_PEREIRA_RABL = 1
hdh_model = COLLARES_PEREIRA_RABL

#double gon;
#double st_zero;


#* conversion tiempo local - tiempo solar en Espanya:
#
#- corelaciones de Duffie/Beckman 1991, p. 11
#- verano = 0/1 corectura de tiempo de verano / invierno
#- 30 minutos (shift que corresponde al tiempo centroeuropeo en el meridiano
#  zero). referencia: experiencia propia buscando el sur despues de haber per-
#  dido el norte) */  

PI = (acos(-1.))
PI2 = 2.0*PI
NSTEPS = 240            #number of time steps per day
dt  = (86400./NSTEPS)   #time step in [s]
HOUR = 3600.0


def BX(doy):
    return (2.*PI*((doy)-1)/365)

def EX(doy):
    return 229.2*(0.000075 + 0.001868*cos(BX(doy)) \
	- 0.032077*sin(BX(doy)) - 0.014615*cos(2.*BX(doy)) \
	- 0.04089*sin(2.*BX(doy)))

def solar_time_zero(doy,ver,longit):
	return 60*(60 + 60*(ver) - EX(doy) + 4.*(longit))
    
def solar_time(t):
    return (t - st_zero)

#void rot(double *x,int axis,double c,double s)
def rot(x,axis,c,s):

    i1 = (axis+1)%3;
    i2 = (axis+2)%3;

    x1    =  c*x[i1] + s*x[i2];
    x[i2] = -s*x[i1] + c*x[i2];
    x[i1] = x1;

#*======================================================================*/

COLLARES_PEREIRA_RABL = 1


#------------------------------------------------------------------------------		
def hdh_kt(kt):
#------------------------------------------------------------------------------		
#   calculation of diffuse fraction from KT (ratio of total to extraterrestrial)
#------------------------------------------------------------------------------		

    if hdh_model == COLLARES_PEREIRA_RABL:
#* diffuse fraction of daily radiation DB p.74 */

        if (kt<0.17):
            hdh = 0.99
        elif (kt<0.75):
                hdh = 1.188 + kt*(-2.272 + kt*(9.473 + kt*(-21.865 + kt*14.648)))
        elif (kt<0.80):
                hdh = -0.54*kt + 0.632
        else:
                hdh = 0.2
    
    else:
        print "SUNDAY(hdh_kt): Error en HDH_KT"

    return(hdh)

#------------------------------------------------------------------------------		
def prep_sun(deg_lat,deg_incl,deg_azi,day_of_year,sf,h):
#------------------------------------------------------------------------------		
#   Initial calculation for daily radiation
#------------------------------------------------------------------------------		
#   datos de entrada:
#
#   DEG_LAT     latitud geografica en grados (Norte = positivo)
#   DEG_AZI     azimuth de la superficie en grados (Oeste = positivo)
#   DEG_INCL    inclinacion de la superficie
#   DAY_OF_YEAR numero del dia del anyo
#   H.T         Radiacion promedia diaria sobre sup. horizontal (en J/m2)
#
#
#   DATOS DE SALIDA
#   SF      Estructura de angulos en radianes con cos y sin
#   H       Vector de Intensidades [in J/m2]
#
#------------------------------------------------------------------------------		

    backshading = 0
    hdh_model = 1

    sf.lat  = deg_lat*PI/180.
    sf.incl = deg_incl*PI/180.
    sf.azi  = deg_azi*PI/180.

#* extraterrestial radiation (DB p.7) */

    gon = Gsc*(1+0.033*cos(PI2*day_of_year/365))

#ifdef print_imrs
    print "PREP_SUN: GON = %10.4f\n"%gon
#endif

#* declination DB p. 11 */

    sf.decl = (23.45*PI/180.)*sin(PI2*(284 + day_of_year)/365.)

    sf.cod = cos(sf.decl)
    sf.sid = sin(sf.decl)

#ifdef print_imrs 
    print "PREP_SUN: DECL = %10.4f %10.4f %10.4f\n"%\
        (sf.decl*180./PI,sf.cod,sf.sid)
#endif

    sf.cob = cos(sf.incl)
    sf.sib = sin(sf.incl)

    sf.cog = cos(sf.azi)
    sf.sig = sin(sf.azi)

    sf.coph = cos(sf.lat)
    sf.siph = sin(sf.lat)

#ifdef print_imrs
    print "PREP_SUN: LAT = %10.4f %10.4f %10.4f\n"%\
        (sf.lat*180./PI,sf.coph,sf.siph)
#endif

#* sunset hour angle */

    sf.sunset = acos(-sf.siph*sf.sid/(sf.coph*sf.cod))

    sf.coss = cos(sf.sunset)
    sf.siss = sin(sf.sunset)

#ifdef print_imrs 
    print "PREP_SUN: SUNSET = %10.4f %10.4f %10.4f\n"%\
        (sf.sunset*180./PI,sf.coss,sf.siss)
#endif

#* extraterrestial radiation on horizontal surface (DB p.22) */

#ifdef print_imrs 
    print "PREP_SUN: CCS = %10.4f, WSS = %10.4f\n"%\
        (sf.coph*sf.cod*sf.siss,sf.sunset*sf.siph*sf.sid)
#endif

    ho = (86400./PI)*gon*(sf.coph*sf.cod*sf.siss + sf.sunset*sf.siph*sf.sid)

#ifdef print_imrs 
    print "PREP_SUN: Ho = %10.4f\n"%ho
#endif
    kt = h.t/ho

#ifdef print_imrs 
    print "PREP_SUN: KT = %10.4f\n"%kt
#endif

    h.d = hdh_kt(kt)*(h.t)
    h.b = h.t - h.d

#ifdef print_imrs 
    print "PREP_SUN: Ht,d,b %10.4f %10.4f %10.4f\n"%\
        (h.t,h.d,h.b)
#endif

#* hourly radiation DB pp.79/80 */

    sf.a = 0.409 + 0.5016 * sin(sf.sunset-(PI/3.))
    sf.b = 0.6609 - 0.4767* sin(sf.sunset-(PI/3.))

    rtsum = 0
    rdsum = 0

    for k in range(NSTEPS):
        
        t = (0.5 + k) * dt
        sf.hour = (PI2*(1.*((int(t))%86400))/86400) - PI
        if (fabs(sf.hour)<sf.sunset):
            sf.cow = cos(sf.hour)
            sf.siw = sin(sf.hour)

            rd = (PI/24.)*(sf.cow-sf.coss)/(sf.siss - sf.sunset*sf.coss)

            rt = (sf.a+sf.b*sf.cow)*rd

            rdsum += rd*dt/HOUR
            rtsum += rt*dt/HOUR

    sf.a /= rtsum
    sf.b /= rtsum

#ifdef print_imrs 
    print "PREP_SUN: a,b %10.4f %10.4f\n"%\
        (sf.a,sf.b)
#endif

#------------------------------------------------------------------------------		
def sun_hourly(sf,h,t,i,sun):
#------------------------------------------------------------------------------		
#   SUN_HOURLY  Calculo de datos instantaneos sobre inclinada a partir
#           de promedios diarios sobre horizontal
#           Hb,Hd -|rb,rt|-> Gd,Gb,s -(sun_proj)-> GbT,GdT,sT 
#------------------------------------------------------------------------------		
#*  datos de entrada:
#
#   (Estructura DAY)
#
#   SF  Vector de angulos
#   HT  Radiacion total diaria (superficie horizontal)
#   HD  Radiacion difusa diaria (superficie horizontal)
#   T   Tiempo [s]
#
#   DATOS DE SALIDA:
#
#   IT  Radiacion total sobre superficie inclinada
#   IBT Radiacion directa sobre superficie inclinada
#   IDT Radiacion difusa sobre superficie inclinada
#   SUN Vector de la direccion del sol
#                                               */
#------------------------------------------------------------------------------		

    sf.hour = (PI2*(1.*((int(t))%86400))/86400) - PI

    if (fabs(sf.hour)>=sf.sunset):
        gonh.b=0
        gonh.d=0
        gonh.t=0
        i.b = 0
        i.d = 0;
        i.t = 0;
        sun = [0,0,-1]
        return

    else:

        sf.cow = cos(sf.hour)
        sf.siw = sin(sf.hour)

        rd = (PI/24.)*(sf.cow-sf.coss)/(sf.siss - sf.sunset*sf.coss)

        rt = (sf.a+sf.b*sf.cow)*rd

#ifdef print_imrs
        print "rd: %10.4e rt: %10.4e\n"%(rd,rt)
#endif
#* conversion J/h -> W */

        it = h.t*rt/3600
        id = h.d*rd/3600

#ifdef print_imrs
        print "SUNDAY: I = %10.4g Id = %10.4g time after sunrise = %8.2f\n"%\
            (it,id,(12./PI)*(sf.cow-sf.coss))
#endif

        if (id<=it):

            ib = it - id

        else:

    #ifdef print_imrs
            print "SUNDAY: warning I = %10.4g<Id = %10.4g time after sunrise = %8.2f\n"%\
                (it,id,(12./PI)*(sf.cow-sf.coss))
    #endif

            id = it
            ib = 0

#* almacenar los datos obtenidos en el 'sol global' */

        gonh.t = it
        gonh.d = id
        gonh.b = ib

#* fixed slope surface (Rb) */

    sunonh = [0,0,1]    #sun in zenith
    rot(sunonh,0,sf.cod,sf.sid) 
    rot(sunonh,1,sf.cow,sf.siw)
    rot(sunonh,0,sf.coph,-sf.siph)

    sun_proj(sf,sun,i)



#------------------------------------------------------------------------------		
def sun_proj(sf,sun,g):
#------------------------------------------------------------------------------		
#   SUN_PROJ    Projeccion del sol a una superficie inclinada
#           (Gb,Gd,s -|SF|-> GbT,GdT,sT)
#------------------------------------------------------------------------------		
#*  datos de entrada:
#
#   (Estructura DAY)
#
#   SF  Vector de angulos
#
#   DATOS DE SALIDA:
#
#   GBT Radiacion directa sobre superficie inclinada
#   GDT Radiacion difusa sobre superficie inclinada
#   SUN Vector de la direccion del sol
#                                               */
#*======================================================================*/

#{
#double rt,rd,Rb;
#double gg,go,fd,fdant,dif;
#double costheta,costhetaz;
#int i,k;


#  SETV(sun,sunonh,3);
    sun = copy.deepcopy(sunonh)
    costhetaz = sun[2]

    if (costhetaz<=0):
        g.t = 0.
        g.b = 0.
        g.d = 0.
        return

    rot(sun,2,sf.cog,-sf.sig)
    rot(sun,0,sf.cob,sf.sib)

    costheta = sun[2]

    if (costheta<=0):
        Rb = 0
    else:
        Rb = costheta/costhetaz

# radiation on inclined surface */

    g.b = gonh.b*Rb;
    if (backshading and (costheta<=0)):
        g.d = gonh.d*(1.+sf.cob)/2. + gonh.d*groundref*(1.-sf.cob)/2.
    else:
        g.d = gonh.d*(1.+sf.cob)/2. + gonh.t*groundref*(1.-sf.cob)/2.
    g.t = g.b + g.d



#*======================================================================*/

if __name__ == "__main__":

    radiacion = 10.
    MEGA = 1.e+6
    sunOnH = Intensity()
    sunOnT = Intensity()
    sunAnglesOnSurface = Angles()
    dirSunOnT = [0.0,0.0,0.0]

    Latitude = 41.4
    Inclination = 30
    Azimuth = 15.0
    dia = 90
    
    sunh.t=radiacion*MEGA
    groundref = 0.2
    prep_sun(latitud,inclinacion,azimuth,dia,sunAnglesOnSurface,sunOnH)

    for k in range(NSTEPS):
        t = dt*k
        sun_hourly(sunAnglesOnSurface,sunOnH,t,sunOnT,dirSunOnT)
