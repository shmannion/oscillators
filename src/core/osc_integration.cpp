#include "oscillators.h"
#include <random>

void Oscillators::set_max_time(double t){
  tMax = t;
}

double Oscillators::get_max_time(){
  return tMax;
}

void Oscillators::set_time_step(double t){
  dt = t;
}

double Oscillators::get_time_step(){
  return dt;
}


void Oscillators::eulers_method(){
  double currentTime = 0;
  while(currentTime < tMax){
    vector<double> dthetaDt = dtheta_dt();
    for(int i = 0; i != theta.size(); ++i){
      if(metronomes[i] == 1){
        theta[i].push_back(theta[i][0] + (currentTime * naturalFrequencies[i]));
      }else{
        theta[i].push_back(theta[i].back() + (dthetaDt[i] * dt));
      }
      if (OSC_VERBOSE == true){
        cout << currentTime << ", " << sin(theta[i].back()) << ", theta" << i << endl; 
      }
    }
    currentTime += dt;
  }
}

double Oscillators::rk4(double y, double t, function<double(double, double)> f){
  double k1 = f(t, y);
  double k2 = f(t + dt/2, y + dt*k1/2);
  double k3 = f(t + dt/2, y + dt*k2/2);
  double k4 = f(t + dt, y + dt*k3);
  return y + (dt/6)*(k1 + 2*k2 + 2*k3 + k4);
}
