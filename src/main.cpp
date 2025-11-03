#include <iostream>
#include <random>
#include <map>
#include <vector>
#include <set>
#include <math.h>
#include <cmath>
#include <numbers>
using namespace std;

const double PI = 3.1415926536;
//beginning the coding of the system of oscillators class, but not actually using here.
class System{
private:
  int N; // number of oscillators
  vector<vector<double>> theta;
  
public:
  System(int N) {}
};

vector<double> initialise_g(int len, double mu, double sig){
  //assumes normal distribution
  vector<double> g;
  mt19937 gen(random_device{}());
  normal_distribution<double> n{mu, sig};
  double sample;
  while(g.size() < len){
    sample = n(gen);
    g.push_back(sample);
  }
  return g;
}

vector<double> initialise_theta(int len){
  vector<double> theta;
  double p;
  mt19937 gen(random_device{}());
  uniform_real_distribution<double> unif_circle(0, 2*PI);
  while(theta.size() < len){
    p = unif_circle(gen);
    theta.push_back(p);
  }
  return theta;
}

vector<double> dtheta_dt(vector<vector<double>> K, vector<double> thetaT, vector<double> g){
  vector<double> dthetaDt;
  mt19937 gen(random_device{}());
  normal_distribution<double> noiseDist{0, 0.4335};
  double dtheta;
  double noise;
  for(int i = 0; i != thetaT.size(); ++i){
    noise = noiseDist(gen);
    dtheta = g[i] + noise;
    for(int j = 0; j != K[i].size(); ++j){
      dtheta += K[i][j] * sin(thetaT[j] - thetaT[i]);
    }
    dthetaDt.push_back(dtheta);
  }
  return dthetaDt;
}

vector<vector<double>> eulers_method(int nOscillators, vector<vector<double>> K, double tMax, vector<double> g, vector<vector<double>> theta){
  double time = 0;
  double dt = 0.001;
  vector<double> thetaT; 
  while(time < tMax){
    thetaT = {};
    for(int i = 0; i != theta.size(); ++i){
      thetaT.push_back(theta[i].back());
    }
    vector<double> dthetaDt = dtheta_dt(K, thetaT, g);
    for(int i = 0; i != theta.size(); ++i){
      theta[i].push_back(thetaT[i] + (dthetaDt[i] * dt));
    }
    time += dt;
  }
  return theta;
}

vector<double> construct_time_stamps(vector<double> theta, double maxTime, double dt, int neglectTransient){
  vector<double> timePoints;
  int start = 0;
  if(neglectTransient != 0){
    start = 2000;
  }
  for(int i = 0; i != theta.size(); ++i){
    timePoints.push_back(0.001*double(i));
  }
  vector<double> timeStamps;
  double product;
  double x1;
  double x2;
  double y1;
  double y2;
  double m;
  double intercept;
  for(int i = start; i != theta.size()-1; ++i){
    product = theta[i]*theta[i+1];
    if(product < 0){ //there is a zero between i and i + 1
      x1 = timePoints[i];
      x2 = timePoints[i+1];
      y1 = theta[i];
      y2 = theta[i+1];
      m = (y2 - y1) / (x2 - x1);
      intercept = (m*x1 - y1)/m;
      timeStamps.push_back(intercept);
    }
  }
  vector<double> tapTimes;
  for(int i = 0; i != timeStamps.size(); ++i){
    if(i % 2 == 0){
      tapTimes.push_back(timeStamps[i]);
    }
  }
  return tapTimes;
}

vector<double> inter_event_times(vector<double> timeStamps){
  vector<double> interEventTimes;
  for(int i = 1; i != timeStamps.size(); ++i){
    interEventTimes.push_back(timeStamps[i] - timeStamps[i-1]);
  }
  return interEventTimes;
}

double pearson_correlation_coefficient(vector<double> xIn, vector<double> yIn, int lag){
  double rho;
  vector<double> x;
  double xSum = 0;
  vector<double> y;
  double ySum = 0;
  if(lag != 0){
    if(lag > 0){ // lag greater than zero, we shift y
      for(int i = lag; i != yIn.size(); ++i){
        y.push_back(yIn[i]);
        ySum += yIn[i];
      }
      for(int i = 0; i != xIn.size() - lag; ++i){
        x.push_back(xIn[i]);
        xSum += xIn[i];
      }
    }else{
      for(int i = abs(lag); i != xIn.size(); ++i){
        x.push_back(xIn[i]);
        xSum += xIn[i];
      }
      for(int i = 0; i != yIn.size() - abs(lag); ++i){
        y.push_back(yIn[i]);
        ySum += yIn[i];
      }
    }
  }else{
    x = xIn;
    y = yIn;
    for(int i = 0; i != xIn.size(); ++i){
      xSum += xIn[i];
      ySum += yIn[i];
    }
  }
  double yBar = ySum/y.size();
  double xBar = xSum/x.size();
  double sigSqX = 0;
  double sigSqY = 0;
  double covXY = 0;
  double sigX;
  double sigY;
  for(int i = 0; i != x.size(); ++i){
    sigSqX += pow((x[i] - xBar),2);
    sigSqY += pow((y[i] - yBar),2);
    covXY += ((x[i] - xBar)*(y[i] - yBar));
  }
  sigX = pow(sigSqX, 0.5);
  sigY = pow(sigSqY, 0.5);
  rho = covXY/(sigX * sigY);
  return rho;
}

