import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import oscillators as osc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
if __name__ == "__main__":
    #get the empirical data I want
    ieEmp = []
    for trial in range(1,5): 
        tapTimes = osc.midi_to_tap_times(f'../data/120/leader_follower_1/pair_01_c1_t{trial}.mid')
        ieEmpTrial = osc.get_inter_event_times(tapTimes)
        for i in ieEmpTrial:
            ieEmp.append(i)
    #coupling:
    
    plt.figure(figsize=(8,5))
    #scalars = [i * 0.1 for i in range(1,10)]
    S = osc.Oscillators(4)
    S.action_oscillators = [0,2]
    S.initialise_system("default")
    S.omega = [11.9, 12.0, 12.4, 12.6]
    fig, axs = plt.subplots(3, 2, figsize=(12,4), sharey=True)
    axis_co_ords = []
    for i in range(0,3):
        for j in range(0,2):
            axis_co_ords.append([i,j])
    for i in range(0,6):
        if i == 0:
            scale = 0.0 
        else:
            scale = ((i-1) * 0.01) + 0.01
        i1 = scale * 1.7
        i2 = 0 * scale * 4.1
        e1 = 0 * scale * 5.5
        e2 = 0 * scale * 5.5
        K = [[0.0,i1,e1,0.0],[i1,0.0,0.0,0.0],[0.0,0.0,0.0,i2],[0.0,e2,i2,0.0]]
        S.coupling = K
        S.kuramoto_simulations(200, "interEventTimes")
        df = S.simulation_results()
        print(df.head())
        
        c1_cols = [col for col in df.columns if 'oscillator_1' in col] 
        ieMod = df[c1_cols].values.flatten()
        ks_stat, ks_p = stats.ks_2samp(ieEmp, ieMod)
        w = stats.wasserstein_distance(ieEmp, ieMod)
        print("KS:", ks_stat, ks_p, "Wasserstein (sec):", w)
        empirical = np.array(ieEmp)   
        model = np.array(ieMod)      
        
        
        bins = np.linspace(
            min(empirical.min(), model.min()),
            max(empirical.max(), model.max()),
            30     # number of bins (adjust as needed)
        )
        
        axs[axis_co_ords[i][0], axis_co_ords[i][1]].hist(empirical, bins=30, density=True, alpha=0.7)
        axs[axis_co_ords[i][0], axis_co_ords[i][1]].hist(model, bins=30, density=True, alpha=0.7)
        axs[axis_co_ords[i][0], axis_co_ords[i][1]].set_title(f"Scale {i}")
        S.reset() 
    
    plt.xlabel("Inter-event time")
    plt.ylabel("Density")
    plt.title("Empirical vs Model IET Distribution")
    
    plt.tight_layout()
    plt.show()


