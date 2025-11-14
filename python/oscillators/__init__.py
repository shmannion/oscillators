from .oscillators import *
from .oscillators import Oscillators as _COscillators
from .data_utils import *
from .goodness_of_fit import *
from .correlations import *
from .python_extensions import OscillatorsPythonAddons


class Oscillators(_COscillators, OscillatorsPythonAddons):
    """ Merge C++ class with the Python extensions class"""
    pass
