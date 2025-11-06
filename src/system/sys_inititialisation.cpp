#include "oscillators.h"

void System::set_noise_distribution(string dist){
  if(dist == "default"){
    noiseDist = "normal";
    noiseParams = {0,0.4335};
  }else if(dist == "normal"){
    noiseDist = "normal";
    noiseParams = {0,0.4335};
  }
}

void System::set_omega_distribution(string dist){
  if(dist == "default"){
    omegaDist = "normal";
    omegaParams = {12.57, 1.26};
  }else if(dist == "normal"){
    omegaDist = "normal";
    omegaParams = {12.57, 1.26};
  }
}

void System::set_theta_distribution(string dist){
  if(dist == "default"){
    thetaDist = "uniform";
    thetaParams = {0, 2*PI};
  }else if(dist == "uniform"){
    thetaDist = "uniform";
    thetaParams = {0, 2*PI};
  }
}


void System::set_noise_distribution(string dist, vector<double> params){
  if(validNoiseDistributions.find(dist) == validNoiseDistributions.end()){
    cerr << "Selected noise distribution is not defined" << endl;
  }else{
    noiseDist = dist;
    noiseParams = params;
  }
}

void System::set_omega_distribution(string dist, vector<double> params){
  if(validOmegaDistributions.find(dist) == validOmegaDistributions.end()){
    cerr << "Selected omega distribution is not defined" << endl;
  }else{
    omegaDist = dist;
    omegaParams = params;
  }
}

void System::set_theta_distribution(string dist, vector<double> params){
  if(validThetaDistributions.find(dist) == validThetaDistributions.end()){
    cerr << "Selected theta distribution is not defined" << endl;
  }else{
    thetaDist = dist;
    thetaParams = params;
  }
}

void System::set_default_distributions(){
  set_noise_distribution("default");
  set_omega_distribution("default");
  set_theta_distribution("default");
}

void System::set_timestamp_method(string method){
  if(validTimestampMethods.find(method) == validTimestampMethods.end()){
    cerr << "selected timestamp method is not defined" << endl;

  }else{
    if(method == "default"){
      timestampMethod = "amplitude";
    }else{
      timestampMethod = method;
    }
  }
}

double System::draw_noise_value(){
  double x = 0;
  if(noiseDist == "normal"){
    x = draw_normal_rnd_value(noiseParams);
  }//else if another
  return x;
}

double System::draw_omega_value(){
  double x = 0;
  if(noiseDist == "normal"){
    x = draw_normal_rnd_value(noiseParams);
  }//else if another
  return x;

}

double System::draw_theta_value(){
  double x = 0;
  if(noiseDist == "normal"){
    x = draw_normal_rnd_value(thetaParams);
  }else if(thetaDist == "uniform"){
    x = draw_uniform_rnd_value(thetaParams);
  }//else if another
  return x;
}

double System::draw_normal_rnd_value(vector<double> params){
  mt19937 gen(random_device{}());
  normal_distribution<double> n{params[0], params[1]};
  double sample = n(gen);
  return sample;
}

double System::draw_uniform_rnd_value(vector<double> params){
  mt19937 gen(random_device{}());
  uniform_real_distribution<double> u(params[0], params[1]);
  double sample = u(gen);
  return sample;
}


void System::initialise_omega(){
  double sample;
  while(omega.size() < N){
    sample = draw_omega_value();
    omega.push_back(sample);
  }
}

void System::initialise_theta(){
  double sample;
  for(int i = 0; i != N; ++i){
    sample = draw_theta_value();
    theta.push_back({sample});
  }
}

void System::set_coupling(vector<vector<double>> coupling){
  K = coupling;
}

void System::set_amplitude_stamp_start(int s){
  amplitudeStampStart = s;
}

void System::set_action_oscillators(vector<int> labels){
  actionOscillators = labels;
}

void System::initialise_system(){
  initialise_default_system();
}

//void System::initialise_system(){
//
//}

void System::initialise_default_system(){
  set_default_distributions();
  initialise_omega();
  initialise_theta();
  set_max_time(12);
  set_time_step(1e-3);
}
