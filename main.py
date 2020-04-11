'''
main execution file
'''
from BasicPlots import *
from AdvancedPlots import  *
from SampleSim import *

#########
#Statics#
#########
demomenu = {1:('Plot Variance Swap vs. Option',plotVSOptionPayoff),
            2:('Plot Realized Vol of Vol', volVolRealized),
            3:('A Plot that Shows Mean Reversion of Volatility', plotMeanRev),
            4:('Plot Dynamic Hedging of Volatility Swap', volSwpHedge),
            5:('Plot Variance Swap Prices Against Skewness', plotSkew),
            6:('Plot Backtesting Results for Short VS Strategy', plt_shtvs),
            7:('Plot Backtesting Results for Forward VS Strategy', plt_fwdvsbt),
            8:('Plot Backtesting Results for Buy and Hold VS', plt_longvs),
            9:('Plot Dollar Gamma for a Series of Options Across Different Strikes',pltManyGamma)}

if __name__ == '__main__':
    print('Welcome to the Variance Swap Playground Demo!')
    print('Please Select a Numeric Keyboard Input: \n')
    for km in demomenu:
        print(str(km) + ':',demomenu[km][0])
    numkey = int(input('\nPlease Enter a Number:'))
    demomenu[numkey][1]()
    print('Done!')