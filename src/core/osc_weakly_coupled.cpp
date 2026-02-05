#include "oscillators.h"
#include "py_wrappers.h"

double Oscillators::dphase_weakly_coupled(vector<double> params){
  double dphase = params[0];
  double phase1 = params[1];
  double phase2 = params[2];
  double c = params.back();
  double pulse = driving_pulse(phase2);
  double phaseResponse = phase_response(phase1);
  dphase += c*pulse*phaseResponse;
  return dphase;
}

double Oscillators::dfrequency_weakly_coupled(vector<double> params){
  double phase1 = params[1];
  double phase2 = params[2];
  double c = params.back();
  double dfrequency = 0;
  double pulse = driving_pulse(phase2);
  double phaseResponse = phase_response(phase1);
  dfrequency += c*pulse*phaseResponse;
  return dfrequency;
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

vector<double> Oscillators::get_frequency_coupling(){
  return frequencyCoupling;
}

void Oscillators::set_frequency_coupling(vector<double> C){
  if(C.size() != N){
    cerr << " number of constants must match number of oscillators" << endl;
  }else{
    frequencyCoupling = C;
  }
}

vector<double> Oscillators::get_phase_coupling(){
  return phaseCoupling;
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
  double noise = 0;
  params.push_back(frequency[index].back()); //frequency
  params.push_back(phase[index].back()); //phase of responding oscillator
  params.push_back(phase[1-index].back()); //phase of driving oscillator
  params.push_back(0); //constant
                       
  double cPhase = phaseCoupling[index];
  double cFreq = frequencyCoupling[index];
  
  auto fTheta = [this](vector<double> params){
    return dphase_weakly_coupled(params);
  };
  
  auto fOmega = [this](vector<double> params){
    return dfrequency_weakly_coupled(params);
  };
  
  // test function for rk4:
  // auto fxcubed = [this](vector<double> params){
  //   return -2 * params[0];
  // };

  params.back() = cPhase;
  double phaseNew = rk4(params, 1, fTheta);
  noise = N01(gen);
  phaseNew += pow(dt, 0.5) * phaseNoise * noise;

  params.back() = cFreq;
  double frequencyNew = rk4(params, 0, fOmega);
  noise = N01(gen);
  frequencyNew += pow(dt, 0.5) * frequencyNoise * noise;
   
  // using the test function for rk4
  // double xnew = rk4({test[index].back()}, 0, fxcubed);
  // test[index].push_back(xnew);

  frequency[index].push_back(frequencyNew);
  phase[index].push_back(phaseNew);
}

