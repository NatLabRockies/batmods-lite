"""
Post-processing Utilities
-------------------------
This module contains all post-processing functions for the P2D package. The
available post-processing options for a given experiment are specific to that
experiment. Therefore, not all ``Solution`` classes may have access to all of
the following functions.
"""

from numpy import ndarray as _ndarray


def post(sol: object) -> dict:
    """
    Run post processing to determine secondary variables.

    Parameters
    ----------
    sol : P2D Solution object
        A pseudo-2D model solution object.

    Returns
    -------
    postvars : dict
        Post processed variables, as described below.

        =========== ========================================================
        Key         Value [units] (*type*)
        =========== ========================================================
        res         DAE residual at t (row) for y (col) [units] (*2D array*)
        div_i_an    divergence of current at t, x_a [A/m^3] (*2D array*)
        div_i_sep   divergence of current at t, x_s [A/m^3] (*2D array*)
        div_i_ca    divergence of current at t, x_c [A/m^3] (*2D array*)
        sdot_an     Faradaic current at t, x_a [kmol/m^2/s] (*1D array*)
        sdot_ca     Faradaic current at t, x_c [kmol/m^2/s] (*1D array*)
        sum_ip      ``i_ed + i_el`` at t, xp interfaces [A/m^2] (*2D array*)
        i_el_x      ``i_el`` at t, x interfaces [A/m^2] (*2D array*)
        i_ext       external current density at t [A/m^2] (*1D array*)
        A*h/m^2     areal capacity at t [A*h/m^2] (*1D array*)
        =========== ========================================================
    """

    import numpy as np
    from scipy.integrate import cumtrapz

    from .dae import residuals

    # Pull sim and exp from sol
    sim, exp = sol._sim, sol._exp.copy()

    # Get needed domains
    an, sep, ca = sim.an, sim.sep, sim.ca

    # Extract desired variables for each time
    div_i_an = np.zeros([sol.t.size, an.Nx])
    div_i_sep = np.zeros([sol.t.size, sep.Nx])
    div_i_ca = np.zeros([sol.t.size, ca.Nx])

    sdot_an = np.zeros([sol.t.size, an.Nx])
    sdot_ca = np.zeros([sol.t.size, ca.Nx])

    sum_ip = np.zeros([sol.t.size, an.Nx + sep.Nx + ca.Nx])
    i_el_x = np.zeros([sol.t.size, an.Nx + sep.Nx + ca.Nx + 1])

    i_ext = np.zeros_like(sol.t)

    # Turn on output from residuals
    sim._flags['post'] = True

    for i, t in enumerate(sol.t):
        sv, svdot = sol.y[i, :], sol.ydot[i, :]

        output = residuals(t, sv, svdot, np.zeros_like(sv), (sim, exp))

        (div_i_an[i, :], div_i_sep[i, :], div_i_ca[i, :], sdot_an[i, :],
         sdot_ca[i, :], sum_ip[i, :], i_el_x[i, :]) = output

        i_ext[i] = exp['i_ext']

    # Turn off output from residuals
    sim._flags['post'] = False

    # Areal capacity [A*h/m^2]
    cap_m2 = np.abs(np.hstack([0., cumtrapz(i_ext, sol.t / 3600.)]))

    # Store outputs
    postvars = {}

    postvars['div_i_an'] = div_i_an
    postvars['div_i_sep'] = div_i_sep
    postvars['div_i_ca'] = div_i_ca

    postvars['sdot_an'] = sdot_an
    postvars['sdot_ca'] = sdot_ca

    postvars['sum_ip'] = sum_ip
    postvars['i_el_x'] = i_el_x

    postvars['i_ext'] = i_ext
    postvars['A*h/m^2'] = cap_m2

    return postvars


