#include <Python.h>
#include "oscillators.h"
#include "py_wrappers.h"

static PyObject* PyOscillators_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
  int n;
  if (!PyArg_ParseTuple(args, "i", &n))
      return nullptr;

  PyOscillators* self = (PyOscillators*)type->tp_alloc(type, 0);
  if (!self)
      return nullptr;

  self->cpp_obj = new Oscillators(n);
  return (PyObject*)self;
}

// --- 3. Destructor (__dealloc__) ---
static void PyOscillators_dealloc(PyOscillators* self) {
  delete self->cpp_obj;
  Py_TYPE(self)->tp_free((PyObject*)self);
}
// --- 4. Method wrappers ---
//static PyObject* PyOscillators_set_coupling(PyOscillatorSystem* self, PyObject* args) {
//    double k;
//    if (!PyArg_ParseTuple(args, "d", &k))
//        return nullptr;
//    self->cpp_obj->set_coupling(k);
//    Py_RETURN_NONE;
//}
//
//static PyObject* PyOscillatorSystem_compute_energy(PyOscillatorSystem* self, PyObject* Py_UNUSED(ignored)) {
//    double energy = self->cpp_obj->compute_energy();
//    return Py_BuildValue("d", energy);
//}
//
//// --- 5. Method table ---
//static PyMethodDef PyOscillatorSystem_methods[] = {
//    {"set_coupling", (PyCFunction)PyOscillatorSystem_set_coupling, METH_VARARGS, "Set the coupling constant"},
//    {"compute_energy", (PyCFunction)PyOscillatorSystem_compute_energy, METH_NOARGS, "Compute system energy"},
//    {NULL, NULL, 0, NULL}
//};

// --- 6. Python type object ---
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

static PyModuleDef oscillatorsModule = { //removed struct from this line after static, in case this breaks something
    PyModuleDef_HEAD_INIT,
    "oscillators",
    "Kuramoto model and oscillator bindings",
    -1,
    PyOscillatorsFunctions
};

PyMODINIT_FUNC PyInit_oscillators(void) {
  if (PyType_Ready(&PyOscillatorsType) < 0){
    return NULL;
  }
  
  PyObject* m = PyModule_Create(&oscillatorsModule);
  if (!m){
    return NULL;
  }
  
  Py_INCREF(&PyOscillatorsType);
  PyModule_AddObject(m, "Oscillator", (PyObject*)&PyOscillatorsType);
  return m;
}


