# -*- coding: iso-8859-15 -*-
import os
import sys
import re
from subprocess import *
import MySQLdb
import wx

def _U(text):
    return unicode(_(text),"utf-8")

class DlgDatabase(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.savedchanges=False
        # get current connection parameters
        self.main = wx.GetApp().GetTopWindow()
        try:self.DBHost = self.main.conf.get('DB', 'DBHost')
        except: self.DBHost=''
        try:self.DBUser = self.main.conf.get('DB', 'DBUser')
        except: self.DBUser=''
        try:self.DBPass = self.main.conf.get('DB', 'DBPass')
        except: self.DBPass=''
        try:self.DBName = self.main.conf.get('DB', 'DBName')
        except: self.DBName=''
        try:self.MySQLBin = self.main.conf.get('DB', 'MYSQLBIN')
        except: self.MySQLBin=''
        try:self.Encoding = self.main.conf.get('GUI', 'ENCODING')
        except: self.Encoding=''
        
        self.notebook_1 = wx.Notebook(self, -1, style=0)
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)
        self.label_1 = wx.StaticText(self.notebook_1_pane_1, -1, "Hostname")
        self.text_host = wx.TextCtrl(self.notebook_1_pane_1, -1, value=self.DBHost)
        self.label_2 = wx.StaticText(self.notebook_1_pane_1, -1, "Database name", style=wx.ALIGN_RIGHT)
        self.text_dbname = wx.TextCtrl(self.notebook_1_pane_1, -1, value=self.DBName)
        self.label_3 = wx.StaticText(self.notebook_1_pane_1, -1, "User name")
        self.text_username = wx.TextCtrl(self.notebook_1_pane_1, -1, value=self.DBUser)
        self.label_4 = wx.StaticText(self.notebook_1_pane_1, -1, "Password")
        self.text_password = wx.TextCtrl(self.notebook_1_pane_1, -1, value=self.DBPass)
        self.buttonDBParams = wx.Button(self.notebook_1_pane_1, -1, "Save parameters")
        self.label_5 = wx.StaticText(self.notebook_1_pane_2, -1, _U("This operation will:\n\n1.- DELETE a previous Einstein database from\nyour MySQL server, if found.\n2.- INSTALL a new Einstein database from a\nprevious backup file (or from your installation\npackage)\n\nWARNING: all your previous data will be lost.\n\n"))
        self.buttonLoadDatabase = wx.Button(self.notebook_1_pane_2, -1, "Select a database file to install")
        self.label_5_copy = wx.StaticText(self.notebook_1_pane_3, -1, _U("This operation will create a backup file containing\nALL the current information from your Einstein\ndatabase.\n\nThis file could be used to restore the contents of\nthe database in the case of accidents, server or\nmachine upgrades, and so on.\n\nThe current contents of the database is not affected\nby this operation."))

        self.label_6 = wx.StaticText(self.notebook_1_pane_1, -1, _U("Folder with MySql executables"))
        self.text_ctrl_6 = wx.TextCtrl(self.notebook_1_pane_1, -1, value=self.MySQLBin)

        self.label_8 = wx.StaticText(self.notebook_1_pane_1, -1, _U("Character encoding"))
        self.chEncoding = wx.Choice(self.notebook_1_pane_1, -1, choices=[])

        self.buttonBackupDatabase = wx.Button(self.notebook_1_pane_3, -1,
                                              _U("Select a file to save the database backup"))
        self.buttonFinish = wx.Button(self, -1, _U("Finish"))
        self.buttonTestConnection = wx.Button(self.notebook_1_pane_1, -1, _U("Test connection"))
        self.buttonFindMySQL = wx.Button(self.notebook_1_pane_1, -1, "...")
        self.buttonFindMySQL.SetMinSize((40, 32))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnTestConnection, self.buttonTestConnection)
        self.Bind(wx.EVT_BUTTON, self.OnSaveParameters, self.buttonDBParams)
        self.Bind(wx.EVT_BUTTON, self.OnRestoreDatabase, self.buttonLoadDatabase)
        self.Bind(wx.EVT_BUTTON, self.OnBackupDatabase, self.buttonBackupDatabase)
        self.Bind(wx.EVT_BUTTON, self.OnFindMySQL, self.buttonFindMySQL)
        self.Bind(wx.EVT_BUTTON, self.OnFinish, self.buttonFinish)


        self.ReadValidEncodings()
        
    def __set_properties(self):
        self.SetTitle(_U("Database administration"))
        #self.label_5.SetBackgroundColour(wx.Colour(255, 0, 0))
        self.label_5.SetForegroundColour(wx.Colour(255, 0, 0))
        self.label_5.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        #self.label_5_copy.SetBackgroundColour(wx.Colour(35, 142, 35))
        self.label_5_copy.SetForegroundColour(wx.Colour(0, 0, 128))
        self.label_5_copy.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

    def __do_layout(self):
        sizerGlobal = wx.BoxSizer(wx.VERTICAL)
        sizerOKCancel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(7, 2, 4, 4)
        grid_sizer_1.Add(self.label_1, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_host, 0, wx.EXPAND, 2)
        grid_sizer_1.Add(self.label_2, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_dbname, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_3, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_username, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_4, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_password, 0, wx.EXPAND, 0)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.text_ctrl_6, 0, wx.EXPAND, 0)
        sizer_4.Add(self.buttonFindMySQL,0,0,0)
        
        grid_sizer_1.Add(self.label_6,  wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(sizer_4, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        grid_sizer_1.Add(self.label_8, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.chEncoding, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)

        grid_sizer_1.AddStretchSpacer()
        grid_sizer_1.Add(self.buttonTestConnection, 0, 0, 0)
        grid_sizer_1.AddStretchSpacer()
        grid_sizer_1.Add(self.buttonDBParams, 0, 0, 0)
        
        self.notebook_1_pane_1.SetSizer(grid_sizer_1)
        sizer_2.Add(self.label_5, 0, wx.EXPAND, 0)
        sizer_2.Add(self.buttonLoadDatabase, 0, wx.ALL|wx.EXPAND, 2)
        self.notebook_1_pane_2.SetSizer(sizer_2)
        sizer_3.Add(self.label_5_copy, 0, wx.EXPAND, 0)
        sizer_3.Add(self.buttonBackupDatabase, 0, wx.EXPAND, 0)
        self.notebook_1_pane_3.SetSizer(sizer_3)
        self.notebook_1.AddPage(self.notebook_1_pane_1, _U("Database parameters"))
        self.notebook_1.AddPage(self.notebook_1_pane_2, _U("Restore database"))
        self.notebook_1.AddPage(self.notebook_1_pane_3, _U("Backup database"))
        sizerGlobal.Add(self.notebook_1, 1, wx.EXPAND, 0)
        sizerOKCancel.Add(self.buttonFinish, 0, 0, 0)
        sizerGlobal.Add(sizerOKCancel, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizerGlobal)
        sizerGlobal.Fit(self)
        self.Layout()

    
    def OnTestConnection(self, event):
        #----- try to connect to the Database
        (rsp,msg) = self.testConnection()
        if rsp:
            self.main.showInfo(_U('Connection OK'))
        else:
            self.main.showError(_U('Connection error:\n%s') % msg)
        
    def OnSaveParameters(self, event):
        (rsp,msg) = self.testConnection()
        if not rsp:
            txt = _U('Cannot connect with these parameters.\n\nError message:\n%s\n\nWant to save them anyway?')
            if self.main.askConfirmation(txt % msg) == wx.NO:
                return

        hostname = self.text_host.GetValue().strip()
        dbname = self.text_dbname.GetValue().strip()
        username = self.text_username.GetValue().strip()
        passwd = self.text_password.GetValue().strip()
        mysqlbin = self.text_ctrl_6.GetValue().strip()
        q = self.chEncoding.GetStringSelection().split('(')
        encoding = q[0].strip()


        if not hostname or not dbname or not username:
            self.main.showWarning(_U('Host name, database name and user name cannot be empty'))
            return

        if not mysqlbin:
            self.main.showWarning(_U('Mysql binary folder is unknown. Database dumps will not be made.'))

        groupmarker = re.compile(r'\[(\w+?)\]')
        itemmarker =  re.compile(r'(\w+?):(.*)')

        newDict = {'GUI':{'TEST'    :'TEST'},
                   'DB': {'ENCODING':encoding,
                          'DBHost'  :hostname,
                          'DBUser'  :username,
                          'DBPass'  :passwd,
                          'DBName'  :dbname,
                          'MYSQLBIN':mysqlbin}
                   }

        oldDict = {}

        inifile = os.path.join(os.getcwd(),'einstein.ini')
        fr = open(inifile, 'r')
        lines = fr.readlines()
        fr.close()

        # read and store the ini file
        for li in lines:
            s = li.strip()
            if not s:
                continue
            # test if line is a group
            m = groupmarker.match(s)
            if m:
                group = m.group(1)
            else:
                m = itemmarker.match(s)
                if m:
                    key = m.group(1).strip()
                    value = m.group(2).strip()
                    if not oldDict.has_key(group):
                        oldDict[group] = {}
                    oldDict[group][key] = value
                else:
                    self.main.showWarning(_U('Bad value in einstein.ini file: %s' % s))

        # substitute new values
        for group in oldDict.keys():        # GUI,DB
            oldgroup = oldDict[group]
            newgroup = newDict[group]
            for key in newgroup.keys():
                value = newgroup[key]
                oldgroup[key] = value
            oldDict[group] = oldgroup

        # rewrite ini file

        fw = open(inifile, 'w')
        for group in oldDict.keys():
            fw.write('[%s]\n' % group)
            oldgroup = oldDict[group]
            for key in oldgroup.keys():
                value = oldgroup[key]
                fw.write('%s:%s\n' % (key,value))

        fw.close()
        self.savedchanges=True
        self.main.showInfo(_U('The configuration has been updated'))

    def OnRestoreDatabase(self, event):
        self.main.showWarning("Not yet, sorry!")
        return
        infile = self.openfile(_U('Choose a file for restoring the Database'),
                                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if infile is not None:
            pass


    def OnFindMySQL(self, event):
        dialog = wx.DirDialog(parent=None,
                              message=_U('Please select the folder where MySQL binaries reside'),
                              defaultPath=self.MySQLBin,
                              style=wx.DD_DIR_MUST_EXIST)
        if dialog.ShowModal() != wx.ID_OK:
            return

        self.text_ctrl_6.SetValue(dialog.GetPath())


    def OnBackupDatabase(self, event):
        binfolder = self.text_ctrl_6.GetValue().strip()
        if binfolder == '':
            self.main.showWarning("The MySQL binary folder is not known. Cannot proceed with backup")
            return
        outfile = self.openfile(_U('Choose a file for writing the Database backup'))
        if outfile is not None:
            if not outfile.endswith('.sql'):
                outfile += '.sql'
            options = '--add-drop-database --add-drop-table --add-locks --disable-keys --extended-insert'
            program = os.path.join(binfolder,'mysqldump')
            print "DialogDatabase: program = ",program
            args = ' %s --host=%s --user=%s --password=%s %s > %s' % \
                   (options,
                    self.text_host.GetValue().strip(),
                    self.text_username.GetValue().strip(),
                    self.text_password.GetValue().strip(),
                    self.text_dbname.GetValue().strip(),
                    outfile)
            try:
                retcode = call(program + args, shell=True)
                if retcode == 0:
                    self.main.showInfo(_U("The database backup has finished"))
                elif retcode < 0:
                    self.main.showError(_U("The database backup was terminated by signal %s") % (-retcode))
                else:
                    self.main.showWarning(_U("The database backup has returned %s") % retcode)
            except OSError, e:
                    self.main.showError(_U("The database backup has failed:\n%s") % e)


    def openfile(self, text,style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT):
        # ask for file for exporting
        dialog = wx.FileDialog(parent=None,
                               message=text,
                               wildcard=_U('SQL files (*.sql)|*.sql'),
                               style=style)
        if dialog.ShowModal() != wx.ID_OK:
            return None

        return dialog.GetPath()

    def testConnection(self):
        host = self.text_host.GetValue()
        try:
            conn = MySQLdb.connect(host=self.text_host.GetValue(),
                                   user=self.text_username.GetValue(),
                                   passwd=self.text_password.GetValue(),
                                   db=self.text_dbname.GetValue())
            conn.close()
            return (True,None)
        except MySQLdb.Error, e:
            return (False,e)


    def getChanges(self):
        return self.savedchanges


    def OnFinish(self,event):
        self.SetReturnCode(wx.CANCEL)
        self.Close()
        

    def ReadValidEncodings(self):
        self.chEncoding.Clear()
        (rsp,msg) = self.testConnection()
        # if not connected ignore this
        if not rsp:
            return
        
        try:
            conn = MySQLdb.connect(host=self.text_host.GetValue(),
                                   user=self.text_username.GetValue(),
                                   passwd=self.text_password.GetValue(),
                                   db=self.text_dbname.GetValue())
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SHOW CHARACTER SET")
            result_set = cursor.fetchall()
            nfields = cursor.rowcount
            for field in result_set:
                charset = field['Charset']
                description = field['Description']
                self.chEncoding.Append(charset + '(' + description + ')')
            conn.close()
        except MySQLdb.Error, e:
            self.main.showError(str(e))

        
