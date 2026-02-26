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


def continuous_frequency_from_taps(ie_times, sigma_c=0.1, delta_f=0.4):
    """
    Generates a continous frequency and phase from inter event times using hilbert transform
    args:
        inter event times
    returns:
        t: time vector corresponding to the phase/frequency values
        t_events: inter event times
        inst_freq: frequency at each value of t
        phase_s: smoothed phase value at each value of t
    """
    ie_times = np.array(ie_times, dtype=float)
    # event times from inter event times
    t_events = np.cumsum(ie_times)
    t_total = t_events[-1]

    #create grid over the time interval
    mean_period = ie_times.mean()
    f0 = 1.0 / mean_period
    fs = max(200.0, 50.0 * f0) # make grid resolution at least 200 points within each oscillation 
    dt = 1.0 / fs
    t = np.arange(0, t_total, dt)

    x = np.zeros_like(t) # create zeros in same shape as t
    idx = np.searchsorted(t, t_events) # place t_events in the grid at the correct position
    idx = idx[idx < len(x)]
    x[idx] = 1.0 # set the entries of the zero vector to 1 at the time points for taps
                 # this makes taps 'binary', maybe some should be bigger than others?
    
    sigma_time = sigma_c * mean_period # This controlls the amount of smoothing done on the signal
    sigma_samp = max(1.0, sigma_time * fs)
    x_s = gaussian_filter1d(x, sigma_samp) # This filters and smooths the signal

    nyq = 0.5 * fs # nyquist frequency is the largest frequency that can be represented from the data
    low = max(0.1 * f0, f0 * (1-delta_f))          # don’t go too close to 0
    high = min(f0 * (1+delta_f), nyq * 0.9)        # stay below Nyquist
    if not (0 < low < high < nyq): # The high/low controls the bandwidth that is allowed
        raise ValueError("Invalid band. Increase fs or widen band.")

    x_bp = bandpass(x_s, fs, low, high) # do the bandpass

    # Hilbert
    analytic = hilbert(x_bp) # hilbert transform the smoothed signal
    phase = np.unwrap(np.angle(analytic)) #extract the phase over time

    # Smooth phase BEFORE derivative (important)
    phase_s = gaussian_filter1d(phase, sigma_samp) #smooth the phase

    inst_freq = np.gradient(phase_s) / (2*np.pi*dt) #get the instaneous frequency over time

    # 8) Ignore edge transients (filter + smoothing padding)
    pad = int(3 * sigma_samp) #unsure on these lines but necessary
    valid = slice(pad, -pad if pad > 0 else None)

    t = t[valid]
    t_events = t_events
    inst_freq = inst_freq[valid]
    return t, t_events, inst_freq, phase_s

def taps_from_continuous_phase(t, phase, shift=0):
    """
    generates the  inter event times from the continuous phase generated via hilbert transform
    args:
        t: vector of time values
        phase: phase at each value of t
        shift: phase shift. Use to get the event times to line up with real data
               ** does not affect ie times in current implementation, need to rethink
    returns:
        t_reconstructed: constructed ie times from the generated phase values.
    """
    while(len(t) < len(phase)):
        t = np.append(t, [t[-1] + 0.005])
    phase = phase + shift
    cycles = phase/(2*np.pi)
    cycle_index = np.floor(cycles)
    crossings = np.where(np.diff(cycle_index) > 0)[0]
    t_reconstructed = []
    for i in crossings:
        c1, c2 = cycles[i], cycles[i+1]
        frac = (np.ceil(c1) - c1) / (c2 - c1)
        t_cross = t[i] + frac * (t[i+1] - t[i])
        t_reconstructed.append(t_cross)

    t_reconstructed = np.array(t_reconstructed)
    return t_reconstructed


