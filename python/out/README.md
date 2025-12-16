# Output directory

This is the output directory for the experiments I run for the oscillator project.

- exp\_01: parameter search data, for the case of the one action oscillator, one metronome experiment. Here we have 
          mu.csv, and sigma.csv. For each, the columns are the coupling coefficient value used for each experiment,
          and the rows are the standard deviation of the noise used for each experiment. These files should be used
          to create heatmaps of the parameter space, to identify regions where the distribution of inter-event times
          is close to that observed in empirical data.

- exp\_02-04: Having searched the parameter space, we are now going to vary three things over the next three experiments.
              They are:
              - time per experiment (exp\_02)
              - number of simulations in the inner loop (here, omega values stay the same between simulation runs) (exp\_03)
              - number of outer loops (equivalent to changing candidates, omega values will change) (exp\_04)
              The baseline for this is: 
              100s per experiment (neglect 20 rows from dataframe (~10 seconds)).
              100 inner loops 
              100 outer loops
              coupling = 0.45, noise standard deviation = 0.1

- exp\_05: From 2-4, we see that the only one that seems to have an effect is increasing the maximum time. I will 
           run another experiment varying it from 20s to 300s in steps of 5, while neglecting the transient.

- exp\_06: From 2-4, we see that the only one that seems to have an effect is increasing the maximum time. I will 
           run another experiment varying it from 20s to 300s in steps of 5, without neglecting the transient.

- exp\_07: Using the results of 2-4 (seeing how much these things vary with the hyper params), run a parameter search 
           of the "good" areas from exp\_01, looking this time at the lagged correlations. (Vertical area)

- exp\_08: Using the results of 2-4 (seeing how much these things vary with the hyper params), run a parameter search 
           of the "good" areas from exp\_01, looking this time at the lagged correlations. (Horizontal area)
