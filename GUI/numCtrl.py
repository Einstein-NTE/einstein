from math import *

def convertDoubleToString(x,nDecimals=2,nMaxDigits=12):

    if nDecimals <> 2:
        print "convertDoubleToString: WARNING - does not work well for nDecimals <> 2"
        return "~!$@)/#$"
    
    decimalSign = '.'
    if x is None:
        return ""
    elif abs(x)>= pow(10.0,nMaxDigits):
        return "%s"%x             #aqui poner formato tipo 2.345e+07
    elif nDecimals > 0:
        if x >=0:
            integerPart = int(floor(x))
        else:
            integerPart = int(ceil(x))
        decimalPartDouble = abs((x - integerPart))*pow(10.0,nDecimals)
        decimalPart = int(floor(decimalPartDouble+0.5))
        if decimalPart < 10:
            string = "%d%s0%d"%(integerPart,decimalSign,decimalPart)
        else:
            string = "%d%s%d"%(integerPart,decimalSign,decimalPart)
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
