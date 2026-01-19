#include "oscillators.h"
#include "py_wrappers.h"
using namespace std;

int main(int argc, char* argv[]){
  double k = 0; 
  if(argc == 2){
    k = stod(argv[1]); 
  }
  set_verbose(true);
  Oscillators s(2);
  s.set_noise_distribution("none");
  s.set_frequency_distribution("default");
  s.initialise_system();
  s.set_phase_values({0, 1.5707});
  s.set_frequency({12.2,12.7});
  s.set_model("kuramoto");
  s.set_kuramoto_coupling({{0,k},{k,0}});
  s.set_time_step(0.01);
  s.set_action_oscillators({0,1});
  s.set_max_time(10);
  s.kuramoto_model();
  // s.integrate(10);
}