def _liquid_phase_Li(sol: object) -> _ndarray:
    """
    Calculate the liquid-phase lithium vs. time.

    Parameters
    ----------
    sol : SPM Solution object
        A single particle model solution object.

    Returns
    -------
    Li_ed_0 : float
        liquid-phase lithium [kmol/m^2] based on ``el.Li_0``.

    Li_ed_t : 1D array
        Solution's liquid-phase lithium [kmol/m^2] vs. time [s].
    """

    import numpy as np

    el, an, sep, ca = sol._sim.el, sol._sim.an, sol._sim.sep, sol._sim.ca

    # Initial total liquid-phase lithium [kmol/m^2]
    Li_el_0 = np.sum(np.hstack([an.eps_el * el.Li_0 * (an.xp - an.xm),
                                sep.eps_el * el.Li_0 * (sep.xp - sep.xm),
                                ca.eps_el * el.Li_0 * (ca.xp - ca.xm)]))

    # Total liquid-phase lithium [kmol/m^2] vs. time [s]
    Li_an = sol.y[:, an.x_ptr['Li_el']]
    Li_sep = sol.y[:, sep.x_ptr['Li_el']]
    Li_ca = sol.y[:, ca.x_ptr['Li_el']]

    Li_el_t = np.sum(np.hstack([an.eps_el * Li_an * (an.xp - an.xm),
                                sep.eps_el * Li_sep * (sep.xp - sep.xm),
                                ca.eps_el * Li_ca * (ca.xp - ca.xm)]), axis=1)

    return Li_el_0, Li_el_t


def _solid_phase_Li(sol: object) -> _ndarray:
    """
    Calculate the solid-phase lithium vs. time.

    Parameters
    ----------
    sol : SPM Solution object
        A single particle model solution object.

    Returns
    -------
    Li_ed_0 : float
        Solid-phase lithium [kmol/m^2] based on ``an.x_0`` and ``ca.x_0``.

    Li_ed_t : 1D array
        Solution's solid-phase lithium [kmol/m^2] vs. time [s].
    """

    import numpy as np

    an, ca = sol._sim.an, sol._sim.ca

    # Initial total solid-phase lithium [kmol/m^2]
    Li_ed_0 = an.x_0 * an.Li_max * an.eps_AM * an.thick \
            + ca.x_0 * ca.Li_max * ca.eps_AM * ca.thick

    # Anode/cathode lithium [kmol/m^2] vs. time [s]
    V_an = 4 * np.pi * an.R_s**3 / 3
    V_ca = 4 * np.pi * ca.R_s**3 / 3

    cs_a = np.zeros([sol.t.size, an.Nx, an.Nr])
    cs_c = np.zeros([sol.t.size, ca.Nx, ca.Nr])
    for i in range(sol.t.size):
        xs_a = sol.y[i, an.xr_ptr['Li_ed'].flatten()]
        cs_a[i, :, :] = xs_a.reshape([an.Nx, an.Nr]) * an.Li_max

        xs_c = sol.y[i, ca.xr_ptr['Li_ed'].flatten()]
        cs_c[i, :, :] = xs_c.reshape([ca.Nx, ca.Nr]) * ca.Li_max

    Li_an = np.zeros_like(sol.t)
    Li_ca = np.zeros_like(sol.t)

    for i in range(sol.t.size):

        Li_ed_xr = cs_a[i, :, :]
        Li_ed_x = np.sum(4 * np.pi * an.r**2 * Li_ed_xr * (an.rp - an.rm),
                         axis=1) / V_an

        Li_an[i] = np.sum(an.eps_AM * Li_ed_x * (an.xp - an.xm))

        Li_ed_xr = cs_c[i, :, :]
        Li_ed_x = np.sum(4 * np.pi * ca.r**2 * Li_ed_xr * (ca.rp - ca.rm),
                         axis=1) / V_ca

        Li_ca[i] = np.sum(ca.eps_AM * Li_ed_x * (ca.xp - ca.xm))

    # Total solid-phase lithium [kmol/m^2] vs. time [s]
    Li_ed_t = Li_an + Li_ca

    return Li_ed_0, Li_ed_t


