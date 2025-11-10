import sys
import os
import mido
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))    
import oscillators as osc

np.set_printoptions(legacy='1.25')

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
    

def get_correlations(df1, df2, lag=0):
  nCols = df1.shape[1]
  correlations = []
  if lag not in [-1, 0, 1]:
    print('Code not written to handle larger lags than +-1!')
    return correlations

  for i in df1.columns:
    x = pd.Series(df1[i])
    y = pd.Series(df2[i])
    x = x.dropna()
    y = y.dropna()
    if lag == 0:
      r = x.corr(y)
    if lag == -1: #put the second oscillator ahead
      x = x.drop(x.index[0])
      y = y.shift(periods=1, fill_value=0)
      y = y.drop(y.index[0])
      r = x.corr(y)
    if lag == 1:  #put the first oscillator ahaed
      y = y.drop(y.index[0])
      x = x.shift(periods=1, fill_value=0)
      x = x.drop(x.index[0])
      r = x.corr(y)
    correlations.append(r)

  return np.array(correlations)


def get_pair_correlations(condition:str, pair:int, lags:list=[-1, 0, 1], freq:int=120, neglect=0):
    """
    Take a condition (self, other, lf etc), and a pair and return the mean correlations between them
    across all their trials for that condition
    
    Args: 
        condition: what condition we are looking at. Options:
                   self
                   other
                   comp
                   lf1
                   lf2

        pair: which pair of candidates.

        lags: the lags at which we want to calculate the correlation between the time series

        freq: the tapping data frequency we are looking at. Can be
              96
              120
              150
    
        neglect: 0 = include transient
                 1 = neglect transient

    Returns:
        list: list of the correlation between the inter event times of each participant at each lag,
              averaged over their trials
    """
    candidate1 = pd.DataFrame(columns=[1,2,3,4])
    candidate2 = pd.DataFrame(columns=[1,2,3,4])
    
    if pair < 10:
        filePath = f'../data/{freq}/{condition}/pair_0{pair}'
    else:
        filePath = f'../data/{freq}/{condition}/pair_{pair}'
    
    for i in range(1,5): # create dataframe of tap times for each candidate
        try:        
            c1TapTimes = midi_to_tap_times(f'{filePath}_c1_t{i}.mid')
            c2TapTimes = midi_to_tap_times(f'{filePath}_c2_t{i}.mid')
        except FileNotFoundError:
            pass

        c1InterEvent = get_inter_event_times(c1TapTimes)
        c2InterEvent = get_inter_event_times(c2TapTimes)
        
        if neglect == 1:
            c1InterEvent = c1InterEvent[5:]
            c2InterEvent = c2InterEvent[5:]

        #print(f'for trial {i}, c1 has {len(c1InterEvent)} taps and c2 has {len(c2InterEvent)}')
        candidate1[i] = pd.Series(c1InterEvent)
        candidate2[i] = pd.Series(c2InterEvent)
        
        #print(f'after adding trial {i}, df1 has shape {candidate1.shape},') 
        #print(f'and df2 has shape {candidate2.shape}')

    corrDict = {}
    
    for lag in lags:
        correlations = get_correlations(candidate1, candidate2, lag)
        corrDict[lag] = correlations
    
    return corrDict

def get_correlation_means(data:dict):
    """
    Take the correlation data in the form data:pair:lag:np.array and calculate the
    means and standard errors
    """
    pairs = list(data.keys())    
    lags = list(data[pairs[0]].keys())
    rootN = len(pairs) ** 0.5
    summary = {}

    for lag in lags:
        means = []
        for pair in pairs:
            means.append(np.mean(data[pair][lag]))

        means = np.array(means)
        summary[lag] = [np.mean(means), np.std(means), np.std(means)/rootN] 

        print(means)
    return summary

def bhattacharyya_coefficient(p, q):
    """
    Compute the Bhattacharyya coefficient between two discrete distributions or vectors.

    Parameters
    ----------
    p, q : array-like
        Non-negative arrays of the same length.
        They don’t need to be normalized; the function will normalize them.

    Returns
    -------
    bc : float
        Bhattacharyya coefficient in [0, 1].
        1 = identical, 0 = no overlap.
    """
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    
    # Check for valid input
    if np.any(p < 0) or np.any(q < 0):
        raise ValueError("Inputs must be non-negative.")
    
    # Normalize to sum to 1 (make them behave like distributions)
    p /= np.sum(p)
    q /= np.sum(q)
    
    # Compute Bhattacharyya coefficient
    bc = np.sum(np.sqrt(p * q))
    return bc


if __name__ == "__main__":
    """
    #TODO:
    x Get the average for the 4 trials within each pair
    x Get the average of the average for each pair across all pairs
    
    Get the C++ code loaded in here
    Run model
    Compare
    """

    if len(sys.argv) < 2:
        print("Usage: python midi_to_tap_times.py <midi_file> [note_number]")
        midiPath = 'data/6_1_other.mid'
    
    #midiPath = sys.argv[1]
    midiPath = '../data/120/leader_follower_1/pair_01_c1_t1.mid'
    #file1 = mido.MidiFile('data/6_1_other.mid') for msg in file1: print(msg)
    tapTimes = midi_to_tap_times(midiPath)
    print("Detected tap times (seconds):")
    for t in tapTimes:
        print(f"{t:.3f}")

    print(f"\nTotal taps: {len(tapTimes)}")

    interEventTimes = get_inter_event_times(tapTimes)
    

    results = {}
    lags = [-1, 0, 1]    
    for i in range(1,17): 
        results[i] = get_pair_correlations('leader_follower_1', i, neglect=1)
    
    means = {}
    for i in range(1, 17):
        means[i] = {}
        for lag in [-1, 0, 1]:
            means[i][lag] = results[i][lag].mean()

    
    K = []
    i1 = 0.6*5.5
    e1 = 0.1*1.7
    i2 = 0.1*1.5
    e2 = 0.6*5.5


    K.append([0,i1,e1,0])
    K.append([i1,0,0,0])
    K.append([0,0,0,i2])
    K.append([0,e2,i2,0])
    
    x = osc.kuramoto_model(4, "default", [0,2], K)
    modelTimes1 = pd.Series(x[0])
    modelTimes2 = pd.Series(x[1])
    df1 = pd.DataFrame(modelTimes1)
    df2 = pd.DataFrame(modelTimes2)
    modelResults = []
    lags = [-1, 0, 1]

    for lag in lags:
        modelResults.append(get_correlations(df1, df2, lag))


    summary = get_correlation_means(results)

    print(summary)
    yVals = [summary[i][0] for i in lags]
    yErr = [summary[i][2] for i in lags]
    plt.bar(lags, yVals, yerr=yErr, capsize=5)
    plt.plot(lags, modelResults)
    plt.show()
    
    print(x[0]) 

