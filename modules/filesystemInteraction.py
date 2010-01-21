import os
import wx

#------------------------------------------------------------------------------
def saveFigure(figure, filename):
#------------------------------------------------------------------------------
    try:
        figure.savefig(filename, dpi=200, format='png')
    except:
        print "could not save", filename
        pass
    

#------------------------------------------------------------------------------
def loadToPanel(panel, filename):
#------------------------------------------------------------------------------
    try:
        image = wx.Image(filename, type = wx.BITMAP_TYPE_ANY)
        client_size = panel.GetClientSize()
        scaled_image = image.Scale(client_size[0], client_size[1], wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.BitmapFromImage(scaled_image)
        wx.StaticBitmap(panel, wx.ID_ANY, bitmap)
    except:
        print "could not load", filename
        pass
    

#------------------------------------------------------------------------------
def deleteFileWithoutPrompt(filename):
#------------------------------------------------------------------------------
    try:
        os.remove(filename)
    except:
        print "could not remove", filename
        pass
    
