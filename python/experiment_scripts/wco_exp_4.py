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
    
    5 delta f values, search the range of c values for each. 
    

    """
    # constant initialisations
    values = [0.1, 0.5, 1, 1.5, 2.0]
    c_values = [0.0 + i/10 for i in range(0,100)]
    if len(sys.argv) != 3:
        raise SystemExit("Requires argument for noise value")
    ind = int(sys.argv[1])
    outdir = sys.argv[2]
    osc.set_verbose(False)
    S = osc.Oscillators(2)
    S.action_oscillators = [0,1]
    S.set_default_distributions()
    S.model = 'weakly_coupled'
    S.pulse_amp = values[ind] 
    S.pulse_width = 64.0 
    S.frequency_distribution = ("fixed", [12.783,12.797])
    S.phase_distribution = ("fixed", [0.0, 0.0]) 
    S.dt = 0.01
    S.tmax = 30.0
    S.initialise_system()
    # S.frequency_distribution = ("normal", [12.83, 1.26]) 

    # Vectors of parameters that we are going through

    outfile_raw = f'{outdir}/exp_4_raw_{ind}.csv'
    outfile_summ = f'{outdir}/exp_4_summ_{ind}.csv'
    out_columns = ['f1', 'f2', 'p1', 'p2', 'c1', 'c2', 'c3', 'c4', 'pulse_amp', 
                   'pulse_width', 'sigma_freq', 'sigma_phase', 'lagm1', 'lag0', 'lag1']
    
    rows = []
    summ_rows = []
    # Things that are changing each simulation
    for c1 in c_values:
        for c2 in c_values:
            c3 = c1
            c4 = c2
            S.phase_noise = 0.0 
            S.frequency_noise = 0.0 
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
                'pulse_amp': values[ind],
                'pulse_width': 64.0,
                'sigma_freq': 0.0,
                'sigma_phase': 0.0,
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
                'pulse_amp': values[ind],
                'pulse_width': 64.0,
                'sigma_freq': 0.0,
                'sigma_phase': 0.0,
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
