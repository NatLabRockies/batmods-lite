"""
Post-processing Utilities Module
--------------------------------
This module contains all post-processing functions for the P2D package. The
available post-processing options for a given experiment are specific to that
experiment. Therefore, not all ``Solution`` classes may have access to all of
the following functions.
"""

from numpy import ndarray as _ndarray


def contour(ax: object, xlim: list[float], ylim: list[float], z: _ndarray,
            label: str) -> None:

    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    ax.set_xticks([])

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='10%', pad=0.2)
    cax.tick_params(direction='in')

    cmap = plt.cm.viridis

    im = ax.imshow(z, cmap=cmap, aspect='auto', vmin=z.min(), vmax=z.max(),
                   extent=[xlim[0], xlim[1], ylim[1], ylim[0]],
                   interpolation='nearest')

    fig = ax.get_figure()

    cbar = fig.colorbar(im, cax=cax)
    cbar.set_label(label)


def debug(sol: object) -> None:
    import matplotlib.pyplot as plt

    from .. import format_ax

    # Pull sim from sol
    sim = sol._sim

    # Get needed domains
    an, sep, ca = sim.an, sim.sep, sim.ca

    # Time variation in each variable
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5,3.5])

    ax.set_xlabel(r'$t$ [s]')
    ax.set_ylabel('Variables [units]')

    ax.plot(sol.t, sol.y)

    format_ax(ax)
    if 'inline' not in plt.get_backend():
        fig.show()

    # Time variation in anode variables
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=[15,3.5])
    fig.suptitle(r'Time vartiation in anode $x$ variables')

    ax[0].set_ylabel(r'$C_{\rm Li^+}$ [kmol/m$^3$]')
    ax[1].set_ylabel(r'$\Phi_{\rm el}$ [V]')
    ax[2].set_ylabel(r'$\Phi_{\rm ed}$ [mV]')

    ax[0].plot(sol.t, sol.y[:, an.x_ptr('Li_el')])
    ax[1].plot(sol.t, sol.y[:, an.x_ptr('phi_el')])
    ax[2].plot(sol.t, sol.y[:, an.x_ptr('phi_ed')]*1e3)

    for i in range(3):
        ax[i].set_xlabel(r'$t$ [s]')
        format_ax(ax[i])

    if 'inline' not in plt.get_backend():
        fig.show()

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[10,3.5])
    fig.suptitle(r'Time vartiation in anode $r$ variables')

    ind = an.x_ptr('Li_ed')
    ax[0].plot(sol.t, sol.y[:, ind[0]:ind[0]+an.Nr])
    ax[1].plot(sol.t, sol.y[:, ind[-1]:ind[-1]+an.Nr])

    fig.subplots_adjust(wspace=0.3)

    for i in range(2):
        ax[i].set_ylim([0,1])
        ax[i].set_xlabel(r'$t$ [s]')
        ax[i].set_ylabel(r'$X_{\rm Li}$ [$-$]')
        format_ax(ax[i])

    if 'inline' not in plt.get_backend():
        fig.show()

    # Time variation in separator variables
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[10,3.5])
    fig.suptitle(r'Time vartiation in separator $x$ variables')

    ax[0].set_ylabel(r'$C_{\rm Li^+}$ [kmol/m$^3$]')
    ax[1].set_ylabel(r'$\Phi_{\rm el}$ [V]')

    ax[0].plot(sol.t, sol.y[:, sep.x_ptr('Li_el')])
    ax[1].plot(sol.t, sol.y[:, sep.x_ptr('phi_el')])

    fig.subplots_adjust(wspace=0.3)

    for i in range(2):
        ax[i].set_xlabel(r'$t$ [s]')
        format_ax(ax[i])

    if 'inline' not in plt.get_backend():
        fig.show()

    # Time variation in cathode variables
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=[15,3.5])
    fig.suptitle(r'Time vartiation in cathode $x$ variables')

    ax[0].set_ylabel(r'$C_{\rm Li^+}$ [kmol/m$^3$]')
    ax[1].set_ylabel(r'$\Phi_{\rm el}$ [V]')
    ax[2].set_ylabel(r'$\Phi_{\rm ed}$ [V]')

    ax[0].plot(sol.t, sol.y[:, ca.x_ptr('Li_el')])
    ax[1].plot(sol.t, sol.y[:, ca.x_ptr('phi_el')])
    ax[2].plot(sol.t, sol.y[:, ca.x_ptr('phi_ed')])

    fig.subplots_adjust(wspace=0.3)

    for i in range(3):
        ax[i].set_xlabel(r'$t$ [s]')
        format_ax(ax[i])

    if 'inline' not in plt.get_backend():
        fig.show()

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[10,3.5])
    fig.suptitle(r'Time vartiation in cathode $r$ variables')

    ind = ca.x_ptr('Li_ed')
    ax[0].plot(sol.t, sol.y[:, ind[0]:ind[0]+ca.Nr])
    ax[1].plot(sol.t, sol.y[:, ind[-1]:ind[-1]+ca.Nr])

    fig.subplots_adjust(wspace=0.3)

    for i in range(2):
        ax[i].set_ylim([0,1])
        ax[i].set_xlabel(r'$t$ [s]')
        ax[i].set_ylabel(r'$X_{\rm Li}$ [$-$]')
        format_ax(ax[i])

    if 'inline' not in plt.get_backend():
        fig.show()


