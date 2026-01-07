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
        cols = [i for i in range(len(o1_cols))]
        df = df[o1_cols]
        df.columns = cols

    mean = df.values.mean()
    std = df.values.std(ddof=1) 
    return mean, std

if __name__ == "__main__":
    inVal = 5.0
    print('tMax', 'mean', 'std')
    while(inVal < 300):
        mean, std = hyper_param_search(inVal, 100, 100) 
        inVal += 5
        print(f'{inVal}, {mean}, {std}') 
