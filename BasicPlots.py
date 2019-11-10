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
from itertools import cycle
colors = cycle(["r",'k',mcolors.CSS4_COLORS['maroon'],mcolors.CSS4_COLORS['indianred'],\
                mcolors.CSS4_COLORS['darkred']])

def capPay(payoff,cap):
    '''
    :param payoff: uncapped payoff vector for the varswap
    :param cap: max payoff
    :return: vector of capped payoffs
    '''
    return payoff*(payoff <= cap) + cap*(payoff>cap)

def varCall(payoff,strike):
    '''
    Plot the payoff for a call on variance
    :return:
    '''
    return payoff*(payoff > strike)


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
    pyplot.savefig('histVolVol.pdf',bbox_inches='tight')
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

def plotVixAuto():
    '''
    Plot scatterplot of historical VIX and its one day lag
    '''
    startDate = '2018-10-19'
    endDate = '2019-10-21'
    myTic = '^GSPC'
    myRef = yfRef(mydate=startDate, undl=myTic)
    myVix = myRef.getVolHist(startDate,endDate)
    pyplot.scatter(myVix[:-1],myVix[1:],color=['r','k'])
    z = np.polyfit(myVix[:-1],myVix[1:],1)
    p = np.poly1d(z)
    pyplot.plot(myVix[:-1],p(myVix[:-1]),color='k' ,label='Trend, R^2 = ' + str(round(r2_score(myVix[:-1],p(myVix[:-1])),4)))
    pyplot.xlabel('VIX 1d Lag')
    pyplot.ylabel('VIX')
    pyplot.legend()
    pyplot.savefig('autoCorVix.pdf')
    pyplot.show()

def pltVIXvsHist():
    '''
    Plot vix index and historical vol for a long period
    :return:
    '''
    startDate = '2006-10-19'
    endDate = '2019-10-21'
    myTic = '^GSPC'
    winvol = 30
    myRef = yfRef(mydate=startDate, undl=myTic)
    myVIX = myRef.getVolHist(startDate,endDate)
    myHist = myRef.getRealized(startDate,endDate,winvol)
    pyplot.plot(myVIX.index,myVIX,color='r',label='VIX Index')
    pyplot.plot(myHist.index,myHist*100,color='k',label=str(winvol) + ' day Realized Vol')
    pyplot.legend()
    pyplot.savefig('vixHist.pdf')
    pyplot.show()

def plotTR():
    '''
    Plot total return vol vs. non-dividend vol
    :return:
    '''
    startDate = '2006-10-19'
    endDate = '2019-10-21'
    myTic = '^GSPC'
    myTicTR = '^SP500TR'
    winvol = 180
    myRef = yfRef(mydate=startDate, undl=myTic)
    myTR = yfRef(mydate=startDate, undl=myTicTR)
    myHist = myRef.getRealized(startDate,endDate,winvol)
    myHistTR = myTR.getRealized(startDate,endDate,winvol)
    pyplot.plot(myHist.index,myHist*100,color='k',label=str(winvol) + ' day Realized Vol')
    pyplot.plot(myHist.index,myHistTR*100,color='r',label=str(winvol) + ' day Realized Vol, Total Return')
    pyplot.legend()
    pyplot.show()

