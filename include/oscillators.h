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
  string noiseDistribution = "normal"; //default noise distribution
  string omegaDistribution = "normal"; //default natural frequency distribution
  string thetaDistribution = "uniform"; //default distribution of initial phases


  vector<double> noiseParameters; //The parameters for the distribution of noise
  vector<double> omegaParameters; //The parameters for the distribution of natural frequencies
  vector<vector<double>> coupling; //The coupling coefficients for the model

  vector<vector<double>> theta; //Vector of vectors - phases over time, one for each oscillator

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
  //void set_noise_distribution(string dist); //distributions

  //void set_omega_distribution(string dist);

  //void set_theta_distribution(string dist);

  //void set_noise_parameters(vector<double> params);
  
  //void set_omega_parameters(vector<double> params);

  //-----------------------------------------------------------------
  
  //void initialise_omega(); //initialisation

  //void initialise_theta(); //initialisation

  //void set_coupling(vector<vector<double>>);

  //void re_initialise();

  //-----------------------------------------------------------------
  
  //void set_timestep(double t); //integration

  //void set_max_time(double t); //integration
  
  //vector<double> dtheta_dt();

  //void eulers_method();

  //-----------------------------------------------------------------
  
  //void set_action_oscillators(vector<int>);

  //void construct_time_stamps(string method); //time_series

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
  
  
  //Functions for setting up memes
  
  void setMu(double p); //memeinit

  void setInputFitnessDistribution(); //memeinit

  void setInputFitnessDistribution(vector<double> pdf, vector<double> fitness); //memeinit

  void set_ages(vector<double> a);

  void set_input_lambdas(vector<double> lambdas);

  void set_emergent_fitness_distribution();

  void initialise_memes(); //memeinit
  
  void initialise_memes(string setting); //memeinit

  void clearMemes(); //memeinit

  void resetMemes();  //memeinit

  void resetMemes(string setting);

  void set_max_time(double t); //memeinit

  void set_strategy(bool b);
  //-----------------------------------------------------------------

  //Functions for running the simulations

  void runSimulationRandomSelection(); //randselection

  void randomSelectionUniform(); //randselection
  
  void randomSelectionBimodal(); //randselection
  
  void runSimulationGillespie(); //gillespie

  void get_emergent_parameters(); // gillespie

  void runSimulationGillespie(string rewireType, double rewireEvery, bool neglectTransient); //gillespie 

  void run_simulation_cascade_times();
  //-----------------------------------------------------------------

  //Functions for checking meme ages and printing simulation results
  
  void checkAges(double tol);  
  
  void print_q_values(vector<double> cascades); //results

  void printSValues(double currentTime);

  void memeCountFitnessClass(map<int, int> count, int t);

  void getProbabilities(map<int, int> count, int t, int fitnessIndex);

  void print_emergent_values();

  //-----------------------------------------------------------------

  //Functions for mean field approximations
  
  double dqdt(double qi, int index);

  double dsdt(double si, double fi, double pi); //meanfield

  void q_meanfield();

  void eulersMethod(); //meanfield

  //-----------------------------------------------------------------
  
  //Functions for rewiring the graph
  
  void randomRewire(); //rewire

  void rewirePreserveS(); //rewire

  //----------------------------------------------------------------

  //Functions for PGFs here

  void set_zeta(int kMin); //in graph_degree_dist
  
  void set_ri(complex<double> r); //will set it to the input vector
  
  void set_ri(); //will set it to the input vector
  
  void print_ri(); //memeinit

  void print_fbar(); //memeinit
  
  void set_initial_fbar(); //memeinit

  void set_complex_fitness(); //memeinit

  void set_complex_fbar(); //memeinit
  
  void set_emergent_complex_values();

  void set_output_vals(); // results

 
  complex<double> create_x_in(double m, int fftPower);
  
  double regular_pgf(double x);

  double polylog(double x, int kMin);

  double powerlaw_pgf(double x);

  double bernoulli_q(double x, int index);
  
  double outdegree_pgf(double x, int index);
  
  double outdegree_plus_one(double x, int index);
  
  complex<double> regular_pgf(complex<double> x);
  
  complex<double> bernoulli_pgf(complex<double> x);
  
  complex<double> bernoulli_pgf(complex<double> x, int index);

  complex<double> polylog(complex<double> x, int kMin);

  complex<double> powerlaw_pgf(complex<double> x);
  
  complex<double> outdegree_pgf(complex<double> x, int index);
  
  complex<double> outdegree_plus_one(complex<double> x, int index);
  
  complex<double> semelparity(complex<double> x);
  
  complex<double> semelparity(complex<double> x, int index);

  complex<double> recursive_semelparity(complex<double> x, int g);
  
  complex<double> recursive_semelparity(complex<double> x, int g, int index);

  complex<double> popularity(complex<double> x, int g);

  complex<double> popularity(complex<double> x, int g, int index);

  void pgf_results_out(vector<complex<double>> h, int index); //results


};
#endif
