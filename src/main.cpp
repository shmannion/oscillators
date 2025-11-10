#include "oscillators.h"
#include "py_wrappers.h"
using namespace std;

int main(){
  string settings = "default";
  vector<int> actors = {0,2};
  vector<vector<double>> K = {};
  K.push_back({0,6.5,1.5,0});
  K.push_back({6.5,0,0,0});
  K.push_back({0,0,0,7.8});
  K.push_back({0,1.3,7.8,0});
  cout << "checkpoint 1" << endl;
  vector<vector<double>> x = kuramoto_model(4, settings, actors, K);
  for(int i = 0; i != x.size(); ++i){
    for(int j = 0; j != x[i].size(); ++j){
      cout << x[i][j] << endl;
    }
  }
}
