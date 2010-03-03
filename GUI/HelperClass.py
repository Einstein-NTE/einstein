#!/usr/bin/env python
# -*- coding: cp1252 -*-

"""
##########################################################################################

EINSTEIN
Expert system for an intelligent supply of thermal energy in industry
www.energyxperts.net

energyXperts.BCN

Ingeniería Termo-energética y Energías Renovables
Thermo-energetical Engineering and Renewable Energies

Dr. Ullés, 2, 3o
08224 Terrassa (Barcelona), Spain


GUI-Modul Version 0.5
2008 by imsai eSoft Heiko Henning
heiko.henning@imsai.de


##########################################################################################
"""


#-----  Imports
import logging
import time
import os
import codecs
from ConfigParser import ConfigParser


#----- Constants
ParameterFile = 'EINSTEIN Parameters 0.4.csv'

LogFile = '..\einsteinTRACK.log'
ConfigFile = 'einstein.ini'



class LogHelper():

    def __init__(self):
        #----- Prepare logging
        global LogFile
        logging.basicConfig(level=logging.INFO, filename=LogFile)


    def LogThis(self, info):
        logging.info('%s - %s' % (time.asctime(), info))





class ParameterDataHelper():

    def __init__(self):
        global ParameterFile        


    def ReadParameterData(self):
        f = codecs.open(ParameterFile, 'r',)
        guidata = {}
        for line in f:
            tmp = line.replace("\n","").replace("\\n","\n").split(';')
            guidata.update({tmp.pop(0): tmp})
        f.close
        return guidata



class ConfigHelper():

    def __init__(self):
        global ConfigFile
        self.config = ConfigParser()
        self.config.read(ConfigFile)


    def get(self, section, setting):
        return self.config.get(section, setting)
