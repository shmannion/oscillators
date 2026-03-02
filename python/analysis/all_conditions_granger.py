import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import oscillators as osc

if __name__ == "__main__":
    # for cond in ['self', 'other','comp' ,'leader_follower_1', 'leader_follower_2']:
    osc.test_granger_causality('comp', lag=1)
