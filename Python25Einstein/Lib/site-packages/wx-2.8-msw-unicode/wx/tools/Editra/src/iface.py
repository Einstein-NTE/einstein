###############################################################################
# Name: iface.py                                                              #
# Purpose: Plugin interface definitions                                       #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2007 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
#--------------------------------------------------------------------------#
# FILE: iface.py
# AUTHOR: Cody Precord
# LANGUAGE: Python
# SUMMARY:
#   This module contains numerous plugin interfaces and the Extension points
# that they extend.
#
# Intefaces:
#   * ShelfI: Interface into the L{Shelf}
#   * MainWindowI: Interface into L{ed_main.MainWindow}
#
#--------------------------------------------------------------------------#
"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: iface.py 49941 2007-11-14 08:58:28Z CJP $"
__revision__ = "$Revision: 49941 $"

#--------------------------------------------------------------------------#
# Dependancies
import re
import wx
import plugin
from extern import flatnotebook as FNB
from profiler import Profile_Get
import ed_menu
import ed_glob

#--------------------------------------------------------------------------#
PGNUM_PAT = re.compile(' - [0-9]+')
_ = wx.GetTranslation

#--------------------------------------------------------------------------#

class MainWindowI(plugin.Interface):
    """The MainWindow Interface is intended as a simple general purpose
    interface for adding functionality to the main window. It does little
    managing of how objects that implement it are handled, most is left up to
    the plugin. Some examples of plugins using this interface are the
    FileBrowser and Calculator plugins.

    """
    def PlugIt(self, window):
        """This method is called once and only once per window when it is 
        created. It should typically be used to register menu entries, 
        bind event handlers and other similar actions.

        @param window: The parent window of the plugin
        @postcondition: The plugins controls are installed in the L{MainWindow}

        """
        raise NotImplementedError

    def GetMenuHandlers(self):
        """Get menu event handlers/id pairs. This function should return a
        list of tuples containing menu ids and their handlers. The handlers
        should be not be a member of this class but a member of the ui component
        that they handler acts upon.
        
        
        @return: list [(ID_FOO, foo.OnFoo), (ID_BAR, bar.OnBar)]

        """
        pass

    def GetUIHandlers(self):
        """Get update ui event handlers/id pairs. This function should return a
        list of tuples containing object ids and their handlers. The handlers
        should be not be a member of this class but a member of the ui component
        that they handler acts upon.
        
        
        @return: list [(ID_FOO, foo.OnFoo), (ID_BAR, bar.OnBar)]

        """
        pass

#-----------------------------------------------------------------------------#

class ShelfI(plugin.Interface):
    """Interface into the L{Shelf}. All plugins wanting to be
    placed on the L{Shelf} should implement this interface.

    """
    def AllowMultiple(self):
        """This method is used to check if multiple instances of this
        item are allowed to be open at one time.
        @return: True/False
        @rtype: boolean

        """

    def CreateItem(self, parent):
        """This is them method used to open the item in the L{Shelf}
        It should return an object that is a Panel or subclass of a Panel.
        @param parent: The would be parent window of this panel
        @return: wx.Panel

        """

    def GetId(self):
        """Return the id that identifies this item (same as the menuid)
        @return: Item ID
        @rtype: int

        """

    def GetMenuEntry(self, menu):
        """Returns the menu entry associated with this item
        @param menu: The menu this entry will be added to
        @return: wx.MenuItem

        """

    def GetName(self):
        """Return the name of this shelf item. This should be the
        same as the MenuEntry's label.
        @return: name of item
        @rtype: string

        """

    def IsStockable(self):
        """Return whether this item type is stockable. The shelf saves
        what pages it had open the last time the program was run and then
        reloads the pages the next time the program starts. If this
        item can be reloaded between sessions return True otherwise return
        False.

        """
        