def post(sol: object) -> dict:
    import numpy as np

    from .dae import residuals

    # Pull sim and exp from sol
    sim, exp = sol._sim, sol._exp

    # Get needed domains
    an, sep, ca = sim.an, sim.sep, sim.ca

    # Extract desired variables for each time
    res = np.zeros_like(sol.y)

    sdot_an = np.zeros([sol.t.size, an.Nx])
    sdot_ca = np.zeros([sol.t.size, ca.Nx])

    sum_ip = np.zeros([sol.t.size, an.Nx+sep.Nx+ca.Nx])
    i_el_x = np.zeros([sol.t.size, an.Nx+sep.Nx+ca.Nx+1])

    # Turn on output from residuals
    sim._flags['post'] = True

    for i, t in enumerate(sol.t):
        sv, svdot = sol.y[i,:], sol.ydot[i,:]

        output = residuals(t, sv, svdot, np.zeros_like(sv), (sim, exp))
        res[i,:], sdot_an[i,:], sdot_ca[i,:], sum_ip[i,:], i_el_x[i,:] = output

    div_i_an = res[:, an.x_ptr('phi_ed')] + res[:, an.x_ptr('phi_el')]
    div_i_sep = res[:, sep.x_ptr('phi_el')]
    div_i_ca = res[:, ca.x_ptr('phi_ed')] + res[:, ca.x_ptr('phi_el')]

    # Turn off output from residuals
    sim._flags['post'] = False

    # Store outputs
    postvars = {}
    postvars['res'] = res

    postvars['div_i_an'] = div_i_an
    postvars['div_i_sep'] = div_i_sep
    postvars['div_i_ca'] = div_i_ca

    postvars['sdot_an'] = sdot_an
    postvars['sdot_ca'] = sdot_ca

    postvars['sum_ip'] = sum_ip
    postvars['i_el_x'] = i_el_x

    return postvars


