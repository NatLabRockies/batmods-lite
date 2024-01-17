def format_lims(ax: object) -> None:
    """
    Formats an ``axis`` object by adjusting the limits.

    Specifically, sets the x and y limits such that there is 10% white space
    all the way around the perimeter. In the case that x or y is constant, the
    default matplotlib behavior is adopted for the limits on that respective
    variable.

    Parameters
    ----------
    ax : object
        An ``axis`` instance from a ``matplotlib`` figure.

    Returns
    -------
    None.
    """

    for i, line in enumerate(ax.lines):

        x = line.get_xdata()
        y = line.get_ydata()

        if i == 0:
            x_min, x_max = x.min(), x.max()
            y_min, y_max = y.min(), y.max()

        if x.min() < x_min: x_min = x.min()
        if x.max() > x_max: x_max = x.max()

        if y.min() < y_min: y_min = y.min()
        if y.max() > y_max: y_max = y.max()

    dx = abs(x_max - x_min)
    dy = abs(y_max - y_min)

    if dx != 0:
        ax.set_xlim([x_min - 0.1*dx, x_max + 0.1*dx])
    else:
        pass

    if dy != 0:
        ax.set_ylim([y_min - 0.1*dy, y_max + 0.1*dy])
    else:
        pass


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
