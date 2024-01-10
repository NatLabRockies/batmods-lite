"""
Post-processing Utilities Module
--------------------------------
This module contains all post-processing functions for the SPM package. The
available post-processing options for a given experiment are specific to that
experiment. Therefore, not all ``Solution`` classes may have access to all of
the following functions.
"""

from numpy import ndarray as _ndarray


def contour(
    ax: object, xlim: list[float], ylim: list[float], z: _ndarray, label: str
) -> None:
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    ax.set_xticks([])

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="10%", pad=0.2)
    cax.tick_params(direction="in")

    cmap = plt.cm.viridis

    im = ax.imshow(
        z,
        cmap=cmap,
        aspect="auto",
        vmin=z.min(),
        vmax=z.max(),
        extent=[xlim[0], xlim[1], ylim[1], ylim[0]],
        interpolation="nearest",
    )

    fig = ax.get_figure()

    cbar = fig.colorbar(im, cax=cax)
    cbar.set_label(label)


def debug(sol: object) -> None:
    import matplotlib.pyplot as plt

    from .. import format_ax

    # Pull sim from sol
    sim = sol._sim

    # Get needed domains
    el, an, ca = sim.el, sim.an, sim.ca

    # Time variation in each variable
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5, 3.5])

    ax.set_xlabel(r"$t$ [s]")
    ax.set_ylabel("Variables [units]")

    ax.plot(sol.t, sol.y)

    format_ax(ax)

    if "inline" not in plt.get_backend():
        fig.show()

    # Time variation in anode variables
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[10, 3.5])
    fig.suptitle(r"Time vartiation in anode variables")

    ax[0].plot(sol.t, sol.y[:, an.r_ptr("Li_ed")])
    ax[1].plot(sol.t, sol.y[:, an.ptr["phi_ed"]])

    fig.subplots_adjust(wspace=0.3)

    ax[0].set_ylabel(r"$X_{\rm Li}$ [$-$]")
    ax[1].set_ylabel(r"$\phi_{\rm an}$ [V]")

    for i in range(2):
        ax[i].set_xlabel(r"$t$ [s]")
        format_ax(ax[i])

    if "inline" not in plt.get_backend():
        fig.show()

    # Time variation in cathode variables
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[10, 3.5])
    fig.suptitle(r"Time vartiation in cathode variables")

    ax[0].plot(sol.t, sol.y[:, ca.r_ptr("Li_ed")])
    ax[1].plot(sol.t, sol.y[:, ca.ptr["phi_ed"]])

    fig.subplots_adjust(wspace=0.3)

    ax[0].set_ylabel(r"$X_{\rm Li}$ [$-$]")
    ax[1].set_ylabel(r"$\phi_{\rm ca}$ [V]")

    for i in range(2):
        ax[i].set_xlabel(r"$t$ [s]")
        format_ax(ax[i])

    if "inline" not in plt.get_backend():
        fig.show()

    # Time variation in electrolyte variables
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5, 3.5])
    fig.suptitle(r"Time vartiation in electrolyte variables")

    ax.set_ylabel(r"$\Phi_{\rm el}$ [V]")
    ax.plot(sol.t, sol.y[:, el.ptr["phi_el"]])

    ax.set_xlabel(r"$t$ [s]")
    format_ax(ax)

    if "inline" not in plt.get_backend():
        fig.show()


def post(sol: object) -> dict:
    import numpy as np

    from .dae import residuals

    # Pull sim and exp from sol
    sim, exp = sol._sim, sol._exp

    # Extract desired variables for each time
    res = np.zeros_like(sol.y)

    sdot_an = np.zeros_like(sol.t)
    sdot_ca = np.zeros_like(sol.t)

    # Turn on output from residuals
    sim._flags["post"] = True

    for i, t in enumerate(sol.t):
        sv, svdot = sol.y[i, :], sol.ydot[i, :]

        output = residuals(t, sv, svdot, np.zeros_like(sv), (sim, exp))
        res[i], sdot_an[i], sdot_ca[i] = output

    # Turn off output from residuals
    sim._flags["post"] = False

    # Store outputs
    postvars = {}
    postvars["res"] = res

    postvars["sdot_an"] = sdot_an
    postvars["sdot_ca"] = sdot_ca

    return postvars


def verify(sol: object) -> None:
    import matplotlib.pyplot as plt

    from .. import Constants, format_ax

    c = Constants()

    # Check for postvars
    if len(sol.postvars) == 0:
        sol.postvars = post(sol)

    postvars = sol.postvars

    # Pull sim and exp from sol
    sim, exp = sol._sim, sol._exp

    # Break inputs into separate objects
    an, ca = sim.an, sim.ca

    # Conservation of Li
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[10, 3.5])

    ax[0].set_ylabel(
        r"$\int \ \dot{s}_{\rm Li^+} A_{\rm s} F \ {\rm d}x$"
        + r"$ \ + \ i_{\rm ext}$ [A/m$^2$]"
    )

    ax[1].set_ylabel(
        r"$\int \ \dot{s}_{\rm Li^+} A_{\rm s} F \ {\rm d}x$"
        + r"$ \ - \ i_{\rm ext}$ [A/m$^2$]"
    )

    ax[0].set_title("Anode")
    ax[1].set_title("Cathode")

    sdot_chk_an = postvars["sdot_an"] * an.A_s * c.F * an.thick
    ax[0].plot(sol.t, sdot_chk_an + exp["i_ext"])

    sdot_chk_ca = postvars["sdot_ca"] * ca.A_s * c.F * ca.thick
    ax[1].plot(sol.t, sdot_chk_ca - exp["i_ext"])

    fig.subplots_adjust(wspace=0.3)

    for i in range(2):
        ax[i].set_xlabel(r"$t$ [s]")
        format_ax(ax[i])

    if "inline" not in plt.get_backend():
        fig.show()


