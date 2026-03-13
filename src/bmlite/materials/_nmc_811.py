import numpy as np


class NMC811:

    def __init__(self, alpha_a: float, alpha_c: float, Li_max: float) -> None:
        """
        Computationally NMC811 kinetic and transport properties.

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
        intercalation fraction ``x`` and temperature ``T``.

        From Table V in
        "Development of Experimental Techniques for Parameterization
        "of Multi-scale Lithium-ion Battery Models",
        Chen et al., J. of the Electrochemical Society, 2020 Vol. 167
        The functional form is the same as NMC532 but is scaled so
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
        A = np.array([
            -2.509010843479270e+2,
             2.391026725259970e+3,
            -4.868420267611360e+3,
            -8.331104102921070e+1,
             1.057636028329000e+4,
            -1.268324548348120e+4,
             5.016272167775530e+3,
             9.824896659649480e+2,
            -1.502439339070900e+3,
             4.723709304247700e+2,
            -6.526092046397090e+1,
        ])

        Ds = (1.48 / 2.38) * np.exp(-30e6/c.R * (1./T - 1./303.15)) \
           * 2.25 * 10.0**(np.polyval(A, x))

        return Ds

    def get_i0(self, x: float | np.ndarray, C_Li: float | np.ndarray,
               T: float, fluxdir: float | np.ndarray) -> float | np.ndarray:
        """
        Calculate the exchange current density given the intercalation
        fraction ``x`` at the particle surface, the local lithium ion
        concentration ``C_Li``, and temperature ``T``. The input types for
        ``x`` and ``C_Li`` should both be the same (i.e., both float or both
        1D arrays).

        From Table VI in
        "Development of Experimental Techniques for Parameterization
        of Multi-scale Lithium-ion Battery Models",
        Chen et al., J. of the Electrochemical Society, 2020 Vol. 167
        The functional form is the same as NMC532 but is scaled so
        the average over x matches the paper above at 30C

        Parameters
        ----------
        x : float | 1D array
            Lithium intercalation fraction at ``r = R_s`` [-].
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
        A = np.array([
             1.650452829641290e+1,
            -7.523567141488800e+1,
             1.240524690073040e+2,
            -9.416571081287610e+1,
             3.249768821737960e+1,
            -3.585290065824760e+0,
        ])

        i0 = (34.8)/(0.214) * 9.*(C_Li/1.2)**self.alpha_a * np.polyval(A, x) \
           * np.exp(-30e6/c.R * (1./T - 1./303.15))

        return i0

    def get_Eeq(self, x: float | np.ndarray) -> float | np.ndarray:
        """
        Calculate the equilibrium potential given the surface intercalation
        fraction ``x`` at the particle surface.

        From Eq 8 in
        "Development of Experimental Techniques for Parameterization
        of Multi-scale Lithium-ion Battery Models",
        Chen et al., J. of the Electrochemical Society, 2020 Vol. 167

        Parameters
        ----------
        x : float
            Lithium intercalation fraction at ``r = R_s`` [-].

        Returns
        -------
        Eeq : float
            Equilibrium potential [V].

        """
        Eeq = -0.8090*x + 4.4875 - 0.0428 * np.tanh(18.5138*(x-0.5542)) \
              - 17.7326 * np.tanh(15.7890*(x-0.3117)) \
              + 17.5842*np.tanh(15.9308*(x-0.3120))

        return Eeq

    def get_Mhyst(self, x: float | np.ndarray) -> float | np.ndarray:
        """
        Calculate the hysteresis magnitude given the surface intercalation
        fraction ``x`` at the particle surface.

        Parameters
        ----------
        x : float | 1D array
            Lithium intercalation fraction at ``r = R_s`` [-].

        Returns
        -------
        M_hyst : float | 1D array
            Hysteresis magnitude [V].

        """
        M_hyst = 0.03
        if isinstance(x, np.ndarray):
            M_hyst *= np.ones_like(x)

        return M_hyst
