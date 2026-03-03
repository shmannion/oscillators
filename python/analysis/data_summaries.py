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
        print(f'For condition {cond}, the mean ie time is {np.mean(ieTimes)}. The std is {np.std(ieTimes)}')
        print(f'Taking the inverse of the mean ie time gives {1/np.mean(ieTimes)}.')
        print(f'Getting the mean freq from individual ie times gives {np.mean(freqs)}.')
        print(f'Getting the std of freq from individual ie times gives {np.std(freqs)}.')
    
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
        lagm1.append(np.mean(osc.get_correlations(df1, df2, -1)))
        lag0.append(np.mean(osc.get_correlations(df1, df2, 0)))
        lag1.append(np.mean(osc.get_correlations(df1, df2, 1)))
        print(f'for condition {cond}, the corrs are: lag -1 {np.mean(lagm1):.3f}; lag 0 {np.mean(lag0):.3f}; lag 1 {np.mean(lag1):.3f}')
        print(f'standard erros: lag -1: {np.std(lagm1)/np.sqrt(len(lagm1))}, lag 0: {np.std(lag0)/np.sqrt(len(lag0))}, lag 1: {np.std(lag1)/np.sqrt(len(lag1))}')

    # Frequency statistics
    freq_rows = []
    for cond in ['self', 'comp', 'other', 'leader', 'follower']:
        ieTimes = osc.get_condition_distribution(cond)
        freqs = [1/i for i in ieTimes]
        freq_rows.append({
            'condition': cond,
            'mean_ie_time': np.mean(ieTimes),
            'std_ie_time': np.std(ieTimes),
            'mean_freq (1/mean)': 2*math.pi * 1/np.mean(ieTimes),
            'mean_freq (mean of inv)': 2*math.pi * np.mean(freqs),
            'std_freq': 2*math.pi * np.std(freqs)
        })

    df_freq = pd.DataFrame(freq_rows).set_index('condition')
    df_freq.to_csv('empirical_freq_data.csv')
    print("\n=== Frequency Statistics ===")
    print(df_freq.round(3).to_string())

    # Correlation statistics
    corr_rows = []
    for cond in ['self', 'comp', 'other', 'leader_follower_1', 'leader_follower_2']:
        if cond == 'leader_follower':
            res1 = osc.get_pair_times_by_trial('leader_follower_1')
            res2 = osc.get_pair_times_by_trial('leader_follower_2')
        else:
            res = osc.get_pair_times_by_trial(cond, 1, 'all')
            df1 = pd.DataFrame({k: pd.Series(v) for k, v in res[1].items()})
            df2 = pd.DataFrame({k: pd.Series(v) for k, v in res[2].items()})
        # df1 = pd.DataFrame(res[1])
        # df2 = pd.DataFrame(res[2])
        lagm1 = osc.get_correlations(df1, df2, -1)
        lag0  = osc.get_correlations(df1, df2,  0)
        lag1  = osc.get_correlations(df1, df2,  1)
        corr_rows.append({
            'condition': cond,
            'lag-1 mean': np.mean(lagm1),
            'lag-1 sem': stats.sem(lagm1),
            'lag0 mean': np.mean(lag0),
            'lag0 sem': stats.sem(lag0),
            'lag1 mean': np.mean(lag1),
            'lag1 sem': stats.sem(lag1)
        })

    df_corr = pd.DataFrame(corr_rows).set_index('condition')
    df_corr.to_csv('empirical_corr_data.csv')
    print("\n=== Correlation Statistics ===")
    print(df_corr.round(3).to_string())

    corr_rows = []
    for cond in ['self', 'comp', 'other', 'leader_follower_1', 'leader_follower_2', 'leader_follower']:
        pair_means_lagm1 = []
        pair_means_lag0  = []
        pair_means_lag1  = []
    
        cond_list = ['leader_follower_1', 'leader_follower_2'] if cond == 'leader_follower' else [cond]
    
        for c in cond_list:
            for pair in range(1, 17):
                res = osc.get_pair_times_by_trial(c, pair, 'all')
                df1 = pd.DataFrame({k: pd.Series(v) for k, v in res[1].items()})
                df2 = pd.DataFrame({k: pd.Series(v) for k, v in res[2].items()})
                if c == 'leader_follower_2':
                    df1 = df1[[1, 2, 3]]
                    df2 = df2[[1, 2, 3]]
                pair_means_lagm1.append(np.mean(osc.get_correlations(df1, df2, -1)))
                pair_means_lag0.append(np.mean(osc.get_correlations(df1, df2,  0)))
                pair_means_lag1.append(np.mean(osc.get_correlations(df1, df2,  1)))

        corr_rows.append({
            'condition': cond,
            'lag-1 mean': np.mean(pair_means_lagm1),
            'lag-1 sem':  stats.sem(pair_means_lagm1),
            'lag0 mean':  np.mean(pair_means_lag0),
            'lag0 sem':   stats.sem(pair_means_lag0),
            'lag1 mean':  np.mean(pair_means_lag1),
            'lag1 sem':   stats.sem(pair_means_lag1)
        })

    df_corr = pd.DataFrame(corr_rows).set_index('condition')
    df_corr.to_csv('empirical_corr_data.csv')
    print("\n=== Correlation Statistics ===")
    print(df_corr.round(3).to_string())
