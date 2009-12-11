#!/usr/bin/env python

#   This program is free software: you can redistribute it or modify it under
#   the terms of the GNU general public license as published by the Free
#   Software Foundation (www.gnu.org).

#   Andreas Hirczy <ahi@itp.tugraz.at>, 2008

import sys
from einstein.modules.messageLogger import *

class CashFlow:
    def __init__(self, maxYears, interestRate, energyPrizeRate):
        '''init

        input:   maxYears - number of years to look in the future
        input:   interestRate - interest corrected by inflation
        input:   energyPrizeRate - prize development for energy
        returns: a object of type CashFlow'''
        self.maxYear         = maxYears
        self.rateInterest    = interestRate/100.0
        self.rateEnergyPrize = energyPrizeRate/100.0
        self.cashflow = [0.0] * self.maxYear 
        
    def Investment(self, year, value):
        '''insert a singular payment or income

        input:   year - year in which payment is due
        input:   value - height of payment - expenses are negative, income is positive
        returns: nothing'''
        year  = int(year)
        value = float(value)
        if year > self.maxYear:
            print >> sys.stderr, "CashFlow/Investment: year %d exceeds range (0-%d)" % (year, self.maxYear)
        else:
            self.cashflow[year] += value

    def Contingency(self, from_year, value):
        '''insert periodic payments from a ertain year onwards

        input:   from_year - year starting the payment
        input:   value - height of payment - expenses are negative, income is positive
        returns: nothing'''
        year  = int(from_year)
        value = float(value)
        if year > self.maxYear:
            print >> sys.stderr, "CashFlow/Contingency: year %d exceeds range (0-%d)" % (year, self.maxYear)
        else:
            for i in xrange(year, self.maxYear):
                self.cashflow[i] += value
                
    def Operating(self, value):
        '''operating costs (same as Contingency, always starting in year one)

        input:   value - height of payment - expenses are negative, income is positive
        returns: nothing'''
        value = float(value)
        self.Contingency(1,value)

    def Energy(self, value):
        '''Energie costs, similar to operating costs, but prize development is different
        and usuall bigger

        input:   value - height of payment - expenses are negative, income is positive
        returns: nothing'''
        value = float(value)
        for i in xrange(1, self.maxYear):
            self.cashflow[i] += value * pow(1+self.rateEnergyPrize, i-1)

    def CF(self):
        '''cash flow as calculated till now
        
        returns: cash flow (array, on entry per year)'''
        return self.cashflow[:]
        
    def Print(self):
        '''Pretty print the cash flow as calculated till now
        returns: nothing'''
        print
        for i in xrange(len(self.cashflow)):
            print "%3d --> % 13.2f" % (i, self.cashflow[i])
        print

def NPV(cf_new, cf_old, rate):
    '''NPV -- net present value
    http://en.wikipedia.org/wiki/Net_present_value
    
    input:   cf_new - cash flow of new process
    input:   cf_old - cash flow of old process
    input:   rate - net interest (scalar), in percent
    returns: npv - net present value (array, on entry per year)'''
    rate = rate/100.0
    sum = 0.0
    assert len(cf_new) == len(cf_old)
    npv = [0.0] * len(cf_new)
    for i in xrange(0,len(cf_new)):
        sum += (cf_new[i] + cf_old[i])*pow(1 + rate, -i)
        npv[i] = sum
        #print i, (cf_new[i] - cf_old[i]) * pow(1 + rate, -i),  sum
    return npv[:]

def NPVcf(cf, rate):
    #print "cf-------"
    #print cf
    '''NPV -- net present value
    http://en.wikipedia.org/wiki/Net_present_value
    
    input:   cf - net cash flow (old process - new process)
    input:   rate - net interest (scalar), in percent
    returns: npv - net present value (array, on entry per year)'''
    rate = rate/100.0
    sum = 0.0
    npv = [0.0] * (len(cf))
    for i in xrange(len(cf)):
        sum += cf[i] * pow(1 + rate, -i)
        npv[i] = sum
    return npv


def payback_period(npv):
    '''payback period
    
    input:   npv -- net present value (array, one entry for every year)
    returns: payback period (scalar)'''
    frac=0;
    i=0.0;
    # find interval where sign changes and interpolate linear    
    for i in xrange(0,len(npv)-1):
        if 0.0 >= npv[i]*npv[i+1]:
            try: frac = abs(npv[i])/abs(npv[i+1]-npv[i])
            except ZeroDivisionError: 
                frac=0
                logWarning(_("Could not calculate payback period. NPV is zero."))
            break
    return i+frac


