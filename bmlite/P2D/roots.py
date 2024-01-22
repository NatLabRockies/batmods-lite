from numpy import ndarray as _ndarray


class VStop(object):

    __slots__ = ['V_stop', 'nr_rootfns']

    def __init__(self, V_stop: float) -> None:
        self.V_stop = V_stop
        self.nr_rootfns = 1

    def __call__(self, t: float, sv: _ndarray, svdot: _ndarray,
                 events: _ndarray, inputs: tuple) -> None:

        sim, _ = inputs

        events[0] = sv[sim.ca.x_ptr('phi_ed')[-1]] - self.V_stop


class VLims(object):

    __slots__ = ['V_low', 'V_high', 'nr_rootfns']

    def __init__(self, V_low: float, V_high: float) -> None:
        self.V_low = V_low
        self.V_high = V_high
        self.nr_rootfns = 2

    def __call__(self, t: float, sv: _ndarray, svdot: _ndarray,
                 events: _ndarray, inputs: tuple) -> None:

        sim, _ = inputs

        events[0] = sv[sim.ca.x_ptr('phi_ed')[-1]] - self.V_low
        events[1] = sv[sim.ca.x_ptr('phi_ed')[-1]] - self.V_high


class IStop(object):

    __slots__ = ['I_stop', 'nr_rootfns']

    def __init__(self, I_stop: float) -> None:
        self.I_stop = I_stop
        self.nr_rootfns = 1

    def __call__(self, t: float, sv: _ndarray, svdot: _ndarray,
                 events: _ndarray, inputs: tuple) -> None:

        sim, exp = inputs

        events[0] = exp['i_ext'] - self.I_stop / sim.bat.area


class ILims(object):

    __slots__ = ['I_low', 'I_high', 'nr_rootfns']

    def __init__(self, I_low: float, I_high: float) -> None:
        self.I_low = I_low
        self.I_high = I_high
        self.nr_rootfns = 2

    def __call__(self, t: float, sv: _ndarray, svdot: _ndarray,
                 events: _ndarray, inputs: tuple) -> None:

        sim, exp = inputs

        events[0] = exp['i_ext'] - self.I_low / sim.bat.area
        events[1] = exp['i_ext'] - self.I_high / sim.bat.area
