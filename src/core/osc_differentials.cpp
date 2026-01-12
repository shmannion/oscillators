#include "oscillators.h"
#include "py_wrappers.h"

vector<double> Oscillators::dtheta_dt(){
  vector<double> dtheta = {};
  if(model == "kuramoto"){
    dtheta = dtheta_kuramoto();
  }else{
    dtheta = dtheta_weakly_coupled();
  }
  return dtheta;
}

vector<double> Oscillators::domega_dt(){
  vector<double> domega = {};
  domega = domega_weakly_coupled();
  return domega;
}

vector<double> Oscillators::dtheta_weakly_coupled(){
  vector<double> dtheta = {};
  for(int i = 0; i != N; ++i){
    double x = omega[i].back();
    double pulse = driving_pulse(drivers[i]);
    double phaseResponse = phase_response(i);
    x += phaseCoupling[i]*pulse*phaseResponse;
    dtheta.push_back(x);
  }  
  return dtheta;
}

vector<double> Oscillators::domega_weakly_coupled(){
  vector<double> domega = {};
  for(int i = 0; i != N; ++i){
    double pulse = driving_pulse(drivers[i]);
    double phaseResponse = phase_response(i);
    double x = frequencyCoupling[i]*pulse*phaseResponse;
    domega.push_back(x);
  }  
  return domega;
}

vector<double> Oscillators::dtheta_kuramoto(){
  vector<double> dthetaDt;
  double dtheta;
  double noise;
  for(int i = 0; i != N; ++i){
    if(metronomes[i] == 1){
      noise = 0;
    }else{
      noise = draw_noise_value();
    }
    dtheta = naturalFrequencies[i] + noise;
    for(int j = 0; j != N; ++j){
      dtheta += K[i][j] * sin(theta[j].back() - theta[i].back());
    }
    dthetaDt.push_back(dtheta);
  }
  return dthetaDt;
}