int main(int argc, char* argv[]){
  //set the parameters for the distribution of oscillator frequencies
  //System G(4);
  cout << "code starts" << endl;
  vector<vector<double>> combos;
  vector<double> vals = {};
  double k = 1.25;
  while(k < 20){
    vals.push_back(k);
    k += 0.5;
  }
  double x1; 
  double x2;
  double x3;
  double x4;
  vector<double> combo;
  for(int i = 0; i != vals.size(); ++i){
    x1 = vals[i];
    for(int j = 0; j != vals.size(); ++j){
      x2 = vals[j];
      for(int k = 0; k != vals.size(); ++k){
        x3 = vals[k];
        for(int l = 0; l != vals.size(); ++l){
          x4 = vals[l];
          combo = {x1, x2, x3, x4};
          combos.push_back(combo);
        }
      }
    }
  }
  int start_idx = 0;
  int end_idx = combos.size();
  if(argc == 3){
    start_idx = stoi(argv[1]);
    end_idx = stoi(argv[2]);

  }
  
  #pragma omp parallel for
  for(int n = start_idx; n != end_idx; ++n){
    double i1 = combos[n][0];
    double i2 = combos[n][1];
    double e1 = combos[n][2];
    double e2 = combos[n][3];
    cout << 'n' << n << " is " << i1 << ", " << e1 << ", " << i2 << ", " << e2 << endl;
    int neglectTransient = 1;
    int nOscillators = 4;
    vector<vector<double>> K; //matrix of our k values
    double dt = 0.001;
    double tMax = 12;
    K.push_back({0, i1, e1, 0}); // {0, i1, e1, 0;}
    K.push_back({i1, 0, 0, 0});   // {i1, 0, 0, 0;}
    K.push_back({0, 0, 0, i2});   // {0, 0, 0, i2;}
    K.push_back({0, e2, i2, 0}); // {0, e2, i2, 0;}
    
    //this time, I actually want the theta values over time so theta should be a vector of vectors, each growing
    //for initial recreation, we want to set dt = 0.025 as well.
    
    mt19937 gen(random_device{}());
    uniform_real_distribution<double> unifCircle(0,2*PI); // uniform distribution about the circle
    vector<int> lags = {-1, 0, 1};
    vector<vector<double>> rhos;
    double rho;
    while(rhos.size() < 200){
      rhos.push_back({});
      vector<double> g = initialise_g(nOscillators, 12.57, 1.26);
      vector<vector<double>> theta;
      for(int i = 0; i != nOscillators; ++i){
        double t = unifCircle(gen);
        theta.push_back({t});
      }
      vector<vector<double>> theta_long = eulers_method(nOscillators, K, tMax, g, theta);
      for(int i = 0; i != theta_long.size(); ++i){
        for(int j = 0; j != theta_long[i].size(); ++j){
          //cout << double(j)*0.025 << ", " << sin(theta_long[i][j]) << ", O" << i << endl; 
        }
      }
      vector<int> actionOscillators = {0,2};
        
      vector<double> amp1;
      vector<double> amp2;
      for(int j = 0; j != theta_long[0].size(); ++j){
        amp1.push_back(sin(theta_long[0][j]));
      }
      for(int j = 0; j != theta_long[2].size(); ++j){
        amp2.push_back(sin(theta_long[2][j]));
      }
      vector<double> tapTimes1 = construct_time_stamps(amp1, tMax, dt, neglectTransient); 
      vector<double> interEventTimes1 = inter_event_times(tapTimes1);    
      vector<double> tapTimes2 = construct_time_stamps(amp2, tMax, dt, neglectTransient);
      vector<double> interEventTimes2 = inter_event_times(tapTimes2);
      for(int m = 0; m != lags.size(); ++m){
        rho = pearson_correlation_coefficient(interEventTimes1, interEventTimes2, lags[m]);
        rhos.back().push_back(rho);
      }

    }
    double meanRho;
    for(int m = 0; m != lags.size(); ++m){
      meanRho = 0;
      for(int i = 0; i != rhos.size(); ++i){
        meanRho += rhos[i][m];
      }
      meanRho /= rhos.size();
      cout << meanRho << ", ";
    }
    cout << 'r' << endl;
  }
}

