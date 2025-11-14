#include "py_wrappers.h"
#include "oscillators.h"

//---------------------------------------------------------------------------------------------------------------------
//public attribute get set
//---------------------------------------------------------------------------------------------------------------------
//noise dist
static PyObject* PyOscillators_get_N(PyOscillators* self, void*) {
  return PyLong_FromLong(self->cpp_obj->N);
}

static int PyOscillators_set_N(PyOscillators* self, PyObject* value, void*) {
  if (!PyLong_Check(value)) {
    PyErr_SetString(PyExc_TypeError, "N must be an integer");
    return -1;
  }
  self->cpp_obj->N = PyLong_AsLong(value);
  return 0;
}

//---------------------------------------------------------------------------------------------------------------------
//distribution get set
//---------------------------------------------------------------------------------------------------------------------
//noise dist
static PyObject* PyOscillators_get_noise_distribution(PyOscillators* self, void*) {
  const string& dist = self->cpp_obj->get_noise_distribution();
  const vector<double>& params = self->cpp_obj->get_noise_params();

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

  vector<double> params;
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

  self->cpp_obj->set_noise_distribution(string(dist), params);
  return 0;
}

//---------------------------------------------------------------------------------------------------------------------
//omega dist
static PyObject* PyOscillators_get_omega_distribution(PyOscillators* self, void*) {
  const string& dist = self->cpp_obj->get_omega_distribution();
  const vector<double>& params = self->cpp_obj->get_omega_params();

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

  vector<double> params;
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
  self->cpp_obj->set_omega_distribution(string(dist), params);
  return 0;
}

//---------------------------------------------------------------------------------------------------------------------
//theta dist

static PyObject* PyOscillators_get_theta_distribution(PyOscillators* self, void*) {
  const string& dist = self->cpp_obj->get_theta_distribution();
  const vector<double>& params = self->cpp_obj->get_theta_params();

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

  vector<double> params;
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

  self->cpp_obj->set_theta_distribution(string(dist), params);
  return 0;
}


//---------------------------------------------------------------------------------------------------------------------
//other initialisation get set
//---------------------------------------------------------------------------------------------------------------------
//coupling

static PyObject* PyOscillators_get_coupling(PyOscillators* self, void*) {
  const vector<vector<double>>& K = self->cpp_obj->get_coupling();

  PyObject* outer_list = PyList_New(K.size());
  for (size_t i = 0; i < K.size(); ++i) {
    const vector<double>& inner = K[i];
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

  vector<vector<double>> K;
  Py_ssize_t outer_size = PyList_Size(value);
  K.reserve(outer_size);

  for (Py_ssize_t i = 0; i < outer_size; ++i) {
    PyObject* inner_obj = PyList_GetItem(value, i);
    if (!PyList_Check(inner_obj)) {
      PyErr_SetString(PyExc_TypeError, "Each row of coupling must be a list");
      return -1;
    }

    Py_ssize_t inner_size = PyList_Size(inner_obj);
    vector<double> inner;
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
  const vector<int>& a = self->cpp_obj->get_action_oscillators();

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

  vector<int> a;
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
//setting dt 

static PyObject* PyOscillators_get_time_step(PyOscillators* self, void*) {
  return PyLong_FromDouble(self->cpp_obj->get_time_step());
}

// Setter: validates Python int, then calls C++ setter
static int PyOscillators_set_time_step(PyOscillators* self, PyObject* value, void*) {
  if (!PyFloat_Check(value)) {
    PyErr_SetString(PyExc_TypeError, "dt must be a float");
    return -1;
  }

  double t = PyFloat_AsDouble(value);

  try {
    self->cpp_obj->set_time_step(t);
  } catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return -1;
  }

  return 0;
}

//---------------------------------------------------------------------------------------------------------------------
//setting tmax

static PyObject* PyOscillators_get_tmax(PyOscillators* self, void*) {
  return PyFloat_FromDouble(self->cpp_obj->get_max_time());
}

// Setter: validates Python int, then calls C++ setter
static int PyOscillators_set_tmax(PyOscillators* self, PyObject* value, void*) {
  if (!PyFloat_Check(value)) {
    PyErr_SetString(PyExc_TypeError, "tmax must be a float");
    return -1;
  }

  double t = PyFloat_AsDouble(value);

  try {
    self->cpp_obj->set_max_time(t);
  } catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return -1;
  }

  return 0;
}

//---------------------------------------------------------------------------------------------------------------------
//method to generate timestamps
static PyObject* PyOscillators_get_timestamp_method(PyOscillators* self, void*) {
  return PyUnicode_FromString(self->cpp_obj->get_timestamp_method().c_str());
}

// Setter for timestamp_method
static int PyOscillators_set_timestamp_method(PyOscillators* self, PyObject* value, void*) {
  if (!PyUnicode_Check(value)) {
    PyErr_SetString(PyExc_TypeError, "timestamp_method must be a string");
    return -1;
  }

  PyObject* temp_bytes = PyUnicode_AsEncodedString(value, "utf-8", "strict");
  if (!temp_bytes) {
    return -1;
  }

  const char* cstr = PyBytes_AS_STRING(temp_bytes);
  self->cpp_obj->set_timestamp_method(string(cstr));
  Py_DECREF(temp_bytes);

  return 0;
}


//---------------------------------------------------------------------------------------------------------------------
//get inter_event times
static PyObject* PyOscillators_get_inter_event_times(PyOscillators* self, void*) {
  const vector<vector<double>>& times = self->cpp_obj->get_inter_event_times();

  PyObject* outer_list = PyList_New(times.size());
  for (size_t i = 0; i < times.size(); ++i) {
    const vector<double>& inner = times[i];
    PyObject* inner_list = PyList_New(inner.size());
    for (size_t j = 0; j < inner.size(); ++j) {
      PyList_SetItem(inner_list, j, PyFloat_FromDouble(inner[j]));
    }
    PyList_SetItem(outer_list, i, inner_list);
  }

  return outer_list;
}

//---------------------------------------------------------------------------------------------------------------------
//get simulation results

static PyObject* PyOscillators_get_simulation_results(PyOscillators* self, void*) {
  try {
    const auto& r = self->cpp_obj->get_simulation_results();
    return map_to_pydict(r);
  }
  catch (const exception& e) {
    PyErr_SetString(PyExc_RuntimeError, e.what());
    return nullptr;
  }
}


//---------------------------------------------------------------------------------------------------------------------
//getset table
//---------------------------------------------------------------------------------------------------------------------

PyGetSetDef PyOscillatorsGetSet[] = {
  {"N", (getter)PyOscillators_get_N, (setter)PyOscillators_set_N,"Number of oscillators", NULL},
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
   "Set the x-axis crossing that represents the first tapping event (int)", NULL},
  {"dt", (getter)PyOscillators_get_time_step, (setter)PyOscillators_set_time_step,
   "Set the integration time step", NULL},
  {"tmax", (getter)PyOscillators_get_tmax, (setter)PyOscillators_set_tmax,
   "Set the max time of each simulation", NULL},
  {"timestamp_method", (getter)PyOscillators_get_timestamp_method, (setter)PyOscillators_set_timestamp_method,
   "Timestamp method used in event calculations (can be 'phase' or 'amplitude')", NULL},
  {"inter_event_times_list", (getter)PyOscillators_get_inter_event_times, NULL,  
   "Inter event times for all oscillators as list of lists", NULL},
  {"simulation_results_dict", (getter)PyOscillators_get_simulation_results, NULL,  
   "Simulation resulst as a dictionary", NULL},
  {NULL}
};

