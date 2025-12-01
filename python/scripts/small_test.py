import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import oscillators as osc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
np.set_printoptions(legacy='1.25')
PLOT = False

if __name__ == "__main__":
    
    times = osc.get_participant_distribution('comp', (1,1), 120)
    times = osc.get_condition_distribution('comp')
    print(times)
    for ind, i in enumerate(times):
        if i > 0.7:
            print(f'Outlier at {ind}')
            del times[ind]
    leaders = osc.get_condition_distribution('leader')
    followers = osc.get_condition_distribution('follower')
    for ind, i in enumerate(followers):
        if i > 0.7:
            print(f'Outlier at {ind}, value is {i}')
            del followers[ind]
        elif i < 0.25:
            print(f'Outlier at {ind}, value is {i}')
            del followers[ind]

    participant_times = osc.get_distribution_per_participant('comp')
    

    candidate_1_times = participant_times.filter(regex='candidate_1')
    outlier_col = 'pair_3_candidate_1'
    outlier = list(candidate_1_times[outlier_col].values)
    for ind, i in enumerate(outlier):
        if i > 0.6:
            print(f'Index {ind} and value {i}')
    del outlier[46]
    meanVal = np.mean(outlier)  
    print(meanVal)
    candidate_1_times.loc[46,'pair_3_candidate_1'] = meanVal
    candidate_2_times = participant_times.filter(regex='candidate_2')
    if PLOT==True: 
        osc.histogram(times, "comp times")
        osc.histogram(leaders, "leader times")
        osc.histogram(followers, "follower times")
        osc.distribution_subplots(candidate_1_times)
        osc.distribution_subplots(candidate_2_times)
    participant_times = osc.get_distribution_per_participant('leader_follower_1')
    followers = participant_times.filter(regex='candidate_2')
    if PLOT==True: 
        osc.distribution_subplots(followers, 'followers 1')
    participant_times = osc.get_distribution_per_participant('leader_follower_2')
    followers = participant_times.filter(regex='candidate_1')
    if PLOT==True: 
        osc.distribution_subplots(followers, 'followers 2')
    
    data = {}
    for cond in ['self', 'other', 'comp', 'leader', 'follower']:
        data[cond] = osc.get_condition_distribution(cond)
    
    keep = osc.remove_outliers(data, [0.2, 0.75])

    #for cond in ['self', 'other', 'comp', 'leader', 'follower']:
    #    data[cond] = osc.get_condition_distribution(cond)
    #    keep[cond] = []
    #for lst in data:
    #    for ind, i in enumerate(data[lst]):
    #        if i > 0.2:
    #            if i < 0.75:
    #                keep[lst].append(i)

    for cond in keep:
        print(f'For condition {cond}, the mean is {np.mean(keep[cond])}, and the standard dev is {np.std(keep[cond])}')
    osc.distribution_subplots(keep, share=True)
    
