import sys
import math
import os
import numpy as np
import pandas as pd
from scipy import stats
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
    path1 = '../data/120/leader_follower_1/pair_01_c1_t1.mid'
    path2 = '../data/120/leader_follower_1/pair_01_c2_t1.mid'

    tt1 = osc.midi_to_tap_times(path1)
    tt2 = osc.midi_to_tap_times(path2)
    print(f'tap times for p1: {tt1}')
    print(f'tap times for p2: {tt2}')
