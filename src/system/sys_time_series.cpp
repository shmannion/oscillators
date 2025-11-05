#include "oscillators.h"

double interpolate(double x1, double y1, double x2, double y2){

}

double interpolate_phase(double x1, double y1, double x2, double y2){

}

void System::construct_time_stamps(string method){
  if(method == "amplitude"){
    construct_time_stamps_from_amplitudes();
  }else if(method == "phase"){
    construct_time_stamps_from_phases();
  }
}

void System::construct_time_stamps_from_phases(){
  for(int i = 0; i != N; ++i){
    timeStamps.push_back({});
    for(int j = 0; j != theta[i].size() - 1; ++j){
      double diff = abs(theta[i][j] - theta[i][j+1]);
      if(diff > 6){ //the difference between two consecutive values is greater than 6 >
                    //the oscillator's phase has gone from 2pi to 0
      }
    }
  }
}

void System::construct_time_stamps_from_amplitudes(){
  for(int i = 0; i != N; ++i){
    timeStamps.push_back({});
    for(int j = 0; j != theta[i].size() - 1; ++j){
      double product = theta[i][j] * theta[i][j+1];
      if(product < 0){ //negative product in the amplitude implies the oscillators amp 
                       //has crossed the x axis.
      }
    }
  }
  //vector<double> timeStamps;
  //double product;
  //double x1;
  //double x2;
  //double y1;
  //double y2;
  //double m;
  //double intercept;
  //for(int i = start; i != theta.size()-1; ++i){
  //  product = theta[i]*theta[i+1];
  //  if(product < 0){ //there is a zero between i and i + 1
  //    x1 = timePoints[i];
  //    x2 = timePoints[i+1];
  //    y1 = theta[i];
  //    y2 = theta[i+1];
  //    m = (y2 - y1) / (x2 - x1);
  //    intercept = (m*x1 - y1)/m;
  //    timeStamps.push_back(intercept);
  //  }
  //}
  //vector<double> tapTimes;
  //for(int i = 0; i != timeStamps.size(); ++i){
  //  if(i % 2 == 0){
  //    tapTimes.push_back(timeStamps[i]);
  //  }
  //}
  //return tapTimes;
}
