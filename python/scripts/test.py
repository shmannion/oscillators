import sys
import os

# Add the parent 'python' folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import oscillators as osc

K = []
K.append([0,6.5,1.5,0])
K.append([6.5,0,0,0])
K.append([0,0,0,7.8])
K.append([0,1.3,7.8,0])

x = osc.kuramoto_model(4, "default", [0,2], K)


print(x)