def current(sol: object, ax: object = None) -> None:
    """
    Plot current density vs. time.

    Parameters
    ----------
    sol : P2D Solution object
        A pseudo-2D model solution object.

    ax : object, optional
        An ``axis`` instance from a ``matplotlib`` figure. The default is
        ``None``. If not specified, a new figure is made.

    Returns
    -------
    None.
    """

    import matplotlib.pyplot as plt

    from ..plotutils import format_ticks, show

    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[4, 3],
                               layout='constrained')

    ax.set_xlabel(r'$t$ [s]')
    ax.set_ylabel(r'$i_{\rm ext}$ [A/m$^2$]')

    ax.plot(sol.t, sol.postvars['i_ext'], '-k')
    format_ticks(ax)

    if ax is None:
        show(fig)


def voltage(sol: object, ax: object = None) -> None:
    """
    Plot cell voltage vs. time.

    Parameters
    ----------
    sol : P2D Solution object
        A pseudo-2D model solution object.

    ax : object, optional
        An ``axis`` instance from a ``matplotlib`` figure. The default is
        ``None``. If not specified, a new figure is made.

    Returns
    -------
    None.
    """

    import matplotlib.pyplot as plt

    from ..plotutils import format_ticks, show

    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[4, 3],
                               layout='constrained')

    ax.set_xlabel(r'$t$ [s]')
    ax.set_ylabel(r'$\phi_{\rm ca} - \phi_{\rm an}$ [V]')

    sim = sol._sim

    ax.plot(sol.t, sol.y[:, sim.ca.x_ptr['phi_ed'][-1]], '-k')
    format_ticks(ax)

    if ax is None:
        show(fig)


def power(sol: object, ax: object = None) -> None:
    """
    Plot power density vs. time.

    Parameters
    ----------
    sol : P2D Solution object
        A pseudo-2D model solution object.

    ax : object, optional
        An ``axis`` instance from a ``matplotlib`` figure. The default is
        ``None``. If not specified, a new figure is made.

    Returns
    -------
    None.
    """

    import matplotlib.pyplot as plt

    from ..plotutils import format_ticks, show

    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[4, 3],
                               layout='constrained')

    ax.set_xlabel(r'$t$ [s]')
    ax.set_ylabel(r'$p_{\rm ext}$ [W/m$^2$]')

    sim = sol._sim

    i_ext = sol.postvars['i_ext']
    V_cell = sol.y[:, sim.ca.x_ptr['phi_ed'][-1]]

    ax.plot(sol.t, i_ext * V_cell, '-k')
    format_ticks(ax)

    if ax is None:
        show(fig)


def ivp(sol: object) -> None:
    """
    Subplots for current, voltage, and power.

    Parameters
    ----------
    sol : P2D Solution object
        A pseudo-2D model solution object.

    Returns
    -------
    None.
    """

    import matplotlib.pyplot as plt

    from ..plotutils import show

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=[12, 3],
                           layout='constrained')

    current(sol, ax[0])
    voltage(sol, ax[1])
    power(sol, ax[2])

    fig.get_layout_engine().set(wspace=0.1)
    show(fig)


