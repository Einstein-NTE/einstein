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
#                           Tom Sobota      July 2008
#                           Hans Schweiger  14/07/2008
#                           Hans Schweiger  26/09/2008
#
#       Changes to previous version:
#       19/06/2008: HS  ExportDataHR created based on ExportDataXML
#       20/06/2008: TS  Compatibility changes: substituted 'information_schema'by 'show tables'
#       23/06/2008: HS  Improvement of ExportDataHR: schedules now exported
#                       - although not yet correctly :-(
#       14/07/2008: HS  Call to "RestoreLinks" added in importProject
#       26/09/2008: HS  Import/Export DB introduced
#                       Import/Export of fluids, fuels and auditorDB in ex/im-project
#                       Workaround in ImportProject for determination of
#                       auto-increment value in questionnaire
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
from messageLogger import *
from einstein.GUI.dialogImport import DialogImport

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
        fd.write('</HeatRecovery>\n')

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
            fd.write('<monthly variation="%s" />\n' % (m,))

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

#------------------------------------------------------------------------------
class ExportProject(object):
#------------------------------------------------------------------------------
#
# exports einstein project in XML format, including the selected information
# required from the databases
#
#------------------------------------------------------------------------------
    def __init__(self, pid=None, outfile=None):
        if pid is None:
            error('ExportProject: PId missing')
            return

#..............................................................................
# creates a list of ID's of fluids of fuels that are used in the project

        (fluidIDs,fuelIDs) = Status.prj.getFluidAndFuelList(pid)
        auditorID = Status.prj.getAuditorID()

#..............................................................................
#..............................................................................
# TOM TOM TOM
#
#   The corresponding rows of the tables dbfluid and dbfuel should be exported !!!
#   Idem: the ONE row of the auditorID corresponding to the current auditor
#   should be exported, too
#..............................................................................
#..............................................................................

        self.DBName = Status.main.conf.get('DB', 'DBName')
        print "DBName = ",self.DBName

        if outfile is None:
            outfile = openfilecreate('Output file for exporting project')
            if outfile is None:
                return None

        (conn, cursor) = openconnection()
            
        fd = open(outfile, 'w')
        fd.write('<?xml version="1.0" encoding="utf-8"?>\n')
        fd.write('<EinsteinProject pid="%s">\n' % (pid,))
        cursor.execute("SHOW TABLES FROM %s"%self.DBName)
        tables = cursor.fetchall()
        for field in tables:
            tablename = field['Tables_in_%s'%self.DBName]
            self.dumpProjectTable(cursor, fd, tablename, pid)

        if len(fuelIDs)>0:
            criterium = "WHERE DBFuel_ID IN %s" % (str(fuelIDs),)
            criterium = criterium.replace('[','(').replace(']',')')
            self.dumpTable(cursor, fd, 'dbfuel', criterium)

        if len(fluidIDs)>0:
            criterium = "WHERE DBFluid_ID IN %s" % (str(fluidIDs),)
            criterium = criterium.replace('[','(').replace(']',')')
            self.dumpTable(cursor, fd, 'dbfluid', criterium)

        if auditorID is not None:
            criterium = "WHERE Auditor_ID='%s'" % (str(auditorID))
            self.dumpTable(cursor, fd, 'auditor', criterium)

        fd.write('</EinsteinProject>\n')
        fd.close()
        conn.close()


    def dumpProjectTable(self, cursor, fd, table, pid):
        fieldtypes = {}
        cursor.execute("SHOW COLUMNS FROM `%s` FROM %s" % (table,self.DBName))
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

    def dumpTable(self, cursor, fd, table, criterium, order=None):
        fieldtypes = {}
        #cursor.execute("SELECT column_name, data_type FROM information_schema.columns " \
        #                "WHERE table_name = '%s' AND table_schema = 'einstein'" % (table,))
        cursor.execute("SHOW COLUMNS FROM `%s` FROM %s" % (table,self.DBName))
        result_set = cursor.fetchall()
        nfields = cursor.rowcount
        for field in result_set:
            fname = field['Field']
            ftype = field['Type']
            fextra = field['Extra']
            fieldtypes[fname] = (ftype,fextra)
    
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
            fd.write('<table name="%s">\n' % (table,))
            nn = 0
            for row in result_set:
                nn+=1
                fd.write('<row n="%s">\n' % (nn,))
                for key in row.keys():
                    value = row[key]
                    if value is not None:
                        type,extra = fieldtypes[key]
                        s = '<element name="%s" type="%s" auto="%s" value="%s" />\n' % (key,type,extra,value)
