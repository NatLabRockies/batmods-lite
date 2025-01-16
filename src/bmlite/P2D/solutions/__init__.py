"""
Solution Classes
----------------
This package contains class definitions for each experimental solution. Most
solutions inherit from :class:`~bmlite.P2D.solutions.BaseSolution`, however,
their verification processes are unique.
"""

from ._base_solution import BaseSolution
from ._cc_solution import CCSolution
from ._cv_solution import CVSolution
from ._cp_solution import CPSolution

__all_exports = [BaseSolution, CCSolution, CVSolution, CPSolution]

for __export in __all_exports:
    __export.__module__ = __name__

__all__ = [export.__name__ for export in __all_exports]
