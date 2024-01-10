"""
Single Particle Model Package
-----------------------------
A packaged single particle model (SPM). Build a model using the ``Simulation``
class, and run any available experiments using its "run" methods, e.g.
``run_CC()``. The experiments return ``Solution`` class instances with post
processing, plotting, and saving methods.
"""

from . import builder, dae, postutils, solutions


class Simulation(object):
    __slots__ = [
        "_yamlfile",
        "_yamlpath",
        "_flags",
        "bat",
        "el",
        "an",
        "ca",
        "sv_0",
        "svdot_0",
        "lband",
        "uband",
        "algidx",
    ]

    def __init__(self, yamlfile: str = "default_SPM") -> None:
        """
        Make a SPM simulation capable of running various experiments.

        The initialization will add all of the battery attributes from the
        ``.yaml`` file under its ``bat``, ``el``, ``an``, and ``ca``
        attributes. The ``pre()`` method runs at the end of the initialization
        to add dependent parameters, including the mesh, algebraic indices,
        etc. to the simulation instance. This only happens in ``__init__``,
        which has some implications if the user modifies parameters after
        initialization (see the warning below).

        Parameters
        ----------
        yamlfile : str, optional
            An absolute or relative path to the ``.yaml`` file that defines the
            battery properties. The ``.yaml`` extension will be added to the
            end of the string if it is not already there. The default is
            ``'default_SPM'``, which loads an internal file from the ``bmlite``
            library.

        Warning
        -------
        The user may choose to modify parameters after loading in a ``.yaml``
        file, however, they will need to manually re-run the ``pre()`` method
        if they do so. Otherwise, the dependent parameters may not be
        consistent with the user-defined inputs.

        Notes
        -----
        * The ``'default_SPM.yaml'`` file can be accessed via the
          ``templates()`` method. Please reference this for help building your
          own ``.yaml`` file.
        """

        import os
        from pathlib import Path

        from ruamel.yaml import YAML

        from .builder import Battery, Electrode, Electrolyte

        if ".yaml" not in yamlfile:
            yamlfile += ".yaml"

        defaults = os.listdir(os.path.dirname(__file__) + "/default_sims")
        if yamlfile in defaults:
            path = os.path.dirname(__file__) + "/default_sims/" + yamlfile
            print("\n[BatMods WARNING] SPM Simulation: Using a default yaml\n")
            yamlpath = Path(path)

        elif os.path.exists(yamlfile):
            yamlpath = Path(yamlfile)

        self._yamlfile = yamlfile
        self._yamlpath = yamlpath

        yaml = YAML(typ="safe")
        yamldict = yaml.load(yamlpath)

        self.bat = Battery(**yamldict["battery"])
        self.el = Electrolyte(**yamldict["electrolyte"])
        self.an = Electrode(**yamldict["anode"])
        self.ca = Electrode(**yamldict["cathode"])

        # Function output flags
        self._flags = {}
        self._flags["band"] = False
        self._flags["post"] = False

        # Pre process dependent parameters, mesh, etc.
        self.pre()

    def pre(self) -> None:
        """
        Pre-process the dependent parameters.

        The dependent parameters include ``A_s``, ``eps_s``, ``eps_AM``,
        ``sigma_s``, and setting the ``material`` classes for each domain. In
        addition, this method determines the mesh, pointers, algebraic indices,
        bandwidth, and initial solution. ``pre()`` is automatically executed
        in the ``__init__()`` method which has some implications if the user
        modifies parameters after initialization (see the warning below).

        Returns
        -------
        None.

        Warning
        -------
        The user may choose to modify parameters after loading in a ``.yaml``
        file, however, they will need to manually re-run the ``pre()`` method
        if they do so. Otherwise, the dependent parameters may not be
        consistent with the user-defined inputs.
        """

        import numpy as np

        from .dae import bandwidth

        # Update dependent parameters
        self.bat.update()
        self.el.update()
        self.an.update()
        self.ca.update()

        # Make meshes
        self.an.make_mesh()
        self.ca.make_mesh()

        # Make pointers
        self.an.make_ptr()

        self.ca.make_ptr()
        for key, val in self.ca.ptr.items():
            if "shift" not in key and "off" not in key:
                self.ca.ptr[key] += self.an.ptr["shift"]

        self.el.make_ptr()
        for key, val in self.el.ptr.items():
            if "shift" not in key and "off" not in key:
                self.el.ptr[key] += self.an.ptr["shift"] + self.ca.ptr["shift"]

        # Initialize potentials [V]
        self.an.phi_0 = 0.0

        self.el.phi_0 = -self.an.get_Eeq(self.an.x_0, self.bat.temp)

        self.ca.phi_0 = self.ca.get_Eeq(
            self.ca.x_0, self.bat.temp
        ) - self.an.get_Eeq(self.an.x_0, self.bat.temp)

        # Initialize sv and svdot
        self.sv_0 = np.hstack([self.an.sv_0(), self.ca.sv_0(), self.el.sv_0()])

        self.svdot_0 = np.zeros_like(self.sv_0)

        # Algebraic indices
        self.algidx = (
            list(self.an.algidx())
            + list(self.ca.algidx())
            + list(self.el.algidx())
        )

        # Determine the bandwidth
        self.lband, self.uband, _ = bandwidth(self)

    def j_pattern(self) -> None:
        """
        Plot the Jacobian pattern.

        Runs the ``bmlite.SPM.dae.bandwidth`` function to determine and plot
        the Jacobian pattern.

        Returns
        -------
        None.

        See also
        --------
        bmlite.SPM.dae.bandwidth
        """

        import matplotlib.pyplot as plt

        from .. import format_ax
        from .dae import bandwidth

        lband, uband, j_pat = bandwidth(self)

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5, 3.5])

        ax.spy(j_pat)
        ax.text(0.1, 0.2, "lband: " + str(lband), transform=ax.transAxes)
        ax.text(0.1, 0.1, "uband: " + str(uband), transform=ax.transAxes)

        format_ax(ax)

        if "inline" not in plt.get_backend():
            fig.show()

    def run_CC(self, exp: dict, **kwargs) -> object:
        """
        Runs a constant current experiment specified by the details given in
        the experiment dictionary ``exp``.

        Parameters
        ----------
        exp : dict
            The constant current experimental details. Required keys and
            descriptions are listed below:

            =========== ==============================================
            Key         Value [units] (type)
            =========== ==============================================
            C_rate      C-rate (+ charge, - discharge) [1/h] (*float*)
            t_min       minimum time [s] (*float*)
            t_max       maximum time [s] (*float*)
            Nt          number of time discretizations [-] (*int*)
            =========== ==============================================

        **kwargs : dict, optional
            The keyword arguments specify the Sundials IDA solver options. A
            partial list of options/defaults is given below:

            =============== =================================================
            Key             Description (type or options, default)
            =============== =================================================
            rtol            relative tolerance (*float*, 1e-6)
            atol            absolute tolerance (*float*, 1e-9)
            linsolver       linear solver (``{'dense', 'band'}``, ``'band'``)
            lband           width of the lower band (*int*, ``self.lband``)
            uband           width of the upper band (*int*, ``self.uband``)
            max_step_size   maximum time step (*float*, 0. -> unrestricted)
            rootfn          root/event function (*Callable*, ``None``)
            nr_rootfns      number of events in ``'rootfn'`` (*int*, 0)
            =============== =================================================

        Returns
        -------
        sol : CCSolution object
            Solution class with the returned variable values, messages, exit
            flags, etc. from the IDA solver. The returned ``CCSolution``
            instance includes post processing, plotting, and saving methods.

        See also
        --------
        bmlite.IDASolver
        bmlite.SPM.solutions.CCSolution
        """

        import time

        import numpy as np

        from .. import IDASolver
        from .dae import residuals
        from .solutions import CCSolution

        # Area-specific current
        exp["i_ext"] = exp["C_rate"] * self.bat.cap / self.bat.area

        # Solver options
        options = {
            "user_data": (self, exp),
            "linsolver": "band",
            "lband": self.lband,
            "uband": self.uband,
            "algebraic_vars_idx": self.algidx,
        }

        for key, val in kwargs.items():
            options[key] = val

        solver = IDASolver(residuals, **options)

        # Run the simulation
        t_span = np.linspace(exp["t_min"], exp["t_max"], exp["Nt"])

        start = time.time()
        idasol = solver.solve(t_span, self.sv_0, self.svdot_0)
        solvetime = time.time() - start

        sol = CCSolution(self, exp)
        sol.ida_fill(idasol, solvetime)

        return sol


