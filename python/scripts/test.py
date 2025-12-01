import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import oscillators as osc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
np.set_printoptions(legacy='1.25')
PLOT = True

if __name__ == "__main__":
    
    data = {}
    for cond in ['self', 'other', 'comp', 'leader', 'follower']:
        data[cond] = osc.get_condition_distribution(cond)
    
    keep = osc.remove_outliers(data, [0.33, 0.7])
    print(np.min(keep['other']))
    print(np.argmin(keep['other']))
    frequencies = osc.frequencies_from_times(keep)
    for cond in frequencies:
        print(f'For condition {cond}, the mean is {np.mean(frequencies[cond])}, and the standard dev is {np.std(frequencies[cond])}')
    
    osc.distribution_subplots(frequencies, share=True)
    osc.distribution_subplots(keep, share=True)
    
