#include "oscillators.h"
#include "py_wrappers.h"
using namespace std;

int main(){
  for(int i = 1; i != 11; ++i){
    double coupling = double(i);
    vector<vector<double>> K = {{0, coupling}, {0,0}};
    Oscillators s(2);
    s.initialise_system("default");
    s.set_metronomes({1});
    s.set_action_oscillators({0, 1});
    s.set_coupling(K);
    s.set_omega({8, 12.567});
    s.set_noise_distribution("normal", {0, 0.01});
    s.set_timestamp_method("amplitude");
    s.set_time_step(0.001);
    s.set_max_time(100);
    s.kuramoto_simulations(1, "interEventTimes");
  }
}
