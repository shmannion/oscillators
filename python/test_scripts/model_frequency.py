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
    S.phase_noise = 0.4
    S.frequency_noise = 0.4
    S.phase_coupling = [1.2,1.2]
    S.frequency_coupling = [1.2,1.2]
    S.pulse_amp = 1.0
    S.pulse_width = 64.0 
    S.initialise_system()
    S.frequency = [12.8,12.7]
    # S.frequency_distribution = ("normal", [12.83, 1.26]) 
    S.phase_distribution = ("fixed", [0.0, 0.0]) 

    S.dt = 0.01
    S.tmax = 15.0
    reductions = []
    mean_m1 = []
    mean_0 = []
    mean_1 = []
    S.integrate()
    theta = S.phase_results
    phi = S.frequency_results
    # print(phi[0])
    # print(tm)
    tm = []
    for i in range(len(phi[0])):
        tm.append(0.01 * i)
    IEI_raw = osc.get_pair_times_by_trial('other', 2, [1])
    t1, t_events1, freq1 = osc.frequency_from_pulses(IEI_raw[1][1])
    IEI_raw = osc.get_pair_times_by_trial('self', 2, [1])
    t2, t_events2, freq2 = osc.frequency_from_pulses(IEI_raw[1][1])
    t1 = t1[:3000] 
    freq1 = freq1[:3000] 
    print(len(freq1))
    plt.figure(figsize=(10,4))
    plt.plot(t1, 2*3.14159*freq1, label='other')
    # plt.plot(t2, 2*3.14159*freq2, label='self')
    plt.plot(tm,phi[0], '--', label='model')
    # plt.plot(t2, 2*3.14159*freq2)
    # plt.plot(t_events2, 2*3.14159*discrete_freq2, '--')
    # plt.axhline(f0, linestyle="--")
    plt.xlabel("Time (s)")
    plt.ylabel("Instantaneous frequency (Hz)")
    plt.title("Instantaneous frequency and transfromed freq")
    plt.legend()
    plt.tight_layout()
    plt.show()
    #                                                                                                                                                                      98,1          Bot

