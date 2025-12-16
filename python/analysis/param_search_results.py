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
    outdir = '../out/exp_01'
    df_mean = pd.read_csv(f'{outdir}/param_search_mu.csv', index_col=0)
    df_sigma = pd.read_csv(f'{outdir}/param_search_sigma.csv', index_col=0)

    data = {}
    for cond in ['comp']:
        data[cond] = osc.get_condition_distribution(cond)
 
    keep = osc.remove_outliers(data, [0.33, 0.7])
    frequencies = osc.frequencies_from_times(keep)
    for cond in frequencies:
        print(f'For condition {cond}, the mean is {np.mean(keep[cond])}, and the standard dev is {np.std(keep[cond])}')
 
    targets = [np.mean(keep['comp']), np.std(keep['comp'])]
    print(df_mean)
    print(df_sigma.shape)
    # df_mean = df_mean.iloc[40:60,20:80]
    # df_sigma = df_sigma.iloc[40:60,20:80]
    relative_pct_mean = (df_mean - targets[0]).abs() / abs(targets[0])
    print(relative_pct_mean)
    relative_pct_sigma = (df_sigma - targets[1]).abs() / abs(targets[1])
    df_both = np.sqrt(relative_pct_mean**2 + relative_pct_mean**2)
    osc.heatmap(df_both, small_vals = True, title="distance from target mean")
    osc.heatmap(relative_pct_mean, small_vals = True, title="distance from target mean")
    osc.heatmap(relative_pct_sigma, small_vals = True, title="distance from target std")
    row_means = df_mean[(df_mean.index >= 4) & (df_mean.index <= 6)].mean(axis=1)
    print(row_means)
    row_means = df_sigma[(df_sigma.index >= 4) & (df_sigma.index <= 6)].mean(axis=1)
    print(row_means)

