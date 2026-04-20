"""
The `materials` package contains kinetic and transport properties for common
battery materials, including both electrode active materials and electrolytes.

"""

from ._gen2_electrolyte import Gen2Electrolyte

from ._graphite import GraphiteFast, GraphiteSlow, GraphiteSlowExtrap
from ._graphite_SiOx import GraphiteSiOx, GraphiteSiOxSlow

from ._lfp import LFPInterp
from ._nmc_532 import NMC532Fast, NMC532Slow, NMC532SlowExtrap
from ._nmc_811 import NMC811, NMC811Slow

__all__ = [
    'Gen2Electrolyte',
    'GraphiteFast',
    'GraphiteSlow',
    'GraphiteSlowExtrap',
    'GraphiteSiOx',
    'GraphiteSiOxSlow',
    'LFPInterp',
    'NMC532Fast',
    'NMC532Slow',
    'NMC532SlowExtrap',
    'NMC811',
    'NMC811Slow',
]
