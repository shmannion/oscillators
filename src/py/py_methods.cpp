#include "py_wrappers.h"
#include "oscillators.h"

static PyObject* PyOscillators_set_default_distributions(PyOscillators* self) {
  try {
    self->cpp_obj->set_default_distributions();
  } catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return nullptr;
  }

  Py_RETURN_NONE;
}

static PyObject* PyOscillators_initialise_system(PyOscillators* self) {
  try {
    self->cpp_obj->initialise_system();
  } catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return nullptr;
  }

  Py_RETURN_NONE;
}

static PyObject* PyOscillators_reinitialise_system(PyOscillators* self, PyObject* args, PyObject* kwargs) {
  const char* method = "default";  // default value
  static const char* kwlist[] = {"method", NULL};

  // Parse optional keyword argument
  if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|s", (char**)kwlist, &method)){
    return nullptr;
  }
  try {
    self->cpp_obj->reinitialise_system(string(method));
  } catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return nullptr;
  }

  Py_RETURN_NONE;
}

static PyObject* PyOscillators_kuramoto_simulations(PyOscillators* self, PyObject* args, PyObject* kwargs){
  int n;
  const char* output = (char*)"phase";  // default
  static const char* kwlist[] = {"n", "output", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i|s", (char**)kwlist, &n, &output)) {
    return nullptr;
  }
  try{
    self->cpp_obj->kuramoto_simulations(n, string(output));
  }catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return nullptr;
  }
  PyObject* mark_dirty = PyObject_GetAttrString((PyObject*)self, "mark_results_dirty");
  if (mark_dirty != NULL) {
    PyObject* r = PyObject_CallObject(mark_dirty, NULL);
    Py_XDECREF(r);
  }
  Py_XDECREF(mark_dirty);
  Py_RETURN_NONE;
}


static PyObject* PyOscillators_coupling_parameter_search_1d(PyOscillators* self, PyObject* args) {
  PyObject* py_indices = nullptr;
  PyObject* py_bounds = nullptr;
  double step;

  // Expect: varyingIndices (list-of-lists), bounds (sequence), step (float)
  if (!PyArg_ParseTuple(args, "OOd", &py_indices, &py_bounds, &step)) {
    return nullptr;
  }

  vector<vector<int>> varyingIndices;
  vector<double> bounds;

  if (!py_to_int_matrix(py_indices, varyingIndices)) {
    return nullptr;
  }
  if (!py_to_double_list(py_bounds, bounds)) {
    return nullptr;
  }

  try {
    vector<vector<double>> summaryValues =
      self->cpp_obj->coupling_parameter_search_1d(varyingIndices, bounds, step);

    // Use your existing vv_to_dict to convert summaryValues -> Python dict
    return vv_to_pydict(summaryValues);
  }
  catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return nullptr;
  }
}

static PyObject* PyOscillators_parameter_search_e7(PyOscillators* self){
  try {
    map<int, vector<vector<double>>> results = self->cpp_obj->parameter_search_e7();

    // Use your existing vv_to_dict to convert summaryValues -> Python dict
    return map_to_pydict(results);
  }
  catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return nullptr;
  }

}

static PyObject* PyOscillators_parameter_search_e8(PyOscillators* self){
  try {
    map<int, vector<vector<double>>> results = self->cpp_obj->parameter_search_e8();

    // Use your existing vv_to_dict to convert summaryValues -> Python dict
    return map_to_pydict(results);
  }
  catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return nullptr;
  }

}

PyMethodDef PyOscillatorsMethods[] = {
  {"set_default_distributions", (PyCFunction)PyOscillators_set_default_distributions, METH_NOARGS,
   "Set the distributions to defaults"},
  {"initialise_system", (PyCFunction)PyOscillators_initialise_system, METH_NOARGS,
   "Initialise the oscillator system"},
  {"reset", (PyCFunction)PyOscillators_reinitialise_system, METH_VARARGS | METH_KEYWORDS,
   "Reinitialise the oscillator system with the given method ('full' or other)."},
  {"kuramoto_simulations", (PyCFunction)PyOscillators_kuramoto_simulations, METH_VARARGS | METH_KEYWORDS,
   "Run n Kuramoto simulations and return a dict of results"},
  {"coupling_parameter_search_1d", (PyCFunction)PyOscillators_coupling_parameter_search_1d, METH_VARARGS,
   "1D coupling parameter search; returns dict[index] -> list[summary values]"},
  {"parameter_search_e7", (PyCFunction)PyOscillators_parameter_search_e7, METH_NOARGS,
   "1D coupling parameter search; returns dict[index] -> list[summary values]"},
  {"parameter_search_e8", (PyCFunction)PyOscillators_parameter_search_e8, METH_NOARGS,
   "1D coupling parameter search; returns dict[index] -> list[summary values]"},
  {NULL, NULL, 0, NULL}  // Sentinel
};
