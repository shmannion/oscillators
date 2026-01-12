# Oscillators

# Overview
Code for modelling systems of coupled oscillators. To be built from ground up with features depending on the type of 
model being run, desired method of numerical integration, and available data.

# Write up
When created, an overleaf document containing a write up of this work will be added here.
slight edit
# Directory Structure
```text
  project\_root/
  │ 
  ├── include/                # C++ headers
  │   ├── oscillators.h
  │   └── py\_wrappers.h   # Python headers
  │ 
  ├── src/                    # C++ source code
  │   ├── core/
  │   │   ├── oscillators.cpp
  │   │   └── ...
  │   │
  │   ├── py/                 # Python wrappers
  │   │   ├── py\_oscillators.cpp
  │   │   └── py\_wrappers.cpp
  │   │
  │   └── main.cpp            # C++ test executable compiled into test.
  │
  ├── obj/                    # object files
  │
  ├── python/                 # Python package root
  │   ├── oscillators/        # Python package
  │   │   ├── __init__.py
  │   │   ├── core.py         # Python-side helpers / logic
  │   │   └── ... 
  │   │
  │   ├── scripts/            # Python scripts for running experiments
  │   │   ├── analysis.py
  │   │   └── simulation.py
  │   │
  │   ├── analysis/           # Python scripts for analysis of experiment output
  │   │
  │   └── oscillators.so      # C++ extension (what is imported to Python)
  │
  ├── Makefile
  │
  ├── test/                   # location of main test executable
  │ 
  └── README.md
```
  
# LATERBASE (To-do, or for now, a list of desired features)
- [x] Should take the number of coupled oscillators into a system object. There is a wrinkle here regarding the fact
  that I will have a population of dyads. Some information I will want from the global system (natural frequencies, 
  for example). The advantage of doing this is in that it will avoid the passing of large vectors/matrices.
- [ ] Depending on whether or not an order parameter is needed, variables need to have capability of being complex.
- [ ] Different methods of numerical integration should be implemented.
- [ ] Kuramoto models to start, but more should be added as time goes on. For example, th HKB model (Zhang et al.)
  I should also ask Sam, James, for more on these. Binary state dynamics useful?
- [ ] Should be simple to do but just to note that we should have the capability of including a network (adjacency 
  matrix of coupling coefficients?) in the models.
- [x] In addition to the C++ code for running the models, will need a Python component for analysing the data and
  extracting the information (for example, the natural frequencies).
- [x] To bypass the continuous distribution issue with maps, use built-in normal distribution etc.
- [ ] How to handle the complex/non-complex issue?

# Diary
Here on is a diary-like list of updates regarding the experiments and development of the package. Most recent entry first. 
Started on 5 December 2025.
## Friday — 2026-01-09

### Notes:
Working on the wekaly coupled oscillators code. Ideally, it will be in a shape where I just call rk4. This would need
lambdas defined for d\omega/dt and d\theta/dt, because then they can easily be passed into rk4. Unless I need a step
function that does the appending to omega and theta? And then rk4 just does this again and again?
### Experiment Notes:
- Experiments finished:
- Experiments failed:
- Experiments run:
- Code changes made:

---



## Wednesday — 2026-01-07

### Notes:
Changing convention of experiment scripts. Every experiment gets its own Python script now.
### Experiment Notes:
- Experiments finished:
- Experiments failed: 7 and 8
- Experiments run:
- Code changes made:

---


## Tuesday — 2025-12-23
Adding rk-4 code for weakly coupled oscillators, no functions added to header yet, only in osc\_weakly\_coupled.cpp.
### Notes:

### Experiment Notes:
- Experiments finished:
- Experiments failed:
- Experiments run:
- Code changes made:

---

## Tuesday — 2025-12-16

### Notes:

### Experiment Notes:
- Experiments finished: exp 2-4 finished. I want to now run experiment
- Experiments failed:
- Experiments run:
- Code changes made:

---




## Monday — 2025-12-08

### Notes
I have been giving some thought to what the experiments should output. I think the best thing particularly for things 
like parameter space searching is to output the phase values, in however many columns that takes. This way, a change in 
the analysis doesn't require the experiments to be run again. I will need to look at how the results are printed - the
dataframe columns must be the same length.


- Experiments finished: N/A
- Experiments failed: exp\_01 from entry 2025-12-05 (reached time limit). 
- Experiments run: resubmitted exp\_01 from entry 2025-12-05.
- Code changes made:

---


## 2025-12-05
Currently writing/using parameter searching functions in C++. Initially, these experiments will search the parameter
space and only report the mean and standard deviation of the inter event times of the action oscillators. The logic
here is that we should first find ranges of coupling coefficient and noise values that give rise to realistic 
distributions of inter-event times. Once we have that, we can start fine-tuning the parameter values to look at the
actual time series data, and correlations between inter-event times. Another piece of the puzzle that I have been 
looking at is the lack of use of the order parameter in the model used in the paper. I want to start looking at
incorporating this to see if it improves model performance. 

- Experiments: set running on HPC an experiment (exp\_01) to search the parameter space of 0-20 in steps of 0.1 both 
  for the coupling coefficient (0,1) for the action Oscillator to metronome (comp data), and for the standard deviation
  of noise.









