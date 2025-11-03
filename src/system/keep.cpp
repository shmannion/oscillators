#include "oscillators.h"
#include <random>
//first two functions need not be class members but degree list should be?
double riemann_zeta(double gamma){
  double rZeta = 0;
  for (int i = 1; i < 100000; ++i){
    rZeta += pow(i, -gamma); 
  }
  return rZeta;
}

//function to generate a powerlaw cdf
vector<double> powerlawCdf(int kMax, double gamma){
  vector<double> cdf;
  map<int, double> pdf;
  double rZeta = riemann_zeta(gamma);
  for (int i = 1; i != kMax + 2; ++i){
    pdf[i] = pow(i, -gamma)/rZeta;
    cdf.push_back(0);
  }
  for (int itr = 0; itr != cdf.size(); ++itr){
    for (int i = 0; i != kMax + 2; ++i){
      if (i <= itr){
        cdf[itr] += pdf[i];
      }
    }
  }
  return cdf;
}


