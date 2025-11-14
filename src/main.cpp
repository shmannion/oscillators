#include "oscillators.h"
#include "py_wrappers.h"
using namespace std;

int main(){
  Oscillators s(4);
  s.initialise_system("default");
  //map<int, vector<vector<double>>> x = s.kuramoto_simulations(10, "phase");
}
