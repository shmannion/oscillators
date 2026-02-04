import sys
import os
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))    
import oscillators as osc

if __name__ == "__main__":

    freq = 120
    results = osc.get_pair_times_by_trial('leader_follower_1', 1, 'all', freq)
    results_self = osc.get_pair_times_by_trial('self', 1, 'all', freq)
    for i in [1,2,3,4]:
        df = pd.DataFrame({
            "X": pd.Series(results[1][i]),
            "Y": pd.Series(results[2][i]) #Y needs to be the follower in this case
        })
        results_yx = grangercausalitytests(
            df[["X", "Y"]],
            maxlag=1,
            verbose=True
        )
        # plt.plot(results[1][i], label='c1 - leader')
        # plt.plot(results[2][i], label='c2 - follower')
        # plt.legend()
        # plt.show()
