# -*- coding: iso-8859-15 -*-
try:
    # only for windows
    from winreg import *
except:
    pass
import MySQLdb
import wx

class DlgDatabase(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.savedchanges=False
        # get current connection parameters
        self.main = wx.GetApp().GetTopWindow()
        self.DBHost = self.main.conf.get('DB', 'DBHost')
        self.DBUser = self.main.conf.get('DB', 'DBUser')
        self.DBPass = self.main.conf.get('DB', 'DBPass')
        self.DBName = self.main.conf.get('DB', 'DBName')
        
        self.notebook_1 = wx.Notebook(self, -1, style=0)
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)
        self.label_1 = wx.StaticText(self.notebook_1_pane_1, -1, "Hostname")
        self.text_ctrl_1 = wx.TextCtrl(self.notebook_1_pane_1, -1, value=self.DBHost)
        self.label_2 = wx.StaticText(self.notebook_1_pane_1, -1, "Database name", style=wx.ALIGN_RIGHT)
        self.text_ctrl_2 = wx.TextCtrl(self.notebook_1_pane_1, -1, value=self.DBName)
        self.label_3 = wx.StaticText(self.notebook_1_pane_1, -1, "User name")
        self.text_ctrl_3 = wx.TextCtrl(self.notebook_1_pane_1, -1, value=self.DBUser)
        self.label_4 = wx.StaticText(self.notebook_1_pane_1, -1, "Password")
        self.text_ctrl_4 = wx.TextCtrl(self.notebook_1_pane_1, -1, value=self.DBPass)
        self.buttonDBParams = wx.Button(self.notebook_1_pane_1, -1, "Save parameters")
        self.label_5 = wx.StaticText(self.notebook_1_pane_2, -1, "This operation will:\n\n1.- DELETE a previous Einstein database from\nyour MySQL server, if found.\n2.- INSTALL a new Einstein database from a\nprevious backup file (or from your installation\npackage)\n\nWARNING: all your previous data will be lost.\n\n")
        self.buttonLoadDatabase = wx.Button(self.notebook_1_pane_2, -1, "Select a database file to install")
        self.label_5_copy = wx.StaticText(self.notebook_1_pane_3, -1, "This operation will create a backup file containing\nALL the current information from your Einstein\ndatabase.\n\nThis file could be used to restore the contents of\nthe database in the case of accidents, server or\nmachine upgrades, and so on.\n\nThe current contents of the database is not affected\nby this operation.")
        self.buttonBackupDatabase = wx.Button(self.notebook_1_pane_3, -1, "Select a database file to save the backup")
        self.buttonOK = wx.Button(self, wx.ID_OK, "")
        self.buttonCancel = wx.Button(self, wx.ID_CANCEL, "")
        self.buttonTestConnection = wx.Button(self.notebook_1_pane_1, -1, "Test connection")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnTestConnection, self.buttonTestConnection)
        self.Bind(wx.EVT_BUTTON, self.OnSaveParameters, self.buttonDBParams)
        self.Bind(wx.EVT_BUTTON, self.OnRestoreDatabase, self.buttonLoadDatabase)
        self.Bind(wx.EVT_BUTTON, self.OnBackupDatabase, self.buttonBackupDatabase)


    def __set_properties(self):
        self.SetTitle("Database administration")
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
        grid_sizer_1 = wx.FlexGridSizer(6, 2, 4, 4)
        grid_sizer_1.Add(self.label_1, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_1, 0, wx.EXPAND, 2)
        grid_sizer_1.Add(self.label_2, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_2, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_3, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_3, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_4, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_4, 0, wx.EXPAND, 0)
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
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Database parameters")
        self.notebook_1.AddPage(self.notebook_1_pane_2, "Restore database")
        self.notebook_1.AddPage(self.notebook_1_pane_3, "Backup database")
        sizerGlobal.Add(self.notebook_1, 1, wx.EXPAND, 0)
        sizerOKCancel.Add(self.buttonCancel, 0, 0, 0)
        sizerOKCancel.Add(self.buttonOK, 0, 0, 0)
        sizerGlobal.Add(sizerOKCancel, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizerGlobal)
        sizerGlobal.Fit(self)
        self.Layout()

    def OnTestConnection(self, event):
        #----- try to connect to the Database
        (rsp,msg) = self.testConnection()
        if rsp:
            self.main.showInfo('Connection OK')
        else:
            self.main.showError('Connection error:\n%s' % msg)
        
    def OnSaveParameters(self, event):
        (rsp,msg) = self.testConnection()
        if not rsp:
            txt = 'Cannot connect with these parameters.\n\nError message:\n%s\n\nWant to save them anyway?'
            if self.main.askConfirmation(txt % msg) == wx.NO:
                return

        hostname = self.text_ctrl_1.GetValue().strip()
        dbname = self.text_ctrl_2.GetValue().strip()
        username = self.text_ctrl_3.GetValue().strip()
        passwd = self.text_ctrl_4.GetValue().strip()

        if not hostname or not dbname or not username:
            self.main.showWarning('Host name, database name and user name cannot be empty')
            return

        fr = open('einstein.ini', 'r')
        lines = fr.readlines()
        fr.close()
        fw = open('einstein.ini', 'w')
        for li in lines:
            s = li.strip()
            if not s:
                continue
            datalist = s.split(':')
            key = datalist[0]
            if key == 'DBHost':
                fw.write('%s:%s\n' % (key,hostname))
            elif key == 'DBUser':
                fw.write('%s:%s\n' % (key,username))
            elif key == 'DBPass':
                fw.write('%s:%s\n' % (key,passwd))
            elif key == 'DBName':
                fw.write('%s:%s\n' % (key,dbname))
            else:
                fw.write(s+'\n')
        fw.close()
        self.savedchanges=True

    def OnRestoreDatabase(self, event):
        infile = self.openfile('Choose a file for restoring the Database',
                                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if infile is not None:
            pass


    def OnBackupDatabase(self, event):
        outfile = self.openfile('Choose a file for writing the Database backup')
        #if outfile is not None:

        # this code is for testing
        for hive in Registry():
            show_all(hive)

    def show_all(key, level=0):
        if level:
            title(repr(key), level)
        else:
            title('HIVE ' + repr(key), level)
        for name in key.values:
            if name:
                point('%r = %r' % (name, key.values[name]), level + 1)
            else:
                point('(Default) = %r' % key.values[name], level + 1)
        for name in key.keys:
            try:
                show_all(key.keys[name], level + 1)
            except WindowsError:
                title('ERROR: %s' % name, level + 1)

    def title(string, level):
        point(string, level)
        point('=' * len(string), level)

    def point(string, level):
        print '  ' * level + string




    def openfile(self, text,style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT):
        # ask for file for exporting
        dialog = wx.FileDialog(parent=None,
                               message=text,
                               wildcard='XML files (*.sql)|*.sql',
                               style=style)
        if dialog.ShowModal() != wx.ID_OK:
            return None

        return dialog.GetPath()

    def testConnection(self):
        host = self.text_ctrl_1.GetValue()
        try:
            conn = MySQLdb.connect(host=self.text_ctrl_1.GetValue(),
                                   user=self.text_ctrl_3.GetValue(),
                                   passwd=self.text_ctrl_4.GetValue(),
                                   db=self.text_ctrl_2.GetValue())
            conn.close()
            return (True,None)
        except MySQLdb.Error, e:
            return (False,e)


    def getChanges(self):
        return self.savedchanges
