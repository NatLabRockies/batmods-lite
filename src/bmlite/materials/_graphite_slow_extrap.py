from numpy import ndarray as _ndarray


class GraphiteSlowExtrap(object):

    def __init__(self, alpha_a: float, alpha_c: float, Li_max: float) -> None:
        """
        Computationally slow Graphite kinetic and transport properties.

        Differs from ``GraphiteFast`` because the equilibrium potential is
        piecewise here, making it more accurate, but slower to evaluate.

        Differs from ``GraphiteSlow`` because the equilibrium potential is
        extrapolated to 0V when x=1

        Parameters
        ----------
        alpha_a : float
            Anodic symmetry factor in Butler-Volmer expression [-].

        alpha_c : float
            Cathodic symmetry factor in Butler-Volmer expression [-].

        Li_max : float
            Maximum lithium concentration in solid phase [kmol/m^3].
        """

        import os

        import pandas as pd
        from scipy.interpolate import CubicSpline

        self.alpha_a = alpha_a
        self.alpha_c = alpha_c
        self.Li_max = Li_max

        csvfile = os.path.dirname(__file__) + '/data/graphite_ocv_extrap.csv'
        df = pd.read_csv(csvfile).sort_values(by='x')

        self.x_min = df['x'].min()
        self.x_max = df['x'].max()
        self._Eeq_spline = CubicSpline(df['x'], df['V'])

    def get_Ds(self, x: float | _ndarray, T: float) -> float | _ndarray:
        """
        Calculate the lithium diffusivity in the solid phase given the local
        intercalation fraction ``x`` and temperature ``T``.

        Parameters
        ----------
        x : float | 1D array
            Lithium intercalation fraction [-].

        T : float
            Battery temperature [K].

        Returns
        -------
        Ds : float | 1D array
            Lithium diffusivity in the solid phase [m^2/s].
        """

        import numpy as np

        from .. import Constants

        c = Constants()

        Ds = 3e-14 * np.exp(-30e6 / c.R * (1 / T - 1 / 303.15))

        if np.atleast_1d(x).size > 1:
            Ds = Ds * np.ones_like(x)

        return Ds

    def get_i0(self, x: float | _ndarray, C_Li: float | _ndarray,
               T: float) -> float | _ndarray:
        """
        Calculate the exchange current density given the intercalation
        fraction ``x`` at the particle surface, the local lithium ion
        concentration ``C_Li``, and temperature ``T``. The input types for
        ``x`` and ``C_Li`` should both be the same (i.e., both float or both
        1D arrays).

        Parameters
        ----------
        x : float | 1D array
            Lithium intercalation fraction at ``r = R_s`` [-].

        C_Li : float | 1D array
            Lithium ion concentration in the local electrolyte [kmol/m^3].

        T : float
            Battery temperature [K].

        Returns
        -------
        i0 : float | 1D array
            Exchange current density [A/m^2].
        """

        import numpy as np

        from .. import Constants

        c = Constants()

        i0 = 2.5 * 0.27 * np.exp(-30e6 / c.R * (1 / T - 1 / 303.15)) \
            * C_Li**self.alpha_a * (self.Li_max * x)**self.alpha_c \
            * (self.Li_max - self.Li_max * x)**self.alpha_a

        return i0

    def get_Eeq(self, x: float | _ndarray, T: float) -> float | _ndarray:
        """
        Calculate the equilibrium potential given the intercalation fraction
        ``x`` at the particle surface and temperature ``T``.

        Parameters
        ----------
        x : float | 1D array
            Lithium intercalation fraction at ``r = R_s`` [-].

        T : float
            Battery temperature [K].

        Returns
        -------
        Eeq : float | 1D array
            Equilibrium potential [V].

        """

        return self._Eeq_spline(x)
