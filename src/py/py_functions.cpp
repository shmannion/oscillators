#include "py_wrappers.h"

PyMethodDef PyOscillatorsFunctions[] = {
    {"kuramoto_model", py_kuramoto_model, METH_VARARGS, "Run Kuramoto model simulation"},
    {NULL, NULL, 0, NULL}  // Sentinel
};
