'''
main execution file
'''


from yfRef import yfRef
from VarSwap import VarSwap
from VarBacktester import VarBacktester
import pickle
import statics as sta
import numpy as np
import matplotlib.pyplot as pyplot
from matplotlib import colors as mcolors

mydate = '2019-09-20'
myTic = '^GSPC'
myVolIdx = '^VIX'
myScale = 0.05
vegaNot = 513000
startDate = '2019-05-20'
fwdStart = '2019-08-20'

# myBT = VarBacktester(startDate,mydate,myTic)
# myBT.myRef.getSpotHist(start=startDate,end=mydate)
# myBT.myRef.getVol('^VIX',scale=0.02)
# #Save into pickle
# with open(r'cache/myBT','wb') as output: ticDist = pickle.dump(myBT,output)
#Load from pickle
with open(r'cache/myBT','rb') as input: myBT = pickle.load(input)




# Plot performance of forward variance swap

near, far, valuation = myBT.btVSFoward(fwdStart=fwdStart)
refVix = myBT.myRef.setVolHist(start=startDate,end=fwdStart)
myrealized = myBT.myRef.getRealized(start=startDate,end=fwdStart,window=30)[1:]

fig , ax1 = pyplot.subplots()
ax2 = ax1.twinx()
#ax1.plot(refVix[1:].index,refVix[1:],color='r',label='VIX')
ax1.plot(refVix[1:].index,myrealized*100,color=mcolors.CSS4_COLORS['maroon'],label='1M Realized')
ax2.plot(refVix[1:].index,valuation.values(),color='k',label=' Forward Variance Swap PNL')
ax1.legend(loc='lower left')
ax2.legend(loc='upper left')
pyplot.title('Performance of 2M/3M Fwd Variance Swap (MEUR)')
fig.autofmt_xdate()
pyplot.show()


# #Plot performance of holding 3M variance
# realized, fairStrike = myBT.runBacktest()
# cumPNL = [x*vegaNot/1000000 for x in myBT.valuation.values()]
#
# refVix = myBT.myRef.setVolHist(start=startDate,end=mydate)

# import matplotlib.pyplot as pyplot
# fig , ax1 = pyplot.subplots()
# ax2 = ax1.twinx()
# ax1.plot(refVix[1:].index,refVix[1:],color='r',label='VIX')
# ax2.plot(refVix[1:].index,myBT.valuation.values(),color='k',label='Variance Swap PNL')
# ax1.legend(loc='upper right')
# ax2.legend(loc='upper left')
# pyplot.title('Performance of 3M Variance Swap (MEUR)')
# fig.autofmt_xdate()
# pyplot.show()

print('done')