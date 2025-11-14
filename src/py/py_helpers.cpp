#include "py_wrappers.h"

using namespace std;

PyObject* matrix_to_pylist(const vector<vector<double>>& mat) {
    PyObject* outer = PyList_New(mat.size());
    for (size_t i = 0; i < mat.size(); ++i) {
        PyObject* inner = PyList_New(mat[i].size());
        for (size_t j = 0; j < mat[i].size(); ++j)
            PyList_SetItem(inner, j, PyFloat_FromDouble(mat[i][j]));
        PyList_SetItem(outer, i, inner);
    }
    return outer;
}

bool py_to_matrix(PyObject* obj, vector<vector<double>>& mat) {
    if (!PyList_Check(obj)) {
        PyErr_SetString(PyExc_TypeError, "Expected list of lists");
        return false;
    }

    Py_ssize_t outer_len = PyList_Size(obj);
    mat.resize(outer_len);

    for (Py_ssize_t i = 0; i < outer_len; ++i) {
        PyObject* row = PyList_GetItem(obj, i);
        if (!PyList_Check(row)) {
            PyErr_SetString(PyExc_TypeError, "Each row must be a list");
            return false;
        }

        Py_ssize_t inner_len = PyList_Size(row);
        mat[i].resize(inner_len);

        for (Py_ssize_t j = 0; j < inner_len; ++j)
            mat[i][j] = PyFloat_AsDouble(PyList_GetItem(row, j));
    }

    return true;
}

PyObject* map_to_pydict(const map<int, vector<vector<double>>>& m) {
  PyObject* dict = PyDict_New();
  if (!dict) {
    return nullptr;
  }

  for (const auto& pair : m) {
    int key = pair.first;
    const vector<vector<double>>& mat = pair.second;

    PyObject* py_key = PyLong_FromLong(key);
    PyObject* py_val = matrix_to_pylist(mat);

    if (!py_key || !py_val) {
      Py_XDECREF(py_key);
      Py_XDECREF(py_val);
      Py_DECREF(dict);
      return nullptr;
    }

    if (PyDict_SetItem(dict, py_key, py_val) < 0) {
      Py_DECREF(py_key);
      Py_DECREF(py_val);
      Py_DECREF(dict);
      return nullptr;
    }

    Py_DECREF(py_key);
    Py_DECREF(py_val);
  }

  return dict;
}
