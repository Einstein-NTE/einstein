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
#	Version No.: 0.04
#	Created by: 	    Tom Sobota	30/04/2008
#
#       Last revised by:    Hans Schweiger  18/06/2008
#                           Hans Schweiger  08/10/2008
#                           Hans Schweiger  12/10/2008
#                           Stoyan Danov    13/10/2008
#
#       Changes to previous version:
#
#       18/06/2008: HS  Call to function prepareDataForReport() in control.py added
#       08/10/2008: HS  Security features added for avoiding crashes
#       12/10/2008: HS  findOneCell substituted by findCellRange ->
#                       speed-up of about factor 10 or more in report writing
#       13/10/2008: SD  change _() to _U()
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
from einstein.modules.control import *
from GUITools import *
from dialogGauge import DialogGauge
#
# constants
#
COLUMNS     ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
PREFIX      ='KEY_'
NEWREPORT   = 'New_EINSTEIN_Report.ods'
TMPFILE     = "./workfile"
CONTENTFILE = 'content.xml'

wxID_BTNSELECTREPORT = wx.NewId()
wxID_PANELBUTTONFWD = wx.NewId()
wxID_PANELBUTTONBACK = wx.NewId()

def _U(text):
    return unicode(_(text),"utf-8")
        
class PanelReport(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=-1, name='', parent=prnt,
              pos=wx.Point(0,0), size=wx.Size(800, 600))
        self.SetClientSize(wx.Size(800, 600))

#..............................................................................
# Description of selected industry

        self.box1 = wx.StaticBox(id=-1,
              label=_U('Project Summary'),
              name='box1', parent=self, pos=wx.Point(10, 10),
              size=wx.Size(780, 520), style=0)
        self.box1.SetForegroundColour(TITLE_COLOR)
        self.box1.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.tc1 = wx.TextCtrl(id=-1, name='tc1',
              parent=self, pos=wx.Point(20, 40), size=wx.Size(760, 480),
                               style=wx.TE_MULTILINE | wx.TE_LINEWRAP, value="")

#------------------------------------------------------------------------------		
#       Button for report selection
#------------------------------------------------------------------------------		

        self.btnSelectReport = wx.Button(id=wxID_BTNSELECTREPORT,
              label=_U('Select report'), name=u'btnSelectReport', parent=self,
              pos=wx.Point(10, 560), size=wx.Size(150, 20), style=0)
        self.btnSelectReport.Bind(wx.EVT_BUTTON, self.OnBtnSelectReport,
              id=wxID_BTNSELECTREPORT)