#                        s = '<%s>%s</%s>\n' % (key,value,key)
                        fd.write(s)
                fd.write('</row>\n')
            fd.write('</table>\n')

#------------------------------------------------------------------------------
class ImportProject(object):
#------------------------------------------------------------------------------
#   complement to ExportProject: imports data from another project
#------------------------------------------------------------------------------
#
#oldKey: es el PRIMARY KEY de la tabla en el file.xml
#       (p.ej. tabla qdistributionhc -> oldKey = valor de QDistributionHC_ID)
#newKey: es el PRIMARY KEY de la misma tabla, una vez importada y colocada en la SQL
#       (allá se hace un auto-increment del QDistributionHC_ID).
#
#
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

#NOTE: a dummy row is added and later on deleted in order to obtain the auto-increment
# status of the table. there should be a more elegant way to to this ...
# => to be changed in the future ...

        dummyID = Status.DB.questionnaire.insert({"Name":"dummy"})
        cursor.execute('SELECT MAX(Questionnaire_id) AS n FROM questionnaire')

        nrows = cursor.rowcount
        if nrows <= 0:
            self.newpid = 1
        else:
            field = cursor.fetchone()
            # new pid for this project
            self.newpid = int(field['n']) + 1

        dummyRows = Status.DB.questionnaire.Questionnaire_ID[dummyID]
        if len(dummyRows) > 0:
            dummyRows[0].delete()

        # create a dom and import in it the xml project file
        self.document = xml.dom.minidom.parse(infile)
        # get the elements from the DOM
        self.projectdict = {}
        projects = self.document.getElementsByTagName('EinsteinProject')
        for project in projects:
            self.pid = project.getAttribute('pid')
            tables = project.getElementsByTagName("table")
            tabledict = {}
            for table in tables:
                tablename =  table.getAttribute('name')
                tablelist = []
                rows = table.getElementsByTagName("row")
                for row in rows:
                    sqlist = []
                    nrow =  row.getAttribute('n')
                    elements = row.getElementsByTagName("element")

                    rowName = None #characteristic name of the row
                    
                    for element in elements:
                        fieldname = element.getAttribute('name').lower()
                        eltype = element.getAttribute('type')
                        elauto = element.getAttribute('auto')
                        elvalue = element.getAttribute('value')

                        if tablename == "questionnaire" and fieldname == "name":
                            rowName = elvalue
                            existingRows = Status.DB.questionnaire.Name[rowName]
                            if len(existingRows) > 0:
                                showWarning(_("Project with name %s already exists in database\nProject renamed to: IMPORTED PROJECT")%rowName)
                                elvalue = 'IMPORTED PROJECT'
                        elif tablename == "dbfluid" and fieldname == "fluidname":
                            rowName = elvalue
                        elif tablename == "dbfuel" and fieldname == "fuelname":
                            rowName = elvalue
                        elif tablename == "auditor" and fieldname == "name":
                            rowName = elvalue

                        # substitute new pid in id field
                        if fieldname == 'projectid' or \
                             fieldname == 'questionnaire_id':
                            elvalue = self.newpid
                        # substitute invalid chars in char fields and enclose in ''
                        if eltype.startswith('char') or eltype.startswith('varchar'):
                            elvalue = "'" + self.subsIllegal(elvalue) + "'"
                        # substitute auto-increment value with NULL
                        if elauto == 'auto_increment':
                            # main key field
                            oldKey = int(elvalue)
                            elvalue = 'NULL'

                        sqlist.append("%s=%s" % (fieldname,elvalue))

