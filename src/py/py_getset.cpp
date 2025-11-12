#include "py_wrappers.h"
#include "oscillators.h"
//---------------------------------------------------------------------------------------------------------------------
//distribution get set
//---------------------------------------------------------------------------------------------------------------------
//noise dist
static PyObject* PyOscillators_get_noise_distribution(PyOscillators* self, void*) {
  const std::string& dist = self->cpp_obj->get_noise_distribution();
  const std::vector<double>& params = self->cpp_obj->get_noise_params();

  PyObject* py_params = PyList_New(params.size());
  for (size_t i = 0; i < params.size(); ++i) {
    PyList_SetItem(py_params, i, PyFloat_FromDouble(params[i]));
  }

  return Py_BuildValue("(sO)", dist.c_str(), py_params);
}

static int PyOscillators_set_noise_distribution(PyOscillators* self, PyObject* value, void*) {
  const char* dist;
  PyObject* paramsObj;

  // Expect a tuple: (str, list)
  if (!PyArg_ParseTuple(value, "sO", &dist, &paramsObj)) {
    PyErr_SetString(PyExc_TypeError, "omega_distribution must be (str, list[float])");
    return -1;
  }

  if (!PyList_Check(paramsObj)) {
    PyErr_SetString(PyExc_TypeError, "Second element must be a list of floats");
    return -1;
  }

  std::vector<double> params;
  Py_ssize_t len = PyList_Size(paramsObj);
  params.reserve(len);
  for (Py_ssize_t i = 0; i < len; ++i) {
    PyObject* item = PyList_GetItem(paramsObj, i);
    if (!PyFloat_Check(item)) {
      PyErr_SetString(PyExc_TypeError, "All parameters must be floats");
      return -1;
    }
    params.push_back(PyFloat_AsDouble(item));
  }

  self->cpp_obj->set_noise_distribution(std::string(dist), params);
  return 0;
}

//---------------------------------------------------------------------------------------------------------------------
//omega dist
static PyObject* PyOscillators_get_omega_distribution(PyOscillators* self, void*) {
  const std::string& dist = self->cpp_obj->get_omega_distribution();
  const std::vector<double>& params = self->cpp_obj->get_omega_params();

  PyObject* py_params = PyList_New(params.size());
  for (size_t i = 0; i < params.size(); ++i) {
    PyList_SetItem(py_params, i, PyFloat_FromDouble(params[i]));
  }

  return Py_BuildValue("(sO)", dist.c_str(), py_params);
}

static int PyOscillators_set_omega_distribution(PyOscillators* self, PyObject* value, void*) {
  const char* dist;
  PyObject* paramsObj;

  // Expect a tuple: (str, list)
  if (!PyArg_ParseTuple(value, "sO", &dist, &paramsObj)) {
    PyErr_SetString(PyExc_TypeError, "omega_distribution must be (str, list[float])");
    return -1;
  }

  if (!PyList_Check(paramsObj)) {
    PyErr_SetString(PyExc_TypeError, "Second element must be a list of floats");
    return -1;
  }

  std::vector<double> params;
  Py_ssize_t len = PyList_Size(paramsObj);
  params.reserve(len);
  for (Py_ssize_t i = 0; i < len; ++i) {
    PyObject* item = PyList_GetItem(paramsObj, i);
    if (!PyFloat_Check(item)) {
      PyErr_SetString(PyExc_TypeError, "All parameters must be floats");
      return -1;
    }
    params.push_back(PyFloat_AsDouble(item));
  }
  self->cpp_obj->set_omega_distribution(std::string(dist), params);
  return 0;
}

//---------------------------------------------------------------------------------------------------------------------
//theta dist

static PyObject* PyOscillators_get_theta_distribution(PyOscillators* self, void*) {
  const std::string& dist = self->cpp_obj->get_theta_distribution();
  const std::vector<double>& params = self->cpp_obj->get_theta_params();

  PyObject* py_params = PyList_New(params.size());
  for (size_t i = 0; i < params.size(); ++i) {
    PyList_SetItem(py_params, i, PyFloat_FromDouble(params[i]));
  }

  return Py_BuildValue("(sO)", dist.c_str(), py_params);
}

static int PyOscillators_set_theta_distribution(PyOscillators* self, PyObject* value, void*) {
  const char* dist;
  PyObject* paramsObj;

  // Expect a tuple: (str, list)
  if (!PyArg_ParseTuple(value, "sO", &dist, &paramsObj)) {
    PyErr_SetString(PyExc_TypeError, "theta_distribution must be (str, list[float])");
    return -1;
  }

  if (!PyList_Check(paramsObj)) {
    PyErr_SetString(PyExc_TypeError, "Second element must be a list of floats");
    return -1;
  }

  std::vector<double> params;
  Py_ssize_t len = PyList_Size(paramsObj);
  params.reserve(len);
  for (Py_ssize_t i = 0; i < len; ++i) {
    PyObject* item = PyList_GetItem(paramsObj, i);
    if (!PyFloat_Check(item)) {
      PyErr_SetString(PyExc_TypeError, "All parameters must be floats");
      return -1;
    }
    params.push_back(PyFloat_AsDouble(item));
  }

  self->cpp_obj->set_theta_distribution(std::string(dist), params);
  return 0;
}


