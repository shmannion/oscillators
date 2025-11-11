import mido
import numpy as np
import pandas as pd
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#import oscillators as osc
from scipy.stats import shapiro, normaltest


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
 
 

