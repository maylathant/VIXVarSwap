'''
Test scripts
'''


from utils import BSPut, BSCall
import numpy as np


##Test zero skew theory
K2 = 0; spot = 10000 #Spot must be an integet
grid = np.linspace(1,2*spot,num=2*spot)
for x in grid:
    temp = BSPut(strike=x,time=30/360,spot=spot) if x <= spot else BSCall(strike=x,time=30/360,spot=spot)
    K2 = K2 + temp/(x*x)

print(np.sqrt(2*K2*360/30))