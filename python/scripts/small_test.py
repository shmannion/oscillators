import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import oscillators as osc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
if __name__ == "__main__":
    times = osc.get_participant_distribution('comp', (1,1), 120)
    times = osc.get_condition_distribution('comp')
    leaders = osc.get_condition_distribution('leader')
    participant_times = osc.get_distribution_per_participant('comp')
    candidate_1_times = participant_times.filter(regex='candidate_1')
    candidate_2_times = participant_times.filter(regex='candidate_2')
    osc.histogram(times)
    osc.histogram(leaders)
    osc.distribution_subplots(candidate_1_times)
    osc.distribution_subplots(candidate_2_times)
