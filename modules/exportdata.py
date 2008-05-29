#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
import os
import wx
import MySQLdb


class ImportDataXML(object):
    def __init__(self,parent):
        self.parent = parent
        dialog = wx.FileDialog(parent=None,message='Choose a data file for importing',
                     wildcard='XML files (*.xml)|*.xml',
                     style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() != wx.ID_OK:
            return
        infile = dialog.GetPath()

        try:
            # get a new connection
            conn = self.parent.connectToDB()
        except MySQLdb.Error, e:
            self.parent.showError('Cannot connect to database to export data. '\
                                  'Error is:\n\n%s\n\nPlease verify.' % (str(e),))
            return

        self.cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        self.fd = open(infile, 'r')
        self.fd.close()
        conn.close()

class ExportDataXML(object):
    def __init__(self,parent,pid=None,ano=None,fuels=[],fluids=[]):
        self.parent = parent
        # ask for file for exporting
        dialog = wx.FileDialog(parent=None,
                               message='Output file for exporting',
                               wildcard='XML files (*.xml)|*.xml',
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() != wx.ID_OK:
            return

        outfile = dialog.GetPath()

        try:
            # get a new connection
            conn = self.parent.connectToDB()
        except MySQLdb.Error, e:
            self.parent.showError('Cannot connect to database to export data. '\
                                  'Error is:\n\n%s\n\nPlease verify.' % (str(e),))
            return

        self.cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        self.fd = open(outfile, 'w')
        self.fd.write('<?xml version="1.0" encoding="utf-8"?>\n')

        if pid is not None and ano is not None:
            criterium = "WHERE Questionnaire_id=%s AND AlternativeProposalNo=%s" % (pid,ano)
            self.dumpTable('qgenerationhc', criterium)
            self.dumpTable('qprocessdata', criterium)

            criterium = "WHERE ProjectID=%s AND AlternativeProposalNo=%s" % (pid,ano)
            self.dumpTable('qheatexchanger', criterium)
            self.dumpTable('qwasteheatelequip', criterium)

        if len(fuels)>0:
            criterium = "WHERE DBFuel_ID IN %s" % (str(fuels),)
            criterium = criterium.replace('[','(').replace(']',')')
            print 'FUELS='+criterium
            self.dumpTable('dbfuel', criterium)

        if len(fluids)>0:
            criterium = "WHERE DBFluid_ID IN %s" % (str(fluids),)
            criterium = criterium.replace('[','(').replace(']',')')
            print 'FLUIDS='+criterium
            self.dumpTable('dbfluid', criterium)
            
        self.fd.close()
        conn.close()

    def dumpTable(self, table, criterium):
        fieldtypes = {}
        self.cursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS " \
                        "WHERE table_name = '%s' AND table_schema = 'einstein'" % (table,))
        result_set = self.cursor.fetchall()
        nfields = self.cursor.rowcount
        for field in result_set:
            fname = field['COLUMN_NAME']
            ftype = field['DATA_TYPE']
            fieldtypes[fname] = ftype
    
        sql = "SELECT * FROM %s" % (table,)
        if criterium:
            sql += (' ' + criterium)
        self.cursor.execute(sql)
        result_set = self.cursor.fetchall()
        nrows = self.cursor.rowcount
        if nrows <= 0:
            self.fd.write('<!-- table %s has no values -->\n' % (table,))
        else:
            self.fd.write('<table name="%s" rows="%s">\n' % (table,nrows))
            i = 0
            for row in result_set:
                self.fd.write('<row i="%s" fields="%s">\n' % (i,nfields))
                i += 1
                for key in row.keys():
                    value = row[key]
                    if value is None:
                        value = ''
                    s = '<field name="%s" type="%s" value="%s" />\n' % (key, fieldtypes[key],value)
                    self.fd.write(s)
                self.fd.write('</row>\n')
            self.fd.write('</table><!-- end of %s -->\n' % (table,))
