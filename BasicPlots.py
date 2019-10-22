'''
Store scripts to generate basic plots for VarSwaps
'''

from VarSwap import VarSwap
import numpy as np
from yfRef import yfRef
import utils
import matplotlib.pyplot as pyplot
from matplotlib import colors as mcolors
from sklearn.metrics import r2_score
from scipy.stats import pearsonr

def plotVSOptionPayoff():
    '''
    Plot variance swap payoff vs option payoff against implied vol
    :return:
    '''
    myTic = '^GSPC'
    myVolIdx = '^VIX'
    vegaNot = 513000
    volstrike = 0.2055
    startDate = '2019-06-20'

    myRef = yfRef(mydate=startDate,undl=myTic)
    myRef.getVol(myVolIdx,voldate=startDate)


    #Create varswap to check payoff grid
    volgrid = np.linspace(0.00001,0.4,200)
    volswp = np.linspace(0,40,200)*0.513 -volstrike*vegaNot/10000
    mySwap = VarSwap(vegaNot,myRef)
    mySwap.strike2 =volstrike*volstrike
    pnlRng = mySwap.pnlSpan(volgrid)

    #Get PNL range for option with similar parameters
    pnlOp = np.nan_to_num(utils.BSPut(vol=volgrid)*1.5)

    ##################################################
    ####### Plot VarSwap PNL Against Option ##########
    ##################################################
    pyplot.plot(volgrid,pnlRng/1000000,color='k',label='Variance Swap Payoff')
    pyplot.plot(volgrid,pnlOp,color=mcolors.CSS4_COLORS['maroon'], label='Vanilla Call Value')
    pyplot.plot(volgrid,volswp,color=mcolors.CSS4_COLORS['indianred'],label='Volatility Swap Payoff')
    pyplot.scatter(volstrike,0,color='r',label='Variance Swap Strike')
    pyplot.xlabel('Volatility')
    pyplot.ylabel('PnL (MEUR)')
    pyplot.legend()
    pyplot.savefig('vsopPNL.pdf')
    pyplot.show()


def volVolRealized(myTic = '^STOXX50E',windowvol = 22,windowvv = 252,startDate = '1990-06-25',endDate = '2006-10-06'):

    myRef = yfRef(mydate=startDate,undl=myTic)
    volR = myRef.getRealized(startDate,endDate,windowvol)
    vvR = myRef.getRealizedVV(startDate,endDate,windowvol=windowvol,windowvv=windowvv)

    ############################################################
    ##########  Plot Realized Vol of Vol Against Other stuff ###
    ############################################################
    pyplot.plot(volR.index,volR,color='r',label=str(windowvol) + 'd Realized Vol')
    pyplot.plot(vvR.index,vvR,color='k',label='Std of Realized Vol (Annualized)')
    pyplot.legend()
    pyplot.show()


def volSpotCorr(startDate = '2018-10-03',endDate = '2019-10-08',myTic = '^GSPC',window = 25):
    myRef = yfRef(mydate=startDate,undl=myTic)
    volR = myRef.getRealized(startDate,endDate,window)
    mySpot = myRef.setSpotHist(startDate,endDate)



    pyplot.scatter(mySpot,volR,color=['r','k'])
    z = np.polyfit(mySpot,volR,1)
    p = np.poly1d(z)
    pyplot.plot(mySpot,p(mySpot),color='k' ,label='Trend, R^2 = ' + str(round(r2_score(volR,p(mySpot)),4)))
    pyplot.xlabel('S&P 500 Spot')
    pyplot.ylabel(str(window) + 'd Realized S&P 500 Vol')
    pyplot.legend()
    pyplot.savefig('Artifacts\spotVol.pdf')
    pyplot.show()



def plotMeanRev(startDate = '2018-10-19',endDate = '2019-10-21',myTic = '^GSPC',winvol = 22):
    '''
    Plot historical realized against the average
    '''
    myRef = yfRef(mydate=startDate,undl=myTic)
    volR = myRef.getRealized(startDate,endDate,winvol)
    pyplot.plot(volR.index, volR, color='r', label=str(winvol) + 'd Realized Vol SP500')
    pyplot.plot(volR.index, np.ones(len(volR))*np.mean(volR), color='k', label='Average')
    pyplot.legend()
    pyplot.savefig('meanRev.pdf')
    pyplot.show()


def plotRealAuto():
    '''
    Plot scatterplot of historical volatility and its one day lag
    '''
    startDate = '2018-10-19'
    endDate = '2019-10-21'
    myTic = '^GSPC'
    winvol = 22
    myRef = yfRef(mydate=startDate, undl=myTic)
    sqret = myRef.getSqRet(startDate,endDate)
    pyplot.scatter(sqret[:-1],sqret[1:])
    pyplot.show()

plotMeanRev()