def MIRR(cf_new, cf_old, financeRate, reinvestRate):
    '''MIRR -- modified internal rate of return
    http://en.wikipedia.org/wiki/Modified_Internal_Rate_of_Return
    http://en.wikipedia.org/wiki/Internal_rate_of_return
    http://www.visitask.com/internal-rate-of-return.asp

    input:   cf_new - cost of old process (array, one entry for every year)
    input:   financeRate (scalar, percent)
    input:   reinvestRate (scalar, percent)
    returns: mirr (array, one entry for every year)'''
    #print "mirr calculation-----"
    #print cf_new
    #print cf_old
    #print financeRate
    #print reinvestRate
    assert len(cf_new) == len(cf_old)    
    cf_pos = [0.0] * (len(cf_new))
    cf_neg = [0.0] * (len(cf_new))
    mirr   = [0.0] * (len(cf_new))
    fv1    = [0.0] * (len(cf_new))

    financeRate  = financeRate/100.0
    reinvestRate = reinvestRate/100.0

    # separate positive and negative periods of cash flow
    for i in xrange(0, len(cf_new)):
        cFlow = cf_old[i] + cf_new[i]
        if (cFlow >= 0):
            cf_pos[i] = cFlow
        else:
            cf_neg[i] = cFlow
    #print "CF possitive:  "
    #print cf_pos
    #print "CF negative:   "
    #print cf_neg
        
    # calculate their future value and net present valuse
    for i in xrange(1, len(cf_new)):
        fv1[i] = 0.0
        for j in xrange (i):
            fv1[i]+= cf_pos[j+1]*pow(1.0+ reinvestRate,i-j-1)

            #print j, "cf possitive j:   ", cf_pos[j]
        #print i, "fv1:  ", fv1[i]

        npv2 = NPVcf(cf_neg, financeRate)
        #print i, "npv2:   ", npv2[i]

    # and sum up with their respective interest rates
    for i in xrange(1, len(cf_new)):
        try:
            mirr[i] = pow(fv1[i]/(-npv2[i]),1.0/i) - 1.0
        except:
            mirr[i] = 0.0

    return mirr                 


    

def BCR(cf_new, cf_old, interest):
    '''benefit cost ratio
    http://en.wikipedia.org/wiki/Benefit-cost_ratio
    
    input:   cf_new -- new cost (array, one entry for every year)
    input:   cf_old -- old cost (array, one entry for every year)
    input:   interest - discount rate (scalar)
    returns: bcr (array, one entry for every year)'''
    assert len(cf_new) == len(cf_old)
    interest = interest/100.0
    
    sum_old = 0.0;
    sum_new = 0.0;
    bcr = [0.0] * len(cf_new)
    for i in xrange(len(cf_new)):
        sum_old += cf_old[i] * pow(1.0 + interest, -i)
        sum_new += cf_new[i] * pow(1.0 + interest, -i)
        try: bcr[i] = -sum_old / sum_new
        except ZeroDivisionError: 
            bcr[i] = 1e300000
            logWarning(_("Could not calculate BCR."))
    return bcr
        

def ANNUITY(I0,r,N):
    #Total Investment Capital
    #real interest rate of external financing
    #ProjectLifetime
    if (I0==0)or(N==0):
        return 0.0
    
    r = r / 100.0
    #print "ANNUITY I0=%s r=%s N=%s" %(I0,r,N)
    sum = 0
    try:
        for i in xrange(1,N+1):
            sum+=1.0/pow(1+r,i)
        a = 1.0 / sum
        A = a * I0
    except ZeroDivisionError:
        logWarning(_("Could not calculate annuity period."))
        return 0.0
    #print "a=%s" % (a)
    #print "A=%s" % (A)
    return A





#################
## MAIN - for testing only
#################

if __name__ == "__main__":
    from pylab import *

    a = CashFlow(30, 5, 3) # max_years, interest rate (inflation - net interest), energie prize development
    a.Investment(0,-180000*0.7)         # investment WT (<invcost>)  (- 30 % funding)
    a.Investment(0,-50000*0.8)          # investment biomass boiler (- 20 % funding)
    a.Investment(0,-400000*0.7+5000)   # investment solarthermal (- 30 % funding, 5000 funding)
    a.Investment(0, 50000*5/20*0.5)    # sale boiler (<residual_value>) AFA: 5 years out of 20 years depracation left
    a.Energy(-3200000*0.051) # energy price (eg. fossil gas) (<energy_demands>)
    a.Operating(-5000)       # operating costs, material maintance
    a.Operating(-800)        # operating costs, 
    a.Operating(-3000)       # operating costs,
    a.Operating(-1000)       # operating costs, 
    a.Investment(4,-30000)     # (<non_recurring_costs>) permits
    a.Contingency(5, 20000)  # zzz
    #a.Print()
    #arrayA = a.CF()          # get cash flow as an array of floats
    #print len(arrayA)

    # old CashFlow to compare with
    b = CashFlow(30, 5, 3)
    b.Energy(-5000000*0.051) # more energy
    b.Operating(-4000)       # operating costs, materials, maintainance and service
    b.Operating(-2000)       # operating costs, materials, maintainance and service
    b.Operating(-400)      # operating costs, wages, operating personal
    b.Investment(1,-4000)    # (<non_recurring_costs>) repair for energy equipment
    b.Investment(4,-50000)   # (<non_recurring_costs>) fines/penalties
    b.Contingency(5, -3000)  # xxx
    #b.Print()
    
    print "CF new:  ", a.CF()
    print "CF old:  ", b.CF()
    
    print
    npv = NPV(a.CF(), b.CF(), 5)       # call with <InterestRate>?
    print "NPV: ", npv
    print "PBP: ", payback_period(npv)
    plot(npv)
    xlabel('time / Y')
    ylabel('NPV / EUR')
    title('net present value')
    grid(True)
    show()

    print
    mirr = MIRR(a.CF(), b.CF(), 5, 6) # call with <InterestRate>, <basDiscountRate>
    print "MIRR:", mirr     
    figure(2)
    plot(mirr)
    xlabel('time / Y')
    ylabel('MIRR')
    title('modified internal rate of return')
    grid(True)
    show()

    bcr = BCR(a.CF(), b.CF(), 5) # call with <InterestRate>?
    print
    print "BCR: ", bcr
    figure(3)
    plot(bcr)
    xlabel('time / Y')
    ylabel('BCR')
    title('benefit cost ratio')
    grid(True)
    show()

    print
    raw_input('Press any key to continue.')
    close('all')
    
        
