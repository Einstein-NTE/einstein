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
#	Version No.: 0.04
#	Created by: 	    Tom Sobota	    June 2008
#
#       Last modified by:   Hans Schweiger  19/06/2008
#                           Tom Sobota      20/06/2008
#                           Hans Schweiger  23/06/2008
#
#       Changes to previous version:
#       19/06/2008: HS  ExportDataHR created based on ExportDataXML
#       20/06/2008: TS  Compatibility changes: substituted 'information_schema'by 'show tables'
#       23/06/2008: HS  Improvement of ExportDataHR: schedules now exported
#                       - although not yet correctly :-(
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
import xml.dom
import xml.dom.minidom
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

def openconnection():
    frame = wx.GetApp().GetTopWindow()
    conn = frame.connectToDB()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    return (conn,cursor)

def error(text):
    frame = wx.GetApp().GetTopWindow()
    frame.showWarning(text)
    
class ImportDataXML(object):
#=> todos los ID's principales de las tablas importadas se deberían sustituir por
#   las ID's auto-incrementadas de la database receptora.
#
#=> más problemático son los vínculos: hay una forma de actualizar los vínculos entre
#   tablas sustituyendolos por las nuevas ID's ? sino, no te preocupes, entonces esto
#   ya lo hacemos de forma manual (solamente necesitaríamos algun diccionario para cada
#   tabla para poder asociar ID antigua en el original e ID nueva en el database ...)
#
#=> lo más complicado, pero de momento solo ocurre en un único lugar, es actualizar los
#   vínculos de equipments con pipes, ya que un equipment puede dar calor a varios pipes,
#   y eso está resuelto de tal forma de momento, que en la columna del vínculo hay un
#   string "IDPipe1;IDPipe2;IDPipe3 ...". Eso último supongo que no habrá nada estándar
#   para resolverlo ... ¿ o sí ... ?
#
#(no sé si pueden servir, pero yo tengo una función copyProject que hace algo similar,
#que es crear un duplicado de un proyecto DENTRO de la misma database. la problemática
#es idéntica ... y lo de los vínculos todavía por resolver :-) ). Así tal vez podemos
#matar dos pájaros con un tiro ...

    def __init__(self,infile=None):
        if infile is None:
            infile = openfilecreate('Choose a data file for importing',
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if infile is None:
                return None

        (conn, cursor) = openconnection()
        self.document = xml.dom.minidom.parse(infile)

        self.fd.close()
        conn.close()

class ExportDataXML(object):
    def __init__(self,pid=None,ano=None,fuels=[],fluids=[],outfile=None):
        if outfile is None:
            outfile = openfilecreate('Output file for exporting tables')
            if outfile is None:
                return None

        (conn, cursor) = openconnection()
        fd = open(outfile, 'w')
        fd.write('<?xml version="1.0" encoding="utf-8"?>\n' +
                      '<InputXMLDataController>\n')

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

    def dumpTable(self, cursor, fd, table, criterium, order=None):
        fieldtypes = {}
        #cursor.execute("SELECT column_name, data_type FROM information_schema.columns " \
        #                "WHERE table_name = '%s' AND table_schema = 'einstein'" % (table,))
        cursor.execute("SHOW COLUMNS FROM `%s` FROM einstein" % (table,))
        result_set = cursor.fetchall()
        nfields = cursor.rowcount
        for field in result_set:
            fname = field['Field']
            ftype = field['Type']
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

#------------------------------------------------------------------------------		
class ExportDataHR(object):
#------------------------------------------------------------------------------		
#   creates the XML input file for the heat recovery module
#------------------------------------------------------------------------------		
    def __init__(self, pid=None,ano=None, fuels=[],fluids=[]):
        self.parent = Status.main
        
        outfile = "inputHR.xml"
        
        (conn, cursor) = openconnection()
        fd = open(outfile, 'w')
        fd.write('<?xml version="1.0" encoding="utf-8"?>\n' +
                      '<HeatRecovery>\n')

        if pid is not None:
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
            
        fd.write('</HeatRecovery>\n')

        fd.write('<Schedules>\n')
        for scheduleList in [Status.schedules.procOpSchedules,
                         Status.schedules.procStartUpSchedules,
                         Status.schedules.procInFlowSchedules,
                         Status.schedules.procOutFlowSchedules,
                         Status.schedules.equipmentSchedules,
                         Status.schedules.WHEESchedules]:
            for schedule in scheduleList:
                self.dumpSchedule(cursor, fd, schedule)
        
        fd.write('</Schedules>\n')

        fd.close()
        conn.close()


    def dumpTable(self, cursor, fd, table, criterium, order=None):
        fieldtypes = {}
        #cursor.execute("SELECT column_name, data_type FROM information_schema.columns " \
        #                "WHERE table_name = '%s' AND table_schema = 'einstein'" % (table,))
        cursor.execute("SHOW COLUMNS FROM `%s` FROM einstein" % (table,))
        result_set = cursor.fetchall()
        nfields = cursor.rowcount
        for field in result_set:
            fname = field['Field']
            ftype = field['Type']
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

    def dumpSchedule(self, cursor, fd, schedule, index=None):
        fd.write('<schedule name ="%s" nweekly="%s" nholidays="%s"/>\n'%\
                 (schedule.name,len(schedule.weekly),len(schedule.holidays)))
        fd.write('<parameters ndays ="%s" hperday="%s" nbatch="%s" hbatch="%s" scheduletype="%s" />\n' % \
                 (schedule.NDays, schedule.HPerDay, schedule.NBatch, schedule.HBatch, schedule.ScheduleType))
#        for d in schedule.daily:
#            fd.write('<daily index="%s" start="%s" end="%s" />\n' % (d[0],d[1]))
            
        i = 0
        for w in schedule.weekly:
            i+=1
            fd.write('<weekly index="%s" start="%s" end="%s" />\n' % (i,w[0],w[1]))

        for m in schedule.monthly:
            fd.write('<monthly wariation="%s" />\n' % (m,))

        i = 0
        for h in schedule.holidays:
            i+=1
            fd.write('<holiday index="%s" start="%s" end="%s" />\n' % (i,h[0],h[1]))



class ExportDataBaseXML(object):
    #
    # exports whole einstein database in XML format
    #
    def __init__(self,outfile=None):
        if outfile is None:
            outfile = openfilecreate('Output file for exporting database')
            if outfile is None:
                return None

        (conn, cursor) = openconnection()
            
        fd = open(outfile, 'w')
        fd.write('<?xml version="1.0" encoding="utf-8"?>\n')
        fd.write('<EinsteinDBDump>\n')
        cursor.execute("SHOW TABLES FROM einstein")
        tables = cursor.fetchall()
        for field in tables:
            tablename = field['Tables_in_einstein']
            self.dumpAllTable(cursor, fd, tablename)

        fd.write('</EinsteinDBDump>\n')
        fd.close()
        conn.close()

    def dumpAllTable(self, cursor, fd, table):
        fieldtypes = {}
        cursor.execute("SHOW COLUMNS FROM `%s` FROM einstein" % (table,))
        cursor.execute(sql)
        result_set = cursor.fetchall()
        nfields = cursor.rowcount
        for field in result_set:
            fname = field['Field']
            ftype = field['Type']
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

        (conn, cursor) = openconnection()

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
#        for d in schedule.daily:
#            fd.write('<daily index="%s" start="%s" end="%s" />\n' % (d[0],d[1]))
            
        for w in schedule.weekly:
            fd.write('<weekly index="%s" start="%s" end="%s" />\n' % (w[0],w[1]))

        for m in schedule.monthly:
            fd.write('<monthly index="%s" value="%s" />\n' % (m,))

        for h in schedule.holidays:
            fd.write('<holiday index="%s" start="%s" end="%s" />\n' % (h[0],h[1]))



# Aparte de esto necesitaría una función ExportProject, que debería hacer lo mismo que ExportDataBaseXML,
# pero exportar los datos de UN SOLO PROYECTO (pero todos los ANo de este proyecto !!!, o sea
# Query por ProjectID / Questionnaire_id / Questionnaire_ID según tabla.
# Esta función se debería poder activar desde el menu principal -> export project;
#

class ExportProject(object):
    #
    # exports einstein project in XML format
    #
    def __init__(self, pid=None, outfile=None):
        if pid is None:
            error('ExportProject: PId missing')
            return
        if outfile is None:
            outfile = openfilecreate('Output file for exporting project')
            if outfile is None:
                return None

        (conn, cursor) = openconnection()
            
        fd = open(outfile, 'w')
        fd.write('<?xml version="1.0" encoding="utf-8"?>\n')
        fd.write('<EinsteinProject pid="%s">\n' % (pid,))
        cursor.execute("SHOW TABLES FROM einstein")
        tables = cursor.fetchall()
        for field in tables:
            tablename = field['Tables_in_einstein']
            self.dumpProjectTable(cursor, fd, tablename, pid)

        fd.write('</EinsteinProject>\n')
        fd.close()
        conn.close()


    def dumpProjectTable(self, cursor, fd, table, pid):
        fieldtypes = {}
        cursor.execute("SHOW COLUMNS FROM `%s` FROM einstein" % (table,))
        result_set = cursor.fetchall()
        nfields = cursor.rowcount
        criterium = None
        for field in result_set:
            fname = field['Field']
            ftype = field['Type']
            fextra = field['Extra']
            fieldtypes[fname] = (ftype,fextra)
            # find the name of the ID field
            if fname == 'ProjectID' or fname == 'Questionnaire_id' or fname == 'Questionnaire_ID':
                criterium = '%s=%s' % (fname,pid)
        if criterium is None:
            fd.write('<!-- table %s ignored -->\n' % (table,))
            return

        sql = "SELECT * FROM %s WHERE %s" % (table, criterium)
        cursor.execute(sql)
        result_set = cursor.fetchall()
        nrows = cursor.rowcount
        if nrows <= 0:
            fd.write('<!-- table %s has no values for id=%s -->\n' % (table,pid))
        else:
            fd.write('<table name="%s">\n' % (table,))
            nn = 0
            for row in result_set:
                nn += 1
                fd.write('<row n="%s">\n' % (nn,))
                for key in row.keys():
                    value = row[key]
                    if value is not None:
                        type,extra = fieldtypes[key]
                        s = '<element name="%s" type="%s" auto="%s" value="%s" />\n' % (key,type,extra,value)
                        fd.write(s)
                fd.write('</row>\n')
            fd.write('</table>\n')


#Y necesitaría evidentemente también la parte complementaria, el "import project", porque sino el pobre
# ExportProject se siente solo e inutil ...

class ImportProject(object):
    def __init__(self,infile=None):
        self.pid = None
        self.newpid = None

        if infile is None:
            infile = openfilecreate('Choose a project file for importing',
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if infile is None:
                return None

        (conn, cursor) = openconnection()
        #
        # get the highest project number so far in the database, add 1, and assign to the
        # imported project
        cursor.execute('SELECT MAX(Questionnaire_id) AS n FROM cgeneraldata') # must confirm this
        nrows = cursor.rowcount
        if nrows <= 0:
            self.newpid = 1
        else:
            field = cursor.fetchone()
            # new pid for this project
            self.newpid = int(field['n']) + 1

        # create a dom and import in it the xml project file
        self.document = xml.dom.minidom.parse(infile)
        # get the elements from the DOM
        projects = self.document.getElementsByTagName('EinsteinProject')
        for project in projects:
            self.pid = project.getAttribute('pid')
            tables = self.document.getElementsByTagName("table")
            for table in tables:
                tablename =  table.getAttribute('name')
                rows = table.getElementsByTagName("row")
                for row in rows:
                    sqlist = []
                    nrow =  table.getAttribute('n')
                    elements = row.getElementsByTagName("element")
                    for element in elements:
                        fieldname = element.getAttribute('name')
                        eltype = element.getAttribute('type')
                        elauto = element.getAttribute('auto')
                        elvalue = element.getAttribute('value')
                        # substitute new pid in id field
                        if fieldname == 'ProjectID' or \
                             fieldname == 'Questionnaire_id' or \
                             fieldname == 'Questionnaire_ID':
                            elvalue = self.newpid
                        # substitute invalid chars in char fields and enclose in ''
                        if eltype.startswith('char') or eltype.startswith('varchar'):
                            elvalue = "'" + self.subsIllegal(elvalue) + "'"
                        # substitute auto-increment value with NULL
                        if elauto == 'auto_increment':
                            elvalue = 'NULL'

                        sqlist.append("%s=%s" % (fieldname,elvalue))
                    # create sql sentence and update database
                    sql = 'INSERT INTO %s SET ' % (tablename,) + ', '.join(sqlist)
                    #print sql
                    cursor.execute(sql)
        conn.close()

    def subsIllegal(self,text):
        parts = text.split("'")
        newtext = "''".join(parts)
        return newtext


    def getPid(self):
        return (self.pid, self.newpid)

