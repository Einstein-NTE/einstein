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

def _U(text):
    try:
        return unicode(_(text),"utf-8")
    except:
        return _(text)


class ImportQ(object):
#Import Dialog for questionnaires    
    def __init__(self):#,mode="ignore",infile=None):
        

        self.infile = openfilecreate('Choose a questionnaire file for importing','Excel files (*.xls)|*.xls',
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if self.infile is None:
            return None       
        frame = wx.GetApp().GetTopWindow() 
        pe = parseExcel(self.infile,frame.DBUser,frame.DBPass)
        
        wx.MessageBox(pe.parse(), 'Info')

        
        #pe.printQ1() 
        #wx.MessageBox(frame.DBName,'Info')
        """
        if infile is None:
            infile = openfilecreate('Choose a questionnarie file for importing','Excel files (*.xls)|*.xls',
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if infile is None:
                return None
        
        #(conn, cursor) = openconnection()

        
        dialog =  DialogImport(None,_U("import data"),\
                               _U("This will modify your databases\nIf You are sure, specify what to do with duplicate data")+\
                               _U("\nElse press CANCEL"))
        ret = dialog.ShowModal()
        if ret == wx.ID_OK:
            mode = "overwrite"
        elif ret == wx.ID_IGNORE:
            mode = "ignore"
        else:
            return
        """
        #conn.close()