#......................................................................
# before inserting new entry, check if entry with the same name exists
# (only for questionnaire, dbfluid, dbfuel

                    ignoreRow = False
                    if tablename == "dbfluid":
                        existingRows = Status.DB.dbfluid.FluidName[rowName]
                        if len(existingRows) > 0:
                            showWarning(_("Fluid %s already in database. Data from imported file will be ignored")%rowName)
                            ignoreRow = True
                            newID = existingRows[0].DBFluid_ID

                    elif tablename == "dbfuel":
                        existingRows = Status.DB.dbfuel.FuelName[rowName]
                        if len(existingRows) > 0:
                            showWarning(_("Fuel %s already in database. Data from imported file will be ignored")%rowName)
                            ignoreRow = True
                            newID = existingRows[0].DBFuel_ID
                    elif tablename == "auditor":
                        existingRows = Status.DB.auditor.Name[rowName]
                        if len(existingRows) > 0:
                            showWarning(_("Auditor %s already in database. Data from imported file will be ignored")%rowName)
                            ignoreRow = True
                            newID = existingRows[0].Auditor_ID
                    else:
                        existingRows = []
                                             
                    if ignoreRow == False:
                        # create sql sentence and update database
                        sql = 'INSERT INTO %s SET ' % (tablename,) + ', '.join(sqlist)
                        cursor.execute(sql)
                        # get last inserted
                        cursor.execute('SELECT LAST_INSERT_ID() AS last')
                        field = cursor.fetchone()
                        newKey = int(field['last'])
                    else:
                        newKey = newID
                    tablelist.append((oldKey,newKey))
                tabledict[tablename] = tablelist
            self.projectdict[self.pid] = tabledict
        conn.close()

#####HS2008-07-14: here restoring links added

        for PId in self.projectdict.keys():
            Status.prj.restoreLinks(self.newpid,self.projectdict[PId])
        

    def subsIllegal(self,text):
        parts = text.split("'")
        newtext = "''".join(parts)
        return newtext


    def getPid(self):
        # returns the pid as stored in the xml file,
        # and the new pid generated when stored in the database.
        return (self.pid, self.newpid)

    def getDict(self):
        # returns the id correspondence dictionary, which has the form:
        #{pid_1:
        # {table_1:
        #  [(oldkey_row_0, newkey_row_0), (oldkey_row_1, newkey_row_1), ... ]
        # {table_2:
        #  [(oldkey_row_0, newkey_row_0), (oldkey_row_1, newkey_row_1), ... ]
        #  .
        #  .
        #  .
        #  },
        #  pid_2:
        #  ...
        # }
        # that is:
        # 1. A dictionary of projects. There can be more than one project
        #    in the xml file.
        #    The key is the pid
        #    The value is:
        # 2.   A dictionary of tablenames.
        #      The key is the table name
        #      The value is a list of tuples, one for each row, containing:
        #      (old key, new key)
        #      for the principal key of the row (in general called 'tablename_id')
        #        The old key is the value contained in the xml file.
        #        The new key is the value autogenerated when the row has been stored.
        #
        return self.projectdict

#------------------------------------------------------------------------------
class ExportDB(object):
#------------------------------------------------------------------------------
#
# exports einstein databases
#
#------------------------------------------------------------------------------
    def __init__(self, dbname="all", outfile=None):

        self.DBName = Status.main.conf.get('DB', 'DBName')

        if outfile is None:
            outfile = openfilecreate('Output file for exporting data base')
            if outfile is None:
                return None

        (conn, cursor) = openconnection()
            
        fd = open(outfile, 'w')
        fd.write('<?xml version="1.0" encoding="utf-8"?>\n')
        fd.write('<EinsteinDataBase dbname="%s">\n' % (dbname,))

        if dbname == "all":
            self.dumpTable(cursor, fd, "dbfluid", "")
            self.dumpTable(cursor, fd, "dbfuel", "")
            
            self.dumpTable(cursor, fd, "dbboiler", "")
            self.dumpTable(cursor, fd, "dbchp", "")
            self.dumpTable(cursor, fd, "dbheatpump", "")
            self.dumpTable(cursor, fd, "dbsolarthermal", "")
            
