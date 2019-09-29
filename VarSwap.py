import utils as util
import numpy as np
from statics import termStru

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
        self.quickCall = lambda K,v,t:\
            util.BSCall(spot=self.refSV.getSpot(), strike=K, div=self.div, rate=self.rate, vol=v, time=t)
        self.quickPut = lambda K,v,t: \
            util.BSPut(spot=self.refSV.getSpot(), strike=K, div=self.div, rate=self.rate, vol=v, time=t)

    def getStrike(self,expiry=-1):
        '''
        Compute the fair stike of the varinace swap
        Defaults to VIX for ATM vol (should be changed)
        :param expiry (double): time to maturity in days
        :return: The fair variance strike
        '''
        if expiry == -1: expiry = self.mat
        myskew = self.refSV.getVol('^VIX')[expiry]
        myspot = self.refSV.getSpot()
        spacing = self.refSV.strikedist

        self.strike2 = 0
        for sk in myskew.keys():
            optionP = self.quickCall(sk,myskew[sk],expiry/360) if sk > myspot\
                else self.quickPut(sk,myskew[sk],expiry/360)
            self.strike2 = self.strike2 +\
                optionP/(sk*sk)*spacing

        #Add discounting and scaling
        self.strike2 = 2*np.exp(self.rate*expiry/360)/(expiry/360)*self.strike2
        return self.strike2

    def getStrikeInterp(self):
        '''
        Gets the strike and interpolates of maturity does not exist
        :return: The fair value varinace
        '''
        #Base case, no interpolation needed
        if self.mat in termStru: return self.getStrike()


        termSize = len(termStru)

        #Find nearest terms
        neighbors = (0,0)
        for i in range(1,termSize):
            if self.mat < termStru[i]:
                neighbors = (termStru[i-1],termStru[i])
                break

        long = self.getStrike(expiry=neighbors[1])
        if self.mat < termStru[0]: #If really short dated, set fair strike to ATM IV
            temp = self.refSV.getVol('^VIX')[termStru[0]][round(self.refSV.getSpot())]
            short = temp*temp
        else:
            short = self.getStrike(expiry=neighbors[0])


        #Return an interpolation between long and short points
        self.strike2 = short*(neighbors[1]-self.mat)/(neighbors[1]-neighbors[0])\
            + long*(self.mat-neighbors[0])/(neighbors[1]-neighbors[0])
        return self.strike2

    def basePNL(self,realized,fair):
        '''
        :param realized: realized vol at maturity
        :param fair: fair strike at inception
        :return: pnl
        '''
        return 0.5*self.vega/fair*(realized*realized-fair)*100

    def pnlSpan(self, volRng):
        '''
        Return posible pnl values at maturity for a range of realized vol
        :param volRng (np.list float): range of possible volatilities
        :return: pnl values
        '''
        if self.strike2 < 0: #Compute strike if not already done
            self.getStrikeInterp()

        return self.basePNL(volRng,self.strike2)











