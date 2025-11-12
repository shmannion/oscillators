#include "py_wrappers.h"
#include "oscillators.h"

static PyObject* PyOscillators_initialise_system(PyOscillators* self, PyObject* args, PyObject* kwargs) {
  const char* method = "default";  // default if not provided
  static const char* kwlist[] = {"method", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|s", (char**)kwlist, &method)) {
    return nullptr;
  }

  try {
    self->cpp_obj->initialise_system(method);
  } catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return nullptr;
  }

  Py_RETURN_NONE;
}

static PyObject* PyOscillators_re_initialise_system(PyOscillators* self, PyObject* args, PyObject* kwargs) {
  const char* method = "default";  // default value
  static const char* kwlist[] = {"method", NULL};

  // Parse optional keyword argument
  if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|s", (char**)kwlist, &method)){
    return nullptr;
  }
  try {
    self->cpp_obj->re_initialise_system(string(method));
  } catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return nullptr;
  }

  Py_RETURN_NONE;
}

static PyObject* PyOscillators_initialise_default_system(PyOscillators* self, PyObject* /*unused*/) {
  try {
    self->cpp_obj->initialise_default_system();
  } catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return nullptr;
  }

  Py_RETURN_NONE;
}

PyMethodDef PyOscillatorsMethods[] = {
  {"initialise_system", (PyCFunction)PyOscillators_initialise_system, METH_VARARGS | METH_KEYWORDS,
   "Initialise the oscillator system (method='default' or 'custom')"},
  {"re_initialise_system", (PyCFunction)PyOscillators_re_initialise_system, METH_VARARGS | METH_KEYWORDS,
   "Reinitialise the oscillator system with the given method ('full' or other)."},
  {"initialise_default_system", (PyCFunction)PyOscillators_initialise_default_system, METH_NOARGS,
   "Initialise system with default settings"},
  {NULL, NULL, 0, NULL}  // Sentinel
};
