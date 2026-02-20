import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))    
import oscillators as osc
import math
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
    freq = 120
    results = osc.get_pair_times_by_trial('other', 1, 'all', freq)
    results_inv = {}
    for x in results:
        results_inv[x] = {}
        for lst_ind in results[x]:
            results_inv[x][lst_ind] = []
            for i in results[x][lst_ind]:
                results_inv[x][lst_ind].append(1/i * 2*3.14159)
    print(results_inv)

    # results_self = osc.get_pair_times_by_trial('self', 1, 'all', freq)
    # print(results_self)
    for i in [1,2,3,4]:
        plt.plot(results_inv[1][i], label='c1 - leader')
        plt.plot(results_inv[2][i], label='c2 - follower')
        plt.legend()
        plt.show()
     
    freq = 120
    results = osc.get_pair_times_by_trial('leader_follower_1', 1, 'all', freq)
    results_self = osc.get_pair_times_by_trial('self', 1, 'all', freq)
    # for i in [1,2,3,4]:
    #     plt.plot(results[1][i], label='c1 - leader')
    #     plt.plot(results[2][i], label='c2 - follower')
    #     plt.plot(results_self[1][i],'--' ,label='c1 - self')
    #     plt.plot(results_self[2][i],'--' ,label='c2 - self')
        # plt.legend()
        # plt.show()
