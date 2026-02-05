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

void Oscillators::integrate(){
  integrate(tMax);
}
void Oscillators::integrate(double t){
  set_max_time(t);
  set_time_step(0.001);
  double currentTime = 0;
  if(model == "weakly_coupled"){
    while(currentTime < tMax){
      for(int i = 0; i != N; ++i){
        rk4_step(i);
        if(OSC_VERBOSE == true){
          if(i % 100 == 0){
            cout << currentTime << ", " << phase[i].back() << ", phase" << i << endl;
            cout << currentTime << ", " << frequency[i].back() << ", freq" << i << endl; 
          }else{
            cout << currentTime << ", " << phase[i].back() << ", phase" << i << "\n";
            cout << currentTime << ", " << frequency[i].back() << ", freq" << i << "\n";
          }
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
  double noise;
  while(currentTime < tMax){
    vector<double> dphaseDt = dphase_kuramoto();
    for(int i = 0; i != phase.size(); ++i){
      if(metronomes[i] == 1){
        phase[i].push_back(phase[i][0] + (currentTime * naturalFrequencies[i]));
      }else{
        noise = N01(gen);
        noise *= pow(dt, 0.5);
        noise *= phaseNoise;
        phase[i].push_back(phase[i].back() + (dphaseDt[i] * dt) + noise);
      }
      if (OSC_VERBOSE == true){
        cout << currentTime << ", " << sin(phase[i].back()) << ", phase" << i << endl; 
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