def load(loadname: str) -> tuple[object]:
    """
    Load a previous SPM simulation and solution pair.

    The ``Solution`` classes have a save method that create a directory
    with saved ``.yaml`` and ``.npz`` files which can be used to reconstruct
    the ``sim`` and ``sol`` objects from a previous experiment.

    Parameters
    ----------
    loadname : str
        The absolute or relative path to a directory with previously saved
        solution files.

    Returns
    -------
    sim : SPM Simulation object
        An initialized SPM simulation instance.

    sol : SPM Solution object
        An initialized and filled SPM solution instance. The solution class is
        determined from information in the previously saved ``.yaml`` files.

    See also
    --------
    bmlite.SPM.Simulation
    bmlite.SPM.solutions.BaseSolution.save
    """

    import os
    from pathlib import Path

    import numpy as np
    from ruamel.yaml import YAML

    yaml = YAML()

    loadpath = Path(loadname)

    simfile = [f for f in os.listdir(loadpath) if "_sim.yaml" in f][0]
    simpath = loadname + "/" + simfile

    sim = Simulation(simpath)

    expfile = [f for f in os.listdir(loadpath) if "_exp.yaml" in f][0]
    exppath = loadpath.joinpath(expfile)

    exp = yaml.load(exppath)

    solfile = [f for f in os.listdir(loadpath) if "_sol.yaml" in f][0]
    solpath = loadpath.joinpath(solfile)

    npfile = [f for f in os.listdir(loadpath) if "_sol.npz" in f][0]
    nppath = loadname + "/" + npfile

    soldict = yaml.load(solpath)

    Solution = getattr(solutions, soldict["classname"])
    sol = Solution(sim, exp)

    data = np.load(nppath)
    for k in ["t", "y", "ydot"]:
        soldict[k] = data[k]

    data.close()

    sol.dict_fill(soldict)

    return sim, sol