//---------------------------------------------------------------------------------------------------------------------
//other initialisation get set
//---------------------------------------------------------------------------------------------------------------------
//coupling

static PyObject* PyOscillators_get_coupling(PyOscillators* self, void*) {
  const std::vector<std::vector<double>>& K = self->cpp_obj->get_coupling();

  PyObject* outer_list = PyList_New(K.size());
  for (size_t i = 0; i < K.size(); ++i) {
    const std::vector<double>& inner = K[i];
    PyObject* inner_list = PyList_New(inner.size());
    for (size_t j = 0; j < inner.size(); ++j) {
      PyList_SetItem(inner_list, j, PyFloat_FromDouble(inner[j]));
    }
    PyList_SetItem(outer_list, i, inner_list);
  }

  return outer_list;
}

static int PyOscillators_set_coupling(PyOscillators* self, PyObject* value, void*) {
  if (!PyList_Check(value)) {
    PyErr_SetString(PyExc_TypeError, "Coupling must be a list of lists of floats");
    return -1;
  }

  std::vector<std::vector<double>> K;
  Py_ssize_t outer_size = PyList_Size(value);
  K.reserve(outer_size);

  for (Py_ssize_t i = 0; i < outer_size; ++i) {
    PyObject* inner_obj = PyList_GetItem(value, i);
    if (!PyList_Check(inner_obj)) {
      PyErr_SetString(PyExc_TypeError, "Each row of coupling must be a list");
      return -1;
    }

    Py_ssize_t inner_size = PyList_Size(inner_obj);
    std::vector<double> inner;
    inner.reserve(inner_size);

    for (Py_ssize_t j = 0; j < inner_size; ++j) {
      PyObject* item = PyList_GetItem(inner_obj, j);
      if (!PyFloat_Check(item)) {
        PyErr_SetString(PyExc_TypeError, "Coupling entries must be floats");
        return -1;
      }
      inner.push_back(PyFloat_AsDouble(item));
    }

    K.push_back(inner);
  }

  self->cpp_obj->set_coupling(K);
  return 0;
}
//---------------------------------------------------------------------------------------------------------------------
//action oscillators
static PyObject* PyOscillators_get_action_oscillators(PyOscillators* self, void*) {
  const std::vector<int>& a = self->cpp_obj->get_action_oscillators();

  PyObject* list = PyList_New(a.size());
  for (size_t i = 0; i < a.size(); ++i) {
    PyList_SetItem(list, i, PyLong_FromLong(a[i]));
  }

  return list;
}

static int PyOscillators_set_action_oscillators(PyOscillators* self, PyObject* value, void*) {
  if (!PyList_Check(value)) {
    PyErr_SetString(PyExc_TypeError, "action_oscillators must be a list of integers");
    return -1;
  }

  std::vector<int> a;
  Py_ssize_t size = PyList_Size(value);
  a.reserve(size);

  for (Py_ssize_t i = 0; i < size; ++i) {
    PyObject* item = PyList_GetItem(value, i);
    if (!PyLong_Check(item)) {
      PyErr_SetString(PyExc_TypeError, "All elements must be integers");
      return -1;
    }
    a.push_back((int)PyLong_AsLong(item));
  }

  self->cpp_obj->set_action_oscillators(a);
  return 0;
}


//---------------------------------------------------------------------------------------------------------------------
//amplitude start stamp
static PyObject* PyOscillators_get_amplitude_stamp_start(PyOscillators* self, void*) {
  return PyLong_FromLong(self->cpp_obj->get_amplitude_stamp_start());
}

// Setter: validates Python int, then calls C++ setter
static int PyOscillators_set_amplitude_stamp_start(PyOscillators* self, PyObject* value, void*) {
  if (!PyLong_Check(value)) {
    PyErr_SetString(PyExc_TypeError, "amplitude_stamp_start must be an integer");
    return -1;
  }

  int s = static_cast<int>(PyLong_AsLong(value));

  try {
    self->cpp_obj->set_amplitude_stamp_start(s);
  } catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return -1;
  }

  return 0;
}
//---------------------------------------------------------------------------------------------------------------------
//getset table
//---------------------------------------------------------------------------------------------------------------------

PyGetSetDef PyOscillatorsGetSet[] = {
  {"noise_distribution", (getter)PyOscillators_get_noise_distribution, (setter)PyOscillators_set_noise_distribution, 
   "Noise distribution (name, (params))", NULL},
  {"omega_distribution", (getter)PyOscillators_get_omega_distribution, (setter)PyOscillators_set_omega_distribution, 
   "Omega distribution (name, (params))", NULL},
  {"theta_distribution", (getter)PyOscillators_get_theta_distribution, (setter)PyOscillators_set_theta_distribution, 
   "Theta distribution (name, (params))", NULL},
  {"coupling", (getter)PyOscillators_get_coupling, (setter)PyOscillators_set_coupling, 
   "Coupling matrix (list of lists of floats)", NULL},
  {"action_oscillators", (getter)PyOscillators_get_action_oscillators, (setter)PyOscillators_set_action_oscillators,
   "List of active oscillator indices", NULL},
  {"amplitude_timestamp_start", (getter)PyOscillators_get_amplitude_stamp_start, (setter)PyOscillators_set_amplitude_stamp_start,
   "Set the x-axis crossing that represents the first tapping event (int)" },
  {NULL}
};

