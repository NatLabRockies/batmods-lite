from __future__ import annotations

from numbers import Real
from typing import Callable

import numpy as np


class Experiment:
    """Experiment builder."""

    __slots__ = ('_steps', '_step_options', '_all_options',)

    def __init__(self, **kwargs) -> None:
        """
        A class to define an experimental protocol. Use the add_step() method
        to add a series of sequential steps. Each step defines a control mode,
        a constant or time-dependent load profile, a time span, and optional
        limiting criteria to stop the step early if a specified event/state is
        detected.

        Parameters
        ----------
        **kwargs : dict, optional
            IDASolver keyword arguments that span all steps.

        See Also
        --------
        ~bmlite.IDASolver :
            The solver class, with documentation for most keyword arguments
            that you might want to adjust.

        """
        self._steps: list[dict] = []
        self._step_options: list[dict] = []
        self._all_options: dict = kwargs.copy()

    def __repr__(self) -> str:  # pragma: no cover
        """
        Return a readable repr string.

        Returns
        -------
        readable : str
            A console-readable instance representation.

        """
        from bmlite._utils import _repr

        keys = ['num_steps', 'options']
        values = [self.num_steps, self._all_options]

        return _repr('Experiment', keys, values)

    @property
    def steps(self) -> list[dict]:
        """
        Return steps list.

        Returns
        -------
        steps : list[dict]
            List of the step dictionaries.

        """
        return self._steps

    @property
    def num_steps(self) -> int:
        """
        Return number of steps.

        Returns
        -------
        num_steps : int
            Number of steps.

        """
        return len(self._steps)

    def print_steps(self) -> None:
        """Print a formatted/readable list of steps."""
        with np.printoptions(threshold=6, edgeitems=2):
            for i, step in enumerate(self.steps):
                print(f"\nStep {i}\n" + "-"*20)
                for key, value in step.items():
                    print(f"{key:<7} : {value!r}")

                print(f"options : {self._step_options[i]!r}")

    def add_step(self, mode: str, value: float | Callable, tspan: tuple,
                 limits: tuple[str, float] = None, **kwargs) -> None:
        """
        Add a step to the experiment.

        Parameters
        ----------
        mode : str
            Control mode, {'current_A', 'current_C', 'voltage_V', 'power_W'}.
        value : float | Callable
            Value of boundary contion mode, in the appropriate units. Note that
            negative and positive values of current and power reference charge
            and discharge directions, respectively.
        tspan : float or tuple[float, float] or 1D array
            Relative times for recording solution [s]. Providing a float will
            result in the solver picking time steps to save on its own. A tuple
            is interpreted as `(tmax, dt)` where the first element is the max
            time for the step (in seconds) and the second is the time interval
            between steps (also seconds). You can also provide any custom array
            of times at which to save the solution by providing a 1D `np.array`;
            however, the first element must be zero and the array must be in a
            monotonically increasing order, and there must be at least three
            elements. An array like `np.array([0, tmax])` will will result in
            the solver choosing its own time steps, similar to just providing a
            float. See notes for more information.
        limits : tuple[str, float], optional
            Stopping criteria for the new step, must be entered in sequential
            name/value pairs. Allowable names are {'current_A', 'current_C',
            'voltage_V', 'power_W', 'capacity_Ah','time_s', 'time_min',
            'time_h'}. Multiple limits are allowed by entering consecutive pairs
            of names and values. Capacity limits track the throughput of the
            step and are calculated by integrating current over time. The time
            limits are in reference to total experiment time. Step times are
            controlled using the 'tspan' argument instead of the 'limits' input.
            The default is None. Current and power limits should follow the
            same sign convention as the mode, i.e., negative values for charge
            and positive for discharge.
        **kwargs : dict, optional
            IDASolver keyword arguments specific to the new step only.

        Raises
        ------
        ValueError
            'mode' is invalid.
        ValueError
            A 'limits' name is invalid.
        TypeError
            'tspan' must be type float, tuple, or np.array.
        ValueError
            'tspan' tuple must be length 2.
        TypeError
            'tspan' tuple values must be type float.
        ValueError
            'tspan[1]' must be less than 'tspan[0]' when given a tuple.
        ValueError
            'tspan' arrays must be one-dimensional.
        ValueError
            'tspan[0]' must be zero when given an array.
        ValueError
            'tspan' arrays must be monotonically increasing.

        See Also
        --------
        ~bmlite.IDASolver :
            The solver class, with documentation for most keyword arguments
            that you might want to adjust.

        Notes
        -----
        For time-dependent loads, use a Callable for `value` with a function
        signature like `def load(t: float) -> float`, where `t` is the step's
        relative time, in seconds.

        When `tspan` is given as a 2-tuple, like `(tmax, dt)`, the time span is
        constructed as:

        .. code-block:: python

            tspan = np.arange(0., tspan[0], tspan[1])

        In the case where `tmax` is not an integer multiple of `dt`, a final
        time point is appended to ensure that `tspan[-1] == tmax`. If this is
        too restrictive, you can instead provide a custom 1D `np.array` for the
        `tspan` argument. However, the array is checked to make sure the first
        element is zero and the array is monotonically increasing. If either of
        these checks fail, a `ValueError` is raised.

        """
        _check_mode(mode)
        _check_limits(limits)

        mode, units = mode.split('_')

        if isinstance(tspan, Real):
            tspan = np.array([0., tspan], dtype=float)

        elif isinstance(tspan, tuple):

            if not len(tspan) == 2:
                raise ValueError("'tspan' tuple must be length 2.")
            elif not all(isinstance(val, Real) for val in tspan):
                raise TypeError("'tspan' tuple values must be type float.")
            elif tspan[1] >= tspan[0]:
                raise ValueError("'tspan[1]' must be less than 'tspan[0]'"
                                 " when given a tuple.")

            tmax, dt = tspan
            tspan = np.arange(0., tmax, dt, dtype=float)

            if tspan[-1] != tmax:
                tspan = np.hstack([tspan, tmax])

        elif not isinstance(tspan, np.ndarray):
            raise TypeError("'tspan' must be type float, tuple, or np.array.")

        tspan = np.asarray(tspan, dtype=float)

        if tspan.ndim != 1:
            raise ValueError("'tspan' must be one-dimensional.")
        elif tspan[0] != 0.:
            raise ValueError("'tspan[0]' must be zero.")
        elif tspan.size < 2:
            raise ValueError("'tspan' array length must be at least two.")
        elif not all(np.diff(tspan) > 0.):
            raise ValueError("'tspan' must be monotonically increasing.")

        step = {}
        step['mode'] = mode
        step['value'] = value
        step['units'] = units
        step['tspan'] = tspan
        step['limits'] = limits

        self._steps.append(step)
        self._step_options.append({**self._all_options, **kwargs})


