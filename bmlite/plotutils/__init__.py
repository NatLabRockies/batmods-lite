"""
BatMods-lite Plotting Utilities
-------------------------------
"""


def show(fig: object) -> None:
    import matplotlib as mpl

    if 'inline' not in mpl.get_backend():
        fig.show()


def format_ticks(ax: object) -> None:
    """
    Formats an ``axis`` object by adjusting the ticks.

    Specifically, the top and right ticks are added, minor ticks are turned on,
    and all ticks are set to face inward.

    Parameters
    ----------
    ax : object
        An ``axis`` instance from a ``matplotlib`` figure.

    Returns
    -------
    None.
    """

    from matplotlib.ticker import AutoMinorLocator

    if ax.get_xaxis().get_scale() != 'log':
        ax.xaxis.set_minor_locator(AutoMinorLocator())

    if ax.get_yaxis().get_scale() != 'log':
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    ax.tick_params(axis='x', top=True, which='both', direction='in')
    ax.tick_params(axis='y', right=True, which='both', direction='in')
