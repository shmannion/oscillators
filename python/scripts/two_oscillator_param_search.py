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
    for cond in frequencies:
        print(f'For condition {cond}, the mean is {np.mean(keep[cond])}, and the standard dev is {np.std(keep[cond])}')
   
    targets = [np.mean(keep['comp']), np.std(keep['comp'])]
    #osc.distribution_subplots(frequencies, share=True)
    #osc.distribution_subplots(keep, share=True)
    S = osc.Oscillators(2)
    S.action_oscillators = [0]
    S.metronomes = [1]
    S.initialise_system("default")
    S.omega = [12.826, 12.567]
    coupling = 0.415
    #fig = plt.figure(figsize=(10,8))
    #fig, axs = plt.subplots(3,3, figsize=(12,9))
    S.noise_distribution = ("normal", [0.0, 1.0])
    #keys = osc.get_plot_keys([3,3])
    sigma = []
    coupling_vals = []
    dists = []
    for i in range(0,100):
        for j in range(0,100):
            coupling = 0 + j*0.1 
            coupling_vals.append(coupling)
            K = [[0.0,coupling],[0.0,0.0]]
            S.noise_distribution = ("normal", [0.0, 0.0+(i*0.1)])
            sigma.append(0 + 0.1*i)
            S.coupling = K
            S.kuramoto_simulations(100, "interEventTimes")
            df = S.simulation_results()
            model_ie_times = df.values.flatten()
            model_vals = [np.mean(model_ie_times), np.std(model_ie_times)]
            distance = ((model_vals[1] - targets[1])**2 + (model_vals[0] - targets[0])**2)**0.5
            normed_dist = (((model_vals[1] - targets[1])/targets[1])**2 + ((model_vals[0] - targets[0])/targets[0])**2)**0.5
            dists.append(normed_dist)
            print(f'For coupling {coupling} and noise st dev {4+(i*0.2)}, mean is {np.mean(model_ie_times)}, stdev is {np.std(model_ie_times)}. Dist: {distance}. Normed: {normed_dist}')
            #plt.figure(figsize=(8,5))
            #axs[keys[i][0], keys[i][1]].hist(keep['comp'], bins=30, density=True, alpha=0.7, label=f'empirical {i}')
            #axs[keys[i][0], keys[i][1]].hist(model_ie_times, bins=30, density=True, alpha=0.7, label=f'model {i}')
            S.reset()
        
    #plt.tight_layout()
    #plt.show()
    best_index = np.argmin(dists)
    print(f'The closest was when sigma is {sigma[best_index]}, coupling is {coupling_vals[best_index]}, and the distance was {dists[best_index]}')
    X = np.array(sigma)
    Y = np.array(coupling_vals)
    Z = np.array(dists)
    
    # Get unique sorted coordinates
    x_unique = np.unique(X)
    y_unique = np.unique(Y)
    
    # Create grid for the heatmap
    heatmap = np.full((len(y_unique), len(x_unique)), np.nan)
    
    # Fill grid with Z values
    for xi, yi, zi in zip(X, Y, Z):
        x_idx = np.where(x_unique == xi)[0][0]
        y_idx = np.where(y_unique == yi)[0][0]
        heatmap[y_idx, x_idx] = zi
    
    # Plot
    n_x = 10
    n_y = 4
    plt.figure(figsize=(8,6))
    plt.imshow(heatmap, cmap='viridis_r', origin='lower')
    plt.colorbar(label="Value (lower is better)")
    plt.xticks(
    ticks=np.arange(0, len(x_unique), n_x),
    labels=[f"{val:.3f}" for val in x_unique[::n_x]], rotation=45)
    plt.yticks(
    ticks=np.arange(0, len(y_unique), n_y),
    labels=[f"{val:.2f}" for val in y_unique[::n_y]])
    #plt.xticks(range(len(x_unique)), x_unique, rotation=45)
    #plt.yticks(range(len(y_unique)), y_unique)
    plt.xlabel("std deviation of noise")
    plt.ylabel("coupling coefficient")
    plt.title("distance from empirical values")
    
    plt.show()
