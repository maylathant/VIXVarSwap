'''
main execution file
'''


from yfRef import yfRef
from VarSwap import VarSwap
from VarBacktester import VarBacktester
import pickle
import statics as sta
import numpy as np

mydate = '2019-09-20'
myTic = '^GSPC'
myVolIdx = '^VIX'
myScale = 0.05
vegaNot = 513000
startDate = '2019-06-20'

# myBT = VarBacktester(startDate,mydate,myTic)
# myBT.myRef.getSpotHist(start=startDate,end=mydate)
# myBT.myRef.getVol('^VIX',scale=0.02)
# #Save into pickle
# with open(r'cache/myBT','wb') as output: ticDist = pickle.dump(myBT,output)
#Load from pickle
with open(r'cache/myBT','rb') as input: myBT = pickle.load(input)


realized, fairStrike = myBT.runBacktest()
cumPNL = [x*vegaNot/1000000 for x in myBT.valuation.values()]

refVix = myBT.myRef.setVolHist(start=startDate,end=mydate)

import matplotlib.pyplot as pyplot
fig , ax1 = pyplot.subplots()
ax2 = ax1.twinx()
ax1.plot(refVix[1:].index,refVix[1:],color='r',label='VIX')
ax2.plot(refVix[1:].index,myBT.valuation.values(),color='k',label='Variance Swap PNL')
ax1.legend(loc='upper right')
ax2.legend(loc='upper left')
pyplot.title('Performance of 3M Variance Swap (MEUR)')
fig.autofmt_xdate()
pyplot.show()

print('done')