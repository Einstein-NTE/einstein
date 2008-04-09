import wx
import pSQL
import HelperClass
from status import Status


class PanelQ6(wx.Panel):
    def __init__(self, parent, main):
	self.main = main
        paramlist = HelperClass.ParameterDataHelper()
        self.PList = paramlist.ReadParameterData()
        self._init_ctrls(parent)

    def _init_ctrls(self, parent):

#------------------------------------------------------------------------------
#--- UI setup
#------------------------------------------------------------------------------		

        wx.Panel.__init__(self, id=-1, name='PanelQ6', parent=parent,
              pos=wx.Point(0, 0), size=wx.Size(800, 600), style=0)


        self.stInfo3 = wx.StaticText(id=-1,
				     label="NOT YET",
				     name='stInfo3',
				     parent=self,
				     pos=wx.Point(400, 300),
				     style=0)
        self.stInfo3.SetFont(wx.Font(40, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Tahoma'))

#------------------------------------------------------------------------------
#--- UI actions
#------------------------------------------------------------------------------		

                          

#------------------------------------------------------------------------------
#--- Public methods
#------------------------------------------------------------------------------		


    def clear(self):
	pass


    def fillPage(self):
	if self.main.activeQid == 0:
	    return

