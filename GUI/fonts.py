import wx
import MySQLdb
from status import Status

def error(text):
    dlg = wx.MessageDialog(None,text,'Error',wx.OK | wx.ICON_ERROR)
    ret = dlg.ShowModal()
    dlg.Destroy()
    
class FontProperties(object):
    #---------------------------------------------------------------
    # stores the default properties for fonts
    #---------------------------------------------------------------
    # font properties
    # family constants:
    # wx.FONTFAMILY_DEFAULT, wx.FONTFAMILY_DECORATIVE, wx.FONTFAMILY_ROMAN,
    # wx.FONTFAMILY_SCRIPT, wx.FONTFAMILY_SWISS, wx.FONTFAMILY_MODERN,
    # wx.FONTFAMILY_TELETYPE
    #
    # style constants:
    # wx.FONTSTYLE_NORMAL, wx.FONTSTYLE_SLANT and wx.FONTSTYLE_ITALIC
    #
    # weight constants:
    # wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_LIGHT, wx.FONTWEIGHT_BOLD
    #
    def __init__(self):
        self.stack = []
        frame = wx.GetApp().GetTopWindow()
        conn = frame.connectToDB()
        cursor = conn.cursor()
        cursor.execute("SELECT Font_facename,Font_family,Font_style," \
                       "Font_weight,Font_size,Font_color FROM preferences WHERE user='default'")
        fields = cursor.fetchone()
        if fields:
            facename = fields[0]
            family = fields[1]
            style = fields[2]
            weight = fields[3]
            size = fields[4]
            color = fields[5]
            underline = False
            conn.close()
            self.changeFont(family,facename,size,style,weight,underline,color)
        else:
            # no data yet. write a default record
            conn.close()
            self.initializeFont()
            self.saveFont('INSERT')


    def saveFont(self, op, cond=''):
        frame = wx.GetApp().GetTopWindow()
        conn = frame.connectToDB()
        cursor = conn.cursor()
        sql = "%s preferences SET Font_facename='%s',Font_family=%s,Font_style=%s," \
              "Font_size=%s,Font_color='%s',Font_weight=%s, user='default' %s" % \
              (op,
               FontProperties.fontFacename.encode('iso-8859-15'),
               FontProperties.fontFamily,
               FontProperties.fontStyle,
               FontProperties.fontSize,
               FontProperties.fontColor.encode('iso-8859-15'),
               FontProperties.fontWeight,
               cond)
        cursor.execute(sql)
        conn.close()

    def initializeFont(self):
        self.stack = []
        # reset the font to system defaults
        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        color = wx.BLACK.GetAsString()
        self.loadFont(font, color)
        
    def loadFont(self, font, color):
        # load font parameters to class variables
        FontProperties.fontStyle = font.GetStyle()
        FontProperties.fontWeight = font.GetWeight()
        FontProperties.fontUnderline = font.GetUnderlined()
        FontProperties.fontFamily = font.GetFamily()
        FontProperties.fontSize = font.GetPointSize()
        FontProperties.fontFacename = font.GetFaceName()
        FontProperties.fontColor = color
        

    def setFont(self,other,family=None,facename=None,size=None,style=None,
                weight=None,underline=None, color=None):
        # set a font for some widget
        self.changeFont(family,facename,size,style,weight,underline,color)
        fnt = self.getFont()
        other.SetFont(fnt)

    def getFont(self):
        # return a font object from present properties
        fnt = wx.Font(pointSize=int(FontProperties.fontSize),
                      family=int(FontProperties.fontFamily),
                      style=int(FontProperties.fontStyle),
                      weight=int(FontProperties.fontWeight),
                      underline=FontProperties.fontUnderline)
        fnt.SetFaceName(FontProperties.fontFacename)
        return fnt

    def changeFont(self,family=None,facename=None,size=None,style=None,
                weight=None,underline=None, color=None):
        # change one or more font properties for future use
        if family is not None:    FontProperties.fontFamily = family
        if facename is not None:  FontProperties.fontFacename = facename
        if size is not None:      FontProperties.fontSize = size
        if style is not None:     FontProperties.fontStyle = style
        if weight is not None:    FontProperties.fontWeight = weight
        if underline is not None: FontProperties.fontUnderline = underline
        if color is not None:     FontProperties.fontColor = color

    def chooseFont(self):
        fd = wx.FontData()
        fd.SetInitialFont(self.getFont())
        fd.SetColour(FontProperties.fontColor)
        dlg = wx.FontDialog(None, fd)
        if dlg.ShowModal() == wx.ID_OK:
            newfd = dlg.GetFontData()
            color = newfd.GetColour().GetAsString()
            self.loadFont(newfd.GetChosenFont(), color)
            self.saveFont("UPDATE","WHERE user='default'")
        dlg.Destroy()

    def pushFont(self):
        # save a font on the font stack
        self.stack.append(self.getFont())

    def popFont(self):
        # pop a font from the font stack
        # (ignore stack empty error)
        try:
            font = self.stack.pop()
            color = wx.BLACK.GetAsString() # color not working yet
            self.loadFont(font, color)
        except:
            pass

    def dumpFont(self):
        print 'fontFacename='+repr(FontProperties.fontFacename)
        print 'fontFamily='+repr(FontProperties.fontFamily)
        print 'fontStyle='+repr(FontProperties.fontStyle)
        print 'fontSize='+repr(FontProperties.fontSize)
        print 'fontColor='+repr(FontProperties.fontColor)
        print 'fontWeight='+repr(FontProperties.fontWeight)

