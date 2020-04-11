#File that contains code for sample simulations
from VarBacktester import VarBacktester
import matplotlib.pyplot as pyplot
from matplotlib import colors as mcolors

#######################
###Static Parameters###
#######################
mydate = '2019-09-20'
myTic = '^GSPC'
myVolIdx = '^VIX'
myScale = 0.05
vegaNot = 513000
startDate = '2019-05-20'
fwdStart = '2019-08-20'

myBT = VarBacktester(startDate,mydate,myTic)
myBT.myRef.getSpotHist(start=startDate,end=mydate)
myBT.myRef.getVol('^VIX',scale=0.02)

def plt_shtvs(compreal=False,savefig=False):
    '''
    Plot a backtest for the PNL of rolling short variance swaps
    Compare to VIX and Realized volatility
    :param compreal: Bool. If true plot realized volatility
    :param savefig: Bool. If true, save a pdf of figure
    :return: None
    '''
    #Plot performance of rolling short variance swaps
    refVix = myBT.myRef.setVolHist(start=startDate,end=mydate)
    if compreal:
        myrealized = myBT.myRef.getRealized(start=startDate,end=mydate,window=30)
    myVIX = myBT.myRef.getVolHist(startDate,mydate)
    realized, fair, value = myBT.btShortVarRoll()
    fig , ax1 = pyplot.subplots()
    ax2 = ax1.twinx()
    if compreal:
        ax1.plot(refVix[1:].index,myrealized[1:]*100,color=mcolors.CSS4_COLORS['maroon'],label='1M Realized')
    ax1.plot(refVix[1:].index,myVIX[1:],color='r',label='VIX Index')
    ax2.plot(refVix[1:].index,value.values(),color='k',label=' Rolled Short VS PNL')
    ax1.legend(loc='lower right')
    ax2.legend(loc='upper left')
    pyplot.title('Performance of Rolling Short Variance Swap (MEUR)')
    fig.autofmt_xdate()
    if savefig:
        pyplot.savefig('Artifacts/rollShort.pdf', bbox_inches='tight')
    pyplot.show()


def plt_fwdvsbt(compreal=False):
    '''
    Run a backtest on forward variance swap performance and plot results
    :param compreal: Bool. If true plot realized volatility
    :return: None
    '''
    # Plot performance of forward variance swap
    refVix = myBT.myRef.setVolHist(start=startDate,end=fwdStart)
    if compreal:
        myrealized = myBT.myRef.getRealized(start=startDate,end=fwdStart,window=30)[1:]
    near, far, valuation = myBT.btVSFoward(fwdStart=fwdStart)

    fig , ax1 = pyplot.subplots()
    ax2 = ax1.twinx()
    ax1.plot(refVix[1:].index,refVix[1:],color='r',label='VIX')
    if compreal:
        ax1.plot(refVix[1:].index,myrealized*100,color=mcolors.CSS4_COLORS['maroon'],label='1M Realized')
    ax2.plot(refVix[1:].index,valuation.values(),color='k',label=' Forward Variance Swap PNL')
    ax1.legend(loc='lower left')
    ax2.legend(loc='upper left')
    pyplot.title('Performance of 2M/3M Fwd Variance Swap (MEUR)')
    fig.autofmt_xdate()
    pyplot.show()


def plt_longvs():
    '''
    Plot performance of holding a long variance swap until maturity
    :return: None
    '''
    realized, fairStrike = myBT.runBacktest()
    cumPNL = [x*vegaNot/1000000 for x in myBT.valuation.values()]

    refVix = myBT.myRef.setVolHist(start=startDate,end=mydate)

    fig , ax1 = pyplot.subplots()
    ax2 = ax1.twinx()
    ax1.plot(refVix[1:].index,refVix[1:],color='r',label='VIX')
    ax2.plot(refVix[1:].index,myBT.valuation.values(),color='k',label='Variance Swap PNL')
    ax1.legend(loc='upper right')
    ax2.legend(loc='upper left')
    pyplot.title('Performance of 3M Variance Swap (MEUR)')
    fig.autofmt_xdate()
    pyplot.show()