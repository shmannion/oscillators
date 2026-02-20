#include "oscillators.h"

int Oscillators::get_N(){
  return N;
}

vector<vector<double>> Oscillators::get_inter_event_times(){
  return interEventTimes;
}

vector<vector<double>> Oscillators::get_phase_values(){
  return phase;
}

vector<vector<double>> Oscillators::get_frequency_values(){
  return frequency;
}

map<int, vector<vector<double>>> Oscillators::get_simulation_results(){
  return simulationResults;
}
