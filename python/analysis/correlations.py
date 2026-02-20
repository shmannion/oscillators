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
import itertools
if __name__ == "__main__":
    
    dfs = []
    freq = 120
    combinations = list(itertools.combinations(range(4), 2))
    for j in range(1,17):
        # build list of dataframes X,Y. X leader, Y follower
        results = osc.get_pair_times_by_trial('self', j, 'all', freq)
        leader_results = osc.get_pair_times_by_trial('leader_follower_1', j, 'all', freq)
        self_correlations = []
        leader_correlations = []
        leader_self_correlations = []
        self = []
        leader = []
        for i in [1,2,3,4]:
            self.append(pd.Series(results[1][i]))
            leader.append(pd.Series(leader_results[1][i])) 
            
        
        for pair in combinations:
            self_correlations.append(self[pair[0]].corr(self[pair[1]]))
            leader_correlations.append(leader[pair[0]].corr(self[pair[1]]))

        for X in self:
            for Y in leader:
                leader_self_correlations.append(X.corr(Y))

        mean_self = np.mean(self_correlations)
        mean_leader = np.mean(leader_correlations)
        mean_self_leader = np.mean(leader_self_correlations)
        print(f'For pair {j}, the avg self corr is {mean_self}, the avergae leader corr is {mean_leader}, and the avg corr between them is {mean_self_leader}')
            # if df[["X", "Y"]].isna().any().any():
            # #     print(f"NaNs in pair {j} trial {i}")
            # # if j == 3:
            # #     if i != 1:
            # #         print(df)
            # # if j == 6:
            # #     if i == 1:
            # #         print(df)

            # # if j == 7:
            # #     if i == 1:
            # #         print(df)

            # # if j == 8:
            # #     if i == 3:
            # #         print(df)

            # # if j == 14:
            # #     if i == 2:
            # #         print(df)

            # dfs.append(df_clean)

    # rows = []
    # for trial_id, df in enumerate(dfs):
        # for t in range(1, len(df)):
            # rows.append({
            #     "trial": trial_id,
            #     "Y_t": df["Y"].iloc[t],
            #     "Y_tm1": df["Y"].iloc[t-1],
            #     "X_t": df["X"].iloc[t],
            #     "X_tm1": df["X"].iloc[t-1]
            # })
    # dflag = pd.DataFrame(rows)
    # dflag.isna().sum()
    
    # X_Y = sm.add_constant(dflag[["Y_tm1", "X_tm1"]])
    # model_X_to_Y = sm.OLS(dflag["Y_t"], X_Y).fit()

    # print('Testing if Yt depends on Xt-1')
    # print(model_X_to_Y.params)

    # Y_X = sm.add_constant(dflag[["X_tm1", "Y_tm1"]])
    # model_Y_to_X = sm.OLS(dflag["X_t"], Y_X).fit()

    # print('Testing if Xt depends on Yt-1')
    # print(model_Y_to_X.params)
    # # print(dflag)
    # # X_r = sm.add_constant(dflag[["Y_tm1"]])
    # # model_r = sm.OLS(dflag["Y_t"], X_r).fit()

    # # X_f = sm.add_constant(dflag[["Y_tm1", "X_tm1"]])
    # # model_f = sm.OLS(dflag["Y_t"], X_f).fit()
    
    # # print(model_f.params)
    # # print("Restricted variance:", model_r.resid.var())
    # # print("Full variance:", model_f.resid.var())
    # # f_test = model_f.compare_f_test(model_r)
    # # print(f"F = {f_test[0]:.3f}, p = {f_test[1]:.3g}")


    # # X = sm.add_constant(dflag[["Y_tm1", "X_tm1", "X_t"]])
    # # model = sm.OLS(dflag["Y_t"], X).fit()

    # # print(model.params)
    # # print(model.summary())

    # scaler = StandardScaler()
    # dflag[["X_t", "X_tm1", "Y_t", "Y_tm1"]] = scaler.fit_transform(
        # dflag[["X_t", "X_tm1", "Y_t", "Y_tm1"]]
    # )
# # X → Y
    # model_XY = sm.OLS(
        # dflag["Y_t"],
        # sm.add_constant(dflag[["Y_tm1", "X_tm1"]])
    # ).fit()

# # Y → X
    # model_YX = sm.OLS(
        # dflag["X_t"],
        # sm.add_constant(dflag[["X_tm1", "Y_tm1"]])
    # ).fit()

    # model_r_Y = sm.OLS(dflag["Y_t"],
            #            sm.add_constant(dflag[["Y_tm1"]])).fit()

    # delta_var_XY = model_r_Y.resid.var() - model_XY.resid.var()

# # Y → X
    # model_r_X = sm.OLS(dflag["X_t"],
            #        sm.add_constant(dflag[["X_tm1"]])).fit()

    # delta_var_YX = model_r_X.resid.var() - model_YX.resid.var()

    # print("Variance reduction X → Y:", delta_var_XY)
    # print("Variance reduction Y → X:", delta_var_YX)

