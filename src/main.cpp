#include "oscillators.h"
#include "py_wrappers.h"
using namespace std;

int main(){
  set_verbose(true);
  Oscillators s(2);
  s.set_noise_distribution("normal", {0, 5.0});
  s.set_omega_distribution("default");
  s.initialise_system();
  s.set_model("kuramoto");
  s.set_coupling({{0,0.45},{0.45,0}});
  s.set_action_oscillators({0,1});
  s.set_max_time(100);
  s.kuramoto_model();
  // s.integrate(10);
}
