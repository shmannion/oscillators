import matplotlib.pyplot as plt
import pandas as pd

def check_shape(n_plots):
    if n_plots % 4 == 0: #4 rows
        return [4, int(n_plots/4)]
    elif n_plots % 3 == 0: #3 rows
        return [3, int(n_plots/3)]
    elif n_plots % 2 == 0: #2 rows
        return [2, int(n_plots/2)]
    elif n_plots % 2 != 0: #1 row
        return [1, int(n_plots)]

def get_plot_keys(axis_shape):
    n_plots = int(axis_shape[0] * axis_shape[1])
    keys = []
    for i in range(0, int(axis_shape[0])):
        for j in range(0, int(axis_shape[1])):
            keys.append([i,j])

    return keys

def distribution_subplots(data:pd.DataFrame, title:str="Distributions"):
    if data.shape[1] > 16:
        return 0
    else:
        n_plots = data.shape[1]

    axis_dimensions = check_shape(n_plots)
    keys = get_plot_keys(axis_dimensions)
    fig, axs = plt.subplots(axis_dimensions[0], axis_dimensions[1], figsize = (9,9))
    column_names = [col for col in data.columns] 
    for i in range(n_plots):
        axs[keys[i][0], keys[i][1]].hist(data.iloc[:, i].values, bins=30, density=True, alpha = 0.6)
        axs[keys[i][0], keys[i][1]].set_title(column_names[i])
    
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

def histogram(data:list, title:str=""):
    plt.hist(data, bins=30, density=True, alpha = 0.6)
    plt.title(title)
    plt.show()
