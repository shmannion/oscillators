import numpy as np
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
    
    sigma_time = 0.14 * mean_period # 
    sigma_samp = max(1.0, sigma_time * fs)
    x_s = gaussian_filter1d(x, sigma_samp)

    nyq = 0.5 * fs
    low = max(0.1 * f0, f0 * 0.3)          # don’t go too close to 0
    high = min(f0 * 1.7, nyq * 0.9)        # stay below Nyquist
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
    discrete_freq1 = np.array([1/i for i in ie1])
    discrete_freq2 = np.array([1/i for i in ie2])
    x1 = np.arange(len(ie1))
    x2 = np.arange(len(ie2))
    # IEI_raw = osc.get_pair_times_by_trial('other', 1, [1])
    # # ---------------------------
    
    # # ---------------------------
    plt.figure(figsize=(10,4))
    # plt.plot(x1, ie1)
    # plt.plot(x2, ie2)
    plt.plot(t1[100:3000], 2*3.14159*freq1[100:3000])
    print(f'the freq has length {len(freq1)}')
    print(f'time resolution is {t1[2] - t1[1]}')
    print(t1)
    print(t_events1)
    print(freq1)
    print(discrete_freq1)
    plt.plot(t_events1, 2*3.14159*discrete_freq1, '--')
    # plt.plot(t2, 2*3.14159*freq2)
    # plt.plot(t_events2, 2*3.14159*discrete_freq2, '--')
    plt.xlabel("Time (s)")
    plt.ylabel("Instantaneous frequency (Hz)")
    plt.title("delta_f = 0.6")
    plt.tight_layout()
    plt.show()


