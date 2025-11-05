#include "oscillators.h"
#include <random>

void System::set_max_time(double t){
  tMax = t;
}

void System::set_time_step(double t){
  dt = t;
}

vector<double> System::dtheta_dt(){
  vector<double> dthetaDt;
  mt19937 gen(random_device{}());
  normal_distribution<double> noiseDist{0, 0.4335};
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

void System::eulers_method(){
  double currentTime = 0;
  while(currentTime < tMax){
    vector<double> dthetaDt = dtheta_dt();
    for(int i = 0; i != theta.size(); ++i){
      theta[i].push_back(theta[i].back() + (dthetaDt[i] * dt));
    }
    currentTime += dt;
  }
}

