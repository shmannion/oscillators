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
    outputs = []
    param_values = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    for k in param_values:
        S.phase_noise = 0.0
        S.frequency_noise = 0.0
        S.phase_coupling = [1.0, 1.0]
        S.frequency_coupling = [1.0, 1.0]
        S.pulse_amp = 1.0 
        S.pulse_width = 64.0 
        S.initialise_system()
        S.frequency = [12.783,12.797]
        S.phase_distribution = ("fixed", [k, 0.0]) 

        S.dt = 0.01
        S.tmax = 120.0
        S.integrate()
        theta = S.phase_results
        phi = S.frequency_results
        outputs.append(pd.Series(phi[0]))
        S.reset()

    outputs2 = []
    # param_values = [0.5, 1.0, 1.5, 2.0]
    for k in param_values:
        S.phase_noise = 0.0
        S.frequency_noise = 0.0
        S.phase_coupling = [10.0, 10.0]
        S.frequency_coupling = [10.0, 10.0]
        S.pulse_amp = 1.0 
        S.pulse_width = 64.0 
        S.initialise_system()
        S.frequency = [12.783,12.797]
        S.phase_distribution = ("fixed", [k, 0.0]) 

        S.dt = 0.01
        S.tmax = 120.0
        S.integrate()
        theta = S.phase_results
        phi = S.frequency_results
        outputs2.append(pd.Series(phi[0]))
        S.reset()
    fig, axes = plt.subplots(2, 1, figsize=(8, 6))
    for param, y, y2 in zip(param_values, outputs, outputs2):
        axes[0].plot(y, label=f"Parameter = {param}")
        axes[1].plot(y2, label=f"Parameter = {param}")
        plt.tight_layout()
    plt.legend()
    plt.show()
    
    # plt.figure(figsize=(10,4))
    # for param, y in zip(param_values, outputs):
    #     plt.plot(y, label=f"Parameter = {param}")
    # plt.legend()
    # plt.tight_layout()
    # plt.show()

