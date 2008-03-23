from math import *

#from auxiliary import *
# changed to full path TS 12/3/2008
from einstein.auxiliary.auxiliary import * 

def createDemandAndAvailabCurves():
    global T, QDh, QAh, QDa, QAa

    #define the temperature range for the hot (QD) and cold (QA) cureves 
    #T = range(0.0,405.0,5.0) # changed to 'frange' TS 12/3/2008
    T = frange(0.0, 405.0, 5.0)

    #Create an hourly heat demand curve 1
    #create an empty hot hourly curve in the range of temperature, filled with '0.0'
    QDh1 = []
    for i in T:
        QDh1.append(0.0)
    #fill the QDh1 with values
    for i in range(len(T)):
        if T[i]<=200.0:
            if T[i]>=35.0:
                QDh1[i]=QDh1[i-1]+100.0

    last1=last_filled(QDh1)
    #print 'last1=',last1

    for i in range(len(T)):
        if i>last1:
            QDh1[i]=QDh1[last1]


    #Create an hourly heat demand curve 2
    #create an empty hot hourly curve in the range of temperature, filled with '0.0'
    QDh2 = []
    for i in T:
        QDh2.append(0.0)
    #fill the QDh2 with values
    for i in range(len(T)):
        if T[i]<=160.0:
            if T[i]>=40.0:
                QDh2[i]=QDh2[i-1]+ 50.0

    last2=last_filled(QDh2)
    #print 'last2=',last2

    for i in range(len(T)):
        if i>last2:
            QDh2[i]=QDh2[last2]

    #Create an hourly heat demand curve 3
    #create an empty hot hourly curve in the range of temperature, filled with '0.0'
    QDh3 = []
    for i in T:
        QDh3.append(0.0)
    #fill the QDh3 with values
    for i in range(len(T)):
        if T[i]<=220.0:
            if T[i]>=120.0:
                QDh3[i]=QDh3[i-1]+ 50.0

    last3=last_filled(QDh3)
    #print 'last3=',last3

    for i in range(len(T)):
        if i>last3:
            QDh3[i]=QDh3[last3]

    #Create an hourly heat availability curve 1
    QAh1 = []
    for i in T:
        QAh1.append(0.0)
    #fill the QAh1 with values
    for i in range(len(T)):
        if T[i]==5.0:
            QAh1[i] = 1500.0
        if T[i]>=10.0:
            if T[i]<=40.0:
                QAh1[i]=QAh1[i-1]-200.0

    QAh1[0]=1500.0

    #Create an hourly heat availability curve 2
    QAh2 = []
    for i in T:
        QAh2.append(0.0)
    #fill the QAh2 with values
    for i in range(len(T)):
        if T[i]==10.0:
            QAh2[i] = 800.0
        if T[i]>10.0:
            if T[i]<=35.0:
                QAh2[i]=QAh2[i-1]-100.0

    QAh2[0]=800.0; QAh2[1]=800.0

    #Create an hourly heat availability curve 3
    QAh3 = []
    for i in T:
        QAh3.append(0.0)

    #Create an annual heat demand and availability curves (summing the hourly curves), 3 hour year supposed for checking
    QDa = []
    QAa = []
    for i in T:
        QDa.append(0.0)
        QAa.append(0.0)
    for i in range(len(T)):
        QDa[i] = QDh1[i] + QDh2[i] + QDh3[i] #summing the hourly demand to obtain the annual demand curve
        QAa[i] = QAh1[i] + QAh2[i] + QAh3[i]

    QDh = [QDh1, QDh2, QDh3]
    QAh = [QAh1, QAh2, QAh3]


if __name__ == "__main__":
    # for testing purposes only
    # should be called:
    # python demand_curves.py
    global T, QDh, QAh, QDa, QAa
    createDemandAndAvailabCurves()
    print "T=" + repr(T)
