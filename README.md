# Oscillators

# Overview
Code for modelling systems of coupled oscillators. To be built from ground up with features depending on the type of 
model being run, desired method of numerical integration, and available data.

# Write up
When created, an overleaf document containing a write up of this work will be added here.

# Directory Structure
  project\_root/
  │ 
  ├── include/                # C++ headers
  │   ├── oscillators.h
  │   └── py\_oscillators.h   # Python headers
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
  │   └── main.cpp            # C++ test executable
  │
  ├── obj/                    # object files
  │
  ├── python/                 # Python package root
  │   ├── oscillators/        # Python package
  │   │   ├── __init__.py
  │   │   ├── core.py         # Python-side helpers / logic
  │   │   └── ... 
  │   │
  │   ├── scripts/            # Detailed Python scripts
  │   │   ├── analysis.py
  │   │   └── simulation.py
  │   │
  │   └── oscillators.so      # C++ extension (what is imported to Python)
  │
  ├── Makefile
  │ 
  └── README.md
  
# LATERBASE (To-do, or for now, a list of desired features)
- [ ] Should take the number of coupled oscillators into a system object. There is a wrinkle here regarding the fact
  that I will have a population of dyads. Some information I will want from the global system (natural frequencies, 
  for example). The advantage of doing this is in that it will avoid the passing of large vectors/matrices.
- [ ] Depending on whether or not an order parameter is needed, variables need to have capability of being complex.
- [ ] Different methods of numerical integration should be implemented.
- [ ] The outputs will change, for example to recreate Heggli et al. 2019, I need to output the phases to generate
  the time series.
- [ ] I will need a wider variety of distributions that needed for the CIC project, give a seperate header file for 
  these. Incorrect - since the CDFs will need to be accessed throughout, keeping them within the system object is
  necessary to again stop them being passed around.
- [ ] Kuramoto models to start, but more should be added as time goes on. For example, th HKB model (Zhang et al.)
  I should also ask Sam, James, for more on these. Binary state dynamics useful?
- [ ] Should be simple to do but just to note that we should have the capability of including a network (adjacency 
  matrix of coupling coefficients?) in the models.
- [ ] In addition to the C++ code for running the models, will need a Python component for analysing the data and
  extracting the information (for example, the natural frequencies).
- [ ] To bypass the continuous distribution issue with maps, use built-in normal distribution etc.
- [ ] How to handle the complex/non-complex issue?
