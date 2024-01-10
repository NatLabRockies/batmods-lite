"""
Material Properties Package
---------------------------
The ``materials`` package contains kinetic and transport properties for common
battery materials, including both electrode active materials and electrolytes.
"""

from ._gen2_electrolyte import Gen2Electrolyte
from ._graphite_fast import GraphiteFast
from ._graphite_slow import GraphiteSlow
from ._nmc_532_fast import NMC532Fast
from ._nmc_532_slow import NMC532Slow

__all_exports = [
    Gen2Electrolyte,
    GraphiteFast,
    GraphiteSlow,
    NMC532Fast,
    NMC532Slow,
]

for __export in __all_exports:
    __export.__module__ = __name__

__all__ = [export.__name__ for export in __all_exports]