#            self.dumpTable(cursor, fd, "dbbenchmark", "")
            
        elif dbname == "all equipments":
            self.dumpTable(cursor, fd, "dbboiler", "")
            self.dumpTable(cursor, fd, "dbchp", "")
            self.dumpTable(cursor, fd, "dbheatpump", "")
            self.dumpTable(cursor, fd, "dbsolarthermal", "")
            
        else:
            print "exportDB: ",dbname
            self.dumpTable(cursor, fd, dbname, "")

        fd.write('</EinsteinDataBase>\n')
        fd.close()
        conn.close()



    def dumpTable(self, cursor, fd, table, criterium, order=None):
        fieldtypes = {}
        #cursor.execute("SELECT column_name, data_type FROM information_schema.columns " \
        #                "WHERE table_name = '%s' AND table_schema = 'einstein'" % (table,))
        cursor.execute("SHOW COLUMNS FROM `%s` FROM %s" % (table,self.DBName))
        result_set = cursor.fetchall()
        nfields = cursor.rowcount
        for field in result_set:
            fname = field['Field']
            ftype = field['Type']
            fextra = field['Extra']
            fieldtypes[fname] = (ftype,fextra)
    
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
            fd.write('<table name="%s">\n' % (table,))
            nn = 0
            for row in result_set:
                nn+=1
                fd.write('<row n="%s">\n' % (nn,))
                for key in row.keys():
                    value = row[key]
                    if value is not None:
                        type,extra = fieldtypes[key]
                        s = '<element name="%s" type="%s" auto="%s" value="%s" />\n' % (key,type,extra,value)
#                        s = '<%s>%s</%s>\n' % (key,value,key)
                        fd.write(s)
                fd.write('</row>\n')
            fd.write('</table>\n')

