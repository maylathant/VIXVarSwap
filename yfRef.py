import yfinance as yf
from statics import termStru
import numpy as np

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

    def setSpot(self):
        '''
        :return: void, sets self.spot price to spot of self.mydate
        '''
        self.spot = yf.download([self.undl],start=self.mydate,end=self.mydate)['Close'][0]
        return self.spot

    def getSpot(self):
        '''
        return spot price of underling index or share
        :return: float spot price
        '''
        return self.spot if self.spot > 0 else self.setSpot()

    def computeSkew(self,myvol,scale=0.1):
        '''
        :param myvol: integer ATM volatility parameter
        :param scale: scale to determine convexity
        :return: dictionary with strikes and implied volatilities
        models the skew as scale*(skewVol - ATMvol)^2 + ATMvol as strike changes
        models term structure as sqrt(IV/10) - 2
        ***Crude model***
        '''
        downside = lambda x: 10 if x < myvol else 1 #Make downside ten times more convex
        myskew = lambda x: downside(x)*scale*(x-myvol)**2 + myvol #Function to model skew
        myterm = lambda x: np.sqrt(x/10) - 2 #Function to model term structure
        self.vol = {}
        for t in termStru:
            self.vol[t] = {}
            for i in range(1, 41):
                temp = myskew(i*myvol*0.05) #Obtain skew for 1m maturity
                self.vol[t][i*self.spot*0.05] = (temp + myterm(t))/100 #Apply term structure effect and put in percent
        self.strikedist = self.spot*0.05
        return self.vol

    def setVolIdx(self,volidx,scale):
        '''
        :param volidx (string): Name of a vol index for which to base the skew
        :param scale (double): Scaling factor for vol skew
        :return: The skew with the volidx being the ATM point
        spaced apart by 1% of the underlying
        '''
        myvol = yf.download([volidx],start=self.mydate,end=self.mydate)['Close'][0]
        return self.computeSkew(myvol,scale)

    def getVol(self,volidx,scale=0.05):
        '''
        :return: The vol surface in dictionary form
        '''
        return self.vol if len(self.vol) > 0 else self.setVolIdx(volidx,scale)