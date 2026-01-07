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
    for cond in ['self', 'comp']:
        data[cond] = osc.get_condition_distribution(cond)
    
    keep = osc.remove_outliers(data, [0.33, 0.7])
    frequencies = osc.frequencies_from_times(keep)
   
    targets = [np.mean(keep['comp']), np.std(keep['comp'])]
    #osc.distribution_subplots(frequencies, share=True)
    #osc.distribution_subplots(keep, share=True)
    S = osc.Oscillators(2)
    S.action_oscillators = [0,1]
    S.metronomes = [1]
    S.initialise_system("default")
    S.omega = [12.826, 12.567]
    coupling = 0.44
    S.noise_distribution = ("normal", [0.0, 5.1])
    K = [[0.0,coupling],[0.0,0.0]]
    S.coupling = K
    lag0 = []
    lag1 = []
    lag_n = []
    for i in range(200):
        S.kuramoto_simulations(200, "interEventTimes")
        df = S.simulation_results()
        o1_cols = [col for col in df.columns if 'oscillator_1' in col]
        o2_cols = [col for col in df.columns if 'oscillator_2' in col]
        cols = [i for i in range(len(o1_cols))]
        df1 = df[o1_cols]
        df2 = df[o2_cols]
        df1.columns = cols
        df2.columns = cols
        lag_n.append(np.mean(osc.get_correlations(df1, df2, -1)))
        lag0.append(np.mean(osc.get_correlations(df1, df2, 0)))
        lag1.append(np.mean(osc.get_correlations(df1, df2, 1)))

    print(f'the lag -1 mean is {np.mean(lag_n)}, with standard error {np.mean(lag_n)/((len(lag_n))**0.5)}')
    print(f'the lag 0  mean is {np.mean(lag0)}, with standard error {np.mean(lag0)/((len(lag0))**0.5)}')
    print(f'the lag 1  mean is {np.mean(lag1)}, with standard error {np.mean(lag1)/((len(lag1))**0.5)}')
    #model_ie_times = df.values.flatten()
    #print(f'The empirical mean is {np.mean(keep['comp'])}, and the standard dev is {np.std(keep['comp'])}')
    #print(f'The model mean is {np.mean(model_ie_times)}, and the standard dev is {np.std(model_ie_times)}')
    #S.reset()
    #plt.hist(keep['comp'], bins=30, density=True, alpha=0.7)
    #plt.hist(model_ie_times, bins=30, density=True, alpha=0.7)
        
    #plt.tight_layout()
