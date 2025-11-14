#include "oscillators.h"

//vector<double> Oscillators::construct_time_stamps(vector<double> theta, double maxTime, double dt, int neglectTransient){
//  vector<double> timePoints;
//  int start = 0;
//  if(neglectTransient != 0){
//    start = 2000;
//  }
//  for(int i = 0; i != theta.size(); ++i){
//    timePoints.push_back(0.001*double(i));
//  }
//  vector<double> timeStamps;
//  double product;
//  double x1;
//  double x2;
//  double y1;
//  double y2;
//  double m;
//  double intercept;
//  for(int i = start; i != theta.size()-1; ++i){
//    product = theta[i]*theta[i+1];
//    if(product < 0){ //there is a zero between i and i + 1
//      x1 = timePoints[i];
//      x2 = timePoints[i+1];
//      y1 = theta[i];
//      y2 = theta[i+1];
//      m = (y2 - y1) / (x2 - x1);
//      intercept = (m*x1 - y1)/m;
//      timeStamps.push_back(intercept);
//    }
//  }
//  vector<double> tapTimes;
//  for(int i = 0; i != timeStamps.size(); ++i){
//    if(i % 2 == 0){
//      tapTimes.push_back(timeStamps[i]);
//    }
//  }
//  return tapTimes;
//}
//
//vector<double> Oscillators::inter_event_times(vector<double> timeStamps){
//  vector<double> interEventTimes;
//  for(int i = 1; i != timeStamps.size(); ++i){
//    interEventTimes.push_back(timeStamps[i] - timeStamps[i-1]);
//  }
//  return interEventTimes;
//}
//
//vector<double> Oscillators::apply_lag(){
//
//}
//
//double Oscillators::pearson_correlation_coefficient(vector<double> xIn, vector<double> yIn, int lag){
//  double rho;
//  vector<double> x;
//  double xSum = 0;
//  vector<double> y;
//  double ySum = 0;
//  if(lag != 0){
//    if(lag > 0){ // lag greater than zero, we shift y
//      for(int i = lag; i != yIn.size(); ++i){
//        y.push_back(yIn[i]);
//        ySum += yIn[i];
//      }
//      for(int i = 0; i != xIn.size() - lag; ++i){
//        x.push_back(xIn[i]);
//        xSum += xIn[i];
//      }
//    }else{
//      for(int i = abs(lag); i != xIn.size(); ++i){
//        x.push_back(xIn[i]);
//        xSum += xIn[i];
//      }
//      for(int i = 0; i != yIn.size() - abs(lag); ++i){
//        y.push_back(yIn[i]);
//        ySum += yIn[i];
//      }
//    }
//  }else{
//    x = xIn;
//    y = yIn;
//    for(int i = 0; i != xIn.size(); ++i){
//      xSum += xIn[i];
//      ySum += yIn[i];
//    }
//  }
//  double yBar = ySum/y.size();
//  double xBar = xSum/x.size();
//  double sigSqX = 0;
//  double sigSqY = 0;
//  double covXY = 0;
//  double sigX;
//  double sigY;
//  for(int i = 0; i != x.size(); ++i){
//    sigSqX += pow((x[i] - xBar),2);
//    sigSqY += pow((y[i] - yBar),2);
//    covXY += ((x[i] - xBar)*(y[i] - yBar));
//  }
//  sigX = pow(sigSqX, 0.5);
//  sigY = pow(sigSqY, 0.5);
//  rho = covXY/(sigX * sigY);
//  return rho;
//}
