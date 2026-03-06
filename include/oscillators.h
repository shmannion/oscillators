#ifndef OSCILLATORS_H
#define OSCILLATORS_H

#include <random>
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <string>
#include <complex>
#include <functional>
//File for a system of oscillators/individuals
//
using namespace std;

extern bool OSC_VERBOSE;

const double PI = 3.1415926536;

class Oscillators{
  
private:
  int N;
  //distribution variables  
  string noiseDist = "normal"; //default noise distribution 
  string frequencyDist = "normal"; //default natural frequency distribution 
  string phaseDist = "uniform"; //default distribution of initial phases 
  string model = "kuramoto";
  
  set<string> validNoiseDistributions = {"default", "normal", "uniform"};
  set<string> validOmegaDistributions = {"default", "normal", "uniform", "fixed"};
  set<string> validThetaDistributions = {"default", "normal", "uniform", "fixed"};
  set<string> validModels = {"kuramoto", "weakly_coupled"};

  vector<double> noiseParams; //The parameters for the distribution of noise 
  double phaseNoise = 0.4335;                              
  double frequencyNoise = 0.4335;                              
  vector<double> frequencyParams; //The parameters for the distribution of natural frequencies 
  vector<double> phaseParams; 
    
  mt19937 gen{random_device{}()};
  normal_distribution<double> N01{0, 1};

  //coupling coefficient, oscillator phases and frequencies
  vector<vector<double>> kuramotoCoupling; //The coupling coefficients for the model 

  vector<vector<double>> phase; //Vector of vectors - phases over time, one for each oscillator /needs get/set
  vector<vector<double>> frequency;
  vector<double> naturalFrequencies; 
  vector<complex<double>> meanPhase = {};                              

  //simulation variables - global
  
  double tMax = 20; 
  double dt = 0.01; 

  //simulation variables - kuramoto
  vector<double> orderParam = {};

  //simulation variables - weakly coupled oscillators
  double pulseWidth = 0;
  double pulseAmp = 0;
  vector<int> drivers;
  vector<double> phaseCoupling;
  vector<double> frequencyCoupling;
  // vector<vector<double>> test = {{3}, {3}};

  vector<vector<double>> timestamps; //needs get/set /
  set<string> validTimestampMethods = {"default", "amplitude", "phase"};
  string timestampMethod = "phase"; //needs get/set
  int amplitudeStampStart = 1; //needs get/set

  vector<int> actionOscillators; 
  vector<int> metronomes; //if metronomes[i] == 1, oscillator i is a metronome
  vector<vector<double>> eventTimes; //needs get/set 
  vector<vector<double>> interEventTimes; //needs get/set (has c get)

  vector<int> lags; // unsure

  int nSimulations = 1; //needs get/set
  map<int, vector<vector<double>>> simulationResults;
  map<int, vector<double>> configLabels;

public:
  //comments are source files in which function is written, function description comments go 
  //in source files. Uncomment functions as they are written

  Oscillators(int N);
  //Oscillators(int N) {}
  
  //int N; //number of oscillators
  
  //--------------------------------------------------------------------------------------------------------------------
  // system initialisation functions - osc_initialisation.cpp
  //--------------------------------------------------------------------------------------------------------------------
  int get_N();
  
  void set_noise_distribution(string dist); //unexposed

  void set_phase_noise(double s);
  
  double get_phase_noise();
  
  void set_frequency_noise(double s);
  
  double get_frequency_noise();
  
  string get_noise_distribution(); //unexposed

  vector<double> get_noise_params(); //unexposed
  
  void set_frequency_distribution(string dist); //unexposed

  string get_frequency_distribution(); //unexposed
  
  vector<double> get_frequency_params(); //unexposed
  
  void set_phase_distribution(string dist); //unexposed
  
  string get_phase_distribution(); //unexposed
  
  vector<double> get_phase_params(); //unexposed

  void set_noise_distribution(string dist, vector<double> params); //exposed      
  
  void set_frequency_distribution(string dist, vector<double> params); //exposed

  void set_frequency(vector<double> g);
  
