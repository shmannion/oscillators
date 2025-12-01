import mido
import numpy as np
import pandas as pd
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#import oscillators as osc
from scipy.stats import shapiro, normaltest
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