def volSwpHedge():
    '''
    Plot vega hedging of volatility swap
    :return:
    '''
    myTic = '^GSPC'
    myVolIdx = '^VIX'
    vegaNot = 513000
    volstrike = 0.2055
    startDate = '2019-06-20'
    volmove = 10 #In % points
    limitx = 40

    myRef = yfRef(mydate=startDate,undl=myTic)
    myRef.getVol(myVolIdx,voldate=startDate)


    #Create varswap to check payoff grid
    volgrid = np.linspace(0.00001,limitx/100,200)
    volswap_g = np.linspace(0,limitx+15,200)
    volswp = volswap_g*0.513 -volstrike*vegaNot/10000
    mySwap = VarSwap(vegaNot,myRef)
    mySwap.strike2 =volstrike*volstrike
    pnlRng = mySwap.pnlSpan(volgrid)
    pltVS = {'VS Hedge Base':0,\
             'VS Hedge + ' + str(volmove) + '%':volmove,\
             'VS Hedge - ' + str(volmove) + '%':-volmove}

    ##################################################
    ####### Plot VarSwap PNL Against Option ##########
    ##################################################
    for k in pltVS.keys():
        itcol = next(colors)
        pyplot.plot(volgrid + 0.01*pltVS[k],pnlRng/1000000 + 0.513*pltVS[k],color=itcol,label=k)
        pyplot.scatter(volstrike + pltVS[k]/100,0.513*pltVS[k],color=itcol,label='Vol Move ' + str(pltVS[k]) + '%')
    pyplot.plot(volswap_g/100,volswp,color=mcolors.CSS4_COLORS['grey'],label='Volatility Swap Payoff')
    pyplot.xlabel('Volatility')
    pyplot.xlim(left=0)
    pyplot.ylabel('PnL (MEUR)')
    pyplot.legend()
    pyplot.savefig('Artifacts/vegaHedge.pdf',bbox_inches='tight')
    pyplot.show()

def pltCap():
    '''
    Plot profile of capped variance swap
    :return:
    '''
    myTic = '^GSPC'
    myVolIdx = '^VIX'
    vegaNot = 513000
    volstrike = 0.2055
    startDate = '2019-06-20'
    cap = 0.40

    myRef = yfRef(mydate=startDate,undl=myTic)
    myRef.getVol(myVolIdx,voldate=startDate)


    #Create varswap to check payoff grid
    volgrid = np.linspace(0.00001,cap+0.2,200)
    mySwap = VarSwap(vegaNot,myRef)
    mySwap.strike2 =volstrike*volstrike
    pnlRng = mySwap.pnlSpan(volgrid)
    cappay = pnlRng[np.argmax(volgrid>cap)] #maximum payoff
    capPNL = capPay(pnlRng,cappay)

    ##################################################
    ####### Plot VarSwap PNL Against Option ##########
    ##################################################
    pyplot.plot(volgrid,pnlRng/10e6,color='k',label='Variance Swap, No Cap')
    pyplot.plot(volgrid,capPNL/10e6,color='r',label='Variance Swap with Cap')
    pyplot.xlabel('Volatility')
    pyplot.xlim(left=0)
    pyplot.ylabel('PnL (MEUR)')
    pyplot.legend()
    pyplot.savefig('Artifacts/capPayoff.pdf',bbox_inches='tight')
    pyplot.show()

def pltCall():
    '''
    Plot call on variance
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
    volgrid = np.linspace(0.00001,volstrike+0.2,200)
    pnlRng = 50*(volgrid*volgrid - volstrike*volstrike)/volstrike
    kpay = pnlRng[np.argmax(volgrid>volstrike)]
    kPNL = varCall(pnlRng,kpay)
    vanPNL = varCall((volgrid-volstrike)*100,0)

    ##################################################
    ####### Plot VarSwap PNL Against Option ##########
    ##################################################
    pyplot.plot(volgrid,kPNL,color='r',label='Option on Variance')
    pyplot.plot(volgrid, vanPNL, color='k', label='Option on Volatility')
    pyplot.xlabel('Volatility')
    pyplot.xlim(left=0)
    pyplot.ylabel('PnL (MEUR)')
    pyplot.legend()
    pyplot.savefig('Artifacts/varcallPay.pdf',bbox_inches='tight')
    pyplot.show()

def plotvixInv():
    startDate = '2015-01-02'
    endDate = '2019-11-08'
    myTic = "SVXY"
    myRef = yfRef(mydate=startDate,undl=myTic)
    mySpot = myRef.setSpotHist(startDate,endDate)

    pyplot.plot(mySpot.index,mySpot,color='r')
    pyplot.savefig('Artifacts/invVix.pdf', bbox_inches='tight')
    pyplot.show()

plotvixInv()