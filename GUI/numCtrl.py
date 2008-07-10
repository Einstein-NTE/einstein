from math import *

def convertDoubleToString(x,nDecimals=2,nMaxDigits=12):

    if nDecimals > 6:
        print "convertDoubleToString: WARNING - does not work well for nDecimals > 6"
        return "~!$@)/#$"

    decimalSign = '.'
#None's to blank space

    if x is None:
        return ""

#before continuing, assure that it's really a number
    try:
        xfloat = float(x)
        x = xfloat
    except:
        print "numCtrl: seems to be a string"
        return str(x)
    
#x is ok, now check the number of decimals ...
    if nDecimals > 6:
        print "convertDoubleToString: WARNING - does not work well for nDecimals > 6"
        return "~!$@)/#$"

    decimalSign = '.'

#... and go ahead
    
    if abs(x)>= pow(10.0,nMaxDigits):
        return "%s"%x             #aqui poner formato tipo 2.345e+07
    elif nDecimals > 0:
        x += 0.5 * pow(10.,-(nDecimals))    #rounding ...
        if x >=0:
            integerPart = int(floor(x))
        else:
            integerPart = int(ceil(x))
        decimalPartDouble = abs((x - integerPart))*pow(10.0,nDecimals)
        decimalPart = int(floor(decimalPartDouble))

        string = "%d"%decimalPart
        if decimalPart < 10:
            for i in range(nDecimals-1):
                newstring = "0%s"%string
                string = newstring
        elif decimalPart < 100:
            for i in range(nDecimals-2):
                newstring = "0%s"%string
                string = newstring
        elif decimalPart < 1000:
            for i in range(nDecimals-3):
                newstring = "0%s"%string
                string = newstring
        elif decimalPart < 10000:
            for i in range(nDecimals-4):
                newstring = "0%s"%string
                string = newstring
        elif decimalPart < 100000:
            for i in range(nDecimals-5):
                newstring = "0%s"%string
                string = newstring
        elif decimalPart < 1000000:
            for i in range(nDecimals-6):
                newstring = "0%s"%string
                string = newstring
        newstring = "%d%s%s"%(integerPart,decimalSign,string)
        string = newstring
        return string
    else :
        if x >=0:
            integerPart = int(floor(x + 0.5))
        else:
            integerPart = int(ceil(x - 0.5))
        string = "%d"%(integerPart)
        return string
    
if __name__ == "__main__":
    x = -17.389
    print x
    print convertDoubleToString(x,0)
    print convertDoubleToString(x,1)
    print convertDoubleToString(x,2)
    print convertDoubleToString(x,3)
    print convertDoubleToString(x,4)
