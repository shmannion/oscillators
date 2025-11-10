#include "oscillators.h"

vector<vector<double>> Oscillators::get_inter_event_times(){
  for(int i = 0; i != interEventTimes.size(); ++i){
    for(int j = 0; j != interEventTimes[i].size(); ++j){
      cout << interEventTimes[i][j] << endl;
    }
  }
  vector<vector<double>> x = interEventTimes;
  return x;
}
