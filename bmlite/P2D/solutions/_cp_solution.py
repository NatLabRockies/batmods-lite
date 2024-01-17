from ._base_solution import BaseSolution


class CPSolution(BaseSolution):
    """
    Constant power solution for P2D simuations.

    Base: :class:`~bmlite.P2D.solutions.BaseSolution`
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

        if 'verify' in args or 'all' in args:
            from ..postutils import verify
            verify(self)

        if 'general' in args or 'all' in args:
            from ..postutils import general
            general(self)

        if 'contours' in args or 'all' in args:
            from ..postutils import contours
            contours(self)

    def slice_and_save(self, savename: str, overwrite: bool = False) -> None:
        """
        Save a ``.npz`` file with all spatial, time, and state variables
        separated into 1D, 2D, and 3D arrays. The keys are given below.
        The index order of the 2D and 3D arrays is given with the value
        descriptions.

        ========= ==========================================================
        Key       Value [units] (type)
        ========= ==========================================================
        x_a       x mesh in anode [m] (1D array)
        x_s       x mesh in separator [m] (1D array)
        x_c       x mesh in cathode [m] (1D array)
        x         stacked x mesh for an, sep, and ca [m] (1D array)
        r_a       r mesh for anode particles [m] (1D array)
        r_c       r mesh for cathode particles [m] (1D array)
        t         saved solution times [s] (1D array)
        phie_a    electrolyte potentials at t, x_a [V] (2D array)
        phis_a    electrode potentials at t, x_a [V] (2D array)
        ce_a      electrolyte Li+ at t, x_a [kmol/m^3] (2D array)
        cs_a      electrode Li at t, x_a, r_a [kmol/m^3] (3D array)
        phie_s    electrolyte potentials at t, x_s [V] (2D array)
        ce_s      electrolyte Li+ at t, x_s [kmol/m^3] (2D array)
        phie_c    electrolyte potentials at t, x_c [V] (2D array)
        phis_c    electrode potentials at t, x_c [V] (2D array)
        ce_c      electrolyte Li+ at t, x_c [kmol/m^3] (2D array)
        cs_c      electrode Li at t, x_c, r_c [kmol/m^3] (3D array)
        phie      electrolyte potentials at t, x [V] (2D array)
        ce        electrolyte Li+ at t, x [kmol/m^3] (2D array)
        ie        electrolyte current at t, x boundarys [A/m^2] (2D array)
        j_a       anode Faradaic current at t, x_a [kmol/m^2/s] (2D array)
        j_c       cathode Faradaic current at t, x_c [kmol/m^2/s] (2D array)
        ========= ==========================================================

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

        x_a = sim.an.x
        x_s = sim.sep.x
        x_c = sim.ca.x

        x = np.hstack([x_a, x_s, x_c])

        r_a = sim.an.r
        r_c = sim.ca.r

        t = self.t

        phie_a = self.y[:, sim.an.x_ptr('phi_el')]
        phis_a = self.y[:, sim.an.x_ptr('phi_ed')]
        ce_a = self.y[:, sim.an.x_ptr('Li_el')]

        phie_s = self.y[:, sim.sep.x_ptr('phi_el')]
        ce_s = self.y[:, sim.sep.x_ptr('Li_el')]

        phie_c = self.y[:, sim.ca.x_ptr('phi_el')]
        phis_c = self.y[:, sim.ca.x_ptr('phi_ed')]
        ce_c = self.y[:, sim.ca.x_ptr('Li_el')]

        phie = np.hstack([phie_a, phie_s, phie_c])
        ce = np.hstack([ce_a, ce_s, ce_c])

        cs_a = np.zeros([t.size, x_a.size, sim.an.Nr])
        for k in range(sim.an.Nr):
            cs_a[:,:,k] = self.y[:, sim.an.x_ptr('Li_ed', k)]*sim.an.Li_max

        cs_c = np.zeros([t.size, x_c.size, sim.ca.Nr])
        for k in range(sim.ca.Nr):
            cs_c[:,:,k] = self.y[:, sim.ca.x_ptr('Li_ed', k)]*sim.ca.Li_max

        ie = self.postvars['i_el_x']
        j_a = self.postvars['sdot_an']
        j_c = self.postvars['sdot_ca']

        np.savez(savename, x_a=x_a, x_s=x_s, x_c=x_c, x=x, r_a=r_a,
                 r_c=r_c, t=t, phie_a=phie_a, phis_a=phis_a, ce_a=ce_a,
                 phie_s=phie_s, ce_s=ce_s, phie_c=phie_c, phis_c=phis_c,
                 ce_c=ce_c, phie=phie, ce=ce, cs_a=cs_a, cs_c=cs_c,
                 ie=ie, j_a=j_a, j_c=j_c)
