import mido
import numpy as np
import pandas as pd
import pretty_midi
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#import oscillators as osc
from scipy.stats import shapiro, normaltest
import math
def get_pair_times_by_trial(condition:str, pair:int, trial='all', freq:int=120):
    """
    For a given pair and condition, return a dictionary of dictionaries, keys = participant, trial. Values = list of ie
    times. E.g.,
    {1: {1: [v1,v2,...,vn], 2: [v1,v2,...,vn]}, <- participant 1, trial 1 inter event times, trial 2 inter event times
     2: {1: [v1,v2,...,vn], 2: [v1,v2,...,vn]}, <- participant 2, trial 1 inter event times, trial 2 inter event times
    """

    inter_event_times = {1: {}, 2: {}} # outer dictionary
    if pair < 10:
        pair = f'0{pair}'
    if trial == 'all':
        trials = [1,2,3,4]
    else:
        trials = trial

    for tnum in trials:
        for candidate in [1,2]:
            try:
                path = f'../data/{freq}/{condition}/pair_{pair}_c{candidate}_t{tnum}.mid'
                trial_inter_event_times = get_inter_event_times_from_file(path)

            except FileNotFoundError:
                print(f'for pair {pair} there is no trial {tnum}')
                trial_inter_event_times = []

            inter_event_times[candidate][tnum] = trial_inter_event_times

    return path



rows = []
for cond in ['self', 'other', 'comp', 'leader_follower_1','leader_follower_2']:
    for pair in range(1,17):
        for c in [1,2]:
            for trial in [1,2,3,4]:
                if pair < 10:
                    midi_path = f'../data/120/{cond}/pair_0{pair}_c{c}_t{trial}.mid'
                else:
                    midi_path = f'../data/120/{cond}/pair_{pair}_c{c}_t{trial}.mid'
                
                try:
                    midi_data = pretty_midi.PrettyMIDI(midi_path)
                except FileNotFoundError:
                    continue

                for instrument in midi_data.instruments:
                    for note in instrument.notes:
                        amplitude = note.velocity          # 0–127 (tap strength)
                        duration = note.end - note.start   # seconds
            
                        rows.append({
                            "cond": cond,
                            "pitch": note.pitch,
                            "amplitude": amplitude,
                            "duration_sec": duration,
                            "start_time": note.start
                        })

df = pd.DataFrame(rows)
for cond in ['self', 'other', 'comp', 'leader_follower_1','leader_follower_2']:
    print(f'for condition {cond}, the mean amplitude is:')
    print(df[df['cond'] == cond]['amplitude'].mean())
    print(f'for condition {cond}, the mean duration is:')
    print(df[df['cond'] == cond]['duration_sec'].describe())
