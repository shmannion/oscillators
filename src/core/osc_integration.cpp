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

// vector<double> Oscillators::dtheta_dt(){
//   vector<double> dtheta = {};
//   if(model == "kuramoto"){
//     dtheta = dtheta_kuramoto();
//   }else{
//     dtheta = dtheta_weakly_coupled();
//   }
//   return dtheta;
// }

// vector<double> Oscillators::domega_dt(){
//   vector<double> domega = {};
//   domega = domega_weakly_coupled();
//   return domega;
// }

void Oscillators::integrate(double t){
  set_max_time(t);
  set_time_step(0.001);
  double currentTime = 0;
  cout << "checkpoint integrate 1" << endl;
  if(model == "weakly_coupled"){
    while(currentTime < tMax){
      cout << "checkpoint integrate 2" << endl;
      for(int i = 0; i != N; ++i){

        cout << "checkpoint integrate 3" << endl;
        rk4_step(i);
        if(OSC_VERBOSE == true){
          cout << currentTime << ", " << theta[i].back() << ", theta" << i << "\n";
          cout << currentTime << ", " << omega[i].back() << ", omega" << i << "\n";
          // cout << currentTime << ", " << test[i].back() << ", xrk" << i << "\n";
          // cout << currentTime << ", " << 3 * exp(-2*currentTime) << ", yrk" << i << "\n";
        }
      }
      currentTime += dt;
    }
  }
  else{
    eulers_method();
  }
}
void Oscillators::eulers_method(){
  double currentTime = 0;
  while(currentTime < tMax){
    vector<double> dthetaDt = dtheta_kuramoto();
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

double Oscillators::rk4(vector<double> y, int index, function<double(vector<double>)> f){
  vector<double> ytemp = y;
  double yn = y[index];
  double k1 = f(ytemp);
  ytemp[index] = yn + dt*k1/2;
  double k2 = f(ytemp);
  ytemp[index] = yn + dt*k2/2;
  double k3 = f(ytemp);
  ytemp[index] = yn + dt*k3;
  double k4 = f(ytemp);
  return yn + (dt/6)*(k1 + 2*k2 + 2*k3 + k4);
}