def potentials(sol: object) -> None:
    """
    Plots anode, electrolyte, and cathode potentials vs. time and space.

    Parameters
    ----------
    sol : P2D Solution object
        A pseudo-2D model solution object.

    Returns
    -------
    None.
    """

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.colors as clrs

    from ..plotutils import format_ticks, show

    an, sep, ca = sol._sim.an, sol._sim.sep, sol._sim.ca

    # Pull time indices and setup colorbar
    t_inds = np.ceil(np.linspace(0, sol.t.size - 1, 11)).astype(int)

    norm = clrs.Normalize(vmin=sol.t.min(), vmax=sol.t.max())
    sm = plt.cm.ScalarMappable(cmap='Greys', norm=norm)

    # Phase potentials [V] vs. time [s]
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[8, 3],
                           layout='constrained')

    cmap = plt.get_cmap('Reds', len(t_inds))
    for i, it in enumerate(t_inds):
        if it != t_inds[-4]:
            label = '__nolabel'
        else:
            label = r'$\phi_{\rm an}$'

        ax.plot(an.x * 1e6, sol.y[it, an.x_ptr['phi_ed']], color=cmap(i),
                label=label)

    x_el = np.hstack([an.x, sep.x, ca.x])
    phi_el = np.hstack([sol.y[:, an.x_ptr['phi_el']],
                        sol.y[:, sep.x_ptr['phi_el']],
                        sol.y[:, ca.x_ptr['phi_el']]])

    cmap = plt.get_cmap('Blues', len(t_inds))
    for i, it in enumerate(t_inds):
        if it != t_inds[-4]:
            label = '__nolabel'
        else:
            label = r'$\phi_{\rm el}$'

        ax.plot(x_el * 1e6, phi_el[it, :], color=cmap(i), label=label)

    cmap = plt.get_cmap('Greens', len(t_inds))
    for i, it in enumerate(t_inds):
        if it != t_inds[-4]:
            label = '__nolabel'
        else:
            label = r'$\phi_{\rm ca}$'

        ax.plot(ca.x * 1e6, sol.y[it, ca.x_ptr['phi_ed']], color=cmap(i),
                label=label)

    cb = plt.colorbar(sm, ax=ax, ticks=sol.t[t_inds])
    cb.set_label(r'$t$ [s]')

    ax.set_xlabel(r'$x$ [$\mu$m]')
    ax.set_ylabel(r'Potentials [V]')

    ax.legend(loc='upper left', frameon=False, borderpad=2)

    ax.set_xlim([0., ca.xp[-1] * 1e6])

    ylims = ax.get_ylim()
    ax.set_ylim(ylims)

    ax.vlines(sep.xm[0] * 1e6, ylims[0], ylims[1], 'k', linestyles='--')
    ax.vlines(sep.xp[-1] * 1e6, ylims[0], ylims[1], 'k', linestyles='--')

    format_ticks(ax)
    show(fig)


def electrolyte(sol: object) -> None:
    """
    Plots electrolyte Li-ion concentration profiles vs. time.

    Parameters
    ----------
    sol : P2D Solution object
        A pseudo-2D model solution object.

    Returns
    -------
    None.
    """

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.colors as clrs

    from ..plotutils import format_ticks, show

    an, sep, ca = sol._sim.an, sol._sim.sep, sol._sim.ca

    # Pull time indices and setup colorbar
    t_inds = np.ceil(np.linspace(0, sol.t.size - 1, 11)).astype(int)
    cmap = plt.get_cmap('jet', len(t_inds))

    norm = clrs.Normalize(vmin=sol.t.min(), vmax=sol.t.max())
    sm = plt.cm.ScalarMappable(cmap='jet', norm=norm)

    # Electrolyte-phase Li-ion concentration [kmol/m^3]
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[8, 3],
                           layout='constrained')

    x_el = np.hstack([an.x, sep.x, ca.x])

    Li_el = np.hstack([sol.y[:, an.x_ptr['Li_el']],
                       sol.y[:, sep.x_ptr['Li_el']],
                       sol.y[:, ca.x_ptr['Li_el']]])

    for i, it in enumerate(t_inds):
        ax.plot(x_el * 1e6, Li_el[it, :], color=cmap(i))

    cb = plt.colorbar(sm, ax=ax, ticks=sol.t[t_inds])
    cb.set_label(r'$t$ [s]')

    ax.set_xlabel(r'$x$ [$\mu$m]')
    ax.set_ylabel(r'$C_{\rm Li^+}$ [kmol/m$^3$]')

    ax.set_xlim([0., ca.xp[-1] * 1e6])

    ylims = ax.get_ylim()
    ax.set_ylim(ylims)

    ax.vlines(sep.xm[0] * 1e6, ylims[0], ylims[1], 'k', linestyles='--')
    ax.vlines(sep.xp[-1] * 1e6, ylims[0], ylims[1], 'k', linestyles='--')

    format_ticks(ax)
    show(fig)


