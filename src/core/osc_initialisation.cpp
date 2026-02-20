#include "oscillators.h"

void Oscillators::set_noise_distribution(string dist){
  if(dist == "default"){
    noiseDist = "normal";
    noiseParams = {0,0.4335};
  }else if(dist == "normal"){
    noiseDist = "normal";
    noiseParams = {0,0.4335};
  }else if(dist == "none"){
    noiseDist = "none";
  }
}

void Oscillators::set_phase_noise(double s){
  phaseNoise = s;
}

double Oscillators::get_phase_noise(){
  return phaseNoise;
}

void Oscillators::set_frequency_noise(double s){
  frequencyNoise = s;
}

double Oscillators::get_frequency_noise(){
  return frequencyNoise;
}

void Oscillators::set_noise_distribution(string dist, vector<double> params){
  if(validNoiseDistributions.find(dist) == validNoiseDistributions.end()){
    cerr << "Selected noise distribution is not defined" << endl;
  }else{
    noiseDist = dist;
    noiseParams = params;
  }
}

string Oscillators::get_noise_distribution(){
  string dist = noiseDist;
  return dist;
}

vector<double> Oscillators::get_noise_params(){
  vector<double> params = noiseParams;
  return params;
}

void Oscillators::set_frequency_distribution(string dist){
  if(dist == "default"){
    frequencyDist = "normal";
    frequencyParams = {12.8, 1.26};
  }else if(dist == "normal"){
    frequencyDist = "normal";
    frequencyParams = {12.8, 1.26};
  }
}

void Oscillators::set_frequency_distribution(string dist, vector<double> params){
  if(validOmegaDistributions.find(dist) == validOmegaDistributions.end()){
    cerr << "Selected frequency distribution is not defined" << endl;
  }else{
    frequencyDist = dist;
    frequencyParams = params;
  }
}

string Oscillators::get_frequency_distribution(){
  string dist = frequencyDist;
  return dist;
}

vector<double> Oscillators::get_frequency_params(){
  vector<double> params = frequencyParams;
  return params;
}

void Oscillators::set_phase_distribution(string dist){
  if(dist == "default"){
    phaseDist = "uniform";
    phaseParams = {0, 2*PI};
  }else if(dist == "uniform"){
    phaseDist = "uniform";
    phaseParams = {0, 2*PI};
  }
}

void Oscillators::set_phase_distribution(string dist, vector<double> params){
  if(validThetaDistributions.find(dist) == validThetaDistributions.end()){
    cerr << "Selected phase distribution is not defined" << endl;
  }else if(dist == "fixed"){
    phaseDist = dist;
    set_phase_values(params);
  }else{
    phaseDist = dist;
    phaseParams = params;
  }
}

void Oscillators::set_phase_values(vector<double> x){
  phaseDist = "fixed";
  phase = {};
  for(int i = 0; i != x.size(); ++i){
    phase.push_back({x[i]});
  }
}

string Oscillators::get_phase_distribution(){
  string dist = phaseDist;
  return dist;
}

vector<double> Oscillators::get_phase_params(){
  vector<double> params = phaseParams;
  return params;
}

void Oscillators::set_default_distributions(){
  set_noise_distribution("default");
  set_frequency_distribution("default");
  set_phase_distribution("default");
}

