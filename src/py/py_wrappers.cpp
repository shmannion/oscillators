#include "py_wrappers.h"

static struct PyModuleDef oscillatorsModule = {
    PyModuleDef_HEAD_INIT,
    "oscillators",
    "Kuramoto model and oscillator bindings",
    -1,
    oscillatorFunctions
};

PyMODINIT_FUNC PyInit_oscillators(void) {
    return PyModule_Create(&oscillatorsModule);
}