def intercalation(sol: object) -> None:
    """
    Plots anode and cathode particle intercalation profiles vs. time.

    Parameters
    ----------
    sol : P2D Solution object
        A pseudo-2D model solution object.

    Returns
    -------
    None.
    """

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.colors as clrs

    from ..plotutils import format_ticks, show

    an, ca = sol._sim.an, sol._sim.ca

    # Pull time indices and setup colorbar
    t_inds = np.ceil(np.linspace(0, sol.t.size - 1, 11)).astype(int)
    cmap = plt.get_cmap('jet', len(t_inds))

    norm = clrs.Normalize(vmin=sol.t.min(), vmax=sol.t.max())
    sm = plt.cm.ScalarMappable(cmap='jet', norm=norm)

    # Solid-phase Li intercalation fracs [-]
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=[8, 6],
                           layout='constrained')

    ax[0, 0].text(0.1, 0.1, r'$x$ = an/sep', transform=ax[0, 0].transAxes)
    ax[0, 1].text(0.1, 0.1, r'$x$ = sep/ca', transform=ax[0, 1].transAxes)
    ax[1, 0].text(0.1, 0.1, r'$x$ = cc/an', transform=ax[1, 0].transAxes)
    ax[1, 1].text(0.1, 0.1, r'$x$ = ca/cc', transform=ax[1, 1].transAxes)

    for i, it in enumerate(t_inds):
        ax[0, 0].plot(an.r * 1e6, sol.y[it, an.xr_ptr['Li_ed'][-1, :]],
                      color=cmap(i))

        ax[0, 1].plot(ca.r * 1e6, sol.y[it, ca.xr_ptr['Li_ed'][0, :]],
                      color=cmap(i))

        ax[1, 0].plot(an.r * 1e6, sol.y[it, an.xr_ptr['Li_ed'][0, :]],
                      color=cmap(i))

        ax[1, 1].plot(ca.r * 1e6, sol.y[it, ca.xr_ptr['Li_ed'][-1, :]],
                      color=cmap(i))

    cax = ax.ravel().tolist()
    cb = plt.colorbar(sm, ax=cax, ticks=sol.t[t_inds], aspect=50)
    cb.set_label(r'$t$ [s]')

    for i in range(2):
        ax[i, 0].set_ylabel(r'$X_{\rm Li}$ [$-$]')
        ax[i, 1].set_yticklabels([])

    for j in range(2):
        ax[0, j].set_xticklabels([])
        ax[1, j].set_xlabel(r'$r$ [$\mu$m]')

    for i in range(2):
        for j in range(2):
            ax[i, j].set_ylim([0., 1.05])
            format_ticks(ax[i, j])

    show(fig)


