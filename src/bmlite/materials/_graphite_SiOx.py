from numbers import Real
import numpy as np


class GraphiteSiOx:

    def __init__(self, alpha_a: float, alpha_c: float, Li_max: float) -> None:
        """
        Computationally fast GraphiteSiOx kinetic and transport properties.

        Parameters
        ----------
        alpha_a : float
            Anodic symmetry factor in Butler-Volmer expression [-].
        alpha_c : float
            Cathodic symmetry factor in Butler-Volmer expression [-].
        Li_max : float
            Maximum lithium concentration in solid phase [kmol/m3].

        """
        self.alpha_a = alpha_a
        self.alpha_c = alpha_c
        self.Li_max = Li_max

    def get_Ds(self, x: float | np.ndarray, T: float,
               fluxdir: float | np.ndarray) -> float | np.ndarray:
        """
        Calculate the lithium diffusivity in the solid phase given the local
        intercalation fraction `x` and temperature `T`.

        From Table V in
        "Development of Experimental Techniques for Parameterization
        "of Multi-scale Lithium-ion Battery Models",
        Chen et al., J. of the Electrochemical Society, 2020 Vol. 167
        The functional form is the same as Graphite but is scaled so
        the average over x matches the paper above at 30C

        Parameters
        ----------
        x : float | 1D array
            Lithium intercalation fraction [-].
        T : float
            Battery temperature [K].
        fluxdir : float | 1D array
            Lithiation direction: +1 for lithiation, -1 for delithiation, 0 for
            rest. Used for direction-dependent parameters. Ensure the zero case
            is handled explicitly or via a default (lithiating or delithiating).

        Returns
        -------
        Ds : float | 1D array
            Lithium diffusivity in the solid phase [m2/s].

        """
        from .. import Constants

        c = Constants()

        Ds = 3e-14 * np.exp(-30e6 / c.R * (1 / T - 1 / 303.15))
        Ds *= (1.74/30)

        if np.atleast_1d(x).size > 1:
            Ds = Ds * np.ones_like(x)

        return Ds

    def get_i0(self, x: float | np.ndarray, C_Li: float | np.ndarray,
               T: float, fluxdir: float | np.ndarray) -> float | np.ndarray:
        """
        Calculate the exchange current density given the intercalation
        fraction `x` at the particle surface, the local lithium ion
        concentration `C_Li`, and temperature `T`. The input types for
        `x` and `C_Li` should both be the same (i.e., both float or both
        1D arrays).

        From Table VI in
        "Development of Experimental Techniques for Parameterization
        of Multi-scale Lithium-ion Battery Models",
        Chen et al., J. of the Electrochemical Society, 2020 Vol. 167
        The functional form is the same as Graphite but is scaled so
        the average over x matches the paper above at 30C

        Parameters
        ----------
        x : float | 1D array
            Lithium intercalation fraction at `r = R_s` [-].
        C_Li : float | 1D array
            Lithium ion concentration in the local electrolyte [kmol/m3].
        T : float
            Battery temperature [K].
        fluxdir : float | 1D array
            Lithiation direction: +1 for lithiation, -1 for delithiation, 0 for
            rest. Used for direction-dependent parameters. Ensure the zero case
            is handled explicitly or via a default (lithiating or delithiating).

        Returns
        -------
        i0 : float | 1D array
            Exchange current density [A/m2].

        """
        from .. import Constants

        c = Constants()

        # Avoid floating point errors
        if isinstance(x, Real):
            if (x < 0 and self.alpha_c < 1) or (x > 1 and self.alpha_a < 1):
                raise ValueError('x is out of [0, 1] during i0 calculation')
        elif isinstance(x, np.ndarray):
            if ((any(x.flatten() < 0) and self.alpha_c < 1)
               or (any(x.flatten() > 1) and self.alpha_a < 1)):
                raise ValueError('x is out of [0, 1] during i0 calculation')

        i0 = 2.5 * 0.27 * np.exp(-30e6 / c.R * (1 / T - 1 / 303.15)) \
            * C_Li**self.alpha_a * (self.Li_max * x)**self.alpha_c \
            * (self.Li_max - self.Li_max * x)**self.alpha_a
        i0 *= (0.354/7.754866189692474)

        return i0

    def get_Eeq(self, x: float | np.ndarray) -> float | np.ndarray:
        """
        Calculate the equilibrium potential given the surface intercalation
        fraction `x` at the particle surface.

        From Eq 9 in
        "Development of Experimental Techniques for Parameterization
        of Multi-scale Lithium-ion Battery Models",
        Chen et al., J. of the Electrochemical Society, 2020 Vol. 167

        Parameters
        ----------
        x : float
            Lithium intercalation fraction at `r = R_s` [-].

        Returns
        -------
        Eeq : float
            Equilibrium potential [V].

        """
        x = np.atleast_1d(x)

        Eeq = 1.9793*np.exp(-39.3631*x) + 0.2482 \
            - 0.0909 * np.tanh(29.8538*(x - 0.1234)) \
            - 0.04478 * np.tanh(14.9159*(x - 0.2769)) \
            - 0.0205 * np.tanh(30.4444*(x - 0.6103))

        Eeq = np.real(Eeq)

        Eeq[x <= 0] = 10
        Eeq[x > 1] = -10

        return Eeq.squeeze()

    def get_Mhyst(self, x: float | np.ndarray) -> float | np.ndarray:
        """
        Calculate the hysteresis magnitude given the surface intercalation
        fraction `x` at the particle surface.

        Parameters
        ----------
        x : float | 1D array
            Lithium intercalation fraction at `r = R_s` [-].

        Returns
        -------
        M_hyst : float | 1D array
            Hysteresis magnitude [V].

        """
        M_hyst = 0.03
        if isinstance(x, np.ndarray):
            M_hyst *= np.ones_like(x)

        return M_hyst


