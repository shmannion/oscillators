#include "oscillators.h"

vector<vector<double>> Oscillators::get_inter_event_times(){
  return interEventTimes;
}

map<int, vector<vector<double>>> Oscillators::get_simulation_results(){
  return simulationResults;
}
