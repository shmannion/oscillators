#include "oscillators.h"
#include "py_wrappers.h"

//void Oscillators::coupling_parameter_search(vector<vector<int>> varyingIndices, vector<double> bounds, double step){
//  if(varyingIndices.size() == 1){
//    
//  }
//  
//}

map<int, vector<vector<double>>> Oscillators::parameter_search(){
  vector<double> bounds = {0,20};
  double step = 0.1;
  vector<int> couplingIndex = {0,1};
  vector<vector<double>> coupling = {};
  for(int i = 0; i != N; ++i){
    coupling.push_back({});
    for(int j = 0; j != N; ++j){
      coupling[i].push_back(0);
    }
  }
  vector<double> singleResult = {};
  vector<double> searchedValues = {};
  vector<double> currentSummary = {};
  map<int, vector<vector<double>>> summaryValues;
  for(int sig = 0; sig != 200; ++sig){
    summaryValues[sig] = {};
    double k = bounds[0];
    while(k <= bounds[1]){
      vector<vector<double>> simResults = {};
      set_noise_distribution("normal", {0, double(sig) * 0.1});
      searchedValues.push_back(k);
      currentSummary = {};
      coupling[couplingIndex[0]][couplingIndex[1]] = k;
      K = coupling;
      kuramoto_simulations(100, "interEventTimes");
      for(int i = 0; i != actionOscillators.size(); ++i){
        for(auto itr = simulationResults.begin(); itr != simulationResults.end(); ++itr){
          singleResult = itr->second[i];
          simResults.push_back(singleResult);
        }
      }
      currentSummary.push_back(vector_mean_2d(simResults));
      currentSummary.push_back(standard_deviation_2d(simResults));
      summaryValues[sig].push_back(currentSummary);
      k += step;
      reinitialise_system("default");
    }
  }
  return summaryValues;
}

vector<vector<double>> Oscillators::coupling_parameter_search_1d(vector<vector<int>> varyingIndices, vector<double> bounds, double step){
  vector<vector<double>> coupling = {};
  for(int i = 0; i != N; ++i){
    coupling.push_back({});
    for(int j = 0; j != N; ++j){
      coupling[i].push_back(0);
    }
  }
  double k = bounds[0];
  vector<vector<double>> simResults = {};
  vector<double> singleResult = {};
  vector<double> searchedValues = {};
  vector<double> currentSummary = {};
  vector<vector<double>> summaryValues = {};
  while(k <= bounds[1]){
    searchedValues.push_back(k);
    currentSummary = {};
    coupling[varyingIndices[0][0]][varyingIndices[0][1]] = k;
    K = coupling;
    kuramoto_simulations(100, "interEventTimes");
    for(int i = 0; i != actionOscillators.size(); ++i){
      for(auto itr = simulationResults.begin(); itr != simulationResults.end(); ++itr){
        singleResult = itr->second[i];
        simResults.push_back(singleResult);
      }
      currentSummary.push_back(vector_mean_2d(simResults));
      currentSummary.push_back(standard_deviation_2d(simResults));
      summaryValues.push_back(currentSummary);
    }
    k += step;
    reinitialise_system("default");
  }
  return summaryValues;
}
