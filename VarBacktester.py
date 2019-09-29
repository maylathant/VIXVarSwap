from yfRef import yfRef
import numpy as np
from VarSwap import VarSwap
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
        retHist = self.myRef.getSpotHist(self.start,self.end).pct_change()[1:]
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