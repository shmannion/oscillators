import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
    osc.set_verbose(False)
    S = osc.Oscillators(2)
    S.action_oscillators = [0,1]
    S.metronomes = [1]
    S.set_default_distributions()
    S.model = 'weakly_coupled'
    x = S.model
    S.phase_noise = 0.1
    S.frequency_noise = 0.1
    S.frequency_coupling = [4.0,1.0]
    S.phase_coupling = [10.0,1.0]
    S.initialise_system()
    S.frequency = [12.82,12.82]
    S.tmax = 20.0
    dfs = [] 
    for i in range(100):
        S.integrate()
        theta = S.phase_results
        phi = S.frequency_results
        x = S.inter_event_times_list
        data = {}
        data[0] = pd.Series(x[1])
        data[1] = pd.Series(x[0])
        dfs.append(pd.DataFrame(data))
        S.reset()
    
    osc.test_granger_causality(dfs)
    # print(dfl.head())
    # corrs = osc.get_correlations(dfl, dff, 0)
    # print(f'for lag 0 the mean correlation is {np.mean(corrs)}')
    # corrs = osc.get_correlations(dfl, dff, -1)
    # print(f'for lag -1 the mean correlation is {np.mean(corrs)}')
    # corrs = osc.get_correlations(dfl, dff, 1)
    # print(f'for lag 1 the mean correlation is {np.mean(corrs)}')
    # freq = 120
    # results = osc.get_pair_times_by_trial('leader_follower_1', 2, 'all', freq)
    
    # xs = []
    # for i in range(1, len(x[0])+1):
    #     xs.append(i)

    # plt.plot(xs, x[0], label='oscillator 1 - leader')
    # xs = []
    # for i in range(1, len(x[1])+1):
    #     xs.append(i)
    # plt.plot(xs, x[1], label='oscillator 2 - follower')
    # plt.plot(results[1][1], '--', label='c1 - leader')
    # plt.plot(results[2][1], '--', label='c2 - follower')
    # plt.legend()
    # plt.show()
