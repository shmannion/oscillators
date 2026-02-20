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
    for freq in [96, 120, 150]:
        for cond in ['self', 'other', 'comp', 'leaders', 'followers']:
            results = []
            for i in range(1,17):
                if cond == 'leaders':
                    ri = osc.get_participant_distribution('leader_follower_1', [i,1], freq)
                    results = results + ri
                    ri = osc.get_participant_distribution('leader_follower_2', [i,2], freq)
                    results = results + ri
                elif cond == 'followers':
                    ri = osc.get_participant_distribution('leader_follower_1', [i,2], freq)
                    results = results + ri
                    ri = osc.get_participant_distribution('leader_follower_2', [i,1], freq)
                    results = results + ri
                else:
                    ri = osc.get_participant_distribution(cond, [i,2], freq)
                    results = results + ri
                    ri = osc.get_participant_distribution(cond, [i,1], freq)
                    results = results + ri
            frequencies = [1/i for i in results]
            print(f'for condition {cond} and frequency {freq}, the mean frequency is {2*3.14159*sum(frequencies)/len(frequencies)}')
            # results = osc.remove_outliers(results, [0.3, 0.7])
            dat = pd.DataFrame(results, columns=['times'])
            # dat.to_csv(f'../out/distribution_data/{freq}/{cond}.dat')
            osc.histogram(results, title=cond)
