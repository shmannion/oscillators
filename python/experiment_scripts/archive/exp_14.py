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
    
    S = osc.Oscillators(2)
    S.action_oscillators = [0]
    S.metronomes = [1]
    S.tmax = 100.0
    S.initialise_system("default")
    S.omega = [12.826, 12.567]
    coupling = 0.415
    K = [[0.0, coupling], [0.0, 0.0]]
    mu = {}
    sigma = {}
    mu_list = []
    sigma_list = []
    res = S.parameter_search_e8()
    for k in res:
        mu[k] = [i[0] for i in res[k]]
        sigma[k] = [i[1] for i in res[k]]
        mu_list.extend(mu[k])
        sigma_list.extend(sigma[k])
    df = pd.DataFrame.from_dict(mu, orient='index')
    n_cols = df.shape[1]
    n_rows = df.shape[0]
    df.columns = [round(i*0.1, 1) for i in range(0,n_cols)]
    df.index = [round(i*0.1, 1) for i in range(0,n_rows)]
    df.index.name = 'noise std'
    df.to_csv('../out/exp_08/param_search_mu.csv')
    
    df = pd.DataFrame.from_dict(sigma, orient='index')
    n_cols = df.shape[1]
    n_rows = df.shape[0]
    df.columns = [round(i*0.1, 1) for i in range(0,n_cols)]
    df.index = [round(i*0.1, 1) for i in range(0,n_rows)]
    df.index.name = 'noise std'
    df.to_csv('../out/exp_08/param_search_sigma.csv')
