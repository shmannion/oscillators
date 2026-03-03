import optuna
import numpy as np
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import oscillators as osc


# Fix these or add them as trial parameters too
# Get all trials that satisfy your conditions

df_good = pd.read_csv('good_params.csv')
print(df_good.describe())


