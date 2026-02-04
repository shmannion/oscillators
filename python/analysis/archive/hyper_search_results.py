import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import oscillators as osc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
np.set_printoptions(legacy='1.25')
PLOT = True

if __name__ == "__main__":
    for i in range (2,7):
        df = pd.read_csv(f'../out/exp_0{i}/res.dat', index_col=0)
        df.plot()  
        plt.title(f'exp {i}')
        plt.show()     
    
