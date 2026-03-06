import optuna
import numpy as np
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import oscillators as osc


# Fix these or add them as trial parameters too
F1 = 12.797
F2 = 12.2
# P = 1.0
# M = 64.0

def run_simulation(c1, c2, sigma):
    S = osc.Oscillators(4)
    S.action_oscillators = [0, 3]
    S.set_default_distributions()
    S.model = 'kuramoto'
    S.frequency_distribution = ("fixed", [F1,F1,F2,F2])
    S.phase_distribution = ("fixed", [0.0, 0.0, 0.0, 0.0])
    S.dt = 0.01
    S.tmax = 30.0
    S.initialise_system()

    S.phase_noise = sigma
    S.kuramoto_coupling = [[0.0, c1, c2, 0.0], [c1, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, c1], [0.0, c2, c1, 0.0]]
    S.initialise_system()

    df1, df2 = {}, {}
    for i in range(100):
        S.integrate()
        x = S.inter_event_times_list
        df1[i] = pd.Series(x[0])
        df2[i] = pd.Series(x[1])
        S.reset()

    df1 = pd.DataFrame(df1)
    df2 = pd.DataFrame(df2)

    lagm1 = np.mean(osc.get_correlations(df1, df2, -1))
    lag0  = np.mean(osc.get_correlations(df1, df2,  0))
    lag1  = np.mean(osc.get_correlations(df1, df2,  1))

    return lagm1, lag0, lag1


def objective(trial):
    c1          = trial.suggest_float('c1', 0.0, 20.0)
    c2          = trial.suggest_float('c2', 0.0, 20.0)
    sigma       = trial.suggest_float('sigma', 0.0, 2.0)

    lagm1, lag0, lag1 = run_simulation(c1, c2, sigma)
    print(f'correlations: -1: {lagm1:.3f}, 0: {lag0:.3f}, 1: {lag1:.3f}')
    # Penalize deviation from desired sign + magnitude
    cost = 0.0
    cost += abs(lagm1 - 0.3)   # want lagm1 > 0.1
    cost += abs(lag0 + 0.3)    # want lag0 < -0.1
    cost += abs(lag1 - 0.3)    # want lag1 > 0.1

    return cost



study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=1000)

print("Best parameters:", study.best_params)
print("Best cost:", study.best_value)
# Get all trials that satisfy your conditions
good_trials = []
for trial in study.trials:
    if trial.value is not None and trial.value < 0.2:  # e.g. threshold = 0.05
        good_trials.append(trial.params | {'cost': trial.value})

df_good = pd.DataFrame(good_trials)
print(f"Found {len(df_good)} good parameter sets")
print(df_good.sort_values('cost'))
df_good.to_csv('kuramoto_good_params.csv', index=False)
df_good.describe()


