import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, hilbert
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt

import sys
import os
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import oscillators as osc

def get_transform_error(cond, sigma_c, delta_f, printing=False, lag=0):
    cond_time_mean_errors = []
    cond_time_rmses = []
    cond_ie_time_mean_errors = []
    cond_ie_time_rmses = []
    cond_lagm1_emp = []
    cond_lagm1_mod = []
    cond_lag0_emp = []
    cond_lag0_mod = []
    cond_lag1_emp = []
    cond_lag1_mod = []
    for pair in range(1,17):
        data_p1_emp = {}
        data_p2_emp = {}
        data_p1_mod = {}
        data_p2_mod = {}
        pair_ie_times = osc.get_pair_times_by_trial(cond, pair, 'all')
        for trial in [1,2,3,4]:
            ie1 = pair_ie_times[1][trial]
            ie2 = pair_ie_times[2][trial]
            data_p1_emp[trial] = pd.Series(ie1)
            data_p2_emp[trial] = pd.Series(ie2)
            t1, te1, f1, p1 = osc.continuous_frequency_from_taps(ie1, sigma_c, delta_f)
            t2, te2, f2, p2 = osc.continuous_frequency_from_taps(ie2, sigma_c, delta_f)
            t_r1 = osc.taps_from_continuous_phase(t1, p1)
            t_r2 = osc.taps_from_continuous_phase(t2, p2)
            # get error in event times:
            min_len = min(len(te1), len(t_r1))
            error = (t_r1[:min_len] - te1[:min_len])/te1[:min_len]
            cond_time_mean_errors.append(np.mean(error))
            cond_time_rmses.append(np.sqrt(np.mean(error**2)))
            min_len = min(len(te2), len(t_r2))
            error = (t_r2[:min_len] - te2[:min_len])/te2[:min_len]
            cond_time_mean_errors.append(np.mean(error))
            cond_time_rmses.append(np.sqrt(np.mean(error**2)))
            # get error in ie times:
            ie_r1 = np.array([t_r1[i] - t_r1[i-1] for i in range(1, len(t_r1))])
            ie_r2 = np.array([t_r2[i] - t_r2[i-1] for i in range(1, len(t_r2))])
            min_len = min(len(ie1), len(ie_r1))
            error = (ie_r1[:min_len] - ie1[:min_len])/ie1[:min_len]
            cond_ie_time_mean_errors.append(np.mean(error))
            cond_ie_time_rmses.append(np.sqrt(np.mean(error**2)))
            min_len = min(len(ie2), len(ie_r2))
            error = (ie_r2[:min_len] - ie2[:min_len])/ie2[:min_len]
            cond_time_mean_errors.append(np.mean(error))
            cond_time_rmses.append(np.sqrt(np.mean(error**2)))
            data_p1_mod[trial] = pd.Series(ie_r1)
            data_p2_mod[trial] = pd.Series(ie_r2)
        df_emp1 = pd.DataFrame(data_p1_emp)
        df_emp2 = pd.DataFrame(data_p2_emp)
        df_mod1 = pd.DataFrame(data_p1_mod)
        df_mod2 = pd.DataFrame(data_p2_mod)
    cond_lagm1_emp.append(np.mean(osc.get_correlations(df_emp1, df_emp2, -1)))
    cond_lag0_emp.append(np.mean(osc.get_correlations(df_emp1, df_emp2, 0)))
    cond_lag1_emp.append(np.mean(osc.get_correlations(df_emp1, df_emp2, 1)))
    cond_lagm1_mod.append(np.mean(osc.get_correlations(df_mod1, df_mod2, -1)))
    cond_lag0_mod.append(np.mean(osc.get_correlations(df_mod1, df_mod2, 0)))
    cond_lag1_mod.append(np.mean(osc.get_correlations(df_mod1, df_mod2, 1)))
    errors = abs(osc.get_correlations(df_mod1, df_mod2, -1) - osc.get_correlations(df_emp1, df_emp2, -1))
    for l in [0, 1]:
        errors = np.append(errors, abs(osc.get_correlations(df_mod1, df_mod2, l) - osc.get_correlations(df_emp1, df_emp2, l)))
    # now just get the means of all of these lists and print them appropriately        
    if printing == True:
        print(f'for condition {cond} the mean event time error is {np.mean(cond_time_mean_errors)}')
        print(f'for condition {cond} the mean event time rmse is {np.mean(cond_time_rmses)}')
        print(f'for condition {cond} the mean ie time error is {np.mean(cond_ie_time_mean_errors)}')
        print(f'for condition {cond} the mean ie time rmse is {np.mean(cond_ie_time_rmses)}')
        print(f'for condition {cond} the mean empirical lag -1 corr is {np.mean(cond_lagm1_emp)}')
        print(f'for condition {cond} the mean model lag -1 corr is {np.mean(cond_lagm1_mod)}')
        print(f'for condition {cond} the mean empirical lag 0 is {np.mean(cond_lag0_emp)}')
        print(f'for condition {cond} the mean model lag 0 is {np.mean(cond_lag0_mod)}')
        print(f'for condition {cond} the mean empirical lag 1 is {np.mean(cond_lag1_emp)}')
        print(f'for condition {cond} the mean model lag 1 is {np.mean(cond_lag1_mod)}')
    return np.mean(errors)

