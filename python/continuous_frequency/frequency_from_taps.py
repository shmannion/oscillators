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

def bandpass(data, fs, low, high, order=3):
    b, a = butter(order, [low/(0.5*fs), high/(0.5*fs)], btype='band')
    return filtfilt(b, a, data)

def frequency_from_pulses(ie_times):

    IEI = np.array(ie_times, dtype=float)
    # event times from inter event times
    t_events = np.cumsum(IEI)
    T_total = t_events[-1]

    #create grid over the time interval
    mean_period = IEI.mean()
    f0 = 1.0 / mean_period
    fs = max(200.0, 50.0 * f0)  # robust default
    dt = 1.0 / fs
    t = np.arange(0, T_total, dt)

    x = np.zeros_like(t) # create zeros in same shape as t
    idx = np.searchsorted(t, t_events) # place t_events in the grid at the correct position
    idx = idx[idx < len(x)]
    x[idx] = 1.0 # set the entries of the zero vector to 1 at the time points for taps
    
    sigma_time = 0.1 * mean_period 
    sigma_samp = max(1.0, sigma_time * fs)
    x_s = gaussian_filter1d(x, sigma_samp)

    nyq = 0.5 * fs
    low = max(0.1 * f0, f0 * 0.65)          # don’t go too close to 0- TWEAKING THIS FIRST original vals = 0.6, 0.4
    high = min(f0 * 1.35, nyq * 0.9)        # stay below Nyquist
    if not (0 < low < high < nyq):
        raise ValueError("Invalid band. Increase fs or widen band.")

    x_bp = bandpass(x_s, fs, low, high)

    # Hilbert
    analytic = hilbert(x_bp)
    phase = np.unwrap(np.angle(analytic))

    # Smooth phase BEFORE derivative (important)
    phase_s = gaussian_filter1d(phase, sigma_samp)

    inst_freq = np.gradient(phase_s) / (2*np.pi*dt)

    # 8) Ignore edge transients (filter + smoothing padding)
    pad = int(3 * sigma_samp)
    valid = slice(pad, -pad if pad > 0 else None)

    t = t[valid]
    t_events = t_events
    inst_freq = inst_freq[valid]
    return t, t_events, inst_freq, phase_s

def taps_from_continuous_phase(t, phase, shift=0):
    while(len(t) < len(phase)):
        t = np.append(t, [t[-1] + 0.005])
    print(phase[0])
    phase = phase + shift
    print(phase[0])
    print(f't has length {len(t)}, phase has length {len(phase)}')
    cycles = phase/(2*np.pi)
    cycle_index = np.floor(cycles)
    crossings = np.where(np.diff(cycle_index) > 0)[0]
    print(f'n crossings = {len(crossings)}')
    t_reconstructed = []
    print(crossings)

    for i in crossings:
        c1, c2 = cycles[i], cycles[i+1]
        frac = (np.ceil(c1) - c1) / (c2 - c1)
        t_cross = t[i] + frac * (t[i+1] - t[i])
        t_reconstructed.append(t_cross)

    t_reconstructed = np.array(t_reconstructed)
    return t_reconstructed


if __name__ == "__main__":
    """
    TODO:
    - trim continuous frequency data to remove the spike at the end.
    - convert cont freq back into taps by using phase = freq*time, try for all starting freqs for each osc in steps of
    0.01
    - 
    """
    IEI_raw = osc.get_pair_times_by_trial('other', 1, [1])
    t1, t_events1, freq1, phase1 = frequency_from_pulses(IEI_raw[1][1])
    t2, t_events2, freq2, phase2 = frequency_from_pulses(IEI_raw[2][1])
    
    ie1 = IEI_raw[1][1]
    ie2 = IEI_raw[2][1]
    ie1 = np.array(ie1)
    tevents1 = np.cumsum(ie1)
    ie2 = np.array(ie2)
    tevents2 = np.cumsum(ie2)
    print(f'correlation between original values is {np.corrcoef(ie1, ie2)}')
    discrete_freq1 = np.array([1/i for i in ie1])
    discrete_freq2 = np.array([1/i for i in ie2])
    x1 = np.arange(len(ie1))
    df1 = pd.DataFrame()
    df1[0] = pd.Series(ie1)
    x2 = np.arange(len(ie2))
    df2 = pd.DataFrame()
    df2[0] = pd.Series(ie2)
    c = osc.get_correlations(df1, df2,lag=0)
    c2 = osc.get_correlations(df1, df2,lag=-1)
    c3 = osc.get_correlations(df1, df2,lag=1)
    print(f'correlation for original: {c2[0],c[0],c3[0]}')
    # IEI_raw = osc.get_pair_times_by_trial('other', 1, [1])
    # # ---------------------------
    
    # # ---------------------------
    plt.figure(figsize=(10,4))
    plt.plot(t_events1, discrete_freq1)
    plt.plot(t1[:3000] + 0.3, freq1[:3000])
    plt.show()
    print(f'the freq has length {len(freq1)}')
    print(f'time resolution is {t1[2] - t1[1]}')


    t_reconstructed = taps_from_continuous_phase(t1, phase1)
    t_reconstructed2 = taps_from_continuous_phase(t2, phase2)
    min_len = min(len(t_events1), len(t_reconstructed))

    error = (t_reconstructed[:min_len] - tevents1[:min_len])/tevents1[:min_len]

    print(t_reconstructed[:min_len])
    print(t_events1[:min_len])
    print('Errors for the event times:')
    print("Mean error:", np.mean(error))
    print("Std error:", np.std(error))
    print("RMSE:", np.sqrt(np.mean(error**2)))

    ie_times_reconstructed = np.array([t_reconstructed[i] - t_reconstructed[i-1] for i in range(1, len(t_reconstructed))])
    ie_times_reconstructed2 = np.array([t_reconstructed2[i] - t_reconstructed2[i-1] for i in range(1, len(t_reconstructed2))])
    df1 = pd.DataFrame()
    df1[0] = pd.Series(ie_times_reconstructed)
    x2 = np.arange(len(ie2))
    df2 = pd.DataFrame()
    df2[0] = pd.Series(ie_times_reconstructed2)
    c = osc.get_correlations(df1, df2,lag=0)
    c2 = osc.get_correlations(df1, df2,lag=-1)
    c3 = osc.get_correlations(df1, df2,lag=1)
    print(f'correlation for reconstructed: {c2[0],c[0],c3[0]}')
    ie_times = np.array([t_events1[i] - t_events1[i-1] for i in range(1, len(t_events1))])
    min_len = min(len(ie_times), len(ie_times_reconstructed))
    error = (ie_times_reconstructed[:min_len] - ie1[:min_len])/ie1[:min_len]

    print(f'the mean ie time of reconstructed data is {np.mean(ie_times_reconstructed[:min_len])}')
    print(f'the real mean is {np.mean(ie1[:min_len])}')
    print('Errors for the inter event times:')
    print("Mean error:", np.mean(error))
    print("Std error:", np.std(error))
    print("RMSE:", np.sqrt(np.mean(error**2)))
