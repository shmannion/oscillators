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
    cd = osc.get_condition_correlations("comp")
    # osc.correlation_plots(cd)
    for j in range(10):
        S = osc.Oscillators(3)
        S.action_oscillators = [0,1]
        S.metronomes = [1, 2]
        S.initialise_system("default")
        S.tmax = 250.0
        S.omega = [12.826, 12.567, 12.826]
        coupling_e = 1.45
        coupling_i = 0.45
        S.noise_distribution = ("normal", [0.0, 0.0 + 0.1*j])
        K = [[0.0,coupling_e, coupling_i],[0.0,0.0, 0.0], [coupling_e, coupling_i, 0.0]]
        S.coupling = K
        # for i in range(200):
        modelOut = {-1: [],
                    0: [],
                    1: []}
        for i in range(17):
            S.kuramoto_simulations(10, "interEventTimes")
            df = S.simulation_results()
            df = df.iloc[10:, :]
            S.reset()
            o1_cols = [col for col in df.columns if 'oscillator_1' in col]
            o2_cols = [col for col in df.columns if 'oscillator_2' in col]
            if i == 1:
                print(df)
            cols = [i for i in range(len(o1_cols))]
            df1 = df[o1_cols]
            df2 = df[o2_cols]
            df1.columns = cols
            df2.columns = cols
            modelOut[-1].append(np.mean(osc.get_correlations(df1, df2, -1)))
            modelOut[0].append(np.mean(osc.get_correlations(df1, df2, 0)))
            modelOut[1].append(np.mean(osc.get_correlations(df1, df2, 1)))
        
        # osc.correlation_plots(modelOut)
        osc.plot_correlation_comparison(cd, modelOut, saveloc="")
