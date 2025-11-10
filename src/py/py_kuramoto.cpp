#include "py_wrappers.h"
#include "oscillators.h"
#include <string>
#include <vector>

PyObject* py_kuramoto_model(PyObject*, PyObject* args) {
    int N;
    const char* settings;
    PyObject* py_actionOsc;
    PyObject* py_K;

    if (!PyArg_ParseTuple(args, "isOO", &N, &settings, &py_actionOsc, &py_K))
        return NULL;

    // Convert list of ints
    std::vector<int> actionOsc;
    if (PyList_Check(py_actionOsc)) {
        Py_ssize_t len = PyList_Size(py_actionOsc);
        actionOsc.reserve(len);
        for (Py_ssize_t i = 0; i < len; ++i)
            actionOsc.push_back((int)PyLong_AsLong(PyList_GetItem(py_actionOsc, i)));
    }

    // Convert matrix
    std::vector<std::vector<double>> K;
    if (!py_to_matrix(py_K, K))
        return NULL;

    std::vector<std::vector<double>> result = kuramoto_model(N, std::string(settings), actionOsc, K);
    return matrix_to_pylist(result);
}

