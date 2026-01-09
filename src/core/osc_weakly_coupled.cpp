#include "oscillators.h"
#include "py_wrappers.h"

double Oscillators::rk4(double y, double t, function<double(double, double)> f){
  double k1 = f(t, y);
  double k2 = f(t + dt/2, y + dt*k1/2);
  double k3 = f(t + dt/2, y + dt*k2/2);
  double k4 = f(t + dt, y + dt*k3);
  return y + (dt/6)*(k1 + 2*k2 + 2*k3 + k4);

void Oscillators::set_pulse_width(double m){
  pulseWidth = m;
}

void Oscillators::set_pulse_amp(double a){
  pulseAmp = a;
}

double Oscillators::pulse(int n){
 //take an oscillator index, return the pulse value
 //pulse amp and pulse width need to be defined
 double p = 0.5 + 0.5 * cos(theta[n].back());
 p = pow(p, pulseWidth);
 p += pulseAmp;
 return p;
}

double Oscillators::phase_response(int n){
  double f = -1*sin(theta[n].back());
}


