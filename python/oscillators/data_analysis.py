from .data_aggregation import get_pair_times_by_trial
import pandas as pd
import numpy as np
from os import listdir
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

def test_granger_causality(data, freq:int=120, scale=True, pairs='all', lag=0):
    """
    Looks at the time series data of taps, pooled together to increase the amount of relevant data. Compares the model
    of OLS with just the previous observation from the individual trial with the data of the previous time point from
    the other time series.
    Args:
        cond:str - the condition we are testing.

        trial:str - what trial data to include, default is all

        freq:int - what frequency data we are looking at, default 120

    returns:
        None, prints the output of reduction in variance in including extra variables.
    """
    if(type(data) == str):
        dfs = []
        freq = 120
        if pairs == 'all':
            pairs = [j for j in range (1,17)]

        for j in pairs:
            # build list of dataframes X,Y. X leader, Y follower
            results = get_pair_times_by_trial(data, j, 'all', freq)
            # results = osc.get_pair_times_by_trial('other', j, 'all', freq)
            for i in [1,2,3,4]:
                df = pd.DataFrame({
                    "X": pd.Series(results[1][i]),
                    "Y": pd.Series(results[2][i]) #Y needs to be the follower in this case
                })
                df_clean = df.replace([np.inf, -np.inf], np.nan).dropna()
                dfs.append(df_clean)
    else:
        dfs = []
        df_raw = data
        for df in df_raw:
            df_clean = df.replace([np.inf, -np.inf], np.nan).dropna()
            df_clean.columns = ['X', 'Y']
            dfs.append(df_clean)

    rows = []
    for trial_id, df in enumerate(dfs):
        for t in range(1, len(df)):
            rows.append({
                "trial": trial_id,
                "Y_t": df["Y"].iloc[t],
                "Y_tm1": df["Y"].iloc[t-1],
                "X_t": df["X"].iloc[t],
                "X_tm1": df["X"].iloc[t-1]
            })
    # clean the data
    dflag = pd.DataFrame(rows)
    if(lag == 1):
        print('Testing if adding the other variable lagged improves the model')
    if(lag == 0):
        print('Testing if adding the other variable without lag improves the model')
    # dflag.isna().sum()
    if(scale == False):
        if(type(data) == str):
            print(f'Testing data for condition {data} without scaling data: Does adding X_tm1 improve Y?') 
        else:
            print(f'Testing data without scaling data: Does adding X_tm1 improve Y?') 
        Y_r = sm.add_constant(dflag[["Y_tm1"]])
        model_r = sm.OLS(dflag["Y_t"], Y_r).fit()

        if(lag == 1):
            Y_f = sm.add_constant(dflag[["Y_tm1", "X_tm1"]])
        if(lag == 0):
            Y_f = sm.add_constant(dflag[["Y_tm1", "X_t"]])
        
        model_f = sm.OLS(dflag["Y_t"], Y_f).fit()
        
        print(model_f.params)
        print("Reduced model summary:\n", model_r.summary())
        print("Full model summary:\n", model_f.summary())
        f_test = model_f.compare_f_test(model_r)
        print(f"F = {f_test[0]:.3f}, p = {f_test[1]:.3g}")
        print(f"Variance of reduced model: {model_r.resid.var()}. Variance of full model: {model_f.resid.var()}")
        print(f"Variance reduction adding X with lag {lag} to Y: {model_r.resid.var() - model_f.resid.var()}")

        if(type(data) == str):
            print(f'Testing data for condition {data} without scaling data: Does adding Y_tm1 improve X?') 
        else:
            print(f'Testing data without scaling data: Does adding Y_tm1 improve X?') 
        X_r = sm.add_constant(dflag[["X_tm1"]])
        model_r = sm.OLS(dflag["X_t"], X_r).fit()

        print(f'Testing if Xt depends on Yt-{lag}')

        if(lag == 1):
            X_f = sm.add_constant(dflag[["X_tm1", "Y_tm1"]])
        if(lag == 0):
            X_f = sm.add_constant(dflag[["X_tm1", "Y_t"]])

        model_f = sm.OLS(dflag["X_t"], X_f).fit()
        print("Reduced model summary:\n", model_r.summary())
        print("Full model summary:\n", model_f.summary())
        f_test = model_f.compare_f_test(model_r)
        print(f"F = {f_test[0]:.3f}, p = {f_test[1]:.3g}")
        print(f"Variance of reduced model: {model_r.resid.var()}. Variance of full model: {model_f.resid.var()}")
        print("Variance reduction adding Y with lag {lag} to X:", model_r.resid.var() - model_f.resid.var())

    
    if(scale == True):
        print('Now scale the data, test dependencies.')
        scaler = StandardScaler()
        dflag[["X_t", "X_tm1", "Y_t", "Y_tm1"]] = scaler.fit_transform(
            dflag[["X_t", "X_tm1", "Y_t", "Y_tm1"]]
        )
        #model Y ~ Xt-1 + Yt-1 
        if(lag == 0):
            model_XY = sm.OLS(
                dflag["Y_t"],
                sm.add_constant(dflag[["Y_tm1", "X_t"]])
            ).fit()
        if(lag == 1):
            model_XY = sm.OLS(
                dflag["Y_t"],
                sm.add_constant(dflag[["Y_tm1", "X_tm1"]])
            ).fit()
        print(f'Summary for Y ~ Xt-{lag} + Yt-1')
        print(model_XY.summary())
        model_r_Y = sm.OLS(dflag["Y_t"],
                           sm.add_constant(dflag[["Y_tm1"]])).fit()

        delta_var_XY = model_r_Y.resid.var() - model_XY.resid.var()
        return_val = delta_var_XY/model_r_Y.resid.var()
        print(model_r_Y.summary())
        print(f"Variance reduction adding X_t-{lag} to Y:  {delta_var_XY}")
        print(f"Variance of reduced model: {model_r_Y.resid.var()}. Variance of full model: {model_XY.resid.var()}")

        #model X ~ Xt-1 + Yt-1 
        if(lag == 0):
            model_YX = sm.OLS(
                dflag["X_t"],
                sm.add_constant(dflag[["X_tm1", "Y_t"]])
            ).fit()

        if(lag == 1):
            model_YX = sm.OLS(
                dflag["X_t"],
                sm.add_constant(dflag[["X_tm1", "Y_tm1"]])
            ).fit()

        print(f'Summary for X ~ Xt-1 + Yt-{lag}')
        print(model_YX.summary())


        model_r_X = sm.OLS(dflag["X_t"],
                       sm.add_constant(dflag[["X_tm1"]])).fit()

        print('Summary for X ~ Xt-1')
        print(model_r_X.summary())
        delta_var_YX = model_r_X.resid.var() - model_YX.resid.var()

        print(f"Variance reduction adding Y_t-{lag} to X: {delta_var_YX}")
        print(f"Variance of reduced model: {model_r_X.resid.var()}. Variance of full model: {model_YX.resid.var()}")
    return return_val
