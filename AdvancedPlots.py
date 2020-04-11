'''
Store proceedures to create relatively complex plots
'''

from VarSwap import VarSwap
import numpy as np
from yfRef import yfRef
import utils
import matplotlib.pyplot as pyplot
from matplotlib import colors as mcolors
from utils import bsDolGam
from itertools import cycle
colors = cycle(["r",'k',mcolors.CSS4_COLORS['maroon'],mcolors.CSS4_COLORS['indianred'],\
                mcolors.CSS4_COLORS['darkred']])

def plotSkew(undl = '^GSPC',volIdx = '^VIX',mydate = '2019-10-11',skPoints = 50,maxSkew = 10):
    '''
    Plot Variance swap values as skew declines
    :param undl: Underlying index
    :param volIdx: Corresponding volatility index
    :param mydate: date to check skew
    :param skPoints: Number of flattenings to the skew
    :param maxSkew: Maximum steepening factor
    '''
    myRef = yfRef(mydate,undl)
    myVS = VarSwap(1,myRef,rate=0.0,div=0.0) #Varswap with unit vega notional


    grid = np.linspace(0,maxSkew,num=skPoints)
    for mat in [30,90,360,720]:
        myRef.setVolIdx(volidx=volIdx,flattener=grid,spacing=0.001)
        implied = myRef.getVolIdx('^VIX')[mat][int(myRef.getSpot())][0]
        flatP = myVS.getStrikeInterp(mat)
        mycol = next(colors)
        pyplot.scatter(0,implied,label=str(mat) + 'd Implied ATM Vol', color=mycol)
        pyplot.plot(grid,np.sqrt(flatP),label='Maturity = ' + str(mat) +' Days',color=mycol)
    pyplot.xlabel('Skewness Factor')
    pyplot.ylabel('Derman''s Approximation')
    pyplot.title('Convergence of Dermans Approximaion to ATM Vol')
    pyplot.legend()
    pyplot.savefig('Artifacts/skewConverge.pdf')
    pyplot.show()

    #With Derman
    for mat in [30,90,360,720]:
        myvol = myRef.getVolIdx('^VIX')[mat][int(myRef.getSpot())][0]
        flatP = myVS.getStrikeDer(vol=myvol,b=grid/10,mat=mat)
        pyplot.plot(grid,np.sqrt(flatP),label='Maturity = ' + str(mat) +' Days',color=next(colors))
    pyplot.xlabel('Skewness Factor')
    pyplot.ylabel('Fair Strike of a Variance Swap')
    pyplot.legend()
    pyplot.title('Convergence of Variance Swaps to ATM Vol')
    pyplot.savefig('Artifacts/derman.pdf')
    pyplot.show()

def pltManyGamma(spot=100,divK=False):
    '''
    :param spot: ATM spot price
    :param divK: Divide gamma by strike in the plot
    :return:
    '''
    grid = 200
    spGrid = np.linspace(0, 2 * spot, grid)
    for K in range(int(spot*0.25),int(spot*1.75),5):
        div = K if divK else 1
        opVals = bsDolGam(strike=K,spot=spGrid)/div
        pyplot.plot(spGrid,opVals,color=next(colors))
    pyplot.xlabel('Spot Price')
    pyplot.ylabel('Dollar Gamma')
    pyplot.show()

def pltTotalGamma():
    spot = 100
    grid = 200
    opVals = np.zeros(grid) #To hold sum of option replication no weights
    opK = np.zeros(grid) #Weighted by inverse strike
    opK2 = np.zeros(grid) #Weighted by square of inverse strike
    spGrid = np.linspace(0, 2 * spot, grid)
    for K in range(int(spot*0.25),int(spot*1.75),5):
        temp = bsDolGam(strike=K,spot=spGrid)
        opVals = opVals + temp
        opK = opK + temp/K
        opK2 = opK2 + temp/(K*K)

    opdic={'Inverse':opK, 'Square Inverse':opK2}
    for op in opdic:
        pyplot.plot(spGrid,opdic[op],color=next(colors),label=op)
    pyplot.legend()
    pyplot.show()
