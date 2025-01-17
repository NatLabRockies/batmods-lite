def templates(sim: str | int = None) -> None:
    """
    Print simulation templates. If ``sim`` is ``None``, a list of available
    templates will be printed. Otherwise, if a name or index is given, that
    template will print to the console.

    Parameters
    ----------
    sim : str | int, optional
        Simulation template file name or index. The default is ``None``.

    Returns
    -------
    None.

    """

    from bmlite import _templates

    _templates(__file__, 'SPM', sim)