class GraphiteSiOxSlow(GraphiteSiOx):

    def __init__(
        self,
        alpha_a: float,
        alpha_c: float,
        Li_max: float,
        csvfile: str | None = None
    ) -> None:
        """
        Computationally slow GraphiteSiOx kinetic and transport properties.

        Differs from `GraphiteSiOx` because the equilibrium potential is
        piecewise here, making it more accurate, but slower to evaluate.

        Parameters
        ----------
        alpha_a : float
            Anodic symmetry factor in Butler-Volmer expression [-].
        alpha_c : float
            Cathodic symmetry factor in Butler-Volmer expression [-].
        Li_max : float
            Maximum lithium concentration in solid phase [kmol/m3].
        csv_file: str | None
            Path to open circuit potential data. Contains 2 column x, V
            If None, reads data/graphite_SiOx_ocv.csv
        """
        import os
        import pandas as pd
        from scipy.interpolate import PchipInterpolator

        super().__init__(alpha_a, alpha_c, Li_max)

        if csvfile is None:
            csvfile = os.path.dirname(__file__) + '/data/graphite_SiOx_ocv.csv'

        self.check_ocv_data(csvfile)

        df = pd.read_csv(csvfile).sort_values(by='x')

        self.x_min = df['x'].min()
        self.x_max = df['x'].max()
        self._Eeq_spline = PchipInterpolator(df['x'], df['V'])

    def check_ocv_data(self, csvfile: str) -> None:
        """
        Check that the open circuit potential data has the right format

        Parameters
        ----------
        csvfile: str
            Path to open circuit potential data. Contains 2 column x,V
        """
        import pandas as pd

        # Basic pandas reading checks
        df = pd.read_csv(csvfile)

        # Check if x and V are in the OCV data
        if not {'x', 'V'}.issubset(df.columns):
            raise ValueError(
                f"Expected 'x' and 'V', but found: {list(df.columns)}"
            )

        # Check if the intercalation fraction x is between 0 and 1
        if not df['x'].between(0, 1).all():
            raise ValueError(
                "Not all values in column 'x' are between 0 and 1."
            )

        # Check if the potential V is positive (>= 0)
        if not (df['V'] >= 0).all():
            raise ValueError(
                "Not all values in column 'V' are positive."
            )

    def get_Eeq(self, x: float | np.ndarray) -> float | np.ndarray:
        """
        Calculate the equilibrium potential given the surface intercalation
        fraction `x` at the particle surface.

        Parameters
        ----------
        x : float
            Lithium intercalation fraction at `r = R_s` [-].

        Returns
        -------
        Eeq : float
            Equilibrium potential [V].

        """
        return self._Eeq_spline(x)
