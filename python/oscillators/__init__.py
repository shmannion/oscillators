import os
import importlib.util

# Path to the C++ extension
_so_path = os.path.join(os.path.dirname(__file__), "../oscillators.so")

_spec = importlib.util.spec_from_file_location("oscillators", _so_path)
_osc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_osc)

# Expose functions/classes from the C++ module
# riemann_zeta = _osc.riemann_zeta
# Vector2 = _osc.Vector2

# Optional: add any Python helpers here

