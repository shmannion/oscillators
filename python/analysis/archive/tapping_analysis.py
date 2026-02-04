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

    #if len(sys.argv) < 2:
    #    print("Usage: python midi_to_tap_times.py <midi_file> [note_number]")
    #    midiPath = 'data/6_1_other.mid'
    
    ##midiPath = sys.argv[1]
    #midiPath = '../data/120/leader_follower_1/pair_01_c1_t1.mid'
    ##file1 = mido.MidiFile('data/6_1_other.mid') for msg in file1: print(msg)
    #tapTimes = osc.midi_to_tap_times(midiPath)
    #print("Detected tap times (seconds):")
    #for t in tapTimes:
    #    print(f"{t:.3f}")

    #print(f"\nTotal taps: {len(tapTimes)}")

    #interEventTimes = osc.get_inter_event_times(tapTimes)
    

    results = {}
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('comp', [i,1], 120)
    results = osc.remove_outliers(results, [0.3, 0.7])
    osc.distribution_subplots(results, title="Comp - participant 1")

    results = {}
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('comp', [i,2], 120)
    results = osc.remove_outliers(results, [0.3, 0.7])
    osc.distribution_subplots(results, title="Comp - participant 2")
    
    results = {}
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('self', [i,1], 120)
    results = osc.remove_outliers(results, [0.3, 0.7])
    osc.distribution_subplots(results, title="Self - participant 1")

    results = {}
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('self', [i,2], 120)
    results = osc.remove_outliers(results, [0.3, 0.7])
    osc.distribution_subplots(results, title="Self - participant 2")

    results = {}
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('other', [i,1], 120)
    results = osc.remove_outliers(results, [0.3, 0.7])
    osc.distribution_subplots(results, title="Other - participant 1")

    results = {}
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('other', [i,2], 120)
    results = osc.remove_outliers(results, [0.3, 0.7])
    osc.distribution_subplots(results, title="Other - participant 2")

    results = {}
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('leader_follower_1', [i,1], 120)
    results = osc.remove_outliers(results, [0.3, 0.7])
    osc.distribution_subplots(results, title="Leader-follower - leaders 1")

    results = {}
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('leader_follower_2', [i,2], 120)
    results = osc.remove_outliers(results, [0.3, 0.7])
    osc.distribution_subplots(results, title="Leader-follower - leaders 2")

    results = {}
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('leader_follower_1', [i,2], 120)
    results = osc.remove_outliers(results, [0.3, 0.7])
    osc.distribution_subplots(results, title="Leader-follower - followers 1")

    results = {}
    for i in range(1,17): 
        results[i] = osc.get_participant_distribution('leader_follower_2', [i,1], 120)
    results = osc.remove_outliers(results, [0.3, 0.7])
    osc.distribution_subplots(results, title="Leader-follower - followers 2")


    for cond in ['self', 'other', 'comp', 'leaders', 'followers']:
        results = []
        for i in range(1,17):
            if cond == 'leaders':
                ri = osc.get_participant_distribution('leader_follower_1', [i,1], 120)
                results = results + ri
                ri = osc.get_participant_distribution('leader_follower_2', [i,2], 120)
                results = results + ri
            elif cond == 'followers':
                ri = osc.get_participant_distribution('leader_follower_1', [i,2], 120)
                results = results + ri
                ri = osc.get_participant_distribution('leader_follower_2', [i,1], 120)
                results = results + ri
            else:
                ri = osc.get_participant_distribution(cond, [i,2], 120)
                results = results + ri
                ri = osc.get_participant_distribution(cond, [i,1], 120)
                results = results + ri
        results = osc.remove_outliers(results, [0.3, 0.7])
        osc.histogram(results, title=cond)
