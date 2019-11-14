from yfRef import yfRef
import numpy as np
from VarSwap import VarSwap, ForwardVS
import datetime as dt

class VarBacktester:
    '''
    Class to handle backtesting of Varswap strategies
    '''
    def __init__(self,start,end,undl):
        self.start = start
        self.end = end
        convST = lambda x : dt.datetime.strptime(x, '%Y-%m-%d')
        self.duration = (convST(end) - convST(start)).days
        self.myRef = yfRef(mydate=start,undl=undl)
        self.myRef.getSpotHist(start=start,end=end)
        self.myRef.getVol('^VIX',voldate=start)
        self.strike0 = VarSwap(1,self.myRef,mat=self.duration).getStrikeInterp() #Initial strike
        self.realized = {} #Realized variance of the backtest
        self.fairStrike = {} #Fair strikes in the backtest
        self.valuation = {} #valuation for the backtest

    def runBacktest(self):
        '''
        Execute baseline backtesting
        :return: realized variance for each day
        '''
        retHist = self.myRef.setSpotHist(self.start,self.end).pct_change()[1:]
        days = list(retHist.index)
        retHist = np.array(retHist)
        dura = len(days)
        realized = {}
        fairStrike = {}
        valuation = {}
        for i,day in zip(range(1,dura+1),days): #Loop through each day
            realized[day] = np.var(retHist[:i])*252
            self.myRef.setSpot(spotDate=day.strftime("%Y-%m-%d"))
            self.myRef.getVol('^VIX',voldate=day.strftime("%Y-%m-%d"))
            remain = (days[-1]-day).days #Remaining days
            fairStrike[day] = VarSwap(1,self.myRef,mat=remain).getStrikeInterp()
            valuation[day] = 1/self.duration*((self.duration-remain)*(realized[day]-self.strike0)\
                + remain*(fairStrike[day]-self.strike0))*10000
        self.realized = realized
        self.fairStrike = fairStrike
        self.valuation = valuation


        #Reset ref data
        self.myRef.setSpot()
        self.myRef.getVol('^VIX',voldate=self.start)

        return (self.realized, self.fairStrike)

    def btVSFoward(self,fwdStart):
        '''
        Compute dynamics of holding a forward variance swap until maturity
        :param fwdStart (string): Start date of Variance swap
        :return: near/far variance and valuation in a tuple
        Only computes up to forward start date
        '''
        #Check fwdStart is less than maturity
        dtend = dt.datetime.strptime(self.end, '%Y-%m-%d')
        dtfwd = dt.datetime.strptime(fwdStart, '%Y-%m-%d')
        if (dtend - dtfwd).days < 0:
            raise ValueError("VarSwap matures on " + self.end\
                             + " but starts on " + fwdStart)

        days = list(self.myRef.setSpotHist(self.start, fwdStart)[1:].index) #get trading days
        dura = len(days) #Time until start date
        near = {}
        far = {}
        Kt = {}
        remainSt = (days[-1] - days[0]).days + 1  # Remaining days until VS begins
        remainEd = (dt.datetime.strptime(self.end, '%Y-%m-%d') - days[0]).days + 1  # Remaining days until maturity
        k0 = ForwardVS(1,self.myRef,mat=remainEd,fwdMat=remainSt).getStrikeInterp()[2]
        for i, day in zip(range(1, dura + 1), days):  # Loop through each day
            self.myRef.getVol('^VIX', voldate=day.strftime("%Y-%m-%d"))
            remainSt = (days[-1] - day).days  # Remaining days until VS begins
            remainEd = (dt.datetime.strptime(self.end, '%Y-%m-%d') - day).days  # Remaining days until VS expires
            near[day], far[day], Kt[day]\
                = ForwardVS(1,self.myRef,mat=remainEd,fwdMat=remainSt).getStrikeInterp()

        self.valuation = {k:Kt[k]-k0 for k in Kt} #Adjust for fair strike

        # Reset ref data
        self.myRef.getVol('^VIX', voldate=self.start)

        return (near, far, self.valuation)

    def btShortVarRoll(self,vsTerm=30):
        '''
        Computes the dynamics of a strategy that repeatedly rolls short variance swaps
        :param vsTerm: (int) Number of days in rolling variance swap
        :return: tuple of (realized, fairstrike, valuation)
        '''

        retHist = self.myRef.setSpotHist(self.start, self.end).pct_change()[1:]
        days = list(retHist.index)
        retHist = np.array(retHist)
        dura = len(days)
        self.realized = {}; self.fairStrike = {}; self.valuation = {}
        strikeLast = VarSwap(1, self.myRef, mat=vsTerm).getStrikeInterp()
        beginIdx = 0; cummu = 0 #cummulative amount from previous varswaps
        for i, day in zip(range(1, dura + 1), days):  # Loop through each day
            if i%vsTerm == 0:
                beginIdx = vsTerm + beginIdx #Increment index for realized computation
                strikeLast = VarSwap(1, self.myRef, mat=vsTerm).getStrikeInterp() #Restrike new swap
                cummu = cummu + self.valuation[days[days.index(day)-1]] #Add on pnl from last variance swap
            self.realized[day] = np.nan_to_num(np.var(retHist[beginIdx:i]) * 252)
            self.myRef.setSpot(spotDate=day.strftime("%Y-%m-%d"))
            self.myRef.getVol('^VIX', voldate=day.strftime("%Y-%m-%d"))
            remain = vsTerm - i%vsTerm  # Remaining days
            self.fairStrike[day] = VarSwap(1, self.myRef, mat=remain).getStrikeInterp()
            self.valuation[day] = -1 / vsTerm * ((vsTerm - remain) * (self.realized[day] - strikeLast) \
                                + remain * (self.fairStrike[day] - strikeLast)) * 10000 + cummu

        # Reset ref data
        self.myRef.setSpot()
        self.myRef.getVol('^VIX', voldate=self.start)

        return (self.realized, self.fairStrike, self.valuation)