import sys
import os
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
import statsmodels.api as sm
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))    
import oscillators as osc
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
   # osc.test_granger_causality('other', 120, True, 'all') 
   osc.test_granger_causality('leader_follower_1', 120, True, 'all') 
