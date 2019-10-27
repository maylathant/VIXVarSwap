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
        lastK = 0

        self.strike2 = 0
        for sk in myskew.keys():
            optionP = self.quickCall(sk,myskew[sk],expiry/360) if sk > myspot\
                else self.quickPut(sk,myskew[sk],expiry/360)
            spacing = sk - lastK
            lastK = sk
            self.strike2 = self.strike2 +\
                optionP/(sk*sk)*spacing

        #Add discounting and scaling
        self.strike2 = 2*np.exp(self.rate*expiry/360)/(expiry/360)*self.strike2
        return self.strike2

    def getStrikeInterp(self,custExp=-1):
        '''
        Gets the strike and interpolates of maturity does not exist
        :return: The fair value varinace
        '''
        expy = self.mat if custExp == -1 else custExp #Default value for custom experation

        #Base case, no interpolation needed
        if expy in termStru: return self.getStrike(expiry=expy)


        termSize = len(termStru)

        #Find nearest terms
        neighbors = (0,0)
        for i in range(1,termSize):
            if expy < termStru[i]:
                neighbors = (termStru[i-1],termStru[i])
                break

        long = self.getStrike(expiry=neighbors[1])
        if expy < termStru[0]: #If really short dated, set fair strike to ATM IV
            temp = self.refSV.getVol('^VIX')[termStru[0]][round(self.refSV.getSpot())]
            short = temp*temp
        else:
            short = self.getStrike(expiry=neighbors[0])


        #Return an interpolation between long and short points
        self.strike2 = short*(neighbors[1]-expy)/(neighbors[1]-neighbors[0])\
            + long*(expy-neighbors[0])/(neighbors[1]-neighbors[0])
        return self.strike2

    def basePNL(self,realized,fair):
        '''
        :param realized: realized vol at maturity
        :param fair: fair strike at inception
        :return: pnl
        '''
        return 0.5*self.vega/np.sqrt(fair)*(realized*realized-fair)

    def pnlSpan(self, volRng):
        '''
        Return posible pnl values at maturity for a range of realized vol
        :param volRng (np.list float): range of possible volatilities in percent
        :return: pnl values
        '''
        if self.strike2 < 0: #Compute strike if not already done
            self.getStrikeInterp()

        return self.basePNL(volRng*100,self.strike2*10000)

    def getStrikeDer(self,vol,b=1,mat=-1):
        '''
        Get fair strike price with derman's approximation
        :param vol: Current implied volatility
        :param b: Slope of skew
        :return: fair variance strike
        '''
        mat = self.mat if mat < 0 else mat
        return vol*vol*(1 + 3*mat/360*b*b)


class ForwardVS(VarSwap):
    '''
    Foward variance swap. Subclass of VarSwap
    '''
    def __init__(self,vega,refSV,mat=30,rate=0.02,div=0.02,fwdMat=20):
        '''
        :param vega: Amount of vega notional
        :param refSV: reference data for spot and vol
        :param mat: maturity in days
        :param rate: annual interest rate
        :param div: annual dividend rate
        :param fwdMat: number of days until VS begins
        '''
        super().__init__(vega,refSV,mat=mat,rate=rate,div=div)
        self.fwdMat = fwdMat

    def getStrikeInterp(self,custExp=-1):
        '''
        :param custExp: Custom maturity
        :return: the fair squared strike for the FwdVarSwap and near/far values
        tuple ~ (near,far,fwdStrike)
        '''
        expy = self.mat if custExp == -1 else custExp  # Default value for custom experation

        near = super().getStrikeInterp(custExp=self.fwdMat)
        far = super().getStrikeInterp(custExp=self.mat)
        fairK = 1 / (expy - self.fwdMat) * (expy * far - self.fwdMat * near) * 10000
        return (near,far,fairK)









