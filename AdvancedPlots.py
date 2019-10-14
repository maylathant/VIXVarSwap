'''
Store proceedures to create relatively complex plots
'''

from VarSwap import VarSwap
import numpy as np
from yfRef import yfRef
import utils
import matplotlib.pyplot as pyplot
from matplotlib import colors as mcolors

'''
Plot Variance swap values as skew declines
'''

undl = '^GSPC'
volIdx = '^VIX'
mydate = '2019-10-11'
mat = 360 #Maturiry in days
skPoints = 50 #Number of flattenings to the skew
maxSkew = 10 #Max steepening factor
myRef = yfRef(mydate,undl)
myVS = VarSwap(1,myRef,rate=0.0,div=0.0) #Varswap with unit vega notional


grid = np.linspace(0,maxSkew,num=skPoints)
for mat in [30,90,360,720]:
    myRef.setVolIdx(volidx=volIdx,flattener=grid)
    flatP = myVS.getStrikeInterp(mat)
    pyplot.plot(grid,np.sqrt(flatP),label='Maturity = ' + str(mat) +' Days')


pyplot.legend()
pyplot.show()

#With Derman
myvol = myRef.setVol()/100
for mat in [30,90,360,720]:
    flatP = myVS.getStrikeDer(vol=myvol,b=grid/10,mat=mat)
    pyplot.plot(grid,np.sqrt(flatP),label='Maturity = ' + str(mat) +' Days')


pyplot.legend()
pyplot.show()

print('done')

