#File that contains code for sample simulations
from VarSwap import VarSwap
from VarBacktester import VarBacktester
import statics as sta
import numpy as np
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