if __name__ == "__main__":
    """
    TODO:
    - for every condition, every pair and every trial, compare the ie times for accuracy as well as the correlations. 
    - read in every pair of ie times 
    - transform each to continuous
    - transform back to taps
    - get correlations and compare for all.
      to do this one, during the for loop create 4 dicts of series of ie times, then at the end of the loop for each participant
      save the mean correlation and append it to a list for the condition, then get the mean for the condition at the end of that loop.
    - compare ie times themselves to original data
    """
    best_error = 100
    lag_index = int(sys.argv[1])
    lags = [-1, 0, 1]
    lag = lags[lag_index]
    p1_vals = [0.01 + (i * 0.01) for i in range(70)]
    p2_vals = [0.1 + (i * 0.01) for i in range(50)]
    for p1 in p1_vals:
        for p2 in p2_vals:
            error = get_transform_error('leader_follower_2', p1, p2, False, lag)
            if error < best_error:
                error = get_transform_error('leader_follower_2', p1, p2, True, lag)
                best_error = error
                best_params = (p1, p2)

                print("New minimum found:")
                print(f"  param1 = {p1}")
                print(f"  param2 = {p2}")
                print(f"  error  = {best_error}\n")
        print(f"finished with val {p1}")

    print(f'best params = {best_params}, best error = {best_error}')

    # _ = get_transform_error('other', )
    # for cond in ['self', 'other', 'comp', 'leader_follower_1']:#, 'leader_follower_2']:
    # for cond in ['other']:#, 'leader_follower_2']:
    #     cond_time_mean_errors = []
    #     cond_time_rmses = []
    #     cond_ie_time_mean_errors = []
    #     cond_ie_time_rmses = []
    #     cond_lagm1_emp = []
    #     cond_lagm1_mod = []
    #     cond_lag0_emp = []
    #     cond_lag0_mod = []
    #     cond_lag1_emp = []
    #     cond_lag1_mod = []
    #     for pair in range(1,17):
    #         data_p1_emp = {}
    #         data_p2_emp = {}
    #         data_p1_mod = {}
    #         data_p2_mod = {}
    #         pair_ie_times = osc.get_pair_times_by_trial(cond, pair, 'all')
    #         for trial in [1,2,3,4]:
    #             ie1 = pair_ie_times[1][trial]
    #             ie2 = pair_ie_times[2][trial]
    #             data_p1_emp[trial] = pd.Series(ie1)
    #             data_p2_emp[trial] = pd.Series(ie2)
    #             t1, te1, f1, p1 = osc.continuous_frequency_from_taps(ie1)
    #             t2, te2, f2, p2 = osc.continuous_frequency_from_taps(ie2)
    #             t_r1 = osc.taps_from_continuous_phase(t1, p1)
    #             t_r2 = osc.taps_from_continuous_phase(t2, p2)
    #             # get error in event times:
    #             min_len = min(len(te1), len(t_r1))
    #             error = (t_r1[:min_len] - te1[:min_len])/te1[:min_len]
    #             cond_time_mean_errors.append(np.mean(error))
    #             cond_time_rmses.append(np.sqrt(np.mean(error**2)))
    #             min_len = min(len(te2), len(t_r2))
    #             error = (t_r2[:min_len] - te2[:min_len])/te2[:min_len]
    #             cond_time_mean_errors.append(np.mean(error))
    #             cond_time_rmses.append(np.sqrt(np.mean(error**2)))
    #             # get error in ie times:
    #             ie_r1 = np.array([t_r1[i] - t_r1[i-1] for i in range(1, len(t_r1))])
    #             ie_r2 = np.array([t_r2[i] - t_r2[i-1] for i in range(1, len(t_r2))])
    #             min_len = min(len(ie1), len(ie_r1))
    #             error = (ie_r1[:min_len] - ie1[:min_len])/ie1[:min_len]
    #             cond_ie_time_mean_errors.append(np.mean(error))
    #             cond_ie_time_rmses.append(np.sqrt(np.mean(error**2)))
    #             min_len = min(len(ie2), len(ie_r2))
    #             error = (ie_r2[:min_len] - ie2[:min_len])/ie2[:min_len]
    #             cond_time_mean_errors.append(np.mean(error))
    #             cond_time_rmses.append(np.sqrt(np.mean(error**2)))
    #             data_p1_mod[trial] = pd.Series(ie_r1)
    #             data_p2_mod[trial] = pd.Series(ie_r2)
    #         df_emp1 = pd.DataFrame(data_p1_emp)
    #         df_emp2 = pd.DataFrame(data_p2_emp)
    #         df_mod1 = pd.DataFrame(data_p1_mod)
    #         df_mod2 = pd.DataFrame(data_p2_mod)
    #     cond_lagm1_emp.append(np.mean(osc.get_correlations(df_emp1, df_emp2, -1)))
    #     cond_lag0_emp.append(np.mean(osc.get_correlations(df_emp1, df_emp2, 0)))
    #     cond_lag1_emp.append(np.mean(osc.get_correlations(df_emp1, df_emp2, 1)))
    #     cond_lagm1_mod.append(np.mean(osc.get_correlations(df_mod1, df_mod2, -1)))
    #     cond_lag0_mod.append(np.mean(osc.get_correlations(df_mod1, df_mod2, 0)))
    #     cond_lag1_mod.append(np.mean(osc.get_correlations(df_mod1, df_mod2, 1)))
    #     # now just get the means of all of these lists and print them appropriately        
    #     # print(f'for condition {cond} the mean event time error is {np.mean(cond_time_mean_errors)}')
    #     # print(f'for condition {cond} the mean event time rmse is {np.mean(cond_time_rmses)}')
    #     print(f'for condition {cond} the mean ie time error is {np.mean(cond_ie_time_mean_errors)}')
    #     print(f'for condition {cond} the mean ie time rmse is {np.mean(cond_ie_time_rmses)}')
    #     print(f'for condition {cond} the mean empirical lag -1 corr is {np.mean(cond_lagm1_emp)}')
    #     print(f'for condition {cond} the mean model lag -1 corr is {np.mean(cond_lagm1_mod)}')
    #     print(f'for condition {cond} the mean empirical lag 0 is {np.mean(cond_lag0_emp)}')
    #     print(f'for condition {cond} the mean model lag 0 is {np.mean(cond_lag0_mod)}')
    #     print(f'for condition {cond} the mean empirical lag 1 is {np.mean(cond_lag1_emp)}')
    #     print(f'for condition {cond} the mean model lag 1 is {np.mean(cond_lag1_mod)}')

    # plt.figure(figsize=(10,4))
    # plt.plot(t, f1)
    # plt.plot(tevents1, discrete_freq1)
    # plt.plot(t1[:3000] + 0.3, freq1[:3000])
    # plt.show()
    
    # # t1, t_events1, freq1, phase1 = frequency_from_pulses(IEI_raw[1][1])
    # # t2, t_events2, freq2, phase2 = frequency_from_pulses(IEI_raw[2][1])
    
    # ie1 = IEI_raw[1][1]
    # ie2 = IEI_raw[2][1]
    # ie1 = np.array(ie1)
    # tevents1 = np.cumsum(ie1)
    # ie2 = np.array(ie2)
    # tevents2 = np.cumsum(ie2)
    # print(f'correlation between original values is {np.corrcoef(ie1, ie2)}')
    # discrete_freq1 = np.array([1/i for i in ie1])
    # discrete_freq2 = np.array([1/i for i in ie2])
    # x1 = np.arange(len(ie1))
    # df1 = pd.DataFrame()
    # df1[0] = pd.Series(ie1)
    # x2 = np.arange(len(ie2))
    # df2 = pd.DataFrame()
    # df2[0] = pd.Series(ie2)
    # c = osc.get_correlations(df1, df2,lag=0)
    # c2 = osc.get_correlations(df1, df2,lag=-1)
    # c3 = osc.get_correlations(df1, df2,lag=1)
    # print(f'correlation for original: {c2[0],c[0],c3[0]}')
    # # IEI_raw = osc.get_pair_times_by_trial('other', 1, [1])
    # # # ---------------------------
    
    # # # ---------------------------
    # plt.figure(figsize=(10,4))
    # plt.plot(t_events1, discrete_freq1)
    # plt.plot(t1[:3000] + 0.3, freq1[:3000])
    # plt.show()
    # print(f'the freq has length {len(freq1)}')
    # print(f'time resolution is {t1[2] - t1[1]}')


    # t_reconstructed = taps_from_continuous_phase(t1, phase1)
    # t_reconstructed2 = taps_from_continuous_phase(t2, phase2)
    # min_len = min(len(t_events1), len(t_reconstructed))

    # print(t_reconstructed[:min_len])
    # print(t_events1[:min_len])
    # print('Errors for the event times:')
    # print("Mean error:", np.mean(error))
    # print("Std error:", np.std(error))
    # print("RMSE:", np.sqrt(np.mean(error**2)))

    # ie_times_reconstructed = np.array([t_reconstructed[i] - t_reconstructed[i-1] for i in range(1, len(t_reconstructed))])
    # ie_times_reconstructed2 = np.array([t_reconstructed2[i] - t_reconstructed2[i-1] for i in range(1, len(t_reconstructed2))])
    # df1 = pd.DataFrame()
    # df1[0] = pd.Series(ie_times_reconstructed)
    # x2 = np.arange(len(ie2))
    # df2 = pd.DataFrame()
    # df2[0] = pd.Series(ie_times_reconstructed2)
    # c = osc.get_correlations(df1, df2,lag=0)
    # c2 = osc.get_correlations(df1, df2,lag=-1)
    # c3 = osc.get_correlations(df1, df2,lag=1)
    # print(f'correlation for reconstructed: {c2[0],c[0],c3[0]}')
    # ie_times = np.array([t_events1[i] - t_events1[i-1] for i in range(1, len(t_events1))])
    # min_len = min(len(ie_times), len(ie_times_reconstructed))
    # error = (ie_times_reconstructed[:min_len] - ie1[:min_len])/ie1[:min_len]

    # print(f'the mean ie time of reconstructed data is {np.mean(ie_times_reconstructed[:min_len])}')
    # print(f'the real mean is {np.mean(ie1[:min_len])}')
    # print('Errors for the inter event times:')
    # print("Mean error:", np.mean(error))
    # print("Std error:", np.std(error))
    # print("RMSE:", np.sqrt(np.mean(error**2)))
