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
    # S.metronomes = [1]
    S.set_default_distributions()
    S.model = 'weakly_coupled'
    x = S.model
    S.phase_noise = 0.3
    S.frequency_noise = 0.3
    S.phase_coupling = [0.0,0.0]
    S.frequency_coupling = [0.0,5.0]
    S.pulse_amp = 1.0
    S.pulse_width = 64.0 
    S.initialise_system()
    S.frequency = [12.82,12.3]
    # S.frequency_distribution = ("normal", [12.83, 1.26]) 
    S.phase_distribution = ("fixed", [0.0, 0.0]) 

    S.dt = 0.01
    S.tmax = 30.0
    reductions = []
    mean_m1 = []
    mean_0 = []
    mean_1 = []
    for j in range(16):
        dfl = {}
        dff = {}
        for i in range(50):
            S.integrate()
            theta = S.phase_results
            phi = S.frequency_results
            # if i == 0:
            #     if j == 0:
            #         print(phi)
            #         for k in phi:
            #             for ind, l in enumerate(phi[k]):
            #                 print(f'{0.01 * ind}, {l}, freq{k}')
            x = S.inter_event_times_list
            data = {}
            data['leader'] = pd.Series(x[1])
            dfl[i] = pd.Series(x[1])
            dff[i] = pd.Series(x[0])
            # dfs.append(pd.DataFrame(data))
            S.reset()
        dfl = pd.DataFrame(dfl)
        dff = pd.DataFrame(dff)
        corrs_0 = osc.get_correlations(dfl, dff, 0)
        mean_0.append(np.mean(corrs_0))
        corrs_1 = osc.get_correlations(dfl, dff, 1)
        mean_1.append(np.mean(corrs_1))
        corrs_m1 = osc.get_correlations(dfl, dff, -1)
        mean_m1.append(np.mean(corrs_m1))
        for i in range(len(corrs_0)):
            if corrs_0[i] < 0:
                if corrs_m1[i] > 0:
                    if corrs_1[i] > 0:
                        print(f'We have a correlation +-+, {corrs_m1[i]}, {corrs_0[i]}, {corrs_1[i]}')
        
        # S.reset('full')

    
        # r = osc.test_granger_causality(dfs, scale=True, lag=0)
        # reductions.append(r)

    print(f'correlations: -1: {np.mean(mean_m1):.3f}, 0: {np.mean(mean_0):.3f}, 1: {np.mean(mean_1):.3f}')
    print(f'correlations: -1: {np.min(mean_m1):.3f} - {np.max(mean_m1):.3f}, 0: {np.min(mean_0):.3f} - {np.max(mean_0):.3f}, 1: {np.min(mean_1):.3f} - {np.max(mean_1):.3f}')
    # print(f'The avg relative reduction in variance was {sum(reductions)/len(reductions)}')
    # osc.test_granger_causality('leader_follower_1', scale=True, lag=1)
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
