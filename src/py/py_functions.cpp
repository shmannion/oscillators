#include "py_wrappers.h"
#include "oscillators.h"
static PyObject* py_set_verbose(PyObject* self, PyObject* args) {
  int flag;

  if (!PyArg_ParseTuple(args, "p", &flag)) {
    return nullptr;
  }

  set_verbose(flag != 0);
  Py_RETURN_NONE;
}

PyMethodDef PyOscillatorsFunctions[] = {
  {"set_verbose", py_set_verbose, METH_VARARGS, "Enable or disable console output. Usage: set_verbose(True/False)"},
  {NULL, NULL, 0, NULL}  // Sentinel
};
