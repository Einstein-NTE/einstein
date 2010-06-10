# -*- coding: iso-8859-15 -*-
#==============================================================================
#
#    E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (<a href="http://www.iee-einstein.org/" target="_blank">www.iee-einstein.org</a>)
#
#------------------------------------------------------------------------------
#
#    spreadsheetIO: provides function for parsing excel or open office spreadsheets
#
#==============================================================================
#
#   EINSTEIN Version No.: 1.0
#   Created by:     André Rattinger 29/03/2010
#
#------------------------------------------------------------------------------
#    (C) copyleft energyXperts.BCN (E4-Experts SL), Barcelona, Spain 2008
#    http://www.energyxperts.net/
#
#    This program is free software: you can redistribute it or modify it under
#    the terms of the GNU general public license as published by the Free
#    Software Foundation (www.gnu.org).
#
#==============================================================================


from xmlIO import *
from parseExcel import *
from parseOO import *

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)


class ImportQ(object):
#Import Dialog for questionnaires    
    def __init__(self):#,mode="ignore",infile=None):
        

        self.infile = openfilecreate('Choose a questionnaire file for importing',
                                     'Spreadsheet files (*.xls,*.odt)|*.xls;*.ods|\
                                     Excel files (*.xls)|*.xls|\
                                     Open Office calc files (*.ods)|*.ods',
                                     style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if self.infile is None:
            return None       
        
        frame = wx.GetApp().GetTopWindow()
        if self.infile.endswith('xls'):
            pe = parseExcel(self.infile,frame.DBUser,frame.DBPass)
            wx.MessageBox(pe.parse(), 'Info')
        elif self.infile.endswith('ods'):
            pe = parseOO(self.infile,frame.DBUser,frame.DBPass)
            wx.MessageBox(pe.parse(), 'Info')
        else:
            wx.MessageBox('File corrupted', 'Info')
        
         
        #conn.close()
        