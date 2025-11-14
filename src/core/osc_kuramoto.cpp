#include "oscillators.h"
#include "py_wrappers.h"

void Oscillators::kuramoto_model(){
  eulers_method();
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
        re_initialise_system("default");
        currentSim += 1;
      }//endwhile
    }else if(output == "timestamps"){
      while(currentSim < n + 1){
        kuramoto_model(); 
        simulationResults[currentSim] = eventTimes;
        re_initialise_system("default");
        currentSim += 1;
      }//endwhile
    }else if(output == "interEventTimes"){
      while(currentSim < n + 1){
        kuramoto_model(); 
        simulationResults[currentSim] = interEventTimes;
        re_initialise_system("default");
        currentSim += 1;
      }//endwhile
    }//end elseif
  }//end else
}
