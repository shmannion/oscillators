#include "oscillators.h"
#include "py_wrappers.h"

vector<double> Oscillators::dtheta_kuramoto(){
  vector<double> dthetaDt;
  double dtheta;
  double noise;
  for(int i = 0; i != N; ++i){
    if(metronomes[i] == 1){
      noise = 0;
    }else{
      noise = draw_noise_value();
      noise /= pow(dt, 0.5);
    }
    dtheta = naturalFrequencies[i] + noise;
    for(int j = 0; j != N; ++j){
      dtheta += K[i][j] * sin(theta[j].back() - theta[i].back());
    }
    dthetaDt.push_back(dtheta);
  }
  return dthetaDt;
}

void Oscillators::kuramoto_model(){
  eulers_method();
  calculate_order_parameter();
  if(OSC_VERBOSE == true){
    print_order_parameter();
  }
  construct_timestamps();
  construct_event_times();
  construct_inter_event_times();
}

void Oscillators::kuramoto_simulations(int n, string output){
  if(n == 1){ //run single simulation
    kuramoto_model();
    if(output == "phase"){
      simulationResults[1] = theta; 
    }else if(output == "timestamps"){
      simulationResults[1] = eventTimes;
    }else if(output == "interEventTimes"){
      simulationResults[1] = interEventTimes; 
    }
  }else{
    int currentSim = 1;
    if(output == "phase"){
      while(currentSim < n + 1){
        kuramoto_model(); 
        simulationResults[currentSim] = theta;
        reinitialise_system("default");
        currentSim += 1;
      }//endwhile
    }else if(output == "timestamps"){
      while(currentSim < n + 1){
        kuramoto_model(); 
        simulationResults[currentSim] = eventTimes;
        reinitialise_system("default");
        currentSim += 1;
      }//endwhile
    }else if(output == "interEventTimes"){
      while(currentSim < n + 1){
        kuramoto_model(); 
        simulationResults[currentSim] = interEventTimes;
        reinitialise_system("default");
        currentSim += 1;
      }//endwhile
    }//end elseif
  }//end else
}

void Oscillators::calculate_order_parameter(){
  complex<double> meanTheta;
  for(int i = 0; i != theta[0].size(); ++i){
    meanTheta = 0;
    for(int j = 0; j != theta.size(); ++j){
      meanTheta += exp(1i*theta[j][i]);
    }
    meanTheta /= double(N);
    meanPhase.push_back(meanTheta);
  }
  double r;
  for(int i = 0; i != meanPhase.size(); ++i){
    r = 0;
    r += pow(meanPhase[i].real(),2);
    r += pow(meanPhase[i].imag(),2);
    orderParam.push_back(pow(r, 0.5));
  }
}

void Oscillators::print_order_parameter(){
  double t;
  for(int i=0; i != orderParam.size(); ++i){
    t = double(i)*dt;
    cout << t << ", " << orderParam[i] << ", order" << "\n"; 
  }
}

