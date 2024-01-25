from ._base_solution import BaseSolution


class CVSolution(BaseSolution):
    """
    Constant voltage solution for SPM simuations.

    Base: :class:`~bmlite.SPM.solutions.BaseSolution`
    """

    __slots__ = []

    def __init__(self, sim: object, exp: dict) -> None:
        super().__init__(sim, exp)

    @property
    def classname(self) -> str:
        """
        Class name. Overwrites ``BaseSolution``.

        Returns
        -------
        classname : str
            Name of current class.
        """
        return 'CVSolution'

    def verify(self, plotflag: bool = False, rtol: float = 5e-3,
               atol: float = 1e-3) -> bool:
        """
        Verifies the solution is consistent.

        Specifically, for a constant voltage experiment, this method checks
        that the calculated voltage was within tolerance of the boundary
        condition. In addition, the anodic and cathodic Faradaic currents are
        checked against the current at each time step.

        Parameters
        ----------
        plotflag : bool, optional
            A flag to see plots showing the verification calculations. The
            default is ``False``.

        rtol : float, optional
            The relative tolerance for array comparisons. The default is 5e-3.

        atol : float, optional
            The relative tolerance for array comparisons. The default is 1e-3.

        Returns
        -------
        checks : bool
            ``True`` is all checks are satisfied, ``False`` otherwise.
        """

        import numpy as np
        import matplotlib.pyplot as plt

        from ... import Constants
        from ...plotutils import format_ticks, show
        from ..postutils import voltage

        c = Constants()

        if len(self.postvars) == 0:
            self.post()

        sim, exp = self._sim, self._exp

        an, ca = sim.an, sim.ca

        V_ext = exp['V_ext']
        V_mod = self.y[:, ca.ptr['phi_ed']]
        i_mod = self.postvars['i_ext']

        i_an = self.postvars['sdot_an'] * an.A_s * an.thick * c.F
        i_ca = self.postvars['sdot_ca'] * ca.A_s * ca.thick * c.F

        checks = []
        checks.append(np.allclose(V_ext, V_mod, rtol=rtol, atol=atol))
        checks.append(np.allclose(i_mod, -i_an, rtol=rtol, atol=atol))
        checks.append(np.allclose(i_mod, i_ca, rtol=rtol, atol=atol))

        if plotflag:
            fig, ax = plt.subplots(nrows=1, ncols=3, figsize=[12, 3],
                                   layout='constrained')

            voltage(self, ax[0])

            if V_mod.mean() != 0.:
                ylims = np.array([0.995 * V_mod.mean(), 1.005 * V_mod.mean()])
                ax[0].set_ylim([min(ylims), max(ylims)])

            ax[1].set_ylabel(r'$i_{\rm ext} + i_{\rm an}$ [A/m$^2$]')
            ax[2].set_ylabel(r'$i_{\rm ext} - i_{\rm ca}$ [A/m$^2$]')

            ax[1].plot(self.t, i_mod + i_an, '-C3')
            ax[2].plot(self.t, i_mod - i_ca, '-C2')

            ymin = min([ax[i].get_ylim()[0] for i in range(1, 3)])
            ymax = max([ax[i].get_ylim()[1] for i in range(1, 3)])

            for i in range(1, 3):
                ax[i].set_ylim([ymin, ymax])
                ax[i].set_xlabel(r'$t$ [s]')
                format_ticks(ax[i])

            fig.get_layout_engine().set(wspace=0.1)
            show(fig)

        return self.success and all(checks)
