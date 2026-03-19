"""
Summary
=======
Battery Analysis and Training Models for Optimization and Degradation Studies
(BATMODS) is a Python package with an API for pre-built battery models. The
original purpose of the package was to quickly generate synthetic data for
machine learning models to train with. However, the models are generally useful
for any battery simulation or analysis. BATMODS-lite includes the following:

1) A library and API for pre-built battery models
2) Kinetic/transport properties for common battery materials

Accessing the documentation
---------------------------
Documentation is accessible via Python's `help()` function which prints
docstrings from the specified package, module, function, class, etc. You can
also access the documentation by visiting the website, hosted on Read the Docs.
The website includes search functionality and more detailed examples.

"""

# Core package
from ._core import (
    Constants,
    Experiment,
    IDASolver,
    IDAResult,
    templates,
)

# Model subpackages
from . import P2D
from . import SPM

# Other submodules/subpackages
from . import mathutils
from . import materials
from . import mesh
from . import plotutils

__version__ = '0.0.2.dev0'

__all__ = [
    'Constants',
    'Experiment',
    'IDASolver',
    'IDAResult',
    'templates',
    'P2D',
    'SPM',
    'mathutils',
    'materials',
    'mesh',
    'plotutils',
]
