import sys
import math
import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))    
import oscillators as osc
from scipy.stats import shapiro, normaltest

np.set_printoptions(legacy='1.25')

if __name__ == "__main__":
    """
    #TODO:
    x Get the average for the 4 trials within each pair
    x Get the average of the average for each pair across all pairs
    
    Get the C++ code loaded in here
    Run model
    Compare
    """
    for cond in ['self', 'comp', 'other', 'leader', 'follower']:
        ieTimes = osc.get_condition_distribution(cond)
        freqs = [1/i for i in ieTimes]
    
    for cond in ['self', 'comp', 'other', 'leader_follower_1', 'leader_follower_2']:
        lagm1 = []
        lag0 = []
        lag1 = []
        res = osc.get_pair_times_by_trial(cond, 1, 'all')
        min_len = 1000
        for i in res[1]:
            if len(res[1][i]) < min_len:
                min_len = len(res[1][i])
        for i in res[1]:
            res[1][i] = res[1][i][:min_len]
        min_len = 1000
        for i in res[2]:
            if len(res[2][i]) < min_len:
                min_len = len(res[2][i])
        for i in res[1]:
            res[2][i] = res[2][i][:min_len]
        df1 = pd.DataFrame(res[1])
        df2 = pd.DataFrame(res[2])

    # Frequency statistics
    freq_rows = []
    for cond in ['self', 'comp', 'other', 'leader', 'follower']:
        ieTimes = osc.get_condition_distribution(cond)
        freqs = [1/i for i in ieTimes[:10]]
        freq_rows.append({
            'condition': cond,
            'mean_ie_time': np.mean(ieTimes),
            'std_ie_time': np.std(ieTimes),
            'mean_freq (1/mean)': 2*math.pi * 1/np.mean(ieTimes),
            'mean_freq (mean of inv)': 2*math.pi * np.mean(freqs),
            'std_freq': 2*math.pi * np.std(freqs)
        })

    df_freq = pd.DataFrame(freq_rows).set_index('condition')
    print("\n=== Frequency Statistics ===")
    print(df_freq.round(3).to_string())

