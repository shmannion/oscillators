#include "oscillators.h"
#include "py_wrappers.h"

void Oscillators::set_pulse_width(double m){
  pulseWidth = m;
}

void Oscillators::set_pulse_amp(double a){
  pulseAmp = a;
}

void Oscillators::set_frequency_coupling(vector<double> C){
  if(C.size() != N){
    cerr << " number of constants must match number of oscillators" << endl;
  }else{
    frequencyCoupling = C;
  }
}

void Oscillators::set_phase_coupling(vector<double> C){
  if(C.size() != N){
    cerr << " number of constants must match number of oscillators" << endl;
  }else{
    phaseCoupling = C;
  }
}

double Oscillators::driving_pulse(int n){
 //take an oscillator index, return the pulse value
 //pulse amp and pulse width need to be defined
 double p = 0.5 + 0.5 * cos(theta[n].back());
 p = pow(p, pulseWidth);
 p += pulseAmp;
 return p;
}

double Oscillators::phase_response(int n){
  double f = -1*sin(theta[n].back());
  return f;
}


