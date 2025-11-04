#include "oscillators.h"
#include <random>

vector<double> System::dtheta_dt(vector<vector<double>> K, vector<double> thetaT, vector<double> g){
  vector<double> dthetaDt;
  mt19937 gen(random_device{}());
  normal_distribution<double> noiseDist{0, 0.4335};
  double dtheta;
  double noise;
  for(int i = 0; i != thetaT.size(); ++i){
    noise = noiseDist(gen);
    dtheta = g[i] + noise;
    for(int j = 0; j != K[i].size(); ++j){
      dtheta += K[i][j] * sin(thetaT[j] - thetaT[i]);
    }
    dthetaDt.push_back(dtheta);
  }
  return dthetaDt;
}

vector<vector<double>> System::eulers_method(vector<double> g){
  double time = 0;
  double dt = 0.001;
  vector<double> thetaT;
  while(time < tMax){
    thetaT = {};
    for(int i = 0; i != theta.size(); ++i){
      thetaT.push_back(theta[i].back());
    }
    vector<double> dthetaDt = dtheta_dt(K, thetaT, g);
    for(int i = 0; i != theta.size(); ++i){
      theta[i].push_back(thetaT[i] + (dthetaDt[i] * dt));
    }
    time += dt;
  }
  return theta;
}

