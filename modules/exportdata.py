#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#============================================================================== 				
#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	EXPORTDATA
#			
#------------------------------------------------------------------------------
#			
#	Short description:
#	
#	Exports/imports parts of the SQL database to XML files
#
#==============================================================================
#
#	Version No.: 0.03
#	Created by: 	    Tom Sobota	    June 2008
#
#       Last modified by:   Hans Schweiger  19/06/2008
#
#       Changes to previous version:
#       19/06/2008: HS  ExportDataHR created based on ExportDataXML
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

import sys
import os
import wx
import MySQLdb
from einstein.GUI.status import Status

def openfilecreate(text,style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT):
    # ask for file for exporting
    dialog = wx.FileDialog(parent=None,
                           message=text,
                           wildcard='XML files (*.xml)|*.xml',
                           style=style)
    if dialog.ShowModal() != wx.ID_OK:
        return None

    return dialog.GetPath()

def openconnection(main):
    try:
        # get a new connection
        conn = main.connectToDB()
    except MySQLdb.Error, e:
        main.showError('Cannot connect to database. '\
                       'Error is:\n\n%s\n\nPlease verify.' % (str(e),))
        return None

    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    return (conn,cursor)



class ImportDataXML(object):
    def __init__(self,parent,infile=None):
        self.parent = parent
        if infile is None:
            infile = openfilecreate('Choose a data file for importing',
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if infile is None:
                return None

        res = openconnection(parent)
        if res is None:
            return None
        (conn, cursor) = res
        self.fd = open(infile, 'r')
        self.fd.close()
        conn.close()

class ExportDataXML(object):
    def __init__(self,parent,pid=None,ano=None,fuels=[],fluids=[],outfile=None):
        self.parent = parent
        if outfile is None:
            outfile = openfilecreate('Output file for exporting tables')
            if outfile is None:
                return None

        res = openconnection(parent)
        if res is None:
            return None
        (conn, cursor) = res
        fd = open(outfile, 'w')
        fd.write('<?xml version="1.0" encoding="utf-8"?>\n' +
                      '<InputXMLDataController xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n')

        if pid is not None and ano is not None:
            criterium = "WHERE Questionnaire_id=%s AND AlternativeProposalNo=%s" % (pid,ano)
            self.dumpTable(cursor, fd, 'qgenerationhc', criterium, 'ORDER BY EqNo')
            self.dumpTable(cursor, fd, 'qprocessdata', criterium, 'ORDER BY ProcNo')
            self.dumpTable(cursor, fd, 'qdistributionhc', criterium,'ORDER BY PipeDuctNo')

            criterium = "WHERE ProjectID=%s AND AlternativeProposalNo=%s" % (pid,ano)
            self.dumpTable(cursor, fd, 'qheatexchanger', criterium,'ORDER BY HXNo')
            self.dumpTable(cursor, fd, 'qwasteheatelequip', criterium,'ORDER BY WHEENo')

        if len(fuels)>0:
            criterium = "WHERE DBFuel_ID IN %s" % (str(fuels),)
            criterium = criterium.replace('[','(').replace(']',')')
            self.dumpTable(cursor, fd, 'dbfuel', criterium)

        if len(fluids)>0:
            criterium = "WHERE DBFluid_ID IN %s" % (str(fluids),)
            criterium = criterium.replace('[','(').replace(']',')')
            self.dumpTable(cursor, fd, 'dbfluid', criterium)
            
        fd.write('</InputXMLDataController>\n')
        fd.close()
        conn.close()

#------------------------------------------------------------------------------		
class ExportDataHR(object):
#------------------------------------------------------------------------------		
#   creates the XML input file for the heat recovery module
#------------------------------------------------------------------------------		
    def __init__(self,pid=None,ano = None, fuels=[],fluids=[]):
        self.parent = Status.main
        
        outfile = "inputHR.xml"
        
        res = openconnection(self.parent)
        if res is None:
            return None
        (conn, cursor) = res
        fd = open(outfile, 'w')
        fd.write('<?xml version="1.0" encoding="utf-8"?>\n' +
                      '<InputXMLDataController xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n')

        if pid is not None:
            criterium = "WHERE Questionnaire_id=%s AND AlternativeProposalNo=%s" % (pid,ano)
            self.dumpTable(cursor, fd, 'qgenerationhc', criterium, 'ORDER BY EqNo')
            self.dumpTable(cursor, fd, 'qprocessdata', criterium, 'ORDER BY ProcNo')
            self.dumpTable(cursor, fd, 'qdistributionhc', criterium,'ORDER BY PipeDuctNo')

            criterium = "WHERE Questionnaire_id=%s AND AlternativeProposalNo=%s" % (pid,ano)
            self.dumpTable(cursor, fd, 'qheatexchanger', criterium,'ORDER BY HXNo')
            self.dumpTable(cursor, fd, 'qwasteheatelequip', criterium,'ORDER BY WHEENo')

        if len(fuels)>0:
            criterium = "WHERE DBFuel_ID IN %s" % (str(fuels),)
            criterium = criterium.replace('[','(').replace(']',')')
            self.dumpTable(cursor, fd, 'dbfuel', criterium)

        if len(fluids)>0:
            criterium = "WHERE DBFluid_ID IN %s" % (str(fluids),)
            criterium = criterium.replace('[','(').replace(']',')')
            self.dumpTable(cursor, fd, 'dbfluid', criterium)
            
        fd.write('</InputXMLDataController>\n')

        fd.write('<Schedules>\n')
        for scheduleList in [Status.schedules.procOpSchedules,
                         Status.schedules.procStartUpSchedules,
                         Status.schedules.procInFlowSchedules,
                         Status.schedules.procOutFlowSchedules,
                         Status.schedules.equipmentSchedules,
                         Status.schedules.WHEESchedules]:
            for schedule in scheduleList:
                pass
#                dumpSchedule(cursor, fd, schedule)
        
        fd.write('</Schedules>\n')

        fd.close()
        conn.close()


    def dumpTable(self, cursor, fd, table, criterium, order=None):
        fieldtypes = {}
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns " \
                        "WHERE table_name = '%s' AND table_schema = 'einstein'" % (table,))
        result_set = cursor.fetchall()
        nfields = cursor.rowcount
        for field in result_set:
            fname = field['column_name']
            ftype = field['data_type']
            fieldtypes[fname] = ftype
    
        sql = "SELECT * FROM %s" % (table,)

        if criterium:
            sql += (' ' + criterium)
        if order:
            sql += (' ' + order)
        cursor.execute(sql)
        result_set = cursor.fetchall()
        nrows = cursor.rowcount
        if nrows <= 0:
            fd.write('<!-- table %s has no values -->\n' % (table,))
        else:
            fd.write('<ListOf%s>\n' % (table,))
            for row in result_set:
                fd.write('<InputXML%s>\n' % (table,))
                for key in row.keys():
                    value = row[key]
                    if value is not None:
                        s = '<%s>%s</%s>\n' % (key,value,key)
                        fd.write(s)
                fd.write('</InputXML%s>\n' % (table,))
            fd.write('</ListOf%s>\n' % (table,))




class ExportDataBaseXML(object):
    #
    # exports whole einstein database in XML format
    #
    def __init__(self,parent,outfile=None):
        self.parent = parent
        if outfile is None:
            outfile = openfilecreate('Output file for exporting database')
            if outfile is None:
                return None
            (conn, outfile) = res

        res = openconnection(parent)
        if res is None:
            return None
        (conn, cursor) = res
            
        fd = open(outfile, 'w')
        fd.write('<?xml version="1.0" encoding="utf-8"?>\n')
        fd.write('<EinsteinDBDump>\n')
        cursor.execute("SELECT DISTINCT table_name from information_schema.columns " \
                        "WHERE table_schema = 'einstein' ORDER BY table_name")
        tables = cursor.fetchall()
        for field in tables:
            tablename = field['table_name']
            self.dumpAllTable(cursor, fd, tablename)

        fd.write('</EinsteinDBDump>\n')
        fd.close()
        conn.close()

    def dumpAllTable(self, cursor, fd, table):
        fieldtypes = {}
        sql = "SELECT column_name, data_type FROM information_schema.columns " \
                        "WHERE table_name = '%s' AND table_schema = 'einstein'" \
                        "ORDER BY column_name" % (table,)
        cursor.execute(sql)
        result_set = cursor.fetchall()
        nfields = cursor.rowcount
        for field in result_set:
            fname = field['column_name']
            ftype = field['data_type']
            fieldtypes[fname] = ftype
    
        cursor.execute("SELECT * FROM %s" % (table,))
        result_set = cursor.fetchall()
        nrows = cursor.rowcount
        fd.write('<table name="%s" rows="%s">\n' % (table,nrows))
        i = 0
        for row in result_set:
            fd.write('<row i="%s" fields="%s">\n' % (i,nfields))
            i += 1
            for key in row.keys():
                fd.write('<field name="%s" type="%s" value="%s" />\n' %\
                         (key, fieldtypes[key],row[key]))
            fd.write('</row>\n')
        fd.write('</table><!-- end of %s -->\n' % (table,))

#A2. Schedules
#Exporta los parámetros tal como están en el __init__: de la estructura "Schedule" (en schedules.py):
#        self.daily = [[(0.0,24.0)]]
#        self.weekly = [(0.0,168.0)]
#        self.monthly = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
#        self.holidays = []
#        self.NDays = 365
#        self.HPerDay = 24.      #operating period for the present schedule
#        self.NBatch = 1
#        self.HBatch = 24.
#        self.ScheduleType = "continuous"
#
#Para las listas de pares de números (start,stop) que pueden ser de longitud variable, tal vez
#convendría poner delante la longitud de la lista (=número de intervalos)
#
#Los schedules tienes en las listas de objetos Schedule que te indiqué en el mail de ayer
#
#   The schedules you get from the following lists:
#
#   The four process schedules for each process (the list index is the proc. number - from 0 to NThProc - 1)
#      self.procOpSchedules = []
#      self.procStartUpSchedules = []
#      self.procInFlowSchedules = []
#      self.procOutFlowSchedules = []
#
#   The equipment schedules (list index = EqNo-1)
#      self.equipmentSchedules = []
#
#   The WHEE schedules (list index = WHEENo - 1)
#      self.WHEESchedules = []
#
#   All can be accessed as "Status.schedules.procOpSchedules", "Status.schedules.equipmentSchedules", etc. ...

class ExportSchedulesXML(object):
    def __init__(self,parent,outfile=None):
        self.parent = parent
        if outfile is None:
            outfile = openfilecreate('Output file for exporting schedules')
            if outfile is None:
                return None
            (conn, outfile) = res

        res = openconnection(parent)
        if res is None:
            return None
        (conn, cursor) = res

        fd = open(outfile, 'w')
        fd.write('<?xml version="1.0" encoding="utf-8"?>\n')
        fd.write('<Schedules>\n')
        for schedule in [Status.schedules.procOpSchedules,
                         Status.schedules.procStartUpSchedules,
                         Status.schedules.procInFlowSchedules,
                         Status.schedules.procOutFlowSchedules]:
            dumpSchedule(cursor, fd, schedule)
        
        dumpSchedule(cursor, fd, Status.schedules.equipmentSchedules, index=Status.schedules.EqNo-1)
        dumpSchedule(cursor, fd, Status.schedules.WHEESchedules, index=Status.schedules.WHEENo - 1)
        fd.write('</Schedules>\n')
        fd.close()
        conn.close()

    def dumpSchedule(self, cursor, fd, schedule, index=None):
        fd.write('<schedule name ="%s" ndaily="%s" nweekly="%s">\n')
        fd.write('<parameters ndays ="%s" hperday="%s" nbatch="%s" hbatch="%s" scheduletype="%s" />\n' % \
                 (schedule.NDays, schedule.HPerDay, schedule.NBatch, schedule.HBatch, schedule.ScheduleType))
        for d in schedule.daily:
            fd.write('<daily index="%s" start="%s" end="%s" />\n' % (d[0],d[1]))
            
        for w in schedule.weekly:
            fd.write('<weekly index="%s" start="%s" end="%s" />\n' % (w[0],w[1]))

        for m in schedule.monthly:
            fd.write('<monthly index="%s" value="%s" />\n' % (m,))

        for h in schedule.holidays:
            fd.write('<holiday index="%s" value="%s" />\n' % (h,))

