#include "oscillators.h"
#include "py_wrappers.h"
using namespace std;

int main(){
  Oscillators s(2);
  s.initialise_system("default");
  s.set_model("weakly_coupled");
  string m = s.get_model();
  s.set_pulse_amp(0.5);
  double a = s.get_pulse_amp();
  s.set_pulse_width(2);
  double w = s.get_pulse_width();
  s.set_phase_coupling({1,2});
  s.set_frequency_coupling({1,2});
  double p = s.driving_pulse(0);
  cout << "pulse val for 0 is " << p << "\n";
  p = s.driving_pulse(1);
  cout << "pulse val for 1 is " << p << "\n";
  double r = s.phase_response(0);
  cout << "phase response for 0 is " << r << "\n";
  r = s.phase_response(1);
  cout << "phase response for 1 is " << r << "\n";
  double dt = s.dtheta_weakly_coupled({12, 1.0, 0.5, 1.5});
  cout << "dtheta is " << dt << "\n"; 
  double dw = s.domega_weakly_coupled({12, 0.5, 1.2, 2});
  cout << "domega is " << dw << "\n"; 
  s.set_omega({12, 12.5});
  s.set_theta_values({0, 0.5});
  s.integrate(10);
}
