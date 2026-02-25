import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))    
import oscillators as osc
from scipy.stats import shapiro, normaltest

np.set_printoptions(legacy='1.25')

if __name__ == "__main__":
    """
    Taking the tap times and getting the average instantaneous frequency from them
    """

    
    freq = 120
    results = {}
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('self', [i,1], freq)
    results = osc.remove_outliers(results, [0.4, 0.85])
    means = []
    for i in range(1,17):
        means.append(2*3.14159*1/np.mean(results[i]))
        print(f'mean frequency is {1/np.mean(results[i])}')
    print(f'for participant 1, the mean is {np.mean(means)}, standard dev is {np.std(means)}')
    means = []
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('self', [i,2], freq)
    results = osc.remove_outliers(results, [0.4, 0.85])
    for i in range(1,17):
        means.append(2*3.14159*1/np.mean(results[i]))
        print(f'mean frequency is {1/np.mean(results[i])}')

    print(f'for participant 2, the mean is {np.mean(means)}, standard dev is {np.std(means)}')