  vector<double> get_frequency();

  vector<vector<double>> get_frequency_values();
  
  vector<vector<double>> get_phase_values();

  void set_phase_distribution(string dist, vector<double> params); //exposed
  
  void set_phase_values(vector<double> params); //exposed
  
  double draw_noise_value(); //unexposed 

  double draw_frequency_value(); //unexposed                                       
  
  double draw_phase_value(); //unexposed                            

  double draw_normal_rnd_value(vector<double> params); //unexposed             

  double draw_uniform_rnd_value(vector<double> params); //unexposed  
  
  void set_action_oscillators(vector<int>); //exposed 
  
  vector<int> get_action_oscillators(); //exposed 
  
  void set_metronomes(vector<int>); //exposed 
  
  vector<int> get_metronomes(); //exposed 
  
  void initialise_natural_frequencies(); //unexposed         
                           
  void initialise_frequency(); //unexposed         

  void initialise_phase(); //unexposed                              

  void set_kuramoto_coupling(vector<vector<double>>);  //exposed                       

  vector<vector<double>> get_kuramoto_coupling();

  void set_amplitude_stamp_start(int s); //exposed

  int get_amplitude_stamp_start(); //exposed
  
  void set_default_distributions(); //exposed            

  void initialise_system(string method); //exposed

  void initialise_system(); //exposed

  void reinitialise_system(string method); //exposed
  
  int get_n_simulations();
  
  void set_n_simulations(int n);
  
  //--------------------------------------------------------------------------------------------------------------------
  // integration functions osc_integration.cpp
  //--------------------------------------------------------------------------------------------------------------------
  
  void set_model(string s);

  string get_model();

  void set_time_step(double t); //to be exposed
  
  double get_time_step(); //exposed

  void set_max_time(double t); //exposed
  
  double get_max_time(); //exposed
  
  void eulers_method(); //to be exposed
  
  double interpolate(double x1, double y1, double x2, double y2); //unexposed

  double interpolate_phase(double x1, double y1, double x2, double y2); //unexposed
  
  double rk4(vector<double> y, int index, function<double(vector<double>)> f);

  void rk4_step(int index);

  void integrate();

  void integrate(double t);

  // vector<double> dphase_dt();

  // vector<double> dfrequency_dt();

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

  vector<double> dphase_kuramoto();

  void kuramoto_model();

  void calculate_order_parameter();

  void print_order_parameter();

  void kuramoto_simulations(int n, string output);

  vector<vector<double>> coupling_parameter_search_1d(vector<vector<int>> varyingIndices, vector<double> bounds, double step);

  map<int, vector<vector<double>>> parameter_search_e7();
  
  map<int, vector<vector<double>>> parameter_search_e8();
  //--------------------------------------------------------------------------------------------------------------------
  //weakly coupled oscillators model
  //--------------------------------------------------------------------------------------------------------------------
  void set_drivers(vector<int> d);

  void set_pulse_width(double m);
  
  double get_pulse_width();

  void set_pulse_amp(double a);
  
  double get_pulse_amp();

  vector<double> get_frequency_coupling(); //unexposed
  
  vector<double> get_phase_coupling(); //unexposed
                                         //
  void set_phase_coupling(vector<double> C);

  void set_frequency_coupling(vector<double> C);

  double phase_response(double phase);

  double driving_pulse(double phase);

  double dphase_weakly_coupled(vector<double> params);

  double dfrequency_weakly_coupled(vector<double> params);
  //--------------------------------------------------------------------------------------------------------------------
  
  
  
  
};//end class

//--------------------------------------------------------------------------------------------------------------------
// important non-member functions
//--------------------------------------------------------------------------------------------------------------------
void set_verbose(bool flag);

vector<vector<double>> kuramoto_model(int N, string settings, vector<int> actionOscillaoros, vector<vector<double>> K);

double vector_mean(vector<double> x);

double vector_mean_2d(vector<vector<double>> x);

double standard_deviation(vector<double> x);

double standard_deviation_2d(vector<vector<double>> x);








#endif
