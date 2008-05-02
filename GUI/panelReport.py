#Boa:Frame:Frame1
#==============================================================================#
#	E I N S T E I N
#
#       Expert System for an Intelligent Supply of Thermal Energy in Industry
#       (www.iee-einstein.org)
#
#------------------------------------------------------------------------------
#
#	panelReport- Component for report generation
#			
#==============================================================================
#
#	Version No.: 0.01
#	Created by: 	    Tom Sobota	30/04/2008
#
#       Changes to previous version:
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
#
# Description of the process of report generation.
#
# 1.  The master document areas subject to change are marked with 'names',
#     which should be related to the keys to the data for the panels.
#     i.e. panelEA2 uses the key 'EA2', so the name will be 'KEY_EA2' (OO does
#     not accept simply 'EA2', so I added the ' KEY_' prefix.). These names
#     are saved in the document (contents.xml) and can be read from there.
#
# 1.1   Creation of a name.
#       a. A region is selected in the sheet.
#       b. Main menu Insert -> Names ->Define (or just Ctrl-F3) will open a dialog
#          where the name is written. The area is taken from the selection. After
#          writing the new name, press Add.
#
# 2.  When the Generate Report option is activated, this module (reporter.py) starts
#     to execute. The steps are:
#
# 2.1   The contents.xml component of the master document (Master) is read and stored
#       as a DOM tree in memory.
#
# 2.2   The names are extracted, together with the ranges they point to. Only the names
#       that start with the prefix 'KEY_' are kept. The prefix is discarded and the
#       rest (that will be the same as the key to the data in Interfaces.GData) is saved
#       as the key to a dictionary entry. The data is the range information. The
#       dictionaries 'names' and 'sheetnames' manage different views of this information.
#
# 2.2   The names dictionary is saved as a XML document, as a reference and debugging
#       aid.
#
# 2.3   Now contents.xml is scanned sequentially looking for worksheets and ranges
#       that exist in the names dictionary. When a correspondence is found, the data
#       is taken from Interfaces using the name (without the prefix) as key. Then
#       the valued are stored in the tree.
#
# 3.  Finally, the DOM tree is saved as a new OO document, which is the generated report.
#
#########################################################################################

import xml.dom
import xml.dom.minidom
from zipfile import *
from StringIO import *
import re
import sys
import os
from numpy import *
import wx
from einstein.modules.interfaces import *
#
# constants
#
COLUMNS     ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
PREFIX      ='KEY_'
NEWREPORT   = 'report.ods'
TMPFILE     = "./workfile"
CONTENTFILE = 'content.xml'
P_RANGE     = re.compile('.*?\'(.+?)\'.*?\$([A-Z]+)\$(\d+).*?\$([A-Z]+)\$(\d+)')
P_CELL      = re.compile('.*?\'(.+?)\'.*?\$([A-Z]+)\$(\d+)')

