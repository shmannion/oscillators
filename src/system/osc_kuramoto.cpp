#include "oscillators.h"

vector<vector<double>> kuramoto_model(int N, string settings, vector<int> actionOscillators, vector<vector<double>> K){
  Oscillators S(4);
  if(settings == "default"){
    S.initialise_default_system();
  }
  S.set_coupling(K);
  S.set_action_oscillators(actionOscillators);
  S.eulers_method();
  S.construct_timestamps();
  S.construct_event_times();
  S.construct_inter_event_times();
  vector<vector<double>> x = S.get_inter_event_times();
  return x;
}