#------------------------------------------------------------------------------
class ImportDB(object):
#------------------------------------------------------------------------------
#   complement to ExportProject: imports data from another project
#------------------------------------------------------------------------------

    def __init__(self,mode="ignore",infile=None):

        if infile is None:
            infile = openfilecreate('Choose a project file for importing',
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if infile is None:
                return None

        (conn, cursor) = openconnection()
        #
        # get the highest project number so far in the database, add 1, and assign to the
        # imported project

#......................................................................
# ask for confirmation before causing a major desaster

        dialog =  DialogImport(None,_("import data"),\
                               _("This will modify your databases\nIf You are sure, specify what to do with duplicate data")+\
                               _("\nElse press CANCEL"))
        ret = dialog.ShowModal()
        if ret == wx.ID_OK:
            mode = "overwrite"
        elif ret == wx.ID_IGNORE:
            mode = "ignore"
        else:
            return

        print "ImportDB in mode ",mode

        # create a dom and import in it the xml project file
        self.document = xml.dom.minidom.parse(infile)
        # get the elements from the DOM
        dbs = self.document.getElementsByTagName('EinsteinDataBase')
        for db in dbs:
            tables = db.getElementsByTagName("table")
            tabledict = {}
            for table in tables:
                tablename =  table.getAttribute('name')
                tablelist = []
                rows = table.getElementsByTagName("row")
                for row in rows:
                    sqlist = []
                    newdict = {}
                    nrow =  row.getAttribute('n')
                    elements = row.getElementsByTagName("element")

                    rowName = None #characteristic name of the row
                    rowPar1 = None
                    rowPar2 = None
                    
                    for element in elements:
                        fieldname = element.getAttribute('name').lower()
                        fieldnameCapitalLetters = element.getAttribute('name')
                        eltype = element.getAttribute('type')
                        elauto = element.getAttribute('auto')
                        elvalue = element.getAttribute('value')

                        if tablename == "dbfluid" and fieldname == "fluidname":
                            rowName = elvalue
                        elif tablename == "dbfuel" and fieldname == "fuelname":
                            rowName = elvalue
                        elif tablename == "auditor" and fieldname == "name":
                            rowName = elvalue
                        elif tablename == "dbelectricitymix":
                            if fieldname == "country":
                                rowName = elvalue
                            elif fieldname == "year":
                                rowPar1 = elvalue
                        elif tablename == "dbboiler":
                            if fieldname == "boilermanufacturer":
                                rowName = elvalue
                            elif fieldname == "boilermodel":
                                rowPar1 = elvalue
                        elif tablename == "dbchp":
                            if fieldname == "chpequip":
                                rowName = elvalue
                        elif tablename == "dbheatpump":
                            if fieldname == "hpmanufacturer":
                                rowName = elvalue
                            elif fieldname == "hpmodel":
                                rowPar1 = elvalue
                        elif tablename == "dbsolarthermal":
                            if fieldname == "stmanufacturer":
                                rowName = elvalue
                            elif fieldname == "stmodel":
                                rowPar1 = elvalue

                        if elauto != 'auto_increment':
                            newdict.update({fieldnameCapitalLetters:elvalue})

                        # substitute invalid chars in char fields and enclose in ''
                        if eltype.startswith('char') or eltype.startswith('varchar') or eltype.startswith('text'):
                            elvalue = "'" + self.subsIllegal(elvalue) + "'"
                        # substitute auto-increment value with NULL
                        if elauto == 'auto_increment':
                            # main key field
                            oldKey = int(elvalue)
                            elvalue = 'NULL'

                        sqlist.append("%s=%s" % (fieldname,elvalue))

#......................................................................
# before inserting new entry, check if entry with the same name exists
# (only for questionnaire, dbfluid, dbfuel

                    ignoreRow = False
                    existingRows = []
                    if tablename == "dbfluid":
                        existingRows = Status.DB.dbfluid.FluidName[rowName]

                    elif tablename == "dbfuel":
                        existingRows = Status.DB.dbfuel.FuelName[rowName]

                    elif tablename == "auditor":
                        existingRows = Status.DB.auditor.Name[rowName]

                    elif tablename == "dbelectricitymix":
                        if rowPar1 is None:
                            existingRows = Status.DB.dbelectricitymix.Country[rowName]
                        else:
                            existingRows = Status.DB.dbelectricitymix.Country[rowName].Year[rowPar1]
                            
                    elif tablename == "dbboiler":
                        if rowPar1 is None:
                            existingRows = Status.DB.dbboiler.BoilerManufacturer[rowName]
                        else:
                            existingRows = Status.DB.dbboiler.BoilerManufacturer[rowName].BoilerModel[rowPar1]
                            
                    elif tablename == "dbchp":
                        existingRows = Status.DB.dbchp.CHPequip[rowName]
                            

                    elif tablename == "dbheatpump":
                        if rowPar1 is None:
                            existingRows = Status.DB.dbheatpump.HPManufacturer[rowName]
                        else:
                            existingRows = Status.DB.dbheatpump.HPManufacturer[rowName].HPModel[rowPar1]
                            
                    elif tablename == "dbsolarthermal":
                        if rowPar1 is None:
                            existingRows = Status.DB.dbsolarthermal.STManufacturer[rowName]
                        else:
                            existingRows = Status.DB.dbsolarthermal.STManufacturer[rowName].STModel[rowPar1]
                            
   
                    else:
                        existingRows = []

                    if len(existingRows) > 0:
                        if rowPar2 is None:
                            par2 = ""
                        else:
                            par2 = " "+str(rowPar2)

                        if rowPar1 is None:
                            par1 = ""
                        else:
                            par1 = " "+str(rowPar1)

                        logWarning("%s: %s%s%s"%(tablename,rowName,par1,par2)+\
                                   _(" already in database. Data from imported file will be ignored"))

                        if mode == "overwrite":
                            existingRows[0].update(newdict)
                                             
                    else:
                        # create sql sentence and update database
                        sql = 'INSERT INTO %s SET ' % (tablename,) + ', '.join(sqlist)
                        cursor.execute(sql)
                        # get last inserted
                        cursor.execute('SELECT LAST_INSERT_ID() AS last')
                        field = cursor.fetchone()
                        
                                                
        conn.close()

        

    def subsIllegal(self,text):
        parts = text.split("'")
        newtext = "''".join(parts)
        return newtext

