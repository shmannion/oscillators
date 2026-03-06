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
    IEI_raw = osc.get_pair_times_by_trial('other', 2, [1])
    ie1 = IEI_raw[1][1]
    ie2 = IEI_raw[2][1]
    t1, t_events1, freq1 = osc.frequency_from_pulses(IEI_raw[1][1])
    t2, t_events2, freq2 = osc.frequency_from_pulses(IEI_raw[2][1])
    discrete_freq1 = [2*3.14159*1/i for i in IEI_raw[1][1]]
    discrete_freq2 = [2*3.14159*1/i for i in IEI_raw[2][1]]
    params = pd.read_csv('good_params.csv')
    x = params['c1'].loc[0]
    osc.set_verbose(False)
    for index in range(304):
        c1 = params['c1'].loc[index]
        c2 = params['c2'].loc[index]
        sigma_freq = params['sigma_freq'].loc[index] 
        sigma_phase = params['sigma_phase'].loc[index] 
        P = params['P'].loc[index]
        M = params['M'].loc[index]
        df = params['delF'].loc[index]
        delTheta = params['delTheta'].loc[index]
        S = osc.Oscillators(2)
        S.action_oscillators = [0,1]
        S.frequency_distribution = ("fixed", [12.797,12.797-df])
        S.model = 'weakly_coupled'
        S.phase_noise = sigma_phase
        S.frequency_noise = sigma_freq
        S.phase_coupling = [c1,c2]
        S.frequency_coupling = [c1,c2]
        S.pulse_amp = P
        S.pulse_width = M
        S.phase_distribution = ("fixed", [0.0, + delTheta]) 
        S.initialise_system()

        mean_m1 = []
        mean_0 = []
        mean_1 = []
        for j in range(1):
            dfl = {}
            dff = {}
            for i in range(1):
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
            
        print(f'correlations: -1: {np.mean(mean_m1):.3f}, 0: {np.mean(mean_0):.3f}, 1: {np.mean(mean_1):.3f}')
        print(f'the mean inter event time is {np.mean(x[0])}, the mean freq is {2*3.14159*1/np.mean(x[0])}')
        t = [0.001*i for i in range(len(phi[0]))]
        plt.plot([i for i in range(len(ie1))], ie1, label='p1 empirical')
        plt.plot([i for i in range(len(ie2))], ie2, label='p2 empirical')
        plt.plot([i for i in range(len(x[0]))], x[0], label='p1 model')
        plt.plot([i for i in range(len(x[1]))], x[1], label='p2 model')
        plt.title(f'Parameter set {index}')
        plt.legend()
        plt.show()
