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
    for i in range(0,100):
        print(round(0.1 * i, 1))
