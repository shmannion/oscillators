#include "oscillators.h"

double Oscillators::interpolate(double x1, double y1, double x2, double y2){
  double t1 = dt * x1;
  double t2 = dt * x2;
  double m = (y2 - y1)/(t2 - t1);
  double intercept = (m * t1 - y1)/m;
  return intercept;
}

double Oscillators::interpolate_phase(double x1, double y1, double x2, double y2){
  double t1 = dt * x1;
  double ydist = (2 * PI - y1);
  ydist += y2;
  double crossPosition = (2 * PI - y1)/ydist;
  double intercept = t1 + crossPosition * dt;
  return intercept;
}

void Oscillators::construct_timestamps(){
  if(timestampMethod == "amplitude"){
    construct_timestamps_from_amplitudes();
  }else if(timestampMethod == "phase"){
    construct_timestamps_from_phases();
  }
}

void Oscillators::construct_timestamps(string method){
  set_timestamp_method(method);
  if(method == "amplitude"){
    construct_timestamps_from_amplitudes();
  }else if(method == "phase"){
    construct_timestamps_from_phases();
  }
}

void Oscillators::construct_timestamps_from_phases(){
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

void Oscillators::construct_timestamps_from_amplitudes(){
  for(int i = 0; i != N; ++i){
    timestamps.push_back({});
    double product;
    double intercept;
    double amp1; 
    double amp2;
    cout << "theta size is " << theta[0].size() << endl;
    for(int j = 0; j != theta[i].size() - 1; ++j){
      amp1 = sin(theta[i][j]);
      amp2 = sin(theta[i][j+1]);
      product = amp1 * amp2;
      cout << 0.001 * double(j) << ", " << amp1 << ", a" << i << endl;
      if(product < 0){ //negative product in the amplitude implies the oscillators amp 
        intercept = interpolate(double(j), amp1, double(j+1), amp2); //has crossed the x axis.
        cout << "intercept is " << intercept << ", int" << i << endl;
        timestamps[i].push_back(intercept);
      }
    }
  }
}

void Oscillators::construct_event_times(){
  for(int i = 0; i != actionOscillators.size(); ++i){
    eventTimes.push_back({}); //event times will be n vectors, one for each action oscillators, n <= N
  }//we handle this differently for phase/amplitude time stamps
  cout << "event times checkpoint 1" << endl;
  cout << "method is " << timestampMethod << " and start is " << amplitudeStampStart << endl;
  for(int i = 0; i != actionOscillators.size(); ++i){
    cout << "event times checkpoint " << 2+i << endl;
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

void Oscillators::construct_inter_event_times(){
  for(int i = 0; i != eventTimes.size(); ++i){
    interEventTimes.push_back({});
    for(int j = 1; j != eventTimes[i].size(); ++j){
      interEventTimes[i].push_back(eventTimes[i][j] - eventTimes[i][j-1]);
      cout << interEventTimes[i].back() << ", ieTimes" << i << endl;
    }//endfor
  }//endfor
}


