'''
Store scripts to generate basic plots for VarSwaps
'''

from VarSwap import VarSwap
import numpy as np
from yfRef import yfRef
import utils

myTic = '^GSPC'
myVolIdx = '^VIX'
vegaNot = 513000
volstrike = 0.2055
startDate = '2019-06-20'

myRef = yfRef(mydate=startDate,undl=myTic)
myRef.getVol(myVolIdx,voldate=startDate)


#Create varswap to check payoff grid
volgrid = np.linspace(0.00001,0.4,200)
mySwap = VarSwap(vegaNot,myRef)
mySwap.strike2 =volstrike*volstrike
pnlRng = mySwap.pnlSpan(volgrid)

#Get PNL range for option with similar parameters
pnlOp = np.nan_to_num(utils.BSPut(vol=volgrid)*6)

import matplotlib.pyplot as pyplot
from matplotlib import colors as mcolors
pyplot.plot(volgrid,pnlRng/1000000,color='k',label='Variance Swap PNL')
pyplot.plot(volgrid,pnlOp,color=mcolors.CSS4_COLORS['maroon'], label='Vanilla Call PNL')
pyplot.scatter(volstrike,0,color='r',label='Variance Swap Strike')
pyplot.title('PnL Profile of a Variance Swap (MEUR)')
pyplot.xlabel('Volatility')
pyplot.ylabel('PnL (MEUR)')
pyplot.legend()
pyplot.show()