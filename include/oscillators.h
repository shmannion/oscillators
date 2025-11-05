#ifndef OSCILLATORS_H
#define OSCILLATORS_H

#include <random>
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <string>
#include <complex>
//File for a system of oscillators/individuals
//
using namespace std;

class System{
private:
  //distribution variables  
  string noiseDist = "normal"; //default noise distribution
  string omegaDist = "normal"; //default natural frequency distribution
  string thetaDist = "uniform"; //default distribution of initial phases
  
  set<string> validNoiseDistributions = {"default", "normal", "uniform"};
  set<string> validOmegaDistributions = {"default", "normal", "uniform"};
  set<string> validThetaDistributions = {"default", "normal", "uniform"};

  vector<double> noiseParams; //The parameters for the distribution of noise
  vector<double> omegaParams; //The parameters for the distribution of natural frequencies
  vector<double> thetaParams;

  vector<vector<double>> K; //The coupling coefficients for the model

  vector<vector<double>> theta; //Vector of vectors - phases over time, one for each oscillator
  vector<double> omega;

  vector<vector<double>> timeStamps;

  double tMax;
  double dt;

  vector<int> lags; //

  int nSimulations; //

public:
  //comments are source files in which function is written, function description comments go 
  //in source files. Uncomment functions as they are written

  System(int N) {}
  
  int N; //number of oscillators
  
  //-----------------------------------------------------------------
  void set_noise_distribution(string dist); //initialisation

  void set_omega_distribution(string dist);

  void set_theta_distribution(string dist);

  void set_noise_distribution(string dist, vector<double> params);
  
  void set_omega_distribution(string dist, vector<double> params);

  void set_theta_distribution(string dist, vector<double> params);
  
  double draw_noise_value();

  double draw_omega_value();
  
  double draw_theta_value();

  double draw_normal_rnd_value(vector<double> params);

  double draw_uniform_rnd_value(vector<double> params);
  
  //-----------------------------------------------------------------
  
  void initialise_omega(); //initialisation

  void initialise_theta(); //initialisation

  void set_coupling(vector<vector<double>>);

  //void re_initialise();

  //-----------------------------------------------------------------
  
  void set_time_step(double t); //integration

  void set_max_time(double t); //integration
  
  vector<double> dtheta_dt();

  void eulers_method();

  //-----------------------------------------------------------------
  
  

  void set_action_oscillators(vector<int>);

  void construct_time_stamps(string method); //time_series

  void construct_time_stamps_from_amplitudes();

  void construct_time_stamps_from_phases();
  
  //void construct_inter_event_times(); //time_series

  //-----------------------------------------------------------------
  
  //void set_lags(); //analysis

  //void set_lags(vector<int> lags); //analysis

  //double pearson_correlation_coefficient(int index1, int index2, int lag); //analysis

  //vector<double> get_correlations(); //analysis

  //-----------------------------------------------------------------
  
  //void set_n_simulations();
  
  //void set_n_simulations(int n);


  //-----------------------------------------------------------------
  
  //-----------------------------------------------------------------
  
  //-----------------------------------------------------------------
  
  
};

double interpolate(double x1, double y1, double x2, double y2);

double interpolate_phase(double x1, double y1, double x2, double y2);


#endif
