import yfinance as yf
from statics import termStru
import numpy as np
import pandas as pd

class yfRef:
    '''
    Class to handle yahoo finance reference data for a single underlying
    '''
    def __init__(self,mydate,undl):
        '''
        :param mydate: string in YYYY-MM-DD format
        :param undl: string underling name
        '''
        self.mydate = mydate
        self.undl = undl
        self.spot = -1
        self.vol = {}
        self.strikedist = -1 #Distance between strikes in the skew
        self.setSpot()
        self.spotHist = pd.Series()
        self.volHist = pd.Series()

    def setSpot(self,spotDate=''):
        '''
        :param spotDate (string date):
        :return: void, sets self.spot price to spot of self.mydate
        '''
        spotDate = self.mydate if spotDate == '' else spotDate
        self.spot = yf.download([self.undl],start=spotDate,end=spotDate)['Close'][0]
        return self.spot

    def setSpotHist(self,start,end):
        '''
        Get history of daily spot prices
        :param start: start date
        :param end: end date
        :return: Series of spot prices
        '''
        self.spotHist = yf.download([self.undl],start=start,end=end)['Close']
        return self.spotHist

    def getSpotHist(self,start,end):
        '''
        Get history of daily spot prices
        :param start: start date
        :param end: end date
        :return: Series of spot prices
        '''
        if len(self.spotHist) < 1:
            self.spotHist = yf.download([self.undl],start=start,end=end)['Close']
        return self.spotHist

    def setVolHist(self,start,end,name='^VIX'):
        '''
        Get history of daily spot prices and set to self variable
        :param start: start date
        :param end: end date
        :param name: Name of volatility parameter
        :return: Series of vol prices
        '''
        self.volHist = yf.download([name],start=start,end=end)['Close']
        return self.volHist

    def getVolHist(self,start,end,name='^VIX'):
        '''
        Get history of daily spot prices
        :param start: start date
        :param end: end date
        :param name: Name of volatility parameter
        :return: Series of vol prices
        '''
        if len(self.volHist) < 1:
            self.volHist = yf.download([name],start=start,end=end)['Close']
        return self.volHist

    def getSpot(self):
        '''
        return spot price of underling index or share
        :return: float spot price
        '''
        return self.spot if self.spot > 0 else self.setSpot()

    def computeSkew(self,myvol,scale=0.02):
        '''
        :param myvol: integer ATM volatility parameter
        :param scale: scale to determine convexity
        :return: dictionary with strikes and implied volatilities
        models the skew as scale*(skewVol - ATMvol)^2 + ATMvol as strike changes
        models term structure as sqrt(IV/10) - 2
        ***Crude model***
        '''
        downside = lambda x: 2.5 if x < myvol else 1 #Make downside ten times more convex
        myskew = lambda x: downside(x)*scale*(x-myvol)**2 + myvol #Function to model skew
        myterm = lambda x: np.sqrt(x/10) - 2 #Function to model term structure
        self.vol = {}
        for t in termStru:
            self.vol[t] = {}
            for i in range(1, 41):
                temp = myskew(i*myvol*0.05) #Obtain skew for 1m maturity
                self.vol[t][round(i*self.spot*0.05)] = (temp + myterm(t))/100 #Apply term structure effect and put in percent
        self.strikedist = self.spot*0.05
        return self.vol

    def setVolIdx(self,volidx,scale,voldate=''):
        '''
        :param volidx (string): Name of a vol index for which to base the skew
        :param scale (double): Scaling factor for vol skew
        :param voldate (string date): Date to pull volatility
        :return: The skew with the volidx being the ATM point
        spaced apart by 1% of the underlying
        '''
        voldate = self.mydate if voldate == '' else voldate
        myvol = yf.download([volidx],start=voldate,end=voldate)['Close'][0]
        return self.computeSkew(myvol,scale)

    def getVol(self,volidx,scale=0.02, voldate=''):
        '''
        :return: The vol surface in dictionary form
        '''
        return self.vol if len(self.vol) > 0 and (voldate == '')\
            else self.setVolIdx(volidx,scale,voldate)