#-----------------------------------------------------------------------------#
SHELF_NAME = u'Shelf'
class Shelf(plugin.Plugin):
    """Plugin that creates a notebook for holding the various Shelf items
    implemented by L{ShelfI}.

    """
    observers = plugin.ExtensionPoint(ShelfI)

    def __init__(self, pmgr):
        """Create the Shelf
        @param pmgr: This plugins manager

        """
        self._log = wx.GetApp().GetLog()
        self._shelf = None
        self._parent = None
        self._open = dict()

    def _GetMenu(self):
        """Return the menu of this object
        @return: ed_menu.EdMenu()

        """
        menu = ed_menu.EdMenu()
        menu.Append(ed_glob.ID_SHOW_SHELF, _("Show Shelf") + "\tCtrl+Alt+S", 
                    _("Show the Shelf"))
        menu.AppendSeparator()
        menu_items = list()
        for observer in self.observers:
            # Register Observers
            self._open[observer.GetName()] = 0
            try:
                menu_i = observer.GetMenuEntry(menu)
                if menu_i:
                    menu_items.append((menu_i.GetLabel(), menu_i))
            except Exception, msg:
                self._log("[shelf][err] %s" % str(msg))
        menu_items.sort()

        combo = 0
        for item in menu_items:
            combo += 1
            item[1].SetText(item[1].GetText() + "\tCtrl+Alt+" + str(combo))
            menu.AppendItem(item[1])
        return menu

    def AddItem(self, item, name):
        """Add an item to the shelfs notebook. This is usefull for interacting
        with the Shelf from outside its interface. It may be necessary to
        call L{EnsureShelfVisible} before or after adding an item if you wish
        the shelf to be shown when the item is added.
        @param item: A panel like instance to add to the shelfs notebook
        @param name: Items name used for page text in notebook

        """
        self._shelf.AddPage(item, u"%s - %d" % (name, self._open.get(name, 0)))
        self._open[name] = self._open.get(name, 0) + 1

    def CanStockItem(self, item_name):
        """See if a named item can be stocked or not, meaning if it
        can be saved and opened in the next session or not.
        @param item_name: name of item to check
        @return: bool whether item can be stocked or not

        """
        for item in self.observers:
            if item_name == item.GetName():
                if hasattr(item, 'IsStockable'):
                    return item.IsStockable()
                else:
                    break
        return False

    def Init(self, parent):
        """Mixes the shelf into the parent window
        @param parent: Reference to MainWindow

        """
        # First check if the parent has an instance already
        self._parent = parent
        mgr = parent.GetFrameManager()
        if mgr.GetPane(SHELF_NAME).IsOk():
            return

        self._shelf = FNB.FlatNotebook(parent, 
                                       style=FNB.FNB_FF2 | \
                                             FNB.FNB_X_ON_TAB | \
                                             FNB.FNB_BACKGROUND_GRADIENT | \
                                             FNB.FNB_NODRAG)
        mgr.AddPane(self._shelf, wx.aui.AuiPaneInfo().Name(SHELF_NAME).\
                            Caption("Shelf").Bottom().Layer(0).\
                            CloseButton(True).MaximizeButton(False).\
                            BestSize(wx.Size(500,250)))

        # Hide the pane and let the perspective manager take care of it
        mgr.GetPane(SHELF_NAME).Hide()
        mgr.Update()

        # Install Menu and bind event handler
        view = parent.GetMenuBar().GetMenuByName("view")
        menu = self._GetMenu()
        pos = 0
        for pos in xrange(view.GetMenuItemCount()):
            mitem = view.FindItemByPosition(pos)
            if mitem.GetId() == ed_glob.ID_PERSPECTIVES:
                break

        view.InsertMenu(pos + 1, ed_glob.ID_SHELF, SHELF_NAME, 
                        menu, _("Put an item on the Shelf"))
        for item in menu.GetMenuItems():
            if item.IsSeparator():
                continue
            parent.Bind(wx.EVT_MENU, self.OnGetShelfItem, item)

        if menu.GetMenuItemCount() < 3:
            view.Enable(ed_glob.ID_SHELF, False)

        self.StockShelf(Profile_Get('SHELF_ITEMS', 'list', []))

    def EnsureShelfVisible(self):
        """Make sure the Shelf is visable
        @precondition: Shelf.Init has been called
        @postcondition: Shelf is shown

        """
        if not hasattr(self._parent, 'GetFrameManager'):
            return

        mgr = self._parent.GetFrameManager()
        pane = mgr.GetPane(SHELF_NAME)
        if not pane.IsShown():
            pane.Show()
            mgr.Update()

    def GetCount(self, item_name):
        """Get the number of open instances of a given Shelf Item
        @param item_name: Name of the Shelf item
        @return: number of instances on the Shelf

        """
        count = 0
        if self._shelf is None:
            return count

        for page in xrange(self._shelf.GetPageCount()):
            if item_name == re.sub(PGNUM_PAT, u'', 
                                   self._shelf.GetPageText(page), 1):
                count = count + 1
        return count

    def GetItemId(self, item_name):
        """Get the id that identifies a given item
        @param item_name: name of item to get ID for
        @return: integer id or None if not found

        """
        for item in self.observers:
            if item_name == item.GetName():
                return item.GetId()
        return None

    def GetItemStack(self):
        """Returns a list of ordered named items that are open in the shelf
        @return: list of strings

        """
        rval = list()
        if self._shelf is None:
            return rval

        for page in xrange(self._shelf.GetPageCount()):
            rval.append(re.sub(PGNUM_PAT, u'', 
                        self._shelf.GetPageText(page), 1))
        return rval

    def GetWindow(self):
        """Return reference to the Shelfs window component
        @return: FlatnoteBook

        """
        return self._shelf

    def Hide(self):
        """Hide the shelf
        @postcondition: Shelf is hidden by aui manager

        """
        if not hasattr(self._parent, 'GetFrameManager'):
            return

        mgr = self._parent.GetFrameManager()
        pane = mgr.GetPane(SHELF_NAME)
        if pane.IsOk():
            pane.Hide()
            mgr.Update()

    def IsShown(self):
        """Is the shelf visible?
        @return: bool

        """
        if not hasattr(self._parent, 'GetFrameManager'):
            return

        mgr = self._parent.GetFrameManager()
        pane = mgr.GetPane(SHELF_NAME)
        if pane.IsOk():
            return pane.IsShown()
        else:
            return False

    def OnGetShelfItem(self, evt):
        """Handles menu events that have been registered
        by the Shelf Items on the Shelf.
        @param evt: Event that called this handler

        """
        e_id = evt.GetId()
        if e_id == ed_glob.ID_SHOW_SHELF:
            if self.IsShown():
                self.Hide()
                self._parent.GetNotebook().GetCurrentCtrl().SetFocus()
            else:
                self.EnsureShelfVisible()
                mgr = self._parent.GetFrameManager()
                pane = mgr.GetPane(SHELF_NAME)
                if pane is not None:
                    page = pane.window.GetCurrentPage()
                    if hasattr(page, 'SetFocus'):
                        page.SetFocus()
        else:
            self.PutItemOnShelf(evt.GetId())

    def OnPutShelfItemAway(self, evt):
        """Handles when an item is closed
        @param evt: event that called this handler
        @todo: is this needed?

        """
        print "OnPutShelfItemAway Not implemented"
        evt.Skip()

    def PutItemOnShelf(self, shelfid):
        """Put an item on the shelf by using its unique shelf id.
        This is only for use with loading items implementing the
        L{ShelfI} interface. See L{AddItem} if you wish to pass
        a panel to the shelf to add.
        @param shelfid: id of the ShelfItem to open

        """
        item = None
        for shelfi in self.observers:
            if shelfi.GetId() == shelfid:
                item = shelfi
                break

        if item is None:
            return

        name = item.GetName()
        if self.ItemIsOnShelf(name) and \
            not item.AllowMultiple() or \
            self._shelf is None:
            return
        else:
            self.EnsureShelfVisible()
            self.AddItem(item.CreateItem(self._shelf), name)

    def ItemIsOnShelf(self, item_name):
        """Check if at least one instance of a given item
        is currently on the Shelf.
        @param item_name: name of Item to look for

        """
        if self._shelf is None:
            return False

        for page in xrange(self._shelf.GetPageCount()):
            if self._shelf.GetPageText(page).startswith(item_name):
                return True
        return False

    def StockShelf(self, i_list):
        """Fill the shelf by opening an ordered list of items
        @param i_list: List of named L{ShelfI} instances
        @type i_list: list of strings

        """
        for item in i_list:
            if self.CanStockItem(item):
                itemid = self.GetItemId(item)
                if itemid:
                    self.PutItemOnShelf(itemid)

#--------------------------------------------------------------------------#
