from ._base_solution import BaseSolution


class CPSolution(BaseSolution):
    """
    Constant power solution for SPM simuations.

    Base: :class:`~bmlite.SPM.solutions.BaseSolution`
    """

    __slots__ = ['postvars']

    def __init__(self, sim: object, exp: dict) -> None:
        super().__init__(sim, exp)

        self.postvars = {}

    @property
    def classname(self) -> str:
        """
        Class name. Overwrites ``classname()`` from ``BaseSolution``.

        Returns
        -------
        classname : str
            Name of current class.
        """
        return 'CPSolution'

    def post(self) -> None:
        from ..postutils import post

        self._sim._flags['BC'] = 'power'
        self.postvars = post(self)
        self._sim._flags['BC'] = None

    def plot(self, *args) -> None:

        if 'debug' in args or 'all' in args:
            from ..postutils import debug
            debug(self)

        if 'current' in args or 'all' in args:
            from ..postutils import current
            current(self)

        if 'voltage' in args or 'all' in args:
            from ..postutils import voltage
            voltage(self)

        if 'power' in args or 'all' in args:
            from ..postutils import power
            power(self)

    def slice_and_save(self, savename: str, overwrite: bool = False) -> None:
        """
        Save a ``.npz`` file with all spatial, time, and state variables
        separated into 1D and 2D arrays. The keys are given below. The index
        order of the 2D arrays is given with the value descriptions.

        ========= =====================================================
        Key       Value [units] (type)
        ========= =====================================================
        r_a       r mesh for anode particles [m] (1D array)
        r_c       r mesh for cathode particles [m] (1D array)
        t         saved solution times [s] (1D array)
        phis_a    anode electrode potentials at t [V] (1D array)
        cs_a      electrode Li at t, r_a [kmol/m^3] (2D array)
        phis_c    cathode electrode potentials at t [V] (1D array)
        cs_c      electrode Li at t, r_c [kmol/m^3] (2D array)
        phie      electrolyte potentials at t [V] (1D array)
        j_a       anode Faradaic current at t [kmol/m^2/s] (1D array)
        j_c       cathode Faradaic current at t [kmol/m^2/s] (1D array)
        ========= =====================================================

        Parameters
        ----------
        savename : str
            Either a file name or the absolute/relative file path. The ``.npz``
            extension will be added to the end of the string if it is not
            already there. If only the file name is given, the file will be
            saved in the user's current working directory.

        overwrite : bool, optional
            A flag to overwrite and existing ``.npz`` file with the same name
            if one exists. The default is ``False``.

        Returns
        -------
        None.
        """

        import os

        import numpy as np

        if len(self.postvars) == 0:
            self.post()

        if '.npz' not in savename:
            savename += '.npz'

        if os.path.exists(savename) and not overwrite:
            raise Exception('save_and_slice file already exists. Overwrite with'
                            ' flag or delete the file and try again.')

        sim = self._sim

        r_a = sim.an.r
        r_c = sim.ca.r

        t = self.t

        phis_a = self.y[:, sim.an.ptr['phi_ed']]
        phis_c = self.y[:, sim.ca.ptr['phi_ed']]
        phie = self.y[:, sim.el.ptr['phi_el']]

        cs_a = self.y[:, sim.an.r_ptr('Li_ed')]*sim.an.Li_max
        cs_c = self.y[:, sim.ca.r_ptr('Li_ed')]*sim.ca.Li_max

        j_a = self.postvars['sdot_an']
        j_c = self.postvars['sdot_ca']

        np.savez(savename, r_a=r_a, r_c=r_c, t=t, phis_a=phis_a, phie=phie,
                 phis_c=phis_c, cs_a=cs_a, cs_c=cs_c, j_a=j_a, j_c=j_c)