def _check_mode(mode: str) -> None:
    """
    Check the operating mode.

    Parameters
    ----------
    mode : str
        Operating mode and units.

    Raises
    ------
    ValueError
        'mode' is invalid.

    """
    valid = ['current_A', 'current_C', 'voltage_V', 'power_W']

    if mode not in valid:
        raise ValueError(f"{mode=} is invalid; valid values are {valid}.")


def _check_limits(limits: tuple[str, float]) -> None:
    """
    Check the limit criteria.

    Parameters
    ----------
    limit : tuple[str, float]
        Stopping criteria and limiting value.

    Raises
    ------
    ValueError
        'limits' length must be even.
    ValueError
        A 'limits' name is invalid.

    """
    valid = [
        'current_A',
        'current_C',
        'voltage_V',
        'power_W',
        'time_s',
        'time_min',
        'time_h',
    ]

    if limits is None:
        pass
    elif len(limits) % 2 != 0:
        raise ValueError("'limits' length must be even.")
    else:

        for i in range(len(limits) // 2):
            name = limits[2*i]
            value = limits[2*i + 1]

            if name not in valid:
                raise ValueError(f"The limit name '{name}' is invalid; valid"
                                 f" values are {valid}.")

            elif not isinstance(value, (int, float)):
                raise TypeError(f"Limit '{name}' value must be type float.")