def verify(sol: object) -> None:
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.colors as clrs

    from .. import Constants, format_ax

    c = Constants()

    # Check for postvars
    if len(sol.postvars) == 0:
        sol.postvars = post(sol)

    postvars = sol.postvars

    # Pull sim and exp from sol
    sim, exp = sol._sim, sol._exp

    # Get needed domains
    el, an, sep, ca = sim.el, sim.an, sim.sep, sim.ca

    # Combine mesh for convenient plotting
    x = np.hstack([an.x, sep.x, ca.x])

    # Pull all times/states
    t, y = sol.t, sol.y

    # Conservation of Li
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=[15,3.5])

    ax[0].set_ylabel(  r'$\int \ \dot{s}_{\rm Li^+} A_{\rm s} F \ {\rm d}x$'
                     + r'$ \ + \ i_{\rm ext}$ [A/m$^2$]')

    ax[1].set_ylabel(  r'$\int \ \epsilon_{\rm el} \ (C_{\rm Li^+}$'
                     + r'$ - C_{\rm Li^+}^0) \ {\rm d}x$ [kmol/m$^3$]')

    ax[2].set_ylabel(  r'$\int \ \dot{s}_{\rm Li^+} A_{\rm s} F \ {\rm d}x$'
                     + r'$ \ - \ i_{\rm ext}$ [A/m$^2$]')

    ax[0].set_title('Anode')
    ax[1].set_title('Electrolyte')
    ax[2].set_title('Cathode')

    sdot_chk_an = postvars['sdot_an']*c.F*an.A_s*(an.xp - an.xm)
    ax[0].plot(t, np.sum(sdot_chk_an, axis=1) + exp['i_ext'])

    Li_el_an  = y[:, an.x_ptr('Li_el')]
    Li_el_sep = y[:, sep.x_ptr('Li_el')]
    Li_el_ca  = y[:, ca.x_ptr('Li_el')]

    eps_Li_x  = np.hstack([an.eps_el*Li_el_an*(an.xp - an.xm),
                           sep.eps_el*Li_el_sep*(sep.xp - sep.xm),
                           ca.eps_el*Li_el_ca*(ca.xp - ca.xm)])

    eps_Li_0  = np.hstack([an.eps_el*el.Li_0*(an.xp - an.xm),
                           sep.eps_el*el.Li_0*(sep.xp - sep.xm),
                           ca.eps_el*el.Li_0*(ca.xp - ca.xm)])

    ax[1].plot(t, np.sum(eps_Li_x - eps_Li_0, axis=1))

    sdot_chk_ca = postvars['sdot_ca']*c.F*ca.A_s*(ca.xp - ca.xm)
    ax[2].plot(t, np.sum(sdot_chk_ca, axis=1) - exp['i_ext'])

    fig.subplots_adjust(wspace=0.3)

    for i in range(3):
        ax[i].set_xlabel(r'$t$ [s]')
        format_ax(ax[i])

    if 'inline' not in plt.get_backend():
        fig.show()

    # Conservation of charge
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=[15,3.5])

    ax[0].set_ylabel(r'$\nabla \cdot (i_{\rm el} + i_{\rm ed})$ [A/m$^3$]')
    ax[1].set_ylabel(r'$\nabla \cdot i_{\rm el}$ [A/m$^3$]')
    ax[2].set_ylabel(r'$\nabla \cdot (i_{\rm el} + i_{\rm ed})$ [A/m$^3$]')

    ax[0].set_title('Anode')
    ax[1].set_title('Separator')
    ax[2].set_title('Cathode')

    ax[0].plot(t, postvars['div_i_an'])
    ax[1].plot(t, postvars['div_i_sep'])
    ax[2].plot(t, postvars['div_i_ca'])

    fig.subplots_adjust(wspace=0.3)

    for i in range(3):
        ax[i].set_xlabel(r'$t$ [s]')
        format_ax(ax[i])

    if 'inline' not in plt.get_backend():
        fig.show()

    # Net current
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[10,3.5])

    if t.max() <= 3600:
        scale = 60
        ax.set_xlabel(r'$t$ [min]')
    else:
        scale = 3600
        ax.set_xlabel(r'$t$ [h]')

    ax.set_xlabel(r'$x$ [$\mu$m]')
    ax.set_ylabel(r'$\sum \ i_{\rm p} - i_{\rm ext}$ [A/m$^2$]')
    ax.set_title('Net current at plus interfaces')

    t_inds = np.ceil(np.linspace(0, t.size-1, 11)).astype(int)
    cmap = plt.get_cmap('jet', len(t_inds))

    for i, it in enumerate(t_inds):
        ax.plot(x*1e6, postvars['sum_ip'][it,:] + exp['i_ext'], color=cmap(i))

    norm = clrs.Normalize(vmin=t.min()/scale, vmax=t.max()/scale)
    sm = plt.cm.ScalarMappable(cmap='jet', norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, ax=ax, ticks=t[t_inds]/scale)

    if t.max() <= 3600:
        cb.set_label(r'$t$ [min]')
    else:
        cb.set_label(r'$t$ [h]')

    ax.set_xlim([0,ca.xp[-1]*1e6])

    ymin, ymax = ax.get_ylim()
    ax.vlines(an.xp[-1]*1e6, 0.95*ymin, 1.05*ymax, 'k', linestyles='dashed')
    ax.vlines(sep.xp[-1]*1e6, 0.95*ymin, 1.05*ymax, 'k', linestyles='dashed')

    format_ax(ax)

    if 'inline' not in plt.get_backend():
        fig.show()


