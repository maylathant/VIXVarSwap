import utils as util
import numpy as np

class VarSwap:
    '''
    Class to price and model a variance swap
    '''
    def __init__(self,vega,refSV,mat=30,rate=0.02,div=0.02):
        '''
        :param vega: Amount of vega notional
        :param refSV: reference data for spot and vol
        :param mat: maturity in days
        :param rate: annual interest rate
        :param div: annual dividend rate
        '''
        self.vega = vega
        self.refSV = refSV
        self.mat = mat
        self.rate = rate
        self.div = div
        self.strike2 = -1 #Variance strike

        #Shortcuts for vanilla option integral
        self.quickCall = lambda K,v:\
            util.BSCall(spot=self.refSV.getSpot(), strike=K, div=self.div, rate=self.rate, vol=v, time=self.mat/360)
        self.quickPut = lambda K,v: \
            util.BSPut(spot=self.refSV.getSpot(), strike=K, div=self.div, rate=self.rate, vol=v, time=self.mat/360)

    def getStrike(self):
        '''
        Compute the fair stike of the varinace swap
        Defaults to VIX for ATM vol (should be changed)
        :return: The fair variance strike
        '''
        myskew = self.refSV.getVol('^VIX')[self.mat]
        myspot = self.refSV.getSpot()
        spacing = self.refSV.strikedist

        self.strike2 = 0
        for sk in myskew.keys():
            optionP = self.quickCall(sk,myskew[sk]) if sk > myspot\
                else self.quickPut(sk,myskew[sk])
            self.strike2 = self.strike2 +\
                optionP/(sk*sk)*spacing

        #Add discounting and scaling
        self.strike2 = 2*np.exp(self.rate*self.mat/360)/(self.mat/360)*self.strike2
        return self.strike2






