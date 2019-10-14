'''
Test scripts
'''


from utils import BSPut, BSCall
import numpy as np


##Test zero skew theory
K2 = 0
grid = np.linspace(1,200,num=200)
for x in grid:
    temp = BSPut(strike=x,time=30/360) if x <= 100 else BSCall(strike=x,time=30/360)
    K2 = K2 + temp/(x*x)

print(np.sqrt(2*K2*30/360))