def general(sol: object) -> None:
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.colors as clrs

    from .. import format_ax

    # Pull sim and exp from sol
    sim, exp = sol._sim, sol._exp

    # Get needed domains
    el, an, sep, ca = sim.el, sim.an, sim.sep, sim.ca

    # Combine mesh for convenient plotting
    x = np.hstack([an.x, sep.x, ca.x])

    # Pull all times/states
    t, y = sol.t, sol.y

    # Cell voltage
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[5,3.5])

    phi_cell = y[:, ca.x_ptr('phi_ed')[-1]]

    if t.max() <= 3600:
        scale = 60
        ax.set_xlabel(r'$t$ [min]')
    else:
        scale = 3600
        ax.set_xlabel(r'$t$ [h]')

    ax.set_ylabel(r'$\phi_{\rm ca} - \phi_{\rm an}$ [V]')

    ax.plot(t/scale, phi_cell, 'k')

    if not exp['C_rate'] == 0:
        ax.set_xlim([0, np.ceil(t.max())/scale])
    else:
        ax.set_xlim([0, np.ceil(t.max())/scale])

    ymin, ymax = min(phi_cell), max(phi_cell)
    ax.set_ylim([0.95*ymin, 1.05*ymax])

    format_ax(ax)

    if 'inline' not in plt.get_backend():
        fig.show()

    # Electrolyte-phase Li-ion concentration
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[10,3.5])

    ax.set_xlabel(r'$x$ [$\mu$m]')
    ax.set_ylabel(r'$C_{\rm Li^+}$ [kmol/m$^3$]')

    t_inds = np.ceil(np.linspace(0, t.size-1, 11)).astype(int)
    cmap = plt.get_cmap('jet', len(t_inds))

    ymin, ymax = el.Li_0, el.Li_0
    for i, it in enumerate(t_inds):

        Li_an_el  = y[it, an.x_ptr('Li_el')]
        Li_sep_el = y[it, sep.x_ptr('Li_el')]
        Li_ca_el  = y[it, ca.x_ptr('Li_el')]
        Li_el_x   = np.hstack([Li_an_el, Li_sep_el, Li_ca_el])

        if ymin > np.min(Li_el_x):
            ymin = np.min(Li_el_x)
        if ymax < np.max(Li_el_x):
            ymax = np.max(Li_el_x)

        ax.plot(x*1e6, Li_el_x, color=cmap(i))

    norm = clrs.Normalize(vmin=t.min()/scale, vmax=t.max()/scale)
    sm = plt.cm.ScalarMappable(cmap='jet', norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, ax=ax, ticks=t[t_inds]/scale)

    if t.max() <= 3600:
        cb.set_label(r'$t$ [min]')
    else:
        cb.set_label(r'$t$ [h]')

    ax.set_xlim([0, ca.xp[-1]*1e6])

    ymin = 0.95*ymin
    ymax = 1.05*ymax

    ax.set_ylim([ymin, ymax])
    ax.vlines(an.xp[-1]*1e6, ymin, ymax, 'k', linestyles='dashed')
    ax.vlines(sep.xp[-1]*1e6, ymin, ymax, 'k', linestyles='dashed')

    format_ax(ax)

    if 'inline' not in plt.get_backend():
        fig.show()

    # Elctrolyte- and solid-phase potentials
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[8,3.5])

    phi_an_el  = y[-1, an.x_ptr('phi_el')]
    phi_sep_el = y[-1, sep.x_ptr('phi_el')]
    phi_ca_el  = y[-1, ca.x_ptr('phi_el')]
    phi_el_x   = np.hstack([phi_an_el, phi_sep_el, phi_ca_el])

    phi_an = y[-1, an.x_ptr('phi_ed')]
    phi_ca = y[-1, ca.x_ptr('phi_ed')]

    ax.set_xlabel(r'$x$ [$\mu$m]')
    ax.set_ylabel(r'Potentials [V]')

    ax.plot(an.x*1e6, phi_an, color='C3')
    ax.plot(x*1e6, phi_el_x, color='C0')
    ax.plot(ca.x*1e6, phi_ca, color='C2')

    ax.set_xlim([0,ca.xp[-1]*1e6])

    phi_min = np.min(phi_el_x)
    phi_max = np.max(phi_ca)

    ymin = phi_min - 0.1*(phi_max-phi_min)
    ymax = phi_max + 0.1*(phi_max-phi_min)

    ax.set_ylim([ymin,ymax])
    ax.vlines(an.xp[-1]*1e6, ymin, ymax, 'k', linestyles='dashed')
    ax.vlines(sep.xp[-1]*1e6, ymin, ymax, 'k', linestyles='dashed')

    format_ax(ax)

    if 'inline' not in plt.get_backend():
        fig.show()

    # Solid-phase Li intercalation fracs -- anode first and last particles
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[10,3.5])

    ax[0].set_ylabel(r'$X_{\rm Li}$ [$-$]')
    ax[0].set_title(r'Particle at $x=$ cc/an')

    ax[1].set_title(r'Particle at $x=$ an/sep')

    t_inds = np.ceil(np.linspace(0, t.size-1, 11)).astype(int)
    cmap = plt.get_cmap('jet', len(t_inds))

    for i, it in enumerate(t_inds):
        ind = an.x_ptr('Li_ed')[0]
        Li_an_cc  = y[it, ind:ind+an.Nr]

        ind = an.x_ptr('Li_ed')[-1]
        Li_an_sep = y[it, ind:ind+an.Nr]

        ax[0].plot(an.r*1e6, Li_an_cc, color=cmap(i))
        ax[1].plot(an.r*1e6, Li_an_sep, color=cmap(i))

    norm = clrs.Normalize(vmin=t.min()/scale, vmax=t.max()/scale)
    sm = plt.cm.ScalarMappable(cmap='jet', norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, ax=ax, ticks=t[t_inds]/scale)

    if t.max() <= 3600:
        cb.set_label(r'$t$ [min]')
    else:
        cb.set_label('$t$ [h]')

    for i in range(2):
        ax[i].set_xlabel(r'$r$ [$\mu$m]')
        ax[i].set_xlim([0,an.R_s*1e6])
        ax[i].set_ylim([0,1.05])
        format_ax(ax[i])

    if 'inline' not in plt.get_backend():
        fig.show()

    # Solid-phase Li intercalation fracs -- cathode first and last particles
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=[10,3.5])

    ax[0].set_ylabel(r'$X_{\rm Li}$ [$-$]')
    ax[0].set_title(r'Particle at $x=$ sep/ca')

    ax[1].set_title(r'Particle at $x=$ ca/cc')

    t_inds = np.ceil(np.linspace(0, t.size-1, 11)).astype(int)
    cmap = plt.get_cmap('jet', len(t_inds))

    for i, it in enumerate(t_inds):

        ind = ca.x_ptr('Li_ed')[0]
        Li_ca_sep = y[it, ind:ind+ca.Nr]

        ind = ca.x_ptr('Li_ed')[0]
        Li_ca_cc  = y[it, ind:ind+ca.Nr]

        ax[0].plot(ca.r*1e6, Li_ca_sep, color=cmap(i))
        ax[1].plot(ca.r*1e6, Li_ca_cc, color=cmap(i))

    norm = clrs.Normalize(vmin=t.min()/scale, vmax=t.max()/scale)
    sm = plt.cm.ScalarMappable(cmap='jet', norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, ax=ax, ticks=t[t_inds]/scale)

    if t.max() <= 3600:
        cb.set_label(r'$t$ [min]')
    else:
        cb.set_label('$t$ [h]')

    for i in range(2):
        ax[i].set_xlabel(r'$r$ [$\mu$m]')
        ax[i].set_xlim([0,ca.R_s*1e6])
        ax[i].set_ylim([0,1.05])
        format_ax(ax[i])

    if 'inline' not in plt.get_backend():
        fig.show()


