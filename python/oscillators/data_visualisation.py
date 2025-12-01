import matplotlib.pyplot as plt
import pandas as pd

def check_shape(n_plots):
    """
    Takes the number of plots needed, returns the best size to display that number of plots
    """
    if n_plots == 2:
        return [1, int(n_plots)]
    elif n_plots % 4 == 0: #4 rows
        return [4, int(n_plots/4)]
    elif n_plots % 3 == 0: #3 rows
        return [3, int(n_plots/3)]
    elif n_plots % 2 == 0: #2 rows
        return [2, int(n_plots/2)]
    elif n_plots % 2 != 0: #1 row
        return [1, int(n_plots)]

def get_plot_keys(axis_shape):
    """
    Takes the grid dimensions for plots, returns a list of co-ordinates for those plots
    """
    n_plots = int(axis_shape[0] * axis_shape[1])
    keys = []
    for i in range(0, int(axis_shape[0])):
        for j in range(0, int(axis_shape[1])):
            keys.append([i,j])

    return keys

#def plot_distribution(data, title:str="Distribution", share=False):
    """
    Function to take any data (list, list of lists, dict, df) and call the relevant function
    """

def distribution_subplots(data, title:str="Distributions", share=False):
    """
    Creates a subplots figure of the data passed. 
    """
    if(type(data) == pd.DataFrame):
        distribution_subplots_dataframe(data, title, share)
    if(type(data) == dict):
        distribution_subplots_dict(data, title, share)
        

def distribution_subplots_dict(data:pd.DataFrame, title:str="Distributions", share=False):
    """
    Creates a subplots figure from dictionary data
    """
    if len(data) > 16:
        return 0
    else:
        n_plots = len(data)

    axis_dimensions = check_shape(n_plots)
    print(axis_dimensions)
    if axis_dimensions[0] == 1: #if there is only one row, the default shape stretches them too much
        size = (9,5)
    else:
        size = (9,9)
    
    keys = get_plot_keys(axis_dimensions)
    fig, axs = plt.subplots(axis_dimensions[0], axis_dimensions[1], figsize = size, sharex=share, sharey=share)
    column_names = list(data.keys()) 
    for i in range(len(column_names)):
        if axis_dimensions[0] == 1:
            axs[i].hist(data[column_names[i]], bins=30, density=True, alpha = 0.6)
            axs[i].set_title(column_names[i])
        else:
            axs[keys[i][0], keys[i][1]].hist(data[column_names[i]], bins=30, density=True, alpha = 0.6)
            axs[keys[i][0], keys[i][1]].set_title(column_names[i])

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

def distribution_subplots_dataframe(data:pd.DataFrame, title:str="Distributions", share=False):
    """
    Creates a subplots figure from dataframe data
    """
    if data.shape[1] > 16:
        return 0
    else:
        n_plots = data.shape[1]

    axis_dimensions = check_shape(n_plots)
    if axis_dimensions[0] == 1:
        size = (9,5)
    else:
        size = (9,9)

    keys = get_plot_keys(axis_dimensions)
    fig, axs = plt.subplots(axis_dimensions[0], axis_dimensions[1], figsize = size, sharex=share, sharey=share)
    column_names = [col for col in data.columns] 
    for i in range(n_plots):
        if axis_dimensions[0] == 1:
            axs[i].hist(data.iloc[:, i].values, bins=30, density=True, alpha = 0.6)
            axs[i].set_title(column_names[i])
        else:
            axs[keys[i][0], keys[i][1]].hist(data.iloc[:, i].values, bins=30, density=True, alpha = 0.6)
            axs[keys[i][0], keys[i][1]].set_title(column_names[i])
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

def histogram(data:list, title:str=""):
    plt.hist(data, bins=30, density=True, alpha = 0.6)
    plt.title(title)
    plt.show()
