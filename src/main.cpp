#include "oscillators.h"
#include "py_wrappers.h"
using namespace std;

int main(int argc, char* argv[]){
  double k1 = 0; 
  double k2 = 0; 
  double k3 = 0; 
  double k4 = 0; 
  if(argc == 5){
    k1 = stod(argv[1]); 
    k2 = stod(argv[2]); 
    k3 = stod(argv[3]); 
    k4 = stod(argv[4]); 
  }
  cout << "ks are " << k1 << ", " << k2 << ", " << k3 << ", " << k4 << endl;
  set_verbose(true);
  Oscillators s(2);
  s.set_noise_distribution("none");
  s.set_frequency_distribution("default");
  s.initialise_system();
  s.set_phase_values({0, 1.5707});
  s.set_frequency({12.2,12.7});
  s.set_action_oscillators({1,1});
  s.set_timestamp_method("amplitude");
  s.set_model("kuramoto");
  s.set_phase_coupling({k1,k2});
  s.set_frequency_coupling({k3,k4});
  s.set_pulse_amp(0.5);
  s.set_pulse_width(64);
  s.set_kuramoto_coupling({{0,1},{5,0}});
  s.set_time_step(0.01);
  s.set_action_oscillators({0,1});
  s.set_max_time(20);
  //s.kuramoto_model();
  s.integrate();
  s.calculate_order_parameter();
  s.print_order_parameter();
  s.construct_timestamps();
  s.construct_event_times();
  s.construct_inter_event_times();
}