def contours(sol: object) -> None:
    import numpy as np
    import matplotlib.pyplot as plt

    # Check for postvars
    if len(sol.postvars) == 0:
        sol.postvars = post(sol)

    postvars = sol.postvars

    # Pull sim from sol
    sim = sol._sim

    # Get needed domains
    an, sep, ca = sim.an, sim.sep, sim.ca

    # Pull all times/states
    t, y = sol.t, sol.y

    # Make figure
    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=[8,10])

    # Li-ion conc. [kmol/m^3]
    Li_el_an  = y[:, an.x_ptr('Li_el')]
    Li_el_sep = y[:, sep.x_ptr('Li_el')]
    Li_el_ca  = y[:, ca.x_ptr('Li_el')]
    Li_el_x   = np.hstack([Li_el_an, Li_el_sep, Li_el_ca])

    xlim = [an.xm[0]*1e6, ca.xp[-1]*1e6]
    ylim = [t.min(), t.max()]
    z = Li_el_x

    contour(ax[0,0], xlim, ylim, z, r'[kmol/m$^3$]')

    ax[0,0].set_ylabel(r'$t$ [s]')
    ax[0,0].set_title(r'$C_{\rm Li+}$')

    # Electrolyte potential [V]
    phi_el_an  = y[:, an.x_ptr('phi_el')]
    phi_el_sep = y[:, sep.x_ptr('phi_el')]
    phi_el_ca  = y[:, ca.x_ptr('phi_el')]
    phi_el_x   = np.hstack([phi_el_an, phi_el_sep, phi_el_ca])

    xlim = [an.xm[0]*1e6, ca.xp[-1]*1e6]
    ylim = [t.min(), t.max()]
    z = phi_el_x

    contour(ax[0,1], xlim, ylim, z, r'[V]')

    ax[0,1].set_yticks([])
    ax[0,1].set_title(r'$\phi_{\rm el}$')

    # Ionic current [A/m^2]
    xlim = [an.xm[0]*1e6, ca.xp[-1]*1e6]
    ylim = [t.min(), t.max()]
    z = postvars['i_el_x']

    contour(ax[0,2], xlim, ylim, z, r'[A/m$^2$]')

    ax[0,2].set_yticks([])
    ax[0,2].set_title(r'$i_{\rm el}$')

    # Surface conc. for anode [kmol/m^3]
    x_Li_an  = y[:, an.x_ptr('Li_ed', an.Nr-1)]
    Li_ed_an = an.Li_max*x_Li_an

    xlim = [an.x[0]*1e6, an.x[-1]*1e6]
    ylim = [t.min(), t.max()]
    z = Li_ed_an

    contour(ax[1,0], xlim, ylim, z, r'[kmol/m$^3$]')

    ax[1,0].set_ylabel(r'$t$ [s]')
    ax[1,0].set_title(r'$C_{\rm s, an}$')

    # Anode potential [mV]
    phi_ed_an = y[:, an.x_ptr('phi_ed')]

    xlim = [an.x[0]*1e6, an.x[-1]*1e6]
    ylim = [t.min(), t.max()]
    z = phi_ed_an

    contour(ax[1,1], xlim, ylim, z*1e3, r'[mV]')

    ax[1,1].set_yticks([])
    ax[1,1].set_title(r'$\phi_{\rm s, an}$')

    # Faradaic current in anode [kmol/m^2/s]
    xlim = [an.x[0]*1e6, an.x[-1]*1e6]
    ylim = [t.min(), t.max()]
    z = postvars['sdot_an']

    contour(ax[1,2], xlim, ylim, z, r'[kmol/m$^2$/s]')

    ax[1,2].set_yticks([])
    ax[1,2].set_title(r'$j_{\rm Far, an}$')

    # Surface conc. for cathode [kmol/m^3]
    x_Li_ca  = y[:, ca.x_ptr('Li_ed', ca.Nr-1)]
    Li_ed_ca = ca.Li_max*x_Li_ca

    xlim = [ca.x[0]*1e6, ca.x[-1]*1e6]
    ylim = [t.min(), t.max()]
    z = Li_ed_ca

    contour(ax[2,0], xlim, ylim, z, r'[kmol/m$^3$]')

    ax[2,0].set_ylabel(r'$t$ [s]')
    ax[2,0].set_xlabel(r'$x$ [$\mu$m]')
    ax[2,0].set_title(r'$C_{\rm s, ca}$')

    # Cathode potential [V]
    phi_ed_ca = y[:, ca.x_ptr('phi_ed')]

    xlim = [ca.x[0]*1e6, ca.x[-1]*1e6]
    ylim = [t.min(), t.max()]
    z = phi_ed_ca

    contour(ax[2,1], xlim, ylim, z, r'[V]')

    ax[2,1].set_yticks([])
    ax[2,1].set_xlabel(r'$x$ [$\mu$m]')
    ax[2,1].set_title(r'$\phi_{\rm s, ca}$')

    # Faradaic current in cathode [kmol/m^2/s]
    xlim = [ca.x[0]*1e6, ca.x[-1]*1e6]
    ylim = [t.min(), t.max()]
    z = postvars['sdot_ca']

    contour(ax[2,2], xlim, ylim, z, r'[kmol/m$^2$/s]')

    ax[2,2].set_yticks([])
    ax[2,2].set_xlabel(r'$x$ [$\mu$m]')
    ax[2,2].set_title(r'$j_{\rm Far, ca}$')

    # Adjust spacing
    fig.subplots_adjust(wspace=0.7, hspace=0.2)

    if 'inline' not in plt.get_backend():
        fig.show()
