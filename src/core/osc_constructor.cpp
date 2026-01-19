#include "oscillators.h"

Oscillators::Oscillators(int N_)
  : N(N_),
    kuramotoCoupling(N_, vector<double>(N_, 1)),
    drivers(N_, 0),
    phaseCoupling(N_, 1),
    frequencyCoupling(N_, 1),
    actionOscillators(N_, 1),
    metronomes(N_, 0)
    //additional variables to initialise go here.
{  
}


