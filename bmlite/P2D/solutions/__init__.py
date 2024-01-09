from ._base_solution import BaseSolution
from ._cc_solution import CCSolution

__all_exports = [BaseSolution, CCSolution]

for __export in __all_exports:
    __export.__module__ = __name__

__all__ = [export.__name__ for export in __all_exports]
