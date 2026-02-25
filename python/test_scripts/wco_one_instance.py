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
    S.frequency_distribution = ("fixed", [12.783,12.797])
    x = S.frequency_distribution
    print(x)
    # S.metronomes = [1]
    S.set_default_distributions()
    x = S.frequency_distribution
    print(x)
    S.model = 'weakly_coupled'
    x = S.model
    S.phase_noise = 0.0
    S.frequency_noise = 0.0
    S.phase_coupling = [5.2,3.6]
    S.frequency_coupling = [5.2,3.6]
    S.pulse_amp = 1.0
    S.pulse_width = 64.0 
    S.frequency_distribution = ("fixed", [12.783,12.797])
    S.phase_distribution = ("fixed", [0.0, 0.0]) 
    x = S.frequency_distribution
    print(x)
    S.dt = 0.01
    S.tmax = 30.0
    S.initialise_system()
    x = S.frequency_distribution
    print(x)

    mean_m1 = []
    mean_0 = []
    mean_1 = []
    for j in range(2):
        dfl = {}
        dff = {}
        for i in range(2):
            S.integrate()
            theta = S.phase_results
            phi = S.frequency_results
            print(phi[0][0])
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
        S.reset("full")
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
        

    # print(corrs_0)
    # print(mean_0)
    # print(mean_1)
    print(f'correlations: -1: {np.mean(mean_m1):.3f}, 0: {np.mean(mean_0):.3f}, 1: {np.mean(mean_1):.3f}')
    S = osc.Oscillators(2)
    S.action_oscillators = [0,1]
    # S.metronomes = [1]
    S.set_default_distributions()
    S.model = 'weakly_coupled'
    x = S.model
    S.phase_noise = 0.0
    S.frequency_noise = 0.0
    S.phase_coupling = [5.2,3.6]
    S.frequency_coupling = [5.2,3.6]
    S.pulse_amp = 1.0
    S.pulse_width = 64.0 
    S.frequency = [12.783,12.797]
    S.frequency_distribution = ("fixed", [12.783,12.797])
    S.phase_distribution = ("fixed", [0.0, 0.0]) 

    S.dt = 0.01
    S.tmax = 30.0
    S.initialise_system()
    mean_m1 = []
    mean_0 = []
    mean_1 = []
    for j in range(1):
        dfl = {}
        dff = {}
        for i in range(1):
            S.integrate()
            theta = S.phase_results
            phi = S.frequency_results
            print(phi[0][0])
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
        

    # print(corrs_0)
    # print(mean_0)
    # print(mean_1)
    print(f'correlations: -1: {np.mean(mean_m1):.3f}, 0: {np.mean(mean_0):.3f}, 1: {np.mean(mean_1):.3f}')
