import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import oscillators as osc
import numpy as np
import pandas as pd
if __name__ == "__main__":
    S = osc.Oscillators(4)
    S.action_oscillators = [0,2]
    S.initialise_system("default")
    S.kuramoto_simulations(10, "interEventTimes")
    print(S.simulation_results())
    df = S.simulation_results()
    print(df.shape)
    #x1 = np.random.normal(10, 2, 100)
    #x2 = np.random.normal(10, 2, 100)
    #x3 = np.random.uniform(0,20,100)
    #X1 = np.random.normal(10, 2, (100,2))
    #X2 = np.random.normal(10, 2, (100,2))
    #X3 = np.random.uniform(0,20, (100,2))
    #b = osc.bhattacharyya_distance(x1, x2)
    #print('1D results')
    #print(f'distance (used by Ole) for two normal samples is {b}')
    #b = osc.bhattacharyya_coefficient(x1, x2)
    #print(f'coeff (simpler one) for two normal samples is {b}')
    #b = osc.bhattacharyya_distance(x1, x3)
    #print(f'distance (used by Ole) for one normal and one uniform sample is {b}')
    #b = osc.bhattacharyya_coefficient(x1, x3)
    #print(f'coeff (simpler one) for one normal and one uniform sample is {b}')
    #
    #print('2D results')
    #b = osc.bhattacharyya_distance(X1, X2)
    #print(f'distance (used by Ole) for two 2D normal samples is {b}')
    #b = osc.bhattacharyya_distance(X1, X3)
    #print(f'distance (used by Ole) for one normal and one uniform sample is {b}')
