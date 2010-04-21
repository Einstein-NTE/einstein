#import wx
#from status import Status
#from GUITools import *
#
#class PanelDBBase(wx.Panel):
#
#    def __init__(self, parent):
#        self.parent = parent
#        wx.Panel.__init__(self, id = -1, name = 'PanelDBBase', parent = parent,
#              pos = wx.Point(0, 0), size = wx.Size(780, 580))
#
#    def fillChoiceOfDBFuel(self, tcentry):
#        fuelDict = Status.prj.getFuelDict()
#        fuelList = fuelDict.values()
#        fillChoice(tcentry, fuelList)
#
#    def fillEquipmentList(self):
#        try: self.page0.clearListBox()
#        except: pass
#        try: self.page1.clearListBox()
#        except: pass
#        try: self.page2.clearListBox()
#        except: pass
#        try: self.page3.clearListBox()
#        except: pass
#
#        self.addEquipmentToList()
#
#    def clearPage0(self):
#        self.clear()
#        try: self.page0.listBoxEquipment.DeselectAll()
#        except: pass
#        try: self.page1.listBoxEquipment.DeselectAll()
#        except: pass
#        try: self.page2.listBoxEquipment.DeselectAll()
#        except: pass
#        try: self.page3.listBoxEquipment.DeselectAll()
#        except: pass
#        self.fillEquipmentList()
#        self.fillChoiceOfDBFuel()
#        self.notebook.ChangeSelection(0)
#
#    def clear(self):
#        try: self.tc1.SetValue('')
#        except: pass
#        try: self.tc2.SetValue('')
#        except: pass
#        try: self.tc3.SetValue('')
#        except: pass
#        try: self.tc4.SetValue('')
#        except: pass
#        try: self.tc5.SetValue('')
#        except: pass
#        try: self.tc6.SetValue('')
#        except: pass
#        try: self.tc7.SetValue('')
#        except: pass
#        try: self.tc8.SetValue('')
#        except: pass
#        try: self.tc9.SetValue('')
#        except: pass
#        try: self.tc10.SetValue('')
#        except: pass
#        try: self.tc11.SetValue('')
#        except: pass
#        try: self.tc12.SetValue('')
#        except: pass
#        try: self.tc13.SetValue('')
#        except: pass
#        try: self.tc14.SetValue('')
#        except: pass
#        try: self.tc15.SetValue('')
#        except: pass
#        try: self.tc16.SetValue('')
#        except: pass
#        try: self.tc17.SetValue('')
#        except: pass
#        try: self.tc18.SetValue('')
#        except: pass
#        try: self.tc19.SetValue('')
#        except: pass
#        try: self.tc20.SetValue('')
#        except: pass
#        try: self.tc21.SetValue('')
#        except: pass
#        try: self.tc22.SetValue('')
#        except: pass
#        try: self.tc23.SetValue('')
#        except: pass
#        try: self.tc24.SetValue('')
#        except: pass
#        try: self.tc25.SetValue('')
#        except: pass
#        try: self.tc26.SetValue('')
#        except: pass
#        try: self.tc27.SetValue('')
#        except: pass
#        try: self.tc28.SetValue('')
#        except: pass
#        try: self.tc29.SetValue('')
#        except: pass
#        try: self.tc30.SetValue('')
#        except: pass
#        try: self.tc31.SetValue('')
#        except: pass
#        try: self.tc32.SetValue('')
#        except: pass
#        try: self.tc33.SetValue('')
#        except: pass
#        try: self.tc34.SetValue('')
#        except: pass
#        try: self.tc35.SetValue('')
#        except: pass
#        try: self.tc36.SetValue('')
#        except: pass
