import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

def heatmap(data, target:str="min", small_vals=False, title:str="",  xlab="", ylab=""):
    if(type(data) == list):
        heatmap_from_lists(data, target, small_vals, title,  xlab, ylab)
    if(type(data) == pd.DataFrame):
        heatmap_from_df(data, target, small_vals, title,  xlab, ylab)


def heatmap_from_df(data:pd.DataFrame, target:str="min", small_vals=False, title:str="",  xlab="", ylab=""):
    n_x = np.min([10, len(data.columns)])                                                      
    n_y = np.min([10, len(data.index)]) 
    if n_x < 10:
        n_x = 1
    if n_y < 10:
        n_y = 1
    x_unique = list(data.columns)
    if type(x_unique[0] == str):
        x_unique = [float(i) for i in x_unique]

    y_unique = list(data.index)
    if small_vals == True:
        data = data.apply(np.log)
        data *= -1
        target = "max"
    plt.figure(figsize=(8,6))                                     
    plt.imshow(data, cmap='coolwarm', origin='lower')
    if(target == "max"):
        plt.colorbar(label="Value (larger is better)")                 
    else:
        plt.colorbar(label="Value (smaller is better)")                 

    print(f'len of columns is {len(x_unique)}')
    plt.xticks(                                                   
        ticks=np.arange(0, len(x_unique), n_x),                       
        labels=[f"{val:.3f}" for val in x_unique[::n_x]], rotation=45)
    
    plt.yticks(                                                   
        ticks=np.arange(0, len(y_unique), n_y),                       
        labels=[f"{val:.2f}" for val in y_unique[::n_y]])             
    
    plt.xlabel(xlab)                          
    plt.ylabel(ylab)                        
    plt.title(title)
                                                             
    plt.show()

def heatmap_from_lists(data:list, target:str="min", small_vals=False, title:str="",  xlab="", ylab=""):
    """
    Take list of 3 numpy arrays. Create heatmap of them.
    args:
        data: list of 3 numpy arrays

        target: "min" or "max": whether we are trying to maximise or minimise

        title: plot title

        small_vals: bool. If True, uses log of Z values
    """

    X = data[0]                                            
    Y = data[1] 
    Z = data[2]
    if(small_vals == True):
        Z = -1*np.log(Z)
        target = "max"

                                                             
    # Get unique sorted coordinates                          
    x_unique = np.unique(X)                                  
    y_unique = np.unique(Y)                                  
                                                             
    # Create grid for the heatmap                            
    heatmap = np.full((len(y_unique), len(x_unique)), np.nan)
                                                                  
    # Fill grid with Z values                                     
    for xi, yi, zi in zip(X, Y, Z):                               
        x_idx = np.where(x_unique == xi)[0][0]                    
        y_idx = np.where(y_unique == yi)[0][0]                    
        heatmap[y_idx, x_idx] = zi                                
                                                                  
    # Plot                                                        
    n_x = np.min([10,len(x_unique)])                                                      
    n_y = np.min([10,len(y_unique)])                                                      
    if n_x < 10:
        n_x = 1
    if n_y < 10:
        n_y = 1
    
    plt.figure(figsize=(8,6))                                     
    plt.imshow(heatmap, cmap='coolwarm', origin='lower')         
    if(target == "max"):
        plt.colorbar(label="Value (larger is better)")                 
    else:
        plt.colorbar(label="Value (smaller is better)")                 

    plt.xticks(                                                   
        ticks=np.arange(0, len(x_unique), n_x),                       
        labels=[f"{val:.3f}" for val in x_unique[::n_x]], rotation=45)
    
    plt.yticks(                                                   
        ticks=np.arange(0, len(y_unique), n_y),                       
        labels=[f"{val:.2f}" for val in y_unique[::n_y]])             
    
    plt.xlabel(xlab)                          
    plt.ylabel(ylab)                        
    plt.title(title)
                                                             
    plt.show()                                               


def correlation_plots(data:dict):
    # lags = list(data.keys())
    # plt.figure(figsize)
    lags = sorted(data.keys())
    means = []
    stderr = []

    for lag in lags:
        values = np.array(data[lag])
        means.append(values.mean())
        stderr.append(values.std(ddof=1) / np.sqrt(len(values)))

    plt.bar(lags, means, yerr=stderr, capsize=5)
    plt.xlabel("lag")
    plt.ylabel("Mean value")
    plt.title("Experiment results (mean ± SE)")
    plt.show()

def plot_correlation_comparison(results_a, results_b, label_a="empirical", label_b="model", saveloc=""):
    # Ensure both dictionaries share the same experiment numbers
    lags = sorted(set(results_a.keys()))
    x = np.arange(len(lags))
    width = 0.35

    means_a = []
    stderr_a = []
    means_b = []
    stderr_b = []

    for lag in lags:
        a_vals = np.array(results_a[lag])
        b_vals = np.array(results_b[lag])

        means_a.append(a_vals.mean())
        stderr_a.append(a_vals.std(ddof=1) / np.sqrt(len(a_vals)))

        means_b.append(b_vals.mean())
        stderr_b.append(b_vals.std(ddof=1) / np.sqrt(len(b_vals)))

    plt.figure(figsize=(7, 4))

    plt.bar(
        x - width / 2,
        means_a,
        width,
        yerr=stderr_a,
        capsize=5,
        label=label_a
    )

    plt.bar(
        x + width / 2,
        means_b,
        width,
        yerr=stderr_b,
        capsize=5,
        label=label_b
    )

    plt.xticks(x, lags)
    plt.xlabel("lag")
    plt.ylabel("Mean value")
    plt.title("Empirical vs model")
    plt.legend()
    plt.tight_layout()
    if saveloc != "":
        plt.savefig(saveloc)
    else:
        plt.show()

