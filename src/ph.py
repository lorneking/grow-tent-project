import ads1115 as ADS
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

'''pH calibration magic numbers'''

PH1 = 4.01 # pH of buffer calibration solution - low
PH2 = 6.86 # pH of buffer calibration solution - mid
PH3 = 9.18 # pH of buffer calibration solution - high

PH1POINT = 31302.29 # Average measured analog calibration value - low
PH2POINT = 27695.95 # Average measured analog calibration value - mid
PH3POINT = 23900.11 # Average measured analog calibration value - high

'''end pH calibration magic numbers'''

rawValues = np.array([PH1POINT, PH2POINT, PH3POINT])
pHValues = np.array([PH1, PH2, PH3])

# Logarithmic function to fit
def log_model(x, a, b):
    return a * np.log(x) + b

def phRead():
    params, covariance = curve_fit(log_model, rawValues, pHValues)
    a, b = params
    phRawVal = ADS.readADS1115(1)
    phVal = a * np.log(phRawVal) + b
    return phVal

def phTempRead():
    tempVal = ADS.readADS1115(2)
    return tempVal





