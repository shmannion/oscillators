import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))    
import oscillators as osc
from scipy.stats import shapiro, normaltest

np.set_printoptions(legacy='1.25')

if __name__ == "__main__":
    """
    #TODO:
    search a range of values for c1 - c4. Starting small, centre c values around 1. Let c1=c2, c3=c4 (other cond)
    
    6 noise values, 0-0.5 in 0.1.
    
    estimate frequency and phase values from data, use the self data to estimate avg freq, use the first ie time from
    other data to get an initial phase.

    output data very regularly. dataframe of all parameters, and the avg lag correlations. Raw data (correlation from
    every trial) and summarised data (correlation from each collection of trials)

    What is changing between each collection of trials?


    """
    # constant initialisations
    osc.set_verbose(False)
    S = osc.Oscillators(2)
    S.action_oscillators = [0,1]
    S.set_default_distributions()
    S.model = 'weakly_coupled'
    S.pulse_amp = 1.0
    S.pulse_width = 64.0 
    S.frequency_distribution = ("fixed", [12.783,12.797])
    S.phase_distribution = ("fixed", [0.0, 0.0]) 
    S.dt = 0.01
    S.tmax = 30.0
    S.initialise_system()
    # S.frequency_distribution = ("normal", [12.83, 1.26]) 

    # Vectors of parameters that we are going through
    noise_values = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    c_values = [0.0 + i/10 for i in range(0,100)]
    if len(sys.argv) != 3:
        raise SystemExit("Requires argument for noise value")

    noise_ind = int(sys.argv[1])
    outdir = sys.argv[2]
    outfile_raw = f'{outdir}/exp_1_raw_{noise_ind}.csv'
    outfile_summ = f'{outdir}/exp_1_summ_{noise_ind}.csv'
    out_columns = ['f1', 'f2', 'p1', 'p2', 'c1', 'c2', 'c3', 'c4', 'pulse_amp', 
                   'pulse_width', 'sigma_freq', 'sigma_phase', 'lagm1', 'lag0', 'lag1']
    
    rows = []
    summ_rows = []
    # Things that are changing each simulation
    for c1 in c_values:
        for c2 in c_values:
            c3 = c1
            c4 = c2
            S.phase_noise = noise_values[noise_ind]
            S.frequency_noise = noise_values[noise_ind]
            S.phase_coupling = [c1,c2]
            S.frequency_coupling = [c1,c2]
            S.initialise_system()
            # corrs = {'lagm1': [], 'lag0': [], 'lag1': []}
            df1 = {}
            df2 = {}
            for i in range(50):
                S.integrate()
                x = S.inter_event_times_list
                phi = S.frequency_results
                if i == 1:
                    print(phi[0][0])
                    print(phi[1][0])
                df1[i] = pd.Series(x[0])
                df2[i] = pd.Series(x[1])
                S.reset()
            df1 = pd.DataFrame(df1)
            df2 = pd.DataFrame(df2)
            corrs_0 = osc.get_correlations(df1, df2, 0)
            corrs_1 = osc.get_correlations(df1, df2, 1)
            corrs_m1 = osc.get_correlations(df1, df2, -1)
            for x,y,z in zip(corrs_m1, corrs_0, corrs_1):
                rows.append({
                'f1': 12.783,
                'f2': 12.797,
                'p1': 0,
                'p2': 0,
                'c1': c1,
                'c2': c2,
                'c3': c3,
                'c4': c4,
                'pulse_amp': 1.0,
                'pulse_width': 64.0,
                'sigma_freq': noise_values[noise_ind],
                'sigma_phase': noise_values[noise_ind],
                'lagm1': x,
                'lag0': y,
                'lag1': z
                })

            summ_rows.append({
                'f1': 12.783,
                'f2': 12.797,
                'p1': 0,
                'p2': 0,
                'c1': c1,
                'c2': c2,
                'c3': c3,
                'c4': c4,
                'pulse_amp': 1.0,
                'pulse_width': 64.0,
                'sigma_freq': noise_values[noise_ind],
                'sigma_phase': noise_values[noise_ind],
                'lagm1': np.mean(corrs_m1),
                'lag0': np.mean(corrs_0),
                'lag1': np.mean(corrs_1),
                })
            df_raw = pd.DataFrame(rows)
            rows = []
            df_summ = pd.DataFrame(summ_rows)
            summ_rows = []
            df_raw.to_csv(outfile_raw, mode='a', header=not os.path.exists(outfile_raw), index=False)
            df_summ.to_csv(outfile_summ, mode='a', header=not os.path.exists(outfile_summ), index=False)
