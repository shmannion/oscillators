import mido
import numpy as np
import pandas as pd
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#import oscillators as osc
from scipy.stats import shapiro, normaltest
from scipy.signal import butter, filtfilt, hilbert
from scipy.ndimage import gaussian_filter1d
import math

def midi_to_tap_times(midi_file_path):
    """
    Convert a MIDI file into a time series of tap times.
 
    Args:
        midi_file_path (str): Path to the MIDI file.
 
    Returns:
        list[float]: List of tap times in seconds.
    """
    mid = mido.MidiFile(midi_file_path)
    tapTimes = []
    currentTime = 0
    for msg in mid:
        currentTime += msg.time  # accumulate delta time
        if msg.type == 'note_on' and msg.velocity > 0:
            tapTimes.append(currentTime)
 
    return tapTimes
 
 
def get_inter_event_times(tapTimes):
    """
    Convert a list of timestamps to a list of inter-event times
 
    Args:
        tap_times: list of timestamps of taps.
 
    Returns:
        list: List of interevent times
    """
    interEventTimes = []
    for i in range(1, len(tapTimes)):
        interEventTimes.append(tapTimes[i] - tapTimes[i-1])
 
    return interEventTimes
 
 
def get_inter_event_times_from_file(midi_file_path):
    """
    merging of the two functions above
    """
    tapTimes = midi_to_tap_times(midi_file_path)
    inter_event_times = get_inter_event_times(tapTimes)
    return inter_event_times


def remove_outliers(data, bounds):
    """
    removes outliers from the data above and below bound values.
    Returns same type as it receives
    """

    if(type(data) == pd.DataFrame):
        clean_data = remove_outliers_from_dataframe(data, bounds)
    if(type(data) == dict):
        clean_data = remove_outliers_from_dict(data, bounds)
    if(type(data) == list):
        clean_data = remove_outliers_from_list(data, bounds)
    return clean_data

def remove_outliers_from_dataframe(data, bounds):
    """
    Removed outliers from a dataframe, replaces them with column mean values
    """
    #columns to lists, get indices to elements, set elements of df to mean
    clean_data = data 
    columns = list(data.columns)
    for column_index, column in enumerate(columns):
        indices = []
        x = list(data[column].values)
        keep = []
        for row_index, i in enumerate(x):
            if i < bounds[1]:
                if i > bounds[0]:
                    keep.append(i)
            elif i > bounds[1]:
                indices.append([row_index, column_index])
            elif i < bounds[0]:
                indices.append([row_index, column_index])
        
        mean = np.mean(keep)
        for pair in indices:
            clean_data.iloc[pair[0], pair[1]] = mean
    return clean_data


def remove_outliers_from_dict(data, bounds):
    """
    Removes outliers from a dict without replacement
    """
    keep = {}
    for lst in data:
        keep[lst] = []
    
    for lst in data:
        for i in data[lst]:
            if i < bounds[1]:
                if i > bounds[0]:
                    keep[lst].append(i)
    
    return keep


def remove_outliers_from_list(data, bounds):
    """
    Removes outliers from a list without replacement
    """
    keep = []
    for i in data:
        if i < bounds[1]:
            if i > bounds[0]:
                keep.append(i)
    
    return keep

def frequencies_from_times(data):
    if(type(data) == pd.DataFrame):
        freq_data = frequencies_from_list(data)
    if(type(data) == dict):
        freq_data = frequencies_from_dict(data) 
    if(type(data) == list):
        freq_data = frequencies_from_df(data)
    return freq_data


def frequencies_from_list(data):
    freq_data = [(1/i)*2*math.pi for i in data]
    return freq_data

def frequencies_from_dict(data):
    freq_data = {}
    for i in data:
        freq_data[i] = [(1/j)*2*math.pi for j in data[i]]
    return freq_data

def frequencies_from_df(data):
    freq_data = data.apply(lambda x: (1/x)*2*math.pi)  
    return freq_data


def bandpass(data, fs, low, high, order=3):
    """
    band pass filtering helper function to be used with the below.
    """
    b, a = butter(order, [low/(0.5*fs), high/(0.5*fs)], btype='band')
    return filtfilt(b, a, data)


def frequency_from_pulses(ie_times):
    """
    Function that takes a list of inter event times, transforms into a continuous frequency
    signal.
    """

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
    
    sigma_time = 0.1 * mean_period # 
    sigma_samp = max(1.0, sigma_time * fs)
    x_s = gaussian_filter1d(x, sigma_samp)

    nyq = 0.5 * fs
    low = max(0.1 * f0, f0 * 0.6)          # don’t go too close to 0
    high = min(f0 * 1.4, nyq * 0.9)        # stay below Nyquist
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
    return t, t_events, inst_freq  












