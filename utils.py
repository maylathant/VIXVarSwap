import numpy as np
import scipy.stats as sp
'''
File containing all utility functions
'''

def getd1(spot = 100, strike = 100, div = 0, rate = 0, vol = 0.15, time = 1):
	'''
	Compute d1 in Black Scholes formula
	'''
	d1 = np.log(spot/strike) + (rate - div + vol*vol/2)*time
	return d1/(np.sqrt(time)*vol)

def BSCall(spot = 100, strike = 100, div = 0, rate = 0, vol = 0.15, time = 1):
	'''
	Compute the price of vanilla option
	'''
	d1 = getd1(spot, strike, div, rate, vol, time)
	d2 = d1 - vol*np.sqrt(time)

	result = spot*np.exp(-div*time)*sp.norm.cdf(d1)
	return result - strike*np.exp(-rate*time)*sp.norm.cdf(d2)

def BSPut(spot = 100, strike = 100, div = 0, rate = 0, vol = 0.15, time = 1):
	'''
	Compute the price of vanilla option
	'''
	d1 = getd1(spot, strike, div, rate, vol, time)
	d2 = d1 - vol*np.sqrt(time)

	result = sp.norm.cdf(-d2)*strike*np.exp(-rate*time)
	return result - spot*np.exp(-time*div)*sp.norm.cdf(-d1)

def BSPutDig(spot = 100, strike = 100, div = 0, rate = 0, vol = 0.15, time = 1):
	'''
	Compute the price of digital vanilla put
	'''
	d1 = getd1(spot, strike, div, rate, vol, time)
	d2 = d1 - vol*np.sqrt(time)
	return np.exp(-rate*time)*sp.norm.cdf(-d2)

def BSCallDig(spot = 100, strike = 100, div = 0, rate = 0, vol = 0.15, time = 1):
	'''
	Compute the price of digital vanilla call
	'''
	d1 = getd1(spot, strike, div, rate, vol, time)
	d2 = d1 - vol*np.sqrt(time)
	return np.exp(-rate*time)*sp.norm.cdf(d2)


def bsGamma(spot = 100, strike = 100, div = 0, rate = 0, vol = 0.15, time = 1):
	'''
	:param spot: Spot price of underlying
	:param strike: strike price of option
	:param div: dividend rate of underlying
	:param rate: risk free rate in years
	:param vol: volatility of underlying in years
	:param time: time to maturity in years
	:return: The gamma of the underlying
	'''
	d1 = getd1(spot, strike, div, rate, vol, time)
	return np.exp(-div*time)*sp.norm.pdf(d1)/(spot*vol*np.sqrt(time))

def bsDolGam(spot = 100, strike = 100, div = 0, rate = 0, vol = 0.15, time = 1):
	'''
	:param spot: Spot price of underlying
	:param strike: strike price of option
	:param div: dividend rate of underlying
	:param rate: risk free rate in years
	:param vol: volatility of underlying in years
	:param time: time to maturity in years
	:return: The dollar gamma of the underlying
	'''
	rawGam = bsGamma(spot, strike, div, rate, vol, time)
	return rawGam*spot*spot/100