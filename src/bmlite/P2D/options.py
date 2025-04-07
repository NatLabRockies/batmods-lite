from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from numpy import ndarray

    from .domains import Electrode


class Hysteresis:

    def __init__(self, domain: Electrode, **options) -> None:
        self.domain = domain
        domain.g_hyst = options.pop('g_hyst')
        domain.M_hyst = options.pop('M_hyst')
        domain.hyst0 = options.pop('hyst0')

    def make_mesh(self, last_xvar: str, pshift: int = 0) -> str:
        domain = self.domain
        domain.ptr['hyst'] = domain.ptr[last_xvar] + 1
        return 'hyst'

    def sv0(self, sv0: ndarray) -> None:
        domain = self.domain
        start = domain.ptr['start']
        sv0[domain.x_ptr['hyst'] - start] = domain.hyst0

    def algidx(self, algdix: ndarray) -> None:
        pass

    def to_dict(self, sol: object) -> None:
        domain = self.domain
        hyst = sol.y[:, domain.x_ptr['hyst']]
        return {'hyst': hyst}