wxID_BTNSELECTREPORT = wx.NewId()

        
class PanelReport(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=-1, name='', parent=prnt,
              pos=wx.Point(0,0), size=wx.Size(800, 600))
        self.SetClientSize(wx.Size(800, 600))

        self.staticText1 = wx.StaticText(id=-1,
              label=u'Report generation', name='staticText1', parent=self,
              pos=wx.Point(352, 25), size=wx.Size(127, 17), style=0)
        self.staticText1.SetFont(wx.Font(12, wx.SWISS,wx.NORMAL,wx.BOLD, False))

        self.btnSelectReport = wx.Button(id=wxID_BTNSELECTREPORT,
              label=u'Select report', name=u'btnSelectReport', parent=self,
              pos=wx.Point(304, 88), size=wx.Size(240, 40), style=0)
        self.btnSelectReport.Bind(wx.EVT_BUTTON, self.OnBtnSelectReport,
              id=wxID_BTNSELECTREPORT)

        self.txtMessage = wx.StaticText(id=-1,
              label='', name=u'txtMessage', parent=self,
              pos=wx.Point(264, 152), size=wx.Size(320, 192), style=0)


    def __init__(self, parent,main):
        self._init_ctrls(parent)
        self.parent = parent
        self.main=main
    #
    # GUI events
    #
    def OnBtnSelectReport(self, event):
        #
        # Open an existing OpenDocument workbook
        # for processing
        #
        dialog = wx.FileDialog(parent=None,message='Choose a master report file',
                               defaultDir=os.path.join(os.getcwd(),'reports'),
                     wildcard='Open Office spreadsheets files (*.ods)|*.ods',
                     style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
        if dialog.ShowModal() == wx.ID_OK:
            self.master = dialog.GetPath()
            if self.master.strip():
                self.generateReport()
        else:
            self.master = None

        event.Skip()
    #
    # public instance methods
    #
    def generateReport(self): 
        self.main.logMessage('Generating report from ' + self.master)

        folder = os.path.dirname(self.master)
        thisreport = os.path.join(folder,NEWREPORT)

        infile = ZipFile(self.master, "r")
        dataSource = StringIO(infile.read(CONTENTFILE))
        self.document = xml.dom.minidom.parse(dataSource)
         # create the names list
        self.createNamesTable()
        # replace values
        self.replaceData()
        # Send the document tree to a temporary file
        # and destroy the tree
        # and store the file in a new OO doc
        
        try:
            outfile = ZipFile(thisreport, "w", ZIP_DEFLATED)
        except IOError,e:
            self.main.showError('Error creating report %s. You have probably another version opened:%s' %\
                  (thisreport,str(e)))
            return

        dataOut = open(CONTENTFILE, "wb")
        dataOut.write(self.document.toxml(encoding='utf-8'))
        dataOut.close()
        self.main.logMessage('Adding OO component '+CONTENTFILE)
        outfile.write(CONTENTFILE)
        self.close()

        # copy the rest of the original components
        # to the new OO document
        infile = ZipFile(self.master, "r")
        for component in infile.namelist():
            if component != CONTENTFILE:
                self.main.logMessage('Adding OO component '+component)
                dataIn = infile.read(component)
                dataOut = open(TMPFILE, "wb")
                dataOut.write(dataIn)
                dataOut.close()
                outfile.write(TMPFILE,component)

        outfile.close()
        infile.close()
        self.main.showInfo('Report generation is finished\n'
                             'The generated report is:' + thisreport)


    def close(self):
        self.document.unlink()

    def getDOM(self):
        return self.document
    
    def createNamesTable(self):
        self.names = {}
        self.sheetnames = {}

        namelements = self.document.getElementsByTagName("table:named-range")
        for namelement in namelements:
            name = namelement.getAttribute('table:name')
            if not name.startswith(PREFIX):
                continue
            name = name[len(PREFIX):]
            range = namelement.getAttribute('table:cell-range-address')
            m = P_RANGE.match(range)
            if m:
                # datum is a range
                colFrom = int(COLUMNS.find(m.group(2).strip().upper())) + 1
                rowFrom = int(m.group(3))
                colTo = int(COLUMNS.find(m.group(4).strip().upper())) + 1
                rowTo = int(m.group(5))
                sheetname = m.group(1)
                itemlist = [rowFrom, colFrom, rowTo, colTo]
            else:
                m = P_CELL.match(range)
                if m:
                    # datum is a single cell
                    col = int(COLUMNS.find(m.group(2).strip().upper())) + 1
                    row = int(m.group(3))
                    sheetname = m.group(1)
                    itemlist = [row, col]

            if m:
                self.names[name] = [sheetname,itemlist]
                sheetlist = []
                if self.sheetnames.has_key(sheetname):
                    sheetlist = self.sheetnames[sheetname]
                sheetlist.append([name,itemlist])
                self.sheetnames[sheetname] = sheetlist


    def replaceData(self):
        #
        # Parse the document and modify table cells
        #
        worksheets = self.document.getElementsByTagName("table:table")
        for sheet in worksheets:
            sheetname =  sheet.getAttribute('table:name')
            if not self.sheetnames.has_key(sheetname):
                continue
            print 'Updating worksheet ' + repr(sheetname)
            nrow=0
            #rowElements = self.document.getElementsByTagName("table:table-row")
            rowElements = sheet.getElementsByTagName("table:table-row")
            for row in rowElements:
                nrow += 1
                things =  self._processRowFindName(sheetname,nrow, row)
                if things is not None:
                    # a name referring to this row has been found
                    (ncol, data, thelist) = things
                    (datarows,datacols) = data.shape
                    for c in range(datacols):
                        for r in range(datarows):
                            self._findOneCell(sheet,nrow+r,ncol+c,data[r,c])


#
# private instance methods
#

    def _findOneCell(self,sheet,nrowfound,ncolfound,newval):
        nrow=0
        rowElements = sheet.getElementsByTagName("table:table-row")
        for row in rowElements:
            nrow += 1
            if nrow != nrowfound:
                continue

            ncol = 1
            for element in row.childNodes:
                if element.nodeName == 'table:covered-table-cell':
                    pass # looks like this doesn't count
                elif element.nodeName == 'table:table-cell':
                    if ncol == ncolfound:
                        # found the place!
                        # replace and exit
                        self._changeOneCell(element,newval)
                        return
                    n = element.getAttribute('table:number-columns-repeated')
                    if n:
                        # if repeated, add the value
                        ncol += int(n)
                    else:
                        # if not, add 1
                        ncol += 1



    def _changeOneCell(self,element,newval):
        # now let's do the change
        if not newval:
            return
        try:
            newval=newval.strip()
            dummy = float(newval)
            element.setAttribute('office:value',newval)
            element.setAttribute('office:value-type','float')
            # there probably is a text node also with the value
            # it is deleted here and OO will recreate it.
            child = element.firstChild
            while child is not None:
                next = child.nextSibling
                if (child.nodeType == child.ELEMENT_NODE and child.tagName == 'text:p') or \
                    (child.nodeType == child.TEXT_NODE):
                    element.removeChild(child)
                child = next
            element.normalize()
            return
        except ValueError:
            pass
        # the value is a text element
        child = element.firstChild
        while child is not None:
            next = child.nextSibling
            if child.nodeType == child.ELEMENT_NODE:
                child.firstChild.data = newval
                return
            child = next
        # if comes here, there was not a previous text node.
        # create a text child for the data
        dataelement = self.document.createElement('text:p')
        # now the text with the value
        text = self.document.createTextNode(newval)
        dataelement.appendChild(text)
        element.appendChild(dataelement)
        element.normalize()



    def _processRowFindName(self,sheetname,nrow,row):
        ncol = 0
        for element in row.childNodes:
            if element.nodeName == 'table:covered-table-cell':
                pass # looks like this doesn't count
            elif element.nodeName == 'table:table-cell':
                n = element.getAttribute('table:number-columns-repeated')
                if n:
                    # if repeated, add the value
                    ncol += int(n)
                else:
                    # if not, add 1
                    ncol += 1

                #
                # get the list of names,changes for this worksheet
                # each element of the list has the structure:
                # [name,[r,c]] for cells
                # [name,[upper_row, left_col, lower_row, right_col]] for ranges
                #
                changeslist = self.sheetnames[sheetname]
                for cl in changeslist:
                    thename = cl[0]
                    thelist = cl[1]
                    if int(thelist[0]) == nrow and int(thelist[1]) == ncol:
                        if not Interfaces.GData.has_key(thename):
                            continue
                        data = Interfaces.GData[thename]
                        return (ncol, data, thelist)

        # no data for this row
        return None


