#include "oscillators.h"
#include "py_wrappers.h"

double Oscillators::dtheta_weakly_coupled(vector<double> params){
  double dtheta = params[0];
  double phase1 = params[1];
  double phase2 = params[2];
  double c = params.back();
  double pulse = driving_pulse(phase2);
  double phaseResponse = phase_response(phase1);
  dtheta += c*pulse*phaseResponse;
  return dtheta;
}

double Oscillators::domega_weakly_coupled(vector<double> params){
  double phase1 = params[1];
  double phase2 = params[2];
  double c = params.back();
  double domega = 0;
  double pulse = driving_pulse(phase2);
  double phaseResponse = phase_response(phase1);
  domega += c*pulse*phaseResponse;
  return domega;
}

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

double Oscillators::driving_pulse(double phase){
 //take an oscillator index, return the pulse value
 //pulse amp and pulse width need to be defined
 double p = 0.5 + 0.5 * cos(phase);
 p = pow(p, pulseWidth);
 p += pulseAmp;
 return p;
}

double Oscillators::phase_response(double phase){
  double f = -1*sin(phase);
  return f;
}

void Oscillators::rk4_step(int index){
  vector<double> params = {};
  params.push_back(omega[index].back()); //frequency
  params.push_back(theta[index].back()); //phase of responding oscillator
  params.push_back(theta[1-index].back()); //phase of driving oscillator
  params.push_back(0); //constant
                       
  double cPhase = phaseCoupling[index];
  double cFreq = frequencyCoupling[index];
  
  auto fTheta = [this](vector<double> params){
    return dtheta_weakly_coupled(params);
  };
  
  auto fOmega = [this](vector<double> params){
    return domega_weakly_coupled(params);
  };

  params.back() = cPhase;
  double thetaNew = rk4(params, 1, fTheta);
  
  params.back() = cFreq;
  double omegaNew = rk4(params, 0, fOmega);
  
  omega[index].push_back(omegaNew);
  theta[index].push_back(thetaNew);
}

