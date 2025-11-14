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

vector<double> Oscillators::dtheta_dt(){
  vector<double> dthetaDt;
  double dtheta;
  double noise;
  for(int i = 0; i != N; ++i){
    noise = draw_noise_value();
    dtheta = omega[i] + noise;
    for(int j = 0; j != N; ++j){
      dtheta += K[i][j] * sin(theta[j].back() - theta[i].back());
    }
    dthetaDt.push_back(dtheta);
  }
  return dthetaDt;
}

void Oscillators::eulers_method(){
  double currentTime = 0;
  while(currentTime < tMax){
    vector<double> dthetaDt = dtheta_dt();
    for(int i = 0; i != theta.size(); ++i){
      if (OSC_VERBOSE == true){
        cout << currentTime << ", " << dthetaDt[i] << ", dt" << i << endl; 
      }
      theta[i].push_back(theta[i].back() + (dthetaDt[i] * dt));
    }
    currentTime += dt;
  }
}

