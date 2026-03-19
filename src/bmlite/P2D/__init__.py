"""
A packaged pseudo-2D (P2D) model. Build a model using the `Simulation` class,
and run an experiment using either the `run()` or `run_step()` methods. These
methods return `Solution` class instances with post processing, plotting, and
saving methods.

"""

from ._simulation import Simulation
from ._solutions import StepSolution, CycleSolution

from . import dae
from . import domains
from . import postutils
from . import submodels

__all__ = [
    'Simulation',
    'StepSolution',
    'CycleSolution',
    'dae',
    'domains',
    'postutils',
    'submodels',
]
