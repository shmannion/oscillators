#pragma once
#include <Python.h>
#include <vector>
#include <map>

using namespace std;


//----------------------------------------------------------------------------------------------------------------------
// module definition
//----------------------------------------------------------------------------------------------------------------------
PyMODINIT_FUNC PyInit_oscillators(void);

//----------------------------------------------------------------------------------------------------------------------
// wrapper for oscillators class
//----------------------------------------------------------------------------------------------------------------------
class Oscillators;
struct PyOscillators{
  PyObject_HEAD
  Oscillators* cpp_obj;
  //public attributes here

};
//----------------------------------------------------------------------------------------------------------------------
// class constructor/destructor
//----------------------------------------------------------------------------------------------------------------------
PyObject* PyOscillators_new(PyTypeObject* type, PyObject* args, PyObject* kwds);
void PyOscillators_dealloc(PyOscillators* self);
//----------------------------------------------------------------------------------------------------------------------
// wrapper functions
//----------------------------------------------------------------------------------------------------------------------
PyObject* py_kuramoto_model(PyObject* self, PyObject* args);


//----------------------------------------------------------------------------------------------------------------------
// methods table
//----------------------------------------------------------------------------------------------------------------------
extern PyMethodDef PyOscillatorsFunctions[];
extern PyMethodDef PyOscillatorsMethods[];
extern PyMemberDef PyOscillatorsMembers[];
extern PyGetSetDef PyOscillatorsGetSet[];
//----------------------------------------------------------------------------------------------------------------------
// module initialisation functions
//----------------------------------------------------------------------------------------------------------------------

//----------------------------------------------------------------------------------------------------------------------
// Helper functions py_helper.cpp for converting python objects
//----------------------------------------------------------------------------------------------------------------------
PyObject* matrix_to_pylist(const vector<vector<double>> &mat);
bool py_to_matrix(PyObject* obj, vector<vector<double>> &mat);
PyObject* map_to_pydict(const map<int, vector<vector<double>>>& m);
