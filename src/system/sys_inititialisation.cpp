#include "oscillators.h"

const double PI = 3.1415926536;

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

double System::draw_noise_value(){
  double x;
  if(noiseDist == "normal"){
    x = draw_normal_rnd_value(noiseParams);
  }//else if another
  return x;
}

double System::draw_omega_value(){
  double x;
  if(noiseDist == "normal"){
    x = draw_normal_rnd_value(noiseParams);
  }//else if another
  return x;

}

double System::draw_theta_value(){
  double x;
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
