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

extern bool OSC_VERBOSE;

const double PI = 3.1415926536;

class Oscillators{
  
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

  vector<vector<double>> theta; //Vector of vectors - phases over time, one for each oscillator /needs get/set
  vector<double> omega; 

  double tMax; //needs get/set
  double dt = 0.001; //needs get/set

  vector<vector<double>> timestamps; //needs get/set /
  set<string> validTimestampMethods = {"default", "amplitude", "phase"};
  string timestampMethod; //needs get/set
  int amplitudeStampStart = 1; //needs get/set

  vector<int> actionOscillators; 
  vector<vector<double>> eventTimes; //needs get/set 
  vector<vector<double>> interEventTimes; //needs get/set (has c get)

  
  vector<int> lags; // unsure

  int nSimulations = 1; //needs get/set
  map<int, vector<vector<double>>> simulationResults;
public:
  //comments are source files in which function is written, function description comments go 
  //in source files. Uncomment functions as they are written
  int N;

  Oscillators(int N) : N(N) {}
  //Oscillators(int N) {}
  
  //int N; //number of oscillators
  
  //--------------------------------------------------------------------------------------------------------------------
  // system initialisation functions - osc_initialisation.cpp
  //--------------------------------------------------------------------------------------------------------------------
  
  void set_noise_distribution(string dist); //unexposed
  
  string get_noise_distribution(); //unexposed

  vector<double> get_noise_params(); //unexposed
  
  void set_omega_distribution(string dist); //unexposed

  string get_omega_distribution(); //unexposed
  
  vector<double> get_omega_params(); //unexposed
  
  void set_theta_distribution(string dist); //unexposed
  
  string get_theta_distribution(); //unexposed
  
  vector<double> get_theta_params(); //unexposed

  void set_noise_distribution(string dist, vector<double> params); //exposed      
  
  void set_omega_distribution(string dist, vector<double> params); //exposed

  void set_omega(vector<double> g);
  
  vector<double> get_omega();

  void set_theta_distribution(string dist, vector<double> params); //exposed
  
  double draw_noise_value(); //unexposed 

  double draw_omega_value(); //unexposed                                       
  
  double draw_theta_value(); //unexposed                            

  double draw_normal_rnd_value(vector<double> params); //unexposed             

  double draw_uniform_rnd_value(vector<double> params); //unexposed  
  
  void set_action_oscillators(vector<int>); //exposed 
  
  vector<int> get_action_oscillators(); //exposed 
  
  void initialise_omega(); //unexposed         

  void initialise_theta(); //unexposed                              

  void set_coupling(vector<vector<double>>);  //exposed                       

  vector<vector<double>> get_coupling();

  void set_amplitude_stamp_start(int s); //exposed

  int get_amplitude_stamp_start(); //exposed
  
  void set_default_distributions(); //exposed            

  void initialise_system(string method); //exposed

  void initialise_default_system(); 
  
  void initialise_custom_system(); 
  
  void reinitialise_system(string method); //exposed
  
  int get_n_simulations();
  
  void set_n_simulations(int n);
  
  //--------------------------------------------------------------------------------------------------------------------
  // integration functions osc_integration.cpp
  //--------------------------------------------------------------------------------------------------------------------
  
  void set_time_step(double t); //to be exposed
  
  double get_time_step(); //exposed

  void set_max_time(double t); //exposed
  
  double get_max_time(); //exposed
  
  vector<double> dtheta_dt(); 

  void eulers_method(); //to be exposed
  
  double interpolate(double x1, double y1, double x2, double y2); //unexposed

  double interpolate_phase(double x1, double y1, double x2, double y2); //unexposed

  //--------------------------------------------------------------------------------------------------------------------
  // time series construction functions osc_time_series.cpp
  //--------------------------------------------------------------------------------------------------------------------

  void construct_timestamps(); //unexposed
  
  void construct_timestamps(string method); //to be exposed 

  void construct_timestamps_from_amplitudes(); //unexposed

  void construct_timestamps_from_phases(); //unexposed
  
  void set_timestamp_method(string method); //exposed
  
  string get_timestamp_method(); //exposed
  
  void construct_event_times(); //unexposed

  void construct_inter_event_times(); //unexposed

  vector<vector<double>> get_inter_event_times(); //to be exposed/just give intereventTimes a getset

  map<int, vector<vector<double>>> get_simulation_results();
  //--------------------------------------------------------------------------------------------------------------------
  //--------------------------------------------------------------------------------------------------------------------

  //void set_lags(); //analysis

  //void set_lags(vector<int> lags); //analysis

  //double pearson_correlation_coefficient(int index1, int index2, int lag); //analysis

  //vector<double> get_correlations(); //analysis

  //--------------------------------------------------------------------------------------------------------------------
  //running simulations - kuramoto - osc_kuramoto.cpp 
  void kuramoto_model();

  void kuramoto_simulations(int n, string output);


  //--------------------------------------------------------------------------------------------------------------------
  //--------------------------------------------------------------------------------------------------------------------
  //--------------------------------------------------------------------------------------------------------------------
  
  
  
  
};//end class

//--------------------------------------------------------------------------------------------------------------------
// important non-member functions
//--------------------------------------------------------------------------------------------------------------------
void set_verbose(bool flag);

vector<vector<double>> kuramoto_model(int N, string settings, vector<int> actionOscillaoros, vector<vector<double>> K);












#endif
