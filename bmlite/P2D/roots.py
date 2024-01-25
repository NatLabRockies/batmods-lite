"""
Root Functions
--------------
This module includes root functions for the SPM model. Root functions allow the
integrator to stop prior to ``t_max`` when an event (or root) occurs. For
example, during a typical CCCV charge protocol, it is common to stop and switch
from constant-current to constant-voltage at a specified voltage.
"""

from numpy import ndarray as _ndarray


class VLimits(object):

    __slots__ = ['V_low', 'V_high', 'nr_rootfns']

    def __init__(self, V_low: float, V_high: float) -> None:
        """
        Generate a root function that stops at voltage limits.

        Parameters
        ----------
        V_low : float
            The desired low voltage limit [V].

        V_high : float
            The desired high voltage limit [V].
        """

        self.V_low = V_low
        self.V_high = V_high
        self.nr_rootfns = 2

    def __call__(self, t: float, sv: _ndarray, svdot: _ndarray,
                 events: _ndarray, inputs: tuple) -> None:
        """
        Definition of the root function. ``events`` is an array whose elements
        are set with expressions. If any of these expressions ever equal zero,
        the IDA solver will stop with ``onroot = True``.

        Parameters
        ----------
        t : float
            Value of time [s].

        sv : 1D array
            Solution/state variables at time ``t``.

        svdot : 1D array
            Solution/state variable time derivatives at time ``t``.

        events : 1D array
            An empty array with a length equal to the number of root functions,
            here ``nr_rootfns = 2``.

        inputs : (sim : P2D Simulation object, exp : experiment dict)
            The simulation object and experimental details dictionary inputs
            that describe the specific battery and experiment to simulate.

        Returns
        -------
        None.
        """

        sim, _ = inputs

        events[0] = sv[sim.ca.x_ptr('phi_ed')[-1]] - self.V_low
        events[1] = sv[sim.ca.x_ptr('phi_ed')[-1]] - self.V_high


class ILimits(object):

    __slots__ = ['I_low', 'I_high', 'nr_rootfns']

    def __init__(self, I_low: float, I_high: float) -> None:
        """
        Generate a root function that stops at current limits.

        Parameters
        ----------
        I_low : float
            The desired low current limit [A], + for charge, - for discharge.

        I_high : float
            The desired high current limit [A], + for charge, - for discharge.
        """

        self.I_low = I_low
        self.I_high = I_high
        self.nr_rootfns = 2

    def __call__(self, t: float, sv: _ndarray, svdot: _ndarray,
                 events: _ndarray, inputs: tuple) -> None:
        """
        Definition of the root function. ``events`` is an array whose elements
        are set with expressions. If any of these expressions ever equal zero,
        the IDA solver will stop with ``onroot = True``.

        Parameters
        ----------
        t : float
            Value of time [s].

        sv : 1D array
            Solution/state variables at time ``t``.

        svdot : 1D array
            Solution/state variable time derivatives at time ``t``.

        events : 1D array
            An empty array with a length equal to the number of root functions,
            here ``nr_rootfns = 2``.

        inputs : (sim : P2D Simulation object, exp : experiment dict)
            The simulation object and experimental details dictionary inputs
            that describe the specific battery and experiment to simulate.

        Returns
        -------
        None.
        """

        sim, exp = inputs

        events[0] = exp['i_ext'] - self.I_low / sim.bat.area
        events[1] = exp['i_ext'] - self.I_high / sim.bat.area