def general(sol: object) -> None:
    import matplotlib.colors as clrs
    import matplotlib.pyplot as plt
    import numpy as np

    from .. import format_ax

    # Pull sim and exp from sol
    sim, exp = sol._sim, sol._exp

    # Break inputs into separate objects
    an, ca = sim.an, sim.ca

    # Pull all times/states
    t, y = sol.t, sol.y

    # Cell voltage
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5, 3.5])

    phi_cell = y[:, ca.ptr["phi_ed"]]

    if t.max() <= 3600:
        scale = 60
        ax.set_xlabel(r"$t$ [min]")
    else:
        scale = 3600
        ax.set_xlabel(r"$t$ [h]")

    ax.set_ylabel(r"$\phi_{\rm ca} - \phi_{\rm an}$ [V]")

    ax.plot(sol.t / scale, phi_cell, "k")

    if not exp["C_rate"] == 0:
        ax.set_xlim([0, np.ceil(1.05 * t.max()) / scale])
    else:
        ax.set_xlim([0, np.ceil(1.05 * t.max()) / scale])

    ymin, ymax = min(phi_cell), max(phi_cell)
    ax.set_ylim([0.95 * ymin, 1.05 * ymax])

    format_ax(ax)

    if "inline" not in plt.get_backend():
        fig.show()

    # Solid-phase Li intercalation fracs -- anode
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5, 3.5])

    ax.set_ylabel(r"$X_{\rm Li}$ [$-$]")
    ax.set_title("Anode particle")

    t_inds = np.ceil(np.linspace(0, t.size - 1, 11)).astype(int)
    cmap = plt.get_cmap("jet", len(t_inds))

    for i, it in enumerate(t_inds):
        Li_an = y[it, an.r_ptr("Li_ed")]
        ax.plot(an.r * 1e6, Li_an, color=cmap(i))

    norm = clrs.Normalize(vmin=t.min() / scale, vmax=t.max() / scale)
    sm = plt.cm.ScalarMappable(cmap="jet", norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, ax=ax, ticks=t[t_inds] / scale)

    if t.max() <= 3600:
        cb.set_label(r"$t$ [min]")
    else:
        cb.set_label("$t$ [h]")

    ax.set_xlabel(r"$r$ [$\mu$m]")
    ax.set_xlim([0, an.R_s * 1e6])
    ax.set_ylim([0, 1.05])
    format_ax(ax)

    if "inline" not in plt.get_backend():
        fig.show()

    # Solid-phase Li intercalation fracs -- cathode
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5, 3.5])

    ax.set_ylabel(r"$X_{\rm Li}$ [$-$]")
    ax.set_title("Cathode particle")

    t_inds = np.ceil(np.linspace(0, t.size - 1, 11)).astype(int)
    cmap = plt.get_cmap("jet", len(t_inds))

    for i, it in enumerate(t_inds):
        Li_ca = y[it, ca.r_ptr("Li_ed")]
        ax.plot(ca.r * 1e6, Li_ca, color=cmap(i))

    norm = clrs.Normalize(vmin=t.min() / scale, vmax=t.max() / scale)
    sm = plt.cm.ScalarMappable(cmap="jet", norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, ax=ax, ticks=t[t_inds] / scale)

    if t.max() <= 3600:
        cb.set_label(r"$t$ [min]")
    else:
        cb.set_label("$t$ [h]")

    ax.set_xlabel(r"$r$ [$\mu$m]")
    ax.set_xlim([0, ca.R_s * 1e6])
    ax.set_ylim([0, 1.05])
    format_ax(ax)

    if "inline" not in plt.get_backend():
        fig.show()


def contours(sol: object) -> None:
    import matplotlib.pyplot as plt

    # Pull sim from sol
    sim = sol._sim

    # Get needed domains
    an, ca = sim.an, sim.ca

    # Pull all times/states
    t, y = sol.t, sol.y

    # Make figure
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[5, 3.5])

    # Li concentrations in anode [kmol/m^3]
    x_Li_an = y[:, an.r_ptr("Li_ed")]
    Li_ed_an = an.Li_max * x_Li_an

    xlim = [an.rm[0] * 1e6, an.rp[-1] * 1e6]
    ylim = [t.min(), t.max()]
    z = Li_ed_an

    contour(ax[0], xlim, ylim, z, r"[kmol/m$^3$]")

    ax[0].set_ylabel(r"$t$ [s]")
    ax[0].set_title(r"$C_{\rm s, an}$")

    # Li concentrations in cathode [kmol/m^3]
    x_Li_ca = y[:, ca.r_ptr("Li_ed")]
    Li_ed_ca = ca.Li_max * x_Li_ca

    xlim = [ca.rm[0] * 1e6, ca.rp[-1] * 1e6]
    ylim = [t.min(), t.max()]
    z = Li_ed_ca

    contour(ax[1], xlim, ylim, z, r"[kmol/m$^3$]")

    ax[1].set_xlabel(r"$x$ [$\mu$m]")
    ax[1].set_title(r"$C_{\rm s, ca}$")

    # Adjust spacing
    fig.subplots_adjust(wspace=0.7, hspace=0.2)

    if "inline" not in plt.get_backend():
        fig.show()
