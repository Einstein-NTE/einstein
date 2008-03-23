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
import wx



class wxFrame(wx.Frame):
    def _init_ctrls(self, prnt):
        
        wx.Frame.__init__(self, id=-1, name='', parent=prnt, 
              pos=wx.Point(0, 0), size=wx.Size(600, 600),
              style=wx.DEFAULT_FRAME_STYLE, title='Preferences')
        



    def __init__(self, parent):
        self._init_ctrls(parent)