#------------------------------------------------------------------------------		
#       Default action buttons: FWD / BACK / OK / Cancel
#------------------------------------------------------------------------------		

        self.buttonOk = wx.Button(id=wx.ID_OK, label=_U('OK'),
              name='buttonOk', parent=self, pos=wx.Point(528, 560),
              size=wx.Size(75, 20), style=0)

        self.buttonOk.Bind(wx.EVT_BUTTON,
              self.OnButtonOkButton,
              id=wx.ID_OK)

        self.buttonCancel = wx.Button(id=wx.ID_CANCEL, label=_U('Cancel'),
              name='buttonCancel', parent=self, pos=wx.Point(616,
              560), size=wx.Size(75, 20), style=0)

        self.buttonCancel.Bind(wx.EVT_BUTTON,
              self.OnButtonCancelButton,
              id=wx.ID_CANCEL)

        self.buttonFwd = wx.Button(id=wxID_PANELBUTTONFWD,
              label='>>>', name='buttonFwd', parent=self,
              pos=wx.Point(704, 560), size=wx.Size(75, 20), style=0)

        self.buttonFwd.Bind(wx.EVT_BUTTON,
              self.OnButtonFwdButton,
              id=wxID_PANELBUTTONFWD)

        self.buttonBack = wx.Button(id=wxID_PANELBUTTONBACK,
              label='<<<', name='buttonBack', parent=self,
              pos=wx.Point(440, 560), size=wx.Size(75, 20), style=0)

        self.buttonBack.Bind(wx.EVT_BUTTON,
              self.OnButtonBackButton,
              id=wxID_PANELBUTTONBACK)

    def __init__(self, parent, main):
        self.parent = parent
        self.main=main
        self._init_ctrls(parent)

        self.display()
        
    #
    # GUI events
    #
    def OnBtnSelectReport(self, event):
        #
        # Open an existing OpenDocument workbook
        # for processing
        #
        dialog = wx.FileDialog(parent=None,message=_U('Choose a master report file'),
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

#------------------------------------------------------------------------------		
    def display(self):
#------------------------------------------------------------------------------		
#   obtains data from SQL and displays in the panel
#------------------------------------------------------------------------------		

        sprojects = Status.DB.sproject.ProjectID[Status.PId]
        if len(sprojects) > 0:
            summary = sprojects[0].Summary

            if summary is not None:
                self.tc1.SetValue(summary)
        self.Show()
        
#------------------------------------------------------------------------------		
#   Default event handlers: FWD / BACK / OK / Cancel - Buttons
#------------------------------------------------------------------------------		

    def OnButtonBackButton(self, event):
#        self.Hide
#        self.main.tree.SelectItem(self.main.qHC, select=True)
        event.Skip()

    def OnButtonFwdButton(self, event):
#        self.Hide
#        self.main.tree.SelectItem(self.main.qHP, select=True)
        event.Skip()

    def OnButtonOkButton(self, event):
        summary = self.tc1.GetValue()
        print summary

        logMessage(_U("summary of project report updated"))

        sprojects = Status.DB.sproject.ProjectID[Status.PId]
        if len(sprojects) > 0:
            sprojects[0].Summary = check(summary)
            Status.SQL.commit()
        
#        self.Hide()
#        self.main.tree.SelectItem(self.main.qHC, select=True)
        event.Skip()

    def OnButtonCancelButton(self, event):
        logTrack("Button exitModuleCancel: CANCEL Option not yet foreseen")

#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
#------------------------------------------------------------------------------		
    #
    # public instance methods
    #
    def generateReport(self): 
        self.main.logMessage('Generating report from ' + self.master)

        prepareDataForReport()

        dlg = DialogGauge(None,_U("Report generation"),_U("creating copy of master"))

        folder = os.path.dirname(self.master)
        thisreport = os.path.join(folder,NEWREPORT)

        infile = ZipFile(self.master, "r")
        dataSource = StringIO(infile.read(CONTENTFILE))
        self.document = xml.dom.minidom.parse(dataSource)

        dlg.Destroy()
        
         # create the names list
        self.createNamesTable()
        # replace values
        self.replaceData()
        # Send the document tree to a temporary file
        # and destroy the tree
        # and store the file in a new OO doc
        
        dlg = DialogGauge(None,_U("Report generation"),_U("storing report file"))
        try:
            outfile = ZipFile(thisreport, "w", ZIP_DEFLATED)
        except IOError,e:
            self.main.showError(_U('Error creating report %s. You have probably another version opened:%s') %\
                  (thisreport,str(e)))
            return

        dataOut = open(CONTENTFILE, "wb")
        dataOut.write(self.document.toxml(encoding='utf-8'))
        dataOut.close()
#        self.main.logMessage('Adding OO component '+CONTENTFILE)
        outfile.write(CONTENTFILE)
        self.close()

        # copy the rest of the original components
        # to the new OO document
        infile = ZipFile(self.master, "r")
        for component in infile.namelist():
            if component != CONTENTFILE:
#                self.main.logMessage('Adding OO component '+component)
                dataIn = infile.read(component)
                dataOut = open(TMPFILE, "wb")
                dataOut.write(dataIn)
                dataOut.close()
                outfile.write(TMPFILE,component)

        outfile.close()
        infile.close()
        dlg.Destroy()
        self.main.showInfo(_U('Report generation is finished\n'
                             'The generated report is:') + thisreport)


    def close(self):
        self.document.unlink()

    def getDOM(self):
        return self.document
    
    def getNameComponents(self, expr):
        result = []
        e1 = expr.replace('.','')
        e2 = e1.replace(':','')
        e3 = e2.replace("'",'')
        e4 = e3.replace('&apos;','')
        comp = e4.split('$')
        for c in comp:
            s = c.strip()
            if s:
                result.append(s)

        if len(result) == 5:
            # range of cells
            return ((result[0],
                    [int(COLUMNS.find(result[1].upper())) + 1,
                     int(result[2]),
                     int(COLUMNS.find(result[3].upper())) + 1,
                     int(result[4])]))
        if len(result) == 3:
            # one single cell
            return ((result[0],
                    [int(COLUMNS.find(result[1].upper())) + 1,
                     int(result[2])]))
        else:
            # not recognized
            print 'panelReport (getNameComponents): name format not recognized->'+repr(expr)
            return None

    def createNamesTable(self):

        dlg = DialogGauge(None,"Report generation","screening master")

        self.names = {}
        self.sheetnames = {}

        namelements = self.document.getElementsByTagName("table:named-range")

        nElements = len(namelements)
        i = 0
        for namelement in namelements:
            name = namelement.getAttribute('table:name')
            if not name.startswith(PREFIX):
                continue
            name = name[len(PREFIX):]
            range = namelement.getAttribute('table:cell-range-address')
            m = self.getNameComponents(range)
            if m is not None:
                (sheetname,itemlist) = m
                self.names[name] = [sheetname,itemlist]
                sheetlist = []
                if self.sheetnames.has_key(sheetname):
                    sheetlist = self.sheetnames[sheetname]
                sheetlist.append([name,itemlist])
                self.sheetnames[sheetname] = sheetlist
        #for s in self.names.keys():
        #    print 'self.names. key',s,'value',self.names[s]
        #for s in self.sheetnames.keys():
        #    print 'self.sheetnames. key',s,'value',self.sheetnames[s]
            dlg.update(100.0 * i / nElements)
            i += 1
        dlg.Destroy()

    def replaceData(self):
        #
        # Scan the sheet names list and change values on each
        # sheet on the list
        #
        dlg = DialogGauge(None,"Report generation","writing report")
        nSheets = len(self.sheetnames.keys())
        i = 0.0

        for sheetname in self.sheetnames.keys():
            #
            # get the list of names,changes for this sheet
            # each element of the list has the structure:
            # [name,[col,row]] for cells
            # [name,[left_col, upper_row,  right_col,lower_row]] for ranges
            #
            changesList = self.sheetnames[sheetname]
            nChanges = len(changesList)
            if nChanges == 0: i += 1
            for cl in changesList:
                thename = cl[0]
                if not Interfaces.GData.has_key(thename):
                    continue
                # found a name on this sheet
                print "PanelReport (replaceData): Key = ",thename
                data = Interfaces.GData[thename]
                thelist = cl[1]
                ncol = thelist[0]
                nrow = thelist[1]
                #print "panelReport: data block found. sheet:%s name:%s row %s col %s" %\
                #      (sheetname,thename,nrow,ncol)
                try:
                    (datarows,datacols) = data.shape
                except:
                    logDebug("PanelReport (replaceData): no data shape found for key %s"%thename)
                    continue
                #print "panelReport: datacols %s datarows %s data %s" % (datacols,datarows,repr(data))
                self._findCellRange(sheetname,nrow,datarows,ncol,datacols,data)
                i += 1.0/nChanges
                dlg.update(100.0 * i / nSheets)

            dlg.update(100.0 * i / nSheets)
        dlg.Destroy()
#
# private instance methods
#

    def _findCellRange(self,sheetname,nrow0,nrows,ncol0,ncols,newdata):
        # traverse the DOM looking for one element, identified by:
        # the name of the sheet, the row and the column
        # When found, call _changeOneCell to modify the element
        #
        elementCounter = nrows*ncols
        worksheets = self.document.getElementsByTagName("table:table")
        for sheet in worksheets:
            thissheet =  sheet.getAttribute('table:name')
            if sheetname == thissheet:
                nrow=0
                rowElements = sheet.getElementsByTagName("table:table-row")
                for row in rowElements:
                    nrow += 1
                    if nrow < nrow0 or nrow >= (nrow0+nrows):
                        continue

                    ncol = 1
                    for element in row.childNodes:
                        if element.nodeName == 'table:covered-table-cell':
                            pass # looks like this doesn't count
                        elif element.nodeName == 'table:table-cell':
                            if ncol in range(ncol0,ncol0+ncols):
                                # found the place!
                                # replace and exit
                                #print 'Call _changeOneCell with element=%s newval %s' %\
                                #      (element.nodeName,newval)
                                self._changeOneCell(element,newdata[nrow-nrow0,ncol-ncol0])
                                elementCounter -= 1
                                if elementCounter == 0: return
                            n = element.getAttribute('table:number-columns-repeated')
                            if n:
                                # if repeated, add the value
                                ncol += int(n)
                            else:
                                # if not, add 1
                                ncol += 1

    def _changeOneCell(self,element,newval):
        if newval is None:
            newval = ''
        elif not newval:
            newval = ''

        # ok we have some value
        try:
            dummy = float(newval)
            aNumber = True
        except ValueError:
            aNumber = False

        newval = str(newval)
        if aNumber:
            print "PanelReport: converting -> %s as a number"%newval
        
            element.setAttribute('office:value',newval)
            ##print "Do: element.setAttribute('office:value',%s)" % (newval,)
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
        else:
            print "PanelReport: converting -> %s as text"%newval
            # the value is a text element
            child = element.firstChild
            while child is not None:
                next = child.nextSibling
                if child.nodeType == child.ELEMENT_NODE:
                    print 'panelReport (changeOneCell): writing data to firstChild -> %s' % (newval)
                    try:
                        child.firstChild.data = newval
                    except:
                        logDebug("PanelReport (_changeOneCell): error writing to child.firstchild.data)")
                    return
                child = next
            # if comes here, there was not a previous text node.
            # create a text child for the data
            dataelement = self.document.createElement('text:p')
            # now the text with the value
            text = self.document.createTextNode(newval)
            print 'panelReport (changeOneCell): text = self.document.createTextNode(%s) -> %s' % (newval,text)
            
            dataelement.appendChild(text)
            element.appendChild(dataelement)
            
        element.normalize()