def pixels(sol: object) -> None:
    """
    Makes pixel plots for most 2D (space/time) variables.

    Parameters
    ----------
    sol : P2D Solution object
        A pseudo-2D model solution object.

    Returns
    -------
    None.
    """

    import numpy as np
    import matplotlib.pyplot as plt

    from ..plotutils import pixel, show

    # Get needed domains
    an, sep, ca = sol._sim.an, sol._sim.sep, sol._sim.ca

    # Make figure
    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=[8, 10],
                           layout='constrained')

    # Li-ion conc. [kmol/m^3]
    xlims = [an.xm[0] * 1e6, ca.xp[-1] * 1e6]
    ylims = [sol.t.min(), sol.t.max()]
    z = np.hstack([sol.y[:, an.x_ptr['Li_el']],
                   sol.y[:, sep.x_ptr['Li_el']],
                   sol.y[:, ca.x_ptr['Li_el']]])

    pixel(ax[0, 0], xlims, ylims, z, r'[kmol/m$^3$]')

    ax[0, 0].set_ylabel(r'$t$ [s]')
    ax[0, 0].set_title(r'$C_{\rm Li+}$')

    # Electrolyte potential [V]
    xlims = [an.xm[0] * 1e6, ca.xp[-1] * 1e6]
    ylims = [sol.t.min(), sol.t.max()]
    z = np.hstack([sol.y[:, an.x_ptr['phi_el']],
                   sol.y[:, sep.x_ptr['phi_el']],
                   sol.y[:, ca.x_ptr['phi_el']]])

    pixel(ax[0, 1], xlims, ylims, z, r'[V]')

    ax[0, 1].set_yticks([])
    ax[0, 1].set_title(r'$\phi_{\rm el}$')

    # Ionic current [A/m^2]
    xlims = [an.xm[0] * 1e6, ca.xp[-1] * 1e6]
    ylims = [sol.t.min(), sol.t.max()]
    z = sol.postvars['i_el_x']

    pixel(ax[0, 2], xlims, ylims, z, r'[A/m$^2$]')

    ax[0, 2].set_yticks([])
    ax[0, 2].set_title(r'$i_{\rm el}$')

    # Surface conc. for anode [kmol/m^3]
    xlims = [an.x[0] * 1e6, an.x[-1] * 1e6]
    ylims = [sol.t.min(), sol.t.max()]
    z = sol.y[:, an.xr_ptr['Li_ed'][:, -1]] * an.Li_max

    pixel(ax[1, 0], xlims, ylims, z, r'[kmol/m$^3$]')

    ax[1, 0].set_ylabel(r'$t$ [s]')
    ax[1, 0].set_title(r'$C_{\rm s, an}$')

    # Anode potential [mV]
    xlims = [an.x[0] * 1e6, an.x[-1] * 1e6]
    ylims = [sol.t.min(), sol.t.max()]
    z = sol.y[:, an.x_ptr['phi_ed']]

    pixel(ax[1, 1], xlims, ylims, z * 1e3, r'[mV]')

    ax[1, 1].set_yticks([])
    ax[1, 1].set_title(r'$\phi_{\rm s, an}$')

    # Faradaic current in anode [kmol/m^2/s]
    xlims = [an.x[0] * 1e6, an.x[-1] * 1e6]
    ylims = [sol.t.min(), sol.t.max()]
    z = sol.postvars['sdot_an']

    pixel(ax[1, 2], xlims, ylims, z, r'[kmol/m$^2$/s]')

    ax[1, 2].set_yticks([])
    ax[1, 2].set_title(r'$j_{\rm Far, an}$')

    # Surface conc. for cathode [kmol/m^3]
    xlims = [ca.x[0] * 1e6, ca.x[-1] * 1e6]
    ylims = [sol.t.min(), sol.t.max()]
    z = sol.y[:, ca.xr_ptr['Li_ed'][:, -1]] * ca.Li_max

    pixel(ax[2, 0], xlims, ylims, z, r'[kmol/m$^3$]')

    ax[2, 0].set_ylabel(r'$t$ [s]')
    ax[2, 0].set_xlabel(r'$x$ [$\mu$m]')
    ax[2, 0].set_title(r'$C_{\rm s, ca}$')

    # Cathode potential [V]
    xlims = [ca.x[0] * 1e6, ca.x[-1] * 1e6]
    ylims = [sol.t.min(), sol.t.max()]
    z = sol.y[:, ca.x_ptr['phi_ed']]

    pixel(ax[2, 1], xlims, ylims, z, r'[V]')

    ax[2, 1].set_yticks([])
    ax[2, 1].set_xlabel(r'$x$ [$\mu$m]')
    ax[2, 1].set_title(r'$\phi_{\rm s, ca}$')

    # Faradaic current in cathode [kmol/m^2/s]
    xlims = [ca.x[0] * 1e6, ca.x[-1] * 1e6]
    ylims = [sol.t.min(), sol.t.max()]
    z = sol.postvars['sdot_ca']

    pixel(ax[2, 2], xlims, ylims, z, r'[kmol/m$^2$/s]')

    ax[2, 2].set_yticks([])
    ax[2, 2].set_xlabel(r'$x$ [$\mu$m]')
    ax[2, 2].set_title(r'$j_{\rm Far, ca}$')

    # Adjust spacing
    fig.get_layout_engine().set(hspace=0.1, wspace=0.1)
    show(fig)
