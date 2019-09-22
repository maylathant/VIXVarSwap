'''
main execution file
'''


from yfRef import yfRef
from VarSwap import VarSwap

mydate = '2019-09-20'
myTic = '^GSPC'
myVolIdx = '^VIX'
myScale = 0.05
vegaNot = 10000

myYF = yfRef(mydate,myTic)
myYF.setVolIdx(myVolIdx,myScale)

mySwap = VarSwap(vegaNot,myYF)
mySwap.getStrike()

print('done')