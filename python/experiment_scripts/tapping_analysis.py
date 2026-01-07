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

    if len(sys.argv) < 2:
        print("Usage: python midi_to_tap_times.py <midi_file> [note_number]")
        midiPath = 'data/6_1_other.mid'
    
    #midiPath = sys.argv[1]
    midiPath = '../data/120/leader_follower_1/pair_01_c1_t1.mid'
    #file1 = mido.MidiFile('data/6_1_other.mid') for msg in file1: print(msg)
    tapTimes = osc.midi_to_tap_times(midiPath)
    print("Detected tap times (seconds):")
    for t in tapTimes:
        print(f"{t:.3f}")

    print(f"\nTotal taps: {len(tapTimes)}")

    interEventTimes = osc.get_inter_event_times(tapTimes)
    

    results = {}
    lags = [-1, 0, 1]    
    for i in range(1,17): 
        results[i] = osc.get_pair_correlations('leader_follower_1', i, neglect=1)
    
    means = {}
    for i in range(1, 17):
        means[i] = {}
        for lag in [-1, 0, 1]:
            means[i][lag] = results[i][lag].mean()

    print(means) 
    K = []
    i1 = 1*5.5
    e1 = 1*1.7
    i2 = 1*1.5
    e2 = 1*5.5


    K.append([0,i1,e1,0])
    K.append([i1,0,0,0])
    K.append([0,0,0,i2])
    K.append([0,e2,i2,0])
   
    modelResults = {}
    empResults = {}
    for i in range(1,17):
        modelResults[i] = {}
        empResults[i] = {}
        x = osc.kuramoto_model(4, "default", [0,2], K)
        modelTimes1 = pd.Series(x[0])
        modelTimes2 = pd.Series(x[1])
        df1 = pd.DataFrame(modelTimes1)
        df2 = pd.DataFrame(modelTimes2)

        for lag in lags:
            modelResults[i][lag] = osc.get_correlations(df1, df2, lag)
            empResults[i][lag] = means[i][lag]

    #summary = get_correlation_means(results)

    #print(summary)
    #yVals = [summary[i][0] for i in lags]
    #yErr = [summary[i][2] for i in lags]
    #plt.bar(lags, yVals, yerr=yErr, capsize=5)
    #plt.plot(lags, modelResults)
    #plt.show()
    
    #print(x[0]) 
    emp = []
    mod = []
    for i in range(1,17):
        emp_lag = []
        mod_lag = []
        for lag in lags:
            emp_lag.append(means[i][lag])
            mod_lag.append(modelResults[i][lag][0])
        emp.append(emp_lag)
        mod.append(mod_lag)


    print(emp)
    print(mod)
    empZeroLag = []
    for i in range(1,17):
        empZeroLag.append(results[i][0][0])
        empZeroLag.append(results[i][0][1])
        empZeroLag.append(results[i][0][2])
        empZeroLag.append(results[i][0][3])

    plt.hist(empZeroLag, bins=8, density=True, alpha=0.6, color='skyblue', edgecolor='k', label="Data")
    plt.show()
    for i in [0,1,2]:
        eTemp = []
        mTemp = []
        for j in range(len(emp)):
            eTemp.append(emp[j][i])
            mTemp.append(mod[j][i])

        b = osc.bhattacharyya_distance(np.array(eTemp), np.array(mTemp))
        print(f'the BC is {b}')

    
    b = osc.bhattacharyya_distance(np.array(emp), np.array(mod))
    print(f'the BC using the whole matrix is {b}')

    for i in [0,1,2]:
        stat, p = shapiro(emp[i])
        print(f"Variable {i+1}: p = {p:.4f} {'(non-Gaussian)' if p < 0.05 else '(Gaussian-like)'}")
