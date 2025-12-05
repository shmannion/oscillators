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

PyObject* vv_to_pydict(const vector<vector<double>>& v) {
  PyObject* dict = PyDict_New();
  if (!dict) {
    return nullptr;
  }

  for (size_t i = 0; i < v.size(); i++) {
    PyObject* py_key = PyLong_FromSize_t(i);
    PyObject* py_val = matrix_to_pylist({v[i]}); 

    if (!py_key || !py_val) {
      Py_XDECREF(py_key);
      Py_XDECREF(py_val);
      Py_DECREF(dict);
      return nullptr;
    }

    // Store plain list instead of list-of-list
    PyObject* inner_list = PyList_GetItem(py_val, 0); 
    Py_INCREF(inner_list);

    if (PyDict_SetItem(dict, py_key, inner_list) < 0) {
      Py_DECREF(py_key);
      Py_DECREF(py_val);
      Py_DECREF(inner_list);
      Py_DECREF(dict);
      return nullptr;
    }

    Py_DECREF(py_key);
    Py_DECREF(py_val);
    Py_DECREF(inner_list);
  }

  return dict;
}


bool py_to_int_matrix(PyObject* obj, vector<vector<int>>& out) {
  if (!PyList_Check(obj)) {
    PyErr_SetString(PyExc_TypeError, "varyingIndices must be a list of lists of ints");
    return false;
  }

  Py_ssize_t outer_size = PyList_Size(obj);
  out.clear();
  out.reserve(outer_size);

  for (Py_ssize_t i = 0; i < outer_size; i++) {
    PyObject* row_obj = PyList_GetItem(obj, i);  // borrowed
    if (!PyList_Check(row_obj)) {
      PyErr_SetString(PyExc_TypeError, "varyingIndices must be a list of lists of ints");
      return false;
    }

    Py_ssize_t inner_size = PyList_Size(row_obj);
    vector<int> row;
    row.reserve(inner_size);

    for (Py_ssize_t j = 0; j < inner_size; j++) {
      PyObject* item = PyList_GetItem(row_obj, j);  // borrowed
      if (!PyLong_Check(item)) {
        PyErr_SetString(PyExc_TypeError, "varyingIndices elements must be ints");
        return false;
      }
      long v = PyLong_AsLong(item);
      row.push_back(static_cast<int>(v));
    }
    out.push_back(row);
  }

  return true;
}

bool py_to_double_list(PyObject* obj, vector<double>& out) {
  if (!PySequence_Check(obj)) {
    PyErr_SetString(PyExc_TypeError, "bounds must be a sequence of floats");
    return false;
  }

  Py_ssize_t n = PySequence_Size(obj);
  out.clear();
  out.reserve(n);

  for (Py_ssize_t i = 0; i < n; i++) {
    PyObject* item = PySequence_GetItem(obj, i);  // new ref
    if (!item) {
      return false;
    }
    if (!PyFloat_Check(item) && !PyLong_Check(item)) {
      Py_DECREF(item);
      PyErr_SetString(PyExc_TypeError, "bounds elements must be numbers");
      return false;
    }
    double v = PyFloat_AsDouble(item);
    Py_DECREF(item);
    out.push_back(v);
  }

  return true;
}