def templates(sim: str | int = None, exp: str | int = None) -> None:
    """
    Print simulation and/or experiment templates. If both ``sim`` and ``exp``
    are ``None``, a list of available templates will be printed. Otherwise, if
    a name or index is given, that template will print to the console.

    Parameters
    ----------
    sim : str | int, optional
        Simulation template file name or index. The default is ``None``.

    exp : str | int, optional
        Experiment template file name or index. The default is ``None``.

    Returns
    -------
    None.
    """

    import json
    import os
    from pathlib import Path

    from ruamel.yaml import YAML

    dirname = os.path.dirname(__file__)

    simlist = os.listdir(dirname + "/default_sims/")
    explist = os.listdir(dirname + "/default_exps/")

    if sim == None and exp == None:
        print("\nAvailable templates list for SPM simulations:")
        for i, file in enumerate(simlist):
            print("\t- [" + str(i) + "] " + file.removesuffix(".yaml"))

        print("\nAvailable templates list for SPM experiments:")
        for i, file in enumerate(explist):
            print("\t- [" + str(i) + "] " + file.removesuffix(".yaml"))

    if type(sim) == str:
        if ".yaml" not in sim:
            sim += ".yaml"

        print("\n" + "=" * 30 + "\n" + sim + "\n" + "=" * 30)
        file = dirname + "/default_sims/" + sim
        with open(file, "r") as f:
            print("\n" + f.read())

    elif type(sim) == int:
        print("\n" + "=" * 30 + "\n" + simlist[sim] + "\n" + "=" * 30)
        file = dirname + "/default_sims/" + simlist[sim]
        with open(file, "r") as f:
            print("\n" + f.read())

    yaml = YAML()

    if type(exp) == str:
        if ".yaml" not in exp:
            exp += ".yaml"

        print("\n" + "=" * 30 + "\n" + exp + "\n" + "=" * 30)
        file = dirname + "/default_exps/" + exp
        expdict = yaml.load(Path(file))
        print("exp = " + json.dumps(expdict, indent=4))

    elif type(exp) == int:
        print("\n" + "=" * 30 + "\n" + explist[exp] + "\n" + "=" * 30)
        file = dirname + "/default_exps/" + explist[exp]
        expdict = yaml.load(Path(file))
        print("exp = " + json.dumps(expdict, indent=4))
