#include <Python.h>
#include "py_wrappers.h"
#include "oscillators.h"
//--------------------------------------------------------------------------------------------------------------------
// Constructor
//--------------------------------------------------------------------------------------------------------------------
PyObject* PyOscillators_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
  int n;
  if (!PyArg_ParseTuple(args, "i", &n))
      return nullptr;

  PyOscillators* self = (PyOscillators*)type->tp_alloc(type, 0);
  if (!self)
      return nullptr;

  self->cpp_obj = new Oscillators(n);
  return (PyObject*)self;
}

//--------------------------------------------------------------------------------------------------------------------
// Destructor
//--------------------------------------------------------------------------------------------------------------------

void PyOscillators_dealloc(PyOscillators* self) {
  delete self->cpp_obj;
  Py_TYPE(self)->tp_free((PyObject*)self);
}

//--------------------------------------------------------------------------------------------------------------------
// Python type object
//--------------------------------------------------------------------------------------------------------------------

PyTypeObject PyOscillatorsType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "oscillators.Oscillators",
    .tp_basicsize = sizeof(PyOscillators),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyOscillators_new,
    .tp_dealloc = (destructor)PyOscillators_dealloc,
    .tp_methods = PyOscillatorsMethods,
    .tp_members = PyOscillatorsMembers,
    .tp_getset  = PyOscillatorsGetSet,
};

//--------------------------------------------------------------------------------------------------------------------
// Module definition (?)
//--------------------------------------------------------------------------------------------------------------------

static PyModuleDef oscillatorsModule = { //removed struct from this line after static, in case this breaks something
    PyModuleDef_HEAD_INIT,
    "oscillators",
    "Kuramoto model and oscillator bindings",
    -1,
    PyOscillatorsFunctions
};

//--------------------------------------------------------------------------------------------------------------------
// Module initialisation
//--------------------------------------------------------------------------------------------------------------------

PyMODINIT_FUNC PyInit_oscillators(void) {
  if (PyType_Ready(&PyOscillatorsType) < 0){
    return NULL;
  }
  
  PyObject* m = PyModule_Create(&oscillatorsModule);
  if (!m){
    return NULL;
  }
  
  Py_INCREF(&PyOscillatorsType);
  PyModule_AddObject(m, "Oscillators", (PyObject*)&PyOscillatorsType);
  return m;
}