void Oscillators::set_timestamp_method(string method){
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

string Oscillators::get_timestamp_method(){
  return timestampMethod;
}

double Oscillators::draw_noise_value(){
  double x = 0;
  if(noiseDist == "normal"){
    x = draw_normal_rnd_value(noiseParams);
  }else if(noiseDist == "none"){
    return x;
  }  //else if another
  return x;
}

double Oscillators::draw_frequency_value(){
  double x = 0;
  if(noiseDist == "normal"){
    x = draw_normal_rnd_value(frequencyParams);
  }//else if another
  return x;

}

double Oscillators::draw_phase_value(){
  double x = 0;
  if(noiseDist == "normal"){
    x = draw_normal_rnd_value(phaseParams);
  }else if(phaseDist == "uniform"){
    x = draw_uniform_rnd_value(phaseParams);
  }//else if another
  return x;
}

double Oscillators::draw_normal_rnd_value(vector<double> params){
  mt19937 gen(random_device{}());
  normal_distribution<double> n{params[0], params[1]};
  double sample = n(gen);
  return sample;
}

double Oscillators::draw_uniform_rnd_value(vector<double> params){
  mt19937 gen(random_device{}());
  uniform_real_distribution<double> u(params[0], params[1]);
  double sample = u(gen);
  return sample;
}

void Oscillators::initialise_natural_frequencies(){
  naturalFrequencies = {};
  double sample;
  while(naturalFrequencies.size() < N){
    sample = draw_frequency_value();
    naturalFrequencies.push_back(sample);
  }
  initialise_frequency();
}

void Oscillators::initialise_frequency(){
  frequency = {};
  for(int i = 0; i != naturalFrequencies.size(); ++i){
    frequency.push_back({naturalFrequencies[i]});
  }
}

void Oscillators::set_frequency(vector<double> g){
  frequency = {};
  naturalFrequencies = {};
  for(int i = 0; i != g.size(); ++i){
    frequency.push_back({g[i]});
    naturalFrequencies.push_back(g[i]);
  }
}

vector<double> Oscillators::get_frequency(){
  return naturalFrequencies;
}

void Oscillators::initialise_phase(){
  //double sample;
  meanPhase = {};
  orderParam = {};
  if(phaseDist == "fixed"){
    vector<vector<double>> newPhase = {};
    for(int i = 0; i != N; ++i){
      newPhase.push_back({phase[i][0]});
    }
    phase = newPhase;
  }else{
    phase = {};
    while(phase.size() < N){
      double sample = 1;//draw_phase_value();
      vector<double> phase0 = {sample};
      phase.push_back(phase0);
    }
  }
}

void Oscillators::set_model(string s){
  if(validModels.find(s) == validModels.end()){
    cerr << "Selected model is not defined" << endl;
  }else{
    model = s;
  }
}

string Oscillators::get_model(){
  if(OSC_VERBOSE == true){
    cout << "model type is " << model << endl;
  }
  return model;
}

void Oscillators::set_kuramoto_coupling(vector<vector<double>> coupling){
  kuramotoCoupling = coupling;
}

vector<vector<double>> Oscillators::get_kuramoto_coupling(){
  vector<vector<double>> coupling = kuramotoCoupling;
  return coupling;
}

void Oscillators::set_amplitude_stamp_start(int s){
  amplitudeStampStart = s;
}

int Oscillators::get_amplitude_stamp_start(){
  return amplitudeStampStart;
}

void Oscillators::set_action_oscillators(vector<int> labels){
  actionOscillators = labels;
}

vector<int> Oscillators::get_action_oscillators(){
  vector<int> labels = actionOscillators;
  return labels;
}

void Oscillators::set_metronomes(vector<int> labels){
  metronomes = {};
  for(int i = 0; i != N; ++i){
    metronomes.push_back(0);
  }
  for(int i = 0; i != labels.size(); ++i){
    metronomes[labels[i]] = 1;
  }
  if(OSC_VERBOSE == true){
    for(int i = 0; i != N; ++i){
      cout << "for " << i << "the metronome value is " << metronomes[i] << endl;
    }
  }
}

vector<int> Oscillators::get_metronomes(){
  vector<int> returnList = {};
  for(int i = 0; i != N; ++i){
    if(metronomes[i] == 1){
      returnList.push_back(i);
    }
  }
  return returnList;
}

void Oscillators::initialise_system(){
  initialise_phase();
  initialise_natural_frequencies();
  set_timestamp_method("amplitude");
  set_max_time(20);
  set_time_step(0.001);
}

void Oscillators::reinitialise_system(string method){
  timestamps = {};
  eventTimes = {};
  interEventTimes = {};
  initialise_phase();
  initialise_frequency();
  if(method == "full"){
    naturalFrequencies = {};
    frequency = {};
    initialise_natural_frequencies();
  }
}
