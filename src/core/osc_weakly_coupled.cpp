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

double Oscillators::get_pulse_width(){
  double m = pulseWidth;
  if(OSC_VERBOSE == true){
    cout << "pulse width is " << m << endl;
  }
  return m;
}

void Oscillators::set_pulse_amp(double a){
  pulseAmp = a;
}

double Oscillators::get_pulse_amp(){
  double a = pulseAmp;
  if(OSC_VERBOSE == true){
    cout << "pulse amp is " << a << endl;
  }
  return a;
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
 p *= pulseAmp;
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
  cout << "checkpoint 1" << endl;
                       
  double cPhase = phaseCoupling[index];
  double cFreq = frequencyCoupling[index];
  cout << "checkpoint 2" << endl;
  
  auto fTheta = [this](vector<double> params){
    return dtheta_weakly_coupled(params);
  };
  
  auto fOmega = [this](vector<double> params){
    return domega_weakly_coupled(params);
  };
  
  // auto fxcubed = [this](vector<double> params){
  //   return -2 * params[0];
  // };

  params.back() = cPhase;
  cout << "checkpoint 3" << endl;
  double thetaNew = rk4(params, 1, fTheta);
  
  params.back() = cFreq;
  cout << "checkpoint 4" << endl;
  double omegaNew = rk4(params, 0, fOmega);
  
  // double xnew = rk4({test[index].back()}, 0, fxcubed);
  // cout << "checkpoint 5" << endl;
  // test[index].push_back(xnew);
  omega[index].push_back(omegaNew);
  theta[index].push_back(thetaNew);
}

