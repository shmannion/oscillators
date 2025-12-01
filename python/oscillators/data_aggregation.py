from .data_utils import get_inter_event_times_from_file
import pandas as pd
from os import listdir

def get_participant_distribution(condition:str, participant:tuple, freq:int=120):
    """
    For a given condition and participant (tuple of pair (1-16 inclusive) and candidate (1 or 2)), returns a list
    of the relevant inter-event times
    args:
        condition: one of {'comp', 'leader_follower_1', 'leader_follower_2', 'self', 'other'}

        participant: tuple(int) first element: Candidate pair number. Second element: Candidate number

    returns:
        list of inter event times for the participant in the condition

    """

    inter_event_times = []
    pair = participant[0]
    candidate = participant[1]
    if pair < 10:
        pair = f'0{pair}'
    for trial in range(1,5):
        try:
            path = f'../data/{freq}/{condition}/pair_{pair}_c{candidate}_t{trial}.mid'
            trial_inter_event_times = get_inter_event_times_from_file(path)
        except FileNotFoundError:
            print(f'for pair {pair} there is no trial {trial}')
            trial_inter_event_times = []
            
        for time in trial_inter_event_times:
            inter_event_times.append(time)

    return inter_event_times


def get_condition_distribution(condition:str, freq:int=120):
    """
    For a given condition, return a vector of inter-event times for all relevant trials.
    For example; leader returns all inter event times for the leader in all trials where either candidate is the leader
    args:
        condition: should be one of {'comp', 'leader', 'leader_1', 'leader_2', 'follower', 'follower_1', 'follower_2',
                                     'other', 'self'}
        
        freq: the frequency of the experiment data we are looking at. Should be one of {96, 120, 150}

    returns:
        list: list of inter event times across all trials of the relevant condition.
    """
    filepaths = []
    inter_event_times = []

    if condition in ['comp', 'other', 'self']:
        path = f'../data/{freq}/{condition}'
        files = listdir(path)
        for file in files:
            filepaths.append(f'{path}/{file}')

    if condition == 'leader':
        path_1 = f'../data/{freq}/{condition}_follower_1'
        path_2 = f'../data/{freq}/{condition}_follower_2'
        files_1 = listdir(path_1)
        files_2 = listdir(path_2)
        
        for file in files_1:
            if "c1" in file:
                filepaths.append(f'{path_1}/{file}')

        for file in files_2:
            if "c2" in file:
                filepaths.append(f'{path_2}/{file}')

    if condition == 'leader_1':
        path = f'../data/{freq}/leader_follower_1'
        files = listdir(path)
        for file in files:
            if "c1" in file:
                filepaths.append(f'{path}/{file}')

    if condition == 'leader_2':
        path = f'../data/{freq}/leader_follower_2'
        files = listdir(path)
        for file in files:
            if "c2" in file:
                filepaths.append(f'{path}/{file}')

    if condition == 'follower':
        path_1 = f'../data/{freq}/leader_follower_1'
        path_2 = f'../data/{freq}/leader_follower_2'
        files_1 = listdir(path_1)
        files_2 = listdir(path_2)
        for file in files_1:
            if "c2" in file:
                filepaths.append(f'{path_1}/{file}')

        for file in files_2:
            if "c1" in file:
                filepaths.append(f'{path_2}/{file}')

    if condition == 'follower_1':
        path = f'../data/{freq}/leader_follower_1'
        files = listdir(path)
        for file in files:
            if "c2" in file:
                filepaths.append(f'{path}/{file}')

    if condition == 'follower_2':
        path = f'../data/{freq}/leader_follower_2'
        files = listdir(path)
        for file in files:
            if "c1" in file:
                filepaths.append(f'{path}/{file}')

    for file in filepaths:
        trial_inter_event_times = get_inter_event_times_from_file(file)
        for time in trial_inter_event_times:
            inter_event_times.append(time)

    return inter_event_times


def get_distribution_per_participant(condition:str, frequency:int=120):
    """
    Take a condition, return a dataframe of the inter-event times for each participant across all of their trials.

    args:
        condition: string. The experiment we are dealing with

        frequency: int. The frequency
    returns:
        df: Pandas dataframe of candidate times
    
    """
    
    inter_event_times = {}
    min_length = 1000
    for i in range(1,17):
        for j in [1,2]:
            candidate_times = get_participant_distribution(condition, (i,j), frequency)
            if len(candidate_times) != 0:
                inter_event_times[f'pair_{i}_candidate_{j}'] = candidate_times
                if len(candidate_times) < min_length:
                    min_length = len(candidate_times)

    for candidate, times in inter_event_times.items():
        inter_event_times[candidate] = times[0:min_length]

    df = pd.DataFrame(inter_event_times)
    return df


