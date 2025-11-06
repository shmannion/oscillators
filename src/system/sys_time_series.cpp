#include "oscillators.h"

double System::interpolate(double x1, double y1, double x2, double y2){
  double t1 = dt * x1;
  double t2 = dt * x2;
  double m = (y2 - y1)/(t2 - t1);
  double intercept = (m * x1 - y1)/m;
  return intercept;
}

double System::interpolate_phase(double x1, double y1, double x2, double y2){
  double t1 = dt * x1;
  double ydist = (2 * PI - y1);
  ydist += y2;
  double crossPosition = (2 * PI - y1)/ydist;
  double intercept = t1 + crossPosition * dt;
  return intercept;
}

void System::construct_timestamps(){
  if(timestampMethod == "amplitude"){
    construct_timestamps_from_amplitudes();
  }else if(timestampMethod == "phase"){
    construct_timestamps_from_phases();
  }
}

void System::construct_timestamps(string method){
  set_timestamp_method(method);
  if(method == "amplitude"){
    construct_timestamps_from_amplitudes();
  }else if(method == "phase"){
    construct_timestamps_from_phases();
  }
}

void System::construct_timestamps_from_phases(){
  for(int i = 0; i != N; ++i){
    timestamps.push_back({});
    for(int j = 0; j != theta[i].size() - 1; ++j){
      double diff = abs(theta[i][j] - theta[i][j+1]);
      if(diff > 6){ //the difference between two consecutive values is greater than 6 >
        double intercept = interpolate_phase(double(j), theta[i][j], double(j+1), theta[i][j+1]);  //the oscillator's phase has gone from 2pi to 0
        timestamps[i].push_back(intercept);
      }
    }
  }
}

void System::construct_timestamps_from_amplitudes(){
  for(int i = 0; i != N; ++i){
    timestamps.push_back({});
    double product;
    double intercept;
    double amp1; 
    double amp2;
    for(int j = 0; j != theta[i].size() - 1; ++j){
      amp1 = sin(theta[i][j]);
      amp2 = sin(theta[i][j+1]);
      product = amp1 * amp2;
      if(product < 0){ //negative product in the amplitude implies the oscillators amp 
        intercept = interpolate(double(j), amp1, double(j+1), amp2); //has crossed the x axis.
        timestamps[i].push_back(intercept);
      }
    }
  }
}

void System::get_event_times(){
  for(int i = 0; i != actionOscillators.size(); ++i){
    eventTimes.push_back({}); //event times will be n vectors, one for each action oscillators, n <= N
  }//we handle this differently for phase/amplitude time stamps
  for(int i = 0; i != actionOscillators.size(); ++i){
    if(timestampMethod == "amplitude"){
      for(int j = amplitudeStampStart; j != timestamps[actionOscillators[i]].size(); ++j){
        if(j % 2 == amplitudeStampStart){
          eventTimes[i].push_back(timestamps[actionOscillators[i]][j]);
        }//endif
      }//endfor
    }else if(timestampMethod == "phase"){
      for(int j = 0; j != timestamps[actionOscillators[i]].size(); ++j){
        eventTimes[i].push_back(timestamps[actionOscillators[i]][j]);
      }//endfor
    }//endif
  }//endfor
}

void System::get_inter_event_times(){
  for(int i = 0; i != eventTimes.size(); ++i){
    interEventTimes.push_back({});
    for(int j = 1; j != eventTimes[i].size(); ++j){
      interEventTimes[i].push_back(eventTimes[i][j] - eventTimes[i][j-1]);
    }//endfor
  }//endfor
}
