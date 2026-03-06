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
    c1': 8.638145573659498, 'c2': 9.851301052577462, 'sigma_freq': 0.016554414506198455, 
    'sigma_phase': 0.06391637666629167, 'P': 2.6667328662738004, 'M': 97.76316361219921, 'delF': 0.3166561048577765, 'delTheta': -1.5984419013313262
    parameters: {'c1': 5.496886994665426, 'c2': 0.007550716253371739, 'sigma_freq': 0.07178617982987173 
                 'sigma_phase': 0.08205630066099186, 'P': 1.4407814228521205, 'M': 107.14446545942181}


    """
    c1 = 5.4969
    c2 = 0.0076
    F_MEAN = 12.828
    F_STD = 0.426
    f1 = np.random.normal(F_MEAN, F_STD)
    f2 = np.random.normal(F_MEAN, F_STD)
    p1 = np.random.uniform(0, 2*np.pi)
    p2 = np.random.uniform(0, 2*np.pi)
    osc.set_verbose(False)
    S = osc.Oscillators(2)
    S.action_oscillators = [0,1]
    # S.frequency_distribution = ("fixed", [12.797,12.477])
    S.frequency_distribution = ("fixed", [f1,f2])
    x = S.frequency_distribution
    print(x)
    # S.metronomes = [1]
    S.model = 'weakly_coupled'
    S.phase_noise = 0.08
    S.frequency_noise = 0.0717
    S.phase_coupling = [8.638,9.851]
    S.frequency_coupling = [8.638, 9.851]
    S.pulse_amp = 1.44 #2.667
    S.pulse_width = 107.1
    S.phase_distribution = ("fixed", [p1, p2]) 
    # S.phase_distribution = ("fixed", [0.0, 0.0]) 
    x = S.frequency_distribution
    print(x)
    S.initialise_system()
    x = S.frequency_distribution
    print(x)

    mean_m1 = []
    mean_0 = []
    mean_1 = []
    for j in range(1):
        dfl = {}
        dff = {}
        for i in range(50):
            S.tmax=20.0
            S.dt = 0.001

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
                        pass
                        # print(f'We have a correlation +-+, {corrs_m1[i]}, {corrs_0[i]}, {corrs_1[i]}')
        
    IEI_raw = osc.get_pair_times_by_trial('other', 2, [1])
    t1, t_events1, freq1 = osc.frequency_from_pulses(IEI_raw[1][1])
    t2, t_events2, freq2 = osc.frequency_from_pulses(IEI_raw[2][1])
    discrete_freq1 = [2*3.14159*1/i for i in IEI_raw[1][1]]
    discrete_freq2 = [2*3.14159*1/i for i in IEI_raw[2][1]]
    print(f'correlations: -1: {np.mean(mean_m1):.3f}, 0: {np.mean(mean_0):.3f}, 1: {np.mean(mean_1):.3f}')
    print(f'the mean inter event time is {np.mean(x[0])}, the mean freq is {2*3.14159*1/np.mean(x[0])}')
    t = [0.001*i for i in range(len(phi[0]))]
    plt.plot(t1, 2*3.14159*freq1, label='p1 empirical')
    plt.plot(t2, 2*3.14159*freq2, label='p2 empirical')
    plt.plot(t, phi[0], label='p1 model')
    plt.plot(t, phi[1], label='p2 model')
    plt.legend()
    plt.show()
