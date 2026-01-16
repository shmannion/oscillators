import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))    
import oscillators as osc
from scipy.stats import shapiro, normaltest

np.set_printoptions(legacy='1.25')

def hyper_param_search(tMax, innerloops, outerloops):
    lags = [-1,0,1]
    S = osc.Oscillators(2)
    S.action_oscillators = [0,1]
    S.metronomes = [1]
    S.initialise_system("default")
    S.tmax = tMax 
    S.omega = [12.826, 12.567]
    coupling = 0.45
    S.noise_distribution = ("normal", [0.0, 0.0 + 0.1])
    K = [[0.0,coupling],[0.0,0.0]]
    S.coupling = K
    modelOut = {-1: [],
                0: [],
                1: []}
    
    for i in range(outerloops):
        S.kuramoto_simulations(innerloops, "interEventTimes")
        df = S.simulation_results()
        # df = df.iloc[20:, :]
        S.reset()
        o1_cols = [col for col in df.columns if 'oscillator_1' in col]
        o2_cols = [col for col in df.columns if 'oscillator_2' in col]
        cols = [i for i in range(len(o1_cols))]
        df1 = df[o1_cols]
        df2 = df[o2_cols]
        df1.columns = cols
        df2.columns = cols
        modelOut[-1].append(np.mean(osc.get_correlations(df1, df2, -1)))
        modelOut[0].append(np.mean(osc.get_correlations(df1, df2, 0)))
        modelOut[1].append(np.mean(osc.get_correlations(df1, df2, 1)))
     
    means = []
    stderr = []
    for lag in lags:
        vals = np.array(modelOut[lag])
        means.append(vals.mean())
        stderr.append(vals.std(ddof=1) / np.sqrt(len(vals))) 

    # print(f'mean value at lag -1: {means[0]}, 0: {means[1]}, 1: {means[1]}')
    # print(f'stderr value at lag -1: {stderr[0]}, 0: {stderr[1]}, 1: {stderr[1]}')
    return means, stderr

if __name__ == "__main__":
    inVal = 5.0
    print(f'tVal, mean_neg1, mean_0, mean_1, stderr_neg1, stderr_0, stderr_1')
    while(inVal < 300):
        means, stderrs = hyper_param_search(inVal, 100, 100) 
        inVal += 5
        print(f'{inVal}, {means[0]}, {means[1]}, {means[2]}, {stderrs[0]}, {stderrs[1]}, {stderrs[2]}')
