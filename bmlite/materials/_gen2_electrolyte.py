from numpy import ndarray as _ndarray


class Gen2Electrolyte(object):

    def __init__(self) -> None:
        """
        Gen 2 Electrolyte transport and material properties.
        """
        pass

    def get_D(self, C_Li: float | _ndarray, T: float) -> float | _ndarray:
        """
        Calculate the lithium ion diffusivity in the electrolyte solution at
        concentration ``C_Li`` and temperature ``T``.

        Parameters
        ----------
        C_Li : float | 1D array
            Lithium ion concentration in the electrolyte [kmol/m^3].

        T : float
            Battery temperature [K].

        Returns
        -------
        D : float | 1D array
            Lithium ion diffusivity in the electrolyte [m^2/s].
        """

        D = 0.0001*10**(
            (-0.568822600 - 1607.003/( T-(-24.83763+64.07366*C_Li) ))      \
          + (-0.810872100 +  475.291/( T-(-24.83763+64.07366*C_Li) ))*C_Li \
          + (-0.005192312 - 33.43827/( T-(-24.83763+64.07366*C_Li) ))*C_Li**2 )

        return D

    def get_t0(self, C_Li: float | _ndarray, T: float) -> float | _ndarray:
        """
        Calculate the lithium ion transference number at concentration ``C_Li``
        and temperature ``T``.

        Parameters
        ----------
        C_Li : float | 1D array
            Lithium ion concentration in the electrolyte [kmol/m^3].

        T : float
            Battery temperature [K].

        Returns
        -------
        t0 : float | 1D array
            Lithium ion transference number [-].
        """

        t0 = (-0.0000002876102*T**2 + 0.0002077407*T - 0.03881203 )*C_Li**2 \
           + ( 0.0000011614630*T**2 - 0.0008682500*T + 0.17772660 )*C_Li    \
           + (-0.0000006766258*T**2 + 0.0006389189*T + 0.30917610 )

        return t0

    def get_kappa(self, C_Li: float | _ndarray, T: float) -> float | _ndarray:
        """
        Calculate the electrolyte conductivity at concentration ``C_Li`` and
        temperature ``T``.

        Parameters
        ----------
        C_Li : float | 1D array
            Lithium ion concentration in the electrolyte [kmol/m^3].

        T : float
            Battery temperature [K].

        Returns
        -------
        kappa : float | 1D array
            Electrolyte conductivity [S/m].
        """

        import numpy as np

        A = np.array([
        [           0.,           0.,  1.909446e-4, -8.038545e-2,  9.003410e+0],
        [-2.8875870e-8,  3.483638e-5, -1.583677e-2,  3.195295e+0, -2.414638e+2],
        [ 1.6537860e-8, -1.998760e-5,  9.071155e-3, -1.828064e+0,  1.380976e+2],
        [-2.7919650e-9,  3.377143e-6, -1.532707e-3,  3.090003e-1, -2.335671e+1]])

        kappa = \
          (A[0,0]*T**4 + A[0,1]*T**3 + A[0,2]*T**2 + A[0,3]*T + A[0,4])*C_Li**1 \
        + (A[1,0]*T**4 + A[1,1]*T**3 + A[1,2]*T**2 + A[1,3]*T + A[1,4])*C_Li**2 \
        + (A[2,0]*T**4 + A[2,1]*T**3 + A[2,2]*T**2 + A[2,3]*T + A[2,4])*C_Li**3 \
        + (A[3,0]*T**4 + A[3,1]*T**3 + A[3,2]*T**2 + A[3,3]*T + A[3,4])*C_Li**4

        return kappa

    def get_gamma(self, C_Li: float | _ndarray, T: float) -> float | _ndarray:
        """
        Calculate the electrolyte thermodynamic factor at concentration
        ``C_Li`` and temperature ``T``.

        Parameters
        ----------
        C_Li : float | 1D array
            Lithium ion concentration in the electrolyte [kmol/m^3].

        T : float
            Battery temperature [K].

        Returns
        -------
        gamma : float | 1D array
            Thermodynamic factor [-].
        """

        import numpy as np

        gamma = 0.540*np.exp(329/T)*C_Li**2 - 0.00225*np.exp(1360/T)*C_Li \
              + 0.341*np.exp(261/T)

        return gamma
