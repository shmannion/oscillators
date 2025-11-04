#include "oscillators.h"

const double PI = 3.1415926536;

void System::set_noise_distribution(string dist){
  if(dist == "default"){
    noiseDistribution = "normal";
    noiseParams = {0,0.4335};
  }else if(dist == "normal"){
    noiseDistribution = "normal";
    noiseParams = {0,0.4335};
  }
}

void System::set_omega_distribution(string dist){
  if(dist == "default"){
    omegaDistribution = "normal";
    omegaParams = {12.57, 1.26};
  }else if(dist == "normal"){
    omegaDistribution = "normal";
    omegaParams = {12.57, 1.26};
  }
}

void System::set_theta_distribution(string dist){
  if(dist == "default"){
    thetaDistribution = "uniform";
    thetaParams = {0, 2*PI};
  }else if(dist == "uniform"){
    thetaDistribution = "uniform";
    thetaParams = {0, 2*PI};
  }
}


void System::set_noise_distribution(string dist, vector<double> params){
  if(validNoiseDistributions.find(dist) == validNoiseDistributions.end()){
    cerr << "Selected fitness distribution is not defined" << endl;
  noiseDistribution = dist;
  noiseParams = params;
}

double System::draw_noise_value(){

}

double System::draw_omega_value(){

}

double System::draw_theta_value(){

}

double System::draw_normal_rnd_value(vector<double> params){

}

double System::draw_uniform_rnd_value(vector<double> params){

}

void System::set_omega_distribution(string dist){
  omegaDistribution = dist;
}

void System::set_theta_distribution(string dist){
  thetaDistribution = dist;
}

void System::set_normal_theta_parameters(vector<double> params){
    
}

vector<double> System::initialise_omega(int len, double mu, double sig){
  //assumes normal distribution
  vector<double> omega;
  mt19937 gen(random_device{}());
  normal_distribution<double> n{mu, sig};
  double sample;
  while(g.size() < len){
    sample = n(gen);
    omega.push_back(sample);
  }
  return g;
}

vector<double> System::initialise_theta(int len){
  vector<double> theta;
  double p;
  mt19937 gen(random_device{}());
  uniform_real_distribution<double> unif_circle(0, 2*PI);
  while(theta.size() < len){
    p = unif_circle(gen);
    theta.push_back(p);
  }
  return theta;
}


