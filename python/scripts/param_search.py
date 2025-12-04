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
    for i in range(0,200):
        S.noise_distribution = ("normal", [0.0, 0.0+(i*0.1)])
        mu_k, sigma_k = S.one_dimensional_coupling_search([0,1], [1,20], 0.1)
        mu[i] = mu_k
        sigma[i] = sigma_k
        
    df = pd.DataFrame.from_dict(mu, orient='index')
    df = df.sort_index().sort_index(axis=1)
    df.to_csv('param_search_mu.csv')
    df = pd.DataFrame.from_dict(sigma, orient='index')
    df = df.sort_index().sort_index(axis=1)
    df.to_csv('param_search_sigma.csv')
